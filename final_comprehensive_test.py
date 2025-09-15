#!/usr/bin/env python3
"""
Final comprehensive test for HS codes and specifications
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Product

def final_comprehensive_test():
    """Final comprehensive test for all products."""
    app = create_app()
    with app.app_context():
        print("🎯 FINAL COMPREHENSIVE TEST")
        print("=" * 80)
        
        # Test all products
        products = Product.query.all()
        
        print(f"📊 Testing {len(products)} products...")
        print("-" * 80)
        
        issues_found = []
        success_count = 0
        
        for product in products:
            print(f"\n🔍 {product.slug.upper()} ({product.name_en}):")
            
            # Test HS Code
            if not product.hs_code:
                issues_found.append(f"{product.slug}: No HS code")
                print(f"   ❌ No HS code")
                continue
            
            # Test HS Code Description
            desc_en = product.get_hs_code_description('en')
            desc_ar = product.get_hs_code_description('ar')
            
            if not desc_en or not desc_ar:
                issues_found.append(f"{product.slug}: Missing HS description")
                print(f"   ❌ Missing HS description")
                continue
            
            # Test Specifications
            specs_en = product.get_specifications_lang('en')
            specs_ar = product.get_specifications_lang('ar')
            
            if not specs_en or not specs_ar:
                issues_found.append(f"{product.slug}: Missing specifications")
                print(f"   ❌ Missing specifications")
                continue
            
            if not isinstance(specs_en, dict) or not isinstance(specs_ar, dict):
                issues_found.append(f"{product.slug}: Invalid specifications format")
                print(f"   ❌ Invalid specifications format")
                continue
            
            # Check for logical consistency
            logical_issues = []
            
            # Check for obvious mismatches
            if product.slug == 'fresh-oranges':
                if any('thyme' in str(v).lower() or 'herb' in str(v).lower() for v in specs_en.values()):
                    logical_issues.append("Orange has herb-related content")
                if desc_en and 'thyme' in desc_en.lower():
                    logical_issues.append("Orange has thyme HS description")
            
            elif product.slug == 'basil':
                if any('orange' in str(v).lower() or 'citrus' in str(v).lower() for v in specs_en.values()):
                    logical_issues.append("Basil has citrus-related content")
                if desc_en and 'orange' in desc_en.lower():
                    logical_issues.append("Basil has orange HS description")
            
            elif product.slug == 'cumin-seed':
                if any('orange' in str(v).lower() or 'fruit' in str(v).lower() for v in specs_en.values()):
                    logical_issues.append("Cumin has fruit-related content")
                if desc_en and 'orange' in desc_en.lower():
                    logical_issues.append("Cumin has orange HS description")
            
            if logical_issues:
                issues_found.extend([f"{product.slug}: {issue}" for issue in logical_issues])
                print(f"   ⚠️ Logical issues: {', '.join(logical_issues)}")
                continue
            
            # All tests passed
            success_count += 1
            print(f"   ✅ HS Code: {product.hs_code} — {desc_en[:50]}...")
            print(f"   ✅ Specs EN: {len(specs_en)} fields")
            print(f"   ✅ Specs AR: {len(specs_ar)} fields")
            print(f"   ✅ All tests passed!")
        
        print("\n" + "=" * 80)
        print("🎯 FINAL RESULTS:")
        print(f"✅ Successful: {success_count}/{len(products)} products")
        print(f"❌ Issues: {len(issues_found)}")
        
        if issues_found:
            print("\n🚨 ISSUES FOUND:")
            for issue in issues_found:
                print(f"   • {issue}")
        else:
            print("\n🎉 ALL TESTS PASSED! System is ready for production!")
        
        # Test specific products mentioned by user
        print("\n" + "-" * 80)
        print("🧪 SPECIFIC PRODUCT VERIFICATION:")
        
        test_cases = [
            ('fresh-oranges', 'برتقال طازج', '080510'),
            ('basil', 'ريحان', '121190'),
            ('cumin-seed', 'بذور كمون', '090930'),
        ]
        
        for slug, expected_ar_name, expected_hs in test_cases:
            product = Product.query.filter_by(slug=slug).first()
            if product:
                print(f"\n🔍 {slug}:")
                print(f"   Name AR: {product.name_ar} (expected: {expected_ar_name})")
                print(f"   HS Code: {product.hs_code} (expected: {expected_hs})")
                print(f"   HS Desc EN: {product.get_hs_code_description('en')}")
                print(f"   HS Desc AR: {product.get_hs_code_description('ar')}")
                
                if product.hs_code == expected_hs:
                    print(f"   ✅ HS Code correct!")
                else:
                    print(f"   ❌ HS Code mismatch!")
        
        return len(issues_found) == 0

if __name__ == "__main__":
    success = final_comprehensive_test()
    
    if success:
        print("\n🏆 CONCLUSION: System is PERFECT and ready for production! 🚀")
        exit(0)
    else:
        print("\n💥 CONCLUSION: Issues found that need to be fixed!")
        exit(1)
