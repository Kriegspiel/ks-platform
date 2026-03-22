# Step 410 - Engine Adapter + Deterministic Serialization - Checklist

## Planning

- [ ] Re-read `step-400/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `410` in `step-400/PROGRESS.md`

## Implementation

- [ ] Implement adapter functions for new game/move/ask-any/projections/serialization
- [ ] Keep engine internals out of router layer
- [ ] Verify acceptance criteria contract

## Testing

- [ ] `cd src && pytest tests/test_engine_adapter.py -v`
- [ ] `cd src && pytest tests/test_engine_adapter.py --cov=app.services.engine_adapter --cov-fail-under=90 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-400/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
