# Step 150 Checklist

Use this as the execution checklist when implementing slice `150`.

## Planning And Context

- [ ] Re-read [development-plan/README.md](../../README.md)
- [ ] Re-read [development-plan/PLAN.md](../../PLAN.md)
- [ ] Re-read [step-100 README](../README.md)
- [ ] Re-read [step-110 README](../110/README.md)
- [ ] Re-read [step-120 README](../120/README.md)
- [ ] Claim slice `150` in [step-100/PROGRESS.md](../PROGRESS.md)

## Files To Create Or Update

- [ ] `src/tests/__init__.py`
- [ ] `src/tests/conftest.py`
- [ ] `src/tests/test_health.py`
- [ ] `pyproject.toml`
- [ ] earlier backend tests that should move onto shared fixtures

## Implementation Tasks

- [ ] Add dedicated test settings fixture
- [ ] Add app factory fixture
- [ ] Add async client fixture
- [ ] Add test database cleanup fixture
- [ ] Move health smoke coverage onto the shared harness
- [ ] Add pytest, black, and ruff configuration to `pyproject.toml`

## Automated Verification Tasks

- [ ] Run the backend pytest suite
- [ ] Run backend coverage
- [ ] Run `compileall`
- [ ] Run `ruff`
- [ ] Run `black --check`
- [ ] Confirm shared fixtures are actually exercised by the tests

## Required Commands

- [ ] `cd src && pytest tests -v`
- [ ] `cd src && pytest tests --cov=app --cov-report=xml -v`
- [ ] `cd src && python -m compileall app tests`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Before Marking Done

- [ ] Record exact command results in [step-100/PROGRESS.md](../PROGRESS.md)
- [ ] Confirm the suite uses `kriegspiel_test` or equivalent isolated DB
- [ ] Confirm the async client does not require `uvicorn`
- [ ] Leave handoff notes for later backend slices
