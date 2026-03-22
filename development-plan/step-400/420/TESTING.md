# Step 420 - Move/Ask-Any/Resign Gameplay Execution API - Testing Plan

## Integration Prerequisites

- Step 410 tests passing on branch baseline.
- Test fixtures can create active game with two authenticated users.

## Required Commands

```bash
cd src && pytest tests/test_game_routes_move.py -v
cd src && pytest tests/test_game_routes_move.py --cov=app.routers.game --cov=app.services.game_service --cov-fail-under=85 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Route mutation tests: PASS, covering legal move, illegal move, out-of-turn, ask-any, resign.
- Coverage gate: PASS >=85% for targeted route/service modules touched in this slice.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
cd src && python - <<PY
print("Use existing dev script to create game + perform one move via API client; verify HTTP 200 then turn flips")
PY
```

Expected outcome: manual run confirms successful move response and turn change in persisted game.

## Fail/Skip Handling Rules

- On failing mutation test, capture failing endpoint + expected/actual status in `step-400/PROGRESS.md`.
- If coverage target is missed, log uncovered branches and planned follow-up tests.
