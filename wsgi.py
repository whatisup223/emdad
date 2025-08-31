#!/usr/bin/env python3
"""
WSGI entry point for Emdad Global application
This file is used by Gunicorn to start the application
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import at module level
try:
    from app import create_app
    # Import specific models to ensure they're registered
    import app.models  # noqa: F401

    # Create app instance
    flask_env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(flask_env)

    print(f"✅ Flask app created successfully in {flask_env} mode")

except Exception as e:
    print(f"❌ Failed to create Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

# For Gunicorn compatibility
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    application.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
