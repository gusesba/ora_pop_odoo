# Requisitos do Sistema — Ora Pop / Odoo

## 1. Estoque e Localizações

- **EST-01** — Controlar estoque de **3 sedes** com saldo independente.
- **EST-02** — Controlar **1 depósito de reposição**.
- **EST-03** — Controlar a área de estoque de embalagens abertas na cozinha.
- **EST-04** — Prever uma futura área de porcionamento em endereço diferente da cozinha.
- **EST-05** — Permitir múltiplas localizações internas e operacionais.
- **EST-06** — Registrar transferências entre sedes/localizações.
- **EST-07** — Permitir fluxo de transferência com solicitação, separação, transporte e confirmação de recebimento.
- **EST-08** — Controlar **estoque em trânsito**.
- **EST-09** — Permitir controle de produtos levados para feiras.
- **EST-10** — Manter histórico das movimentações de estoque.
- **EST-11** — Permitir inventários periódicos/cíclicos.
- **EST-12** — Permitir ajustes de inventário com rastreabilidade.

## 2. Produtos, Lotes e Validade

- **LOT-01** — Controlar produtos por lote quando aplicável.
- **LOT-02** — Registrar lote e validade informados pelo fornecedor.
- **LOT-03** — Permitir que a empresa gere lotes próprios para produtos fracionados e de fabricação própria.
- **LOT-04** — Permitir receber o mesmo produto, na mesma compra, com **lotes e validades diferentes**.
- **LOT-05** — Controlar a validade individualmente por lote.
- **LOT-06** — Manter rastreabilidade entre produto fracionado e lote de origem.
- **LOT-07** — Manter no produto fracionado a mesma validade do lote de origem.
- **LOT-08** — Priorizar futuramente a saída do lote com vencimento mais próximo.
- **LOT-09** — Permitir estratégia de separação do tipo **FEFO**, caso confirmada como regra definitiva.
- **LOT-10** — Permitir alertas de vencimento configuráveis por produto.
- **LOT-11** — Considerar como regra inicial um primeiro alerta quando restarem aproximadamente **30% da validade total**.
- **LOT-12** — Considerar como regra inicial um segundo alerta quando restarem aproximadamente **15% da validade total**.
- **LOT-13** — Permitir descontos progressivos para produtos próximos do vencimento.
- **LOT-14** — Impedir a venda de produtos/lotes vencidos.
- **LOT-15** — Permitir registrar descarte de produtos vencidos.

## 3. Fracionamento e Porcionamento

- **FRA-01** — Permitir abrir uma embalagem maior e fracioná-la em quantidades menores.
- **FRA-02** — Permitir destinar as frações para venda, armazenamento, produção ou transferência.
- **FRA-03** — Manter a rastreabilidade do produto fracionado até o lote de origem.
- **FRA-04** — Preservar a validade original durante o fracionamento.
- **FRA-05** — Permitir trabalhar com produtos fracionados usando o mesmo SKU ou outro SKU, conforme decisão final.
- **FRA-06** — Suportar diferentes unidades de medida, como unidade, pacote, caixa, kg, g e litro.
- **FRA-07** — Permitir controle de produtos por peso.
- **FRA-08** — Permitir conversões entre unidades de medida quando aplicável.
- **FRA-09** — Registrar perdas de peso/quantidade durante o fracionamento.
- **FRA-10** — Permitir parametrizar uma faixa de perda esperada.
- **FRA-11** — Permitir revisão periódica das faixas de perda, atualmente prevista a cada **4 a 6 meses**.
- **FRA-12** — Considerar custos adicionais de fracionamento, incluindo mão de obra, espaço, embalagem, etiquetas e impressão.
- **FRA-13** — Permitir que o produto fracionado tenha preço proporcionalmente superior ao produto fechado.
- **FRA-14** — Permitir aplicação de coeficiente de acréscimo para quantidades fracionadas que não correspondam a múltiplos da embalagem original.

## 4. Balança, Etiquetas e Código de Barras

- **BAL-01** — Integrar a operação com balança/etiquetadora.
- **BAL-02** — Avaliar a compatibilidade da balança antes da compra do equipamento.
- **BAL-03** — Suportar códigos de barras com peso, quantidade e/ou preço variável.
- **BAL-04** — Permitir leitura no PDV de etiquetas geradas pela balança.
- **ETQ-01** — Gerar etiqueta para produto fracionado.
- **ETQ-02** — A etiqueta deve poder conter:
  - nome do produto;
  - ingredientes em ordem de peso;
  - tabela nutricional básica;
  - validade;
  - observações;
  - instruções de armazenagem;
  - instruções após abertura;
  - peso/quantidade;
  - código de barras.
