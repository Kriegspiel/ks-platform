# Step 600 - Review and Player Features

## Goal

Implement post-game review plus the player-facing read features: profile, history, leaderboard, and settings.

## Read First

- [FRONTEND.md](../../FRONTEND.md)
- [API_SPEC.md](../../API_SPEC.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-500`

## Task Slices

- `600.1` Implement archive-backed game history and profile API reads.
- `600.2` Build profile, history, leaderboard, and settings pages.
- `600.3` Implement review/replay data flow and the review page UI.
- `600.4` Add pagination, settings persistence, and feature tests for these read flows.

## Required Tests Before Done

- Integration tests for history/profile/leaderboard/settings endpoints.
- Replay correctness tests.
- Page rendering smoke tests.

## Exit Criteria

- Users can view profiles, history, rankings, and settings.
- Completed games can be reviewed and replayed.
- Archive-backed reads behave correctly.

## Out of Scope

- TLS/deployment
- Backup/restore
- Final launch signoff
