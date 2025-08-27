#!/usr/bin/env python3
"""Check and test translation coverage"""

import os
import re
from simple_translations import TRANSLATIONS

def find_translation_strings_in_templates():
    """Find all _('...') strings in templates"""
    template_dir = 'templates'
    translation_strings = set()
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Find all _('...') patterns
                        matches = re.findall(r"_\(['\"]([^'\"]+)['\"]\)", content)
                        translation_strings.update(matches)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return translation_strings

def check_missing_translations():
    """Check for missing translations"""
    template_strings = find_translation_strings_in_templates()
    ar_translations = TRANSLATIONS.get('ar', {})
    
    missing_translations = []
    for string in template_strings:
        if string not in ar_translations:
            missing_translations.append(string)
    
    print(f"Found {len(template_strings)} translation strings in templates")
    print(f"Found {len(ar_translations)} Arabic translations")
    print(f"Missing {len(missing_translations)} translations")
    
    if missing_translations:
        print("\nMissing translations:")
        for string in sorted(missing_translations):
            print(f"  '{string}': 'TRANSLATION_NEEDED',")
    else:
        print("\n✅ All translations are covered!")
    
    return missing_translations

def generate_missing_translations_dict(missing_translations):
    """Generate a dictionary of missing translations for easy copy-paste"""
    if not missing_translations:
        return
    
    print("\n" + "="*50)
    print("COPY THIS TO simple_translations.py:")
    print("="*50)
    
    for string in sorted(missing_translations):
        # Try to provide a reasonable Arabic translation
        # This is a basic attempt - manual review is recommended
        arabic_translation = auto_translate_to_arabic(string)
        print(f'        "{string}": "{arabic_translation}",')

def auto_translate_to_arabic(english_text):
    """Basic auto-translation - needs manual review"""
    # This is a very basic mapping - real translation should be done manually
    basic_translations = {
        'Add New': 'إضافة جديد',
        'Edit': 'تعديل',
        'Delete': 'حذف',
        'View': 'عرض',
        'Save': 'حفظ',
        'Cancel': 'إلغاء',
        'Back': 'رجوع',
        'Next': 'التالي',
        'Previous': 'السابق',
        'Search': 'البحث',
        'Filter': 'تصفية',
        'All': 'الكل',
        'Active': 'نشط',
        'Inactive': 'غير نشط',
        'Yes': 'نعم',
        'No': 'لا',
        'Name': 'الاسم',
        'Description': 'الوصف',
        'Status': 'الحالة',
        'Date': 'التاريخ',
        'Actions': 'الإجراءات',
        'Title': 'العنوان',
        'Image': 'الصورة',
        'Category': 'الفئة',
        'Product': 'المنتج',
        'User': 'المستخدم',
        'Email': 'البريد الإلكتروني',
        'Phone': 'الهاتف',
        'Address': 'العنوان',
        'Company': 'الشركة',
        'Message': 'الرسالة',
        'Priority': 'الأولوية',
        'High': 'عالية',
        'Medium': 'متوسطة',
        'Low': 'منخفضة',
        'New': 'جديد',
        'Draft': 'مسودة',
        'Published': 'منشور',
        'Archived': 'مؤرشف',
        'Completed': 'مكتمل',
        'Cancelled': 'ملغي',
        'In Progress': 'قيد المعالجة',
        'Pending': 'معلق'
    }
    
    # Check if we have a direct translation
    if english_text in basic_translations:
        return basic_translations[english_text]
    
    # For compound phrases, try to break them down
    for eng, ar in basic_translations.items():
        if eng.lower() in english_text.lower():
            return english_text.replace(eng, ar)
    
    # If no translation found, return the original with a note
    return f"[ترجمة مطلوبة] {english_text}"

if __name__ == "__main__":
    print("Checking translation coverage...")
    missing = check_missing_translations()
    if missing:
        generate_missing_translations_dict(missing)
    
    print("\n" + "="*50)
    print("Translation check complete!")
    print("="*50)
