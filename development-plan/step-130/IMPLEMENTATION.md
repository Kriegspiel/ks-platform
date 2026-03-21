# Step 130 Implementation Plan

## Implementation Sequence

Build this slice in the following order:

1. Create `frontend/package.json` with scripts and dependencies.
2. Add Vite configuration.
3. Add the HTML and React entrypoint files.
4. Add the route shell and placeholder pages.
5. Add the shared Axios client.
6. Add the smallest linting and test setup needed for fully automated signoff.

## File-By-File Requirements

### `frontend/package.json`

Required dependencies:

- `react`
- `react-dom`
- `react-router-dom`
- `axios`

Required dev dependencies:

- `vite`
- `@vitejs/plugin-react`
- `eslint`
- `eslint-plugin-react-hooks`

For fully automated signoff, the implementing agent should also add the smallest needed frontend test tooling, preferably:

- `vitest`
- `jsdom`
- `@testing-library/react`
- `@testing-library/jest-dom`

Required scripts:

- `dev`
- `build`
- `lint`
- `test`

### `frontend/vite.config.js`

Required behavior:

- enable the React plugin,
- proxy `/api` to `http://localhost:8000`,
- proxy `/auth` to `http://localhost:8000`,
- preserve a straightforward config shape that later slices can extend.

### `frontend/index.html`

Required contents:

- `<div id="root"></div>`
- the standard Vite module entry pointing at `src/main.jsx`

### `frontend/src/main.jsx`

Required behavior:

- render the React app into `#root`
- keep the file minimal and side-effect light

### `frontend/src/App.jsx`

Required behavior:

- define the route map for:
  - `/`
  - `/auth/login`
  - `/auth/register`
  - `/lobby`
  - `/game/:gameId`
- render deterministic placeholder content for each route so tests can assert against stable text
- keep routing logic separate enough that tests can render route state without booting a browser

Recommended shape:

- export a pure routes component for testability,
- wrap it with `BrowserRouter` in the default app component.

### `frontend/src/services/api.js`

Required behavior:

- create an Axios instance,
- use a relative `baseURL` such as `""`,
- set `withCredentials: true`,
- avoid hard-coding `http://localhost:8000` in the client because the Vite proxy is the planned dev path.

### Styles

`frontend/src/App.css` and `frontend/src/index.css` should:

- provide a small reset/base style layer,
- make the placeholder pages legible on desktop and mobile,
- avoid spending design budget that belongs to later slices.

## Placeholder Route Requirements

Each placeholder route should expose stable visible text suitable for automated tests, for example:

- `/` → `Home`
- `/auth/login` → `Login`
- `/auth/register` → `Register`
- `/lobby` → `Lobby`
- `/game/:gameId` → `Game`

It is acceptable to include more descriptive copy, but each placeholder must have one predictable heading or label.

## Guardrails

- Do not add global state libraries.
- Do not implement real auth flows.
- Do not hard-code the backend origin in Axios.
- Do not rely on manual browser checks as the primary verification path.
- Do not import backend code into the frontend.

## Exact Handoff Expectations For Later Frontend Slices

Later slices should be able to:

- swap placeholder pages for real screens without changing the route map,
- reuse the shared Axios client without re-creating it,
- extend Vite config rather than replacing it.
