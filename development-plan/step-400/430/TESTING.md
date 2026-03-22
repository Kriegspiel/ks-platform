# Step 430 - Polling Game-State API + Hidden-Information Projection - Testing Plan

## Integration Prerequisites

- Step 420 mutation endpoints available to generate move history fixtures.
- Test users/fixtures support participant and non-participant identities.

## Required Commands

```bash
cd src && pytest tests/test_game_state_polling.py -v
cd src && pytest tests/test_game_state_polling.py --cov=app.routers.game --cov=app.services.state_projection --cov-fail-under=85 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Polling tests: PASS for white/black projection correctness and permission checks.
- Coverage gate: PASS >=85% across route + projection modules touched.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
# terminal A
cd src && uvicorn app.main:app --reload

# terminal B
curl -s -b cookie.txt "http://localhost:8000/api/game/<game_id>/state" | jq possible_actions
```

Expected outcome: payload returns quickly, includes expected turn/actions for requesting player.

## Fail/Skip Handling Rules

- On hidden-information leak failure, log leaked field and expected redaction behavior before proceeding.
- Skip only when fixture setup blocked; include actionable unblock requirement.
