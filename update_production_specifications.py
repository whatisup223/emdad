#!/usr/bin/env python3
"""
Production Update Script: Force update all product specifications
This script will update ALL products in production with comprehensive specifications
regardless of their current state.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def force_update_all_specifications():
    """Force update ALL products with comprehensive specifications."""
    app = create_app()
    with app.app_context():
        print("🔄 PRODUCTION UPDATE: Force updating ALL product specifications...")
        print("=" * 70)
        
        # Import all specifications
        try:
            from migrations.add_default_product_specifications import get_product_specifications
            specifications_data = get_product_specifications()
            print(f"✅ Loaded specifications for {len(specifications_data)} products")
        except Exception as e:
            print(f"❌ Error loading specifications: {e}")
            return False
        
        # Get all products
        all_products = Product.query.all()
        print(f"📊 Found {len(all_products)} products in database")
        
        updated_count = 0
        not_found_count = 0
        
        print("\n🔄 Starting FORCE update process...")
        print("-" * 50)
        
        for slug, specs in specifications_data.items():
            product = Product.query.filter_by(slug=slug).first()
            if product:
                # Get current specifications for comparison
                current_specs = product.get_specifications()
                current_en = product.get_specifications_lang('en') if current_specs else {}
                current_ar = product.get_specifications_lang('ar') if current_specs else {}
                
                # Count current fields
                current_en_fields = len(current_en) if isinstance(current_en, dict) else 0
                current_ar_fields = len(current_ar) if isinstance(current_ar, dict) else 0
                
                # FORCE UPDATE regardless of current state
                product.specifications = json.dumps(specs, ensure_ascii=False)
                
                # Count new fields
                new_en = specs.get('en', {})
                new_ar = specs.get('ar', {})
                new_en_fields = len(new_en) if isinstance(new_en, dict) else 0
                new_ar_fields = len(new_ar) if isinstance(new_ar, dict) else 0
                
                updated_count += 1
                print(f"✅ {slug}:")
                print(f"   📊 Before: EN({current_en_fields}) AR({current_ar_fields}) fields")
                print(f"   📈 After:  EN({new_en_fields}) AR({new_ar_fields}) fields")
                
            else:
                not_found_count += 1
                print(f"⚠️ Product not found: {slug}")
        
        # Commit all changes
        if updated_count > 0:
            try:
                db.session.commit()
                print(f"\n✅ Successfully FORCE UPDATED {updated_count} products")
                print("💾 All changes committed to database")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error committing changes: {e}")
                return False
        else:
            print("\n⚠️ No products were updated")
        
        if not_found_count > 0:
            print(f"⚠️ {not_found_count} products from specifications list not found")
        
        # Final verification
        print("\n" + "=" * 70)
        print("🔍 FINAL VERIFICATION:")
        
        total_products = Product.query.count()
        products_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
        coverage = (products_with_specs / total_products) * 100
        
        print(f"📊 Total products: {total_products}")
        print(f"📋 Products with specifications: {products_with_specs}")
        print(f"📈 Coverage: {coverage:.1f}%")
        
        # Test sample products
        test_products = [
            'fresh-oranges', 'cumin-seed', 'dates-whole', 
            'basil', 'sesame-seed', 'iqf-strawberries'
        ]
        
        print("\n🧪 Testing sample products:")
        all_good = True
        
        for slug in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if product and product.specifications:
                specs_en = product.get_specifications_lang('en')
                specs_ar = product.get_specifications_lang('ar')
                en_fields = len(specs_en) if isinstance(specs_en, dict) else 0
                ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 0
                
                if en_fields >= 5 and ar_fields >= 5:
                    print(f"   ✅ {slug}: EN({en_fields}) AR({ar_fields}) - EXCELLENT")
                else:
                    print(f"   ⚠️ {slug}: EN({en_fields}) AR({ar_fields}) - LIMITED")
                    all_good = False
            else:
                print(f"   ❌ {slug}: NO SPECIFICATIONS")
                all_good = False
        
        # Final result
        print("\n" + "=" * 70)
        if coverage == 100 and all_good:
            print("🎉 SUCCESS: All products now have comprehensive specifications!")
            print("🌍 Both English and Arabic specifications are complete")
            print("🚀 Production is ready with full specifications")
            return True
        else:
            print("❌ ISSUES: Some products still have incomplete specifications")
            return False

def show_before_after_comparison():
    """Show before/after comparison for verification."""
    app = create_app()
    with app.app_context():
        print("\n📊 BEFORE/AFTER COMPARISON:")
        print("=" * 50)
        
        sample_products = ['fresh-oranges', 'cumin-seed', 'basil']
        
        for slug in sample_products:
            product = Product.query.filter_by(slug=slug).first()
            if product:
                print(f"\n🔍 {slug.upper()}:")
                specs_en = product.get_specifications_lang('en')
                specs_ar = product.get_specifications_lang('ar')
                
                if isinstance(specs_en, dict):
                    print(f"   📋 English fields ({len(specs_en)}):")
                    for key, value in list(specs_en.items())[:3]:  # Show first 3
                        print(f"      • {key}: {value[:50]}...")
                
                if isinstance(specs_ar, dict):
                    print(f"   📋 Arabic fields ({len(specs_ar)}):")
                    for key, value in list(specs_ar.items())[:3]:  # Show first 3
                        print(f"      • {key}: {value[:50]}...")

if __name__ == "__main__":
    print("🚀 PRODUCTION SPECIFICATIONS UPDATE TOOL")
    print("=" * 70)
    print("This will FORCE UPDATE all products with comprehensive specifications")
    print("Use this to sync production with development specifications")
    print("=" * 70)
    
    # Run the update
    success = force_update_all_specifications()
    
    if success:
        print("\n🎯 RUNNING VERIFICATION...")
        show_before_after_comparison()
        print("\n✅ CONCLUSION: Production specifications update SUCCESSFUL!")
        print("🌟 All products now have comprehensive bilingual specifications")
    else:
        print("\n❌ CONCLUSION: Production specifications update FAILED!")
        print("🔧 Please check the errors above and try again")
    
    sys.exit(0 if success else 1)
