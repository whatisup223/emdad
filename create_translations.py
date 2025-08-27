#!/usr/bin/env python3
"""Create translation files for Flask-Babel"""

import os
from babel.messages import Catalog
from babel.messages.pofile import write_po
from babel.messages.mofile import write_mo

# Arabic translations
ar_translations = {
    "Dashboard": "لوحة التحكم",
    "Categories": "الفئات", 
    "Products": "المنتجات",
    "RFQs": "طلبات الأسعار",
    "News": "الأخبار",
    "Gallery": "المعرض",
    "Users": "المستخدمين",
    "Settings": "الإعدادات",
    "Logout": "تسجيل الخروج",
    "Content": "المحتوى",
    "Services": "الخدمات",
    "Certifications": "الشهادات",
    "Reports": "التقارير",
    "Quick Links": "روابط سريعة",
    "View Website": "عرض الموقع",
    "Welcome to Admin Panel": "مرحباً بك في لوحة التحكم",
    "Total Products": "إجمالي المنتجات",
    "Total Categories": "إجمالي الفئات",
    "Pending RFQs": "طلبات الأسعار المعلقة",
    "Total RFQs": "إجمالي طلبات الأسعار",
    "Published News": "الأخبار المنشورة",
    "Gallery Images": "صور المعرض",
    "Recent RFQs": "طلبات الأسعار الحديثة",
    "Recent Activity": "النشاط الحديث",
    "Add New": "إضافة جديد",
    "Edit": "تعديل",
    "Delete": "حذف",
    "Save": "حفظ",
    "Cancel": "إلغاء",
    "Back to List": "العودة للقائمة",
    "Actions": "الإجراءات",
    "Status": "الحالة",
    "Active": "نشط",
    "Inactive": "غير نشط",
    "Name": "الاسم",
    "Description": "الوصف",
    "Image": "الصورة",
    "Category Management": "إدارة الفئات",
    "Product Management": "إدارة المنتجات",
    "RFQ Management": "إدارة طلبات الأسعار",
    "News Management": "إدارة الأخبار",
    "Gallery Management": "إدارة المعرض",
    "Services Management": "إدارة الخدمات",
    "Certifications Management": "إدارة الشهادات",
    "Users Management": "إدارة المستخدمين",
    "System Settings": "إعدادات النظام",
    "Reports & Analytics": "التقارير والتحليلات"
}

def create_catalog(locale, translations=None):
    """Create a catalog for the given locale"""
    catalog = Catalog(locale=locale)
    
    if translations:
        for msgid, msgstr in translations.items():
            catalog.add(msgid, string=msgstr)
    else:
        # English - just add the keys as both msgid and msgstr
        for key in ar_translations.keys():
            catalog.add(key, string=key)
    
    return catalog

def save_catalog(catalog, locale):
    """Save catalog as both .po and .mo files"""
    # Create directories
    locale_dir = f'translations/{locale}/LC_MESSAGES'
    os.makedirs(locale_dir, exist_ok=True)
    
    # Save .po file
    po_path = f'{locale_dir}/messages.po'
    with open(po_path, 'wb') as f:
        write_po(f, catalog)
    
    # Save .mo file
    mo_path = f'{locale_dir}/messages.mo'
    with open(mo_path, 'wb') as f:
        write_mo(f, catalog)
    
    print(f'Created {po_path} and {mo_path}')

# Create Arabic catalog
ar_catalog = create_catalog('ar', ar_translations)
save_catalog(ar_catalog, 'ar')

# Create English catalog
en_catalog = create_catalog('en')
save_catalog(en_catalog, 'en')

print("Translation files created successfully!")
