#!/bin/sh

# Run Django migrations
python manage.py migrate

# Start Gunicorn for Django
gunicorn --bind 0.0.0.0:8000 mychatapp.wsgi &

# Start the Telegram bot
python telegram/app.py