# Step 130 - React Frontend Scaffold

This folder is the detailed execution packet for slice `130` from [step-100](../README.md).

Canonical status for this slice still lives in [step-100/PROGRESS.md](../PROGRESS.md). This folder expands the slice into implementation-ready planning docs; it does not create a new top-level rollup step.

## Goal

Create the initial React + Vite SPA scaffold that matches the active development plan, provides placeholder routes for the MVP flow, and includes fully automated frontend smoke tests.

## Why This Slice Exists

The root repo docs still describe a server-rendered frontend, but the active development plan explicitly moved to a React + Vite SPA. This slice establishes the frontend baseline that every later UI slice depends on:

- Vite project wiring,
- router structure,
- shared API client setup,
- deterministic placeholder pages for early smoke tests,
- the first automated frontend verification path.

## Read First

- [development-plan/README.md](../../README.md)
- [development-plan/PLAN.md](../../PLAN.md)
- [step-100 README](../README.md)
- [README.md](../../../README.md)
- [FRONTEND.md](../../../FRONTEND.md)

For implementation choices that conflict with [FRONTEND.md](../../../FRONTEND.md), follow the development plan's React + Vite decision.

## Scope

In scope:

- create the Vite-based React app skeleton,
- add React Router placeholder routes,
- add a shared Axios client,
- add minimal base styles,
- add automated frontend route and API-client tests.

Out of scope:

- real auth forms or API integration,
- final visual design or branding polish,
- game board rendering,
- state management beyond basic routing and placeholders.

## Deliverables

The implementing agent should leave behind at least these files:

- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/index.html`
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`
- `frontend/src/App.css`
- `frontend/src/index.css`
- `frontend/src/services/api.js`
- `frontend/.gitignore`

Additional files are allowed when they are the smallest pieces needed for automation, for example:

- `frontend/eslint.config.js`
- `frontend/vitest.config.js`
- `frontend/vitest.setup.js`
- `frontend/src/__tests__/App.test.jsx`
- `frontend/src/__tests__/api.test.js`

## Contract For This Slice

The finished code must satisfy all of the following:

- Vite boots the app from `frontend/index.html`
- the root React entrypoint renders into `#root`
- placeholder routes exist for `/`, `/auth/login`, `/auth/register`, `/lobby`, and `/game/:gameId`
- the shared Axios client uses a relative base URL so Vite's proxy can handle backend routing
- the Axios client enables credentials
- the scaffold can build without the backend running

## Required Reading Order For The Implementing Agent

1. Read [IMPLEMENTATION.md](./IMPLEMENTATION.md)
2. Read [TESTING.md](./TESTING.md)
3. Read [CHECKLIST.md](./CHECKLIST.md)
4. Claim slice `130` in [step-100/PROGRESS.md](../PROGRESS.md) before writing code

## Definition Of Done

This slice is done only when:

- the implementation matches [IMPLEMENTATION.md](./IMPLEMENTATION.md),
- every automated frontend check in [TESTING.md](./TESTING.md) passes,
- exact commands and results are recorded in [step-100/PROGRESS.md](../PROGRESS.md), and
- route coverage is proven with automation rather than browser-only inspection.

## Handoff To The Next Slices

- Slice `140` can assume the frontend has a build output path and dev proxy expectations.
- Later UI slices can replace placeholder route bodies, but they should keep the route map stable unless the plan changes.
