#!/usr/bin/env python3
"""
Add default specifications for all 38 products.
Realistic and appropriate specifications for each product category.
"""

import json

def get_product_specifications():
    """Return comprehensive specifications for all products."""
    base_specs = {
        # Fresh Citrus Fruits
        'fresh-oranges': {
            'en': {
                "Variety": "Valencia • Navel • Blood Orange",
                "Size": "60-88mm diameter (Size 1-4)",
                "Brix Level": "11-14% (minimum 10%)",
                "Juice Content": "≥ 45% by weight",
                "Color": "Orange to deep orange, uniform",
                "Shelf Life": "2-4 weeks at 3-8°C",
                "Harvest Season": "December - May",
                "Packaging": "15kg cartons • 18kg cartons • Bulk bins"
            },
            'ar': {
                "الصنف": "فالنسيا • نافيل • برتقال أحمر",
                "الحجم": "60-88 مم قطر (حجم 1-4)",
                "مستوى البريكس": "11-14% (الحد الأدنى 10%)",
                "محتوى العصير": "≥ 45% بالوزن",
                "اللون": "برتقالي إلى برتقالي غامق، موحد",
                "مدة الصلاحية": "2-4 أسابيع عند 3-8 درجة مئوية",
                "موسم الحصاد": "ديسمبر - مايو",
                "التعبئة": "كراتين 15 كجم • كراتين 18 كجم • صناديق كبيرة"
            }
        },
        
        'fresh-mandarins': {
            'en': {
                "Variety": "Clementine • Satsuma • Murcott",
                "Size": "45-70mm diameter",
                "Brix Level": "10-13% (minimum 9%)",
                "Peel": "Easy peeling, thin skin",
                "Seeds": "Seedless or minimal seeds",
                "Color": "Orange to deep orange",
                "Shelf Life": "2-3 weeks at 2-4°C",
                "Harvest Season": "November - March"
            },
            'ar': {
                "الصنف": "كليمنتين • ساتسوما • مركوت",
                "الحجم": "45-70 مم قطر",
                "مستوى البريكس": "10-13% (الحد الأدنى 9%)",
                "القشرة": "سهلة التقشير، جلد رقيق",
                "البذور": "بدون بذور أو بذور قليلة",
                "اللون": "برتقالي إلى برتقالي غامق",
                "مدة الصلاحية": "2-3 أسابيع عند 2-4 درجة مئوية",
                "موسم الحصاد": "نوفمبر - مارس"
            }
        },

        'fresh-tangerines': {
            'en': {
                "Variety": "Dancy • Honey • Sunburst",
                "Size": "50-75mm diameter",
                "Brix Level": "9-12% (minimum 8.5%)",
                "Acidity": "0.6-1.2%",
                "Peel": "Loose skin, easy peeling",
                "Color": "Deep orange to reddish-orange",
                "Shelf Life": "2-3 weeks at 2-4°C",
                "Harvest Season": "October - February"
            },
            'ar': {
                "الصنف": "دانسي • هوني • صن بيرست",
                "الحجم": "50-75 مم قطر",
                "مستوى البريكس": "9-12% (الحد الأدنى 8.5%)",
                "الحموضة": "0.6-1.2%",
                "القشرة": "جلد فضفاض، سهل التقشير",
                "اللون": "برتقالي غامق إلى برتقالي محمر",
                "مدة الصلاحية": "2-3 أسابيع عند 2-4 درجة مئوية",
                "موسم الحصاد": "أكتوبر - فبراير"
            }
        },

        # Fresh Fruits
        'fresh-strawberries': {
            'en': {
                "Variety": "Festival • Camarosa • Albion",
                "Size": "15-35mm diameter",
                "Brix Level": "7-11% (minimum 6%)",
                "Color": "Bright red, uniform",
                "Firmness": "Firm, not soft or mushy",
                "Shelf Life": "3-7 days at 0-2°C",
                "Harvest Season": "December - April",
                "Packaging": "250g • 500g • 1kg punnets"
            },
            'ar': {
                "الصنف": "فيستيفال • كاماروسا • ألبيون",
                "الحجم": "15-35 مم قطر",
                "مستوى البريكس": "7-11% (الحد الأدنى 6%)",
                "اللون": "أحمر زاهي، موحد",
                "الصلابة": "صلبة، ليست طرية أو مهروسة",
                "مدة الصلاحية": "3-7 أيام عند 0-2 درجة مئوية",
                "موسم الحصاد": "ديسمبر - أبريل",
                "التعبئة": "عبوات 250 جم • 500 جم • 1 كجم"
            }
        },

        'fresh-grapes': {
            'en': {
                "Variety": "Thompson Seedless • Red Globe • Flame",
                "Size": "12-22mm diameter",
                "Brix Level": "16-22% (minimum 14%)",
                "Color": "Green • Red • Purple varieties",
                "Cluster Weight": "300-800g per cluster",
                "Seeds": "Seedless varieties preferred",
                "Shelf Life": "2-8 weeks at -1 to 0°C",
                "Harvest Season": "May - September"
            },
            'ar': {
                "الصنف": "طومسون بدون بذور • ريد جلوب • فليم",
                "الحجم": "12-22 مم قطر",
                "مستوى البريكس": "16-22% (الحد الأدنى 14%)",
                "اللون": "أخضر • أحمر • أرجواني",
                "وزن العنقود": "300-800 جم لكل عنقود",
                "البذور": "الأصناف الخالية من البذور مفضلة",
                "مدة الصلاحية": "2-8 أسابيع عند -1 إلى 0 درجة مئوية",
                "موسم الحصاد": "مايو - سبتمبر"
            }
        },

        'fresh-pomegranates': {
            'en': {
                "Variety": "Wonderful • Hicaz • Balegal",
                "Size": "70-120mm diameter",
                "Weight": "200-600g per fruit",
                "Aril Color": "Deep red to dark red",
                "Juice Content": "≥ 50% by weight",
                "Brix Level": "15-17% (minimum 14%)",
                "Shelf Life": "2-3 months at 5°C",
                "Harvest Season": "September - February"
            },
            'ar': {
                "الصنف": "وندرفول • حجازي • بالجال",
                "الحجم": "70-120 مم قطر",
                "الوزن": "200-600 جم لكل ثمرة",
                "لون الحبوب": "أحمر غامق إلى أحمر داكن",
                "محتوى العصير": "≥ 50% بالوزن",
                "مستوى البريكس": "15-17% (الحد الأدنى 14%)",
                "مدة الصلاحية": "2-3 أشهر عند 5 درجة مئوية",
                "موسم الحصاد": "سبتمبر - فبراير"
            }
        },

        'fresh-mango': {
            'en': {
                "Variety": "Keitt • Tommy Atkins • Kent • Haden",
                "Size": "300-600g per fruit",
                "Brix Level": "14-18% (minimum 12%)",
                "Color": "Green to yellow-red blush",
                "Firmness": "Firm to slightly soft when ripe",
                "Shelf Life": "1-3 weeks depending on ripeness",
                "Harvest Season": "April - September",
                "Ripeness": "Mature green or tree-ripe"
            },
            'ar': {
                "الصنف": "كيت • تومي أتكينز • كينت • هادن",
                "الحجم": "300-600 جم لكل ثمرة",
                "مستوى البريكس": "14-18% (الحد الأدنى 12%)",
                "اللون": "أخضر إلى أصفر مع حمرة",
                "الصلابة": "صلبة إلى طرية قليلاً عند النضج",
                "مدة الصلاحية": "1-3 أسابيع حسب درجة النضج",
                "موسم الحصاد": "أبريل - سبتمبر",
                "النضج": "أخضر ناضج أو ناضج على الشجرة"
            }
        },

        # Vegetables
        'potatoes-spunta': {
            'en': {
                "Variety": "Spunta • Early variety",
                "Size": "35-75mm diameter",
                "Shape": "Oval to long oval",
                "Skin Color": "Yellow, smooth",
                "Flesh Color": "Light yellow",
                "Dry Matter": "18-22%",
                "Shelf Life": "3-6 months in proper storage",
                "Harvest Season": "February - May",
                "Storage": "2-4°C, 85-90% humidity"
            },
            'ar': {
                "الصنف": "سبونتا • صنف مبكر",
                "الحجم": "35-75 مم قطر",
                "الشكل": "بيضاوي إلى بيضاوي طويل",
                "لون القشرة": "أصفر، ناعم",
                "لون اللب": "أصفر فاتح",
                "المادة الجافة": "18-22%",
                "مدة الصلاحية": "3-6 أشهر في التخزين المناسب",
                "موسم الحصاد": "فبراير - مايو",
                "التخزين": "2-4 درجة مئوية، رطوبة 85-90%"
            }
        },

        'sweet-potatoes-beauregard': {
            'en': {
                "Variety": "Beauregard • Orange flesh",
                "Size": "100-400g per tuber",
                "Shape": "Uniform, smooth",
                "Skin Color": "Copper to reddish-brown",
                "Flesh Color": "Deep orange",
                "Dry Matter": "25-30%",
                "Beta Carotene": "High content",
                "Shelf Life": "6-10 months in proper storage",
                "Harvest Season": "September - November"
            },
            'ar': {
                "الصنف": "بيوريجارد • لب برتقالي",
                "الحجم": "100-400 جم لكل درنة",
                "الشكل": "منتظم، ناعم",
                "لون القشرة": "نحاسي إلى بني محمر",
                "لون اللب": "برتقالي غامق",
                "المادة الجافة": "25-30%",
                "البيتا كاروتين": "محتوى عالي",
                "مدة الصلاحية": "6-10 أشهر في التخزين المناسب",
                "موسم الحصاد": "سبتمبر - نوفمبر"
            }
        },

        'fresh-spring-onions': {
            'en': {
                "Type": "Green onions • Scallions",
                "Length": "25-40cm total length",
                "Bulb Diameter": "8-15mm",
                "Color": "White bulb, green tops",
                "Freshness": "Crisp, firm texture",
                "Shelf Life": "7-14 days at 0-2°C",
                "Harvest Season": "Year-round",
                "Packaging": "Bunches of 8-12 pieces"
            },
            'ar': {
                "النوع": "بصل أخضر • بصل الربيع",
                "الطول": "25-40 سم الطول الكلي",
                "قطر البصلة": "8-15 مم",
                "اللون": "بصلة بيضاء، قمم خضراء",
                "النضارة": "قوام مقرمش وصلب",
                "مدة الصلاحية": "7-14 يوم عند 0-2 درجة مئوية",
                "موسم الحصاد": "على مدار السنة",
                "التعبئة": "حزم من 8-12 قطعة"
            }
        },

        'onions-red-golden': {
            'en': {
                "Variety": "Red • Golden • Yellow varieties",
                "Size": "50-90mm diameter",
                "Shape": "Round to slightly flattened",
                "Dry Matter": "12-18%",
                "Pungency": "Medium to strong",
                "Storage Life": "6-8 months in proper storage",
                "Harvest Season": "May - August",
                "Curing": "Properly cured and dried"
            },
            'ar': {
                "الصنف": "أحمر • ذهبي • أصناف صفراء",
                "الحجم": "50-90 مم قطر",
                "الشكل": "دائري إلى مسطح قليلاً",
                "المادة الجافة": "12-18%",
                "الحدة": "متوسطة إلى قوية",
                "مدة التخزين": "6-8 أشهر في التخزين المناسب",
                "موسم الحصاد": "مايو - أغسطس",
                "المعالجة": "معالج ومجفف بشكل صحيح"
            }
        },

        'garlic-white': {
            'en': {
                "Variety": "White garlic • Hardneck/Softneck",
                "Bulb Size": "40-70mm diameter",
                "Cloves": "8-15 cloves per bulb",
                "Skin": "White, papery outer skin",
                "Flavor": "Strong, pungent",
                "Dry Matter": "35-40%",
                "Storage Life": "6-10 months in proper storage",
                "Harvest Season": "June - August"
            },
            'ar': {
                "الصنف": "ثوم أبيض • صلب/طري الرقبة",
                "حجم الرأس": "40-70 مم قطر",
                "الفصوص": "8-15 فص لكل رأس",
                "القشرة": "قشرة خارجية بيضاء ورقية",
                "النكهة": "قوية، حادة",
                "المادة الجافة": "35-40%",
                "مدة التخزين": "6-10 أشهر في التخزين المناسب",
                "موسم الحصاد": "يونيو - أغسطس"
            }
        }
    }

    # Import additional specifications from other files
    try:
        from migrations.product_specs_part2 import get_additional_specifications
        from migrations.product_specs_part3 import get_final_specifications
        from migrations.product_specs_part4 import get_remaining_specifications

        # Merge all specifications
        all_specs = {}
        all_specs.update(base_specs)
        all_specs.update(get_additional_specifications())
        all_specs.update(get_final_specifications())
        all_specs.update(get_remaining_specifications())

        return all_specs
    except ImportError as e:
        print(f"⚠️ Could not import additional specifications: {e}")
        return base_specs

