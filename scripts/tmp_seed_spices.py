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

# Local temporary script to seed Spices products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Cumin Seed',
        'name_ar': 'بذور الكمون',
        'slug': 'cumin-seed',
        'short_en': 'Premium cumin seeds with warm, earthy aroma.',
        'short_ar': 'بذور كمون عالية الجودة برائحة دافئة وترابية.',
        'desc_en': 'Carefully cleaned and graded cumin seeds ideal for seasoning and industrial use.',
        'desc_ar': 'بذور كمون مُنظَّفة ومصنَّفة بعناية مثالية للتتبيل والاستخدام الصناعي.',
        'image_candidates': ['cumin-seed-emdad-global.webp'],
    },
    {
        'name_en': 'Coriander Seed',
        'name_ar': 'بذور الكزبرة',
        'slug': 'coriander-seed',
        'short_en': 'Aromatic coriander seeds with citrusy notes.',
        'short_ar': 'بذور كزبرة عطرية بلمسات حمضية.',
        'desc_en': 'Well-dried coriander seeds suitable for whole or ground applications.',
        'desc_ar': 'بذور كزبرة مجففة جيداً مناسبة للاستخدام حباً أو مطحونة.',
        'image_candidates': ['coriander-seed-emdad-global.webp'],
    },
    {
        'name_en': 'Fennel Seed',
        'name_ar': 'بذور الشمر',
        'slug': 'fennel-seed',
        'short_en': 'Sweet fennel seeds with distinctive anise-like flavor.',
        'short_ar': 'بذور شمر بحلاوة ونكهة مميزة قريبة من اليانسون.',
        'desc_en': 'Uniform fennel seeds, ideal for bakery, tea blends, and spice mixes.',
        'desc_ar': 'بذور شمر متجانسة مثالية للمخبوزات وخليط الشاي والبهارات.',
        'image_candidates': ['fennel-seed-emdad-global.webp'],
    },
    {
        'name_en': 'Caraway Seed',
        'name_ar': 'بذور الكراوية',
        'slug': 'caraway-seed',
        'short_en': 'High-quality caraway seeds with warm, peppery notes.',
        'short_ar': 'بذور كراوية عالية الجودة بنكهات دافئة ولمسات فلفلية.',
        'desc_en': 'Suitable for confectionery, bread, and savory dishes.',
        'desc_ar': 'مناسبة للحلويات والخبز والأطباق المالحة.',
        'image_candidates': ['caraway-seed-emdad-global.webp'],
    },
    {
        'name_en': 'Anise Seed',
        'name_ar': 'بذور اليانسون',
        'slug': 'anise-seed',
        'short_en': 'Fragrant anise seeds with sweet, licorice-like flavor.',
        'short_ar': 'بذور يانسون عطرية بنكهات حلوة قريبة من العِرقسوس.',
        'desc_en': 'Perfect for bakery, tea, and flavoring applications.',
        'desc_ar': 'مثالية للمخبوزات والشاي وتطبيقات النكهات.',
        'image_candidates': ['anise-seed-emdad-global.webp'],
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
    cat = Category.query.filter_by(key='spices').first()
    if not cat:
        cat = Category.query.filter_by(name_en='Spices').first()
    if not cat:
        raise RuntimeError('Spices category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

