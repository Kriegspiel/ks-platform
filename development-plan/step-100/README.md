# Step 100 - Foundation and Scaffold

## Goal

Create the runnable backend + frontend skeleton with MongoDB wiring, Docker setup, and test harness.

## Read First

- [ARCHITECTURE.md](../../ARCHITECTURE.md) — system overview (note: frontend is React, not Jinja2)
- [INFRA.md](../../INFRA.md) — Docker, NGINX, requirements
- [development-plan/PLAN.md](../PLAN.md) — architecture decisions override specs

## Depends On

- None

## Task Slices

### 110 — Backend: App Factory, Settings, Health Endpoint

Detailed execution packet: [development-plan/step-110](../step-110/README.md)

**Create these files:**

- `src/app/__init__.py` — empty
- `src/app/main.py` — FastAPI app with:
  - App title "Kriegspiel Chess API"
  - CORS middleware (allow `http://localhost:5173` for Vite dev, credentials=True)
  - `/health` endpoint returning `{"status": "ok"}`
  - Lifespan context manager (startup/shutdown hooks, wired in 120)
- `src/app/config.py` — `Settings` class using `pydantic-settings`:
  - `SECRET_KEY: str` (default: "dev-secret-change-me")
  - `MONGO_URI: str` (default: "mongodb://localhost:27017/kriegspiel?replicaSet=rs0")
  - `ENVIRONMENT: str` (default: "development")
  - `LOG_LEVEL: str` (default: "info")
  - `SITE_ORIGIN: str` (default: "http://localhost:5173")
- `src/app/routers/__init__.py` — empty
- `src/app/models/__init__.py` — empty
- `src/app/services/__init__.py` — empty

**Acceptance criteria:**
- `cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py -v` passes
- Automated tests confirm `from app.main import app` builds an app titled "Kriegspiel Chess API"
- Automated tests confirm `/health` returns exactly `{"status": "ok"}`
- Automated tests confirm CORS allows requests from localhost:5173 with credentials enabled

Manual `uvicorn` and `curl` smoke checks are optional for debugging, but this slice is not complete without the automated checks defined in [development-plan/step-110/TESTING.md](../step-110/TESTING.md).

---

### 120 — MongoDB Motor Wiring

Detailed execution packet: [development-plan/step-120](../step-120/README.md)

**Create/modify these files:**

- `src/app/db.py`:
  - `init_db(settings)` — create Motor async client, connect to database, create indexes from DATA_MODEL.md (users, games, sessions, game_archives, audit_log)
  - `close_db()` — close Motor client
  - `get_db()` — return the database handle
- `src/app/main.py` — wire `init_db()`/`close_db()` into lifespan context manager, store db on `app.state.db`
- Update `/health` to ping MongoDB: return `{"status": "ok", "db": "connected"}` or 503 with `{"status": "error", "db": "disconnected"}`

**Acceptance criteria:**
- `cd src && pytest tests/test_db.py tests/test_health.py -v` passes
- Automated tests confirm `/health` returns 200 with `{"status": "ok", "db": "connected"}` when Mongo is reachable
- Automated tests confirm `/health` returns 503 with `{"status": "error", "db": "disconnected"}` when Mongo is unavailable
- Automated tests confirm the required MongoDB indexes are created

Manual testing against a developer-started MongoDB instance is optional for debugging, but this slice is not complete without the automated checks defined in [development-plan/step-120/TESTING.md](../step-120/TESTING.md).

---

### 130 — React Frontend Scaffold

Detailed execution packet: [development-plan/step-130](../step-130/README.md)

**Create these files:**

- `frontend/package.json` — dependencies: react, react-dom, react-router-dom, axios. Dev deps: vite, @vitejs/plugin-react, eslint, eslint-plugin-react-hooks
- `frontend/vite.config.js` — React plugin, proxy `/api` and `/auth` to `http://localhost:8000` for dev
- `frontend/index.html` — root HTML with `<div id="root">`
- `frontend/src/main.jsx` — render `<App />` into `#root`
- `frontend/src/App.jsx` — React Router with placeholder routes: `/`, `/auth/login`, `/auth/register`, `/lobby`, `/game/:gameId`
- `frontend/src/App.css` — minimal base styles
- `frontend/src/index.css` — reset/base styles
- `frontend/src/services/api.js` — axios instance with `baseURL` (empty string — Vite proxy handles it), `withCredentials: true`
- `frontend/.gitignore` — node_modules, dist

