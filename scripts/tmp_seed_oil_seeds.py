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

# Local temporary script to seed Oil Seeds products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Sesame Seeds',
        'name_ar': 'بذور السمسم',
        'slug': 'sesame-seeds',
        'short_en': 'High-quality sesame seeds rich in oil and flavor.',
        'short_ar': 'بذور سمسم عالية الجودة غنية بالزيت والنكهة.',
        'desc_en': 'Suitable for bakery, tahini, and oil extraction.',
        'desc_ar': 'مناسبة للمخبوزات وإنتاج الطحينة واستخلاص الزيت.',
        'image_candidates': ['sesame-seeds-emdad-global.webp'],
    },
    {
        'name_en': 'Flax Seeds',
        'name_ar': 'بذور الكتان',
        'slug': 'flax-seeds',
        'short_en': 'Nutrient-rich flax seeds with mild nutty flavor.',
        'short_ar': 'بذور كتان غنية بالعناصر الغذائية بنكهة جوزية خفيفة.',
        'desc_en': 'Ideal for bakery, cereals, and oil extraction.',
        'desc_ar': 'مثالية للمخبوزات والحبوب واستخلاص الزيت.',
        'image_candidates': ['flax-seeds-emdad-global.webp'],
    },
]


def find_first_existing_image(app, candidates):
    uploads_root = os.path.join(app.instance_path, app.config.get('UPLOAD_FOLDER', 'uploads'), 'products')
    for fname in candidates:
        if fname and os.path.exists(os.path.join(uploads_root, fname)):
            return fname
    return None


def upsert_product(cat, pdata, sort_order):
    p = Product.query.filter_by(slug=pdata['slug']).first()
    if p:
        return p, False
    p = Product(
        name_en=pdata['name_en'],
        name_ar=pdata['name_ar'],
        slug=pdata['slug'],
        category_id=cat.id,
        description_en=pdata['desc_en'],
        description_ar=pdata['desc_ar'],
        short_description_en=pdata['short_en'],
        short_description_ar=pdata['short_ar'],
        status='active',
        featured=True,
        show_on_homepage=True,
        sort_order=sort_order,
    )

    img_name = find_first_existing_image(app, pdata['image_candidates'])
    if img_name:
        p.image_path = img_name
    db.session.add(p)
    db.session.flush()

    if img_name:
        db.session.add(ProductImage(
            product_id=p.id,
            filename=img_name,
            alt_text_en=pdata['name_en'],
            alt_text_ar=pdata['name_ar'],
            is_main=True,
            sort_order=0,
        ))

    return p, True


with app.app_context():
    cat = Category.query.filter_by(key='oil-seeds').first()
    if not cat:
        cat = Category.query.filter_by(name_en='Oil Seeds').first()
    if not cat:
        raise RuntimeError('Oil Seeds category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

