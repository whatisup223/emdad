#!/usr/bin/env python3
"""
إضافة بيانات التوفر الشهري للمنتجات الجديدة
"""

from app import create_app
from app.models import Product, db
import json

def add_seasonal_data():
    """إضافة بيانات التوفر الشهري للمنتجات الجديدة"""

    app = create_app()
    with app.app_context():
        print("📅 إضافة بيانات التوفر الشهري للمنتجات الجديدة...")

        # بيانات التوفر الشهري للمنتجات الجديدة
        seasonal_data = {
            # Fresh Vegetables
            'fresh-spring-onions': ['available','available','peak','peak','peak','available','available','limited','limited','available','available','available'],

            # Fresh Fruit
            'fresh-pomegranates': ['off','off','off','off','off','off','off','off','peak','peak','available','available'],
            'fresh-grapes': ['off','off','off','off','off','peak','peak','peak','available','available','off','off'],
            'fresh-mango': ['off','off','off','off','peak','peak','peak','available','available','off','off','off'],

            # Dates
            'dates-pitted': ['available','available','available','available','available','available','available','available','available','peak','peak','available'],
            'medjool-dates-pitted': ['available','available','available','available','available','available','available','available','available','peak','peak','available'],
            'medjool-dates-whole': ['available','available','available','available','available','available','available','available','available','peak','peak','available'],

            # Spices
            'nigella-black-seed': ['available','available','available','available','available','available','available','available','available','available','available','available'],

            # Herbs & Herbal Plants
            'oregano': ['available','available','available','available','available','available','available','available','available','available','available','available'],
            'thyme': ['available','available','available','available','available','available','available','available','available','available','available','available'],
        }

        try:
            added_count = 0

            for slug, months_state in seasonal_data.items():
                # البحث عن المنتج
                product = Product.query.filter_by(slug=slug).first()

                if product:
                    # التحقق من عدم وجود بيانات توفر مسبقاً
                    existing_seasonality = product.get_seasonality()

                    if not existing_seasonality:
                        # إنشاء بيانات التوفر الشهري
                        seasonality_data = {
                            'months_state': months_state
                        }
                        product.seasonality = json.dumps(seasonality_data)
                        added_count += 1
                        print(f"   ✅ تم إضافة بيانات التوفر للمنتج: {product.name_ar}")
                    else:
                        print(f"   ⚠️  بيانات التوفر موجودة مسبقاً للمنتج: {product.name_ar}")
                else:
                    print(f"   ❌ لم يتم العثور على المنتج: {slug}")

            # حفظ التغييرات
            if added_count > 0:
                db.session.commit()
                print(f"\n✅ تم إضافة بيانات التوفر لـ {added_count} منتج بنجاح!")
            else:
                print("\n⚠️  لم يتم إضافة أي بيانات جديدة")

            # عرض إحصائيات
            total_products = Product.query.count()
            products_with_seasons = Product.query.filter(Product.seasonality.isnot(None)).count()
            products_without_seasons = total_products - products_with_seasons

            print(f"\n📊 إحصائيات التوفر الشهري:")
            print(f"   📦 إجمالي المنتجات: {total_products}")
            print(f"   ✅ منتجات لها بيانات توفر: {products_with_seasons}")
            print(f"   ❌ منتجات بدون بيانات توفر: {products_without_seasons}")

            if products_without_seasons > 0:
                print(f"\n⚠️  المنتجات التي تحتاج بيانات توفر:")
                products_no_season = Product.query.filter(Product.seasonality.is_(None)).all()
                for product in products_no_season:
                    print(f"   - {product.name_ar} (slug: {product.slug})")

        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في إضافة بيانات التوفر: {e}")
            raise

def add_missing_seasonal_data():
    """إضافة بيانات التوفر للمنتجات التي لا تملك بيانات"""

    app = create_app()
    with app.app_context():
        print("🔍 البحث عن المنتجات بدون بيانات توفر...")

        # البحث عن المنتجات بدون بيانات توفر
        products_no_season = Product.query.filter(Product.seasonality.is_(None)).all()

        if not products_no_season:
            print("✅ جميع المنتجات لديها بيانات توفر شهري")
            return

        print(f"📦 تم العثور على {len(products_no_season)} منتج بدون بيانات توفر")

        # بيانات توفر افتراضية حسب نوع المنتج
        default_patterns = {
            'herbs': ['available','available','available','available','available','available','available','available','available','available','available','available'],  # متاح طوال السنة
            'spices': ['available','available','available','available','available','available','available','available','available','available','available','available'],  # متاح طوال السنة
            'seeds': ['available','available','available','available','available','available','available','available','available','available','available','available'],  # متاح طوال السنة
            'citrus': ['peak','peak','peak','available','available','off','off','off','off','available','available','peak'],  # موسم الشتاء
            'vegetables': ['available','available','available','available','available','available','available','available','available','available','available','available'],  # متاح طوال السنة
            'fruits': ['off','off','off','off','available','peak','peak','peak','available','available','off','off'],  # موسم الصيف
            'dates': ['available','available','available','available','available','available','available','available','available','peak','peak','available'],  # ذروة في الخريف
            'iqf': ['available','available','available','available','available','available','available','available','available','available','available','available']  # متاح طوال السنة
        }

        try:
            added_count = 0

            for product in products_no_season:
                # تحديد نمط التوفر حسب الفئة
                pattern = ['available','available','available','available','available','available','available','available','available','available','available','available']  # افتراضي

                if product.category_id == 1:  # Fresh Citrus
                    pattern = default_patterns['citrus']
                elif product.category_id == 2:  # Fresh Vegetables
                    pattern = default_patterns['vegetables']
                elif product.category_id == 3:  # Fresh Fruit
                    pattern = default_patterns['fruits']
                elif product.category_id == 4:  # Dates
                    pattern = default_patterns['dates']
                elif product.category_id == 5:  # IQF
                    pattern = default_patterns['iqf']
                elif product.category_id == 6:  # Spices
                    pattern = default_patterns['spices']
                elif product.category_id == 7:  # Herbs & Herbal Plants
                    pattern = default_patterns['herbs']
                elif product.category_id == 8:  # Oil Seeds
                    pattern = default_patterns['seeds']

                # إنشاء بيانات التوفر
                seasonality_data = {
                    'months_state': pattern
                }
                product.seasonality = json.dumps(seasonality_data)
                added_count += 1
                print(f"   ✅ تم إضافة بيانات توفر افتراضية للمنتج: {product.name_ar}")

            # حفظ التغييرات
            if added_count > 0:
                db.session.commit()
                print(f"\n✅ تم إضافة بيانات التوفر لـ {added_count} منتج بنجاح!")

        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في إضافة البيانات الافتراضية: {e}")
            raise

if __name__ == "__main__":
    print("📅 إضافة بيانات التوفر الشهري")
    print("=" * 50)
    
    # إضافة بيانات محددة للمنتجات الجديدة
    add_seasonal_data()
    
    print("\n" + "=" * 50)
    
    # إضافة بيانات افتراضية للمنتجات المتبقية
    add_missing_seasonal_data()
    
    print("\n🎉 تم الانتهاء من إضافة جميع بيانات التوفر الشهري!")
