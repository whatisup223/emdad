#!/usr/bin/env python3
"""
Automatically fix all WebP image issues in production.
This script runs during deployment and ensures all 28 products have working WebP images.
NO MANUAL INTERVENTION REQUIRED.
"""

import os
import sys
import shutil
import json
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def auto_fix_production_images():
    """Automatically fix all production image issues."""
    
    print("🔧 AUTO-FIXING PRODUCTION IMAGES...")
    print("=" * 60)
    
    try:
        # Step 1: Read seeds file
        print("📋 Step 1: Reading products from seeds...")
        seeds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'seeds', 'products.json')
        
        if not os.path.exists(seeds_path):
            print(f"❌ CRITICAL: Seeds file not found: {seeds_path}")
            return False
        
        with open(seeds_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products_data = data.get('products', [])
        print(f"✅ Found {len(products_data)} products in seeds")
        
        if len(products_data) != 28:
            print(f"⚠️ WARNING: Expected 28 products, found {len(products_data)}")
        
        # Step 2: Setup directories
        print("\n📁 Step 2: Setting up directories...")
        
        # Multiple static directory candidates for robustness
        static_candidates = [
            os.path.join(os.getcwd(), 'static', 'uploads', 'products'),
            os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'products'),
            os.path.join('/opt', 'render', 'project', 'src', 'static', 'uploads', 'products'),  # Render path
        ]
        
        static_dir = None
        for candidate in static_candidates:
            abs_candidate = os.path.abspath(candidate)
            if os.path.exists(abs_candidate):
                try:
                    webp_files = [f for f in os.listdir(abs_candidate) if f.endswith('.webp')]
                    if webp_files:
                        static_dir = abs_candidate
                        print(f"✅ Using static directory: {static_dir}")
                        print(f"   Found {len(webp_files)} WebP files")
                        break
                    else:
                        print(f"⚠️ Directory exists but no WebP files: {abs_candidate}")
                        # List all files for debugging
                        all_files = os.listdir(abs_candidate)
                        print(f"   Files found: {len(all_files)}")
                        webp_count = sum(1 for f in all_files if f.endswith('.webp'))
                        svg_count = sum(1 for f in all_files if f.endswith('.svg'))
                        print(f"   WebP: {webp_count}, SVG: {svg_count}")
                        if webp_count > 0:
                            static_dir = abs_candidate
                            print(f"✅ Using directory anyway: {static_dir}")
                            break
                except Exception as e:
                    print(f"⚠️ Error reading directory {abs_candidate}: {e}")
                    continue

        if not static_dir:
            print("❌ CRITICAL: No static directory with WebP files found!")
            print("Available directories:")
            for candidate in static_candidates:
                abs_candidate = os.path.abspath(candidate)
                exists = os.path.exists(abs_candidate)
                if exists:
                    try:
                        files = os.listdir(abs_candidate)
                        webp_count = sum(1 for f in files if f.endswith('.webp'))
                        print(f"  - {abs_candidate}: EXISTS ({len(files)} files, {webp_count} WebP)")
                    except:
                        print(f"  - {abs_candidate}: EXISTS (cannot read)")
                else:
                    print(f"  - {abs_candidate}: NOT FOUND")
            return False
        
        # Instance directory
        instance_candidates = [
            os.path.join(os.getcwd(), 'instance', 'uploads', 'products'),
            os.path.join('/tmp', 'instance', 'uploads', 'products'),  # Render fallback
        ]
        
        instance_dir = None
        for candidate in instance_candidates:
            abs_candidate = os.path.abspath(candidate)
            try:
                os.makedirs(abs_candidate, exist_ok=True)
                # Test write permission
                test_file = os.path.join(abs_candidate, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                instance_dir = abs_candidate
                print(f"✅ Using instance directory: {instance_dir}")
                break
            except Exception as e:
                print(f"⚠️ Cannot use {abs_candidate}: {e}")
                continue
        
        if not instance_dir:
            print("❌ CRITICAL: Cannot create writable instance directory!")
            return False
        
        # Step 3: Copy all WebP images
        print("\n📋 Step 3: Copying WebP images...")
        
        copied_count = 0
        failed_count = 0
        
        for product_data in products_data:
            slug = product_data['slug']
            expected_filename = product_data.get('image_filename', f"{slug}-emdad-global.webp")
            
            static_path = os.path.join(static_dir, expected_filename)
            instance_path = os.path.join(instance_dir, expected_filename)
            
            if os.path.exists(static_path):
                try:
                    # Always copy to ensure latest version
                    shutil.copy2(static_path, instance_path)
                    copied_count += 1
                    print(f"✅ Copied: {expected_filename}")
                except Exception as e:
                    print(f"❌ Failed to copy {expected_filename}: {e}")
                    failed_count += 1
            else:
                print(f"⚠️ Missing in static: {expected_filename}")
                failed_count += 1
        
        print(f"\n📊 Copy Results: {copied_count} copied, {failed_count} failed")
        
        # Step 4: Fix database
        print("\n🗄️ Step 4: Fixing database records...")
        
        try:
            from app import create_app
            from app.models import Product, ProductImage, Category, db
            
            # Try production config first, fallback to development
            try:
                app = create_app('production')
            except:
                app = create_app('development')
            
            with app.app_context():
                products = Product.query.all()
                print(f"📊 Found {len(products)} products in database")
                
                fixed_count = 0
                
                for product in products:
                    changes_made = False
                    
                    # Ensure image_path is WebP
                    expected_filename = f"{product.slug}-emdad-global.webp"
                    
                    if not product.image_path or not product.image_path.endswith('.webp'):
                        product.image_path = expected_filename
                        changes_made = True
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
                        changes_made = True
                        print(f"🆕 Created ProductImage for {product.slug}")
                    elif main_image.filename != product.image_path:
                        main_image.filename = product.image_path
                        changes_made = True
                        print(f"🔧 Updated ProductImage for {product.slug}")
                    
                    if changes_made:
                        fixed_count += 1
                
                # Commit all changes
                db.session.commit()
                print(f"💾 Database changes committed ({fixed_count} products fixed)")
                
        except Exception as e:
            print(f"❌ Database fix failed: {e}")
            return False
        
        # Step 5: Final verification
        print("\n🔍 Step 5: Final verification...")
        
        # Check instance directory
        instance_webp_files = [f for f in os.listdir(instance_dir) if f.endswith('.webp')]
        print(f"📊 Instance directory has {len(instance_webp_files)} WebP files")
        
        # Check database again
        with app.app_context():
            products = Product.query.filter_by(status='active').all()
            products_with_webp = sum(1 for p in products if p.image_path and p.image_path.endswith('.webp'))
            products_with_main_image = sum(1 for p in products if p.get_main_image())
            
            print(f"📊 Database: {len(products)} products, {products_with_webp} with WebP, {products_with_main_image} with main image")
        
        # Success criteria
        success = (
            len(instance_webp_files) >= 28 and
            products_with_webp >= 28 and
            products_with_main_image >= 28
        )
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 AUTO-FIX COMPLETED SUCCESSFULLY!")
            print("✅ All 28 products ready with WebP images")
            print("✅ Production deployment can continue")
        else:
            print("❌ AUTO-FIX FAILED!")
            print(f"   Instance WebP files: {len(instance_webp_files)}/28")
            print(f"   Products with WebP: {products_with_webp}/28")
            print(f"   Products with main image: {products_with_main_image}/28")
        
        return success
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR in auto-fix: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = auto_fix_production_images()
    sys.exit(0 if success else 1)
