#!/usr/bin/env python3
"""
Database initialization script for Render deployment with complete sample data
"""

import sys
import os
from datetime import datetime, timedelta

def create_admin_user(db):
    """Create admin user"""
    from app.models import User

    admin_user = User.query.filter_by(email='admin@emdadglobal.com').first()
    if not admin_user:
        print("Creating admin user...")
        admin_user = User(
            name='Administrator',
            email='admin@emdadglobal.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        print("✅ Admin user created successfully!")
    else:
        print("✅ Admin user already exists")

def reset_and_seed_categories(db):
    """One-time hard reset of categories/products and seed new official categories.
    Uses AppMeta flag to ensure it runs only once per environment.
    """
    from app.models import Category, Product, ProductImage, AppMeta

    FLAG_KEY = 'seed:new_categories_v1'
    if AppMeta.get(FLAG_KEY):
        print("✅ Category reset already applied. Skipping hard reset.")
        return

    print("⚠️ Resetting existing products and categories...")
    # Delete product images via cascade by deleting products
    try:
        # Remove products first (cascade removes ProductImage)
        Product.query.delete()
        db.session.commit()
    except Exception as e:
        print(f"⚠️ Failed deleting products: {e}")
        db.session.rollback()

    try:
        # Remove all categories
        Category.query.delete()
        db.session.commit()
    except Exception as e:
        print(f"⚠️ Failed deleting categories: {e}")
        db.session.rollback()

    print("✅ Inserting new official categories...")
    categories = [
        {
            'key': 'iqf-fruit',
            'name_en': 'IQF Fruit',
            'name_ar': 'فواكه مجمدة (IQF)',
            'slug': 'iqf-fruit',
            'description_en': 'Individually Quick Frozen fruits preserving taste and nutrition.',
            'description_ar': 'فواكه مجمدة سريعاً بشكل فردي مع الحفاظ على الطعم والقيمة الغذائية.',
            'sort_order': 3,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'fresh-fruit',
            'name_en': 'Fresh Fruit',
            'name_ar': 'فواكه طازجة',
            'slug': 'fresh-fruit',
            'description_en': 'Seasonal premium fresh fruits from selected farms.',
            'description_ar': 'فواكه طازجة موسمية ممتازة من مزارع مختارة.',
            'sort_order': 1,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'dates',
            'name_en': 'Dates',
            'name_ar': 'تمور',
            'slug': 'dates',
            'description_en': 'High-quality Egyptian dates with rich flavor.',
            'description_ar': 'تمور مصرية عالية الجودة بطعم غني.',
            'sort_order': 4,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'spices',
            'name_en': 'Spices',
            'name_ar': 'توابل',
            'slug': 'spices',
            'description_en': 'Aromatic spices sourced and processed with care.',
            'description_ar': 'توابل عطرية يتم الحصول عليها ومعالجتها بعناية.',
            'sort_order': 5,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'dried-herbs',
            'name_en': 'Dried Herbs',
            'name_ar': 'أعشاب مجففة',
            'slug': 'dried-herbs',
            'description_en': 'Naturally dried herbs retaining their essential aromas.',
            'description_ar': 'أعشاب مجففة بشكل طبيعي تحتفظ بروائحها الأساسية.',
            'sort_order': 6,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'vegetables-roots',
            'name_en': 'Vegetables & Roots',
            'name_ar': 'خضروات وجذور',
            'slug': 'vegetables-roots',
            'description_en': 'Fresh vegetables and root crops of export quality.',
            'description_ar': 'خضروات ومحاصيل جذرية طازجة بجودة التصدير.',
            'sort_order': 2,
            'show_on_homepage': True,
            'image_path': None,
        },
        {
            'key': 'herbs-herbal-plants',
            'name_en': 'Herbs & Herbal Plants',
            'name_ar': 'أعشاب ونباتات عشبية',
            'slug': 'herbs-herbal-plants',
            'description_en': 'Culinary and medicinal herbs, carefully curated.',
            'description_ar': 'أعشاب للطهي والطب التقليدي مختارة بعناية.',
            'sort_order': 7,
            'show_on_homepage': False,
            'image_path': None,
        },
        {
            'key': 'oil-seeds',
            'name_en': 'Oil Seeds',
            'name_ar': 'بذور زيتية',
            'slug': 'oil-seeds',
            'description_en': 'Premium oil seeds suitable for various applications.',
            'description_ar': 'بذور زيتية ممتازة مناسبة لتطبيقات متعددة.',
            'sort_order': 8,
            'show_on_homepage': False,
            'image_path': None,
        },
    ]

    from app.models import Category
    for c in categories:
        category = Category(
            key=c['key'],
            name_en=c['name_en'],
            name_ar=c['name_ar'],
            slug=c['slug'],
            description_en=c['description_en'],
            description_ar=c['description_ar'],
            sort_order=c['sort_order'],
            is_active=True,
            show_on_homepage=c['show_on_homepage'],
            image_path=c['image_path']
        )
        db.session.add(category)
    db.session.commit()

    # Mark flag so this hard reset does not run again automatically
    AppMeta.set(FLAG_KEY, "applied")
    db.session.commit()
    print("✅ New categories seeded successfully.")


def ensure_min_homepage_categories(db, min_count=6):
    """Ensure at least `min_count` active categories are marked to show on homepage.
    Idempotent and safe to run on every deploy.
    """
    from app.models import Category
    try:
        cats = Category.query.filter_by(is_active=True).order_by(Category.sort_order, Category.name_en).all()
        current = [c for c in cats if c.show_on_homepage]
        if len(current) >= min_count:
            print(f"✅ Homepage categories already >= {min_count}.")
            return
        for c in cats:
            if not c.show_on_homepage:
                c.show_on_homepage = True
                db.session.add(c)
                current.append(c)
                if len(current) >= min_count:
                    break
        db.session.commit()
        print(f"✅ Ensured at least {min_count} homepage categories (now {len(current)}).")
    except Exception as e:
        print(f"⚠️ Failed ensuring homepage categories: {e}")
        db.session.rollback()



def ensure_category_images(db):
    """Download real illustrative images for categories into uploads and update DB.
    Safe to run every deploy; skips if files already exist.
    """
    import os
    import urllib.request
    from flask import current_app
    from app.models import Category

    # Target filenames per category
    image_plan = {
        'fresh-fruit': {
            'filename': 'fresh-fruit.jpg',
            'url': 'https://source.unsplash.com/1200x800/?fruit,fruits'
        },
        'vegetables-roots': {
            'filename': 'vegetables-roots.jpg',
            'url': 'https://source.unsplash.com/1200x800/?vegetables,roots'
        },
        'iqf-fruit': {
            'filename': 'iqf-fruit.jpg',
            'url': 'https://source.unsplash.com/1200x800/?frozen,fruit,berries'
        },
        'dates': {
            'filename': 'dates.jpg',
            'url': 'https://source.unsplash.com/1200x800/?dates,fruit'
        },
        'spices': {
            'filename': 'spices.jpg',
            'url': 'https://source.unsplash.com/1200x800/?spices'
        },
        'dried-herbs': {
            'filename': 'dried-herbs.jpg',
            'url': 'https://source.unsplash.com/1200x800/?dried,herbs'
        },
        'herbs-herbal-plants': {
            'filename': 'herbs-herbal-plants.jpg',
            'url': 'https://source.unsplash.com/1200x800/?herbs,plants'
        },
        'oil-seeds': {
            'filename': 'oil-seeds.jpg',
            'url': 'https://source.unsplash.com/1200x800/?seeds'
        },
    }

    # Determine upload base paths (instance and project uploads)
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    instance_upload_categories = os.path.join(current_app.instance_path, upload_folder, 'categories')
    project_upload_categories = os.path.join('uploads', 'categories')

    os.makedirs(instance_upload_categories, exist_ok=True)
    os.makedirs(project_upload_categories, exist_ok=True)

    changed = False

    for key, info in image_plan.items():
        filename = info['filename']
        url = info['url']
        instance_dst = os.path.join(instance_upload_categories, filename)
        project_dst = os.path.join(project_upload_categories, filename)

        # Download once if not present in either location
        need_download = not (os.path.exists(instance_dst) or os.path.exists(project_dst))
        if need_download:
            try:
                print(f"Downloading category image for {key}...")
                # Download to project uploads first
                urllib.request.urlretrieve(url, project_dst)
                # Copy to instance uploads
                with open(project_dst, 'rb') as src, open(instance_dst, 'wb') as dst:
                    dst.write(src.read())
                print(f"✅ Downloaded image for {key}: {filename}")
            except Exception as e:
                print(f"⚠️ Failed to download image for {key}: {e}")
                continue

        # Update DB image_path if needed
        cat = Category.query.filter_by(key=key).first()
        if cat:
            if cat.image_path != filename:
                cat.image_path = filename
                db.session.add(cat)
                changed = True

    if changed:
        try:
            db.session.commit()
            print("✅ Category images updated in database.")
        except Exception as e:
            print(f"⚠️ Failed to commit category image updates: {e}")
            db.session.rollback()
    else:
        print("✅ Category images already up-to-date.")



def ensure_link_owner_category_images(db):
    """Link owner-provided images in instance/uploads/categories to categories.
    Idempotent and safe to run every deploy. Will not overwrite an existing
    image_path if the file exists.
    """
    import os
    from flask import current_app
    from app.models import Category

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    cats_dir = os.path.join(current_app.instance_path, upload_folder, 'categories')
    os.makedirs(cats_dir, exist_ok=True)

    # Fallback static dir (tracked in repo) used to populate instance on deploy
    # Support both top-level './static' and Flask's 'app/static' layouts
    app_static_cats = os.path.join(current_app.static_folder, 'uploads', 'categories')
    root_static_cats = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'categories')
    # Prefer the directory that actually contains files; fallback to existing dir
    def _pick_static_dir(primary, secondary):
        p_files = []
        s_files = []
        if os.path.isdir(primary):
            try:
                p_files = [f for f in os.listdir(primary) if os.path.isfile(os.path.join(primary, f))]
            except Exception:
                p_files = []
        if os.path.isdir(secondary):
            try:
                s_files = [f for f in os.listdir(secondary) if os.path.isfile(os.path.join(secondary, f))]
            except Exception:
                s_files = []
        if p_files:
            return primary
        if s_files:
            return secondary
        return primary if os.path.isdir(primary) else secondary
    static_cats_dir = _pick_static_dir(app_static_cats, root_static_cats)
    os.makedirs(static_cats_dir, exist_ok=True)

    import shutil

    exts = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP']
    changed = False

    try:
        files_instance = [f for f in os.listdir(cats_dir) if os.path.isfile(os.path.join(cats_dir, f))]
    except Exception:
        files_instance = []

    try:
        files_static = [f for f in os.listdir(static_cats_dir) if os.path.isfile(os.path.join(static_cats_dir, f))]
    except Exception:
        files_static = []

    def _case_insensitive_lookup(name, pool):
        name_l = name.lower()
        for real in pool:
            if real.lower() == name_l:
                return real
        return None

    def find_candidate(key: str):
        key_lower = key.lower()
        # Prefer exact "<key>-emdad-global" filename with allowed extensions
        for ext in exts:
            fname = f"{key}-emdad-global{ext}"
            # 1) Check instance dir
            real = _case_insensitive_lookup(fname, files_instance)
            if real:
                return real
            # 2) Check static dir; if found, copy to instance
            real_static = _case_insensitive_lookup(fname, files_static)
            if real_static:
                src = os.path.join(static_cats_dir, real_static)
                dst = os.path.join(cats_dir, real_static)
                try:
                    shutil.copy2(src, dst)
                    files_instance.append(real_static)
                    return real_static
                except Exception as e:
                    print(f"⚠️ Could not copy {real_static} from static to instance: {e}")
        # Next, any file starting with "<key>-"
        # 1) Instance
        for f in files_instance:
            fl = f.lower()
            if any(fl.endswith(ext.lower()) for ext in exts) and fl.startswith(f"{key_lower}-"):
                return f
        # 2) Static → copy to instance then return


    # Link candidates to categories
    changed = False
    for cat in Category.query.all():
        key = getattr(cat, 'key', None) or getattr(cat, 'slug', None)
        if not key:
            continue
        candidate = find_candidate(key)
        if candidate and candidate != cat.image_path:
            cat.image_path = candidate
            db.session.add(cat)
            changed = True

    if changed:
        try:
            db.session.commit()
            print("✅ Linked owner-provided category images.")
        except Exception as e:
            print(f"⚠️ Failed to link category images: {e}")
            db.session.rollback()
    else:
        print("✅ Category images already linked or no changes needed.")


