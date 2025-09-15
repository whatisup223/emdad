#!/usr/bin/env python3
"""
Check HS codes for all products to identify mismatches
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product

def check_hs_codes():
    """Check HS codes for all products."""
    app = create_app()
    with app.app_context():
        print("🔍 CHECKING HS CODES FOR ALL PRODUCTS")
        print("=" * 70)
        
        # Get all products
        products = Product.query.all()
        
        # Expected HS codes for verification
        expected_hs_codes = {
            # Fresh Fruits
            'fresh-oranges': '080510',  # Fresh oranges
            'fresh-mandarins': '080520',  # Fresh mandarins
            'fresh-tangerines': '080520',  # Fresh tangerines  
            'fresh-strawberries': '081010',  # Fresh strawberries
            'fresh-grapes': '080610',  # Fresh grapes
            'fresh-pomegranates': '081090',  # Other fresh fruits
            'fresh-mango': '080450',  # Fresh mango
            
            # Vegetables
            'potatoes-spunta': '070190',  # Other fresh potatoes
            'sweet-potatoes-beauregard': '071420',  # Sweet potatoes
            'fresh-spring-onions': '070390',  # Other onions
            'onions-red-golden': '070310',  # Onions
            'garlic-white': '070320',  # Garlic
            
            # Dates
            'dates-whole': '080410',  # Dates
            'dates-pitted': '080410',  # Dates
            'medjool-dates-whole': '080410',  # Dates
            'medjool-dates-pitted': '080410',  # Dates
            
            # Spices
            'cumin-seed': '090930',  # Cumin seeds
            'coriander-seed': '090920',  # Coriander seeds
            'fennel-seed': '090960',  # Fennel seeds
            'anise-seed': '090950',  # Anise seeds
            'caraway-seed': '090940',  # Caraway seeds
            
            # Seeds
            'nigella-black-seed': '121190',  # Other oil seeds
            'sesame-seed': '120740',  # Sesame seeds
            'flax-seeds': '120400',  # Flax seeds
            
            # Herbs
            'basil': '121190',  # Other plants/herbs
            'parsley-flakes': '121190',  # Other plants/herbs
            'dill': '121190',  # Other plants/herbs
            'mint': '121190',  # Other plants/herbs
            'oregano': '121190',  # Other plants/herbs
            'thyme': '121190',  # Other plants/herbs
            'sage': '121190',  # Other plants/herbs
            'marjoram': '121190',  # Other plants/herbs
            'lemongrass': '121190',  # Other plants/herbs
            'chamomile': '121190',  # Other plants/herbs
            'calendula': '121190',  # Other plants/herbs
            'hibiscus': '121190',  # Other plants/herbs
            
            # Frozen
            'iqf-strawberries': '081110',  # Frozen strawberries
            'iqf-mango': '081140',  # Frozen mango
        }
        
        print("🧪 Checking HS codes for accuracy:")
        print("-" * 70)
        
        issues_found = []
        
        for product in products:
            expected_code = expected_hs_codes.get(product.slug)
            actual_code = product.hs_code
            
            if not expected_code:
                print(f"⚠️ {product.slug}: No expected HS code defined")
                continue
            
            if actual_code != expected_code:
                issues_found.append({
                    'slug': product.slug,
                    'name': product.name_en,
                    'expected': expected_code,
                    'actual': actual_code
                })
                print(f"❌ {product.slug} ({product.name_en}):")
                print(f"   Expected: {expected_code}")
                print(f"   Actual:   {actual_code}")
            else:
                print(f"✅ {product.slug}: {actual_code} (correct)")
        
        print("\n" + "=" * 70)
        print("🎯 SUMMARY:")
        
        if issues_found:
            print(f"❌ Found {len(issues_found)} HS code issues:")
            for issue in issues_found:
                print(f"   • {issue['slug']}: {issue['actual']} → should be {issue['expected']}")
        else:
            print("✅ All HS codes are correct!")
        
        return issues_found

if __name__ == "__main__":
    issues = check_hs_codes()
    
    if issues:
        print(f"\n💥 CONCLUSION: {len(issues)} HS code issues found!")
        print("🔧 These need to be fixed immediately.")
    else:
        print("\n🎉 CONCLUSION: All HS codes are correct!")
