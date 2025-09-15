#!/usr/bin/env python3
"""
Additional product specifications - Part 4
Remaining Herbs and Frozen Products
"""

def get_remaining_specifications():
    """Return specifications for remaining herbs and frozen products."""
    return {
        # Remaining Herbs
        'marjoram': {
            'en': {
                "Botanical Name": "Origanum majorana",
                "Type": "Sweet marjoram • Dried leaves",
                "Cut Size": "Whole leaves • Crushed • Powder",
                "Moisture": "≤ 10%",
                "Essential Oil": "0.7-3%",
                "Color": "Grayish-green to light brown",
                "Flavor": "Sweet, pine-like, citrusy",
                "Aroma": "Delicate, floral, herb-like",
                "Quality": "Hand-selected, premium grade",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Origanum majorana",
                "النوع": "مردقوش حلو • أوراق مجففة",
                "حجم القطع": "أوراق كاملة • مطحون • مسحوق",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "0.7-3%",
                "اللون": "أخضر رمادي إلى بني فاتح",
                "النكهة": "حلوة، تشبه الصنوبر، حمضية",
                "الرائحة": "رقيقة، زهرية، عشبية",
                "الجودة": "منتقى يدوياً، درجة ممتازة",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'lemongrass': {
            'en': {
                "Botanical Name": "Cymbopogon citratus",
                "Type": "Dried lemongrass • Cut leaves",
                "Cut Size": "5-15mm pieces",
                "Moisture": "≤ 10%",
                "Essential Oil": "0.2-0.5%",
                "Color": "Light green to yellowish-green",
                "Flavor": "Citrusy, lemony, fresh",
                "Aroma": "Strong lemon scent",
                "Citral Content": "High (main component)",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Cymbopogon citratus",
                "النوع": "عشبة الليمون المجففة • أوراق مقطعة",
                "حجم القطع": "قطع 5-15 مم",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "0.2-0.5%",
                "اللون": "أخضر فاتح إلى أخضر مصفر",
                "النكهة": "حمضية، ليمونية، طازجة",
                "الرائحة": "رائحة ليمون قوية",
                "محتوى السيترال": "عالي (المكون الرئيسي)",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'chamomile': {
            'en': {
                "Botanical Name": "Matricaria chamomilla",
                "Type": "German chamomile • Dried flowers",
                "Grade": "Premium grade • Whole flowers",
                "Moisture": "≤ 10%",
                "Essential Oil": "0.2-1.9%",
                "Color": "White petals, yellow center",
                "Flavor": "Mild, sweet, apple-like",
                "Aroma": "Honey-like, floral",
                "Apigenin Content": "High (active compound)",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Matricaria chamomilla",
                "النوع": "بابونج ألماني • أزهار مجففة",
                "الدرجة": "درجة ممتازة • أزهار كاملة",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "0.2-1.9%",
                "اللون": "بتلات بيضاء، مركز أصفر",
                "النكهة": "خفيفة، حلوة، تشبه التفاح",
                "الرائحة": "تشبه العسل، زهرية",
                "محتوى الأبيجينين": "عالي (المركب النشط)",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'calendula': {
            'en': {
                "Botanical Name": "Calendula officinalis",
                "Type": "Pot marigold • Dried petals",
                "Grade": "Premium grade • Whole petals",
                "Moisture": "≤ 10%",
                "Color": "Bright orange to deep orange",
                "Flavor": "Slightly bitter, peppery",
                "Aroma": "Mild, slightly musky",
                "Carotenoids": "High content (natural color)",
                "Uses": "Herbal tea • Cosmetic applications",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Calendula officinalis",
                "النوع": "آذريون الحدائق • بتلات مجففة",
                "الدرجة": "درجة ممتازة • بتلات كاملة",
                "الرطوبة": "≤ 10%",
                "اللون": "برتقالي زاهي إلى برتقالي غامق",
                "النكهة": "مرة قليلاً، فلفلية",
                "الرائحة": "خفيفة، مسكية قليلاً",
                "الكاروتينات": "محتوى عالي (لون طبيعي)",
                "الاستخدامات": "شاي عشبي • تطبيقات تجميلية",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'hibiscus': {
            'en': {
                "Botanical Name": "Hibiscus sabdariffa",
                "Type": "Hibiscus flowers • Dried calyces",
                "Grade": "Premium grade • Whole pieces",
                "Moisture": "≤ 10%",
                "Color": "Deep red to burgundy",
                "Flavor": "Tart, cranberry-like, acidic",
                "Aroma": "Fruity, floral",
                "Vitamin C": "High content",
                "Anthocyanins": "Rich in antioxidants",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Hibiscus sabdariffa",
                "النوع": "أزهار الكركديه • كؤوس مجففة",
                "الدرجة": "درجة ممتازة • قطع كاملة",
                "الرطوبة": "≤ 10%",
                "اللون": "أحمر غامق إلى بورجوندي",
                "النكهة": "حامضة، تشبه التوت البري، حمضية",
                "الرائحة": "فاكهية، زهرية",
                "فيتامين سي": "محتوى عالي",
                "الأنثوسيانين": "غني بمضادات الأكسدة",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        # Frozen Products
        'iqf-strawberries': {
            'en': {
                "Type": "IQF (Individually Quick Frozen)",
                "Variety": "Festival • Camarosa • Albion",
                "Processing": "Whole • Sliced • Diced options",
                "Size": "15-35mm diameter",
                "Brix Level": "7-11% (minimum 6%)",
                "Color": "Bright red, natural",
                "Temperature": "-18°C or below",
                "Packaging": "10kg • 20kg • 25kg cartons",
                "Shelf Life": "24 months frozen",
                "Quality": "Grade A • Premium quality"
            },
            'ar': {
                "النوع": "مجمد فردي سريع (IQF)",
                "الصنف": "فيستيفال • كاماروسا • ألبيون",
                "المعالجة": "كامل • مقطع شرائح • مكعبات",
                "الحجم": "15-35 مم قطر",
                "مستوى البريكس": "7-11% (الحد الأدنى 6%)",
                "اللون": "أحمر زاهي، طبيعي",
                "درجة الحرارة": "-18 درجة مئوية أو أقل",
                "التعبئة": "كراتين 10 كجم • 20 كجم • 25 كجم",
                "مدة الصلاحية": "24 شهر مجمد",
                "الجودة": "درجة أ • جودة ممتازة"
            }
        },

        'iqf-mango': {
            'en': {
                "Type": "IQF (Individually Quick Frozen)",
                "Variety": "Keitt • Tommy Atkins • Kent",
                "Processing": "Chunks • Slices • Diced options",
                "Size": "10x10mm to 20x20mm pieces",
                "Brix Level": "14-18% (minimum 12%)",
                "Color": "Golden yellow to orange",
                "Temperature": "-18°C or below",
                "Packaging": "10kg • 20kg • 25kg cartons",
                "Shelf Life": "24 months frozen",
                "Quality": "Grade A • Premium quality"
            },
            'ar': {
                "النوع": "مجمد فردي سريع (IQF)",
                "الصنف": "كيت • تومي أتكينز • كينت",
                "المعالجة": "قطع • شرائح • مكعبات",
                "الحجم": "قطع 10×10 مم إلى 20×20 مم",
                "مستوى البريكس": "14-18% (الحد الأدنى 12%)",
                "اللون": "أصفر ذهبي إلى برتقالي",
                "درجة الحرارة": "-18 درجة مئوية أو أقل",
                "التعبئة": "كراتين 10 كجم • 20 كجم • 25 كجم",
                "مدة الصلاحية": "24 شهر مجمد",
                "الجودة": "درجة أ • جودة ممتازة"
            }
        }
    }
