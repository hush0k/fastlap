#!/bin/bash

echo "Setting up FastLap project..."

cp .env.example .env

docker compose down -v

docker compose up --build -d

echo "Waiting for database..."
sleep 5

docker compose exec web python manage.py migrate

docker compose exec web python manage.py seed_db

docker compose exec web python manage.py createsuperuser

echo "Done! Project is running at http://localhost:8000"
echo "API docs: http://localhost:8000/api"