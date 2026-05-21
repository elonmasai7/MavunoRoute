# Database Schema

The database uses PostgreSQL with a migration-first approach via Alembic.

## Key Tables

- `users`, `refresh_tokens`
- `farmer_profiles`, `cooperatives`, `crops`, `harvest_batches`
- `buyer_profiles`, `buyer_demands`
- `transporter_profiles`, `vehicles`, `cold_hubs`
- `route_plans`, `route_stops`, `transport_jobs`
- `proof_events`, `temperature_events`
- `payments`, `mpesa_transactions`
- `notifications`, `audit_logs`, `api_integration_logs`

## Migration

Initial migration file:

- `backend/alembic/versions/0001_initial_schema.py`

Run:

```bash
alembic upgrade head
```

## Indexing Guidance

- Index foreign keys, status fields, and creation timestamps.
- Add PostGIS indexes for geospatial workloads as routing volume grows.
