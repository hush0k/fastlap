# FastLap

REST API for a motorsport platform. Drivers, teams, races, tournaments, news — all in one place.

Stack: Django 5.2, DRF, PostgreSQL, Redis, Firebase Firestore, Django Channels (WebSockets), Daphne.

---

## Requirements

- Docker + Docker Compose
- Firebase project with Firestore enabled

---

## Setup

**1. Create `.env.example`** (copied to `.env` by the setup script)

```env
SECRET_KEY=your-secret-key

DATABASE_NAME=fastlap
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=secrets/firebase-credentials.json

SMTP_SERVER_EMAIL=your@email.com
SMTP_SERVER_PASSWORD=your-smtp-password
ADMIN_EMAIL=admin@example.com

LOG_LEVEL=INFO
```

**2. Put Firebase credentials at `secrets/firebase-credentials.json`**

**3. Run setup**

```bash
bash scripts/setup.sh
```

This will: copy `.env.example` to `.env`, build and start containers, run migrations, seed the database, and prompt to create a superuser.

---

## Scripts

```bash
bash scripts/start.sh      # build and start containers
bash scripts/migrate.sh    # makemigrations + migrate inside the container
bash scripts/clean.sh      # stop containers, wipe volumes, restart fresh
bash scripts/logs.sh       # tail web container logs
```

---

## API docs

Swagger UI — `http://localhost:8000/api/schema/swagger-ui/`

OpenAPI schema — `http://localhost:8000/api/schema/`

---

## Project structure

```
apps/
  users/          auth, registration, avatar (Firestore)
  drivers/        driver profiles and race results
  teams/          teams and standings
  team_stuff/     staff members and rosters
  races/          series and individual races
  race_tracks/    track catalog
  tournaments/    tournament management
  news/           articles, tags, series
  common/         shared pagination, permissions, Redis service, cache decorators
config/
  settings/
    base.py       shared settings
    local.py      local overrides
    prod.py       production settings
middleware/       request ID and logging middleware (async-capable)
scripts/          helper shell scripts
secrets/          firebase credentials (not committed)
```

---

## Auth

JWT via `djangorestframework-simplejwt`.

- `POST /api/v1/auth/register/` — registration, multipart, avatar optional
- `POST /api/v1/auth/login/` — returns `access` and `refresh` tokens
- `POST /api/v1/auth/refresh/` — refresh access token

Pass the token as `Authorization: Bearer <access_token>`.

---

## Linting

```bash
ruff check .
black .
```

Config is in `pyproject.toml`.
