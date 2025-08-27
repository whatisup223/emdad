#!/usr/bin/env python3
"""
Database initialization script for Emdad Global website.
This script creates the database tables and populates them with initial data.
"""

import os
import sys
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    User, Category, Product, ProductImage, Certification, Service, 
    News, Gallery, RFQ, CompanyInfo, AuditLog
)

def create_admin_user():
    """Create default admin user."""
    admin = User.query.filter_by(email='admin@emdadglobal.com').first()
    if not admin:
        admin = User(
            name='Admin User',
            email='admin@emdadglobal.com',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')  # Change this in production!
        db.session.add(admin)
        print("✓ Created admin user (admin@emdadglobal.com / admin123)")
    else:
        print("✓ Admin user already exists")

def create_categories():
    """Create product categories."""
    categories_data = [
        {
            'key': 'citrus',
            'name_en': 'Citrus Fruits',
            'name_ar': 'الحمضيات',
            'slug': 'citrus-fruits',
            'description_en': 'Premium Egyptian citrus fruits including oranges, mandarins, lemons, and more.',
            'description_ar': 'ثمار الحمضيات المصرية الممتازة بما في ذلك البرتقال واليوسفي والليمون وغيرها.',
            'sort_order': 1
        },
        {
            'key': 'fresh-fruits',
            'name_en': 'Fresh Fruits',
            'name_ar': 'الفواكه الطازجة',
            'slug': 'fresh-fruits',
            'description_en': 'Fresh seasonal fruits including grapes, mangoes, pomegranates, and dates.',
            'description_ar': 'الفواكه الموسمية الطازجة بما في ذلك العنب والمانجو والرمان والتمر.',
            'sort_order': 2
        },
        {
            'key': 'fresh-vegetables',
            'name_en': 'Fresh Vegetables',
            'name_ar': 'الخضروات الطازجة',
            'slug': 'fresh-vegetables',
            'description_en': 'High-quality fresh vegetables including garlic, onions, carrots, and potatoes.',
            'description_ar': 'خضروات طازجة عالية الجودة بما في ذلك الثوم والبصل والجزر والبطاطس.',
            'sort_order': 3
        },
        {
            'key': 'frozen-fruits',
            'name_en': 'Frozen Fruits (IQF)',
            'name_ar': 'الفواكه المجمدة',
            'slug': 'frozen-fruits',
            'description_en': 'Individually Quick Frozen (IQF) fruits maintaining freshness and nutritional value.',
            'description_ar': 'فواكه مجمدة بسرعة فردية تحافظ على النضارة والقيمة الغذائية.',
            'sort_order': 4
        }
    ]
    
    for cat_data in categories_data:
        category = Category.query.filter_by(key=cat_data['key']).first()
        if not category:
            category = Category(**cat_data)
            db.session.add(category)
            print(f"✓ Created category: {cat_data['name_en']}")

def create_products():
    """Create sample products."""
    # Get categories
    citrus = Category.query.filter_by(key='citrus').first()
    fresh_fruits = Category.query.filter_by(key='fresh-fruits').first()
    vegetables = Category.query.filter_by(key='fresh-vegetables').first()
    frozen = Category.query.filter_by(key='frozen-fruits').first()
    
    products_data = [
        # Citrus Fruits
        {
            'name_en': 'Egyptian Oranges',
            'name_ar': 'البرتقال المصري',
            'slug': 'egyptian-oranges',
            'category_id': citrus.id if citrus else 1,
            'description_en': 'Premium quality Egyptian oranges known for their sweetness and juiciness. Available in various sizes and packaging options.',
            'description_ar': 'برتقال مصري عالي الجودة معروف بحلاوته وعصيريته. متوفر بأحجام وخيارات تعبئة مختلفة.',
            'short_description_en': 'Premium Egyptian oranges with exceptional sweetness and juice content.',
            'specifications': '{"sizes": ["Small (60-70mm)", "Medium (70-80mm)", "Large (80-90mm)"], "brix": "11-13%", "acidity": "0.8-1.2%"}',
            'seasonality': '{"harvest": "December - April", "peak": "January - March"}',
            'packaging_options': '{"bulk": "15kg cartons", "retail": "1kg, 2kg, 5kg bags"}',
            'featured': True,
            'sort_order': 1
        },
        {
            'name_en': 'Mandarins',
            'name_ar': 'اليوسفي',
            'slug': 'mandarins',
            'category_id': citrus.id if citrus else 1,
            'description_en': 'Sweet and easy-to-peel Egyptian mandarins, perfect for fresh consumption and export.',
            'short_description_en': 'Sweet, easy-to-peel mandarins with excellent flavor.',
            'featured': True,
            'sort_order': 2
        },
        # Fresh Fruits
        {
            'name_en': 'Egyptian Grapes',
            'name_ar': 'العنب المصري',
            'slug': 'egyptian-grapes',
            'category_id': fresh_fruits.id if fresh_fruits else 2,
            'description_en': 'High-quality table grapes in various varieties including Thompson Seedless and Red Globe.',
            'short_description_en': 'Premium table grapes in multiple varieties.',
            'featured': True,
            'sort_order': 1
        },
        {
            'name_en': 'Pomegranates',
            'name_ar': 'الرمان',
            'slug': 'pomegranates',
            'category_id': fresh_fruits.id if fresh_fruits else 2,
            'description_en': 'Antioxidant-rich Egyptian pomegranates with deep red color and sweet-tart flavor.',
            'short_description_en': 'Antioxidant-rich pomegranates with exceptional flavor.',
            'featured': True,
            'sort_order': 2
        },
        # Vegetables
        {
            'name_en': 'Egyptian Garlic',
            'name_ar': 'الثوم المصري',
            'slug': 'egyptian-garlic',
            'category_id': vegetables.id if vegetables else 3,
            'description_en': 'Premium white garlic with strong flavor and long shelf life.',
            'short_description_en': 'Premium white garlic with strong flavor.',
            'featured': True,
            'sort_order': 1
        },
        {
            'name_en': 'Red Onions',
            'name_ar': 'البصل الأحمر',
            'slug': 'red-onions',
            'category_id': vegetables.id if vegetables else 3,
            'description_en': 'High-quality red onions with excellent storage capabilities.',
            'short_description_en': 'High-quality red onions with excellent storage.',
            'sort_order': 2
        },
        # Frozen Fruits
        {
            'name_en': 'IQF Strawberries',
            'name_ar': 'الفراولة المجمدة',
            'slug': 'iqf-strawberries',
            'category_id': frozen.id if frozen else 4,
            'description_en': 'Individually Quick Frozen strawberries maintaining fresh taste and nutritional value.',
            'short_description_en': 'IQF strawberries maintaining fresh taste and nutrition.',
            'featured': True,
            'sort_order': 1
        },
        {
            'name_en': 'IQF Mango Chunks',
            'name_ar': 'قطع المانجو المجمدة',
            'slug': 'iqf-mango-chunks',
            'category_id': frozen.id if frozen else 4,
            'description_en': 'Premium frozen mango chunks perfect for smoothies and desserts.',
            'short_description_en': 'Premium frozen mango chunks for various applications.',
            'sort_order': 2
        }
    ]
    
    for prod_data in products_data:
        product = Product.query.filter_by(slug=prod_data['slug']).first()
        if not product:
            product = Product(**prod_data)
            db.session.add(product)
            print(f"✓ Created product: {prod_data['name_en']}")

def create_certifications():
    """Create certifications."""
    certifications_data = [
        {
            'name_en': 'GlobalG.A.P.',
            'name_ar': 'جلوبال جاب',
            'description_en': 'Good Agricultural Practices certification ensuring food safety and sustainability.',
            'description_ar': 'شهادة الممارسات الزراعية الجيدة التي تضمن سلامة الغذاء والاستدامة.',
            'website_url': 'https://www.globalgap.org',
            'sort_order': 1
        },
        {
            'name_en': 'HACCP',
            'name_ar': 'هاسب',
            'description_en': 'Hazard Analysis and Critical Control Points system for food safety.',
            'description_ar': 'نظام تحليل المخاطر ونقاط التحكم الحرجة لسلامة الغذاء.',
            'sort_order': 2
        },
        {
            'name_en': 'ISO 22000',
            'name_ar': 'آيزو 22000',
            'description_en': 'Food Safety Management System certification.',
            'description_ar': 'شهادة نظام إدارة سلامة الغذاء.',
            'sort_order': 3
        },
        {
            'name_en': 'Halal Certification',
            'name_ar': 'شهادة الحلال',
            'description_en': 'Islamic dietary law compliance certification.',
            'description_ar': 'شهادة الامتثال لقوانين الغذاء الإسلامية.',
            'sort_order': 4
        }
    ]
    
    for cert_data in certifications_data:
        certification = Certification.query.filter_by(name_en=cert_data['name_en']).first()
        if not certification:
            certification = Certification(**cert_data)
            db.session.add(certification)
            print(f"✓ Created certification: {cert_data['name_en']}")

def create_services():
    """Create services."""
    services_data = [
        {
            'title_en': 'FOB & CIF Shipping',
            'title_ar': 'الشحن فوب وسيف',
            'description_en': 'Flexible shipping terms including Free on Board (FOB) and Cost, Insurance, and Freight (CIF) options.',
            'description_ar': 'شروط شحن مرنة تشمل خيارات التسليم على ظهر السفينة والتكلفة والتأمين والشحن.',
            'icon': 'fas fa-ship',
            'sort_order': 1
        },
        {
            'title_en': 'Cold Chain Logistics',
            'title_ar': 'لوجستيات السلسلة الباردة',
            'description_en': 'Temperature-controlled storage and transportation to maintain product quality.',
            'description_ar': 'تخزين ونقل محكوم بدرجة الحرارة للحفاظ على جودة المنتج.',
            'icon': 'fas fa-thermometer-half',
            'sort_order': 2
        },
        {
            'title_en': 'Custom Packaging',
            'title_ar': 'التعبئة المخصصة',
            'description_en': 'Tailored packaging solutions to meet specific customer requirements.',
            'description_ar': 'حلول تعبئة مصممة خصيصاً لتلبية متطلبات العملاء المحددة.',
            'icon': 'fas fa-box',
            'sort_order': 3
        },
        {
            'title_en': 'Documentation & Compliance',
            'title_ar': 'التوثيق والامتثال',
            'description_en': 'Complete documentation support and regulatory compliance assistance.',
            'description_ar': 'دعم كامل للتوثيق والمساعدة في الامتثال التنظيمي.',
            'icon': 'fas fa-file-alt',
            'sort_order': 4
        }
    ]
    
    for service_data in services_data:
        service = Service.query.filter_by(title_en=service_data['title_en']).first()
        if not service:
            service = Service(**service_data)
            db.session.add(service)
            print(f"✓ Created service: {service_data['title_en']}")

def create_company_info():
    """Create company information sections."""
    company_info_data = [
        {
            'key': 'about_intro',
            'title_en': 'About Emdad Global',
            'title_ar': 'حول إمداد جلوبال',
            'content_en': '''<p>Emdad Global is a leading Egyptian export company specializing in premium agricultural products. 
            With over 25 years of experience, we have built a reputation for delivering the highest quality fresh and frozen 
            fruits and vegetables to markets worldwide.</p>
            <p>Our commitment to excellence, combined with state-of-the-art facilities and international certifications, 
            ensures that our products meet the strictest quality standards demanded by global markets.</p>''',
            'content_ar': '''<p>إمداد جلوبال هي شركة تصدير مصرية رائدة متخصصة في المنتجات الزراعية الممتازة. 
            مع أكثر من 25 عاماً من الخبرة، بنينا سمعة في تقديم أعلى جودة من الفواكه والخضروات الطازجة والمجمدة 
            إلى الأسواق في جميع أنحاء العالم.</p>''',
            'sort_order': 1
        },
        {
            'key': 'why_choose_us',
            'title_en': 'Why Choose Emdad Global?',
            'title_ar': 'لماذا تختار إمداد جلوبال؟',
            'content_en': '''<p>We combine traditional Egyptian agricultural expertise with modern technology and international 
            standards to deliver exceptional products and services to our global partners.</p>''',
            'sort_order': 2
        }
    ]
    
    for info_data in company_info_data:
        info = CompanyInfo.query.filter_by(key=info_data['key']).first()
        if not info:
            info = CompanyInfo(**info_data)
            db.session.add(info)
            print(f"✓ Created company info: {info_data['key']}")

def create_sample_news():
    """Create sample news articles."""
    news_data = [
        {
            'title_en': 'Emdad Global Expands to New Markets in 2024',
            'title_ar': 'إمداد جلوبال توسع إلى أسواق جديدة في 2024',
            'slug': 'emdad-global-expands-new-markets-2024',
            'excerpt_en': 'We are excited to announce our expansion into new international markets, bringing Egyptian agricultural excellence to more customers worldwide.',
            'excerpt_ar': 'نحن متحمسون للإعلان عن توسعنا في أسواق دولية جديدة، لجلب التميز الزراعي المصري لمزيد من العملاء حول العالم.',
            'content_en': '''<p>Emdad Global is proud to announce our strategic expansion into new international markets in 2024.
            This expansion represents our commitment to bringing the finest Egyptian agricultural products to customers worldwide.</p>
            <p>Our new market initiatives include partnerships in Southeast Asia, Eastern Europe, and South America,
            where demand for premium Egyptian produce continues to grow.</p>''',
            'content_ar': '''<p>تفخر إمداد جلوبال بالإعلان عن توسعها الاستراتيجي في أسواق دولية جديدة في عام 2024.
            يمثل هذا التوسع التزامنا بجلب أجود المنتجات الزراعية المصرية للعملاء حول العالم.</p>
            <p>تشمل مبادراتنا الجديدة في السوق شراكات في جنوب شرق آسيا وأوروبا الشرقية وأمريكا الجنوبية،
            حيث يستمر الطلب على المنتجات المصرية الممتازة في النمو.</p>''',
            'tags': 'expansion,markets,international,2024',
            'seo_title_en': 'Emdad Global Expands to New Markets in 2024 - Egyptian Agricultural Exports',
            'seo_title_ar': 'إمداد جلوبال توسع إلى أسواق جديدة في 2024 - الصادرات الزراعية المصرية',
            'seo_description_en': 'Emdad Global announces strategic expansion into new international markets in 2024, bringing premium Egyptian agricultural products worldwide.',
            'seo_description_ar': 'إمداد جلوبال تعلن عن التوسع الاستراتيجي في أسواق دولية جديدة في 2024، لجلب المنتجات الزراعية المصرية الممتازة عالمياً.',
            'status': 'published',
            'featured': True,
            'publish_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'title_en': 'Sustainable Farming Practices at Emdad Global',
            'title_ar': 'ممارسات الزراعة المستدامة في إمداد جلوبال',
            'slug': 'sustainable-farming-practices-emdad-global',
            'excerpt_en': 'Learn about our commitment to sustainable agriculture and environmental responsibility in our farming operations.',
            'excerpt_ar': 'تعرف على التزامنا بالزراعة المستدامة والمسؤولية البيئية في عملياتنا الزراعية.',
            'content_en': '''<p>At Emdad Global, sustainability is at the heart of everything we do. Our farming partners
            implement environmentally responsible practices that protect the land while producing the highest quality crops.</p>
            <p>We work closely with local farmers to implement water conservation techniques, organic pest control methods,
            and soil health management practices that ensure long-term agricultural productivity.</p>''',
            'content_ar': '''<p>في إمداد جلوبال، الاستدامة هي جوهر كل ما نقوم به. شركاؤنا المزارعون
            ينفذون ممارسات مسؤولة بيئياً تحمي الأرض بينما تنتج أعلى جودة من المحاصيل.</p>
            <p>نعمل بشكل وثيق مع المزارعين المحليين لتنفيذ تقنيات الحفاظ على المياه وطرق مكافحة الآفات العضوية
            وممارسات إدارة صحة التربة التي تضمن الإنتاجية الزراعية طويلة المدى.</p>''',
            'tags': 'sustainability,farming,environment,organic',
            'seo_title_en': 'Sustainable Farming Practices at Emdad Global - Environmental Responsibility',
            'seo_title_ar': 'ممارسات الزراعة المستدامة في إمداد جلوبال - المسؤولية البيئية',
            'seo_description_en': 'Discover Emdad Global\'s commitment to sustainable agriculture and environmental responsibility in farming operations.',
            'seo_description_ar': 'اكتشف التزام إمداد جلوبال بالزراعة المستدامة والمسؤولية البيئية في العمليات الزراعية.',
            'status': 'published',
            'featured': False,
            'publish_at': datetime.utcnow() - timedelta(days=15)
        }
    ]
    
    for news_item in news_data:
        article = News.query.filter_by(slug=news_item['slug']).first()
        if not article:
            article = News(**news_item)
            db.session.add(article)
            print(f"✓ Created news article: {news_item['title_en']}")

def main():
    """Main initialization function."""
    print("Initializing Emdad Global database...")
    
    # Create Flask app
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Create initial data
        create_admin_user()
        create_categories()
        db.session.commit()
        
        create_products()
        create_certifications()
        create_services()
        create_company_info()
        create_sample_news()
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database initialization completed successfully!")
        print("\nDefault admin credentials:")
        print("Email: admin@emdadglobal.com")
        print("Password: admin123")
        print("\n⚠️  Please change the admin password in production!")

if __name__ == '__main__':
    main()
