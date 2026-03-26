# Step 500 Progress

Status: IN PROGRESS
Last Updated: 2026-03-26

## Slice Checklist

- [x] `510` Chess board component and visual-state primitives
- [ ] `520` Game page polling loop + gameplay actions
- [ ] `530` Phantom tray + client persistence
- [ ] `540` Promotion modal + interaction polish
- [ ] `550` Home/rules/navigation polish

## Planning Packet Checklist

- [x] Slice folders `510/520/530/540/550` created
- [x] Per-slice `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, `CHECKLIST.md` created
- [x] Scope rationale documented for 5-slice breakdown
- [x] Testing expectations include exact commands + expected pass/fail/skip semantics
- [x] Runtime smoke checks included for stateful UI flows

## Test Evidence

### Slice 510 (implemented in `ks-v2` PR #40)
- PR: https://github.com/Kriegspiel/ks-v2/pull/40
- Merge commit (`ks-v2/main`): `3aac00f`
- Automated checks:
  - `cd frontend && npm run test -- --run ChessBoard` → PASS (6 passed, 0 skipped)
  - `cd frontend && npm run lint` → PASS
  - Packet command `cd frontend && npm run test -- --coverage --runInBand ChessBoard` → BLOCKED (`--runInBand` not supported by Vitest)
  - Equivalent coverage run `cd frontend && npm run test -- --run --coverage ChessBoard` → PASS
- Runtime smoke (`npm run dev -- --host 0.0.0.0 --port 4173`) → BLOCKED on host Node v18 (`crypto.hash is not a function`; frontend engine expects Node >=20.19)
- Evidence logs stored in `ks-v2/.evidence/step500-slice510-*`

## Blockers

- Host runtime on `rpi-server-02` uses Node 18, while frontend toolchain (Vite 7 / react-router 7) expects Node >=20.19. This blocks Step 510 runtime smoke and may impact interactive validation for Step 520.

## Handoff

- Next execution order: `520 -> 530 -> 540 -> 550`.
- Carry forward UI-state contracts from 510 (`orientation`, `highlightedSquares`, `phantomSquares`, `disabled`, square click algebraic callback).
