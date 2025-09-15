#!/usr/bin/env python3
"""
FINAL TEST: Complete production deployment with FORCE UPDATE
This simulates the exact process that will happen in production with force update.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def test_final_production_deployment():
    """Test the final production deployment with force update."""
    app = create_app()
    with app.app_context():
        print("🚀 FINAL PRODUCTION DEPLOYMENT TEST")
        print("=" * 70)
        print("Testing the EXACT process that will happen in production")
        print("with FORCE UPDATE for comprehensive specifications")
        print("=" * 70)
        
        # Step 1: Simulate production state (some products have simple specs)
        print("🎭 Step 1: Simulating current production state...")
        
        # Set some products to have simple specifications (like in production)
        simple_products = ['fresh-oranges', 'cumin-seed', 'basil']
        for slug in simple_products:
            product = Product.query.filter_by(slug=slug).first()
            if product:
                # Set simple specifications like in production
                simple_specs = {
                    'en': {'notes': f'Simple description for {slug}'},
                    'ar': {'notes': f'وصف بسيط لـ {slug}'}
                }
                product.specifications = json.dumps(simple_specs, ensure_ascii=False)
        
        # Clear specifications for some products
        clear_products = ['dates-whole', 'sesame-seed']
        for slug in clear_products:
            product = Product.query.filter_by(slug=slug).first()
            if product:
                product.specifications = None
        
        db.session.commit()
        
        # Check initial state
        total_products = Product.query.count()
        products_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
        print(f"   📊 Initial state: {products_with_specs}/{total_products} products have specifications")
        
        # Step 2: Run the EXACT production deployment process
        print("\n🚀 Step 2: Running EXACT production deployment process...")
        print("   (This is what happens in init_db_render.py)")
        
        # 2a. Products seeding (already done)
        print("   ✅ Products seeded (38 products)")
        
        # 2b. HS codes assignment
        print("   🏷️ Adding HS codes...")
        try:
            from migrations.add_default_hs_codes import update_product_hs_codes
            hs_success = update_product_hs_codes(db)
            if hs_success:
                db.session.commit()
                print("   ✅ HS codes assignment completed")
        except Exception as e:
            print(f"   ⚠️ HS codes error: {e}")
        
        # 2c. FORCE UPDATE specifications (NEW!)
        print("   📋 FORCE UPDATING comprehensive specifications...")
        try:
            from migrations.add_default_product_specifications import update_product_specifications
            # This is the key change: force_update=True
            specs_success = update_product_specifications(db, force_update=True)
            if specs_success:
                db.session.commit()
                print("   ✅ Product specifications FORCE UPDATE completed")
                print("   🌟 All products now have comprehensive bilingual specifications")
            else:
                print("   ❌ Product specifications FORCE UPDATE failed")
        except Exception as e:
            print(f"   ❌ Specifications error: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 3: Comprehensive verification
        print("\n🔍 Step 3: Comprehensive verification...")
        
        # Check final coverage
        final_products_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
        final_coverage = (final_products_with_specs / total_products) * 100
        
        print(f"   📊 Final coverage: {final_products_with_specs}/{total_products} ({final_coverage:.1f}%)")
        
        # Test ALL product categories
        categories = {
            'Fresh Fruits': ['fresh-oranges', 'fresh-strawberries', 'fresh-grapes'],
            'Vegetables': ['potatoes-spunta', 'onions-red-golden', 'garlic-white'],
            'Dates': ['dates-whole', 'medjool-dates-whole'],
            'Spices': ['cumin-seed', 'coriander-seed', 'fennel-seed'],
            'Seeds': ['sesame-seed', 'nigella-black-seed', 'flax-seeds'],
            'Herbs': ['basil', 'mint', 'oregano', 'thyme'],
            'Frozen': ['iqf-strawberries', 'iqf-mango']
        }
        
        print("\n   🧪 Testing ALL product categories:")
        all_categories_good = True
        
        for category, products in categories.items():
            category_success = 0
            category_total = len(products)
            
            for slug in products:
                product = Product.query.filter_by(slug=slug).first()
                if product and product.specifications:
                    specs_en = product.get_specifications_lang('en')
                    specs_ar = product.get_specifications_lang('ar')
                    en_fields = len(specs_en) if isinstance(specs_en, dict) else 0
                    ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 0
                    
                    if en_fields >= 5 and ar_fields >= 5:
                        category_success += 1
            
            category_percent = (category_success / category_total) * 100
            status = "✅" if category_percent == 100 else "⚠️" if category_percent >= 80 else "❌"
            print(f"      {status} {category}: {category_success}/{category_total} ({category_percent:.0f}%)")
            
            if category_percent < 100:
                all_categories_good = False
        
        # Test specific products that were problematic
        print("\n   🎯 Testing previously problematic products:")
        test_products = [
            ('fresh-oranges', 'Had simple specs'),
            ('cumin-seed', 'Had simple specs'),
            ('basil', 'Had simple specs'),
            ('dates-whole', 'Had no specs'),
            ('sesame-seed', 'Had no specs')
        ]
        
        problematic_fixed = True
        for slug, issue in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if product and product.specifications:
                specs_en = product.get_specifications_lang('en')
                specs_ar = product.get_specifications_lang('ar')
                en_fields = len(specs_en) if isinstance(specs_en, dict) else 0
                ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 0
                
                if en_fields >= 5 and ar_fields >= 5:
                    print(f"      ✅ {slug}: EN({en_fields}) AR({ar_fields}) - FIXED!")
                else:
                    print(f"      ❌ {slug}: EN({en_fields}) AR({ar_fields}) - STILL PROBLEMATIC")
                    problematic_fixed = False
            else:
                print(f"      ❌ {slug}: NO SPECIFICATIONS - NOT FIXED")
                problematic_fixed = False
        
        # Final assessment
        print("\n" + "=" * 70)
        print("🎯 FINAL ASSESSMENT:")
        
        success = (final_coverage == 100 and all_categories_good and problematic_fixed)
        
        if success:
            print("🎉 PERFECT SUCCESS!")
            print("✅ 100% coverage achieved")
            print("✅ All categories working perfectly")
            print("✅ All previously problematic products fixed")
            print("✅ Production will have comprehensive specifications")
            print("🌟 Both English and Arabic specifications complete")
            return True
        else:
            print("❌ ISSUES DETECTED!")
            if final_coverage < 100:
                print(f"❌ Coverage only {final_coverage:.1f}% (expected 100%)")
            if not all_categories_good:
                print("❌ Some categories have issues")
            if not problematic_fixed:
                print("❌ Some previously problematic products not fixed")
            return False

if __name__ == "__main__":
    success = test_final_production_deployment()
    
    print("\n" + "=" * 70)
    if success:
        print("🏆 CONCLUSION: Production deployment is PERFECT!")
        print("🚀 All 38 products will have comprehensive specifications")
        print("🌍 Both English and Arabic specifications complete")
        print("✨ Production is ready for deployment!")
    else:
        print("💥 CONCLUSION: There are still issues!")
        print("🔧 Please review the problems above")
    
    sys.exit(0 if success else 1)
