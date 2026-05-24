from flask import Blueprint, request, session, jsonify, flash, redirect, url_for, render_template
from app.models.usuario_model import UsuarioModel
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__)

def verificar_permissao(papeis_permitidos):
    papel_usuario = session.get('papel')
    return papel_usuario in papeis_permitidos

@admin_bp.route('/admin/cadastrar-admin', methods=['GET'])
def cadastrar_admin_view():
    if not verificar_permissao(['ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.admin_dashboard'))
    return render_template('admin/cadastrar_usuario.html', papel_alvo='Administrador')

@admin_bp.route('/admin/cadastrar-admin', methods=['POST'])
def cadastrar_admin():
    if not verificar_permissao(['ADMIN_INICIAL']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.admin_dashboard'))
    
    data = request.form
    senha_hash = generate_password_hash(data.get('senha'))
    novo_admin = UsuarioModel(nome=data.get('nome'), email=data.get('email'), senha_hash=senha_hash, papel='ADMIN')
    novo_admin.salvar()
    
    flash('Administrador cadastrado com sucesso', 'success')
    return redirect(url_for('livro.admin_dashboard'))

@admin_bp.route('/admin/cadastrar-bibliotecario', methods=['GET'])
def cadastrar_bibliotecario_view():
    if not verificar_permissao(['ADMIN_INICIAL', 'ADMIN']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.admin_dashboard'))
    return render_template('admin/cadastrar_usuario.html', papel_alvo='Bibliotecário')

@admin_bp.route('/admin/cadastrar-bibliotecario', methods=['POST'])
def cadastrar_bibliotecario():
    if not verificar_permissao(['ADMIN_INICIAL', 'ADMIN']):
        flash('Acesso negado', 'danger')
        return redirect(url_for('livro.admin_dashboard'))
    
    data = request.form
    senha_hash = generate_password_hash(data.get('senha'))
    novo_biblio = UsuarioModel(nome=data.get('nome'), email=data.get('email'), senha_hash=senha_hash, papel='BIBLIOTECARIO')
    novo_biblio.salvar()
    
    flash('Bibliotecário cadastrado com sucesso', 'success')
    return redirect(url_for('livro.admin_dashboard'))