def ensure_link_owner_news_images(db):
    """Link owner-provided images in instance/uploads/news to News.cover_image.
    Idempotent and safe to run every deploy. Will not overwrite an existing
    cover_image if the file exists. Falls back to static/uploads/news for
    production first-run population, similar to categories/products.
    Proposed naming: <slug>-emdad-global.webp (preferred) or any <slug>-*.ext
    where ext is one of .webp/.jpg/.jpeg/.png/.svg
    """
    import os
    import shutil
    from flask import current_app
    from app.models import News

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    news_dir = os.path.join(current_app.instance_path, upload_folder, 'news')
    os.makedirs(news_dir, exist_ok=True)

    # Fallback static dir (tracked in repo) to populate instance on deploy
    # Support both top-level './static' and Flask's 'app/static' layouts
    app_static_news = os.path.join(current_app.static_folder, 'uploads', 'news')
    root_static_news = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'news')
    static_news_dir = app_static_news if os.path.isdir(app_static_news) else root_static_news
    os.makedirs(static_news_dir, exist_ok=True)

    exts = ['.webp', '.jpg', '.jpeg', '.png', '.svg', '.WEBP', '.JPG', '.JPEG', '.PNG', '.SVG']

    try:
        files_instance = [f for f in os.listdir(news_dir) if os.path.isfile(os.path.join(news_dir, f))]
    except Exception:
        files_instance = []

    try:
        files_static = [f for f in os.listdir(static_news_dir) if os.path.isfile(os.path.join(static_news_dir, f))]
    except Exception:
        files_static = []

    def _case_insensitive_lookup(name, pool):
        name_l = name.lower()
        for real in pool:
            if real.lower() == name_l:
                return real
        return None

    def find_candidate(slug: str):
        slug_lower = slug.lower()
        # Prefer exact "<slug>-emdad-global" filename with allowed extensions
        for ext in exts:
            fname = f"{slug_lower}-emdad-global{ext}"
            # 1) Check instance dir
            real = _case_insensitive_lookup(fname, files_instance)
            if real:
                return real
            # 2) Check static dir; if found, copy to instance
            real_static = _case_insensitive_lookup(fname, files_static)
            if real_static:
                src = os.path.join(static_news_dir, real_static)
                dst = os.path.join(news_dir, real_static)
                try:
                    shutil.copy2(src, dst)
                    files_instance.append(real_static)
                    return real_static
                except Exception as e:
                    print(f"⚠️ Could not copy {real_static} from static to instance: {e}")
        # Next, any file starting with "<slug>-"
        # Then, exact "<slug><ext>" match
        for ext in exts:
            fname = f"{slug_lower}{ext}"
            real = _case_insensitive_lookup(fname, files_instance)
            if real:
                return real
            real_static = _case_insensitive_lookup(fname, files_static)
            if real_static:
                src = os.path.join(static_news_dir, real_static)
                dst = os.path.join(news_dir, real_static)
                try:
                    shutil.copy2(src, dst)
                    files_instance.append(real_static)
                    return real_static
                except Exception as e:
                    print(f"⚠️ Could not copy {real_static} from static to instance: {e}")

        # 1) Instance
        for f in files_instance:
            fl = f.lower()
            if any(fl.endswith(ext.lower()) for ext in exts) and fl.startswith(f"{slug_lower}-"):
                return f
        # 2) Static → copy to instance then return
        for f in files_static:
            fl = f.lower()
            if any(fl.endswith(ext.lower()) for ext in exts) and fl.startswith(f"{slug_lower}-"):
                src = os.path.join(static_news_dir, f)
                dst = os.path.join(news_dir, f)
                try:
                    shutil.copy2(src, dst)
                    files_instance.append(f)
                    return f
                except Exception as e:
                    print(f"⚠️ Could not copy {f} from static to instance: {e}")
        return None

    changed = False

    for n in News.query.all():
        # Prefer an owner-provided candidate based on slug pattern, even if a previous image exists
        candidate = find_candidate(n.slug)
        if candidate and candidate != n.cover_image:
            n.cover_image = candidate
            db.session.add(n)
            changed = True
        else:
            # If no candidate was found, keep existing only if the file still exists; otherwise clear it
            if n.cover_image:
                existing_path = os.path.join(news_dir, n.cover_image)
                if not os.path.isfile(existing_path):
                    n.cover_image = None
                    db.session.add(n)
                    changed = True

    if changed:
        try:
            db.session.commit()
            print("✅ Linked owner-provided news images to articles.")
        except Exception as e:
            print(f"⚠️ Failed to commit news image links: {e}")
            db.session.rollback()
    else:
        print("✅ News images already linked or using existing fallbacks.")


