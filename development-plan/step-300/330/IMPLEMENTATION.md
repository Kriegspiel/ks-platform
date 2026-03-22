# Step 330 - Authenticated Game API Surface - Implementation Plan

## Objective

Add production-shaped game lifecycle routes using existing auth/session dependency patterns from Step 200.

## Delivery Sequence

1. Scaffold router module with endpoint signatures + response DTO usage.
2. Wire all endpoints to `GameService` calls and map domain exceptions to HTTP responses.
3. Register router in app bootstrap (`main.py`).
4. Add API tests for auth gating + happy/failure paths.
5. Execute required checks and record evidence in progress tracker.

## Engineering Notes

- Keep route handlers thin; business logic stays in service layer.
- Maintain stable response keys to avoid frontend thrash in slice 340.
- Reuse standardized error formatter/helpers already used by auth routes.
- Avoid introducing move/board payload overfetch in `GET /api/game/{id}` during this slice.

## Definition of Done

- All acceptance criteria met and tested.
- No unauthenticated lifecycle access paths remain.
- Progress evidence updated with exact command outcomes.
