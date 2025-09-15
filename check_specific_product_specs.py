#!/usr/bin/env python3
"""
Check specific product specifications in detail
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def check_specific_product(slug):
    """Check a specific product's specifications in detail."""
    app = create_app()
    with app.app_context():
        product = Product.query.filter_by(slug=slug).first()
        if not product:
            print(f"❌ Product '{slug}' not found")
            return
        
        print(f"🔍 DETAILED CHECK: {slug.upper()}")
        print(f"📝 Product Name EN: {product.name_en}")
        print(f"📝 Product Name AR: {product.name_ar}")
        print("=" * 60)
        
        if not product.specifications:
            print("❌ No specifications found")
            return
        
        # Show raw JSON
        print("📄 Raw JSON specifications:")
        try:
            raw_specs = json.loads(product.specifications)
            print(json.dumps(raw_specs, indent=2, ensure_ascii=False)[:1000] + "...")
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
            print(f"Raw content: {product.specifications[:500]}...")
        
        print("\n" + "-" * 60)
        
        # Show parsed specifications
        try:
            specs_en = product.get_specifications_lang('en')
            specs_ar = product.get_specifications_lang('ar')
            
            print("🇺🇸 ENGLISH SPECIFICATIONS:")
            if isinstance(specs_en, dict):
                for key, value in specs_en.items():
                    print(f"   • {key}: {value}")
            else:
                print(f"   {specs_en}")
            
            print("\n🇸🇦 ARABIC SPECIFICATIONS:")
            if isinstance(specs_ar, dict):
                for key, value in specs_ar.items():
                    print(f"   • {key}: {value}")
            else:
                print(f"   {specs_ar}")
                
        except Exception as e:
            print(f"❌ Error getting specifications: {e}")

if __name__ == "__main__":
    # Check the products mentioned as having issues
    products_to_check = [
        'fresh-oranges',
        'basil',
        'cumin-seed'
    ]
    
    for slug in products_to_check:
        check_specific_product(slug)
        print("\n" + "=" * 80 + "\n")
