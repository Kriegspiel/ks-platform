# Repo Map

This file is the quick index for the active Kriegspiel repositories.

It is grouped by responsibility so `ks-platform` can act as the main entry point for deployment and architecture work.

## Link policy

- Repo links go to the repository root for easy browsing.
- Default-branch links go to `main` or `master` and are therefore always the latest branch view.
- HEAD commit links are pinned snapshots of the current default-branch commit at generation time.
- Use branch links for navigation and pinned commit links for rollout notes, audits, and deployment references.

A single link cannot be both permanently pinned and always-latest. Keeping both link types is the safest pattern.

## Workspace bootstrap

Use [`scripts/bootstrap_workspace.py`](../scripts/bootstrap_workspace.py) after cloning `ks-platform` if you want this repo to act as the entry point for a fresh machine.

That script clones the sibling repos into the same workspace root and creates the shared helper directories.

## Core services

| Repo | Purpose | Surface / deployment | Default branch | Current default-branch HEAD |
| --- | --- | --- | --- | --- |
| [`ks-backend`](https://github.com/Kriegspiel/ks-backend) | FastAPI backend for API contracts, persistence, ratings, auth, and transcripts | `api.kriegspiel.org`, `ks-backend.service` | [`main`](https://github.com/Kriegspiel/ks-backend/tree/main) | [`6cfd6c0`](https://github.com/Kriegspiel/ks-backend/commit/6cfd6c05530a6fc8291cc581d9523b633015e7b8) |
| [`ks-web-app`](https://github.com/Kriegspiel/ks-web-app) | Authenticated React frontend for lobby, play, review, profiles, and reports | `app.kriegspiel.org`, `ks-web-app-frontend.service` | [`main`](https://github.com/Kriegspiel/ks-web-app/tree/main) | [`e3e3d63`](https://github.com/Kriegspiel/ks-web-app/commit/e3e3d63755ebc590e28aeef376c8dfd1326050ae) |
| [`ks-home`](https://github.com/Kriegspiel/ks-home) | Static public site renderer and server for the marketing/docs website | `kriegspiel.org`, `ks-home.service` | [`master`](https://github.com/Kriegspiel/ks-home/tree/master) | [`c1b10d4`](https://github.com/Kriegspiel/ks-home/commit/c1b10d43eca1d4c38e6f9102b374f80a78b09fd1) |

## Content and shared library

| Repo | Purpose | Surface / deployment | Default branch | Current default-branch HEAD |
| --- | --- | --- | --- | --- |
| [`content`](https://github.com/Kriegspiel/content) | Source-of-truth content for blog, changelog, rules, and site copy | Consumed by `ks-home` during refresh/build | [`master`](https://github.com/Kriegspiel/content/tree/master) | [`01913ca`](https://github.com/Kriegspiel/content/commit/01913cac41cce2f777bc463c5e77801748a237f7) |
| [`ks-game`](https://github.com/Kriegspiel/ks-game) | Python Kriegspiel engine library, move objects, and serialization | Library dependency, published to PyPI | [`master`](https://github.com/Kriegspiel/ks-game/tree/master) | [`3e25b35`](https://github.com/Kriegspiel/ks-game/commit/3e25b35ef8a511a5583d0d5eb46dfb867c01699a) |

## Bots

| Repo | Purpose | Surface / deployment | Default branch | Current default-branch HEAD |
| --- | --- | --- | --- | --- |
| [`bot-random`](https://github.com/Kriegspiel/bot-random) | Baseline random bot | `kriegspiel-random-bot.service` | [`main`](https://github.com/Kriegspiel/bot-random/tree/main) | [`484c36f`](https://github.com/Kriegspiel/bot-random/commit/484c36f4f97df3ece55e5e65098bc4d08f5894b0) |
| [`bot-random-any`](https://github.com/Kriegspiel/bot-random-any) | Random bot that asks pawn-capture questions first | `kriegspiel-random-any-bot.service` | [`master`](https://github.com/Kriegspiel/bot-random-any/tree/master) | [`c7e95d0`](https://github.com/Kriegspiel/bot-random-any/commit/c7e95d050cdce1498a7c329c1ec0839bea2c5948) |
| [`bot-simple-heuristics`](https://github.com/Kriegspiel/bot-simple-heuristics) | Heuristic bot with recapture, promotion, and weighted choice logic | `kriegspiel-simple-heuristics-bot.service` | [`main`](https://github.com/Kriegspiel/bot-simple-heuristics/tree/main) | [`14da679`](https://github.com/Kriegspiel/bot-simple-heuristics/commit/14da67996405cb91cd95d2e95a50c5e7499e23fb) |
| [`bot-gpt-nano`](https://github.com/Kriegspiel/bot-gpt-nano) | OpenAI-driven model bot | `kriegspiel-gpt-nano-bot.service` | [`main`](https://github.com/Kriegspiel/bot-gpt-nano/tree/main) | [`6cc1a5c`](https://github.com/Kriegspiel/bot-gpt-nano/commit/6cc1a5cfcdd3540f54de4162c2028c39e2f32a01) |
| [`bot-haiku`](https://github.com/Kriegspiel/bot-haiku) | Anthropic-driven model bot | `kriegspiel-haiku-bot.service` | [`main`](https://github.com/Kriegspiel/bot-haiku/tree/main) | [`31076da`](https://github.com/Kriegspiel/bot-haiku/commit/31076daaf782e33a7d6f13be2933f9241f09ad79) |

## Platform and operations

| Repo | Purpose | Surface / deployment | Default branch | Current default-branch HEAD |
| --- | --- | --- | --- | --- |
| [`ks-platform`](https://github.com/Kriegspiel/ks-platform) | Org-level documentation, deployment handbook, and operator memory | Documentation-only handbook repo | [`main`](https://github.com/Kriegspiel/ks-platform/tree/main) | [`f99b690`](https://github.com/Kriegspiel/ks-platform/commit/f99b6904b578e79eac2830349c21c0f7f55cc6e6) |
