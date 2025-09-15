#!/usr/bin/env python3
"""
Migration script to add default HS codes to existing products.
This script can be run in development and will be automatically executed during production deployment.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_default_hs_codes():
    """
    Returns a dictionary mapping product slugs to their appropriate HS codes.
    HS codes are based on the Harmonized System for international trade classification.
    Based on actual products in the database as of 2025-01-15.
    """
    return {
        # Fresh Citrus Fruits (Chapter 08)
        'fresh-oranges': '080510',          # Fresh oranges
        'fresh-mandarins': '080520',        # Fresh mandarins
        'fresh-tangerines': '080520',       # Fresh tangerines (same as mandarins)

        # Fresh Fruits (Chapter 08)
        'fresh-strawberries': '081010',     # Fresh strawberries
        'fresh-grapes': '080610',           # Fresh grapes
        'fresh-pomegranates': '081090',     # Other fresh fruits
        'fresh-mango': '080450',            # Fresh mangoes

        # Fresh Vegetables (Chapter 07)
        'potatoes-spunta': '070190',        # Other fresh vegetables
        'sweet-potatoes-beauregard': '071420', # Sweet potatoes
        'fresh-spring-onions': '070390',    # Other onions
        'onions-red-golden': '070310',      # Fresh onions
        'garlic-white': '070320',           # Fresh garlic

        # Dried Fruits (Chapter 08)
        'dates-whole': '080410',            # Fresh or dried dates
        'dates-pitted': '080410',           # Fresh or dried dates
        'medjool-dates-whole': '080410',    # Fresh or dried dates (premium variety)
        'medjool-dates-pitted': '080410',   # Fresh or dried dates (premium variety)

        # Spices (Chapter 09)
        'cumin-seed': '090930',             # Cumin seeds
        'coriander-seed': '090920',         # Coriander seeds
        'fennel-seed': '090960',            # Fennel seeds
        'anise-seed': '090950',             # Anise seeds
        'caraway-seed': '090940',           # Caraway seeds
        'nigella-black-seed': '121190',     # Other oil seeds (black cumin)

        # Oil Seeds (Chapter 12)
        'sesame-seed': '120740',            # Sesame seeds
        'flax-seeds': '120400',             # Flax seeds

        # Herbs and Plants (Chapter 12)
        'basil': '121190',                  # Other plants/herbs
        'parsley-flakes': '121190',         # Other plants/herbs
        'dill': '121190',                   # Other plants/herbs
        'mint': '121190',                   # Other plants/herbs
        'oregano': '121190',                # Other plants/herbs
        'thyme': '121190',                  # Other plants/herbs
        'sage': '121190',                   # Other plants/herbs
        'marjoram': '121190',               # Other plants/herbs
        'lemongrass': '121190',             # Other plants/herbs
        'chamomile': '121190',              # Other plants/herbs
        'calendula': '121190',              # Other plants/herbs
        'hibiscus': '121190',               # Other plants/herbs

        # IQF/Frozen Products (Chapter 08/07)
        'iqf-strawberries': '081110',       # Frozen strawberries
        'iqf-mango': '081140',              # Frozen mangoes
    }

def update_product_hs_codes():
    """Update products with default HS codes."""
    try:
        from app import create_app, db
        from app.models import Product
        
        app = create_app()
        with app.app_context():
            hs_codes = get_default_hs_codes()
            updated_count = 0
            not_found_count = 0
            
            print("🔄 Starting HS code assignment...")
            
            for slug, hs_code in hs_codes.items():
                product = Product.query.filter_by(slug=slug).first()
                if product:
                    if not product.hs_code:  # Only update if HS code is not already set
                        product.hs_code = hs_code
                        updated_count += 1
                        print(f"✅ Updated {slug}: HS:{hs_code}")
                    else:
                        print(f"⏭️ Skipped {slug}: Already has HS code {product.hs_code}")
                else:
                    not_found_count += 1
                    print(f"⚠️ Product not found: {slug}")
            
            if updated_count > 0:
                db.session.commit()
                print(f"\n✅ Successfully updated {updated_count} products with HS codes")
            else:
                print("\n✅ No products needed HS code updates")
                
            if not_found_count > 0:
                print(f"⚠️ {not_found_count} products from the HS code list were not found in database")
                
            # Verify results
            total_with_hs = Product.query.filter(Product.hs_code.isnot(None)).count()
            total_products = Product.query.count()
            print(f"📊 Final status: {total_with_hs}/{total_products} products have HS codes")
            
            return True
            
    except Exception as e:
        print(f"❌ Error updating HS codes: {e}")
        return False

if __name__ == "__main__":
    success = update_product_hs_codes()
    sys.exit(0 if success else 1)
