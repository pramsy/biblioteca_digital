# Sistema de Biblioteca Digital

Este é um sistema de gerenciamento de biblioteca digital desenvolvido com Flask e SQLite, seguindo uma arquitetura modular e práticas de TDD.

## 🚀Funcionalidade

Autenticação e Autorização: Controle de acesso baseado em papéis (Admin Inicial, Admin, Bibliotecário e Leitor).
Gestão de Livros: Catálogo completo com busca por título, autor e categoria.
Fluxo de Empréstimos: Ciclo completo de solicitação, aprovação e devolução de livros.
Relatórios: Métricas de uso do sistema para administradores.

## 📋 Requisitos tecnicos


## 🛠️ Tecnologias

- **Backend**: Flask 3.0, SQLite
- **Frontend**: Jinja2, Bootstrap 5, Vanilla JS
- **Testes**: Pytest

## 🔧 Instalação e Execução

1. **Dependências**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r biblioteca_digital/requirements.txt
   ```

2. **Configuração**:
   Copie o `.env.example` para `.env` e ajuste as variáveis.

3. **Execução**:
   ```bash
   cd biblioteca_digital
   python run.py
   ```

## 🧪 Testes Automatizados

Para garantir a integridade do sistema após as mudanças:
```bash
cd biblioteca_digital
PYTHONPATH=. pytest
```

## Estrutura

app/: Código fonte da aplicação.
controllers/: Gerenciamento de rotas e lógica de negócio.
models/: Definições de dados e persistência.
templates/: Interface do usuário (HTML/Jinja2).
tests/: Testes automatizados (TDD).
config.py: Configurações centralizadas.
run.py: Ponto de entrada.