def create_categories(db):
    """Deprecated: replaced by reset_and_seed_categories (no-op)"""
    return



def purge_category_images(db):
    """Remove all category images and clear image_path for all categories.
    Safe to run on any environment. This will not remove product/news images.
    """
    import os, shutil
    from flask import current_app
    from app.models import Category

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    dirs = [
        os.path.join('uploads', 'categories'),
        os.path.join(current_app.instance_path, upload_folder, 'categories'),
    ]

    for d in dirs:
        try:
            if os.path.isdir(d):
                for fname in os.listdir(d):
                    path = os.path.join(d, fname)
                    if os.path.isfile(path):
                        os.remove(path)
                print(f"✅ Cleared category images in: {d}")
        except Exception as e:
            print(f"⚠️ Could not clear {d}: {e}")

    # Clear image_path in DB
    changed = False
    for cat in Category.query.all():
        if cat.image_path:
            cat.image_path = None
            db.session.add(cat)
            changed = True
    if changed:
        try:
            db.session.commit()
            print("✅ Cleared image_path for all categories in DB.")
        except Exception as e:
            print(f"⚠️ Failed DB commit while clearing image_path: {e}")
            db.session.rollback()
    else:
        print("✅ No category image_path to clear in DB.")


def create_services(db):
    """Create default services (bilingual, production-ready)"""
    from app.models import Service

    if Service.query.count() == 0:
        print("Creating default services...")
        services_data = [
            {
                'title_en': 'FOB & CIF Shipping',
                'title_ar': 'شحن FOB و CIF',
                'description_en': 'Flexible shipping terms with FOB and CIF options to suit your budget and logistics preferences.',
                'description_ar': 'شروط شحن مرنة بخياري FOB و CIF لتناسب ميزانيتك وتفضيلاتك اللوجستية.',
                'icon': 'fas fa-ship',
                'sort_order': 1,
                'is_active': True
            },
            {
                'title_en': 'Cold Chain Logistics',
                'title_ar': 'سلسلة تبريد',
                'description_en': 'Temperature-controlled storage and transport to keep your products fresh throughout the journey.',
                'description_ar': 'تخزين ونقل بدرجة حرارة مضبوطة للحفاظ على نضارة منتجاتك طوال الرحلة.',
                'icon': 'fas fa-thermometer-half',
                'sort_order': 2,
                'is_active': True
            },
            {
                'title_en': 'Custom Packaging',
                'title_ar': 'تعبئة مخصصة',
                'description_en': 'Private labeling and tailored packaging formats to meet your market requirements.',
                'description_ar': 'علامة خاصة وتعبئة مخصصة لتلبية متطلبات أسواقك.',
                'icon': 'fas fa-box',
                'sort_order': 3,
                'is_active': True
            },
            {
                'title_en': 'Documentation & Compliance',
                'title_ar': 'مستندات وامتثال',
                'description_en': 'Full documentation support including certificates and regulatory compliance.',
                'description_ar': 'دعم كامل للمستندات بما في ذلك الشهادات والامتثال للجهات الرقابية.',
                'icon': 'fas fa-file-alt',
                'sort_order': 4,
                'is_active': True
            }
        ]

        for s in services_data:
            service = Service(
                title_en=s['title_en'],
                title_ar=s['title_ar'],
                description_en=s['description_en'],
                description_ar=s['description_ar'],
                icon=s['icon'],
                sort_order=s['sort_order'],
                is_active=s['is_active']
            )
            db.session.add(service)

        print("✅ Default services created successfully!")
    else:
        print("✅ Services already exist")

