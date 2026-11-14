# Planejamento de Módulos Odoo — Ora Pop

> Base de referência: requisitos do arquivo `requisitos_sistema_ora_pop_odoo.md`.
>
> Premissa recomendada para este planejamento: **Odoo 18 Community self-hosted + módulos OCA**, com addons próprios isolados quando necessário.
>
> Motivo da versão: em novembro/2026, a própria OCA informa que a localização brasileira 19.0 é uma branch de transição e recomenda **18.0 para novos projetos brasileiros de maior complexidade**. A decisão final deve ser validada com a GrowScale antes do início da implementação.

---

## 1. Legenda de cobertura

| Status | Significado |
|---|---|
| ✅ **100% padrão** | O requisito pode ser atendido com módulo padrão + configuração, sem código próprio. |
| 🟢 **100% com OCA** | O requisito pode ser atendido sem addon próprio da Ora Pop, mas usando módulo da OCA/comunidade. |
| 🟡 **Parcial / extensão** | A base já existe, mas é necessário estender comportamento, modelo, tela ou regra. |
| 🔴 **Custom / integração** | Não foi identificado um módulo pronto que cubra suficientemente a regra; recomenda-se addon próprio ou integração. |
| ⚪ **Decisão / infraestrutura** | Não é principalmente um requisito resolvido por módulo Odoo; depende de decisão de negócio, equipamento ou infraestrutura. |

### Origem dos módulos

- **Odoo CE** — Odoo Community Edition / módulos padrão open source.
- **Odoo EE** — Odoo Enterprise Edition / módulo proprietário opcional.
- **OCA** — Odoo Community Association.
- **Ora Pop** — módulo próprio recomendado para o projeto.

---

# 2. Arquitetura de addons recomendada

```text
odoo/
├── addons/                         # Odoo Community
│
├── oca/
│   ├── l10n-brazil/
│   ├── stock-logistics-warehouse/
│   ├── stock-logistics-workflow/
│   ├── stock-logistics-barcode/
│   ├── stock-weighing/
│   ├── manufacture/
│   ├── product-attribute/
│   ├── account-payment/
│   └── account-financial-tools/
│
└── custom-addons/
    ├── ora_pop_expiration/
    ├── ora_pop_fractioning/
    ├── ora_pop_food_label/
    ├── ora_pop_pos/
    ├── ora_pop_scale/              # somente se necessário
    └── ora_pop_integration/        # somente quando houver integração específica
```

**Regra:** não alterar diretamente os fontes de `stock`, `mrp`, `point_of_sale` ou de módulos OCA.  
As adaptações devem ser feitas por dependência/herança em addons próprios.

---

# 3. Estoque e Localizações

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `stock` | Odoo CE | Armazéns, localizações, transferências, saldos, movimentos e inventário. |
| `stock_inventory` | OCA / `stock-logistics-warehouse` | Gestão mais estruturada dos inventários. Opcional. |
| `stock_cycle_count` | OCA / `stock-logistics-warehouse` | Regras avançadas de contagem cíclica. Opcional; o core já possui frequência de inventário por localização. |
| `stock_inventory_discrepancy` | OCA / `stock-logistics-warehouse` | Controle e bloqueio por divergência de inventário. |
| `stock_inventory_justification` | OCA / `stock-logistics-warehouse` | Justificativa de ajustes de inventário. |
| `stock_inventory_lockdown` | OCA / `stock-logistics-warehouse` | Bloqueio de localização durante contagem. Opcional. |
| `stock_no_negative` | OCA / `stock-logistics-workflow` | Impede saldo negativo. Recomendado. |

### Cobertura

| Requisito | Cobertura | Módulo / solução | Observação |
|---|---|---|---|
| EST-01 — 3 sedes com saldo independente | ✅ 100% padrão | `stock` | Configurar warehouses/localizações. |
| EST-02 — depósito de reposição | ✅ 100% padrão | `stock` | Warehouse ou localização, conforme desenho físico. |
| EST-03 — estoque de embalagens abertas na cozinha | ✅ 100% padrão | `stock` | Localização interna. |
| EST-04 — futura área de porcionamento | ✅ 100% padrão | `stock` | Warehouse/localização própria. |
| EST-05 — múltiplas localizações | ✅ 100% padrão | `stock` | Recurso nativo. |
| EST-06 — transferências entre sedes | ✅ 100% padrão | `stock` | Transferências internas/interwarehouse. |
| EST-07 — solicitação, separação, transporte e recebimento | 🟡 Parcial | `stock` + possível `ora_pop_stock` | O fluxo físico é suportado; caso seja necessário registrar explicitamente cada responsável/etapa e aprovações específicas, estender o picking. |
| EST-08 — estoque em trânsito | ✅ 100% padrão | `stock` | Criar localização de trânsito/rota entre warehouses. |
| EST-09 — produtos em feiras | ✅ 100% padrão | `stock` | Criar localização ou warehouse “Feira”. |
| EST-10 — histórico de movimentações | ✅ 100% padrão | `stock` | Movimentos e rastreabilidade. |
| EST-11 — inventários periódicos/cíclicos | ✅ 100% padrão | `stock` | Frequência pode ser definida por localização. OCA pode sofisticar. |
| EST-12 — ajustes com rastreabilidade | 🟢 100% com OCA | `stock` + `stock_inventory_justification` / `stock_inventory_discrepancy` | O core registra ajustes; OCA melhora justificativa e governança. |

### Desenvolvimento previsto

**Nenhum módulo próprio obrigatório inicialmente.**

