#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Pre populate receivers table"
python manage.py pre_populate_receivers --number 30

python manage.py collectstatic --skip-checks

# Start server
echo "Starting server"

gunicorn --bind 0.0.0.0:8000 --access-logfile - django_app.wsgi
