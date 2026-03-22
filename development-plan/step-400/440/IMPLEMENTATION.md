# Step 440 - Clock Service + Timeout Adjudication - Implementation Plan

## Objective

Deliver deterministic, testable server clock behavior for active gameplay.

## Delivery Sequence

1. Define clock persistence fields and defaults for active games.
2. Implement clock service (`get_remaining`, `deduct_and_increment`, `check_timeout`).
3. Integrate service calls into move execution flow.
4. Integrate current clock projection into polling response.
5. Add deterministic tests using frozen/monkeypatched time to avoid flake.
6. Record results in `step-400/PROGRESS.md`.

## Engineering Notes

- Avoid relying on client timestamps.
- Keep time unit conventions explicit (seconds with decimals or integer milliseconds).
- Ensure timeout and non-timeout terminal states remain distinguishable in result metadata.

## Definition of Done

- Acceptance criteria satisfied.
- Testing commands in `TESTING.md` pass.
- Progress evidence recorded.
