# Development Plan

This plan covers the MVP build path for the Kriegspiel platform.

Sequence is strict unless a step explicitly documents a justified dependency exception.

## High-Level Steps

| Step | Name | Slices | Goal | Depends On |
|---|---|---|---|---|
| `step-100` | Foundation and Scaffold | 4 | App skeleton, settings, MongoDB wiring, Docker, tests | — |
| `step-200` | Auth and Sessions | 6 | Users, sessions, register/login/logout, CSRF, auth pages | `step-100` |
| `step-300` | Lobby and Game Lifecycle REST | 6 | Game create/join/open/mine/resign, lobby page, expiry | `step-200` |
| `step-400` | Real-Time Gameplay Core | 7 | WebSocket gameplay, engine, clocks, reconnect, abandon | `step-300` |
| `step-500` | Core Game UI | 6 | Design system, pages, board UX, phantoms, promotion | `step-400` |
| `step-600` | Review and Player Features | 5 | Profile, history, leaderboard, settings, game review | `step-500` |
| `step-700` | Infra and Operations | 5 | Docker finalize, NGINX, CI, backup, logging | `step-600` |
| `step-800` | Hardening and Launch Readiness | 5 | Regression, security audit, error paths, docs, launch | `step-700` |

**Total: 44 slices**

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
