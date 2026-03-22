# Step 320 - GameService Lifecycle Operations - Checklist

## Planning

- [ ] Re-read `step-300/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `320` in `step-300/PROGRESS.md`

## Implementation

- [ ] Implement GameService lifecycle methods in scope
- [ ] Enforce all state/ownership guards
- [ ] Keep router/frontend changes deferred

## Testing

- [ ] `cd src && pytest tests/test_game_service.py -v`
- [ ] `cd src && pytest tests/test_game_service.py --cov=app.services.game_service --cov-fail-under=90 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record outcomes in `step-300/PROGRESS.md`
- [ ] Note unresolved risks/blockers
- [ ] Mark slice done only after gates pass
