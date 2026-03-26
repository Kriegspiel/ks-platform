# Step 440 - Clock Service + Timeout Adjudication - Checklist

## Planning

- [x] Re-read `step-400/README.md`
- [x] Re-read this slice `README.md`
- [x] Claim slice `440` in `step-400/PROGRESS.md`

## Implementation

- [x] Implement clock service methods and persistence contract
- [x] Integrate move-time deduction + increment on successful moves
- [x] Wire timeout completion and polling clock payload

## Testing

- [x] `cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py -v`
- [x] `cd src && pytest tests/test_clock_service.py tests/test_game_timeouts.py --cov=app.services.clock_service --cov=app.services.game_service --cov-fail-under=85 -v`
- [x] `cd src && ruff check app tests`
- [x] `cd src && black --check app tests`

## Evidence + Handoff

- [x] Record command outcomes in `step-400/PROGRESS.md`
- [x] Capture blockers/follow-ups if any
- [x] Mark slice done only after automated gates pass