- **ETQ-03** — Permitir personalização do layout da etiqueta.

## 5. Produção / Fabricação

- **PRD-01** — Cadastrar receitas/composições dos produtos de fabricação própria.
- **PRD-02** — Controlar os ingredientes utilizados na produção.
- **PRD-03** — Consumir os ingredientes do estoque/localização correta.
- **PRD-04** — Dar entrada no estoque do produto acabado após a produção.
- **PRD-05** — Permitir que ingredientes sejam vendidos ou enviados para produção.
- **PRD-06** — Registrar movimentação de ingredientes da loja para a cozinha.
- **PRD-07** — Preservar lote, validade e quantidade durante essas movimentações.
- **PRD-08** — Permitir rastrear, futuramente, quais lotes de ingredientes foram utilizados em cada lote produzido.
- **PRD-09** — Registrar rendimento esperado.
- **PRD-10** — Registrar perdas de produção.
- **PRD-11** — Permitir revisão periódica das faixas de rendimento/perda.

## 6. Horta Própria

- **HOR-01** — Permitir entrada em estoque de ingredientes provenientes da horta própria.
- **HOR-02** — Permitir uso desses ingredientes na produção.
- **HOR-03** — Permitir venda direta desses produtos futuramente.
- **HOR-04** — Permitir definição de regra de custo/valoração.
- **HOR-05** — Permitir controle por lote quando aplicável.

## 7. Compras e Recebimento

- **COM-01** — Cadastrar e gerenciar fornecedores.
- **COM-02** — Suportar o fluxo de cotação/orçamento.
- **COM-03** — Registrar pedido de compra formal.
- **COM-04** — Permitir confirmação da compra após retorno do fornecedor.
- **COM-05** — Registrar recebimento e conferência da mercadoria.
- **COM-06** — Permitir futuramente uma área específica de recebimento antes da distribuição aos estoques.
- **COM-07** — Permitir receber o mesmo produto com múltiplos lotes e validades.
- **COM-08** — Permitir posterior distribuição do recebimento entre sedes/localizações.

## 8. Reposição de Estoque

- **REP-01** — Permitir definição de estoque mínimo por produto.
- **REP-02** — Permitir pontos de reposição por produto e localização.
- **REP-03** — Emitir alertas de necessidade de reposição.
- **REP-04** — Permitir futuramente reposição automática ou sugerida.

## 9. Vendas e Canais

- **VEN-01** — Atender vendas em loja física.
- **VEN-02** — Atender pedidos de e-commerce.
- **VEN-03** — Atender vendas B2B/atacado.
- **VEN-04** — Permitir operação com representantes, se necessário.
- **VEN-05** — Trabalhar inicialmente com uma tabela de preço única.
- **VEN-06** — Permitir futuramente tabelas ou regras de preço por canal, cliente ou condição comercial.
- **VEN-07** — Diferenciar o fluxo fiscal B2B do varejo quando necessário.

## 10. PDV

- **PDV-01** — Substituir o sistema de PDV atual.
- **PDV-02** — Integrar o PDV ao estoque.
- **PDV-03** — Integrar o PDV ao controle de lotes e validade.
- **PDV-04** — Integrar o PDV a códigos de barras.
- **PDV-05** — Integrar o PDV a preços e descontos.
- **PDV-06** — Integrar o PDV aos meios de pagamento.
- **PDV-07** — Integrar o PDV à emissão fiscal.
- **PDV-08** — Impedir a venda de lote vencido.
- **PDV-09** — Interpretar códigos de barras de produtos vendidos por peso/preço variável.
- **PDV-10** — Aplicar corretamente as regras de desconto por proximidade do vencimento.

## 11. Autoatendimento / Totem

- **TOT-01** — Prever futuro mini totem de autoatendimento.
- **TOT-02** — Permitir seleção de produtos pelo cliente.
- **TOT-03** — Permitir pagamento no autoatendimento.
- **TOT-04** — Integrar as vendas do totem ao estoque.
- **TOT-05** — Permitir emissão de cupom/documento fiscal.
- **TOT-06** — Avaliar equipamentos e meios de pagamento compatíveis.
- **TOT-07** — Definir comportamento em caso de indisponibilidade ou falha de conectividade.

