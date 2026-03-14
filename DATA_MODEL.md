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
    "user_id": null,
    "username": null,
    "connected": false,
    "last_seen_at": null
  },

  "state": "waiting",

  "turn": "white",
  "move_number": 12,
  "half_move_count": 23,

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

  "white_fen": "8/8/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
  "black_fen": "rnbqkbnr/pppppppp/8/8/8/8/8/8 b KQkq - 0 1",

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

  "result": {
    "winner": "white",
    "reason": "checkmate",
    "ended_at": "ISODate"
  },

  "time_control": null,

  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

State values: `waiting`, `active`, `paused`, `completed`, `abandoned`, `aborted`

### Indexes

```javascript
db.games.createIndex({ "game_code": 1 }, { unique: true })
db.games.createIndex({ "state": 1, "created_at": -1 })
db.games.createIndex({ "white.user_id": 1, "state": 1 })
db.games.createIndex({ "black.user_id": 1, "state": 1 })
db.games.createIndex({ "state": 1, "updated_at": 1 },
                      { expireAfterSeconds: 86400,
                        partialFilterExpression: { "state": "waiting" } })
```

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
   └─ Insert into `games` with state="waiting", black=null

2. POST /api/game/join/{game_code}
   └─ Update `games`: set black player, state="active"

3. WebSocket /ws/game/{game_id}  (gameplay)
   └─ On each move: update `games.engine_state`, `games.moves[]`,
      `games.white_fen`, `games.black_fen`, `games.turn`

4. Game ends (checkmate/resign/etc.)
   └─ Update `games.state` → "completed", set `games.result`
   └─ Update both `users.stats` (wins/losses/elo)
   └─ Move document from `games` → `game_archives`
   └─ Write to `audit_log`
```

## Document Size Considerations

- A typical game has 40-80 half-moves, but Kriegspiel games include illegal attempts.
- Expect **100-300 entries** in `moves[]` per game (includes all "No" responses).
- At ~200 bytes per move entry, that's **20-60 KB** per game — well within MongoDB's 16 MB doc limit.
- The `engine_state` (serialized `BerkeleyGame`) is typically **5-15 KB**.
- Total game document: **30-80 KB** for a typical game.
