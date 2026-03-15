# Step 300 - Lobby and Game Lifecycle

## Goal

Implement game create/join/list/resign with join codes and a simplified state machine (waiting → active → completed). Build React lobby UI.

## Read First

- [API_SPEC.md](../../API_SPEC.md) — game endpoints
- [DATA_MODEL.md](../../DATA_MODEL.md) — games collection
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — state machine (we use a simplified version: only waiting/active/completed)
- [development-plan/PLAN.md](../PLAN.md) — architecture decisions

## Depends On

- `step-200`

## Simplified Game Lifecycle

```
  create game       join game         checkmate/resign/stalemate
  ──────────► [waiting] ──────────► [active] ──────────► [completed]
```

Three states only. No `paused`, `abandoned`, or `aborted`. Games in `waiting` can be deleted by the creator.

## Task Slices

### 310 — Game Models and Code Generator

**Create these files:**

- `src/app/models/game.py` — Pydantic models from DATA_MODEL.md:
  - `PlayerEmbed` (user_id, username, connected, last_seen_at)
  - `MoveAnswer` (main, capture_square, special, check_1, check_2)
  - `MoveRecord` (ply, color, question_type, uci, answer, move_done, timestamp)
  - `GameResult` (winner, reason, ended_at)
  - `TimeControl` (base, increment, white_remaining, black_remaining, active_color)
  - `GameDocument` (game_code, rule_variant, white, black, state, turn, move_number, half_move_count, engine_state, white_fen, black_fen, moves, result, time_control, created_at, updated_at)
  - **State is limited to:** `Literal["waiting", "active", "completed"]`
- API models from API_SPEC.md:
  - `CreateGameRequest` (rule_variant, play_as, time_control)
  - `CreateGameResponse` (game_id, game_code, play_as, rule_variant, state, join_url)
  - `JoinGameResponse` (game_id, game_code, play_as, rule_variant, state, game_url)
  - `OpenGameItem` (game_code, rule_variant, created_by, created_at, available_color)
- `src/app/services/code_generator.py` — `generate_game_code(db) -> str`:
  - 6-char uppercase alphanumeric (exclude ambiguous: 0, O, I, 1, L)
  - Check uniqueness against `games` collection
  - Retry if collision

**Acceptance criteria:**
- All models instantiate with valid sample data
- `GameDocument.state` only accepts "waiting", "active", "completed"
- `generate_game_code` produces unique 6-char codes

---

### 320 — GameService: Create, Join, Resign

**Create this file:**

- `src/app/services/game_service.py` — `GameService` class:
  - `create_game(db, user_id, username, rule_variant, play_as) -> dict`:
    - Generate game code
    - Resolve "random" play_as to white or black
    - Create game doc: state="waiting", creator as their chosen color, opponent fields null
    - Set time_control to rapid defaults (base=1500, increment=10)
    - Insert into `games` collection
    - Return created game doc
  - `join_game(db, game_code, user_id, username) -> dict`:
    - Find game by code, validate: exists (404), not own game (409), state=waiting (409)
    - Assign joining player to remaining color
    - Set state="active"
    - Return updated game doc
  - `get_game(db, game_id) -> dict | None` — lookup by _id
  - `get_open_games(db) -> list[dict]` — state=waiting, sorted by created_at desc, limit 50
  - `get_my_games(db, user_id) -> list[dict]` — user is white or black, state in (waiting, active)
  - `resign_game(db, game_id, user_id) -> dict`:
    - Validate user is a player, game is active
    - Set result (winner=opponent, reason="resignation")
    - Set state="completed"
  - `delete_waiting_game(db, game_id, user_id)`:
    - Validate user is creator, state=waiting
    - Delete game doc

**Acceptance criteria:**
- `create_game` inserts a valid game doc with state="waiting"
- `join_game` transitions waiting→active, assigns second player
- `join_game` rejects joining own game (409) or full game (409)
- `resign_game` transitions active→completed with correct winner
- `get_open_games` returns only waiting games
- `get_my_games` returns user's waiting + active games

