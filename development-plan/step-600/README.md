# Step 600 - Review and Player Features

## Goal

Implement post-game review plus the player-facing read features: profile, history, leaderboard, and settings.

## Read First

- [FRONTEND.md](../../FRONTEND.md)
- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)

## Depends On

- `step-500`

## Task Slices

### 610 — Profile and History API Endpoints

**Create/modify these files:**

- `src/app/routers/user.py` — FastAPI router with prefix `/api/user`:
  - `GET /api/user/{username}` — public profile: username, profile (bio, avatar, country), stats, member_since. Returns 404 if user not found.
  - `GET /api/user/{username}/games` — paginated game history from `game_archives`. Query params: `page` (default 1), `per_page` (default 20, max 100). Returns `GameHistoryItem` list + pagination metadata.
  - `PATCH /api/user/settings` — update current user's settings (board_theme, piece_set, sound_enabled, auto_ask_any). Requires auth. Validates against allowed values. Returns updated settings.
- Wire user router into `src/app/main.py`
- `src/app/services/user_service.py` — add methods:
  - `get_public_profile(username) -> dict | None`
  - `get_game_history(user_id, page, per_page) -> (list[dict], int)` — returns (games, total_count) from `game_archives`
  - `update_settings(user_id, settings_update) -> dict`

**Acceptance criteria:**
- `GET /api/user/alexfil` returns profile with stats
- `GET /api/user/alexfil/games?page=1&per_page=10` returns paginated history
- `PATCH /api/user/settings` updates and persists settings
- Out-of-range pages return empty data with correct pagination.total

---

### 620 — Leaderboard Endpoint

**Create/modify these files:**

- `src/app/routers/user.py` — add:
  - `GET /api/leaderboard` — paginated leaderboard. Query params: `page`, `per_page` (default 50). Returns players sorted by ELO descending, filtered to `status=active` and `games_played >= 5`. Each entry includes: rank, username, elo, games_played, win_rate.
- `src/app/services/user_service.py` — add method:
  - `get_leaderboard(page, per_page) -> (list[dict], int)` — query users collection as specified in DATA_MODEL.md common queries

**Acceptance criteria:**
- Leaderboard returns players ranked by ELO
- Only players with 5+ games appear
- Pagination works correctly
- Win rate is calculated (games_won / games_played)

---

### 630 — Profile, History, Leaderboard, and Settings Pages

**Create these files:**

- `src/app/templates/profile.html` — extends base.html:
  - Username, member since date
  - Stats: games played, W/L/D, ELO, peak ELO, win rate
  - Recent games table (last 5) with link to "View all games"
  - Link to game review for each game
- `src/app/templates/game_history.html` — extends base.html:
  - Paginated table of completed games: opponent, color played, result, reason, move count, date
  - Each row links to the game review page
  - Pagination controls (prev/next)
- `src/app/templates/leaderboard.html` — extends base.html:
  - Ranked table: rank, username (links to profile), ELO, games played, win rate
  - Pagination controls
- `src/app/templates/settings.html` — extends base.html (requires auth):
  - Form with: board theme dropdown, piece set dropdown, sound enabled checkbox, auto ask-any checkbox
  - Save button using `hx-patch="/api/user/settings"` with HTMX
  - Success/error feedback
- `src/app/routers/pages.py` — add routes:
  - `GET /user/{username}` → render profile.html
  - `GET /user/{username}/games` → render game_history.html
  - `GET /leaderboard` → render leaderboard.html
  - `GET /settings` → render settings.html (requires auth)

**Acceptance criteria:**
- All four pages render with correct data
- Profile shows user stats and recent games
- Game history paginates correctly
- Leaderboard ranks players by ELO
- Settings form saves preferences via HTMX
- Pages use consistent design from DESIGN.md

---

### 640 — Review/Replay Page and review.js

**Create these files:**

- `src/app/routers/game.py` — add:
  - `GET /api/game/{game_id}/moves` — full move transcript. Available to participants anytime, to anyone after game ends. Checks `games` then `game_archives`.
- `src/app/templates/review.html` — extends base.html:
  - Two-column layout: board (left) + move log (right)
  - Board container for chessboard.js (non-draggable)
  - Move log: numbered list of moves with referee announcements
  - Navigation controls: first (|◄), prev (◄), next (►), last (►|) buttons
  - Perspective radio buttons: Referee (full board), White's view, Black's view
  - Click a move in the log to jump to that position
  - Game result summary at bottom
  - Script tags for chessboard.js, chess.js, review.js
- `src/app/static/js/review.js` — `GameReview` class (~120 lines) as specified in FRONTEND.md:
  - `load()` — fetch `/api/game/{game_id}/moves`, store moves array, init board
  - `initBoard()` — configure chessboard.js with start position, non-draggable
  - `bindControls()` — keyboard (arrow keys), step buttons, perspective radios, move log clicks
  - `next()` / `prev()` / `goTo(ply)` — navigate through moves
  - `renderAtCurrentPly()` — rebuild board state by replaying moves up to currentPly, filter by perspective (referee=full FEN, white/black=sanitized per-player FEN), highlight current move in log
- `src/app/routers/pages.py` — add `GET /game/{game_id}/review` route (renders review.html, passes game metadata)

**Acceptance criteria:**
- Review page loads move transcript from API
- Board updates on next/prev/goto
- Three perspectives work (referee sees all pieces, white/black see only own)
- Arrow keys navigate moves
- Clicking a move in the log jumps to that position
- Game result is displayed

---

### 650 — Review and Player Feature Tests

**Create this file:**

- `src/tests/test_player_features.py` — integration tests:
  - `GET /api/user/{username}` — returns profile for existing user, 404 for missing
  - `GET /api/user/{username}/games` — returns paginated history
  - `GET /api/leaderboard` — returns ranked players, respects min games filter
  - `PATCH /api/user/settings` — updates settings, returns updated values
  - `PATCH /api/user/settings` without auth — 401
  - `GET /api/game/{game_id}/moves` — returns move transcript for completed game
  - `GET /api/game/{game_id}/moves` for non-participant on active game — 403
  - Pagination edge cases: page beyond total, per_page > 100 capped

**Acceptance criteria:**
- `cd src && pytest tests/test_player_features.py -v` — all pass
- At least 10 test cases
- Tests verify correct data shapes and pagination behavior

---

## Required Tests Before Done

- Integration tests for history/profile/leaderboard/settings endpoints
- Replay correctness tests
- Page rendering smoke tests

## Exit Criteria

- Users can view profiles, history, rankings, and settings
- Completed games can be reviewed and replayed
- Archive-backed reads behave correctly

## Out of Scope

- TLS/deployment
- Backup/restore
- Final launch signoff
