#!/usr/bin/env bash
# Run on VM2 (Ubuntu 22.04 LTS EC2 instance) after copying the repo to
# /opt/urlshortener (e.g. via git clone or scp/rsync).
# Security-group note: only allow inbound 8000 from VM1's private IP/security
# group, never from 0.0.0.0/0.
set -euo pipefail

APP_DIR=/opt/urlshortener/backend

sudo apt-get update
sudo apt-get install -y python3-venv python3-pip

if ! id urlshortener &>/dev/null; then
    sudo useradd --system --home /opt/urlshortener --shell /usr/sbin/nologin urlshortener
fi

sudo mkdir -p /opt/urlshortener
sudo chown -R urlshortener:urlshortener /opt/urlshortener

cd "$APP_DIR"
sudo -u urlshortener python3 -m venv venv
sudo -u urlshortener ./venv/bin/pip install --upgrade pip
sudo -u urlshortener ./venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
    sudo -u urlshortener cp .env.example .env
    echo "Created .env from .env.example — edit /opt/urlshortener/backend/.env"
    echo "with real DB_HOST, DB_PASSWORD, SECRET_KEY, and BASE_URL before continuing."
fi

sudo -u urlshortener mkdir -p logs

echo "Once .env is configured and VM3 is reachable, run the migration as the"
echo "urlshortener user:"
echo "  sudo -u urlshortener bash -c 'cd $APP_DIR && set -a && source .env && set +a && FLASK_APP=wsgi.py ./venv/bin/flask db upgrade'"

sudo cp ../deployment/systemd/urlshortener.service /etc/systemd/system/urlshortener.service
sudo systemctl daemon-reload
sudo systemctl enable urlshortener
echo "Service installed. Start it with: sudo systemctl start urlshortener"
