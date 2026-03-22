# Step 420 - Move/Ask-Any/Resign Gameplay Execution API

## Goal

Implement authenticated gameplay mutation endpoints that enforce turn/state rules and persist engine outcomes.

## Objective and Scope

- In scope: `POST /api/game/{id}/move`, `POST /api/game/{id}/ask-any`, and gameplay-aware resign flow.
- In scope: service-layer orchestration for move append, state persistence, turn transitions, and terminal-state completion hooks.
- Out of scope: polling projection response design (430), clock decrement/timeout calculation internals (440), transcript/recent-game read APIs (450).

## Dependencies and Order

- Depends on: 410 adapter primitives.
- Blocks: 430, 440, 450, 460.
- Requires Step 300 auth + participation guards already stable.

## Backend/Frontend/Data/API Impacts

- Backend: router + service mutation path for gameplay actions.
- Frontend: no UI work yet, but API contracts consumed by upcoming gameplay page integrations.
- Data: updates `games.moves`, `engine_state`, `turn`, `state`, and terminal result metadata.
- API: introduces/locks move/ask-any response shape and error semantics for illegal/out-of-turn actions.

## Acceptance Criteria

- Legal move persists engine state update and move record.
- Illegal move returns deterministic non-terminal response without corrupting persisted state.
- Out-of-turn and non-participant mutation attempts are rejected by contract.
- Ask-any requests record result without leaking hidden move data.
- Resign transitions game to `completed` with winner/reason set.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
