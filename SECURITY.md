# Security

## Implemented Controls

- Password hashing with bcrypt
- JWT authentication with refresh tokens
- Role-based permission checks
- Structured API error responses
- Integration and audit logging models
- Security headers middleware
- Redis-backed distributed rate limiting for auth/public endpoints (with safe in-memory fallback)
- Optional M-Pesa callback signature verification (`MPESA_CALLBACK_SECRET`)

## Hardening Checklist

- Configure strict CORS allowlist
- Add rate limiting middleware for auth/public routes
- Add secure HTTP headers at Nginx and app layers
- Validate and constrain file uploads before enabling media endpoints
- Verify provider callbacks with signature and replay protection

## Operational Security

- Store secrets outside source code
- Rotate credentials and API keys
- Monitor audit logs and integration failures
