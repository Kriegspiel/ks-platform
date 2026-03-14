# Infrastructure & Deployment

## Deployment Topology

Single VPS running Docker Compose. Suitable for the expected user base (niche chess variant). Scales vertically before needing horizontal scaling.

```
┌─────────────────────────────────────────────┐
│  VPS (e.g., Hetzner CX31 or DigitalOcean)  │
│  4 vCPU / 8 GB RAM / 80 GB SSD             │
│                                             │
│  ┌─── Docker Compose ─────────────────────┐ │
│  │                                        │ │
│  │  ┌──────────┐   ┌──────────────────┐   │ │
│  │  │  NGINX   │──▶│  FastAPI (app)   │   │ │
│  │  │  :80/443 │   │  :8000           │   │ │
│  │  └──────────┘   └────────┬─────────┘   │ │
│  │                          │             │ │
│  │                          ▼             │ │
│  │                 ┌──────────────────┐   │ │
│  │                 │   MongoDB 7+     │   │ │
│  │                 │   :27017         │   │ │
│  │                 │   (replica set)  │   │ │
│  │                 └──────────────────┘   │ │
│  │                                        │ │
│  │  ┌──────────────────┐  (dev only)      │ │
│  │  │  Mongo Express   │                  │ │
│  │  │  :8081           │                  │ │
│  │  └──────────────────┘                  │ │
│  └──────────────────────────────────────────┘ │
│                                             │
│  certbot (Let's Encrypt)                    │
│  unattended-upgrades                        │
│  UFW firewall (22, 80, 443 only)            │
└─────────────────────────────────────────────┘
```

## Docker Compose

```yaml
# docker-compose.yml

services:

  nginx:
    image: nginx:1.27-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
      - app-static:/var/www/static:ro
    depends_on:
      app:
        condition: service_healthy
    restart: unless-stopped

  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: ks-app
    environment:
      - MONGO_URI=mongodb://mongo:27017/kriegspiel?replicaSet=rs0
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - LOG_LEVEL=${LOG_LEVEL:-info}
    volumes:
      - app-static:/app/static
    expose:
      - "8000"
    depends_on:
      mongo:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  mongo:
    image: mongo:7
    container_name: ks-mongo
    command: ["mongod", "--replSet", "rs0", "--bind_ip_all"]
    volumes:
      - mongo-data:/data/db
      - ./mongo/init-replica.sh:/docker-entrypoint-initdb.d/init-replica.sh:ro
    expose:
      - "27017"
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "rs.status().ok || rs.initiate()"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Dev only — not included in production profile
  mongo-express:
    image: mongo-express:1.0
    container_name: ks-mongo-express
    environment:
      - ME_CONFIG_MONGODB_URL=mongodb://mongo:27017/?replicaSet=rs0
      - ME_CONFIG_BASICAUTH=true
      - ME_CONFIG_BASICAUTH_USERNAME=${ME_USERNAME:-admin}
      - ME_CONFIG_BASICAUTH_PASSWORD=${ME_PASSWORD:-admin}
    ports:
      - "8081:8081"
    depends_on:
      - mongo
    profiles:
      - dev
    restart: unless-stopped

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h; done'"
    profiles:
      - production

volumes:
  mongo-data:
  app-static:

networks:
  default:
    name: kriegspiel
```

## App Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Collect static files (if any build step needed)
# RUN python manage_static.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--ws-max-size", "65536"]
```

Single worker because:
- WebSocket connections are per-process (no cross-worker routing without Redis)
- The async event loop handles concurrency within the single process
- For the expected load (<100 concurrent games), one worker is sufficient

## NGINX Configuration

```nginx
# nginx/conf.d/kriegspiel.conf

upstream app {
    server app:8000;
}

