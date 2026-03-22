# Step 320 - GameService Lifecycle Operations - Implementation Plan

## Objective

Build deterministic lifecycle transition logic in service layer with explicit guardrails and stable return contracts.

## Delivery Sequence

1. Define service-level error taxonomy for 404/409/403/400 style failures.
2. Implement create/join paths first, then retrieval helpers, then resign/delete mutations.
3. Add tests for happy paths and state/ownership denial paths.
4. Confirm sort/limit semantics for open and mine listings.
5. Run required tests and update `step-300/PROGRESS.md` evidence.

## Engineering Notes

- Keep write operations atomic where feasible (`find_one_and_update` with state preconditions).
- Preserve timezone-aware timestamps in UTC.
- Avoid leaking Mongo ObjectId internals into service contracts unexpectedly.
- Keep random color assignment deterministic-testable (injectable RNG helper).

## Definition of Done

- All acceptance criteria satisfied and tested.
- Testing gate commands pass as documented.
- Slice status and evidence captured in progress file.
