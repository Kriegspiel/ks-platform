# Step 340 - Frontend Lobby UX and Polling Flows - Implementation Plan

## Objective

Implement user-facing lobby workflows and integrate them cleanly with authenticated backend APIs.

## Delivery Sequence

1. Extend API client with typed-ish helper methods for game endpoints.
2. Build Lobby page sections in order: create, join, open list, mine list.
3. Add polling loops with controlled intervals and cleanup guards.
4. Wire `/lobby` route and auth guard behavior in app routing.
5. Add/update frontend tests and run required command gates.

## Engineering Notes

- Keep polling intervals practical: waiting-game status ~3s, open list ~5s, mine list ~10s.
- Prevent duplicate interval timers across rerenders (use stable effects + cleanup).
- Surface server error messages without exposing raw stack traces.
- Use optimistic UI only where rollback behavior is explicit and tested.

## Definition of Done

- Acceptance criteria satisfied across create/join/list flows.
- Required test/lint/format commands pass.
- Slice evidence captured in `step-300/PROGRESS.md`.
