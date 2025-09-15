#!/usr/bin/env python3
"""
Test script to verify HS codes are working correctly.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_hs_codes():
    """Test that all products have HS codes and they display correctly."""
    try:
        from app import create_app, db
        from app.models import Product
        
        app = create_app()
        with app.app_context():
            print("🧪 Testing HS codes functionality...")
            
            # Test 1: Check all products have HS codes
            products = Product.query.all()
            total_products = len(products)
            products_with_hs = Product.query.filter(Product.hs_code.isnot(None)).count()
            
            print(f"📊 Products with HS codes: {products_with_hs}/{total_products}")
            
            if products_with_hs == total_products:
                print("✅ All products have HS codes")
            else:
                print("❌ Some products are missing HS codes")
                missing = Product.query.filter(Product.hs_code.is_(None)).all()
                for product in missing:
                    print(f"   - {product.slug}")
                return False
            
            # Test 2: Check HS code formatting
            print("\n🔍 Testing HS code formatting...")
            for product in products[:5]:  # Test first 5 products
                formatted = product.get_hs_code_formatted()
                if formatted:
                    print(f"✅ {product.slug}: {formatted}")
                else:
                    print(f"❌ {product.slug}: No formatted HS code")
                    return False
            
            # Test 3: Check calendar route data includes HS codes
            print("\n📅 Testing calendar route data...")
            from app.main.routes import bp
            
            # Simulate the normalize function from calendar route
            def normalize_test(prod):
                return {
                    'id': prod.id,
                    'name': prod.name_en,
                    'slug': prod.slug,
                    'hs_code': prod.hs_code,
                }
            
            test_products = products[:3]  # Test first 3 products
            items = [normalize_test(p) for p in test_products]
            
            for item in items:
                if item['hs_code']:
                    print(f"✅ Calendar data for {item['slug']}: HS:{item['hs_code']}")
                else:
                    print(f"❌ Calendar data for {item['slug']}: No HS code")
                    return False
            
            print("\n🎉 All HS code tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hs_codes()
    sys.exit(0 if success else 1)
