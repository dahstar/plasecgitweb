#!/bin/sh



# Run Django migrations
python manage.py migrate &

gunicorn --bind 0.0.0.0:8000 mychatapp.wsgi &

python app.py

 
 
