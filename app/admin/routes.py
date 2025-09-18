from flask import render_template, request, redirect, url_for, flash, current_app, jsonify, session, send_from_directory, abort, Response
from flask_babel import gettext as _

from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin import bp
from app.models import User, Category, Product, Certification, Service, News, Gallery, RFQ, CompanyInfo, AuditLog, GalleryCategory

# Localized text helper for API responses (scoped to reports only)
# Avoids touching global translations; uses session language and minimal mapping.
def _t(text: str) -> str:
    try:
        lang = session.get('language', 'en')
    except Exception:
        lang = 'en'
    if lang != 'ar':
        return text
    mapping = {
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
        'Cancelled': 'ملغي'
    }
    return mapping.get(text, text)

from app.forms import LoginForm, UserForm, CategoryForm, ProductForm, CertificationForm, ServiceForm, NewsForm, GalleryForm, CompanyInfoForm
from app import db
import os
import json
from datetime import datetime
import uuid

def admin_required(f):
    """Decorator to require admin role."""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_permission('manage_users'):
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def editor_required(f):
    """Decorator to require editor role or higher."""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.has_permission('create'):
            flash('Access denied. Editor privileges required.', 'error')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login."""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, is_active=True).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()

            # Log the login
            audit_log = AuditLog(
                user_id=user.id,
                action='login',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db.session.add(audit_log)
            db.session.commit()

            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('admin.dashboard')
            return redirect(next_page)

        flash('Invalid email or password.', 'error')

    return render_template('admin/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    """Admin logout."""
    # Log the logout
    audit_log = AuditLog(
        user_id=current_user.id,
        action='logout',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(audit_log)
    db.session.commit()

    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard."""
    # Get statistics
    stats = {
        'total_products': Product.query.filter_by(status='active').count(),
        'total_categories': Category.query.filter_by(is_active=True).count(),
        'pending_rfqs': RFQ.query.filter_by(status='new').count(),
        'total_rfqs': RFQ.query.count(),
        'published_news': News.query.filter_by(status='published').count(),
        'gallery_images': Gallery.query.filter_by(is_active=True).count()
    }

    # Get recent RFQs
    recent_rfqs = RFQ.query.order_by(RFQ.created_at.desc()).limit(5).all()

    # Get recent audit logs
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_rfqs=recent_rfqs,
                         recent_logs=recent_logs)

# Categories Management

@bp.route('/calendar')
@login_required
def calendar_admin():
    """Admin Seasonality Calendar management."""
    products = Product.query.filter_by(status='active').order_by(Product.sort_order, Product.name_en).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('admin/calendar.html', products=products, categories=categories)

@bp.route('/calendar/<int:product_id>/save', methods=['POST'])
@editor_required
def calendar_save(product_id):
    """Save seasonality JSON for a product."""
    import json
    product = Product.query.get_or_404(product_id)
    payload = request.get_json(silent=True) or {}
    # sanitize: ensure arrays of ints 1..12
    def clean(arr):
        try:
            return sorted({m for m in (arr or []) if isinstance(m, int) and 1 <= m <= 12})
        except Exception:
            return []
    # Backward-compatible save format:
    # If payload has 'fresh' or 'iqf', store as nested; else treat payload as fresh-only.
    if ('fresh' in payload) or isinstance(payload.get('iqf'), dict):
        fresh = payload.get('fresh') or {}
        iqf_payload = payload.get('iqf')
        # Normalize IQF payload which can be dict or list
        if isinstance(iqf_payload, dict):
            yr = bool(iqf_payload.get('year_round'))
            iqf_months = [] if yr else clean(iqf_payload.get('months'))
        elif isinstance(iqf_payload, list):
            yr = False
            iqf_months = clean(iqf_payload)
        else:
            yr = False
            iqf_months = []
        data = {
            'fresh': {
                'peak': clean(fresh.get('peak')),
                'available': clean(fresh.get('available')),
                'limited': clean(fresh.get('limited')),
                'off': clean(fresh.get('off')),
                'iqf': clean(fresh.get('iqf'))
            },
            'iqf': {
                'year_round': yr,
                'months': iqf_months
            }
        }
    else:
        data = {
            'peak': clean(payload.get('peak')),
            'available': clean(payload.get('available')),
            'limited': clean(payload.get('limited')),
            'off': clean(payload.get('off')),
            'iqf': clean(payload.get('iqf'))
        }

    product.seasonality = json.dumps(data)
    db.session.commit()
    return jsonify({'ok': True, 'nested': ('fresh' in payload or 'iqf' in payload)})

@bp.route('/categories')
@login_required
def categories():
    """Categories listing."""
    categories = Category.query.order_by(Category.sort_order, Category.name_en).all()
    return render_template('admin/categories.html', categories=categories)

@bp.route('/categories/new', methods=['GET', 'POST'])
@editor_required
def category_new():
    """Create new category."""
    form = CategoryForm()

    # Load parent category choices
    categories = Category.query.filter_by(is_active=True).all()
    form.parent_id.choices = [('', 'No Parent')] + [(str(cat.id), cat.name_en) for cat in categories]

    if request.method == 'POST':
        if form.validate_on_submit():
            category = Category(
            key=form.key.data,
            name_en=form.name_en.data,
            name_ar=form.name_ar.data,
            slug=form.slug.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            parent_id=form.parent_id.data or None,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data,
            show_on_homepage=form.show_on_homepage.data
        )

        # Handle image upload
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'categories', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)
            category.image_path = filename

            db.session.add(category)
            db.session.commit()

            # Log the action
            audit_log = AuditLog(
                user_id=current_user.id,
                action='create',
                entity_type='category',
                entity_id=category.id,
                ip_address=request.remote_addr
            )
            db.session.add(audit_log)
            db.session.commit()

            flash('Category created successfully.', 'success')
            return redirect(url_for('admin.categories'))
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'error')
            return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', form=form, title='New Category')

