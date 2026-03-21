# Step 130 Checklist

Use this as the execution checklist when implementing slice `130`.

## Planning And Context

- [ ] Re-read [development-plan/README.md](../../README.md)
- [ ] Re-read [development-plan/PLAN.md](../../PLAN.md)
- [ ] Re-read [step-100 README](../README.md)
- [ ] Claim slice `130` in [step-100/PROGRESS.md](../PROGRESS.md)

## Files To Create

- [ ] `frontend/package.json`
- [ ] `frontend/vite.config.js`
- [ ] `frontend/index.html`
- [ ] `frontend/src/main.jsx`
- [ ] `frontend/src/App.jsx`
- [ ] `frontend/src/App.css`
- [ ] `frontend/src/index.css`
- [ ] `frontend/src/services/api.js`
- [ ] `frontend/.gitignore`
- [ ] smallest frontend lint/test config needed for automation

## Implementation Tasks

- [ ] Add React, React Router, Axios, and Vite wiring
- [ ] Add proxy rules for `/api` and `/auth`
- [ ] Render the app into `#root`
- [ ] Add placeholder routes for `/`, `/auth/login`, `/auth/register`, `/lobby`, and `/game/:gameId`
- [ ] Add shared Axios client with relative base URL
- [ ] Enable credentials on the Axios client
- [ ] Add minimal base styles

## Automated Test Tasks

- [ ] Add route smoke tests
- [ ] Add Axios client configuration tests
- [ ] Ensure `npm run test -- --run` is non-interactive
- [ ] Ensure `npm run lint` passes
- [ ] Ensure `npm run build` passes

## Required Commands

- [ ] `cd frontend && npm install`
- [ ] `cd frontend && npm run test -- --run`
- [ ] `cd frontend && npm run lint`
- [ ] `cd frontend && npm run build`

## Before Marking Done

- [ ] Record exact command results in [step-100/PROGRESS.md](../PROGRESS.md)
- [ ] Confirm route coverage is automated
- [ ] Confirm the Axios client relies on the Vite proxy, not a hard-coded backend URL
- [ ] Leave handoff notes for later frontend slices
