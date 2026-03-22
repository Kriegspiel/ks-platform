# Step 410 - Engine Adapter + Deterministic Serialization

## Goal

Establish a single backend adapter for Berkeley Kriegspiel engine operations so later slices consume stable, testable primitives.

## Objective and Scope

- In scope: engine wrapper service for game creation, move attempt, ask-any attempt, full/visible FEN projections, serialize/deserialize helpers.
- In scope: unit tests for legal/illegal moves, ask-any behavior, and serialization round-trip integrity.
- Out of scope: HTTP routes, auth checks, persistent game lifecycle updates, clock logic.

## Dependencies and Order

- Depends on: Step 300 completed data contracts.
- Blocks: 420, 430, 440, 450, 460.
- Must land first to avoid duplicated engine-call logic in routers/services.

## Backend/Frontend/Data/API Impacts

- Backend: new `engine_adapter` service APIs and focused tests.
- Frontend: none.
- Data: defines serialized engine payload shape expected in game records.
- API: no direct route changes, but establishes response fragments consumed by later endpoints.

## Acceptance Criteria

- Adapter creates valid new game state.
- Legal move attempt returns `move_done=true`; illegal move returns `move_done=false` with proper announcement classification.
- Visible-board projection hides opponent pieces for a given color.
- Serialize + deserialize round-trip preserves board/move state.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
