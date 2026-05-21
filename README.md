# MavunoRoute AI

MavunoRoute AI is a Kenya-first agri-logistics operating system for coordinating the movement of perishable produce from farms to buyers using real operational data, secure workflows, and route intelligence.

## Problem Solved

Perishable produce logistics often fail due to fragmented communication between farmers, buyers, transporters, and cold-chain operators. MavunoRoute AI unifies harvest reporting, demand matching, route planning, proof verification, temperature monitoring, and payment lifecycle tracking.

## Current Features

- JWT authentication with refresh token support.
- Role-aware user and farmer/buyer profile management APIs.
- Harvest batch and buyer demand management APIs.
- Deterministic spoilage risk calculation.
- Harvest-to-demand matching engine.
- Route planning flow with routing provider abstraction (OSRM).
- Transport jobs, proof events, and temperature event APIs.
- Payment initiation and M-Pesa callback handling structure.
- Dashboard metrics endpoint powered by live database values.

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic
- Data: PostgreSQL + PostGIS-ready image, Redis
- Jobs: Celery
- Reverse proxy: Nginx
- Frontend: Server-rendered templates + minimal vanilla JavaScript
- Containerization: Docker, Docker Compose

## Repository Layout

- `backend/` FastAPI API, domain services, providers, migrations, tests
- `frontend/` templates and static assets
- `infra/` infrastructure configs (Nginx)
- `docker-compose.yml` local platform orchestration

## Setup

1. Copy env file:

```bash
cp backend/.env.example backend/.env
```

2. Start services:

```bash
docker compose up --build
```

3. Run migrations:

```bash
docker compose exec backend alembic upgrade head
```

4. Open API docs:

- `http://localhost:8000/docs`

## Running Backend Without Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

## Running Tests

```bash
pytest backend/tests -q
```

## Documentation

- Architecture: `ARCHITECTURE.md`
- API reference: `API_DOCUMENTATION.md`
- Deployment guide: `DEPLOYMENT.md`
- Environment variables: `ENVIRONMENT_VARIABLES.md`
- Database schema: `DATABASE_SCHEMA.md`
- Testing guide: `TESTING.md`
- Security controls: `SECURITY.md`
