# Step 600 Progress

Status: IN PROGRESS
Last Updated: 2026-03-27

## Slice Checklist

- [x] `610` Profile, history, and leaderboard API
- [x] `620` Review/replay API and React review page
- [ ] `630` React profile, history, leaderboard, settings pages
- [ ] `640` Direct join URL
- [ ] `650` Player feature integration tests

## Test Evidence

### Slice 610 (completed)
- ks-v2 PR: https://github.com/Kriegspiel/ks-v2/pull/45
- Merge commit: `24cb71e2894e32e3a965a2186e05d33c153d0122`
- `cd backend/src && ../.venv/bin/pytest tests/test_user_routes.py -v` → 1 passed
- `cd backend/src && ../.venv/bin/pytest tests/test_user_service.py -v` → 8 passed
- `cd backend/src && ../.venv/bin/pytest tests/test_player_features.py -k "profile or leaderboard or settings" -v` → 2 passed
- `cd backend/src && ../.venv/bin/pytest -q --maxfail=1 --disable-warnings` → 160 passed, 22 skipped, 1 warning
- `cd backend/src && ../.venv/bin/ruff check app tests` → pass
- Smoke check: `uvicorn app.main:app` + `curl /api/health` → HTTP 200 (`{"status":"ok","db":"connected"}`)

### Slice 620 (completed)
- ks-v2 PR: https://github.com/Kriegspiel/ks-v2/pull/46
- Merge commit: `1eda2d3e1e6b867c2a40c419873589825e76b164`
- Scope delivered:
  - `/api/game/{gameId}/moves` payload extended with per-ply `replay_fen` (`full`/`white`/`black`) and fallback replay reconstruction for legacy records.
  - `/game/:gameId/review` React page shipped with transcript rendering, ply controls (First/Prev/Next/Last), arrow-key nav, move-log jump, perspective selector, and result summary.
- Frontend checks:
  - `cd frontend && npm run test -- --run Review` → 3 passed, 0 skipped
  - `cd frontend && npm run test -- --run ChessBoard` → 6 passed, 0 skipped
  - `cd frontend && npm run test -- --run App` → 8 passed, 0 skipped
  - `cd frontend && npm run test -- --run --coverage --coverage.include=src/pages/Review.jsx Review` → `Review.jsx` 95.03% lines / 82.97% branches
  - `cd frontend && npm run lint` → pass
- Backend checks:
  - `cd backend/src && uv run pytest tests/test_game_history_routes.py tests/test_gameplay_integration.py -v` → 9 passed, 0 skipped
  - `cd backend/src && uv run pytest tests/test_game_routes_move.py::test_service_game_over_result_mapping_branches tests/test_telemetry_contracts.py::test_game_move_logging_contract -v` → 2 passed
  - `cd backend/src && uv run pytest tests -v` → 160 passed, 22 skipped, 1 warning
- CI merge gates for PR #46: backend-quality ✅, frontend-quality ✅, ops-scripts-quality ✅

## Blockers

- Slice 620: no blockers.
- Slice 630: no hard blockers; follow-on dependency is available (`/api/game/{gameId}/moves` replay contract now stable with `replay_fen`).

## Discovery Notes

- Expanded Step 600 from high-level README into a full packet: `CHECKLIST.md`, `HANDOFF.md`, and scope-based slice folders `610`-`650`.
- Standardized QA bar across slices with explicit CI merge gates and rollback-ready procedures.
- Added deterministic fixture requirements to prevent flaky ranking/pagination/replay tests.
- Sequenced work so API contract stability (`610`) lands before dependent UI (`620`-`640`) and final integration suite (`650`).

## Handoff

- Continue at Slice 630 using `step-600/630/README.md`, `IMPLEMENTATION.md`, and `TESTING.md`.
- Keep evidence logging in this file with explicit command outcomes and gate status.
