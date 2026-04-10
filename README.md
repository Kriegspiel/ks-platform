# ks-platform

Org-level documentation and operations handbook for the Kriegspiel.org codebase.

This repository does not ship production runtime code. Its job is to document:

- the active repositories in the `Kriegspiel` org
- the shared architecture and data structures
- deployment and orchestration rules
- agent/operator guidance for future work

## Active repos

| Repo | Role |
| --- | --- |
| `ks-backend` | FastAPI backend for `api.kriegspiel.org` and the `/api` surface behind `app.kriegspiel.org` |
| `ks-web-app` | Authenticated React application at `app.kriegspiel.org` |
| `ks-home` | Static public website at `kriegspiel.org` |
| `content` | Source-of-truth content for blog, changelog, rules, and site copy |
| `ks-game` | Python Kriegspiel engine library used by the backend |
| `bot-random` | Baseline random bot |
| `bot-random-any` | Random bot that asks `any pawn captures?` first |
| `bot-gpt-nano` | OpenAI-driven model bot |
| `bot-haiku` | Anthropic-driven model bot |
| `ks-platform` | This handbook repo |

## Repo layout

- [`AGENTS.md`](./AGENTS.md): cross-repo working rules for agents and operators
- [`documentation/`](./documentation/README.md): architecture, repo notes, data structures, runtime flows, exhaustive module index
- [`deployment/`](./deployment/README.md): deployment topology, domains, services, rollout rules
- [`scripts/generate_inventory.py`](./scripts/generate_inventory.py): regenerates the module inventory snapshot

## Recommended reading order

1. [`AGENTS.md`](./AGENTS.md)
2. [`documentation/README.md`](./documentation/README.md)
3. [`deployment/README.md`](./deployment/README.md)
4. [`documentation/module-index.md`](./documentation/module-index.md)

## Local workspace notes

Outside this repo, the current local workspace typically also contains:

- `/home/fil/dev/kriegspiel/.site-refresh`: detached worktrees used by the hourly static-site refresh job
- `/home/fil/dev/kriegspiel/_tmp`: local holding area for non-active repos/worktrees
- `/home/fil/dev/kriegspiel/node_modules`: top-level Codex CLI dependency install
- `/home/fil/dev/kriegspiel/localsetup`: local machine notes such as Cloudflare tunnel setup

Those are workspace details, not organization repos.

## Refreshing the module index

Run:

```bash
python scripts/generate_inventory.py
```

That rewrites [`documentation/module-index.md`](./documentation/module-index.md) from the live checked-out repos under `/home/fil/dev/kriegspiel`.
