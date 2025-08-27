#!/usr/bin/env python3
"""
Rollback script to restore original images and settings
"""

import os
import shutil
from pathlib import Path

def rollback_images():
    """Rollback all image changes to original state"""
    
    print("🔄 Rolling back image changes...")
    print("=" * 50)
    
    try:
        # 1. Restore original hero background
        backup_hero = Path("static/images/backup/hero-bg.jpg.backup")
        if backup_hero.exists():
            shutil.copy2(backup_hero, "static/images/hero-bg.jpg")
            print("✅ Restored original hero background (hero-bg.jpg)")
        else:
            print("⚠️  Original hero background backup not found")
        
        # 2. Restore original logo
        backup_logo = Path("static/images/backup/logo.svg.backup")
        if backup_logo.exists():
            shutil.copy2(backup_logo, "static/images/logo.svg")
            print("✅ Restored original logo (logo.svg)")
        else:
            print("⚠️  Original logo backup not found")
        
        # 3. Remove new images
        new_logo = Path("static/images/logo.png")
        if new_logo.exists():
            new_logo.unlink()
            print("✅ Removed new logo (logo.png)")
        
        new_hero = Path("static/images/hero-bg.webp")
        if new_hero.exists():
            new_hero.unlink()
            print("✅ Removed new hero background (hero-bg.webp)")
        
        print("\n📝 Manual steps required:")
        print("=" * 30)
        print("1. Update templates/base.html:")
        print("   Change logo src back to: {{ url_for('logo_file') }}")
        print("   Change onerror back to: this.src='/uploads/logo.png'")
        print()
        print("2. Update static/css/style.css:")
        print("   Change all hero background URLs back to: url('/uploads/bg.webp')")
        print()
        print("3. Restore uploads folder files:")
        print("   Copy logo.png and bg.webp back to uploads/ folder")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during rollback: {e}")
        return False

def rollback_css():
    """Rollback CSS changes"""
    
    print("\n🎨 Rolling back CSS changes...")
    print("=" * 30)
    
    try:
        css_file = Path("static/css/style.css")
        if not css_file.exists():
            print("❌ CSS file not found")
            return False
        
        # Read current CSS
        content = css_file.read_text(encoding='utf-8')
        
        # Replace new paths with old paths
        replacements = [
            ("url('../images/hero-bg.webp')", "url('/uploads/bg.webp')"),
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Write back
        css_file.write_text(content, encoding='utf-8')
        print("✅ CSS paths restored to original")
        
        return True
        
    except Exception as e:
        print(f"❌ Error rolling back CSS: {e}")
        return False

def rollback_templates():
    """Rollback template changes"""
    
    print("\n📄 Rolling back template changes...")
    print("=" * 30)
    
    try:
        base_template = Path("templates/base.html")
        if not base_template.exists():
            print("❌ Base template not found")
            return False
        
        # Read current template
        content = base_template.read_text(encoding='utf-8')
        
        # Replace new logo with old logo
        old_logo = '''                <img src="{{ url_for('logo_file') }}"
                     alt="{{ COMPANY_NAME }}"
                     class="navbar-logo d-inline-block align-text-top me-2"
                     onerror="this.src='/uploads/logo.png'; this.onerror=function(){this.style.display='none'; this.nextElementSibling.classList.remove('d-none', 'd-sm-inline'); this.nextElementSibling.classList.add('d-inline');};">'''
        
        new_logo = '''                <img src="{{ url_for('static', filename='images/logo.png') }}"
                     alt="{{ COMPANY_NAME }}"
                     class="navbar-logo d-inline-block align-text-top me-2"
                     onerror="this.src='{{ url_for('static', filename='images/logo.svg') }}'; this.onerror=function(){this.style.display='none'; this.nextElementSibling.classList.remove('d-none', 'd-sm-inline'); this.nextElementSibling.classList.add('d-inline');};">'''
        
        content = content.replace(new_logo, old_logo)
        
        # Write back
        base_template.write_text(content, encoding='utf-8')
        print("✅ Template logo restored to original")
        
        return True
        
    except Exception as e:
        print(f"❌ Error rolling back templates: {e}")
        return False

def restore_uploads_folder():
    """Restore files to uploads folder"""
    
    print("\n📁 Restoring uploads folder...")
    print("=" * 30)
    
    try:
        # Create uploads folder if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        # Copy files back from static/images
        logo_src = Path("static/images/logo.png")
        hero_src = Path("static/images/hero-bg.webp")
        
        if logo_src.exists():
            shutil.copy2(logo_src, "uploads/logo.png")
            print("✅ Restored logo.png to uploads/")
        
        if hero_src.exists():
            shutil.copy2(hero_src, "uploads/bg.webp")
            print("✅ Restored bg.webp to uploads/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring uploads: {e}")
        return False

def main():
    """Run complete rollback"""
    
    print("🔄 Complete Image Rollback Script")
    print("=" * 50)
    print("This will restore all images to their original state")
    print()
    
    # Ask for confirmation
    response = input("Are you sure you want to rollback? (y/N): ").lower().strip()
    if response != 'y':
        print("❌ Rollback cancelled")
        return
    
    steps = [
        ("Rollback Images", rollback_images),
        ("Rollback CSS", rollback_css),
        ("Rollback Templates", rollback_templates),
        ("Restore Uploads", restore_uploads_folder)
    ]
    
    results = []
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
            results.append((step_name, False))
    
    # Summary
    print("\n📊 Rollback Results")
    print("=" * 30)
    
    passed = 0
    total = len(results)
    
    for step_name, result in results:
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{status} {step_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} steps completed successfully")
    
    if passed == total:
        print("\n🎉 Rollback completed successfully!")
        print("All images have been restored to their original state.")
    else:
        print(f"\n⚠️  {total - passed} step(s) failed.")
        print("Please check the errors above and fix manually if needed.")

if __name__ == "__main__":
    main()
