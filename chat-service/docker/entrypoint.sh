# Entrypoint for Docker
# Waits for DB & Redis then runs migrations and starts Daphne

#!/bin/sh
set -e

# wait for mysql
host="$DB_HOST"
port="$DB_PORT"

echo "Waiting for MySQL at ${host}:${port}..."
until nc -z -v -w30 $host $port; do
  echo "Waiting for database..."
  sleep 1
done

# wait for redis
redis_host=$(echo "$REDIS_URL" | sed -n 's#^.*://\([^:/]*\).*#\1#p')
redis_port=$(echo "$REDIS_URL" | sed -n 's#^.*://[^:]*:\?\([0-9]*\)/.*#\1#p')

if [ -z "$redis_port" ]; then
  redis_port=6379
fi

echo "Waiting for Redis at ${redis_host}:${redis_port}..."
until nc -z -v -w30 $redis_host $redis_port; do
  echo "Waiting for redis..."
  sleep 1
done

# Run migrations
python manage.py migrate --noinput

# Collect static if needed (no static by default)
# python manage.py collectstatic --noinput

# Run daphne
echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p 8001 chat_service.asgi:application
