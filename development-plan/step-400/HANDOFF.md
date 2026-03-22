# Step 400 Handoff Notes

## Purpose

Operator handoff companion for Step 400 gameplay-core execution.

## Current State

- Detailed planning packet exists for slices 410-460.
- No implementation code changed in this planning commit.

## Next Action

1. Start with `410/README.md`, then `410/IMPLEMENTATION.md`, then `410/TESTING.md`.
2. Preserve strict hidden-information semantics while implementing state APIs.
3. Keep clock/time accounting deterministic and testable before integration merge.

## Guardrails

- Engine state is source-of-truth; never trust client-provided board state.
- Move legality outcome visibility must not leak illegal/valid details to non-moving player.
- Poll response must only expose information allowed by current player perspective.
- Timeout handling must transition game to `completed` with explicit reason and recorded winner.
- Transcript/archive endpoints must enforce participant/public visibility boundaries.

## Evidence Protocol

For each slice, append:

- Branch/PR pointer (if applicable)
- Exact commands executed
- Outcome counts (pass/fail/skip)
- Any justified deviation from packet docs
