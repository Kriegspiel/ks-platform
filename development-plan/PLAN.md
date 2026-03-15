# Development Plan

This plan covers the MVP build path for the Kriegspiel platform.

Sequence is strict unless a step explicitly documents a justified dependency exception.

## High-Level Steps

| Step | Name | Goal | Depends On |
|---|---|---|---|
| `step-100` | Foundation and Scaffold | Make the app runnable with the expected project layout, settings, health check, DB wiring, and test harness. | — |
| `step-200` | Auth and Sessions | Implement users, sessions, registration/login/logout, session hydration, CSRF, and auth pages. | `step-100` |
| `step-300` | Lobby and Game Lifecycle REST | Implement game create/join/open/mine/resign flows, lobby behavior, and waiting-game expiry. | `step-200` |
| `step-400` | Real-Time Gameplay Core | Implement WebSocket gameplay, engine integration, clocks, reconnect, pause/abandon, and hidden-information payloads. | `step-300` |
| `step-500` | Core Game UI | Build the main player-facing pages and board UX: lobby polish, game page, phantom pieces, promotion, referee log, and clock rendering. | `step-400` |
| `step-600` | Review and Player Features | Implement profile/history/leaderboard/settings plus the review/replay experience. | `step-500` |
| `step-700` | Infra and Operations | Finish Docker, NGINX, CI, backup/restore, deployment scripts, logging, and health/ops readiness. | `step-600` |
| `step-800` | Hardening and Launch Readiness | Run full-system QA, security/error-path checks, documentation cleanup, and launch checklist signoff. | `step-700` |

## Notes

- Each step is intentionally split into smaller slices in its own `README.md`.
- A single agent should usually pick up one slice at a time, not a whole step at once.
- Every step must have passing tests before it can be marked `DONE`.