---

### 330 — Game REST Endpoints

**Create this file:**

- `src/app/routers/game.py` — FastAPI router, prefix `/api/game`, all endpoints use `get_current_user` dependency:
  - `POST /api/game/create` — accepts `CreateGameRequest`, calls `GameService.create_game`, returns 201 `CreateGameResponse`
  - `POST /api/game/join/{game_code}` — calls `GameService.join_game`, returns `JoinGameResponse`
  - `GET /api/game/open` — returns `{"games": [OpenGameItem, ...]}`
  - `GET /api/game/mine` — returns `{"games": [...]}`
  - `GET /api/game/{game_id}` — returns game metadata (not board state)
  - `POST /api/game/{game_id}/resign` — calls `GameService.resign_game`, returns result
  - `DELETE /api/game/{game_id}` — calls `GameService.delete_waiting_game`
- Wire game router into `src/app/main.py`
- All error responses use the standardized format: `{"error": {"code": "...", "message": "..."}}`

**Acceptance criteria:**
- Create returns 201 with game_code
- Join returns 200 with assigned color
- Open games list works
- My games list works
- All endpoints return 401 without auth
- Errors match API_SPEC.md format

---

### 340 — React Lobby Page

**Create these files:**

- `frontend/src/pages/Lobby.jsx` — lobby page with sections:
  - **Create Game**: rule variant dropdown (Berkeley / Berkeley+Any), play-as selector (Random/White/Black), create button. On success: show game code + "Waiting for opponent" with auto-poll (every 3s check if game state changed to active → redirect to /game/:id)
  - **Join by Code**: text input + join button. On success: redirect to /game/:id
  - **Open Games**: list of waiting games with creator username, rule variant, join button. Auto-refresh every 5s.
  - **My Active Games**: list of user's active games with opponent name, "your turn" indicator, link to /game/:id. Auto-refresh every 10s.
- `frontend/src/pages/Lobby.css` — lobby styling
- `frontend/src/services/api.js` — add game API functions:
  - `gameApi.create(ruleVariant, playAs)`
  - `gameApi.join(gameCode)`
  - `gameApi.getOpen()`
  - `gameApi.getMine()`
  - `gameApi.getGame(gameId)`
  - `gameApi.resign(gameId)`
  - `gameApi.deleteGame(gameId)`
- `frontend/src/App.jsx` — add `/lobby` route with auth guard (redirect to /auth/login if not logged in)

**Acceptance criteria:**
- Create game shows game code and waiting state
- Joining a game redirects to game page
- Open games list auto-refreshes
- My games shows active games with turn indicator
- Lobby requires login (redirects if not authenticated)

---

### 350 — Game Lifecycle Integration Tests

**Create this file:**

- `src/tests/test_game_lifecycle.py` — integration tests:
  - Create game → 201 with game_code
  - Create game without auth → 401
  - Join game with valid code → 200, state=active
  - Join own game → 409
  - Join game that's already active → 409
  - Join nonexistent code → 404
  - List open games → includes waiting, excludes active/completed
  - List my games → includes user's active + waiting games
  - Resign active game → 200, correct winner
  - Resign non-active game → 400
  - Delete waiting game as creator → success
  - Delete waiting game as non-creator → 403
  - Game code is 6 chars, uppercase alphanumeric

**Acceptance criteria:**
- `cd src && pytest tests/test_game_lifecycle.py -v` — all pass
- At least 12 test cases
- Tests verify state transitions

---

## Exit Criteria

- A logged-in user can create a game with a join code
- Another user can join via the code
- Lobby shows open games and active games
- Games transition correctly: waiting → active → completed

## Out of Scope

- Move execution (step 400)
- Board UI (step 500)
- Pause/abandon/expiry (not in MVP)
