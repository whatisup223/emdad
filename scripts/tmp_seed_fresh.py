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

# Local temporary script to seed Fresh Fruit test products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Oranges',
        'name_ar': 'برتقال',
        'slug': 'oranges',
        'short_en': 'Fresh Egyptian oranges with vibrant color and rich citrus flavor.',
        'short_ar': 'برتقال مصري طازج بلون زاهٍ ونكهة حمضية غنية.',
        'desc_en': 'Carefully selected oranges known for juiciness and sweetness, ideal for fresh consumption and juicing.',
        'desc_ar': 'برتقال مختار بعناية يتميز بالعصيرية والحلاوة، مثالي للأكل الطازج والعصير.',
        'image_candidates': [
            'oranges-emdad-global.webp',
            'egyptian-oranges.svg',
            'premium-valencia-oranges.svg',
        ],
    },
    {
        'name_en': 'Mandarins',
        'name_ar': 'يوسفي',
        'slug': 'mandarins',
        'short_en': 'Sweet and easy-to-peel Egyptian mandarins.',
        'short_ar': 'يوسفي مصري حلو سهل التقشير.',
        'desc_en': 'Popular citrus variety with tender segments and bright aroma, perfect for snacks and salads.',
        'desc_ar': 'نوع شائع من الموالح بفصوص طرية ورائحة منعشة، مثالي للوجبات الخفيفة والسلطات.',
        'image_candidates': [
            'mandarins-emdad-global.webp',
            'mandarins.svg',
        ],
    },
    {
        'name_en': 'Tangerines',
        'name_ar': 'تانجرين',
        'slug': 'tangerines',
        'short_en': 'Aromatic, juicy tangerines with balanced sweetness.',
        'short_ar': 'تانجرين عطِر وعصيري بحلاوة متوازنة.',
        'desc_en': 'Delicate citrus fruits known for their fragrant peel and tender segments.',
        'desc_ar': 'فاكهة حمضية لطيفة مع قشر عطِر وفصوص طرية.',
        'image_candidates': [
            'tangerines-emdad-global.webp',
            # fallback intentionally none if not found
        ],
    },
    {
        'name_en': 'Strawberries',
        'name_ar': 'فراولة طازجة',
        'slug': 'strawberries',
        'short_en': 'Fresh Egyptian strawberries, bright red and naturally sweet.',
        'short_ar': 'فراولة مصرية طازجة بلون أحمر زاهٍ وحلاوة طبيعية.',
        'desc_en': 'Hand-picked strawberries ideal for fresh eating, desserts, and smoothies.',
        'desc_ar': 'فراولة منتقاة بعناية مثالية للأكل الطازج والحلويات والعصائر.',
        'image_candidates': [
            'strawberries-emdad-global.webp',
            # if no fresh image is available, leave placeholder
        ],
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
    cat = Category.query.filter_by(key='fresh-fruit').first()
    if not cat:
        raise RuntimeError('Fresh Fruit category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

