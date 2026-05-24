from flask import Blueprint, request, session, jsonify, flash, redirect, url_for, render_template
from app.models.emprestimo_model import EmprestimoModel
from app.models.livro_model import LivroModel
from app.database import conectar_db

emprestimo_bp = Blueprint('emprestimo', __name__)

def verificar_permissao(papeis_permitidos):
    papel_usuario = session.get('papel')
    return papel_usuario in papeis_permitidos

@emprestimo_bp.route('/emprestimo/solicitar', methods=['POST'])
def solicitar_emprestimo():
    if not verificar_permissao(['LEITOR']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.listar_livros'))
    
    data = request.form
    livro_id = data.get('livro_id')
    usuario_id = session.get('user_id')
    
    conn = conectar_db()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM Livros WHERE id = ?', (livro_id,))
        livro = cursor.fetchone()
        
        if livro and livro['status'] == 'DISPONIVEL':
            novo_emprestimo = EmprestimoModel(livro_id=livro_id, usuario_id=usuario_id)
            novo_emprestimo.registrar_emprestimo()
            # ATUALIZAR livro_model para 'REQUISITADO'
            cursor.execute('UPDATE Livros SET status = "REQUISITADO" WHERE id = ?', (livro_id,))
            conn.commit()
            flash('Solicitação enviada com sucesso!', 'success')
        else:
            flash('Livro não disponível para solicitação', 'warning')
    finally:
        conn.close()
    
    return redirect(url_for('livro.listar_livros'))

@emprestimo_bp.route('/emprestimo/aprovar', methods=['POST'])
def aprovar_emprestimo():
    if not verificar_permissao(['BIBLIOTECARIO', 'ADMIN', 'ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.listar_livros'))
    
    data = request.form
    emprestimo_id = data.get('emprestimo_id')
    
    emprestimo = EmprestimoModel.buscar_por_id(emprestimo_id)
    if emprestimo and emprestimo.status == 'SOLICITADO':
        conn = conectar_db()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE Emprestimos SET status = "ATIVO" WHERE id = ?', (emprestimo_id,))
            cursor.execute('UPDATE Livros SET status = "EMPRESTADO" WHERE id = ?', (emprestimo.livro_id,))
            conn.commit()
            flash('Empréstimo aprovado!', 'success')
        finally:
            conn.close()
    else:
        flash('Solicitação não encontrada ou já processada', 'warning')
    
    return redirect(url_for('livro.admin_dashboard'))

@emprestimo_bp.route('/emprestimo/devolver', methods=['POST'])
def devolver_emprestimo():
    if not verificar_permissao(['BIBLIOTECARIO', 'ADMIN', 'ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.listar_livros'))
    
    data = request.form
    emprestimo_id = data.get('emprestimo_id')
    
    emprestimo = EmprestimoModel.buscar_por_id(emprestimo_id)
    if emprestimo and emprestimo.status == 'ATIVO':
        emprestimo.finalizar_emprestimo()
        conn = conectar_db()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE Livros SET status = "DISPONIVEL" WHERE id = ?', (emprestimo.livro_id,))
            conn.commit()
            flash('Livro devolvido com sucesso!', 'success')
        finally:
            conn.close()
    else:
        flash('Empréstimo não encontrado ou já devolvido', 'warning')
    
    return redirect(url_for('livro.admin_dashboard'))

@emprestimo_bp.route('/emprestimo/devolvidos', methods=['GET'])
def listar_devolvidos():
    if not verificar_permissao(['BIBLIOTECARIO', 'ADMIN', 'ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.listar_livros'))
    
    data_busca = request.args.get('data_devolucao')
    
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''
        SELECT E.id, L.titulo, U.nome as usuario, E.data_devolucao 
        FROM Emprestimos E
        JOIN Livros L ON E.livro_id = L.id
        JOIN Usuarios U ON E.usuario_id = U.id
        WHERE E.status = 'DEVOLVIDO'
    '''
    params = []
    if data_busca:
        query += " AND date(E.data_devolucao) = ?"
        params.append(data_busca)
    
    cursor.execute(query, params)
    devolvidos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return render_template('admin/devolvidos.html', devolvidos=devolvidos, data_busca=data_busca)

@emprestimo_bp.route('/emprestimo/excluir', methods=['POST'])
def excluir_emprestimo():
    if not verificar_permissao(['BIBLIOTECARIO', 'ADMIN', 'ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.listar_livros'))
    
    data = request.form
    emprestimo_id = data.get('emprestimo_id')
    
    emprestimo = EmprestimoModel.buscar_por_id(emprestimo_id)
    if emprestimo and emprestimo.status == 'SOLICITADO':
        conn = conectar_db()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE Livros SET status = "DISPONIVEL" WHERE id = ?', (emprestimo.livro_id,))
            cursor.execute('DELETE FROM Emprestimos WHERE id = ?', (emprestimo_id,))
            conn.commit()
            flash('Solicitação excluída com sucesso!', 'success')
        finally:
            conn.close()
    else:
        flash('Apenas solicitações pendentes podem ser excluídas', 'warning')
    
    return redirect(url_for('livro.admin_dashboard'))
