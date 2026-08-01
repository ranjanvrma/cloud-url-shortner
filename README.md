# Cloud URL Shortener

A scalable URL shortener built on a three-tier architecture, deployable
across three AWS EC2 instances:

- **VM1** — Nginx reverse proxy (public entry point, serves the frontend)
- **VM2** — Flask REST API (URL shortening, redirects, analytics)
- **VM3** — MySQL database

See [docs/architecture.md](docs/architecture.md) for the full diagram and
request flow.

## Project structure

```
backend/            Flask app (app factory, models, routes, migrations, tests)
frontend/            Static HTML/CSS/JS UI
deployment/
  nginx/              VM1 Nginx site config
  systemd/            VM2 systemd unit for Gunicorn
  mysql/              VM3 schema bootstrap
  scripts/            Per-VM setup scripts + redeploy script
docs/                 Architecture, API, database, testing docs
```

## Features

- Shorten a URL to a 7-character code; resubmitting the same URL returns the
  existing code instead of creating a duplicate.
- Redirect endpoint tracks total clicks, created/last-accessed timestamps,
  and per-click IP address + User-Agent.
- URL validation (scheme + host required), rate limiting on the shorten
  endpoint, parameterized queries throughout (SQLAlchemy ORM), and
  XSS-safe frontend rendering (`textContent`, never `innerHTML`).
- Responsive UI with light/dark mode and a copy-to-clipboard button.

## Local development

```bash
cd backend
python -m venv venv
./venv/Scripts/activate            # Windows; use `source venv/bin/activate` on Linux/macOS
pip install -r requirements-dev.txt

export SQLALCHEMY_DATABASE_URI=sqlite:///dev.db   # no MySQL needed locally
export BASE_URL=http://localhost:5000
export FLASK_APP=wsgi.py

flask db upgrade      # apply migrations
python wsgi.py        # runs on http://localhost:5000
```

The frontend (`frontend/`) calls the API via relative paths (`/api/...`), so
for local testing it needs to be served from the same origin as the backend
(in production, Nginx does this). See [docs/testing.md](docs/testing.md) for
details and the automated test suite.

## Deploying to AWS EC2

1. Launch 3 EC2 instances (Ubuntu 22.04 LTS) in the same VPC. Only VM1 gets
   a public IP.
2. Configure security groups per [docs/architecture.md](docs/architecture.md#security-boundaries).
3. Copy this repo to each VM (`git clone` or `scp`/`rsync`), then run, in
   order:
   - `deployment/scripts/01_setup_vm3_mysql.sh` on VM3
   - `deployment/scripts/02_setup_vm2_backend.sh` on VM2 (edit
     `backend/.env` with real `DB_HOST`/`DB_PASSWORD`/`SECRET_KEY`/`BASE_URL`
     before running the migration step it prints)
   - `deployment/scripts/03_setup_vm1_nginx.sh` on VM1 (edit
     `deployment/nginx/urlshortener.conf`'s `VM2_PRIVATE_IP` first)
4. Redeploy backend changes later with `deployment/scripts/deploy_backend.sh`.

This setup runs over plain HTTP. Once you have a domain name, add TLS via
Certbot/Let's Encrypt in front of the Nginx config on VM1.

## Documentation

- [Architecture](docs/architecture.md)
- [API reference](docs/api.md)
- [Database schema](docs/database.md)
- [Testing guide](docs/testing.md)
