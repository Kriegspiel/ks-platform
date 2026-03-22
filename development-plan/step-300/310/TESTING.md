# Step 310 - Game Domain Models and Code Generator - Testing Plan

## Integration Prerequisites

- Python dependencies installed (`src/app/requirements-dev.txt`).
- Test Mongo URI available for collision simulation tests if db access is required.
- Step 200 user/auth model tests already green on current branch baseline.

## Required Commands

```bash
cd src && pytest tests/test_game_models.py tests/test_code_generator.py -v
cd src && pytest tests/test_game_models.py tests/test_code_generator.py --cov=app.models.game --cov=app.services.code_generator --cov-fail-under=90 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Model + generator tests: PASS with zero skips under normal dev environment.
- Coverage gate: PASS >=90% across targeted modules.
- Lint/format checks: PASS.

## Runtime Smoke Checks

- Python REPL/one-liner creates sample `GameDocument` and confirms lifecycle literal rejection on invalid state.
- Manual invocation of generator emits uppercase 6-char code in allowed alphabet.

## Fail/Skip Handling Rules

- On failure: stop, capture exact traceback/output in `step-300/PROGRESS.md`, and note likely root cause.
- On intentional skip: document skip reason + prerequisite gate, then run remaining mandatory checks.
- Do not mark slice done with only manual smoke checks.