def create_news(db):
    """Create sample news articles (slugs aligned with production assets)"""
    from app.models import News
    from datetime import datetime, timedelta

    if News.query.count() == 0:
        print("Creating news articles...")

        news_data = [
            {
                'title_en': 'Emdad Global Expands to New Markets in 2025',
                'title_ar': 'إمداد جلوبال تتوسع في أسواق جديدة في 2025',
                'slug': 'emdad-global-expands-new-markets-2024',
                'excerpt_en': 'We are excited to announce our expansion into European and Asian markets, bringing Egyptian agricultural excellence to new customers worldwide.',
                'excerpt_ar': 'نحن متحمسون للإعلان عن توسعنا في الأسواق الأوروبية والآسيوية، مما يجلب التميز الزراعي المصري لعملاء جدد في جميع أنحاء العالم.',
                'content_en': '''<p>Emdad Global is proud to announce a significant milestone in our journey of agricultural excellence. In 2025, we are expanding our operations to serve new markets across Europe and Asia, bringing the finest Egyptian agricultural products to customers worldwide.</p>

<p>This expansion represents years of careful planning and investment in our infrastructure, quality systems, and international partnerships. Our commitment to delivering premium Egyptian citrus fruits, fresh produce, and frozen products has earned us recognition in global markets.</p>

<h3>New Market Opportunities</h3>
<p>Our expansion includes:</p>
<ul>
<li>Direct partnerships with major European distributors</li>
<li>New supply chains to Asian markets</li>
<li>Enhanced cold chain logistics for global reach</li>
<li>Increased production capacity to meet growing demand</li>
</ul>

<p>We remain committed to our core values of quality, sustainability, and customer satisfaction as we grow our international presence.</p>''',
                'content_ar': '''<p>تفخر إمداد جلوبال بالإعلان عن معلم مهم في رحلتنا للتميز الزراعي. في عام 2025، نقوم بتوسيع عملياتنا لخدمة أسواق جديدة عبر أوروبا وآسيا، مما يجلب أفضل المنتجات الزراعية المصرية للعملاء في جميع أنحاء العالم.</p>

<p>يمثل هذا التوسع سنوات من التخطيط الدقيق والاستثمار في البنية التحتية وأنظمة الجودة والشراكات الدولية. التزامنا بتقديم ثمار الحمضيات المصرية الممتازة والمنتجات الطازجة والمجمدة قد كسبنا الاعتراف في الأسواق العالمية.</p>

<h3>فرص السوق الجديدة</h3>
<p>يشمل توسعنا:</p>
<ul>
<li>شراكات مباشرة مع الموزعين الأوروبيين الرئيسيين</li>
<li>سلاسل توريد جديدة للأسواق الآسيوية</li>
<li>لوجستيات سلسلة التبريد المحسنة للوصول العالمي</li>
<li>زيادة الطاقة الإنتاجية لتلبية الطلب المتزايد</li>
</ul>

<p>نبقى ملتزمين بقيمنا الأساسية للجودة والاستدامة ورضا العملاء بينما ننمو حضورنا الدولي.</p>''',
                'status': 'published',
                'featured': True,
                'publish_at': datetime.utcnow() - timedelta(days=5),
                'tags': 'expansion,markets,international,growth'
            },
            {
                'title_en': 'Sustainable Farming Practices at Emdad Global',
                'title_ar': 'ممارسات الزراعة المستدامة في إمداد جلوبال',
                'slug': 'sustainable-farming-practices-emdad-global',
                'excerpt_en': 'Learn about our commitment to sustainable agriculture and environmental conservation while maintaining the highest quality standards.',
                'excerpt_ar': 'تعرف على التزامنا بالزراعة المستدامة والحفاظ على البيئة مع الحفاظ على أعلى معايير الجودة.',
                'content_en': '''<p>At Emdad Global, sustainability is not just a buzzword – it's a fundamental principle that guides every aspect of our agricultural operations. We believe that protecting our environment is essential for ensuring the long-term viability of Egyptian agriculture.</p>

<h3>Our Sustainable Practices</h3>
<p>We have implemented comprehensive sustainable farming practices across all our operations:</p>

<h4>Water Conservation</h4>
<ul>
<li>Advanced drip irrigation systems reducing water usage by 40%</li>
<li>Rainwater harvesting and recycling programs</li>
<li>Soil moisture monitoring for optimal irrigation timing</li>
</ul>

<h4>Soil Health Management</h4>
<ul>
<li>Organic composting programs</li>
<li>Crop rotation to maintain soil fertility</li>
<li>Minimal tillage practices to preserve soil structure</li>
</ul>

<h4>Integrated Pest Management</h4>
<ul>
<li>Biological pest control methods</li>
<li>Reduced chemical pesticide usage</li>
<li>Natural predator conservation programs</li>
</ul>

<p>These practices not only protect our environment but also result in healthier, more nutritious products for our customers worldwide.</p>''',
                'content_ar': '''<p>في إمداد جلوبال، الاستدامة ليست مجرد كلمة رنانة - إنها مبدأ أساسي يوجه كل جانب من جوانب عملياتنا الزراعية. نؤمن أن حماية بيئتنا أمر ضروري لضمان الجدوى طويلة المدى للزراعة المصرية.</p>

<h3>ممارساتنا المستدامة</h3>
<p>لقد نفذنا ممارسات زراعية مستدامة شاملة عبر جميع عملياتنا:</p>

<h4>الحفاظ على المياه</h4>
<ul>
<li>أنظمة الري بالتنقيط المتقدمة تقلل استخدام المياه بنسبة 40%</li>
<li>برامج حصاد مياه الأمطار وإعادة التدوير</li>
<li>مراقبة رطوبة التربة للتوقيت الأمثل للري</li>
</ul>

<h4>إدارة صحة التربة</h4>
<ul>
<li>برامج التسميد العضوي</li>
<li>دوران المحاصيل للحفاظ على خصوبة التربة</li>
<li>ممارسات الحراثة الدنيا للحفاظ على بنية التربة</li>
</ul>

<h4>الإدارة المتكاملة للآفات</h4>
<ul>
<li>طرق المكافحة البيولوجية للآفات</li>
<li>تقليل استخدام المبيدات الكيميائية</li>
<li>برامج الحفاظ على الحيوانات المفترسة الطبيعية</li>
</ul>

<p>هذه الممارسات لا تحمي بيئتنا فحسب، بل تؤدي أيضًا إلى منتجات أكثر صحة وتغذية لعملائنا في جميع أنحاء العالم.</p>''',
                'status': 'published',
                'featured': True,
                'publish_at': datetime.utcnow() - timedelta(days=12),
                'tags': 'sustainability,environment,farming,organic'
            },
            {
                'title_en': 'New Export Markets Expansion',
                'title_ar': 'توسع أسواق التصدير الجديدة',
                'slug': 'new-export-markets-expansion',
                'excerpt_en': 'Emdad Global announces successful entry into new international markets, strengthening our global presence in agricultural exports.',
                'excerpt_ar': 'إمداد جلوبال تعلن عن دخول ناجح في أسواق دولية جديدة، مما يعزز حضورنا العالمي في الصادرات الزراعية.',
                'content_en': '''<p>We are thrilled to announce that Emdad Global has successfully entered several new international markets, marking a significant milestone in our global expansion strategy. This achievement reflects our commitment to bringing Egyptian agricultural excellence to customers worldwide.</p>

<h3>Market Expansion Highlights</h3>
<p>Our recent expansion includes:</p>
<ul>
<li>Entry into Scandinavian markets with premium citrus fruits</li>
<li>New partnerships in Southeast Asian countries</li>
<li>Expanded presence in Middle Eastern markets</li>
<li>Growing demand for our frozen fruit products in European markets</li>
</ul>

<h3>Quality Assurance</h3>
<p>Our success in these new markets is built on our unwavering commitment to quality:</p>
<ul>
<li>International certifications including ISO 22000 and HACCP</li>
<li>Advanced cold chain logistics ensuring product freshness</li>
<li>Rigorous quality control at every stage of production</li>
<li>Compliance with international food safety standards</li>
</ul>

<p>We look forward to serving our new customers with the same dedication to quality and service that has made us a trusted partner in agricultural exports.</p>''',
                'content_ar': '''<p>نحن متحمسون للإعلان أن إمداد جلوبال قد دخلت بنجاح عدة أسواق دولية جديدة، مما يمثل معلمًا مهمًا في استراتيجية التوسع العالمي. هذا الإنجاز يعكس التزامنا بجلب التميز الزراعي المصري للعملاء في جميع أنحاء العالم.</p>

<h3>أبرز نقاط توسع السوق</h3>
<p>يشمل توسعنا الأخير:</p>
<ul>
<li>الدخول في الأسواق الاسكندنافية بثمار الحمضيات الممتازة</li>
<li>شراكات جديدة في دول جنوب شرق آسيا</li>
<li>حضور موسع في أسواق الشرق الأوسط</li>
<li>طلب متزايد على منتجات الفواكه المجمدة في الأسواق الأوروبية</li>
</ul>

<h3>ضمان الجودة</h3>
<p>نجاحنا في هذه الأسواق الجديدة مبني على التزامنا الثابت بالجودة:</p>
<ul>
<li>الشهادات الدولية بما في ذلك ISO 22000 و HACCP</li>
<li>لوجستيات سلسلة التبريد المتقدمة لضمان نضارة المنتج</li>
<li>مراقبة الجودة الصارمة في كل مرحلة من مراحل الإنتاج</li>
<li>الامتثال لمعايير سلامة الغذاء الدولية</li>
</ul>

<p>نتطلع إلى خدمة عملائنا الجدد بنفس التفاني في الجودة والخدمة التي جعلتنا شريكًا موثوقًا في الصادرات الزراعية.</p>''',
                'status': 'published',
                'featured': False,
                'publish_at': datetime.utcnow() - timedelta(days=20),
                'tags': 'export,markets,international,expansion'
            }
        ]

        # Map news to sample images
        news_images = {
            'emdad-global-expands-new-markets-2025': 'expansion.svg',
            'sustainable-farming-practices-emdad-global': 'sustainability.svg',
            'new-export-markets-expansion': 'export-markets.svg'
        }

        for news_item in news_data:
            # Set sample image
            cover_image = news_images.get(news_item['slug'], 'expansion.svg')

            news = News(
                title_en=news_item['title_en'],
                title_ar=news_item['title_ar'],
                slug=news_item['slug'],
                excerpt_en=news_item['excerpt_en'],
                excerpt_ar=news_item['excerpt_ar'],
                content_en=news_item['content_en'],
                content_ar=news_item['content_ar'],
                status=news_item['status'],
                featured=news_item['featured'],
                publish_at=news_item['publish_at'],
                tags=news_item['tags'],
                cover_image=cover_image
            )
            db.session.add(news)

        print("✅ News articles created successfully!")
    else:
        print("✅ News articles already exist")

