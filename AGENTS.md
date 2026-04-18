# Kriegspiel Workspace Notes

This workspace keeps project-specific Codex skills in `/Users/fil/Developer/kriegspiel/_skills/`.

## Project-Local Skills

- For remote machine work on host alias `rpis02-cf`, use `/Users/fil/Developer/kriegspiel/_skills/rpis02-cf-remote-ops/`.
- Keep that skill project-local. Do not install or symlink it into `~/.codex/skills` unless explicitly requested.

## Remote Ops Defaults

- Remote host: `rpis02-cf`
- Remote repo root: `/home/fil/dev/kriegspiel`
- Prefer `/Users/fil/Developer/kriegspiel/_skills/rpis02-cf-remote-ops/scripts/run-remote.sh` for non-interactive commands.
- Prefer `/Users/fil/Developer/kriegspiel/_skills/rpis02-cf-remote-ops/scripts/open-shell.sh` for interactive SSH sessions.
- Use `ks-platform` as the operations handbook for service names, rollout steps, and verification expectations.

## Typical Workflow

- Do development locally in a dedicated branch and dedicated worktree under `/Users/fil/Developer/kriegspiel/_wroktrees/`.
- Prefer clean, focused changes per repo. Do not mix unrelated repo changes in one branch.
- When code changes ship to users, bump the repo version before merge. For test-only or docs-only changes, do not bump the version unless explicitly requested.
- Open a PR for substantive changes. Use a clear title and a detailed description covering what changed, why, how it was tested, and any deployment notes.
- Test remotely on `rpis02-cf` before merge when remote validation matters. Prefer a temporary remote worktree for pre-merge validation instead of changing the deployed checkout.
- Comment on the PR with remote test results, important observations, and the exact commit that was verified.
- If remote tests fail, fix locally, commit, push, and rerun remote verification. Iterate until green rather than stopping after the first failure.
- Merge the PR once validation is complete, then delete the feature branch unless there is a reason to keep it.
- After merge, fast-forward the deployed remote checkout, rerun the needed tests there, and restart the relevant service when runtime code changed.
- After restart, verify service health and any relevant public endpoint, then report back with the final deployed commit and verification result.

## ks-platform Role

Use this repo as the source of truth for:

- repo responsibilities
- deployment shape
- architecture constraints
- historical decisions that should not be rediscovered repeatedly

## Canonical Repo Responsibilities

- `ks-backend`
  - owns API contracts, persistence, authentication, rating/stat computation, transcript generation, and game lifecycle
- `ks-web-app`
  - owns the authenticated browser UI for lobby, play, review, profile, leaderboard, settings, and technical reports
- `ks-home`
  - owns the static public website and static content rendering
- `content`
  - owns all editable long-form/public content
- `ks-game`
  - owns the Berkeley Kriegspiel engine and serialization primitives
- `bot-*`
  - own individual bot runtimes and systemd units

## Current Runtime Shape

- `kriegspiel.org`
  - static site built by `ks-home`
  - content pulled from `content`
- `app.kriegspiel.org`
  - browser app from `ks-web-app`
  - frontend uses same-origin relative `/api/...` requests
- `api.kriegspiel.org`
  - dedicated API hostname for bots, scripts, docs examples, and external clients

Practical rule:

- browser code should prefer `app.kriegspiel.org/api`
- programmatic clients can use `api.kriegspiel.org`

## Architecture Rules That Should Stay True

### Game identifiers

- public browser URLs should use `game_code`, not Mongo ObjectIds
- internal persistence can still use `_id`
- examples:
  - `/game/ABC123`
  - `/game/ABC123/review`

### Hidden-information safety

- active game views must never leak opponent pieces to the browser
- completed-game review may expose full replay data by design
- if a feature needs more review detail, prefer perspective-specific rendering over leaking active hidden state

### Backend is the source of truth for stats

- frontend should not recompute lifetime player stats from partial history pages
- `ks-backend` owns:
  - lifetime results
  - lifetime ratings
  - aggregated rating-history series
  - bots report data

### Data migrations are better than permanent compatibility branches

