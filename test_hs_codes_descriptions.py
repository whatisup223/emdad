#!/usr/bin/env python3
"""
Test the new HS codes description system
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product

def test_hs_descriptions():
    """Test HS code descriptions for all products."""
    app = create_app()
    with app.app_context():
        print("🔍 TESTING HS CODE DESCRIPTIONS")
        print("=" * 70)
        
        # Test specific products that were mentioned as having issues
        test_products = [
            'fresh-oranges',
            'basil', 
            'cumin-seed',
            'fresh-strawberries',
            'dates-whole',
            'sesame-seed'
        ]
        
        print("🧪 Testing HS code descriptions for key products:")
        print("-" * 70)
        
        for slug in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if not product:
                print(f"❌ {slug}: Product not found")
                continue
            
            print(f"\n🔍 {slug.upper()} ({product.name_en}):")
            print(f"   HS Code: {product.hs_code}")
            
            # Test English description
            desc_en = product.get_hs_code_description('en')
            print(f"   EN Description: {desc_en}")
            
            # Test Arabic description  
            desc_ar = product.get_hs_code_description('ar')
            print(f"   AR Description: {desc_ar}")
            
            # Test full display format
            display_en = product.get_hs_code_display('en')
            display_ar = product.get_hs_code_display('ar')
            print(f"   EN Display: {display_en}")
            print(f"   AR Display: {display_ar}")
            
            # Verify it's not the old generic text
            if desc_en and 'thyme' in desc_en.lower() and slug != 'thyme':
                print(f"   ⚠️ WARNING: Still showing thyme description for {slug}")
            elif desc_ar and 'زعتر' in desc_ar and slug not in ['thyme', 'oregano']:
                print(f"   ⚠️ WARNING: Still showing thyme description for {slug}")
            else:
                print(f"   ✅ Description looks correct!")
        
        print("\n" + "=" * 70)
        print("🎯 TESTING COMPLETE")

if __name__ == "__main__":
    test_hs_descriptions()
