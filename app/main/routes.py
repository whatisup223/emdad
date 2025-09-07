from flask import render_template, request, redirect, url_for, flash, current_app, session, jsonify, send_from_directory
from flask_mail import Message
from werkzeug.utils import secure_filename
from app.main import bp
from app.models import Category, Product, Certification, Service, News, Gallery, RFQ, CompanyInfo, GalleryCategory
from app.forms import RFQForm
from app import db, mail
import os
from datetime import datetime

@bp.route('/')
def index():
    """Homepage."""
    try:
        # Get featured categories (now using show_on_homepage instead of parent_id=None)
        featured_categories = Category.query.filter_by(
            is_active=True,
            show_on_homepage=True
        ).order_by(Category.sort_order).limit(4).all() or []
    except Exception as e:
        print(f"Warning: Could not load categories: {e}")
        featured_categories = []

    try:
        # Get featured products (now using show_on_homepage)
        featured_products = Product.query.filter_by(
            status='active',
            show_on_homepage=True
        ).order_by(Product.sort_order).limit(8).all() or []
    except Exception as e:
        print(f"Warning: Could not load products: {e}")
        featured_products = []

    # Get latest news (now using show_on_homepage)
    latest_news = News.query.filter_by(
        status='published',
        show_on_homepage=True
    ).filter(News.publish_at <= datetime.utcnow()).order_by(News.publish_at.desc()).limit(3).all() or []

    # Get company info sections for homepage
    about_intro = CompanyInfo.query.filter_by(key='about_intro', is_active=True).first()
    why_choose_us = CompanyInfo.query.filter_by(key='why_choose_us', is_active=True).first()

    return render_template('main/index.html',
                         featured_categories=featured_categories,
                         featured_products=featured_products,
                         latest_news=latest_news,
                         about_intro=about_intro,
                         why_choose_us=why_choose_us)

@bp.route('/about')
def about():
    """About page (new)."""
    return render_template('main/about.html')


@bp.route('/calendar')
def calendar():
    """Public Seasonality Calendar page."""
    from app.models import Product, Category
    from flask import request
    language = request.args.get('lang') or ('ar' if session.get('language') == 'ar' else 'en')
    category_key = request.args.get('category')
    q = (Product.query
         .filter_by(status='active')
         .order_by(Product.sort_order, Product.name_en))
    categories = Category.query.filter_by(is_active=True, parent_id=None).order_by(Category.sort_order).all() or []
    if category_key:
        from app.models import Category as Cat
        cat = Cat.query.filter_by(key=category_key, is_active=True).first()
        if cat:
            q = q.filter_by(category_id=cat.id)
    products = q.all()
    # Build a simple normalized seasonality map per product for the template
    def normalize(prod):
        raw = prod.get_seasonality() or {}
        data_lang = prod.get_seasonality_lang(language) or {}
        # Unwrap 'fresh' if present in language-scoped data
        base = data_lang.get('fresh') if isinstance(data_lang, dict) and 'fresh' in data_lang else data_lang
        # Normalize five states from base
        peak = sorted(set((base.get('peak') or []))) if isinstance(base, dict) else []
        available = sorted(set((base.get('available') or []))) if isinstance(base, dict) else []
        limited = sorted(set((base.get('limited') or []))) if isinstance(base, dict) else []
        off = sorted(set((base.get('off') or []))) if isinstance(base, dict) else []
        # IQF months can live under base['iqf'] (list) or raw['iqf'] (list or dict)
        iqf_months = []
        if isinstance(base, dict) and isinstance(base.get('iqf'), list):
            iqf_months = base.get('iqf')
        else:
            iqf = raw.get('iqf') if isinstance(raw, dict) else None
            if isinstance(iqf, list):
                iqf_months = iqf
            elif isinstance(iqf, dict):
                if iqf.get('year_round'):
                    iqf_months = [1,2,3,4,5,6,7,8,9,10,11,12]
                elif isinstance(iqf.get('months'), list):
                    iqf_months = iqf.get('months')
        return {
            'id': prod.id,
            'name': prod.get_name(language),
            'slug': prod.slug,
            'category_key': prod.category.key if prod.category else None,
            'peak': peak,
            'available': available,
            'limited': limited,
            'off': off,
            'iqf': sorted(set(iqf_months))
        }
    items = [normalize(p) for p in products]
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    # Inject iqf sub-structure if exists
    for it, p in zip(items, products):
        data = p.get_seasonality() or {}
        it['iqf'] = data.get('iqf', {})
    return render_template('main/calendar.html', items=items, months=months, categories=categories, current_category=category_key)


