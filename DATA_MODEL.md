# Data Model (MongoDB)

## Database: `kriegspiel`

All collections live in a single database. MongoDB runs as a **replica set** (even if single-node) to enable Change Streams.

---

## Collection: `users`

Stores player accounts and profile data.

```json
{
  "_id": "ObjectId",
  "username": "alexfil",
  "username_display": "AlexFil",
  "email": "alex@example.com",
  "password_hash": "$2b$12$...",
  "auth_providers": ["local"],

  "profile": {
    "bio": "",
    "avatar_url": null,
    "country": null
  },

  "stats": {
    "games_played": 47,
    "games_won": 22,
    "games_lost": 20,
    "games_drawn": 5,
    "elo": 1200,
    "elo_peak": 1350
  },

  "settings": {
    "board_theme": "default",
    "piece_set": "cburnett",
    "sound_enabled": true,
    "auto_ask_any": false
  },

  "role": "user",                  // "user" | "admin"

  "status": "active",
  "last_active_at": "ISODate",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

### Indexes

```javascript
db.users.createIndex({ "username": 1 }, { unique: true })
db.users.createIndex({ "email": 1 }, { unique: true, sparse: true })
db.users.createIndex({ "stats.elo": -1 })
db.users.createIndex({ "status": 1, "last_active_at": -1 })
```

---

## Collection: `games`

Stores active and recently completed games. This is the hot collection.

```json
{
  "_id": "ObjectId",
  "game_code": "A7K2M9",
  "rule_variant": "berkeley_any",

  "white": {
    "user_id": "ObjectId",
    "username": "alexfil",
    "connected": true,
    "last_seen_at": "ISODate"
  },
  "black": {
    "user_id": "ObjectId",
    "username": "opponent1",
    "connected": true,
    "last_seen_at": "ISODate"
  },

  "state": "active",
  "expires_at": null,                  // Waiting-game TTL (null once the game starts)

  "turn": "black",
  "move_number": 1,                 // Chess full-move counter (increments after Black moves)
  "half_move_count": 1,             // Total ply counter (all successful moves, both colors)

  "engine_state": {
    "version": "1.2.0",
    "game_type": "BerkeleyGame",
    "game_state": {
      "any_rule": true,
      "board_fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
      "must_use_pawns": false,
      "game_over": false,
      "white_scoresheet": {},
      "black_scoresheet": {}
    }
  },

  "white_fen": "8/8/8/8/4P3/8/PPPP1PPP/RNBQKBNR b - - 0 1",
  "black_fen": "rnbqkbnr/pppppppp/8/8/8/8/8/8 b - - 0 1",

  "moves": [
    {
      "ply": 1,
      "color": "white",
      "question_type": "COMMON",
      "uci": "e2e4",
      "answer": {
        "main": "REGULAR_MOVE",
        "capture_square": null,
        "special": "NONE",
        "check_1": null,
        "check_2": null
      },
      "move_done": true,
      "timestamp": "ISODate"
    }
  ],

  "result": null,

  "time_control": {
    "base": 1500,                    // 25 minutes in seconds
    "increment": 10,                 // 10 seconds per move
    "white_remaining": 1423.5,       // Seconds remaining for white
    "black_remaining": 1500.0,       // Seconds remaining for black
    "active_color": "black"          // Whose clock is ticking (null if paused)
  },

  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

State values: `waiting`, `active`, `paused`, `completed`, `abandoned`, `aborted`. See [ARCHITECTURE.md](./ARCHITECTURE.md) for the full state machine with transition triggers and timeout values.

### Indexes

```javascript
db.games.createIndex({ "game_code": 1 }, { unique: true })
db.games.createIndex({ "state": 1, "created_at": -1 })
db.games.createIndex({ "white.user_id": 1, "state": 1 })
db.games.createIndex({ "black.user_id": 1, "state": 1 })
db.games.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 })
```

`expires_at` is set only for games in the `waiting` state. When a second player joins, set `expires_at` to `null`.

---

## Collection: `game_archives`

Completed games are moved here from `games` (keeps the hot collection small). Same schema as `games` but immutable.

### Indexes

```javascript
db.game_archives.createIndex({ "white.user_id": 1, "created_at": -1 })
db.game_archives.createIndex({ "black.user_id": 1, "created_at": -1 })
db.game_archives.createIndex({ "result.winner": 1, "created_at": -1 })
db.game_archives.createIndex({ "created_at": -1 })
```

---

## Collection: `audit_log`

Append-only log for debugging and moderation.

```json
{
  "_id": "ObjectId",
  "event": "game.move",
  "user_id": "ObjectId",
  "game_id": "ObjectId",
  "details": {
    "uci": "e2e4",
    "answer": "REGULAR_MOVE"
  },
  "ip": "192.168.1.1",
  "timestamp": "ISODate"
}
```

### Indexes

```javascript
db.audit_log.createIndex({ "timestamp": 1 }, { expireAfterSeconds: 7776000 })
db.audit_log.createIndex({ "user_id": 1, "timestamp": -1 })
db.audit_log.createIndex({ "game_id": 1 })
```

---

## Collection: `sessions`

Server-side session storage.

```json
{
  "_id": "session_abc123def456",
  "user_id": "ObjectId",
  "username": "alexfil",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "created_at": "ISODate",
  "expires_at": "ISODate"
}
```

### Indexes

```javascript
db.sessions.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 })
db.sessions.createIndex({ "user_id": 1 })
```

---

## Data Flow: Game Lifecycle

```
1. POST /api/game/create
   └─ Insert into `games` with state="waiting", black=null,
      expires_at=now+24h

2. POST /api/game/join/{game_code}
   └─ Update `games`: set black player, state="active", expires_at=null

3. WebSocket /ws/game/{game_id}  (gameplay)
   └─ On each move: update `games.engine_state`, `games.moves[]`,
      `games.white_fen`, `games.black_fen`, `games.turn`

4. Game ends (checkmate/resign/etc.)
   └─ Update `games.state` → "completed", set `games.result`
   └─ Update both `users.stats` (wins/losses/elo)
   └─ Move document from `games` → `game_archives`
   └─ Write to `audit_log`
```

---

## Pydantic Models

These models map directly to the MongoDB documents above. Use them in `models/game.py` and `models/user.py`.

```python
# models/game.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class PlayerEmbed(BaseModel):
    user_id: str | None = None
    username: str | None = None
    connected: bool = False
    last_seen_at: datetime | None = None


class MoveAnswer(BaseModel):
    main: str                              # MainAnnouncement enum name
    capture_square: str | None = None      # e.g., "d4"
    special: str = "NONE"                  # SpecialCaseAnnouncement enum name
    check_1: str | None = None
    check_2: str | None = None


class MoveRecord(BaseModel):
    ply: int                               # 1-indexed sequential move counter
    color: Literal["white", "black"]
    question_type: Literal["COMMON", "ASK_ANY"]
    uci: str | None = None                 # None for ASK_ANY
    answer: MoveAnswer
    move_done: bool
    timestamp: datetime


class GameResult(BaseModel):
    winner: Literal["white", "black"] | None = None   # None for draws
    reason: str                            # "checkmate", "stalemate", "resignation", "abandonment", etc.
    ended_at: datetime


class GameDocument(BaseModel):
    game_code: str
    rule_variant: Literal["berkeley", "berkeley_any"] = "berkeley_any"
    white: PlayerEmbed
    black: PlayerEmbed
    state: Literal["waiting", "active", "paused", "completed", "abandoned", "aborted"]
    expires_at: datetime | None = None      # Waiting-game TTL only
    turn: Literal["white", "black"] = "white"
    move_number: int = 1                   # Chess full-move counter
    half_move_count: int = 0               # Ply counter
    engine_state: dict                     # Serialized BerkeleyGame (see GAME_ENGINE.md)
    white_fen: str                         # Sanitized display FEN showing only white's pieces
    black_fen: str                         # Sanitized display FEN showing only black's pieces
    moves: list[MoveRecord] = []
    result: GameResult | None = None
    time_control: dict                     # Rapid 25+10 clock state in Phase 1
    created_at: datetime
    updated_at: datetime
```

```python
# models/user.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class UserStats(BaseModel):
    games_played: int = 0
    games_won: int = 0
    games_lost: int = 0
    games_drawn: int = 0
    elo: int = 1200
    elo_peak: int = 1200


class UserSettings(BaseModel):
    board_theme: str = "default"
    piece_set: str = "cburnett"
    sound_enabled: bool = True
    auto_ask_any: bool = False


class UserProfile(BaseModel):
    bio: str = ""
    avatar_url: str | None = None
    country: str | None = None


class UserDocument(BaseModel):
    username: str                          # Lowercase, unique
    username_display: str                  # Original case for display
    email: str | None = None
    password_hash: str
    auth_providers: list[str] = ["local"]
    profile: UserProfile = UserProfile()
    stats: UserStats = UserStats()
    settings: UserSettings = UserSettings()
    role: Literal["user", "admin"] = "user"
    status: Literal["active", "suspended", "deleted"] = "active"
    last_active_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
```

---

## Common MongoDB Query Patterns

These are the exact queries the service layer should use. All queries use Motor's async API.

```python
# ── Open games (lobby) ─────────────────────────────────────────
await db.games.find(
    {"state": "waiting"}
).sort("created_at", -1).to_list(50)

# ── User's active games ───────────────────────────────────────
await db.games.find({
    "$or": [
        {"white.user_id": user_id},
        {"black.user_id": user_id}
    ],
    "state": {"$in": ["active", "paused"]}
}).to_list(100)

# ── Find game by join code ────────────────────────────────────
await db.games.find_one({"game_code": game_code})

# ── Find game metadata by ID (active or archived) ─────────────
await db.games.find_one({"_id": game_id}) or await db.game_archives.find_one({"_id": game_id})

# ── Leaderboard ───────────────────────────────────────────────
await db.users.find(
    {"status": "active", "stats.games_played": {"$gte": 5}}
).sort("stats.elo", -1).skip(offset).limit(per_page).to_list(per_page)

# ── User game history (paginated) ─────────────────────────────
await db.game_archives.find({
    "$or": [
        {"white.user_id": user_id},
        {"black.user_id": user_id}
    ]
}).sort("created_at", -1).skip(offset).limit(per_page).to_list(per_page)

# ── Count for pagination ──────────────────────────────────────
total = await db.game_archives.count_documents({
    "$or": [
        {"white.user_id": user_id},
        {"black.user_id": user_id}
    ]
})
```

---

## Document Size Considerations

- A typical game has 40-80 half-moves, but Kriegspiel games include illegal attempts.
- Expect **100-300 entries** in `moves[]` per game (includes all "No" responses).
- At ~200 bytes per move entry, that's **20-60 KB** per game — well within MongoDB's 16 MB doc limit.
- The `engine_state` (serialized `BerkeleyGame`) is typically **5-15 KB**.
- Total game document: **30-80 KB** for a typical game.
