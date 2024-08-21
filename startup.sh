#!/bin/bash
python manage.py migrate
python manage.py collectstatic --no-input
cp -r /app/static/. /backend_static/static
gunicorn --bind 0.0.0.0:8000 donations.wsgi
