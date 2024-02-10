#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

#python manage.py spectacular --color --file schema.yml


# Start server
echo "Starting server"
gunicorn app.wsgi -b 0.0.0.0:8080 
