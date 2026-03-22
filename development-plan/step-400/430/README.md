# Step 430 - Polling Game-State API + Hidden-Information Projection

## Goal

Provide a polling endpoint that returns player-scoped game state without leaking opponent-only information.

## Objective and Scope

- In scope: `GET /api/game/{id}/state` response model with player-specific board view, allowed actions, result/status, and referee-visible announcements.
- In scope: participant authorization and projection helpers that map persisted game state to player-visible payload.
- Out of scope: clock math implementation details (440), transcript/recent-game endpoints (450).

## Dependencies and Order

- Depends on: 410 adapter + 420 mutation flow.
- Blocks: 440 (clock fields wiring), 450, 460.

## Backend/Frontend/Data/API Impacts

- Backend: new read endpoint + response projection logic.
- Frontend: establishes polling payload contract for gameplay page consumers.
- Data: reads `engine_state`, `moves`, lifecycle/result fields; no schema expansion required.
- API: locks hidden-information-safe state response shape.

## Acceptance Criteria

- Participants receive `your_fen` projection containing only own pieces.
- Response includes deterministic `possible_actions` based on turn + game state.
- Referee log includes allowed announcements without move-coordinate leakage.
- Non-participants are rejected.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
