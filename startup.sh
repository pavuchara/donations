#!/bin/bash
python manage.py migrate
python manage.py collectstatic --no-input
cp -r /app/media/. /app/media/
gunicorn --bind 0.0.0.0:8000 donations.wsgi
