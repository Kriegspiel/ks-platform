# Step 210 - User Domain Models and UserService - Checklist

## Planning

- [ ] Re-read `step-200/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `210` in `step-200/PROGRESS.md`

## Implementation

- [ ] Complete in-scope file changes for slice `210`
- [ ] Validate acceptance criteria contract
- [ ] Keep out-of-scope items deferred

## Testing

- [ ] `cd src && pytest tests/test_user_models.py tests/test_user_service.py -v`
- [ ] `cd src && pytest tests/test_user_models.py tests/test_user_service.py --cov=app.models.auth --cov=app.models.user --cov=app.services.user_service --cov-fail-under=90 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes (pass/fail/skip) in `step-200/PROGRESS.md`
- [ ] Add any blocker notes or follow-up tasks
- [ ] Mark slice `{sid}` done only after automated gates pass
