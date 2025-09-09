#!/usr/bin/env python3
"""
التحقق من النتائج النهائية للتحديث
"""

from app import create_app
from app.models import Category, Product, db
from pathlib import Path
import json

def check_categories():
    """التحقق من الفئات"""
    print("📁 التحقق من الفئات...")
    
    app = create_app()
    with app.app_context():
        categories = Category.query.all()
        
        expected_categories = [
            {'id': 1, 'name_en': 'Fresh Citrus', 'name_ar': 'حمضيات طازجة'},
            {'id': 2, 'name_en': 'Fresh Vegetables', 'name_ar': 'خضروات طازجة'},
            {'id': 3, 'name_en': 'Fresh Fruit', 'name_ar': 'فواكه طازجة'},
            {'id': 4, 'name_en': 'Dates', 'name_ar': 'تمور'},
            {'id': 5, 'name_en': 'IQF', 'name_ar': 'مجمدة سريعاً'},
            {'id': 6, 'name_en': 'Spices', 'name_ar': 'توابل'},
            {'id': 7, 'name_en': 'Herbs & Herbal Plants', 'name_ar': 'أعشاب ونباتات عشبية'},
            {'id': 8, 'name_en': 'Oil Seeds', 'name_ar': 'بذور زيتية'}
        ]
        
        print(f"   📊 إجمالي الفئات: {len(categories)}")
        print(f"   🎯 المتوقع: {len(expected_categories)}")
        
        success = True
        for expected in expected_categories:
            category = Category.query.get(expected['id'])
            if category:
                if category.name_en == expected['name_en'] and category.name_ar == expected['name_ar']:
                    print(f"   ✅ {expected['name_ar']}")
                else:
                    print(f"   ⚠️  {expected['name_ar']} - أسماء غير متطابقة")
                    success = False
            else:
                print(f"   ❌ فئة مفقودة: {expected['name_ar']}")
                success = False
        
        return success

def check_products():
    """التحقق من المنتجات"""
    print("\n📦 التحقق من المنتجات...")
    
    app = create_app()
    with app.app_context():
        products = Product.query.all()
        
        # العدد المتوقع للمنتجات في كل فئة
        expected_counts = {
            1: 3,  # Fresh Citrus
            2: 5,  # Fresh Vegetables  
            3: 4,  # Fresh Fruit
            4: 4,  # Dates
            5: 2,  # IQF
            6: 6,  # Spices
            7: 12, # Herbs & Herbal Plants
            8: 2   # Oil Seeds
        }
        
        total_expected = sum(expected_counts.values())
        
        print(f"   📊 إجمالي المنتجات: {len(products)}")
        print(f"   🎯 المتوقع: {total_expected}")
        
        success = True
        for category_id, expected_count in expected_counts.items():
            actual_count = Product.query.filter_by(category_id=category_id).count()
            category = Category.query.get(category_id)
            category_name = category.name_ar if category else f"فئة {category_id}"
            
            if actual_count == expected_count:
                print(f"   ✅ {category_name}: {actual_count} منتج")
            else:
                print(f"   ⚠️  {category_name}: {actual_count} منتج (متوقع: {expected_count})")
                success = False
        
        # التحقق من المنتجات بدون فئة
        orphan_products = Product.query.filter_by(category_id=None).count()
        if orphan_products > 0:
            print(f"   ❌ منتجات بدون فئة: {orphan_products}")
            success = False
        else:
            print(f"   ✅ جميع المنتجات مصنفة")
        
        return success and len(products) == total_expected

def check_images():
    """التحقق من الصور"""
    print("\n🖼️  التحقق من الصور...")
    
    app = create_app()
    with app.app_context():
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
                        'filename': filename
                    })
        
        print(f"   📊 إجمالي المنتجات: {len(products)}")
        print(f"   ✅ صور موجودة: {len(existing_images)}")
        print(f"   ❌ صور مفقودة: {len(missing_images)}")
        
        if missing_images:
            print(f"   ⚠️  المنتجات التي تحتاج صور:")
            for item in missing_images:
                print(f"      - {item['product']} → {item['filename']}")
        
        return len(missing_images) == 0

