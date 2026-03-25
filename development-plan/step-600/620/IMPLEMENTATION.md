# Slice 620 - Implementation Plan

## Required Behaviors

- Load transcript from `GET /api/game/{gameId}/moves`
- Render non-interactive board from reconstructed state at selected ply
- Controls: first/prev/next/last and arrow key mapping
- Perspective selector:
  - Referee: full board
  - White: white-only view
  - Black: black-only view
- Move list supports direct jump
- Display game result summary footer

## Constraints

- No move submission on this page
- Replay must be deterministic from transcript
- Avoid shared mutable board state between plies
