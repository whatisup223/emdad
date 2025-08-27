from flask import jsonify, request
from app.api import bp
from app.models import Category, Product

@bp.route('/categories')
def api_categories():
    """Get all active categories."""
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return jsonify([{
        'id': cat.id,
        'key': cat.key,
        'name_en': cat.name_en,
        'name_ar': cat.name_ar,
        'slug': cat.slug
    } for cat in categories])

@bp.route('/products')
def api_products():
    """Get products with optional category filter."""
    category_key = request.args.get('category')
    
    query = Product.query.filter_by(status='active')
    
    if category_key:
        category = Category.query.filter_by(key=category_key, is_active=True).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    products = query.order_by(Product.sort_order, Product.name_en).all()
    
    return jsonify([{
        'id': product.id,
        'name_en': product.name_en,
        'name_ar': product.name_ar,
        'slug': product.slug,
        'category_key': product.category.key if product.category else None
    } for product in products])

@bp.route('/products/<slug>')
def api_product_detail(slug):
    """Get product details."""
    product = Product.query.filter_by(slug=slug, status='active').first()
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify({
        'id': product.id,
        'name_en': product.name_en,
        'name_ar': product.name_ar,
        'slug': product.slug,
        'description_en': product.description_en,
        'description_ar': product.description_ar,
        'category': {
            'key': product.category.key,
            'name_en': product.category.name_en,
            'name_ar': product.category.name_ar
        } if product.category else None,
        'specifications': product.get_specifications(),
        'seasonality': product.get_seasonality(),
        'packaging_options': product.get_packaging_options()
    })
