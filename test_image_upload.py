#!/usr/bin/env python3
"""
Test script to verify image upload functionality
"""

import os
import sys
from PIL import Image
from io import BytesIO

def create_test_image():
    """Create a test image for upload testing"""
    
    # Create a simple test image
    img = Image.new('RGB', (300, 200), color='red')
    
    # Save to bytes
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_upload_directories():
    """Test that upload directories exist and are writable"""
    
    print("🔍 Testing Upload Directory Structure")
    print("=" * 50)
    
    # Check instance directory
    instance_path = 'instance'
    if os.path.exists(instance_path):
        print(f"✅ Instance directory exists: {instance_path}")
    else:
        print(f"❌ Instance directory missing: {instance_path}")
        return False
    
    # Check uploads directory
    uploads_path = os.path.join(instance_path, 'uploads')
    if os.path.exists(uploads_path):
        print(f"✅ Uploads directory exists: {uploads_path}")
    else:
        print(f"❌ Uploads directory missing: {uploads_path}")
        return False
    
    # Check news subdirectory
    news_path = os.path.join(uploads_path, 'news')
    if os.path.exists(news_path):
        print(f"✅ News directory exists: {news_path}")
    else:
        print(f"❌ News directory missing: {news_path}")
        return False
    
    # Test write permissions
    test_file = os.path.join(news_path, 'test_write.txt')
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print(f"✅ News directory is writable")
    except Exception as e:
        print(f"❌ News directory not writable: {e}")
        return False
    
    return True

def test_image_processing():
    """Test image creation and processing"""
    
    print("\n🖼️  Testing Image Processing")
    print("-" * 30)
    
    try:
        # Create test image
        img_bytes = create_test_image()
        print(f"✅ Test image created ({len(img_bytes.getvalue())} bytes)")
        
        # Test saving to file
        test_path = os.path.join('instance', 'uploads', 'news', 'test_image.jpg')
        with open(test_path, 'wb') as f:
            f.write(img_bytes.getvalue())
        
        # Verify file exists
        if os.path.exists(test_path):
            file_size = os.path.getsize(test_path)
            print(f"✅ Test image saved successfully ({file_size} bytes)")
            
            # Clean up
            os.remove(test_path)
            print(f"✅ Test image cleaned up")
            
            return True
        else:
            print(f"❌ Test image not saved")
            return False
            
    except Exception as e:
        print(f"❌ Image processing error: {e}")
        return False

def test_url_generation():
    """Test URL generation for uploaded files"""
    
    print("\n🔗 Testing URL Generation")
    print("-" * 30)
    
    try:
        from app import create_app
        from flask import url_for
        
        app = create_app('development')
        
        with app.test_request_context():
            # Test URL generation
            test_filename = 'news/test_image.jpg'
            url = url_for('main.uploaded_file', filename=test_filename)
            expected_url = f'/uploads/{test_filename}'
            
            if url == expected_url:
                print(f"✅ URL generation correct: {url}")
                return True
            else:
                print(f"❌ URL generation incorrect: {url} (expected: {expected_url})")
                return False
                
    except Exception as e:
        print(f"❌ URL generation error: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🧪 Image Upload Test Suite")
    print("=" * 50)
    
    tests = [
        ("Upload Directories", test_upload_directories),
        ("Image Processing", test_image_processing),
        ("URL Generation", test_url_generation)
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
        print("\n🎉 All tests passed! Image upload should work correctly.")
        print("\n💡 Next steps:")
        print("   1. Start your Flask application")
        print("   2. Go to Admin > News > Add New Article")
        print("   3. Try uploading an image")
        print("   4. Check that the image appears in the news list")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
