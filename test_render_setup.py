#!/usr/bin/env python3
"""
Test script to verify Render deployment setup
"""

import os
import sys

def test_environment():
    """Test environment variables and setup"""
    print("🔍 Testing Environment Setup")
    print("=" * 50)
    
    # Test Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Test environment variables
    env_vars = [
        'FLASK_ENV',
        'DATABASE_URL',
        'SECRET_KEY',
        'PORT'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NOT_SET')
        print(f"📝 {var}: {value}")
    
    # Test current directory
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"📁 Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    
    # Test file existence
    required_files = [
        'wsgi.py',
        'app.py',
        'config.py',
        'requirements.txt',
        'app/__init__.py',
        'app/models.py'
    ]
    
    print("\n📋 Required Files Check:")
    for file_path in required_files:
        exists = "✅" if os.path.exists(file_path) else "❌"
        print(f"{exists} {file_path}")

def test_imports():
    """Test critical imports"""
    print("\n🔧 Testing Imports")
    print("=" * 30)
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except Exception as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        from app import create_app
        print("✅ create_app import successful")
    except Exception as e:
        print(f"❌ create_app import failed: {e}")
        return False
    
    try:
        import app.models
        print("✅ app.models import successful")
    except Exception as e:
        print(f"❌ app.models import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test Flask app creation"""
    print("\n🚀 Testing App Creation")
    print("=" * 30)
    
    try:
        from app import create_app
        
        # Test with production config
        app = create_app('production')
        print(f"✅ Production app created: {app}")
        print(f"   App name: {app.name}")
        print(f"   Debug mode: {app.debug}")
        
        # Test app context
        with app.app_context():
            print("✅ App context works")
            
            # Test database
            try:
                from app.models import db
                print("✅ Database models accessible")
            except Exception as e:
                print(f"⚠️ Database models issue: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_wsgi():
    """Test WSGI module"""
    print("\n🌐 Testing WSGI Module")
    print("=" * 30)
    
    try:
        import wsgi
        print("✅ WSGI module imported")
        
        app = wsgi.app
        print(f"✅ WSGI app accessible: {app}")
        print(f"   App type: {type(app)}")
        
        return True
        
    except Exception as e:
        print(f"❌ WSGI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Render Deployment Test Suite")
    print("=" * 50)
    
    # Set production environment for testing
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('DATABASE_URL', 'sqlite:////tmp/test.db')
    os.environ.setdefault('SECRET_KEY', 'test-secret-key')
    
    tests = [
        ("Environment Setup", test_environment),
        ("Critical Imports", test_imports),
        ("App Creation", test_app_creation),
        ("WSGI Module", test_wsgi)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
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
        print("\n🎉 All tests passed! Ready for Render deployment!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Check issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