def create_company_info(db):
    """Create company information sections"""
    from app.models import CompanyInfo

    if CompanyInfo.query.count() == 0:
        print("Creating company information...")

        company_info_data = [
            {
                'key': 'about_intro',
                'title_en': 'About Emdad Global',
                'title_ar': 'عن إمداد جلوبال',
                'content_en': 'Emdad Global is a leading Egyptian export company specializing in premium agricultural products. With over 25 years of experience, we have built a reputation for delivering the highest quality fresh and frozen fruits and vegetables to markets worldwide. Our commitment to excellence, combined with state-of-the-art facilities and international certifications, ensures that our products meet the strictest quality standards demanded by global markets.',
                'content_ar': 'إمداد جلوبال هي شركة تصدير مصرية رائدة متخصصة في المنتجات الزراعية الممتازة. مع أكثر من 25 عاماً من الخبرة، بنينا سمعة في تقديم أعلى جودة من الفواكه والخضروات الطازجة والمجمدة إلى الأسواق في جميع أنحاء العالم. التزامنا بالتميز، إلى جانب المرافق الحديثة والشهادات الدولية، يضمن أن منتجاتنا تلبي أصرم معايير الجودة التي تتطلبها الأسواق العالمية.',
                'sort_order': 1,
                'is_active': True
            },
            {

                'key': 'why_choose_us',
                'title_en': 'Why Choose Emdad Global?',
                'title_ar': 'لماذا تختار إمداد جلوبال؟',
                'content_en': 'Our success is built on three pillars: uncompromising quality, reliable supply chains, and exceptional customer service. We work directly with carefully selected farms across Egypt, ensuring traceability and quality control from farm to fork. Our modern facilities, international certifications, and experienced team guarantee that every shipment meets the highest standards of freshness, safety, and quality.',
                'content_ar': 'نجاحنا مبني على ثلاث ركائز: الجودة بلا تنازل، وسلاسل التوريد الموثوقة، وخدمة العملاء الاستثنائية. نعمل مباشرة مع المزارع المختارة بعناية في جميع أنحاء مصر، مما يضمن إمكانية التتبع ومراقبة الجودة من المزرعة إلى المائدة. مرافقنا الحديثة والشهادات الدولية والفريق ذو الخبرة يضمن أن كل شحنة تلبي أعلى معايير النضارة والسلامة والجودة.',
                'sort_order': 2,
                'is_active': True
            }
        ]

        for info_data in company_info_data:
            company_info = CompanyInfo(
                key=info_data['key'],
                title_en=info_data['title_en'],
                title_ar=info_data['title_ar'],
                content_en=info_data['content_en'],
                content_ar=info_data['content_ar'],
                sort_order=info_data['sort_order'],
                is_active=info_data['is_active']
            )
            db.session.add(company_info)

        print("✅ Company information created successfully!")
    else:
        print("✅ Company information already exists")

