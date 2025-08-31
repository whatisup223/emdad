#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""

import sys

def init_database():
    """Initialize database for production"""
    try:
        import os

        # Ensure instance directory exists
        os.makedirs('instance', exist_ok=True)

        print("Creating Flask app...")
        from app import create_app
        app = create_app('production')

        print("Initializing database...")
        with app.app_context():
            from app.models import db, User
            # Import all models to ensure they're registered
            import app.models  # noqa: F401

            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")

            # Check if admin user exists
            try:
                admin_user = User.query.filter_by(email='admin@emdadglobal.com').first()
                if not admin_user:
                    print("Creating admin user...")
                    admin_user = User(
                        name='Administrator',
                        email='admin@emdadglobal.com',
                        role='admin'
                    )
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)
                    db.session.commit()
                    print("✅ Admin user created successfully!")
                else:
                    print("✅ Admin user already exists")
            except Exception as user_error:
                print(f"⚠️ Admin user creation skipped: {user_error}")

            print("✅ Database initialization completed!")
            return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
