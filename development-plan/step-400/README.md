# Step 400 - Real-Time Gameplay Core

## Goal

Implement the authoritative gameplay loop over WebSockets, including engine integration, hidden-information responses, clocks, reconnect, and abandon handling.

## Read First

- [GAME_ENGINE.md](../../GAME_ENGINE.md)
- [API_SPEC.md](../../API_SPEC.md) — WebSocket section
- [ARCHITECTURE.md](../../ARCHITECTURE.md) — state machine, connection manager, game cache, move flow
- [AUTH.md](../../AUTH.md) — WebSocket auth detail
- [DATA_MODEL.md](../../DATA_MODEL.md)

## Depends On

- `step-300`

## Task Slices

### 410 — ConnectionManager

**Create this file:**

- `src/app/ws/connection_manager.py` — `ConnectionManager` class exactly as specified in ARCHITECTURE.md:
  - `active_games: dict[str, dict[str, WebSocket]]` — game_id → {color → WebSocket}
  - `connect(game_id, color, ws)` — register a player connection
  - `disconnect(game_id, color)` — remove a player connection
  - `send_to_player(game_id, color, message)` — send JSON to a specific player
  - `broadcast_to_game(game_id, message)` — send JSON to both players
  - `is_connected(game_id, color) -> bool` — check if a player is connected
  - `get_connection(game_id, color) -> WebSocket | None`

**Acceptance criteria:**
- Unit test: connect two players, send_to_player delivers to correct one, disconnect removes correctly
- `broadcast_to_game` sends to both connected players
- Missing player connection returns None / is handled gracefully

---

### 420 — WebSocket Auth Handshake

**Create/modify these files:**

- `src/app/ws/auth.py` — `authenticate_ws(websocket, db) -> dict | None` function:
  - Check `?token=` query param → validate JWT (for external clients)
  - Otherwise check `session_id` cookie → MongoDB lookup
  - If cookie auth: validate `Origin` header against allowed origins
  - Returns `{user_id, username}` or None
- `src/app/ws/game_handler.py` — the WebSocket endpoint function (wire into main.py as `/ws/game/{game_id}`):
  - Accept the WebSocket connection
  - Call `authenticate_ws` — close with 1008 if auth fails
  - Look up game, verify user is a participant — close with 4002 if not
  - Verify game is in `active` or `paused` state — close with 4003 if not
  - Determine player color
  - Register in ConnectionManager
  - Send `connected` message with full game state (as specified in API_SPEC.md)
  - Notify opponent of reconnection (if applicable)
  - Enter message receive loop (stub — actual message handling in 400.3)
  - On disconnect: unregister from ConnectionManager

**Acceptance criteria:**
- WebSocket connects successfully with valid session cookie
- WebSocket is closed with 1008 when no auth is provided
- WebSocket is closed with 4002 when user is not a game participant
- WebSocket is closed with 4003 when game is not active/paused
- `connected` message contains all fields from API_SPEC.md

---

### 430 — Heartbeat, Disconnect Detection, Pause/Abandon

**Modify these files:**

- `src/app/ws/game_handler.py` — add heartbeat logic:
  - Server sends `{"type": "ping"}` every 30 seconds to each connected client
  - Client must respond with `{"type": "pong"}` within 10 seconds
  - If no pong received: close WebSocket, mark player disconnected
  - On disconnect: update game `white.connected`/`black.connected` to false, update `last_seen_at`
  - If both players were connected and one disconnects: transition game to `paused`, notify remaining player with `{"type": "opponent_status", "connected": false}`
- `src/app/services/game_service.py` — add methods:
  - `pause_game(game_id)` — transition active→paused
  - `resume_game(game_id)` — transition paused→active
  - `abandon_game(game_id, disconnected_color)` — transition paused→abandoned→completed, award win to connected player
- `src/app/ws/abandon_watcher.py` — background task that checks paused games every 60 seconds: if a game has been paused for >15 minutes, call `abandon_game`. Start this task in the app lifespan.

**Acceptance criteria:**
- Server sends ping every 30s, closes connection on missing pong
- Disconnecting one player pauses the game and notifies the other
- Reconnecting after pause resumes the game
- A game paused for >15 minutes is auto-abandoned, opponent wins
- `opponent_status` messages are sent on connect/disconnect events

---

### 440 — Move Flow with Engine Integration

**Create/modify these files:**

- `src/app/services/engine_adapter.py` — adapter wrapping the `kriegspiel` PyPI package:
  - `create_new_game(any_rule=True) -> BerkeleyGame` — creates a fresh game instance
  - `attempt_move(game: BerkeleyGame, uci: str) -> dict` — builds a `KriegspielMove` from UCI, calls `game.ask_for(move)`, returns a dict with: `answer` (MoveAnswer fields), `move_done` (bool), `game_over` (bool), `result` (if game over)
  - `serialize_game(game: BerkeleyGame) -> dict` — serialize engine state for MongoDB storage
  - `deserialize_game(data: dict) -> BerkeleyGame` — restore engine from stored state
  - `get_player_fen(game: BerkeleyGame, color: str) -> str` — extract sanitized display FEN for one player (own pieces only, no opponent pieces)
  - `get_possible_actions(game: BerkeleyGame, color: str) -> list[str]` — return available actions ("move", "ask_any")
