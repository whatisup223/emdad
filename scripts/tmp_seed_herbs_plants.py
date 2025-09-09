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

# Local temporary script to seed Herbs & Herbal Plants products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Chamomile',
        'name_ar': 'بابونج',
        'slug': 'chamomile',
        'short_en': 'Dried chamomile with soothing aroma.',
        'short_ar': 'بابونج مجفف برائحة مهدّئة.',
        'desc_en': 'Carefully dried chamomile flowers ideal for tea blends and herbal infusions.',
        'desc_ar': 'أزهار بابونج مجففة بعناية مثالية لخليط الشاي والمشروبات العشبية.',
        'image_candidates': ['chamomile-emdad-global.webp'],
    },
    {
        'name_en': 'Hibiscus',
        'name_ar': 'كركديه',
        'slug': 'hibiscus',
        'short_en': 'Premium dried hibiscus with rich color and tangy flavor.',
        'short_ar': 'كركديه مجفف ممتاز بلون غني ونكهة حامضية.',
        'desc_en': 'Selected hibiscus petals perfect for teas, syrups, and culinary uses.',
        'desc_ar': 'بتلات كركديه مختارة مثالية للشاي والشرابات والاستخدامات الطهوية.',
        'image_candidates': ['hibiscus-emdad-global.webp'],
    },
    {
        'name_en': 'Calendula',
        'name_ar': 'آذريون',
        'slug': 'calendula',
        'short_en': 'Dried calendula petals with bright color.',
        'short_ar': 'بتلات آذريون مجففة بلون زاهٍ.',
        'desc_en': 'Ideal for herbal blends, seasoning, and natural coloring.',
        'desc_ar': 'مثالية للخلطات العشبية والتتبيل والتلوين الطبيعي.',
        'image_candidates': ['calendula-emdad-global.webp'],
    },
    {
        'name_en': 'Lemongrass',
        'name_ar': 'حشيشة الليمون',
        'slug': 'lemongrass',
        'short_en': 'Aromatic lemongrass with fresh citrus notes.',
        'short_ar': 'حشيشة ليمون عطرية بلمسات حمضية طازجة.',
        'desc_en': 'Dried lemongrass suitable for teas and seasoning.',
        'desc_ar': 'حشيشة ليمون مجففة مناسبة للشاي والتتبيل.',
        'image_candidates': ['lemongrass-emdad-global.webp'],
    },
    {
        'name_en': 'Sage',
        'name_ar': 'مريمية',
        'slug': 'sage',
        'short_en': 'Dried sage leaves with warm herbal aroma.',
        'short_ar': 'أوراق مريمية مجففة برائحة عشبية دافئة.',
        'desc_en': 'Perfect for teas and culinary seasoning.',
        'desc_ar': 'مثالية للشاي والتتبيل الطهوي.',
        'image_candidates': ['sage-emdad-global.webp'],
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
    cat = Category.query.filter_by(key='herbs-herbal-plants').first()
    if not cat:
        cat = Category.query.filter_by(name_en='Herbs & Herbal Plants').first()
    if not cat:
        raise RuntimeError('Herbs & Herbal Plants category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

