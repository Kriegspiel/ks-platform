# Step 300 - Lobby and Game Lifecycle

## Goal

Deliver production-shaped lobby and game lifecycle foundations across backend + frontend with deterministic test gates for each slice.

## Read First

- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [FRONTEND.md](../../FRONTEND.md)
- [development-plan/README.md](../README.md)
- [development-plan/PLAN.md](../PLAN.md)

## Depends On

- `step-200` (DONE before implementation start)

## Lifecycle Contract (Locked for MVP)

Step 300 must keep the game lifecycle constrained to:

`waiting -> active -> completed`

The following are explicitly out of scope for Step 300 implementation: `paused`, `abandoned`, timeout adjudication, reconnect state machine, and move execution internals.

## Slice Packets

Each slice has a detailed implementation packet:

- [310 - Game domain models + code generation service](./310/README.md)
- [320 - GameService lifecycle operations](./320/README.md)
- [330 - Authenticated game/lobby API surface](./330/README.md)
- [340 - Frontend lobby UX + polling flows](./340/README.md)
- [350 - Integration verification + lifecycle hardening checks](./350/README.md)

Every slice folder contains:

- `README.md` (scope contract)
- `IMPLEMENTATION.md` (execution-level build plan)
- `TESTING.md` (exact commands + expected outcomes)
- `CHECKLIST.md` (operator checklist)

## Exit Criteria

- Logged-in user can create a game and receive a unique join code.
- Second user can join via join code and transition game from `waiting` to `active`.
- Lobby UI supports create/join/open/mine flows with documented polling intervals.
- Resign and waiting-game delete flows enforce ownership/state rules.
- Step-300 progress docs contain exact command evidence per completed slice.

## Out of Scope

- Move execution and board-state mutation (Step 400)
- Board rendering and piece interactions (Step 500)
- Game review/player profile features (Step 600+)
