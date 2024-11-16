#!/bin/sh

# Exit on error
set -e

# Run Django migrations
python manage.py migrate

# Start Gunicorn in the background
gunicorn --bind 0.0.0.0:8000 mychatapp.wsgi &

# Wait briefly to ensure Gunicorn starts properly
sleep 5

# Start the Telegram bot
python telegram/app.py