## 12. E-commerce e Integrações

- **INT-01** — Integrar a loja virtual ao ERP.
- **INT-02** — Avaliar integração com Bling ou solução similar.
- **INT-03** — Definir qual sistema será a fonte principal de produtos.
- **INT-04** — Definir qual sistema será a fonte principal de preços.
- **INT-05** — Definir qual sistema será a fonte principal de estoque.
- **INT-06** — Definir qual sistema será a fonte principal de pedidos.
- **INT-07** — Definir qual sistema será a fonte principal de clientes.
- **INT-08** — Avaliar se o Bling continuará necessário após a implantação do Odoo.

## 13. Fiscal

- **FIS-01** — Substituir o NATO System.
- **FIS-02** — Atender os requisitos fiscais brasileiros aplicáveis à empresa.
- **FIS-03** — Emitir notas fiscais.
- **FIS-04** — Emitir cupons/documentos fiscais do varejo.
- **FIS-05** — Avaliar suporte a NF-e.
- **FIS-06** — Avaliar suporte a NFC-e.
- **FIS-07** — Integrar o fiscal ao PDV.
- **FIS-08** — Integrar o fiscal às vendas B2B.
- **FIS-09** — Integrar o fiscal ao financeiro.

## 14. Financeiro

- **FIN-01** — Controlar contas a pagar.
- **FIN-02** — Controlar contas a receber.
- **FIN-03** — Avaliar conciliação bancária.
- **FIN-04** — Avaliar fluxo de caixa.
- **FIN-05** — Controlar formas de pagamento.
- **FIN-06** — Avaliar integração bancária.
- **FIN-07** — Avaliar cartões.
- **FIN-08** — Avaliar PIX.
- **FIN-09** — Avaliar parcelamentos.
- **FIN-10** — Avaliar centros de custo.
- **FIN-11** — Disponibilizar relatórios financeiros.

## 15. Contabilidade

- **CTB-01** — Disponibilizar ao contador os dados necessários da operação.
- **CTB-02** — Avaliar acesso direto do contador.
- **CTB-03** — Permitir exportações quando necessário.
- **CTB-04** — Disponibilizar documentos fiscais.
- **CTB-05** — Disponibilizar relatórios contábeis/fiscais.
- **CTB-06** — Avaliar integrações com sistemas utilizados pela contabilidade.

## 16. Usuários e Permissões

- **USR-01** — Suportar inicialmente **8 usuários**.
- **USR-02** — Considerar inicialmente **2 gerentes e 6 caixas**.
- **USR-03** — Definir permissões por perfil.
- **USR-04** — Controlar permissões de visualização.
- **USR-05** — Controlar permissões de edição.
- **USR-06** — Controlar permissões de cancelamento.
- **USR-07** — Controlar permissões de autorização/aprovação.
- **USR-08** — Restringir acesso a estoque, financeiro, fiscal, produção e configurações conforme o perfil.
- **USR-09** — Os gerentes serão inicialmente os usuários-chave para homologação.

## 17. Equipamentos

- **EQP-01** — Suportar computadores convencionais.
- **EQP-02** — Suportar leitores de código de barras.
- **EQP-03** — Suportar impressoras.
- **EQP-04** — Suportar impressoras/etiquetadoras.
- **EQP-05** — Suportar balança etiquetadora.
- **EQP-06** — Prever equipamento para o futuro totem de autoatendimento.
- **EQP-07** — Prever equipamentos/terminais de pagamento.
- **EQP-08** — Validar compatibilidade dos equipamentos antes da compra.

## 18. Backup, Infraestrutura e Continuidade

- **INF-01** — Possuir rotina de backup.
- **INF-02** — Permitir restauração dos backups.
- **INF-03** — Definir política de retenção.
- **INF-04** — Definir frequência de backup.
- **INF-05** — Definir tolerância aceitável à perda de dados.
- **INF-06** — Definir tolerância aceitável à indisponibilidade.
- **INF-07** — Possuir monitoramento da aplicação e infraestrutura.
- **INF-08** — Definir processo de atualização.
- **INF-09** — Definir medidas de segurança.
- **INF-10** — Definir procedimento de recuperação em caso de falha.

