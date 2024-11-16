#!/bin/sh

# Exit on error
set -e

 
# Start Gunicorn in the background
python manage.py runserever &

# Wait briefly to ensure Gunicorn starts properly
sleep 5

# Start the Telegram bot
python telegram/app.py