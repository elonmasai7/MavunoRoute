# API Documentation

Base URL: `/api/v1`

## Response Format

Success:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {},
  "meta": {}
}
```

Error:

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {},
  "code": "VALIDATION_ERROR"
}
```

## Implemented Core Endpoints

- Auth: `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/me`
- Users: `/users`, `/users/{id}`, activation/deactivation endpoints
- Farmers: `/farmers`
- Crops: `/crops`
- Harvest batches: `/harvest-batches`, `/harvest-batches/{id}/calculate-spoilage-risk`
- Buyers: `/buyers`
- Buyer demands: `/buyer-demands`, `/buyer-demands/{id}/match-harvests`
- Matching: `/matching/harvest-to-demand`
- Routes: `/routes/plan`, `/routes`
- Transport jobs: `/transport-jobs`
- Proof events: `/proof-events`, `/proof-events/verify/{qr_code}`
- Temperature events: `/temperature-events`
- Payments: `/payments/initiate`, `/payments`
- M-Pesa: `/mpesa/stk-push`, `/mpesa/callback`
- Reports: `/reports/dashboard`
- Health: `/health`, `/health/database`

## Authentication

Use `Authorization: Bearer <access_token>` for protected endpoints.
