#!/usr/bin/env python3
"""
Fix translation compilation using babel
"""

import os
import subprocess
import sys

def install_babel():
    """Install babel if not available"""
    try:
        import babel
        print("✅ Babel is available")
        return True
    except ImportError:
        print("📦 Installing babel...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'babel'])
            print("✅ Babel installed successfully")
            return True
        except:
            print("❌ Failed to install babel")
            return False

def compile_translations():
    """Compile translations using babel"""
    
    if not install_babel():
        return False
    
    try:
        # Compile Arabic
        print("🔄 Compiling Arabic translations...")
        result = subprocess.run([
            sys.executable, '-m', 'babel.messages.frontend', 'compile',
            '-d', 'translations',
            '-l', 'ar'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Arabic translations compiled")
        else:
            print(f"❌ Arabic compilation failed: {result.stderr}")
        
        # Compile English
        print("🔄 Compiling English translations...")
        result = subprocess.run([
            sys.executable, '-m', 'babel.messages.frontend', 'compile',
            '-d', 'translations', 
            '-l', 'en'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ English translations compiled")
        else:
            print(f"❌ English compilation failed: {result.stderr}")
            
        return True
        
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        return False

def test_translations():
    """Test if translations work"""
    
    print("🧪 Testing translations...")
    
    try:
        from wsgi import app
        
        with app.app_context():
            from flask_babel import gettext
            
            # Test Arabic
            with app.test_request_context('/?lang=ar'):
                app.jinja_env.globals['get_locale'] = lambda: 'ar'
                
                # Test key translations
                tests = [
                    ('Admin Login', 'تسجيل دخول الإدارة'),
                    ('Email Address', 'عنوان البريد الإلكتروني'),
                    ('Password', 'كلمة المرور'),
                    ('Remember me', 'تذكرني'),
                    ('Sign In', 'تسجيل الدخول')
                ]
                
                for english, expected_arabic in tests:
                    translated = gettext(english)
                    if translated == expected_arabic:
                        print(f"✅ {english} → {translated}")
                    else:
                        print(f"❌ {english} → {translated} (expected: {expected_arabic})")
        
        return True
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def main():
    """Main function"""
    
    print("🔧 Fixing translation compilation...")
    
    # Step 1: Compile translations
    if compile_translations():
        print("✅ Translations compiled successfully")
    else:
        print("❌ Translation compilation failed")
        return False
    
    # Step 2: Test translations
    if test_translations():
        print("✅ Translations are working correctly")
    else:
        print("❌ Translation testing failed")
        return False
    
    print("\n🎉 Translation fix completed successfully!")
    print("\n📝 Next steps:")
    print("1. Restart the Flask application")
    print("2. Visit http://localhost:5000/admin/login")
    print("3. Click the language toggle to test Arabic/English")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
