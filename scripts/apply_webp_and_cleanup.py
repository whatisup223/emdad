# -*- coding: utf-8 -*-
import os
import sys
import shutil

# Ensure project root on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from app.models import db, Product, ProductImage

app = create_app('production')

PRODUCTS_SUBDIR = os.path.join('uploads', 'products')


def ensure_instance_dir(path):
    os.makedirs(path, exist_ok=True)


def expected_webp_name(slug: str) -> str:
    return f"{slug}-emdad-global.webp"


def main():
    with app.app_context():
        instance_products_dir = os.path.join(app.instance_path, PRODUCTS_SUBDIR)
        static_products_dir = os.path.join(app.static_folder, PRODUCTS_SUBDIR)
        ensure_instance_dir(instance_products_dir)

        products = Product.query.order_by(Product.category_id, Product.sort_order, Product.name_en).all()
        in_use_files = set()
        missing_files = []

        for p in products:
            webp_name = expected_webp_name(p.slug)
            instance_fp = os.path.join(instance_products_dir, webp_name)
            static_fp = os.path.join(static_products_dir, webp_name)

            # If not in instance, try to copy from static fallback
            if not os.path.exists(instance_fp):
                if os.path.exists(static_fp):
                    shutil.copy2(static_fp, instance_fp)
                    print(f"Copied from static: {webp_name}")
                else:
                    missing_files.append((p.slug, webp_name))
                    # Continue but still update DB so we can detect missing assets

            # Update product main image_path
            p.image_path = webp_name
            db.session.add(p)
            in_use_files.add(webp_name)

            # Ensure ProductImage main entry
            existing_images = list(p.images)
            webp_img = None
            for img in existing_images:
                if img.filename == webp_name:
                    webp_img = img
                    break

            if webp_img is None:
                webp_img = ProductImage(product_id=p.id, filename=webp_name, alt_text_en=p.name_en, alt_text_ar=p.name_ar, is_main=True, sort_order=0)
                db.session.add(webp_img)
            else:
                # Mark it as main
                if not webp_img.is_main:
                    webp_img.is_main = True
                    db.session.add(webp_img)

            # Remove other ProductImage entries that are not the webp main (avoid broken thumbs)
            for img in existing_images:
                if img.id != getattr(webp_img, 'id', None):
                    # Delete DB row; underlying file will be handled later by FS cleanup
                    db.session.delete(img)

        db.session.commit()

        # After DB update, rebuild in-use set from DB to be exact
        in_use_files = set()
        products = Product.query.all()
        for p in products:
            if p.image_path:
                in_use_files.add(p.image_path)
            for img in p.images:
                in_use_files.add(img.filename)

        # Cleanup filesystem: delete unused PNG/JPG/SVG files in instance/uploads/products
        deletable_exts = {'.png', '.jpg', '.jpeg', '.svg'}
        deleted = []
        kept = []
        if os.path.isdir(instance_products_dir):
            for fname in os.listdir(instance_products_dir):
                fpath = os.path.join(instance_products_dir, fname)
                _, ext = os.path.splitext(fname.lower())
                if os.path.isfile(fpath):
                    if fname in in_use_files:
                        kept.append(fname)
                        continue
                    if ext in deletable_exts:
                        try:
                            os.remove(fpath)
                            deleted.append(fname)
                        except Exception as e:
                            print(f"Failed to delete {fname}: {e}")
                    else:
                        kept.append(fname)

        print("SUMMARY:")
        print(" - Missing webp files:", len(missing_files))
        for slug, name in missing_files:
            print(f"   * {slug} -> {name} (NOT FOUND)")
        print(" - Deleted old files:", len(deleted))
        for name in deleted:
            print(f"   - {name}")
        print(" - Kept files:", len(kept))


if __name__ == '__main__':
    main()