## 19. Relatórios e Gestão

O sistema deverá permitir, diretamente ou por relatórios a definir:

- **REL-01** — Saldo por sede/localização.
- **REL-02** — Saldo por lote.
- **REL-03** — Produtos próximos do vencimento.
- **REL-04** — Produtos vencidos e descartados.
- **REL-05** — Perdas de fracionamento.
- **REL-06** — Perdas de produção.
- **REL-07** — Transferências entre estoques.
- **REL-08** — Inventários e divergências.
- **REL-09** — Produção.
- **REL-10** — Rendimento.
- **REL-11** — Margem.
- **REL-12** — Vendas.
- **REL-13** — Compras.
- **REL-14** — Financeiro.

## 20. Requisitos de Implantação e Homologação

- **IMP-01** — Utilizar uma base de testes antes da entrada em produção.
- **IMP-02** — Dividir o projeto em fases quando necessário.
- **IMP-03** — Priorizar no primeiro go-live os processos essenciais da operação.
- **IMP-04** — Permitir evolução posterior sem necessidade de reconstrução da solução.
- **IMP-05** — Os usuários-chave devem homologar os principais fluxos.
- **IMP-06** — Validar cenários reais antes do go-live.

### Cenários mínimos para homologação

1. Recebimento do mesmo produto com múltiplos lotes e validades.
2. Transferência entre sedes.
3. Estoque em trânsito.
4. Operação de feira.
5. Fracionamento de produto.
6. Registro de perda no fracionamento.
7. Geração e leitura de etiqueta por peso.
8. Impressão de etiqueta alimentar.
9. Aplicação de desconto por proximidade do vencimento.
10. Bloqueio de lote vencido no PDV.
11. Produção própria.
12. Consumo de ingredientes por lote.
13. Rastreabilidade de produto produzido.
14. Compra e recebimento.
15. Reposição de estoque.
16. Venda no PDV.
17. Emissão fiscal.
18. Inventário.

## 21. Decisões Ainda em Aberto

- **ABR-01** — Produto fracionado mantém o mesmo SKU ou recebe novo SKU.
- **ABR-02** — Unidade-base de estoque para produtos por peso.
- **ABR-03** — Uso de kg/g diretamente ou quantidade proporcional.
- **ABR-04** — Modelo da balança/etiquetadora.
- **ABR-05** — Padrão definitivo do código de barras.
- **ABR-06** — Fórmula do coeficiente de acréscimo do produto fracionado.
- **ABR-07** — Percentuais de desconto por proximidade do vencimento.
- **ABR-08** — Estrutura final de armazéns e localizações.
- **ABR-09** — Política/frequência de inventário.
- **ABR-10** — Estoques mínimos e pontos de reposição.
- **ABR-11** — Política detalhada de perdas.
- **ABR-12** — Regra de custo/valoração dos produtos da horta.
- **ABR-13** — Plataforma definitiva de e-commerce.
- **ABR-14** — Permanência ou não do Bling.
- **ABR-15** — Escopo fiscal definitivo.
- **ABR-16** — Escopo financeiro definitivo.
- **ABR-17** — Política de backup e continuidade.
- **ABR-18** — Escopo e prioridade do futuro totem de autoatendimento.

## 22. Diretrizes Técnicas

- Priorizar **configuração de módulos padrão do Odoo** antes de desenvolver código próprio.
- Reutilizar módulos maduros da comunidade/OCA quando forem adequados.
- Quando necessário, criar módulos de extensão por herança sobre módulos padrão/OCA.
- Evitar alterações diretas no código-fonte dos módulos padrão ou da OCA.
- Criar módulos próprios apenas para regras específicas que não sejam adequadamente atendidas pelas camadas anteriores.
- Manter customizações desacopladas para facilitar manutenção e atualização.
- Avaliar Community e Enterprise conforme aderência funcional e custo total do projeto.
- Dar preferência a soluções que reduzam dependência de fornecedor específico.

### Possíveis extensões/módulos próprios já identificados

- controle avançado de validade e descontos;
- bloqueio de venda de lote vencido;
- fluxo simplificado de fracionamento;
- regras específicas de custo/preço do fracionamento;
- etiquetas alimentares;
- integração direta com balança, somente se necessária;
- integrações específicas com terceiros, quando não houver solução adequada existente.
