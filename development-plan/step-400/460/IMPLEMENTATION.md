# Step 460 - Gameplay Integration + Regression Hardening - Implementation Plan

## Objective

Create deterministic integration coverage proving Step 400 gameplay contracts are production-ready for Step 500 UI work.

## Delivery Sequence

1. Build/extend integration fixtures for two-player active game scenarios.
2. Add lifecycle tests: legal move, illegal move, out-of-turn denial, ask-any, resign, timeout.
3. Add polling tests validating hidden-information projections and action availability.
4. Add archive/recent/transcript checks for post-completion behavior.
5. Run full targeted gameplay suite and quality gates.
6. Update `step-400/PROGRESS.md` with pass/fail/skip counts and key artifacts.

## Engineering Notes

- Keep tests deterministic: no sleeping-based timing where fake time controls can be used.
- Fail fast on data-leak assertions (hidden info leaks are release blockers).
- No production-code churn unless needed to fix failing contractual behavior.

## Definition of Done

- Acceptance criteria satisfied.
- Required test/lint/format commands pass.
- Step-level progress evidence supports marking Step 400 `DONE` once all slices complete.
