#!/usr/bin/env python3
"""
فحص سريع للتأكد من أن جميع المنتجات لها صور تعمل
"""

from app import create_app
from app.models import Product
import os
from pathlib import Path

def verify_images():
    app = create_app()
    with app.app_context():
        print('🔍 فحص صور جميع المنتجات...')
        print('=' * 50)
        
        products = Product.query.all()
        
        products_with_main_image = 0
        products_with_image_path = 0
        products_without_images = 0
        
        # مسار مجلد الصور
        static_dir = Path(app.root_path) / 'static' / 'uploads' / 'products'
        instance_dir = Path(app.instance_path) / 'uploads' / 'products'
        
        print(f'📁 مجلد الصور الثابتة: {static_dir}')
        print(f'📁 مجلد الصور المرفوعة: {instance_dir}')
        print()
        
        for product in products:
            main_image = product.get_main_image()
            has_main_image = main_image is not None
            has_image_path = product.image_path is not None
            
            if has_main_image:
                # تحقق من وجود الملف
                image_file = instance_dir / main_image.filename
                file_exists = image_file.exists()
                products_with_main_image += 1
                status = f'✅ Main Image {"(موجود)" if file_exists else "(مفقود)"}'
                
            elif has_image_path:
                # تحقق من وجود الملف
                # image_path يحتوي على "static/uploads/products/filename.webp"
                relative_path = product.image_path.replace('static/', '')
                image_file = Path(app.root_path) / 'static' / relative_path
                file_exists = image_file.exists()
                products_with_image_path += 1
                status = f'✅ Image Path {"(موجود)" if file_exists else "(مفقود)"}'

                # إذا لم توجد في static، تحقق من instance
                if not file_exists:
                    filename = Path(product.image_path).name
                    instance_file = instance_dir / filename
                    if instance_file.exists():
                        file_exists = True
                        status = f'✅ Image Path (في instance)'
                
            else:
                products_without_images += 1
                status = '❌ No Image'
                file_exists = False
            
            # عرض النتيجة
            emoji = '✅' if (has_main_image or has_image_path) else '❌'
            print(f'{emoji} {product.name_ar} | {product.slug} | {status}')
        
        print(f'\n📊 ملخص الصور:')
        print(f'   ✅ منتجات لها Main Image: {products_with_main_image}')
        print(f'   ✅ منتجات لها Image Path: {products_with_image_path}')
        print(f'   ❌ منتجات بدون صور: {products_without_images}')
        print(f'   📦 إجمالي المنتجات: {len(products)}')
        
        if products_without_images == 0:
            print('\n🎉 جميع المنتجات لها صور!')
            return True
        else:
            print('\n⚠️  بعض المنتجات تحتاج صور')
            return False

if __name__ == "__main__":
    success = verify_images()
    exit(0 if success else 1)