Criar `ora_pop_stock` somente se o fluxo EST-07 exigir:
- aprovação formal;
- solicitante/separador/transportador/recebedor explícitos;
- estados adicionais;
- regras de permissão específicas.

---

# 4. Produtos, Lotes e Validade

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `stock` | Odoo CE | Lotes, rastreabilidade e movimentos. |
| recursos de Expiration Dates do Inventory | Odoo padrão | Validade, Best Before, Removal Date e Alert Date. |
| `stock_move_line_expiration_date_required` | OCA / `stock-logistics-workflow` | Obriga preenchimento da validade em movimentos configurados. |
| `stock_picking_auto_create_lot` | OCA / `stock-logistics-workflow` | Criação automática de lote em recebimentos. Opcional. |
| `product_lot_sequence` | OCA / `product-attribute` | Sequência de lotes por produto. |
| `stock_lock_lot` | OCA / `stock-logistics-workflow` | Bloqueio de lote. |
| `stock_lot_scrap` | OCA / `stock-logistics-workflow` | Descarte de todo o saldo de um lote. |
| `scrap_reason_code` | OCA / `stock-logistics-workflow` | Motivos de descarte. |
| `stock_scrap_security` | OCA / `stock-logistics-workflow` | Permissões específicas para descarte. |

### Cobertura

| Requisito | Cobertura | Módulo / solução | Observação |
|---|---|---|---|
| LOT-01 — controle por lote | ✅ 100% padrão | `stock` | Nativo. |
| LOT-02 — lote e validade do fornecedor | ✅ 100% padrão | `stock` | Informados no recebimento. |
| LOT-03 — lotes próprios para fracionados/fabricados | ✅ 100% padrão | `stock` + `mrp` | Pode ser manual ou automatizado. |
| LOT-04 — mesmo produto, vários lotes/validades no mesmo recebimento | ✅ 100% padrão | `stock` + `purchase_stock` | Nativo. |
| LOT-05 — validade por lote | ✅ 100% padrão | `stock` | Nativo. |
| LOT-06 — rastrear fracionado até lote origem | ✅ 100% se fracionamento for modelado via MRP | `stock` + `mrp` | A cadeia componente → produto acabado fica rastreável. |
| LOT-07 — copiar automaticamente validade do lote origem | 🟡 Parcial | `stock` + `mrp` + `ora_pop_fractioning` | A validade pode ser informada, mas a herança automática exata deve ser implementada. |
| LOT-08 — priorizar vencimento mais próximo | ✅ 100% padrão | FEFO / `stock` | Estratégia nativa. |
| LOT-09 — FEFO | ✅ 100% padrão | `stock` | Nativo. |
| LOT-10 — alerta configurável por produto | ✅ 100% padrão para prazo em dias | Expiration Dates | Core trabalha com dias antes/depois da validade. |
| LOT-11 — alerta em 30% da vida útil | 🟡 Parcial | `ora_pop_expiration` | Percentual da vida útil não é a regra padrão. |
| LOT-12 — alerta em 15% da vida útil | 🟡 Parcial | `ora_pop_expiration` | Mesma extensão. |
| LOT-13 — desconto progressivo conforme validade | 🔴 Custom | `ora_pop_expiration` + `point_of_sale` | Preço precisa considerar lote e estágio de validade. |
| LOT-14 — impedir venda de lote vencido | 🔴 Custom | `ora_pop_expiration` + `ora_pop_pos` | O POS padrão aceita lotes e não deve ser considerado suficiente para esse bloqueio rígido. |
| LOT-15 — descarte de vencidos | ✅ 100% padrão | `stock` Scrap | `stock_lot_scrap` e `scrap_reason_code` são melhorias recomendadas. |

### Desenvolvimento previsto

Criar **`ora_pop_expiration`**:
- percentual de vida útil restante;
- estágios de vencimento;
- desconto por estágio;
- bloqueio de lote vencido;
- integração com POS;
- opcionalmente sugestão automática de descarte.

---

# 5. Fracionamento e Porcionamento

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `mrp` | Odoo CE | Transformação/reembalagem como ordem de fabricação. |
| `stock` | Odoo CE | Movimentos, lote, validade, perdas. |
| UoM | Odoo padrão | kg, g, L, unidade etc. |
| `stock_weighing` | OCA / `stock-weighing` | Assistente de pesagem em operações de estoque. |
| `mrp_weighing` | OCA / `stock-weighing` | Pesagem ligada a operações de fabricação. |
| `stock_weighing_auto_create_lot` | OCA / `stock-weighing` | Cria lotes a partir da pesagem. |
| `stock_remote_measure` | OCA / `stock-weighing` | Captura medidas de dispositivo remoto. |
| `stock_weighing_remote_measure` | OCA / `stock-weighing` | Integra pesagem com medida remota. |
| `product_logistics_uom` | OCA / `product-attribute` | Unidades logísticas de peso/volume. |
| `product_net_weight` | OCA / `product-attribute` | Peso líquido. |
| `mrp_bom_location` | OCA / `manufacture` | Localização específica para componentes da BoM. |
| `mrp_bom_version` | OCA / `manufacture` | Versionamento de receitas/processos. |
| `mrp_bom_tracking` | OCA / `manufacture` | Histórico de alterações da BoM. |

### Cobertura

