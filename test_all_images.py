#!/usr/bin/env python3
"""
Test script to verify all image URLs are working correctly
"""

import os
import re
from pathlib import Path

def find_image_urls_in_templates():
    """Find all image URL references in templates"""
    
    print("🔍 Scanning Templates for Image URLs")
    print("=" * 50)
    
    template_dir = Path("templates")
    issues = []
    fixed_count = 0
    total_count = 0
    
    # Patterns to look for
    old_patterns = [
        r"url_for\('static',\s*filename='uploads/([^']+)'\)",
        r"url_for\('uploaded_file',\s*filename='([^']+)'\)",
    ]
    
    correct_pattern = r"url_for\('main\.uploaded_file',\s*filename='([^']+)'\)"
    
    for template_file in template_dir.rglob("*.html"):
        if template_file.is_file():
            try:
                content = template_file.read_text(encoding='utf-8')
                
                # Check for old patterns
                for pattern in old_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        total_count += 1
                        issues.append({
                            'file': str(template_file),
                            'pattern': pattern,
                            'match': match,
                            'type': 'old_pattern'
                        })
                
                # Check for correct patterns
                correct_matches = re.findall(correct_pattern, content)
                fixed_count += len(correct_matches)
                total_count += len(correct_matches)
                
                if correct_matches:
                    print(f"✅ {template_file.name}: {len(correct_matches)} correct URLs")
                
            except Exception as e:
                print(f"❌ Error reading {template_file}: {e}")
    
    # Report issues
    if issues:
        print(f"\n⚠️  Found {len(issues)} URLs that need fixing:")
        print("-" * 40)
        
        for issue in issues:
            print(f"❌ {issue['file']}")
            print(f"   Pattern: {issue['pattern']}")
            print(f"   Match: {issue['match']}")
            print()
    else:
        print(f"\n✅ No issues found!")
    
    print(f"\n📊 Summary:")
    print(f"   Total URLs found: {total_count}")
    print(f"   Correctly formatted: {fixed_count}")
    print(f"   Need fixing: {len(issues)}")
    
    return len(issues) == 0

def test_url_generation():
    """Test URL generation for different file types"""
    
    print("\n🔗 Testing URL Generation")
    print("=" * 30)
    
    try:
        from app import create_app
        from flask import url_for
        
        app = create_app('development')
        
        with app.test_request_context():
            # Test different file types
            test_files = [
                ('news/test-article.jpg', 'News image'),
                ('products/test-product.png', 'Product image'),
                ('categories/test-category.webp', 'Category image'),
                ('gallery/test-gallery.jpg', 'Gallery image'),
                ('certifications/test-cert.png', 'Certification logo')
            ]
            
            all_passed = True
            
            for filename, description in test_files:
                try:
                    url = url_for('main.uploaded_file', filename=filename)
                    expected = f'/uploads/{filename}'
                    
                    if url == expected:
                        print(f"✅ {description}: {url}")
                    else:
                        print(f"❌ {description}: {url} (expected: {expected})")
                        all_passed = False
                        
                except Exception as e:
                    print(f"❌ {description}: Error - {e}")
                    all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"❌ URL generation test failed: {e}")
        return False

def check_upload_directories():
    """Check that all upload directories exist"""
    
    print("\n📁 Checking Upload Directories")
    print("=" * 30)
    
    base_path = Path("instance/uploads")
    required_dirs = [
        'news',
        'products', 
        'categories',
        'gallery',
        'certifications',
        'rfq'
    ]
    
    all_exist = True
    
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    
    print("🧪 Complete Image URL Test Suite")
    print("=" * 50)
    
    tests = [
        ("Template URL Scanning", find_image_urls_in_templates),
        ("URL Generation", test_url_generation),
        ("Upload Directories", check_upload_directories)
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
    print("\n📊 Final Test Results")
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
        print("\n🎉 All tests passed! Image URLs are working correctly.")
        print("\n💡 What this means:")
        print("   ✅ All templates use the correct URL format")
        print("   ✅ URL generation works properly")
        print("   ✅ Upload directories exist")
        print("   ✅ Images should display correctly on all pages")
        
        print("\n🚀 Next steps:")
        print("   1. Start your Flask application")
        print("   2. Upload some test images through the admin panel")
        print("   3. Check that images appear correctly on:")
        print("      - Admin news list")
        print("      - Homepage news section")
        print("      - News detail pages")
        print("      - Product pages")
        print("      - Gallery")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please review the issues above before testing image uploads.")

if __name__ == "__main__":
    main()
