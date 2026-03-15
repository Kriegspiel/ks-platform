# Step 300 - Lobby and Game Lifecycle REST

## Goal

Implement the non-WebSocket game lifecycle: create, join, list, mine, resign, and waiting-game expiry behavior.

## Read First

- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — game state machine section
- [GAME_ENGINE.md](../../GAME_ENGINE.md)

## Depends On

- `step-200`

## Task Slices

### 310 — Game Models and Code Generator

**Create these files:**

- `src/app/models/game.py` — Pydantic models exactly as defined in DATA_MODEL.md:
  - `PlayerEmbed` (user_id, username, connected, last_seen_at)
  - `MoveAnswer` (main, capture_square, special, check_1, check_2)
  - `MoveRecord` (ply, color, question_type, uci, answer, move_done, timestamp)
  - `GameResult` (winner, reason, ended_at)
  - `GameDocument` (all fields from DATA_MODEL.md games collection)
  - `TimeControl` (base, increment, white_remaining, black_remaining, active_color)
- API request/response models from API_SPEC.md:
  - `CreateGameRequest` (rule_variant, play_as, time_control)
  - `CreateGameResponse` (game_id, game_code, play_as, rule_variant, state, join_url)
  - `JoinGameResponse` (game_id, game_code, play_as, rule_variant, state, game_url)
  - `OpenGameItem` (game_code, rule_variant, created_by, created_at, available_color)
- `src/app/services/code_generator.py` — `generate_game_code() -> str` that produces a 6-char alphanumeric code (uppercase letters + digits, excluding ambiguous chars like 0/O/I/1), with a uniqueness check against the `games` collection

**Acceptance criteria:**
- All models can be instantiated with sample data from DATA_MODEL.md
- `CreateGameRequest` validates `rule_variant` and `play_as` enums
- `generate_game_code()` produces unique 6-char codes
- `python -c "from app.models.game import GameDocument; print('ok')"` works

---

### 320 — GameService: Create, Join, State Transitions

**Create this file:**

- `src/app/services/game_service.py` — `GameService` class with methods:
  - `create_game(user_id, username, rule_variant, play_as, time_control) -> dict` — generates game code, resolves "random" color, creates game doc in `waiting` state with `expires_at` = now + 24h, inserts into `games` collection, returns the created game doc
  - `join_game(game_code, user_id, username) -> dict` — finds game by code, validates (not own game, not full, state=waiting), assigns joining player to remaining color, transitions to `active`, clears `expires_at`, returns updated game doc. Raises appropriate errors (404 not found, 409 full, 409 own game).
  - `get_game(game_id) -> dict | None` — look up game by ID
  - `get_open_games() -> list[dict]` — find games with state=waiting, sorted by created_at desc, limit 50
  - `get_my_games(user_id) -> list[dict]` — find games where user is white or black and state in (active, paused, waiting)
  - `resign_game(game_id, user_id) -> dict` — validate user is a player, game is active, set result with winner=opponent and reason="resignation", transition to completed

