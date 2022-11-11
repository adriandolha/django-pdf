#!/bin/bash
echo Postgres password:
read password
helm del postgres
helm install postgres bitnami/postgresql -n demo\
    --set postgresqlPassword=$password,postgresqlDatabase=djangopdf