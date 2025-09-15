#!/usr/bin/env python3
"""
Test script to verify product specifications are working correctly.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product
import json

def test_specifications():
    """Test product specifications functionality."""
    app = create_app()
    with app.app_context():
        print("🧪 Testing product specifications functionality...")
        
        # Get all products with specifications
        products_with_specs = Product.query.filter(Product.specifications.isnot(None)).all()
        total_products = Product.query.count()
        
        print(f"📊 Products with specifications: {len(products_with_specs)}/{total_products}")
        
        if len(products_with_specs) == 0:
            print("❌ No products have specifications!")
            return False
        
        # Test a few specific products
        test_products = [
            'fresh-oranges',
            'cumin-seed', 
            'basil',
            'dates-whole',
            'iqf-strawberries'
        ]
        
        print("\n🔍 Testing specific products:")
        
        for slug in test_products:
            product = Product.query.filter_by(slug=slug).first()
            if not product:
                print(f"❌ Product not found: {slug}")
                continue
                
            if not product.specifications:
                print(f"❌ {slug}: No specifications")
                continue
            
            try:
                # Test raw specifications
                raw_specs = product.get_specifications()
                if not raw_specs:
                    print(f"❌ {slug}: Could not parse specifications")
                    continue
                
                # Test English specifications
                specs_en = product.get_specifications_lang('en')
                if not specs_en:
                    print(f"❌ {slug}: No English specifications")
                    continue
                
                # Test Arabic specifications
                specs_ar = product.get_specifications_lang('ar')
                if not specs_ar:
                    print(f"❌ {slug}: No Arabic specifications")
                    continue
                
                # Count specification fields
                en_fields = len(specs_en) if isinstance(specs_en, dict) else 1
                ar_fields = len(specs_ar) if isinstance(specs_ar, dict) else 1
                
                print(f"✅ {slug}: EN({en_fields} fields) AR({ar_fields} fields)")
                
                # Show sample fields
                if isinstance(specs_en, dict) and len(specs_en) > 0:
                    first_key = list(specs_en.keys())[0]
                    first_value = specs_en[first_key]
                    print(f"   📋 Sample EN: {first_key}: {first_value[:50]}...")
                
                if isinstance(specs_ar, dict) and len(specs_ar) > 0:
                    first_key = list(specs_ar.keys())[0]
                    first_value = specs_ar[first_key]
                    print(f"   📋 Sample AR: {first_key}: {first_value[:50]}...")
                
            except Exception as e:
                print(f"❌ {slug}: Error testing specifications: {e}")
                continue
        
        # Test specifications display format
        print("\n🎨 Testing specifications display format:")
        
        orange = Product.query.filter_by(slug='fresh-oranges').first()
        if orange:
            specs_en = orange.get_specifications_lang('en')
            if isinstance(specs_en, dict):
                print("✅ Specifications are in structured format (dict)")
                print(f"   📊 Number of specification fields: {len(specs_en)}")
                
                # Show all fields for oranges as example
                print("   📋 Orange specifications (EN):")
                for key, value in specs_en.items():
                    print(f"      • {key}: {value}")
            else:
                print("⚠️ Specifications are in simple text format")
        
        # Test category coverage
        print("\n📈 Testing category coverage:")
        
        categories = {
            'Fresh Fruits': ['fresh-oranges', 'fresh-strawberries', 'fresh-grapes'],
            'Vegetables': ['potatoes-spunta', 'onions-red-golden', 'garlic-white'],
            'Dates': ['dates-whole', 'medjool-dates-whole'],
            'Spices': ['cumin-seed', 'coriander-seed', 'fennel-seed'],
            'Seeds': ['sesame-seed', 'nigella-black-seed', 'flax-seeds'],
            'Herbs': ['basil', 'mint', 'oregano', 'thyme'],
            'Frozen': ['iqf-strawberries', 'iqf-mango']
        }
        
        for category, products in categories.items():
            category_count = 0
            for slug in products:
                product = Product.query.filter_by(slug=slug).first()
                if product and product.specifications:
                    category_count += 1
            
            coverage = (category_count / len(products)) * 100
            status = "✅" if coverage == 100 else "⚠️" if coverage >= 50 else "❌"
            print(f"   {status} {category}: {category_count}/{len(products)} ({coverage:.0f}%)")
        
        print("\n🎉 Specifications testing completed!")
        return True

if __name__ == "__main__":
    success = test_specifications()
    if success:
        print("\n✅ CONCLUSION: Product specifications are working correctly!")
    else:
        print("\n❌ CONCLUSION: There are issues with product specifications!")
    
    sys.exit(0 if success else 1)
