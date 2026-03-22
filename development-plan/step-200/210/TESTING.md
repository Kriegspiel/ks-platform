# Step 210 - User Domain Models and UserService - Testing Plan

## Integration Prerequisites

- Mongo test instance reachable (`MONGO_URI` points to test DB).
- `users` unique indexes exist (username + email).
- Python deps installed from `src/app/requirements-dev.txt`.

## Required Commands

```bash
cd src && pytest tests/test_user_models.py tests/test_user_service.py -v
cd src && pytest tests/test_user_models.py tests/test_user_service.py --cov=app.models.auth --cov=app.models.user --cov=app.services.user_service --cov-fail-under=90 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Unit/model tests: PASS with zero skips.
- Coverage gate: PASS >=90%.
- Lint/format checks: PASS.

## Runtime Smoke Checks

- python one-liner to create hash and verify true/false roundtrip.
- Manual DB inspect confirms canonical lowercase username and non-plaintext password_hash.

## Fail/Skip Handling Rules

- If a command fails: stop and record exact failure output + suspected root cause in `step-200/PROGRESS.md`.
- If a command is intentionally skipped: record the explicit skip gate (env var or prerequisite) and confirm remaining mandatory coverage still passed.
- Do not mark this slice complete on manual smoke checks alone.
