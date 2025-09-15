#!/usr/bin/env python3
"""
Diagnose specifications issues - check if products have correct specifications
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def diagnose_specifications():
    """Diagnose specifications issues."""
    app = create_app()
    with app.app_context():
        print("🔍 DIAGNOSING PRODUCT SPECIFICATIONS ISSUES")
        print("=" * 60)
        
        # Test specific products mentioned
        test_products = [
            'fresh-oranges',
            'cumin-seed', 
            'basil',
            'dates-whole',
            'sesame-seed',
            'fresh-strawberries',
            'potatoes-spunta'
        ]
        
        print("🧪 Checking specific products for specification accuracy:")
        print("-" * 60)
        
        for slug in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if not product:
                print(f"❌ {slug}: Product not found")
                continue
            
            print(f"\n🔍 {slug.upper()} ({product.name_en}):")
            
            if not product.specifications:
                print("   ❌ No specifications found")
                continue
            
            try:
                specs_en = product.get_specifications_lang('en')
                specs_ar = product.get_specifications_lang('ar')
                
                print(f"   📊 EN fields: {len(specs_en) if isinstance(specs_en, dict) else 0}")
                print(f"   📊 AR fields: {len(specs_ar) if isinstance(specs_ar, dict) else 0}")
                
                if isinstance(specs_en, dict):
                    print("   📋 English specifications:")
                    for key, value in specs_en.items():
                        print(f"      • {key}: {value[:80]}...")
                        
                        # Check for obvious mismatches
                        if slug == 'fresh-oranges':
                            if 'thyme' in value.lower() or 'oregano' in value.lower() or 'herb' in value.lower():
                                print(f"      ⚠️ MISMATCH DETECTED: Orange has herb-related content!")
                        elif slug == 'cumin-seed':
                            if 'orange' in value.lower() or 'citrus' in value.lower() or 'fruit' in value.lower():
                                print(f"      ⚠️ MISMATCH DETECTED: Cumin has fruit-related content!")
                        elif slug == 'basil':
                            if 'orange' in value.lower() or 'citrus' in value.lower() or 'fruit' in value.lower():
                                print(f"      ⚠️ MISMATCH DETECTED: Basil has fruit-related content!")
                
                if isinstance(specs_ar, dict):
                    print("   📋 Arabic specifications:")
                    for key, value in list(specs_ar.items())[:3]:  # Show first 3
                        print(f"      • {key}: {value[:80]}...")
                        
            except Exception as e:
                print(f"   ❌ Error parsing specifications: {e}")
        
        print("\n" + "=" * 60)
        print("🎯 DIAGNOSIS COMPLETE")

if __name__ == "__main__":
    diagnose_specifications()
