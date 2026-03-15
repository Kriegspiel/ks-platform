# Step 600 - Review and Player Features

## Goal

Implement profile, game history, leaderboard, settings, and post-game review.

## Read First

- [API_SPEC.md](../../API_SPEC.md) — user/leaderboard/settings endpoints
- [DATA_MODEL.md](../../DATA_MODEL.md) — users.stats, game_archives
- [FRONTEND.md](../../FRONTEND.md) — review page spec (adapt for React)

## Depends On

- `step-500`

## Task Slices

### 610 — Profile, History, and Leaderboard API

**Create these files:**

- `src/app/routers/user.py` — FastAPI router, prefix `/api/user`:
  - `GET /api/user/{username}` — public profile: username, profile (bio, avatar, country), stats, member_since. Returns 404 if not found.
  - `GET /api/user/{username}/games` — paginated game history from `game_archives`. Query params: `page` (default 1), `per_page` (default 20, max 100). Returns `GameHistoryItem` list + pagination.
  - `PATCH /api/user/settings` — update current user's settings (board_theme, piece_set, sound_enabled, auto_ask_any). Requires auth.
  - `GET /api/leaderboard` — paginated, sorted by ELO desc, filtered to `status=active` and `games_played >= 5`. Each entry: rank, username, elo, games_played, win_rate.
- `src/app/services/user_service.py` — add methods:
  - `get_public_profile(db, username) -> dict | None`
  - `get_game_history(db, user_id, page, per_page) -> (list[dict], int)`
  - `update_settings(db, user_id, settings) -> dict`
  - `get_leaderboard(db, page, per_page) -> (list[dict], int)`
- Wire user router into `src/app/main.py`

**Acceptance criteria:**
- Profile returns stats for existing user, 404 for missing
- Game history paginates correctly
- Settings update persists
- Leaderboard ranks by ELO, filters by min games
- Out-of-range pages return empty data with correct total

---

### 620 — Review/Replay API and React Review Page

**Create these files:**

- `src/app/routers/game.py` — (moves endpoint already exists from 440)
- `frontend/src/pages/Review.jsx` — post-game review page:
  - Loads move transcript from `GET /api/game/{gameId}/moves`
  - ChessBoard component (non-interactive, no click handler)
  - Move-by-move navigation: First, Prev, Next, Last buttons
  - Arrow key support (Left = prev, Right = next)
  - Move log panel: numbered list, click to jump to that ply
  - Perspective selector: Referee (full board), White (white pieces only), Black (black pieces only)
  - `renderAtPly(n)`: rebuild board FEN by replaying moves up to ply n. Referee perspective shows full FEN, player perspectives show filtered FEN.
  - Game result summary at bottom
- `frontend/src/pages/Review.css` — review page styling (two-column, responsive)
- `frontend/src/App.jsx` — add `/game/:gameId/review` route

**Acceptance criteria:**
- Review page loads move transcript
- Board updates on next/prev/goto
- Three perspectives work correctly
- Arrow keys navigate moves
- Clicking a move in log jumps to that position
- Game result displayed

---

### 630 — React Profile, History, Leaderboard, Settings Pages

**Create these files:**

- `frontend/src/pages/Profile.jsx` — public profile page:
  - Username, member since
  - Stats: games played, W/L/D, ELO, peak, win rate
  - Recent games (last 5) with links to review
  - "View all games" link
- `frontend/src/pages/Profile.css`
- `frontend/src/pages/GameHistory.jsx` — paginated game history:
  - Table: opponent, color, result, reason, moves, date
  - Each row links to review page
  - Prev/Next pagination
- `frontend/src/pages/GameHistory.css`
- `frontend/src/pages/Leaderboard.jsx` — ranked table:
  - Rank, username (links to profile), ELO, games played, win rate
  - Pagination
- `frontend/src/pages/Leaderboard.css`
- `frontend/src/pages/Settings.jsx` — user preferences (requires auth):
  - Board theme, piece set, sound toggle, auto ask-any toggle
  - Save button
  - Success/error feedback
- `frontend/src/pages/Settings.css`
- `frontend/src/services/api.js` — add:
  - `userApi.getProfile(username)`
  - `userApi.getGameHistory(username, page, perPage)`
  - `userApi.updateSettings(settings)`
  - `userApi.getLeaderboard(page, perPage)`
- `frontend/src/App.jsx` — add routes: `/user/:username`, `/user/:username/games`, `/leaderboard`, `/settings`

**Acceptance criteria:**
- Profile page shows user stats and recent games
- Game history paginates
- Leaderboard ranks players
- Settings saves and loads preferences
- All pages responsive

---

### 640 — Direct Join URL

**Create/modify these files:**

- `frontend/src/pages/Join.jsx` — direct join page (`/join/:gameCode`):
  - On mount: call `POST /api/game/join/{gameCode}`
  - On success: redirect to `/game/{gameId}`
  - On error (game not found, already full): show error message with link to lobby
  - If not logged in: redirect to `/auth/login` with return URL
- `frontend/src/App.jsx` — add `/join/:gameCode` route
- `frontend/src/pages/Lobby.jsx` — when creating a game, display the join URL (`/join/{gameCode}`) for sharing

**Acceptance criteria:**
- `/join/A7K2M9` auto-joins the game and redirects to game page
- Invalid/full game shows error with lobby link
- Unauthenticated user is redirected to login

---

### 650 — Player Feature Integration Tests

**Create this file:**

- `src/tests/test_player_features.py` — integration tests:
  - `GET /api/user/{username}` → profile for existing user, 404 for missing
  - `GET /api/user/{username}/games` → paginated history
  - `GET /api/leaderboard` → ranked players, min games filter
  - `PATCH /api/user/settings` → updates and returns settings
  - `PATCH /api/user/settings` without auth → 401
  - `GET /api/game/{game_id}/moves` → transcript for completed game
  - Pagination: page beyond total returns empty, per_page capped at 100

**Acceptance criteria:**
- `cd src && pytest tests/test_player_features.py -v` — all pass
- At least 8 test cases

---

## Exit Criteria

- Users can view profiles, history, and rankings
- Completed games can be reviewed move-by-move
- Settings persist
- Direct join URLs work

## Out of Scope

- Deployment
- Sound effects
- Final launch QA
