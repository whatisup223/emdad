#!/usr/bin/env python3
"""
Populate default values for product detail fields:
- packaging_options
- applications
- quality_targets (typical targets)
- commercial_docs

Design:
- Bilingual JSON structure: { 'en': {...}, 'ar': {...} }
- Category-aware templates with a few product-level overrides
- Idempotent: only fills fields that are empty (or missing). Does NOT overwrite existing values unless force_update=True
- Guarded with AppMeta flag so it won't repeat unnecessarily in production
"""

import json


def _merge(a, b):
    """Shallow merge dict b into dict a and return result (does not mutate inputs)."""
    out = dict(a or {})
    for k, v in (b or {}).items():
        out[k] = v
    return out


def get_category_defaults():
    """Category-level defaults for the four fields.
    Keys are Category.key values as used in seeds (e.g., 'fresh-citrus', 'fresh-fruit').
    """
    return {
        # Citrus
        'fresh-citrus': {
            'packaging_options': {
                'en': {
                    'Bulk Packaging': '15kg export cartons • 10x1kg net bags',
                    'Retail': '1kg • 2kg consumer nets (by request)',
                    'Cold Chain': 'Chilled 4–8°C; avoid freezing',
                },
                'ar': {
                    'التعبئة بالجملة': 'كراتين تصدير 15كجم • شِباك 10×1كجم',
                    'التجزئة': 'أكياس شبكية 1كجم • 2كجم (حسب الطلب)',
                    'سلسلة التبريد': 'تبريد 4–8°م؛ تجنب التجميد',
                },
            },
            'applications': {
                'en': {
                    'Beverages': 'Fresh juice • Blends • Concentrates',
                    'Culinary': 'Fresh consumption • Fruit salads',
                },
                'ar': {
                    'المشروبات': 'عصير طازج • خلطات • مركزات',
                    'الطهي': 'استهلاك طازج • سلطات فواكه',
                },
            },
            'quality_targets': {
                'en': {
                    'Brix': '11–13° (typical)',
                    'Residues': 'Within EU MRL limits',
                    'Defects': 'Sorted to export grade; sound fruit',
                },
                'ar': {
                    'البركس': '°11–13 (نموذجي)',
                    'المتبقيات': 'ضمن حدود الاتحاد الأوروبي (MRL)',
                    'العيوب': 'فرز بجودة تصدير؛ ثمار سليمة',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # Fresh fruits
        'fresh-fruit': {
            'packaging_options': {
                'en': {
                    'Retail': 'Clamshells 250g • 400g • 500g (by product)',
                    'Bulk': '2–5kg cartons (varies by product)',
                    'Cold Chain': '0–5°C depending on product',
                },
                'ar': {
                    'التجزئة': 'علب كلارشيل 250جم • 400جم • 500جم (حسب المنتج)',
                    'الجملة': 'كراتين 2–5كجم (حسب المنتج)',
                    'سلسلة التبريد': '0–5°م حسب المنتج',
                },
            },
            'applications': {
                'en': {
                    'Fresh Use': 'Direct consumption • Fruit bowls',
                    'Processing': 'Jams • Purees • Desserts',
                },
                'ar': {
                    'الاستهلاك الطازج': 'استهلاك مباشر • أطباق فواكه',
                    'التصنيع': 'مربيات • بيوريه • حلويات',
                },
            },
            'quality_targets': {
                'en': {
                    'Brix': 'Typical per product variety',
                    'Color': 'Uniform color per grade',
                    'Cold Chain': 'Maintained end-to-end',
                },
                'ar': {
                    'البركس': 'نموذجي حسب الصنف',
                    'اللون': 'لون موحد حسب الدرجة',
                    'سلسلة التبريد': 'مستمرة من المصدر إلى العميل',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },


        },

        # Fresh vegetables
        'fresh-vegetables': {
            'packaging_options': {
                'en': {
                    'Bulk': '25kg mesh/PP bags • 10kg cartons',
                    'Retail': '1kg • 2kg consumer bags (by product)',
                    'Storage': '2–8°C; ventilated as needed',
                },
                'ar': {
                    'الجملة': 'أكياس شبكية/بولي بروبيلين 25كجم • كراتين 10كجم',
                    'التجزئة': 'أكياس 1كجم • 2كجم (حسب المنتج)',
                    'التخزين': '2–8°م؛ تهوية حسب الحاجة',
                },
            },
            'applications': {
                'en': {
                    'Culinary': 'Cooking • Frying • Roasting • Soups',
                    'Processing': 'Chips • Frozen • Dehydrated',
                },
                'ar': {
                    'الطهي': 'طبخ • قلي • تحميص • شوربات',
                    'التصنيع': 'رقائق • تجميد • تجفيف',
                },
            },
            'quality_targets': {
                'en': {
                    'Grading': 'Uniform caliber • Export tolerances',
                    'Dry Matter': 'Typical per product',
                    'Defects': 'Sprouting/soft rot absent',
                },
                'ar': {
                    'الفرز': 'عيار متجانس • سماحات التصدير',
                    'المادة الجافة': 'حسب المنتج',
                    'العيوب': 'خلو من التبرعم/العفن الطري',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # Dates
        'dates': {
            'packaging_options': {
                'en': {
                    'Bulk': '5kg • 10kg cartons',
                    'Retail': '500g • 1kg boxes; Vacuum or Flow Pack',
                    'Cold Chain': 'Chilled 0–5°C',
                },
                'ar': {
                    'الجملة': 'كراتين 5كجم • 10كجم',
                    'التجزئة': 'عبوات 500جم • 1كجم؛ فاكيوم أو فلو باك',
                    'سلسلة التبريد': 'تبريد 0–5°م',
                },
            },
            'applications': {
                'en': {
                    'Snacking': 'Direct consumption',
                    'Processing': 'Bakery • Energy bars • Syrups',
                },
                'ar': {
                    'وجبات خفيفة': 'استهلاك مباشر',
                    'التصنيع': 'مخبوزات • ألواح طاقة • شرابات',
                },
            },
            'quality_targets': {
                'en': {
                    'Moisture': '16–22% typical',
                    'Pests': 'Absent (visual + sieve)',
                    'Metal Detection': 'Passed per lot',
                },
                'ar': {
                    'الرطوبة': '16–22% نموذجي',
                    'الآفات': 'منعدم (فحص بصري ومنخل)',
                    'كشف المعادن': 'مستوفى لكل شحنة',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # IQF
        'iqf': {
            'packaging_options': {
                'en': {
                    'Bulk': '10kg polybag-in-carton',
                    'Retail': '1kg polybags (by request)',
                    'Cold Chain': 'Frozen at ≤ -18°C',
                },
                'ar': {
                    'الجملة': '10كجم كيس بولي داخل كرتون',
                    'التجزئة': '1كجم أكياس بولي (حسب الطلب)',
                    'سلسلة التبريد': 'مجمد عند ≤ -18°م',
                },
            },
            'applications': {
                'en': {
                    'Beverages': 'Smoothies • Shakes',
                    'Food Service': 'Desserts • Toppings',
                },
                'ar': {
                    'المشروبات': 'سموذي • شيك',
                    'الخدمة الغذائية': 'حلويات • إضافات للمنتجات',
                },
            },
            'quality_targets': {
                'en': {
                    'Microbiology': 'Meets frozen RT standards',
                    'Foreign Matter': 'Nil (optical + metal detection)',
                    'Cold Chain': 'Maintained below -18°C',
                },
                'ar': {
                    'الميكروبيولوجيا': 'ضمن معايير المنتجات المجمدة',
                    'شوائب خارجية': 'منعدمة (بصري + كشف معادن)',
                    'سلسلة التجميد': 'أدنى من -18°م باستمرار',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # Spices
        'spices': {
            'packaging_options': {
                'en': {
                    'Bulk': '25kg PP bags • 10–15kg paper bags',
                    'Private Label': 'Glass jars 250g/500g (by request)',
                },
                'ar': {
                    'الجملة': 'أكياس PP 25كجم • أكياس ورقية 10–15كجم',
                    'علامة خاصة': 'برطمانات زجاج 250جم/500جم (حسب الطلب)',
                },
            },
            'applications': {
                'en': {
                    'Spice Blends': 'Seasonings • Mixes',
                    'Bakery': 'Bread • Crackers',
                },
                'ar': {
                    'خلطات التوابل': 'توابل • خلطات',
                    'المخبوزات': 'خبز • مقرمشات',
                },
            },
            'quality_targets': {
                'en': {
                    'Moisture': '≤ 10–12% typical',
                    'Aflatoxin': 'Within EU limits',
                    'Salmonella': 'Absent',
                },
                'ar': {
                    'الرطوبة': '≤ 10–12% نموذجي',
                    'الأفلاتوكسين': 'ضمن حدود الاتحاد الأوروبي',
                    'السالمونيلا': 'منعدمة',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # Herbs & Herbal Plants
        'herbs-herbal-plants': {
            'packaging_options': {
                'en': {
                    'Bulk': '10–20kg compressed bales/cartons',
                    'Retail': 'Tea pouches 50–200g',
                },
                'ar': {
                    'الجملة': 'بالات/كراتين 10–20كجم مضغوطة',
                    'التجزئة': 'أكياس شاي 50–200جم',
                },
            },
            'applications': {
                'en': {
                    'Herbal Tea': 'Infusions • Blends',
                    'Seasoning': 'Culinary use',
                },
                'ar': {
                    'شاي عشبي': 'منقوعات • خلطات',
                    'التتبيل': 'استخدام طهوي',
                },
            },
            'quality_targets': {
                'en': {
                    'Moisture': '≤ 12% typical',
                    'Foreign Matter': '≤ 1%',
                    'Cut Size': 'Uniform per product',
                },
                'ar': {
                    'الرطوبة': '≤ 12% نموذجي',
                    'شوائب خارجية': '≤ 1%',
                    'درجة التقطيع': 'متجانسة حسب المنتج',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },

        # Oil seeds
        'oil-seeds': {
            'packaging_options': {
                'en': {
                    'Bulk': '25kg • 50kg PP bags',
                    'Retail': '1kg consumer packs (by request)',
                },
                'ar': {
                    'الجملة': 'أكياس PP 25كجم • 50كجم',
                    'التجزئة': 'عبوات 1كجم للمستهلك (حسب الطلب)',
                },
            },
            'applications': {
                'en': {
                    'Processing': 'Tahini • Oil extraction • Bakery',
                    'Retail': 'Direct use in cooking/baking',
                },
                'ar': {
                    'التصنيع': 'طحينة • عصر زيت • مخبوزات',
                    'التجزئة': 'استخدام مباشر في الطبخ/الخبز',
                },
            },
            'quality_targets': {
                'en': {
                    'Purity': '≥ 99.5% typical',
                    'Moisture': '≤ 8–10%',
                    'Aflatoxin': 'Within EU limits',
                },
                'ar': {
                    'النقاوة': '≥ 99.5% نموذجي',
                    'الرطوبة': '≤ 8–10%',
                    'الأفلاتوكسين': 'ضمن حدود الاتحاد الأوروبي',
                },
            },
            'commercial_docs': {
                'en': {
                    'Payment': 'T/T or L/C (subject to approval)',
                    'MOQ': "Typically 1 × 20' FCL (mix types possible)",
                    'Lead Time': '1–2 weeks after PO (sterilization may add time)',
                    'Incoterms': 'FOB Alexandria / Damietta / Port Said · CFR/CIF on request',
                    'Docs': 'Invoice, Packing List, COO, Phytosanitary (if required), COA, Fumigation (if required)',
                    'Samples': '250–1000 g (courier at cost)',
                    'Private Label': 'Bag printing & carton branding available'
                },
                'ar': {
                    'الدفع': 'تحويل بنكي T/T أو اعتماد L/C (رهناً بالموافقة)',
                    'الحد الأدنى للطلب': "عادة 20 قدم FCL × 1 (إمكانية خلط الأنواع)",
                    'مدة التجهيز': '1–2 أسبوع بعد أمر الشراء (قد تضيف التعقيم وقتاً)',
                    'مصطلحات الشحن': 'FOB الإسكندرية/دمياط/بورسعيد · CFR/CIF عند الطلب',
                    'المستندات': 'فاتورة، بيان تعبئة، شهادة منشأ، شهادة صحة نباتية (إن لزم)، شهادة تحليل COA، تبخير (إن لزم)',
                    'العيّنات': '250–1000 جم (شحن سريع على نفقة العميل)',
                    'علامة خاصة': 'طباعة على الأكياس وتخصيص العلامة على الكراتين متاح'
                },
            },
        },
    }


def get_slug_overrides():
    """Product-specific overrides for notable items where details differ substantially."""
    return {
        # Fresh Strawberries
        'fresh-strawberries': {
            'packaging_options': {
                'en': {
                    'Retail': 'Clamshells 250g • 400g • 500g (with pads)',
                    'Bulk': '2kg cartons (food service)',
                    'Cold Chain': '-0.5–2°C continuous; avoid condensation',
                },
                'ar': {
                    'التجزئة': 'علب كلارشيل 250جم • 400جم • 500جم (مع وسادات)',
                    'الجملة': 'كراتين 2كجم (خدمة غذاء)',
                    'سلسلة التبريد': '-0.5–2°م باستمرار؛ تجنب التكاثف',
                },
            },
            'quality_targets': {
                'en': {
                    'Brix': '7–10° (typical)',
                    'Color': 'Deep, uniform red',
                    'Firmness': 'Firm; free of bruising',
                },
                'ar': {
                    'البركس': '°7–10 (نموذجي)',
                    'اللون': 'أحمر عميق موحد',
                    'الصلابة': 'صلبة وخالية من الكدمات',
                },
            },
        },
        # Fresh Grapes
        'fresh-grapes': {
            'packaging_options': {
                'en': {
                    'Retail': '500g clamshells with vent',
                    'Bulk': '4.5–8kg cartons with liners',
                    'Cold Chain': '-1–0°C; high humidity',
                },
                'ar': {
                    'التجزئة': 'علب 500جم ذات فتحات تهوية',
                    'الجملة': 'كراتين 4.5–8كجم مع بطانة',
                    'سلسلة التبريد': '-1–0°م؛ رطوبة مرتفعة',
                },
            },
            'quality_targets': {
                'en': {
                    'Brix': '16–18° (typical)',
                    'Seeds': 'Seedless preferred for retail',
                },
                'ar': {
                    'البركس': '°16–18 (نموذجي)',
                    'البذور': 'خالٍ من البذور مفضل للبيع بالتجزئة',
                },
            },
        },
        # Potatoes Spunta
        'potatoes-spunta': {
            'quality_targets': {
                'en': {
                    'Size Grading': '55–75 mm (common export size)',
                    'Dry Matter': '19–21% typical',
                    'Defects': 'Sprouting/green/soft rot absent',
                },
                'ar': {
                    'تدرج الحجم': '55–75 مم (حجم تصدير شائع)',
                    'المادة الجافة': '19–21% نموذجي',
                    'العيوب': 'خلو من التبرعم/الاخضرار/العفن الطري',
                },
            },
        },
        # Garlic/Onions
        'garlic-white': {
            'quality_targets': {
                'en': {
                    'Bulb Size': '40–70mm',
                    'Dry Matter': '35–40% typical',
                    'Defects': 'No sprouting; well cured',
                },
                'ar': {
                    'حجم الرأس': '40–70 مم',
                    'المادة الجافة': '35–40% نموذجي',
                    'العيوب': 'بدون تبرعم؛ معالجة وتجفيف جيد',
                },
            },
        },
        'onions-red-golden': {
            'quality_targets': {
                'en': {
                    'Dry Matter': '12–18%',
                    'Pungency': 'Medium to strong',
                    'Storage Life': '6–8 months (proper storage)',
                },
                'ar': {
                    'المادة الجافة': '12–18%',
                    'الحدة': 'متوسطة إلى قوية',
                    'مدة التخزين': '6–8 أشهر (تخزين مناسب)',
                },
            },
        },
        # Dates
        'medjool-dates-whole': {
            'quality_targets': {
                'en': {
                    'Size Grade': 'Jumbo/Large (by request)',
                    'Moisture': '17–22% typical',
                },
                'ar': {
                    'درجة الحجم': 'جامبو/كبير (حسب الطلب)',
                    'الرطوبة': '17–22% نموذجي',
                },
            },
        },
        'medjool-dates-pitted': {
            'quality_targets': {
                'en': {
                    'Pitting': 'Mechanically pitted; fragments controlled',
                },
                'ar': {
                    'نزع النواة': 'ميكانيكياً؛ ضبط الشظايا',
                },
            },
        },
        # IQF specifics
        'iqf-strawberries': {
            'quality_targets': {
                'en': {
                    'Microbiology': 'Meets frozen fruit standards',
                    'Metal Detection': 'Passed',
                },
                'ar': {
                    'الميكروبيولوجيا': 'ضمن معايير الفاكهة المجمدة',
                    'كشف المعادن': 'مستوفى',
                },
            },
        },
        'iqf-mango': {
            'quality_targets': {
                'en': {
                    'Brix': '14–18° (raw material)',
                },
                'ar': {
                    'البركس': '°14–18 (المادة الخام)',
                },
            },
        },
        # Oil seeds specifics
        'sesame-seed': {
            'quality_targets': {
                'en': {
                    'Purity': '≥ 99.9% (premium grades available)',
                },
                'ar': {
                    'النقاوة': '≥ 99.9% (درجات متميزة متاحة)',
                },
            },
        },
    }


def update_product_details_defaults(db=None, force_update=False):
    """Populate default detail fields for products.

    Args:
        db: Database instance (optional). If None, will create app context.
        force_update: If True, overwrite existing values as well.
    """
    try:
        if db is None:
            from app import create_app, db as app_db
            from app.models import Product, Category, AppMeta
            app = create_app()
            with app.app_context():
                return _update_details_internal(app_db, Product, Category, AppMeta, force_update)
        else:
            from app.models import Product, Category, AppMeta
            return _update_details_internal(db, Product, Category, AppMeta, force_update)
    except Exception as e:
        print(f"❌ Error updating product details defaults: {e}")
        import traceback
        traceback.print_exc()
        return False


def _is_empty(val):
    return not bool(val) or (isinstance(val, dict) and len(val) == 0)


def _update_details_internal(db, Product, Category, AppMeta, force_update=False):
    FLAG_KEY = 'seed:product_detail_defaults_v1'

    if not force_update and AppMeta.get(FLAG_KEY):
        print('✅ Product detail defaults already applied (flag present). Skipping.')
        return True

    cat_defaults = get_category_defaults()
    slug_over = get_slug_overrides()

    updated = 0
    products = Product.query.join(Category).add_entity(Category).all()

    for prod, cat in products:
        try:
            ckey = getattr(cat, 'key', None)
            base = cat_defaults.get(ckey, {})
            over = slug_over.get(prod.slug, {})

            # Compute each field's final payload (base + override)
            def build_payload(field):
                b = base.get(field)
                o = over.get(field)
                if b and o:
                    # Merge per language shallowly
                    en = _merge(b.get('en'), o.get('en'))
                    ar = _merge(b.get('ar'), o.get('ar'))
                    return {'en': en, 'ar': ar}
                return o or b or None

            desired = {
                'packaging_options': build_payload('packaging_options'),
                'applications': build_payload('applications'),
                'quality_targets': build_payload('quality_targets'),
                'commercial_docs': build_payload('commercial_docs'),
            }

            # Read current values using model helpers (they normalize shapes)
            current_pack = prod.get_packaging_options()
            current_apps = prod.get_applications()
            current_qfs = prod.get_quality_targets()
            current_com = prod.get_commercial_docs()

            # Decide updates (only if empty or force)
            did_change = False
            if force_update or _is_empty(current_pack):
                if desired['packaging_options']:
                    prod.packaging_options = json.dumps(desired['packaging_options'], ensure_ascii=False)
                    did_change = True
            if force_update or _is_empty(current_apps):
                if desired['applications']:
                    prod.applications = json.dumps(desired['applications'], ensure_ascii=False)
                    did_change = True
            if force_update or _is_empty(current_qfs):
                if desired['quality_targets']:
                    prod.quality_targets = json.dumps(desired['quality_targets'], ensure_ascii=False)
                    did_change = True
            if force_update or _is_empty(current_com):
                if desired['commercial_docs']:
                    prod.commercial_docs = json.dumps(desired['commercial_docs'], ensure_ascii=False)
                    did_change = True

            if did_change:
                updated += 1
        except Exception as e:
            print(f"⚠️ Skipped {prod.slug} due to error: {e}")

    try:
        db.session.commit()
        print(f"✅ Product detail defaults: updated {updated} products")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error committing product detail defaults: {e}")
        return False

    # Set flag if we actually performed updates and not forcing
    if not force_update:
        try:
            from datetime import datetime
            meta = AppMeta(key=FLAG_KEY, value=datetime.utcnow().isoformat())
            db.session.add(meta)
            db.session.commit()
            print('🏁 Flag recorded to avoid re-applying defaults automatically.')
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ Could not record AppMeta flag: {e}")

    return True


if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ok = update_product_details_defaults()
    sys.exit(0 if ok else 1)

