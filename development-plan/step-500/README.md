# Step 500 - Game UI

## Goal

Deliver production-shaped React gameplay UX on top of Step 400 APIs: board interaction, polling game screen, phantom workflow, promotion UX, and navigation polish.

## Read First

- [FRONTEND.md](../../FRONTEND.md)
- [API_SPEC.md](../../API_SPEC.md)
- [DESIGN.md](../../DESIGN.md)
- [development-plan/README.md](../README.md)
- [development-plan/PLAN.md](../PLAN.md)

## Depends On

- `step-400` (DONE before implementation start)

## Scope Decision: 5 Slices (No Split Needed)

Step 500 remains 5 slices because each slice maps to one UI seam with low cross-coupling:

1. `510` board rendering + click primitives
2. `520` game page orchestration + polling/actions
3. `530` phantom tray + local persistence
4. `540` promotion modal + in-game interaction polish
5. `550` home/rules/nav entry flow polish

Unlike Step 400, there is no backend timing seam that forces additional decomposition.

## Slice Packets

- [510 - Chess board component and visual-state primitives](./510/README.md)
- [520 - Game page polling loop and gameplay actions](./520/README.md)
- [530 - Phantom tray and client persistence](./530/README.md)
- [540 - Promotion modal and interaction polish](./540/README.md)
- [550 - Home/rules/navigation polish](./550/README.md)

Every slice folder contains `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, and `CHECKLIST.md`.

## Exit Criteria

- Authenticated user can play by click-to-move from `/game/:id`.
- Polling updates board/referee/clock and stops at completion.
- Phantom state is client-only and persisted per game id.
- Promotion UX correctly appends `q/r/b/n` suffix and handles cancel.
- Home/rules/nav provides clear entry and active-game discoverability.

## Out of Scope

- Profile/history/leaderboard deep features (Step 600)
- Deployment/ops concerns (Step 700)
