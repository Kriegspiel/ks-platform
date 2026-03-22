# Step 400 - Gameplay Core

## Goal

Deliver production-shaped gameplay core across backend + frontend integration surfaces: engine adapter, move/ask-any execution, hidden-information polling, clock/timeouts, and gameplay-level integration verification.

## Read First

- [GAME_ENGINE.md](../../GAME_ENGINE.md)
- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [FRONTEND.md](../../FRONTEND.md)
- [development-plan/README.md](../README.md)
- [development-plan/PLAN.md](../PLAN.md)

## Depends On

- `step-300` (DONE before implementation start)

## Scope Decision: 6 Slices (Not 5)

Step 400 has two high-risk seams that were previously bundled together: (1) engine state mutation + move legality handling and (2) hidden-information polling + server clock math. Keeping those in one slice creates wide blast radius and unclear failure ownership.

We split Step 400 into **6 slices** so each seam has a deterministic validation gate:

1. `410` engine adapter + serialization primitives
2. `420` move/ask-any/resign execution API + service orchestration
3. `430` polling state API + hidden-information response shaping
4. `440` server clock lifecycle + timeout completion integration
5. `450` gameplay transcript/archive/read APIs
6. `460` integration/regression verification for complete gameplay loop

This count keeps each slice implementable in one focused execution session while preserving clear dependency order and narrow rollback scope.

## Gameplay Contract (Locked for MVP)

Step 400 must enforce:

- Lifecycle remains `waiting -> active -> completed` (no pause/reconnect state machine here)
- Transport remains polling (no WebSocket in MVP)
- Hidden information remains strict (player sees only own-board view + referee announcements allowed by rules)
- Move execution is authoritative server-side using Berkeley Kriegspiel engine wrapper

## Slice Packets

Each slice has a detailed implementation packet:

- [410 - Engine adapter + deterministic state serialization](./410/README.md)
- [420 - Move/ask-any/resign gameplay execution endpoints](./420/README.md)
- [430 - Polling game-state endpoint + hidden-information projections](./430/README.md)
- [440 - Clock service, timeout adjudication, and move-time accounting](./440/README.md)
- [450 - Transcript/archive/recent-game read APIs](./450/README.md)
- [460 - Gameplay integration + regression hardening test suite](./460/README.md)

Every slice folder contains:

- `README.md` (scope contract)
- `IMPLEMENTATION.md` (execution-level build plan)
- `TESTING.md` (exact commands + expected outcomes)
- `CHECKLIST.md` (operator checklist)

## Exit Criteria

- Two authenticated users can complete a game via API-driven flow: join, move, ask-any, resign/finish.
- Move legality and hidden-information behavior are enforced by backend contracts.
- Polling endpoint returns correct player-specific state and allowed actions.
- Clock state is server-calculated, decrements over time, and can trigger timeout completion.
- Transcript/recent-game endpoints cover active/archived access rules.
- Step-400 progress docs contain exact command evidence for each completed slice.

## Out of Scope

- Rich board interaction UI and piece-drag UX (Step 500)
- WebSocket transport
- Reconnect recovery protocol
- Advanced adjudication/exotic variants beyond current engine contract
