#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    DO
    \$do\$
    BEGIN
       IF NOT EXISTS (
          SELECT
          FROM   pg_database
          WHERE  datname = 'memes') THEN
          CREATE DATABASE memes;
       END IF;
    END
    \$do\$;
    GRANT ALL PRIVILEGES ON DATABASE memes TO $POSTGRES_USER;
EOSQL
