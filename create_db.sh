#!/bin/sh
name_bd=parse_wiki
user=postgres
pass=password

psql postgres <<-EOSQL
    CREATE USER $user WITH PASSWORD '$pass';
    CREATE DATABASE $name_bd;
    GRANT ALL PRIVILEGES ON DATABASE $name_bd TO $user;
EOSQL