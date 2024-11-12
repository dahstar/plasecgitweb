FROM python:3.10-slim-buster

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=mychatapp.settings
ENV PYTHONUNBUFFERED 1

# Collect static files (if needed for the app)
RUN python manage.py collectstatic --noinput

# Expose the Gunicorn port
EXPOSE 8000

# Run the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mychatapp.wsgi:application"]