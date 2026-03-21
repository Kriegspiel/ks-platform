# Development Plan

This folder is the execution system for building the platform from the repo specs.

Developers and agents must treat this folder as operational policy, not optional guidance.

## Strict Rules

1. Always read this file before starting work.
2. Always read [PLAN.md](./PLAN.md) before choosing or changing a step.
3. Always read the relevant step `README.md` and `PROGRESS.md` before touching code for that step.
4. Always update the matching step `PROGRESS.md` when work starts, when scope changes, when blocked, and when work stops.
5. Always update the top-level [PROGRESS.md](./PROGRESS.md) when a step status changes.
6. Always test before marking any slice or step complete.
7. Never mark a slice or step complete without recording the test command(s) and result(s) in the step `PROGRESS.md`.
8. Never start a dependent step until its prerequisite step is complete, unless the step `PROGRESS.md` explicitly documents the reason.
9. Keep scope small: work on one agent-sized slice at a time whenever possible.
10. If blocked, mark the slice as `BLOCKED`, explain why, and list the next unblock options.
11. If specs conflict, follow the precedence in the repository root [README.md](../README.md).
12. Do not silently change the plan structure. If the plan must change, update `PLAN.md`, the affected step `README.md`, and the top-level `PROGRESS.md` together.

## Required Workflow

### Before starting

1. Read this file.
2. Read [PLAN.md](./PLAN.md).
3. Read the target step `README.md` and `PROGRESS.md`.
4. Read the root spec documents listed in that step's "Read First" section.
5. Claim the slice in the step `PROGRESS.md`.

### During work

1. Keep work inside the current step unless a documented prerequisite forces a small cross-step change.
2. Update the step `PROGRESS.md` as soon as a slice changes state.
3. Add notes, evidence, or temporary research inside the step folder if needed.

### Before marking complete

1. Run the relevant tests.
2. Record the exact test commands and results in the step `PROGRESS.md`.
3. Update slice status to `DONE`.
4. If every slice is done and tested, mark the step `DONE` in both the step `PROGRESS.md` and the top-level [PROGRESS.md](./PROGRESS.md).

### If blocked

1. Mark the slice `BLOCKED`.
2. Explain the blocker clearly.
3. List the smallest next action that would unblock it.
4. Do not mark the step `DONE`.

## Status Vocabulary

Use these statuses consistently:

- `NOT STARTED`
- `IN PROGRESS`
- `BLOCKED`
- `DONE`

## Plan Structure Overview

This plan is organized in two layers:

- Top level:
  - [PLAN.md](./PLAN.md): the master sequence of high-level steps.
  - [PROGRESS.md](./PROGRESS.md): rollup view of step status across the whole project.
- Per step:
  - `step-XYZ/README.md`: the step goal, scope, dependencies, task slices, tests, and exit criteria.
  - `step-XYZ/PROGRESS.md`: live status, test evidence, blockers, and handoff notes for that step.
- Optional slice detail packets:
  - A folder such as `step-110/` may exist when a single slice needs a more detailed execution packet split across multiple Markdown files.
  - These slice folders do not change the top-level rollup model on their own.
  - Unless a plan document says otherwise, slice status still belongs in the parent step `PROGRESS.md`.

Step numbers use 100-point spacing (`step-100`, `step-200`, etc.) so new steps can be inserted later without renumbering everything.

## Extra Rules Worth Following

- Record assumptions instead of hiding them.
- Prefer small commits and small PR-sized slices.
- Keep step artifacts local to the step folder when possible.
- When you finish a slice, leave the next agent enough context to continue without re-discovery.
- Do not start Phase 2 or later work inside this plan until the MVP steps here are complete and the plan is refreshed.
