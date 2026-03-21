# Step 110 Checklist

Use this as the execution checklist when implementing slice `110`.

## Planning And Context

- [ ] Re-read [development-plan/README.md](../README.md)
- [ ] Re-read [development-plan/PLAN.md](../PLAN.md)
- [ ] Re-read [step-100 README](../step-100/README.md)
- [ ] Claim slice `110` in [step-100/PROGRESS.md](../step-100/PROGRESS.md)

## Files To Create

- [ ] `src/app/__init__.py`
- [ ] `src/app/config.py`
- [ ] `src/app/main.py`
- [ ] `src/app/routers/__init__.py`
- [ ] `src/app/models/__init__.py`
- [ ] `src/app/services/__init__.py`
- [ ] `src/tests/test_config.py`
- [ ] `src/tests/test_app_factory.py`
- [ ] `src/tests/test_health.py`

## Implementation Tasks

- [ ] Add `Settings` with the required defaults
- [ ] Add cached `get_settings()`
- [ ] Add a no-op async lifespan context manager
- [ ] Add `create_app(settings: Settings | None = None)`
- [ ] Add module-level `app = create_app()`
- [ ] Store settings on `app.state.settings`
- [ ] Add CORS middleware with credentials enabled
- [ ] Allow `settings.SITE_ORIGIN`
- [ ] Allow `http://localhost:8000` when `ENVIRONMENT == "development"`
- [ ] Add `GET /health`
- [ ] Keep `/health` payload exactly `{"status": "ok"}`
- [ ] Keep MongoDB out of this slice

## Automated Test Tasks

- [ ] Add tests for settings defaults
- [ ] Add tests for environment overrides
- [ ] Add tests for clearing the settings cache
- [ ] Add tests for app title and settings on app state
- [ ] Add tests proving the app factory is repeatable
- [ ] Add tests proving lifespan starts without external dependencies
- [ ] Add preflight CORS tests for allowed origins
- [ ] Add a preflight CORS test for a disallowed origin
- [ ] Add `/health` response tests

## Required Commands

- [ ] `cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py -v`
- [ ] `cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py --cov=app.config --cov=app.main --cov-fail-under=90 -v`
- [ ] `cd src && python -m compileall app tests`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Before Marking Done

- [ ] Record the exact command results in [step-100/PROGRESS.md](../step-100/PROGRESS.md)
- [ ] Confirm no test required MongoDB
- [ ] Confirm no manual smoke check is being used as the only signoff
- [ ] Leave clear handoff notes for slice `120` and slice `150`
