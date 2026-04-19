# Deployment

This folder documents how the Kriegspiel.org system is run and orchestrated.

## What is deployed

- `api.kriegspiel.org`
  - FastAPI backend from `ks-backend`
- `app.kriegspiel.org`
  - authenticated frontend from `ks-web-app`
- `kriegspiel.org`
  - static public site from `ks-home`
- bot services
  - `bot-random`
  - `bot-random-any`
  - `bot-simple-heuristics`
  - `bot-gpt-nano`
  - `bot-haiku`

## Key documents

- [`new-server-bootstrap.md`](./new-server-bootstrap.md)
  - single-machine bootstrap checklist for a fresh workstation or server
- [`bootstrap-and-startup.md`](./bootstrap-and-startup.md)
  - prerequisites, env files, startup order, live process commands, and common failure modes
- [`services-and-processes.md`](./services-and-processes.md)
  - systemd services, background loops, timers
- [`domains-and-routing.md`](./domains-and-routing.md)
  - hostname responsibilities and routing rules
- [`runbook.md`](./runbook.md)
  - rollout, refresh, and verification checklist
