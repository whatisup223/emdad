#!/usr/bin/env python3
"""
تنفيذ التحديث الشامل للفئات والمنتجات
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """تشغيل سكريبت وعرض النتائج"""
    print(f"\n🚀 {description}")
    print("=" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print("⚠️  تحذيرات:")
                print(result.stderr)
            return True
        else:
            print(f"❌ خطأ في تشغيل {script_name}:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل {script_name}: {e}")
        return False

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    print("💾 إنشاء نسخة احتياطية من قاعدة البيانات...")
    
    db_path = Path("instance/emdad.db")
    backup_path = Path("instance/emdad_backup.db")
    
    if db_path.exists():
        try:
            import shutil
            shutil.copy2(db_path, backup_path)
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    else:
        print(f"⚠️  قاعدة البيانات غير موجودة: {db_path}")
        return False

def backup_images():
    """إنشاء نسخة احتياطية من الصور"""
    print("\n📸 إنشاء نسخة احتياطية من الصور...")
    
    images_dir = Path("static/uploads/products")
    backup_dir = Path("static/uploads/products_backup")
    
    if images_dir.exists():
        try:
            import shutil
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(images_dir, backup_dir)
            print(f"✅ تم إنشاء نسخة احتياطية: {backup_dir}")
            return True
        except Exception as e:
            print(f"❌ خطأ في إنشاء نسخة احتياطية للصور: {e}")
            return False
    else:
        print(f"⚠️  مجلد الصور غير موجود: {images_dir}")
        return False

def check_prerequisites():
    """التحقق من المتطلبات المسبقة"""
    print("🔍 التحقق من المتطلبات المسبقة...")
    
    required_files = [
        "update_categories_products.py",
        "rename_images.py", 
        "add_seasonal_data.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ ملفات مفقودة: {missing_files}")
        return False
    
    print("✅ جميع الملفات المطلوبة موجودة")
    return True

def show_summary():
    """عرض ملخص التحديث"""
    print("\n📊 ملخص التحديث المطلوب:")
    print("=" * 60)
    print("🎯 الهدف: تحديث النظام ليطابق الصورة المرجعية")
    print("\n📋 المراحل:")
    print("   1️⃣  إنشاء نسخ احتياطية")
    print("   2️⃣  تحديث قاعدة البيانات (فئات ومنتجات)")
    print("   3️⃣  إعادة تسمية الصور الموجودة")
    print("   4️⃣  إضافة بيانات التوفر الشهري")
    print("   5️⃣  التحقق من النتائج")
    
    print("\n📈 النتيجة المتوقعة:")
    print("   📁 8 فئات منظمة")
    print("   📦 38 منتج مصنف")
    print("   🖼️  جميع الصور محدثة")
    print("   📅 بيانات توفر شهري كاملة")

def main():
    """الدالة الرئيسية للتنفيذ"""
    print("🌟 تحديث شامل للفئات والمنتجات")
    print("=" * 60)
    print("📋 هذا السكريبت سيقوم بتحديث النظام ليطابق الصورة المرجعية")
    
    # عرض الملخص
    show_summary()
    
    # طلب التأكيد
    print("\n" + "=" * 60)
    response = input("🤔 هل تريد المتابعة مع التحديث؟ (y/N): ")
    
    if response.lower() != 'y':
        print("❌ تم إلغاء التحديث")
        return
    
    # التحقق من المتطلبات
    if not check_prerequisites():
        print("❌ لا يمكن المتابعة بسبب ملفات مفقودة")
        return
    
    success_count = 0
    total_steps = 5
    
    # المرحلة 1: النسخ الاحتياطية
    print("\n" + "🔄" * 20 + " المرحلة 1: النسخ الاحتياطية " + "🔄" * 20)
    if backup_database() and backup_images():
        success_count += 1
        print("✅ تم إنشاء النسخ الاحتياطية بنجاح")
    else:
        print("⚠️  تحذير: لم يتم إنشاء النسخ الاحتياطية بشكل كامل")
    
    # المرحلة 2: تحديث قاعدة البيانات
    print("\n" + "🔄" * 20 + " المرحلة 2: تحديث قاعدة البيانات " + "🔄" * 20)
    if run_script("update_categories_products.py", "تحديث الفئات والمنتجات"):
        success_count += 1
    
    # المرحلة 3: إعادة تسمية الصور
    print("\n" + "🔄" * 20 + " المرحلة 3: إدارة الصور " + "🔄" * 20)
    if run_script("rename_images.py", "إعادة تسمية وإدارة الصور"):
        success_count += 1
    
    # المرحلة 4: إضافة بيانات التوفر
    print("\n" + "🔄" * 20 + " المرحلة 4: بيانات التوفر الشهري " + "🔄" * 20)
    if run_script("add_seasonal_data.py", "إضافة بيانات التوفر الشهري"):
        success_count += 1
    
    # المرحلة 5: التحقق النهائي
    print("\n" + "🔄" * 20 + " المرحلة 5: التحقق النهائي " + "🔄" * 20)
    if run_script("check_final_results.py", "التحقق من النتائج النهائية"):
        success_count += 1
    
    # النتائج النهائية
    print("\n" + "🎉" * 20 + " النتائج النهائية " + "🎉" * 20)
    print(f"📊 تم إنجاز {success_count}/{total_steps} مراحل بنجاح")
    
    if success_count == total_steps:
        print("🎉 تم التحديث بنجاح! النظام جاهز للاستخدام")
        print("\n📋 الخطوات التالية:")
        print("   1️⃣  اختبار الموقع محلياً")
        print("   2️⃣  رفع الصور الجديدة المطلوبة")
        print("   3️⃣  اختبار جميع الوظائف")
        print("   4️⃣  نشر التحديثات للإنتاج")
    elif success_count >= 3:
        print("⚠️  التحديث مكتمل جزئياً - راجع الأخطاء أعلاه")
    else:
        print("❌ فشل التحديث - راجع الأخطاء وأعد المحاولة")
        print("💡 يمكنك استعادة النسخ الاحتياطية إذا لزم الأمر")

if __name__ == "__main__":
    main()
