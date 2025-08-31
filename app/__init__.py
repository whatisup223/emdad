import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()
limiter = Limiter(key_func=get_remote_address)

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
    os.makedirs(os.path.join(upload_dir, 'products'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'gallery'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'news'), exist_ok=True)
    os.makedirs(os.path.join(upload_dir, 'rfq'), exist_ok=True)

    # Language selector function
    def get_locale():
        from flask import request, session
        # 1. Check if language is set in session
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            print(f"Using session language: {session['language']}")  # Debug
            return session['language']
        # 2. Check Accept-Language header
        default_lang = request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']
        print(f"Using default language: {default_lang}")  # Debug
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
        from flask import session
        from simple_translations import translate, get_current_language

        current_language = session.get('language', 'en')

        def _(text):
            return translate(text, current_language)

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
            'get_latest_news': get_latest_news
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

    # Initialize database on first request
    @app.before_first_request
    def initialize_database():
        """Initialize database tables and basic data on first request"""
        try:
            # Create all tables
            db.create_all()

            # Check if we need to create basic data
            from app.models import User, Category

            # Create admin user if not exists
            if User.query.count() == 0:
                admin_user = User(
                    name='Administrator',
                    email='admin@emdadglobal.com',
                    role='admin'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                print("✅ Created admin user")

            # Create basic categories if not exist
            if Category.query.count() == 0:
                categories = [
                    {'key': 'citrus', 'name_en': 'Citrus Fruits', 'name_ar': 'الحمضيات', 'slug': 'citrus-fruits'},
                    {'key': 'fresh-fruits', 'name_en': 'Fresh Fruits', 'name_ar': 'الفواكه الطازجة', 'slug': 'fresh-fruits'},
                    {'key': 'vegetables', 'name_en': 'Fresh Vegetables', 'name_ar': 'الخضروات الطازجة', 'slug': 'fresh-vegetables'},
                    {'key': 'frozen', 'name_en': 'Frozen Fruits', 'name_ar': 'الفواكه المجمدة', 'slug': 'frozen-fruits'}
                ]

                for i, cat_data in enumerate(categories):
                    category = Category(
                        key=cat_data['key'],
                        name_en=cat_data['name_en'],
                        name_ar=cat_data['name_ar'],
                        slug=cat_data['slug'],
                        sort_order=i + 1,
                        is_active=True
                    )
                    db.session.add(category)
                print("✅ Created basic categories")

            db.session.commit()
            print("✅ Database initialization completed")

        except Exception as e:
            print(f"⚠️ Database initialization error: {e}")
            db.session.rollback()

    return app
