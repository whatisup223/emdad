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

# Local temporary script to seed Vegetables & Roots products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Potatoes',
        'name_ar': 'بطاطس',
        'slug': 'potatoes',
        'short_en': 'Fresh Egyptian potatoes suitable for multiple culinary uses.',
        'short_ar': 'بطاطس مصرية طازجة مناسبة لمختلف الاستخدامات الطهوية.',
        'desc_en': 'Carefully selected potatoes with good texture, great for frying, baking, or mashing.',
        'desc_ar': 'بطاطس مختارة بعناية بقوام ممتاز للقلي والخبز والهرس.',
        'image_candidates': ['potatoes-emdad-global.webp', 'fresh-potatoes.svg'],
    },
    {
        'name_en': 'Sweet Potatoes',
        'name_ar': 'بطاطا حلوة',
        'slug': 'sweet-potatoes',
        'short_en': 'Naturally sweet Egyptian sweet potatoes.',
        'short_ar': 'بطاطا حلوة مصرية بطعم طبيعي حلو.',
        'desc_en': 'Rich in flavor and nutrients, ideal for baking, roasting, and purees.',
        'desc_ar': 'غنية بالنكهة والعناصر الغذائية، مثالية للخبز والتحميص والهرسات.',
        'image_candidates': ['sweet-potatoes-emdad-global.webp'],
    },
    {
        'name_en': 'Onions',
        'name_ar': 'بصل',
        'slug': 'onions',
        'short_en': 'Quality Egyptian onions with strong flavor and aroma.',
        'short_ar': 'بصل مصري عالي الجودة بنكهة ورائحة قوية.',
        'desc_en': 'Suitable for fresh consumption, cooking, and industrial processing.',
        'desc_ar': 'مناسب للأكل الطازج والطهي والمعالجة الصناعية.',
        'image_candidates': ['onions-emdad-global.webp', 'fresh-red-onions.svg'],
    },
    {
        'name_en': 'Garlic',
        'name_ar': 'ثوم',
        'slug': 'garlic',
        'short_en': 'Egyptian garlic with robust aroma and taste.',
        'short_ar': 'ثوم مصري بنكهة ورائحة قوية.',
        'desc_en': 'Popular variety ideal for seasonings, pickling, and culinary uses.',
        'desc_ar': 'نوع شائع مثالي للتتبيل والتخليل والاستخدامات الطهوية.',
        'image_candidates': ['garlic-emdad-global.webp', 'egyptian-garlic.svg'],
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
    cat = Category.query.filter_by(key='vegetables-roots').first()
    if not cat:
        cat = Category.query.filter_by(name_en='Vegetables & Roots').first()
    if not cat:
        raise RuntimeError('Vegetables & Roots category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

