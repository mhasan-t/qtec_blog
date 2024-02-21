
# syntax=docker/dockerfile:1

FROM python:3.10.8-slim-bullseye

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config python3-enchant \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install mysqlclient \
    && pip install -r requirements.txt

COPY . .


CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

EXPOSE 8000