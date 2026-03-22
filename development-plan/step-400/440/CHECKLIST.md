# Step 440 - Clock Service + Timeout Adjudication - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `440` in `step-400/PROGRESS.md`

## Implementation

- [ ] Implement clock service methods and persistence contract
- [ ] Integrate move-time deduction + increment on successful moves
- [ ] Wire timeout completion and polling clock payload

## Testing

- [ ] `cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py -v`
- [ ] `cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py --cov=app.services.clock_service --cov=app.services.game_service --cov-fail-under=85 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
