# Step 110 - Backend App Factory, Settings, Health Endpoint

This folder is the detailed execution packet for slice `110` from [step-100](../README.md).

Canonical status for this slice still lives in [step-100/PROGRESS.md](../PROGRESS.md). This folder expands the slice into implementation-ready planning docs; it does not create a new top-level rollup step.

## Goal

Create the first runnable FastAPI application shell for the platform, with:

- a testable app factory,
- environment-backed settings,
- a no-op lifespan hook that can accept database wiring in slice `120`,
- CORS configured for the SPA/dev workflow, and
- a minimal `/health` endpoint.

## Why This Slice Exists

Everything else in the backend depends on this slice establishing a stable import path and startup shape:

- slice `120` needs a lifespan hook and app state to attach MongoDB,
- slice `150` needs an app factory that test fixtures can instantiate repeatedly,
- later routers need a package layout that already exists,
- Docker and CI need an importable ASGI app that boots without external services.

## Read First

- [development-plan/README.md](../../README.md)
- [development-plan/PLAN.md](../../PLAN.md)
- [step-100 README](../README.md)
- [ARCHITECTURE.md](../../../ARCHITECTURE.md)
- [INFRA.md](../../../INFRA.md)
- [AUTH.md](../../../AUTH.md)

## Scope

This slice covers only the backend scaffold needed to boot an app cleanly.

In scope:

- Create the initial Python package structure under `src/app/`
- Add `Settings` with the required defaults
- Add `create_app()` and module-level `app`
- Add an async lifespan context manager that does not touch MongoDB yet
- Add CORS middleware for the frontend/dev workflow
- Add `/health` returning `{"status": "ok"}`
- Add automated tests for config loading, app construction, CORS, and health behavior

Out of scope:

- Database connections or health pinging MongoDB
- Router registration beyond what is needed for `/health`
- Logging setup
- Auth/session behavior
- Docker or CI implementation details outside what is needed to define automated checks

## Deliverables

The implementing agent should leave behind at least these files:

- `src/app/__init__.py`
- `src/app/config.py`
- `src/app/main.py`
- `src/app/routers/__init__.py`
- `src/app/models/__init__.py`
- `src/app/services/__init__.py`
- `src/tests/test_config.py`
- `src/tests/test_app_factory.py`
- `src/tests/test_health.py`

If `src/tests/` fixtures do not exist yet, the implementing agent may add only the smallest shared test helpers needed to keep this slice fully automated. Broader reusable harness work still belongs to slice `150`.

## Contract For This Slice

The finished code must satisfy all of the following:

- `from app.main import app` succeeds without requiring MongoDB or any network dependency
- `app.title == "Kriegspiel Chess API"`
- `create_app()` can be called repeatedly in tests without cross-test contamination
- `app.state.settings` exists and contains the settings instance used to build the app
- `GET /health` returns HTTP `200` with exactly `{"status": "ok"}`
- CORS allows the configured site origin and supports credentials
- Importing `app.main` does not start background tasks or connect to external systems

## Required Reading Order For The Implementing Agent

1. Read [IMPLEMENTATION.md](./IMPLEMENTATION.md)
2. Read [TESTING.md](./TESTING.md)
3. Read [CHECKLIST.md](./CHECKLIST.md)
4. Claim slice `110` in [step-100/PROGRESS.md](../PROGRESS.md) before writing code

## Definition Of Done

This slice is done only when:

- the implementation matches [IMPLEMENTATION.md](./IMPLEMENTATION.md),
- every required automated check in [TESTING.md](./TESTING.md) passes,
- exact test commands and results are recorded in [step-100/PROGRESS.md](../PROGRESS.md), and
- no manual browser, `curl`, or ad-hoc `uvicorn` smoke test is used as the sole signoff evidence.

Manual smoke checks are optional for local debugging, but they do not satisfy completion on their own.

## Handoff To The Next Slices

- Slice `120` can assume `create_app()` and lifespan already exist, and should extend them rather than rewriting them.
- Slice `150` can either keep the tests created here or fold them into broader shared fixtures, but it must preserve their assertions.
