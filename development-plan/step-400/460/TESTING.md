# Step 460 - Gameplay Integration + Regression Hardening - Testing Plan

## Integration Prerequisites

- Slices 410-450 implemented and green.
- Test DB fixtures support multi-user auth sessions and archive records.

## Required Commands

```bash
cd src && pytest tests/test_gameplay_integration.py tests/test_engine_adapter.py tests/test_clock_service.py -v
cd src && pytest tests/test_gameplay_integration.py --cov=app --cov-report=term-missing --cov-fail-under=80 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Integration suite: PASS for lifecycle, hidden-info, authz, timeout, archive paths.
- Coverage gate: PASS >=80% for app package in Step-400-focused run.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
# two authenticated sessions
curl -s -b white_cookie.txt -X POST "http://localhost:8000/api/game/<id>/move" -H "Content-Type: application/json" -d {uci:e2e4} | jq
curl -s -b black_cookie.txt "http://localhost:8000/api/game/<id>/state" | jq clock
```

Expected outcome: move succeeds for active player, polling payload for opponent remains hidden-information-safe and clock is present.

## Fail/Skip Handling Rules

- On any hidden-information regression, stop and file blocker in `step-400/PROGRESS.md`.
- On fixture-dependent skips, document missing prerequisite and rerun unaffected suites.