If old data can be normalized once, prefer:

1. write a migration/backfill
2. run it
3. remove the legacy fallback

Recent examples already cleaned this way:

- legacy root-level scoresheets vs `engine_state`
- legacy archive rating snapshot shapes
- legacy bot bcrypt auth fallback

Do not reintroduce compatibility branches unless the data is genuinely unrecoverable.

### Review and transcript semantics

- replay controls move by ply, not raw attempts
- move logs group all same-player attempts inside one ply box
- capture highlights should remain visible in both private replay views
- public review and history links should use `game_code`

### Ratings

- every player has three tracks:
  - `overall`
  - `vs_humans`
  - `vs_bots`
- backend stores both lifetime summary stats and track rating snapshots
- charts use backend-prepared series, not frontend-derived slices

### Bot auth

- bot tokens use HMAC digest auth
- in-process bot auth cache TTL is `3600` seconds
- legacy bcrypt token fallback has already been removed

### Active game persistence

- active games are cached in memory by backend
- human-involved games flush after every successful visible action
- bot-vs-bot games flush:
  - every 20 plies
  - on completion
  - after 30s idle
- backend flushes all cached games on graceful shutdown

### Static public leaderboard

- `kriegspiel.org/leaderboard` is static, human-only, overall-rating only
- richer live leaderboard stays on `app.kriegspiel.org/leaderboard`

## Bot Behavior Rules Worth Preserving

- bots cannot join human-created waiting lobby games
- humans can create selected-bot games directly
- all main bots now sample bot-vs-bot joins at most once per minute
- `randobot`
  - allows up to 5 active games
  - auto-creates human-joinable waiting games
  - samples bot-vs-bot joins once per minute with 50% probability
- `randobotany`
  - allows up to 5 active games
  - auto-creates human-joinable waiting games
  - samples bot-vs-bot joins once per minute with 50% probability
  - asks `any pawn captures?` first where supported
- model bots (`gptnano`, `haiku`) are intentionally low-concurrency
  - active-game cap is 1
  - bot-vs-bot join probability is 0.1%
  - they do not auto-create waiting games
  - provider preflight is checked only before joining a new bot-vs-bot game, not before every turn
- random bots are single-process serial pollers, not multi-worker schedulers
- `simpleheuristics`
  - auto-creates human-joinable waiting games
  - allows up to 5 active games
  - samples bot-vs-bot joins once per minute with 10% probability
  - prioritizes recaptures, queen promotions, then weighted piece selection

If bot join behavior changes, document:

- sampling interval
- probability
- active-game cap
- whether the bot auto-creates waiting games

### Waiting-game lifecycle and code retention

- waiting games expire after 10 minutes if nobody joins
- deleted waiting games release their `game_code`
- completed archived games keep their `game_code` reserved permanently

## Deployment Rules

- by default, shared-repo changes should land through a branch plus PR flow
- direct pushes to `main` should be treated as exceptions for:
  - explicit user instruction
  - urgent operational repair
- user-facing changes in `ks-web-app` should bump the frontend version
- user-facing/API changes in `ks-backend` should bump backend version
- `ks-home` has its own independent version
- content-only changes usually do not require backend/frontend version bumps
- content changes require a `ks-home` refresh to reach `kriegspiel.org`

## Validation Expectations

Before calling work done:

- run focused tests in the touched repo
- run a production build where applicable
- verify the live endpoint or service after rollout

Typical examples:

- backend:
  - `pytest ...`
  - health check at `/health`
- web app:
  - `npm test -- --run ...`
  - `npm run build`
- ks-home:
  - `npm run build`
  - route/content tests

## Repo Hygiene

- keep `ks-platform` documentation current when architecture changes materially
- regenerate [`documentation/repo-map.md`](./documentation/repo-map.md) after repo ownership/default-branch/HEAD changes
- regenerate [`documentation/module-index.md`](./documentation/module-index.md) after major repo/layout changes
- do not let `ks-platform` drift into a second source of truth for content owned elsewhere
- document decisions here, but keep the actual implementation in its owning repo
