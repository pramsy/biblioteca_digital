import pytest
from app.models.livro_model import LivroModel

def test_cadastrar_livro_sucesso(client, app):
    # Setup: Admin login
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['papel'] = 'ADMIN'

    from flask import url_for
    with app.app_context():
        url = url_for('livro.cadastrar_livro')

    response = client.post(url, data={
        'titulo': 'Livro Novo',
        'autor': 'Autor Novo',
        'categoria': 'Ficção'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Livro cadastrado com sucesso!' in response.get_data(as_text=True)
    
    with app.app_context():
        livros = LivroModel.buscar_todos()
        titulos = [l.titulo for l in livros]
        assert 'Livro Novo' in titulos

def test_buscar_livros(client, app):
    with app.app_context():
        l1 = LivroModel(titulo="Python para Todos", autor="Autor A", categoria="TI")
        l1.salvar()
        l2 = LivroModel(titulo="Java para Fortes", autor="Autor B", categoria="TI")
        l2.salvar()

    # Busca por título no /catalogo
    response = client.get('/catalogo?titulo=Python', follow_redirects=True)
    assert response.status_code == 200
    assert 'Python para Todos' in response.get_data(as_text=True)
    assert 'Java para Fortes' not in response.get_data(as_text=True)

def test_cadastrar_livro_permissao(client, app):
    # Testar permissão de cadastro (Apenas ADMIN/BIBLIOTECARIO)
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['papel'] = 'LEITOR'

    response = client.post('/livro/cadastrar', data={
        'titulo': 'Novo Livro',
        'autor': 'Autor',
        'categoria': 'Cat'
    }, follow_redirects=True)
    
    assert 'Acesso negado' in response.get_data(as_text=True)
