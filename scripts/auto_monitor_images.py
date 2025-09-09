#!/usr/bin/env python3
"""
Auto-monitor and fix image issues in production.
This script can be called periodically to ensure images stay working.
"""

import os
import sys
import time
import shutil
from datetime import datetime

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def auto_monitor_images():
    """Monitor and auto-fix image issues."""
    
    print(f"🔍 AUTO-MONITOR STARTED at {datetime.now()}")
    
    try:
        from app import create_app
        from app.models import Product, ProductImage, db
        
        # Use production config
        try:
            app = create_app('production')
        except:
            app = create_app('development')
        
        with app.app_context():
            # Check products
            products = Product.query.filter_by(status='active').all()
            
            issues_found = 0
            issues_fixed = 0
            
            # Find instance directory
            upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
            instance_candidates = [
                os.path.join(app.instance_path, upload_folder, 'products'),
                os.path.join('/tmp', 'instance', 'uploads', 'products'),
            ]
            
            instance_dir = None
            for candidate in instance_candidates:
                if os.path.exists(candidate):
                    instance_dir = candidate
                    break
            
            if not instance_dir:
                print("⚠️ No instance directory found")
                return False
            
            # Find static directory
            static_candidates = [
                os.path.join(os.getcwd(), 'static', 'uploads', 'products'),
                os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'products'),
            ]
            
            static_dir = None
            for candidate in static_candidates:
                if os.path.exists(candidate):
                    webp_files = [f for f in os.listdir(candidate) if f.endswith('.webp')]
                    if webp_files:
                        static_dir = candidate
                        break
            
            if not static_dir:
                print("⚠️ No static directory found")
                return False
            
            # Check each product
            for product in products:
                # Check 1: image_path
                if not product.image_path or not product.image_path.endswith('.webp'):
                    issues_found += 1
                    expected_filename = f"{product.slug}-emdad-global.webp"
                    product.image_path = expected_filename
                    issues_fixed += 1
                    print(f"🔧 Fixed image_path for {product.slug}")
                
                # Check 2: file exists in instance
                if product.image_path:
                    instance_path = os.path.join(instance_dir, product.image_path)
                    static_path = os.path.join(static_dir, product.image_path)
                    
                    if not os.path.exists(instance_path) and os.path.exists(static_path):
                        issues_found += 1
                        try:
                            shutil.copy2(static_path, instance_path)
                            issues_fixed += 1
                            print(f"🔧 Copied missing image for {product.slug}")
                        except Exception as e:
                            print(f"❌ Failed to copy image for {product.slug}: {e}")
                
                # Check 3: ProductImage record
                main_image = product.get_main_image()
                if not main_image and product.image_path:
                    issues_found += 1
                    main_image = ProductImage(
                        product_id=product.id,
                        filename=product.image_path,
                        alt_text_en=product.name_en,
                        alt_text_ar=product.name_ar,
                        is_main=True,
                        sort_order=0
                    )
                    db.session.add(main_image)
                    issues_fixed += 1
                    print(f"🔧 Created ProductImage for {product.slug}")
            
            # Commit fixes
            if issues_fixed > 0:
                db.session.commit()
                print(f"💾 Committed {issues_fixed} fixes")
            
            print(f"📊 Monitor Results: {issues_found} issues found, {issues_fixed} fixed")
            
            return issues_found == issues_fixed
            
    except Exception as e:
        print(f"❌ Monitor error: {e}")
        return False

def run_periodic_monitor():
    """Run monitor periodically."""
    
    # Run once immediately
    auto_monitor_images()
    
    # Then run every 30 minutes
    while True:
        try:
            time.sleep(1800)  # 30 minutes
            auto_monitor_images()
        except KeyboardInterrupt:
            print("🛑 Monitor stopped")
            break
        except Exception as e:
            print(f"❌ Monitor cycle error: {e}")
            time.sleep(300)  # Wait 5 minutes before retry

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--periodic':
        run_periodic_monitor()
    else:
        success = auto_monitor_images()
        sys.exit(0 if success else 1)
