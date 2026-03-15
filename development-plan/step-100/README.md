# Step 100 - Foundation and Scaffold

## Goal

Create the runnable project skeleton and developer workflow foundation for the MVP.

## Read First

- [README.md](../../README.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [INFRA.md](../../INFRA.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- None

## Task Slices

- `100.1` Create the `src/app` package structure, settings/config, app factory, and `/health` endpoint.
- `100.2` Wire MongoDB startup/shutdown lifecycle and shared dependencies.
- `100.3` Add initial local development plumbing: `.env.example`, Dockerfile, Docker Compose, and NGINX/Mongo stubs in the expected layout.
- `100.4` Add the first smoke tests and a minimal CI path for this scaffold.

## Required Tests Before Done

- Run the narrowest scaffold tests added in this step.
- Verify the app starts locally.
- Verify the health endpoint responds successfully.
- Verify Docker configuration parses cleanly.

## Exit Criteria

- The project layout matches the agreed `src/` structure.
- `cd src && uvicorn app.main:app` starts successfully.
- The health endpoint works.
- Mongo wiring is present and testable.
- Smoke tests exist and pass.

## Out of Scope

- Registration/login behavior
- Game creation/join logic
- WebSocket gameplay