@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def category_edit(id):
    """Edit category."""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category, category=category)

    # Load parent category choices (exclude current category to prevent circular reference)
    categories = Category.query.filter(Category.is_active == True, Category.id != id).all()
    form.parent_id.choices = [('', 'No Parent')] + [(str(cat.id), cat.name_en) for cat in categories]

    if form.validate_on_submit():
        category.key = form.key.data
        category.name_en = form.name_en.data
        category.name_ar = form.name_ar.data
        category.slug = form.slug.data
        category.description_en = form.description_en.data
        category.description_ar = form.description_ar.data
        category.parent_id = form.parent_id.data or None
        category.sort_order = form.sort_order.data
        category.is_active = form.is_active.data
        category.show_on_homepage = form.show_on_homepage.data
        category.updated_at = datetime.utcnow()

        # Handle image upload
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'categories', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)
            category.image_path = filename

        db.session.commit()

        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='category',
            entity_id=category.id,
            ip_address=request.remote_addr
        )
        db.session.add(audit_log)
        db.session.commit()

        flash('Category updated successfully.', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', form=form, category=category, title='Edit Category')

@bp.route('/categories/<int:id>/delete', methods=['POST'])
@admin_required
def category_delete(id):
    """Delete category."""
    category = Category.query.get_or_404(id)

    # Check if category has products
    if category.products.count() > 0:
        flash('Cannot delete category with products. Move products first.', 'error')
        return redirect(url_for('admin.categories'))

    # Check if category has subcategories
    if category.children:
        flash('Cannot delete category with subcategories. Delete subcategories first.', 'error')
        return redirect(url_for('admin.categories'))

    db.session.delete(category)
    db.session.commit()

    # Log the action
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity_type='category',
        entity_id=id,
        ip_address=request.remote_addr
    )
    db.session.add(audit_log)
    db.session.commit()

    flash('Category deleted successfully.', 'success')
    return redirect(url_for('admin.categories'))

