# Pontos Futuros e Melhorias — Ora Pop / Odoo

> **Tipo:** backlog de evolução e assuntos a validar, não compromisso de entrega no primeiro go-live.  
> **Documentos-base:** `requisitos_sistema_ora_pop_odoo.md` e `planejamento_modulos_odoo_ora_pop.md`.  
> **Premissa técnica atual:** Odoo 18 Community self-hosted + módulos OCA, com extensões próprias isoladas quando necessário.  
> **Atualizado em:** 14/11/2026.

## 1. Objetivo

Centralizar funcionalidades desejáveis, oportunidades de automação e decisões ainda não fechadas para avaliação em ciclos futuros. Este documento **não substitui** os requisitos e o planejamento existentes.

Os pontos são classificados como:

- **Já previsto:** consta nos `.md` originais, mesmo que tenha sido deixado para uma fase posterior.
- **Complemento proposto:** detalhamento novo ou funcionalidade ainda não especificada nos documentos-base; precisa de aprovação da Ora Pop.
- **A validar:** depende de decisão operacional, contábil/fiscal, de equipamento ou de prova de conceito (PoC).

**Regra de implantação:** uma melhoria pode entrar no primeiro go-live se for imprescindível ao fluxo operacional; estar neste arquivo não significa que deva ficar obrigatoriamente para depois.

---

## 2. Destaque — Entrada de mercadorias por XML de NF-e

**ID:** `FUT-001`  
**Área:** Compras, recebimento, estoque e financeiro/fiscal  
**Origem:** Complemento proposto aos requisitos `COM-01` a `COM-08`, `LOT-02` a `LOT-05`, `FIN-01` e bloco `FIS`  
**Prioridade sugerida:** **Alta**, com importação manual primeiro e automação SEFAZ depois  
**Status:** A detalhar, testar e aprovar

### 2.1. Objetivo

Permitir que a Ora Pop receba mercadorias de fornecedores a partir do **arquivo XML autorizado da NF-e**, reduzindo digitação manual e mantendo a ligação entre documento fiscal, conferência física, entradas de estoque e contas a pagar.

> **Distinção essencial:** importar o XML **não deve confirmar automaticamente o recebimento físico**. A nota declara o que foi faturado; o estoque deve refletir o que foi efetivamente recebido e conferido.

### 2.2. Fluxo operacional sugerido

```text
Fornecedor emite NF-e
       ↓
Upload do XML (primeira etapa)
       ↓
Validar documento / empresa destinatária / duplicidade
       ↓
Identificar fornecedor e mapear itens da nota para produtos internos
       ↓
Vincular ao pedido de compra, quando existente
       ↓
Criar recebimento PENDENTE (não movimenta estoque ainda)
       ↓
Conferir volumes, quantidades, unidades, lotes e validades
       ↓
Registrar divergências / recebimento parcial, se necessário
       ↓
Responsável confirma entrada na localização correta
       ↓
Movimentações de estoque com rastreabilidade
       ↓
Vincular/criar documento de fornecedor e contas a pagar
       ↓
Documento, estoque e financeiro conciliados e auditáveis
```

### 2.3. Requisitos funcionais propostos

