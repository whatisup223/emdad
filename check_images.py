#!/usr/bin/env python3
"""Check if product images exist in filesystem."""

import os
from app import create_app
from app.models import Product, ProductImage, Category

app = create_app('development')
with app.app_context():
    products = Product.query.order_by(Product.category_id, Product.sort_order).all()
    
    # Check both static and instance directories
    static_dir = os.path.join('static', 'uploads', 'products')
    instance_dir = os.path.join('instance', 'uploads', 'products')
    
    print(f'Total products in database: {len(products)}')
    print(f'Static directory: {static_dir}')
    print(f'Instance directory: {instance_dir}')
    print()
    
    missing_static = []
    missing_instance = []
    
    for p in products:
        cat = Category.query.filter_by(id=p.category_id).first()
        main_image = p.get_main_image()
        image_filename = main_image.filename if main_image else p.image_path
        
        if image_filename:
            static_path = os.path.join(static_dir, image_filename)
            instance_path = os.path.join(instance_dir, image_filename)
            
            static_exists = os.path.exists(static_path)
            instance_exists = os.path.exists(instance_path)
            
            print(f'Product: {p.slug}')
            print(f'  Category: {cat.key if cat else "None"}')
            print(f'  Image: {image_filename}')
            print(f'  Static exists: {static_exists}')
            print(f'  Instance exists: {instance_exists}')
            
            if not static_exists:
                missing_static.append((p.slug, image_filename))
            if not instance_exists:
                missing_instance.append((p.slug, image_filename))
            print()
    
    print(f'\nSummary:')
    print(f'Missing from static: {len(missing_static)}')
    print(f'Missing from instance: {len(missing_instance)}')
    
    if missing_static:
        print('\nMissing from static:')
        for slug, filename in missing_static:
            print(f'  {slug}: {filename}')
    
    if missing_instance:
        print('\nMissing from instance:')
        for slug, filename in missing_instance:
            print(f'  {slug}: {filename}')
