# Slice 720 - Implementation Plan
- Add gzip, rate-limit zones, and security headers baseline.
- Implement production TLS + ACME + SPA `try_files` routing.
- Proxy `/api/` and `/auth/` to app upstream with forwarded headers.
- Add dev HTTP-only config parity for local runs.
