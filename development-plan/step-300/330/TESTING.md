# Step 330 - Authenticated Game API Surface - Testing Plan

## Integration Prerequisites

- Slices 310 and 320 complete on branch.
- Auth/session fixtures from Step 200 available in backend test harness.
- API test client supports cookie-backed authenticated requests.

## Required Commands

```bash
cd src && pytest tests/test_game_router.py -v
cd src && pytest tests/test_game_router.py tests/test_auth_router.py -v
cd src && pytest tests/test_game_router.py --cov=app.routers.game --cov-fail-under=90 -v
cd src && ruff check app tests
cd src && black --check app tests
```

## Expected Outcomes

- Router tests: PASS covering create/join/list/get/resign/delete + auth-required checks.
- Regression pairing with auth router: PASS (no Step 200 contract regressions).
- Coverage gate: PASS >=90% for game router module.
- Lint/format checks: PASS.

## Runtime Smoke Checks

- Use local server + curl/httpie to create then join game with two sessions; verify response payloads.
- Validate one representative domain error returns standardized envelope (e.g., self-join 409).

## Fail/Skip Handling Rules

- Record any auth regression immediately in `step-300/PROGRESS.md` with failing endpoint and status code mismatch.
- Skips require clear environment gating rationale (e.g., auth fixture unavailable) and remediation step.
- Do not mark complete if only happy-path API tests run.
