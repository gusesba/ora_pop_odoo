# Ora Pop — Odoo

Projeto de implantação e customização do Odoo 18 Community para a Ora Pop.

## Estrutura

```text
ora-pop-odoo/
├── docs/                   # Requisitos e planejamento
├── custom-addons/          # Módulos próprios
├── oca/                    # Dependências OCA da série 18.0
├── config/
│   ├── Caddyfile            # Proxy HTTPS de produção
│   ├── odoo.conf            # Modelo de configuração, sem segredos
│   └── postgres-init.sh     # Criação do usuário PostgreSQL do Odoo
├── scripts/
│   ├── configure.py         # Configuração local de dev/prod
│   └── data.py              # Backup e restauração com filestore
├── .env.example
├── compose.yaml
└── compose.prod.yaml
```

Os documentos em `docs/` são referências de requisitos e planejamento. As decisões de negócio ainda precisam de homologação.

## Ambiente portátil

Desenvolvimento e produção usam Docker Compose, Odoo 18 Community e PostgreSQL 16. As imagens estão fixadas por digest em `.env.example` para reproduzir a mesma versão nas duas máquinas, inclusive ao baixar novamente. Os caminhos de montagem são relativos ao projeto.

| Item | Desenvolvimento | Produção na VM |
|---|---|---|
| Configuração Compose | `compose.yaml` | Base + `compose.prod.yaml` |
| Projeto/volumes | `ora-pop-odoo-dev` | `ora-pop-odoo-prod` |
| Acesso | `http://localhost:8070` | HTTPS no domínio configurado |
| Gerenciador de bancos | Disponível em localhost | Bloqueado no Odoo e no proxy |
| Processamento Odoo | Padrão, sem workers de processos | 2 workers + 1 de cron |
| Nome da base | `ora_pop` | `ora_pop` |

O mesmo nome de base facilita a migração; os volumes e as senhas são independentes por ambiente. PostgreSQL não publica porta no host. Odoo publica apenas em `127.0.0.1`; na produção o Caddy recebe as conexões externas nas portas 80/443 e encaminha também os WebSockets.

Banco e filestore ficam em volumes nomeados. Senhas ficam em `.env` e `config/odoo.local.conf`, ignorados pelo Git. O usuário PostgreSQL `odoo` não é superusuário; a criação de bases é permitida para inicialização e restauração pelo CLI. Os logs dos containers têm rotação.

## Desenvolvimento local

Pré-requisitos: Python 3.10+ e Docker Desktop com containers Linux e Docker Compose 2.20+ ativos. Execute na raiz do projeto:

```powershell
python scripts/configure.py dev
docker compose config --quiet
docker compose up -d
```

O script gera senhas aleatórias e seleciona os arquivos Compose em `.env`. Recusa sobrescrever configuração existente. Não instala dependências nem inicia serviços. No Linux, restringe o diretório do projeto ao proprietário; o arquivo de configuração continua legível para o usuário do container. No Windows, mantenha a pasta em seu perfil de usuário.

