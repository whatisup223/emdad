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

def create_application():
    """Create and configure the Flask application"""
    try:
        from app import create_app
        
        # Import all models to ensure they're registered
        from app.models import *
        
        # Create app instance
        flask_env = os.environ.get('FLASK_ENV', 'production')
        application = create_app(flask_env)
        
        print(f"✅ Flask app created successfully in {flask_env} mode")
        return application
        
    except Exception as e:
        print(f"❌ Failed to create Flask app: {e}")
        import traceback
        traceback.print_exc()
        raise

# Create the application instance
application = create_application()

# For Gunicorn compatibility
app = application

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    application.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