# Products Management
@bp.route('/products')
@login_required
def products():
    """Products listing."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    try:
        category_id = request.args.get('category', type=int) if request.args.get('category') else None
    except ValueError:
        category_id = None

    status = request.args.get('status', 'all')
    search = request.args.get('search', '')

    # Base query
    query = Product.query

    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)

    if status != 'all':
        query = query.filter_by(status=status)

    if search:
        query = query.filter(Product.name_en.contains(search))

    # Paginate
    products = query.order_by(Product.updated_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    # Get categories for filter
    categories = Category.query.filter_by(is_active=True).order_by(Category.name_en).all()

    return render_template('admin/products.html',
                         products=products,
                         categories=categories,
                         current_category=category_id,
                         current_status=status,
                         current_search=search)

@bp.route('/products/new', methods=['GET', 'POST'])
@editor_required
def product_new():
    """Create new product."""
    form = ProductForm()

    if request.method == 'POST':
        # Check for CSRF errors specifically
        if not form.validate():
            csrf_errors = form.csrf_token.errors if hasattr(form, 'csrf_token') and form.csrf_token.errors else []
            if csrf_errors:
                flash('خطأ في الأمان: انتهت صلاحية النموذج. يرجى المحاولة مرة أخرى.', 'error')
                return render_template('admin/product_form.html', form=form, title='إضافة منتج جديد')

    if form.validate_on_submit():
        # Prepare specifications as JSON
        specifications = {}
        if form.specifications_en.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_specs = json.loads(form.specifications_en.data)
                specifications['en'] = parsed_specs
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                specifications['en'] = {'notes': form.specifications_en.data}

        if form.specifications_ar.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_specs = json.loads(form.specifications_ar.data)
                specifications['ar'] = parsed_specs
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                specifications['ar'] = {'notes': form.specifications_ar.data}

        # Prepare packaging as JSON
        packaging = {}
        if form.packaging_en.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_packaging = json.loads(form.packaging_en.data)
                packaging['en'] = parsed_packaging
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                packaging['en'] = {'notes': form.packaging_en.data}

        if form.packaging_ar.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_packaging = json.loads(form.packaging_ar.data)
                packaging['ar'] = parsed_packaging
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                packaging['ar'] = {'notes': form.packaging_ar.data}

        # Prepare applications/use cases as JSON
        applications = {}
        if getattr(form, 'applications_en', None) and form.applications_en.data:
            try:
                parsed_apps = json.loads(form.applications_en.data)
                applications['en'] = parsed_apps
            except json.JSONDecodeError:
                applications['en'] = {'notes': form.applications_en.data}
        if getattr(form, 'applications_ar', None) and form.applications_ar.data:
            try:
                parsed_apps = json.loads(form.applications_ar.data)
                applications['ar'] = parsed_apps
            except json.JSONDecodeError:
                applications['ar'] = {'notes': form.applications_ar.data}

        # Prepare quality targets as JSON
        quality_targets = {}
        if getattr(form, 'quality_targets_en', None) and form.quality_targets_en.data:
            try:
                quality_targets['en'] = json.loads(form.quality_targets_en.data)
            except json.JSONDecodeError:
                quality_targets['en'] = {'notes': form.quality_targets_en.data}
        if getattr(form, 'quality_targets_ar', None) and form.quality_targets_ar.data:
            try:
                quality_targets['ar'] = json.loads(form.quality_targets_ar.data)
            except json.JSONDecodeError:
                quality_targets['ar'] = {'notes': form.quality_targets_ar.data}

        # Prepare commercial docs as JSON
        commercial_docs = {}
        if getattr(form, 'commercial_docs_en', None) and form.commercial_docs_en.data:
            try:
                commercial_docs['en'] = json.loads(form.commercial_docs_en.data)
            except json.JSONDecodeError:
                commercial_docs['en'] = {'notes': form.commercial_docs_en.data}
        if getattr(form, 'commercial_docs_ar', None) and form.commercial_docs_ar.data:
            try:
                commercial_docs['ar'] = json.loads(form.commercial_docs_ar.data)
            except json.JSONDecodeError:
                commercial_docs['ar'] = {'notes': form.commercial_docs_ar.data}

        product = Product(
            name_en=form.name_en.data,
            name_ar=form.name_ar.data,
            slug=form.slug.data,
            category_id=form.category_id.data,
            hs_code=form.hs_code.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            short_description_en=form.short_description_en.data,
            short_description_ar=form.short_description_ar.data,
            specifications=json.dumps(specifications) if specifications else None,
            packaging_options=json.dumps(packaging) if packaging else None,
            applications=json.dumps(applications) if applications else None,
            quality_targets=json.dumps(quality_targets) if quality_targets else None,
            commercial_docs=json.dumps(commercial_docs) if commercial_docs else None,
            seo_title_en=form.seo_title_en.data,
            seo_title_ar=form.seo_title_ar.data,
            seo_description_en=form.seo_description_en.data,
            seo_description_ar=form.seo_description_ar.data,
            status=form.status.data,
            featured=form.featured.data,
            show_on_homepage=form.show_on_homepage.data,
            sort_order=form.sort_order.data
        )

        db.session.add(product)
        db.session.flush()  # Get the product ID

        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'products', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)

            # Create ProductImage record
            from app.models import ProductImage
            product_image = ProductImage(
                product_id=product.id,
                filename=filename,
                alt_text_en=product.name_en,
                alt_text_ar=product.name_ar,
                is_main=True,
                sort_order=0
            )
            db.session.add(product_image)

        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='create',
            entity_type='products',
            entity_id=product.id,
            details=json.dumps({'name': product.name_en})
        )
        db.session.add(audit_log)
        db.session.commit()

        flash('Product created successfully.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title='New Product')

@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def product_edit(id):
    """Edit product."""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    if request.method == 'POST':
        # Check for CSRF errors specifically
        if not form.validate():
            csrf_errors = form.csrf_token.errors if hasattr(form, 'csrf_token') and form.csrf_token.errors else []
            if csrf_errors:
                flash('خطأ في الأمان: انتهت صلاحية النموذج. يرجى المحاولة مرة أخرى.', 'error')
                return render_template('admin/product_form.html', form=form, title=f'تعديل المنتج: {product.name_ar or product.name_en}', product=product)

    if form.validate_on_submit():
        # Prepare specifications as JSON
        specifications = {}
        if form.specifications_en.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_specs = json.loads(form.specifications_en.data)
                specifications['en'] = parsed_specs
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                specifications['en'] = {'notes': form.specifications_en.data}

        if form.specifications_ar.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_specs = json.loads(form.specifications_ar.data)
                specifications['ar'] = parsed_specs
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                specifications['ar'] = {'notes': form.specifications_ar.data}

        # Prepare packaging as JSON
        packaging = {}
        if form.packaging_en.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_packaging = json.loads(form.packaging_en.data)
                packaging['en'] = parsed_packaging
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                packaging['en'] = {'notes': form.packaging_en.data}

        if form.packaging_ar.data:
            # Try to parse as JSON first, fallback to plain text
            try:
                # If it's already valid JSON, parse and store it
                parsed_packaging = json.loads(form.packaging_ar.data)
                packaging['ar'] = parsed_packaging
            except json.JSONDecodeError:
                # If not JSON, store as plain text under 'notes'
                packaging['ar'] = {'notes': form.packaging_ar.data}

        # Prepare applications/use cases as JSON
        applications = {}
        if getattr(form, 'applications_en', None) and form.applications_en.data:
            try:
                parsed_apps = json.loads(form.applications_en.data)
                applications['en'] = parsed_apps
            except json.JSONDecodeError:
                applications['en'] = {'notes': form.applications_en.data}
        if getattr(form, 'applications_ar', None) and form.applications_ar.data:
            try:
                parsed_apps = json.loads(form.applications_ar.data)
                applications['ar'] = parsed_apps
            except json.JSONDecodeError:
                applications['ar'] = {'notes': form.applications_ar.data}


        # Prepare quality targets as JSON
        quality_targets = {}
        if getattr(form, 'quality_targets_en', None) and form.quality_targets_en.data:
            try:
                quality_targets['en'] = json.loads(form.quality_targets_en.data)
            except json.JSONDecodeError:
                quality_targets['en'] = {'notes': form.quality_targets_en.data}
        if getattr(form, 'quality_targets_ar', None) and form.quality_targets_ar.data:
            try:
                quality_targets['ar'] = json.loads(form.quality_targets_ar.data)
            except json.JSONDecodeError:
                quality_targets['ar'] = {'notes': form.quality_targets_ar.data}

        # Prepare commercial docs as JSON
        commercial_docs = {}
        if getattr(form, 'commercial_docs_en', None) and form.commercial_docs_en.data:
            try:
                commercial_docs['en'] = json.loads(form.commercial_docs_en.data)
            except json.JSONDecodeError:
                commercial_docs['en'] = {'notes': form.commercial_docs_en.data}
        if getattr(form, 'commercial_docs_ar', None) and form.commercial_docs_ar.data:
            try:
                commercial_docs['ar'] = json.loads(form.commercial_docs_ar.data)
            except json.JSONDecodeError:
                commercial_docs['ar'] = {'notes': form.commercial_docs_ar.data}

        product.name_en = form.name_en.data
        product.name_ar = form.name_ar.data
        product.slug = form.slug.data
        product.category_id = form.category_id.data
        product.hs_code = form.hs_code.data
        product.description_en = form.description_en.data
        product.description_ar = form.description_ar.data
        product.short_description_en = form.short_description_en.data
        product.short_description_ar = form.short_description_ar.data
        product.specifications = json.dumps(specifications) if specifications else None
        product.packaging_options = json.dumps(packaging) if packaging else None
        product.applications = json.dumps(applications) if applications else None
        product.quality_targets = json.dumps(quality_targets) if quality_targets else None
        product.commercial_docs = json.dumps(commercial_docs) if commercial_docs else None
        product.seo_title_en = form.seo_title_en.data
        product.seo_title_ar = form.seo_title_ar.data
        product.seo_description_en = form.seo_description_en.data
        product.seo_description_ar = form.seo_description_ar.data
        product.status = form.status.data
        product.featured = form.featured.data
        product.show_on_homepage = form.show_on_homepage.data
        product.sort_order = form.sort_order.data
        product.updated_at = datetime.utcnow()

        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'products', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)

            # Remove old main image
            from app.models import ProductImage
            old_main_image = ProductImage.query.filter_by(product_id=product.id, is_main=True).first()
            if old_main_image:
                db.session.delete(old_main_image)

            # Create new ProductImage record
            product_image = ProductImage(
                product_id=product.id,
                filename=filename,
                alt_text_en=product.name_en,
                alt_text_ar=product.name_ar,
                is_main=True,
                sort_order=0
            )
            db.session.add(product_image)

        db.session.commit()

        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='products',
            entity_id=product.id,
            details=json.dumps({'name': product.name_en})
        )
        db.session.add(audit_log)
        db.session.commit()

        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, title='Edit Product')

@bp.route('/products/<int:id>/delete', methods=['POST'])
@admin_required
def product_delete(id):
    """Delete product."""
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    # Log the action
    audit_log = AuditLog(
        user_id=current_user.id,
        action='delete',
        entity_type='products',
        entity_id=id,
        details=json.dumps({'name': product.name_en})
    )
    db.session.add(audit_log)
    db.session.commit()

    flash('Product deleted successfully.', 'success')
    return redirect(url_for('admin.products'))

# RFQ Management
@bp.route('/rfqs')
@login_required
def rfqs():
    """RFQ listing."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    status = request.args.get('status', 'all')

    # Base query
    query = RFQ.query

    # Apply status filter
    if status != 'all':
        query = query.filter_by(status=status)

    # Paginate
    rfqs = query.order_by(RFQ.created_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    return render_template('admin/rfqs.html', rfqs=rfqs, current_status=status)

@bp.route('/rfqs/<int:id>')
@login_required
def rfq_detail(id):
    """RFQ detail view."""
    rfq = RFQ.query.get_or_404(id)
    return render_template('admin/rfq_detail.html', rfq=rfq)
@bp.route('/rfqs/<int:id>/attachment')
@login_required
def rfq_download_attachment(id):
    """Download RFQ attachment if exists."""
    rfq = RFQ.query.get_or_404(id)
    if not rfq.attachment_path:
        abort(404)
    # Build path under instance/uploads/rfq
    base_dir = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'rfq')
    return send_from_directory(base_dir, rfq.attachment_path, as_attachment=True)


