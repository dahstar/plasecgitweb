FROM python:3.12

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

ADD ./requirements.txt ./

RUN pip install -r ./requirements.txt

ADD ./ ./

ENTRYPOINT ["/entrypoint.sh"]




