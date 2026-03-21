# Step 150 - Test Harness And Smoke Tests

This folder is the detailed execution packet for slice `150` from [step-100](../README.md).

Canonical status for this slice still lives in [step-100/PROGRESS.md](../PROGRESS.md). This folder expands the slice into implementation-ready planning docs; it does not create a new top-level rollup step.

## Goal

Create the shared backend test harness, pytest configuration, and smoke tests that make the foundation slices reproducibly testable in CI and local development.

## Why This Slice Exists

Earlier slices can create targeted tests, but this slice is where the repo gets its reusable testing foundation:

- shared settings and app fixtures,
- shared async HTTP client setup,
- isolated test database cleanup,
- central pytest/format/lint configuration,
- a single place to normalize smoke coverage for the foundation stack.

## Read First

- [development-plan/README.md](../../README.md)
- [development-plan/PLAN.md](../../PLAN.md)
- [step-100 README](../README.md)
- [step-110 README](../110/README.md)
- [step-120 README](../120/README.md)
- [INFRA.md](../../../INFRA.md)

## Scope

In scope:

- `src/tests/__init__.py`
- `src/tests/conftest.py`
- `src/tests/test_health.py`
- `pyproject.toml`
- refactoring earlier slice tests to use shared fixtures when needed

Out of scope:

- end-to-end browser testing,
- frontend test tooling,
- game-logic correctness beyond smoke coverage,
- CI workflow authoring beyond keeping the harness compatible with planned CI usage.

## Deliverables

The implementing agent should leave behind at least these files:

- `src/tests/__init__.py`
- `src/tests/conftest.py`
- `src/tests/test_health.py`
- `pyproject.toml`

The implementing agent may also update earlier backend tests so they reuse the shared harness rather than duplicating setup.

## Contract For This Slice

The finished harness must satisfy all of the following:

- tests can build a FastAPI app with dedicated test settings,
- tests can make async HTTP requests against the app without a manually started server,
- tests use a separate test database,
- the test database is cleaned up between tests,
- health tests assert the connected database response contract,
- pytest, black, and ruff configuration live in `pyproject.toml`.

## Required Reading Order For The Implementing Agent

1. Read [IMPLEMENTATION.md](./IMPLEMENTATION.md)
2. Read [TESTING.md](./TESTING.md)
3. Read [CHECKLIST.md](./CHECKLIST.md)
4. Claim slice `150` in [step-100/PROGRESS.md](../PROGRESS.md) before writing code

## Definition Of Done

This slice is done only when:

- the implementation matches [IMPLEMENTATION.md](./IMPLEMENTATION.md),
- the automated commands in [TESTING.md](./TESTING.md) pass,
- exact commands and results are recorded in [step-100/PROGRESS.md](../PROGRESS.md), and
- the shared fixtures are actually used by the smoke tests rather than existing unused.

## Handoff To Later Steps

Later backend slices should treat this harness as the default place to add shared fixtures and baseline smoke coverage. They should avoid re-creating app and database setup logic ad hoc inside individual test files.
