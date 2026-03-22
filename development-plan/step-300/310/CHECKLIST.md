# Step 310 - Game Domain Models and Code Generator - Checklist

## Planning

- [ ] Re-read `step-300/README.md`
- [ ] Re-read this slice `README.md`
- [ ] Claim slice `310` in `step-300/PROGRESS.md`

## Implementation

- [ ] Implement in-scope model + generator files
- [ ] Validate acceptance criteria contract
- [ ] Keep service/router/frontend changes out of this slice

## Testing

- [ ] `cd src && pytest tests/test_game_models.py tests/test_code_generator.py -v`
- [ ] `cd src && pytest tests/test_game_models.py tests/test_code_generator.py --cov=app.models.game --cov=app.services.code_generator --cov-fail-under=90 -v`
- [ ] `cd src && ruff check app tests`
- [ ] `cd src && black --check app tests`

## Evidence + Handoff

- [ ] Record command outcomes in `step-300/PROGRESS.md`
- [ ] Capture blockers/follow-ups if any
- [ ] Mark slice done only after automated gates pass
