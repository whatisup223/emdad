# -*- coding: utf-8 -*-
import os
import sys

# Ensure project root is on sys.path when running from scripts/
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import db, Category, Product, ProductImage

# This is a local, temporary seeding script. Do NOT commit this file.

app = create_app('production')

MANGO = {
    'name_en': 'IQF Mango',
    'name_ar': 'مانجو مجمدة IQF',
    'slug': 'iqf-mango',
    'short_en': 'Premium Egyptian IQF mango slices preserving natural taste and texture.',
    'short_ar': 'شرائح مانجو مصرية مجمدة بتقنية IQF تحافظ على الطعم والقوام الطبيعي.',
    'desc_en': 'Individually Quick Frozen (IQF) mango made from selected ripe mangoes, ideal for smoothies and desserts.',
    'desc_ar': 'مانجو مجمدة فرديًا (IQF) من ثمار مانجو ناضجة مختارة، مثالية للعصائر والحلويات.',
    'image_candidates': [
        'iqf-mango-emdad-global.webp',
        'iqf-mango.svg',
    ],
}

STRAWBERRIES = {
    'name_en': 'IQF Strawberries',
    'name_ar': 'فراولة مجمدة IQF',
    'slug': 'iqf-strawberries',
    'short_en': 'High-quality IQF strawberries with vibrant color and rich flavor.',
    'short_ar': 'فراولة IQF عالية الجودة بلون زاهٍ ونكهة غنية.',
    'desc_en': 'Carefully selected strawberries, individually quick frozen to lock in freshness and nutrients.',
    'desc_ar': 'فراولة مختارة بعناية، مجمدة فرديًا للحفاظ على النضارة والقيمة الغذائية.',
    'image_candidates': [
        'iqf-strawberries-emdad-global.webp',
        'iqf-strawberries.svg',  # exists locally in instance/uploads/products
    ],
}


def find_first_existing_image(app, candidates):
    uploads_root = os.path.join(app.instance_path, app.config.get('UPLOAD_FOLDER', 'uploads'), 'products')
    for fname in candidates:
        if os.path.exists(os.path.join(uploads_root, fname)):
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

    # Try to link an existing local image if available
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
    cat = Category.query.filter_by(key='iqf-fruit').first()
    if not cat:
        raise RuntimeError('IQF Fruit category not found')

    created = []
    for idx, pdata in enumerate([MANGO, STRAWBERRIES], start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

