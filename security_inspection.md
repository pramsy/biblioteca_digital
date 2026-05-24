# Relatório de Inspeção de Cibersegurança - BIBLIOTECA_DIGITAL

Este documento apresenta os resultados de uma inspeção profunda de segurança realizada no projeto BIBLIOTECA_DIGITAL, baseada nas melhores práticas de desenvolvimento seguro e no OWASP Top 10.

## Resumo Executivo

A inspeção identificou vulnerabilidades significativas que podem comprometer a integridade dos dados e a segurança dos usuários. A falta de proteção contra CSRF e o uso de algoritmos de hash fracos para senhas são os pontos mais críticos.

### Contagem de Achados por Severidade
- **Crítica**: 1
- **Alta**: 1
- **Média**: 3
- **Baixa**: 1

### As 5 Ações Mais Urgentes
1. Implementar proteção contra CSRF (Cross-Site Request Forgery) em todas as rotas de submissão de dados.
2. Substituir o hash SHA-256 simples por um algoritmo robusto com salt (ex: Bcrypt ou Argon2).
3. Desativar o `DEBUG_MODE` em ambiente de produção e configurar uma `SECRET_KEY` forte.
4. Adicionar cabeçalhos de segurança HTTP (HSTS, X-Frame-Options, CSP).
5. Implementar requisitos de complexidade de senha e proteção contra força bruta (rate limiting).

---

## Detalhamento das Vulnerabilidades

### 1. Ausência de Proteção contra CSRF (Cross-Site Request Forgery)
- **Localização**: Global (`app/__init__.py`, formulários em `templates/`, controladores em `controllers/`)
- **Descrição**: O sistema não utiliza tokens CSRF em seus formulários. Um atacante pode induzir um usuário autenticado a realizar ações indesejadas (como deletar livros ou solicitar empréstimos) sem o seu conhecimento.
- **Evidência**:
  ```html
  <!-- Em login.html -->
  <form action="{{ url_for('auth.login') }}" method="POST" ...>
    <!-- Falta o token CSRF -->
  ```
- **Impacto**: Alta. Permite a execução de transações não autorizadas em nome do usuário.
- **Nível de Severidade**: **Crítica**
- **Recomendação**: Utilizar a extensão `Flask-WTF` e adicionar `{{ form.csrf_token }}` em todos os formulários.
- **Referências**: OWASP A01:2021-Broken Access Control, CWE-352.

### 2. Armazenamento Inseguro de Senhas (Hash Sem Salt)
- **Localização**: `app/controllers/auth_controller.py`, `app/database.py`
- **Descrição**: O sistema utiliza SHA-256 simples para armazenar hashes de senhas. Sem o uso de um "salt" e um fator de custo, as senhas estão vulneráveis a ataques de dicionário e Rainbow Tables.
- **Evidência**:
  ```python
  hashlib.sha256(senha.encode()).hexdigest()
  ```
- **Impacto**: Alta. Em caso de vazamento do banco de dados, as senhas dos usuários podem ser facilmente recuperadas.
- **Nível de Severidade**: **Alta**
- **Recomendação**: Utilizar `werkzeug.security.generate_password_hash` e `check_password_hash` que utilizam PBKDF2 com salt por padrão.
- **Referências**: OWASP A02:2021-Cryptographic Failures, CWE-916.

### 3. Modo de Depuração (Debug Mode) Ativado por Padrão
- **Localização**: `config.py`, `run.py`
- **Descrição**: O sistema é configurado com `DEBUG_MODE=True` por padrão. Isso expõe informações sensíveis do sistema e permite execução de código em caso de erros não tratados.
- **Evidência**:
  ```python
  DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"
  ```
- **Impacto**: Média. Exposição de stack traces e variáveis de ambiente.
- **Nível de Severidade**: **Média**
- **Recomendação**: Garantir que `DEBUG_MODE` seja `False` em produção e nunca usar o servidor de desenvolvimento do Flask para produção.
- **Referências**: OWASP A05:2021-Security Misconfiguration, CWE-489.

### 4. Chave Secreta Padrão e Fraca
- **Localização**: `config.py`
- **Descrição**: A `SECRET_KEY` possui um valor padrão `"default_secret_key"`. Se o arquivo `.env` não estiver presente ou configurado, o sistema utilizará uma chave conhecida.
- **Evidência**:
  ```python
  SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
  ```
- **Impacto**: Média. Permite a falsificação de cookies de sessão.
- **Nível de Severidade**: **Média**
- **Recomendação**: Forçar o encerramento do sistema se a `SECRET_KEY` não for configurada com um valor seguro.
- **Referências**: OWASP A05:2021-Security Misconfiguration, CWE-522.

### 5. Falta de Cabeçalhos de Segurança HTTP
- **Localização**: `app/__init__.py`
- **Descrição**: A aplicação não configura cabeçalhos como `Content-Security-Policy`, `X-Frame-Options` ou `Strict-Transport-Security`.
- **Impacto**: Média. Aumenta a superfície de ataque para Clickjacking e ataques de injeção de script.
- **Nível de Severidade**: **Média**
- **Recomendação**: Utilizar a extensão `Flask-Talisman` para configurar cabeçalhos de segurança automaticamente.
- **Referências**: OWASP A05:2021-Security Misconfiguration.

### 6. Armazenamento de Credenciais Administrativas em Texto Simples no .env
- **Localização**: `.env`
- **Descrição**: A senha do administrador inicial está armazenada no arquivo `.env`.
- **Evidência**:
  ```text
  PROPRIETARIO_PASSWORD=senha_segura
  ```
- **Impacto**: Baixa. Se o acesso ao servidor for comprometido, a senha do admin é exposta (embora o hash no banco seja o principal alvo).
- **Nível de Severidade**: **Baixa**
- **Recomendação**: Utilizar um sistema de gerenciamento de segredos (como AWS Secrets Manager ou HashiCorp Vault) ou deletar a variável após a primeira inicialização.
- **Referências**: CWE-522.
