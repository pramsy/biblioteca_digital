# Plano de Testes de Frontend - Sistema de Biblioteca Digital

Este documento detalha os cenários de testes focados na experiência do usuário, interface e integração frontend.

## 1. Testes de Componentes e Interface (UI)

| ID | Cenário | Requisito | Técnica |
|:---|:---|:---|:---|
| UI-01 | Responsividade do Catálogo | Verificar se a grade de livros se ajusta de 1 a 4 colunas conforme o dispositivo. | Manual/Simulador |
| UI-02 | Acessibilidade Navbar | Validar navegação por teclado (TAB) e leitura de labels por Screen Readers. | Lighthouse/Axe |
| UI-03 | Estados de Botões | Garantir que botões exibem spinner e ficam desabilitados ao clicar. | E2E |
| UI-04 | Feedback de Flash | Validar se alertas desaparecem após 5 segundos ou ao clicar no fechar. | Unidade/JS |

## 2. Testes de Fluxo e Integração

| ID | Cenário | Requisito | Técnica |
|:---|:---|:---|:---|
| INT-01 | Validação de Formulário | Impedir submissão com campos vazios e mostrar erro visual. | E2E |
| INT-02 | Renderização Condicional | Garantir que botões de Admin NÃO aparecem para usuários Leitor. | Integração |
| INT-03 | Empty States | Simular banco vazio e verificar exibição da mensagem "Nenhum livro encontrado". | Mock |
| INT-04 | Skeleton/Loading | Verificar se o indicador de loading aparece durante a busca no catálogo. | Manual |

## 3. Testes de Regressão Visual e Usabilidade

| ID | Cenário | Requisito | Técnica |
|:---|:---|:---|:---|
| VIS-01 | Consistência de Design | Comparar cores, fontes e espaçamentos com o Design System definido. | Manual |
| USA-01 | Fluxo de Login | Medir facilidade de recuperação de senha e clareza nas mensagens de erro. | Teste com Usuário |

## 4. Testes de Acessibilidade (Mandatórios)

- **Contraste de Cor**: Validar todas as cores de texto contra o fundo (Min 4.5:1).
- **Navegação por Teclado**: O foco deve seguir uma ordem lógica e ser sempre visível.
- **Atributos ARIA**: Verificar `aria-live` em notificações e `aria-expanded` em menus.

## 5. Ferramentas e Execução

- **Lighthouse**: Para auditoria de performance, SEO e acessibilidade.
- **Playwright/Cypress**: Para testes E2E (Opcional se integrado).
- **Manual Checklist**: Para validações de "sentir" e usabilidade fina.
