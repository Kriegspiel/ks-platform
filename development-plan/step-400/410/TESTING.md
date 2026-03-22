# Step 410 - Engine Adapter + Deterministic Serialization - Testing Plan

## Integration Prerequisites

- Python dev dependencies installed from `src/app/requirements-dev.txt`.
- `kriegspiel` package importable in test environment.

## Required Commands

```bash
cd src && pytest tests/test_engine_adapter.py -v
cd src && pytest tests/test_engine_adapter.py --cov=app.services.engine_adapter --cov-fail-under=90 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Engine adapter tests: PASS with zero unexpected skips.
- Coverage gate: PASS >=90% for `app.services.engine_adapter`.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
cd src && python - <<PY
from app.services.engine_adapter import create_new_game, attempt_move

g = create_new_game(any_rule=True)
print(attempt_move(g, "e2e4")["move_done"])
PY
```

Expected output includes `True`.

## Fail/Skip Handling Rules

- On failure: log exact failing assertion and stack trace summary in `step-400/PROGRESS.md`.
- On skip: capture why dependency is unavailable and run remaining required checks.
- Do not mark slice complete with only smoke checks.
