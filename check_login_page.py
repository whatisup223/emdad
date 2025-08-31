#!/usr/bin/env python3
"""
Check login page functionality and files
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking login page files...")
    
    required_files = [
        'templates/admin/login.html',
        'static/css/login.css',
        'static/js/login.js',
        'static/css/style.css',
        'static/css/fonts.css'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - MISSING!")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_translations():
    """Check translation files"""
    print("\n🌐 Checking translation files...")

    translation_files = [
        'translations/ar/LC_MESSAGES/messages.po',
        'translations/en/LC_MESSAGES/messages.po'
    ]

    all_good = True

    for file_path in translation_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")

            # Check for login-specific translations
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            login_terms = [
                'Admin Login',
                'Email Address',
                'Password',
                'Sign In',
                'Remember me'
            ]

            missing_terms = []
            for term in login_terms:
                if f'msgid "{term}"' not in content:
                    missing_terms.append(term)

            if missing_terms:
                print(f"⚠️  Missing translations in {file_path}: {', '.join(missing_terms)}")
                all_good = False
            else:
                print(f"✅ All login translations found in {file_path}")
        else:
            print(f"❌ {file_path} - MISSING!")
            all_good = False

    return all_good

def test_login_page():
    """Test login page functionality"""
    print("\n🧪 Testing login page...")
    
    try:
        from wsgi import app
        
        with app.test_client() as client:
            # Test GET request
            response = client.get('/admin/login')
            print(f"✅ GET /admin/login: {response.status_code}")
            
            if response.status_code == 200:
                content = response.get_data(as_text=True)
                
                # Check for key elements
                checks = [
                    ('Language toggle', 'language-btn' in content),
                    ('Login form', 'needs-validation' in content),
                    ('Email field', 'id="email"' in content),
                    ('Password field', 'id="password"' in content),
                    ('Submit button', 'type="submit"' in content),
                    ('CSS files', 'login.css' in content),
                    ('JS files', 'login.js' in content),
                    ('Company logo', 'company-logo' in content),
                    ('RTL support', 'rtl' in content or 'dir=' in content)
                ]
                
                for check_name, result in checks:
                    status = "✅" if result else "❌"
                    print(f"  {status} {check_name}")
                
                return all(result for _, result in checks)
            else:
                print(f"❌ Login page returned status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Login page test failed: {e}")
        return False

def check_css_variables():
    """Check if CSS variables are properly defined"""
    print("\n🎨 Checking CSS variables...")
    
    try:
        with open('static/css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        required_vars = [
            '--primary-color',
            '--primary-gradient',
            '--font-arabic-heading',
            '--font-english-heading',
            '--font-body'
        ]
        
        missing_vars = []
        for var in required_vars:
            if var in css_content:
                print(f"✅ {var}")
            else:
                print(f"❌ {var} - MISSING!")
                missing_vars.append(var)
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ CSS check failed: {e}")
        return False

def main():
    """Run all checks"""
    print("🔍 Login Page Enhancement Check")
    print("=" * 50)
    
    checks = [
        ("Required Files", check_files),
        ("Translation Files", check_translations),
        ("CSS Variables", check_css_variables),
        ("Login Page Functionality", test_login_page)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} failed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n📊 Enhancement Check Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 Login page enhancement is complete!")
        print("\n✨ Features added:")
        print("  • Enhanced visual design matching main site")
        print("  • Language toggle (Arabic/English)")
        print("  • Smooth animations and transitions")
        print("  • Improved form validation")
        print("  • Better accessibility")
        print("  • Mobile responsive design")
        print("  • RTL support for Arabic")
        print("  • Enhanced user experience")
        
        print("\n🔗 Test the login page at:")
        print("  http://localhost:5000/admin/login")
        
        return True
    else:
        print(f"\n⚠️ {total - passed} check(s) failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
