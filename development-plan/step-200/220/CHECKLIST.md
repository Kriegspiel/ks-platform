# Step 220 - Session Service, Auth Dependency, and Auth Router - Checklist

## Planning

- [ ] Re-read `step-200/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `220` in `step-200/PROGRESS.md`

## Implementation

- [ ] Complete in-scope file changes for slice `220`
- [ ] Validate acceptance criteria contract
- [ ] Keep out-of-scope items deferred

## Testing

- [ ] `cd src && pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py -v`
- [ ] `cd src && pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py --cov=app.routers.auth --cov=app.services.session_service --cov=app.dependencies --cov-fail-under=90 -v`
- [ ] `cd src && python -m compileall app tests`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes (pass/fail/skip) in `step-200/PROGRESS.md`
- [ ] Add any blocker notes or follow-up tasks
- [ ] Mark slice `{sid}` done only after automated gates pass
