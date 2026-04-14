# ks-backend

`ks-backend` is the main application server for Kriegspiel.org.

It owns:

- browser and bot auth
- game creation/join/play/resign
- hidden-state projection
- review transcript generation
- ratings and result stats
- leaderboard/profile APIs
- technical reports such as the bots report

## Runtime role

- public API host: `api.kriegspiel.org`
- same-origin API behind: `app.kriegspiel.org/api`
- framework: FastAPI
- database: MongoDB via Motor

## Startup notes

Local development:

```bash
cd .../kriegspiel/ks-backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r src/app/requirements-dev.txt
uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Live service:

- `ks-backend.service`
- environment file: `/etc/default/ks-backend`

## Main module layout

### `src/app/main.py`

Application bootstrap.

Responsibilities:

- create FastAPI app
- configure CORS
- initialize DB
- create/start `GameService`
- expose `/health`

### `src/app/config.py`

Settings model.

Important settings:

- `APP_VERSION`
- `SECRET_KEY`
- `BOT_TOKEN_HMAC_SECRET`
- `BOT_TOKEN_CACHE_TTL_SECONDS`
- `MONGO_URI`
- `SITE_ORIGIN`
- `BOT_REGISTRATION_KEY`

### `src/app/db.py`

Database bootstrap and index management.

Functions:

- initialize Mongo
- resolve DB name
- ensure indexes
- close DB on shutdown

### `src/app/dependencies.py`

Request-level dependency helpers.

Responsibilities:

- require DB
- get session service
- resolve current user from cookie or bot bearer token

### `src/app/models/`

Pydantic data contracts.

Important files:

- `auth.py`
- `bot.py`
- `game.py`
- `user.py`

### `src/app/routers/`

HTTP route surfaces.

- `auth.py`
- `bot.py`
- `game.py`
- `user.py`

### `src/app/services/`

Business logic layer.

Most important service modules:

- `game_service.py`
- `user_service.py`
- `session_service.py`
- `bot_service.py`
- `engine_adapter.py`
- `state_projection.py`
- `clock_service.py`
- `code_generator.py`

## Important classes and structures

### `GameService`

Core orchestrator.

Responsibilities:

- create/join/delete/resign games
- maintain active-game cache
- flush dirty cached games asynchronously
- run timeout sweeper
- produce review transcripts and metadata
- update ratings/results on completion

Related classes:

- `CachedGameEntry`
- `GameServiceError`
- `GameNotFoundError`
- `GameConflictError`
- `GameForbiddenError`
- `GameValidationError`

### `UserService`

Owns:

- create/authenticate users
- create/authenticate bots
- public profile assembly
- history and rating-history
- leaderboard
- bots report
- summary stat normalization/backfill

### `SessionService`

Owns:

- session creation
- lookup
- expiry extension
- session deletion

### `BotService`

Owns:

- public bot listing
- listed/unlisted filtering

### `engine_adapter.py`

Adapter between backend persistence and `ks-game`.

Responsibilities:

- create new engine instances
- serialize/deserialize engine state
- attempt moves
- ask-any
- serialize/deserialize scoresheets and answers

### `state_projection.py`

Builds player-visible views from engine state.

Responsibilities:

- player FEN projection
- allowed moves
- referee log
- referee turns
- viewer scoresheet
- rebuild scoresheet projections from stored moves when needed

## API contracts worth knowing

### Auth

- `POST /api/auth/register`
- `POST /api/auth/bots/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/auth/session`

### Games

- `POST /api/game/create`
- `POST /api/game/join/{game_code}`
- `GET /api/game/open`
- `GET /api/game/stats`
- `GET /api/game/mine`
- `GET /api/game/{game_code}`
- `GET /api/game/{game_code}/state`
- `GET /api/game/{game_code}/moves`
- `POST /api/game/{game_code}/move`
- `POST /api/game/{game_code}/ask-any`
- `POST /api/game/{game_code}/resign`
- `DELETE /api/game/{game_code}`

### Users and reports

- `GET /api/user/{username}`
- `GET /api/user/{username}/games`
- `GET /api/user/{username}/rating-history`
- `PATCH /api/user/settings`
- `GET /api/leaderboard`
- `GET /api/tech/bots-report`
- `GET /api/bots`

## Operational rules already encoded here

- public browser URLs use `game_code`
- active games do not expose hidden opponent state
- completed review may expose full replay
- bot auth uses HMAC digests plus a 3600-second cache
- backend owns lifetime stat totals and chart aggregation
- legacy compatibility paths should be removed after migration where possible

## Migration / maintenance scripts

Important scripts:

- `scripts/recalculate_archive_ratings.py`
- `scripts/migrate_scoresheets_to_engine_state.py`
- `scripts/impute_missing_bot_owner_emails.py`
- `scripts/retire_legacy_bcrypt_bots.py`

These scripts embody the preferred cleanup pattern:

- normalize once
- remove the fallback

## Test coverage

`src/tests/` is broad and important.

Useful anchors:

- auth/session/security tests
- game service and router tests
- game state polling tests
- gameplay integration tests
- timeout tests
- user service and route tests

For file-level coverage, use [`../module-index.md`](../module-index.md).
