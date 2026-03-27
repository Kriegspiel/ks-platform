# Step 900 Master Checklist

## Before Starting Any Slice

- [ ] Read `development-plan/README.md`
- [ ] Read `development-plan/PLAN.md`
- [ ] Read `development-plan/step-900/README.md`
- [ ] Read `development-plan/step-900/PROGRESS.md`
- [ ] Verify Step 800 launch-readiness artifacts are available
- [ ] Confirm target repos (`ks-home`, `Kriegspiel/content`, and implementation host repo) are accessible
- [ ] Claim target slice in `development-plan/step-900/PROGRESS.md`

## Required Execution Order

- [ ] Slice 910
- [ ] Slice 920
- [ ] Slice 930
- [ ] Slice 940
- [ ] Slice 950
- [ ] Slice 960

## Slice Completion Gate (repeat for each slice)

- [ ] Scope implemented exactly as defined in slice `IMPLEMENTATION.md`
- [ ] All commands in slice `TESTING.md` executed and logged
- [ ] Required CI merge gates green for impacted lanes
- [ ] Accessibility checks pass at required thresholds
- [ ] Smoke checks pass in preview and release candidate environment
- [ ] Link and metadata validation pass
- [ ] Static-regeneration checks pass for content-triggered website builds
- [ ] Visual regression checks pass or waivers documented
- [ ] Any skipped checks recorded with owner, risk, and mitigation ETA
- [ ] Slice marked done in `step-900/PROGRESS.md`


## Operator-Required Cloudflared/Domain Gate (`kriegspiel.org`)

### Fil-required (interactive/approval)

- [ ] `cloudflared tunnel login` completed on production host and auth artifact confirmed.
- [ ] Production tunnel selected (or created with approval) and UUID recorded in release notes.
- [ ] DNS routes approved/applied for `kriegspiel.org`, `app.kriegspiel.org`, and `api.kriegspiel.org`.
- [ ] Production cutover window approved by Fil.

### Agent-automatable (post-approval)

- [ ] `cloudflared --version` and `cloudflared tunnel list` evidence captured.
- [ ] `cloudflared` service installed/restarted and healthy (`systemctl status`).
- [ ] Domain + endpoint verification captured (`dig`, `curl`, smoke routes).
- [ ] Rollback command path validated (restore previous DNS/tunnel target).

## Step Completion Gate

- [ ] Slices 910-960 all complete
- [ ] Required pages validated live: home, leaderboard, blog, changelog, rules
- [ ] Step status set to `DONE` in `step-900/PROGRESS.md`
- [ ] Top-level `development-plan/PROGRESS.md` updated
- [ ] Launch/rollback handoff finalized in `step-900/HANDOFF.md`
