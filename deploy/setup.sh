#!/bin/bash
set -e

echo "=== Market Bot GCP Setup ==="

# Wait for GCP's background apt process to finish
while fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
    echo "Waiting for apt lock..."
    sleep 5
done

# Install system dependencies
apt-get update -q
apt-get install -y -q python3 python3-pip curl git

# Install uv as root
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.local/bin:$PATH"

# Create dedicated user and app directory
useradd -r -s /bin/false market-bot || true
mkdir -p /opt/market-bot
chown market-bot:market-bot /opt/market-bot

# Clone the repo
sudo -u market-bot git clone https://github.com/jayanth-veeravalli/market-bot.git /opt/market-bot

# Install Python dependencies
cd /opt/market-bot
/root/.local/bin/uv sync

# Set up .env
if [ ! -f /opt/market-bot/.env ]; then
    cp /opt/market-bot/.env.sample /opt/market-bot/.env
fi

# Install and enable systemd service
cp /opt/market-bot/deploy/market-bot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable market-bot

echo "=== Setup complete ==="
