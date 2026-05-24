import pytest
from app import criar_app
from app.database import conectar_db, inicializar_db
import os

@pytest.fixture
def app():
    # Configuração para testes
    os.environ['DATABASE_PATH'] = ':memory:'
    os.environ['SECRET_KEY'] = 'test_secret'
    
    app = criar_app()
    app.config['WTF_CSRF_ENABLED'] = False 
    app.config['TESTING'] = True
    
    # Desativar HTTPS forçado do Talisman em testes
    for extension in app.extensions:
        if extension == 'talisman':
            app.extensions['talisman'].force_https = False
    
    # Garantir banco limpo
    with app.app_context():
        inicializar_db()
        
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
