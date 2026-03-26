# Step 800 - Hardening and Launch Readiness

## Goal

Drive the MVP from "feature complete" to "safe-to-launch" with deterministic regression gates, security hardening verification, resilient failure-path behavior, operator-facing docs, and a signed launch readiness checklist.

Step 800 is the final quality barrier before soft launch.

## Read First

- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [AUTH.md](../../AUTH.md)
- [INFRA.md](../../INFRA.md)
- [development-plan/PLAN.md](../PLAN.md)
- [development-plan/step-700/HANDOFF.md](../step-700/HANDOFF.md)

## Depends On

- `step-700`

## Scope-Based Slices

### 810 — Regression Gate Hardening
- Unify backend, frontend, and integration tests under reproducible command wrappers
- Enforce coverage, flaky-test retry, and deterministic seed policy
- Build regression matrix for auth, lobby, gameplay, review, and infra-adjacent paths
- Produce CI gate mapping for merge protection

### 820 — Security Verification and Abuse-Path Coverage
- Validate session/cookie/auth controls and request hardening
- Verify hidden-information guarantees and authorization boundaries
- Add explicit checks for information leakage, logging redaction, and payload constraints
- Define security merge gates with evidence artifacts

### 830 — Failure and Recovery Behavior Certification
- Stress API/application behavior under dependency outages and race conditions
- Verify frontend error UX behavior and non-crashing boundaries
- Add deterministic chaos-style fixtures for DB/app disruption scenarios
- Require rollback-safe recovery checks and post-recovery invariants

### 840 — Documentation and Runbook Reconciliation
- Align root docs with actual implementation and launch sequence
- Reconcile operator deployment/runbook with Step 700 infra contracts
- Add explicit divergence notes between specs and implementation
- Gate documentation quality with command-validity and fresh-clone checks

### 850 — Launch Readiness Signoff and Rollback Drill
- Build launch checklist with hard PASS criteria and owners
- Require pre-launch smoke + post-deploy smoke + rollback drill
- Codify go/no-go decision policy and residual-risk logging
- Define release evidence bundle required for soft launch approval

## Exit Criteria

- All slices `810`-`850` completed with evidence and no unresolved critical defects
- CI merge gates enforce required hardening/security/regression checks
- Docs and runbooks match current implementation and deployment topology
- Launch checklist is signed with explicit go/no-go decision and rollback viability

## Out of Scope

- Phase-2 feature roadmap (WebSocket migration, OAuth, spectator mode, tournaments)
- Multi-region high-availability architecture
- Non-MVP platform re-architecture
