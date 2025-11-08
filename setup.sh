#!/bin/bash
# Setup script for Oxford Debate Agent

echo "🎭 Setting up Oxford Debate Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for config
if [ ! -f "config/secrets/config.json" ]; then
    echo ""
    echo "⚠️  WARNING: API configuration not found!"
    echo "Please copy your OpenAI config.json to config/secrets/config.json"
    echo ""
    echo "Example:"
    echo "  cp /path/to/your/config.json config/secrets/config.json"
    echo ""
else
    echo "✅ API configuration found."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "To generate a debate, run:"
echo "  python src/main.py --motion \"Your debate motion here\""
echo ""