@bp.route('/rfqs/<int:id>/status', methods=['POST'])
@editor_required
def rfq_update_status(id):
    """Update RFQ status."""
    from flask import jsonify
    rfq = RFQ.query.get_or_404(id)
    data = request.get_json()

    if 'status' in data:
        rfq.status = data['status']
        rfq.updated_at = datetime.utcnow()
        db.session.commit()

        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='rfq',
            entity_id=rfq.id,
            details=json.dumps({'status': data['status']})
        )
        db.session.add(audit_log)
        db.session.commit()

        return jsonify({'success': True})

    return jsonify({'success': False})

@bp.route('/rfqs/<int:id>/priority', methods=['POST'])
@editor_required
def rfq_update_priority(id):
    """Update RFQ priority."""
    from flask import jsonify
    rfq = RFQ.query.get_or_404(id)
    data = request.get_json()

    if 'priority' in data:
        rfq.priority = data['priority']
        rfq.updated_at = datetime.utcnow()
        db.session.commit()

        # Log the action
        audit_log = AuditLog(
            user_id=current_user.id,
            action='update',
            entity_type='rfq',
            entity_id=rfq.id,
            details=json.dumps({'priority': data['priority']})
        )
        db.session.add(audit_log)
        db.session.commit()

        return jsonify({'success': True})

    return jsonify({'success': False})

