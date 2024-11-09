FROM python:3.10-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
LABEL maintainer="admin@playandsecure.com"

# Install dependencies required for building SQLite and Django
RUN apt-get update && \
    apt-get install -y wget build-essential libsqlite3-dev && \
    rm -rf /var/lib/apt/lists/*

# Download and build SQLite 3.42.0 from source
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz && \
    tar xvfz sqlite-autoconf-3420000.tar.gz && \
    cd sqlite-autoconf-3420000 && \
    ./configure && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3420000* && \
    ldconfig

# Set the PATH and LD_LIBRARY_PATH to the newly installed SQLite
ENV PATH="/usr/local/bin:$PATH"
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Set up working directory
WORKDIR /django_app/

# Copy requirements file and install Python dependencies
ADD ./requirements.txt ./
RUN pip3 install --upgrade pip --index https://mirrors.aliyun.com/pypi/simple/ && \
    pip3 install -r requirements.txt --index https://mirrors.aliyun.com/pypi/simple/

# Copy application files
ADD ./ ./

# Run Django migrations and start Gunicorn
ENTRYPOINT ["/bin/sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 django_app.wsgi"]
