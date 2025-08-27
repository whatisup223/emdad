#!/usr/bin/env python3
"""
Test script to verify translations are working correctly
"""

import os
import sys
from flask import Flask
from flask_babel import Babel, gettext, ngettext
from app import create_app

def test_translations():
    """Test that translations are working correctly"""
    
    print("🔍 Testing Translation System")
    print("=" * 50)
    
    # Create app
    app = create_app('development')
    
    with app.test_request_context():
        # Test Arabic translations
        print("\n📝 Testing Arabic Translations:")
        print("-" * 30)

        # Simulate Arabic locale
        from flask import session
        session['language'] = 'ar'
        
        # Test common translations
        test_strings = [
            'News Management',
            'Add New Article', 
            'Edit Article',
            'Article Details',
            'English Content',
            'Arabic Content',
            'Draft',
            'Published',
            'Featured',
            'Save Draft',
            'Publish',
            'Back to News',
            'Search articles...',
            'No articles found'
        ]
        
        for string in test_strings:
            try:
                from simple_translations import translate
                translated = translate(string, 'ar')
                status = "✅" if translated != string else "❌"
                print(f"{status} '{string}' -> '{translated}'")
            except Exception as e:
                print(f"❌ Error translating '{string}': {e}")
        
        # Test English translations
        print("\n📝 Testing English Translations:")
        print("-" * 30)
        
        session['language'] = 'en'
        
        for string in test_strings:
            try:
                from simple_translations import translate
                translated = translate(string, 'en')
                status = "✅" if translated == string else "❌"
                print(f"{status} '{string}' -> '{translated}'")
            except Exception as e:
                print(f"❌ Error translating '{string}': {e}")
    
    print("\n🎯 Translation Files Check:")
    print("-" * 30)
    
    # Check translation files exist
    ar_po = 'translations/ar/LC_MESSAGES/messages.po'
    ar_mo = 'translations/ar/LC_MESSAGES/messages.mo'
    en_po = 'translations/en/LC_MESSAGES/messages.po'
    en_mo = 'translations/en/LC_MESSAGES/messages.mo'
    
    files_to_check = [ar_po, ar_mo, en_po, en_mo]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - Missing!")
    
    print("\n🔧 Configuration Check:")
    print("-" * 30)
    
    with app.test_request_context():
        # Check app configuration
        languages = app.config.get('LANGUAGES', {})
        default_locale = app.config.get('BABEL_DEFAULT_LOCALE', 'en')

        print(f"✅ Supported Languages: {list(languages.keys())}")
        print(f"✅ Default Locale: {default_locale}")

        # Check Babel is initialized
        try:
            from flask_babel import get_locale
            current_locale = str(get_locale())
            print(f"✅ Current Locale: {current_locale}")
        except Exception as e:
            print(f"❌ Babel Error: {e}")
    
    print("\n🌐 News Form Translation Test:")
    print("-" * 30)
    
    with app.test_request_context():
        from app.forms import NewsForm

        # Test form in Arabic
        session['language'] = 'ar'
        form_ar = NewsForm()

        # Test form in English
        session['language'] = 'en'
        form_en = NewsForm()

        # Check some field labels
        fields_to_check = ['title_en', 'title_ar', 'status', 'featured']

        for field_name in fields_to_check:
            if hasattr(form_ar, field_name) and hasattr(form_en, field_name):
                ar_label = getattr(form_ar, field_name).label.text
                en_label = getattr(form_en, field_name).label.text
                print(f"✅ {field_name}: AR='{ar_label}' | EN='{en_label}'")
            else:
                print(f"❌ Field '{field_name}' not found in form")
    
    print("\n🎉 Translation Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_translations()
