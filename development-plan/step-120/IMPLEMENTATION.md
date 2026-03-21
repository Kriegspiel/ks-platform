# Step 120 Implementation Plan

## Implementation Sequence

Build this slice in the following order:

1. Create `src/app/db.py`.
2. Define the module-level database lifecycle helpers.
3. Wire the lifecycle into the existing app lifespan from slice `110`.
4. Upgrade the `/health` endpoint to check database connectivity.
5. Add unit tests.
6. Add integration coverage against a disposable MongoDB replica set.

## File-By-File Requirements

### `src/app/db.py`

This file becomes the shared database lifecycle module for the backend.

Required contents:

- `init_db(settings)`
- `get_db()`
- `close_db()`

Recommended module-level state:

- `_client`
- `_db`

Implementation requirements:

- Use `motor.motor_asyncio.AsyncIOMotorClient`.
- Build the client from `settings.MONGO_URI`.
- Set a finite `serverSelectionTimeoutMS` so health failures surface quickly in tests.
- Resolve the database handle from the URI's default database name. Do not hard-code the database name separately if the URI already contains it.
- Ping MongoDB during initialization when possible.
- Create the required indexes after a successful connection.
- Make `close_db()` safe to call multiple times.
- Make `get_db()` raise a clear runtime error if the database has not been initialized.

### Required Index Set

The implementation must create these exact index families from [DATA_MODEL.md](../../DATA_MODEL.md):

- `users`
  - unique `username`
  - unique sparse `email`
  - descending `stats.elo`
  - compound `status`, `last_active_at`
- `games`
  - unique `game_code`
  - compound `state`, `created_at`
  - compound `white.user_id`, `state`
  - compound `black.user_id`, `state`
  - TTL `expires_at` with `expireAfterSeconds=0`
- `game_archives`
  - compound `white.user_id`, `created_at`
  - compound `black.user_id`, `created_at`
  - compound `result.winner`, `created_at`
  - descending `created_at`
- `audit_log`
  - TTL `timestamp` with `expireAfterSeconds=7776000`
  - compound `user_id`, `timestamp`
  - `game_id`
- `sessions`
  - TTL `expires_at` with `expireAfterSeconds=0`
  - `user_id`

Create indexes idempotently using normal MongoDB index creation APIs so repeated app startups do not fail.

### `src/app/main.py`

This slice extends the app factory created in slice `110`.

Required changes:

- During startup, call `init_db(settings)`.
- Store the client and database on `app.state`.
- During shutdown, call `close_db()`.
- Keep the app factory shape from slice `110`. Do not revert to import-time database initialization.
- Upgrade `GET /health` to check MongoDB availability.

Health implementation requirements:

- If a database handle exists and ping succeeds, return HTTP `200` with `{"status": "ok", "db": "connected"}`.
- If ping fails or the database is not ready, return HTTP `503` with `{"status": "error", "db": "disconnected"}`.
- The endpoint should never leak raw exception text.

Startup error-handling requirements:

- Do not let import-time app creation fail because MongoDB is unavailable.
- Lifespan startup may mark the app unhealthy if MongoDB initialization fails, but the app process should remain bootable so `/health` can report the failure.
- Record enough state on `app.state` for `/health` to distinguish connected from disconnected.

## Suggested Shape

The code does not need to match this verbatim, but it should preserve this separation of concerns:

```python
async def init_db(settings: Settings) -> AsyncIOMotorDatabase:
    ...


def get_db() -> AsyncIOMotorDatabase:
    ...


async def close_db() -> None:
    ...
```

And in `main.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db = await init_db(app.state.settings)
        app.state.db = db
        app.state.db_ready = True
    except Exception:
        app.state.db = None
        app.state.db_ready = False
    try:
        yield
    finally:
        await close_db()
```

## Guardrails

- Do not move MongoDB initialization to module import time.
- Do not start implementing auth/session queries here.
- Do not silently skip index creation.
- Do not make `/health` depend on any collection-specific query.
- Do not require a human to start MongoDB before the automated test suite can run.

## Exact Handoff Expectations For Slice 150

Slice `150` should be able to:

- reuse the database lifecycle helpers directly in fixtures,
- build a `test_app` fixture that points at a separate test database,
- drop the test database between test cases without changing the app factory shape.
