# Step 310 - Game Domain Models and Code Generator - Checklist

## Planning

- [x] Re-read `step-300/README.md`
- [x] Re-read this slice `README.md`
- [x] Claim slice `310` in `step-300/PROGRESS.md`

## Implementation

- [x] Implement in-scope model + generator files
- [x] Validate acceptance criteria contract
- [x] Keep service/router/frontend changes out of this slice

## Testing

- [x] `cd src && pytest tests/test_game_models.py tests/test_code_generator.py -v`
- [x] `cd src && pytest tests/test_game_models.py tests/test_code_generator.py --cov=app.models.game --cov=app.services.code_generator --cov-fail-under=90 -v`
- [x] `cd src && ruff check app tests`
- [x] `cd src && black --check app tests`

## Evidence + Handoff

- [x] Record command outcomes in `step-300/PROGRESS.md`
- [x] Capture blockers/follow-ups if any
- [x] Mark slice done only after automated gates pass
