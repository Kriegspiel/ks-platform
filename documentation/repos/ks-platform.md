# ks-platform

`ks-platform` is the org-level documentation and operations handbook repo.

It does not ship production runtime code.

It owns:

- cross-repo architecture notes
- deployment and orchestration rules
- shared data-structure explanations
- agent/operator memory
- generated repo/module inventory

## Why it exists

The active Kriegspiel.org system spans multiple repos with different runtimes:

- backend
- authenticated frontend
- static public site
- content source repo
- engine library
- multiple bots

This repo keeps the operational memory in one place so future work does not depend on reconstructing it from terminal history.

## Main files

### `README.md`

Org map and repo-structure entry point.

### `deployment/new-server-bootstrap.md`

Single-machine bootstrap guide for a fresh workstation or server.

### `AGENTS.md`

Cross-repo working rules and architectural constraints.

### `documentation/`

Human-facing docs:

- shared data structures
- runtime flows
- repo notes
- generated module index

### `deployment/`

How the system is run:

- domains and routing
- services and processes
- rollout/runbook

### `scripts/generate_inventory.py`

Regenerates the exhaustive `documentation/module-index.md` snapshot from the live checked-out repos.

## Practical rule

`ks-platform` should document implementation and operations, but should not become a shadow implementation repo.

Meaning:

- content still belongs in `content`
- runtime code still belongs in its owning repo
- this repo should explain, link, and record decisions

## When to update it

Update `ks-platform` when:

- repo responsibilities change
- routing or domain usage changes
- service/process rules change
- visibility or replay rules change
- rating/stat architecture changes
- bot orchestration rules change

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
