# Step 440 - Clock Service + Timeout Adjudication - Testing Plan

## Integration Prerequisites

- Step 420/430 contracts implemented and green.
- Test harness supports deterministic time controls (e.g., freezegun or monkeypatch).

## Required Commands

```bash
cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py -v
cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py --cov=app.services.clock_service --cov=app.services.game_service --cov-fail-under=85 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Clock/timeout tests: PASS, including decrement, increment, timeout transition cases.
- Coverage gate: PASS >=85% for targeted service modules.
- Lint/format checks: PASS.

## Runtime Smoke Checks

```bash
cd src && python - <<PY
print("Manual smoke: run local game, wait ~3-5s before move, confirm remaining time decreases in next poll")
PY
```

Expected outcome: observed remaining time for active color decreases between polls, then stabilizes after turn switch.

## Fail/Skip Handling Rules

- If time-based test flakes, capture timestamps and repro details before rerun.
- Do not silently disable timeout assertions; document any temporary xfail with reason and follow-up owner.
