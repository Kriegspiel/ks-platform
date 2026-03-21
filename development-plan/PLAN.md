# Development Plan

This plan covers the MVP build path for the Kriegspiel platform.

Sequence is strict unless a step explicitly documents a justified dependency exception.

## Architecture Decisions

These override the original spec docs where they conflict:

| Concern | Decision | Rationale |
|---|---|---|
| Frontend | React + Vite SPA | Matches ks-v2 prototype |
| Database | MongoDB (Motor async) | Per platform specs |
| Real-time | Polling (2s interval) | Simpler than WebSocket, matches ks-v2 |
| Auth | Simple (bcrypt + session cookie) | No CSRF middleware, no session hydration middleware — just a dependency |
| CSS | Component CSS files | No custom design system — style per component |
| Board UI | Custom React component (click-based, Unicode pieces) | Matches ks-v2 ChessBoard.jsx pattern |
| Game lifecycle | Simplified: waiting → active → completed | Join codes, no pause/abandon/aborted |
| Deployment | Docker Compose + NGINX | Per platform specs |
| CI/CD | GitHub Actions | Per platform specs |
| Phantom pieces | React component + localStorage | Client-only, per platform spec |

## High-Level Steps

| Step | Name | Slices | Goal | Depends On |
|---|---|---|---|---|
| `step-100` | Foundation and Scaffold | 5 | Backend app factory, MongoDB, React scaffold, Docker, tests | — |
| `step-200` | Auth and Sessions | 5 | Users, passwords, login/register API + React pages | `step-100` |
| `step-300` | Lobby and Game Lifecycle | 5 | Create/join/list games, join codes, lobby UI | `step-200` |
| `step-400` | Gameplay Core | 5 | Engine integration, moves, ask-any, resign, polling, clock | `step-300` |
| `step-500` | Game UI | 5 | Board component, game page, phantoms, promotion, polish | `step-400` |
| `step-600` | Review and Player Features | 5 | Profile, history, leaderboard, settings, game review | `step-500` |
| `step-700` | Infra and Operations | 5 | Docker finalize, NGINX, CI, backup, logging | `step-600` |
| `step-800` | Hardening and Launch Readiness | 5 | Regression, security, error paths, docs, launch | `step-700` |

**Total: 40 slices**

## Slice Sizing

Each slice is designed to be completable in a single ~$20 agent session (~15-20 minutes of focused work). A slice typically involves:

- Creating or modifying 3-8 files
- Writing 100-400 lines of code/config
- Running tests to verify the work

## Notes

- Each step is split into smaller slices in its own `README.md`.
- A single agent should pick up **one slice at a time**, not a whole step.
- Every step must have passing tests before it can be marked `DONE`.
- Each slice has specific file lists, acceptance criteria, and a clear "done" definition.
- Some slices may also get their own detailed execution packet in a folder such as `step-100/110/` when the slice needs multiple planning documents.
- When that happens, the slice packet expands the parent step's slice; it does not become a new top-level rollup step unless this file explicitly says so.
- Where this plan conflicts with spec docs (ARCHITECTURE.md, FRONTEND.md, AUTH.md, etc.), **this plan wins**.

## Detailed Slice Packets

- [step-100/110](./step-100/110/README.md) expands slice `110` from `step-100` into a dedicated implementation and automated-testing packet.
- [step-100/120](./step-100/120/README.md) expands slice `120` from `step-100` into a dedicated implementation and automated-testing packet.
- [step-100/130](./step-100/130/README.md) expands slice `130` from `step-100` into a dedicated implementation and automated-testing packet.
- [step-100/140](./step-100/140/README.md) expands slice `140` from `step-100` into a dedicated implementation and automated-testing packet.
- [step-100/150](./step-100/150/README.md) expands slice `150` from `step-100` into a dedicated implementation and automated-testing packet.
