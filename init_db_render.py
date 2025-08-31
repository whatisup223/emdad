#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""

import sys

def init_database():
    """Initialize database for production"""
    try:
        import os

        # Ensure temp directory is writable
        os.makedirs('/tmp', exist_ok=True)

        # Test write permissions and set appropriate database URL
        db_paths = [
            '/tmp/emdad_global.db',
            './emdad_global.db',
            'emdad_global.db'
        ]

        database_url = None
        for db_path in db_paths:
            try:
                # Test if we can create a file in this location
                test_path = db_path.replace('.db', '_test.db')
                with open(test_path, 'w') as f:
                    f.write('test')
                os.remove(test_path)
                database_url = f'sqlite:///{db_path}'
                print(f"✅ Using database path: {db_path}")
                break
            except Exception as e:
                print(f"⚠️ Cannot write to {db_path}: {e}")
                continue

        if database_url:
            os.environ['DATABASE_URL'] = database_url
        else:
            # Last resort - in-memory database
            os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
            print("⚠️ Using in-memory database as fallback")

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
