#!/usr/bin/env bash
# Run on VM1 (Ubuntu 22.04 LTS EC2 instance) after copying the repo's
# frontend/ directory to this VM (e.g. via git clone or scp/rsync).
# Edit deployment/nginx/urlshortener.conf to set VM2_PRIVATE_IP before running.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir -p /var/www/urlshortener
sudo cp -r "$REPO_DIR"/frontend/* /var/www/urlshortener/
sudo chown -R www-data:www-data /var/www/urlshortener

sudo cp "$REPO_DIR/deployment/nginx/urlshortener.conf" /etc/nginx/sites-available/urlshortener.conf
sudo ln -sf /etc/nginx/sites-available/urlshortener.conf /etc/nginx/sites-enabled/urlshortener.conf
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "Nginx configured. Make sure /etc/nginx/sites-available/urlshortener.conf"
echo "has VM2_PRIVATE_IP replaced with VM2's actual private IP address."
