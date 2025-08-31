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
        # 1. Check URL parameter
        if request.args.get('lang') in app.config['LANGUAGES']:
            session['language'] = request.args.get('lang')
            return request.args.get('lang')

        # 2. Check if language is set in session
        if 'language' in session and session['language'] in app.config['LANGUAGES']:
            return session['language']

        # 3. Check Accept-Language header
        default_lang = request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['BABEL_DEFAULT_LOCALE']
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
        from flask_babel import gettext

        current_language = session.get('language', 'en')

        def _(text):
            return gettext(text)

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
            'csrf_token': csrf_token
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
