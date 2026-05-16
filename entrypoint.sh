#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

celery -A config worker -l INFO &
celery -A config beat -l INFO &

gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application