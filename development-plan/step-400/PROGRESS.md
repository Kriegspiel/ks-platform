# Step 400 Progress

Status: IN PROGRESS
Last Updated: 2026-03-26

## Slice Checklist

- [x] `410` Engine adapter + serialization primitives
- [ ] `420` Move/ask-any/resign execution API
- [ ] `430` Polling state endpoint + hidden-information shaping
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

## Blockers

- None for starting slice 420.

## Notes

- Slice 410 delivered engine adapter primitives only; no route/service orchestration, polling API shaping, or clock integration was introduced.
- Clock/time-based tests should use deterministic time control (freezegun/monkeypatch) where available to avoid flaky CI outcomes.

## Handoff

- Continue execution order: `420 -> 430 -> 440 -> 450 -> 460`.
- Keep backend-first sequencing; slice `460` remains verification-only and should not introduce contract drift.