| Requisito | Cobertura | Módulo / solução | Observação |
|---|---|---|---|
| FRA-01 — abrir embalagem e gerar frações | 🟡 Parcial | `mrp` + `ora_pop_fractioning` | Pode ser modelado com MO, mas recomenda-se wizard simplificado. |
| FRA-02 — destinar frações para venda/estoque/produção/transferência | ✅ 100% padrão | `stock` + `mrp` | Após gerar estoque, destinos são padrão. |
| FRA-03 — rastreabilidade até lote origem | ✅ 100% padrão via MRP | `mrp` + `stock` | Consumir lote origem na MO e produzir novo lote. |
| FRA-04 — preservar validade automaticamente | 🟡 Parcial | `ora_pop_fractioning` | Copiar validade do lote de origem para o lote fracionado. |
| FRA-05 — mesmo SKU ou novo SKU | ⚪ Decisão | `stock` / `mrp` | Ambos são possíveis; recomenda-se validar regra fiscal/comercial. |
| FRA-06 — unidade, pacote, caixa, kg, g, L | ✅ 100% padrão | UoM | Desde que conversões sejam da mesma categoria de UoM. |
| FRA-07 — controle por peso | ✅ 100% padrão | produto com UoM kg/g | OCA `stock-weighing` é útil para operação de balança. |
| FRA-08 — conversões de UoM | ✅ 100% padrão dentro da mesma categoria | UoM | Não tratar “unidade ↔ kg” como conversão genérica sem modelagem. |
| FRA-09 — perdas de peso | ✅ 100% padrão | MRP Scrap | Registrar descarte/perda. |
| FRA-10 — faixa de perda esperada | 🟡 Parcial | `mrp` + `ora_pop_fractioning` | Core registra perda, não a política de faixa esperada da Ora Pop. |
| FRA-11 — histórico/revisão da faixa a cada 4–6 meses | 🟡 Parcial | `mrp_bom_version` + `ora_pop_fractioning` | OCA ajuda a versionar; regra/alerta específico exige extensão. |
| FRA-12 — custos de mão de obra, embalagem, etiqueta etc. | ✅ 100% padrão, se modelados | `mrp` | Componentes + operações + work centers permitem compor custo. |
| FRA-13 — preço proporcionalmente maior do fracionado | ✅ 100% padrão se for SKU distinto e preço definido | Pricelist/Product | Se preço depender dinamicamente do lote/processo, extensão. |
| FRA-14 — coeficiente para frações não múltiplas | 🔴 Custom | `ora_pop_fractioning` / `ora_pop_pos` | Regra específica da operação. |

### Desenvolvimento previsto

Criar **`ora_pop_fractioning`** como camada sobre `mrp` e `stock`.

Exemplo de interface:

```text
Produto origem: Queijo 1 kg
Lote origem: Q001
Validade: 20/12/2026
Quantidade disponível: 8,450 kg

Peso fracionado: 0,230 kg
Perda: 0,003 kg
Produto destino: Queijo fracionado

[Confirmar] [Imprimir etiqueta]
```

O addon deve gerar movimentos/MO padrão em vez de criar estoque paralelo.

---

# 6. Balança, Etiquetas e Código de Barras

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| nomenclatura de barcode do POS/core | Odoo CE | EAN com peso, preço, desconto, produto etc. |
| `point_of_sale` | Odoo CE | Leitura do barcode no caixa. |
| `stock_barcode` | Odoo EE | Aplicativo oficial de barcode para operações de armazém. **Não considerar como Community.** |
| `barcodes_generator_abstract` | OCA / `stock-logistics-barcode` | Infraestrutura de geração de barcodes. |
| `barcodes_generator_product` | OCA / `stock-logistics-barcode` | Geração de códigos EAN para produtos. |
| `product_multi_barcode` | OCA / `stock-logistics-barcode` | Múltiplos códigos por produto. |
| `stock_weighing` | OCA / `stock-weighing` | Pesagem. |
| `stock_remote_measure` | OCA / `stock-weighing` | Comunicação com dispositivos de medição. |

### Cobertura

| Requisito | Cobertura | Módulo / solução | Observação |
|---|---|---|---|
| BAL-01 — integração com balança/etiquetadora | 🟡 Parcial | OCA `stock-weighing` / barcode | Se a balança apenas imprime EAN com peso, integração direta pode nem ser necessária. |
| BAL-02 — avaliar compatibilidade | ⚪ Equipamento | — | Fazer PoC antes da compra. |
| BAL-03 — barcode com peso/preço variável | ✅ 100% padrão | barcode nomenclature | Odoo possui padrões nativos para produto pesado e produto precificado. |
| BAL-04 — leitura da etiqueta no PDV | ✅ 100% padrão | `point_of_sale` | Desde que a etiqueta use nomenclatura compatível. |
| ETQ-01 — gerar etiqueta de fracionado | 🟡 Parcial | QWeb + `ora_pop_food_label` | Etiqueta básica é possível; conteúdo alimentar exige campos próprios. |
| ETQ-02 — ingredientes, nutrição, validade, conservação etc. | 🔴 Custom | `ora_pop_food_label` | Criar cadastro e relatório específico. |
| ETQ-03 — layout customizável | 🟡 Parcial | QWeb / `ora_pop_food_label` | Desenvolver template de relatório/ZPL conforme impressora. |

### Estratégia recomendada para balança

**Preferir inicialmente:**

```text
Balança → imprime EAN-13 com produto + peso
                    ↓
                Scanner
                    ↓
               Odoo POS
```

em vez de:

```text
Odoo ↔ driver/API ↔ balança
```

Criar `ora_pop_scale` somente se o modelo comprado exigir comunicação direta e os módulos OCA `stock_remote_measure` / `stock_weighing_remote_measure` não forem suficientes.

