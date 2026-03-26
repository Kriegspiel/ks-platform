# Step 700 Master Checklist

## Before Starting Any Slice

- [ ] Read `development-plan/README.md`
- [ ] Read `development-plan/PLAN.md`
- [ ] Read `development-plan/step-700/README.md`
- [ ] Read `development-plan/step-700/PROGRESS.md`
- [ ] Confirm Step 600 implementation handoff assumptions are true in codebase
- [ ] Claim target slice in `development-plan/step-700/PROGRESS.md`

## Required Execution Order

- [ ] Slice 710
- [ ] Slice 720
- [ ] Slice 730
- [ ] Slice 740
- [ ] Slice 750

## Slice Completion Gate (repeat for each slice)

- [ ] Scope implemented exactly as in slice `IMPLEMENTATION.md`
- [ ] All commands in slice `TESTING.md` executed and logged
- [ ] Thresholds/coverage/performance gates satisfied
- [ ] CI merge gates are green for impacted lanes
- [ ] Deterministic fixtures/seeding constraints honored
- [ ] Regression matrix rows marked PASS/WAIVED with evidence
- [ ] Skip policy honored and documented for any skipped check
- [ ] Post-deploy smoke checks passed
- [ ] Rollback validation executed and documented
- [ ] Slice marked done in `step-700/PROGRESS.md`

## Step Completion Gate

- [ ] Slices 710-750 all complete
- [ ] Step status set to `DONE` in `step-700/PROGRESS.md`
- [ ] Top-level `development-plan/PROGRESS.md` updated
- [ ] Step 800 kickoff notes added to `step-700/HANDOFF.md`