**Acceptance criteria:**
- `create_game` inserts a game doc matching DATA_MODEL.md schema
- `join_game` transitions waiting→active and assigns the second player
- `join_game` raises 409 when trying to join own game or full game
- `resign_game` transitions active→completed with correct winner
- State transition guards prevent invalid transitions (e.g., can't resign a completed game)

---

### 330 — Game REST Endpoints

**Create this file:**

- `src/app/routers/game.py` — FastAPI router with prefix `/api/game`, all endpoints require auth:
  - `POST /api/game/create` — accepts `CreateGameRequest`, calls `GameService.create_game`, returns `CreateGameResponse` with 201
  - `POST /api/game/join/{game_code}` — calls `GameService.join_game`, returns `JoinGameResponse`
  - `GET /api/game/open` — calls `GameService.get_open_games`, returns `{"games": [OpenGameItem, ...]}`
  - `GET /api/game/mine` — calls `GameService.get_my_games`, returns `{"games": [...]}`
  - `GET /api/game/{game_id}` — calls `GameService.get_game`, returns game metadata (not board state). Falls back to `game_archives` collection if not found in `games`.
  - `POST /api/game/{game_id}/resign` — calls `GameService.resign_game`, returns result
- Wire game router into `src/app/main.py`

**Acceptance criteria:**
- `POST /api/game/create` returns 201 with game_code and join_url
- `POST /api/game/join/{code}` returns 200 with assigned color and game_url
- `GET /api/game/open` returns list of waiting games
- `GET /api/game/mine` returns current user's active/waiting games
- All endpoints return 401 without auth
- Error responses match the standardized format from API_SPEC.md

---

### 340 — Waiting-Game Expiry

**Modify these files:**

- `src/app/db.py` — ensure the `expires_at` TTL index exists on the `games` collection (TTL index with `expireAfterSeconds: 0` — MongoDB auto-deletes docs when `expires_at` passes)
- `src/app/services/game_service.py` — add `cancel_game(game_id, user_id)` method: validates user is creator, game is in waiting state, transitions to `aborted`
- `src/app/routers/game.py` — add `POST /api/game/{game_id}/cancel` endpoint

**Note:** MongoDB's TTL index handles automatic deletion of expired waiting games. The `aborted` state is for explicit creator cancellation. When a waiting game expires via TTL, MongoDB simply removes the document — no state transition needed.

**Acceptance criteria:**
- TTL index exists on `games.expires_at`
- Creating a game sets `expires_at` to now + 24h
- Joining a game sets `expires_at` to null
- `cancel_game` transitions waiting→aborted for the creator only
- Non-creators get 403 when trying to cancel

---

### 350 — Lobby Page

**Create these files:**

- `src/app/templates/lobby.html` — extends `base.html`, contains:
  - "Create Game" form (rule variant dropdown, play-as radio buttons, submit button) — uses `hx-post="/api/game/create"` with HTMX
  - "Join by Code" form (text input + join button) — uses `hx-post` to `/api/game/join/{code}`
  - "Open Games" list — uses `hx-get="/api/game/open" hx-trigger="load, every 5s"` for auto-refresh
  - "My Active Games" list — uses `hx-get="/api/game/mine" hx-trigger="load, every 10s"`
  - Waiting state: when user creates a game, show the game code and a "waiting for opponent" message with auto-poll for game state change
- `src/app/templates/partials/open_games.html` — HTMX partial for the open games list
- `src/app/templates/partials/my_games.html` — HTMX partial for the user's active games
- `src/app/routers/pages.py` — add `GET /lobby` route (requires auth, renders lobby.html)
- Modify game router endpoints to return HTML partials when request has `HX-Request` header, JSON otherwise

**Acceptance criteria:**
- `GET /lobby` renders the lobby page (redirects to login if not authenticated)
- Creating a game shows the game code and "waiting" status
- Open games list refreshes automatically every 5 seconds
- Joining a game via code or open games list works
- My active games shows games where user is a participant

---

### 360 — Game Lifecycle Integration Tests

**Create this file:**

- `src/tests/test_game_lifecycle.py` — integration tests covering:
  - Create game → returns 201 with code
  - Create game while not logged in → 401
  - Join game with valid code → 200, state becomes active
  - Join own game → 409
  - Join full game → 409
  - Join nonexistent code → 404
  - List open games → includes waiting games, excludes active/completed
  - List my games → includes user's active games only
  - Resign active game → 200, correct winner
  - Resign non-active game → 400
  - Cancel waiting game as creator → success
  - Cancel waiting game as non-creator → 403
  - Game has expires_at set on creation, cleared on join

**Acceptance criteria:**
- `cd src && pytest tests/test_game_lifecycle.py -v` — all pass
- At least 12 test cases
- Tests verify state transitions match ARCHITECTURE.md state machine

---

## Required Tests Before Done

- Service tests for create/join/resign/state transitions
- Integration tests for REST endpoints
- Expiry handling tests for waiting games

## Exit Criteria

- A logged-in user can create a game, share a join code, and another user can join it
- Waiting games expire correctly
- Open-games and my-games reads work
- Lobby flow is usable without WebSocket gameplay yet

## Out of Scope

- Move execution
- Reconnect logic
- Player board UX beyond minimal lobby flow
