# Testing Guide

## Scope

The backend test suite focuses on core platform flows:

- registration and login
- role-protected access
- farmer and harvest creation
- buyer demand creation
- matching and spoilage scoring
- route planning
- transport job lifecycle
- proof and temperature events
- payment initiation and callback updates
- dashboard report metrics

## Run Tests

```bash
pytest backend/tests -q
```

## Rules

- Test fixtures are only for test runtime.
- No seeded runtime production data is used.
- Add regression tests for every fixed bug in core workflows.
