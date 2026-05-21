# MavunoRoute AI

> Kenya-first agri-logistics operating system — coordinating perishable produce movement from farms to markets with real operational data, secure workflows, and route intelligence.

## Status

| Component | Status |
|-----------|--------|
| Backend API (FastAPI) | ✅ Complete — 50+ route groups, 22 services, all providers |
| Web Frontend (Jinja2) | ✅ Complete — 80 web routes, 100+ templates, 8 role layouts |
| Database (PostgreSQL) | ✅ Complete — 20+ domain tables, Alembic migration |
| Auth & Security | ✅ Complete — JWT, RBAC, rate limiting, audit logs, security headers |
| Integrations | ✅ Abstracted — OSRM routing, OpenWeather, M-Pesa, SMS/Email, S3 |
| Background Jobs | ✅ Scaﬀolded — Celery workers for routes, risk, notifications, reports |
| Tests | ✅ 17 passing — e2e MVP flow test, smoke tests, real DB fixtures |

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Browser   │────▶│  FastAPI App │────▶│ PostgreSQL  │
│ (Jinja2 +   │     │  + Jinja2    │     │  + PostGIS  │
│  minimal JS)│◀────│  Templates   │◀────│  + Redis     │
└─────────────┘     ├──────────────┤     └─────────────┘
                    │  Celery      │
                    │  Workers     │
                    ├──────────────┤
                    │  Providers   │
                    │  (OSRM, MPesa│
                    │   OpenWeather│
                    │   SMS, Email)│
                    └──────────────┘
```

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2
- **Frontend**: Jinja2 server-rendered templates, vanilla JS, modular CSS
- **Database**: PostgreSQL 16 + PostGIS, Redis 7
- **Jobs**: Celery + Redis broker
- **Auth**: JWT access/refresh tokens, httpOnly cookie + Authorization header
- **Integrations**: OSRM (routing), OpenWeather (weather), M-Pesa (payments), SMTP/SMS (notifications), S3/Local (storage)
- **Infra**: Docker Compose, Nginx reverse proxy

## Repository Layout

```
backend/
├── app/
│   ├── api/v1/        # REST API route groups (50+ endpoints)
│   ├── web/           # Server-rendered web routes (80 routes)
│   │   ├── public.py
│   │   ├── farmer.py
│   │   ├── buyer.py
│   │   ├── transporter.py
│   │   ├── cold_hub.py
│   │   ├── cooperative.py
│   │   ├── admin.py
│   │   ├── shared.py
│   │   └── dependencies.py   # Web auth middleware
│   ├── models/        # SQLAlchemy ORM models (20+ tables)
│   ├── schemas/       # Pydantic request/response schemas
│   ├── services/      # Domain services (22 services)
│   ├── repositories/  # Data access layer
│   ├── providers/     # External integration abstractions
│   ├── jobs/          # Celery task definitions
│   └── utils/         # Permissions, response envelope, etc.
├── alembic/           # Database migrations
└── tests/             # pytest suite (real DB, e2e flow)
frontend/
├── templates/
│   ├── base.html                 # Root template
│   ├── layouts/                  # Role-based layouts (8)
│   │   ├── public.html
│   │   ├── auth.html
│   │   ├── farmer.html
│   │   ├── buyer.html
│   │   ├── transporter.html
│   │   ├── cold_hub.html
│   │   ├── cooperative.html
│   │   └── admin.html
│   ├── partials/                 # Reusable components
│   │   ├── flash_messages.html
│   │   ├── header.html
│   │   ├── breadcrumb.html
│   │   ├── mobile_nav.html
│   │   └── sidebar_*.html        # 7 role-specific sidebars
│   └── pages/                    # Page templates (80+)
│       ├── public/               # about, contact, forgot/reset password, 403/404/500
│       ├── shared/               # profile, settings
│       ├── farmer/               # dashboard, harvests CRUD, offers, pickups, payments, reports
│       ├── buyer/                # dashboard, demands CRUD, matches, orders, payments, deliveries
│       ├── transporter/          # dashboard, vehicles CRUD, jobs, routes, earnings
│       ├── cold_hub/             # dashboard, capacity, check-in/out, temp logs, breaches
│       ├── cooperative/          # dashboard, farmers CRUD, harvests, aggregate, reports
│       └── admin/                # 28 pages — users, farmers, buyers, transporters, vehicles,
│                                 # harvests, demands, routes, jobs, cold hubs, payments,
│                                 # reports, audit logs, integration logs, system health, settings
├── static/
│   ├── css/                      # Modular (8 files)
│   │   ├── base.css, layout.css, sidebar.css
│   │   ├── forms.css, tables.css
│   │   ├── badges.css, buttons.css, dashboard.css
│   └── js/                       # Modular (11 files)
│       ├── api.js, auth.js, forms.js
│       └── pages/                # Per-role: public, farmer, buyer, transporter,
│                                 # cold_hub, cooperative, admin
└── infra/nginx/                  # Nginx configuration
docker-compose.yml                # Multi-service orchestration
```

## Frontend Architecture

### Template Inheritance Chain

```
base.html
  └── layouts/{role}.html          # Adds sidebar, header, breadcrumb
       └── pages/{role}/{page}.html  # Page-specific content