**Acceptance criteria:**
- `cd frontend && npm install` succeeds
- `cd frontend && npm run test -- --run` passes
- `cd frontend && npm run lint` passes
- `cd frontend && npm run build` produces a `dist/` folder
- Automated tests confirm the placeholder routes render and the Axios client uses the dev proxy strategy

Manual browser checks are optional for debugging, but this slice is not complete without the automated checks defined in [development-plan/step-130/TESTING.md](../step-130/TESTING.md).

---

### 140 — Dev Environment Files

Detailed execution packet: [development-plan/step-140](../step-140/README.md)

**Create these files:**

- `.env.example` — all env vars with comments (SECRET_KEY, MONGO_URI, ENVIRONMENT, LOG_LEVEL, SITE_ORIGIN, ME_USERNAME, ME_PASSWORD)
- `src/app/requirements.txt` — from INFRA.md: fastapi, uvicorn[standard], motor, pydantic, pydantic-settings, bcrypt, python-jose[cryptography], kriegspiel>=1.1.2, structlog, python-multipart, httpx
- `src/app/requirements-dev.txt` — extends requirements.txt: pytest, pytest-asyncio, pytest-cov, black, ruff
- `src/app/Dockerfile` — Python 3.12-slim, install requirements, copy app code, expose 8000, CMD uvicorn
- `docker-compose.yml` — services: app (build from src), mongo (mongo:7 with replica set), nginx, mongo-express (dev profile), certbot (production profile)
- `src/nginx/nginx.conf` — http block with rate limit zones
- `src/nginx/conf.d/kriegspiel-dev.conf` — HTTP-only dev config: proxy `/api/` and `/auth/` to app:8000, serve frontend dist at `/`
- `src/mongo/init-replica.sh` — single-node replica set init

**Acceptance criteria:**
- `docker compose config` parses without errors
- `docker build -f src/app/Dockerfile src` passes
- Automated NGINX syntax validation passes
- Automated replica-init script validation passes
- `docker compose --profile dev up -d --build` starts the dev stack and automated health probing succeeds

Manual stack inspection is optional for debugging, but this slice is not complete without the automated checks defined in [development-plan/step-140/TESTING.md](../step-140/TESTING.md).

---

### 150 — Test Harness and Smoke Tests

Detailed execution packet: [development-plan/step-150](../step-150/README.md)

**Create these files:**

- `src/tests/__init__.py` — empty
- `src/tests/conftest.py` — shared pytest fixtures:
  - `test_settings` — Settings with test database name (`kriegspiel_test`)
  - `test_app` — FastAPI app with test settings
  - `test_client` — httpx `AsyncClient` bound to test app
  - `db_cleanup` — drop test database after each test
- `src/tests/test_health.py`:
  - Test `/health` returns 200 with correct shape
  - Test health check response includes db status
- `pyproject.toml` — pytest config (asyncio_mode=auto), black config (line-length=128), ruff config

**Acceptance criteria:**
- `cd src && pytest tests/ -v` runs and passes
- `cd src && pytest tests --cov=app --cov-report=xml -v` runs and passes
- Test fixtures use separate test database
- `cd src && black --check app tests` passes
- `cd src && ruff check app tests` passes

This slice is not complete without the automated checks defined in [development-plan/step-150/TESTING.md](../step-150/TESTING.md).

---

## Exit Criteria

- Backend starts with `uvicorn app.main:app` and serves `/health`
- Frontend starts with `npm run dev` and renders placeholder pages
- MongoDB wiring works (indexes created, health check pings)
- Docker Compose starts all services
- Smoke tests pass

## Out of Scope

- Registration/login
- Game logic
- Styled UI
