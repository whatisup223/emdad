#!/usr/bin/env python3
"""
Test upload directories and image system
"""

import os
from app import create_app, db
from app.models import Product, ProductImage, Category, News

def test_upload_system():
    """Test upload system"""
    app = create_app()
    
    with app.app_context():
        print("=== Testing Upload System ===")
        
        # Check upload directories
        upload_path = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
        print(f"Upload path: {upload_path}")
        print(f"Path exists: {os.path.exists(upload_path)}")
        
        for subdir in ['categories', 'products', 'news', 'gallery']:
            subdir_path = os.path.join(upload_path, subdir)
            exists = os.path.exists(subdir_path)
            print(f"{subdir}: {'exists' if exists else 'missing'}")
            if exists:
                files = os.listdir(subdir_path)
                print(f"  - Files: {len(files)}")
        
        # Check products
        print("\n=== Testing Products ===")
        products = Product.query.filter_by(status='active').limit(3).all()
        print(f"Products: {len(products)}")
        
        for prod in products:
            main_image = prod.get_main_image()
            if main_image:
                print(f"✅ {prod.name_en}: {main_image.filename}")
            else:
                print(f"❌ {prod.name_en}: No main image")
        
        # Check categories
        print("\n=== Testing Categories ===")
        categories = Category.query.filter_by(is_active=True).limit(3).all()
        for cat in categories:
            if cat.image_path:
                print(f"✅ {cat.name_en}: {cat.image_path}")
            else:
                print(f"❌ {cat.name_en}: No image")
        
        # Check news
        print("\n=== Testing News ===")
        news_items = News.query.filter_by(status='published').limit(3).all()
        for article in news_items:
            if article.cover_image:
                print(f"✅ {article.title_en[:30]}...: {article.cover_image}")
            else:
                print(f"❌ {article.title_en[:30]}...: No cover image")

if __name__ == '__main__':
    test_upload_system()
