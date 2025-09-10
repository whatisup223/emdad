#!/usr/bin/env python3
"""
Test script to verify the updated seeding system works correctly.
This script tests the new 38-product structure with all categories and seasonality data.
"""

import os
import sys
import json

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_seeds_file():
    """Test that the seeds/products.json file is valid and contains 38 products."""
    print("🧪 Testing seeds/products.json file...")
    
    seeds_path = os.path.join(os.path.dirname(__file__), 'seeds', 'products.json')
    if not os.path.exists(seeds_path):
        print(f"❌ Seeds file not found: {seeds_path}")
        return False
    
    try:
        with open(seeds_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data.get('products', [])
        print(f"   Found {len(products)} products in seeds file")
        
        if len(products) != 38:
            print(f"❌ Expected 38 products, found {len(products)}")
            return False
        
        # Test required fields
        required_fields = ['slug', 'category_key', 'name_en', 'name_ar', 'image_filename']
        missing_fields = []
        
        for i, product in enumerate(products):
            for field in required_fields:
                if field not in product:
                    missing_fields.append(f"Product {i+1} missing {field}")
        
        if missing_fields:
            print(f"❌ Missing required fields:")
            for error in missing_fields[:5]:  # Show first 5 errors
                print(f"   {error}")
            return False
        
        # Test category keys
        expected_categories = {
            'fresh-citrus', 'fresh-vegetables', 'fresh-fruit', 'dates', 
            'iqf', 'spices', 'herbs-herbal-plants', 'oil-seeds'
        }
        found_categories = set(p['category_key'] for p in products)
        
        if found_categories != expected_categories:
            print(f"❌ Category key mismatch:")
            print(f"   Expected: {expected_categories}")
            print(f"   Found: {found_categories}")
            return False
        
        # Test seasonality data
        products_with_seasonality = sum(1 for p in products if 'seasonality' in p)
        print(f"   Products with seasonality data: {products_with_seasonality}/38")
        
        if products_with_seasonality != 38:
            print(f"❌ Expected all 38 products to have seasonality data, found {products_with_seasonality}")
            return False
        
        print("✅ Seeds file validation passed")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in seeds file: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading seeds file: {e}")
        return False

def test_database_seeding():
    """Test that the database seeding works correctly."""
    print("\n🧪 Testing database seeding...")
    
    try:
        from app import create_app
        from app.models import Product, Category, db
        from init_db_render import seed_official_products, reset_and_seed_categories
        
        app = create_app()
        with app.app_context():
            # Clear existing data
            print("   Clearing existing data...")
            Product.query.delete()
            Category.query.delete()
            db.session.commit()
            
            # Test category seeding
            print("   Testing category seeding...")
            reset_and_seed_categories(db)
            db.session.commit()
            
            categories = Category.query.all()
            print(f"   Created {len(categories)} categories")
            
            if len(categories) != 8:
                print(f"❌ Expected 8 categories, found {len(categories)}")
                return False
            
            # Test product seeding
            print("   Testing product seeding...")
            seed_official_products(db)
            db.session.commit()
            
            products = Product.query.filter_by(status='active').all()
            print(f"   Created {len(products)} active products")
            
            if len(products) != 38:
                print(f"❌ Expected 38 products, found {len(products)}")
                return False
            
            # Test seasonality data
            products_with_seasonality = sum(1 for p in products if p.seasonality)
            print(f"   Products with seasonality: {products_with_seasonality}/38")
            
            if products_with_seasonality != 38:
                print(f"❌ Expected all 38 products to have seasonality, found {products_with_seasonality}")
                return False
            
            # Test category distribution
            category_counts = {}
            for product in products:
                cat_key = product.category.key if product.category else 'unknown'
                category_counts[cat_key] = category_counts.get(cat_key, 0) + 1
            
            print("   Category distribution:")
            for cat_key, count in sorted(category_counts.items()):
                print(f"     {cat_key}: {count} products")
            
            expected_distribution = {
                'fresh-citrus': 3,
                'fresh-vegetables': 5,
                'fresh-fruit': 4,
                'dates': 4,
                'iqf': 2,
                'spices': 6,
                'herbs-herbal-plants': 12,
                'oil-seeds': 2
            }
            
            if category_counts != expected_distribution:
                print(f"❌ Category distribution mismatch:")
                print(f"   Expected: {expected_distribution}")
                print(f"   Found: {category_counts}")
                return False
            
            print("✅ Database seeding test passed")
            return True
            
    except Exception as e:
        print(f"❌ Database seeding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Updated Seeding System")
    print("=" * 50)
    
    tests = [
        test_seeds_file,
        test_database_seeding,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test failed: {test.__name__}")
        except Exception as e:
            print(f"❌ Test error in {test.__name__}: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The updated seeding system is ready for production deployment")
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️ Please fix the issues before deploying to production")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
