# Slice 620 - Testing (Automated + Gates)

## Exact Commands

```bash
cd frontend && npm run test -- Review
cd frontend && npm run test -- ChessBoard
cd frontend && npm run test -- --runInBand --coverage src/pages/Review.jsx
cd frontend && npm run lint
cd src && pytest tests/test_game_routes.py -k moves -v
```

## Thresholds

- Review page test suite: 100% pass, zero snapshots pending
- Coverage on `Review.jsx`: >= 85% lines, >= 80% branches
- Keyboard navigation assertions for both left/right keys
- Lint: zero new errors in touched files

## CI Merge Gates

Must be green:
- frontend tests workflow
- frontend lint workflow
- backend route tests workflow

## Deterministic Fixtures

- Use fixed transcript fixtures with known FEN progression.
- No tests relying on wall clock or locale-specific date formatting.
- Pin key move transcripts for short and long games.

## Regression Matrix

- Transcript loads successfully
- First/Prev at ply 0 remains ply 0
- Next/Last caps at final ply
- Click move n jumps to expected board state
- Left/right keys mirror prev/next behavior
- Perspective toggle preserves current ply
- Empty/invalid transcript produces controlled error UI

## Skip Policy

Skips allowed only for missing frontend toolchain in runner.
Document skipped command + remediation and mark slice `BLOCKED` until rerun.

## Smoke / Rollback Checks

Smoke:
```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 4173
# open /game/<id>/review and verify replay controls manually
```

Rollback:
- Remove `/game/:gameId/review` route wiring from `App.jsx`
- Revert review page files and any route changes in `game.py`
- Re-run targeted tests for baseline confirmation
