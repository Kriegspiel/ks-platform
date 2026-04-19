# New Server Bootstrap

This is the fastest path from a blank machine to a working Kriegspiel workspace.

Use it when you want to:

- clone one repo first
- materialize the rest of the workspace beside it
- install the minimum runtime dependencies
- create the needed env files and secrets
- start the stack locally on the new machine
- know what still needs host-level setup before public cutover

If you already have the workspace and only need startup details, use [`bootstrap-and-startup.md`](./bootstrap-and-startup.md).

## Default assumptions

This guide assumes:

- Linux with `systemd`
- one checkout owner user
- workspace root: `~/dev/kriegspiel`
- services bind to localhost and are fronted separately if exposed publicly
- GitHub access is available through SSH keys or HTTPS credentials

Recommended path layout:

- `~/dev/kriegspiel/ks-platform`
- `~/dev/kriegspiel/ks-backend`
- `~/dev/kriegspiel/ks-web-app`
- `~/dev/kriegspiel/ks-home`
- `~/dev/kriegspiel/content`
- `~/dev/kriegspiel/ks-game`
- optional bot repos beside them

The bootstrap script also ensures these shared directories exist:

- `~/dev/kriegspiel/_wroktrees`
- `~/dev/kriegspiel/_tmp`
- `~/dev/kriegspiel/.site-refresh`

## 1. Install machine prerequisites

Install the OS-level tools first.

Minimum baseline:

- `git`
- `curl`
- `rsync`
- `build-essential`
- Python `3.12+` with `venv`
- Node `20.19.0` or newer
- MongoDB, or network access to the MongoDB instance the backend will use

Typical Debian or Ubuntu example:

```bash
sudo apt-get update
sudo apt-get install -y git curl rsync build-essential python3.12 python3.12-venv
```

For Node, prefer `nvm` and standardize on the frontend-pinned version:

```bash
export NVM_DIR="$HOME/.nvm"
. "$NVM_DIR/nvm.sh"
nvm install 20.19.0
nvm alias default 20.19.0
nvm use 20.19.0
```

Before going further, confirm:

```bash
python3.12 --version
node --version
npm --version
git --version
rsync --version
```

## 2. Clone `ks-platform` first and bootstrap the workspace

Create the workspace root, clone `ks-platform`, then let it fetch the sibling repos.

```bash
mkdir -p ~/dev/kriegspiel
cd ~/dev/kriegspiel
git clone git@github.com:Kriegspiel/ks-platform.git
cd ks-platform
python3 scripts/bootstrap_workspace.py --include-bots
```

If the machine should host only the main application repos, omit `--include-bots`.

Useful variants:

- `python3 scripts/bootstrap_workspace.py --update-existing`
- `python3 scripts/bootstrap_workspace.py --workspace-root /srv/kriegspiel`
- `python3 scripts/bootstrap_workspace.py --https`

After the script finishes, read:

1. [`../AGENTS.md`](../AGENTS.md)
2. [`./new-server-bootstrap.md`](./new-server-bootstrap.md)
3. [`./bootstrap-and-startup.md`](./bootstrap-and-startup.md)

## 3. Install repo-local dependencies

Do this once on the new machine before trying to start services.

### `ks-backend`

```bash
cd ~/dev/kriegspiel/ks-backend
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r src/app/requirements-dev.txt
deactivate
```

### `ks-web-app`

```bash
cd ~/dev/kriegspiel/ks-web-app/frontend
npm ci
```

### `ks-home`

```bash
cd ~/dev/kriegspiel/ks-home
npm ci
```

### `content`

`content` is a source repo, but installing its local Node dependencies is useful for validation:

```bash
cd ~/dev/kriegspiel/content
npm ci
```

### `ks-game`

This is mainly needed if you plan to work on the engine library directly:

```bash
cd ~/dev/kriegspiel/ks-game
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
deactivate
```

### Optional bot repos

Each bot repo is independent and normally uses its own `.venv` plus `.env`.
Follow the repo-local README when you actually want a bot running on the machine.

## 4. Create env files and secrets

Do not commit host secrets into git. Keep them in local `.env` files or host-managed env files.

### Backend

Local development config usually lives at:

- `~/dev/kriegspiel/ks-backend/.env`

Production-style systemd config on the live host currently lives at:

- `/etc/default/ks-backend`

Important backend settings:

