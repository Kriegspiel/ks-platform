# Step 450 - Transcript/Archive/Recent-Game Read APIs - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `450` in `step-400/PROGRESS.md`

## Implementation

- [ ] Implement game-or-archive lookup helper
- [ ] Add transcript + recent routes with visibility rules
- [ ] Keep response schemas consistent across active/archive source

## Testing

- [ ] `cd src && pytest tests/test_game_history_routes.py -v`
- [ ] `cd src && pytest tests/test_game_history_routes.py --cov=app.routers.game --cov=app.services.game_service --cov-fail-under=85 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