@bp.route('/set_language/<language>')
def set_language(language):
    """Set language preference."""
    if language in current_app.config['LANGUAGES']:
        session['language'] = language
        session.permanent = True
        flash(f'Language changed to {language}', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

# News Management
@bp.route('/news')
@login_required
def news():
    """News management page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    status = request.args.get('status', 'all')
    search = request.args.get('search', '')

    query = News.query

    if status != 'all':
        query = query.filter_by(status=status)

    if search:
        query = query.filter(
            db.or_(
                News.title_en.contains(search),
                News.title_ar.contains(search),
                News.content_en.contains(search),
                News.content_ar.contains(search)
            )
        )

    news_items = query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/news.html',
                         news_items=news_items,
                         current_status=status,
                         current_search=search)

@bp.route('/news/new', methods=['GET', 'POST'])
@editor_required
def news_new():
    """Create new news article."""
    form = NewsForm()

    if form.validate_on_submit():
        # Debug: Print form data
        print(f"DEBUG: Featured checkbox value: {form.featured.data}")
        print(f"DEBUG: Show on homepage checkbox value: {form.show_on_homepage.data}")
        print(f"DEBUG: Raw form data: featured={request.form.get('featured')}, show_on_homepage={request.form.get('show_on_homepage')}")

        # Handle action buttons (save_draft or publish)
        action = request.form.get('action', 'save')

        # Set status based on action
        if action == 'save_draft':
            status = 'draft'
            publish_at = form.publish_at.data
        elif action == 'publish':
            status = 'published'
            # Set publish date if not set
            if not form.publish_at.data:
                publish_at = datetime.utcnow()
            else:
                publish_at = form.publish_at.data
        else:
            status = form.status.data
            publish_at = form.publish_at.data

        news_item = News(
            title_en=form.title_en.data,
            title_ar=form.title_ar.data,
            slug=form.slug.data,
            content_en=form.content_en.data,
            content_ar=form.content_ar.data,
            excerpt_en=form.excerpt_en.data,
            excerpt_ar=form.excerpt_ar.data,
            tags=form.tags.data,

            # Enhanced Keywords
            focus_keyword_en=form.focus_keyword_en.data,
            focus_keyword_ar=form.focus_keyword_ar.data,

            # Enhanced SEO
            seo_title_en=form.seo_title_en.data,
            seo_title_ar=form.seo_title_ar.data,
            seo_description_en=form.seo_description_en.data,
            seo_description_ar=form.seo_description_ar.data,

            # Open Graph
            og_title_en=form.og_title_en.data,
            og_title_ar=form.og_title_ar.data,
            og_description_en=form.og_description_en.data,
            og_description_ar=form.og_description_ar.data,

            # Twitter Card
            twitter_title_en=form.twitter_title_en.data,
            twitter_title_ar=form.twitter_title_ar.data,
            twitter_description_en=form.twitter_description_en.data,
            twitter_description_ar=form.twitter_description_ar.data,

            # Schema.org and Content Metadata
            article_type=form.article_type.data,
            estimated_reading_time=form.estimated_reading_time.data,
            content_difficulty=form.content_difficulty.data,

            # Publishing
            status=status,
            featured=form.featured.data,
            show_on_homepage=form.show_on_homepage.data,
            publish_at=publish_at
        )

        # Handle cover image upload
        if form.cover_image.data and hasattr(form.cover_image.data, 'filename') and form.cover_image.data.filename:
            filename = secure_filename(form.cover_image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'news', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.cover_image.data.save(upload_path)
            news_item.cover_image = filename

        db.session.add(news_item)
        db.session.commit()

        flash('News article created successfully.', 'success')
        return redirect(url_for('admin.news'))

    return render_template('admin/news_form.html', form=form, title='New News Article')

@bp.route('/news/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def news_edit(id):
    """Edit news article."""
    news_item = News.query.get_or_404(id)
    form = NewsForm(obj=news_item)

    if form.validate_on_submit():
        # Debug: Print form data
        print(f"DEBUG EDIT: Featured checkbox value: {form.featured.data}")
        print(f"DEBUG EDIT: Show on homepage checkbox value: {form.show_on_homepage.data}")
        print(f"DEBUG EDIT: Raw form data: featured={request.form.get('featured')}, show_on_homepage={request.form.get('show_on_homepage')}")

        # Basic Information
        news_item.title_en = form.title_en.data
        news_item.title_ar = form.title_ar.data
        news_item.slug = form.slug.data
        news_item.content_en = form.content_en.data
        news_item.content_ar = form.content_ar.data
        news_item.excerpt_en = form.excerpt_en.data
        news_item.excerpt_ar = form.excerpt_ar.data
        news_item.tags = form.tags.data

        # Enhanced Keywords
        news_item.focus_keyword_en = form.focus_keyword_en.data
        news_item.focus_keyword_ar = form.focus_keyword_ar.data

        # Enhanced SEO
        news_item.seo_title_en = form.seo_title_en.data
        news_item.seo_title_ar = form.seo_title_ar.data
        news_item.seo_description_en = form.seo_description_en.data
        news_item.seo_description_ar = form.seo_description_ar.data

        # Open Graph
        news_item.og_title_en = form.og_title_en.data
        news_item.og_title_ar = form.og_title_ar.data
        news_item.og_description_en = form.og_description_en.data
        news_item.og_description_ar = form.og_description_ar.data

        # Twitter Card
        news_item.twitter_title_en = form.twitter_title_en.data
        news_item.twitter_title_ar = form.twitter_title_ar.data
        news_item.twitter_description_en = form.twitter_description_en.data
        news_item.twitter_description_ar = form.twitter_description_ar.data

        # Schema.org and Content Metadata
        news_item.article_type = form.article_type.data
        news_item.estimated_reading_time = form.estimated_reading_time.data
        news_item.content_difficulty = form.content_difficulty.data

        # Publishing
        news_item.status = form.status.data
        news_item.featured = form.featured.data
        news_item.show_on_homepage = form.show_on_homepage.data
        news_item.publish_at = form.publish_at.data
        news_item.updated_at = datetime.utcnow()

        # Handle cover image upload
        if form.cover_image.data and hasattr(form.cover_image.data, 'filename') and form.cover_image.data.filename:
            filename = secure_filename(form.cover_image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'news', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.cover_image.data.save(upload_path)
            news_item.cover_image = filename

        db.session.commit()
        flash('News article updated successfully.', 'success')
        return redirect(url_for('admin.news'))

    return render_template('admin/news_form.html', form=form, news_item=news_item, title='Edit News Article')

@bp.route('/news/<int:id>/delete', methods=['POST'])
@admin_required
def news_delete(id):
    """Delete news article."""
    news_item = News.query.get_or_404(id)
    db.session.delete(news_item)
    db.session.commit()
    flash('News article deleted successfully.', 'success')
    return redirect(url_for('admin.news'))

# Gallery Management
@bp.route('/gallery')
@login_required
def gallery():
    """Gallery management page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    gallery_items = Gallery.query.order_by(Gallery.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/gallery.html', gallery_items=gallery_items)

@bp.route('/gallery/new', methods=['GET', 'POST'])
@editor_required
def gallery_new():
    """Upload new gallery image."""
    form = GalleryForm()

    # Extend category choices with any existing categories found in DB (keep fixed first)
    try:
        existing = db.session.query(Gallery.category).distinct().all()
        existing_cats = [c[0] for c in existing if c[0]]
    except Exception:
        existing_cats = []
    default_keys = ['farms','packing','storage','exports']
    defaults = [('farms','Farms'),('packing','Packing Houses'),('storage','Cold Storage'),('exports','Exports')]
    extras = [(c, c) for c in sorted(existing_cats) if c not in default_keys]
    form.category.choices = defaults + extras

    if form.validate_on_submit():
        # Allow admin to add a new custom category on the fly while preserving fixed options
        selected_category = form.category.data
        if form.new_category.data:
            selected_category = form.new_category.data.strip()
            # Persist metadata for category with optional Arabic name and icon
            icon = request.form.get('new_category_icon', 'fa-tags').strip() or 'fa-tags'
            key = selected_category.lower().replace(' ', '-')[:50]
            name_ar = (form.new_category_ar.data or selected_category).strip()
            existing = GalleryCategory.query.filter_by(key=key).first()
            if not existing:
                db.session.add(GalleryCategory(key=key, name_en=selected_category.title(), name_ar=name_ar, icon_class=icon, is_active=True))
            else:
                # Update Arabic name/icon if provided
                updated = False
                if form.new_category_ar.data:
                    existing.name_ar = name_ar; updated = True
                if icon:
                    existing.icon_class = icon; updated = True
                if updated:
                    db.session.add(existing)
            selected_category = key

        gallery_item = Gallery(
            title_en=form.title_en.data,
            title_ar=form.title_ar.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            category=selected_category
        )

        # Handle image upload
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename

            upload_path = os.path.join(current_app.instance_path,
                                     current_app.config['UPLOAD_FOLDER'],
                                     'gallery', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)
            gallery_item.image_path = filename

        db.session.add(gallery_item)
        db.session.commit()

        flash('Gallery image uploaded successfully.', 'success')
        return redirect(url_for('admin.gallery'))


    # GET request: render form with custom categories list for deletion section
    try:
        custom_cats = GalleryCategory.query.filter_by(is_active=True).order_by(GalleryCategory.sort_order).all()
    except Exception:
        custom_cats = []
    return render_template('admin/gallery_form.html', form=form, title='Upload New Image', custom_cats=custom_cats)

@bp.route('/gallery/category/delete', methods=['POST'])
@editor_required
def gallery_category_delete():
    """Delete a gallery category and ALL its images (always cascade)."""
    key = request.form.get('key', '').strip()
    if not key:
        return jsonify({'ok': False, 'error': 'Missing key'}), 400

    # Always cascade delete images then metadata
    images = Gallery.query.filter_by(category=key).all()
    for img in images:
        try:
            if img.image_path:
                upload_path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'gallery', img.image_path)
                if os.path.exists(upload_path):
                    os.remove(upload_path)
        except Exception:
            pass
        db.session.delete(img)

    cat = GalleryCategory.query.filter_by(key=key).first()
    if cat:
        db.session.delete(cat)

    db.session.commit()
    return jsonify({'ok': True, 'deleted_images': len(images)})

@bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def gallery_edit(id):
    """Use the same form and template as creation, with minor differences (image optional)."""
    item = Gallery.query.get_or_404(id)
    form = GalleryForm(obj=item)

    # Extend category choices similar to gallery_new
    try:
        existing = db.session.query(Gallery.category).distinct().all()
        existing_cats = [c[0] for c in existing if c[0]]
    except Exception:
        existing_cats = []
    default_keys = ['farms','packing','storage','exports']
    defaults = [('farms','Farms'),('packing','Packing Houses'),('storage','Cold Storage'),('exports','Exports')]
    extras = [(c, c) for c in sorted(existing_cats) if c not in default_keys]
    form.category.choices = defaults + extras

    # In edit mode, image upload should be optional (unlike creation)
    try:
        from wtforms.validators import Optional as WTOptional
        form.image.validators = [WTOptional()]
    except Exception:
        form.image.validators = []

    if form.validate_on_submit():
        item.title_en = form.title_en.data or item.title_en
        item.title_ar = form.title_ar.data or item.title_ar
        item.description_en = form.description_en.data or item.description_en
        item.description_ar = form.description_ar.data or item.description_ar

        # Allow changing/creating category like in gallery_new
        selected_category = form.category.data or item.category
        if form.new_category.data:
            selected_category = form.new_category.data.strip()
            icon = request.form.get('new_category_icon', 'fa-tags').strip() or 'fa-tags'
            key = selected_category.lower().replace(' ', '-')[:50]
            name_ar = (form.new_category_ar.data or selected_category).strip()
            existing_meta = GalleryCategory.query.filter_by(key=key).first()
            if not existing_meta:
                db.session.add(GalleryCategory(key=key, name_en=selected_category.title(), name_ar=name_ar, icon_class=icon, is_active=True))
            else:
                updated = False
                if form.new_category_ar.data:
                    existing_meta.name_ar = name_ar; updated = True
                if icon:
                    existing_meta.icon_class = icon; updated = True
                if updated:
                    db.session.add(existing_meta)
            selected_category = key
        item.category = selected_category

        item.sort_order = form.sort_order.data if form.sort_order.data is not None else item.sort_order
        item.is_active = form.is_active.data

        # handle replacing image (optional)
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            try:
                if item.image_path:
                    old_path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'gallery', item.image_path)
                    if os.path.exists(old_path):
                        os.remove(old_path)
            except Exception:
                pass
            filename = secure_filename(form.image.data.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            upload_path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'gallery', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            form.image.data.save(upload_path)
            item.image_path = filename

        db.session.commit()
        flash('Gallery image updated successfully.', 'success')
        return redirect(url_for('admin.gallery'))

    # Reuse the same template as "new" but change the title
    try:
        custom_cats = GalleryCategory.query.filter_by(is_active=True).order_by(GalleryCategory.sort_order).all()
    except Exception:
        custom_cats = []
    return render_template('admin/gallery_form.html', form=form, title='Edit Gallery Image', custom_cats=custom_cats)

    # Allow deleting any category key, including previously default ones

    if cascade:
        # delete all images in this category (DB + files)
        images = Gallery.query.filter_by(category=key).all()
        for img in images:
            # try remove file
            try:
                if img.image_path:
                    upload_path = os.path.join(current_app.instance_path, current_app.config['UPLOAD_FOLDER'], 'gallery', img.image_path)
                    if os.path.exists(upload_path):
                        os.remove(upload_path)
            except Exception:
                pass
            db.session.delete(img)
        # delete metadata if exists
        cat = GalleryCategory.query.filter_by(key=key).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()
        return jsonify({'ok': True, 'deleted_images': len(images)})
    else:
        used = Gallery.query.filter_by(category=key).count()
        if used > 0:
            return jsonify({'ok': False, 'error': 'Category is used by gallery items'}), 400
        cat = GalleryCategory.query.filter_by(key=key).first()
        if cat:
            db.session.delete(cat)
            db.session.commit()
        return jsonify({'ok': True})

    # Load custom categories (metadata) to allow deletion in UI
    try:
        custom_cats = GalleryCategory.query.filter_by(is_active=True).order_by(GalleryCategory.sort_order).all()
    except Exception:
        custom_cats = []
    return render_template('admin/gallery_form.html', form=form, title='Upload New Image', custom_cats=custom_cats)

@bp.route('/gallery/<int:id>/delete', methods=['POST'])
@admin_required
def gallery_delete(id):
    """Delete gallery image."""
    gallery_item = Gallery.query.get_or_404(id)
    db.session.delete(gallery_item)
    db.session.commit()
    flash('Gallery image deleted successfully.', 'success')
    return redirect(url_for('admin.gallery'))

# Services Management
@bp.route('/services')
@login_required
def services():
    """Services management page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    services_items = Service.query.order_by(Service.sort_order).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/services.html', services_items=services_items)

@bp.route('/services/new', methods=['GET', 'POST'])
@editor_required
def services_new():
    """Create new service."""
    form = ServiceForm()

    if form.validate_on_submit():
        service = Service(
            title_en=form.title_en.data,
            title_ar=form.title_ar.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            icon=form.icon.data,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data
        )

        db.session.add(service)
        db.session.commit()

        flash('Service created successfully.', 'success')
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', form=form, title='New Service')

@bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def services_edit(id):
    """Edit service."""
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)

    if form.validate_on_submit():
        service.title_en = form.title_en.data
        service.title_ar = form.title_ar.data
        service.description_en = form.description_en.data
        service.description_ar = form.description_ar.data
        service.icon = form.icon.data
        service.sort_order = form.sort_order.data
        service.is_active = form.is_active.data

        db.session.commit()
        flash('Service updated successfully.', 'success')
        return redirect(url_for('admin.services'))

    return render_template('admin/service_form.html', form=form, service=service, title='Edit Service')

@bp.route('/services/<int:id>/delete', methods=['POST'])
@admin_required
def services_delete(id):
    """Delete service."""
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully.', 'success')
    return redirect(url_for('admin.services'))

# Certifications Management
@bp.route('/certifications')
@login_required
def certifications():
    """Certifications management page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    # For now, we'll use a simple list since we don't have a Certification model
    # You can create one later if needed
    certifications_data = [
        {'id': 1, 'name': 'ISO 9001:2015', 'description': 'Quality Management System', 'status': 'active'},
        {'id': 2, 'name': 'ISO 14001:2015', 'description': 'Environmental Management System', 'status': 'active'},
        {'id': 3, 'name': 'OHSAS 18001', 'description': 'Occupational Health and Safety', 'status': 'active'},
    ]

    return render_template('admin/certifications.html', certifications=certifications_data)

# Users Management
@bp.route('/users')
@admin_required
def users():
    """Users management page."""
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1

    users_list = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users.html', users_list=users_list)

@bp.route('/users/new', methods=['GET', 'POST'])
@admin_required
def users_new():
    """Create new user."""
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('User created successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', form=form, title='New User')

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def users_edit(id):
    """Edit user."""
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.role = form.role.data
        user.is_active = form.is_active.data

        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', form=form, user=user, title='Edit User')

# Reports
@bp.route('/reports')
@login_required
def reports():
    """Reports page."""
    # Calculate statistics
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_rfqs = RFQ.query.count()
    pending_rfqs = RFQ.query.filter_by(status='new').count()
    total_news = News.query.count()
    published_news = News.query.filter_by(status='published').count()
    total_users = User.query.count()

    # Recent activity
    recent_rfqs = RFQ.query.order_by(RFQ.created_at.desc()).limit(10).all()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()

    stats = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_rfqs': total_rfqs,
        'pending_rfqs': pending_rfqs,
        'total_news': total_news,
        'published_news': published_news,
        'total_users': total_users,
        'recent_rfqs': recent_rfqs,
        'recent_products': recent_products
    }

    return render_template('admin/reports.html', stats=stats)

