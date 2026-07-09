#!/bin/sh
set -e

host="$DB_HOST"
port="$DB_PORT"

echo "Waiting for MySQL at ${host}:${port}..."
until nc -z -v -w30 $host $port; do
  echo "Waiting for database..."
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

# Collect static if necessary
# python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn company_service.wsgi:application -b 0.0.0.0:8002 --workers=3
