#!/usr/bin/env bash
# BonziAssist setup script
set -e

echo "=== BonziAssist Setup ==="

# Check Python
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required. Install from https://www.python.org/downloads/"; exit 1; }

# Check for .env
if [ ! -f helpers/.env ]; then
    echo ""
    echo "Creating helpers/.env from template..."
    cp helpers/.env.example helpers/.env
    echo "Please edit helpers/.env and set your GROQ_API_KEY"
    echo "Get a key at: https://console.groq.com/keys"
    echo ""
fi

# Install deps
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Done! Run: python3 main.py"
