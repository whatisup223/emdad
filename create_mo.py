#!/usr/bin/env python3
"""Simple script to create .mo files from .po files"""

import os
import struct

def create_mo_file(translations):
    """Create a .mo file content from translations dictionary"""
    keys = sorted(translations.keys())
    
    # Prepare data
    ids = [key.encode('utf-8') for key in keys]
    strs = [translations[key].encode('utf-8') for key in keys]
    
    # Calculate offsets
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + sum(len(id) + 1 for id in ids)
    
    koffsets = []
    voffsets = []
    
    # Key offsets
    offset = keystart
    for id in ids:
        koffsets.append((len(id), offset))
        offset += len(id) + 1
    
    # Value offsets  
    offset = valuestart
    for str_val in strs:
        voffsets.append((len(str_val), offset))
        offset += len(str_val) + 1
    
    # Build .mo file content
    output = b''
    
    # Header
    output += struct.pack('<I', 0x950412de)  # Magic number
    output += struct.pack('<I', 0)           # Version
    output += struct.pack('<I', len(keys))   # Number of entries
    output += struct.pack('<I', 7 * 4)       # Offset of key table
    output += struct.pack('<I', 7 * 4 + 8 * len(keys))  # Offset of value table
    output += struct.pack('<I', 0)           # Hash table size
    output += struct.pack('<I', 0)           # Hash table offset
    
    # Key table
    for length, offset in koffsets:
        output += struct.pack('<I', length)
        output += struct.pack('<I', offset)
        
    # Value table
    for length, offset in voffsets:
        output += struct.pack('<I', length)
        output += struct.pack('<I', offset)
        
    # Keys
    for id_val in ids:
        output += id_val + b'\0'
        
    # Values
    for str_val in strs:
        output += str_val + b'\0'
    
    return output

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
    "Add New Category": "إضافة فئة جديدة",
    "Add New Product": "إضافة منتج جديد",
    "Edit Category": "تعديل الفئة",
    "Edit Product": "تعديل المنتج",
    "Category": "الفئة",
    "Featured": "مميز",
    "Created At": "تاريخ الإنشاء",
    "Updated At": "تاريخ التحديث",
    "View": "عرض",
    "Details": "التفاصيل",
    "All": "الكل",
    "Search": "البحث",
    "Filter": "تصفية",
    "Yes": "نعم",
    "No": "لا",
    "Draft": "مسودة",
    "Published": "منشور",
    "Company": "الشركة",
    "Email": "البريد الإلكتروني",
    "Phone": "الهاتف",
    "Country": "البلد",
    "Priority": "الأولوية",
    "High": "عالية",
    "Medium": "متوسطة",
    "Low": "منخفضة",
    "New": "جديد",
    "In Progress": "قيد المعالجة",
    "Completed": "مكتمل",
    "Cancelled": "ملغي",
    "Message": "الرسالة",
    "Customer Information": "معلومات العميل",
    "Request Information": "معلومات الطلب",
    "Product Details": "تفاصيل المنتج",
    "Change Status": "تغيير الحالة",
    "Change Priority": "تغيير الأولوية",
    "Send Email Reply": "إرسال رد بالبريد الإلكتروني",
    "RFQ Details": "تفاصيل طلب السعر",
    "Quantity": "الكمية",
    "Budget": "الميزانية",
    "Delivery Date": "تاريخ التسليم",

    # New sections
    "Content": "المحتوى",
    "Services": "الخدمات",
    "Certifications": "الشهادات",
    "Reports": "التقارير",
    "Settings": "الإعدادات",
    "Quick Links": "روابط سريعة",
    "View Website": "عرض الموقع",

    # News
    "News Management": "إدارة الأخبار",
    "Add New Article": "إضافة مقال جديد",
    "All Status": "جميع الحالات",
    "Archived": "مؤرشف",
    "Search articles...": "البحث في المقالات...",
    "Title": "العنوان",
    "Author": "الكاتب",
    "No Image": "لا توجد صورة",
    "Are you sure you want to delete this article?": "هل أنت متأكد من حذف هذا المقال؟",
    "No articles found": "لا توجد مقالات",
    "Previous": "السابق",
    "Next": "التالي",
    "Current Image": "الصورة الحالية",
    "Save Changes": "حفظ التغييرات",
    "Create Article": "إنشاء مقال",

    # Gallery
    "Gallery Management": "إدارة المعرض",
    "Upload New Image": "رفع صورة جديدة",
    "Are you sure you want to delete this image?": "هل أنت متأكد من حذف هذه الصورة؟",
    "Untitled": "بدون عنوان",
    "Uploaded": "تم الرفع",
    "No images in gallery": "لا توجد صور في المعرض",
    "Upload your first image to get started": "ارفع أول صورة للبدء",
    "Upload Image": "رفع صورة",
    "Back to Gallery": "العودة للمعرض",
    "Supported formats: JPG, JPEG, PNG, GIF. Max size: 5MB": "الصيغ المدعومة: JPG, JPEG, PNG, GIF. الحد الأقصى: 5 ميجابايت",
    "Preview": "معاينة",

    # Services
    "Services Management": "إدارة الخدمات",
    "Add New Service": "إضافة خدمة جديدة",
    "Icon": "الأيقونة",
    "Sort Order": "ترتيب العرض",
    "Are you sure you want to delete this service?": "هل أنت متأكد من حذف هذه الخدمة؟",
    "No services found": "لا توجد خدمات",
    "FontAwesome icon class (e.g., fas fa-shipping-fast)": "فئة أيقونة FontAwesome (مثل: fas fa-shipping-fast)",

    # Certifications
    "Certifications Management": "إدارة الشهادات",

    # Users
    "Users Management": "إدارة المستخدمين",
    "Add New User": "إضافة مستخدم جديد",
    "Username": "اسم المستخدم",
    "Role": "الدور",
    "Last Login": "آخر تسجيل دخول",
    "No users found": "لا توجد مستخدمين",
    "Leave empty to keep current password": "اتركه فارغاً للاحتفاظ بكلمة المرور الحالية",

    # Reports
    "Reports & Analytics": "التقارير والتحليلات",
    "Recent RFQs": "طلبات الأسعار الحديثة",
    "Recent Products": "المنتجات الحديثة",
    "Date": "التاريخ",

    # Settings
    "System Settings": "إعدادات النظام",
    "Company Information": "معلومات الشركة",
    "Company Name": "اسم الشركة",
    "Address": "العنوان",
    "Website Settings": "إعدادات الموقع",
    "Site Title": "عنوان الموقع",
    "Site Description": "وصف الموقع",
    "Default Language": "اللغة الافتراضية",
    "Timezone": "المنطقة الزمنية",
    "Social Media": "وسائل التواصل الاجتماعي",
    "SEO Settings": "إعدادات SEO",
    "Meta Keywords": "الكلمات المفتاحية",
    "Meta Description": "وصف Meta",
    "Save Settings": "حفظ الإعدادات"
}

# English translations (same as keys)
en_translations = {key: key for key in ar_translations.keys()}

# Create .mo files
os.makedirs('translations/ar/LC_MESSAGES', exist_ok=True)
os.makedirs('translations/en/LC_MESSAGES', exist_ok=True)

with open('translations/ar/LC_MESSAGES/messages.mo', 'wb') as f:
    f.write(create_mo_file(ar_translations))

with open('translations/en/LC_MESSAGES/messages.mo', 'wb') as f:
    f.write(create_mo_file(en_translations))

print("Created .mo files successfully!")
