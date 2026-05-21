# Deployment Guide

## Local and Staging

1. Set environment variables from `backend/.env.example`.
2. Build and run services with Docker Compose.
3. Run migrations before serving traffic.

## Commands

```bash
docker compose up --build -d
docker compose exec backend alembic upgrade head
```

## Production Notes

- Use managed PostgreSQL and Redis where possible.
- Store secrets in a secure secret manager.
- Run Nginx with TLS in front of backend API.
- Run at least one worker process for background jobs.
- Enable structured logging and metrics before go-live.

## Health Checks

- API: `/api/v1/health`
- Database: `/api/v1/health/database`

## Rollback

- Roll back app container image tag.
- Use backward-compatible schema migration strategy.
- Restore database backups only with approved runbook.
