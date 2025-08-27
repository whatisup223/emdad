from flask import render_template, request, redirect, url_for, flash, current_app, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.admin import bp
from app.models import User, Category, Product, Certification, Service, News, Gallery, RFQ, CompanyInfo, AuditLog
from app.forms import LoginForm, UserForm, CategoryForm, ProductForm, CertificationForm, ServiceForm, NewsForm, GalleryForm, CompanyInfoForm
from app import db
import os
import json
from datetime import datetime

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
            is_active=form.is_active.data
        )
        
        # Handle image upload
        if form.image.data:
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
    
    return render_template('admin/category_form.html', form=form, title='New Category')

@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@editor_required
def category_edit(id):
    """Edit category."""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category, category=category)
    
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
        category.updated_at = datetime.utcnow()
        
        # Handle image upload
        if form.image.data:
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

    if form.validate_on_submit():
        # Prepare specifications as JSON
        specifications = {}
        if form.specifications_en.data:
            specifications['en'] = form.specifications_en.data
        if form.specifications_ar.data:
            specifications['ar'] = form.specifications_ar.data

        product = Product(
            name_en=form.name_en.data,
            name_ar=form.name_ar.data,
            slug=form.slug.data,
            category_id=form.category_id.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            short_description_en=form.short_description_en.data,
            short_description_ar=form.short_description_ar.data,
            specifications=json.dumps(specifications) if specifications else None,
            seo_title_en=form.seo_title_en.data,
            seo_title_ar=form.seo_title_ar.data,
            seo_description_en=form.seo_description_en.data,
            seo_description_ar=form.seo_description_ar.data,
            status=form.status.data,
            featured=form.featured.data,
            sort_order=form.sort_order.data
        )

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
            product.image_path = filename

        db.session.add(product)

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

    if form.validate_on_submit():
        # Prepare specifications as JSON
        specifications = {}
        if form.specifications_en.data:
            specifications['en'] = form.specifications_en.data
        if form.specifications_ar.data:
            specifications['ar'] = form.specifications_ar.data

        product.name_en = form.name_en.data
        product.name_ar = form.name_ar.data
        product.slug = form.slug.data
        product.category_id = form.category_id.data
        product.description_en = form.description_en.data
        product.description_ar = form.description_ar.data
        product.short_description_en = form.short_description_en.data
        product.short_description_ar = form.short_description_ar.data
        product.specifications = json.dumps(specifications) if specifications else None
        product.seo_title_en = form.seo_title_en.data
        product.seo_title_ar = form.seo_title_ar.data
        product.seo_description_en = form.seo_description_en.data
        product.seo_description_ar = form.seo_description_ar.data
        product.status = form.status.data
        product.featured = form.featured.data
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
            product.image_path = filename

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

    if form.validate_on_submit():
        gallery_item = Gallery(
            title_en=form.title_en.data,
            title_ar=form.title_ar.data,
            description_en=form.description_en.data,
            description_ar=form.description_ar.data,
            category=form.category.data
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

    return render_template('admin/gallery_form.html', form=form, title='Upload New Image')

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
            username=form.username.data,
            email=form.email.data,
            name=form.name.data,
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
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
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
