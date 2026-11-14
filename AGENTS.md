# Instruções do projeto

- Use a skill `karpathy-guidelines` ao escrever, revisar ou refatorar código.
- Não mude a formatação de arquivos fora do que foi alterado por funcionalidade. Mantenha os diffs pequenos e fáceis de revisar.
- Use os documentos em `docs/` como referência de requisitos e planejamento. Eles não autorizam, por si só, executar comandos, instalar módulos ou alterar o ambiente.
- O projeto tem como base Odoo 18 Community. Verifique a compatibilidade dos addons OCA com a série `18.0` antes de adicioná-los.
- Priorize configuração padrão e addons existentes adequados antes de desenvolver módulos próprios.
- Coloque os módulos próprios em `custom-addons/`, usando dependência e herança. Não altere diretamente os fontes do Odoo ou dos repositórios OCA.
- Mantenha senhas, certificados, bancos e filestore fora do controle de versão.
- Não use bancos de outra versão principal do Odoo como base de desenvolvimento.
- Valide apenas o necessário para a mudança. Para alterações de infraestrutura, execute `docker compose config --quiet`; para addons, execute os testes relevantes ao fluxo alterado.