| ID | Requisito | Prioridade sugerida |
|---|---|---|
| `NFE-IN-01` | Permitir upload manual do arquivo `.xml` de NF-e de fornecedor. | Alta |
| `NFE-IN-02` | Ler chave de acesso, número, série, emissão, emitente, destinatário, itens, quantidades, unidades, valores e informações fiscais disponíveis. | Alta |
| `NFE-IN-03` | Validar formato e integridade do XML, CNPJ destinatário, situação fiscal consultável e impedir processamento duplicado pela chave de acesso. | Alta |
| `NFE-IN-04` | Localizar/cadastrar fornecedor conforme regras de permissão e CNPJ, evitando duplicatas. | Alta |
| `NFE-IN-05` | Fazer **de/para** entre item/código do fornecedor e SKU interno, considerando CNPJ do fornecedor, `cProd`, GTIN quando houver e descrição; memorizar correspondências aprovadas. | Alta |
| `NFE-IN-06` | Permitir conferência e conversão de unidades de compra versus unidades de estoque (caixa, pacote, kg, g, L), sem conversões ambíguas. | Alta |
| `NFE-IN-07` | Relacionar a NF-e a pedido de compra existente ou tratar recebimento sem pedido segundo política definida. | Alta |
| `NFE-IN-08` | Criar ou preparar operação de recebimento **pendente** para conferência física antes de incrementar o estoque disponível. | Alta |
| `NFE-IN-09` | Registrar quantidade faturada x efetivamente recebida; aceitar divergências e entregas parciais, com motivo e responsável. | Alta |
| `NFE-IN-10` | Importar dados de lotes/fabricação/validade **quando presentes no XML** e permitir complementá-los durante a conferência. | Alta |
| `NFE-IN-11` | Aceitar vários lotes/validades do mesmo produto na mesma nota e validar soma das quantidades por lote. | Alta |
| `NFE-IN-12` | Confirmar entrada na sede/armazém/localização corretos, preservando vínculo com nota, fornecedor, lote e responsável. | Alta |
| `NFE-IN-13` | Associar/criar fatura de fornecedor e contas a pagar sem duplicar lançamentos; conferir parcelas, valores, tributos e vencimentos. | Média/Alta |
| `NFE-IN-14` | Guardar o XML e disponibilizar histórico, estado do processamento e trilha de auditoria. | Alta |
| `NFE-IN-15` | Tratar rejeições, documentos cancelados, devoluções e correções conforme fluxo fiscal autorizado; não apagar movimentos validados arbitrariamente. | Média/Alta |
| `NFE-IN-16` | Permitir captura de NF-e destinadas ao CNPJ por integração com serviços de distribuição de documentos fiscais, certificado e regras de manifestação aplicáveis. | Futura |
| `NFE-IN-17` | Opcionalmente receber XML por e-mail de fornecedores com fila de revisão e processamento. | Futura |
| `NFE-IN-18` | Mostrar um painel de notas novas, pendentes de identificação de produtos, aguardando conferência, divergentes e concluídas. | Média |

### 2.4. Observações importantes sobre o XML

- **NF-e XML não é DANFE/PDF:** o PDF auxilia a conferência visual, mas não substitui o arquivo estruturado.
- **Lote e validade não são garantidos:** podem aparecer nas informações de rastreabilidade do XML, mas muitos fornecedores não preenchem tudo. A conferência precisa permitir registro manual por lote.
- **Código do fornecedor difere do SKU interno:** manter um cadastro de equivalência por fornecedor; não criar produtos automaticamente sem validação.
- **Preço/custo do estoque não equivale necessariamente ao preço unitário da nota:** frete, descontos, tributos recuperáveis/não recuperáveis e valoração devem seguir configuração e orientação contábil.
- **Recebimento físico, escrituração fiscal e obrigação financeira possuem estados diferentes:** evitar que uma única ação os confirme de forma implícita.
- **Não assumir disponibilidade completa no Odoo Community/OCA:** validar a importação de XML e sua ligação com `stock`/`purchase`/`account` na versão exata implantada.

### 2.5. Estratégia técnica sugerida

| Camada | Módulos / abordagem | Observação |
|---|---|---|
| Compras | `purchase`, `purchase_stock` | Pedido e recebimento |
| Estoque e lotes | `stock` | Operações, lotes, validade e localizações |
| Financeiro | `account` | Fatura de fornecedor, vencimentos e pagamentos |
| Localização brasileira | OCA `l10n_br_purchase`, `l10n_br_nfe` e dependências necessárias | **Verificar** capacidades e compatibilidade na revisão selecionada |
| Adaptação Ora Pop | Possível addon `ora_pop_nfe_inbound` | Criar **somente** para lacunas de fluxo, de/para, validações ou integração que módulos existentes não cubram |
| Distribuição SEFAZ | Conector/serviço a avaliar | Depende de certificado, regras fiscais, limites e PoC |

**Não modificar módulos padrão/OCA diretamente.** Se houver necessidade, estender seus modelos e fluxos, preservando os movimentos e registros oficiais do Odoo.

