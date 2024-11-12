FROM python:3.10-slim-buster

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY requirements.txt .
COPY app.py .
COPY profile.db .
COPY train.db .
COPY plasec.py .
COPY . .
RUN python create_db.py
RUN pip3 install --upgrade pip --index https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 install -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/ && \
    apt-get update  

ENTRYPOINT ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 django_app.wsgi"]
