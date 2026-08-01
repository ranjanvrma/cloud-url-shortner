#!/usr/bin/env bash
# Redeploy script for VM2: pulls latest code, installs dependencies,
# runs migrations, and restarts the service. Run from /opt/urlshortener.
set -euo pipefail

APP_DIR=/opt/urlshortener/backend

cd /opt/urlshortener
sudo -u urlshortener git pull

cd "$APP_DIR"
sudo -u urlshortener ./venv/bin/pip install -r requirements.txt

sudo -u urlshortener bash -c "cd $APP_DIR && set -a && source .env && set +a && FLASK_APP=wsgi.py ./venv/bin/flask db upgrade"

sudo systemctl restart urlshortener
sudo systemctl status urlshortener --no-pager
