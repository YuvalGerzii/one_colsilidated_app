#!/bin/sh
set -e

if [ -z "$DATABASE_URL" ]; then
  echo "DATABASE_URL is not set" >&2
  exit 1
fi

# Wait for PostgreSQL to be ready
printf 'Waiting for PostgreSQL to become available'
until python - <<'PY'
import os
import sys
import psycopg2

dsn = os.environ.get("DATABASE_URL")
try:
    conn = psycopg2.connect(dsn)
except psycopg2.OperationalError:
    sys.exit(1)
else:
    conn.close()
PY
  do
  printf '.'
  sleep 2
  done

echo ' done!'

# Start the application server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
