#!/usr/bin/env bash
# Run on VM3 (Ubuntu 22.04 LTS EC2 instance). Installs MySQL Server and
# loads the schema. Security-group note: only allow inbound 3306 from
# VM2's private IP/security group, never from 0.0.0.0/0.
set -euo pipefail

sudo apt-get update
sudo apt-get install -y mysql-server

# Allow connections from VM2 (adjust bind-address; default is 127.0.0.1 only).
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo systemctl restart mysql
sudo systemctl enable mysql

echo "Loading schema (using sudo mysql, which authenticates via the root unix socket)."
sudo mysql < "$(dirname "$0")/../mysql/schema.sql"

echo "Done. Edit the schema.sql-created user password if you haven't already,"
echo "and make sure the EC2 security group for VM3 only allows port 3306 from VM2."
