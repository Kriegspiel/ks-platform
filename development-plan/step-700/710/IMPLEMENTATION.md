# Slice 710 - Implementation Plan
- Harden backend Dockerfile (non-root, healthcheck, deterministic copy/install).
- Add frontend multi-stage Dockerfile with `npm ci` + `npm run build` artifact stage.
- Finalize compose service topology (`app`, `frontend`, `nginx`, `mongo`) with `dev` and `prod` profiles.
- Validate explicit volume contracts between frontend build output and NGINX static root.