---

# 7. Produção / Fabricação

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `mrp` | Odoo CE | BoM, ordens de produção, componentes, produto acabado. |
| `stock` | Odoo CE | Estoque/lotes. |
| `mrp_bom_location` | OCA / `manufacture` | Localização de componentes na receita. |
| `mrp_bom_version` | OCA / `manufacture` | Versionamento de receita. |
| `mrp_bom_tracking` | OCA / `manufacture` | Histórico de alteração da receita. |
| `mrp_lot_number_propagation` | OCA / `manufacture` | Propagação de identificação de lote/serial em cenários específicos. |
| `quality_control_oca` | OCA / `manufacture` | Infraestrutura de controle de qualidade. |
| `quality_control_mrp_oca` | OCA / `manufacture` | Qualidade integrada ao MRP. |

### Cobertura

| Requisito | Cobertura | Módulo / solução |
|---|---|---|
| PRD-01 — receitas/composição | ✅ 100% padrão | `mrp` / BoM |
| PRD-02 — ingredientes | ✅ 100% padrão | `mrp` |
| PRD-03 — consumir da localização correta | 🟢 100% com OCA | `mrp_bom_location` ou rotas/localizações padrão |
| PRD-04 — produto acabado entra no estoque | ✅ 100% padrão | `mrp` |
| PRD-05 — ingrediente pode ser vendido ou produzido | ✅ 100% padrão | `stock` + `sale` + `mrp` |
| PRD-06 — loja → cozinha | ✅ 100% padrão | `stock` |
| PRD-07 — preservar lote/validade no movimento | ✅ 100% padrão | `stock` |
| PRD-08 — rastrear lotes usados em lote produzido | ✅ 100% padrão | `mrp` + lot tracking |
| PRD-09 — rendimento esperado | ✅ 100% padrão para rendimento planejado | BoM + quantidade produzida |
| PRD-10 — perdas de produção | ✅ 100% padrão | MRP Scrap |
| PRD-11 — revisão histórica das faixas | 🟢/🟡 | `mrp_bom_version` + possível campo custom | Versionamento pronto; política específica pode exigir extensão. |

---

# 8. Horta Própria

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `stock` | Odoo CE | Entrada, saldo, lote e movimentação. |
| `mrp` | Odoo CE | Consumo na fabricação. |
| `sale_management` / `point_of_sale` | Odoo CE | Venda futura. |
| `stock_account` | Odoo CE | Valoração de estoque. |

### Cobertura

| Requisito | Cobertura | Solução |
|---|---|---|
| HOR-01 — entrada em estoque | ✅ 100% padrão | Entrada/produção/ajuste conforme processo definido. |
| HOR-02 — uso na produção | ✅ 100% padrão | `mrp` |
| HOR-03 — venda | ✅ 100% padrão | Sales/POS |
| HOR-04 — custo/valoração | ⚪ Regra contábil | Ferramenta existe, mas método de custo precisa ser definido com a empresa/contabilidade. |
| HOR-05 — lote | ✅ 100% padrão | `stock` |

**Não criar módulo específico para a horta inicialmente.**

---

# 9. Compras e Recebimento

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `purchase` | Odoo CE | RFQ, fornecedores e pedidos de compra. |
| `purchase_stock` | Odoo CE | Recebimento e integração com estoque. |
| `stock` | Odoo CE | Lotes, localizações e distribuição. |
| `l10n_br_purchase` | OCA / `l10n-brazil` | Regras fiscais brasileiras de compra. |
| `stock_receipt_lot_info` | OCA / `stock-logistics-workflow` | Informações adicionais de lote no recebimento. Opcional. |

### Cobertura

COM-01 a COM-08: **✅ 100% padrão/OCA**, sem necessidade identificada de addon próprio.

A única customização possível seria uma futura aprovação interna de compra muito específica.

---

# 10. Reposição de Estoque

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `stock` | Odoo CE | Reordering Rules / Replenishment. |
| `purchase` | Odoo CE | Gera RFQ quando a rota é Buy. |
| `mrp` | Odoo CE | Gera MO quando a rota é Manufacture. |

### Cobertura

REP-01 a REP-04: **✅ 100% padrão**.

Odoo já permite:
- mínimo;
- máximo;
- localização;
- trigger automático ou manual;
- rota de compra/fabricação.

---

# 11. Vendas e Canais

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `sale_management` | Odoo CE | Pedidos B2B/comerciais. |
| `sale_stock` | Odoo CE | Integração venda → estoque. |
| `point_of_sale` | Odoo CE | Loja física. |
| `website_sale` | Odoo CE | E-commerce Odoo. |
| Pricelists | Odoo padrão | Preço por cliente/canal/quantidade. |
| `sale_pricelist_global_rule` | OCA / `sale-workflow` | Regras globais adicionais. Opcional. |
| `sale_pricelist_display_surcharge` | OCA / `sale-workflow` | Exibição de acréscimos. Opcional. |
| `l10n_br_sale` | OCA / `l10n-brazil` | Localização fiscal de vendas. |

### Cobertura