def update_product_specifications(db=None, force_update=False):
    """Update products with default specifications.

    Args:
        db: Database instance (optional)
        force_update: If True, update ALL products regardless of current specifications
    """
    try:
        # If called from init_db_render.py, db will be passed
        # If called standalone, we need to create app context
        if db is None:
            from app import create_app, db as app_db
            from app.models import Product

            app = create_app()
            with app.app_context():
                return _update_specifications_internal(app_db, Product, force_update)
        else:
            # We're already in app context, just import Product model
            from app.models import Product
            return _update_specifications_internal(db, Product, force_update)
            
    except Exception as e:
        print(f"❌ Error updating product specifications: {e}")
        import traceback
        traceback.print_exc()
        return False

def _update_specifications_internal(db, Product, force_update=False):
    """Internal function to update product specifications.

    Args:
        db: Database instance
        Product: Product model class
        force_update: If True, update ALL products regardless of current specifications
    """
    specifications_data = get_product_specifications()
    updated_count = 0
    not_found_count = 0
    
    print("🔄 Starting product specifications assignment...")
    
    for slug, specs in specifications_data.items():
        product = Product.query.filter_by(slug=slug).first()
        if product:
            should_update = False

            if force_update:
                # Force update ALL products regardless of current state
                should_update = True
                update_reason = "Force update requested"
            else:
                # Only update if specifications are not already set or are simple text
                current_specs = product.get_specifications()

                if not current_specs:
                    should_update = True
                    update_reason = "No specifications"
                elif isinstance(current_specs, dict):
                    # Check if it's just simple text (notes format)
                    en_specs = current_specs.get('en', {})
                    ar_specs = current_specs.get('ar', {})
                    if (isinstance(en_specs, dict) and len(en_specs) == 1 and 'notes' in en_specs) or \
                       (isinstance(ar_specs, dict) and len(ar_specs) == 1 and 'notes' in ar_specs) or \
                       (isinstance(en_specs, str)) or (isinstance(ar_specs, str)):
                        should_update = True
                        update_reason = "Simple specifications detected"

            if should_update:
                product.specifications = json.dumps(specs, ensure_ascii=False)
                updated_count += 1
                if force_update:
                    print(f"🔄 FORCE Updated {slug}: {update_reason}")
                else:
                    print(f"✅ Updated {slug}: {update_reason}")
            else:
                print(f"⏭️ Skipped {slug}: Already has detailed specifications")
        else:
            not_found_count += 1
            print(f"⚠️ Product not found: {slug}")
    
    # Commit changes
    if updated_count > 0:
        try:
            db.session.commit()
            print(f"\n✅ Successfully updated {updated_count} products with specifications")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error committing changes: {e}")
            return False
    else:
        print("\n✅ No products needed specification updates")

    if not_found_count > 0:
        print(f"⚠️ {not_found_count} products from the specifications list were not found in database")

    # Verify results
    total_with_specs = Product.query.filter(Product.specifications.isnot(None)).count()
    total_products = Product.query.count()
    print(f"📊 Final status: {total_with_specs}/{total_products} products have specifications")

    return True

if __name__ == "__main__":
    import sys
    import os

    # Add the project root to the Python path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    success = update_product_specifications()
    if success:
        print("\n✅ CONCLUSION: Product specifications updated successfully!")
    else:
        print("\n❌ CONCLUSION: There were issues updating product specifications!")

    sys.exit(0 if success else 1)
