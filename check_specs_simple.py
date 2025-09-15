#!/usr/bin/env python3
"""
Simple script to check product specifications.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product

def check_specs():
    """Check product specifications."""
    app = create_app()
    with app.app_context():
        print("🔍 Checking product specifications...")
        
        # Check a specific product
        cumin = Product.query.filter_by(slug='cumin-seed').first()
        if cumin:
            print(f'✅ Cumin found: {cumin.name_en}')
            print(f'   Specifications: {bool(cumin.specifications)}')
            if cumin.specifications:
                print(f'   Length: {len(cumin.specifications)} chars')
                specs_en = cumin.get_specifications_lang('en')
                specs_ar = cumin.get_specifications_lang('ar')
                print(f'   EN fields: {len(specs_en) if isinstance(specs_en, dict) else 0}')
                print(f'   AR fields: {len(specs_ar) if isinstance(specs_ar, dict) else 0}')
                if isinstance(specs_en, dict) and len(specs_en) > 0:
                    first_key = list(specs_en.keys())[0]
                    print(f'   Sample EN: {first_key}: {specs_en[first_key][:50]}...')
        else:
            print('❌ Cumin not found')
        
        # Check all products with specs
        products_with_specs = Product.query.filter(Product.specifications.isnot(None)).all()
        print(f'\n📊 Products with specifications: {len(products_with_specs)}/38')
        
        for p in products_with_specs[:5]:  # Show first 5
            print(f'  - {p.slug}: {len(p.specifications) if p.specifications else 0} chars')

if __name__ == "__main__":
    check_specs()
