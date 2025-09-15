#!/usr/bin/env python3
"""
Test script to simulate production deployment and verify HS codes are assigned automatically.
This simulates what happens when deploying to Render.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def simulate_production_deployment():
    """Simulate the production deployment process."""
    try:
        from app import create_app, db
        from app.models import Product, Category
        
        app = create_app()
        with app.app_context():
            print("🚀 Simulating production deployment...")
            
            # Step 1: Check if products exist (they should from previous seeding)
            initial_product_count = Product.query.count()
            print(f"📊 Initial products in database: {initial_product_count}")
            
            if initial_product_count == 0:
                print("⚠️ No products found. This test requires products to be seeded first.")
                return False
            
            # Step 2: Clear HS codes to simulate fresh deployment
            print("🧹 Clearing existing HS codes to simulate fresh deployment...")
            products = Product.query.all()
            for product in products:
                product.hs_code = None
            db.session.commit()
            
            # Verify HS codes are cleared
            products_with_hs = Product.query.filter(Product.hs_code.isnot(None)).count()
            print(f"📊 Products with HS codes after clearing: {products_with_hs}")
            
            # Step 3: Simulate the HS code assignment that happens in init_db_render.py
            print("\n🏷️ Simulating HS code assignment during deployment...")
            from migrations.add_default_hs_codes import update_product_hs_codes
            
            success = update_product_hs_codes(db)
            if success:
                db.session.commit()
                print("✅ HS codes assignment completed successfully")
            else:
                print("❌ HS codes assignment failed")
                return False
            
            # Step 4: Verify all products have HS codes
            final_products_with_hs = Product.query.filter(Product.hs_code.isnot(None)).count()
            total_products = Product.query.count()
            
            print(f"\n📊 Final verification:")
            print(f"   - Total products: {total_products}")
            print(f"   - Products with HS codes: {final_products_with_hs}")
            print(f"   - Coverage: {(final_products_with_hs/total_products)*100:.1f}%")
            
            if final_products_with_hs == total_products:
                print("✅ SUCCESS: All products have HS codes after deployment simulation!")
                
                # Step 5: Test a few specific products
                print("\n🔍 Testing specific products:")
                test_products = [
                    'fresh-oranges',
                    'basil', 
                    'dates-whole',
                    'iqf-strawberries',
                    'sesame-seed'
                ]
                
                for slug in test_products:
                    product = Product.query.filter_by(slug=slug).first()
                    if product and product.hs_code:
                        formatted = product.get_hs_code_formatted()
                        print(f"   ✅ {slug}: {formatted}")
                    else:
                        print(f"   ❌ {slug}: No HS code or product not found")
                        return False
                
                print("\n🎉 Production deployment simulation PASSED!")
                print("🚀 HS codes will be automatically assigned when deploying to Render!")
                return True
            else:
                print(f"❌ FAILED: Only {final_products_with_hs}/{total_products} products have HS codes")
                return False
                
    except Exception as e:
        print(f"❌ Error during deployment simulation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simulate_production_deployment()
    if success:
        print("\n✅ CONCLUSION: HS codes WILL be automatically assigned in production deployment!")
    else:
        print("\n❌ CONCLUSION: There may be issues with HS code assignment in production!")
    
    sys.exit(0 if success else 1)
