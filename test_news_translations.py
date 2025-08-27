#!/usr/bin/env python3
"""
Test script to verify news translations are working correctly
"""

from simple_translations import translate

def test_news_translations():
    """Test news-specific translations"""
    
    print("🔍 Testing News Translation System")
    print("=" * 50)
    
    # Test strings for news management
    test_strings = [
        'News Management',
        'Add New Article', 
        'Edit Article',
        'Article Details',
        'English Content',
        'Arabic Content',
        'Draft',
        'Published',
        'Archived',
        'Scheduled',
        'Featured',
        'Save Draft',
        'Publish',
        'Back to News',
        'Search articles...',
        'No articles found',
        'No Image',
        'Admin Panel',
        'Status',
        'Author',
        'Created At',
        'Actions',
        'Cover Image',
        'Tags',
        'Content',
        'Title',
        'Excerpt'
    ]
    
    print("\n📝 Testing Arabic Translations:")
    print("-" * 40)
    
    for string in test_strings:
        translated = translate(string, 'ar')
        status = "✅" if translated != string else "❌"
        print(f"{status} '{string}' -> '{translated}'")
    
    print("\n📝 Testing English Translations:")
    print("-" * 40)
    
    for string in test_strings:
        translated = translate(string, 'en')
        status = "✅" if translated == string else "❌"
        print(f"{status} '{string}' -> '{translated}'")
    
    print("\n🎯 Form Field Translations:")
    print("-" * 40)
    
    form_fields = [
        'Title (English)',
        'Title (Arabic)',
        'Content (English)',
        'Content (Arabic)',
        'Featured Article',
        'Content Difficulty',
        'Beginner',
        'Intermediate',
        'Advanced',
        'Expert'
    ]
    
    for field in form_fields:
        ar_translation = translate(field, 'ar')
        en_translation = translate(field, 'en')
        ar_status = "✅" if ar_translation != field else "❌"
        en_status = "✅" if en_translation == field else "❌"
        print(f"{ar_status}{en_status} {field}: AR='{ar_translation}' | EN='{en_translation}'")
    
    print("\n🎉 News Translation Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_news_translations()
