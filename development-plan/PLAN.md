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
| `step-400` | Gameplay Core | 6 | Engine integration, moves/ask-any/resign, hidden-info polling, clock/timeouts, transcript/archive, gameplay integration tests | `step-300` |
| `step-500` | Game UI | 5 | Board component, game page, phantoms, promotion, polish | `step-400` |
| `step-600` | Review and Player Features | 5 | Profile, history, leaderboard, settings, game review | `step-500` |
| `step-700` | Infra and Operations | 5 | Docker finalize, NGINX, CI, backup, logging | `step-600` |
| `step-800` | Hardening and Launch Readiness | 5 | Regression, security, error paths, docs, launch | `step-700` |

**Total: 41 slices**

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
- [step-200/210](./step-200/210/README.md) expands slice `210` from `step-200` into a dedicated implementation and automated-testing packet.
- [step-200/220](./step-200/220/README.md) expands slice `220` from `step-200` into a dedicated implementation and automated-testing packet.
- [step-200/230](./step-200/230/README.md) expands slice `230` from `step-200` into a dedicated implementation and automated-testing packet.
- [step-200/240](./step-200/240/README.md) expands slice `240` from `step-200` into a dedicated implementation and automated-testing packet.
- [step-200/250](./step-200/250/README.md) expands slice `250` from `step-200` into a dedicated implementation and automated-testing packet.
- [step-300/310](./step-300/310/README.md) expands slice `310` from `step-300` into a dedicated implementation and automated-testing packet.
- [step-300/320](./step-300/320/README.md) expands slice `320` from `step-300` into a dedicated implementation and automated-testing packet.
- [step-300/330](./step-300/330/README.md) expands slice `330` from `step-300` into a dedicated implementation and automated-testing packet.
- [step-300/340](./step-300/340/README.md) expands slice `340` from `step-300` into a dedicated implementation and automated-testing packet.
- [step-300/350](./step-300/350/README.md) expands slice `350` from `step-300` into a dedicated implementation and automated-testing packet.
- [step-400/410](./step-400/410/README.md) expands slice `410` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-400/420](./step-400/420/README.md) expands slice `420` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-400/430](./step-400/430/README.md) expands slice `430` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-400/440](./step-400/440/README.md) expands slice `440` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-400/450](./step-400/450/README.md) expands slice `450` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-400/460](./step-400/460/README.md) expands slice `460` from `step-400` into a dedicated implementation and automated-testing packet.
- [step-500/510](./step-500/510/README.md) expands slice `510` from `step-500` into a dedicated implementation and automated-testing packet.
- [step-500/520](./step-500/520/README.md) expands slice `520` from `step-500` into a dedicated implementation and automated-testing packet.
- [step-500/530](./step-500/530/README.md) expands slice `530` from `step-500` into a dedicated implementation and automated-testing packet.
- [step-500/540](./step-500/540/README.md) expands slice `540` from `step-500` into a dedicated implementation and automated-testing packet.
- [step-500/550](./step-500/550/README.md) expands slice `550` from `step-500` into a dedicated implementation and automated-testing packet.
- [step-600/610](./step-600/610/README.md) expands slice `610` from `step-600` into a dedicated implementation and automated-testing packet.
- [step-600/620](./step-600/620/README.md) expands slice `620` from `step-600` into a dedicated implementation and automated-testing packet.
- [step-600/630](./step-600/630/README.md) expands slice `630` from `step-600` into a dedicated implementation and automated-testing packet.
- [step-600/640](./step-600/640/README.md) expands slice `640` from `step-600` into a dedicated implementation and automated-testing packet.
- [step-600/650](./step-600/650/README.md) expands slice `650` from `step-600` into a dedicated implementation and automated-testing packet.
- [step-700/710](./step-700/710/README.md) expands slice `710` from `step-700` into a dedicated implementation and automated-testing packet.
- [step-700/720](./step-700/720/README.md) expands slice `720` from `step-700` into a dedicated implementation and automated-testing packet.
- [step-700/730](./step-700/730/README.md) expands slice `730` from `step-700` into a dedicated implementation and automated-testing packet.
- [step-700/740](./step-700/740/README.md) expands slice `740` from `step-700` into a dedicated implementation and automated-testing packet.
- [step-700/750](./step-700/750/README.md) expands slice `750` from `step-700` into a dedicated implementation and automated-testing packet.
- [step-800/810](./step-800/810/README.md) expands slice `810` from `step-800` into a dedicated implementation and automated-testing packet.
- [step-800/820](./step-800/820/README.md) expands slice `820` from `step-800` into a dedicated implementation and automated-testing packet.
- [step-800/830](./step-800/830/README.md) expands slice `830` from `step-800` into a dedicated implementation and automated-testing packet.
- [step-800/840](./step-800/840/README.md) expands slice `840` from `step-800` into a dedicated implementation and automated-testing packet.
- [step-800/850](./step-800/850/README.md) expands slice `850` from `step-800` into a dedicated implementation and automated-testing packet.