Acesse [o gerenciador local](http://localhost:8070/web/database/manager) e crie a base **`ora_pop`**, em português do Brasil, país Brasil e sem dados de demonstração. A senha mestra está em `admin_passwd` no arquivo local `config/odoo.local.conf`. Escolha o login e uma senha própria para o administrador do Odoo. A senha mestra, a senha do PostgreSQL e a senha de acesso ao Odoo são diferentes.

```powershell
docker compose ps
docker compose logs --tail 100 odoo
docker compose down
```

`down` preserva os volumes. **Não use `down --volumes` para parar o ambiente:** essa opção apaga banco e filestore. Mantenha `COMPOSE_PROJECT_NAME` estável depois de iniciar: mudar o nome seleciona outros volumes.

O Odoo nativo do Windows, na porta 8069 e com a base `ora_pop_dev`, permanece independente. A configuração deste projeto é para containers Linux; nenhum banco nativo é importado automaticamente. Se precisar trazer essa base, use um backup ZIP do Odoo 18 que inclua o filestore, restaurando-o como `ora_pop`. Bancos de outras versões principais precisam de migração própria.

## Produção em VM Linux

Use uma VM com Docker Engine, Compose 2.20+ e Python 3.10+. A configuração inicial de workers deve ser ajustada à CPU, RAM e carga da VM antes da entrada em operação. O domínio precisa apontar para o IP público da VM; libere 80/TCP e 443/TCP no firewall, mantendo SSH restrito à administração. O Caddy emite e renova o certificado automaticamente; certificados ficam no volume `caddy-data`.

Copie o código do projeto para a VM, preservando a estrutura e a revisão exata dos addons. Use Git quando houver um remoto configurado ou transfira o código por SCP/SFTP. Exclua `.env`, `config/odoo.local.conf`, backups e dados locais da cópia do código.

Na raiz do projeto da VM, substitua o domínio abaixo pelo domínio real:

```bash
python3 scripts/configure.py prod --domain erp.sualoja.com.br
docker compose config --quiet
```

Os comandos seguintes usam automaticamente o overlay de produção por meio de `COMPOSE_FILE` em `.env`. Novas senhas são geradas na VM. Para aproveitar uma base existente, siga a restauração abaixo **antes de iniciar o Odoo**. Para uma implantação limpa, use o procedimento de criação inicial.

### Criação inicial de uma base de produção vazia

Inicie temporariamente o gerenciador somente na interface local da VM, sem o proxy público:

```bash
docker compose up -d --wait db
docker compose run -d --name ora-pop-bootstrap --service-ports odoo odoo --workers=0
```

No seu computador, abra um túnel SSH, substituindo `usuario@IP_DA_VM` e usando uma porta local livre:

```powershell
ssh -L 8071:127.0.0.1:8070 usuario@IP_DA_VM
```

Acesse [o gerenciador pelo túnel](http://localhost:8071/web/database/manager), use a senha mestra gerada **na VM** e crie `ora_pop`, sem demonstração, escolhendo a senha do administrador. Depois de criar a base, execute na VM:

```bash
docker stop ora-pop-bootstrap
docker rm ora-pop-bootstrap
docker compose up -d
```

Acesse o domínio por HTTPS. O modo normal de produção desativa o gerenciador de bancos. Configure o fuso horário `America/Sao_Paulo` nos usuários e valide os dados da empresa antes de instalar/configurar os módulos de negócio.

## Backup e transferência de dados

O script usa o comando oficial `odoo db dump/load`. O ZIP contém SQL, manifesto e filestore, incluindo anexos e imagens. **Copiar somente o código ou somente um dump SQL não transfere o ambiente completo.** Não copie o diretório físico do PostgreSQL entre Windows e Linux.

Com o Docker ativo, na máquina de origem:

```powershell
python scripts/data.py backup backups/ora_pop-2026-11-14.zip
```

Escolha um nome novo a cada execução. O script pausa o Odoo durante o backup para manter banco e filestore consistentes e reinicia o serviço caso estivesse em execução, inclusive se o backup falhar. Há indisponibilidade durante esse período. O arquivo é escrito em modo binário, sem redirecionamento pelo PowerShell, e só recebe o nome final depois de verificar a integridade do ZIP. Arquivos `.partial` indicam execução incompleta e precisam ser examinados antes de repetir.

Transfira o ZIP por SCP/SFTP para `backups/` da VM, separadamente do código. Na VM já configurada, para uma migração definitiva:

```bash
python3 scripts/data.py restore backups/ora_pop-2026-11-14.zip --move
docker compose up -d
```

`--move` preserva o identificador da base. Para a virada definitiva, pare o Odoo na origem, gere o backup final com o serviço já parado e mantenha a origem desligada enquanto a VM opera. Assim não entram novas vendas após o backup e não há duas instâncias ativas da mesma base.

Para restaurar uma **cópia de produção em desenvolvimento/homologação**, configure uma pasta/ambiente separado e use:

```powershell
python scripts/data.py restore backups/ora_pop-2026-11-14.zip --neutralize
docker compose up -d
```

`--neutralize` usa a neutralização padrão do Odoo para testes; revise também integrações dos addons antes de liberar essa cópia. O restore exige o Odoo parado e **não sobrescreve uma base existente**. Não há opção de exclusão forçada no script. Se for testar recuperação, use um ambiente novo com outros volumes e portas; uma restauração que falhe pode deixar uma base parcial que requer análise.

Depois de restaurar, confira login, módulos instalados, anexos, imagens de produtos e um fluxo de venda. Atualize `web.base.url` para a URL do destino e, em produção, fixe `web.base.url.freeze = True` nos parâmetros do sistema. O restore não altera credenciais dos usuários do Odoo.

Backups não incluem código, `.env` ou configuração local. Preserve a revisão do código e as referências `*_IMAGE` usadas com cada backup; ao mudar as imagens do projeto, mantenha os mesmos digests em dev e prod. Guarde também uma cópia protegida das configurações necessárias à recuperação. Os segredos da VM podem ser novos ao restaurar em uma implantação vazia.

Agende o comando de backup no cron/agendador da máquina, em uma janela de indisponibilidade adequada à loja, e mantenha cópias protegidas fora da VM. Frequência, retenção e tolerância à perda de dados ainda precisam ser definidas com a operação. A configuração inicial não agenda tarefas nem exclui backups antigos.

## Atualizações e addons

Valide mudanças primeiro em desenvolvimento/homologação. Para atualizar, faça backup, registre os novos digests em `.env.example` e nos ambientes correspondentes e execute:

```bash
docker compose pull
docker compose up -d
```

Para mudanças que exijam atualização de módulos, pare o Odoo e execute a atualização apenas dos módulos alterados com `docker compose run --rm odoo odoo -d ora_pop -u NOME_DO_MODULO --stop-after-init`, antes de subir o serviço novamente. Não use `-u all` como rotina. Para rollback após mudanças no banco, restaure o backup com o código e as imagens correspondentes em um destino vazio.

- `custom-addons/`: módulos próprios, por dependência e herança.
- `oca/`: repositórios compatíveis com `18.0`, fixados por revisão; consulte `oca/README.md`.

Os addons são montados como somente leitura nos dois ambientes. Transfira seus fontes junto ao projeto; dependências Python/SO adicionais deverão ser incorporadas a uma imagem própria quando algum addon realmente exigir. Nenhum módulo de negócio, localização fiscal ou repositório OCA foi instalado por esta configuração.

Referências: [produção com Compose](https://docs.docker.com/compose/how-tos/production/), [CLI de bancos do Odoo 18](https://github.com/odoo/odoo/blob/18.0/odoo/cli/db.py) e [proxy reverso do Caddy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy).
