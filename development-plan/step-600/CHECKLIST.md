# Step 600 Master Checklist

## Before Starting Any Slice

- [ ] Read `development-plan/README.md`
- [ ] Read `development-plan/PLAN.md`
- [ ] Read `development-plan/step-600/README.md`
- [ ] Read `development-plan/step-600/PROGRESS.md`
- [ ] Confirm Step 500 exit criteria are met in codebase/tests
- [ ] Claim target slice in `development-plan/step-600/PROGRESS.md`

## Required Execution Order

- [ ] Slice 610
- [ ] Slice 620
- [ ] Slice 630
- [ ] Slice 640
- [ ] Slice 650

## Slice Completion Gate (repeat for each slice)

- [ ] Scope implemented exactly as in slice `IMPLEMENTATION.md`
- [ ] All commands in slice `TESTING.md` executed and logged
- [ ] Thresholds/coverage/perf gates satisfied
- [ ] CI merge gates are green for impacted lanes
- [ ] Deterministic fixtures used (no non-deterministic seeds/time)
- [ ] Regression matrix rows marked PASS/WAIVED with reason
- [ ] Skip policy honored and documented for any skipped check
- [ ] Smoke and rollback checks completed
- [ ] Slice marked done in `step-600/PROGRESS.md`

## Step Completion Gate

- [ ] Slices 610-650 all complete
- [ ] Step status set to `DONE` in `step-600/PROGRESS.md`
- [ ] Top-level `development-plan/PROGRESS.md` updated
- [ ] Step 700 kickoff notes added to `step-600/HANDOFF.md`
