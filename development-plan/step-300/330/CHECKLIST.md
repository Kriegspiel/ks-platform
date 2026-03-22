# Step 330 - Authenticated Game API Surface - Checklist

## Planning

- [ ] Re-read `step-300/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `330` in `step-300/PROGRESS.md`

## Implementation

- [ ] Implement router endpoints and app registration
- [ ] Enforce auth dependency on all routes
- [ ] Map domain errors to contract-compliant responses

## Testing

- [ ] `cd src && pytest tests/test_game_router.py -v`
- [ ] `cd src && pytest tests/test_game_router.py tests/test_auth_router.py -v`
- [ ] `cd src && pytest tests/test_game_router.py --cov=app.routers.game --cov-fail-under=90 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record outcomes in `step-300/PROGRESS.md`
- [ ] Capture any contract deviations or TODOs
- [ ] Mark slice done only after automated gates pass
