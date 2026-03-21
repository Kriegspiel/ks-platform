# Step 110 Implementation Plan

## Implementation Sequence

Build this slice in the following order:

1. Create the package markers so imports resolve predictably.
2. Implement `Settings` and `get_settings()` in `src/app/config.py`.
3. Implement the lifespan function and `create_app()` in `src/app/main.py`.
4. Add the `/health` route.
5. Add automated tests before considering the slice complete.

Do not start MongoDB wiring in this slice. The lifespan hook is a placeholder for slice `120`, not a place to pre-implement database behavior.

## File-By-File Requirements

### `src/app/__init__.py`

- Create the file.
- Keep it empty.
- Do not add side effects, imports, or version constants here.

### `src/app/routers/__init__.py`

- Create the file.
- Keep it empty.

### `src/app/models/__init__.py`

- Create the file.
- Keep it empty.

### `src/app/services/__init__.py`

- Create the file.
- Keep it empty.

### `src/app/config.py`

This file should define the application settings contract for the backend.

Required contents:

- `Settings` class based on `pydantic_settings.BaseSettings`
- defaults for the following fields:
  - `SECRET_KEY: str = "dev-secret-change-me"`
  - `MONGO_URI: str = "mongodb://localhost:27017/kriegspiel?replicaSet=rs0"`
  - `ENVIRONMENT: str = "development"`
  - `LOG_LEVEL: str = "info"`
  - `SITE_ORIGIN: str = "http://localhost:5173"`
- `get_settings()` helper returning a cached `Settings` instance

Implementation requirements:

- Prefer `@lru_cache` on `get_settings()` so tests can override environment variables by clearing the cache.
- Configure `BaseSettings` to read from environment variables. Reading from `.env` is acceptable if it is done through normal `pydantic-settings` configuration rather than custom parsing.
- Keep the module dependency-light. Importing `config.py` must not import FastAPI or touch the filesystem beyond standard settings loading.

Behavior expectations:

- Instantiating `Settings()` with no environment overrides must yield the defaults above.
- Environment variable overrides must work without code changes.
- Test code must be able to create multiple `Settings(...)` instances directly without relying on global state.

### `src/app/main.py`

This file should be the first stable backend entrypoint.

Required contents:

- `asynccontextmanager` lifespan function
- `create_app(settings: Settings | None = None) -> FastAPI`
- module-level `app = create_app()`

App construction requirements:

- Set the FastAPI title to exactly `"Kriegspiel Chess API"`.
- If `settings` is `None`, call `get_settings()`.
- Store the resolved settings object on `app.state.settings`.
- Register `CORSMiddleware`.
- Register `GET /health`.

Lifespan requirements:

- The lifespan function must be present in this slice so slice `120` has a clean place to attach MongoDB startup/shutdown.
- In slice `110`, the lifespan body should do no external I/O.
- Startup and shutdown must succeed even when MongoDB is unavailable because MongoDB is not part of this slice yet.

CORS requirements:

- Always allow `settings.SITE_ORIGIN`.
- Set `allow_credentials=True`.
- Set `allow_headers=["*"]`.
- Allow at least `GET`, `POST`, `PATCH`, and `DELETE`.
- In `development`, also allow `http://localhost:8000` so local same-machine tooling remains compatible with the auth/infra guidance.
- Deduplicate origins before passing them to the middleware.

Health endpoint requirements:

- Route path must be `/health`.
- Method must be `GET`.
- Response body for slice `110` must be exactly `{"status": "ok"}`.
- Do not add database state to the response yet. That belongs to slice `120`.

App factory requirements:

- The app factory must be reusable in tests.
- The app factory must not mutate module-level globals other than the module-level `app` instance created at import time.
- The module must import cleanly with `python -c "from app.main import app"` once dependencies are installed.

## Suggested Function Shape

The code does not need to match this verbatim, but it should follow this shape closely enough to keep tests straightforward:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings, get_settings


def build_cors_origins(settings: Settings) -> list[str]:
    ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    resolved_settings = settings or get_settings()
    app = FastAPI(title="Kriegspiel Chess API", lifespan=lifespan)
    app.state.settings = resolved_settings
    app.add_middleware(...)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
```

## Guardrails

- Do not import Motor or database helpers in this slice.
- Do not create placeholder routers if they are not used yet.
- Do not add WebSocket code.
- Do not add production-only CORS origins hard-coded into the default settings. Production origin support should come from environment configuration.
- Do not let the `/health` contract drift toward slice `120` early.

## Exact Handoff Expectations For Slice 120

Slice `120` should be able to:

- reuse `Settings` without renaming fields,
- extend lifespan startup/shutdown without changing the app factory shape,
- attach database handles to `app.state`,
- upgrade `/health` from app-only readiness to app-plus-db readiness.
