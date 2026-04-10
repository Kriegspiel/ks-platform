# Domains and Routing

This document explains why Kriegspiel.org uses multiple hostnames and how traffic is intended to flow.

## Public domains

### `kriegspiel.org`

Purpose:

- public static marketing/content site
- rules
- blog
- changelog
- about
- static leaderboard

Owning repo:

- `ks-home`

Content source:

- `content`

### `app.kriegspiel.org`

Purpose:

- authenticated browser app
- lobby
- active play
- review
- profile pages
- live leaderboard
- technical reports

Owning repo:

- `ks-web-app`

### `api.kriegspiel.org`

Purpose:

- dedicated API host for:
  - bots
  - scripts
  - curl/docs examples
  - external clients

Owning repo:

- `ks-backend`

## Why both `app.kriegspiel.org/api` and `api.kriegspiel.org` exist

They point at the same backend, but they are used differently.

### `app.kriegspiel.org/api`

Use for:

- browser frontend requests

Reasons:

- same-origin browser requests
- simpler cookie/session behavior
- no extra CORS complexity

### `api.kriegspiel.org`

Use for:

- bots
- scripts
- public docs examples
- non-browser clients

Reasons:

- clear dedicated API hostname
- clean separation for programmatic access

## Practical routing rule

- browser code should prefer same-origin `/api/...`
- non-browser clients can use `https://api.kriegspiel.org`

## URL design rules

### Games

Public URLs should use `game_code`, not Mongo ids.

Examples:

- `/game/ABC123`
- `/game/ABC123/review`
- `/join/ABC123`

### Profiles

Public profile URLs are username-based:

- `/user/notifil`
- `/user/gptnano`
- `/user/randobotany/games`

## Access patterns

### Active game state

- only participants can load active state
- active state should expose only player-visible information

### Completed review

- completed review can expose full replay information by design
- this is intentionally different from active-game visibility

## Static vs live leaderboard split

### `kriegspiel.org/leaderboard`

- static
- human-only
- overall rating only

### `app.kriegspiel.org/leaderboard`

- live
- paginated
- richer player data

## Content publication path

Content moves like this:

1. edit `content`
2. refresh `ks-home`
3. static site rebuild publishes the change to `kriegspiel.org`

Changing `content` alone does not publish anything until `ks-home` rebuilds.
