# ks-platform

Org-level documentation and operations handbook for the Kriegspiel.org codebase.

This repository does not ship production runtime code. Its job is to document:

- the active repositories in the `Kriegspiel` org
- the shared architecture and data structures
- deployment and orchestration rules
- agent/operator guidance for future work

## Main entry points

- [`deployment/new-server-bootstrap.md`](./deployment/new-server-bootstrap.md)
  - start-here checklist for bringing up a fresh workstation or server from a single `ks-platform` clone
- [`documentation/repo-map.md`](./documentation/repo-map.md)
  - grouped index of active repos, default branches, and current default-branch HEAD commits
- [`scripts/bootstrap_workspace.py`](./scripts/bootstrap_workspace.py)
  - clones the rest of the active repos beside this checkout so `ks-platform` can be the first repo on a new machine
- [`AGENTS.md`](./AGENTS.md)
  - workspace workflow plus platform-specific operational rules
- [`deployment/README.md`](./deployment/README.md)
  - deployment topology, services, routing, and rollout docs
- [`documentation/module-index.md`](./documentation/module-index.md)
  - exhaustive generated file/module inventory across the active repos

## Clone one repo first

If you are setting up a fresh server or workstation, clone `ks-platform` first and use it to create the rest of the workspace:

```bash
git clone git@github.com:Kriegspiel/ks-platform.git
cd ks-platform
python3 scripts/bootstrap_workspace.py --include-bots
```

Then continue with:

- [`deployment/new-server-bootstrap.md`](./deployment/new-server-bootstrap.md)
- [`AGENTS.md`](./AGENTS.md)
- [`deployment/bootstrap-and-startup.md`](./deployment/bootstrap-and-startup.md)

By default that script:

- treats the parent directory of the current `ks-platform` checkout as the workspace root
- clones the required sibling repos there
- optionally clones the bot repos when `--include-bots` is passed
- ensures the shared workspace directories exist:
  - `_wroktrees`
  - `_tmp`
  - `.site-refresh`

If you want only the main application repos, omit `--include-bots`.

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
- [`scripts/bootstrap_workspace.py`](./scripts/bootstrap_workspace.py): clones the active repos into a fresh workspace root
- [`scripts/workspace_repos.py`](./scripts/workspace_repos.py): shared repo catalog for bootstrap and repo-map generation
- [`scripts/generate_repo_map.py`](./scripts/generate_repo_map.py): regenerates the grouped repo map
- [`scripts/generate_inventory.py`](./scripts/generate_inventory.py): regenerates the module inventory snapshot

## Recommended reading order

1. [`deployment/new-server-bootstrap.md`](./deployment/new-server-bootstrap.md)
2. [`AGENTS.md`](./AGENTS.md)
3. [`documentation/README.md`](./documentation/README.md)
4. [`deployment/bootstrap-and-startup.md`](./deployment/bootstrap-and-startup.md)
5. [`deployment/README.md`](./deployment/README.md)
6. [`documentation/module-index.md`](./documentation/module-index.md)

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
python3 scripts/generate_repo_map.py
python3 scripts/generate_inventory.py
```

That rewrites:

- [`documentation/repo-map.md`](./documentation/repo-map.md)
- [`documentation/module-index.md`](./documentation/module-index.md)

from the checked-out active repos under `.../kriegspiel/`.
