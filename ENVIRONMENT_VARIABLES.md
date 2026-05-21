# Environment Variables

Primary env template: `backend/.env.example`

## Required Core

- `APP_ENV`
- `APP_SECRET_KEY`
- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`

## Optional Integrations

- M-Pesa: `MPESA_*`
- Callback signature validation: `MPESA_CALLBACK_SECRET`
- Routing provider: `ROUTING_PROVIDER`, `OSRM_BASE_URL`, provider keys
- Weather: `OPENWEATHER_API_KEY`
- Notifications: `SMS_PROVIDER`, `AFRICAS_TALKING_*`, `TWILIO_*`
- Email: `EMAIL_*`
- Storage: `STORAGE_PROVIDER`, local or S3 settings

## Security Rules

- Never commit populated `.env` files.
- Rotate integration secrets periodically.
- Use different values per environment.
