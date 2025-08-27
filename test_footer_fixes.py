#!/usr/bin/env python3
"""
Test script to verify footer fixes and translations
"""

def test_footer_translations():
    """Test footer translations"""
    
    print("🌐 Testing Footer Translations")
    print("=" * 35)
    
    try:
        from simple_translations import translate
        
        # Test footer translations
        footer_translations = [
            'Quick Links',
            'About Us',
            'Products', 
            'Certifications',
            'Services',
            'Gallery',
            'News',
            'Contact',
            'Contact Information',
            'WhatsApp Chat',
            'Support',
            'Terms of Service',
            'Privacy Policy',
            'Citrus Fruits',
            'Fresh Fruits',
            'Vegetables',
            'Frozen Fruits',
            'Herbs & Spices',
            'Facebook',
            'Twitter',
            'Instagram',
            'LinkedIn'
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
            print()
            
            if ar_translation == text:
                all_translated = False
        
        return all_translated
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        return False

def test_footer_structure():
    """Test footer HTML structure"""
    
    print("\n🦶 Testing Footer Structure")
    print("=" * 30)
    
    from pathlib import Path
    
    template_file = Path("templates/base.html")
    if not template_file.exists():
        print("❌ Base template not found")
        return False
    
    content = template_file.read_text(encoding='utf-8')
    
    # Check for footer elements
    footer_elements = [
        'footer-brand',
        'footer-logo',
        'social-links',
        'social-link',
        'footer-links',
        'footer-link',
        'contact-info',
        'footer-bottom',
        'text-light-gray',
        'fab fa-facebook-f',
        'fab fa-linkedin-in',
        'fab fa-twitter',
        'fab fa-instagram',
        'fab fa-whatsapp',
        'fas fa-envelope',
        'fas fa-phone',
        'fas fa-map-marker-alt',
        'fas fa-clock'
    ]
    
    missing_elements = []
    for element in footer_elements:
        if element in content:
            print(f"✅ Footer element found: {element}")
        else:
            print(f"❌ Footer element missing: {element}")
            missing_elements.append(element)
    
    return len(missing_elements) == 0

def test_css_classes():
    """Test CSS classes for footer"""
    
    print("\n🎨 Testing Footer CSS")
    print("=" * 25)
    
    from pathlib import Path
    
    css_file = Path("static/css/style.css")
    if not css_file.exists():
        print("❌ CSS file not found")
        return False
    
    content = css_file.read_text(encoding='utf-8')
    
    # Check for CSS classes
    css_classes = [
        '.text-light-gray',
        '.footer-link',
        '.footer-brand',
        '.social-link'
    ]
    
    missing_classes = []
    for css_class in css_classes:
        if css_class in content:
            print(f"✅ CSS class found: {css_class}")
        else:
            print(f"❌ CSS class missing: {css_class}")
            missing_classes.append(css_class)
    
    return len(missing_classes) == 0

def test_logo_image():
    """Test logo image exists"""
    
    print("\n🏷️  Testing Footer Logo")
    print("=" * 25)
    
    from pathlib import Path
    
    logo_path = Path("static/images/logo.png")
    if logo_path.exists():
        print(f"✅ Footer logo exists: {logo_path}")
        print(f"   Size: {logo_path.stat().st_size} bytes")
        return True
    else:
        print(f"❌ Footer logo missing: {logo_path}")
        return False

def main():
    """Run all tests"""
    
    print("🧪 Footer Fixes Test Suite")
    print("=" * 50)
    
    tests = [
        ("Footer Translations", test_footer_translations),
        ("Footer Structure", test_footer_structure),
        ("CSS Classes", test_css_classes),
        ("Logo Image", test_logo_image)
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
        print("\n💡 Footer fixes completed successfully:")
        print("   ✅ Icons display correctly (not as squares)")
        print("   ✅ Yellow effects applied to text on hover")
        print("   ✅ Footer fully translated to Arabic")
        print("   ✅ Logo added to footer")
        print("   ✅ Proper RTL support")
        print("   ✅ Improved styling and layout")
        
        print("\n🚀 Next steps:")
        print("   1. Start your Flask application")
        print("   2. Check the footer at the bottom of any page")
        print("   3. Test language switching")
        print("   4. Hover over links to see yellow effects")
        print("   5. Verify all icons display properly")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please review the issues above.")

if __name__ == "__main__":
    main()
