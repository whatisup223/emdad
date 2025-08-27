from flask import send_from_directory
import os
from app import create_app

# Import models to ensure they are registered with SQLAlchemy
from app.models import *

app = create_app()

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    # استخدام مجلد uploads المباشر
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    return send_from_directory(upload_path, filename)

@app.route('/logo.png')
def logo_file():
    """Serve logo file directly."""
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    try:
        return send_from_directory(upload_path, 'logo.png')
    except FileNotFoundError:
        # إذا لم يوجد اللوجو، أرجع صورة افتراضية أو خطأ 404
        from flask import abort
        abort(404)

@app.route('/bg.webp')
def hero_bg_file():
    """Serve hero background file directly."""
    upload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    try:
        return send_from_directory(upload_path, 'bg.webp')
    except FileNotFoundError:
        # إذا لم توجد الصورة، أرجع خطأ 404
        from flask import abort
        abort(404)

if __name__ == '__main__':
    # تشغيل التطبيق على جميع عناوين IP للوصول من الشبكة المحلية
    app.run(
        host='0.0.0.0',  # يسمح بالوصول من أي عنوان IP على الشبكة
        port=5000,       # المنفذ
        debug=True       # وضع التطوير
    )
