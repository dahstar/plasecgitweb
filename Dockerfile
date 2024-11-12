FROM python:3.10-slim-buster

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY . .
RUN pip3 install --upgrade pip --index https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 install -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/ && \
    apt-get update  

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mychatapp.wsgi:application"]