| Requisito | Cobertura | Observação |
|---|---|---|
| VEN-01 — loja física | ✅ 100% padrão | POS |
| VEN-02 — e-commerce | ✅ 100% padrão se usar e-commerce Odoo | Se loja externa, vira integração. |
| VEN-03 — B2B/atacado | ✅ 100% padrão | Sales |
| VEN-04 — representantes | ✅ 100% padrão básico | Vendedores/equipes comerciais; comissões avançadas podem exigir OCA/custom. |
| VEN-05 — tabela única | ✅ 100% padrão | Pricelist |
| VEN-06 — preços por canal/cliente | ✅ 100% padrão na maioria dos casos | Pricelists |
| VEN-07 — fluxo fiscal B2B | 🟢 100% com localização fiscal, sujeito a homologação | `l10n_br_sale` + fiscal brasileiro. |

---

# 12. PDV

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `point_of_sale` | Odoo CE | Caixa/PDV. |
| barcode nomenclature | Odoo CE | Produto, peso, preço, desconto. |
| lot/serial tracking no POS | Odoo padrão | Captura de lote no caixa. |
| `pos_barcode_rule_priced_with_change_rate` | OCA / `pos` | Regra adicional para barcode com preço. Apenas se necessário. |
| `ora_pop_pos` | Ora Pop | Regras de validade/desconto e integrações específicas. |

### Cobertura

| Requisito | Cobertura | Solução |
|---|---|---|
| PDV-01 — substituir PDV atual | ✅ 100% base | `point_of_sale` |
| PDV-02 — estoque | ✅ 100% padrão | POS + stock |
| PDV-03 — lotes e validade | 🟡 Parcial | POS suporta lote; regras rígidas de validade exigem extensão. |
| PDV-04 — barcode | ✅ 100% padrão | POS |
| PDV-05 — preços/descontos | ✅ padrão para regras comuns | Regra dependente do lote exige custom. |
| PDV-06 — pagamentos | ✅ padrão para meios comuns / 🟡 para integração brasileira específica | Validar adquirente/TEF. |
| PDV-07 — fiscal | 🟡/🔴 | OCA l10n-brazil ou stack Enterprise oficial; exige PoC. |
| PDV-08 — impedir lote vencido | 🔴 Custom | `ora_pop_pos` + `ora_pop_expiration` |
| PDV-09 — barcode peso/preço | ✅ 100% padrão | nomenclature |
| PDV-10 — desconto por proximidade da validade | 🔴 Custom | `ora_pop_expiration` + POS |

### Observação

O POS padrão permite trabalhar com produtos rastreados por lote, mas a própria documentação informa que a ausência do lote não necessariamente impede a conclusão da venda. Portanto, para o controle sanitário desejado pela Ora Pop, deve existir validação própria.

---

# 13. Autoatendimento / Totem

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `point_of_sale` | Odoo CE | POS base. |
| `pos_self_order` | Odoo padrão | Autoatendimento por QR/kiosk. |
| módulos de pagamento | Odoo / terceiros | Pagamento. |
| localização fiscal | OCA ou Odoo EE | NFC-e/documento fiscal. |

### Cobertura

| Requisito | Cobertura | Observação |
|---|---|---|
| TOT-01 — mini totem | ✅ base pronta | `pos_self_order` |
| TOT-02 — seleção de produtos | ✅ 100% padrão | |
| TOT-03 — pagamento | 🟡 Parcial | Depende do meio de pagamento brasileiro escolhido. |
| TOT-04 — estoque | ✅ 100% padrão | Ordem entra no POS. |
| TOT-05 — documento fiscal | 🟡/🔴 | Depende da solução fiscal adotada. |
| TOT-06 — equipamentos/pagamentos | ⚪ Hardware/integração | PoC necessária. |
| TOT-07 — comportamento offline | ⚪/🔴 | Deve ser definido; self-order não deve ser assumido como fluxo offline completo. |

**Não implementar o totem na primeira fase.**

---

# 14. E-commerce e Integrações

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `website_sale` | Odoo CE | E-commerce nativo. |
| `sale_management` | Odoo CE | Pedidos. |
| `stock` | Odoo CE | Estoque. |
| `l10n_br_sale` / fiscal | OCA | Fiscal brasileiro. |

### Cobertura

| Requisito | Cobertura | Observação |
|---|---|---|
| INT-01 — integrar loja ao ERP | ✅ se a loja for Odoo / 🔴 se externa | Integração externa depende da plataforma. |
| INT-02 — Bling | 🔴 Integração/terceiro | Não assumir módulo OCA oficial sem validar conector específico. |
| INT-03 a INT-07 — fonte de verdade | ⚪ Arquitetura | Decidir master de produtos/preços/estoque/pedidos/clientes. |
| INT-08 — manter ou remover Bling | ⚪ Decisão | Reavaliar depois que o Odoo assumir o ERP. |

Se a loja atual puder ser migrada para `website_sale`, a complexidade de sincronização diminui bastante.

---

# 15. Fiscal Brasileiro

Este é o bloco com maior necessidade de PoC antes do go-live.

## Caminho A — Community + OCA

### Principais módulos

| Módulo | Origem | Função |
|---|---|---|
| `l10n_br_base` | OCA / `l10n-brazil` | Dados brasileiros de empresas/parceiros. |
| `l10n_br_fiscal` | OCA | Motor fiscal. |
| `l10n_br_fiscal_certificate` | OCA | Certificado A1. |
| `l10n_br_account` | OCA | Contabilidade/faturamento BR. |
| `l10n_br_purchase` | OCA | Compras BR. |
| `l10n_br_sale` | OCA | Vendas BR. |
| `l10n_br_stock` | OCA | Estoque BR. |
| `l10n_br_sale_stock` | OCA | Integração venda/estoque. |
| `l10n_br_stock_account` | OCA | Estoque/faturamento fiscal. |
| `l10n_br_nfe` | OCA | NF-e. |
| `l10n_br_account_nfe` | OCA | Integração Accounting ↔ NF-e. |
| `l10n_br_sped_base` | OCA | Base para SPED. |

