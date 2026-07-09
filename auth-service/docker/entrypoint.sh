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

# Create initial superuser if env set
if [ ! -z "$DJANGO_SUPERUSER_EMAIL" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Creating superuser..."
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model();\
  User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists() or User.objects.create_superuser(email='$DJANGO_SUPERUSER_EMAIL', password='$DJANGO_SUPERUSER_PASSWORD')"
fi

echo "Starting gunicorn..."
exec gunicorn auth_service.wsgi:application -b 0.0.0.0:8000 --workers=3
