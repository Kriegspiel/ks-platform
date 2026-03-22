# Step 250 - Auth Integration Verification and Regression Guardrails - Testing Plan

## Integration Prerequisites

- Mongo integration test DB reachable and isolated.
- Session expiry tests control time or set crafted expiry timestamps.
- Cleanup fixture drops test DB after runs.

## Required Commands

```bash
cd src && pytest tests/test_auth.py tests/test_password.py -v
cd src && pytest tests/test_auth.py tests/test_password.py --cov=app.routers.auth --cov=app.services.user_service --cov=app.services.session_service --cov-fail-under=90 -v
cd src && pytest tests/test_auth.py -k 'me or login or register' -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Primary auth suite: PASS.
- If optional integration env variable missing, explicitly-marked integration tests may be SKIP; unit-level auth contract tests must still PASS.
- Coverage/lint/format gates: PASS.

## Runtime Smoke Checks

- Terminal smoke: register/login/me/logout sequence yields 201->200->200->200, then 401 for me after logout.
- Mongo smoke: session document created on register/login and deleted on logout.

## Fail/Skip Handling Rules

- If a command fails: stop and record exact failure output + suspected root cause in `step-200/PROGRESS.md`.
- If a command is intentionally skipped: record the explicit skip gate (env var or prerequisite) and confirm remaining mandatory coverage still passed.
- Do not mark this slice complete on manual smoke checks alone.
