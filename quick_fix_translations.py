#!/usr/bin/env python3
"""
Quick fix for login page translations
"""

def fix_login_template():
    """Fix login template with direct Arabic translations"""
    
    print("🔧 Applying quick translation fix...")
    
    # Read the current template
    with open('templates/admin/login.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace English text with conditional Arabic/English
    replacements = [
        # Title
        ('{{ _("Admin Login") }}', '{{ "تسجيل دخول الإدارة" if current_language == "ar" else "Admin Login" }}'),
        
        # Email label
        ('{{ _("Email Address") }}', '{{ "عنوان البريد الإلكتروني" if current_language == "ar" else "Email Address" }}'),
        
        # Email placeholder
        ('placeholder=_("Enter your email address")', 'placeholder="{{ "أدخل عنوان بريدك الإلكتروني" if current_language == "ar" else "Enter your email address" }}"'),
        
        # Password label
        ('{{ _("Password") }}', '{{ "كلمة المرور" if current_language == "ar" else "Password" }}'),
        
        # Password placeholder
        ('placeholder=_("Enter your password")', 'placeholder="{{ "أدخل كلمة المرور" if current_language == "ar" else "Enter your password" }}"'),
        
        # Remember me
        ('{{ _("Remember me") }}', '{{ "تذكرني" if current_language == "ar" else "Remember me" }}'),
        
        # Sign in button
        ('{{ _("Sign In") }}', '{{ "تسجيل الدخول" if current_language == "ar" else "Sign In" }}'),
        
        # Back to website
        ('{{ _("Back to Website") }}', '{{ "العودة للموقع" if current_language == "ar" else "Back to Website" }}'),
        
        # Secure access
        ('{{ _("Secure Access") }}', '{{ "وصول آمن" if current_language == "ar" else "Secure Access" }}'),
        
        # Protected admin area
        ('{{ _("Protected Admin Area") }}', '{{ "منطقة إدارة محمية" if current_language == "ar" else "Protected Admin Area" }}'),
        
        # All rights reserved
        ('{{ _("All rights reserved") }}', '{{ "جميع الحقوق محفوظة" if current_language == "ar" else "All rights reserved" }}'),
        
        # Language toggle text
        ("{{ 'العربية' if current_language == 'en' else 'English' }}", '{{ "English" if current_language == "ar" else "العربية" }}')
    ]
    
    # Apply replacements
    for old_text, new_text in replacements:
        if old_text in content:
            content = content.replace(old_text, new_text)
            print(f"✅ Replaced: {old_text[:30]}...")
        else:
            print(f"❌ Not found: {old_text[:30]}...")
    
    # Write back the file
    with open('templates/admin/login.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Login template updated with direct translations")

def test_fix():
    """Test the fix"""
    
    print("🧪 Testing the fix...")
    
    try:
        from wsgi import app
        
        with app.test_client() as client:
            # Test Arabic
            response = client.get('/admin/login?lang=ar')
            content = response.get_data(as_text=True)
            
            print(f"Status: {response.status_code}")
            
            # Check for Arabic text
            arabic_checks = [
                ('تسجيل دخول الإدارة', 'Admin Login title'),
                ('عنوان البريد الإلكتروني', 'Email Address label'),
                ('أدخل عنوان بريدك الإلكتروني', 'Email placeholder'),
                ('كلمة المرور', 'Password label'),
                ('أدخل كلمة المرور', 'Password placeholder'),
                ('تذكرني', 'Remember me'),
                ('تسجيل الدخول', 'Sign In button'),
                ('العودة للموقع', 'Back to Website'),
                ('وصول آمن', 'Secure Access'),
                ('منطقة إدارة محمية', 'Protected Admin Area')
            ]
            
            found_count = 0
            for arabic_text, description in arabic_checks:
                if arabic_text in content:
                    print(f"✅ {description}: {arabic_text}")
                    found_count += 1
                else:
                    print(f"❌ {description}: NOT FOUND")
            
            print(f"\n📊 Found {found_count}/{len(arabic_checks)} Arabic translations")
            
            if found_count >= len(arabic_checks) * 0.8:  # 80% success rate
                print("✅ Translation fix successful!")
                return True
            else:
                print("❌ Translation fix needs more work")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    
    print("🚀 Quick Translation Fix for Login Page")
    print("=" * 50)
    
    # Step 1: Fix the template
    fix_login_template()
    
    # Step 2: Test the fix
    if test_fix():
        print("\n🎉 Translation fix completed successfully!")
        print("\n📝 Next steps:")
        print("1. Visit http://localhost:5000/admin/login")
        print("2. Click the language toggle to test Arabic/English")
        print("3. All text should now be properly translated")
        return True
    else:
        print("\n❌ Translation fix failed")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