A branch 18 possui módulos centrais de fiscal, account, sale, purchase e stock migrados. Ainda assim, a localização brasileira é extensa e deve ser homologada com cenários reais da empresa.

### NFC-e

**Não classificar como 100% antes de uma PoC.**

A emissão de NFC-e no POS Community deve ser validada especificamente na branch/revisão escolhida da localização brasileira e no fluxo da Ora Pop.

## Caminho B — Odoo Enterprise oficial

A localização oficial da Odoo possui módulos como:
- `l10n_br`;
- `l10n_br_edi`;
- `l10n_br_edi_sale`;
- `l10n_br_edi_stock`;
- `l10n_br_edi_pos`;
- integração AvaTax/Avalara.

O caminho oficial oferece NF-e/NFC-e, mas envolve licença Enterprise e consumo de créditos/IAP da Avalara.

### Cobertura dos requisitos

| Requisito | Cobertura |
|---|---|
| FIS-01 — substituir NATO | 🟡 Depende da homologação completa |
| FIS-02 — fiscal brasileiro | 🟢 OCA ou Odoo Enterprise, mas precisa de PoC |
| FIS-03 — notas fiscais | 🟢 NF-e possui módulos existentes |
| FIS-04 — cupom/NFC-e | 🟡 Validar no stack escolhido |
| FIS-05 — NF-e | 🟢 OCA `l10n_br_nfe` / Enterprise oficial |
| FIS-06 — NFC-e | 🟡 Validar implantação concreta |
| FIS-07 — fiscal no POS | 🟡/🔴 Pode exigir glue/custom no Community |
| FIS-08 — fiscal B2B | 🟢 OCA/Enterprise |
| FIS-09 — fiscal + financeiro | 🟢 OCA/Enterprise |

---

# 16. Financeiro

### Módulos-base

| Módulo | Origem | Uso |
|---|---|---|
| `account` | Odoo CE | Faturas, contas a pagar/receber e pagamentos básicos. |
| `l10n_br_account` | OCA | Contabilidade/faturamento BR. |
| `l10n_br_account_due_list` | OCA / `l10n-brazil` | Lista de vencimentos. |
| `account_due_list` | OCA / `account-payment` | Créditos/débitos em aberto e vencimentos. |
| `account_payment_notification` | OCA / `account-payment` | Alertas de pagamentos próximos. |
| `account_payment_credit_card` | OCA / `account-payment` | Suporte adicional a pagamentos com cartão. |
| `account-financial-tools` | OCA | Utilitários contábeis adicionais. |
| módulos bancários/CNAB | OCA | Avaliar conforme banco e cobrança. |

### Cobertura

| Requisito | Cobertura | Observação |
|---|---|---|
| FIN-01 — contas a pagar | 🟢 100% com Community/OCA | |
| FIN-02 — contas a receber | 🟢 100% com Community/OCA | |
| FIN-03 — conciliação bancária | 🟡 | Recursos variam entre CE/OCA/Enterprise e banco. |
| FIN-04 — fluxo de caixa | 🟡 | Relatórios podem exigir OCA/relatório próprio. |
| FIN-05 — formas de pagamento | ✅ padrão | |
| FIN-06 — integração bancária | 🟡/🔴 | Depende do banco/API/CNAB. |
| FIN-07 — cartões | 🟡 | Pagamento POS/adquirente deve ser validado. |
| FIN-08 — PIX | 🟡/🔴 | Depende do provedor escolhido. |
| FIN-09 — parcelamentos | ✅/🟢 | Termos de pagamento + OCA quando necessário. |
| FIN-10 — centros de custo | ✅/🟡 | Analítico atende boa parte; validar profundidade desejada. |
| FIN-11 — relatórios | 🟡 | Community/OCA cobre base; relatórios avançados podem exigir módulos adicionais. |

---

# 17. Contabilidade

### Módulos-base

- `account` — Odoo CE.
- `l10n_br_account` — OCA.
- `l10n_br_coa`, `l10n_br_coa_generic` ou `l10n_br_coa_simple` — OCA.
- `l10n_br_mis_report` — OCA, quando aplicável.
- `account-financial-tools` — OCA.
- MIS Builder/OCA pode ser avaliado para relatórios gerenciais.

### Cobertura

CTB-01 a CTB-05: **🟢 atendíveis com Community + OCA**, sujeito a validação com o contador.

CTB-06: **🟡/🔴**, pois depende do sistema utilizado pelo escritório contábil.

---

# 18. Usuários e Permissões

### Módulos-base

- `base` / grupos e ACLs — Odoo CE.
- Record Rules — Odoo framework.
- Grupos próprios em addons Ora Pop quando necessário.

### Cobertura

USR-01 a USR-09: **✅ 100% padrão** para estrutura de usuários/permissões.

Pode haver pequena extensão de segurança nos módulos próprios para:
- descarte;
- alteração de validade;
- desconto manual;
- cancelamento fiscal;
- inventário;
- configurações.

---

# 19. Equipamentos