@bp.route('/products')
def products():
    """Products listing page."""
    # Get category filter
    category_key = request.args.get('cat')
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    # Base query
    query = Product.query.filter_by(status='active')

    # Filter by category if specified
    selected_category = None
    if category_key:
        selected_category = Category.query.filter_by(key=category_key, is_active=True).first()
        if selected_category:
            query = query.filter_by(category_id=selected_category.id)

    # Paginate results
    products = query.order_by(Product.sort_order, Product.name_en).paginate(
        page=page,
        per_page=current_app.config['PRODUCTS_PER_PAGE'],
        error_out=False
    )

    # Get all categories for filter menu
    categories = Category.query.filter_by(is_active=True, parent_id=None).order_by(Category.sort_order).all() or []

    return render_template('main/products.html',
                         products=products,
                         categories=categories,
                         selected_category=selected_category)

@bp.route('/product/<slug>')
def product_detail(slug):
    """Product detail page."""
    product = Product.query.filter_by(slug=slug, status='active').first_or_404()

    # Get related products from same category
    related_products = Product.query.filter_by(
        category_id=product.category_id,
        status='active'
    ).filter(Product.id != product.id).order_by(Product.sort_order).limit(4).all()

    return render_template('main/product_detail.html',
                         product=product,
                         related_products=related_products)

@bp.route('/certifications')
def certifications():
    """Certifications page."""
    certifications = Certification.query.filter_by(is_active=True).order_by(Certification.sort_order).all()
    return render_template('main/certifications.html', certifications=certifications)

@bp.route('/services')
def services():
    """Services page."""
    services = Service.query.filter_by(is_active=True).order_by(Service.sort_order).all()
    return render_template('main/services.html', services=services)

@bp.route('/gallery')
def gallery():
    """Gallery page."""
    category = request.args.get('category', 'all')

    # Base query
    query = Gallery.query.filter_by(is_active=True)

    # Filter by category if specified
    if category != 'all':
        query = query.filter_by(category=category)

    gallery_items = query.order_by(Gallery.sort_order).all()

    # Get available categories (include seeded defaults if used in DB)
    categories = db.session.query(Gallery.category).filter_by(is_active=True).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]

    # Ensure default categories appear if they exist in GalleryCategory (seeded) even لو لم توجد صور بعد
    try:
        defaults = ['farms','packing','storage','exports']
        default_rows = GalleryCategory.query.filter(GalleryCategory.key.in_(defaults), GalleryCategory.is_active == True).all()
        for row in default_rows:
            if row.key not in categories:
                categories.append(row.key)
    except Exception:
        pass

    # Map icons
    try:
        icon_rows = GalleryCategory.query.filter(GalleryCategory.key.in_(categories)).all()
        category_icons = {row.key: row.icon_class for row in icon_rows}
    except Exception:
        category_icons = {}

    # Map localized names (en, ar) for categories if available
    try:
        name_rows = GalleryCategory.query.filter(GalleryCategory.key.in_(categories)).all()
        category_names = {row.key: (row.name_en, row.name_ar) for row in name_rows}
    except Exception:
        category_names = {}

    return render_template('main/gallery.html',
                         gallery_items=gallery_items,
                         categories=categories,
                         category_icons=category_icons,
                         category_names=category_names,
                         selected_category=category)

