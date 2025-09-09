#!/usr/bin/env python3
"""
إعادة تسمية الصور لتطابق أسماء المنتجات الجديدة
"""

import os
import shutil
from pathlib import Path

def rename_product_images():
    """إعادة تسمية صور المنتجات"""
    
    # مسار مجلد الصور
    images_dir = Path("static/uploads/products")
    
    if not images_dir.exists():
        print(f"❌ مجلد الصور غير موجود: {images_dir}")
        return
    
    # قائمة الصور التي تحتاج إعادة تسمية
    rename_map = {
        'mandarins-emdad-global.webp': 'fresh-mandarins-emdad-global.webp',
        'oranges-emdad-global.webp': 'fresh-oranges-emdad-global.webp',
        'tangerines-emdad-global.webp': 'fresh-tangerines-emdad-global.webp',
        'strawberries-emdad-global.webp': 'fresh-strawberries-emdad-global.webp',
        'garlic-emdad-global.webp': 'garlic-white-emdad-global.webp',
        'onions-emdad-global.webp': 'onions-red-golden-emdad-global.webp',
        'potatoes-emdad-global.webp': 'potatoes-spunta-emdad-global.webp',
        'sweet-potatoes-emdad-global.webp': 'sweet-potatoes-beauregard-emdad-global.webp',
        'parsley-emdad-global.webp': 'parsley-flakes-emdad-global.webp',
        'sesame-seeds-emdad-global.webp': 'sesame-seed-emdad-global.webp'
    }
    
    print("🔄 إعادة تسمية صور المنتجات...")
    print("=" * 50)
    
    renamed_count = 0
    skipped_count = 0
    
    for old_name, new_name in rename_map.items():
        old_path = images_dir / old_name
        new_path = images_dir / new_name
        
        if old_path.exists():
            if new_path.exists():
                print(f"⚠️  الصورة الجديدة موجودة مسبقاً: {new_name}")
                skipped_count += 1
            else:
                try:
                    # نسخ الصورة بالاسم الجديد (أكثر أماناً من إعادة التسمية)
                    shutil.copy2(old_path, new_path)
                    print(f"✅ تم نسخ: {old_name} → {new_name}")
                    renamed_count += 1
                except Exception as e:
                    print(f"❌ خطأ في نسخ {old_name}: {e}")
        else:
            print(f"⚠️  الصورة الأصلية غير موجودة: {old_name}")
            skipped_count += 1
    
    print("\n" + "=" * 50)
    print(f"📊 النتائج:")
    print(f"   ✅ تم نسخ: {renamed_count} صورة")
    print(f"   ⚠️  تم تخطي: {skipped_count} صورة")
    
    if renamed_count > 0:
        print(f"\n💡 تم نسخ الصور بأسماء جديدة. يمكنك حذف الصور القديمة لاحقاً إذا أردت.")

def create_placeholder_images():
    """إنشاء صور placeholder للمنتجات الجديدة"""
    
    images_dir = Path("static/uploads/products")
    
    # قائمة الصور الجديدة المطلوبة
    new_images = [
        'fresh-spring-onions-emdad-global.webp',
        'fresh-pomegranates-emdad-global.webp',
        'fresh-grapes-emdad-global.webp',
        'fresh-mango-emdad-global.webp',
        'dates-pitted-emdad-global.webp',
        'medjool-dates-pitted-emdad-global.webp',
        'medjool-dates-whole-emdad-global.webp',
        'nigella-black-seed-emdad-global.webp',
        'oregano-emdad-global.webp',
        'thyme-emdad-global.webp'
    ]
    
    print("\n📸 التحقق من الصور الجديدة المطلوبة...")
    print("=" * 50)
    
    missing_images = []
    existing_images = []
    
    for image_name in new_images:
        image_path = images_dir / image_name
        if image_path.exists():
            existing_images.append(image_name)
            print(f"✅ موجودة: {image_name}")
        else:
            missing_images.append(image_name)
            print(f"❌ مفقودة: {image_name}")
    
    print(f"\n📊 إحصائيات الصور الجديدة:")
    print(f"   ✅ موجودة: {len(existing_images)}")
    print(f"   ❌ مفقودة: {len(missing_images)}")
    
    if missing_images:
        print(f"\n⚠️  تحتاج لرفع الصور التالية:")
        for image in missing_images:
            print(f"   📁 {image}")
        
        print(f"\n💡 يمكنك رفع هذه الصور في المجلد:")
        print(f"   📂 {images_dir.absolute()}")

def check_all_images():
    """التحقق من جميع صور المنتجات"""
    
    from app import create_app
    from app.models import Product
    
    app = create_app()
    with app.app_context():
        print("\n🔍 التحقق من صور جميع المنتجات...")
        print("=" * 50)
        
        products = Product.query.all()
        images_dir = Path("static/uploads/products")
        
        missing_images = []
        existing_images = []
        
        for product in products:
            if product.image_path:
                # استخراج اسم الملف من المسار الكامل
                filename = product.image_path.split('/')[-1] if '/' in product.image_path else product.image_path
                image_path = images_dir / filename
                if image_path.exists():
                    existing_images.append(filename)
                else:
                    missing_images.append({
                        'product': product.name_ar,
                        'filename': filename,
                        'slug': product.slug
                    })
        
        print(f"📊 إحصائيات شاملة:")
        print(f"   📦 إجمالي المنتجات: {len(products)}")
        print(f"   ✅ صور موجودة: {len(existing_images)}")
        print(f"   ❌ صور مفقودة: {len(missing_images)}")
        
        if missing_images:
            print(f"\n⚠️  المنتجات التي تحتاج صور:")
            for item in missing_images:
                print(f"   - {item['product']} → {item['filename']}")
        else:
            print(f"\n🎉 جميع المنتجات لديها صور!")

def cleanup_old_images():
    """تنظيف الصور القديمة (اختياري)"""
    
    images_dir = Path("static/uploads/products")
    
    # الصور القديمة التي يمكن حذفها بعد النسخ
    old_images = [
        'mandarins-emdad-global.webp',
        'oranges-emdad-global.webp', 
        'tangerines-emdad-global.webp',
        'strawberries-emdad-global.webp',
        'garlic-emdad-global.webp',
        'onions-emdad-global.webp',
        'potatoes-emdad-global.webp',
        'sweet-potatoes-emdad-global.webp',
        'parsley-emdad-global.webp',
        'sesame-seeds-emdad-global.webp'
    ]
    
    print("\n🗑️  تنظيف الصور القديمة...")
    print("=" * 50)
    print("⚠️  هذه العملية ستحذف الصور القديمة نهائياً!")
    
    response = input("هل تريد المتابعة؟ (y/N): ")
    
    if response.lower() == 'y':
        deleted_count = 0
        for image_name in old_images:
            image_path = images_dir / image_name
            if image_path.exists():
                try:
                    image_path.unlink()
                    print(f"🗑️  تم حذف: {image_name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"❌ خطأ في حذف {image_name}: {e}")
        
        print(f"\n✅ تم حذف {deleted_count} صورة قديمة")
    else:
        print("❌ تم إلغاء عملية التنظيف")

if __name__ == "__main__":
    print("🖼️  إدارة صور المنتجات")
    print("=" * 60)
    
    # إعادة تسمية الصور الموجودة
    rename_product_images()
    
    # التحقق من الصور الجديدة
    create_placeholder_images()
    
    # التحقق من جميع الصور
    check_all_images()
    
    # خيار تنظيف الصور القديمة
    print("\n" + "=" * 60)
    cleanup_old_images()
