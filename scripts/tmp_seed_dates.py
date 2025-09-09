# -*- coding: utf-8 -*-
import os
import sys

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import db, Category, Product, ProductImage

# Local temporary script to seed Dates -> "Dates Whole". Do NOT commit.

app = create_app('production')

PRODUCT = {
    'name_en': 'Dates Whole',
    'name_ar': 'تمور كاملة',
    'slug': 'dates-whole',
    'short_en': 'Premium Egyptian whole dates, naturally sweet and energy-rich.',
    'short_ar': 'تمور مصرية كاملة عالية الجودة بطعم طبيعي حلو وغنية بالطاقة.',
    'desc_en': 'Whole dates carefully selected, ideal for snacking, baking, and industrial uses.',
    'desc_ar': 'تمور كاملة مختارة بعناية، مثالية للتناول الخفيف والخبز والاستخدامات الصناعية.',
    'image_candidates': [
        'dates-whole-emdad-global.webp',
        'dates-emdad-global.webp',
    ],
}


def find_first_existing_image(app, candidates):
    uploads_root = os.path.join(app.instance_path, app.config.get('UPLOAD_FOLDER', 'uploads'), 'products')
    for fname in candidates:
        if fname and os.path.exists(os.path.join(uploads_root, fname)):
            return fname
    return None


with app.app_context():
    cat = Category.query.filter_by(key='dates').first()
    if not cat:
        # fallback by english name if key not found
        cat = Category.query.filter_by(name_en='Dates').first()
    if not cat:
        raise RuntimeError('Dates category not found')

    slug = PRODUCT['slug']
    p = Product.query.filter_by(slug=slug).first()
    if not p:
        p = Product(
            name_en=PRODUCT['name_en'],
            name_ar=PRODUCT['name_ar'],
            slug=slug,
            category_id=cat.id,
            description_en=PRODUCT['desc_en'],
            description_ar=PRODUCT['desc_ar'],
            short_description_en=PRODUCT['short_en'],
            short_description_ar=PRODUCT['short_ar'],
            status='active',
            featured=True,
            show_on_homepage=True,
            sort_order=1,
        )
        img_name = find_first_existing_image(app, PRODUCT['image_candidates'])
        if img_name:
            p.image_path = img_name
        db.session.add(p)
        db.session.flush()
        if img_name:
            db.session.add(ProductImage(
                product_id=p.id,
                filename=img_name,
                alt_text_en=PRODUCT['name_en'],
                alt_text_ar=PRODUCT['name_ar'],
                is_main=True,
                sort_order=0,
            ))
        db.session.commit()
        print('Created product:', slug, '| image:', p.image_path)
    else:
        print('Product already exists:', slug, '| image:', p.image_path)