def ensure_link_owner_product_images(db):
    """Link/copy owner-provided product images (webp preferred) from static to instance and
    set product.image_path and main ProductImage accordingly. Safe to run each deploy.
    """
    import os, shutil
    from flask import current_app
    from app.models import Product, ProductImage

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    inst_dir = os.path.join(current_app.instance_path, upload_folder, 'products')
    os.makedirs(inst_dir, exist_ok=True)

    # Fallback static dir (tracked in repo) used to populate instance on deploy
    # Support both top-level './static' and Flask's 'app/static' layouts
    app_static_products = os.path.join(current_app.static_folder, 'uploads', 'products')
    root_static_products = os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'products')
    # Prefer static dir that actually contains files
    def _pick_static_dir(primary, secondary):
        p_files = []
        s_files = []
        if os.path.isdir(primary):
            try:
                p_files = [f for f in os.listdir(primary) if os.path.isfile(os.path.join(primary, f))]
            except Exception:
                p_files = []
        if os.path.isdir(secondary):
            try:
                s_files = [f for f in os.listdir(secondary) if os.path.isfile(os.path.join(secondary, f))]
            except Exception:
                s_files = []
        if p_files:
            return primary
        if s_files:
            return secondary
        return primary if os.path.isdir(primary) else secondary
    static_dir = _pick_static_dir(app_static_products, root_static_products)
    os.makedirs(static_dir, exist_ok=True)

    def _find_real_case(name: str, pool: list[str]) -> str | None:
        name_l = name.lower()
        for real in pool:
            if real.lower() == name_l:
                return real
        return None

    try:
        files_instance = [f for f in os.listdir(inst_dir) if os.path.isfile(os.path.join(inst_dir, f))]
    except Exception:
        files_instance = []
    try:
        files_static = [f for f in os.listdir(static_dir) if os.path.isfile(os.path.join(static_dir, f))]
    except Exception:
        files_static = []

    changed = False

    for p in Product.query.all():
        # Expected preferred filename: <slug>-emdad-global.webp
        preferred = f"{p.slug}-emdad-global.webp"

        def ensure_present(fname: str) -> str | None:
            # Return real filename present in instance; copy from static if needed
            real = _find_real_case(fname, files_instance)
            if real:
                return real
            real_static = _find_real_case(fname, files_static)
            if real_static:
                src = os.path.join(static_dir, real_static)
                dst = os.path.join(inst_dir, real_static)
                try:
                    shutil.copy2(src, dst)
                    files_instance.append(real_static)
                    return real_static
                except Exception as e:
                    print(f"⚠️ Could not copy {real_static} from static to instance: {e}")
            return None

        real_name = ensure_present(preferred)

        if real_name:
            # Update product.image_path and main ProductImage
            if p.image_path != real_name:
                p.image_path = real_name
                db.session.add(p)
                changed = True

            main = p.images.filter_by(is_main=True).first()
            if main and main.filename != real_name:
                main.filename = real_name
                db.session.add(main)
                changed = True
            elif not main:
                # Create main image record
                main = ProductImage(product_id=p.id, filename=real_name, alt_text_en=p.name_en, alt_text_ar=p.name_ar, is_main=True, sort_order=0)
                db.session.add(main)
                changed = True
        else:
            # If preferred not found, do not clear existing to avoid regressions
            pass

    if changed:
        try:
            db.session.commit()
            print("✅ Linked owner-provided product images.")
        except Exception as e:
            print(f"⚠️ Failed to link product images: {e}")
            db.session.rollback()
    else:
        print("✅ Product images already linked or no changes needed.")




