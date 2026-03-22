# Step 250 - Auth Integration Verification and Regression Guardrails - Checklist

## Planning

- [ ] Re-read `step-200/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `250` in `step-200/PROGRESS.md`

## Implementation

- [ ] Complete in-scope file changes for slice `250`
- [ ] Validate acceptance criteria contract
- [ ] Keep out-of-scope items deferred

## Testing

- [ ] `cd src && pytest tests/test_auth.py tests/test_password.py -v`
- [ ] `cd src && pytest tests/test_auth.py tests/test_password.py --cov=app.routers.auth --cov=app.services.user_service --cov=app.services.session_service --cov-fail-under=90 -v`
- [ ] `cd src && pytest tests/test_auth.py -k 'me or login or register' -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes (pass/fail/skip) in `step-200/PROGRESS.md`
- [ ] Add any blocker notes or follow-up tasks
- [ ] Mark slice `{sid}` done only after automated gates pass
