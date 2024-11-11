FROM python:3.10-slim-buster

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY requirements.txt .
COPY app.py .
COPY profile.db .
COPY train.db .
COPY plasec.py .
COPY ./ .

RUN pip3 install --upgrade pip --index https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 install pydantic && \
    pip3 install -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/ && \
    apt-get update && apt-get install -y supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
