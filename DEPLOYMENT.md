# Deployment Guide

## Render (Production)

### Manual Deploy Steps

A root `Dockerfile` is included at the repo root for Render deployment. Create a **Web Service** on Render — do NOT use Blueprint, as the repo is public and manually configured services give you more control.

1. Go to [Render Dashboard](https://dashboard.render.com) → **New +** → **Web Service**.

2. In the "Public Git Repository" field, paste:
   ```
   https://github.com/elonmasai7/MavunoRoute
   ```
   (No GitHub OAuth needed — the repo is public.)

3. Configure the service:

   | Setting | Value |
   |---------|-------|
   | **Name** | `mavunoroute-backend` |
   | **Runtime** | `Docker` |
   | **Branch** | `main` |
   | **Plan** | Starter |

4. Add environment variables:

   | Key | Value |
   |-----|-------|
   | `APP_ENV` | `production` |
   | `APP_SECRET_KEY` | Generate a random 32+ char string |
   | `JWT_SECRET_KEY` | Generate a random 32+ char string |
   | `DATABASE_URL` | Your Render Postgres connection string |
   | `REDIS_URL` | Your Render Redis connection string |
   | `CORS_ALLOWED_ORIGINS` | Your Render service URL (e.g. `https://mavunoroute-backend.onrender.com`) |

5. Create two additional services manually:
   - **Render Postgres** (Starter plan)
   - **Render Redis** (Starter plan)

6. After the web service deploys, run migrations via Render Shell:
   ```bash
   alembic upgrade head
   ```

7. Your app is live at `https://mavunoroute-backend.onrender.com`.

### Post-Deploy

- **Health check**: `https://mavunoroute-backend.onrender.com/api/v1/health`
- **API docs**: `https://mavunoroute-backend.onrender.com/docs`
- **Web app**: `https://mavunoroute-backend.onrender.com/` (landing page)

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
