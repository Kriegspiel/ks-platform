# API Specification

All REST endpoints return JSON. All WebSocket messages are JSON frames.

Base URL: `https://kriegspiel.org/api`

---

## Authentication

### `POST /auth/register`

Create a new account.

**Request:**
```json
{
  "username": "alexfil",
  "email": "alex@example.com",       // optional
  "password": "s3cureP@ss"
}
```

**Validation:**
- `username`: 3-20 chars, `[a-zA-Z0-9_]`, unique (case-insensitive)
- `password`: 8-72 chars (bcrypt max), at least 1 letter + 1 digit
- `email`: valid format if provided, unique

**Response `201`:**
```json
{
  "user_id": "664a1b...",
  "username": "alexfil",
  "message": "Account created. You are now logged in."
}
```
Sets session cookie.

**Errors:** `409` username/email taken, `422` validation failure

---

### `POST /auth/login`

**Request:**
```json
{
  "username": "alexfil",
  "password": "s3cureP@ss"
}
```

**Response `200`:**
```json
{
  "user_id": "664a1b...",
  "username": "alexfil"
}
```
Sets session cookie.

**Errors:** `401` invalid credentials, `429` rate limited

---

### `POST /auth/logout`

Destroys session. No request body.

**Response `200`:** `{"message": "Logged out"}`

---

### `GET /auth/me`

Returns current authenticated user.

**Response `200`:**
```json
{
  "user_id": "664a1b...",
  "username": "alexfil",
  "email": "alex@example.com",
  "stats": {
    "games_played": 47,
    "games_won": 22,
    "games_lost": 20,
    "games_drawn": 5,
    "elo": 1200
  },
  "settings": { "...": "..." }
}
```

**Errors:** `401` not authenticated

---

## Game Management (REST)

### `POST /api/game/create`

Create a new game and get a join code.

**Request:**
```json
{
  "rule_variant": "berkeley_any",    // "berkeley" | "berkeley_any" (default)
  "play_as": "white",               // "white" | "black" | "random" (default)
  "time_control": "rapid"           // "rapid" (25+10) — only option in Phase 1
}
```

**Response `201`:**
```json
{
  "game_id": "664b2c...",
  "game_code": "A7K2M9",
  "play_as": "white",
  "rule_variant": "berkeley_any",
  "state": "waiting",
  "join_url": "https://kriegspiel.org/join/A7K2M9"
}
```

---

### `POST /api/game/join/{game_code}`

Join an existing game as the second player.

**Response `200`:**
```json
{
  "game_id": "664b2c...",
  "game_code": "A7K2M9",
  "play_as": "black",
  "rule_variant": "berkeley_any",
  "state": "active",
  "game_url": "https://kriegspiel.org/game/664b2c..."
}
```

**Errors:** `404` game not found, `409` game already full, `409` cannot join your own game

---

### `GET /api/game/open`

List games waiting for an opponent (lobby).

**Response `200`:**
```json
{
  "games": [
    {
      "game_code": "A7K2M9",
      "rule_variant": "berkeley_any",
      "created_by": "alexfil",
      "created_at": "2026-03-13T20:00:00Z",
      "available_color": "black"
    }
  ]
}
```

---

### `GET /api/game/{game_id}`

Get game metadata (not the board state — that comes via WebSocket).

**Response `200`:**
```json
{
  "game_id": "664b2c...",
  "game_code": "A7K2M9",
  "rule_variant": "berkeley_any",
  "state": "active",
  "white": { "username": "alexfil", "connected": true },
  "black": { "username": "opponent1", "connected": true },
  "turn": "white",
  "move_number": 12,
  "created_at": "2026-03-13T20:00:00Z"
}
```

---

### `POST /api/game/{game_id}/resign`

Current player resigns.

**Response `200`:**
```json
{
  "result": {
    "winner": "black",
    "reason": "resignation"
  }
}
```

---

### `GET /api/game/{game_id}/moves`

Full move transcript. Available to game participants at any time; available publicly after game ends.

**Response `200`:**
```json
{
  "game_id": "664b2c...",
  "rule_variant": "berkeley_any",
  "moves": [
    {
      "ply": 1,
      "color": "white",
      "question_type": "COMMON",
      "uci": "e2e4",
      "answer": {
        "main": "REGULAR_MOVE",
        "capture_square": null,
        "special": "NONE"
      },
      "move_done": true,
      "timestamp": "2026-03-13T20:01:15Z"
    }
  ]
}
```

---

## User Profile

### `GET /api/user/{username}`

Public profile.

**Response `200`:**
```json
{
  "username": "alexfil",
  "profile": {
    "bio": "Kriegspiel enthusiast",
    "avatar_url": null,
    "country": "US"
  },
  "stats": {
    "games_played": 47,
    "games_won": 22,
    "games_lost": 20,
    "games_drawn": 5,
    "elo": 1200,
    "elo_peak": 1350
  },
  "member_since": "2025-01-15T00:00:00Z"
}
```

