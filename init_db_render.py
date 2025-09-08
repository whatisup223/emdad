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

    exts = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP']
    changed = False

    try:
        files = [f for f in os.listdir(cats_dir) if os.path.isfile(os.path.join(cats_dir, f))]
    except Exception:
        files = []

    def find_candidate(key: str):
        key_lower = key.lower()
        # Prefer exact "<key>-emdad-global" filename with allowed extensions
        for ext in exts:
            fname = f"{key}-emdad-global{ext}"
            if fname in files:
                return fname
            # Also check case-insensitive variant just in case
            if fname.lower() in [f.lower() for f in files]:
                # Return the actual-cased filename from files list
                for real in files:
                    if real.lower() == fname.lower():
                        return real
        # Next, any file starting with "<key>-"
        for f in files:
            fl = f.lower()
            if any(fl.endswith(ext.lower()) for ext in exts) and fl.startswith(f"{key_lower}-"):
                return f
        # Finally, any file that contains the key segment
        for f in files:
            if key_lower in f.lower() and any(f.lower().endswith(ext.lower()) for ext in exts):
                return f
        return None

    for cat in Category.query.all():
        # If image_path already points to an existing file, skip
        if cat.image_path:
            cur_path = os.path.join(cats_dir, cat.image_path)
            if os.path.exists(cur_path):
                continue
        candidate = find_candidate(cat.key)
        if candidate:
            cat.image_path = candidate
            db.session.add(cat)
            changed = True
        else:
            # Clear any placeholder (e.g., seeded .svg) to avoid broken links
            if cat.image_path:
                cat.image_path = None
                db.session.add(cat)
                changed = True

    if changed:
        try:
            db.session.commit()
            print("✅ Linked owner-provided category images (and cleared missing ones).")
        except Exception as e:
            print(f"⚠️ Failed to link owner images: {e}")
            db.session.rollback()
    else:
        print("✅ Owner-provided category images already linked (or none found).")


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
    """Create sample news articles"""
    from app.models import News
    from datetime import datetime, timedelta

    if News.query.count() == 0:
        print("Creating news articles...")

        news_data = [
            {
                'title_en': 'Emdad Global Expands to New Markets in 2024',
                'title_ar': 'إمداد جلوبال تتوسع في أسواق جديدة في 2024',
                'slug': 'emdad-global-expands-new-markets-2024',
                'excerpt_en': 'We are excited to announce our expansion into European and Asian markets, bringing Egyptian agricultural excellence to new customers worldwide.',
                'excerpt_ar': 'نحن متحمسون للإعلان عن توسعنا في الأسواق الأوروبية والآسيوية، مما يجلب التميز الزراعي المصري لعملاء جدد في جميع أنحاء العالم.',
                'content_en': '''<p>Emdad Global is proud to announce a significant milestone in our journey of agricultural excellence. In 2024, we are expanding our operations to serve new markets across Europe and Asia, bringing the finest Egyptian agricultural products to customers worldwide.</p>

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
                'content_ar': '''<p>تفخر إمداد جلوبال بالإعلان عن معلم مهم في رحلتنا للتميز الزراعي. في عام 2024، نقوم بتوسيع عملياتنا لخدمة أسواق جديدة عبر أوروبا وآسيا، مما يجلب أفضل المنتجات الزراعية المصرية للعملاء في جميع أنحاء العالم.</p>

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
            'emdad-global-expands-new-markets-2024': 'expansion.svg',
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

def copy_sample_images():
    """Copy sample images to upload directories"""
    import shutil
    import os

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

        # Copy product images
        if os.path.exists('static/images/samples/products'):
            for filename in os.listdir('static/images/samples/products'):
                if filename.endswith('.svg'):
                    src = f'static/images/samples/products/{filename}'
                    for dest_dir in ['uploads/products', 'instance/uploads/products']:
                        dest = f'{dest_dir}/{filename}'
                        shutil.copy2(src, dest)
                        print(f"✅ Copied product image: {filename}")

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

                # Create default services
                create_services(db)
                db.session.commit()

                # Create news articles
                create_news(db)
                db.session.commit()

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
