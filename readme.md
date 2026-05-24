# Sistema de Biblioteca Digital - UAB IFTO

Sistema de gerenciamento de biblioteca digital focado em acessibilidade, responsividade e experiência do usuário.

## 🚀 Novidades da Versão (Refinamento Frontend)

Esta versão foca na modernização da interface e melhoria da acessibilidade:
- **Design System**: Padronização visual baseada em Bootstrap 5 com feedback tátil e visual.
- **Acessibilidade**: Conformidade básica com WCAG (ARIA roles, contraste, navegação por teclado).
- **Responsividade**: Layout adaptável para Mobile, Tablet e Desktop.
- **Validations & Feedback**: Estados de carregamento (spinners), validações em tempo real e mensagens claras.

## 📋 Documentação

A documentação detalhada foi subdividida para melhor manutenção:
- [Especificação de Requisitos e UI](01markdow.md)
- [Plano de Testes de Frontend](doc/testing.md)

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

## ♿ Acessibilidade

O sistema foi testado para garantir:
- Navegação lógica via tecla `TAB`.
- Indicações visuais de foco em todos os elementos interativos.
- Suporte a leitores de tela através de atributos ARIA.
