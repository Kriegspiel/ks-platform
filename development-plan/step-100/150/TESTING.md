# Step 150 Testing Plan

This slice defines the backend test harness, so its verification must prove the harness itself is reusable and CI-friendly.

## Automated Test Goals

The automated suite must prove all of the following:

- shared fixtures build a test app successfully,
- the async client can hit backend routes without `uvicorn`,
- the test database is isolated from the main database,
- health smoke tests pass through the shared harness,
- lint and formatting configuration are active and usable,
- coverage reporting works.

## Required Test Coverage

### Fixture-Level Expectations

The harness should support these verified behaviors:

1. settings fixture builds a test-specific configuration
2. app fixture creates an app from the factory
3. async client fixture can perform requests against the app
4. cleanup fixture removes test data between cases

These behaviors can be asserted either directly in dedicated tests or indirectly through stable smoke tests that clearly exercise them.

### Health Smoke Coverage

`src/tests/test_health.py` must verify:

1. `GET /health` returns HTTP `200` with the connected payload when the test database is available
2. `GET /health` returns HTTP `503` with the disconnected payload when ping fails

If mocking is used for the failure path, it must still go through the shared test harness rather than bypassing it entirely.

## Required Command Gates

The minimum automated gate for this slice should include:

```bash
cd src && pytest tests -v
cd src && pytest tests --cov=app --cov-report=xml -v
cd src && python -m compileall app tests
cd src && ruff check app tests
cd src && black --check app tests
```

If integration tests depend on a disposable MongoDB instance, the final `pytest tests -v` flow should either:

- work directly against the already-automated local/CI MongoDB service, or
- invoke a thin wrapper that starts and stops the dependency non-interactively.

## CI Expectations

This slice should remain compatible with the MongoDB service-container approach documented in [INFRA.md](../../../INFRA.md).

That means:

- tests should run from `cd src`,
- environment variables should be enough to point the suite at the test database,
- no fixture should assume a developer shell session or preloaded state.

## Failure Conditions

The slice is not complete if any of the following happen:

- shared fixtures exist but the smoke tests still use bespoke setup code,
- tests point at `kriegspiel` instead of `kriegspiel_test`,
- `pyproject.toml` does not actually drive pytest, black, and ruff,
- coverage generation only works locally and not from the standard test command.

## Evidence To Record In Progress

When the slice is implemented, record in [step-100/PROGRESS.md](../PROGRESS.md):

- the exact pytest command(s),
- the exact lint/format commands,
- whether coverage generation succeeded,
- any fixture limitations that later slices should know about.