server {
    listen 80;
    server_name kriegspiel.org www.kriegspiel.org;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name kriegspiel.org www.kriegspiel.org;

    ssl_certificate /etc/letsencrypt/live/kriegspiel.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kriegspiel.org/privkey.pem;

    # Static files (CSS, JS, images, chess pieces)
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # REST API
    location /api/ {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Rate limiting
        limit_req zone=api burst=20 nodelay;
    }

    # Auth endpoints (stricter rate limiting)
    location /auth/ {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        limit_req zone=auth burst=5 nodelay;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        proxy_read_timeout 3600s;    # Keep WS alive for 1 hour
        proxy_send_timeout 3600s;

        limit_conn ws_conn 5;        # Max 5 WS connections per IP
    }

    # Server-rendered pages (Jinja2)
    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Rate limit zones
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;
limit_conn_zone $binary_remote_addr zone=ws_conn:10m;
```

## MongoDB Replica Set Init

```bash
#!/bin/bash
# mongo/init-replica.sh
# Initializes a single-node replica set (required for Change Streams)

sleep 5
mongosh --eval '
  rs.initiate({
    _id: "rs0",
    members: [{ _id: 0, host: "mongo:27017" }]
  })
'
```

## Environment Variables

```bash
# .env.example

# App
SECRET_KEY=change-me-to-random-64-char-string
ENVIRONMENT=production          # "development" | "production"
LOG_LEVEL=info                  # "debug" | "info" | "warning" | "error"

# MongoDB
MONGO_URI=mongodb://mongo:27017/kriegspiel?replicaSet=rs0

# OAuth (Phase 2)
# GOOGLE_CLIENT_ID=
# GOOGLE_CLIENT_SECRET=

# Mongo Express (dev only)
ME_USERNAME=admin
ME_PASSWORD=change-me
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongo:
        image: mongo:7
        ports: ["27017:27017"]
        options: >-
          --health-cmd "mongosh --eval 'db.runCommand({ping:1})'"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r app/requirements.txt
          pip install -r app/requirements-dev.txt

      - name: Lint
        run: |
          black --check --line-length 128 app/
          ruff check app/

      - name: Test
        env:
          MONGO_URI: mongodb://localhost:27017/kriegspiel_test
          SECRET_KEY: test-secret
          ENVIRONMENT: testing
        run: |
          cd app
          pytest --cov=. --cov-report=xml -v

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: app/coverage.xml

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/kriegspiel
            git pull origin main
            docker compose build app
            docker compose up -d app
            docker compose exec app python -c "print('Deployment OK')"
```

## Monitoring & Logging

### Application Logging

```python
import logging
import structlog

# Structured JSON logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(),
)

log = structlog.get_logger()

# Usage:
log.info("game.move", game_id=game_id, color="white", uci="e2e4", result="REGULAR_MOVE")
log.warning("auth.failed_login", username="unknown", ip="1.2.3.4")
```

### Health Check

```python
@app.get("/health")
async def health():
    """Used by Docker healthcheck and uptime monitoring."""
    try:
        await app.state.db.command("ping")
        return {"status": "ok", "db": "connected"}
    except Exception:
        return JSONResponse({"status": "error", "db": "disconnected"}, status_code=503)
```

### Uptime Monitoring

Use a free external service (UptimeRobot, Healthchecks.io) to ping `/health` every 5 minutes. Alert on downtime via email or Telegram.

### Backup

```bash
#!/bin/bash
# backup.sh — run via cron daily at 3 AM

BACKUP_DIR="/opt/backups/kriegspiel"
DATE=$(date +%Y%m%d_%H%M%S)

docker compose exec -T mongo mongodump \
    --archive="/tmp/kriegspiel_${DATE}.gz" \
    --gzip \
    --db=kriegspiel

docker cp ks-mongo:/tmp/kriegspiel_${DATE}.gz "${BACKUP_DIR}/"

# Keep last 30 days
find ${BACKUP_DIR} -name "*.gz" -mtime +30 -delete
```

## Local Development

```bash
# Clone and start
git clone git@github.com:kriegspiel/ks-platform.git
cd ks-platform
cp .env.example .env

# Start with dev profile (includes mongo-express)
docker compose --profile dev up --build

# Access:
# App:           http://localhost:8000
# Mongo Express: http://localhost:8081

# Or run without Docker for faster iteration:
cd app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
