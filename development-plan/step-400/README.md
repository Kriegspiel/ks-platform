# Step 400 - Gameplay Core

## Goal

Implement the game engine integration, move/ask-any/resign endpoints, game state polling with hidden-information responses, and clock tracking.

## Read First

- [GAME_ENGINE.md](../../GAME_ENGINE.md) — BerkeleyGame API, KriegspielMove, KriegspielAnswer
- [API_SPEC.md](../../API_SPEC.md) — move endpoint, game state endpoint
- [DATA_MODEL.md](../../DATA_MODEL.md) — engine_state, moves array, white_fen/black_fen
- [development-plan/PLAN.md](../PLAN.md) — polling (not WebSocket)

## Depends On

- `step-300`

## Polling Architecture

No WebSocket. The frontend polls `GET /api/game/{game_id}/state?player=white` every 2 seconds during active games. The backend returns the player-specific view each time.

## Task Slices

### 410 — Engine Adapter

**Create this file:**

- `src/app/services/engine_adapter.py` — wraps the `kriegspiel` PyPI package (mirrors ks-v2's `kriegspiel_wrapper.py` pattern but adapted for MongoDB):
  - `create_new_game(any_rule=True) -> BerkeleyGame` — create fresh BerkeleyGame instance
  - `attempt_move(game: BerkeleyGame, uci: str) -> dict` — build `KriegspielMove(COMMON, chess.Move.from_uci(uci))`, call `game.ask_for(move)`, return dict with: `main` (announcement name), `capture_square` (square name or None), `special` (special announcement or None), `check_1`, `check_2`, `move_done` (bool), `game_over` (bool), `result` (if game over)
  - `attempt_ask_any(game: BerkeleyGame) -> dict` — build `KriegspielMove(ASK_ANY, None)`, call `game.ask_for(move)`, return dict with: `has_any` (bool), `main` (announcement name), `move_done` (bool)
  - `get_visible_fen(game: BerkeleyGame, color: str) -> str` — create board copy, remove opponent pieces, return FEN (same logic as ks-v2's `get_visible_board`)
  - `get_full_fen(game: BerkeleyGame) -> str` — return full referee board FEN
  - `serialize_game(game: BerkeleyGame) -> dict` — use `kriegspiel.serialization` to serialize
  - `deserialize_game(data: dict) -> BerkeleyGame` — restore from serialized state

**Acceptance criteria:**
- `create_new_game()` returns a valid BerkeleyGame in starting position
- `attempt_move` with "e2e4" on a new game returns `move_done: true`, `main: "REGULAR_MOVE"`
- `attempt_move` with an illegal move returns `move_done: false`, `main: "ILLEGAL_MOVE"`
- `get_visible_fen` for white shows only white pieces
- `serialize_game` / `deserialize_game` round-trip preserves game state

---

### 420 — Move and Ask-Any Endpoints

**Create/modify these files:**

- `src/app/routers/game.py` — add endpoints:
  - `POST /api/game/{game_id}/move` — params: `uci` (str). Requires auth + user is a player in this game + game is active + it's this player's turn. Calls `engine_adapter.attempt_move`. On success:
    - Append `MoveRecord` to game's `moves` array
    - Update `engine_state` with serialized game
    - Update `white_fen` and `black_fen`
    - If `move_done`: update `turn`, increment `half_move_count`, handle clock (deduct time, add increment)
    - If `game_over`: set result, transition to completed
    - Return player-specific response (the moving player gets full answer; clock state included)
  - `POST /api/game/{game_id}/ask-any` — Requires auth + player's turn. Calls `engine_adapter.attempt_ask_any`. Append to moves array. Return result (`has_any`).
  - `POST /api/game/{game_id}/resign` — (already exists from 330, but now also: update stats, archive game)
- `src/app/services/game_service.py` — add:
  - `complete_game(db, game_id, winner, reason)` — set result, state=completed, update both players' stats (games_played, wins/losses/draws), move game to `game_archives`

**Acceptance criteria:**
- Legal move updates game state and returns `move_done: true`
- Illegal move returns `move_done: false`, game state unchanged
- Moving out of turn returns 400
- Ask-any returns `has_any: true/false`
- Game over (checkmate/stalemate) is detected and transitions to completed
- Resign works and updates player stats

---

### 430 — Game State Polling Endpoint

**Create/modify these files:**

- `src/app/routers/game.py` — add endpoint:
  - `GET /api/game/{game_id}/state?player={color}` — returns player-specific game view:
    ```json
    {
      "game_id": "...",
      "your_color": "white",
      "your_fen": "8/8/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
      "turn": "black",
      "move_number": 1,
      "half_move_count": 1,
      "state": "active",
      "is_game_over": false,
      "result": null,
      "opponent_username": "player2",
      "referee_log": [...last 20 announcements...],
      "possible_actions": ["move", "ask_any"],
      "clock": {
        "white_remaining": 1498.5,
        "black_remaining": 1500.0,
        "active_color": "black"
      }
    }
    ```
  - `your_fen` uses `engine_adapter.get_visible_fen` — only shows this player's pieces
  - `referee_log` is built from the `moves` array: extract announcements both players can see (captures, checks, ask-any results) but NOT the move itself or whether it was legal/illegal (only the moving player knows that)
  - `possible_actions` returns what the player can do right now: `["move", "ask_any"]` on their turn, `[]` otherwise
  - Auth required: user must be a participant in the game
- `src/app/services/clock_service.py` — `ClockService`:
  - `get_remaining(game, color) -> float` — calculate current remaining time based on stored remaining + time elapsed since last move
  - `deduct_and_increment(db, game_id, color) -> dict` — deduct elapsed time from moving player, add increment, store updated clock, return new clock state
  - `check_timeout(game) -> str | None` — return color that timed out, or None

**Acceptance criteria:**
- Polling returns player-specific FEN (no opponent pieces visible)
- Referee log shows announcements visible to both players
- Possible actions are correct for current turn
- Clock remaining decreases between polls (calculated server-side)
- Non-participant gets 403

---

### 440 — Game History and Recent Games Endpoints

**Create/modify these files:**

- `src/app/routers/game.py` — add endpoints:
  - `GET /api/game/{game_id}/moves` — full move transcript. Available to participants anytime, publicly after game ends. Checks `games` then `game_archives`.
  - `GET /api/game/recent` — last 10 completed games from `game_archives` (for home page)
- `src/app/services/game_service.py` — add:
  - `get_game_or_archive(db, game_id) -> dict | None` — check `games` first, then `game_archives`
  - `get_recent_completed(db, limit=10) -> list[dict]` — from `game_archives`, sorted by completed_at desc

**Acceptance criteria:**
- Move transcript endpoint returns all moves for a completed game
- Active game transcript only accessible to participants
- Recent games returns last 10 completed
- Archived games are found by `get_game_or_archive`

---

### 450 — Gameplay Integration Tests

**Create these files:**

- `src/tests/test_gameplay.py` — integration tests:
  - Make a legal move → game state updated, `move_done: true`
  - Make an illegal move → `move_done: false`, state unchanged
  - Move when not your turn → 400
  - Ask-any → returns `has_any`
  - Poll game state as white → only white pieces in FEN
  - Poll game state as black → only black pieces in FEN
  - Referee log shows announcements without leaking moves
  - Resign → game completed, stats updated, game archived
  - Clock deducts time on moves
  - Non-participant can't poll or move → 403
- `src/tests/test_engine_adapter.py` — unit tests:
  - Create game → valid starting position
  - Legal move → correct answer
  - Illegal move → ILLEGAL_MOVE
  - Serialize/deserialize round-trip
  - Visible FEN shows only one color's pieces
  - Ask-any returns correct result

**Acceptance criteria:**
- `cd src && pytest tests/test_gameplay.py tests/test_engine_adapter.py -v` — all pass
- At least 10 gameplay tests + 6 engine tests
- Tests verify hidden-information is preserved

---

## Exit Criteria

- Two authenticated users can play a game via REST API (create, join, make moves, resign)
- Hidden information is preserved (each player only sees own pieces)
- Ask-any question works
- Clock tracks time
- Game state is pollable

## Out of Scope

- Board UI (step 500)
- WebSocket (not in MVP)
- Pause/reconnect (not in MVP)
