# MavunoRoute AI

MavunoRoute AI is a Kenya-first, multi-role agri-logistics operating platform for coordinating perishable produce from farms to buyers through routing, transport execution, cold-chain visibility, and payments.

The system is built as a production-oriented modular monolith with strict role-based access control, API-first domain services, and server-rendered multi-page workflows.

## Platform Status

| Area | Status |
|---|---|
| Backend API | Production-structured (FastAPI, service/repository layers) |
| Web Platform | Multi-page role-based UI (82 web routes) |
| Security | JWT auth, RBAC, rate limiting, audit logging |
| Data Layer | PostgreSQL + PostGIS-ready models, Alembic migrations |
| Async Jobs | Celery scaffolding (routes, notifications, risk, reports) |
| Test Suite | 23 passing tests (API + route/permission matrix) |

## Core Capabilities

- Multi-role workflows: Farmer, Buyer, Transporter, Cold Hub Operator, Cooperative Admin, Ops/Admin.
- Harvest-to-demand logistics lifecycle with route and job orchestration.
- Cold-chain observability through temperature/breach tracking.
- Payments and M-Pesa integration abstraction.
- Centralized response envelope, pagination, and access enforcement.
- Professional multi-page web UX with role dashboards and isolated modules.

## Architecture Overview

```text
Browser (Jinja2 + Vanilla JS)
        |
        v
FastAPI App
  - API routes (/api/v1/*)
  - Web routes (role-based pages)
  - RBAC + auth dependencies
        |
        v
PostgreSQL / PostGIS   Redis
        |
        v
Celery Workers (background processing)
```

## Technology Stack

- Backend: Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, Pydantic v2
- Frontend: Jinja2 templates, modular CSS, minimal vanilla JavaScript
- Data: PostgreSQL 16, PostGIS-ready schema, Redis 7
- Async: Celery
- Infra: Docker Compose, Nginx (local), Render-ready Docker setup

## Repository Structure

```text
backend/
  app/
    api/v1/           # REST endpoints
    web/              # Server-rendered page routes
    models/           # SQLAlchemy models
    schemas/          # Pydantic contracts
    services/         # Domain services
    repositories/     # Data access
    providers/        # External integration abstractions
    middleware.py     # Security + rate limit middleware
    dependencies.py   # Auth/permission dependencies
  alembic/            # Migrations
  tests/              # API + web route/permission tests

frontend/
  templates/
    layouts/          # Role-specific shell layouts
    partials/         # Shared UI fragments
    pages/            # Role/public/shared page templates
  static/
    css/              # Modular styles + role page styles
    js/               # API/auth/forms/tables + page scripts
```

## Multi-Page Route Groups

- Public: `/`, `/login`, `/register`, `/forgot-password`, `/reset-password`, `/about`, `/contact`
- Shared authenticated: `/dashboard`, `/profile`, `/settings`, `/notifications`
- Farmer: `/farmer/*`
- Buyer: `/buyer/*`
- Transporter: `/transporter/*`
- Cold hub: `/cold-hub/*`
- Cooperative: `/cooperative/*`
- Admin: `/admin/*`

All protected routes enforce authentication and role constraints. Unauthenticated users are redirected to `/login`; role violations return a 403 page.

## Frontend Design Principles

- True multi-page architecture (no hidden-div pseudo-routing).
- Page isolation with dedicated route/template/script responsibilities.
- Defensive rendering for loading, empty, error, and invalid-data states.
- Reusable partials for alerts, empty states, form errors, and pagination.
- Scoped page scripts to avoid cross-module side effects.

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Redis 7+

### Local Setup (Non-Docker)

```bash
git clone https://github.com/elonmasai7/MavunoRoute.git
cd MavunoRoute

python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cp backend/.env.example backend/.env
# update secrets and connection settings in backend/.env

cd backend
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:
- App: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Compose

```bash
docker compose up --build -d
docker compose exec backend alembic upgrade head
```

## Testing

Run all tests:

```bash
cd backend
pytest -q
```

Current baseline: **23 passing tests**.

## Deployment

- See `DEPLOYMENT.md` for production deployment instructions.
- The repository includes a root `Dockerfile` suitable for Render Docker web service deployment.

## Security and Data Integrity

- JWT access/refresh auth flow.
- Role-based permission map with endpoint-level enforcement.
- Security headers and distributed rate limiting.
- Audit logging for sensitive operations.
- No seeded or dummy runtime data in application flows.

## Documentation Index

- `ARCHITECTURE.md`
- `API_DOCUMENTATION.md`
- `DEPLOYMENT.md`
- `ENVIRONMENT_VARIABLES.md`
- `DATABASE_SCHEMA.md`
- `TESTING.md`
- `SECURITY.md`
