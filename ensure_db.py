#!/usr/bin/env python3
"""
Ensure database is initialized before starting the app
This runs as part of the startup process
"""

import os
import sys

def ensure_database():
    """Ensure database is properly initialized"""
    try:
        print("🔍 Checking database initialization...")
        
        from app import create_app
        from app.models import db, User, Category
        
        app = create_app(os.environ.get('FLASK_ENV', 'production'))
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables ensured")
            
            # Check and create admin user
            if User.query.count() == 0:
                admin_user = User(
                    name='Administrator',
                    email='admin@emdadglobal.com',
                    role='admin'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                print("✅ Created admin user")
            
            # Check and create basic categories
            if Category.query.count() == 0:
                categories = [
                    {'key': 'citrus', 'name_en': 'Citrus Fruits', 'name_ar': 'الحمضيات', 'slug': 'citrus-fruits'},
                    {'key': 'fresh-fruits', 'name_en': 'Fresh Fruits', 'name_ar': 'الفواكه الطازجة', 'slug': 'fresh-fruits'},
                    {'key': 'vegetables', 'name_en': 'Fresh Vegetables', 'name_ar': 'الخضروات الطازجة', 'slug': 'fresh-vegetables'},
                    {'key': 'frozen', 'name_en': 'Frozen Fruits', 'name_ar': 'الفواكه المجمدة', 'slug': 'frozen-fruits'}
                ]
                
                for i, cat_data in enumerate(categories):
                    category = Category(
                        key=cat_data['key'],
                        name_en=cat_data['name_en'],
                        name_ar=cat_data['name_ar'],
                        slug=cat_data['slug'],
                        sort_order=i + 1,
                        is_active=True
                    )
                    db.session.add(category)
                print("✅ Created basic categories")
            
            db.session.commit()
            print("✅ Database initialization verified")
            
            # Test a simple query
            category_count = Category.query.count()
            print(f"✅ Database test successful - {category_count} categories found")
            
            return True
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = ensure_database()
    if not success:
        print("❌ Database initialization failed!")
        sys.exit(1)
    else:
        print("✅ Database is ready!")
        sys.exit(0)
