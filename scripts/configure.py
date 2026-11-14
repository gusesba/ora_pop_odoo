"""Gera configuração local sem dependências e sem sobrescrever arquivos existentes."""

import argparse
import os
import re
import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("environment", choices=("dev", "prod"))
    parser.add_argument("--domain", help="Domínio público do Odoo, sem https://")
    args = parser.parse_args()
    if (args.environment == "prod" or args.domain) and not (
        args.domain and re.fullmatch(
            r"(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+"
            r"[a-zA-Z]{2,63}", args.domain
        )
    ):
        parser.error("Produção requer --domain com um domínio válido, sem protocolo ou caminho.")

    env_path = ROOT / ".env"
    config_path = ROOT / "config" / "odoo.local.conf"
    for path in (env_path, config_path):
        if path.exists():
            parser.error(f"{path.name} já existe; mantenha-o ou mova-o antes de configurar.")

    values = {
        "COMPOSE_PROJECT_NAME": f"ora-pop-odoo-{args.environment}",
        "COMPOSE_FILE": "compose.yaml:compose.prod.yaml" if args.environment == "prod" else "compose.yaml",
        "DB_PASSWORD": secrets.token_hex(32),
        "DB_ADMIN_PASSWORD": secrets.token_hex(32),
        "ODOO_DOMAIN": args.domain or "",
    }
    lines = []
    for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines():
        key = line.split("=", 1)[0]
        lines.append(f"{key}={values[key]}" if key in values else line)

    config = (ROOT / "config" / "odoo.conf").read_text(encoding="utf-8")
    config += f"\nadmin_passwd = {secrets.token_hex(32)}\n"
    # O arquivo montado precisa ser legível pelo usuário odoo dentro do container.
    # No Linux, o diretório do projeto protege os segredos contra outros usuários.
    if os.name != "nt":
        ROOT.chmod(0o700)
    for path, content in ((env_path, "\n".join(lines) + "\n"), (config_path, config)):
        with path.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content)
        path.chmod(0o600 if path == env_path else 0o644)
    print(f"Ambiente {args.environment} configurado. Senhas geradas nos arquivos locais ignorados pelo Git.")
    print("Próxima validação: docker compose config --quiet")


if __name__ == "__main__":
    main()
