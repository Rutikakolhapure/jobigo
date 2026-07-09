#!/bin/sh
set -e

host="$DB_HOST"
port="$DB_PORT"

echo "Waiting for MySQL at ${host}:${port}..."
until nc -z -v -w30 $host $port; do
  echo "Waiting for database..."
  sleep 1
done

# Run migrations
python manage.py migrate --noinput

# Start server
exec gunicorn ai_service.wsgi:application -b 0.0.0.0:8004 --workers=4
