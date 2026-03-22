# Step 450 - Transcript/Archive/Recent-Game Read APIs

## Goal

Expose gameplay history endpoints with correct participant/public visibility and archive fallback behavior.

## Objective and Scope

- In scope: transcript endpoint for active/completed games with participant/public access rules.
- In scope: recent-completed endpoint from archives for homepage/lobby use.
- In scope: service helper to retrieve game from active or archive collection.
- Out of scope: gameplay mutation flow and clock internals.

## Dependencies and Order

- Depends on: 420 completion flow and archival writes.
- Parallel-friendly with late-stage 440 validation, but should finish before 460 integration tests.

## Backend/Frontend/Data/API Impacts

- Backend: route + service read helpers for current/archived games.
- Frontend: enables recent-games and completed-game transcript views in later UI slices.
- Data: reads from `games` and `game_archives` with deterministic sort + limit rules.
- API: introduces transcript/recent payload contracts with explicit authorization behavior.

## Acceptance Criteria

- Participants can fetch transcript for active or completed games.
- Non-participants can fetch transcript only for completed/publicly eligible games.
- Recent endpoint returns last N completed games in descending completion time.
- Archive lookup gracefully falls back when game no longer in active collection.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
