# Step 350 - Lifecycle Integration Verification and Hardening - Checklist

## Planning

- [ ] Re-read `step-300/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `350` in `step-300/PROGRESS.md`

## Implementation

- [ ] Execute full verification matrix
- [ ] Resolve or document discovered regressions
- [ ] Keep scope to validation/hardening (no unrelated feature work)

## Testing

- [ ] `cd src && pytest tests/test_game_lifecycle.py -v`
- [ ] `cd src && pytest tests/test_game_lifecycle.py tests/test_game_router.py tests/test_auth_router.py -v`
- [ ] `cd src && pytest tests/test_game_lifecycle.py --cov=app.routers.game --cov=app.services.game_service --cov=app.models.game --cov-fail-under=90 -v`
- [ ] `cd frontend && npm run test -- Lobby App`
- [ ] `cd frontend && npm run lint && npm run build`

## Evidence + Handoff

- [ ] Record pass/fail/skip counts in `step-300/PROGRESS.md`
- [ ] Update `step-300/HANDOFF.md` with final readiness notes
- [ ] Mark slice done only after required gates pass
