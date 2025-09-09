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

# Local temporary script to seed Dried Herbs products. Do NOT commit.

app = create_app('production')

PRODUCTS = [
    {
        'name_en': 'Basil',
        'name_ar': 'ريحان',
        'slug': 'basil',
        'short_en': 'High-quality dried basil with aromatic flavor.',
        'short_ar': 'ريحان مجفف عالي الجودة بنكهة عطرية.',
        'desc_en': 'Carefully dried basil leaves ideal for sauces, seasonings, and culinary applications.',
        'desc_ar': 'أوراق ريحان مجففة بعناية مثالية للصلصات والتتبيل والاستخدامات الطهوية.',
        'image_candidates': ['basil-emdad-global.webp'],
    },
    {
        'name_en': 'Marjoram',
        'name_ar': 'مردقوش',
        'slug': 'marjoram',
        'short_en': 'Premium dried marjoram with warm herbal notes.',
        'short_ar': 'مردقوش مجفف ممتاز بنكهات عشبية دافئة.',
        'desc_en': 'Well-dried marjoram suitable for seasoning and spice blends.',
        'desc_ar': 'مردقوش مُجفف جيداً مناسب للتتبيل وخلطات البهارات.',
        'image_candidates': ['marjoram-emdad-global.webp'],
    },
    {
        'name_en': 'Mint',
        'name_ar': 'نعناع',
        'slug': 'mint',
        'short_en': 'Aromatic dried mint, refreshing and flavorful.',
        'short_ar': 'نعناع مجفف عطِر ومنعش.',
        'desc_en': 'Dried mint leaves perfect for tea blends and seasoning.',
        'desc_ar': 'أوراق نعناع مجففة مثالية لخليط الشاي والتتبيل.',
        'image_candidates': ['mint-emdad-global.webp'],
    },
    {
        'name_en': 'Dill',
        'name_ar': 'شبت',
        'slug': 'dill',
        'short_en': 'Dried dill with distinctive herbal taste.',
        'short_ar': 'شبت مجفف بطعم عشبي مميز.',
        'desc_en': 'Ideal for pickling, soups, and savory dishes.',
        'desc_ar': 'مثالي للتخليل والشوربات والأطباق المالحة.',
        'image_candidates': ['dill-emdad-global.webp'],
    },
    {
        'name_en': 'Parsley',
        'name_ar': 'بقدونس',
        'slug': 'parsley',
        'short_en': 'Dried parsley with fresh herbal notes.',
        'short_ar': 'بقدونس مجفف بنكهات عشبية طازجة.',
        'desc_en': 'Finely dried parsley for seasoning and garnish.',
        'desc_ar': 'بقدونس مجفف بدقة للتتبيل والزينة.',
        'image_candidates': ['parsley-emdad-global.webp'],
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
    cat = Category.query.filter_by(key='dried-herbs').first()
    if not cat:
        cat = Category.query.filter_by(name_en='Dried Herbs').first()
    if not cat:
        raise RuntimeError('Dried Herbs category not found')

    created = []
    for idx, pdata in enumerate(PRODUCTS, start=1):
        _, was_created = upsert_product(cat, pdata, sort_order=idx)
        if was_created:
            created.append(pdata['slug'])

    db.session.commit()
    print('Created products:', created)