# Reports Data API for charts
@bp.route('/reports/data')
@login_required
def reports_data():
    """Return JSON data for reports charts based on metric and date range.
    Query params:
      - metric: one of [rfq_trend, rfq_status, products_by_category]
      - start: YYYY-MM-DD (optional, default last 30 days)
      - end: YYYY-MM-DD (optional)
    """
    from datetime import timedelta, date
    metric = request.args.get('metric', 'rfq_trend')
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    def parse_date(s):
        if not s:
            return None
        try:
            return datetime.strptime(s, '%Y-%m-%d').date()
        except Exception:
            return None

    # Default to last 30 days (inclusive)
    today = datetime.utcnow().date()
    start_date = parse_date(start_str) or (today - timedelta(days=29))
    end_date = parse_date(end_str) or today

    # Normalize to datetimes for querying
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    if metric == 'rfq_trend':
        # Count RFQs per day in range
        rfqs = RFQ.query.filter(RFQ.created_at >= start_dt, RFQ.created_at <= end_dt).all()
        def build_series(start_d, end_d, rfqs_list):
            rfq_by_day = {}
            for r in rfqs_list:
                if not r.created_at:
                    continue
                d = r.created_at.date()
                rfq_by_day[d] = rfq_by_day.get(d, 0) + 1
            days_local = []
            counts_local = []
            cur = start_d
            while cur <= end_d:
                days_local.append(cur.isoformat())
                counts_local.append(rfq_by_day.get(cur, 0))
                cur = cur + timedelta(days=1)
            return days_local, counts_local
        days, counts = build_series(start_date, end_date, rfqs)
        # Fallback: if default range and no data, expand to all-time (capped to 365 days)
        if (sum(counts) == 0) and (not start_str and not end_str):
            first = RFQ.query.order_by(RFQ.created_at.asc()).first()
            if first and first.created_at:
                fb_start = first.created_at.date()
                if (end_date - fb_start).days > 365:
                    fb_start = end_date - timedelta(days=365)
                fb_start_dt = datetime.combine(fb_start, datetime.min.time())
                fb_end_dt = datetime.combine(end_date, datetime.max.time())
                rfqs_fb = RFQ.query.filter(RFQ.created_at >= fb_start_dt, RFQ.created_at <= fb_end_dt).all()
                days, counts = build_series(fb_start, end_date, rfqs_fb)
        return jsonify({
            'metric': 'rfq_trend',
            'labels': days,
            'datasets': [{
                'label': _t('RFQs'),
                'data': counts
            }]
        })

    if metric == 'rfq_status':
        # Distribution of RFQ statuses within range
        rfqs = RFQ.query.filter(RFQ.created_at >= start_dt, RFQ.created_at <= end_dt).all()
        status_defs = [
            ('new', 'New'),
            ('in_review', 'In Review'),
            ('quoted', 'Quoted'),
            ('closed', 'Closed'),
            ('cancelled', 'Cancelled')
        ]
        counts = {code: 0 for code, _ in status_defs}
        for r in rfqs:
            if r.status not in counts:
                counts[r.status] = counts.get(r.status, 0) + 1
            else:
                counts[r.status] += 1
        labels = [_t(label) for code, label in status_defs]
        values = [counts.get(code, 0) for code, label in status_defs]
        # Fallback: if default range and no data, compute all-time distribution
        if (sum(values) == 0) and (not start_str and not end_str):
            counts = {code: 0 for code, _ in status_defs}
            for r in RFQ.query.all():
                if r.status not in counts:
                    counts[r.status] = counts.get(r.status, 0) + 1
                else:
                    counts[r.status] += 1
            values = [counts.get(code, 0) for code, label in status_defs]
        return jsonify({
            'metric': 'rfq_status',
            'labels': labels,
            'datasets': [{
                'label': _t('RFQ Status'),
                'data': values
            }]
        })

    if metric == 'products_by_category':
        # Count products by category created in range with localized category names
        from sqlalchemy import func
        lang = session.get('language', 'en')
        q = db.session.query(Category, func.count(Product.id)) \
            .join(Product, Product.category_id == Category.id) \
            .group_by(Category.id) \
            .order_by(func.count(Product.id).desc())
        rows = q.all()
        # Localize labels via manual translations if available
        labels = [_(c.get_name(lang) or c.get_name('en')) for c, cnt in rows]
        values = [cnt for c, cnt in rows]
        # Fallback: if no data in selected range, show all-time top categories
        if sum(values) == 0:
            q_all = db.session.query(Category, func.count(Product.id)) \
                .join(Product, Product.category_id == Category.id) \
                .group_by(Category.id) \
                .order_by(func.count(Product.id).desc())
            rows_all = q_all.all()
            labels = [_(c.get_name(lang)) for c, cnt in rows_all]
            values = [cnt for c, cnt in rows_all]
        # Include Uncategorized bucket (products without category)
        from sqlalchemy import func
        uncat_count = db.session.query(func.count(Product.id)).filter(Product.category_id == None).scalar()
        if uncat_count and uncat_count > 0:
            labels.append(_('Uncategorized'))
            values.append(uncat_count)
        return jsonify({
            'metric': 'products_by_category',
            'labels': labels,
            'datasets': [{
                'label': _t('Products'),
                'data': values
            }]
        })

    return jsonify({'error': 'unknown metric'}), 400


