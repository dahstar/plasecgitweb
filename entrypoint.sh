#!/bin/sh

# Run Django migrations
python manage.py migrate

# Start Gunicorn for Django
python manage.py runserver &

# Start the Telegram bot
python telegram/app.py
