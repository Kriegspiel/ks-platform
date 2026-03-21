# Step 120 - MongoDB Motor Wiring

This folder is the detailed execution packet for slice `120` from [step-100](../step-100/README.md).

Canonical status for this slice still lives in [step-100/PROGRESS.md](../step-100/PROGRESS.md). This folder expands the slice into implementation-ready planning docs; it does not create a new top-level rollup step.

## Goal

Connect the FastAPI app from slice `110` to MongoDB using Motor, create the required indexes, and upgrade `/health` from app-only readiness to app-plus-database readiness.

## Why This Slice Exists

This slice is the first backend step that introduces a real external dependency. It establishes:

- the shared database lifecycle that later routers and services will use,
- the database handle on `app.state`,
- the canonical MongoDB index bootstrap for the platform, and
- a health contract that can support Docker and uptime monitoring.

Without this slice, later work in auth, lobby, and gameplay would each invent their own MongoDB boot sequence.

## Read First

- [development-plan/README.md](../README.md)
- [development-plan/PLAN.md](../PLAN.md)
- [step-100 README](../step-100/README.md)
- [step-110 README](../step-110/README.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [INFRA.md](../../INFRA.md)
- [AUTH.md](../../AUTH.md)

## Scope

In scope:

- Add Motor client lifecycle management
- Add database and client storage on `app.state`
- Create required indexes for `users`, `games`, `game_archives`, `audit_log`, and `sessions`
- Upgrade `/health` to report database connectivity
- Add automated unit and integration tests for the database lifecycle and health endpoint

Out of scope:

- Collection-specific repository helpers
- Auth/session query logic
- Game data persistence beyond connectivity and index creation
- Retry loops or background reconnect daemons
- MongoDB container or Compose setup beyond the smallest automation needed to test this slice

## Deliverables

The implementing agent should leave behind at least these files:

- `src/app/db.py`
- updates to `src/app/main.py`
- `src/tests/test_db.py`
- updates to `src/tests/test_health.py`

If the repo does not yet have a reusable integration harness for disposable MongoDB instances, the implementing agent may add the smallest helper script needed to make the slice signoff fully automated.

## Contract For This Slice

The finished code must satisfy all of the following:

- `init_db(settings)` creates a Motor client for `settings.MONGO_URI`
- the app stores the client and database handle on `app.state`
- `get_db()` returns the initialized database handle
- `close_db()` closes the client and clears any module-level cached handles
- the app attempts to create every required index at startup when MongoDB is reachable
- `GET /health` returns HTTP `200` with `{"status": "ok", "db": "connected"}` when MongoDB is reachable
- `GET /health` returns HTTP `503` with `{"status": "error", "db": "disconnected"}` when MongoDB is unavailable
- importing `app.main` still does not perform network I/O

## Required Reading Order For The Implementing Agent

1. Read [IMPLEMENTATION.md](./IMPLEMENTATION.md)
2. Read [TESTING.md](./TESTING.md)
3. Read [CHECKLIST.md](./CHECKLIST.md)
4. Claim slice `120` in [step-100/PROGRESS.md](../step-100/PROGRESS.md) before writing code

## Definition Of Done

This slice is done only when:

- the implementation matches [IMPLEMENTATION.md](./IMPLEMENTATION.md),
- every required automated check in [TESTING.md](./TESTING.md) passes,
- exact commands and results are recorded in [step-100/PROGRESS.md](../step-100/PROGRESS.md), and
- the database-connected and database-disconnected `/health` cases are both covered by automation.

Manual testing against a developer-started MongoDB instance is optional for debugging, but it does not count as primary signoff evidence.

## Handoff To The Next Slices

- Slice `140` can assume `MONGO_URI` is now an active dependency that the Docker stack must satisfy.
- Slice `150` can refactor the tests created here into shared fixtures, but it must preserve coverage of index creation and `/health` degradation behavior.