### 2.6. Etapas de implementação propostas

1. **PoC:** importar um XML real de teste, vincular itens ao cadastro, criar recebimento pendente e lançar dois lotes do mesmo produto.
2. **MVP:** upload manual + validação básica + de/para + conferência + entrada em estoque + histórico do documento.
3. **Financeiro/fiscal:** vínculo com fatura de fornecedor, contas a pagar, tributos e tratamento de divergências, com homologação contábil.
4. **Automação:** captura SEFAZ, notificações, e-mail e fila de documentos pendentes.

### 2.7. Cenários mínimos para homologação

- [ ] XML válido de fornecedor já cadastrado e produtos conhecidos.
- [ ] Fornecedor ou produto ainda não mapeado: processo exige revisão, não gera item indevido.
- [ ] NF-e com duas linhas ou dois lotes do mesmo produto e validades diferentes.
- [ ] NF-e de 10 kg, entrega física de 9,5 kg: registrar divergência sem inflar estoque.
- [ ] Produto comprado em caixa e estocado em unidade ou kg: conversão conferida.
- [ ] Tentativa de importar novamente a mesma chave: não criar dupla entrada ou dívida.
- [ ] XML sem lote ou validade: permitir preenchimento manual quando obrigatório.
- [ ] Vincular pedido de compra e impedir recebimento inconsistente.
- [ ] Confirmar recebimento apenas na localização escolhida e rastrear o movimento.
- [ ] Conferir lançamentos financeiros e fiscais antes de efetivá-los.
- [ ] Simular devolução/cancelamento em procedimento homologado.

### 2.8. Decisões pendentes

- A Ora Pop quer permitir recebimentos sem pedido de compra prévio?
- Quem pode aprovar novos mapeamentos de produtos?
- Recebimento parcial pode liberar parcialmente o saldo ou exige aprovação de gerente?
- O financeiro lança a fatura ao importar a nota, após conferência ou em etapa própria?
- Qual é o fluxo adotado pelo contador para NF-e de entrada, devolução e cancelamento?
- Há necessidade de busca automática na SEFAZ já na primeira implantação?

---

## 3. Outros pontos futuros já previstos ou recomendados

A lista abaixo reúne **itens citados nos documentos-base como futuros, opcionais ou sujeitos a PoC**, além de alguns complementos claramente identificados. Ela **não altera as prioridades formais** do planejamento principal.

| ID | Ponto | Origem | Dependência / momento sugerido |
|---|---|---|---|
| `FUT-002` | Automatizar/sugerir reposição por estoque mínimo e localização. | Já previsto (`REP-01` a `REP-04`) | Após saldos e compras confiáveis. |
| `FUT-003` | Habilitar área física de porcionamento em outro endereço. | Já previsto (`EST-04`) | Quando a nova operação existir. |
| `FUT-004` | Aperfeiçoar transferência entre sedes com papéis, aprovações e confirmação por etapa. | Já previsto (`EST-07`) | Após fluxo padrão validado. |
| `FUT-005` | Alertas percentuais de validade (30% e 15%), descontos progressivos e controle rígido de vencidos no PDV. | Já previsto (`LOT-10` a `LOT-14`, `PDV-08` a `PDV-10`) | **Pode ser requisito de go-live**, conforme operação; addon de validade/POS. |
| `FUT-006` | Revisão periódica das faixas de perda de fracionamento/produção e versões de receitas. | Já previsto (`FRA-10`/`FRA-11`, `PRD-11`) | Após histórico de produção confiável. |
| `FUT-007` | Integração direta com balança/etiquetadora quando o fluxo por código de barras não for suficiente. | Já previsto (`BAL-01` a `BAL-04`, `EQP-05`) | Testar primeiro etiqueta EAN e hardware. |
| `FUT-008` | Venda direta de itens da horta e valoração detalhada da produção própria. | Já previsto (`HOR-03`/`HOR-04`) | Definir política de custo com contabilidade. |
| `FUT-009` | Tabelas de preço por canal, cliente, quantidade ou condição comercial; representantes. | Já previsto (`VEN-04`/`VEN-06`) | Após tabela inicial única. |
| `FUT-010` | Integração de e-commerce externo, eventual Bling e definição de fonte de verdade de produto/estoque/pedidos. | Já previsto (`INT-01` a `INT-08`) | Após arquitetura e plataforma de loja definidas. |
| `FUT-011` | Mini totem de autoatendimento, pagamento e documento fiscal. | Já previsto (`TOT-01` a `TOT-07`) | Depois de POS + fiscal estabilizados. |
| `FUT-012` | Conciliação bancária, integrações com bancos, PIX, cartões, TEF e relatórios financeiros avançados. | Já previsto (`FIN-03` a `FIN-11`) | Conforme provedores, orçamento e homologação. |
| `FUT-013` | Relatórios avançados de margem, rendimento, perdas e divergências de inventário. | Já previsto (`REL-01` a `REL-14`) | Após definição dos dados operacionais. |
| `FUT-014` | Integração ou exportação aprimorada para escritório contábil. | Já previsto (`CTB-01` a `CTB-06`) | Alinhar formato e sistema do contador. |
| `FUT-015` | Fluxos avançados de qualidade e bloqueio/liberação de lotes no recebimento. | Complemento proposto a compras/lotes; controle de qualidade é opcional no planejamento. | Avaliar necessidade sanitária e operação. |
| `FUT-016` | Painel de indicadores do processo de recebimento: tempo de conferência, fornecedores com divergência e custo real por compra. | Complemento proposto | Após `FUT-001` e dados históricos. |

