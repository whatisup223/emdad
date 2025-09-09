#!/usr/bin/env python3
"""
🚀 Production Deployment Script
تشغيل هذا الملف في الإنتاج لتطبيق جميع التحديثات تلقائياً
"""

import os
import sys
from pathlib import Path

def run_production_update():
    """تشغيل جميع التحديثات المطلوبة في الإنتاج"""
    
    print("🚀 بدء تحديث الإنتاج...")
    print("=" * 50)
    
    # قائمة الملفات المطلوب تشغيلها بالترتيب
    scripts = [
        "update_categories_products.py",
        "add_seasonal_data.py", 
        "manage_product_images.py",
        "fix_product_descriptions.py",
        "check_final_results.py"
    ]
    
    success_count = 0
    
    for script in scripts:
        print(f"\n📋 تشغيل: {script}")
        print("-" * 30)
        
        if not Path(script).exists():
            print(f"❌ الملف غير موجود: {script}")
            continue
            
        try:
            # تشغيل الملف
            exit_code = os.system(f"python {script}")
            
            if exit_code == 0:
                print(f"✅ نجح: {script}")
                success_count += 1
            else:
                print(f"❌ فشل: {script} (exit code: {exit_code})")
                
        except Exception as e:
            print(f"❌ خطأ في تشغيل {script}: {e}")
    
    print(f"\n📊 النتائج النهائية:")
    print(f"   ✅ نجح: {success_count}/{len(scripts)} scripts")
    print(f"   ❌ فشل: {len(scripts) - success_count}/{len(scripts)} scripts")
    
    if success_count == len(scripts):
        print("\n🎉 تم تحديث الإنتاج بنجاح!")
        print("✅ جميع المنتجات والصور جاهزة الآن")
        return True
    else:
        print("\n⚠️  بعض التحديثات فشلت - يرجى المراجعة")
        return False

def check_environment():
    """التحقق من بيئة الإنتاج"""
    print("🔍 فحص بيئة الإنتاج...")
    
    # التحقق من وجود Flask app
    try:
        from app import create_app
        app = create_app()
        print("✅ Flask app متاح")
    except Exception as e:
        print(f"❌ مشكلة في Flask app: {e}")
        return False
    
    # التحقق من قاعدة البيانات
    try:
        with app.app_context():
            from app.models import Product, Category
            product_count = Product.query.count()
            category_count = Category.query.count()
            print(f"✅ قاعدة البيانات متاحة: {product_count} منتج، {category_count} فئة")
    except Exception as e:
        print(f"❌ مشكلة في قاعدة البيانات: {e}")
        return False
    
    # التحقق من مجلد الصور
    static_dir = Path("static/uploads/products")
    if static_dir.exists():
        image_count = len(list(static_dir.glob("*.webp")))
        print(f"✅ مجلد الصور متاح: {image_count} صورة")
    else:
        print("❌ مجلد الصور غير موجود")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Production Deployment - Emdad Global")
    print("=" * 50)
    
    # فحص البيئة أولاً
    if not check_environment():
        print("❌ فشل فحص البيئة - توقف التحديث")
        sys.exit(1)
    
    # تشغيل التحديثات
    success = run_production_update()
    
    if success:
        print("\n🎉 تم تحديث الإنتاج بنجاح!")
        print("🌐 الموقع جاهز الآن مع جميع المنتجات والصور")
        sys.exit(0)
    else:
        print("\n❌ فشل في بعض التحديثات")
        sys.exit(1)
