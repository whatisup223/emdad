#!/usr/bin/env python3
"""
Development server runner for Emdad Global website.
"""

from app import create_app

if __name__ == '__main__':
    # Create the Flask application
    app = create_app()
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
