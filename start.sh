#!/bin/bash

# Render startup script for Emdad Global
set -e

echo "🚀 Starting Emdad Global Application"
echo "=" * 50

# Set default PORT if not provided
export PORT=${PORT:-10000}
echo "🌐 Using PORT: $PORT"

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "🐍 Python path: $PYTHONPATH"

# Ensure database is ready
echo "🗄️ Ensuring database is ready..."
if python3.11 init_db_render.py; then
    echo "✅ Database is ready"
else
    echo "❌ Database initialization failed"
    exit 1
fi

# Test WSGI import
echo "🔍 Testing WSGI import..."
python3.11 -c "
import sys
print(f'Python version: {sys.version}')
try:
    from wsgi import app
    print('✅ WSGI import successful')
    print(f'App: {app}')
    print(f'App name: {app.name}')
except Exception as e:
    print(f'❌ WSGI import failed: {e}')
    import traceback
    traceback.print_exc()
    exit(1)
"

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
exec python3.11 -m gunicorn wsgi:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info
