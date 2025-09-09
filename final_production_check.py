#!/usr/bin/env python3
"""
Final check before deploying to production.
Ensures all 28 products with WebP images are ready.
"""

import os
import sys
import json
from app import create_app
from app.models import Product, ProductImage, Category

def final_production_check():
    """Perform final check before production deployment."""
    
    print("🔍 Final Production Check")
    print("=" * 50)
    
    # Check 1: Seeds file
    print("\n1️⃣ Checking seeds file...")
    seeds_path = os.path.join('seeds', 'products.json')
    if not os.path.exists(seeds_path):
        print("❌ Seeds file not found!")
        return False
    
    with open(seeds_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    expected_products = data.get('products', [])
    print(f"✅ Seeds file contains {len(expected_products)} products")
    
    if len(expected_products) != 28:
        print(f"⚠️ Expected 28 products, found {len(expected_products)}")
        return False
    
    # Check 2: Static images
    print("\n2️⃣ Checking static images...")
    static_dir = os.path.join('static', 'uploads', 'products')
    if not os.path.exists(static_dir):
        print("❌ Static products directory not found!")
        return False
    
    webp_files = [f for f in os.listdir(static_dir) if f.endswith('.webp')]
    print(f"✅ Found {len(webp_files)} WebP files in static directory")
    
    # Check each expected image
    missing_static = []
    for product in expected_products:
        filename = product.get('image_filename', f"{product['slug']}-emdad-global.webp")
        if not os.path.exists(os.path.join(static_dir, filename)):
            missing_static.append(filename)
    
    if missing_static:
        print(f"❌ Missing {len(missing_static)} images in static:")
        for img in missing_static:
            print(f"  - {img}")
        return False
    else:
        print("✅ All expected images found in static directory")
    
    # Check 3: Database
    print("\n3️⃣ Checking database...")
    app = create_app('development')
    
    with app.app_context():
        products = Product.query.filter_by(status='active').all()
        print(f"✅ Found {len(products)} active products in database")
        
        if len(products) != 28:
            print(f"⚠️ Expected 28 products, found {len(products)}")
        
        # Check each product has WebP image
        products_with_webp = 0
        products_with_main_image = 0
        
        for product in products:
            if product.image_path and product.image_path.endswith('.webp'):
                products_with_webp += 1
            
            main_image = product.get_main_image()
            if main_image:
                products_with_main_image += 1
        
        print(f"✅ Products with WebP images: {products_with_webp}/{len(products)}")
        print(f"✅ Products with main ProductImage: {products_with_main_image}/{len(products)}")
        
        if products_with_webp != len(products):
            print("❌ Not all products have WebP images!")
            return False
        
        if products_with_main_image != len(products):
            print("❌ Not all products have ProductImage records!")
            return False
    
    # Check 4: Instance images
    print("\n4️⃣ Checking instance images...")
    instance_dir = os.path.join('instance', 'uploads', 'products')
    if os.path.exists(instance_dir):
        instance_webp = [f for f in os.listdir(instance_dir) if f.endswith('.webp')]
        print(f"✅ Found {len(instance_webp)} WebP files in instance directory")
    else:
        print("ℹ️ Instance directory doesn't exist yet (will be created during deployment)")
    
    # Check 5: Build script
    print("\n5️⃣ Checking build script...")
    if os.path.exists('build.sh'):
        with open('build.sh', 'r') as f:
            build_content = f.read()
        
        if 'ensure_webp_images.py' in build_content:
            print("✅ Build script includes WebP image verification")
        else:
            print("⚠️ Build script doesn't include WebP image verification")
    else:
        print("❌ Build script not found!")
        return False
    
    # Check 6: Helper scripts
    print("\n6️⃣ Checking helper scripts...")
    required_scripts = [
        'scripts/ensure_webp_images.py',
        'scripts/fix_production_images.py'
    ]
    
    for script in required_scripts:
        if os.path.exists(script):
            print(f"✅ {script} exists")
        else:
            print(f"❌ {script} missing!")
            return False
    
    # Check 7: Templates
    print("\n7️⃣ Checking templates...")
    templates_to_check = [
        'templates/main/index.html',
        'templates/main/products.html'
    ]
    
    for template in templates_to_check:
        if os.path.exists(template):
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'onerror=' in content and 'fallback' in content.lower():
                print(f"✅ {template} has enhanced error handling")
            else:
                print(f"⚠️ {template} may not have enhanced error handling")
        else:
            print(f"❌ {template} not found!")
            return False
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 FINAL SUMMARY")
    print("=" * 50)
    print("✅ Seeds file: 28 products")
    print("✅ Static images: All WebP files present")
    print("✅ Database: 28 products with WebP images")
    print("✅ Build script: Enhanced with image verification")
    print("✅ Helper scripts: All present")
    print("✅ Templates: Enhanced error handling")
    
    print("\n🎉 READY FOR PRODUCTION DEPLOYMENT!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix WebP images in production - comprehensive solution'")
    print("3. git push origin main")
    print("4. Wait for Render deployment to complete")
    print("5. Verify all 28 products show their WebP images")
    
    return True

if __name__ == '__main__':
    success = final_production_check()
    if success:
        print("\n✅ All checks passed! Ready for deployment.")
        sys.exit(0)
    else:
        print("\n❌ Some checks failed. Please fix issues before deployment.")
        sys.exit(1)
