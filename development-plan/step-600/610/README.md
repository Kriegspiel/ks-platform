# Slice 610 - Profile, History, Leaderboard API

## Objective

Deliver user-facing read/update API endpoints for profile, game history, settings, and leaderboard with strict pagination/filtering behavior.

## Scope

- Router work in `src/app/routers/user.py`
- Service methods in `src/app/services/user_service.py`
- Router wiring in `src/app/main.py`
- No frontend implementation in this slice

## Dependencies

- Step 500 complete
- Existing auth/session dependencies available
- `game_archives` and user stats collections populated in fixtures

## Deliverables

- New/updated API endpoints exactly as declared in Step 600 README
- Validation and auth handling for settings endpoint
- Pagination semantics documented and tested
