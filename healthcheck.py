#!/usr/bin/env python3
"""
Health check script for Emdad Global application
"""

import sys
import os
import requests
from urllib.parse import urljoin

def check_app_health(base_url="http://localhost:5000"):
    """Check if the application is running and healthy"""
    
    print(f"🏥 Health Check for {base_url}")
    print("=" * 50)
    
    try:
        # Check main page
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Main page is accessible")
        else:
            print(f"❌ Main page returned status {response.status_code}")
            return False
            
        # Check admin login page
        admin_url = urljoin(base_url, "/admin/login")
        response = requests.get(admin_url, timeout=10)
        if response.status_code == 200:
            print("✅ Admin login page is accessible")
        else:
            print(f"❌ Admin login page returned status {response.status_code}")
            return False
            
        # Check API health endpoint (if exists)
        api_url = urljoin(base_url, "/api/health")
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                print("✅ API health endpoint is accessible")
            else:
                print("ℹ️  API health endpoint not available (optional)")
        except:
            print("ℹ️  API health endpoint not available (optional)")
            
        print("\n🎉 Application is healthy!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application")
        print("   Make sure the application is running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Application is responding too slowly")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_database_connection():
    """Check database connection"""
    
    print("\n🗄️  Database Connection Check")
    print("-" * 30)
    
    try:
        from app import create_app
        from app.models import db, User
        
        app = create_app(os.environ.get('FLASK_ENV', 'production'))
        
        with app.app_context():
            # Try to query the database
            user_count = User.query.count()
            print(f"✅ Database connection successful")
            print(f"   Users in database: {user_count}")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Run all health checks"""
    
    print("🧪 Emdad Global Health Check Suite")
    print("=" * 50)
    
    # Check if we're running in production
    flask_env = os.environ.get('FLASK_ENV', 'development')
    print(f"Environment: {flask_env}")
    
    # Determine base URL
    if flask_env == 'production':
        base_url = os.environ.get('SITE_URL', 'https://emdad-global.onrender.com')
    else:
        base_url = "http://localhost:5000"
    
    # Run checks
    checks = [
        ("Database Connection", check_database_connection),
        ("Application Health", lambda: check_app_health(base_url))
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n📊 Health Check Summary")
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
        print("\n🎉 All health checks passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
