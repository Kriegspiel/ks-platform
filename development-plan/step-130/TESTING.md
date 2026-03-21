# Step 130 Testing Plan

Testing for this slice must be fully automated.

The purpose of the tests here is not deep UI validation. The purpose is to prove the scaffold boots, routes render, the API client is configured correctly, and the project is buildable in CI without a running backend.

## Automated Test Goals

The automated suite must prove all of the following:

- the route shell renders successfully,
- every required placeholder route can be exercised in tests,
- the shared Axios client uses the intended dev-proxy configuration,
- the frontend builds successfully,
- linting passes.

## Required Test Files

The implementing agent should add the smallest needed test files, preferably:

- `frontend/src/__tests__/App.test.jsx`
- `frontend/src/__tests__/api.test.js`

### `frontend/src/__tests__/App.test.jsx`

Required test cases:

1. `renders_home_route`
   - Render the app at `/`.
   - Assert the `Home` placeholder is visible.

2. `renders_login_route`
   - Render the app at `/auth/login`.
   - Assert the `Login` placeholder is visible.

3. `renders_register_route`
   - Render the app at `/auth/register`.
   - Assert the `Register` placeholder is visible.

4. `renders_lobby_route`
   - Render the app at `/lobby`.
   - Assert the `Lobby` placeholder is visible.

5. `renders_game_route_with_param`
   - Render the app at `/game/test-game-id`.
   - Assert the `Game` placeholder is visible.
   - Assert the route can access the `gameId` parameter if the placeholder displays it.

### `frontend/src/__tests__/api.test.js`

Required test cases:

1. `api_client_uses_relative_base_url`
   - Import the Axios instance.
   - Assert the configured `baseURL` is relative or empty.

2. `api_client_enables_credentials`
   - Assert `withCredentials` is enabled.

3. `api_client_sets_json_defaults_if_added`
   - If default JSON headers are configured, assert them explicitly.

## Required Command Gates

The minimum automated gate for this slice should include:

```bash
cd frontend && npm install
cd frontend && npm run test -- --run
cd frontend && npm run lint
cd frontend && npm run build
```

If the implementing agent adds Vitest, `npm run test -- --run` must execute non-interactively and exit non-zero on failure.

## CI Expectations

This slice should be CI-compatible without a running backend.

That means:

- route tests must not depend on network calls,
- the build must succeed with only the local frontend files present,
- lint and test commands must be deterministic from a fresh install.

## Failure Conditions

The slice is not complete if any of the following happen:

- route coverage is checked only in a browser,
- the Axios client points directly to `http://localhost:8000`,
- the build requires the backend to be running,
- the route shell has no automated tests.

## Evidence To Record In Progress

When the slice is implemented, record in [step-100/PROGRESS.md](../step-100/PROGRESS.md):

- the exact `npm` commands,
- whether each command passed or failed,
- what frontend test tooling was added,
- any intentionally deferred frontend test coverage.
