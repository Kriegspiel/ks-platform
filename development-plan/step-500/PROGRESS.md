# Step 500 Progress

Status: IN PROGRESS
Last Updated: 2026-03-27

## Slice Checklist

- [x] 510 Chess board component and visual-state primitives
- [x] 520 Game page polling loop + gameplay actions
- [x] 530 Phantom tray + client persistence
- [x] 540 Promotion modal + interaction polish
- [ ] 550 Home/rules/navigation polish

## Planning Packet Checklist

- [x] Slice folders 510/520/530/540/550 created
- [x] Per-slice README.md, IMPLEMENTATION.md, TESTING.md, CHECKLIST.md created
- [x] Scope rationale documented for 5-slice breakdown
- [x] Testing expectations include exact commands + expected pass/fail/skip semantics
- [x] Runtime smoke checks included for stateful UI flows

## Test Evidence

### Slice 510 (implemented in ks-v2 PR #40)
- PR: https://github.com/Kriegspiel/ks-v2/pull/40
- Merge commit (ks-v2/main): 3aac00f
- Automated checks:
  - cd frontend && npm run test -- --run ChessBoard → PASS (6 passed, 0 skipped)
  - cd frontend && npm run lint → PASS
  - Packet command cd frontend && npm run test -- --coverage --runInBand ChessBoard → BLOCKED (--runInBand not supported by Vitest)
  - Equivalent coverage run cd frontend && npm run test -- --run --coverage ChessBoard → PASS
- Runtime smoke (npm run dev -- --host 0.0.0.0 --port 4173) → BLOCKED on host Node v18 (crypto.hash is not a function; frontend engine expects Node >=20.19)
- Evidence logs stored in ks-v2/.evidence/step500-slice510-*

### Slice 520 (implemented in ks-v2 PR #41)
- PR: https://github.com/Kriegspiel/ks-v2/pull/41
- Merge commit (ks-v2/main): b552b5d
- Automated checks:
  - cd frontend && npm run test -- --run Game → PASS (4 passed, 0 skipped)
  - cd frontend && npm run test -- --run api → PASS (11 passed, 0 skipped)
  - cd frontend && npm run lint → PASS
  - cd frontend && npm run test:e2e -- --grep "game polling" → BLOCKED (Missing script: test:e2e)
  - Additional impacted suite: cd frontend && npm run test -- --run App Lobby Game api → PASS (28 passed, 0 skipped)
- Evidence log: ks-v2/.evidence/step500-slice520-frontend-gates.txt

### Slice 530 (implemented in ks-v2 PR #42)
- PR: https://github.com/Kriegspiel/ks-v2/pull/42
- Merge commit (ks-v2/main): 09f0470
- Automated checks:
  - cd frontend && npm run test -- --run usePhantoms → PASS (5 passed, 0 skipped)
  - cd frontend && npm run test -- --run PhantomTray → PASS (2 passed, 0 skipped)
  - cd frontend && npm run test -- --run GamePage PhantomTray usePhantoms → PASS (12 passed, 0 skipped)
  - cd frontend && npm run lint → PASS
  - cd frontend && npm run test:e2e -- --grep "phantom persistence" → BLOCKED (Missing script: test:e2e)

### Slice 540 (implemented in ks-v2 PR #43)
- PR: https://github.com/Kriegspiel/ks-v2/pull/43
- Merge commit (ks-v2/main): dff162c
- Automated checks:
  - cd frontend && npm run test -- --run PromotionModal → PASS (2 passed, 0 skipped)
  - Packet command cd frontend && npm run test -- --run Game --runInBand → BLOCKED (--runInBand not supported by Vitest)
  - Equivalent impacted suite: cd frontend && npm run test -- --run GamePage → PASS (8 passed, 0 skipped)
  - Additional impacted suite: cd frontend && npm run test -- --run ChessBoard → PASS (6 passed, 0 skipped)
  - cd frontend && npm run lint → PASS
  - cd frontend && npm run test:e2e -- --grep "promotion flow" → BLOCKED (Missing script: test:e2e)
- Evidence log: ks-v2/.evidence/step500-slice540-frontend-gates.txt

## Blockers

- Host runtime on rpi-server-02 uses Node 18, while frontend toolchain (Vite 7 / react-router 7) expects Node >=20.19. This blocks Step 510 runtime smoke and may impact interactive validation for Step 520.
- Slice 520/530/540 packet e2e gates remain blocked because frontend/package.json has no test:e2e script.

## Handoff

- Next execution order: 550.
- Carry forward UI-state contracts from 510 (orientation, highlightedSquares, phantomSquares, disabled, square click algebraic callback).
- Carry forward 520 contracts: game-state poll cadence/cleanup, possible-actions gating, and action re-poll behavior.
