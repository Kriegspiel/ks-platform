# Step 540 - Promotion Modal and Interaction Polish

## Goal

Finalize promotion path and high-value game interaction feedback.

## Objective and Scope

- In scope: `PromotionModal`, promotion detection, suffix submission, cancel handling.
- In scope: last-move highlight, illegal-move feedback, waiting/loading/turn emphasis states.
- Out of scope: animation-heavy or non-MVP cosmetic work.

## Dependencies and Order

- Depends on 520 + 530.
- Feeds final UX quality before 550 handoff.

## Acceptance Criteria

- Promotion modal appears only on eligible pawn moves.
- Selected piece appends correct UCI suffix.
- Cancel resets pending move safely.
- Illegal/waiting/loading cues are visible and correct.
