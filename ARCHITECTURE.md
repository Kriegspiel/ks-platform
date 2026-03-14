# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        NGINX                                │
│              (TLS termination, static files)                 │
├────────────────────────┬────────────────────────────────────┤
│      HTTP (REST)       │         WebSocket (/ws)            │
└────────────┬───────────┴──────────────┬─────────────────────┘
             │                          │
             ▼                          ▼
┌────────────────────────────────────────────────────────────┐
│                     FastAPI (Uvicorn)                       │
│                                                            │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌────────┐  │
│  │ Auth     │  │ Game API  │  │ WS Manager │  │ Admin  │  │
│  │ Router   │  │ Router    │  │            │  │ Router │  │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘  └───┬────┘  │
│       │              │              │             │        │
│       ▼              ▼              ▼             ▼        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Service Layer                          │   │
│  │  UserService │ GameService │ MatchmakingService     │   │
│  └────────────────────────┬────────────────────────────┘   │
│                         │                                  │
│  ┌──────────────────────▼────────────────────────────┐   │
│  │              Game Engine Layer                       │   │
│  │         kriegspiel.BerkeleyGame (PyPI)               │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│                      MongoDB 7+                            │
│                                                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  users   │  │  games   │  │ game_    │  │  audit_   │  │
│  │          │  │          │  │ archives │  │  log      │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────┘  │
└────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### 1. NGINX (Reverse Proxy)

