#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo ".env not found — copy .env.example and update values before starting"
  exit 1
fi

docker-compose up --build
