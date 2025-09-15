#!/usr/bin/env python3
"""Check current specifications format."""

from app import create_app, db
from app.models import Product
import json

app = create_app()
with app.app_context():
    # Get first few products
    products = Product.query.limit(5).all()
    
    for product in products:
        print(f"\n=== {product.name_en} ===")
        print(f"Specifications raw: {product.specifications}")
        
        if product.specifications:
            try:
                specs = json.loads(product.specifications)
                print(f"Specifications parsed: {specs}")
                
                specs_en = product.get_specifications_lang('en')
                print(f"Specifications EN: {specs_en}")
                
                specs_ar = product.get_specifications_lang('ar')
                print(f"Specifications AR: {specs_ar}")
            except Exception as e:
                print(f"Error parsing: {e}")
        else:
            print("No specifications")