# Reports RFQs list (JSON)
@bp.route('/reports/rfqs')
@login_required
def reports_rfqs():
    """Return list of RFQs filtered by date range and optional status.
    Query params: start, end (YYYY-MM-DD), status (optional), limit (default 200)
    """
    from datetime import timedelta
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    status = request.args.get('status')
    try:
        limit = min(int(request.args.get('limit', 200)), 1000)
    except Exception:
        limit = 200

    def parse_date(s):
        if not s:
            return None
        try:
            return datetime.strptime(s, '%Y-%m-%d').date()
        except Exception:
            return None

    today = datetime.utcnow().date()
    start_date = parse_date(start_str) or (today - timedelta(days=29))
    end_date = parse_date(end_str) or today
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    q = RFQ.query.filter(RFQ.created_at >= start_dt, RFQ.created_at <= end_dt)
    if status:
        q = q.filter(RFQ.status == status)

    rfqs = q.order_by(RFQ.created_at.desc()).limit(limit).all()
    data = []
    for r in rfqs:
        data.append({
            'id': r.id,
            'name': r.name,
            'company': r.company,
            'country': r.country,
            'status': r.status,
            'priority': r.priority,
            'product_name': r.product_name,
            'category_key': r.category_key,
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else None
        })
    return jsonify({'items': data, 'count': len(data)})


