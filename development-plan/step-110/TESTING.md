# Step 110 Testing Plan

Testing for this slice must be fully automated.

`uvicorn`, browser checks, and manual `curl` calls are useful for local debugging, but they are not acceptable as the primary completion evidence for this slice.

## Automated Test Goals

The automated suite must prove all of the following:

- settings defaults are correct,
- environment overrides work,
- the app factory builds a valid FastAPI app,
- the app boots and shuts down without MongoDB,
- the `/health` contract is stable,
- allowed origins receive CORS headers,
- disallowed origins do not receive permissive CORS headers.

## Required Test Files

### `src/tests/test_config.py`

Required test cases:

1. `test_settings_defaults`
   - Clear the relevant environment variables.
   - Instantiate `Settings()`.
   - Assert every default exactly:
     - `SECRET_KEY == "dev-secret-change-me"`
     - `MONGO_URI == "mongodb://localhost:27017/kriegspiel?replicaSet=rs0"`
     - `ENVIRONMENT == "development"`
     - `LOG_LEVEL == "info"`
     - `SITE_ORIGIN == "http://localhost:5173"`

2. `test_settings_reads_environment_overrides`
   - Use `monkeypatch.setenv(...)` for every field above.
   - Instantiate `Settings()`.
   - Assert the override values are returned.

3. `test_get_settings_cache_can_be_cleared_between_tests`
   - Call `get_settings()`.
   - Change at least one environment variable with `monkeypatch`.
   - Clear the cache.
   - Call `get_settings()` again.
   - Assert the new instance reflects the override.

### `src/tests/test_app_factory.py`

Required test cases:

1. `test_create_app_sets_expected_title`
   - Build the app with explicit `Settings(...)`.
   - Assert `app.title == "Kriegspiel Chess API"`.

2. `test_create_app_stores_settings_on_app_state`
   - Build the app with an explicit non-default `SITE_ORIGIN`.
   - Assert `app.state.settings` exists.
   - Assert the stored settings object contains that exact origin.

3. `test_app_factory_is_repeatable`
   - Create two app instances with different explicit settings.
   - Assert they are distinct objects.
   - Assert each app keeps its own `app.state.settings`.

4. `test_lifespan_runs_without_external_dependencies`
   - Enter the app through a test client context manager so startup and shutdown run.
   - Assert no exception is raised when no database is present.

5. `test_cors_allows_site_origin_preflight`
   - Build an app with `SITE_ORIGIN="http://localhost:5173"`.
   - Send `OPTIONS /health` with:
     - `Origin: http://localhost:5173`
     - `Access-Control-Request-Method: GET`
   - Assert the response grants CORS for that origin.
   - Assert `access-control-allow-credentials == "true"`.

6. `test_cors_allows_local_backend_origin_in_development`
   - Build an app with `ENVIRONMENT="development"`.
   - Send a preflight request from `http://localhost:8000`.
   - Assert the origin is allowed.

7. `test_cors_does_not_grant_unknown_origin`
   - Send a preflight request from an unknown origin such as `http://evil.example`.
   - Assert the response does not echo that origin in `access-control-allow-origin`.

### `src/tests/test_health.py`

Required test cases:

1. `test_health_returns_http_200`
   - Call `GET /health`.
   - Assert status code `200`.

2. `test_health_returns_exact_slice_110_payload`
   - Assert the response body is exactly `{"status": "ok"}`.
   - Do not allow extra keys in this slice.

3. `test_health_response_is_json`
   - Assert the response content type is JSON.

## Required Tooling Gates

The implementing agent should run these commands as the minimum automated gate for the slice:

```bash
cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py -v
cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py --cov=app.config --cov=app.main --cov-fail-under=90 -v
cd src && python -m compileall app tests
cd src && ruff check app tests
cd src && black --check app tests
```

If `black`, `ruff`, or coverage configuration is not available yet, the implementing agent must either:

- add the smallest missing project configuration needed for these commands to run, or
- document the exact blocker in [step-100/PROGRESS.md](../step-100/PROGRESS.md) and stop without marking the slice done.

## CI Expectations

This slice should be compatible with non-interactive CI execution.

That means:

- no test may depend on a manually started server,
- no test may require live MongoDB,
- no test may depend on internet access,
- all tests must run from a fresh process using only local code and explicit environment variables.

## Failure Conditions

The slice is not complete if any of the following happen:

- `/health` only works after a developer starts `uvicorn` manually
- tests rely on local MongoDB
- the CORS check is verified only by browser inspection
- `get_settings()` cannot be reset cleanly in tests
- importing `app.main` attempts external I/O

## Evidence To Record In Progress

When the slice is implemented, record in [step-100/PROGRESS.md](../step-100/PROGRESS.md):

- the exact commands that were run,
- whether each command passed or failed,
- any temporary deviations from this plan,
- any follow-up testing debt that remains for slice `150`.