| Requisito | Cobertura |
|---|---|
| EQP-01 — computadores | ✅ browser/web padrão |
| EQP-02 — leitores de barcode | ✅ padrão no POS; armazém avançado: EE `stock_barcode` ou alternativas OCA |
| EQP-03 — impressoras | ✅ relatórios/browser |
| EQP-04 — etiquetadoras | 🟡 validar ZPL/PDF e modelo |
| EQP-05 — balança | 🟡 OCA `stock-weighing` ou fluxo por etiqueta EAN |
| EQP-06 — totem | 🟡 `pos_self_order` + hardware |
| EQP-07 — terminais de pagamento | 🟡 depende adquirente |
| EQP-08 — validação pré-compra | ⚪ PoC obrigatória |

### Barcode em armazém

O aplicativo oficial **Barcode (`stock_barcode`) é Enterprise**.

Para Community:
- usar scanners como teclado nos formulários/fluxos simples;
- avaliar OCA `stock-logistics-barcode`;
- avaliar módulos de shopfloor/WMS se operações por scanner se tornarem prioridade.

---

# 20. Backup, Infraestrutura e Continuidade

Não é responsabilidade principal de addon Odoo.

### Stack sugerida

```text
Odoo 18 Community
PostgreSQL
Docker / Docker Compose
Reverse Proxy (Caddy/Nginx)
Volumes persistentes
Backup de PostgreSQL
Backup do filestore
Monitoramento
Ambiente de homologação
Git para addons
```

INF-01 a INF-10: **⚪ infraestrutura**, implementar fora do módulo de negócio.

Obrigatório testar restauração; não basta somente gerar backup.

---

# 21. Relatórios e Gestão

### Base padrão

Odoo fornece:
- listas;
- filtros;
- agrupamentos;
- pivôs;
- gráficos;
- relatórios operacionais por módulo.

### Mapeamento

| Requisito | Cobertura |
|---|---|
| REL-01 — saldo por localização | ✅ padrão |
| REL-02 — saldo/lote | ✅ padrão |
| REL-03 — próximos do vencimento | ✅ padrão básico; 🟡 para regra 30%/15% |
| REL-04 — vencidos/descartes | ✅/🟢 com Scrap/OCA |
| REL-05 — perdas de fracionamento | 🟡 `ora_pop_fractioning` |
| REL-06 — perdas de produção | ✅ padrão MRP/Scrap |
| REL-07 — transferências | ✅ padrão |
| REL-08 — inventário/divergências | 🟢 OCA `stock_inventory_discrepancy` recomendado |
| REL-09 — produção | ✅ padrão |
| REL-10 — rendimento | ✅ básico / 🟡 para KPI específico |
| REL-11 — margem | 🟡 depende de custo/fiscal/relatório escolhido |
| REL-12 — vendas | ✅ padrão |
| REL-13 — compras | ✅ padrão |
| REL-14 — financeiro | 🟡 Community/OCA; Enterprise possui pacote mais completo |

---

# 22. Módulos próprios recomendados

## 22.1 `ora_pop_expiration`

**Depende de:**
- `stock`
- `point_of_sale`
- opcionalmente `sale_management`

Responsabilidades:
- calcular percentual de validade restante;
- estágios 30% / 15%;
- descontos;
- bloquear lote vencido;
- disponibilizar status ao POS;
- relatórios específicos.

---

## 22.2 `ora_pop_fractioning`

**Depende de:**
- `stock`
- `mrp`
- opcionalmente OCA `stock_weighing`

Responsabilidades:
- wizard simplificado de fracionamento;
- escolher lote origem;
- registrar peso utilizado;
- registrar perda;
- gerar/usar produto destino;
- criar lote destino;
- copiar validade;
- preservar origem;
- calcular dados auxiliares de custo;
- chamar impressão de etiqueta.

---

## 22.3 `ora_pop_food_label`

**Depende de:**
- `product`
- `stock`
- `ora_pop_fractioning`

Responsabilidades:
- ingredientes;
- informação nutricional;
- armazenamento;
- instruções pós-abertura;
- template de etiqueta;
- peso;
- lote;
- validade;
- barcode;
- PDF/ZPL conforme impressora.

---

## 22.4 `ora_pop_pos`

**Depende de:**
- `point_of_sale`
- `ora_pop_expiration`

Responsabilidades:
- bloquear vencidos;
- aplicar desconto do lote;
- garantir identificação do lote quando obrigatório;
- adaptar UI do POS;
- glue fiscal quando necessário;
- regras específicas para produto fracionado.

---

## 22.5 `ora_pop_scale`

Criar **somente se necessário**.

Antes dele, testar:
- barcode EAN gerado pela balança;
- OCA `stock_weighing`;
- `stock_remote_measure`;
- `stock_weighing_remote_measure`.

---

## 22.6 `ora_pop_integration`

Criar somente para integrações sem conector adequado:
- e-commerce externo;
- Bling;
- gateway/TEF;
- sistema contábil;
- outros serviços.

Não criar um único addon gigante; preferir addons por integração quando crescerem.

---

# 23. Requisitos que podem ser atendidos sem código próprio

Principais grupos com cobertura praticamente completa por configuração/OCA:

- estrutura de warehouses e localizações;
- saldos independentes;
- estoque em trânsito;
- feiras;
- transferências;
- inventário;
- lotes;
- validade básica;
- FEFO;
- descarte;
- UoM;
- produção padrão;
- BoM;
- consumo de ingredientes;
- rastreabilidade de produção;
- compras;
- recebimento;
- reordering rules;
- pedidos de venda;
- tabela de preços padrão;
- POS básico;
- e-commerce Odoo;
- usuários e permissões;
- contas a pagar/receber básicas;
- entrada e consumo da horta.

---

# 24. Requisitos que provavelmente exigem extensão

