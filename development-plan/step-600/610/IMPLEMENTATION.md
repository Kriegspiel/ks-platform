# Slice 610 - Implementation Plan

## Files

- `src/app/routers/user.py`
- `src/app/services/user_service.py`
- `src/app/main.py`
- (optional) shared schemas for response typing if project already uses them

## Required Behaviors

1. `GET /api/user/{username}`
   - Return: username, profile, stats, member_since
   - 404 on missing user
2. `GET /api/user/{username}/games`
   - Query: `page` default 1, `per_page` default 20, max 100
   - Return deterministic ordering (newest first) + total count
3. `PATCH /api/user/settings`
   - Requires auth
   - Persist and return settings payload
4. `GET /api/leaderboard`
   - Filter to `status=active` and `games_played >= 5`
   - Sort ELO descending, stable tiebreaker (username asc)
   - Return rank + pagination metadata

## Non-Goals

- UI wiring
- replay rendering