@bp.route('/news')
def news():
    """News listing page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    # Get published news
    news_items = News.query.filter_by(status='published').filter(
        News.publish_at <= datetime.utcnow()
    ).order_by(News.publish_at.desc()).paginate(
        page=page,
        per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )

    # Get featured news
    featured_news = News.query.filter_by(
        status='published',
        featured=True
    ).filter(News.publish_at <= datetime.utcnow()).order_by(News.publish_at.desc()).limit(3).all()

    return render_template('main/news.html',
                         news_items=news_items,
                         featured_news=featured_news)

@bp.route('/news/<slug>')
def news_detail(slug):
    """News article detail page."""
    article = News.query.filter_by(slug=slug, status='published').filter(
        News.publish_at <= datetime.utcnow()
    ).first_or_404()

    # Get related articles
    related_articles = News.query.filter_by(status='published').filter(
        News.id != article.id,
        News.publish_at <= datetime.utcnow()
    ).order_by(News.publish_at.desc()).limit(3).all()

    return render_template('main/news_detail.html',
                         article=article,
                         related_articles=related_articles)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with RFQ form."""
    form = RFQForm()

    if form.validate_on_submit():
        # Create RFQ record (avoid passing fields not in DB to prevent constructor errors)
        rfq = RFQ(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            country=form.country.data,
            category_key=form.category_key.data,
            product_name=form.product_name.data,
            quantity=form.quantity.data,
            packaging_preference=form.packaging_preference.data,
            message=form.message.data
        )
        # Set optional fields if model supports them (forward-compatible without migrations)
        try:
            if hasattr(RFQ, 'delivery_date') and form.delivery_date.data:
                rfq.delivery_date = form.delivery_date.data.date()
            if hasattr(RFQ, 'budget') and form.budget.data:
                rfq.budget = form.budget.data
        except Exception:
            pass

        # Handle file upload
        if form.attachment.data:
            filename = secure_filename(form.attachment.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'rfq', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.attachment.data.save(upload_path)
            rfq.attachment_path = filename

        # Save to database
        db.session.add(rfq)
        db.session.commit()

        # Send notification emails
        try:
            # Email to admin
            admin_msg = Message(
                subject=f'New RFQ from {rfq.name}',
                recipients=[current_app.config['COMPANY_EMAIL']],
                body=f"""
New RFQ received:

Name: {rfq.name}
Email: {rfq.email}
Company: {rfq.company or 'N/A'}
Country: {rfq.country}
Category: {rfq.category_key}
Product: {rfq.product_name or 'N/A'}
Quantity: {rfq.quantity or 'N/A'}

Message:
{rfq.message}

RFQ ID: {rfq.id}
                """
            )
            mail.send(admin_msg)

            # Auto-reply to customer
            customer_msg = Message(
                subject='Thank you for your inquiry - Emdad Global',
                recipients=[rfq.email],
                body=f"""
Dear {rfq.name},

Thank you for your inquiry. We have received your request for quote and will respond within 24 hours.

Your inquiry details:
- Product Category: {rfq.category_key}
- Product: {rfq.product_name or 'N/A'}
- Quantity: {rfq.quantity or 'N/A'}

Reference ID: {rfq.id}

Best regards,
Emdad Global Team
{current_app.config['COMPANY_EMAIL']}
{current_app.config['COMPANY_PHONE']}
                """
            )
            mail.send(customer_msg)

        except Exception as e:
            current_app.logger.error(f'Failed to send RFQ emails: {e}')

        return redirect(url_for('main.contact', submitted=1))

    return render_template('main/contact.html', form=form)

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files with cache control."""
    from flask import make_response
    upload_path = os.path.join(current_app.instance_path, current_app.config.get('UPLOAD_FOLDER', 'uploads'))

    try:
        response = make_response(send_from_directory(upload_path, filename))

        # Add cache control headers to prevent caching issues
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response
    except FileNotFoundError:
        # If file not found, return 404
        from flask import abort
        abort(404)

@bp.route('/set-language/<language>')
def set_language(language):
    """Set user language preference."""
    if language in current_app.config['LANGUAGES']:
        session['language'] = language
    return redirect(request.referrer or url_for('main.index'))

@bp.route('/api/products/<category_key>')
def api_products_by_category(category_key):
    """API endpoint to get products by category (for dynamic form updates)."""
    category = Category.query.filter_by(key=category_key, is_active=True).first()
    if not category:
        return jsonify([])

    products = Product.query.filter_by(
        category_id=category.id,
        status='active'
    ).order_by(Product.sort_order, Product.name_en).all()

    # Return both languages so the client can display based on current language
    return jsonify([{
        'id': product.id,
        'name': product.name_en,  # backward compat
        'name_en': product.name_en,
        'name_ar': product.name_ar,
        'slug': product.slug
    } for product in products])
