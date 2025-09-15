#!/usr/bin/env python3
"""Check CSRF configuration."""

from app import create_app
from flask_wtf.csrf import generate_csrf

app = create_app()
with app.app_context():
    with app.test_request_context():
        try:
            token = generate_csrf()
            print(f"CSRF Token generated: {token[:20]}...")
            print(f"SECRET_KEY exists: {bool(app.config.get('SECRET_KEY'))}")
            print(f"WTF_CSRF_TIME_LIMIT: {app.config.get('WTF_CSRF_TIME_LIMIT')}")
            print("✅ CSRF configuration looks good")
        except Exception as e:
            print(f"❌ CSRF error: {e}")
