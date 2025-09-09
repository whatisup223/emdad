#!/usr/bin/env python3
"""
سكريبت تحديث الفئات والمنتجات لتطابق الصورة المرجعية
"""

from app import create_app
from app.models import Category, Product, db
import re

def create_slug(text):
    """إنشاء slug من النص"""
    # تحويل إلى أحرف صغيرة وإزالة المسافات والرموز
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def update_categories_and_products():
    """تحديث الفئات والمنتجات"""
    
    app = create_app()
    with app.app_context():
        print("🚀 بدء تحديث الفئات والمنتجات...")
        
        # الفئات الجديدة حسب الصورة
        new_categories = [
            {
                'id': 1,
                'name_en': 'Fresh Citrus',
                'name_ar': 'حمضيات طازجة',
                'description_en': 'Fresh citrus fruits including oranges, mandarins, and tangerines',
                'description_ar': 'حمضيات طازجة تشمل البرتقال واليوسفي والكلمنتينا'
            },
            {
                'id': 2,
                'name_en': 'Fresh Vegetables',
                'name_ar': 'خضروات طازجة',
                'description_en': 'Fresh vegetables including garlic, onions, potatoes, and sweet potatoes',
                'description_ar': 'خضروات طازجة تشمل الثوم والبصل والبطاطس والبطاطا الحلوة'
            },
            {
                'id': 3,
                'name_en': 'Fresh Fruit',
                'name_ar': 'فواكه طازجة',
                'description_en': 'Fresh fruits including pomegranates, grapes, strawberries, and mango',
                'description_ar': 'فواكه طازجة تشمل الرمان والعنب والفراولة والمانجو'
            },
            {
                'id': 4,
                'name_en': 'Dates',
                'name_ar': 'تمور',
                'description_en': 'Various types of dates including whole and pitted varieties',
                'description_ar': 'أنواع مختلفة من التمور تشمل الكامل ومنزوع النواة'
            },
            {
                'id': 5,
                'name_en': 'IQF',
                'name_ar': 'مجمدة سريعاً',
                'description_en': 'Individually Quick Frozen fruits',
                'description_ar': 'فواكه مجمدة سريعاً بشكل فردي'
            },
            {
                'id': 6,
                'name_en': 'Spices',
                'name_ar': 'توابل',
                'description_en': 'Various spices and seeds for cooking',
                'description_ar': 'توابل وبذور مختلفة للطبخ'
            },
            {
                'id': 7,
                'name_en': 'Herbs & Herbal Plants',
                'name_ar': 'أعشاب ونباتات عشبية',
                'description_en': 'Dried herbs and herbal plants for culinary and medicinal use',
                'description_ar': 'أعشاب مجففة ونباتات عشبية للاستخدام الطبخي والطبي'
            },
            {
                'id': 8,
                'name_en': 'Oil Seeds',
                'name_ar': 'بذور زيتية',
                'description_en': 'Seeds rich in oils for various uses',
                'description_ar': 'بذور غنية بالزيوت لاستخدامات مختلفة'
            }
        ]
        
        # المنتجات الجديدة والمحدثة حسب الصورة
        updated_products = [
            # Fresh Citrus
            {'id': 4, 'category_id': 1, 'name_en': 'Fresh Mandarins', 'name_ar': 'يوسفي طازج', 'slug': 'fresh-mandarins'},
            {'id': 3, 'category_id': 1, 'name_en': 'Fresh Oranges', 'name_ar': 'برتقال طازج', 'slug': 'fresh-oranges'},
            {'id': 5, 'category_id': 1, 'name_en': 'Fresh Tangerines', 'name_ar': 'كلمنتينا طازجة', 'slug': 'fresh-tangerines'},
            
            # Fresh Vegetables
            {'id': 21, 'category_id': 2, 'name_en': 'Garlic (White)', 'name_ar': 'ثوم أبيض', 'slug': 'garlic-white'},
            {'id': 20, 'category_id': 2, 'name_en': 'Onions (Red/Golden)', 'name_ar': 'بصل أحمر/ذهبي', 'slug': 'onions-red-golden'},
            {'id': 18, 'category_id': 2, 'name_en': 'Potatoes (Spunta)', 'name_ar': 'بطاطس سبونتا', 'slug': 'potatoes-spunta'},
            {'id': 19, 'category_id': 2, 'name_en': 'Sweet Potatoes (Beauregard)', 'name_ar': 'بطاطا حلوة بوريجارد', 'slug': 'sweet-potatoes-beauregard'},
            
            # Fresh Fruit
            {'id': 6, 'category_id': 3, 'name_en': 'Fresh Strawberries', 'name_ar': 'فراولة طازجة', 'slug': 'fresh-strawberries'},
            
            # Dates
            {'id': 7, 'category_id': 4, 'name_en': 'Dates — Whole', 'name_ar': 'تمر كامل', 'slug': 'dates-whole'},
            
            # IQF
            {'id': 1, 'category_id': 5, 'name_en': 'IQF Mango', 'name_ar': 'مانجو مجمد', 'slug': 'iqf-mango'},
            {'id': 2, 'category_id': 5, 'name_en': 'IQF Strawberries', 'name_ar': 'فراولة مجمدة', 'slug': 'iqf-strawberries'},
            
            # Spices
            {'id': 12, 'category_id': 6, 'name_en': 'Anise Seed', 'name_ar': 'بذور يانسون', 'slug': 'anise-seed'},
            {'id': 11, 'category_id': 6, 'name_en': 'Caraway Seed', 'name_ar': 'بذور كراوية', 'slug': 'caraway-seed'},
            {'id': 9, 'category_id': 6, 'name_en': 'Coriander Seed', 'name_ar': 'بذور كزبرة', 'slug': 'coriander-seed'},
            {'id': 8, 'category_id': 6, 'name_en': 'Cumin Seed', 'name_ar': 'بذور كمون', 'slug': 'cumin-seed'},
            {'id': 10, 'category_id': 6, 'name_en': 'Fennel Seed', 'name_ar': 'بذور شمر', 'slug': 'fennel-seed'},
            
            # Herbs & Herbal Plants
            {'id': 13, 'category_id': 7, 'name_en': 'Basil', 'name_ar': 'ريحان', 'slug': 'basil'},
            {'id': 14, 'category_id': 7, 'name_en': 'Marjoram', 'name_ar': 'مردقوش', 'slug': 'marjoram'},
            {'id': 16, 'category_id': 7, 'name_en': 'Dill', 'name_ar': 'شبت', 'slug': 'dill'},
            {'id': 17, 'category_id': 7, 'name_en': 'Parsley Flakes', 'name_ar': 'رقائق بقدونس', 'slug': 'parsley-flakes'},
            {'id': 15, 'category_id': 7, 'name_en': 'Mint', 'name_ar': 'نعناع', 'slug': 'mint'},
            {'id': 22, 'category_id': 7, 'name_en': 'Chamomile', 'name_ar': 'بابونج', 'slug': 'chamomile'},
            {'id': 23, 'category_id': 7, 'name_en': 'Hibiscus', 'name_ar': 'كركديه', 'slug': 'hibiscus'},
            {'id': 24, 'category_id': 7, 'name_en': 'Calendula', 'name_ar': 'أذريون', 'slug': 'calendula'},
            {'id': 25, 'category_id': 7, 'name_en': 'Lemongrass', 'name_ar': 'عشبة الليمون', 'slug': 'lemongrass'},
            {'id': 26, 'category_id': 7, 'name_en': 'Sage', 'name_ar': 'مريمية', 'slug': 'sage'},
            
            # Oil Seeds
            {'id': 27, 'category_id': 8, 'name_en': 'Sesame (seed)', 'name_ar': 'سمسم', 'slug': 'sesame-seed'},
            {'id': 28, 'category_id': 8, 'name_en': 'Flax seeds', 'name_ar': 'بذور كتان', 'slug': 'flax-seeds'},
        ]
        
        # المنتجات الجديدة التي تحتاج إضافة
        new_products = [
            # Fresh Vegetables
            {'name_en': 'Fresh Spring Onions / Scallions', 'name_ar': 'بصل أخضر طازج', 'category_id': 2, 'slug': 'fresh-spring-onions'},
            
            # Fresh Fruit
            {'name_en': 'Fresh Pomegranates', 'name_ar': 'رمان طازج', 'category_id': 3, 'slug': 'fresh-pomegranates'},
            {'name_en': 'Fresh Grapes', 'name_ar': 'عنب طازج', 'category_id': 3, 'slug': 'fresh-grapes'},
            {'name_en': 'Fresh Mango', 'name_ar': 'مانجو طازج', 'category_id': 3, 'slug': 'fresh-mango'},
            
            # Dates
            {'name_en': 'Dates — Pitted', 'name_ar': 'تمر منزوع النواة', 'category_id': 4, 'slug': 'dates-pitted'},
            {'name_en': 'Medjool Dates — Pitted', 'name_ar': 'تمر مجهول منزوع النواة', 'category_id': 4, 'slug': 'medjool-dates-pitted'},
            {'name_en': 'Medjool Dates — Whole', 'name_ar': 'تمر مجهول كامل', 'category_id': 4, 'slug': 'medjool-dates-whole'},
            
            # Spices
            {'name_en': 'Nigella (Black Seed)', 'name_ar': 'حبة البركة', 'category_id': 6, 'slug': 'nigella-black-seed'},
            
            # Herbs & Herbal Plants
            {'name_en': 'Oregano', 'name_ar': 'أوريجانو', 'category_id': 7, 'slug': 'oregano'},
            {'name_en': 'Thyme', 'name_ar': 'زعتر', 'category_id': 7, 'slug': 'thyme'},
        ]
        
        try:
            # تحديث الفئات
            print("📁 تحديث الفئات...")
            for cat_data in new_categories:
                category = Category.query.get(cat_data['id'])
                if category:
                    category.name_en = cat_data['name_en']
                    category.name_ar = cat_data['name_ar']
                    category.description_en = cat_data['description_en']
                    category.description_ar = cat_data['description_ar']
                    print(f"   ✅ تم تحديث الفئة: {cat_data['name_ar']}")
                else:
                    new_category = Category(
                        id=cat_data['id'],
                        name_en=cat_data['name_en'],
                        name_ar=cat_data['name_ar'],
                        description_en=cat_data['description_en'],
                        description_ar=cat_data['description_ar']
                    )
                    db.session.add(new_category)
                    print(f"   ➕ تم إنشاء فئة جديدة: {cat_data['name_ar']}")
            
            # تحديث المنتجات الموجودة
            print("\n📦 تحديث المنتجات الموجودة...")
            for prod_data in updated_products:
                product = Product.query.get(prod_data['id'])
                if product:
                    product.name_en = prod_data['name_en']
                    product.name_ar = prod_data['name_ar']
                    product.category_id = prod_data['category_id']
                    product.slug = prod_data['slug']
                    print(f"   ✅ تم تحديث المنتج: {prod_data['name_ar']}")
            
            # إضافة المنتجات الجديدة (بدون image_path - سيتم إضافتها لاحقاً)
            print("\n➕ إضافة المنتجات الجديدة...")
            for prod_data in new_products:
                # التحقق من عدم وجود المنتج
                existing = Product.query.filter_by(slug=prod_data['slug']).first()
                if not existing:
                    new_product = Product(
                        name_en=prod_data['name_en'],
                        name_ar=prod_data['name_ar'],
                        category_id=prod_data['category_id'],
                        slug=prod_data['slug'],
                        description_en=f"High quality {prod_data['name_en'].lower()}",
                        description_ar=f"{prod_data['name_ar']} عالي الجودة"
                        # image_path سيتم إضافتها بعد رفع الصور
                    )
                    db.session.add(new_product)
                    print(f"   ➕ تم إضافة منتج جديد: {prod_data['name_ar']} (بدون صورة)")
                else:
                    print(f"   ⚠️  المنتج موجود بالفعل: {prod_data['name_ar']}")
            
            # حفظ التغييرات
            db.session.commit()
            print("\n✅ تم حفظ جميع التغييرات بنجاح!")
            
            # عرض الإحصائيات النهائية
            print("\n📊 الإحصائيات النهائية:")
            categories = Category.query.all()
            for category in categories:
                product_count = Product.query.filter_by(category_id=category.id).count()
                print(f"   {category.name_ar}: {product_count} منتج")
            
            total_products = Product.query.count()
            print(f"\n📈 إجمالي المنتجات: {total_products}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في التحديث: {e}")
            raise

