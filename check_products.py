#!/usr/bin/env python3
"""Check products and their images in the database."""

from app import create_app
from app.models import Product, ProductImage, Category

app = create_app('development')
with app.app_context():
    products = Product.query.order_by(Product.category_id, Product.sort_order).all()
    print(f'Total products in database: {len(products)}')
    print()
    
    for p in products:
        cat = Category.query.get(p.category_id)
        main_image = p.get_main_image()
        print(f'Product: {p.slug}')
        print(f'  Category: {cat.key if cat else "None"}')
        print(f'  image_path: {p.image_path}')
        print(f'  main_image: {main_image.filename if main_image else "None"}')
        print(f'  total_images: {p.images.count()}')
        print()
