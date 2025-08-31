from flask import send_from_directory
import os
from app import create_app

# Import models to ensure they are registered with SQLAlchemy
from app.models import *

# Create app instance
app = create_app(os.environ.get('FLASK_ENV', 'production'))

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
    # تشغيل التطبيق للتطوير المحلي فقط
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
