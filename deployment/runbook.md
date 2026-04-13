# Runbook

This is the short operator checklist for common changes across the active Kriegspiel.org repos.

## 1. Backend change

Repo:

- `ks-backend`

Checklist:

1. run focused pytest for touched areas
2. run a compile check for changed Python modules when useful
3. roll the backend service
4. verify:
   - `/health`
   - affected API routes
   - critical flows such as lobby/game/profile if relevant

Extra checks for schema/data changes:

- run migration/backfill script
- verify post-migration counts
- remove legacy fallback code only after data is normalized

## 2. Authenticated frontend change

Repo:

- `ks-web-app`

Checklist:

1. bump frontend version for user-visible change
2. run focused Vitest suites
3. run `npm run build`
4. roll the frontend process
5. verify:
   - home
   - affected page
   - version footer

## 3. Static public site change

Repo:

- `ks-home`

Checklist:

1. bump `ks-home` version for user-visible site change
2. run `npm run build`
3. run focused route/content tests
4. refresh the static site
5. verify the public page on `kriegspiel.org`

## 4. Content-only change

Repo:

- `content`

Checklist:

1. update content source files
2. run any content index build if relevant
3. refresh `ks-home`
4. verify the public page on `kriegspiel.org`

Important:

- content changes are not live until `ks-home` rebuilds

## 5. Bot change

Repo:

- one of `bot-random`, `bot-random-any`, `bot-simple-heuristics`, `bot-gpt-nano`, `bot-haiku`

Checklist:

1. run unit tests
2. compile-check `bot.py`
3. roll the systemd unit
4. verify:
   - process is back up
   - bot can still authenticate
   - active game behavior still works

## 6. Architecture cleanup or migration

Preferred pattern:

1. identify the old compatibility path
2. write the one-time migration
3. run it and verify counts
4. remove the fallback
5. add regression coverage for the normalized state

Recent examples:

- scoresheets moved fully into `engine_state`
- archive rating snapshots recalculated globally
- legacy bot bcrypt auth removed

## 7. Static-site refresh command

Reference script:

- `.../kriegspiel/ks-home/scripts/refresh-static-site.sh`

What it does:

- updates detached worktrees for `ks-home` and `content`
- builds `ks-home`
- syncs generated files into the live `dist`

## 8. Things to verify after restart/rollout

### Backend

- health endpoint version
- DB connected
- active games still accessible
- timeout sweeper starts correctly

### Frontend

- page loads
- version footer updated
- no raw API error text regressions

### Bots

- process PID changed as expected
- token restore/auth still works
- join/create policy is still what was intended

### Static site

- page returns `200`
- timestamp/version updated when expected
- content changes actually rendered

## 9. When to update `ks-platform`

Update this repo when:

- a runtime contract changes
- a new repo becomes part of the active system
- service names or deployment patterns change
- identifier, visibility, replay, bot, or ratings rules change materially

`ks-platform` should stay an operator handbook, not a second implementation source of truth.
