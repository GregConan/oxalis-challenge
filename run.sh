#!/usr/bin/env bash

# Launch and build the Docker container
docker compose up -d --build;

# Identify the new Docker container to run commands on
container_ID="$(docker ps | grep oxalis-challenge | cut -d ' ' -f1)";

# Send a command to the Docker container to run Python ELT & dbt setup
docker exec ${container_ID} bash /app/build.sh;