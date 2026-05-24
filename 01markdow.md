# Especificação Técnica do Frontend - Sistema de Biblioteca Digital

Este documento detalha exclusivamente as melhorias, refinamentos e padrões do frontend do Sistema de Biblioteca Digital.

## 1. Padrões de Design System (Baseado em Bootstrap 5)

---

### Identidade Visual e Consistência
* **Cores**:
  * Primária: `#0d6efd` (Bootstrap Primary) - Ações principais e botões.
  * Secundária: `#6c757d` - Ações secundárias.
  * Sucesso: `#198754` - Confirmações e status positivo.
  * Erro: `#dc3545` - Erros críticos e estados inválidos.
  * Aviso: `#ffc107` - Alertas preventivos.
* **Tipografia**: Sistema de fontes nativo (Sans-serif) para legibilidade em múltiplas plataformas.
* **Espaçamento**: Utilização estrita da escala de utilitários do Bootstrap (m-1 a m-5).

## 2. Componentes de Interface e Comportamento

---

### Layout Base (`layout.html`)
* **Descrição**: Estrutura global com navegação responsiva e suporte a acessibilidade.
* **Refinamentos**:
  * **Acessibilidade**: Adicionar `role="navigation"` na Navbar e `main` na área de conteúdo.
  * **Foco**: Garantir que o indicador de foco (`outline`) seja visível em todos os links e botões.
  * **Feedback de Carregamento**: Implementar uma barra de progresso no topo da página para mudanças de rota (Simulado via CSS/JS).

### Cards de Livros (`catalogo.html`)
* **Descrição**: Componente para exibição de livros no catálogo.
* **Comportamento Visual**:
  * **Hover**: Efeito de elevação leve (`box-shadow`) ao passar o mouse.
  * **Status**: Badges coloridas para 'Disponível' (Verde) e 'Emprestado' (Vermelho).
  * **Estados Vazios**: Mensagem amigável com ilustração ou ícone quando nenhum livro for encontrado.

### Formulários (`login.html`, `cadastro_leitor.html`)
* **Validações Visuais**:
  * Campos obrigatórios marcados com `*`.
  * Validação em tempo real (HTML5) com feedback visual do Bootstrap (`is-invalid`).
* **Mensagens de Erro**: Exibição clara de mensagens de erro específicas abaixo do campo afetado.
* **Feedback de Carregamento**: O botão de submissão deve entrar em estado `disabled` com um spinner (`spinner-border`) durante o processamento.

## 3. Estados de Tela e Fluxos

---

### Estados Globais
* **Loading**: Overlay semitransparente ou skeleton screens para carregamento de dados assíncronos (se aplicável).
* **Erro (Fallback)**: Página de erro genérica amigável para 404 e 500.
* **Empty State**: Mensagens como "Nenhum empréstimo registrado" ou "Nenhum livro disponível no momento".

### Responsividade (Breakpoints)
* **Mobile (< 576px)**: Navbar colapsável total, cards em coluna única, formulários ocupando 100% da largura.
* **Tablet (>= 768px)**: Cards em grade (2 ou 3 colunas), formulários centralizados com largura máxima.
* **Desktop (>= 992px)**: Layout completo, navegação horizontal, cards em grade (4 colunas).

## 4. Integração e Regras de Renderização

---

### Renderização Condicional
* **Admin/Bibliotecário**: Acesso visível a botões de edição, exclusão e geração de relatórios.
* **Leitor**: Visualização apenas de botões de solicitação de empréstimo.
* **Visitante**: Visualização do catálogo com botões de ação redirecionando para login.

### Acessibilidade (WCAG 2.1)
* **Contraste**: Garantir contraste mínimo de 4.5:1 para textos.
* **Labels**: Todos os inputs devem possuir `<label>` associado via `for/id`.
* **Aria Attributes**: Uso de `aria-label` em ícones e botões sem texto.

## 5. Variáveis de Ambiente e Configurações Frontend
* **UI_DEBUG_MODE**: Ativa guias visuais para depuração de layout.
* **MOCK_API**: Se `True`, utiliza dados estáticos para testes de interface.
