# Slice 650 - Implementation Plan

## Required Test Cases

- Existing profile returns expected payload
- Missing profile returns 404
- Game history paginates correctly
- Out-of-range pagination returns empty with stable total
- `per_page` clamped to max 100
- Leaderboard ordering + min games filter
- Settings patch requires auth (401 when missing)
- Settings patch persists on authenticated request
- Completed game moves transcript returns expected data shape

## Constraints

- Tests must be independent and order-safe
- Use deterministic dataset setup/teardown
- Avoid broad sleeps/time-based assertions
