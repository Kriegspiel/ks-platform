# Step 460 - Gameplay Integration + Regression Hardening - Checklist

## Planning

- [x] Re-read `step-400/README.md`
- [x] Re-read this slice `README.md`
- [x] Claim slice `460` in `step-400/PROGRESS.md`

## Implementation

- [x] Add/extend integration fixtures and gameplay regression tests
- [x] Cover lifecycle, hidden-info, authz, timeout, archive scenarios
- [x] Keep production code untouched unless test-proven fix is required

## Testing

- [x] `cd src && pytest tests/test_gameplay_integration.py tests/test_engine_adapter.py tests/test_clock_service.py -v`
- [x] `cd src && pytest tests/test_gameplay_integration.py --cov=app --cov-report=term-missing --cov-fail-under=80 -v`
- [x] `cd src && ruff check app tests`
- [x] `cd src && black --check app tests`

## Evidence + Handoff

- [x] Record command outcomes in `step-400/PROGRESS.md`
- [x] Capture blockers/follow-ups if any
- [x] Mark slice done only after automated gates pass
