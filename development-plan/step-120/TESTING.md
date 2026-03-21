# Step 120 Testing Plan

Testing for this slice must be fully automated.

The signoff for this slice must prove both code-path correctness and real MongoDB connectivity behavior. Unit tests alone are not enough, and a manually started local MongoDB instance is not acceptable as the only verification method.

## Automated Test Goals

The automated suite must prove all of the following:

- `init_db()` builds a Motor client from the configured URI,
- all required indexes are created,
- `close_db()` closes and clears the client safely,
- `get_db()` behaves correctly in initialized and uninitialized states,
- `/health` returns the connected response when MongoDB is reachable,
- `/health` returns the disconnected response when MongoDB is unavailable.

## Required Test Files

### `src/tests/test_db.py`

Required test cases:

1. `test_get_db_raises_when_not_initialized`
   - Ensure module state is cleared.
   - Assert `get_db()` raises a clear runtime error.

2. `test_init_db_builds_motor_client_from_settings`
   - Patch `AsyncIOMotorClient`.
   - Assert it is called with `settings.MONGO_URI`.
   - Assert the database handle for the URI's database name is selected.

3. `test_init_db_creates_required_indexes`
   - Patch the Motor collection objects or use lightweight fakes.
   - Assert each required collection receives the expected index calls.
   - Assert TTL indexes use the correct `expireAfterSeconds` values.

4. `test_close_db_is_idempotent`
   - Call `close_db()` twice.
   - Assert no exception is raised.
   - Assert the client close method is only applied when a client exists.

5. `test_init_db_returns_handle_for_expected_database`
   - Use a URI with a distinct database name such as `kriegspiel_slice120_test`.
   - Assert the resolved handle targets that database.

### `src/tests/test_health.py`

Required test cases:

1. `test_health_returns_connected_payload_when_db_ping_succeeds`
   - Build the app with a test settings object.
   - Mock or provide a reachable database handle.
   - Assert HTTP `200`.
   - Assert the payload is exactly `{"status": "ok", "db": "connected"}`.

2. `test_health_returns_disconnected_payload_when_db_ping_fails`
   - Force ping to raise.
   - Assert HTTP `503`.
   - Assert the payload is exactly `{"status": "error", "db": "disconnected"}`.

3. `test_health_returns_disconnected_payload_when_db_not_initialized`
   - Build the app in a disconnected state.
   - Assert HTTP `503`.
   - Assert the payload is the disconnected contract.

### Integration Coverage

This slice also requires real-Mongo integration coverage.

The integration suite must:

- start a disposable MongoDB `mongo:7` instance automatically,
- initialize it as a single-node replica set,
- point the app to a disposable test database,
- verify the app becomes healthy,
- verify indexes are present in MongoDB after startup,
- tear the environment down automatically even on test failure.

If no reusable repo-wide helper exists yet, add the thinnest possible wrapper such as `scripts/test-step-120.sh` to automate this sequence end to end. The final signoff command must be non-interactive.

## Required Command Gates

The minimum automated gate for this slice should include:

```bash
cd src && pytest tests/test_db.py tests/test_health.py -v
cd src && pytest tests/test_db.py tests/test_health.py --cov=app.db --cov=app.main --cov-fail-under=90 -v
cd src && python -m compileall app tests
cd src && ruff check app tests
cd src && black --check app tests
```

And one fully automated MongoDB integration command, for example:

```bash
./scripts/test-step-120.sh
```

An acceptable wrapper must:

- create or start a disposable MongoDB replica set,
- wait for readiness,
- run the integration subset of the tests,
- stop and remove temporary resources,
- return a non-zero exit status on failure.

## CI Expectations

This slice should be compatible with CI service containers as described in [INFRA.md](../../INFRA.md).

That means:

- no test should require an already-running personal MongoDB instance,
- integration tests must be runnable from a clean checkout,
- failure in MongoDB initialization must be surfaced as a failing test, not hidden as a warning.

## Failure Conditions

The slice is not complete if any of the following happen:

- indexes are created only in manual testing and not asserted in automation,
- `/health` is validated only with a hand-run `curl`,
- the app crashes at import time when MongoDB is down,
- the integration suite leaves containers or databases behind after failure.

## Evidence To Record In Progress

When the slice is implemented, record in [step-100/PROGRESS.md](../step-100/PROGRESS.md):

- the exact unit-test commands,
- the exact integration command,
- whether each command passed or failed,
- what disposable MongoDB mechanism was used.
