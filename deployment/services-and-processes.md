# Services and Processes

This document lists the main deployed processes, what they do, and how they relate to each other.

## Main HTTP surfaces

| Surface | Owning repo | Notes |
| --- | --- | --- |
| `api.kriegspiel.org` | `ks-backend` | Dedicated API host for bots, scripts, docs, and external clients |
| `app.kriegspiel.org` | `ks-web-app` | Authenticated browser app; frontend calls same-origin `/api/...` |
| `kriegspiel.org` | `ks-home` | Static public site built from `ks-home` + `content` |

## Backend

Observed production process:

- service: `ks-backend.service`
- repo: `ks-backend`
- entrypoint: [`src/app/main.py`](/home/fil/dev/kriegspiel/ks-backend/src/app/main.py)

Responsibilities:

- auth and sessions
- game lifecycle
- active-game cache and async flush loop
- timeout sweeper
- transcripts/review payloads
- leaderboard and profile APIs
- technical reports

Runtime notes:

- starts `GameService` during FastAPI lifespan
- flushes cached games during graceful shutdown

## Authenticated frontend

Observed production process:

- service: `ks-web-app-frontend.service`
- repo: `ks-web-app`

Responsibilities:

- serves the built React frontend
- browser app uses same-origin `/api/...`

Operational note:

- browser auth and session cookies are simpler because the app and `/api` share origin

## Static public site

Primary repo:

- `ks-home`

Refresh automation:

- service: `ks-home-refresh.service`
- timer: `ks-home-refresh.timer`
- script: [`ks-home/scripts/refresh-static-site.sh`](/home/fil/dev/kriegspiel/ks-home/scripts/refresh-static-site.sh)

Responsibilities:

- build public static site
- pull content from `content`
- hydrate static pages such as rules, changelog, blog, about, and static leaderboard

Operational note:

- the refresh script uses detached worktrees in `/home/fil/dev/kriegspiel/.site-refresh`

## Bot services

All main bots run as single Python processes under systemd.

### `bot-random`

- service: `kriegspiel-random-bot.service`
- file: [`bot-random/deploy/kriegspiel-random-bot.service`](/home/fil/dev/kriegspiel/bot-random/deploy/kriegspiel-random-bot.service)
- entrypoint: `bot.py --poll-seconds 2`

### `bot-random-any`

- service: `kriegspiel-random-any-bot.service`
- file: [`bot-random-any/deploy/kriegspiel-random-any-bot.service`](/home/fil/dev/kriegspiel/bot-random-any/deploy/kriegspiel-random-any-bot.service)
- entrypoint: `bot.py --poll-seconds 2`

### `bot-gpt-nano`

- service: `kriegspiel-gpt-nano-bot.service`
- file: [`bot-gpt-nano/deploy/kriegspiel-gpt-nano-bot.service`](/home/fil/dev/kriegspiel/bot-gpt-nano/deploy/kriegspiel-gpt-nano-bot.service)
- entrypoint: `bot.py --poll-seconds 2`

### `bot-haiku`

- service: `kriegspiel-haiku-bot.service`
- file: [`bot-haiku/deploy/kriegspiel-haiku-bot.service`](/home/fil/dev/kriegspiel/bot-haiku/deploy/kriegspiel-haiku-bot.service)
- entrypoint: `bot.py --poll-seconds 2`

## Background loops inside processes

### `ks-backend`

- active-game cache
- flush loop
- timeout sweep loop

### main bots

- poll loop
- active-game iteration
- optional lobby join/create checks

There are no multi-worker bot schedulers right now. Each bot process handles multiple games serially.

## Content and documentation repos

These are not long-running services:

- `content`
- `ks-platform`

They are source repos consumed by:

- `ks-home`
- human operators

## Workspace-only directories that matter operationally

- `/home/fil/dev/kriegspiel/.site-refresh`
  - detached worktrees used by the static refresh script
- `/home/fil/dev/kriegspiel/_tmp`
  - holding area for non-active repos/worktrees

These are local machine concerns, not org repos.
