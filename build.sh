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
mkdir -p uploads/categories
mkdir -p uploads/gallery
mkdir -p instance/uploads/news
mkdir -p instance/uploads/products
mkdir -p instance/uploads/categories
mkdir -p instance/uploads/gallery
mkdir -p instance/uploads/rfq
mkdir -p instance/uploads/editor
mkdir -p instance
mkdir -p /tmp
mkdir -p static/images/samples

# Test database directory permissions
echo "🔍 Testing database directory permissions..."
touch /tmp/test_db.db && rm -f /tmp/test_db.db && echo "✅ /tmp is writable" || echo "❌ /tmp is not writable"

# Sample images are now created automatically in init_db_render.py
echo "🖼️ Sample images will be created during database initialization..."

# Initialize database
echo "🗄️ Initializing database..."
if python3.11 init_db_render.py; then
    echo "✅ Database initialized with python3.11"
elif python3 init_db_render.py; then
    echo "✅ Database initialized with python3"
else
    echo "❌ Database initialization failed"
    exit 1
fi

echo "✅ Build completed successfully!"
