FROM python:3.12

LABEL maintainer="admin@playandsecure.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /

ADD ./requirements.txt ./

RUN pip install -r ./requirements.txt

ADD ./ ./

ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 mychatapp.wsgi && python telegram/app.py"]