def enforce_strict_product_webp(db):
    """Strictly enforce presence of webp images for all products in production.
    For each product, require <slug>-emdad-global.webp to exist in instance/uploads/products
    or at least any slug-*.webp to exist under one of known static roots (then copy).
    If any are missing, raise RuntimeError to abort startup.
    """
    import os, shutil
    from flask import current_app
    from app.models import Product

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    inst_dir = os.path.join(current_app.instance_path, upload_folder, 'products')
    os.makedirs(inst_dir, exist_ok=True)

    # Candidate static roots to search (robust across layouts)
    candidates = []
    try:
        candidates.append(os.path.join(current_app.static_folder, 'uploads', 'products'))
    except Exception:
        pass
    try:
        candidates.append(os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'products'))
    except Exception:
        pass
    # Also search CWD/static in case of atypical environments
    candidates.append(os.path.join(os.getcwd(), 'static', 'uploads', 'products'))
    # De-duplicate while preserving order
    seen = set()
    static_roots = []
    for c in candidates:
        if c and c not in seen and os.path.isdir(c):
            static_roots.append(c)
            seen.add(c)

    def _find_in_statics(expected_lower: str, slug_lower: str):
        # Try exact match (case-insensitive) across all roots
        for root in static_roots:
            try:
                for f in os.listdir(root):
                    fl = f.lower()
                    if fl == expected_lower:
                        return os.path.join(root, f)
            except Exception:
                continue
        # Try any slug-*.webp
        for root in static_roots:
            try:
                for f in os.listdir(root):
                    fl = f.lower()
                    if fl.endswith('.webp') and fl.startswith(f"{slug_lower}-"):
                        return os.path.join(root, f)
            except Exception:
                continue
        return None

    missing = []

    for p in Product.query.all():
        expected = f"{p.slug}-emdad-global.webp"
        expected_lower = expected.lower()
        inst_path = os.path.join(inst_dir, expected)
        if os.path.isfile(inst_path):
            continue

        src = _find_in_statics(expected_lower, p.slug.lower())
        if src and os.path.isfile(src):
            # Copy to instance with original basename from src
            try:
                basename = os.path.basename(src)
                dst = os.path.join(inst_dir, basename)
                if not os.path.isfile(dst):
                    shutil.copy2(src, dst)
                continue
            except Exception:
                pass

        missing.append(f"{p.slug}:{expected}")

    if missing:
        msg = "Strict assets check failed for products (missing webp):\n" + "\n".join(missing)
        raise RuntimeError(msg)


def copy_sample_images():
    """Copy sample images to upload directories"""
    import shutil
    import os


