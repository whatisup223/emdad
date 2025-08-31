#!/bin/bash

# Exit on any error
set -e

echo "Starting build process..."

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads/news
mkdir -p uploads/products
mkdir -p uploads/gallery
mkdir -p instance/uploads

# Set proper permissions
chmod -R 755 uploads/
chmod -R 755 instance/

# Initialize database
echo "Initializing database..."
python -c "
from app import create_app
from app.models import db
import os

app = create_app(os.environ.get('FLASK_ENV', 'production'))
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"

# Compile translations
echo "Compiling translations..."
if [ -d "translations" ]; then
    python -c "
from flask_babel import Babel
from app import create_app
import os

app = create_app(os.environ.get('FLASK_ENV', 'production'))
babel = Babel(app)

# Compile all translation files
import subprocess
import glob

po_files = glob.glob('translations/*/LC_MESSAGES/*.po')
for po_file in po_files:
    mo_file = po_file.replace('.po', '.mo')
    subprocess.run(['msgfmt', '-o', mo_file, po_file], check=False)
    print(f'Compiled {po_file} to {mo_file}')
"
fi

echo "Build completed successfully!"
