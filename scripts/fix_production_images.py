#!/usr/bin/env python3
"""
Fix production image issues by ensuring all 28 products have proper WebP images.
This script addresses the specific issue where products are created but images don't display.
"""

import os
import sys
import shutil
import json
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fix_production_images():
    """Fix production image issues."""
    
    print("🔧 Starting production image fix...")
    
    # Read the seeds file to get expected products
    seeds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'seeds', 'products.json')
    if not os.path.exists(seeds_path):
        print(f"❌ Seeds file not found: {seeds_path}")
        return False
    
    with open(seeds_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products_data = data.get('products', [])
    print(f"📊 Found {len(products_data)} products in seeds file")
    
    # Define directories
    static_dir = os.path.join(os.getcwd(), 'static', 'uploads', 'products')
    instance_dir = os.path.join(os.getcwd(), 'instance', 'uploads', 'products')
    
    # Ensure directories exist
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(instance_dir, exist_ok=True)
    
    print(f"📁 Static directory: {static_dir}")
    print(f"📁 Instance directory: {instance_dir}")
    
    # Check what's in static directory
    if os.path.exists(static_dir):
        static_files = [f for f in os.listdir(static_dir) if f.endswith('.webp')]
        print(f"📋 Found {len(static_files)} WebP files in static directory")
    else:
        static_files = []
        print("⚠️ Static directory does not exist")
    
    # Check what's in instance directory
    if os.path.exists(instance_dir):
        instance_files = [f for f in os.listdir(instance_dir) if f.endswith('.webp')]
        print(f"📋 Found {len(instance_files)} WebP files in instance directory")
    else:
        instance_files = []
        print("⚠️ Instance directory does not exist")
    
    # Process each product from seeds
    missing_images = []
    copied_images = []
    
    for product_data in products_data:
        slug = product_data['slug']
        expected_filename = product_data.get('image_filename', f"{slug}-emdad-global.webp")
        
        static_path = os.path.join(static_dir, expected_filename)
        instance_path = os.path.join(instance_dir, expected_filename)
        
        # Check if image exists in static
        if os.path.exists(static_path):
            # Copy to instance if not exists or if static is newer
            if not os.path.exists(instance_path) or os.path.getmtime(static_path) > os.path.getmtime(instance_path):
                try:
                    shutil.copy2(static_path, instance_path)
                    copied_images.append(expected_filename)
                    print(f"✅ Copied {expected_filename}")
                except Exception as e:
                    print(f"❌ Failed to copy {expected_filename}: {e}")
            else:
                print(f"✓ {expected_filename} already exists in instance")
        else:
            missing_images.append((slug, expected_filename))
            print(f"⚠️ Missing image: {expected_filename}")
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"✅ Images copied: {len(copied_images)}")
    print(f"⚠️ Missing images: {len(missing_images)}")
    
    if missing_images:
        print(f"\n📋 Missing images:")
        for slug, filename in missing_images:
            print(f"  - {slug}: {filename}")
    
    if copied_images:
        print(f"\n📋 Copied images:")
        for filename in copied_images:
            print(f"  - {filename}")
    
    # Now fix the database
    try:
        from app import create_app
        from app.models import Product, ProductImage, Category, db
        
        app = create_app('production')
        
        with app.app_context():
            print(f"\n🗄️ Fixing database records...")
            
            products = Product.query.all()
            print(f"📊 Found {len(products)} products in database")
            
            fixed_count = 0
            
            for product in products:
                # Ensure image_path is set to WebP
                expected_filename = f"{product.slug}-emdad-global.webp"
                
                if not product.image_path or not product.image_path.endswith('.webp'):
                    product.image_path = expected_filename
                    fixed_count += 1
                    print(f"🔧 Fixed image_path for {product.slug}")
                
                # Ensure ProductImage record exists
                main_image = product.images.filter_by(is_main=True).first()
                if not main_image:
                    main_image = ProductImage(
                        product_id=product.id,
                        filename=product.image_path,
                        alt_text_en=product.name_en,
                        alt_text_ar=product.name_ar,
                        is_main=True,
                        sort_order=0
                    )
                    db.session.add(main_image)
                    fixed_count += 1
                    print(f"🆕 Created ProductImage for {product.slug}")
                elif main_image.filename != product.image_path:
                    main_image.filename = product.image_path
                    fixed_count += 1
                    print(f"🔧 Updated ProductImage for {product.slug}")
            
            # Commit changes
            db.session.commit()
            print(f"💾 Database changes committed ({fixed_count} fixes)")
            
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False
    
    print(f"\n✅ Production image fix completed!")
    return len(missing_images) == 0

if __name__ == '__main__':
    success = fix_production_images()
    sys.exit(0 if success else 1)
