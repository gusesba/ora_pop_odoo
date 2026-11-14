#!/usr/bin/env bash
set -e

# Executado pela imagem oficial somente ao inicializar um volume vazio.
psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set=ON_ERROR_STOP=1 --set=odoo_password="$ODOO_DB_PASSWORD" <<'SQL'
CREATE ROLE odoo LOGIN NOSUPERUSER NOCREATEROLE CREATEDB
    PASSWORD :'odoo_password';
SQL
