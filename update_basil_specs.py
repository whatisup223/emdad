#!/usr/bin/env python3
"""Update basil product with structured specifications."""

from app import create_app, db
from app.models import Product
import json

app = create_app()
with app.app_context():
    # Find basil product
    basil = Product.query.filter_by(slug='basil').first()
    
    if basil:
        print(f"Found product: {basil.name_en}")
        
        # Create structured specifications
        specs_en = {
            "Essential Oil (EO)": "0.3–1.5% (starter target: ISO 6571/ASTA)",
            "Cut Sizes": "Whole leaf • Crushed 3–6 mm • Tea Bag Cut 1–3 mm • Powder 60–120 mesh",
            "Moisture": "≤ 10–12% (typical)",
            "Color": "Green retention target: sortex available",
            "Metal Detection": "Ferrous/Non-ferrous/SS per QA plan",
            "Crop Year": "Current season (declare on COA)"
        }
        
        specs_ar = {
            "الزيت العطري": "0.3–1.5% (الهدف المبدئي: ISO 6571/ASTA)",
            "أحجام القطع": "ورقة كاملة • مطحون 3–6 مم • قطع أكياس الشاي 1–3 مم • مسحوق 60–120 شبكة",
            "الرطوبة": "≤ 10–12% (نموذجي)",
            "اللون": "هدف الاحتفاظ بالأخضر: sortex متاح",
            "كشف المعادن": "حديدي/غير حديدي/SS حسب خطة ضمان الجودة",
            "سنة المحصول": "الموسم الحالي (يُعلن في شهادة التحليل)"
        }
        
        # Create the specifications JSON structure
        specifications = {
            'en': specs_en,
            'ar': specs_ar
        }
        
        # Update the product
        basil.specifications = json.dumps(specifications, ensure_ascii=False)
        
        db.session.commit()
        
        print("✅ Updated basil specifications successfully!")
        print(f"Specifications: {basil.specifications}")
        
        # Test the get_specifications_lang method
        specs_en_result = basil.get_specifications_lang('en')
        specs_ar_result = basil.get_specifications_lang('ar')
        
        print(f"\nEN specs: {specs_en_result}")
        print(f"AR specs: {specs_ar_result}")
        
    else:
        print("❌ Basil product not found")
