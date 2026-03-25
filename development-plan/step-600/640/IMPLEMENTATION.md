# Slice 640 - Implementation Plan

## Required Behaviors

- On mount of `Join.jsx`, call `POST /api/game/join/{gameCode}`
- Success -> redirect to `/game/{gameId}`
- Not logged in -> redirect `/auth/login` preserving return path
- Failure (`404`, full game, invalid) -> actionable error message + link to `/lobby`
- Lobby create-game flow displays shareable join URL

## Constraints

- Avoid duplicate join requests on rerender
- Do not leak backend internal error details in UI
