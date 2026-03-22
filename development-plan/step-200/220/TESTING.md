# Step 220 - Session Service, Auth Dependency, and Auth Router - Testing Plan

## Integration Prerequisites

- Slice 210 complete and merged in working tree.
- Test Mongo reachable and cleanup fixture enabled.
- Time-sensitive session tests pin/freeze clock or assert via bounded window.

## Required Commands

```bash
cd src && pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py -v
cd src && pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py --cov=app.routers.auth --cov=app.services.session_service --cov=app.dependencies --cov-fail-under=90 -v
cd src && python -m compileall app tests
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Auth/service tests: PASS; integration-only cases may be SKIP when `RUN_MONGO_INTEGRATION!=1` (must be explicit).
- Compile/lint/format: PASS.

## Runtime Smoke Checks

- curl register, then /auth/me with cookie, then logout and re-check /auth/me => 401.
- Expired session document returns 401 and is treated as unauthenticated.

## Fail/Skip Handling Rules

- If a command fails: stop and record exact failure output + suspected root cause in `step-200/PROGRESS.md`.
- If a command is intentionally skipped: record the explicit skip gate (env var or prerequisite) and confirm remaining mandatory coverage still passed.
- Do not mark this slice complete on manual smoke checks alone.
