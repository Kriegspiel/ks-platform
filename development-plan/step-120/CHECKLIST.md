# Step 120 Checklist

Use this as the execution checklist when implementing slice `120`.

## Planning And Context

- [ ] Re-read [development-plan/README.md](../README.md)
- [ ] Re-read [development-plan/PLAN.md](../PLAN.md)
- [ ] Re-read [step-100 README](../step-100/README.md)
- [ ] Re-read [step-110 README](../step-110/README.md)
- [ ] Claim slice `120` in [step-100/PROGRESS.md](../step-100/PROGRESS.md)

## Files To Create Or Modify

- [ ] `src/app/db.py`
- [ ] `src/app/main.py`
- [ ] `src/tests/test_db.py`
- [ ] `src/tests/test_health.py`
- [ ] smallest automation helper for Mongo integration, if needed

## Implementation Tasks

- [ ] Add Motor client lifecycle helpers
- [ ] Resolve the database name from `MONGO_URI`
- [ ] Create every required index from `DATA_MODEL.md`
- [ ] Store database readiness state on `app.state`
- [ ] Wire startup and shutdown into the existing lifespan
- [ ] Upgrade `/health` to return connected and disconnected payloads
- [ ] Keep import-time app construction free of network I/O

## Automated Test Tasks

- [ ] Add unit coverage for `init_db()`
- [ ] Add unit coverage for `get_db()`
- [ ] Add unit coverage for `close_db()`
- [ ] Add health tests for connected and disconnected cases
- [ ] Add automated real-Mongo integration coverage
- [ ] Ensure the Mongo integration run is non-interactive

## Required Commands

- [ ] `cd src && pytest tests/test_db.py tests/test_health.py -v`
- [ ] `cd src && pytest tests/test_db.py tests/test_health.py --cov=app.db --cov=app.main --cov-fail-under=90 -v`
- [ ] `cd src && python -m compileall app tests`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`
- [ ] automated integration wrapper for disposable MongoDB

## Before Marking Done

- [ ] Record exact command results in [step-100/PROGRESS.md](../step-100/PROGRESS.md)
- [ ] Confirm all required indexes are asserted by tests
- [ ] Confirm `/health` covers both 200 and 503 cases in automation
- [ ] Leave handoff notes for slices `140` and `150`
