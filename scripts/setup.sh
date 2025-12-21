#!/bin/bash

# Setup script for S3 Storage Cost Optimization project

set -e

echo "=================================="
echo "S3 Storage Cost Optimization Setup"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Install development dependencies
echo ""
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Create config template
echo ""
echo "Creating configuration template..."
cat > config.template.json << EOF
{
  "aws": {
    "region": "us-east-1",
    "profile": null
  },
  "lifecycle": {
    "standard_ia_days": 30,
    "glacier_days": 90,
    "deep_archive_days": 180,
    "expiration_days": 365
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  },
  "monitoring": {
    "enabled": true,
    "interval_hours": 24
  }
}
EOF

echo "Configuration template created: config.template.json"

# Run tests
echo ""
echo "Running tests..."
python -m pytest tests/unit/ -v

echo ""
echo "=================================="
echo "Setup completed successfully!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Copy config.template.json to config.json and customize"
echo "3. Configure AWS credentials (aws configure)"
echo "4. Run examples: python examples/basic_usage.py"
echo ""
