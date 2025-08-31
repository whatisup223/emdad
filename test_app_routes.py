#!/usr/bin/env python3
"""
Quick test for app routes
"""

def test_home_page():
    """Test home page route"""
    try:
        from wsgi import app
        
        with app.test_client() as client:
            response = client.get('/')
            print(f"Home page status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Home page works!")
                return True
            else:
                print(f"❌ Home page failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Home page test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_page():
    """Test admin login page"""
    try:
        from wsgi import app
        
        with app.test_client() as client:
            response = client.get('/admin/login')
            print(f"Admin login page status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Admin login page works!")
                return True
            else:
                print(f"❌ Admin login page failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Admin login test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing App Routes")
    print("=" * 30)
    
    home_ok = test_home_page()
    admin_ok = test_admin_page()
    
    if home_ok and admin_ok:
        print("\n🎉 All route tests passed!")
    else:
        print("\n⚠️ Some route tests failed!")
