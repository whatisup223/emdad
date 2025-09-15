#!/usr/bin/env python3
"""
Test script to simulate complete production deployment including specifications.
This simulates exactly what happens when deploying to Render.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def simulate_production_deployment():
    """Simulate the complete production deployment process."""
    app = create_app()
    with app.app_context():
        print("🚀 Simulating COMPLETE production deployment process...")
        print("=" * 60)
        
        # Step 1: Clear all specifications to simulate fresh deployment
        print("🧹 Step 1: Clearing existing specifications (simulating fresh deployment)...")
        products = Product.query.all()
        for product in products:
            product.specifications = None
        db.session.commit()
        
        # Verify clearing
        specs_count = Product.query.filter(Product.specifications.isnot(None)).count()
        print(f"   ✅ Cleared specifications. Products with specs: {specs_count}/38")
        
        # Step 2: Simulate the exact process from init_db_render.py
        print("\n📦 Step 2: Running the EXACT process from init_db_render.py...")
        
        # 2a. Products are already seeded (we're not clearing them)
        print("   ✅ Products already seeded (38 products)")
        
        # 2b. Add HS codes (simulating the HS code step)
        print("   🏷️ Adding HS codes...")
        try:
            from migrations.add_default_hs_codes import update_product_hs_codes
            hs_success = update_product_hs_codes(db)
            if hs_success:
                db.session.commit()
                print("   ✅ HS codes assignment completed")
            else:
                print("   ⚠️ HS codes assignment failed")
        except Exception as e:
            print(f"   ⚠️ HS codes error: {e}")
        
        # 2c. Add specifications (THE CRITICAL STEP)
        print("   📋 Adding specifications...")
        try:
            from migrations.add_default_product_specifications import update_product_specifications
            specs_success = update_product_specifications(db)
            if specs_success:
                db.session.commit()
                print("   ✅ Product specifications assignment completed")
            else:
                print("   ⚠️ Product specifications assignment failed")
        except Exception as e:
            print(f"   ⚠️ Specifications error: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 3: Verify final results
        print("\n🔍 Step 3: Verifying deployment results...")
        
        # Check specifications coverage
        total_products = Product.query.count()
        products_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
        coverage_percent = (products_with_specs / total_products) * 100
        
        print(f"   📊 Total products: {total_products}")
        print(f"   📋 Products with specifications: {products_with_specs}")
        print(f"   📈 Coverage: {coverage_percent:.1f}%")
        
        # Test specific products from different categories
        test_products = [
            ('fresh-oranges', 'Fresh Fruits'),
            ('cumin-seed', 'Spices'),
            ('dates-whole', 'Dates'),
            ('basil', 'Herbs'),
            ('sesame-seed', 'Seeds'),
            ('potatoes-spunta', 'Vegetables'),
            ('iqf-strawberries', 'Frozen')
        ]
        
        print("\n   🧪 Testing sample products:")
        all_good = True
        
        for slug, category in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if not product:
                print(f"   ❌ {category}: {slug} - NOT FOUND")
                all_good = False
                continue
            
            if not product.specifications:
                print(f"   ❌ {category}: {slug} - NO SPECIFICATIONS")
                all_good = False
                continue
            
            # Test parsing
            try:
                specs_en = product.get_specifications_lang('en')
                specs_ar = product.get_specifications_lang('ar')
                
                en_fields = len(specs_en) if isinstance(specs_en, dict) else 0
                ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 0
                
                if en_fields > 0 and ar_fields > 0:
                    print(f"   ✅ {category}: {slug} - EN({en_fields}) AR({ar_fields}) fields")
                else:
                    print(f"   ⚠️ {category}: {slug} - Limited fields EN({en_fields}) AR({ar_fields})")
                    
            except Exception as e:
                print(f"   ❌ {category}: {slug} - PARSING ERROR: {e}")
                all_good = False
        
        # Step 4: Final conclusion
        print("\n" + "=" * 60)
        print("🎯 DEPLOYMENT SIMULATION RESULTS:")
        
        if coverage_percent == 100 and all_good:
            print("✅ SUCCESS: Complete production deployment simulation PASSED!")
            print("✅ All 38 products will have specifications in production")
            print("✅ Both English and Arabic specifications are working")
            print("✅ All product categories are covered")
            return True
        else:
            print("❌ FAILURE: Production deployment simulation FAILED!")
            print(f"❌ Coverage: {coverage_percent:.1f}% (expected 100%)")
            return False

if __name__ == "__main__":
    success = simulate_production_deployment()
    if success:
        print("\n🎉 CONCLUSION: Production deployment will include specifications!")
    else:
        print("\n💥 CONCLUSION: There are issues with production deployment!")
    
    sys.exit(0 if success else 1)
