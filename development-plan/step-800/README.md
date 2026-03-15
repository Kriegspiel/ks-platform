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

### 810 — Full Regression Suite

**Actions:**

- Run the complete test suite: `cd src && pytest tests/ --cov=app --cov-report=term-missing -v`
- Fix any failing tests
- Identify and write tests for any untested critical paths:
  - Auth edge cases: expired session, concurrent login, session sliding
  - Game lifecycle edge cases: join race condition, resign during pause, double resign
  - WebSocket edge cases: message during reconnect, malformed messages, oversized messages
  - Clock edge cases: timeout at exact 0, increment overflow
- Target: >80% code coverage on `app/` package

**Acceptance criteria:**
- Full test suite passes with 0 failures
- Coverage report shows >80% line coverage
- No critical paths are untested
- Test results are recorded in step PROGRESS.md

---

### 820 — Security Audit

**Actions — test each manually or with scripts:**

- **Auth flows:**
  - Verify `HttpOnly`, `Secure` (in prod), `SameSite=Lax` on session cookie
  - Verify CSRF token is required on all POST/PATCH/DELETE routes
  - Verify password is hashed with bcrypt (not stored in plaintext or weak hash)
  - Verify expired sessions return 401 (not stale data)
  - Verify rate limiting on `/auth/login` (5/min) and `/auth/register` (3/min)
- **WebSocket security:**
  - Verify Origin header validation on cookie-authenticated WebSocket connections
  - Verify non-participant cannot connect to game WebSocket
  - Verify game state is not leaked (opponent pieces never sent)
  - Verify WebSocket close codes are correct (1008, 4002, 4003)
- **Information leakage:**
  - Verify error responses don't include stack traces in production mode
  - Verify no sensitive data in logs (passwords, tokens, session IDs)
  - Verify phantom pieces are never sent to/from the server
- **Input validation:**
  - Test oversized payloads (>64KB WebSocket messages rejected)
  - Test malformed UCI strings
  - Test SQL/NoSQL injection patterns in username, game_code fields

**Acceptance criteria:**
- All security checks pass
- No information leakage found
- Rate limiting works as configured
- Findings and evidence recorded in step PROGRESS.md

---

### 830 — Error Path Testing

**Actions — test each scenario:**

- **Network failures:**
  - MongoDB goes down during gameplay → health endpoint returns 503, games pause gracefully
  - WebSocket disconnect during move processing → move is not lost, game state is consistent
  - Client reconnect after server restart → game state is restored from MongoDB
- **Game edge cases:**
  - Both players disconnect simultaneously → game pauses, then abandons after 15 min
  - Player sends move when it's not their turn → error response, game state unchanged
  - Player tries to join a game that just filled → 409, not 500
  - Very long game (>500 moves) → no performance degradation
- **Concurrency:**
  - Two players make moves at the same time → only the correct turn's move succeeds
  - Multiple WebSocket connections from same user → only latest is active

**Acceptance criteria:**
- All error paths return appropriate error codes (not 500)
- Game state remains consistent after error scenarios
- No data corruption from edge cases
- Results recorded in step PROGRESS.md

---

### 840 — Documentation Cleanup

**Modify/create these files:**

- `README.md` — update to reflect actual implementation:
  - Quick start guide (clone, .env, docker compose up)
  - Local development setup (without Docker)
  - Running tests
  - Project structure overview
  - Links to spec docs
- `docs/DEPLOYMENT.md` — create operator deployment guide:
  - VPS provisioning checklist (firewall, SSH, Docker)
  - DNS setup
  - First deploy steps
  - TLS certificate setup with certbot
  - Updating / redeploying
  - Backup setup (cron job for backup.sh)
  - Monitoring setup (uptime service pointing at /health)
  - Troubleshooting common issues
- Review and update all spec docs (ARCHITECTURE.md, API_SPEC.md, etc.) for any divergence from actual implementation
  - Remove or mark Phase 2 items clearly
  - Fix any incorrect examples or outdated details

**Acceptance criteria:**
- A new developer can clone, set up, and run the project using only README.md
- An operator can deploy to a VPS using docs/DEPLOYMENT.md
- Spec docs match the actual implementation (no misleading info)

---

### 850 — Launch Checklist Signoff

**Create this file:**

- `docs/LAUNCH_CHECKLIST.md` — comprehensive launch checklist:

  **Pre-launch:**
  - [ ] All tests pass (`pytest tests/ -v`)
  - [ ] Docker Compose starts cleanly on fresh clone
  - [ ] Health endpoint returns 200
  - [ ] Registration → login → create game → join game → play moves → resign works end-to-end
  - [ ] Phantom pieces work on desktop and mobile
  - [ ] Promotion modal works
  - [ ] Clock ticks correctly
  - [ ] Reconnection works (close tab, reopen)
  - [ ] Review page shows completed game correctly
  - [ ] Leaderboard shows ranked players
  - [ ] Settings page saves preferences
  - [ ] CSRF protection works (POST without token → 403)
  - [ ] Rate limiting works (rapid login attempts → 429)
  - [ ] Structured logs in production mode
  - [ ] Backup script runs successfully
  - [ ] SSL/TLS works (https://kriegspiel.org)
  - [ ] www redirects to bare domain

  **Residual risks:**
  - Document any known issues, missing features, or technical debt
  - Note Phase 2 items that were deferred
  - List any manual operational steps needed

**Acceptance criteria:**
- Every checklist item is verified and checked off (or explicitly documented as deferred)
- Residual risks are documented
- The platform is ready for soft launch to initial users

---

## Required Tests Before Done

- Full automated test suite passes
- Manual acceptance pass against MVP acceptance criteria
- Security/error-path checks for auth, gameplay, and reconnect flows

## Exit Criteria

- MVP acceptance criteria are verified against the real implementation
- Critical regressions are resolved
- Docs match reality closely enough for handoff and operation
- Remaining risks are documented explicitly

## Out of Scope

- Phase 2 implementation
- New features outside MVP acceptance criteria
