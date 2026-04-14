# Runtime Flows

This document explains how the main Kriegspiel.org runtime paths work across the active repos.

## 1. Browser Auth Flow

Repos involved:

- `ks-web-app`
- `ks-backend`

Flow:

1. User opens `app.kriegspiel.org`.
2. Frontend uses same-origin relative `/api/...` requests.
3. Register/login hits backend auth routes.
4. Backend creates a session document and sets a cookie.
5. Later requests reuse the cookie; the browser app does not send a password again.
6. Backend resolves the current user through session lookup.

Important rule:

- browser code should use same-origin `/api/...`
- bots and external scripts should use `api.kriegspiel.org`

## 2. Game Creation and Join Flow

Repos involved:

- `ks-web-app`
- `ks-backend`
- `ks-game`

Flow:

1. User chooses rule set and opponent mode in the app.
2. Frontend calls `POST /api/game/create`.
3. Backend assigns:
   - `game_code`
   - `state`
   - player colors
   - initial engine state
4. If the game starts immediately, it becomes `active`.
5. If it waits for a joiner, it stays `waiting`.
6. A join operation uses `POST /api/game/join/{game_code}`.

Important rules:

- public joining is code-based
- browser URLs should remain code-based
- direct selected-bot games are created by the human, not by bots joining human waiting games
- waiting games expire after 10 minutes if nobody joins

## 3. Active Game Play Flow

Repos involved:

- `ks-web-app`
- `ks-backend`
- `ks-game`

Flow:

1. Frontend loads `GET /api/game/{game_code}` for metadata.
2. Frontend polls `GET /api/game/{game_code}/state`.
3. Backend resolves the active game from the in-memory cache when possible.
4. Backend projects the engine state into:
   - `your_fen`
   - allowed moves
   - player-visible referee log
   - player-visible scoresheet
5. Player submits:
   - `POST /move`
   - `POST /ask-any`
   - or `POST /resign`
6. Backend mutates the cached game first.
7. Backend schedules async persistence according to policy.

Persistence policy:

- human-involved games:
  - flush after every successful visible action
- bot-vs-bot games:
  - flush every 20 plies
  - flush on completion
  - flush after 30 seconds idle
- all cached games:
  - flush on graceful shutdown

## 4. Replay / Review Flow

Repos involved:

- `ks-web-app`
- `ks-backend`

Flow:

1. User opens `/game/{game_code}/review`.
2. Frontend requests the completed-game transcript.
3. Backend serves a completed-game replay payload with:
   - metadata
   - transcript attempts
   - replay board states for referee / white / black views
4. Frontend groups attempts into plies and rows:
   - one white ply box
   - one black ply box
5. Replay controls move by ply, not raw attempts.
6. Board overlays show:
   - legal completed move arrows
   - illegal attempt arrows and markers
   - capture highlighting

Important visibility rule:

- active games must not leak hidden opponent state
- completed review may expose full replay data by design

## 5. Profile, Leaderboard, and Rating History Flow

Repos involved:

- `ks-web-app`
- `ks-backend`

Flow:

1. Frontend loads the public profile payload.
2. Backend provides:
   - public user profile
   - exact lifetime result totals
   - exact lifetime rating tracks
3. Frontend separately loads rating-history series for the selected track.
4. Backend returns pre-aggregated chart series:
   - end-of-day ratings for date mode
   - per-game or aggregated buckets for game mode
5. Frontend renders tiles and plots without recomputing lifetime stats client-side.

Important rule:

- frontend should not derive lifetime totals from paginated history pages

## 6. Bot Runtime Flow

Repos involved:

- `bot-random`
- `bot-random-any`
- `bot-simple-heuristics`
- `bot-gpt-nano`
- `bot-haiku`
- `ks-backend`

Common flow:

1. Bot starts as a single Python process under systemd.
2. It restores saved token/state if present.
3. It polls `mine`, lobby/open games, and relevant game state endpoints.
4. It handles active games sequentially in one loop.
5. It may create or join games based on repo-specific policy.

Shared current join rule for main bots:

- sample bot-vs-bot joins at most once per minute

Differences:

- `randobot`
  - random move selection
  - auto-creates waiting games
  - allows up to 5 active games
  - bot-vs-bot join probability is 50%
- `randobotany`
  - asks `any pawn captures?` before random moves
  - auto-creates waiting games
  - allows up to 5 active games
  - bot-vs-bot join probability is 50%
- `simpleheuristics`
  - recaptures on the last capture square when possible
  - prefers queen promotion
  - otherwise picks `ask-any` or a piece using geometric weights, then tries that piece's moves from longest to shortest
  - auto-creates waiting games and allows up to 5 active games
  - bot-vs-bot join probability is 10%
- `gptnano`
  - OpenAI model loop
  - per-game conversation state
  - active-game cap is 1
  - no auto-created waiting games
  - bot-vs-bot join probability is 0.1%
  - provider preflight is checked only before joining a new bot-vs-bot game
- `haiku`
  - Anthropic model loop
  - per-game conversation state
  - active-game cap is 1
  - no auto-created waiting games
  - bot-vs-bot join probability is 0.1%
  - provider preflight is checked only before joining a new bot-vs-bot game

## 7. Bot Auth Flow

Repos involved:

- bots
- `ks-backend`

Flow:

1. Bot registers or restores its one-time API token.
2. Bot sends bearer auth on API requests.
3. Backend verifies token using:
   - token id lookup
   - HMAC digest comparison
4. Backend caches successful bot auth results in memory for 3600 seconds.

Important rule:

- human password hashing remains expensive and rare
- bot token auth is optimized for high-frequency request paths

## 8. Static Public Site Flow

Repos involved:

- `content`
- `ks-home`
- `ks-backend`

Flow:

1. `content` stores blog, changelog, rules, and snippet assets.
2. `ks-home` consumes `content` during its build.
3. A refresh script creates/updates detached worktrees in `.site-refresh`.
4. `ks-home` builds static output using:
   - `KS_CONTENT_PATH`
   - `KS_API_BASE`
5. Built files are synced into the live `ks-home/dist`.
6. `kriegspiel.org` serves that static output.

Important rules:

- content changes do not reach the public site until a `ks-home` refresh runs
- the static public leaderboard is human-only and overall-rating only

## 9. Timeout and Cleanup Flow

Repos involved:

- `ks-backend`

Flow:

1. Live requests can adjudicate timeout when they touch a game.
2. A background sweeper also scans active games.
3. The sweep runs:
   - immediately on backend startup
   - then every 25 minutes
4. Stale timed-out games are completed even if nobody reopens them manually.

## 10. Migration and Cleanup Flow

Repos involved:

- mostly `ks-backend`

Preferred pattern:

1. Identify legacy persisted shape.
2. Write a one-shot script or targeted recalculation.
3. Run the migration against live data.
4. Remove the compatibility branch.

Recent examples:

- root-level scoresheets migrated into `engine_state`
- archive rating snapshots recalculated globally
- legacy bot bcrypt auth removed after normalization
