#!/usr/bin/env python3
"""
Script to check if the project is ready for Render deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} - MISSING!")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and return status"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        files_count = len(os.listdir(dir_path))
        print(f"✅ {description}: {dir_path} ({files_count} items)")
        return True
    else:
        print(f"❌ {description}: {dir_path} - MISSING!")
        return False

def check_requirements_file():
    """Check requirements.txt content"""
    print("\n📦 Checking requirements.txt content...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    required_packages = [
        'Flask',
        'gunicorn',
        'psycopg2-binary',
        'Flask-SQLAlchemy',
        'Flask-Migrate'
    ]
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        return False
    else:
        print("✅ All required packages found in requirements.txt")
        return True

def check_config_file():
    """Check config.py for production settings"""
    print("\n⚙️  Checking config.py...")
    
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        return False
    
    with open('config.py', 'r') as f:
        content = f.read()
    
    required_configs = [
        'ProductionConfig',
        'DATABASE_URL',
        'SECRET_KEY',
        'postgresql://'
    ]
    
    missing_configs = []
    for config in required_configs:
        if config not in content:
            missing_configs.append(config)
    
    if missing_configs:
        print(f"❌ Missing configurations: {', '.join(missing_configs)}")
        return False
    else:
        print("✅ Production configuration found")
        return True

def check_app_structure():
    """Check application structure"""
    print("\n🏗️  Checking application structure...")
    
    required_dirs = [
        'app',
        'templates',
        'static',
        'migrations',
        'uploads'
    ]
    
    required_files = [
        'app/__init__.py',
        'app/models.py',
        'app/forms.py',
        'templates/base.html',
        'static/css',
        'static/js',
        'static/images'
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if not check_directory_exists(dir_path, f"Directory {dir_path}"):
            all_good = False
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file/directory: {file_path} - MISSING!")
            all_good = False
        else:
            print(f"✅ Required file/directory: {file_path}")
    
    return all_good

def main():
    """Run all deployment readiness checks"""
    
    print("🚀 Render Deployment Readiness Check")
    print("=" * 50)
    
    # Check required files for Render deployment
    deployment_files = [
        ('requirements.txt', 'Python dependencies'),
        ('render.yaml', 'Render configuration'),
        ('Procfile', 'Process file'),
        ('runtime.txt', 'Python runtime'),
        ('gunicorn.conf.py', 'Gunicorn configuration'),
        ('app.py', 'Application entry point'),
        ('config.py', 'Application configuration'),
        ('.env.example', 'Environment variables example'),
        ('README.md', 'Documentation'),
        ('DEPLOY.md', 'Deployment guide')
    ]
    
    print("\n📋 Checking deployment files...")
    files_ok = True
    for file_path, description in deployment_files:
        if not check_file_exists(file_path, description):
            files_ok = False
    
    # Check requirements content
    requirements_ok = check_requirements_file()
    
    # Check config content
    config_ok = check_config_file()
    
    # Check application structure
    structure_ok = check_app_structure()
    
    # Check Python version
    print(f"\n🐍 Python version: {sys.version}")
    
    # Summary
    print("\n📊 Deployment Readiness Summary")
    print("=" * 50)
    
    checks = [
        ("Deployment Files", files_ok),
        ("Requirements Content", requirements_ok),
        ("Configuration", config_ok),
        ("Application Structure", structure_ok)
    ]
    
    passed = 0
    total = len(checks)
    
    for check_name, result in checks:
        status = "✅ READY" if result else "❌ NOT READY"
        print(f"{status} {check_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 PROJECT IS READY FOR RENDER DEPLOYMENT!")
        print("\n📝 Next steps:")
        print("1. Push your code to GitHub:")
        print("   git add .")
        print("   git commit -m 'feat: ready for Render deployment'")
        print("   git push origin master")
        print("\n2. Go to Render.com and create a new Web Service")
        print("3. Connect your GitHub repository")
        print("4. Follow the instructions in DEPLOY.md")
        print("\n🔗 Your app will be available at:")
        print("   https://emdad-global.onrender.com")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} check(s) failed.")
        print("Please fix the issues above before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
