# Step 450 - Transcript/Archive/Recent-Game Read APIs - Implementation Plan

## Objective

Build retrieval endpoints/services for gameplay history while preserving visibility constraints.

## Delivery Sequence

1. Implement service helper `get_game_or_archive` with clear precedence + null handling.
2. Add transcript route with active/completed + participant/public policy checks.
3. Add recent-completed route with limit/default cap and stable ordering.
4. Add tests for active/archived lookup and permission matrix.
5. Execute required checks; document outcomes in `step-400/PROGRESS.md`.

## Engineering Notes

- Keep response schemas consistent regardless of active/archive source.
- Clamp client-provided limits to a safe upper bound.
- Avoid loading full engine payload for recent list if summary fields suffice.

## Definition of Done

- Acceptance criteria met.
- All `TESTING.md` commands pass.
- Progress evidence logged.
