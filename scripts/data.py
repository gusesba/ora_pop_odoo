"""Backup e restauração de banco + filestore pelo CLI oficial do Odoo 18."""

import argparse
import configparser
import json
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# O entrypoint oficial não encaminha credenciais para o subcomando `odoo db`.
DB_COMMAND = (
    'exec odoo db --db_host "$HOST" --db_port "$PORT" '
    '--db_user "$USER" --db_password "$PASSWORD" "$@"'
)
RESTORE_COMMAND = (
    'set -e\narchive=$(mktemp)\ntrap \'rm -f "$archive"\' EXIT\n'
    'cat > "$archive"\n' + DB_COMMAND.removeprefix("exec ") + ' "$archive"'
)


def compose(*args, **kwargs):
    return subprocess.run(["docker", "compose", *args], cwd=ROOT, check=True, **kwargs)


def check_archive(path):
    with zipfile.ZipFile(path) as archive:
        if not {"dump.sql", "manifest.json"}.issubset(archive.namelist()):
            raise ValueError("O arquivo não contém um backup ZIP completo do Odoo.")
        manifest = json.loads(archive.read("manifest.json"))
        if manifest.get("major_version") != "18.0":
            raise ValueError("Somente backups do Odoo 18.0 podem ser usados neste projeto.")
        if archive.testzip() is not None:
            raise ValueError("O backup contém dados corrompidos.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("backup", "restore"))
    parser.add_argument("archive", type=Path, help="Caminho do backup .zip")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--neutralize", action="store_true", help="Desativa integrações ao restaurar uma cópia para testes")
    mode.add_argument("--move", action="store_true", help="Preserva UUID ao mover definitivamente para outra máquina")
    args = parser.parse_args()
    if args.action == "backup" and (args.neutralize or args.move):
        parser.error("--neutralize e --move são opções de restore.")
    if args.action == "restore" and not (args.neutralize or args.move):
        parser.error("Escolha --neutralize para testes ou --move para migração definitiva.")
    config = configparser.ConfigParser(interpolation=None)
    if not config.read(ROOT / "config" / "odoo.local.conf", encoding="utf-8"):
        parser.error("Execute scripts/configure.py antes de usar backups.")
    database = config["options"]["db_name"]
    path = args.archive.resolve()
    if args.action == "backup" and path.exists():
        parser.error("O arquivo de destino já existe. Escolha outro nome.")
    if args.action == "restore":
        check_archive(path)

    running = compose("ps", "--status", "running", "--services", capture_output=True, text=True)
    was_running = "odoo" in running.stdout.splitlines()
    if args.action == "restore" and was_running:
        parser.error("Pare o Odoo com docker compose stop odoo antes de restaurar.")
    compose("up", "-d", "--wait", "db")
    command = ["run", "--rm", "--no-deps", "-T"]
    if args.action == "backup":
        path.parent.mkdir(parents=True, exist_ok=True)
        partial = path.with_name(path.name + ".partial")
        if partial.exists():
            parser.error(f"Há um backup parcial em {partial}; examine-o antes de tentar novamente.")
        try:
            if was_running:
                compose("stop", "odoo")
            with partial.open("xb") as output:
                partial.chmod(0o600)
                compose(*command, "odoo", "bash", "-c", DB_COMMAND, "--", "dump", database, "-", stdout=output)
            check_archive(partial)
            partial.rename(path)
        finally:
            if was_running:
                compose("start", "odoo")
    else:
        command += ["odoo", "bash", "-c", RESTORE_COMMAND, "--", "load"]
        command += ["--move" if args.move else "--neutralize", database]
        # Envia bytes ao container sem depender de permissões/paths do host Linux/Windows.
        with path.open("rb") as source:
            compose(*command, stdin=source)
    print(f"{args.action} concluído: {path}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Falha: {error}") from error
