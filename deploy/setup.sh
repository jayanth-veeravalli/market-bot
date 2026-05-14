#!/bin/bash
set -e

echo "=== Market Bot GCP Setup ==="

# Install system dependencies
sudo apt-get update -q
sudo apt-get install -y -q python3 python3-pip curl git

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Create dedicated user and app directory
sudo useradd -r -s /bin/false market-bot || true
sudo mkdir -p /opt/market-bot
sudo chown market-bot:market-bot /opt/market-bot

# Clone the repo
sudo -u market-bot git clone https://github.com/jayanth-veeravalli/market-bot.git /opt/market-bot

# Install Python dependencies
cd /opt/market-bot
sudo -u market-bot /home/$USER/.local/bin/uv sync

# Set up .env
if [ ! -f /opt/market-bot/.env ]; then
    sudo cp /opt/market-bot/.env.sample /opt/market-bot/.env
    echo ""
    echo "⚠️  Fill in /opt/market-bot/.env with your credentials, then run:"
    echo "    sudo systemctl start market-bot"
else
    echo ".env already exists, skipping."
fi

# Install and enable systemd service
sudo cp /opt/market-bot/deploy/market-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable market-bot

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. sudo nano /opt/market-bot/.env   (fill in your credentials)"
echo "  2. sudo systemctl start market-bot"
echo "  3. sudo systemctl status market-bot"
