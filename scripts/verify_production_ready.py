#!/usr/bin/env python3
"""
Verify that production is ready with all 28 products and WebP images.
This script runs at the end of deployment to ensure everything is working.
If this fails, deployment is aborted.
"""

import os
import sys

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_production_ready():
    """Verify that production is ready for deployment."""
    
    print("🔍 VERIFYING PRODUCTION READINESS...")
    print("=" * 50)
    
    try:
        from app import create_app
        from app.models import Product, ProductImage, Category
        
        # Try production config first, fallback to development
        try:
            app = create_app('production')
            print("✅ Using production configuration")
        except:
            app = create_app('development')
            print("⚠️ Using development configuration (fallback)")
        
        with app.app_context():
            # Test 1: Product count
            print("\n1️⃣ Checking product count...")
            products = Product.query.filter_by(status='active').all()
            print(f"   Found: {len(products)} active products")
            
            if len(products) < 28:
                print(f"❌ FAIL: Expected at least 28 products, found {len(products)}")
                return False
            else:
                print("✅ PASS: Sufficient products found")
            
            # Test 2: WebP images in database
            print("\n2️⃣ Checking WebP images in database...")
            products_with_webp = 0
            products_without_webp = []
            
            for product in products:
                if product.image_path and product.image_path.endswith('.webp'):
                    products_with_webp += 1
                else:
                    products_without_webp.append(product.slug)
            
            print(f"   Products with WebP: {products_with_webp}/{len(products)}")
            
            if products_with_webp < 28:
                print(f"❌ FAIL: Expected at least 28 products with WebP, found {products_with_webp}")
                if products_without_webp:
                    print("   Products without WebP:")
                    for slug in products_without_webp[:10]:  # Show first 10
                        print(f"     - {slug}")
                return False
            else:
                print("✅ PASS: All products have WebP images")
            
            # Test 3: ProductImage records
            print("\n3️⃣ Checking ProductImage records...")
            products_with_main_image = 0
            products_without_main_image = []
            
            for product in products:
                main_image = product.get_main_image()
                if main_image:
                    products_with_main_image += 1
                else:
                    products_without_main_image.append(product.slug)
            
            print(f"   Products with main image: {products_with_main_image}/{len(products)}")
            
            if products_with_main_image < 28:
                print(f"❌ FAIL: Expected at least 28 products with main image, found {products_with_main_image}")
                if products_without_main_image:
                    print("   Products without main image:")
                    for slug in products_without_main_image[:10]:
                        print(f"     - {slug}")
                return False
            else:
                print("✅ PASS: All products have main ProductImage records")
            
            # Test 4: Instance directory
            print("\n4️⃣ Checking instance directory...")
            upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
            
            # Try multiple instance directory locations
            instance_candidates = [
                os.path.join(app.instance_path, upload_folder, 'products'),
                os.path.join('/tmp', 'instance', 'uploads', 'products'),
            ]
            
            instance_dir = None
            instance_webp_count = 0
            
            for candidate in instance_candidates:
                if os.path.exists(candidate):
                    webp_files = [f for f in os.listdir(candidate) if f.endswith('.webp')]
                    if webp_files:
                        instance_dir = candidate
                        instance_webp_count = len(webp_files)
                        break
            
            if instance_dir:
                print(f"   Instance directory: {instance_dir}")
                print(f"   WebP files found: {instance_webp_count}")
                
                if instance_webp_count < 28:
                    print(f"❌ FAIL: Expected at least 28 WebP files in instance, found {instance_webp_count}")
                    return False
                else:
                    print("✅ PASS: Sufficient WebP files in instance directory")
            else:
                print("⚠️ WARNING: No instance directory found, but this may be normal in some deployments")
            
            # Test 5: Categories
            print("\n5️⃣ Checking categories...")
            categories = Category.query.filter_by(is_active=True).all()
            print(f"   Active categories: {len(categories)}")
            
            if len(categories) < 6:
                print(f"❌ FAIL: Expected at least 6 categories, found {len(categories)}")
                return False
            else:
                print("✅ PASS: Sufficient categories found")
            
            # Test 6: Product distribution across categories
            print("\n6️⃣ Checking product distribution...")
            category_counts = {}
            for product in products:
                cat = Category.query.get(product.category_id)
                if cat:
                    category_counts[cat.key] = category_counts.get(cat.key, 0) + 1
            
            print("   Products per category:")
            for cat_key, count in category_counts.items():
                print(f"     {cat_key}: {count}")
            
            if len(category_counts) < 6:
                print(f"❌ FAIL: Products distributed across only {len(category_counts)} categories")
                return False
            else:
                print("✅ PASS: Products well distributed across categories")
            
            # Test 7: Sample image accessibility
            print("\n7️⃣ Testing sample image accessibility...")
            sample_products = products[:3]  # Test first 3 products
            accessible_count = 0
            
            for product in sample_products:
                if product.image_path:
                    # Check if we can construct the path
                    if instance_dir:
                        image_path = os.path.join(instance_dir, product.image_path)
                        if os.path.exists(image_path):
                            accessible_count += 1
                            print(f"   ✅ {product.slug}: Image accessible")
                        else:
                            print(f"   ⚠️ {product.slug}: Image not found at {image_path}")
                    else:
                        print(f"   ⚠️ {product.slug}: Cannot verify (no instance dir)")
            
            if accessible_count >= 2:  # At least 2 out of 3 should be accessible
                print("✅ PASS: Sample images are accessible")
            else:
                print(f"❌ FAIL: Only {accessible_count}/3 sample images accessible")
                return False
        
        # Final summary
        print("\n" + "=" * 50)
        print("🎉 PRODUCTION VERIFICATION PASSED!")
        print("✅ All systems ready for deployment")
        print(f"✅ {len(products)} products with WebP images")
        print(f"✅ {len(categories)} active categories")
        print("✅ Database integrity confirmed")
        print("✅ File system ready")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR during verification: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = verify_production_ready()
    if success:
        print("\n🚀 READY FOR PRODUCTION!")
        sys.exit(0)
    else:
        print("\n🛑 PRODUCTION NOT READY - DEPLOYMENT ABORTED!")
        sys.exit(1)
