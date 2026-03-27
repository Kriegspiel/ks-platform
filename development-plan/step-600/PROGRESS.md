# Step 600 Progress

Status: DONE
Last Updated: 2026-03-27

## Slice Checklist

- [x] `610` Profile, history, and leaderboard API
- [x] `620` Review/replay API and React review page
- [x] `630` React profile, history, leaderboard, settings pages
- [x] `640` Direct join URL
- [x] `650` Player feature integration tests

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


### Slice 630 (completed)
- ks-v2 PR: https://github.com/Kriegspiel/ks-v2/pull/51
- Merge commit: `0843ddf00189522b655cb33b6417e7de337e279b`
- Scope delivered:
  - Added React pages/routes for `/user/:username`, `/user/:username/games`, `/leaderboard`, and auth-protected `/settings`.
  - Wired `frontend/src/services/api.js` with `userApi.getProfile`, `getGameHistory`, `updateSettings`, `getLeaderboard` against slice-610/620 contracts.
  - Implemented responsive tables/cards/forms plus empty/error/success UX and review/profile cross-linking.
- Frontend checks:
  - `cd frontend && npm run test -- --run Profile GameHistory Leaderboard Settings` → 12 passed, 0 skipped
  - `cd frontend && npm run test -- --run --coverage --coverage.include=src/pages/Profile.jsx --coverage.include=src/pages/GameHistory.jsx --coverage.include=src/pages/Leaderboard.jsx --coverage.include=src/pages/Settings.jsx Profile GameHistory Leaderboard Settings` → 12 passed, 0 skipped; combined coverage 99.06% lines / 77.77% branches
  - `cd frontend && npm run test -- --run api Profile GameHistory Leaderboard Settings` → 25 passed, 0 skipped
  - `cd frontend && npm run test -- --run App` → 8 passed, 0 skipped
  - `cd frontend && npm run lint` → pass
  - `cd frontend && npm run build` → pass
- CI merge gates for PR #51: backend-quality ✅, frontend-quality ✅, ops-scripts-quality ✅

### Slice 640 (completed)
- ks-v2 PR: https://github.com/Kriegspiel/ks-v2/pull/52
- Merge commit: `e1825842cc0e1fef4f04ea8ed3bd03e68b9b6829`
- Scope delivered:
  - Added `/join/:gameCode` route and join page with one-shot auto-join behavior.
  - Unauthenticated joins redirect to login with preserved return path.
  - Invalid/full join responses render actionable error with lobby recovery link.
  - Lobby now surfaces shareable join URL after game creation.
- Validation checks:
  - `cd frontend && npm run test -- --run Join Lobby` → 11 passed
  - `cd frontend && npm run test -- --coverage --coverage.include=src/pages/JoinPage.jsx --coverage.include=src/pages/LobbyPage.jsx --run Join Lobby` → pass (`JoinPage.jsx` 96.92% lines)
  - `cd frontend && npm run lint` → pass
  - `cd backend/src && ../.venv/bin/pytest tests/test_game_router.py tests/test_game_service.py -k join -v` → 4 passed
- CI merge gates for PR #52: backend-quality ✅, frontend-quality ✅, ops-scripts-quality ✅

### Slice 650 (completed)
- ks-v2 PR: https://github.com/Kriegspiel/ks-v2/pull/53
- Merge commit: `7e6616c071f1b70d60c47989f0ebea3064f0f095`
- Scope delivered:
  - Expanded `tests/test_player_features.py` to 9 deterministic integration tests covering profile/history/leaderboard/settings/transcript flows and auth boundary.
  - Added deterministic fake fixtures for users and archives with stable ordering and pagination assertions.
- Validation checks:
  - `cd backend/src && ../.venv/bin/pytest tests/test_player_features.py -v` → 9 passed
  - `cd backend/src && ../.venv/bin/pytest tests/test_player_features.py -q --maxfail=1` → 9 passed
  - `cd backend/src && ../.venv/bin/pytest tests/test_player_features.py --cov=app --cov-report=term-missing` → 9 passed
  - `cd backend/src && ../.venv/bin/pytest -q --maxfail=1` → 167 passed, 22 skipped, 1 warning
- CI merge gates for PR #53: backend-quality ✅, frontend-quality ✅, ops-scripts-quality ✅

## Blockers

- Step 600: no blockers.

## Discovery Notes

- Packet command references required minor path normalization (`tests/test_game_routes.py` no longer exists; join coverage now in `test_game_router.py` and `test_game_service.py`).
- Packet wording for per-page clamp conflicts with route contract (`le=100` returns `422` pre-service); tests now codify observed API boundary behavior.

## Handoff

- Step 600 complete.
- Continue execution at Step 800 Slice 810.
