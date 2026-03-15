# Step 400 - Real-Time Gameplay Core

## Goal

Implement the authoritative gameplay loop over WebSockets, including engine integration, hidden-information responses, clocks, reconnect, and abandon handling.

## Read First

- [GAME_ENGINE.md](../../GAME_ENGINE.md)
- [API_SPEC.md](../../API_SPEC.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [AUTH.md](../../AUTH.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)

## Depends On

- `step-300`

## Task Slices

- `400.1` Implement WebSocket authentication, connection management, heartbeat, and reconnect/pause transitions.
- `400.2` Implement move, ask-any, resign, and game-over flows backed by the `kriegspiel` engine.
- `400.3` Implement clock state, timeout handling, and persistence updates.
- `400.4` Add archive/write-through/cache behavior and exhaustive gameplay tests.

## Required Tests Before Done

- WebSocket integration tests for connect/move/ask-any/resign/game-over.
- Illegal move and hidden-information payload tests.
- Reconnect/pause/abandon tests.
- Clock timeout tests.

## Exit Criteria

- Two players can play a full game over WebSockets.
- Payloads preserve imperfect information correctly.
- Reconnect and timeout behavior works.
- Gameplay tests cover the main referee cases.

## Out of Scope

- Final UI polish
- Profile/history/leaderboard pages
- Production deployment work
