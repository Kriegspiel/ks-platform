# Step 100 - Foundation and Scaffold

## Goal

Create the runnable project skeleton and developer workflow foundation for the MVP.

## Read First

- [README.md](../../README.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [INFRA.md](../../INFRA.md)

## Depends On

- None

## Task Slices

### 110 — Package Structure, Settings, App Factory, and Health Endpoint

**Create these files:**

- `src/app/__init__.py` — empty
- `src/app/main.py` — FastAPI app factory with lifespan context manager, CORS middleware setup, health endpoint
- `src/app/config.py` — `Settings` class using `pydantic-settings` with fields: `SECRET_KEY`, `MONGO_URI`, `ENVIRONMENT` (dev/production), `LOG_LEVEL`, `SITE_ORIGIN`
- `src/app/routers/__init__.py` — empty
- `src/app/models/__init__.py` — empty
- `src/app/services/__init__.py` — empty
- `src/app/ws/__init__.py` — empty

**Acceptance criteria:**
- `cd src && python -c "from app.main import app; print(app.title)"` prints the app name
- `Settings` loads from environment variables with sensible defaults for local dev
- `/health` returns `{"status": "ok"}` (db check comes in 100.2)
- CORS middleware configured per AUTH.md (allow localhost in dev mode)

---

### 120 — MongoDB Motor Wiring

**Modify/create these files:**

- `src/app/db.py` — async `get_db()` function, Motor client setup, `init_db()` to create indexes from DATA_MODEL.md, `close_db()` to shut down client
- `src/app/main.py` — wire `init_db()`/`close_db()` into the lifespan context manager
- Update `/health` to ping MongoDB and return `{"status": "ok", "db": "connected"}` or 503

**Acceptance criteria:**
- App starts successfully when MongoDB is running locally
- `/health` returns 200 with `db: connected` when Mongo is up
- `/health` returns 503 when Mongo is unreachable
- Index creation runs on startup (users, games, sessions, game_archives, audit_log collections)

---

### 130 — Dev Environment Files

**Create these files:**

- `.env.example` — all env vars from INFRA.md with comments
- `src/app/requirements.txt` — exact deps from INFRA.md
- `src/app/requirements-dev.txt` — dev deps from INFRA.md (extends requirements.txt)
- `src/app/Dockerfile` — from INFRA.md spec
- `docker-compose.yml` — from INFRA.md spec (app, mongo, mongo-express, certbot, nginx services)
- `src/nginx/nginx.conf` — base nginx config with rate limit zones in http block
- `src/nginx/conf.d/kriegspiel.conf` — upstream + server blocks from INFRA.md (use HTTP-only for local dev, TLS for prod)
- `src/mongo/init-replica.sh` — single-node replica set init from INFRA.md

**Acceptance criteria:**
- `docker compose config` parses without errors
- `docker compose --profile dev up --build` starts all services (app, mongo, mongo-express, nginx)
- App is reachable at `http://localhost:8000/health` (direct) and `http://localhost/health` (via nginx)

---

### 140 — Test Harness and Smoke Tests

**Create these files:**

- `src/tests/__init__.py` — empty
- `src/tests/conftest.py` — shared pytest fixtures: async test client (httpx `AsyncClient`), test MongoDB connection (use `kriegspiel_test` database), app fixture with test settings, db cleanup fixture
- `src/tests/test_health.py` — test `/health` returns 200 and correct shape, test `/health` returns 503 when db is down (mock or skip)
- `pyproject.toml` or `src/pyproject.toml` — pytest config (asyncio_mode=auto), black config (line-length=128), ruff config

**Acceptance criteria:**
- `cd src && pytest tests/ -v` runs and passes
- Test fixtures create/use a separate test database
- Linting passes: `black --check --line-length 128 src/app src/tests` and `ruff check src/app src/tests`

---

## Required Tests Before Done

- `pytest tests/test_health.py` passes
- App starts locally via `uvicorn app.main:app`
- Health endpoint responds at `/health`
- Docker Compose parses cleanly (`docker compose config`)
- Lint passes

## Exit Criteria

- The project layout matches the `src/` structure from ARCHITECTURE.md
- `cd src && uvicorn app.main:app` starts successfully
- The health endpoint works and checks MongoDB
- Mongo wiring is present and testable
- Smoke tests exist and pass

## Out of Scope

- Registration/login behavior
- Game creation/join logic
- WebSocket gameplay
