# Step 600 Handoff Notes

## Purpose

Operator handoff companion for Step 600 (review + player-facing features) implementation.

## Current State (Planning Packet)

- Step 600 has been expanded into executable slices 610-650.
- Each slice now includes: `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, `CHECKLIST.md`.
- Testing docs include explicit commands, merge gates, deterministic fixtures, regression matrix, skip policy, and smoke/rollback checks.

## Execution Priority

1. **610 API foundation first** so downstream UI routes have stable contracts.
2. **620 review/replay next** to lock transcript + board replay behavior.
3. **630 player-facing pages** after APIs are validated.
4. **640 join URL flow** once lobby/game navigation is stable.
5. **650 integration suite** as final gate to prevent regression before Step 700 infra work.

## Quality Guardrails

- Preserve hidden-information rules in replay/player views.
- No schema drift: responses must match existing API spec names/types.
- Pagination semantics must stay consistent across profile history + leaderboard.
- Settings writes must be authenticated and idempotent.
- Join flow must fail safely (invalid/full game) with deterministic UX.

## Handoff to Step 700

Step 700 should assume Step 600 delivered:
- Stable user/profile/history/leaderboard endpoints
- Review page route and move replay reliability
- Regression coverage in `test_player_features.py`

Step 700 can then focus on infra (compose/nginx/ci/ops) without reworking feature behavior.
