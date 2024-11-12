FROM python:3.10-slim-buster

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /django_app/

ADD ./requirements.txt ./


RUN pip3 install --upgrade pip --index https://mirrors.aliyun.com/pypi/simple/ &&     apt-get install -y sqlite3 libsqlite3-dev build-essential && \
pip3 install -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/
ADD ./ ./

 

ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 mychatapp.wsgi"]



 