# Step 300 Progress

Status: IN PROGRESS
Last Updated: 2026-03-26

## Slice Checklist

- [x] 310 Game models, DTOs, and join-code generator
- [x] 320 GameService create/join/resign/delete lifecycle methods
- [ ] 330 Authenticated game API routes + contract errors
- [ ] 340 Lobby page + create/join/open/mine polling UX
- [ ] 350 Integration and regression verification for lifecycle rules

## Planning Packet Checklist

- [x] Slice folders 310/320/330/340/350 created
- [x] Per-slice README.md, IMPLEMENTATION.md, TESTING.md, CHECKLIST.md created
- [x] Locked lifecycle contract (waiting -> active -> completed) embedded in step + slice docs
- [x] Testing expectations include exact commands + expected pass/fail/skip semantics
- [x] Integration prerequisites + smoke checks documented per slice

## Test Evidence

- Slice 310 implemented in ks-v2 and merged via PR: https://github.com/Kriegspiel/ks-v2/pull/20
- Command evidence (rpi-server-02, ks-v2/backend/src):
  - uv run pytest tests/test_game_models.py tests/test_code_generator.py -v -> 15 passed, 0 skipped
  - uv run pytest tests/test_game_models.py tests/test_code_generator.py --cov=app.models.game --cov=app.services.code_generator --cov-fail-under=90 -v -> 15 passed, 0 skipped, coverage 99.02% (gate 90%)
  - uv run ruff check app tests -> pass
  - uv run black --check app tests -> pass
- Manual smoke checks executed:
  - GameDocument accepts waiting and rejects invalid lifecycle state paused
  - generate_game_code() emits a valid uppercase safe code B3H7Q2

- Slice 320 implemented in ks-v2 and merged via PR: https://github.com/Kriegspiel/ks-v2/pull/21
- Command evidence (rpi-server-02, ks-v2/backend/src):
  - uv run pytest tests/test_game_service.py -v -> 11 passed, 0 skipped
  - uv run pytest tests/test_game_service.py --cov=app.services.game_service --cov-fail-under=90 -v -> 11 passed, 0 skipped, coverage 97.95% (gate 90%)
  - uv run ruff check app tests -> pass
  - uv run black --check app tests -> pass
- Lifecycle guard coverage validated:
  - create/join/open/mine/get/resign/delete success paths
  - ownership/state denial paths
  - race-condition safe update/delete denial paths

## Blockers

- None for slices 310 and 320. Next slice: 330 authenticated game routes.

## Notes

- Execution agents must append exact command outputs + outcomes as each slice moves to DONE.
- Do not mark a slice complete without running TESTING.md commands or recording an explicit blocker.

## Handoff

- Continue in order 330 -> 340 -> 350.
- Favor backend completion (330) before frontend polish (340) and final verification (350).
