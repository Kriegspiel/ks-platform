# Step 400 Progress

Status: IN PROGRESS
Last Updated: 2026-03-26

## Slice Checklist

- [x] `410` Engine adapter + serialization primitives
- [x] `420` Move/ask-any/resign execution API
- [x] `430` Polling state endpoint + hidden-information shaping
- [ ] `440` Clock service + timeout adjudication integration
- [ ] `450` Transcript/archive/recent-game APIs
- [ ] `460` Gameplay integration/regression verification

## Planning Packet Checklist

- [x] Slice folders `410/420/430/440/450/460` created
- [x] Per-slice `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, `CHECKLIST.md` created
- [x] Scope rationale documented for 6-slice breakdown
- [x] Testing expectations include exact commands + expected pass/fail/skip semantics
- [x] Runtime smoke checks included where backend behavior is stateful/time-based

## Test Evidence

### Slice 410 (ks-v2 PR #28)
- Branch: `step-400-slice-410-engine-adapter`
- Merge commit: `e479c049bd21ccf38420e5b404eb93a2c066f5a3`
- Required commands executed in `ks-v2/backend/src`:
  - `../.venv/bin/pytest tests/test_engine_adapter.py -v` → **PASS** (5 passed, 0 skipped)
  - `../.venv/bin/pytest tests/test_engine_adapter.py --cov=app.services.engine_adapter --cov-fail-under=90 -v` → **PASS** (5 passed, 0 skipped, coverage 92%, gate >=90% passed)
  - `../.venv/bin/ruff check app tests` → **PASS**
  - `../.venv/bin/black --check app tests` → **PASS**
- Runtime smoke:
  - `attempt_move(create_new_game(any_rule=True), "e2e4")["move_done"]` → `True`

### Slice 420 (ks-v2 PR #29)
- Branch: `step-400-slice-420-execution-api`
- PR: https://github.com/Kriegspiel/ks-v2/pull/29
- Merge commit: `ae2a174753e37be0032b92889a2ceb1f137eea01`
- Required commands executed in `ks-v2/backend/src`:
  - `../.venv/bin/pytest tests/test_game_routes_move.py -v` → **PASS** (16 passed, 0 skipped)
  - `../.venv/bin/pytest tests/test_game_routes_move.py --cov=app.routers.game --cov=app.services.game_service --cov-fail-under=85 -v` → **PASS** (16 passed, 0 skipped, total coverage 87.16%, gate >=85% passed)
  - `../.venv/bin/ruff check app tests` → **PASS**
  - `../.venv/bin/black --check app tests` → **PASS**
- Delivered scope:
  - Added gameplay mutation endpoints: `POST /api/game/{id}/move` and `POST /api/game/{id}/ask-any`
  - Wired service execution to Slice-410 adapter contracts (`attempt_move`, `ask_any`, serialized engine state)
  - Added strict participant/state/turn guards with deterministic error mapping (`FORBIDDEN`, `GAME_NOT_ACTIVE`, `NOT_YOUR_TURN`)
  - Persisted move history and engine-state transitions, including terminal outcome signaling and active resign completion

### Slice 430 (ks-v2 PR #30)
- Branch: `step-400-slice-430-polling-projection`
- PR: https://github.com/Kriegspiel/ks-v2/pull/30
- Merge commit: `28b100bf13beb9302a2815e83f0f5cc628804927`
- Required commands executed in `ks-v2/backend/src`:
  - `../.venv/bin/pytest tests/test_game_state_polling.py -v` → **PASS** (9 passed, 0 skipped)
  - `../.venv/bin/pytest tests/test_game_state_polling.py --cov=app.routers.game --cov=app.services.state_projection --cov-fail-under=85 -v` → **PASS** (9 passed, 0 skipped, total coverage 87.60%, gate >=85% passed)
  - `../.venv/bin/ruff check app tests` → **PASS**
  - `../.venv/bin/black --check app tests` → **PASS**
- Delivered scope:
  - Added polling endpoint `GET /api/game/{game_id}/state` with participant-only authorization and standardized error mapping.
  - Added projection helpers for hidden-information-safe FEN, deterministic action lists, and public-only referee logs.
  - Added state polling tests for white/black visibility, non-participant rejection, completed-game reveal, and route-level error behavior.


## Blockers

- None blocking slice 440 start.

## Notes

- Slice 410 delivered engine adapter primitives only; no route/service orchestration, polling API shaping, or clock integration was introduced.
- Slice 420 intentionally stayed within mutation execution + persistence; polling projection remains scoped to slice 430.
- Clock/time-based tests should use deterministic time control (freezegun/monkeypatch) where available to avoid flaky CI outcomes.

## Handoff

- Continue execution order: `440 -> 450 -> 460`.
- Keep backend-first sequencing; slice `460` remains verification-only and should not introduce contract drift.