```

### Role-Based Access

Each layout includes a role-specific sidebar with server-rendered active state. Web routes are protected by `require_web_role()` dependency that reads JWT from httpOnly cookie:

- **Public**: landing, about, contact, login, register, forgot-password, reset-password, error pages
- **Farmer**: dashboard, harvests (list/create/detail), offers, pickups, payments, reports
- **Buyer**: dashboard, demands (list/create/detail), matches, orders (list/detail), payments, deliveries
- **Transporter**: dashboard, vehicles (list/create/detail), jobs (list/detail), routes (list/detail), earnings
- **Cold Hub Operator**: dashboard, capacity, check-in, check-out, temperature logs, breaches
- **Cooperative Admin**: dashboard, farmers (list/create/detail), harvests, aggregate-harvests, reports
- **Admin**: dashboard, users, farmers, buyers, transporters, vehicles, harvests, demands, routes, transport-jobs, cold-hubs, payments, reports, audit-logs, integration-logs, system-health, settings

### Auth Flow

1. Login form submits to `/api/v1/auth/login` → JWT returned
2. `auth.js` stores token in both `localStorage` (for API calls) and httpOnly cookie (for web routes)
3. Web routes read JWT via `get_web_user()` dependency
4. Unauthenticated requests to protected routes return 303 redirect to `/login`
5. Role mismatch returns 403

### CSS Architecture (8 modular files)

| File | Purpose |
|------|---------|
| `base.css` | Reset, variables, typography, utilities |
| `layout.css` | Shell layout, header, responsive breakpoints |
| `sidebar.css` | Fixed sidebar, nav items, section labels |
| `forms.css` | Form elements, validation states, form cards |
| `tables.css` | Data tables, empty states, metrics tables |
| `badges.css` | Status badges (success, warning, danger, etc.) |
| `buttons.css` | Button variants (primary, accent, danger, outline) |
| `dashboard.css` | Stat cards, breadcrumbs, flash messages, mobile nav, detail grids |

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL 16 + PostGIS
- Redis 7

### Quick Start

```bash
# Clone
git clone https://github.com/elonmasai7/MavunoRoute.git
cd MavunoRoute

# Backend setup
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Environment
cp backend/.env.example backend/.env
# Edit backend/.env with your database URL, secrets, API keys

# Database
alembic upgrade head

# Start
uvicorn app.main:app --reload --app-dir backend

# Open
open http://localhost:8000
```

### Docker

```bash
docker compose up --build
docker compose exec backend alembic upgrade head
```

## Running Tests

```bash
pytest backend/tests -q
```

## Documentation

| Doc | Description |
|-----|-------------|
| `ARCHITECTURE.md` | System architecture and design decisions |
| `API_DOCUMENTATION.md` | Complete API reference |
| `DEPLOYMENT.md` | Production deployment guide |
| `ENVIRONMENT_VARIABLES.md` | All configurable env vars |
| `DATABASE_SCHEMA.md` | Entity relationship documentation |
| `TESTING.md` | Test strategy and patterns |
| `SECURITY.md` | Authentication, authorization, and security controls |

## Key Design Decisions

- **Modular monolith** with strict bounded contexts — path to extract microservices later without breaking changes.
- **Deterministic spoilage risk engine** — additive factor blocks with explainable output, ready for data-driven ML upgrade.
- **UUIDs for public identifiers**, integer PKs for internal consistency, soft deletes where useful.
- **Provider abstraction** for all external integrations — routing, weather, payments, notifications, storage — swappable without domain logic changes.
- **In-memory rate limiting** with Redis-backed distributed upgrade path and automatic fallback.
- **Audit logging** via dependency injection with graceful failure handling.
- **Test DB** uses same PostgreSQL as development with transactional rollback per test — no mocking the database.
- **No seeded/dummy runtime data** — every record created through API endpoints; test data lives only in `backend/tests/`.
