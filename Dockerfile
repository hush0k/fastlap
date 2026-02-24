FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements/base.txt requirements/base.txt
RUN pip install -r requirements/base.txt

COPY . .
