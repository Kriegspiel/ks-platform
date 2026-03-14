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
  "play_as": "white"                 // "white" | "black" | "random" (default)
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
  "your_fen": "RNBQKBNR/PPPPPPPP/8/8/8/8/8/8",
  "turn": "white",
  "move_number": 1,
  "opponent_connected": true,
  "possible_actions": ["move", "ask_any"]
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
  "your_fen": "RNBQKBNR/PPPP1PPP/8/4P3/8/8/8/8",
  "turn": "black",
  "possible_actions": []
}
```

#### Opponent moved (sent to non-moving player)
```json
{
  "type": "opponent_moved",
  "announcement": {
    "capture_square": null,
    "special": "NONE",
    "check_1": null,
    "check_2": null
  },
  "your_fen": "rnbqkbnr/pppppppp/8/8/8/8/8/8",
  "turn": "black",
  "possible_actions": ["move", "ask_any"]
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