---

### `GET /api/user/{username}/games`

Paginated game history.

**Query params:** `?page=1&per_page=20&status=completed`

**Response `200`:**
```json
{
  "games": [
    {
      "game_id": "664b2c...",
      "opponent": "opponent1",
      "play_as": "white",
      "result": "win",
      "reason": "checkmate",
      "move_count": 45,
      "played_at": "2026-03-13T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 47,
    "pages": 3
  }
}
```

---

### `PATCH /api/user/settings`

Update user settings (authenticated).

**Request:**
```json
{
  "board_theme": "dark",
  "piece_set": "merida",
  "sound_enabled": false
}
```

**Response `200`:** Updated settings object.

---

## Leaderboard

### `GET /api/leaderboard`

**Query params:** `?page=1&per_page=50`

**Response `200`:**
```json
{
  "players": [
    {
      "rank": 1,
      "username": "grandmaster42",
      "elo": 1850,
      "games_played": 312,
      "win_rate": 0.68
    }
  ],
  "pagination": { "...": "..." }
}
```

---

## WebSocket: Gameplay

### Connection

```
wss://kriegspiel.org/ws/game/{game_id}?token={session_token}
```

The `session_token` is the same session cookie value. Passed as query param because WebSocket connections don't reliably send cookies in all clients.

### Authentication Handshake

On connect, server validates token, determines player color, and sends:

```json
{
  "type": "connected",
  "game_id": "664b2c...",
  "your_color": "white",
  "your_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "turn": "white",
  "move_number": 1,
  "referee_log": [],
  "opponent_connected": true,
  "possible_actions": ["move", "ask_any"],
  "clock": {
    "white_remaining": 1500.0,
    "black_remaining": 1500.0,
    "active_color": "white"
  }
}
```

### Client → Server Messages

#### Make a move
```json
{
  "action": "move",
  "uci": "e2e4"
}
```

#### Ask "Any?" (pawn captures)
```json
{
  "action": "ask_any"
}
```

#### Resign
```json
{
  "action": "resign"
}
```

#### Offer draw (Phase 2)
```json
{
  "action": "offer_draw"
}
```

### Server → Client Messages

#### Move result (sent to moving player)
```json
{
  "type": "move_result",
  "uci": "e2e4",
  "answer": {
    "main": "REGULAR_MOVE",
    "capture_square": null,
    "special": "NONE",
    "check_1": null,
    "check_2": null
  },
  "move_done": true,
  "your_fen": "8/8/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
  "turn": "black",
  "possible_actions": [],
  "clock": {
    "white_remaining": 1498.5,
    "black_remaining": 1500.0,
    "active_color": "black"
  }
}
```

#### Opponent moved (sent to non-moving player)
```json
{
  "type": "opponent_moved",
  "illegal_attempts_this_turn": 3,
  "announcement": {
    "capture_square": null,
    "special": "NONE",
    "check_1": null,
    "check_2": null
  },
  "your_fen": "rnbqkbnr/pppppppp/8/8/8/8/8/8 b KQkq - 0 1",
  "turn": "black",
  "possible_actions": ["move", "ask_any"],
  "clock": {
    "white_remaining": 1498.5,
    "black_remaining": 1500.0,
    "active_color": "black"
  }
}
```

Note: The opponent receives the referee's public announcements (captures, checks) but NOT the move itself or whether it was legal/illegal. This preserves Kriegspiel's imperfect information.

#### "Any?" result (sent to asking player)
```json
{
  "type": "any_result",
  "result": "try",
  "must_capture_pawn": true,
  "possible_actions": ["move"]
}
```

#### "Any?" announcement (sent to opponent)
```json
{
  "type": "opponent_asked_any",
  "result": "try"
}
```

#### Illegal move (sent to moving player only)
```json
{
  "type": "move_result",
  "uci": "e2e5",
  "answer": {
    "main": "ILLEGAL_MOVE"
  },
  "move_done": false,
  "possible_actions": ["move", "ask_any"]
}
```

Note: Per Berkeley rules, the opponent hears that a move was attempted and rejected, but not what the move was. The number of illegal attempts is public.

#### Game over
```json
{
  "type": "game_over",
  "result": {
    "winner": "white",
    "reason": "checkmate",
    "special": "CHECKMATE_WHITE_WINS"
  },
  "full_board_fen": "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP22P/RNBQKBNR w KQkq - 1 3",
  "move_log_url": "/api/game/664b2c.../moves"
}
```

After game ends, the full board is revealed to both players.

#### Connection status
```json
{
  "type": "opponent_status",
  "connected": false,
  "message": "Opponent disconnected. Game paused."
}
```

### Error Messages
```json
{
  "type": "error",
  "code": "NOT_YOUR_TURN",
  "message": "It is not your turn."
}
```