- Modify `src/app/ws/game_handler.py` — handle `{"action": "move", "uci": "..."}` messages:
  - Validate it's this player's turn
  - Call `engine_adapter.attempt_move`
  - Build player-specific response messages (moving player gets full answer, opponent gets filtered announcement — as defined in API_SPEC.md)
  - Send via ConnectionManager
  - Persist updated game state to MongoDB

**Acceptance criteria:**
- A legal move returns `move_result` with `move_done: true` to the moving player
- An illegal move returns `move_result` with `ILLEGAL_MOVE` and `move_done: false`
- The opponent receives `opponent_moved` with announcement but NOT the move itself
- Game state is persisted to MongoDB after each successful move
- Player FENs show only that player's pieces

---

### 450 — Ask-Any, Resign, and Game-Over via WebSocket

**Modify these files:**

- `src/app/ws/game_handler.py` — handle remaining action types:
  - `{"action": "ask_any"}` — call engine, send `any_result` to asking player and `opponent_asked_any` to opponent (per API_SPEC.md)
  - `{"action": "resign"}` — call `GameService.resign_game`, send `game_over` to both players with full board FEN revealed
  - Game-over detection: after each successful move, check if `game_over` is true. If so, send `game_over` message to both players, reveal full board, close WebSocket connections.
- `src/app/services/game_service.py` — add `complete_game(game_id, winner, reason)` method:
  - Set game result and state=completed
  - Update both players' stats (games_played, games_won/lost/drawn, elo — simple elo calculation)
  - Move game document from `games` to `game_archives`
  - Write to `audit_log`

**Acceptance criteria:**
- `ask_any` returns "try" or "no" to the asking player and announces to opponent
- `resign` ends the game and reveals the full board to both players
- Checkmate/stalemate detection works via the engine
- On game over: both players' stats are updated, game is archived
- `game_over` message includes `full_board_fen` and result details

---

### 460 — Game Cache and Clock

**Create/modify these files:**

- `src/app/ws/game_cache.py` — `GameCache` class as specified in ARCHITECTURE.md:
  - LRU cache (`OrderedDict`) with max 500 entries
  - `get(game_id) -> BerkeleyGame` — from cache or load from MongoDB
  - `put(game_id, game)` — store in cache + async write to MongoDB
  - `evict(game_id)` — remove from cache (game ended or idle)
  - Idle games (no move for 30 min) evicted from cache
- `src/app/services/clock_service.py` — `ClockService`:
  - `start_clock(game_id, color)` — record clock start time
  - `stop_clock(game_id, color) -> float` — calculate elapsed, deduct from remaining, add increment, return remaining
  - `check_timeout(game_id) -> str | None` — return color that timed out, or None
  - Uses the time_control from game doc (base=1500s, increment=10s for rapid)
- Integrate cache into `game_handler.py` — use cache instead of direct MongoDB reads for engine state
- Integrate clock into move flow — start/stop clock on turns, send clock state in messages, check for timeout

**Acceptance criteria:**
- Game cache reduces MongoDB reads during active gameplay
- Clock deducts time correctly, adds increment after each move
- Timeout detection works (player runs out of time → game over)
- Clock state is included in all `move_result` and `opponent_moved` messages
- Cache evicts idle games after 30 minutes

---

### 470 — WebSocket Gameplay Integration Tests

**Create this file:**

- `src/tests/test_websocket_gameplay.py` — integration tests using httpx + WebSocket test client:
  - Connect to game WebSocket → receive `connected` message with correct fields
  - Connect without auth → WebSocket closed with 1008
  - Connect as non-participant → closed with 4002
  - Make a legal move → receive `move_result` with `move_done: true`
  - Make an illegal move → receive `move_result` with `ILLEGAL_MOVE`
  - Opponent receives `opponent_moved` on legal move (without seeing the move)
  - Ask "any?" → receive `any_result`
  - Resign → both players receive `game_over`
  - Disconnect one player → opponent receives `opponent_status: disconnected`
  - Reconnect → receive full game state, opponent notified
  - Clock decrements on moves
- `src/tests/test_engine_adapter.py` — unit tests for the engine adapter:
  - Create new game → valid initial state
  - Legal move → correct answer
  - Illegal move → ILLEGAL_MOVE answer
  - Serialize/deserialize round-trip preserves game state
  - Player FEN shows only own pieces

**Acceptance criteria:**
- `cd src && pytest tests/test_websocket_gameplay.py tests/test_engine_adapter.py -v` — all pass
- At least 12 WebSocket tests and 6 engine adapter tests
- Tests cover the main referee cases from GAME_ENGINE.md

---

## Required Tests Before Done

- WebSocket integration tests for connect/move/ask-any/resign/game-over
- Illegal move and hidden-information payload tests
- Reconnect/pause/abandon tests
- Clock timeout tests

## Exit Criteria

- Two players can play a full game over WebSockets
- Payloads preserve imperfect information correctly
- Reconnect and timeout behavior works
- Gameplay tests cover the main referee cases

## Out of Scope

- Final UI polish
- Profile/history/leaderboard pages
- Production deployment work
