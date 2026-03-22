# Step 460 - Gameplay Integration + Regression Hardening - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `460` in `step-400/PROGRESS.md`

## Implementation

- [ ] Add/extend integration fixtures and gameplay regression tests
- [ ] Cover lifecycle, hidden-info, authz, timeout, archive scenarios
- [ ] Keep production code untouched unless test-proven fix is required

## Testing

- [ ] `cd src && pytest tests/test_gameplay_integration.py tests/test_engine_adapter.py tests/test_clock_service.py -v`
- [ ] `cd src && pytest tests/test_gameplay_integration.py --cov=app --cov-report=term-missing --cov-fail-under=80 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
