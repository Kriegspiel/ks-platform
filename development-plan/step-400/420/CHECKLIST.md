# Step 420 - Move/Ask-Any/Resign Gameplay Execution API - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `420` in `step-400/PROGRESS.md`

## Implementation

- [ ] Implement move/ask-any/resign route handlers + validation ordering
- [ ] Persist move outcomes and engine-state transitions
- [ ] Keep polling projection concerns out of this slice

## Testing

- [ ] `cd src && pytest tests/test_game_routes_move.py -v`
- [ ] `cd src && pytest tests/test_game_routes_move.py --cov=app.routers.game --cov=app.services.game_service --cov-fail-under=85 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
