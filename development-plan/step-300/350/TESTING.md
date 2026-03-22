# Step 350 - Lifecycle Integration Verification and Hardening - Testing Plan

## Integration Prerequisites

- Slices 310-340 merged into current working branch.
- Backend + frontend environments runnable locally with auth/session flow operational.
- Clean test DB state before integration run.

## Required Commands

```bash
cd src && pytest tests/test_game_lifecycle.py -v
cd src && pytest tests/test_game_lifecycle.py tests/test_game_router.py tests/test_auth_router.py -v
cd src && pytest tests/test_game_lifecycle.py --cov=app.routers.game --cov=app.services.game_service --cov=app.models.game --cov-fail-under=90 -v
cd frontend && npm run test -- Lobby App
cd frontend && npm run lint && npm run build
```

## Expected Outcomes

- Lifecycle integration tests: PASS with explicit state-transition and denial-path assertions.
- Cross-suite regression run: PASS (no auth/session regressions).
- Coverage gate: PASS >=90% across targeted Step 300 backend modules.
- Frontend validation commands: PASS, or explicitly documented skip gate with manual evidence fallback.

## Runtime Smoke Checks

- Two-user manual smoke: create, join, active visibility, resign completion state.
- Unauthorized request smoke: confirm at least one protected endpoint returns 401.
- Waiting-game delete smoke: creator allowed, non-creator denied.

## Fail/Skip Handling Rules

- Any failure blocks Step 300 DONE status until resolved or explicitly waived with owner signoff.
- For skipped frontend automation, record reason + manual smoke transcript summary.
- Do not set step `DONE` without command evidence for backend lifecycle suite.
