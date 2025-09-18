import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    # Handle CSRF errors globally
    try:
        @csrf.error_handler
        def csrf_error(reason):
            from flask import flash, redirect, request, url_for
            flash('خطأ في الأمان: انتهت صلاحية النموذج. يرجى المحاولة مرة أخرى.', 'error')
            # Redirect back to the same page
            return redirect(request.url)
    except AttributeError:
        # Fallback for older Flask-WTF versions
        pass
    # Auto-create missing RFQ columns in non-migrated environments (safe fallback)
    # Flask 3 removed before_first_request; run once at startup inside app context
    try:
        from sqlalchemy import inspect, text
        with app.app_context():
            inspector = inspect(db.engine)
            cols = {c['name'] for c in inspector.get_columns('rfq')}
            # Add columns if missing (SQLite/Postgres compatible SQL)
            if 'delivery_date' not in cols:
                try:
                    db.session.execute(text('ALTER TABLE rfq ADD COLUMN delivery_date DATE'))
                except Exception:
                    pass
            if 'budget' not in cols:
                try:
                    db.session.execute(text('ALTER TABLE rfq ADD COLUMN budget VARCHAR(100)'))
                except Exception:
                    pass

            # Auto-add new Product columns in non-migrated environments (safe no-op if exists)
            try:
                pcols = {c['name'] for c in inspector.get_columns('product')}
                if 'applications' not in pcols:
                    db.session.execute(text('ALTER TABLE product ADD COLUMN applications TEXT'))
                if 'quality_targets' not in pcols:
                    db.session.execute(text('ALTER TABLE product ADD COLUMN quality_targets TEXT'))
                if 'commercial_docs' not in pcols:
                    db.session.execute(text('ALTER TABLE product ADD COLUMN commercial_docs TEXT'))
            except Exception:
                # Ignore if DB doesn't support runtime ALTER or column already exists
                pass

            db.session.commit()
    except Exception:
        # Ignore if inspection fails; rely on proper migrations
        pass


    # Configure Flask-Login
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Create upload directories
    upload_dir = os.path.join(app.instance_path, app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'categories'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'products'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'gallery'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'news'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'rfq'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'editor'), exist_ok=True)

    # Ensure critical DB tables exist (no manual migration needed for essential new tables)
    try:
        with app.app_context():
            from sqlalchemy import inspect
            insp = inspect(db.engine)
            from app.models import GalleryCategory
            if not insp.has_table('gallery_category'):
                # Create only the missing table to avoid touching existing schema
                GalleryCategory.__table__.create(db.engine)
            # Seed default categories if not present
            defaults = [
                ('farms','Farms','المزارع','fa-seedling'),
                ('packing','Packing Houses','بيوت التعبئة','fa-industry'),
                ('storage','Cold Storage','التخزين البارد','fa-warehouse'),
                ('exports','Exports','التصدير','fa-ship')
            ]
            created_any = False
            for key, en, ar, icon in defaults:
                if not GalleryCategory.query.filter_by(key=key).first():
                    db.session.add(GalleryCategory(key=key, name_en=en, name_ar=ar, icon_class=icon, is_active=True))
                    created_any = True
            if created_any:
                db.session.commit()
    except Exception as e:
        app.logger.warning(f"DB ensure/seed failed (gallery_category): {e}")


    # Language selector function
    def get_locale():
        from flask import request, session, g
        # 1. Check URL parameter
        if request.args.get('lang') in app.config['LANGUAGES']:
            session['language'] = request.args.get('lang')
            g.locale = request.args.get('lang')
            return request.args.get('lang')

        # 2. Check if language is set in session
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            g.locale = session.get('language')
            return session['language']

        # 3. Check Accept-Language header
        default_lang = request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']
        g.locale = default_lang
        return default_lang

    # Initialize Babel with locale selector
    try:
        babel.init_app(app, locale_selector=get_locale)
    except TypeError:
        # Fallback for older versions
        babel.init_app(app)
        babel.localeselector(get_locale)

    # Context processors
    @app.context_processor
    def inject_config():
        from flask import session, g
        from flask_babel import gettext
        import time
        # Lazy import to avoid circular imports during app initialization
        try:
            from app.models import Category, Product
        except Exception:
            Category = None
            Product = None

        current_language = session.get('language', 'en')

        # Set the locale in g for Babel
        g.locale = current_language

        # Build categories for navbar (dynamic)
        nav_categories = []
        if Category is not None:
            try:
                nav_categories = (Category.query
                                  .filter_by(is_active=True)
                                  .order_by(Category.sort_order, Category.name_en)
                                  .all()) or []
            except Exception:
                nav_categories = []

        # Build products for sidebar/mobile (dynamic)
        nav_products = []
        if Product is not None:
            try:
                nav_products = (Product.query
                                  .filter_by(status='active')
                                  .order_by(Product.sort_order, Product.name_en)
                                  .all()) or []
            except Exception:
                nav_products = []

        # Manual translation dictionary for critical texts
        manual_translations = {
            'ar': {
                'Premium Quality Since 1999': 'جودة ممتازة منذ عام 1999',
                'Premium Egyptian': 'إمداد جلوبال',
                'Agricultural': 'لتصدير المنتجات',
                'Exports': 'الزراعية المصرية',
                'Supplying the world with the finest Egyptian citrus fruits, fresh produce, and frozen products.': 'نزود العالم بأجود المنتجات الزراعية المصرية الطازجة والمجمدة.',
                'Quality assured with international certifications and reliable global logistics.': 'جودة مضمونة بشهادات دولية ولوجستيات عالمية موثوقة.',

                # News Articles
                'Expanding Global Reach': 'توسيع النطاق العالمي',
                'Emdad Global announces new partnerships in European and Asian markets, strengthening our international presence.': 'تعلن إمداد جلوبال عن شراكات جديدة في الأسواق الأوروبية والآسيوية، مما يعزز حضورنا الدولي.',

                'Quality Certification Update': 'تحديث شهادات الجودة',
                'Successfully renewed ISO 22000 and Good Agricultural Practices certifications, reinforcing our commitment to quality standards.': 'تم تجديد شهادات ISO 22000 وممارسات الزراعة الجيدة بنجاح، مما يعزز التزامنا بمعايير الجودة.',

                'Sustainable Agriculture Initiative': 'مبادرة الزراعة المستدامة',
                'Launching new sustainable farming practices to support environmental conservation and premium product quality.': 'إطلاق ممارسات زراعية مستدامة جديدة لدعم الحفاظ على البيئة وجودة المنتجات المتميزة.',

                # Navigation
                'Emdad Global': 'إمداد جلوبال',
                'Request Quote': 'طلب عرض سعر',
                'Quote': 'عرض سعر',
                'Countries Served': 'دولة نخدمها',
                'Premium Products': 'منتج ممتاز',
                'Years Experience': 'سنة خبرة',
                'Cold Chain': 'سلسلة التبريد',
                'Logistics': 'اللوجستيات',
                'Certified': 'معتمد',
                'About Us': 'من نحن',
                'Calendar': 'التقويم',

                'Get Quote': 'احصل على عرض سعر',
                'Request a Quote': 'طلب عرض سعر',
                'View Products': 'عرض المنتجات',
                'Product Categories': 'فئات المنتجات',
                'Our Premium Product Range': 'مجموعة منتجاتنا الممتازة',
                'Featured Products': 'المنتجات المميزة',
                'Premium Quality Selection': 'مجموعة مختارة عالية الجودة',
                'Why Choose Us': 'لماذا تختارنا',
                'Your Trusted Export Partner': 'شريكك الموثوق في التصدير',
                'Latest Updates': 'آخر التحديثات',
                'News & Industry Insights': 'الأخبار ورؤى الصناعة',
                'Our Introduction': 'مقدمتنا',
                'Professional Farmers': 'مزارعون محترفون',
                'Organic & Eco Solutions': 'حلول عضوية وبيئية',
                'Discover More': 'اكتشف المزيد',
                'Trusted by': 'موثوق من قبل',
                'Customers': 'العملاء',
                'Worldwide': 'حول العالم',
                'Our Achievements': 'إنجازاتنا',
                'Over two decades of excellence in Egyptian agricultural exports,': 'أكثر من عقدين من التميز في الصادرات الزراعية المصرية،',
                'serving customers across 50+ countries with unwavering quality and reliability.': 'نخدم العملاء في أكثر من 50 دولة بجودة وموثوقية لا تتزعزع.',
                'ISO 22000 Certified': 'معتمد ISO 22000',
                'Food Safety Management System': 'نظام إدارة سلامة الغذاء',
                'Cold Chain Excellence': 'تميز سلسلة التبريد',
                'Temperature-controlled logistics': 'لوجستيات مُتحكم بدرجة الحرارة',
                'Map Coverage': 'تغطية الخريطة',
                'Discover our carefully curated selection of Egyptian agricultural products,': 'اكتشف مجموعتنا المختارة بعناية من المنتجات الزراعية المصرية،',
                'each category representing the finest quality and authentic taste.': 'كل فئة تمثل أجود جودة وطعم أصيل.',
                'Explore Products': 'استكشف المنتجات',
                'Premium quality products from Egypt\'s finest agricultural regions.': 'منتجات عالية الجودة من أجود المناطق الزراعية في مصر.',
                'View All Categories': 'عرض جميع الفئات',
                'Discover our handpicked selection of the finest Egyptian agricultural products,': 'اكتشف مجموعتنا المختارة يدوياً من أجود المنتجات الزراعية المصرية،',
                'each representing the pinnacle of quality and taste.': 'كل منها يمثل قمة الجودة والطعم.',
                'Featured': 'مميز',
                'Quick View': 'عرض سريع',
                'Premium': 'ممتاز',
                'Premium quality Egyptian agricultural product with exceptional taste and nutritional value.': 'منتج زراعي مصري عالي الجودة بطعم استثنائي وقيمة غذائية عالية.',
                'Fresh': 'طازج',
                'Details': 'التفاصيل',
                'Citrus Fruits': 'الحمضيات',
                'Premium Egyptian oranges, lemons, and mandarins with exceptional sweetness and quality.': 'حمضيات مصرية ممتازة من البرتقال والليمون واليوسفي بحلاوة وجودة استثنائية.',
                'Fresh Fruits': 'الفواكه الطازجة',
                'Seasonal fresh fruits including grapes, mangoes, and pomegranates from Egyptian farms.': 'فواكه طازجة موسمية تشمل العنب والمانجو والرمان من المزارع المصرية.',
                'Fresh Vegetables': 'الخضروات الطازجة',
                'High-quality vegetables including garlic, onions, and potatoes for global markets.': 'خضروات عالية الجودة تشمل الثوم والبصل والبطاطس للأسواق العالمية.',
                'Frozen Products': 'المنتجات المجمدة',
                'IQF frozen fruits and vegetables maintaining freshness and nutritional value.': 'فواكه وخضروات مجمدة سريعاً تحافظ على النضارة والقيمة الغذائية.',
                'Explore All Products': 'استكشف جميع المنتجات',
                'Experience the difference of working with Egypt\'s premier agricultural export company,': 'اختبر الفرق في العمل مع شركة التصدير الزراعي الرائدة في مصر،',
                'where quality meets reliability and tradition meets innovation.': 'حيث تلتقي الجودة بالموثوقية والتقليد بالابتكار.',
                'Premium Quality': 'جودة ممتازة',
                'Rigorous quality control processes and international certifications ensure': 'عمليات مراقبة الجودة الصارمة والشهادات الدولية تضمن',
                'every product meets the highest global standards.': 'أن كل منتج يلبي أعلى المعايير العالمية.',
                'Reliable Logistics': 'لوجستيات موثوقة',
                'Advanced cold chain management ensures your products': 'إدارة سلسلة التبريد المتقدمة تضمن أن منتجاتك',
                'arrive fresh and on time, anywhere in the world.': 'تصل طازجة وفي الوقت المحدد، في أي مكان في العالم.',
                'Global Network': 'شبكة عالمية',
                'Global Reach': 'نطاق عالمي',
                'Serving 50+ countries worldwide with trusted partnerships': 'نخدم أكثر من 50 دولة حول العالم بشراكات موثوقة',
                'and comprehensive market knowledge.': 'ومعرفة شاملة بالسوق.',
                '50+ Countries': 'أكثر من 50 دولة',
                'Trusted Partners': 'شركاء موثوقون',
                'Trusted Partnership': 'شراكة موثوقة',
                'Over 25 years of experience building lasting relationships': 'أكثر من 25 عاماً من الخبرة في بناء علاقات دائمة',
                'with clients through integrity and excellence.': 'مع العملاء من خلال النزاهة والتميز.',
                '25+ Years Experience': 'أكثر من 25 عاماً من الخبرة',
                '500+ Clients': 'أكثر من 500 عميل',
                'Satisfied Clients': 'عميل راضي',
                'Stay informed about our latest developments, industry trends, and insights': 'ابق على اطلاع على آخر التطورات واتجاهات الصناعة والرؤى',
                'from the world of Egyptian agricultural exports.': 'من عالم الصادرات الزراعية المصرية.',
                'News': 'أخبار',
                'Stay updated with the latest news and developments from Emdad Global.': 'ابق على اطلاع بآخر الأخبار والتطورات من إمداد جلوبال.',
                'Read More': 'اقرأ المزيد',
                'Expanding Global Reach': 'توسيع النطاق العالمي',
                'Emdad Global announces new partnerships in European and Asian markets, strengthening our international presence.': 'إمداد جلوبال تعلن عن شراكات جديدة في الأسواق الأوروبية والآسيوية، مما يعزز حضورنا الدولي.',
                'Quality Certification Update': 'تحديث شهادات الجودة',
                'Successfully renewed ISO 22000 and Good Agricultural Practices certifications, reinforcing our commitment to quality standards.': 'تم تجديد شهادات ISO 22000 والممارسات الزراعية الجيدة بنجاح، مما يعزز التزامنا بمعايير الجودة.',
                'Sustainable Agriculture Initiative': 'مبادرة الزراعة المستدامة',
                'Launching new sustainable farming practices to support environmental conservation and premium product quality.': 'إطلاق ممارسات زراعية مستدامة جديدة لدعم الحفاظ على البيئة وجودة المنتجات الممتازة.',
                'View All News': 'عرض جميع الأخبار',
                'Partnership Opportunity': 'فرصة شراكة',
                'Ready to Start Your': 'هل أنت مستعد لبدء',
                'Agricultural Order?': 'طلبك الزراعي؟',
                'Join hundreds of satisfied clients worldwide who trust Emdad Global for their': 'انضم إلى مئات العملاء الراضين حول العالم الذين يثقون في إمداد جلوبال لتلبية',
                'agricultural sourcing needs. Get a personalized quote today and experience the difference.': 'احتياجاتهم من المصادر الزراعية. احصل على عرض أسعار مخصص اليوم واختبر الفرق.',
                'Quick Response': 'استجابة سريعة',
                'Quality Guaranteed': 'جودة مضمونة',
                '24-hour quote turnaround': 'دورة عرض أسعار خلال 24 ساعة',
                'International certifications': 'شهادات دولية',
                'Browse Products': 'تصفح المنتجات',
                'Egyptian Oranges': 'البرتقال المصري',
                'Premium quality Egyptian oranges with exceptional sweetness and juice content.': 'برتقال مصري عالي الجودة بحلاوة استثنائية ومحتوى عصير عالي.',
                'Fresh Grapes': 'العنب الطازج',
                'High-quality table grapes in various varieties for global markets.': 'عنب مائدة عالي الجودة بأصناف متنوعة للأسواق العالمية.',
                'Egyptian Garlic': 'الثوم المصري',
                'Vegetables': 'الخضروات',
                'Premium white garlic with strong flavor and excellent storage capabilities.': 'ثوم أبيض ممتاز بنكهة قوية وقدرات تخزين ممتازة.',
                'IQF Strawberries': 'الفراولة المجمدة سريعاً',
                'Individually Quick Frozen strawberries maintaining fresh taste and nutrition.': 'فراولة مجمدة سريعاً بشكل فردي تحافظ على الطعم الطازج والتغذية.',
                'Organic': 'عضوي',
                'Export Quality': 'جودة التصدير',
                'Years of Excellence': 'سنوات من التميز',
                'Products Exported': 'منتج مُصدر',
                'GlobalG.A.P': 'الممارسات الزراعية العالمية الجيدة',
                'Quality Assurance': 'ضمان الجودة',
                'Reliable Supply Chain': 'سلسلة توريد موثوقة',
                'Expert Team': 'فريق خبراء',
                'Customer Support': 'دعم العملاء',
                'Competitive Pricing': 'أسعار تنافسية',
                'On-Time Delivery': 'التسليم في الوقت المحدد',
                'Learn More': 'تعرف على المزيد',
                'Contact Us Today': 'اتصل بنا اليوم',
                'Get Started': 'ابدأ الآن',
                'Explore Our Products': 'استكشف منتجاتنا',
                'Download Catalog': 'تحميل الكتالوج',
                'Request Samples': 'طلب عينات',
                'Schedule Meeting': 'جدولة اجتماع',
                # Navigation Menu
                'Toggle navigation': 'تبديل التنقل',
                'Home': 'الرئيسية',
                'Products': 'المنتجات',
                'All Products': 'جميع المنتجات',
                'Certifications': 'الشهادات',
                'Services': 'الخدمات',
                'Gallery': 'المعرض',
                'Contact': 'اتصل بنا',
                # Footer
                'Quick Links': 'روابط سريعة',
                'Categories': 'الفئات',
                'Frozen Fruits': 'الفواكه المجمدة',
                'Herbs & Spices': 'الأعشاب والتوابل',
                'WhatsApp Chat': 'محادثة واتساب',
                'Cairo, Egypt': 'القاهرة، مصر',
                'Privacy Policy': 'سياسة الخصوصية',
                'Terms of Service': 'شروط الخدمة',
                'Support': 'الدعم',
                # Additional common terms
                'Contact Information': 'معلومات الاتصال',
                'Follow Us': 'تابعنا',
                'Social Media': 'وسائل التواصل الاجتماعي',
                'Company': 'الشركة',
                'Information': 'المعلومات',
                'Links': 'الروابط',
                'Address': 'العنوان',
                'Phone': 'الهاتف',
                'Email': 'البريد الإلكتروني',
                'Working Hours': 'ساعات العمل',
                'Business Hours': 'ساعات العمل',
                'Office Hours': 'ساعات المكتب',
                'Monday': 'الإثنين',
                'Tuesday': 'الثلاثاء',
                'Wednesday': 'الأربعاء',
                'Thursday': 'الخميس',
                'Friday': 'الجمعة',
                'Saturday': 'السبت',
                'Sunday': 'الأحد',
                'Mon - Fri': 'الإثنين - الجمعة',
                'All rights reserved': 'جميع الحقوق محفوظة',
                'Copyright': 'حقوق الطبع والنشر',
                'Website': 'الموقع الإلكتروني',
                'Online': 'متصل',
                'Offline': 'غير متصل',
                'Available': 'متاح',
                'Unavailable': 'غير متاح',
                'Open': 'مفتوح',
                'Closed': 'مغلق',
                'Loading': 'جاري التحميل',
                'Please wait': 'يرجى الانتظار',
                'Error': 'خطأ',
                'Success': 'نجح',
                'Warning': 'تحذير',
                'Info': 'معلومات',
                'Back to top': 'العودة إلى الأعلى',
                'Go to top': 'الذهاب إلى الأعلى',
                'Scroll to top': 'التمرير إلى الأعلى',
                'Menu': 'القائمة',
                'Navigation': 'التنقل',
                'Main Menu': 'القائمة الرئيسية',
                'Language': 'اللغة',
                'Select Language': 'اختر اللغة',
                'Change Language': 'تغيير اللغة',
                'English': 'الإنجليزية',
                'Arabic': 'العربية',

                # Admin Reports section (keep scoped to avoid affecting other areas)
                'Reports & Analytics': 'التقارير والتحليلات',
                'Apply': 'تطبيق',
                'RFQs Trend': 'اتجاه طلبات عروض الأسعار',
                'RFQs by Status': 'طلبات العروض حسب الحالة',
                'Products by Category': 'المنتجات حسب الفئة',
                'Export RFQs (CSV)': 'تصدير طلبات العروض (CSV)',
                'RFQs': 'طلبات العروض',
                'RFQ Status': 'حالة طلبات العروض',
                'Products': 'المنتجات',
                'New': 'جديد',
                'In Review': 'قيد المراجعة',
                'Quoted': 'مُسَعَّر',
                'Closed': 'مغلق',
                'Cancelled': 'ملغي',

                # Stats cards in reports section
                'Total Products': 'إجمالي المنتجات',
                'Total Categories': 'إجمالي الفئات',
                'Total RFQs': 'إجمالي طلبات العروض',
                'Pending RFQs': 'طلبات العروض المعلقة'
,

                # Recent sections in reports
                'Recent RFQs': 'أحدث طلبات العروض',
                'Recent Products': 'أحدث المنتجات',
                'Name': 'الاسم',
                'Company': 'الشركة',
                'Status': 'الحالة',
                'Date': 'التاريخ',
                'Category': 'الفئة',
                'Active': 'نشط',
                'Inactive': 'غير نشط',
                'Draft': 'مسودة',
                'Uncategorized': 'بدون تصنيف',
                'Reports': 'التقارير'
,
                'Learn More About Us': 'تعرف علينا أكثر'
,
                'In Progress': 'قيد التنفيذ',
                'Completed': 'مكتمل'
            }
        }

        def _(text):
            # First try manual translations
            if current_language in manual_translations and text in manual_translations[current_language]:
                return manual_translations[current_language][text]

            # Fallback to gettext
            try:
                if not hasattr(g, 'locale'):
                    g.locale = current_language
                translated = gettext(text)
                return translated
            except:
                return text

        def get_latest_news(limit=2):
            """Get latest published news for footer"""
            try:
                from app.models import News
                from datetime import datetime
                return News.query.filter_by(status='published').filter(
                    News.publish_at <= datetime.utcnow()
                ).order_by(News.publish_at.desc()).limit(limit).all()
            except:
                return []

        def csrf_token():
            """Generate CSRF token for templates"""
            from flask_wtf.csrf import generate_csrf
            return generate_csrf()

        def image_url_with_timestamp(filename):
            """Add timestamp to image URL to prevent caching"""
            import time
            from flask import url_for
            timestamp = int(time.time())
            return f"{url_for('main.uploaded_file', filename=filename)}?t={timestamp}"

        return {
            'COMPANY_NAME': app.config['COMPANY_NAME'],
            'COMPANY_EMAIL': app.config['COMPANY_EMAIL'],
            'COMPANY_PHONE': app.config['COMPANY_PHONE'],
            'COMPANY_WHATSAPP': app.config['COMPANY_WHATSAPP'],
            'COMPANY_ADDRESS': app.config['COMPANY_ADDRESS'],
            'SITE_NAME': app.config['SITE_NAME'],
            'LANGUAGES': app.config['LANGUAGES'],
            'current_language': current_language,
            'get_locale': lambda: current_language,
            'is_rtl': current_language == 'ar',
            '_': _,
            'get_latest_news': get_latest_news,
            'csrf_token': csrf_token,
            'image_url_with_timestamp': image_url_with_timestamp,
            'nav_categories': nav_categories,
            'nav_products': nav_products
        }

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500



    return app
