#!/usr/bin/env python3
"""
Additional product specifications - Part 3
Seeds, Herbs, and Frozen Products
"""

def get_final_specifications():
    """Return specifications for seeds, herbs, and frozen products."""
    return {
        # Seeds
        'nigella-black-seed': {
            'en': {
                "Botanical Name": "Nigella sativa",
                "Common Names": "Black seed • Black cumin • Kalonji",
                "Origin": "Egypt • Turkey • India",
                "Purity": "99% minimum",
                "Moisture": "≤ 8%",
                "Oil Content": "32-40%",
                "Color": "Black to dark brown",
                "Size": "2-3mm length",
                "Flavor": "Bitter, pungent, aromatic",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Nigella sativa",
                "الأسماء الشائعة": "حبة البركة • الكمون الأسود • كالونجي",
                "المنشأ": "مصر • تركيا • الهند",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 8%",
                "محتوى الزيت": "32-40%",
                "اللون": "أسود إلى بني غامق",
                "الحجم": "2-3 مم طول",
                "النكهة": "مرة، نفاذة، عطرية",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'sesame-seed': {
            'en': {
                "Botanical Name": "Sesamum indicum",
                "Variety": "White • Natural • Hulled",
                "Origin": "Sudan • Ethiopia • India",
                "Purity": "99% minimum",
                "Moisture": "≤ 6%",
                "Oil Content": "48-55%",
                "Color": "White to cream (hulled)",
                "Size": "2-4mm length",
                "FFA": "≤ 2% (Free Fatty Acid)",
                "Shelf Life": "12-18 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Sesamum indicum",
                "الصنف": "أبيض • طبيعي • مقشر",
                "المنشأ": "السودان • إثيوبيا • الهند",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 6%",
                "محتوى الزيت": "48-55%",
                "اللون": "أبيض إلى كريمي (مقشر)",
                "الحجم": "2-4 مم طول",
                "الأحماض الدهنية الحرة": "≤ 2%",
                "مدة الصلاحية": "12-18 شهر في التخزين المناسب"
            }
        },

        'flax-seeds': {
            'en': {
                "Botanical Name": "Linum usitatissimum",
                "Variety": "Brown • Golden varieties",
                "Origin": "Canada • Argentina • Kazakhstan",
                "Purity": "99% minimum",
                "Moisture": "≤ 8%",
                "Oil Content": "35-45%",
                "Omega-3": "High in alpha-linolenic acid",
                "Color": "Brown to golden brown",
                "Size": "4-6mm length",
                "Shelf Life": "12-24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Linum usitatissimum",
                "الصنف": "بني • أصناف ذهبية",
                "المنشأ": "كندا • الأرجنتين • كازاخستان",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 8%",
                "محتوى الزيت": "35-45%",
                "أوميجا-3": "عالي في حمض الألفا لينولينيك",
                "اللون": "بني إلى بني ذهبي",
                "الحجم": "4-6 مم طول",
                "مدة الصلاحية": "12-24 شهر في التخزين المناسب"
            }
        },

        # Herbs
        'basil': {
            'en': {
                "Botanical Name": "Ocimum basilicum",
                "Type": "Sweet basil • Dried leaves",
                "Origin": "Egypt • India • Mediterranean",
                "Essential Oil": "0.3-1.5% (starter target: ISO 6571/ASTA)",
                "Cut Sizes": "Whole leaf • Crushed 3-6 mm • Tea Bag Cut 1-3 mm • Powder 60-120 mesh",
                "Moisture": "≤ 10-12% (typical)",
                "Color": "Green retention target: sortex available",
                "Metal Detection": "Ferrous/Non-ferrous/SS per QA plan",
                "Crop Year": "Current season (declare on COA)"
            },
            'ar': {
                "الاسم النباتي": "Ocimum basilicum",
                "النوع": "ريحان حلو • أوراق مجففة",
                "المنشأ": "مصر • الهند • البحر المتوسط",
                "الزيت العطري": "0.3-1.5% (الهدف المبدئي: ISO 6571/ASTA)",
                "أحجام القطع": "ورقة كاملة • مطحون 3-6 مم • قطع أكياس الشاي 1-3 مم • مسحوق 60-120 شبكة",
                "الرطوبة": "≤ 10-12% (نموذجي)",
                "اللون": "هدف الاحتفاظ بالأخضر: sortex متاح",
                "كشف المعادن": "حديدي/غير حديدي/SS حسب خطة ضمان الجودة",
                "سنة المحصول": "الموسم الحالي (يُعلن في شهادة التحليل)"
            }
        },

        'parsley-flakes': {
            'en': {
                "Botanical Name": "Petroselinum crispum",
                "Type": "Flat leaf • Curly leaf varieties",
                "Processing": "Air dried, flaked",
                "Cut Size": "2-8mm flakes",
                "Moisture": "≤ 10%",
                "Color": "Bright green to dark green",
                "Flavor": "Fresh, grassy, slightly peppery",
                "Essential Oil": "0.1-0.7%",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Petroselinum crispum",
                "النوع": "ورقة مسطحة • أصناف مجعدة",
                "المعالجة": "مجفف بالهواء، رقائق",
                "حجم القطع": "رقائق 2-8 مم",
                "الرطوبة": "≤ 10%",
                "اللون": "أخضر زاهي إلى أخضر غامق",
                "النكهة": "طازجة، عشبية، فلفلية قليلاً",
                "الزيت العطري": "0.1-0.7%",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'dill': {
            'en': {
                "Botanical Name": "Anethum graveolens",
                "Type": "Dill weed • Dried leaves",
                "Cut Size": "2-6mm pieces",
                "Moisture": "≤ 10%",
                "Color": "Green to dark green",
                "Flavor": "Fresh, tangy, slightly sweet",
                "Essential Oil": "0.5-1.5%",
                "Aroma": "Strong, characteristic dill scent",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Anethum graveolens",
                "النوع": "عشبة الشبت • أوراق مجففة",
                "حجم القطع": "قطع 2-6 مم",
                "الرطوبة": "≤ 10%",
                "اللون": "أخضر إلى أخضر غامق",
                "النكهة": "طازجة، حامضة، حلوة قليلاً",
                "الزيت العطري": "0.5-1.5%",
                "الرائحة": "قوية، رائحة شبت مميزة",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'mint': {
            'en': {
                "Botanical Name": "Mentha spicata • Mentha piperita",
                "Type": "Spearmint • Peppermint varieties",
                "Cut Size": "Whole leaves • 3-8mm pieces",
                "Moisture": "≤ 10%",
                "Color": "Green to dark green",
                "Essential Oil": "0.5-2.5%",
                "Menthol Content": "Varies by variety",
                "Flavor": "Cool, refreshing, aromatic",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Mentha spicata • Mentha piperita",
                "النوع": "نعناع عادي • نعناع فلفلي",
                "حجم القطع": "أوراق كاملة • قطع 3-8 مم",
                "الرطوبة": "≤ 10%",
                "اللون": "أخضر إلى أخضر غامق",
                "الزيت العطري": "0.5-2.5%",
                "محتوى المنثول": "يختلف حسب الصنف",
                "النكهة": "باردة، منعشة، عطرية",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'oregano': {
            'en': {
                "Botanical Name": "Origanum vulgare",
                "Type": "Mediterranean oregano • Dried leaves",
                "Cut Size": "Whole leaves • Crushed • Powder",
                "Moisture": "≤ 10%",
                "Essential Oil": "1-4%",
                "Color": "Green to brownish-green",
                "Flavor": "Pungent, aromatic, slightly bitter",
                "Carvacrol Content": "High (quality indicator)",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Origanum vulgare",
                "النوع": "أوريجانو متوسطي • أوراق مجففة",
                "حجم القطع": "أوراق كاملة • مطحون • مسحوق",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "1-4%",
                "اللون": "أخضر إلى أخضر بني",
                "النكهة": "نفاذة، عطرية، مرة قليلاً",
                "محتوى الكارفاكرول": "عالي (مؤشر الجودة)",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'thyme': {
            'en': {
                "Botanical Name": "Thymus vulgaris",
                "Type": "Common thyme • Dried leaves",
                "Cut Size": "Whole leaves • Crushed • Powder",
                "Moisture": "≤ 10%",
                "Essential Oil": "1-2.5%",
                "Color": "Grayish-green to brown",
                "Flavor": "Earthy, minty, slightly floral",
                "Thymol Content": "High (quality indicator)",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Thymus vulgaris",
                "النوع": "زعتر عادي • أوراق مجففة",
                "حجم القطع": "أوراق كاملة • مطحون • مسحوق",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "1-2.5%",
                "اللون": "أخضر رمادي إلى بني",
                "النكهة": "ترابية، نعناعية، زهرية قليلاً",
                "محتوى الثيمول": "عالي (مؤشر الجودة)",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'sage': {
            'en': {
                "Botanical Name": "Salvia officinalis",
                "Type": "Garden sage • Dried leaves",
                "Cut Size": "Whole leaves • Crushed • Powder",
                "Moisture": "≤ 10%",
                "Essential Oil": "1-2.8%",
                "Color": "Grayish-green to olive green",
                "Flavor": "Earthy, slightly bitter, aromatic",
                "Texture": "Velvety, soft leaves",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Salvia officinalis",
                "النوع": "مرمرية الحديقة • أوراق مجففة",
                "حجم القطع": "أوراق كاملة • مطحون • مسحوق",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "1-2.8%",
                "اللون": "أخضر رمادي إلى أخضر زيتوني",
                "النكهة": "ترابية، مرة قليلاً، عطرية",
                "القوام": "أوراق مخملية، ناعمة",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        }
    }
