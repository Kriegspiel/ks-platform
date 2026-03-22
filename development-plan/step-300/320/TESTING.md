# Step 320 - GameService Lifecycle Operations - Testing Plan

## Integration Prerequisites

- Slice 310 completed and merged on working branch.
- Test Mongo database reachable and isolated per test run.
- Factory fixtures for at least two users available (creator + opponent).

## Required Commands

```bash
cd src && pytest tests/test_game_service.py -v
cd src && pytest tests/test_game_service.py --cov=app.services.game_service --cov-fail-under=90 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Service tests: PASS, with explicit assertions for all guarded failure paths.
- Coverage gate: PASS >=90% for `game_service`.
- Lint/format checks: PASS.

## Runtime Smoke Checks

- Manual script creates game, joins with second user, resigns, confirms state sequence in DB (`waiting -> active -> completed`).
- Manual delete smoke check verifies only creator can delete waiting game.

## Fail/Skip Handling Rules

- Failures must be recorded with command + output excerpt + suspect function branch.
- Any skipped test requires explicit gate reason and compensating validation notes.
- Slice cannot be marked done if transition denial-path assertions are missing.
