#!/usr/bin/env python3
"""
Ensure all products have WebP images in both static and instance directories.
This script should be run during deployment to guarantee image availability.
"""

import os
import sys
import shutil
from pathlib import Path

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import Product, ProductImage, Category

def ensure_webp_images():
    """Ensure all products have WebP images available."""
    
    app = create_app('production')
    
    with app.app_context():
        print("🔍 Checking WebP images for all products...")
        
        # Get all products
        products = Product.query.filter_by(status='active').order_by(Product.category_id, Product.sort_order).all()
        print(f"📊 Found {len(products)} active products")
        
        # Define directories
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        instance_dir = os.path.join(app.instance_path, upload_folder, 'products')
        
        # Multiple static directory candidates
        static_candidates = []
        try:
            static_candidates.append(os.path.join(app.static_folder, 'uploads', 'products'))
        except Exception:
            pass
        try:
            static_candidates.append(os.path.join(os.path.dirname(app.root_path), 'static', 'uploads', 'products'))
        except Exception:
            pass
        static_candidates.append(os.path.join(os.getcwd(), 'static', 'uploads', 'products'))
        
        # Find the best static directory
        static_dir = None
        for candidate in static_candidates:
            if os.path.isdir(candidate):
                webp_files = [f for f in os.listdir(candidate) if f.endswith('.webp')]
                if webp_files:
                    static_dir = candidate
                    print(f"✅ Using static directory: {static_dir} ({len(webp_files)} WebP files)")
                    break
        
        if not static_dir:
            print("❌ No static directory with WebP files found!")
            return False
        
        # Ensure instance directory exists
        os.makedirs(instance_dir, exist_ok=True)
        print(f"📁 Instance directory: {instance_dir}")
        
        # Process each product
        success_count = 0
        error_count = 0
        copied_count = 0
        
        for product in products:
            try:
                # Get expected WebP filename
                expected_filename = f"{product.slug}-emdad-global.webp"
                
                # Check if product has image_path set
                if not product.image_path:
                    product.image_path = expected_filename
                    print(f"🔧 Set image_path for {product.slug}: {expected_filename}")
                
                # Ensure the filename is WebP
                if not product.image_path.endswith('.webp'):
                    product.image_path = expected_filename
                    print(f"🔧 Changed image_path to WebP for {product.slug}: {expected_filename}")
                
                # Check if file exists in static
                static_path = os.path.join(static_dir, product.image_path)
                instance_path = os.path.join(instance_dir, product.image_path)
                
                if os.path.exists(static_path):
                    # Copy to instance if needed
                    if not os.path.exists(instance_path) or os.path.getmtime(static_path) > os.path.getmtime(instance_path):
                        shutil.copy2(static_path, instance_path)
                        copied_count += 1
                        print(f"📋 Copied {product.image_path} to instance")
                    
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
                        from app.models import db
                        db.session.add(main_image)
                        print(f"🆕 Created ProductImage record for {product.slug}")
                    elif main_image.filename != product.image_path:
                        main_image.filename = product.image_path
                        from app.models import db
                        db.session.add(main_image)
                        print(f"🔧 Updated ProductImage filename for {product.slug}")
                    
                    success_count += 1
                    
                else:
                    print(f"⚠️ Missing WebP image for {product.slug}: {product.image_path}")
                    error_count += 1
                    
            except Exception as e:
                print(f"❌ Error processing {product.slug}: {e}")
                error_count += 1
        
        # Commit changes
        try:
            from app.models import db
            db.session.commit()
            print("💾 Database changes committed")
        except Exception as e:
            print(f"❌ Failed to commit database changes: {e}")
            from app.models import db
            db.session.rollback()
            return False
        
        # Print summary
        print(f"\n📊 Summary:")
        print(f"✅ Successful: {success_count}")
        print(f"❌ Errors: {error_count}")
        print(f"📋 Images copied: {copied_count}")
        print(f"📈 Success rate: {success_count/(success_count+error_count)*100:.1f}%")
        
        return error_count == 0

if __name__ == '__main__':
    success = ensure_webp_images()
    sys.exit(0 if success else 1)