def create_missing_images():
    """إنشاء قائمة بالصور المطلوبة للمنتجات الجديدة"""

    missing_images = [
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

    print("\n📸 الصور المطلوبة للمنتجات الجديدة:")
    print("=" * 50)
    for image in missing_images:
        print(f"   📁 static/uploads/products/{image}")

    print(f"\n📊 إجمالي الصور المطلوبة: {len(missing_images)}")
    print("\n⚠️  تحتاج لرفع هذه الصور بصيغة WebP في المجلد:")
    print("   📂 static/uploads/products/")

def show_updated_images():
    """عرض الصور التي تحتاج تحديث أسماء"""

    updated_images = [
        {'old': 'mandarins-emdad-global.webp', 'new': 'fresh-mandarins-emdad-global.webp'},
        {'old': 'oranges-emdad-global.webp', 'new': 'fresh-oranges-emdad-global.webp'},
        {'old': 'tangerines-emdad-global.webp', 'new': 'fresh-tangerines-emdad-global.webp'},
        {'old': 'strawberries-emdad-global.webp', 'new': 'fresh-strawberries-emdad-global.webp'},
        {'old': 'garlic-emdad-global.webp', 'new': 'garlic-white-emdad-global.webp'},
        {'old': 'onions-emdad-global.webp', 'new': 'onions-red-golden-emdad-global.webp'},
        {'old': 'potatoes-emdad-global.webp', 'new': 'potatoes-spunta-emdad-global.webp'},
        {'old': 'sweet-potatoes-emdad-global.webp', 'new': 'sweet-potatoes-beauregard-emdad-global.webp'},
        {'old': 'parsley-emdad-global.webp', 'new': 'parsley-flakes-emdad-global.webp'},
        {'old': 'sesame-seeds-emdad-global.webp', 'new': 'sesame-seed-emdad-global.webp'}
    ]

    print("\n🔄 الصور التي تحتاج إعادة تسمية:")
    print("=" * 50)
    for img in updated_images:
        print(f"   📁 {img['old']} → {img['new']}")

    print(f"\n📊 إجمالي الصور للتحديث: {len(updated_images)}")

if __name__ == "__main__":
    print("🚀 تحديث النظام ليطابق الصورة المرجعية")
    print("=" * 60)

    # تحديث قاعدة البيانات
    update_categories_and_products()

    # عرض الصور المطلوبة
    create_missing_images()
    show_updated_images()
