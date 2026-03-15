# Step 700 - Infra and Operations

## Goal

Finish the operational layer: containers, proxying, CI, deployment, backup, logging, and runtime readiness.

## Read First

- [INFRA.md](../../INFRA.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)

## Depends On

- `step-600`

## Task Slices

### 710 — Finalize Docker and Compose for Production

**Modify these files:**

- `src/app/Dockerfile` — review and finalize:
  - Multi-stage build if needed (separate build/runtime stages)
  - Non-root user for security
  - Health check instruction
  - Verify all app files are copied correctly
  - Ensure static files are accessible via the shared volume
- `docker-compose.yml` — review and finalize:
  - Production profile: app + mongo + nginx + certbot (no mongo-express)
  - Dev profile: adds mongo-express
  - Volume mounts for static files, TLS certs, mongo data
  - Resource limits (memory, CPU) if appropriate
  - Restart policies
  - Network configuration
- Test: `docker compose build` succeeds, `docker compose up` starts all services, app is healthy

**Acceptance criteria:**
- `docker compose build` succeeds with no warnings
- `docker compose up -d` starts app, mongo, nginx
- `docker compose ps` shows all services healthy
- App serves pages through nginx at port 80
- `docker compose --profile dev up` additionally starts mongo-express

---

### 720 — NGINX Production Configuration

**Modify these files:**

- `src/nginx/nginx.conf` — finalize:
  - Rate limit zones: `api` (30r/s), `auth` (5r/m), `register` (3r/m), `ws_conn` (5 connections per IP)
  - Gzip compression for text/html, text/css, application/json, application/javascript
  - Security headers: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
  - Worker processes and connections tuning
- `src/nginx/conf.d/kriegspiel.conf` — finalize:
  - HTTP→HTTPS redirect (port 80)
  - TLS configuration with Let's Encrypt cert paths
  - Static file serving with caching headers (30-day expiry, immutable)
  - Proxy pass for `/api/`, `/auth/`, `/ws/`, `/` to app
  - WebSocket proxy with upgrade headers and 1-hour timeouts
  - Rate limiting references on auth and API locations
  - ACME challenge location for certbot
- Create `src/nginx/conf.d/kriegspiel-dev.conf` — HTTP-only config for local development (no TLS)

**Acceptance criteria:**
- NGINX starts without config errors
- Static files are served directly by NGINX with cache headers
- WebSocket connections work through NGINX (1-hour timeout)
- Rate limiting works on `/auth/login` (test with curl)
- Dev config works without TLS certificates

---

### 730 — GitHub Actions CI Workflow

**Create this file:**

- `.github/workflows/ci.yml` — as specified in INFRA.md:
  - Trigger: push to main, pull requests to main
  - Test job:
    - MongoDB 7 service container
    - Python 3.12 setup
    - Install requirements + dev requirements
    - Lint: `black --check` + `ruff check`
    - Test: `pytest tests/ --cov=app --cov-report=xml -v`
    - Upload coverage to Codecov
  - Deploy job (only on main push, after tests pass):
    - SSH to VPS, git pull, docker compose build, docker compose up
    - Uses GitHub secrets: `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`

**Acceptance criteria:**
- CI workflow YAML is valid (test with `act` or push to a branch)
- Lint step would catch formatting issues
- Test step runs with MongoDB service
- Deploy step is conditional on main branch push

---

### 740 — Backup, Restore, and Health Scripts

**Create these files:**

- `scripts/backup.sh` — daily MongoDB backup script from INFRA.md:
  - `mongodump` with gzip to backup directory
  - Retain last 30 days of backups
  - Log backup success/failure
  - Designed to run via cron (`0 3 * * *`)
- `scripts/restore.sh` — restore from a backup:
  - Takes backup file path as argument
  - `mongorestore` from gzip archive
  - Confirmation prompt before overwriting
- `scripts/health-check.sh` — quick health verification:
  - Curl `/health` endpoint
  - Check Docker container status
  - Check MongoDB replica set status
  - Check disk space
  - Output summary
- Add cron setup instructions to script comments

**Acceptance criteria:**
- `backup.sh` runs without errors when MongoDB is available
- `restore.sh` accepts a backup file and can restore it
- `health-check.sh` reports status of all services
- Scripts are executable (`chmod +x`)
- Scripts have usage instructions in comments

---

### 750 — Structured Logging and Health Finalization

**Modify these files:**

- `src/app/config.py` — add `LOG_LEVEL` and `LOG_FORMAT` settings
- `src/app/main.py` — configure structlog as specified in INFRA.md:
  - JSON output in production
  - Human-readable output in development
  - Timestamp, log level, logger name in each entry
- Add structured log calls to key operations:
  - `src/app/routers/auth.py` — log register, login, logout, failed login attempts (with IP)
  - `src/app/services/game_service.py` — log game create, join, resign, complete, abandon
  - `src/app/ws/game_handler.py` — log WebSocket connect, disconnect, moves (game_id + color, not the move itself for security)
- Verify `/health` endpoint works correctly under Docker with MongoDB health check

**Acceptance criteria:**
- App outputs structured JSON logs in production mode
- Key events are logged with relevant context (game_id, user_id, IP for auth)
- Logs do NOT include sensitive data (passwords, session tokens)
- Health endpoint returns correct status under Docker
- `docker compose logs app` shows clean structured output

---

## Required Tests Before Done

- `docker compose` boot test — all services start and are healthy
- CI workflow dry run or equivalent local reproduction
- Backup script dry run
- Health endpoint and logging checks under containerized startup

## Exit Criteria

- The app runs correctly via Docker Compose
- CI can lint and test the repo
- Backup and health mechanisms exist and are documented
- The deployment path is documented well enough to execute without guesswork

## Out of Scope

- Final production launch decision
- Community/Phase 2 features