- workflow exato de responsabilidades nas transferências, se for obrigatório registrar cada papel;
- herança automática de validade no fracionamento;
- faixa de perda esperada;
- histórico/regra de revisão de perda;
- etiqueta alimentar;
- integração direta com balança, se necessária;
- desconto baseado em percentual da validade do lote;
- bloqueio rígido de lote vencido no POS;
- coeficiente de acréscimo para fracionamento;
- regras de preço dependentes de lote;
- alguns relatórios específicos;
- integrações bancárias/PIX/TEF;
- fiscal Community no POS/NFC-e, conforme resultado da PoC;
- integração com loja externa/Bling.

---

# 25. Ordem de implementação recomendada

## Fase 0 — Fundação

1. Subir Odoo 18 Community em ambiente de desenvolvimento/homologação.
2. PostgreSQL + Docker.
3. Repositórios OCA.
4. Estrutura `custom-addons`.
5. Git e estratégia de branches.
6. Backup do banco e filestore.
7. Instalar localização brasileira mínima necessária para testes iniciais.

---

## Fase 1 — Estoque

Implementar primeiro:

- EST-01 a EST-12;
- LOT-01 a LOT-10;
- UoM;
- FEFO;
- lotes;
- validade;
- inventários;
- transferências;
- trânsito;
- feira.

**Objetivo:** provar que o estoque real cabe no modelo padrão.

---

## Fase 2 — PoC de fracionamento

Antes de desenvolver muito, validar um caso real:

```text
Receber:
Queijo 10 kg
Lote Q001
Validade 20/12/2026

↓ transferir para porcionamento

↓ fracionar

230 g
410 g
340 g
20 g de perda

↓ produzir lotes/fracionados

↓ rastrear tudo até Q001
```

Somente após essa PoC fechar a arquitetura do `ora_pop_fractioning`.

---

## Fase 3 — Pesagem e etiqueta

1. Definir SKU do fracionado.
2. Definir UoM principal.
3. Escolher padrão do código de barras.
4. Testar barcode por peso.
5. Testar uma balança candidata.
6. Implementar `ora_pop_food_label`.
7. Só depois comprar os equipamentos definitivos.

---

## Fase 4 — Produção

- BoMs;
- cozinha;
- movimentação de ingredientes;
- horta;
- lotes de produto acabado;
- rastreabilidade;
- custos;
- perdas;
- versionamento de receitas.

---

## Fase 5 — Compras e reposição

- fornecedores;
- RFQ;
- PO;
- recebimento;
- reposição mínima/máxima;
- distribuição entre sedes.

Baixo risco de desenvolvimento.

---

## Fase 6 — POS

Primeiro POS padrão.

Depois:
- lote obrigatório;
- `ora_pop_expiration`;
- bloqueio de vencido;
- desconto por validade;
- produtos pesados;
- regras de preço do fracionado.

---

## Fase 7 — Fiscal brasileiro

Executar PoC completa de:
- venda B2B → NF-e;
- venda POS → NFC-e;
- cancelamento;
- devolução;
- certificado;
- contingência;
- impostos reais da Ora Pop;
- reforma tributária;
- integração estoque/fiscal/financeiro.

**Não ir para produção sem homologar com contador e operação.**

---

## Fase 8 — Financeiro

- contas a pagar;
- contas a receber;
- pagamentos;
- conciliação;
- PIX/cartão/bancos;
- relatórios.

---

## Fase 9 — E-commerce

Decidir:

```text
Opção A:
Odoo Website/eCommerce → Odoo ERP

Opção B:
Loja externa → integração → Odoo ERP
```

Somente então decidir se Bling continua necessário.

---

## Fase 10 — Totem e melhorias

Por último:
- self-order;
- pagamento no totem;
- NFC-e;
- equipamentos;
- relatórios avançados;
- qualidade;
- automações.

---

# 26. Primeiro milestone recomendado

O primeiro marco técnico não deve ser “ter o ERP inteiro”.

Deve ser conseguir executar este fluxo:

```text
Compra / recebimento
      ↓
Produto + lote + validade
      ↓
Estoque em uma sede
      ↓
Transferência para porcionamento
      ↓
Fracionamento por peso
      ↓
Novo estoque rastreável
      ↓
Etiqueta com barcode
      ↓
Leitura no POS
      ↓
Venda
      ↓
Rastreabilidade até o lote de origem
```

Se esse fluxo funcionar corretamente, os principais riscos técnicos do projeto estarão validados.

---

# 27. Resumo de decisão

| Área | Recomendação |
|---|---|
| Estoque | Odoo CE `stock` + poucos addons OCA |
| Lotes/validade | `stock` + addon próprio apenas para política específica |
| Fracionamento | `mrp` como motor + `ora_pop_fractioning` |
| Peso/balança | barcode padrão + OCA `stock-weighing`; integração própria só se necessária |
| Etiqueta alimentar | `ora_pop_food_label` |
| Produção | `mrp` + OCA `manufacture` seletivamente |
| Compras | `purchase` padrão |
| Reposição | `stock` padrão |
| Vendas | `sale_management` padrão |
| POS | `point_of_sale` + `ora_pop_pos` |
| Fiscal | OCA `l10n-brazil` ou Enterprise oficial; PoC obrigatória |
| Financeiro | `account` + OCA |
| E-commerce | `website_sale` se possível; integração se loja externa |
| Totem | `pos_self_order`, depois do core estabilizado |
| Infra | Docker/PostgreSQL/backup/monitoramento |
