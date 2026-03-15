# Step 500 - Core Game UI

## Goal

Build the main player-facing web experience for landing, lobby polish, the live game board, phantom pieces, promotion, and referee presentation.

## Read First

- [FRONTEND.md](../../FRONTEND.md)
- [DESIGN.md](../../DESIGN.md)
- [API_SPEC.md](../../API_SPEC.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-400`

## Task Slices

- `500.1` Build the shared layout, home page, and polished lobby page against the working backend.
- `500.2` Implement the live game page with board rendering, connection state, and referee log wiring.
- `500.3` Implement phantom piece UX and persistence.
- `500.4` Implement promotion modal, clock rendering, and core interaction polish.

## Required Tests Before Done

- Frontend smoke tests for primary pages.
- Focused interaction tests for phantom pieces and promotion.
- Manual QA across desktop and mobile breakpoints.

## Exit Criteria

- The live game page is usable end-to-end by a human player.
- Phantom pieces work and remain client-only.
- Promotion uses an explicit chooser.
- The core pages match the intended design system well enough for MVP use.

## Out of Scope

- Profile/history/leaderboard features
- Deploy/VPS/TLS work
- Final launch QA
