# Step 430 - Polling Game-State API + Hidden-Information Projection - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `430` in `step-400/PROGRESS.md`

## Implementation

- [ ] Implement polling endpoint + DTO
- [ ] Enforce participant-only access and hidden-information projection
- [ ] Compute `possible_actions` deterministically

## Testing

- [ ] `cd src && pytest tests/test_game_state_polling.py -v`
- [ ] `cd src && pytest tests/test_game_state_polling.py --cov=app.routers.game --cov=app.services.state_projection --cov-fail-under=85 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