def check_seasonal_data():
    """التحقق من بيانات التوفر الشهري"""
    print("\n📅 التحقق من بيانات التوفر الشهري...")
    
    app = create_app()
    with app.app_context():
        total_products = Product.query.count()
        products_with_seasons = Product.query.filter(Product.seasonality.isnot(None)).count()
        products_without_seasons = total_products - products_with_seasons

        print(f"   📊 إجمالي المنتجات: {total_products}")
        print(f"   ✅ منتجات لها بيانات توفر: {products_with_seasons}")
        print(f"   ❌ منتجات بدون بيانات توفر: {products_without_seasons}")

        if products_without_seasons > 0:
            products_no_season = Product.query.filter(Product.seasonality.is_(None)).all()
            print(f"   ⚠️  المنتجات بدون بيانات توفر:")
            for product in products_no_season:
                print(f"      - {product.name_ar}")
        
        return products_without_seasons == 0

def check_slugs():
    """التحقق من slugs المنتجات"""
    print("\n🔗 التحقق من slugs المنتجات...")
    
    app = create_app()
    with app.app_context():
        products = Product.query.all()
        
        duplicate_slugs = []
        empty_slugs = []
        valid_slugs = []
        
        slugs_seen = set()
        
        for product in products:
            if not product.slug:
                empty_slugs.append(product.name_ar)
            elif product.slug in slugs_seen:
                duplicate_slugs.append(product.slug)
            else:
                slugs_seen.add(product.slug)
                valid_slugs.append(product.slug)
        
        print(f"   📊 إجمالي المنتجات: {len(products)}")
        print(f"   ✅ slugs صحيحة: {len(valid_slugs)}")
        print(f"   ❌ slugs فارغة: {len(empty_slugs)}")
        print(f"   ❌ slugs مكررة: {len(duplicate_slugs)}")
        
        if empty_slugs:
            print(f"   ⚠️  منتجات بدون slugs:")
            for name in empty_slugs:
                print(f"      - {name}")
        
        if duplicate_slugs:
            print(f"   ⚠️  slugs مكررة:")
            for slug in duplicate_slugs:
                print(f"      - {slug}")
        
        return len(empty_slugs) == 0 and len(duplicate_slugs) == 0

def generate_final_report():
    """إنشاء تقرير نهائي"""
    print("\n📋 التقرير النهائي:")
    print("=" * 60)
    
    app = create_app()
    with app.app_context():
        # إحصائيات عامة
        total_categories = Category.query.count()
        total_products = Product.query.count()
        products_with_seasons = Product.query.filter(Product.seasonality.isnot(None)).count()
        
        print(f"📊 الإحصائيات العامة:")
        print(f"   📁 إجمالي الفئات: {total_categories}")
        print(f"   📦 إجمالي المنتجات: {total_products}")
        print(f"   📅 منتجات لها بيانات توفر: {products_with_seasons}")
        
        # تفاصيل الفئات
        print(f"\n📁 تفاصيل الفئات:")
        categories = Category.query.all()
        for category in categories:
            product_count = Product.query.filter_by(category_id=category.id).count()
            print(f"   {category.name_ar}: {product_count} منتج")
        
        # حالة الصور
        images_dir = Path("static/uploads/products")
        if images_dir.exists():
            image_files = list(images_dir.glob("*.webp"))
            print(f"\n🖼️  حالة الصور:")
            print(f"   📁 ملفات WebP في المجلد: {len(image_files)}")
        
        print(f"\n🎯 النتيجة:")
        if total_categories == 8 and total_products >= 38 and products_with_seasons == total_products:
            print(f"   🎉 التحديث مكتمل بنجاح!")
            print(f"   ✅ النظام جاهز للاستخدام")
        else:
            print(f"   ⚠️  التحديث مكتمل جزئياً - راجع التفاصيل أعلاه")

def main():
    """الدالة الرئيسية للتحقق"""
    print("🔍 التحقق من النتائج النهائية للتحديث")
    print("=" * 60)
    
    checks = [
        ("الفئات", check_categories),
        ("المنتجات", check_products),
        ("الصور", check_images),
        ("بيانات التوفر الشهري", check_seasonal_data),
        ("Slugs", check_slugs)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_function in checks:
        try:
            if check_function():
                print(f"✅ {check_name}: نجح")
                passed_checks += 1
            else:
                print(f"⚠️  {check_name}: يحتاج مراجعة")
        except Exception as e:
            print(f"❌ {check_name}: خطأ - {e}")
    
    # التقرير النهائي
    generate_final_report()
    
    print(f"\n📊 نتيجة التحقق: {passed_checks}/{total_checks} فحوصات نجحت")
    
    if passed_checks == total_checks:
        print("🎉 جميع الفحوصات نجحت! النظام جاهز")
        return True
    else:
        print("⚠️  بعض الفحوصات تحتاج مراجعة")
        return False

if __name__ == "__main__":
    main()
