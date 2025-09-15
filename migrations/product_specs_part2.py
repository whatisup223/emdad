#!/usr/bin/env python3
"""
Additional product specifications - Part 2
Dates, Spices, Seeds, and Herbs
"""

def get_additional_specifications():
    """Return specifications for dates, spices, seeds, and herbs."""
    return {
        # Dates
        'dates-whole': {
            'en': {
                "Variety": "Zahidi • Halawi • Deglet Noor",
                "Grade": "Grade A • Premium quality",
                "Moisture": "18-25% (typical 20-22%)",
                "Size": "2.5-4.0cm length",
                "Color": "Golden brown to dark brown",
                "Texture": "Soft to semi-dry",
                "Sugar Content": "65-80% (natural sugars)",
                "Shelf Life": "12-18 months in proper storage",
                "Packaging": "5kg • 10kg • 25kg cartons"
            },
            'ar': {
                "الصنف": "زهيدي • حلاوي • دقلة نور",
                "الدرجة": "درجة أ • جودة ممتازة",
                "الرطوبة": "18-25% (نموذجي 20-22%)",
                "الحجم": "2.5-4.0 سم طول",
                "اللون": "بني ذهبي إلى بني غامق",
                "القوام": "طري إلى شبه جاف",
                "محتوى السكر": "65-80% (سكريات طبيعية)",
                "مدة الصلاحية": "12-18 شهر في التخزين المناسب",
                "التعبئة": "كراتين 5 كجم • 10 كجم • 25 كجم"
            }
        },

        'dates-pitted': {
            'en': {
                "Variety": "Zahidi • Halawi • Deglet Noor",
                "Processing": "Machine pitted, pit-free",
                "Grade": "Grade A • Premium quality",
                "Moisture": "18-25% (typical 20-22%)",
                "Size": "2.5-4.0cm length",
                "Color": "Golden brown to dark brown",
                "Texture": "Soft, ready to eat",
                "Quality": "No broken pieces, uniform",
                "Shelf Life": "12-18 months in proper storage"
            },
            'ar': {
                "الصنف": "زهيدي • حلاوي • دقلة نور",
                "المعالجة": "منزوع النوى آلياً، خالي من النوى",
                "الدرجة": "درجة أ • جودة ممتازة",
                "الرطوبة": "18-25% (نموذجي 20-22%)",
                "الحجم": "2.5-4.0 سم طول",
                "اللون": "بني ذهبي إلى بني غامق",
                "القوام": "طري، جاهز للأكل",
                "الجودة": "بدون قطع مكسورة، موحد",
                "مدة الصلاحية": "12-18 شهر في التخزين المناسب"
            }
        },

        'medjool-dates-whole': {
            'en': {
                "Variety": "Medjool • King of Dates",
                "Grade": "Jumbo • Large • Medium sizes",
                "Moisture": "23-27% (soft texture)",
                "Size": "4-6cm length, 2-3cm width",
                "Color": "Dark brown to reddish-brown",
                "Texture": "Soft, chewy, moist",
                "Flavor": "Rich, sweet, caramel-like",
                "Quality": "Premium grade, hand-selected",
                "Shelf Life": "12-24 months refrigerated"
            },
            'ar': {
                "الصنف": "مجهول • ملك التمور",
                "الدرجة": "جامبو • كبير • أحجام متوسطة",
                "الرطوبة": "23-27% (قوام طري)",
                "الحجم": "4-6 سم طول، 2-3 سم عرض",
                "اللون": "بني غامق إلى بني محمر",
                "القوام": "طري، مطاطي، رطب",
                "النكهة": "غنية، حلوة، تشبه الكراميل",
                "الجودة": "درجة ممتازة، منتقى يدوياً",
                "مدة الصلاحية": "12-24 شهر مبرد"
            }
        },

        'medjool-dates-pitted': {
            'en': {
                "Variety": "Medjool • King of Dates",
                "Processing": "Hand-pitted, premium quality",
                "Grade": "Jumbo • Large • Medium sizes",
                "Moisture": "23-27% (soft texture)",
                "Size": "4-6cm length, 2-3cm width",
                "Color": "Dark brown to reddish-brown",
                "Texture": "Soft, chewy, ready to eat",
                "Quality": "No broken pieces, premium grade",
                "Shelf Life": "12-24 months refrigerated"
            },
            'ar': {
                "الصنف": "مجهول • ملك التمور",
                "المعالجة": "منزوع النوى يدوياً، جودة ممتازة",
                "الدرجة": "جامبو • كبير • أحجام متوسطة",
                "الرطوبة": "23-27% (قوام طري)",
                "الحجم": "4-6 سم طول، 2-3 سم عرض",
                "اللون": "بني غامق إلى بني محمر",
                "القوام": "طري، مطاطي، جاهز للأكل",
                "الجودة": "بدون قطع مكسورة، درجة ممتازة",
                "مدة الصلاحية": "12-24 شهر مبرد"
            }
        },

        # Spices
        'cumin-seed': {
            'en': {
                "Botanical Name": "Cuminum cyminum",
                "Origin": "Egypt • India • Middle East",
                "Purity": "99% minimum",
                "Moisture": "≤ 10%",
                "Essential Oil": "2.5-4.5%",
                "Color": "Brown to dark brown",
                "Flavor": "Warm, earthy, slightly bitter",
                "Mesh Size": "8-40 mesh (whole seeds)",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Cuminum cyminum",
                "المنشأ": "مصر • الهند • الشرق الأوسط",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "2.5-4.5%",
                "اللون": "بني إلى بني غامق",
                "النكهة": "دافئة، ترابية، مرة قليلاً",
                "حجم الشبكة": "8-40 شبكة (بذور كاملة)",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'coriander-seed': {
            'en': {
                "Botanical Name": "Coriandrum sativum",
                "Origin": "Egypt • India • Eastern Europe",
                "Purity": "99% minimum",
                "Moisture": "≤ 10%",
                "Essential Oil": "0.8-2.6%",
                "Color": "Light brown to yellowish-brown",
                "Flavor": "Sweet, citrusy, slightly spicy",
                "Size": "3-5mm diameter",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Coriandrum sativum",
                "المنشأ": "مصر • الهند • أوروبا الشرقية",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "0.8-2.6%",
                "اللون": "بني فاتح إلى بني مصفر",
                "النكهة": "حلوة، حمضية، حارة قليلاً",
                "الحجم": "3-5 مم قطر",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'fennel-seed': {
            'en': {
                "Botanical Name": "Foeniculum vulgare",
                "Origin": "Egypt • India • Mediterranean",
                "Purity": "99% minimum",
                "Moisture": "≤ 10%",
                "Essential Oil": "2-6%",
                "Color": "Greenish-brown to brown",
                "Flavor": "Sweet, licorice-like, aromatic",
                "Size": "4-8mm length",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Foeniculum vulgare",
                "المنشأ": "مصر • الهند • البحر المتوسط",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "2-6%",
                "اللون": "بني مخضر إلى بني",
                "النكهة": "حلوة، تشبه العرقسوس، عطرية",
                "الحجم": "4-8 مم طول",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'anise-seed': {
            'en': {
                "Botanical Name": "Pimpinella anisum",
                "Origin": "Egypt • Turkey • Syria",
                "Purity": "99% minimum",
                "Moisture": "≤ 10%",
                "Essential Oil": "2-6%",
                "Color": "Greenish-brown to brown",
                "Flavor": "Sweet, licorice-like, intense",
                "Size": "2-4mm length",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Pimpinella anisum",
                "المنشأ": "مصر • تركيا • سوريا",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "2-6%",
                "اللون": "بني مخضر إلى بني",
                "النكهة": "حلوة، تشبه العرقسوس، قوية",
                "الحجم": "2-4 مم طول",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        },

        'caraway-seed': {
            'en': {
                "Botanical Name": "Carum carvi",
                "Origin": "Egypt • Netherlands • Eastern Europe",
                "Purity": "99% minimum",
                "Moisture": "≤ 10%",
                "Essential Oil": "3-7%",
                "Color": "Dark brown",
                "Flavor": "Sharp, pungent, slightly bitter",
                "Size": "3-5mm length",
                "Shelf Life": "24 months in proper storage"
            },
            'ar': {
                "الاسم النباتي": "Carum carvi",
                "المنشأ": "مصر • هولندا • أوروبا الشرقية",
                "النقاء": "99% كحد أدنى",
                "الرطوبة": "≤ 10%",
                "الزيت العطري": "3-7%",
                "اللون": "بني غامق",
                "النكهة": "حادة، نفاذة، مرة قليلاً",
                "الحجم": "3-5 مم طول",
                "مدة الصلاحية": "24 شهر في التخزين المناسب"
            }
        }
    }
