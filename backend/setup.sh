#!/bin/bash

# Notes API Setup Script
# This script helps set up the FastAPI backend for the notes application

set -e  # Exit on any error

echo "🚀 Setting up Notes API Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Environment file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please update .env file with your Firebase credentials before running the API."
fi

# Create directories if they don't exist
mkdir -p logs

echo "✅ Setup completed successfully!"
echo ""
echo "🔧 Next steps:"
echo "1. Update the .env file with your Firebase credentials"
echo "2. Run the API with: python run.py"
echo "3. Open http://localhost:8000/docs to view the API documentation"
echo ""
echo "📚 For more information, see README.md and FLUTTER_INTEGRATION.md"
