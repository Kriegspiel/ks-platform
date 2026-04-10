# Shared Data Structures

This document explains the shared identifiers, persisted records, API payloads, and derived statistics that matter across the active Kriegspiel.org repos.

For the exhaustive file/module inventory, see [`module-index.md`](./module-index.md).

## Identifiers

### `game_id`

- Internal Mongo `_id`.
- Usually an `ObjectId`.
- Used for persistence, foreign-key style references, and server-side lookups.
- Should not be the primary identifier shown in public browser URLs.

### `game_code`

- Six-character human-facing game code from a 31-character safe alphabet.
- Used in public URLs and join/review flows.
- Example:
  - `/game/ABC123`
  - `/game/ABC123/review`

### `user_id`

- Mongo `_id` for users.
- Usually embedded into `white_player.id` / `black_player.id` inside games.

### `session_id`

- Mongo `_id` for browser auth sessions.
- Stored server-side and represented in cookies.

## Live Game Persistence

The canonical live-game record is defined in [`ks-backend/src/app/models/game.py`](/home/fil/dev/kriegspiel/ks-backend/src/app/models/game.py) as `GameDocument`.

Important fields:

- `_id`
- `game_code`
- `state`
  - `waiting`
  - `active`
  - `completed`
- `rule_variant`
  - currently `berkeley`
  - or `berkeley+any`
- `white_player`
- `black_player`
- `engine_state`
- `time_control`
- `result`
- `created_at`
- `updated_at`
- `completed_at`

### `engine_state`

`engine_state` is the single canonical home for live referee state.

It contains:

- serialized `ks-game` engine position
- scoresheets
- possible actions / repairable derived state
- information needed to rebuild player projections and replay transcripts

Historical root-level scoresheet duplicates were migrated away. New code should never reintroduce:

- `white_scoresheet`
- `black_scoresheet`

at the root of the game document.

### Embedded players

`PlayerEmbed` keeps the per-side public snapshot that belongs inside a game document:

- `id`
- `username`
- `display_name`
- `is_bot`
- color assignment / player role context

This lets a game stay readable even if the user profile later changes.

## Archived Game Records

Completed games are written to `game_archives`.

Archived records are the source of truth for:

- public profile game history
- review/replay
- rating-history generation
- technical reports such as the bots report
- static leaderboard snapshots

Important normalized fields in archives:

- `game_code`
- player identities
- `rule_variant`
- `result`
- `completed_at`
- normalized `rating_snapshot`
- transcript-ready move/replay data

The archive rating snapshots were globally recalculated, so the backend no longer relies on older fallback shapes.

## Engine and Referee Objects

The `ks-game` repo provides the engine-level types used by the backend.

### `QuestionAnnouncement`

Defined in [`ks-game/kriegspiel/move.py`](/home/fil/dev/kriegspiel/ks-game/kriegspiel/move.py).

Represents what the player is asking:

- `COMMON`
- `ASK_ANY`

### `KriegspielMove`

Referee question object:

- `question_type`
- `chess_move`

This is the engine-side representation of a move attempt or `any pawn captures?` query.

### `MainAnnouncement`

Primary referee outcome:

- `IMPOSSIBLE_TO_ASK`
- `ILLEGAL_MOVE`
- `REGULAR_MOVE`
- `CAPTURE_DONE`
- `HAS_ANY`
- `NO_ANY`

### `SpecialCaseAnnouncement`

Secondary announcements:

- draw states
- checkmate states
- check families such as file, rank, diagonal, knight, or double-check

### `KriegspielAnswer`

Referee response object containing:

- `main_announcement`
- optional `capture_at_square`
- optional `special_announcement`
- convenience flags such as `move_done`

### `KriegspielScoresheet`

The engine-owned scoresheet structure from which the backend builds:

- player-visible scoresheet turns
- referee logs
- replay ply boxes

## API Payloads

### Active game view

`GameStateResponse` is the main active-game payload returned by the backend.

Important properties:

- `game_code`
- `state`
- `your_color`
- `your_fen`
- `turn`
- `allowed_moves`
- `referee_log`
- `referee_turns`
- player-visible scoresheets

Security rule:

- active-game payloads must expose only the requesting player’s visible projection
- not the full board
- not the opponent’s hidden pieces

### Game transcript / review payload

`GameTranscriptResponse` contains replay-ready data for completed games.

Important properties:

- metadata for the completed game
- ordered move/attempt entries
- replay board states for:
  - referee view
  - white view
  - black view

Completed review is allowed to expose full-board replay data by design.

### Lobby payloads

The lobby uses:

- `OpenGameItem`
- `OpenGamesResponse`
- `LobbyStatsResponse`
- `MyGamesResponse`

Important derived rules:

- waiting games are joinable via `game_code`
- active games shown in `mine` are driven by backend ownership/visibility

## User and Rating Shapes

Defined in [`ks-backend/src/app/models/user.py`](/home/fil/dev/kriegspiel/ks-backend/src/app/models/user.py).

### `EloRatingTrack`

Per-track rating block:

- current Elo
- peak Elo
- last-updated markers as needed by the backend

### `ResultTrack`

Per-track outcome counters:

- `games_played`
- `wins`
- `losses`
- `draws`

### `UserStats`

Contains:

- `elo`
- `elo_peak`
- `ratings`
  - `overall`
  - `vs_humans`
  - `vs_bots`
- `results`
  - `overall`
  - `vs_humans`
  - `vs_bots`

`elo` / `elo_peak` are aliases for overall rating for compatibility with simpler consumers.

### `UserSettings`

Current user-controlled preferences, such as:

- theme
- board orientation defaults
- related UI settings

### `UserProfile`

Public profile fields used by the frontend:

- username
- display name
- bio/description if present
- member-since metadata
- bot markers and owner email where allowed

## Bot Data

Bot-specific models live in [`ks-backend/src/app/models/bot.py`](/home/fil/dev/kriegspiel/ks-backend/src/app/models/bot.py).

### `BotProfile`

Important fields:

- `api_token_id`
- `api_token_digest`
- `listed`
- `owner_email`
- join-sampling state such as cooldown markers

Bot auth uses:

- HMAC digest verification
- in-process token cache with a `3600s` TTL

Legacy bcrypt token fallback has already been removed from live code.

### Public bot list

`BotListItem` and `BotListResponse` are used by:

- selected-bot create-game flows
- public bot listings

## Rating History and Reporting

### Rating history endpoint

The backend now owns rating-history aggregation.

For a selected track, it serves:

- `game` series
  - per-game when small
  - aggregated to at most 100 buckets when large
- `date` series
  - end-of-day ratings
  - aggregated when the day count is large

Frontend charts should treat those series as canonical and should not recompute from paginated history pages.

### Bots report payload

`/api/tech/bots-report` returns listed-bot daily stats using completed games grouped by local date.

Current grouped metrics:

- `overall`
- `vs_humans`
- `vs_bots`

Each group includes:

- total games count
- win rate

## Static-Site Content Shape

The `content` repo is not a code repo, but it still has structure that other repos depend on.

Important rules:

- blog entries are folder-based
  - `blog/<slug>/README.md`
- snippets/assets live next to the owning article
- changelog entries are dated markdown files
- rules pages are markdown files consumed by `ks-home`

`ks-home` is the renderer.
`content` is the source of truth.

## Practical Rules

- If a value can be recomputed once and normalized, prefer migration plus cleanup over permanent fallback logic.
- Public browser URLs should use `game_code`.
- Active hidden state must stay private.
- Completed review data can be richer, but that should remain an explicit completed-game capability.
