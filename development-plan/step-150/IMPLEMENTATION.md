# Step 150 Implementation Plan

## Implementation Sequence

Build this slice in the following order:

1. Add `src/tests/__init__.py`.
2. Add shared fixtures in `src/tests/conftest.py`.
3. Update or create `src/tests/test_health.py` to rely on the shared fixtures.
4. Add `pyproject.toml` for pytest, black, and ruff.
5. Refactor earlier backend tests to use the harness if duplication exists.

## File-By-File Requirements

### `src/tests/__init__.py`

- Create the file.
- Keep it empty.

### `src/tests/conftest.py`

Required fixtures:

- `test_settings`
- `test_app`
- `test_client`
- `db_cleanup`

Recommended additional fixtures if helpful:

- `mongo_client`
- `test_db`

`test_settings` requirements:

- point to a separate database such as `kriegspiel_test`,
- set `ENVIRONMENT="testing"`,
- set a deterministic `SECRET_KEY`,
- set `SITE_ORIGIN` to a local dev-safe value,
- clear any cached settings state before and after use.

`test_app` requirements:

- build the app with `create_app(settings=test_settings)`,
- avoid importing a globally preconfigured production app when the factory can be used directly,
- ensure lifespan startup and shutdown occur under test.

`test_client` requirements:

- use `httpx.AsyncClient`,
- bind to the ASGI app directly,
- avoid requiring a live `uvicorn` process.

`db_cleanup` requirements:

- drop the test database before or after each test, or both if needed,
- never touch the non-test database,
- run automatically so individual tests do not need to remember cleanup.

### `src/tests/test_health.py`

This file becomes the shared smoke test for the backend health contract.

Required test cases:

- connected health response returns HTTP `200`
- connected health response returns `{"status": "ok", "db": "connected"}`
- disconnected or failing DB ping returns HTTP `503`
- disconnected or failing DB ping returns `{"status": "error", "db": "disconnected"}`

### `pyproject.toml`

Required configuration:

- pytest:
  - `asyncio_mode = "auto"`
  - appropriate test discovery settings for `src/tests`
- black:
  - line length `128`
- ruff:
  - include `src/app` and `src/tests`

Recommended additions:

- coverage configuration for `app`
- pytest markers if integration tests need labeling

## Guardrails

- Do not make tests depend on a manually started app server.
- Do not let tests point at the non-test database.
- Do not duplicate settings/app setup logic across multiple test files when it belongs in `conftest.py`.
- Do not leave `pyproject.toml` half-configured such that local and CI behavior diverge.

## Exact Handoff Expectations For Later Backend Slices

Later slices should be able to:

- import shared fixtures from `conftest.py` implicitly,
- add API tests without rebuilding app setup each time,
- run the backend suite with the same commands locally and in CI.
