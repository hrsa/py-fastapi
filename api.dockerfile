FROM bitnami/python

WORKDIR /var/www/api

COPY alembic ./alembic
COPY app ./app
COPY .env ./
COPY requirements.txt ./
COPY alembic.ini ./

RUN apt-get update && \
    apt-get install -y postgresql libpq-dev && \
    pip install -r requirements.txt