# Step 450 - Transcript/Archive/Recent-Game Read APIs - Testing Plan

## Integration Prerequisites

- Completed-game fixtures available (resign or timeout path acceptable).
- Archive collection present in test DB.

## Required Commands

```bash
cd src && pytest tests/test_game_history_routes.py -v
cd src && pytest tests/test_game_history_routes.py --cov=app.routers.game --cov=app.services.game_service --cov-fail-under=85 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- History route tests: PASS for participant/public access matrix and archive fallback.
- Coverage gate: PASS >=85% for touched history route/service code paths.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
curl -s -b cookie.txt "http://localhost:8000/api/game/recent" | jq length
```

Expected outcome: returns JSON list length <= configured limit (default 10).

## Fail/Skip Handling Rules

- On auth mismatch failure, record expected policy vs actual HTTP status.
- If archive fixture setup fails, capture setup blocker and continue with active-game permission tests.