- `SECRET_KEY`
- `BOT_TOKEN_HMAC_SECRET`
- `MONGO_URI`
- `SITE_ORIGIN`
- `BOT_REGISTRATION_KEY`
- `LOG_LEVEL`

The settings model is in:

- `~/dev/kriegspiel/ks-backend/src/app/config.py`

### Authenticated frontend

The frontend repo contains:

- `~/dev/kriegspiel/ks-web-app/.env`
- `~/dev/kriegspiel/ks-web-app/.env.example`

The production browser app uses same-origin `/api/...`, so public deployment does not rely on a separate frontend API-base switch.

### Static public site

`ks-home` usually does not need a dedicated checked-in `.env` file for normal serving.
The important build-time variables are:

- `KS_CONTENT_PATH`
- `KS_API_BASE`
- optionally `ROOT`
- optionally `WORK_ROOT`
- optionally `HOME_BRANCH`
- optionally `CONTENT_BRANCH`

### Bots

Each bot repo typically uses:

- a local `.env`
- a persisted `.bot-state.json`

## 5. Prove the stack starts locally before wiring systemd

Do a manual bring-up first. It is much easier to debug than a half-configured service unit.

### Start the backend

```bash
cd ~/dev/kriegspiel/ks-backend
. .venv/bin/activate
uvicorn app.main:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

### Start the authenticated frontend

```bash
cd ~/dev/kriegspiel/ks-web-app/frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

Open:

- `http://127.0.0.1:5173`

### Build and serve the public site

```bash
cd ~/dev/kriegspiel/ks-home
KS_CONTENT_PATH=~/dev/kriegspiel/content KS_API_BASE=http://127.0.0.1:8000 npm run build
HOST=127.0.0.1 PORT=4180 npm run serve:prod
```

Open:

- `http://127.0.0.1:4180`

If these three pieces work manually, the machine is ready for service automation.

## 6. Move to production-style service startup

Current service names used on the live host:

- `ks-backend.service`
- `ks-web-app-frontend.service`
- `ks-home.service`
- `ks-home-refresh.service`
- `ks-home-refresh.timer`

Important operational details:

- `ks-backend.service`
  - should run `ks-backend/.venv/bin/uvicorn`
  - should load its secrets from `/etc/default/ks-backend` or an equivalent host-managed env file
- `ks-web-app-frontend.service`
  - should run Vite preview from `ks-web-app/frontend/node_modules`
  - a built `dist/` alone is not enough if `node_modules` is missing
- `ks-home.service`
  - should build and then serve the public site
  - depends on the sibling `content` repo being available
- `ks-home-refresh.service`
  - uses `ks-home/scripts/refresh-static-site.sh`
  - depends on `rsync` and the `.site-refresh` worktree area

Use these docs for the production command details:

- [`bootstrap-and-startup.md`](./bootstrap-and-startup.md)
- [`services-and-processes.md`](./services-and-processes.md)
- [`runbook.md`](./runbook.md)

## 7. Public cutover prerequisites

Starting the services locally is not the same thing as exposing the stack publicly.

A brand-new public server still needs host-level setup for:

- DNS
- TLS termination
- reverse proxying or tunnel routing
- firewall policy
- any Cloudflare or edge-specific approvals

That edge layer is not fully managed from `ks-platform`.
Treat it as a separate deployment concern after the stack works locally on the machine.

## 8. First-day verification checklist

Before calling the server usable, verify:

### Workspace

- all required repos exist under the same workspace root
- `_wroktrees`, `_tmp`, and `.site-refresh` exist
- local dependency installs completed successfully

### Backend

- `curl http://127.0.0.1:8000/health` returns success
- MongoDB is reachable
- env values are loaded as expected

### Authenticated frontend

- the app loads locally
- it can reach `/api/...`
- `npm run build` succeeds

### Static site

- `KS_CONTENT_PATH` points at the sibling `content` repo
- `npm run build` succeeds in `ks-home`
- the served site returns `200`

### Optional bots

- each enabled bot can start
- each enabled bot can authenticate
- each enabled bot has its own `.env` and `.bot-state.json`

## 9. Day-2 operator workflow

Once the machine is bootstrapped, ongoing work should follow the normal workspace rules:

- create a dedicated worktree under `~/dev/kriegspiel/_wroktrees`
- do the actual change in the owning repo
- use PRs for substantive work
- validate locally and remotely as appropriate
- update `ks-platform` when architecture, deploy shape, or operator memory changes

The cross-repo workflow expectations live in:

- [`../AGENTS.md`](../AGENTS.md)
