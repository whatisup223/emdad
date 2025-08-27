#!/usr/bin/env python3
"""
Test script to verify footer and hero changes
"""

import os
from pathlib import Path

def test_hero_background():
    """Test hero background image"""
    
    print("🖼️  Testing Hero Background")
    print("=" * 30)
    
    # Check if new hero image exists
    hero_image = Path("static/images/hero-bg.webp")
    if hero_image.exists():
        print(f"✅ Hero background image exists: {hero_image}")
        print(f"   Size: {hero_image.stat().st_size} bytes")
    else:
        print(f"❌ Hero background image missing: {hero_image}")
        return False
    
    # Check CSS references
    css_file = Path("static/css/style.css")
    if css_file.exists():
        content = css_file.read_text(encoding='utf-8')
        if '/static/images/hero-bg.webp' in content:
            print("✅ CSS references correct hero background path")
        else:
            print("❌ CSS does not reference correct hero background path")
            return False
    else:
        print("❌ CSS file not found")
        return False
    
    return True

def test_logo():
    """Test logo image"""
    
    print("\n🏷️  Testing Logo")
    print("=" * 20)
    
    # Check if new logo exists
    logo_image = Path("static/images/logo.png")
    if logo_image.exists():
        print(f"✅ Logo image exists: {logo_image}")
        print(f"   Size: {logo_image.stat().st_size} bytes")
    else:
        print(f"❌ Logo image missing: {logo_image}")
        return False
    
    # Check template references
    template_file = Path("templates/base.html")
    if template_file.exists():
        content = template_file.read_text(encoding='utf-8')
        if "static/images/logo.png" in content:
            print("✅ Template references correct logo path")
        else:
            print("❌ Template does not reference correct logo path")
            return False
    else:
        print("❌ Base template not found")
        return False
    
    return True

def test_footer_structure():
    """Test footer structure"""
    
    print("\n🦶 Testing Footer Structure")
    print("=" * 30)
    
    template_file = Path("templates/base.html")
    if not template_file.exists():
        print("❌ Base template not found")
        return False
    
    content = template_file.read_text(encoding='utf-8')
    
    # Check for footer sections
    footer_sections = [
        'footer-section',
        'footer-wave-top',
        'News Update',
        'Contact Info',
        'social-links',
        'newsletter-signup'
    ]
    
    missing_sections = []
    for section in footer_sections:
        if section in content:
            print(f"✅ Footer section found: {section}")
        else:
            print(f"❌ Footer section missing: {section}")
            missing_sections.append(section)
    
    return len(missing_sections) == 0

def test_translations():
    """Test footer translations"""
    
    print("\n🌐 Testing Footer Translations")
    print("=" * 35)
    
    try:
        from simple_translations import translate
        
        # Test footer translations
        footer_translations = [
            'News Update',
            'Contact Info', 
            'Facebook',
            'Twitter',
            'YouTube',
            'Instagram',
            'Terms of Use',
            'Privacy Policy'
        ]
        
        all_translated = True
        
        for text in footer_translations:
            ar_translation = translate(text, 'ar')
            en_translation = translate(text, 'en')
            
            ar_status = "✅" if ar_translation != text else "❌"
            en_status = "✅" if en_translation == text else "❌"
            
            print(f"{ar_status}{en_status} {text}")
            print(f"   AR: {ar_translation}")
            print(f"   EN: {en_translation}")
            
            if ar_translation == text:
                all_translated = False
        
        return all_translated
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def test_css_enhancements():
    """Test CSS enhancements"""
    
    print("\n🎨 Testing CSS Enhancements")
    print("=" * 30)
    
    css_file = Path("static/css/style.css")
    if not css_file.exists():
        print("❌ CSS file not found")
        return False
    
    content = css_file.read_text(encoding='utf-8')
    
    # Check for new CSS classes
    css_classes = [
        '.footer-section',
        '.footer-wave-top',
        '.social-link',
        '.footer-news',
        '.newsletter-signup',
        '.contact-item'
    ]
    
    missing_classes = []
    for css_class in css_classes:
        if css_class in content:
            print(f"✅ CSS class found: {css_class}")
        else:
            print(f"❌ CSS class missing: {css_class}")
            missing_classes.append(css_class)
    
    return len(missing_classes) == 0

def main():
    """Run all tests"""
    
    print("🧪 Footer and Hero Test Suite")
    print("=" * 50)
    
    tests = [
        ("Hero Background", test_hero_background),
        ("Logo", test_logo),
        ("Footer Structure", test_footer_structure),
        ("Translations", test_translations),
        ("CSS Enhancements", test_css_enhancements)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        print("\n💡 Changes completed successfully:")
        print("   ✅ Hero background updated to hero-bg.webp")
        print("   ✅ Logo updated to logo.png")
        print("   ✅ Footer redesigned with new sections")
        print("   ✅ News Update section added")
        print("   ✅ Contact Info section enhanced")
        print("   ✅ All sections translated to Arabic")
        print("   ✅ CSS enhancements applied")
        
        print("\n🚀 Next steps:")
        print("   1. Start your Flask application")
        print("   2. Check the homepage hero section")
        print("   3. Scroll down to see the new footer")
        print("   4. Test language switching")
        print("   5. Verify all links and functionality")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please review the issues above.")

if __name__ == "__main__":
    main()
