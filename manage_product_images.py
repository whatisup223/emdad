#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إدارة صور المنتجات - الحفاظ على الصور الموجودة وتحديد الصور المطلوبة للمنتجات الجديدة
"""

import shutil
from pathlib import Path
from app import create_app
from app.models import Product, db

def manage_product_images():
    """إدارة صور المنتجات بشكل صحيح"""
    
    app = create_app()
    with app.app_context():
        print("🖼️  إدارة صور المنتجات")
        print("=" * 60)
        
        # مسار مجلد الصور
        images_dir = Path("static/uploads/products")
        
        if not images_dir.exists():
            print("❌ مجلد الصور غير موجود!")
            return
        
        # الحصول على جميع المنتجات
        all_products = Product.query.all()
        
        print(f"📦 إجمالي المنتجات: {len(all_products)}")
        
        # تصنيف المنتجات
        products_with_images = []
        products_without_images = []
        
        for product in all_products:
            if product.image_path:
                # استخراج اسم الملف من المسار
                filename = product.image_path.split('/')[-1] if '/' in product.image_path else product.image_path
                image_file = images_dir / filename
                
                if image_file.exists():
                    products_with_images.append({
                        'product': product,
                        'filename': filename,
                        'status': 'موجودة'
                    })
                else:
                    products_with_images.append({
                        'product': product,
                        'filename': filename,
                        'status': 'مفقودة'
                    })
            else:
                products_without_images.append(product)
        
        # عرض النتائج
        print(f"\n📊 إحصائيات الصور:")
        print(f"   ✅ منتجات لها مسار صورة: {len(products_with_images)}")
        print(f"   ❌ منتجات بدون مسار صورة: {len(products_without_images)}")
        
        # عرض المنتجات التي لها صور موجودة
        existing_images = [p for p in products_with_images if p['status'] == 'موجودة']
        missing_images = [p for p in products_with_images if p['status'] == 'مفقودة']
        
        print(f"\n✅ منتجات لها صور موجودة ({len(existing_images)}):")
        for item in existing_images:
            print(f"   📁 {item['product'].name_ar} → {item['filename']}")
        
        if missing_images:
            print(f"\n⚠️  منتجات لها مسار صورة لكن الملف مفقود ({len(missing_images)}):")
            for item in missing_images:
                print(f"   ❌ {item['product'].name_ar} → {item['filename']}")
        
        # عرض المنتجات الجديدة التي تحتاج صور
        print(f"\n🆕 منتجات جديدة تحتاج صور ({len(products_without_images)}):")
        new_images_needed = []
        
        for product in products_without_images:
            expected_filename = f"{product.slug}-emdad-global.webp"
            new_images_needed.append({
                'product': product,
                'filename': expected_filename
            })
            print(f"   📸 {product.name_ar} → {expected_filename}")
        
        # إنشاء قائمة الصور المطلوبة للرفع
        print(f"\n📋 قائمة الصور المطلوبة للرفع:")
        print("=" * 60)
        
        if new_images_needed:
            print("🆕 صور جديدة مطلوبة:")
            for item in new_images_needed:
                print(f"   📁 {item['filename']}")
            
            print(f"\n💡 يرجى رفع هذه الصور ({len(new_images_needed)}) في المجلد:")
            print(f"   📂 {images_dir.absolute()}")
            
            # إنشاء ملف نصي بقائمة الصور المطلوبة
            required_images_file = Path("required_images.txt")
            with open(required_images_file, 'w', encoding='utf-8') as f:
                f.write("قائمة الصور المطلوبة للمنتجات الجديدة:\n")
                f.write("=" * 50 + "\n\n")
                for item in new_images_needed:
                    f.write(f"{item['filename']} - {item['product'].name_ar}\n")
            
            print(f"\n📄 تم إنشاء ملف قائمة الصور: {required_images_file.absolute()}")
        
        if missing_images:
            print(f"\n⚠️  صور مفقودة للمنتجات الموجودة:")
            for item in missing_images:
                print(f"   📁 {item['filename']}")
        
        return {
            'total_products': len(all_products),
            'products_with_images': len(existing_images),
            'products_missing_images': len(missing_images),
            'products_need_new_images': len(new_images_needed),
            'new_images_needed': new_images_needed
        }

def update_image_paths_after_upload():
    """تحديث مسارات الصور بعد رفع الصور الجديدة"""
    
    app = create_app()
    with app.app_context():
        print("\n🔄 تحديث مسارات الصور للمنتجات الجديدة...")
        print("=" * 60)
        
        # مسار مجلد الصور
        images_dir = Path("static/uploads/products")
        
        # البحث عن المنتجات بدون image_path
        products_without_path = Product.query.filter(Product.image_path.is_(None)).all()
        
        if not products_without_path:
            print("✅ جميع المنتجات لها مسارات صور")
            return
        
        print(f"📦 منتجات بدون مسار صورة: {len(products_without_path)}")
        
        updated_count = 0
        
        for product in products_without_path:
            expected_filename = f"{product.slug}-emdad-global.webp"
            image_file = images_dir / expected_filename
            
            if image_file.exists():
                # تحديث مسار الصورة
                product.image_path = f"static/uploads/products/{expected_filename}"
                updated_count += 1
                print(f"   ✅ تم تحديث مسار الصورة: {product.name_ar}")
            else:
                print(f"   ❌ الصورة غير موجودة: {product.name_ar} → {expected_filename}")
        
        if updated_count > 0:
            try:
                db.session.commit()
                print(f"\n✅ تم تحديث مسارات {updated_count} صورة بنجاح!")
            except Exception as e:
                db.session.rollback()
                print(f"❌ خطأ في حفظ التحديثات: {e}")
        else:
            print("\n⚠️  لم يتم تحديث أي مسارات صور")

if __name__ == "__main__":
    import sys

    # التحقق من المعاملات
    if len(sys.argv) > 1 and sys.argv[1] == "--update-paths":
        # تحديث مسارات الصور
        update_image_paths_after_upload()
    else:
        # إدارة الصور
        results = manage_product_images()

        print(f"\n📊 ملخص النتائج:")
        print(f"   📦 إجمالي المنتجات: {results['total_products']}")
        print(f"   ✅ منتجات لها صور: {results['products_with_images']}")
        print(f"   ⚠️  منتجات صورها مفقودة: {results['products_missing_images']}")
        print(f"   🆕 منتجات تحتاج صور جديدة: {results['products_need_new_images']}")

        if results['products_need_new_images'] > 0:
            print(f"\n🎯 الخطوة التالية:")
            print(f"   1. ارفع الصور المطلوبة ({results['products_need_new_images']}) في مجلد static/uploads/products")
            print(f"   2. شغل الأمر: python manage_product_images.py --update-paths")
            print(f"   3. تحقق من النتائج")
