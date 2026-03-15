# Step 300 - Lobby and Game Lifecycle REST

## Goal

Implement the non-WebSocket game lifecycle: create, join, list, mine, resign, and waiting-game expiry behavior.

## Read First

- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [GAME_ENGINE.md](../../GAME_ENGINE.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-200`

## Task Slices

- `300.1` Implement game creation, join codes, waiting-game expiry, and state transitions in the service layer.
- `300.2` Implement REST endpoints for create/join/open/mine/resign and metadata reads.
- `300.3` Build the minimal lobby page flow with HTMX-backed create/join/open-games behavior.
- `300.4` Add archive-aware reads needed for future profile/review work where appropriate.

## Required Tests Before Done

- Service tests for create/join/resign/state transitions.
- Integration tests for REST endpoints.
- Expiry handling tests for waiting games.

## Exit Criteria

- A logged-in user can create a game, share a join code, and another user can join it.
- Waiting games expire correctly.
- Open-games and my-games reads work.
- Lobby flow is usable without WebSocket gameplay yet.

## Out of Scope

- Move execution
- Reconnect logic
- Player board UX beyond minimal lobby flow
