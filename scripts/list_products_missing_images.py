# -*- coding: utf-8 -*-
import os
import sys

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import db, Product, Category

# Local inspection script. Do NOT commit.

app = create_app('production')

with app.app_context():
    products = Product.query.order_by(Product.category_id, Product.sort_order, Product.name_en).all()
    missing = []
    have_any = []
    for p in products:
        cat = Category.query.get(p.category_id)
        main = p.get_main_image()
        has_any = bool(main) or bool(p.image_path)
        if not has_any:
            candidate = f"{p.slug}-emdad-global.webp"
            missing.append({
                'category_key': getattr(cat, 'key', None),
                'slug': p.slug,
                'name_en': p.name_en,
                'name_ar': p.name_ar,
                'proposed_filename': candidate,
            })
        else:
            have_any.append({
                'category_key': getattr(cat, 'key', None),
                'slug': p.slug,
                'name_en': p.name_en,
                'name_ar': p.name_ar,
                'image_path': p.image_path,
                'has_main_image': bool(main),
            })

    print('TOTAL PRODUCTS:', len(products))
    print('NEED IMAGES (no main image and no image_path):', len(missing))
    for m in missing:
        print(f" - [{m['category_key']}] {m['slug']} :: {m['proposed_filename']}")