Error codes: `NOT_YOUR_TURN`, `INVALID_MOVE_FORMAT`, `GAME_NOT_ACTIVE`, `SESSION_EXPIRED`

### WebSocket Close Codes

| Code | Meaning |
|---|---|
| 1000 | Normal close (game ended) |
| 1008 | Policy violation (authentication failed) |
| 4001 | Session expired during gameplay |
| 4002 | Not a participant in this game |
| 4003 | Game not in active/paused state |

---

## Standardized Error Response

All REST endpoints return errors in this format:

```json
{
  "error": {
    "code": "GAME_NOT_FOUND",
    "message": "No game with code 'XYZ123' exists.",
    "details": {}
  }
}
```

### Error Code Catalog

| Code | HTTP Status | Endpoint(s) | Description |
|---|---|---|---|
| `USERNAME_TAKEN` | 409 | POST /auth/register | Username already exists |
| `EMAIL_TAKEN` | 409 | POST /auth/register | Email already registered |
| `VALIDATION_ERROR` | 422 | POST /auth/register | Field validation failed (details in `details`) |
| `INVALID_CREDENTIALS` | 401 | POST /auth/login | Wrong username or password |
| `RATE_LIMITED` | 429 | POST /auth/login, /auth/register | Too many requests |
| `NOT_AUTHENTICATED` | 401 | All protected endpoints | No valid session or token |
| `FORBIDDEN` | 403 | Admin endpoints | User lacks required role |
| `GAME_NOT_FOUND` | 404 | /api/game/* | Game code or ID does not exist |
| `GAME_FULL` | 409 | POST /api/game/join | Game already has two players |
| `CANNOT_JOIN_OWN_GAME` | 409 | POST /api/game/join | Player trying to join their own game |
| `GAME_NOT_ACTIVE` | 400 | POST /api/game/resign, WS | Game is not in active state |
| `NOT_YOUR_TURN` | 400 | WS move/ask_any | Not this player's turn |
| `INVALID_MOVE_FORMAT` | 400 | WS move | UCI string is malformed |
| `USER_NOT_FOUND` | 404 | /api/user/* | Username does not exist |

---

## Pagination

All paginated endpoints accept these query parameters:

| Param | Default | Max | Description |
|---|---|---|---|
| `page` | 1 | — | Page number (1-indexed) |
| `per_page` | 20 | 100 | Items per page |

Paginated responses always include:

```json
{
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 47,
    "pages": 3
  }
}
```

Out-of-range pages return empty data arrays with correct `pagination.total`.

---

## Phantom Pieces (Opponent Tracking)

Phantom pieces are **entirely client-side**. No API endpoints exist for storing, retrieving, or validating phantom piece positions. The server never receives phantom data. See [FRONTEND.md](./FRONTEND.md) for the client-side implementation.

---

## Pydantic Request/Response Models

These models define the exact API contracts. Use them in `models/auth.py` and `models/game.py`.

```python
# models/auth.py
from pydantic import BaseModel, Field
from typing import Literal


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")
    email: str | None = None
    password: str = Field(min_length=8, max_length=72)


class RegisterResponse(BaseModel):
    user_id: str
    username: str
    message: str = "Account created. You are now logged in."


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: str
    username: str
```

```python
# models/game.py (API schemas — see also DATA_MODEL.md for DB schemas)
from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class CreateGameRequest(BaseModel):
    rule_variant: Literal["berkeley", "berkeley_any"] = "berkeley_any"
    play_as: Literal["white", "black", "random"] = "random"
    time_control: Literal["rapid"] = "rapid"  # 25+10 — only option in Phase 1


class CreateGameResponse(BaseModel):
    game_id: str
    game_code: str
    play_as: Literal["white", "black"]
    rule_variant: str
    state: str = "waiting"
    join_url: str


class JoinGameResponse(BaseModel):
    game_id: str
    game_code: str
    play_as: Literal["white", "black"]
    rule_variant: str
    state: str = "active"
    game_url: str


class OpenGameItem(BaseModel):
    game_code: str
    rule_variant: str
    created_by: str
    created_at: datetime
    available_color: Literal["white", "black"]


class GameHistoryItem(BaseModel):
    game_id: str
    opponent: str
    play_as: Literal["white", "black"]
    result: Literal["win", "loss", "draw"]
    reason: str
    move_count: int
    played_at: datetime
```

---

## API Authentication for External Clients

For programmatic access (bots, analysis tools), API key authentication is supported:

### `POST /api/auth/token`

Generate an API token (authenticated via session).

**Response `201`:**
```json
{
  "token": "ks_live_abc123...",
  "expires_at": "2026-06-13T00:00:00Z"
}
```

Use via header: `Authorization: Bearer ks_live_abc123...`

API tokens work for all REST endpoints and WebSocket connections (pass as `?token=` query param).
