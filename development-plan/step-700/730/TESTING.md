# Slice 730 - Testing (Automated + Gates)
## Exact Commands
```bash
python - <<'PY'
import yaml
yaml.safe_load(open('.github/workflows/ci.yml'))
print('ci.yml parse ok')
PY
cd src && black --check app tests
cd src && ruff check app tests
cd src && pytest tests -v --cov=app --cov-report=term-missing --cov-fail-under=80
cd frontend && npm ci
cd frontend && npm run lint
cd frontend && npm run build
```
## Thresholds / Coverage Gates
- YAML parse succeeds.
- Backend coverage gate >= 80%.
- Zero lint errors for backend/frontend.
- Deploy job condition restricts to push on `main`.
## CI Merge Gates
- backend + frontend jobs required.
- deploy job blocked on PRs and required on main pushes.
## Deterministic Fixtures/Seeding
- Fixed test env defaults and explicit seeds for randomized tests.
## Regression Matrix
- workflow syntax valid; backend lint/test/coverage gated; frontend lint/build gated; deploy dependency and branch gate enforced.
## Skip Policy + Prereqs
- Optional local `act` dry run may be skipped only when `act` absent.
## Post-Deploy Smoke + Rollback
```bash
# verify successful backend/frontend/deploy checks in Actions UI
# rollback
git checkout -- .github/workflows/ci.yml
```
