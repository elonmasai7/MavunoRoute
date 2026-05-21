# Deployment Guide

## Render (Production)

### One-Click Blueprint Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/elonmasai7/MavunoRoute)

The `render.yaml` at the repository root defines three services:

| Service | Type | Plan |
|---------|------|------|
| `mavunoroute-backend` | Web Service (Docker) | Starter |
| `mavunoroute-db` | PostgreSQL 16 | Starter |
| `mavunoroute-redis` | Redis 7 | Starter |

### Manual Deploy Steps

1. Fork/clone the repo to your GitHub account.
2. In the [Render Dashboard](https://dashboard.render.com):
   - **New Blueprint** → Connect your repo → Render reads `render.yaml`.
   - Or create services individually:
     - **Web Service**: Docker runtime, `./backend/Dockerfile`, port auto-assigned.
     - **PostgreSQL**: Render Postgres, starter plan.
     - **Redis**: Render Redis, starter plan.
3. Set required environment variables in the Render dashboard:
   - `APP_ENV`: `production`
   - `APP_SECRET_KEY`: generate a strong random string
   - `JWT_SECRET_KEY`: generate a strong random string
   - `DATABASE_URL`: auto-filled from Render Postgres
   - `REDIS_URL`: auto-filled from Render Redis
   - `CORS_ALLOWED_ORIGINS`: your Render web service URL
4. Run migrations:
   ```bash
   # Via Render Shell or a one-off job:
   alembic upgrade head
   ```
5. Your app is live at `https://<service-name>.onrender.com`.

### Post-Deploy

- **Health check**: `https://<your-url>/api/v1/health`
- **API docs**: `https://<your-url>/docs`
- **Web app**: `https://<your-url>/` (landing page)

## Local and Staging (Docker Compose)

1. Set environment variables from `backend/.env.example`.
2. Build and run services with Docker Compose.
3. Run migrations before serving traffic.

```bash
docker compose up --build -d
docker compose exec backend alembic upgrade head
```

## Manual (No Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
# Ensure PostgreSQL + Redis are running
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Production Notes

- Use managed PostgreSQL and Redis where possible.
- Store secrets in a secure secret manager (Render auto-generates for Blueprint).
- Run Nginx with TLS in front of backend API (Render handles TLS automatically).
- Run at least one worker process for background jobs (add as a separate Render service).
- Enable structured logging and metrics before go-live.

## Health Checks

- API: `/api/v1/health`
- Database: `/api/v1/health/database`

## Rollback

- Roll back to a previous deploy from the Render dashboard.
- Use backward-compatible schema migration strategy.
- Restore database backups only with approved runbook.