# Reports export (CSV)
@bp.route('/reports/export')
@login_required
def reports_export():
    """Export reports data as CSV. Supported types: rfqs"""
    export_type = request.args.get('type', 'rfqs')
    if export_type == 'rfqs':
        # Reuse same filters as reports_rfqs
        start = request.args.get('start')
        end = request.args.get('end')
        status = request.args.get('status')
        request_args = request.args.to_dict(flat=True)
        # Get JSON list via function to avoid duplicating logic
        with current_app.test_request_context(f"/admin/reports/rfqs?start={start or ''}&end={end or ''}&status={status or ''}&limit=1000"):
            resp = reports_rfqs()
        rfqs_json = resp.get_json().get('items', [])

        # Build CSV
        import csv
        from io import StringIO
        output = StringIO()
        writer = csv.writer(output)
        headers = ['ID', 'Name', 'Company', 'Country', 'Status', 'Priority', 'Product', 'Category', 'Created At']
        writer.writerow(headers)
        for it in rfqs_json:
            writer.writerow([
                it.get('id'), it.get('name'), it.get('company') or '', it.get('country') or '',
                it.get('status'), it.get('priority'), it.get('product_name') or '', it.get('category_key') or '',
                it.get('created_at') or ''
            ])
        csv_text = output.getvalue()
        filename = f"rfqs_{(start or 'start')}_{(end or 'end')}.csv"
        return Response(
            csv_text,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )

    return jsonify({'error': 'unsupported export type'}), 400


# Settings
@bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Settings page."""
    if request.method == 'POST':
        # Handle settings update
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    # Get current settings from CompanyInfo
    company_info = CompanyInfo.query.first()

    return render_template('admin/settings.html', company_info=company_info)

@bp.route('/upload-editor-image', methods=['POST'])
@login_required
def upload_editor_image():
    """Upload image for Summernote editor."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})

        # Check file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not ('.' in file.filename and
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'success': False, 'error': 'Invalid file type'})

        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{unique_id}_{filename}"

        # Save file
        upload_path = os.path.join(current_app.instance_path,
                                 current_app.config['UPLOAD_FOLDER'],
                                 'editor', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        # Return URL
        file_url = url_for('main.uploaded_file', filename=f'editor/{filename}')
        return jsonify({'success': True, 'url': file_url})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
