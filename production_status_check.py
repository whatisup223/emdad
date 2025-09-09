#!/usr/bin/env python3
"""
🔍 Production Status Check
فحص سريع لحالة الإنتاج قبل وبعد التحديث
"""

from app import create_app
from app.models import Product, Category
from pathlib import Path

def check_production_status():
    """فحص حالة الإنتاج الحالية"""
    
    app = create_app()
    with app.app_context():
        print("🔍 فحص حالة الإنتاج...")
        print("=" * 50)
        
        # فحص الفئات
        categories = Category.query.all()
        print(f"📁 إجمالي الفئات: {len(categories)}")
        for cat in categories:
            product_count = Product.query.filter_by(category_id=cat.id).count()
            print(f"   📂 {cat.name_ar} ({cat.name_en}): {product_count} منتج")
        
        # فحص المنتجات
        products = Product.query.all()
        print(f"\n📦 إجمالي المنتجات: {len(products)}")
        
        # فحص الصور
        products_with_main_image = 0
        products_with_image_path = 0
        products_without_images = 0
        
        for product in products:
            main_image = product.get_main_image()
            has_main_image = main_image is not None
            has_image_path = product.image_path is not None
            
            if has_main_image:
                products_with_main_image += 1
            elif has_image_path:
                products_with_image_path += 1
            else:
                products_without_images += 1
        
        print(f"\n🖼️  حالة الصور:")
        print(f"   ✅ منتجات لها Main Image: {products_with_main_image}")
        print(f"   ✅ منتجات لها Image Path: {products_with_image_path}")
        print(f"   ❌ منتجات بدون صور: {products_without_images}")
        
        # فحص بيانات التوفر الشهري
        products_with_seasonality = 0
        for product in products:
            if product.seasonality:
                products_with_seasonality += 1
        
        print(f"\n📅 بيانات التوفر الشهري:")
        print(f"   ✅ منتجات لها بيانات: {products_with_seasonality}")
        print(f"   ❌ منتجات بدون بيانات: {len(products) - products_with_seasonality}")
        
        # فحص الملفات
        static_dir = Path("static/uploads/products")
        if static_dir.exists():
            webp_count = len(list(static_dir.glob("*.webp")))
            svg_count = len(list(static_dir.glob("*.svg")))
            print(f"\n📁 ملفات الصور:")
            print(f"   🖼️  صور WebP: {webp_count}")
            print(f"   🎨 صور SVG: {svg_count}")
        else:
            print(f"\n❌ مجلد الصور غير موجود: {static_dir}")
        
        # تحديد ما إذا كان التحديث مطلوب
        needs_update = False
        issues = []
        
        if len(categories) != 8:
            needs_update = True
            issues.append(f"عدد الفئات خاطئ: {len(categories)} بدلاً من 8")
        
        if len(products) < 38:
            needs_update = True
            issues.append(f"عدد المنتجات ناقص: {len(products)} بدلاً من 38")
        
        if products_without_images > 0:
            needs_update = True
            issues.append(f"منتجات بدون صور: {products_without_images}")
        
        if len(products) - products_with_seasonality > 0:
            needs_update = True
            issues.append(f"منتجات بدون بيانات توفر: {len(products) - products_with_seasonality}")
        
        print(f"\n🎯 التقييم النهائي:")
        if needs_update:
            print("❌ الإنتاج يحتاج تحديث")
            print("📋 المشاكل المكتشفة:")
            for issue in issues:
                print(f"   • {issue}")
            print(f"\n💡 الحل: تشغيل python deploy_production_update.py")
        else:
            print("✅ الإنتاج محدث ويعمل بشكل صحيح")
        
        return not needs_update

if __name__ == "__main__":
    try:
        success = check_production_status()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ خطأ في فحص الإنتاج: {e}")
        exit(1)
