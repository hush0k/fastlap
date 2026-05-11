#!/bin/bash

echo "Setting up the development environment..."

cp .env.example .env

docker-compose up --build -d

sleep 5

docker-compose exec web python manage.py migrate


