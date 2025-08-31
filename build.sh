#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Render build process..."

# Force Python 3.11
export PYTHON_VERSION=3.11.9
echo "🐍 Using Python $PYTHON_VERSION"

# Check Python version
python3.11 --version || python3 --version || python --version

# Upgrade pip and install dependencies
echo "📦 Installing Python dependencies..."
python3.11 -m pip install --upgrade pip setuptools wheel || python3 -m pip install --upgrade pip setuptools wheel
python3.11 -m pip install -r requirements.txt || python3 -m pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads/news
mkdir -p uploads/products
mkdir -p uploads/gallery
mkdir -p instance/uploads
mkdir -p instance
mkdir -p /tmp

# Test database directory permissions
echo "🔍 Testing database directory permissions..."
touch /tmp/test_db.db && rm -f /tmp/test_db.db && echo "✅ /tmp is writable" || echo "❌ /tmp is not writable"

# Initialize database
echo "🗄️ Initializing database..."
python3.11 init_db_render.py || python3 init_db_render.py

echo "✅ Build completed successfully!"
