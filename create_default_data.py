#!/usr/bin/env python3
"""
Script to create default data for production/development
Creates default categories, products, and news articles
"""

from app import create_app
from app.models import db, Category, Product, News, ProductImage, CompanyInfo
from datetime import datetime
import os

def create_default_categories():
    """Create default product categories"""
    categories = [
        {
            'name_en': 'Fresh Citrus',
            'name_ar': 'الحمضيات الطازجة',
            'slug': 'fresh-citrus',
            'description_en': 'Premium quality fresh citrus fruits from Egypt\'s finest groves.',
            'description_ar': 'حمضيات طازجة عالية الجودة من أفضل بساتين مصر.',
            'key': 'fresh-citrus',
            'sort_order': 1,
            'is_active': True
        },
        {
            'name_en': 'Fresh Vegetables',
            'name_ar': 'الخضروات الطازجة',
            'slug': 'fresh-vegetables',
            'description_en': 'Farm-fresh vegetables grown with sustainable agricultural practices.',
            'description_ar': 'خضروات طازجة من المزرعة مزروعة بممارسات زراعية مستدامة.',
            'key': 'fresh-vegetables',
            'sort_order': 2,
            'is_active': True
        },
        {
            'name_en': 'Frozen Products',
            'name_ar': 'المنتجات المجمدة',
            'slug': 'frozen-products',
            'description_en': 'IQF frozen fruits and vegetables maintaining nutritional value.',
            'description_ar': 'فواكه وخضروات مجمدة بتقنية IQF تحافظ على القيمة الغذائية.',
            'key': 'frozen-products',
            'sort_order': 3,
            'is_active': True
        },
        {
            'name_en': 'Dried Fruits',
            'name_ar': 'الفواكه المجففة',
            'slug': 'dried-fruits',
            'description_en': 'Naturally dried fruits with concentrated flavors and nutrients.',
            'description_ar': 'فواكه مجففة طبيعياً بنكهات مركزة وعناصر غذائية.',
            'key': 'dried-fruits',
            'sort_order': 4,
            'is_active': True
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        # Check if category already exists
        existing = Category.query.filter_by(key=cat_data['key']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
            created_categories.append(category)
            print(f"✅ Created category: {cat_data['name_en']}")
        else:
            print(f"⚠️  Category already exists: {cat_data['name_en']}")
            created_categories.append(existing)
    
    return created_categories

def create_default_products(categories):
    """Create default featured products"""
    products = [
        {
            'name_en': 'Premium Valencia Oranges',
            'name_ar': 'برتقال فالنسيا المميز',
            'slug': 'premium-valencia-oranges',
            'short_description_en': 'Sweet and juicy Valencia oranges, perfect for fresh consumption and juice production.',
            'short_description_ar': 'برتقال فالنسيا الحلو والعصيري، مثالي للاستهلاك الطازج وإنتاج العصير.',
            'description_en': 'Our premium Valencia oranges are carefully selected from the finest groves in Egypt. Known for their exceptional sweetness and high juice content, these oranges are perfect for both fresh consumption and commercial juice production.',
            'description_ar': 'يتم اختيار برتقال فالنسيا المميز بعناية من أفضل البساتين في مصر. معروف بحلاوته الاستثنائية ومحتواه العالي من العصير، هذا البرتقال مثالي للاستهلاك الطازج وإنتاج العصير التجاري.',
            'category_key': 'fresh-citrus',
            'featured': True,
            'status': 'active',
            'sort_order': 1
        },
        {
            'name_en': 'Fresh Red Onions',
            'name_ar': 'البصل الأحمر الطازج',
            'slug': 'fresh-red-onions',
            'short_description_en': 'High-quality red onions with strong flavor and excellent storage life.',
            'short_description_ar': 'بصل أحمر عالي الجودة بنكهة قوية وعمر تخزين ممتاز.',
            'description_en': 'Our fresh red onions are grown in optimal conditions and carefully harvested to ensure maximum flavor and quality. They have excellent storage properties and are perfect for export markets.',
            'description_ar': 'يُزرع البصل الأحمر الطازج في ظروف مثلى ويُحصد بعناية لضمان أقصى نكهة وجودة. له خصائص تخزين ممتازة ومثالي لأسواق التصدير.',
            'category_key': 'fresh-vegetables',
            'featured': True,
            'status': 'active',
            'sort_order': 2
        },
        {
            'name_en': 'IQF Strawberries',
            'name_ar': 'الفراولة المجمدة',
            'slug': 'iqf-strawberries',
            'short_description_en': 'Individually Quick Frozen strawberries maintaining fresh taste and nutrition.',
            'short_description_ar': 'فراولة مجمدة بتقنية التجميد السريع الفردي تحافظ على الطعم الطازج والتغذية.',
            'description_en': 'Our IQF strawberries are processed using advanced freezing technology that preserves the natural taste, color, and nutritional value. Perfect for food processing and retail markets.',
            'description_ar': 'تُعالج الفراولة المجمدة باستخدام تقنية التجميد المتقدمة التي تحافظ على الطعم الطبيعي واللون والقيمة الغذائية. مثالية لمعالجة الأغذية وأسواق التجزئة.',
            'category_key': 'frozen-products',
            'featured': True,
            'status': 'active',
            'sort_order': 3
        }
    ]
    
    created_products = []
    for prod_data in products:
        # Find category
        category = next((cat for cat in categories if cat.key == prod_data['category_key']), None)
        if not category:
            print(f"⚠️  Category not found for product: {prod_data['name_en']}")
            continue
            
        # Check if product already exists
        existing = Product.query.filter_by(slug=prod_data['slug']).first()
        if not existing:
            # Remove category_key from data and add category_id
            prod_data_copy = prod_data.copy()
            del prod_data_copy['category_key']
            prod_data_copy['category_id'] = category.id
            
            product = Product(**prod_data_copy)
            db.session.add(product)
            created_products.append(product)
            print(f"✅ Created product: {prod_data['name_en']}")
        else:
            print(f"⚠️  Product already exists: {prod_data['name_en']}")
            created_products.append(existing)
    
    return created_products

def create_about_intro():
    """Create about intro section if it doesn't exist"""
    existing = CompanyInfo.query.filter_by(key='about_intro').first()

    if existing:
        print(f"⚠️  About intro already exists: {existing.title_en}")
        return

    about_intro = CompanyInfo(
        key='about_intro',
        title_en='About Emdad Global',
        title_ar='حول إمداد جلوبال',
        content_en='<p>Emdad Global is a leading Egyptian export company specializing in premium agricultural products. With over 25 years of experience, we have built a reputation for delivering the highest quality fresh and frozen fruits and vegetables to markets worldwide.</p><p>Our commitment to excellence, combined with state-of-the-art facilities and international certifications, ensures that our products meet the strictest quality standards demanded by global markets.</p>',
        content_ar='<p>إمداد جلوبال هي شركة تصدير مصرية رائدة متخصصة في المنتجات الزراعية الممتازة. مع أكثر من 25 عاماً من الخبرة، بنينا سمعة في تقديم أعلى جودة من الفواكه والخضروات الطازجة والمجمدة إلى الأسواق في جميع أنحاء العالم.</p>',
        is_active=True,
        sort_order=1
    )
    db.session.add(about_intro)
    print(f"✅ Created about intro section")

def create_default_news():
    """Create default news articles if less than 3 exist"""
    existing_count = News.query.filter_by(status='published').count()

    if existing_count >= 3:
        print(f"⚠️  Already have {existing_count} published articles. Skipping news creation.")
        return
    
    articles = [
        {
            'title_en': 'Expanding Global Reach',
            'title_ar': 'توسيع النطاق العالمي',
            'slug': 'expanding-global-reach',
            'excerpt_en': 'Emdad Global announces new partnerships in European and Asian markets, strengthening our international presence.',
            'excerpt_ar': 'تعلن إمداد جلوبال عن شراكات جديدة في الأسواق الأوروبية والآسيوية، مما يعزز حضورنا الدولي.',
            'content_en': 'We are excited to announce our expansion into new markets across Europe and Asia. These strategic partnerships will allow us to bring Egyptian agricultural excellence to more customers worldwide.',
            'content_ar': 'نحن متحمسون للإعلان عن توسعنا في أسواق جديدة عبر أوروبا وآسيا. هذه الشراكات الاستراتيجية ستتيح لنا تقديم التميز الزراعي المصري لمزيد من العملاء حول العالم.',
            'status': 'published',
            'featured': True,
            'publish_at': datetime.utcnow(),
            'tags': 'expansion,partnerships,europe,asia'
        },
        {
            'title_en': 'Quality Certification Update',
            'title_ar': 'تحديث شهادات الجودة',
            'slug': 'quality-certification-update',
            'excerpt_en': 'Successfully renewed ISO 22000 and Good Agricultural Practices certifications, reinforcing our commitment to quality standards.',
            'excerpt_ar': 'تم تجديد شهادات ISO 22000 وممارسات الزراعة الجيدة بنجاح، مما يعزز التزامنا بمعايير الجودة.',
            'content_en': 'We are proud to announce the successful renewal of our ISO 22000 and Good Agricultural Practices certifications. This achievement reinforces our unwavering commitment to maintaining the highest quality standards.',
            'content_ar': 'نحن فخورون بالإعلان عن التجديد الناجح لشهادات ISO 22000 وممارسات الزراعة الجيدة. هذا الإنجاز يعزز التزامنا الثابت بالحفاظ على أعلى معايير الجودة.',
            'status': 'published',
            'featured': False,
            'publish_at': datetime.utcnow(),
            'tags': 'certification,quality,iso22000,gap'
        },
        {
            'title_en': 'Sustainable Agriculture Initiative',
            'title_ar': 'مبادرة الزراعة المستدامة',
            'slug': 'sustainable-agriculture-initiative',
            'excerpt_en': 'Launching new sustainable farming practices to support environmental conservation and premium product quality.',
            'excerpt_ar': 'إطلاق ممارسات زراعية مستدامة جديدة لدعم الحفاظ على البيئة وجودة المنتجات المتميزة.',
            'content_en': 'Our new sustainable agriculture initiative focuses on environmentally friendly farming practices that not only protect our planet but also enhance the quality of our products.',
            'content_ar': 'تركز مبادرة الزراعة المستدامة الجديدة على الممارسات الزراعية الصديقة للبيئة التي لا تحمي كوكبنا فحسب، بل تعزز أيضاً جودة منتجاتنا.',
            'status': 'published',
            'featured': False,
            'publish_at': datetime.utcnow(),
            'tags': 'sustainability,environment,farming,quality'
        }
    ]
    
    for article_data in articles:
        # Check if article already exists
        existing = News.query.filter_by(slug=article_data['slug']).first()
        if not existing:
            article = News(**article_data)
            db.session.add(article)
            print(f"✅ Created news article: {article_data['title_en']}")
        else:
            print(f"⚠️  News article already exists: {article_data['title_en']}")

def main():
    """Main function to create all default data"""
    app = create_app()
    
    with app.app_context():
        print("🚀 Creating default data for Emdad Global...")
        print("=" * 50)
        
        # Create about intro
        print("\n📄 Creating about intro section...")
        create_about_intro()

        # Create categories
        print("\n📁 Creating default categories...")
        categories = create_default_categories()

        # Commit categories first
        db.session.commit()

        # Create products
        print("\n🥕 Creating default products...")
        products = create_default_products(categories)

        # Create news articles
        print("\n📰 Creating default news articles...")
        create_default_news()
        
        # Final commit
        db.session.commit()
        
        print("\n" + "=" * 50)
        print("✅ Default data creation completed successfully!")
        print(f"📁 Categories: {len(categories)}")
        print(f"🥕 Products: {len(products)}")
        print("📰 News articles: Check manually")
        print("\n🌐 Your website now has default content for production!")

if __name__ == "__main__":
    main()