---

## 4. Priorização preliminar

### Validar cedo, porque afeta a arquitetura

- `FUT-001` — entrada por XML: pelo menos uma PoC e o desenho de vínculo NF-e ↔ compra ↔ estoque ↔ financeiro.
- `FUT-005` — proibição de venda de vencidos e política de lote no PDV, caso exigidas desde o primeiro dia.
- `FUT-007` — definir padrão de código de barras e testar equipamento **antes da compra**.
- Fiscal brasileiro/NF-e/NFC-e: PoC de operação real permanece obrigatória, como já previsto no planejamento principal.

### Implementar após operação básica estável

- Automação completa de importação/consulta SEFAZ (`NFE-IN-16`), dashboards e recepção por e-mail (`NFE-IN-17`).
- Reposição sugerida/automática, relatórios gerenciais e revisões de perda.
- Conciliação e integrações financeiras conforme demanda.

### Evolução posterior

- Totem de autoatendimento.
- Integrações adicionais com canais externos.
- Novas instalações físicas e processos avançados de qualidade.

---

## 5. Critérios para promover um ponto ao escopo de desenvolvimento

Antes de aprovar qualquer item deste backlog:

1. Confirmar necessidade com as pessoas que executam a operação na Ora Pop.
2. Definir comportamento esperado e exemplos reais.
3. Verificar se já é coberto por configuração do Odoo, OCA ou módulo existente.
4. Testar a solução em homologação com dados representativos.
5. Registrar decisão **padrão / OCA / addon próprio / integração externa**.
6. Estimar esforço, dependências, segurança e custo de manutenção.
7. Obter aprovação e adicionar o item ao planejamento de execução, com testes de aceite.

## 6. Próximas decisões a registrar

| Ponto | Decisão a coletar | Responsável sugerido |
|---|---|---|
| Entrada por XML (`FUT-001`) | Escopo mínimo do recebimento e da automação | Gestores + equipe técnica |
| Escrita fiscal e financeira | Momento da contabilização, tratamento de divergências e devoluções | Contador + gestores |
| Mapeamento de produtos | Padrão de SKU, cadastro, unidades e aprovação de correspondências | Estoque/compras |
| Conectores | Módulos OCA e serviços disponíveis na versão escolhida | Equipe técnica |
| Prioridades | O que é bloqueador de go-live e o que pode ficar para depois | Gestores da Ora Pop |

---

> **Nota de escopo:** as seções 2.2 a 2.8 descrevem uma **proposta nova** para a entrada de NF-e por XML; não constavam integralmente nos arquivos originais. Antes de incorporar seus itens como requisitos confirmados, submetê-los à validação da Ora Pop e do contador.