def seed_official_products(db):
    """Upsert official products from seeds/products.json and link images.
    - Uses slug as unique key
    - Assigns category by category_key
    - Sets Product.image_path and ensures main ProductImage
    - Accepts .webp/.svg tracked in static/uploads/products
    - Enhanced with better error handling and image verification
    """
    import json, os, shutil
    from flask import current_app
    from app.models import Product, ProductImage, Category

    seeds_path = os.path.join(os.path.dirname(__file__), 'seeds', 'products.json')
    if not os.path.isfile(seeds_path):
        print(f"⚠️ seeds file not found: {seeds_path}")
        return

    with open(seeds_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    items = payload.get('products') or []

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    inst_dir = os.path.join(current_app.instance_path, upload_folder, 'products')
    os.makedirs(inst_dir, exist_ok=True)

    # Support multiple static directory layouts for robustness
    static_candidates = []
    try:
        static_candidates.append(os.path.join(current_app.static_folder, 'uploads', 'products'))
    except Exception:
        pass
    try:
        static_candidates.append(os.path.join(os.path.dirname(current_app.root_path), 'static', 'uploads', 'products'))
    except Exception:
        pass
    # Also check current working directory
    static_candidates.append(os.path.join(os.getcwd(), 'static', 'uploads', 'products'))

    def _pick_static_dir(candidates):
        for candidate in candidates:
            if os.path.isdir(candidate):
                try:
                    files = [f for f in os.listdir(candidate) if os.path.isfile(os.path.join(candidate, f)) and f.endswith('.webp')]
                    if files:
                        print(f"✅ Using static directory: {candidate} (found {len(files)} webp files)")
                        return candidate
                except Exception:
                    continue
        # Fallback to first existing directory
        for candidate in candidates:
            if os.path.isdir(candidate):
                print(f"⚠️ Using fallback static directory: {candidate}")
                return candidate
        # Create first candidate if none exist
        if candidates:
            os.makedirs(candidates[0], exist_ok=True)
            print(f"📁 Created static directory: {candidates[0]}")
            return candidates[0]
        return None

    static_dir = _pick_static_dir(static_candidates)
    if not static_dir:
        print("❌ Could not determine static directory for products")
        return

    successful_products = 0
    failed_products = 0
    copied_images = 0
    missing_images = []

    for item in items:
        slug = item['slug']
        cat = Category.query.filter_by(key=item['category_key']).first()
        if not cat:
            print(f"⚠️ Category not found for product {slug}: {item['category_key']}")
            failed_products += 1
            continue

        p = Product.query.filter_by(slug=slug).first()
        if not p:
            p = Product(slug=slug, category_id=cat.id)
        p.name_en = item['name_en']
        p.name_ar = item['name_ar']
        p.description_en = item.get('desc_en')
        p.description_ar = item.get('desc_ar')
        p.short_description_en = item.get('short_en')
        p.short_description_ar = item.get('short_ar')
        p.status = 'active'
        p.featured = bool(item.get('featured', True))
        p.show_on_homepage = bool(item.get('show_on_homepage', True))
        p.sort_order = int(item.get('sort_order', 1))
        p.category_id = cat.id

        # Enhanced image handling
        fname = item.get('image_filename')
        image_copied = False
        if fname:
            src = os.path.join(static_dir, fname)
            dst = os.path.join(inst_dir, fname)

            # Check if source exists
            if os.path.isfile(src):
                # Copy to instance if not exists or if source is newer
                if not os.path.isfile(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                    try:
                        shutil.copy2(src, dst)
                        print(f"✅ Copied product image: {fname}")
                        copied_images += 1
                        image_copied = True
                    except Exception as e:
                        print(f"⚠️ Failed to copy {fname}: {e}")
                else:
                    image_copied = True

                # Verify the image exists in destination
                if os.path.isfile(dst):
                    p.image_path = fname
                else:
                    print(f"⚠️ Image not found in destination: {fname}")
                    missing_images.append((slug, fname))
            else:
                print(f"⚠️ Source image not found: {src}")
                missing_images.append((slug, fname))

        db.session.add(p)
        db.session.flush()

        # Ensure main ProductImage record
        main = p.images.filter_by(is_main=True).first()
        if p.image_path:
            if main and main.filename != p.image_path:
                main.filename = p.image_path
                db.session.add(main)
            elif not main:
                db.session.add(ProductImage(
                    product_id=p.id,
                    filename=p.image_path,
                    alt_text_en=p.name_en,
                    alt_text_ar=p.name_ar,
                    is_main=True,
                    sort_order=0
                ))

        successful_products += 1

    db.session.commit()

    # Print detailed summary
    print(f"\n📊 Product seeding summary:")
    print(f"✅ Successful products: {successful_products}")
    print(f"❌ Failed products: {failed_products}")
    print(f"📁 Images copied: {copied_images}")
    print(f"⚠️ Missing images: {len(missing_images)}")

    if missing_images:
        print(f"\n📋 Missing images list:")
        for slug, fname in missing_images:
            print(f"  - {slug}: {fname}")

    print("✅ Seeded/updated official products from seeds.")


    try:
        print("Copying sample images...")

        # Create upload directories
        upload_dirs = [
            'uploads/products',
            'uploads/categories',
            'uploads/news',
            'instance/uploads/products',
            'instance/uploads/categories',
            'instance/uploads/news'
        ]

        for upload_dir in upload_dirs:
            os.makedirs(upload_dir, exist_ok=True)

        # Skip copying sample category images to allow real photos provided by owner
        # (no-op for categories)

        # Copy product images (disabled for SVG to avoid overriding real webp assets)
        if os.path.exists('static/images/samples/products'):
            for filename in os.listdir('static/images/samples/products'):
                # Skip copying SVG placeholders for products in production
                if filename.lower().endswith('.svg'):
                    continue

        # Copy news images
        if os.path.exists('static/images/samples/news'):
            for filename in os.listdir('static/images/samples/news'):
                if filename.endswith('.svg'):
                    src = f'static/images/samples/news/{filename}'
                    for dest_dir in ['uploads/news', 'instance/uploads/news']:
                        dest = f'{dest_dir}/{filename}'
                        shutil.copy2(src, dest)
                        print(f"✅ Copied news image: {filename}")

        print("✅ Sample images copied successfully!")

    except Exception as e:
        print(f"⚠️ Error copying sample images: {e}")
        # Continue anyway - not critical

def init_database():
    """Initialize database for production with complete sample data"""
    try:
        import os
        import sys

        # Ensure temp directory is writable
        os.makedirs('/tmp', exist_ok=True)

        # Test write permissions and set appropriate database URL
        db_paths = [
            '/tmp/emdad_global.db',
            './emdad_global.db',
            'emdad_global.db'
        ]

        database_url = None
        for db_path in db_paths:
            try:
                # Test if we can create a file in this location
                test_path = db_path.replace('.db', '_test.db')
                with open(test_path, 'w') as f:
                    f.write('test')
                os.remove(test_path)
                database_url = f'sqlite:///{db_path}'
                print(f"✅ Using database path: {db_path}")
                break
            except Exception as e:
                print(f"⚠️ Cannot write to {db_path}: {e}")
                continue

        if database_url:
            os.environ['DATABASE_URL'] = database_url
        else:
            # Last resort - in-memory database
            os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
            print("⚠️ Using in-memory database as fallback")

        print("Creating Flask app...")
        from app import create_app
        app = create_app('production')

        print("Initializing database...")
        with app.app_context():
            from app.models import db
            # Import all models to ensure they're registered
            import app.models  # noqa: F401

            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")

            # Create all sample data
            try:
                print("Creating sample data...")

                # Create sample images first
                copy_sample_images()

                # Create admin user
                create_admin_user(db)
                db.session.commit()

                # Reset and seed official categories (one-time)
                reset_and_seed_categories(db)
                db.session.commit()

                # Link any owner-provided category images (safe, idempotent)
                ensure_link_owner_category_images(db)
                db.session.commit()

                # Always ensure at least 6 homepage categories (idempotent)
                ensure_min_homepage_categories(db, min_count=6)
                db.session.commit()

                # Seed official products from seeds/products.json (idempotent upsert)
                try:
                    print("🌱 Seeding official products...")
                    seed_official_products(db)
                    db.session.commit()

                    # Verify seeding was successful
                    from app.models import Product
                    product_count = Product.query.filter_by(status='active').count()
                    print(f"✅ Seeding completed: {product_count} active products")

                    if product_count < 28:
                        print(f"⚠️ WARNING: Expected at least 28 products, found {product_count}")
                        print("🔄 Attempting to re-seed...")
                        seed_official_products(db)
                        db.session.commit()

                        product_count = Product.query.filter_by(status='active').count()
                        print(f"🔄 After re-seeding: {product_count} active products")

                except Exception as e:
                    print(f"❌ Could not seed official products: {e}")
                    import traceback
                    traceback.print_exc()
                    # Don't fail the entire initialization for this
                    print("⚠️ Continuing with initialization despite seeding issues...")

                # Link/copy owner-provided product images (idempotent, run AFTER seeding)
                ensure_link_owner_product_images(db)
                db.session.commit()

                # Enforce strict presence of product webp assets (fail startup if missing)
                enforce_strict_product_webp(db)

                # Create default services
                create_services(db)

                # Force exactly the target three articles on homepage (idempotent)
                try:
                    def _ensure_homepage_news_exact_three(db):
                        from app.models import News
                        target_slugs = {
                            'emdad-global-expands-new-markets-2024',
                            'sustainable-farming-practices-emdad-global',
                            'new-export-markets-expansion',
                        }
                        changed = False
                        for n in News.query.all():
                            want = n.slug in target_slugs
                            if n.show_on_homepage != want:
                                n.show_on_homepage = want
                                db.session.add(n)
                                changed = True
                        if changed:
                            db.session.commit()
                            print('✅ Enforced homepage news to the exact three target slugs')
                        else:
                            print('✅ Homepage news already set to the three target slugs')
                    _ensure_homepage_news_exact_three(db)
                except Exception as e:
                    print(f"⚠️ Could not enforce homepage news selection: {e}")

                db.session.commit()

                # Create news articles
                create_news(db)
                db.session.commit()
                # Rewrite news with long-form 2025 SEO content (dev/prod safe)
                try:
                    from scripts.rewrite_news_content_2025 import apply_updates as _rewrite_news_2025
                    _rewrite_news_2025()
                    print("✅ Rewrote news articles with 2025 long-form SEO content")
                except Exception as e:
                    print(f"⚠️ Could not rewrite news content (2025 long-form): {e}")

                # Link/copy owner-provided news images (idempotent)
                try:
                    ensure_link_owner_news_images(db)
                    db.session.commit()
                except Exception as e:
                    print(f"⚠️ Could not link news images: {e}")


                # Create company information
                create_company_info(db)
                db.session.commit()

                print("✅ All sample data created successfully!")

            except Exception as data_error:
                print(f"⚠️ Sample data creation error: {data_error}")
                import traceback
                traceback.print_exc()
                # Continue anyway - basic tables are created

            print("✅ Database initialization completed!")
            return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = init_database()
    sys.exit(0 if success else 1)
