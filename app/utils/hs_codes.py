#!/usr/bin/env python3
"""
HS Code descriptions and utilities
Harmonized System codes with accurate descriptions for each product category
"""

def get_hs_code_descriptions():
    """
    Returns accurate descriptions for HS codes used in our products.
    Based on official Harmonized System classification.
    """
    return {
        # Fresh Citrus Fruits (Chapter 08.05)
        '080510': {
            'en': 'Fresh oranges',
            'ar': 'برتقال طازج'
        },
        '080520': {
            'en': 'Fresh mandarins (including tangerines and satsumas)',
            'ar': 'مندرين طازج (يشمل اليوسفي والساتسوما)'
        },
        
        # Fresh Fruits (Chapter 08)
        '080450': {
            'en': 'Fresh mangoes',
            'ar': 'مانجو طازج'
        },
        '080610': {
            'en': 'Fresh grapes',
            'ar': 'عنب طازج'
        },
        '081010': {
            'en': 'Fresh strawberries',
            'ar': 'فراولة طازجة'
        },
        '081090': {
            'en': 'Other fresh fruits',
            'ar': 'فواكه طازجة أخرى'
        },
        '080410': {
            'en': 'Fresh or dried dates',
            'ar': 'تمر طازج أو مجفف'
        },
        
        # Vegetables (Chapter 07)
        '070190': {
            'en': 'Other fresh potatoes',
            'ar': 'بطاطس طازجة أخرى'
        },
        '070310': {
            'en': 'Fresh onions and shallots',
            'ar': 'بصل وكراث طازج'
        },
        '070320': {
            'en': 'Fresh garlic',
            'ar': 'ثوم طازج'
        },
        '070390': {
            'en': 'Other fresh leeks and alliaceous vegetables',
            'ar': 'كراث وخضروات ثومية طازجة أخرى'
        },
        '071420': {
            'en': 'Fresh sweet potatoes',
            'ar': 'بطاطا حلوة طازجة'
        },
        
        # Spices (Chapter 09.09)
        '090920': {
            'en': 'Coriander seeds',
            'ar': 'بذور كزبرة'
        },
        '090930': {
            'en': 'Cumin seeds',
            'ar': 'بذور كمون'
        },
        '090940': {
            'en': 'Caraway seeds',
            'ar': 'بذور كراوية'
        },
        '090950': {
            'en': 'Anise, badian, fennel, coriander seeds',
            'ar': 'يانسون، بادیان، شمر، بذور كزبرة'
        },
        '090960': {
            'en': 'Juniper berries and other spices',
            'ar': 'توت العرعر وتوابل أخرى'
        },
        
        # Oil Seeds (Chapter 12)
        '120400': {
            'en': 'Flax seeds (linseed)',
            'ar': 'بذور الكتان'
        },
        '120740': {
            'en': 'Sesame seeds',
            'ar': 'بذور سمسم'
        },
        '121190': {
            'en': 'Plants, seeds and fruits used in perfumery, pharmacy or for insecticidal purposes',
            'ar': 'نباتات وبذور وثمار تستعمل في العطارة أو الصيدلة أو لأغراض مبيدة للحشرات'
        },
        
        # Frozen Fruits (Chapter 08.11)
        '081110': {
            'en': 'Frozen strawberries',
            'ar': 'فراولة مجمدة'
        },
        '081140': {
            'en': 'Frozen mangoes',
            'ar': 'مانجو مجمدة'
        }
    }

def get_hs_code_description(hs_code, language='en'):
    """
    Get the description for a specific HS code in the specified language.
    
    Args:
        hs_code (str): The HS code (e.g., '080510')
        language (str): Language code ('en' or 'ar')
    
    Returns:
        str: Description of the HS code or None if not found
    """
    descriptions = get_hs_code_descriptions()
    code_info = descriptions.get(hs_code)
    
    if code_info:
        return code_info.get(language, code_info.get('en'))
    
    return None

def get_hs_code_category(hs_code):
    """
    Get the general category for an HS code.
    
    Args:
        hs_code (str): The HS code
    
    Returns:
        dict: Category information with English and Arabic names
    """
    if not hs_code:
        return None
    
    # Extract first 2 digits for chapter classification
    chapter = hs_code[:2]
    
    categories = {
        '07': {
            'en': 'Vegetables and certain roots and tubers',
            'ar': 'خضروات وجذور ودرنات معينة'
        },
        '08': {
            'en': 'Fruits and nuts',
            'ar': 'فواكه ومكسرات'
        },
        '09': {
            'en': 'Coffee, tea, spices',
            'ar': 'قهوة وشاي وتوابل'
        },
        '12': {
            'en': 'Oil seeds and oleaginous fruits',
            'ar': 'بذور زيتية وثمار زيتية'
        }
    }
    
    return categories.get(chapter, {
        'en': 'Other agricultural products',
        'ar': 'منتجات زراعية أخرى'
    })

def format_hs_code_display(hs_code, language='en'):
    """
    Format HS code for display with description.
    
    Args:
        hs_code (str): The HS code
        language (str): Language code ('en' or 'ar')
    
    Returns:
        str: Formatted display string
    """
    if not hs_code:
        return None
    
    description = get_hs_code_description(hs_code, language)
    
    if description:
        return f"{hs_code} — {description}"
    else:
        # Fallback for unknown codes
        category = get_hs_code_category(hs_code)
        if category:
            return f"{hs_code} — {category[language]}"
        else:
            return hs_code
