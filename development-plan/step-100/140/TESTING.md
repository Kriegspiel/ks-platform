# Step 140 Testing Plan

Testing for this slice is configuration validation plus automated stack bring-up.

This slice does not need traditional unit tests, but it does need non-interactive command-level verification. A developer manually eyeballing generated YAML or NGINX config is not enough.

## Automated Test Goals

The automated signoff must prove all of the following:

- Compose syntax is valid,
- the backend image builds,
- NGINX configuration is syntactically valid,
- the replica-init script is syntactically valid and usable,
- the dev stack boots,
- the backend health endpoint becomes reachable through the containerized app.

## Required Verification Commands

The minimum automated gate for this slice should include:

```bash
docker compose config
docker build -f src/app/Dockerfile src
bash -n src/mongo/init-replica.sh
docker run --rm -v "$PWD/src/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" -v "$PWD/src/nginx/conf.d:/etc/nginx/conf.d:ro" nginx:1.27-alpine nginx -t
docker compose --profile dev up -d --build
curl --fail http://localhost:8000/health
docker compose exec -T mongo mongosh --quiet --eval 'rs.status().ok'
docker compose down -v
```

If the implementing agent wraps these in a helper script, that is acceptable, but the final verification must remain fully automated and non-interactive.

## Additional Recommended Checks

These are recommended when practical:

- verify `mongo-express` appears only when `--profile dev` is used,
- verify the `certbot` service is absent from the default profile bring-up,
- verify the app container receives the expected environment values.

## CI Expectations

This slice should be runnable on a machine that has Docker installed and no pre-existing local services.

That means:

- Compose bring-up must not assume a manually prepared MongoDB replica set,
- health probing must be scripted,
- teardown must happen automatically.

## Failure Conditions

The slice is not complete if any of the following happen:

- Compose parses only after a developer edits values by hand,
- NGINX syntax is never validated by a command,
- `docker compose up` is run manually but not captured in automated evidence,
- the replica-set script requires copy-pasted shell input.

## Evidence To Record In Progress

When the slice is implemented, record in [step-100/PROGRESS.md](../PROGRESS.md):

- the exact Docker and shell commands that were run,
- whether each command passed or failed,
- any temporary container cleanup steps that were needed,
- any follow-up infra gaps left for later steps.
