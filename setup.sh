#!/bin/bash

# BonziAssist Setup Script
# Checks Python, creates .env, and installs dependencies

set -e

echo "=== BonziAssist Setup ==="

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Found Python $PYTHON_VERSION"

# Create .env file from template if it doesn't exist
echo "Setting up .env file..."
if [ -f "helpers/.env" ]; then
    echo "helpers/.env already exists. Skipping..."
else
    if [ -f "helpers/.env.template" ]; then
        cp helpers/.env.template helpers/.env
        echo "Created helpers/.env from template"
    else
        mkdir -p helpers
        cat > helpers/.env << 'EOF'
# Add your GROQ API key here
GROQ_API_KEY=your_api_key_here
EOF
        echo "Created helpers/.env"
    fi
    echo "Please edit helpers/.env and add your GROQ_API_KEY"
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=== Setup Complete ==="
echo "Next steps:"
echo "1. Edit helpers/.env with your GROQ_API_KEY"
echo "2. Run: python3 main.py"
echo "The Vosk model will download automatically on first run."
