# Step 800 - Hardening and Launch Readiness

## Goal

Final MVP hardening: regression testing, security checks, error path testing, documentation, launch checklist.

## Read First

- [README.md](../../README.md)
- [AUTH.md](../../AUTH.md)
- [INFRA.md](../../INFRA.md)

## Depends On

- `step-700`

## Task Slices

### 810 — Full Regression Suite

**Actions:**

- Run full test suite: `cd src && pytest tests/ --cov=app --cov-report=term-missing -v`
- Fix any failures
- Write tests for untested critical paths:
  - Auth edge cases: expired session, concurrent login
  - Game lifecycle edge cases: join race condition, double resign
  - Clock edge cases: timeout at 0, increment overflow
  - Polling edge cases: poll completed game, poll as non-participant
- Target: >80% code coverage

**Acceptance criteria:**
- Full suite passes with 0 failures
- Coverage >80%
- Results recorded in step PROGRESS.md

---

### 820 — Security Audit

**Test each manually or with scripts:**

- **Auth:**
  - `HttpOnly`, `SameSite=Lax` on session cookie
  - Passwords hashed with bcrypt (not plaintext)
  - Expired sessions return 401
  - Rate limiting on `/auth/login` (if NGINX is configured)
- **Game security:**
  - Non-participant can't poll game state (403)
  - Player can't see opponent's pieces (FEN filtering)
  - Phantom pieces never sent to server
  - Can't move when it's not your turn
- **Information leakage:**
  - Error responses don't include stack traces in production
  - No sensitive data in logs
- **Input validation:**
  - Malformed UCI strings handled gracefully
  - Oversized request bodies rejected
  - Invalid game codes / user IDs handled

**Acceptance criteria:**
- All security checks pass
- No information leakage found
- Findings recorded in step PROGRESS.md

---

### 830 — Error Path Testing

**Test each scenario:**

- MongoDB goes down → /health returns 503, game operations fail gracefully
- Poll a game that was just completed → returns completed state, not error
- Two players try to join the same game simultaneously → one succeeds, one gets 409
- Very long game (>500 moves) → no performance issues
- Invalid session cookie → 401, not 500
- Move on completed game → appropriate error
- Frontend handles API errors gracefully (shows message, doesn't crash)

**Acceptance criteria:**
- All error paths return proper error codes (not 500)
- Game state remains consistent after errors
- Frontend doesn't crash on API errors
- Results recorded in step PROGRESS.md

---

### 840 — Documentation Cleanup

**Modify/create these files:**

- `README.md` — update to reflect actual implementation:
  - Quick start (clone, .env, docker compose up)
  - Local dev setup (backend: uvicorn, frontend: npm run dev)
  - Running tests
  - Project structure
  - Architecture decisions (React, MongoDB, polling)
- `docs/DEPLOYMENT.md` — operator guide:
  - VPS provisioning (firewall, SSH, Docker)
  - DNS setup
  - First deploy
  - TLS with certbot
  - Backup cron setup
  - Monitoring (/health)
  - Troubleshooting
- Note in spec docs where implementation diverges (React instead of Jinja2, polling instead of WebSocket, simplified lifecycle)

**Acceptance criteria:**
- New developer can set up and run the project from README.md
- Operator can deploy from docs/DEPLOYMENT.md
- Divergences from spec docs are documented

---

### 850 — Launch Checklist Signoff

**Create this file:**

- `docs/LAUNCH_CHECKLIST.md`:
  - [ ] All tests pass
  - [ ] Docker Compose starts on fresh clone
  - [ ] Health endpoint returns 200
  - [ ] Register → login → create → join → play → resign works end-to-end
  - [ ] Phantom pieces work (desktop + mobile)
  - [ ] Promotion modal works
  - [ ] Clock ticks correctly
  - [ ] Review page replays games correctly
  - [ ] Leaderboard shows ranked players
  - [ ] Settings persist
  - [ ] Hidden info preserved (can't see opponent pieces)
  - [ ] Rate limiting works
  - [ ] Structured logs in production
  - [ ] Backup script works
  - [ ] TLS works (https://kriegspiel.org)
  - Residual risks documented
  - Phase 2 deferrals listed

**Acceptance criteria:**
- Every item verified and checked off (or documented as deferred)
- Platform ready for soft launch

---

## Exit Criteria

- MVP acceptance criteria verified
- Critical regressions resolved
- Docs match reality
- Risks documented

## Out of Scope

- Phase 2 (WebSocket upgrade, OAuth, spectators, tournaments)