- TLS termination (Let's Encrypt via certbot)
- Serve static files (`/static/`) directly — CSS, JS, images, chess piece SVGs
- Proxy `/api/*` and `/ws/*` to Uvicorn
- Rate limiting: 30 req/s per IP on API, 5 WebSocket connections per IP
- Gzip compression for text responses

### 2. FastAPI Application

Single FastAPI process running under **Uvicorn** with **1 worker** (single async event loop). See [INFRA.md](./INFRA.md) for rationale.

#### Routers (URL namespaces)

| Router | Prefix | Purpose |
|---|---|---|
| `auth` | `/auth/` | Login, register, logout, sessions, OAuth |
| `game` | `/api/game/` | Create, join, resign, list games (REST) |
| `play` | `/ws/game/{game_id}` | Real-time gameplay (WebSocket) |
| `user` | `/api/user/` | Profile, stats, game history |
| `pages` | `/` | Server-rendered HTML pages (Jinja2) |
| `admin` | `/api/admin/` | Admin endpoints (user management, game moderation) |

#### Service Layer

Services contain business logic and are framework-agnostic (testable without HTTP).

| Service | Responsibilities |
|---|---|
| `UserService` | Registration, authentication, profile CRUD, password hashing |
| `GameService` | Game lifecycle: create → wait → play → end → archive. Wraps `BerkeleyGame`. |
| `MatchmakingService` | Open game listings, random pairing, optional ELO-based matching (Phase 2) |
| `NotificationService` | Push game events to connected WebSocket clients |

#### Game Engine Layer

The `kriegspiel` PyPI package (`BerkeleyGame`) is used as-is. The platform wraps it:

1. **GameService** creates a `BerkeleyGame(any_rule=True)` instance per game.
2. On each move attempt, calls `game.ask_for(move)` and gets back a `KriegspielAnswer`.
3. The answer is translated into a WebSocket message and sent to the appropriate player(s).
4. After each move, the full game state is serialized (via `kriegspiel.serialization`) and persisted to MongoDB.
5. On reconnect, the game is restored via `BerkeleyGame.load_game()` from the stored JSON.

## Game State Machine

Every game moves through a defined set of states. No other transitions are valid.

```
                    ┌─────────────────────────────────────────────────┐
                    │                                                 │
  create game       ▼            join game                            │
  ──────────►  [ waiting ] ──────────────────► [ active ] ◄───────┐  │
                    │                              │    │          │  │
                    │ creator cancels               │    │ player   │  │
                    │ or 24h TTL expires            │    │ reconnects│  │
                    ▼                              │    │          │  │
               [ aborted ]          no heartbeat   │    │          │  │
                                    for 30s        ▼    │          │  │
                                              [ paused ]──────────┘  │
                                                   │                 │
                    checkmate / stalemate /         │ 15 min timeout  │
                    resign / draw                  │ (no reconnect)  │
                    ──────────────────┐            ▼                 │
                                      ▼       [ abandoned ]          │
                                 [ completed ] ◄─────────────────────┘
                                               (system awards win)
```

| Transition | Trigger | Timeout / Condition |
|---|---|---|
| `waiting → active` | Second player calls `POST /api/game/join/{code}` | — |
| `waiting → aborted` | Creator cancels, or MongoDB TTL expires | 24 hours |
| `active → paused` | Player disconnects (no WebSocket heartbeat pong) | 30 seconds without pong |
| `paused → active` | Disconnected player reconnects via WebSocket | — |
| `active → completed` | Checkmate, stalemate, insufficient material, resignation, draw agreement | — |
| `paused → abandoned` | Disconnected player does not reconnect | 15 minutes |
| `abandoned → completed` | System awards win to remaining player | Immediate (auto-transition) |

State values: `waiting`, `active`, `paused`, `completed`, `abandoned`, `aborted`

### 3. MongoDB

Single replica set (required for Change Streams). Collections detailed in [DATA_MODEL.md](./DATA_MODEL.md).

### 4. WebSocket Connection Manager

Manages active player connections during gameplay:

```python
class ConnectionManager:
    """Tracks active WebSocket connections per game."""

    def __init__(self):
        # game_id -> {color -> WebSocket}
        self.active_games: dict[str, dict[str, WebSocket]] = {}
        # game_id -> [WebSocket] (spectators, Phase 2)
        self.spectators: dict[str, list[WebSocket]] = {}

    async def connect(self, game_id: str, color: str, ws: WebSocket):
        """Register a player connection for a game."""
        ...

    async def disconnect(self, game_id: str, color: str):
        """Handle player disconnect (game pauses, not forfeited)."""
        ...

    async def send_to_player(self, game_id: str, color: str, message: dict):
        """Send a message to a specific player."""
        ...

    async def broadcast_to_game(self, game_id: str, message: dict):
        """Send a message to all participants (both players + spectators)."""
        ...
```

### WebSocket Heartbeat Protocol

The server maintains connection liveness via a ping/pong mechanism:

1. Server sends `{"type": "ping"}` every **30 seconds** to each connected client.
2. Client must respond with `{"type": "pong"}` within **10 seconds**.
3. If no pong received within 10s, the server closes the WebSocket and marks the player as disconnected. The game transitions to `paused`.
4. Client-side: if no message received from the server for **35 seconds**, the client assumes the connection is dead and initiates reconnection.

### Reconnection Protocol

When a player disconnects and reconnects:

1. Client initiates a new WebSocket connection to `/ws/game/{game_id}?token={session_token}`.
2. Server authenticates the token and verifies the player belongs to this game.
3. Server sends a `connected` message with the **full current game state**:
   - `your_fen`: current board from the player's perspective
   - `turn`: whose turn it is
   - `move_number`: current move number
   - `referee_log`: last 20 referee announcements (so the player can see recent history)
   - `possible_actions`: available actions if it's their turn
   - `opponent_connected`: whether the opponent is still connected
4. Server sends `{"type": "opponent_status", "connected": true}` to the other player.
5. Game transitions from `paused` back to `active`.

**Client-side reconnection logic:**
- Exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s (capped).
- Maximum **10 reconnect attempts** before showing "Connection lost" UI.
- On successful reconnect, restore phantom piece positions from `localStorage`.

## Request Flow: Making a Move

```
Player (browser)
    │
    ├─ WebSocket message: {"action": "move", "uci": "e2e4"}
    │
    ▼
FastAPI WS Handler (/ws/game/{game_id})
    │
    ├─ 1. Validate session (player belongs to this game, correct color)
    ├─ 2. Validate it's this player's turn
    ├─ 3. Build KriegspielMove from UCI string
    ├─ 4. Call game_service.attempt_move(game_id, move)
    │       │
    │       ├─ Load BerkeleyGame from in-memory cache (or MongoDB fallback)
    │       ├─ Call game.ask_for(move) → KriegspielAnswer
    │       ├─ Persist updated game state to MongoDB
    │       └─ Return answer + game metadata
    │
    ├─ 5. Build player-specific messages from KriegspielAnswer
    │       │
    │       ├─ Moving player gets: full answer (legal/illegal, captures, checks)
    │       └─ Opponent gets: filtered answer (announcement type, capture square, check direction)
    │
    ├─ 6. Send via ConnectionManager
    │       ├─ send_to_player(game_id, "white", white_message)
    │       └─ send_to_player(game_id, "black", black_message)
    │
    └─ 7. If game_over: trigger end-of-game flow (stats, archive, cleanup)
```

## Request Flow: "Any?" Question

```
Player (browser)
    │
    ├─ WebSocket message: {"action": "ask_any"}
    │
    ▼
FastAPI WS Handler
    │
    ├─ Build KriegspielMove(QuestionAnnouncement.ASK_ANY, None)
    ├─ Call game.ask_for(move) → KriegspielAnswer
    │       │
    │       ├─ HAS_ANY → player must now capture with pawn
    │       │   Response to player: {"answer": "try", "must_capture_pawn": true}
    │       │   Response to opponent: {"opponent_asked_any": true, "result": "try"}
    │       │
    │       └─ NO_ANY → pawn captures removed from options
    │           Response to player: {"answer": "no"}
    │           Response to opponent: {"opponent_asked_any": true, "result": "no"}
    │
    └─ Per Berkeley rules: the "Any?" exchange count is added to
       the number of illegal tries visible to the opponent.
```

## In-Memory Game Cache

Active games are kept in memory to avoid MongoDB round-trips on every move:

```python
class GameCache:
    """LRU cache for active BerkeleyGame instances."""

    def __init__(self, max_size: int = 500):
        self._cache: OrderedDict[str, BerkeleyGame] = OrderedDict()
        self._max_size = max_size

    async def get(self, game_id: str) -> BerkeleyGame:
        """Get game from cache, or load from MongoDB."""
        ...

    async def put(self, game_id: str, game: BerkeleyGame):
        """Store game in cache and persist to MongoDB."""
        ...

    async def evict(self, game_id: str):
        """Remove game from cache (game ended or idle timeout)."""
        ...
```

- On each successful move: update cache + async write to MongoDB.
- On server restart: games are reloaded from MongoDB on first access.
- Idle games (no move for 30 minutes) are evicted from cache.

## Concurrency Model

- **Uvicorn** with 1 worker process (single event loop) is sufficient for the expected scale.
- All I/O is async: MongoDB via **Motor** (async pymongo), WebSocket via FastAPI native.
- Game engine calls (`ask_for`) are CPU-bound but sub-millisecond; safe to call inline.
- If scale requires it later: increase workers + use Redis pub/sub for cross-worker WS routing.

## Security Boundaries

| Concern | Mitigation |
|---|---|
| Player sees opponent's board | Server never sends opponent piece positions. Each player gets their own view. |
| Player impersonates other color | WebSocket handler checks session → user → game → assigned color |
| Replay attacks | Each move validated against current `possible_to_ask` from game engine |
| Phantom piece data leakage | Phantom pieces are entirely client-side (`localStorage`). The server never receives, stores, or validates phantom piece data. No API endpoint exists for phantoms. |
| Brute-force login | Rate limiting at NGINX (5/min on `/auth/login`) |
| Session hijacking | `HttpOnly`, `Secure`, `SameSite=Lax` cookies; CSRF tokens on forms |
