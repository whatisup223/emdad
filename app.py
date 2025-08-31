#!/usr/bin/env python3
"""
WSGI entry point for Emdad Global application
"""

from flask import send_from_directory
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the app package (not this file)
    import app as app_package
    # Import models to ensure they are registered with SQLAlchemy
    import app.models  # noqa: F401

    # Create app instance
    flask_app = app_package.create_app(os.environ.get('FLASK_ENV', 'production'))

    print(f"✅ Flask app created successfully in {os.environ.get('FLASK_ENV', 'production')} mode")

except Exception as e:
    print(f"❌ Failed to create Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

@flask_app.route('/logo.png')
def logo_file():
    """Serve logo file directly."""
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    try:
        return send_from_directory(upload_path, 'logo.png')
    except FileNotFoundError:
        # If logo not found, return 404 error
        from flask import abort
        abort(404)

@flask_app.route('/bg.webp')
def hero_bg_file():
    """Serve hero background file directly."""
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    try:
        return send_from_directory(upload_path, 'bg.webp')
    except FileNotFoundError:
        # If background image not found, return 404 error
        from flask import abort
        abort(404)

if __name__ == '__main__':
    # Run the application for local development only
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"🚀 Starting Flask development server on port {port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"🌐 Access the application at: http://localhost:{port}")

    flask_app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
