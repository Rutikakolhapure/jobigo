#!/bin/sh
set -e

host="$DB_HOST"
port="$DB_PORT"

echo "Waiting for MySQL at ${host}:${port}..."
until nc -z -v -w30 $host $port; do
  echo "Waiting for database..."
  sleep 1
done

# Ensure spaCy model is installed
python - <<'PY'
import importlib
try:
    importlib.import_module('en_core_web_sm')
    print('spaCy model en_core_web_sm already installed')
except Exception:
    try:
        import spacy
        print('Downloading spaCy model en_core_web_sm...')
        spacy.cli.download('en_core_web_sm')
    except Exception as e:
        echo='Failed to download spaCy model: {}'.format(e)
        print(e)
PY

python manage.py migrate --noinput

# Collect static if needed
# python manage.py collectstatic --noinput

exec gunicorn seeker_service.wsgi:application -b 0.0.0.0:8003 --workers=3
