#!/usr/bin/env python3
"""
Test the production setup to ensure all 28 products with WebP images work correctly.
"""

import os
import sys
from app import create_app
from app.models import Product, ProductImage, Category

def test_production_setup():
    """Test that production setup is correct."""
    
    print("🧪 Testing production setup...")
    
    app = create_app('production')
    
    with app.app_context():
        # Test 1: Check total products
        products = Product.query.filter_by(status='active').all()
        print(f"📊 Total active products: {len(products)}")
        
        if len(products) != 28:
            print(f"⚠️ Expected 28 products, found {len(products)}")
        else:
            print("✅ Correct number of products (28)")
        
        # Test 2: Check each product has WebP image
        webp_count = 0
        missing_images = []
        
        for product in products:
            if product.image_path and product.image_path.endswith('.webp'):
                webp_count += 1
            else:
                missing_images.append(product.slug)
        
        print(f"📊 Products with WebP images: {webp_count}")
        
        if webp_count == len(products):
            print("✅ All products have WebP images")
        else:
            print(f"⚠️ {len(products) - webp_count} products missing WebP images")
            for slug in missing_images:
                print(f"  - {slug}")
        
        # Test 3: Check ProductImage records
        products_with_main_image = 0
        
        for product in products:
            main_image = product.get_main_image()
            if main_image:
                products_with_main_image += 1
        
        print(f"📊 Products with main ProductImage: {products_with_main_image}")
        
        if products_with_main_image == len(products):
            print("✅ All products have ProductImage records")
        else:
            print(f"⚠️ {len(products) - products_with_main_image} products missing ProductImage records")
        
        # Test 4: Check file system
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        instance_dir = os.path.join(app.instance_path, upload_folder, 'products')
        static_dir = os.path.join(os.getcwd(), 'static', 'uploads', 'products')
        
        instance_files = []
        static_files = []
        
        if os.path.exists(instance_dir):
            instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.webp')]
        
        if os.path.exists(static_dir):
            static_files = [f for f in os.listdir(static_dir) if f.endswith('.webp')]
        
        print(f"📊 WebP files in instance: {len(instance_files)}")
        print(f"📊 WebP files in static: {len(static_files)}")
        
        # Test 5: Check specific products from seeds
        expected_products = [
            'oranges', 'mandarins', 'tangerines', 'strawberries',
            'potatoes', 'sweet-potatoes', 'onions', 'garlic',
            'iqf-strawberries', 'iqf-mango',
            'dates-whole',
            'cumin-seed', 'coriander-seed', 'fennel-seed', 'caraway-seed',
            'sesame-seeds', 'flax-seeds',
            'anise-seed', 'basil', 'calendula', 'chamomile', 'dill',
            'lemongrass', 'marjoram', 'mint', 'parsley', 'sage', 'hibiscus'
        ]
        
        found_products = [p.slug for p in products]
        missing_expected = [slug for slug in expected_products if slug not in found_products]
        extra_products = [slug for slug in found_products if slug not in expected_products]
        
        print(f"📊 Expected products found: {len(expected_products) - len(missing_expected)}/{len(expected_products)}")
        
        if missing_expected:
            print(f"⚠️ Missing expected products:")
            for slug in missing_expected:
                print(f"  - {slug}")
        
        if extra_products:
            print(f"ℹ️ Extra products (not in expected list):")
            for slug in extra_products:
                print(f"  - {slug}")
        
        # Test 6: Check categories
        categories = Category.query.filter_by(is_active=True).all()
        print(f"📊 Active categories: {len(categories)}")
        
        category_product_counts = {}
        for product in products:
            cat = Category.query.get(product.category_id)
            if cat:
                category_product_counts[cat.key] = category_product_counts.get(cat.key, 0) + 1
        
        print(f"📊 Products by category:")
        for cat_key, count in category_product_counts.items():
            print(f"  - {cat_key}: {count}")
        
        # Overall assessment
        issues = 0
        
        if len(products) != 28:
            issues += 1
        
        if webp_count != len(products):
            issues += 1
        
        if products_with_main_image != len(products):
            issues += 1
        
        if missing_expected:
            issues += 1
        
        print(f"\n📊 Overall Assessment:")
        if issues == 0:
            print("✅ All tests passed! Production setup is correct.")
            return True
        else:
            print(f"⚠️ {issues} issues found. Production setup needs attention.")
            return False

if __name__ == '__main__':
    success = test_production_setup()
    sys.exit(0 if success else 1)
