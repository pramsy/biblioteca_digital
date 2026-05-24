import pytest
from app.models.livro_model import LivroModel
from app.models.emprestimo_model import EmprestimoModel

def test_fluxo_emprestimo_completo(client, app):
    with app.app_context():
        # Setup: Livro e Leitor
        livro = LivroModel(titulo="Livro Teste", autor="Autor", categoria="Geral")
        livro.salvar()
        livro_id = livro.id

    # 1. Solicitação (LEITOR)
    with client.session_transaction() as sess:
        sess['user_id'] = 2 # Supondo ID 2 para o leitor
        sess['papel'] = 'LEITOR'

    # T-LOAN-01: Solicitação de Empréstimo
    response = client.post('/emprestimo/solicitar', data={'livro_id': livro_id}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Solicitação enviada com sucesso!' in response.get_data(as_text=True)

    # Verificar se o status mudou para SOLICITADO (o model faz isso no registrar_emprestimo)
    # Mas como estamos num banco em memória no fixture, precisamos checar o banco
    from app.database import conectar_db
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM Emprestimos WHERE livro_id = ?', (livro_id,))
    emp = cursor.fetchone()
    assert emp['status'] == 'SOLICITADO'
    conn.close()
