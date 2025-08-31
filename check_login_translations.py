#!/usr/bin/env python3
"""
Check login page translations
"""

def check_translations():
    """Check if all login translations exist"""
    
    # Required translations for login page
    required_translations = [
        'Admin Login',
        'Email Address', 
        'Enter your email address',
        'Password',
        'Enter your password',
        'Remember me',
        'Sign In',
        'Back to Website',
        'Secure Access',
        'Protected Admin Area',
        'All rights reserved',
        'Hide password',
        'Show password',
        'Signing in...',
        'Loading...'
    ]
    
    print("🔍 Checking Arabic translations...")
    
    # Check Arabic translations
    with open('translations/ar/LC_MESSAGES/messages.po', 'r', encoding='utf-8') as f:
        ar_content = f.read()
    
    missing_ar = []
    for term in required_translations:
        if f'msgid "{term}"' not in ar_content:
            missing_ar.append(term)
        else:
            print(f"✅ {term}")
    
    if missing_ar:
        print("\n❌ Missing Arabic translations:")
        for term in missing_ar:
            print(f"  - {term}")
        return False
    else:
        print("\n✅ All Arabic translations found!")
        return True

if __name__ == "__main__":
    check_translations()
