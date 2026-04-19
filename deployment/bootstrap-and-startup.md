# Bootstrap and Startup

This document is the operational starting point for bringing the Kriegspiel.org stack up on a machine or understanding how the live host runs it today.

If you are starting from a blank machine, read [`new-server-bootstrap.md`](./new-server-bootstrap.md) first.
That document is the clean step-by-step entrypoint. This one is the lower-level runtime and process reference.

It is intentionally concrete:

- what repos must exist
- what runtime prerequisites are expected
- which env files matter
- which commands or systemd units actually start the services
- what order to bring things up in

## Required repos

The active stack expects these repos under the same workspace root:

- `.../kriegspiel/ks-backend`
- `.../kriegspiel/ks-web-app`
- `.../kriegspiel/ks-home`
- `.../kriegspiel/content`
- `.../kriegspiel/ks-game`

Optional bot repos:

- `.../kriegspiel/bot-random`
- `.../kriegspiel/bot-random-any`
- `.../kriegspiel/bot-simple-heuristics`
- `.../kriegspiel/bot-gpt-nano`
- `.../kriegspiel/bot-haiku`

## One-repo bootstrap

If you are starting from a fresh machine, `ks-platform` can be the only repo you clone manually.

Example:

```bash
git clone git@github.com:Kriegspiel/ks-platform.git
cd ks-platform
python3 scripts/bootstrap_workspace.py --include-bots
```

What that does:

- treats the parent of the current `ks-platform` checkout as the workspace root
- clones the required sibling repos there
- optionally clones the bot repos
- ensures the shared workspace helper directories exist:
  - `_wroktrees`
  - `_tmp`
  - `.site-refresh`

If you do not need the bots on the new machine, omit `--include-bots`.

Useful options:

- `--workspace-root /path/to/kriegspiel`
  - clones the sibling repos into an explicit workspace root
- `--update-existing`
  - fetches already-cloned repos instead of leaving them untouched
- `--https`
  - clones over HTTPS instead of SSH

## Runtime prerequisites

### Backend

- Python `3.12+`
- MongoDB reachable through `MONGO_URI`
- `ks-backend/.venv` with backend requirements installed

### Authenticated frontend

- Node `>= 20.19.0`
- `ks-web-app/frontend/node_modules` installed

### Static public site

- Node available for `ks-home`
- `ks-home/node_modules` installed
- sibling `content` repo available for builds or refreshes

## Ports and processes

Live host ports:

- backend: `127.0.0.1:8000`
- web app frontend preview: `127.0.0.1:4173`
- public static site server: `127.0.0.1:4180`

Public routing then fronts those processes as:

- `api.kriegspiel.org` -> backend
- `app.kriegspiel.org` -> frontend preview + same-origin `/api`
- `kriegspiel.org` -> static public site

## Environment files and settings

### `ks-backend`

Config source:

- local development: `.../kriegspiel/ks-backend/.env`
- live service: `/etc/default/ks-backend`

Important settings:

- `SECRET_KEY`
- `BOT_TOKEN_HMAC_SECRET`
- `MONGO_URI`
- `SITE_ORIGIN`
- `BOT_REGISTRATION_KEY`
- `LOG_LEVEL`

The backend settings model lives in `.../kriegspiel/ks-backend/src/app/config.py`.

### `ks-web-app`

The frontend repo has:

- `.../kriegspiel/ks-web-app/.env`
- `.../kriegspiel/ks-web-app/.env.example`

The live frontend process itself is just Vite preview serving built assets from `frontend/dist/`.
It does not call a separate configured API base in production; browser code uses same-origin `/api/...`.

### `ks-home`

The live static-site server does not need a dedicated `.env` file for normal serving.
The build/refresh flow depends on environment variables at execution time:

- `KS_CONTENT_PATH`
- `KS_API_BASE`
- optionally `ROOT`, `WORK_ROOT`, `HOME_BRANCH`, `CONTENT_BRANCH`

### Bots

Each bot repo normally uses:

- a local `.env`
- a persisted `.bot-state.json`

Those repos are independent from the main website startup path.

## Local bring-up order

For a local full-stack session, bring things up in this order.

### 1. Start the backend

```bash
cd .../kriegspiel/ks-backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r src/app/requirements-dev.txt
uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Expected health check:

```bash
curl http://127.0.0.1:8000/health
```

### 2. Start the authenticated frontend

```bash
cd .../kriegspiel/ks-web-app/frontend
npm ci
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

- `http://127.0.0.1:5173`

### 3. Build and serve the public static site

```bash
cd .../kriegspiel/ks-home
npm ci
KS_CONTENT_PATH=.../kriegspiel/content KS_API_BASE=http://127.0.0.1:8000 npm run build
HOST=127.0.0.1 PORT=4180 npm run serve:prod
```

Open:

- `http://127.0.0.1:4180`

### 4. Optional: run a bot

Each bot README contains its own setup flow. Typical pattern:

```bash
cd .../kriegspiel/bot-random
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python bot.py --register
python bot.py
```

## Live production startup model

### Backend

Systemd unit:

- `ks-backend.service`

Current live command:

```bash
.../kriegspiel/ks-backend/.venv/bin/uvicorn app.main:app --app-dir src --host 127.0.0.1 --port 8000
```

### Web app frontend

Systemd unit:

- `ks-web-app-frontend.service`

Current live command:

```bash
.../.nvm/versions/node/v20.19.0/bin/node .../kriegspiel/ks-web-app/frontend/node_modules/vite/bin/vite.js preview --host 127.0.0.1 --port 4173 --strictPort
```

Important operational note:

- this service depends on `.../kriegspiel/ks-web-app/frontend/node_modules/` existing on disk
- `dist/` alone is not enough because the service runs Vite preview from `node_modules`

### Public static site

Systemd unit:

- `ks-home.service`

Current live behavior:

- `ExecStartPre=/usr/bin/npm run build`
- `ExecStart=/usr/bin/npm run serve:prod`

Refresh automation:

- `ks-home-refresh.service`
- `ks-home-refresh.timer`

Refresh script:

- `.../kriegspiel/ks-home/scripts/refresh-static-site.sh`

## Operational startup checks

After bringing the stack up, verify:

### Backend

```bash
curl http://127.0.0.1:8000/health
```

### Frontend preview

```bash
curl -I http://127.0.0.1:4173/
```

### Static public site

```bash
curl -I http://127.0.0.1:4180/
```

### Browser/API wiring

Check:

- app pages load
- `/api/auth/session` responds through the app origin
- public site renders current content

## Common failure modes

### Frontend service loops with `MODULE_NOT_FOUND`

Likely cause:

- `.../kriegspiel/ks-web-app/frontend/node_modules` is missing

Why:

- the live service starts Vite preview from `node_modules/vite/bin/vite.js`

### Content edits do not appear on `kriegspiel.org`

Likely cause:

- `content` changed, but `ks-home` was not refreshed

### Backend is up but app auth fails

Likely cause:

- `SITE_ORIGIN` or session secret mismatch
- wrong same-origin assumption in the environment

### Bot behavior differs from docs

Likely cause:

- repo defaults changed and `ks-platform` was not updated
- a live `.env` override differs from source defaults
