#!/bin/bash
set -e

# create user database
psql -v ON_ERROR_STOP=1 --username "$POSTGRE_USER" <<-EOSQL
    SELECT 'CREATE DATABASE $POSTGRE_NAME'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRE_NAME')\gexec
EOSQL