# Step 800 - Hardening and Launch Readiness

## Goal

Perform the final MVP hardening pass: regression testing, security/error-path checks, documentation cleanup, and launch checklist signoff.

## Read First

- [README.md](../../README.md)
- [AUTH.md](../../AUTH.md)
- [INFRA.md](../../INFRA.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-700`

## Task Slices

- `800.1` Run the full regression suite and close critical failures.
- `800.2` Exercise security-sensitive flows, error paths, and rate-limited behavior.
- `800.3` Clean up setup docs, developer docs, and operational docs based on actual implementation.
- `800.4` Complete the MVP launch checklist and record residual risks.

## Required Tests Before Done

- Full automated test suite.
- Manual acceptance pass against MVP acceptance criteria.
- Security/error-path checks for auth, gameplay, and reconnect flows.

## Exit Criteria

- MVP acceptance criteria are verified against the real implementation.
- Critical regressions are resolved.
- Docs match reality closely enough for handoff and operation.
- Remaining risks are documented explicitly.

## Out of Scope

- Phase 2 implementation
- New features outside MVP acceptance criteria
