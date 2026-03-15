# Step 700 - Infra and Operations

## Goal

Finish the operational layer: Docker (with React build), NGINX, CI, backup, logging.

## Read First

- [INFRA.md](../../INFRA.md)
- [development-plan/PLAN.md](../PLAN.md)

## Depends On

- `step-600`

## Task Slices

### 710 — Finalize Docker for React + FastAPI

**Modify these files:**

- `src/app/Dockerfile` — finalize:
  - Non-root user
  - Health check instruction
  - Verify all app files copied correctly
- `frontend/Dockerfile` — NEW, multi-stage build:
  - Stage 1: `node:20-alpine`, install deps, `npm run build`
  - Stage 2: output `dist/` folder (used by NGINX)
- `docker-compose.yml` — finalize:
  - `app` service: FastAPI backend only (no frontend serving)
  - `frontend` service: build React, output to shared volume
  - `nginx` service: serves React dist at `/`, proxies `/api/` and `/auth/` to app
  - `mongo` service: with replica set
  - Dev profile: adds mongo-express
  - Production profile: adds certbot
  - Shared volume for frontend build output → NGINX

**Acceptance criteria:**
- `docker compose build` succeeds
- `docker compose up -d` starts all services healthy
- `http://localhost/` serves the React app via NGINX
- `http://localhost/api/game/open` proxies to FastAPI
- `docker compose --profile dev up` adds mongo-express

---

### 720 — NGINX Production Configuration

**Modify these files:**

- `src/nginx/nginx.conf` — finalize:
  - Rate limit zones: api (30r/s), auth (5r/m)
  - Gzip compression
  - Security headers (X-Frame-Options, X-Content-Type-Options)
- `src/nginx/conf.d/kriegspiel.conf` — production config:
  - HTTP → HTTPS redirect
  - TLS with Let's Encrypt cert paths
  - Serve React `dist/` at `/` with `try_files $uri /index.html` (SPA routing)
  - Proxy `/api/` and `/auth/` to app:8000
  - Static asset caching (30-day expiry for `/assets/`)
  - ACME challenge location
- `src/nginx/conf.d/kriegspiel-dev.conf` — HTTP-only dev config (no TLS)

**Acceptance criteria:**
- NGINX starts without config errors
- SPA routing works (direct URL access to `/lobby`, `/game/123` etc. serves React app)
- API proxying works
- Rate limiting on `/auth/login`
- Dev config works without TLS certs

---

### 730 — GitHub Actions CI

**Create this file:**

- `.github/workflows/ci.yml`:
  - Trigger: push to main, PRs to main
  - **Test job:**
    - MongoDB 7 service container
    - Python 3.12 setup
    - Install backend requirements
    - Lint: `black --check` + `ruff check`
    - Test: `pytest tests/ --cov=app -v`
  - **Frontend job:**
    - Node 20 setup
    - `npm ci` + `npm run lint` + `npm run build`
  - **Deploy job** (main push only, after both jobs pass):
    - SSH to VPS, pull, build, restart

**Acceptance criteria:**
- CI YAML is valid
- Backend lint + test steps defined
- Frontend lint + build steps defined
- Deploy conditional on main branch

---

### 740 — Backup and Health Scripts

**Create these files:**

- `scripts/backup.sh` — daily MongoDB backup: mongodump + gzip, retain 30 days
- `scripts/restore.sh` — restore from backup file (with confirmation prompt)
- `scripts/health-check.sh` — curl /health, check container status, check disk space

**Acceptance criteria:**
- Scripts are executable
- `backup.sh` produces a gzipped backup file
- `restore.sh` accepts a backup path
- `health-check.sh` reports service status
- Scripts have usage instructions in comments

---

### 750 — Structured Logging

**Modify these files:**

- `src/app/main.py` — configure structlog:
  - JSON in production, human-readable in development
  - Timestamp + level in each entry
- Add log calls to key operations:
  - `src/app/routers/auth.py` — log register, login, failed login (with IP)
  - `src/app/services/game_service.py` — log game create, join, resign, complete
  - Move endpoint — log moves (game_id + color, not the move itself)
- Verify logs don't include sensitive data (passwords, session IDs)

**Acceptance criteria:**
- App outputs structured JSON logs in production mode
- Key events logged with context (game_id, user_id)
- No sensitive data in logs
- `docker compose logs app` shows clean output

---

## Exit Criteria

- App runs via Docker Compose with React frontend served by NGINX
- CI lints and tests both backend and frontend
- Backup/restore scripts exist
- Structured logging works

## Out of Scope

- Final launch decision
- Phase 2 features
