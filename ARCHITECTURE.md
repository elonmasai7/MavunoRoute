# Architecture

## Overview

MavunoRoute AI is implemented as a modular FastAPI backend with clean separation of concerns:

- API routes: request/validation/response only
- Services: business workflows and transaction boundaries
- Repositories: database access abstraction
- Providers: external integrations (routing, weather, payments, notifications, storage)
- Jobs: asynchronous workers for heavy workflows

## Domain Modules

- Identity and access
- Farmer supply (farmer profiles, harvest batches)
- Buyer demand
- Matching and route optimization
- Execution (transport jobs, proof events, temperature events)
- Payments and reconciliation
- Reporting and observability

## Cross-Cutting

- Consistent API response envelope
- Pagination conventions for list endpoints
- JWT auth + role-based permissions
- Audit and integration logs for sensitive workflows
- Provider abstraction to allow external API replacement

## MVP Flow

1. Farmer creates harvest batch
2. Buyer creates demand
3. System matches harvest to demand
4. Ops plans route
5. Transporter accepts job and confirms pickup/delivery with proof
6. Temperature events captured
7. Payment initiated and updated via provider callback
8. Reports reflect live transaction metrics
