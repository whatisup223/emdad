#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح أوصاف المنتجات المفقودة
"""

from app import create_app
from app.models import Product, db

def fix_product_descriptions():
    """إضافة أوصاف للمنتجات التي لا تحتوي على أوصاف"""
    
    app = create_app()
    with app.app_context():
        print("🔄 إصلاح أوصاف المنتجات...")
        print("=" * 50)
        
        # البحث عن المنتجات بدون وصف قصير
        products_without_desc = Product.query.filter(
            (Product.short_description_en.is_(None)) | 
            (Product.short_description_ar.is_(None)) |
            (Product.short_description_en == '') |
            (Product.short_description_ar == '')
        ).all()
        
        print(f"📦 منتجات بدون وصف قصير: {len(products_without_desc)}")
        
        if not products_without_desc:
            print("✅ جميع المنتجات لها أوصاف قصيرة")
            return
        
        updated_count = 0
        
        for product in products_without_desc:
            # إضافة وصف إنجليزي إذا كان مفقود
            if not product.short_description_en:
                product.short_description_en = f"High quality {product.name_en.lower()} sourced from Egypt with exceptional taste and nutritional value."
            
            # إضافة وصف عربي إذا كان مفقود
            if not product.short_description_ar:
                product.short_description_ar = f"{product.name_ar} عالي الجودة من مصر بطعم استثنائي وقيمة غذائية عالية."
            
            updated_count += 1
            print(f"   ✅ تم إضافة وصف للمنتج: {product.name_ar}")
        
        try:
            if updated_count > 0:
                db.session.commit()
                print(f"\n✅ تم تحديث {updated_count} منتج بنجاح!")
            
            # التحقق من النتائج
            remaining_without_desc = Product.query.filter(
                (Product.short_description_en.is_(None)) | 
                (Product.short_description_ar.is_(None)) |
                (Product.short_description_en == '') |
                (Product.short_description_ar == '')
            ).count()
            
            print(f"\n📊 النتائج:")
            print(f"   📦 إجمالي المنتجات: {Product.query.count()}")
            print(f"   ✅ منتجات لها أوصاف: {Product.query.count() - remaining_without_desc}")
            print(f"   ❌ منتجات بدون أوصاف: {remaining_without_desc}")
            
            if remaining_without_desc == 0:
                print("\n🎉 جميع المنتجات لها أوصاف قصيرة الآن!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ في حفظ التحديثات: {e}")
            raise

if __name__ == "__main__":
    fix_product_descriptions()
