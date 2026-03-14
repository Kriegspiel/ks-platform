# Game Engine Integration

## Overview

The platform uses the **`kriegspiel`** PyPI package ([ks-game](https://github.com/kriegspiel/ks-game)) as the single source of truth for game logic. The platform never re-implements chess rules or Kriegspiel-specific logic — it delegates entirely to the engine.

## Dependency

```
# requirements.txt
kriegspiel>=1.1.2
```

```python
from kriegspiel.berkeley import BerkeleyGame
from kriegspiel.move import (
    KriegspielMove,
    KriegspielAnswer,
    QuestionAnnouncement,
    MainAnnouncement,
    SpecialCaseAnnouncement,
)
from kriegspiel.serialization import (
    save_game_to_json,
    load_game_from_json,
    KriegspielJSONEncoder,
)
import chess
```

## GameService Implementation

```python
"""
game_service.py — Orchestrates game lifecycle around the kriegspiel engine.

This is the central service. Routers and WebSocket handlers call into this;
it owns the BerkeleyGame instances and MongoDB persistence.
"""

from kriegspiel.berkeley import BerkeleyGame
from kriegspiel.move import (
    KriegspielMove, KriegspielAnswer,
    QuestionAnnouncement as QA,
    MainAnnouncement as MA,
    SpecialCaseAnnouncement as SA,
)
import chess
import json
from datetime import datetime, timezone


class GameService:

    def __init__(self, db, cache: GameCache):
        self.db = db                  # Motor async MongoDB client
        self.cache = cache            # In-memory LRU cache

    # ── Game Creation ────────────────────────────────────────

    async def create_game(
        self,
        user_id: str,
        username: str,
        rule_variant: str = "berkeley_any",
        play_as: str = "random",
    ) -> dict:
        """Create a new game, store initial engine state, return game doc."""

        any_rule = rule_variant == "berkeley_any"
        game = BerkeleyGame(any_rule=any_rule)

        # Determine color assignment
        color = self._resolve_color(play_as)

        # Serialize initial engine state
        engine_state = self._serialize_engine(game)

        game_doc = {
            "game_code": self._generate_code(),
            "rule_variant": rule_variant,
            "white": self._make_player(user_id, username) if color == "white" else self._empty_player(),
            "black": self._make_player(user_id, username) if color == "black" else self._empty_player(),
            "state": "waiting",
            "turn": "white",
            "move_number": 0,
            "half_move_count": 0,
            "engine_state": engine_state,
            "white_fen": self._player_fen(game, chess.WHITE),
            "black_fen": self._player_fen(game, chess.BLACK),
            "moves": [],
            "result": None,
            "time_control": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        result = await self.db.games.insert_one(game_doc)
        game_doc["_id"] = result.inserted_id

        # Cache the live engine instance
        await self.cache.put(str(result.inserted_id), game)

        return game_doc

    # ── Move Execution ───────────────────────────────────────

    async def attempt_move(
        self,
        game_id: str,
        color: str,
        uci: str,
    ) -> dict:
        """
        Player attempts a regular move.

        Returns a dict with:
          - answer: the KriegspielAnswer
          - move_done: bool
          - your_fen: updated FEN for the moving player
          - opponent_fen: updated FEN for the opponent
          - game_over: bool
          - result: game result if over
          - possible_actions: list of available actions
        """

        game = await self.cache.get(game_id)

        # Build the KriegspielMove
        chess_move = chess.Move.from_uci(uci)
        ks_move = KriegspielMove(QA.COMMON, chess_move)

        # Validate: is this move in possible_to_ask?
        if not game.is_possible_to_ask(ks_move):
            return {
                "answer": {"main": "IMPOSSIBLE_TO_ASK"},
                "move_done": False,
                "game_over": False,
            }

        # Execute
        answer = game.ask_for(ks_move)

        # Build response
        response = self._build_move_response(game, answer, color)

        # Record in move log
        move_record = self._build_move_record(color, "COMMON", uci, answer)

        # Persist
        await self._persist_game_state(game_id, game, move_record)

        # Check game over
        if game.is_game_over():
            await self._handle_game_over(game_id, game, answer)

        return response

    # ── "Any?" Question ──────────────────────────────────────

    async def ask_any(self, game_id: str, color: str) -> dict:
        """
        Player asks "Any pawn captures?"

        Returns:
          - result: "try" (HAS_ANY) or "no" (NO_ANY)
          - must_capture_pawn: bool
          - possible_actions: updated list
        """

        game = await self.cache.get(game_id)

        ks_move = KriegspielMove(QA.ASK_ANY)

        if not game.is_possible_to_ask(ks_move):
            return {"error": "Cannot ask 'Any?' right now"}

        answer = game.ask_for(ks_move)

        result = "try" if answer.main_announcement == MA.HAS_ANY else "no"

        move_record = self._build_move_record(color, "ASK_ANY", None, answer)
        await self._persist_game_state(game_id, game, move_record)

        return {
            "result": result,
            "must_capture_pawn": game.must_use_pawns,
            "possible_actions": self._get_possible_actions(game),
        }

    # ── Board View Generation ────────────────────────────────

    def _player_fen(self, game: BerkeleyGame, color: bool) -> str:
        """
        Generate a FEN showing only the given player's pieces.

        The opponent's pieces are replaced with empty squares.
        This is what each player sees on their board.

        NOTE: game._board is a private attribute of BerkeleyGame. We access it
        intentionally because the engine does not expose a public board accessor.
        If the kriegspiel package adds a public API for this in the future, migrate to it.
        """
        board = game._board.copy()

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color != color:
                board.remove_piece_at(square)

        return board.fen()

    # ── Serialization ────────────────────────────────────────

    def _serialize_engine(self, game: BerkeleyGame) -> dict:
        """Serialize BerkeleyGame to a dict suitable for MongoDB storage."""
        # Use kriegspiel's built-in JSON serialization
        json_str = json.dumps(game, cls=KriegspielJSONEncoder)
        return json.loads(json_str)

    async def _load_engine(self, game_id: str) -> BerkeleyGame:
        """Load BerkeleyGame from MongoDB."""
        doc = await self.db.games.find_one({"_id": game_id})
        # Write engine_state to temp file, load via kriegspiel
        import tempfile, os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(doc["engine_state"], f)
            tmp_path = f.name
        try:
            game = BerkeleyGame.load_game(tmp_path)
        finally:
            os.unlink(tmp_path)
        return game

    # ── Persistence ──────────────────────────────────────────

    async def _persist_game_state(
        self,
        game_id: str,
        game: BerkeleyGame,
        move_record: dict,
    ):
        """Write current game state to MongoDB."""
        engine_state = self._serialize_engine(game)
        turn = "white" if game.turn == chess.WHITE else "black"

        await self.db.games.update_one(
            {"_id": game_id},
            {
                "$set": {
                    "engine_state": engine_state,
                    "white_fen": self._player_fen(game, chess.WHITE),
                    "black_fen": self._player_fen(game, chess.BLACK),
                    "turn": turn,
                    "updated_at": datetime.now(timezone.utc),
                },
                "$push": {"moves": move_record},
                "$inc": {"half_move_count": 1 if move_record["move_done"] else 0},
            }
        )

        # Update cache
        await self.cache.put(game_id, game)

    # ── Answer Translation ───────────────────────────────────

    def _build_move_response(
        self,
        game: BerkeleyGame,
        answer: KriegspielAnswer,
        color: str,
    ) -> dict:
        """Translate KriegspielAnswer into a response dict."""

        capture_square = None
        if answer.capture_at_square is not None:
            capture_square = chess.square_name(answer.capture_at_square)

        return {
            "answer": {
                "main": answer.main_announcement.name,
                "capture_square": capture_square,
                "special": answer.special_announcement.name,
                "check_1": answer.check_1.name if answer.check_1 else None,
                "check_2": answer.check_2.name if answer.check_2 else None,
            },
            "move_done": answer.move_done,
            "game_over": game.is_game_over(),
            "possible_actions": self._get_possible_actions(game),
        }

    def _get_possible_actions(self, game: BerkeleyGame) -> list[str]:
        """Determine what actions the current player can take."""
        actions = []
        for move in game.possible_to_ask:
            if move.question_type == QA.COMMON and "move" not in actions:
                actions.append("move")
            if move.question_type == QA.ASK_ANY and "ask_any" not in actions:
                actions.append("ask_any")
        return actions

    # ── Helpers ───────────────────────────────────────────────

    def _build_move_record(
        self, color: str, question_type: str, uci: str | None, answer: KriegspielAnswer, ply_number: int
    ) -> dict:
        capture_square = None
        if answer.capture_at_square is not None:
            capture_square = chess.square_name(answer.capture_at_square)

        return {
            "ply": ply_number,   # Caller must pass: len(game_doc["moves"]) + 1
            "color": color,
            "question_type": question_type,
            "uci": uci,
            "answer": {
                "main": answer.main_announcement.name,
                "capture_square": capture_square,
                "special": answer.special_announcement.name,
                "check_1": answer.check_1.name if answer.check_1 else None,
                "check_2": answer.check_2.name if answer.check_2 else None,
            },
            "move_done": answer.move_done,
            "timestamp": datetime.now(timezone.utc),
        }

    @staticmethod
    def _generate_code() -> str:
        """Generate a 6-char alphanumeric join code."""
        import secrets, string
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(6))

    @staticmethod
    def _make_player(user_id, username):
        return {
            "user_id": user_id,
            "username": username,
            "connected": False,
            "last_seen_at": None,
        }

    @staticmethod
    def _empty_player():
        return {
            "user_id": None,
            "username": None,
            "connected": False,
            "last_seen_at": None,
        }

    @staticmethod
    def _resolve_color(play_as: str) -> str:
        if play_as == "random":
            import random
            return random.choice(["white", "black"])
        return play_as
```

    # ── Resign ─────────────────────────────────────────────────

    async def resign(self, game_id: str, color: str) -> dict:
        """Player resigns. Opponent wins."""
        winner = "black" if color == "white" else "white"
        await self._end_game(game_id, winner=winner, reason="resignation")
        return {"winner": winner, "reason": "resignation"}

    # ── Abandon ────────────────────────────────────────────────

    async def handle_abandon(self, game_id: str, disconnected_color: str) -> dict:
        """Called when disconnected player doesn't return within 15 minutes."""
        winner = "black" if disconnected_color == "white" else "white"
        await self._end_game(game_id, winner=winner, reason="abandonment")
        return {"winner": winner, "reason": "abandonment"}

    # ── End Game ───────────────────────────────────────────────

    async def _end_game(
        self,
        game_id: str,
        winner: str | None,          # None for draws
        reason: str,
    ):
        """
        Full game-ending flow:
        1. Update game state to "completed" with result.
        2. Update both users' stats (games_played, wins/losses/draws, ELO).
        3. Move game document from `games` to `game_archives`.
        4. Evict game from in-memory cache.
        5. Write to audit_log.
        """
        now = datetime.now(timezone.utc)

        # 1. Update game document
        game_doc = await self.db.games.find_one_and_update(
            {"_id": game_id},
            {"$set": {
                "state": "completed",
                "result": {
                    "winner": winner,
                    "reason": reason,
                    "ended_at": now,
                },
                "updated_at": now,
            }},
            return_document=True,
        )

        # 2. Update user stats
        white_uid = game_doc["white"]["user_id"]
        black_uid = game_doc["black"]["user_id"]

        if winner == "white":
            await self.db.users.update_one({"_id": white_uid}, {"$inc": {"stats.games_played": 1, "stats.games_won": 1}})
            await self.db.users.update_one({"_id": black_uid}, {"$inc": {"stats.games_played": 1, "stats.games_lost": 1}})
        elif winner == "black":
            await self.db.users.update_one({"_id": black_uid}, {"$inc": {"stats.games_played": 1, "stats.games_won": 1}})
            await self.db.users.update_one({"_id": white_uid}, {"$inc": {"stats.games_played": 1, "stats.games_lost": 1}})
        else:
            # Draw
            await self.db.users.update_one({"_id": white_uid}, {"$inc": {"stats.games_played": 1, "stats.games_drawn": 1}})
            await self.db.users.update_one({"_id": black_uid}, {"$inc": {"stats.games_played": 1, "stats.games_drawn": 1}})

        # 3. Archive: copy to game_archives, delete from games
        await self.db.game_archives.insert_one(game_doc)
        await self.db.games.delete_one({"_id": game_id})

        # 4. Evict from cache
        await self.cache.evict(game_id)

        # 5. Audit log
        await self.db.audit_log.insert_one({
            "event": "game.ended",
            "game_id": game_id,
            "details": {"winner": winner, "reason": reason},
            "timestamp": now,
        })
```

## Time Control (Fischer Clock)

Phase 1 implements a single time control: **Rapid 25+10** (25 minutes base + 10 seconds increment per move).

The clock is managed **server-side** to prevent cheating. The `kriegspiel` engine does not handle time — the platform manages it independently.

```python
class ClockManager:
    """Fischer clock for a single game. Server-side, authoritative."""

    def __init__(self, base_seconds: int = 1500, increment_seconds: int = 10):
        self.base = base_seconds          # 25 minutes = 1500 seconds
        self.increment = increment_seconds # 10 seconds
        self.remaining = {"white": float(base_seconds), "black": float(base_seconds)}
        self.active_color: str | None = None
        self.last_tick: float | None = None  # time.monotonic()

    def start(self, color: str):
        """Start the clock for the given color (called when their turn begins)."""
        self.active_color = color
        self.last_tick = time.monotonic()

    def stop_and_increment(self, color: str):
        """
        Stop the clock for the given color (they made a move).
        Add increment. Called after a successful move (move_done=True).
        """
        if self.active_color == color and self.last_tick is not None:
            elapsed = time.monotonic() - self.last_tick
            self.remaining[color] -= elapsed
            self.remaining[color] += self.increment
            self.active_color = None
            self.last_tick = None

    def get_remaining(self, color: str) -> float:
        """Get remaining time in seconds. Accounts for currently ticking time."""
        remaining = self.remaining[color]
        if self.active_color == color and self.last_tick is not None:
            elapsed = time.monotonic() - self.last_tick
            remaining -= elapsed
        return max(0, remaining)

    def is_flagged(self, color: str) -> bool:
        """Check if a player has run out of time."""
        return self.get_remaining(color) <= 0

    def pause(self):
        """Pause the clock (e.g., opponent disconnects)."""
        if self.active_color and self.last_tick:
            elapsed = time.monotonic() - self.last_tick
            self.remaining[self.active_color] -= elapsed
            self.last_tick = None

    def resume(self):
        """Resume the clock after pause."""
        if self.active_color:
            self.last_tick = time.monotonic()

    def to_dict(self) -> dict:
        """Serialize for MongoDB storage and WebSocket messages."""
        return {
            "base": self.base,
            "increment": self.increment,
            "white_remaining": round(self.get_remaining("white"), 1),
            "black_remaining": round(self.get_remaining("black"), 1),
            "active_color": self.active_color,
        }
```

### Clock Integration with GameService

- On game start (both players connected): `clock.start("white")`.
- After each successful move (`move_done=True`): `clock.stop_and_increment(moving_color)` then `clock.start(opponent_color)`.
- On player disconnect: `clock.pause()`.
- On player reconnect: `clock.resume()`.
- **Flag check**: after every move and on a 1-second server-side timer, check `clock.is_flagged()`. If flagged, the game ends with the opponent winning.
- Clock state is included in every WebSocket message to both players (see [API_SPEC.md](./API_SPEC.md)).
- Clock state is serialized to MongoDB alongside `engine_state` on every move.

### WebSocket Clock Messages

Clock remaining times are sent with every `move_result` and `opponent_moved` message:

```json
{
  "clock": {
    "white_remaining": 1423.5,
    "black_remaining": 1500.0,
    "active_color": "black"
  }
}
```

When a player flags (runs out of time):

```json
{
  "type": "game_over",
  "result": {
    "winner": "black",
    "reason": "timeout",
    "special": "FLAG"
  },
  "clock": { "white_remaining": 0, "black_remaining": 892.3, "active_color": null }
}
```

## Pawn Promotion

Pawn promotion is handled via the UCI move format. When a pawn reaches the last rank, the client appends a promotion suffix to the UCI string:

| UCI | Meaning |
|---|---|
| `e7e8q` | Promote to Queen |
| `e7e8r` | Promote to Rook |
| `e7e8b` | Promote to Bishop |
| `e7e8n` | Promote to Knight |

- If the client sends a promotion move without a suffix (e.g., `e7e8`), the server defaults to Queen promotion by appending `q`.
- Promotion is **silent** per Berkeley rules — the referee says nothing special about it beyond the normal move result ("Yes"/"No"). The opponent does not know a promotion occurred.
- The `chess.Move.from_uci()` function handles the promotion suffix natively.
- See [FRONTEND.md](./FRONTEND.md) for the promotion piece selector modal UI.

## En Passant

En passant is handled entirely by the `kriegspiel` engine. No special platform logic is needed.

- The move UCI looks like a regular pawn move (e.g., `d5e6`) where the target square is empty.
- The referee announces **"Capture on e6"** (the target square where the capturing pawn lands, not the square of the captured pawn).
- The captured pawn disappears from its original square. The `_player_fen` function reflects this correctly because it reads the engine's board state after the move.
- En passant is **silent** per Berkeley rules — the referee says "Capture on [square]" but does not announce that it was en passant.

## No Legal Moves (Checkmate / Stalemate)

When a player has no legal moves, the engine detects this automatically:

- If `game.possible_to_ask` returns an empty list and the player is **in check** → **checkmate**.
- If `game.possible_to_ask` returns an empty list and the player is **not in check** → **stalemate**.
- In both cases, `game.is_game_over()` returns `True` and `answer.special_announcement` contains the result (`CHECKMATE_WHITE_WINS`, `CHECKMATE_BLACK_WINS`, or `DRAW_STALEMATE`).
- The `_get_possible_actions` method returns `[]`, and the WebSocket handler triggers the game-over flow.

The platform does **not** need to implement checkmate/stalemate detection — it relies entirely on the engine.

## Error Recovery

If the game engine state becomes corrupted (e.g., `BerkeleyGame.load_game()` fails):

1. Log the error with full context: `log.error("engine.state_corrupted", game_id=game_id, error=str(e))`.
2. Send an error message to both connected players: `{"type": "error", "code": "ENGINE_STATE_CORRUPTED", "message": "Game state is corrupted. This game has been abandoned."}`.
3. Mark the game as `abandoned` in the database (no winner).
4. Write to `audit_log` with `event: "game.engine_corrupted"`.
5. The raw `engine_state` JSON remains in the game document for admin debugging.

This should be extremely rare in practice — the engine serialization is well-tested.

## Mapping: Engine Enums → User-Facing Messages

The engine speaks in enum values. The platform translates them into human-readable announcements:

| Engine Value | Referee Says (UI) | Sent to |
|---|---|---|
| `REGULAR_MOVE` | *(move executes silently)* | Moving player only |
| `ILLEGAL_MOVE` | "No." | Moving player; opponent hears attempt count |
| `IMPOSSIBLE_TO_ASK` | "Nonsense." | Moving player only |
| `CAPTURE_DONE` | "Capture on {square}." | Both players |
| `HAS_ANY` | "Try." | Both players |
| `NO_ANY` | "No." | Both players |
| `CHECK_RANK` | "Check on a rank." | Both players |
| `CHECK_FILE` | "Check on a file." | Both players |
| `CHECK_LONG_DIAGONAL` | "Check on the long diagonal." | Both players |
| `CHECK_SHORT_DIAGONAL` | "Check on the short diagonal." | Both players |
| `CHECK_KNIGHT` | "Check from a knight." | Both players |
| `CHECKMATE_WHITE_WINS` | "Checkmate. White wins." | Both players |
| `CHECKMATE_BLACK_WINS` | "Checkmate. Black wins." | Both players |
| `DRAW_STALEMATE` | "Stalemate. Draw." | Both players |
| `DRAW_INSUFFICIENT_MATERIAL` | "Insufficient material. Draw." | Both players |
| `DRAW_HALFMOVE_LIMIT` | "Move limit reached. Draw." | Both players |

## What the Opponent Hears

Per Berkeley rules, both players hear all referee announcements. But the opponent does NOT hear:
- What move was attempted
- Whether a specific move was legal or illegal (they only know an attempt happened)

The opponent sees:
- That the other player made an attempt (increment attempt counter)
- Capture announcements (square only)
- Check announcements (direction only)
- "Any?" results
- Game end announcements

## Game Inspection (Post-Game Analysis)

After a game ends, the full referee board is revealed. The game transcript (all moves + answers) becomes available at `/api/game/{game_id}/moves`.

The inspection view shows:
1. Move-by-move replay with the referee's board
2. Each player's visible board at each step
3. All announcements in chronological order
4. A toggle to view from White's or Black's perspective

This is built from the `moves[]` array in the game document and the saved `engine_state`.
