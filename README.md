# ks-platform

Org-level documentation and operations handbook for the Kriegspiel.org codebase.

This repository does not ship production runtime code. Its job is to document:

- the active repositories in the `Kriegspiel` org
- the shared architecture and data structures
- deployment and orchestration rules
- agent/operator guidance for future work

## Main entry points

- [`documentation/repo-map.md`](./documentation/repo-map.md)
  - grouped index of active repos, default branches, and current default-branch HEAD commits
- [`AGENTS.md`](./AGENTS.md)
  - workspace workflow plus platform-specific operational rules
- [`deployment/README.md`](./deployment/README.md)
  - deployment topology, services, routing, and rollout docs
- [`documentation/module-index.md`](./documentation/module-index.md)
  - exhaustive generated file/module inventory across the active repos

## Repo grouping

- Core services:
  - `ks-backend`
  - `ks-web-app`
  - `ks-home`
- Content and shared library:
  - `content`
  - `ks-game`
- Bots:
  - `bot-random`
  - `bot-random-any`
  - `bot-simple-heuristics`
  - `bot-gpt-nano`
  - `bot-haiku`
- Platform and operations:
  - `ks-platform`

For the structured version with GitHub links, branch links, and pinned HEAD commit links, use [`documentation/repo-map.md`](./documentation/repo-map.md).

## Repo layout

- [`AGENTS.md`](./AGENTS.md): cross-repo working rules for agents and operators
- [`documentation/repo-map.md`](./documentation/repo-map.md): grouped repo index with current default-branch commit links
- [`documentation/`](./documentation/README.md): architecture, repo notes, data structures, runtime flows, exhaustive module index
- [`deployment/`](./deployment/README.md): deployment topology, domains, services, rollout rules
- [`scripts/generate_repo_map.py`](./scripts/generate_repo_map.py): regenerates the grouped repo map
- [`scripts/generate_inventory.py`](./scripts/generate_inventory.py): regenerates the module inventory snapshot

## Recommended reading order

1. [`AGENTS.md`](./AGENTS.md)
2. [`documentation/README.md`](./documentation/README.md)
3. [`deployment/bootstrap-and-startup.md`](./deployment/bootstrap-and-startup.md)
4. [`deployment/README.md`](./deployment/README.md)
5. [`documentation/module-index.md`](./documentation/module-index.md)

## Local workspace notes

Outside this repo, the current local workspace typically also contains:

- `.../kriegspiel/.site-refresh/`: detached worktrees used by the hourly static-site refresh job
- `.../kriegspiel/_tmp/`: local holding area for non-active repos/worktrees
- `.../kriegspiel/node_modules/`: top-level Codex CLI dependency install
- `.../kriegspiel/localsetup/`: local machine notes such as Cloudflare tunnel setup

Those are workspace details, not organization repos.

## Refreshing generated docs

Run:

```bash
python scripts/generate_repo_map.py
python scripts/generate_inventory.py
```

That rewrites:

- [`documentation/repo-map.md`](./documentation/repo-map.md)
- [`documentation/module-index.md`](./documentation/module-index.md)

from the checked-out active repos under `.../kriegspiel/`.
