#!/usr/bin/env python3
"""
PRODUCTION FORCE UPDATE: Update all product specifications
This script forces update of ALL products with comprehensive specifications.
Use this to sync production with development specifications.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to force update all specifications."""
    print("🚀 PRODUCTION FORCE UPDATE TOOL")
    print("=" * 60)
    print("This will update ALL products with comprehensive specifications")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from migrations.add_default_product_specifications import update_product_specifications
        
        app = create_app()
        with app.app_context():
            print("🔄 Starting FORCE UPDATE of all product specifications...")
            
            # Force update ALL products
            success = update_product_specifications(db, force_update=True)
            
            if success:
                print("\n✅ FORCE UPDATE completed successfully!")
                
                # Verify results
                from app.models import Product
                total_products = Product.query.count()
                products_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
                coverage = (products_with_specs / total_products) * 100
                
                print(f"📊 Final status: {products_with_specs}/{total_products} products ({coverage:.1f}%)")
                
                # Test sample products
                test_products = ['fresh-oranges', 'cumin-seed', 'basil', 'dates-whole']
                print("\n🧪 Testing sample products:")
                
                for slug in test_products:
                    product = Product.query.filter_by(slug=slug).first()
                    if product and product.specifications:
                        specs_en = product.get_specifications_lang('en')
                        specs_ar = product.get_specifications_lang('ar')
                        en_fields = len(specs_en) if isinstance(specs_en, dict) else 0
                        ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 0
                        print(f"   ✅ {slug}: EN({en_fields}) AR({ar_fields}) fields")
                    else:
                        print(f"   ❌ {slug}: No specifications")
                
                if coverage == 100:
                    print("\n🎉 SUCCESS: All products now have comprehensive specifications!")
                    return True
                else:
                    print(f"\n⚠️ WARNING: Only {coverage:.1f}% coverage achieved")
                    return False
            else:
                print("\n❌ FORCE UPDATE failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error during force update: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ CONCLUSION: Production specifications are now complete!")
        print("🌟 All products have comprehensive bilingual specifications")
        print("🚀 Production is ready!")
    else:
        print("\n❌ CONCLUSION: Force update failed!")
        print("🔧 Please check the errors and try again")
    
    sys.exit(0 if success else 1)
