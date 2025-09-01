#!/usr/bin/env python3
"""
Database initialization script for Render deployment with complete sample data
"""

import sys
import os
from datetime import datetime, timedelta

def create_admin_user(db):
    """Create admin user"""
    from app.models import User

    admin_user = User.query.filter_by(email='admin@emdadglobal.com').first()
    if not admin_user:
        print("Creating admin user...")
        admin_user = User(
            name='Administrator',
            email='admin@emdadglobal.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        print("✅ Admin user created successfully!")
    else:
        print("✅ Admin user already exists")

def create_categories(db):
    """Create sample categories"""
    from app.models import Category

    if Category.query.count() == 0:
        print("Creating categories...")
        categories_data = [
            {
                'key': 'citrus',
                'name_en': 'Citrus Fruits',
                'name_ar': 'الحمضيات',
                'slug': 'citrus-fruits',
                'description_en': 'Premium Egyptian citrus fruits including oranges, lemons, and mandarins with exceptional quality and taste.',
                'description_ar': 'ثمار الحمضيات المصرية الممتازة بما في ذلك البرتقال والليمون واليوسفي بجودة وطعم استثنائي.',
                'sort_order': 1
            },
            {
                'key': 'fresh-fruits',
                'name_en': 'Fresh Fruits',
                'name_ar': 'الفواكه الطازجة',
                'slug': 'fresh-fruits',
                'description_en': 'Seasonal fresh fruits including grapes, mangoes, and pomegranates from Egyptian farms.',
                'description_ar': 'الفواكه الطازجة الموسمية بما في ذلك العنب والمانجو والرمان من المزارع المصرية.',
                'sort_order': 2
            },
            {
                'key': 'vegetables',
                'name_en': 'Fresh Vegetables',
                'name_ar': 'الخضروات الطازجة',
                'slug': 'fresh-vegetables',
                'description_en': 'High-quality vegetables including garlic, onions, and potatoes for global markets.',
                'description_ar': 'خضروات عالية الجودة بما في ذلك الثوم والبصل والبطاطس للأسواق العالمية.',
                'sort_order': 3
            },
            {
                'key': 'frozen',
                'name_en': 'Frozen Products',
                'name_ar': 'المنتجات المجمدة',
                'slug': 'frozen-products',
                'description_en': 'IQF frozen fruits and vegetables maintaining freshness and nutritional value.',
                'description_ar': 'الفواكه والخضروات المجمدة بتقنية IQF مع الحفاظ على النضارة والقيمة الغذائية.',
                'sort_order': 4
            },
            {
                'key': 'dried-fruits',
                'name_en': 'Dried Fruits',
                'name_ar': 'الفواكه المجففة',
                'slug': 'dried-fruits',
                'description_en': 'Premium dried fruits processed with advanced techniques for extended shelf life.',
                'description_ar': 'فواكه مجففة ممتازة معالجة بتقنيات متقدمة لفترة صلاحية ممتدة.',
                'sort_order': 5
            },
            {
                'key': 'fresh-citrus',
                'name_en': 'Fresh Citrus',
                'name_ar': 'الحمضيات الطازجة',
                'slug': 'fresh-citrus',
                'description_en': 'Fresh citrus fruits with superior quality and international standards.',
                'description_ar': 'ثمار الحمضيات الطازجة بجودة فائقة ومعايير دولية.',
                'sort_order': 6
            },
            {
                'key': 'frozen-fruits-iqf',
                'name_en': 'Frozen Fruits (IQF)',
                'name_ar': 'الفواكه المجمدة',
                'slug': 'frozen-fruits-iqf',
                'description_en': 'Individually Quick Frozen fruits maintaining texture and nutritional benefits.',
                'description_ar': 'فواكه مجمدة بسرعة فردية مع الحفاظ على الملمس والفوائد الغذائية.',
                'sort_order': 7
            }
        ]

        for cat_data in categories_data:
            # Set sample image path
            image_path = f"{cat_data['key']}.svg"

            category = Category(
                key=cat_data['key'],
                name_en=cat_data['name_en'],
                name_ar=cat_data['name_ar'],
                slug=cat_data['slug'],
                description_en=cat_data['description_en'],
                description_ar=cat_data['description_ar'],
                sort_order=cat_data['sort_order'],
                image_path=image_path,
                is_active=True
            )
            db.session.add(category)

        print("✅ Categories created successfully!")
    else:
        print("✅ Categories already exist")

def create_products(db):
    """Create sample products"""
    from app.models import Product, Category

    if Product.query.count() == 0:
        print("Creating products...")

        # Get categories
        citrus_cat = Category.query.filter_by(key='citrus').first()
        fresh_fruits_cat = Category.query.filter_by(key='fresh-fruits').first()
        vegetables_cat = Category.query.filter_by(key='vegetables').first()
        frozen_cat = Category.query.filter_by(key='frozen').first()

        products_data = [
            {
                'name_en': 'Egyptian Oranges',
                'name_ar': 'البرتقال المصري',
                'slug': 'egyptian-oranges',
                'category_id': citrus_cat.id if citrus_cat else 1,
                'description_en': 'Premium quality Egyptian oranges with exceptional sweetness and juice content. Grown in the fertile Nile Delta region.',
                'description_ar': 'برتقال مصري عالي الجودة بحلاوة استثنائية ومحتوى عصير عالي. مزروع في منطقة دلتا النيل الخصبة.',
                'short_description_en': 'Premium Egyptian oranges with exceptional sweetness',
                'short_description_ar': 'برتقال مصري ممتاز بحلاوة استثنائية',
                'featured': True,
                'sort_order': 1
            },
            {
                'name_en': 'Mandarins',
                'name_ar': 'اليوسفي',
                'slug': 'mandarins',
                'category_id': citrus_cat.id if citrus_cat else 1,
                'description_en': 'Sweet and juicy Egyptian mandarins, perfect for fresh consumption and export markets.',
                'description_ar': 'يوسفي مصري حلو وعصيري، مثالي للاستهلاك الطازج وأسواق التصدير.',
                'short_description_en': 'Sweet and juicy Egyptian mandarins',
                'short_description_ar': 'يوسفي مصري حلو وعصيري',
                'featured': True,
                'sort_order': 2
            },
            {
                'name_en': 'Egyptian Grapes',
                'name_ar': 'العنب المصري',
                'slug': 'egyptian-grapes',
                'category_id': fresh_fruits_cat.id if fresh_fruits_cat else 2,
                'description_en': 'High-quality table grapes in various varieties including Thompson Seedless and Red Globe.',
                'description_ar': 'عنب مائدة عالي الجودة بأصناف مختلفة بما في ذلك طومسون بدون بذور والكرة الحمراء.',
                'short_description_en': 'High-quality table grapes in various varieties',
                'short_description_ar': 'عنب مائدة عالي الجودة بأصناف مختلفة',
                'featured': True,
                'sort_order': 3
            },
            {
                'name_en': 'Pomegranates',
                'name_ar': 'الرمان',
                'slug': 'pomegranates',
                'category_id': fresh_fruits_cat.id if fresh_fruits_cat else 2,
                'description_en': 'Fresh Egyptian pomegranates rich in antioxidants and natural sweetness.',
                'description_ar': 'رمان مصري طازج غني بمضادات الأكسدة والحلاوة الطبيعية.',
                'short_description_en': 'Fresh Egyptian pomegranates rich in antioxidants',
                'short_description_ar': 'رمان مصري طازج غني بمضادات الأكسدة',
                'featured': True,
                'sort_order': 4
            },
            {
                'name_en': 'Egyptian Garlic',
                'name_ar': 'الثوم المصري',
                'slug': 'egyptian-garlic',
                'category_id': vegetables_cat.id if vegetables_cat else 3,
                'description_en': 'Premium white garlic with strong flavor and excellent storage capabilities.',
                'description_ar': 'ثوم أبيض ممتاز بنكهة قوية وقدرات تخزين ممتازة.',
                'short_description_en': 'Premium white garlic with strong flavor',
                'short_description_ar': 'ثوم أبيض ممتاز بنكهة قوية',
                'featured': True,
                'sort_order': 5
            },
            {
                'name_en': 'IQF Strawberries',
                'name_ar': 'الفراولة المجمدة',
                'slug': 'iqf-strawberries',
                'category_id': frozen_cat.id if frozen_cat else 4,
                'description_en': 'Individually Quick Frozen strawberries maintaining fresh taste and nutrition.',
                'description_ar': 'فراولة مجمدة بسرعة فردية مع الحفاظ على الطعم الطازج والتغذية.',
                'short_description_en': 'IQF strawberries maintaining fresh taste',
                'short_description_ar': 'فراولة مجمدة مع الحفاظ على الطعم الطازج',
                'featured': True,
                'sort_order': 6
            },
            {
                'name_en': 'Premium Valencia Oranges',
                'name_ar': 'برتقال فالنسيا الممتاز',
                'slug': 'premium-valencia-oranges',
                'category_id': citrus_cat.id if citrus_cat else 1,
                'description_en': 'Premium Valencia oranges perfect for juice production and fresh consumption.',
                'description_ar': 'برتقال فالنسيا ممتاز مثالي لإنتاج العصير والاستهلاك الطازج.',
                'short_description_en': 'Premium Valencia oranges for juice and fresh consumption',
                'short_description_ar': 'برتقال فالنسيا ممتاز للعصير والاستهلاك الطازج',
                'featured': True,
                'sort_order': 7
            },
            {
                'name_en': 'Fresh Red Onions',
                'name_ar': 'البصل الأحمر الطازج',
                'slug': 'fresh-red-onions',
                'category_id': vegetables_cat.id if vegetables_cat else 3,
                'description_en': 'Fresh red onions with excellent quality and long shelf life.',
                'description_ar': 'بصل أحمر طازج بجودة ممتازة وفترة صلاحية طويلة.',
                'short_description_en': 'Fresh red onions with excellent quality',
                'short_description_ar': 'بصل أحمر طازج بجودة ممتازة',
                'featured': True,
                'sort_order': 8
            },
            {
                'name_en': 'Egyptian Lemons',
                'name_ar': 'الليمون المصري',
                'slug': 'egyptian-lemons',
                'category_id': citrus_cat.id if citrus_cat else 1,
                'description_en': 'Fresh Egyptian lemons with high acidity and excellent aroma.',
                'description_ar': 'ليمون مصري طازج بحموضة عالية ورائحة ممتازة.',
                'short_description_en': 'Fresh Egyptian lemons with high acidity',
                'short_description_ar': 'ليمون مصري طازج بحموضة عالية',
                'featured': False,
                'sort_order': 9
            },
            {
                'name_en': 'Fresh Potatoes',
                'name_ar': 'البطاطس الطازجة',
                'slug': 'fresh-potatoes',
                'category_id': vegetables_cat.id if vegetables_cat else 3,
                'description_en': 'High-quality Egyptian potatoes suitable for various culinary applications.',
                'description_ar': 'بطاطس مصرية عالية الجودة مناسبة لتطبيقات الطهي المختلفة.',
                'short_description_en': 'High-quality Egyptian potatoes',
                'short_description_ar': 'بطاطس مصرية عالية الجودة',
                'featured': False,
                'sort_order': 10
            }
        ]

        for prod_data in products_data:
            # Create product
            product = Product(
                name_en=prod_data['name_en'],
                name_ar=prod_data['name_ar'],
                slug=prod_data['slug'],
                category_id=prod_data['category_id'],
                description_en=prod_data['description_en'],
                description_ar=prod_data['description_ar'],
                short_description_en=prod_data['short_description_en'],
                short_description_ar=prod_data['short_description_ar'],
                status='active',
                featured=prod_data['featured'],
                sort_order=prod_data['sort_order']
            )
            db.session.add(product)
            db.session.flush()  # Get the product ID

            # Create product image
            from app.models import ProductImage
            image_filename = f"{prod_data['slug']}.svg"
            product_image = ProductImage(
                product_id=product.id,
                filename=image_filename,
                alt_text_en=prod_data['name_en'],
                alt_text_ar=prod_data['name_ar'],
                is_main=True,
                sort_order=0
            )
            db.session.add(product_image)

        print("✅ Products created successfully!")
    else:
        print("✅ Products already exist")

def create_news(db):
    """Create sample news articles"""
    from app.models import News
    from datetime import datetime, timedelta

    if News.query.count() == 0:
        print("Creating news articles...")

        news_data = [
            {
                'title_en': 'Emdad Global Expands to New Markets in 2024',
                'title_ar': 'إمداد جلوبال تتوسع في أسواق جديدة في 2024',
                'slug': 'emdad-global-expands-new-markets-2024',
                'excerpt_en': 'We are excited to announce our expansion into European and Asian markets, bringing Egyptian agricultural excellence to new customers worldwide.',
                'excerpt_ar': 'نحن متحمسون للإعلان عن توسعنا في الأسواق الأوروبية والآسيوية، مما يجلب التميز الزراعي المصري لعملاء جدد في جميع أنحاء العالم.',
                'content_en': '''<p>Emdad Global is proud to announce a significant milestone in our journey of agricultural excellence. In 2024, we are expanding our operations to serve new markets across Europe and Asia, bringing the finest Egyptian agricultural products to customers worldwide.</p>

<p>This expansion represents years of careful planning and investment in our infrastructure, quality systems, and international partnerships. Our commitment to delivering premium Egyptian citrus fruits, fresh produce, and frozen products has earned us recognition in global markets.</p>

<h3>New Market Opportunities</h3>
<p>Our expansion includes:</p>
<ul>
<li>Direct partnerships with major European distributors</li>
<li>New supply chains to Asian markets</li>
<li>Enhanced cold chain logistics for global reach</li>
<li>Increased production capacity to meet growing demand</li>
</ul>

<p>We remain committed to our core values of quality, sustainability, and customer satisfaction as we grow our international presence.</p>''',
                'content_ar': '''<p>تفخر إمداد جلوبال بالإعلان عن معلم مهم في رحلتنا للتميز الزراعي. في عام 2024، نقوم بتوسيع عملياتنا لخدمة أسواق جديدة عبر أوروبا وآسيا، مما يجلب أفضل المنتجات الزراعية المصرية للعملاء في جميع أنحاء العالم.</p>

<p>يمثل هذا التوسع سنوات من التخطيط الدقيق والاستثمار في البنية التحتية وأنظمة الجودة والشراكات الدولية. التزامنا بتقديم ثمار الحمضيات المصرية الممتازة والمنتجات الطازجة والمجمدة قد كسبنا الاعتراف في الأسواق العالمية.</p>

<h3>فرص السوق الجديدة</h3>
<p>يشمل توسعنا:</p>
<ul>
<li>شراكات مباشرة مع الموزعين الأوروبيين الرئيسيين</li>
<li>سلاسل توريد جديدة للأسواق الآسيوية</li>
<li>لوجستيات سلسلة التبريد المحسنة للوصول العالمي</li>
<li>زيادة الطاقة الإنتاجية لتلبية الطلب المتزايد</li>
</ul>

<p>نبقى ملتزمين بقيمنا الأساسية للجودة والاستدامة ورضا العملاء بينما ننمو حضورنا الدولي.</p>''',
                'status': 'published',
                'featured': True,
                'publish_at': datetime.utcnow() - timedelta(days=5),
                'tags': 'expansion,markets,international,growth'
            },
            {
                'title_en': 'Sustainable Farming Practices at Emdad Global',
                'title_ar': 'ممارسات الزراعة المستدامة في إمداد جلوبال',
                'slug': 'sustainable-farming-practices-emdad-global',
                'excerpt_en': 'Learn about our commitment to sustainable agriculture and environmental conservation while maintaining the highest quality standards.',
                'excerpt_ar': 'تعرف على التزامنا بالزراعة المستدامة والحفاظ على البيئة مع الحفاظ على أعلى معايير الجودة.',
                'content_en': '''<p>At Emdad Global, sustainability is not just a buzzword – it's a fundamental principle that guides every aspect of our agricultural operations. We believe that protecting our environment is essential for ensuring the long-term viability of Egyptian agriculture.</p>

<h3>Our Sustainable Practices</h3>
<p>We have implemented comprehensive sustainable farming practices across all our operations:</p>

<h4>Water Conservation</h4>
<ul>
<li>Advanced drip irrigation systems reducing water usage by 40%</li>
<li>Rainwater harvesting and recycling programs</li>
<li>Soil moisture monitoring for optimal irrigation timing</li>
</ul>

<h4>Soil Health Management</h4>
<ul>
<li>Organic composting programs</li>
<li>Crop rotation to maintain soil fertility</li>
<li>Minimal tillage practices to preserve soil structure</li>
</ul>

<h4>Integrated Pest Management</h4>
<ul>
<li>Biological pest control methods</li>
<li>Reduced chemical pesticide usage</li>
<li>Natural predator conservation programs</li>
</ul>

<p>These practices not only protect our environment but also result in healthier, more nutritious products for our customers worldwide.</p>''',
                'content_ar': '''<p>في إمداد جلوبال، الاستدامة ليست مجرد كلمة رنانة - إنها مبدأ أساسي يوجه كل جانب من جوانب عملياتنا الزراعية. نؤمن أن حماية بيئتنا أمر ضروري لضمان الجدوى طويلة المدى للزراعة المصرية.</p>

<h3>ممارساتنا المستدامة</h3>
<p>لقد نفذنا ممارسات زراعية مستدامة شاملة عبر جميع عملياتنا:</p>

<h4>الحفاظ على المياه</h4>
<ul>
<li>أنظمة الري بالتنقيط المتقدمة تقلل استخدام المياه بنسبة 40%</li>
<li>برامج حصاد مياه الأمطار وإعادة التدوير</li>
<li>مراقبة رطوبة التربة للتوقيت الأمثل للري</li>
</ul>

<h4>إدارة صحة التربة</h4>
<ul>
<li>برامج التسميد العضوي</li>
<li>دوران المحاصيل للحفاظ على خصوبة التربة</li>
<li>ممارسات الحراثة الدنيا للحفاظ على بنية التربة</li>
</ul>

<h4>الإدارة المتكاملة للآفات</h4>
<ul>
<li>طرق المكافحة البيولوجية للآفات</li>
<li>تقليل استخدام المبيدات الكيميائية</li>
<li>برامج الحفاظ على الحيوانات المفترسة الطبيعية</li>
</ul>

<p>هذه الممارسات لا تحمي بيئتنا فحسب، بل تؤدي أيضًا إلى منتجات أكثر صحة وتغذية لعملائنا في جميع أنحاء العالم.</p>''',
                'status': 'published',
                'featured': True,
                'publish_at': datetime.utcnow() - timedelta(days=12),
                'tags': 'sustainability,environment,farming,organic'
            },
            {
                'title_en': 'New Export Markets Expansion',
                'title_ar': 'توسع أسواق التصدير الجديدة',
                'slug': 'new-export-markets-expansion',
                'excerpt_en': 'Emdad Global announces successful entry into new international markets, strengthening our global presence in agricultural exports.',
                'excerpt_ar': 'إمداد جلوبال تعلن عن دخول ناجح في أسواق دولية جديدة، مما يعزز حضورنا العالمي في الصادرات الزراعية.',
                'content_en': '''<p>We are thrilled to announce that Emdad Global has successfully entered several new international markets, marking a significant milestone in our global expansion strategy. This achievement reflects our commitment to bringing Egyptian agricultural excellence to customers worldwide.</p>

<h3>Market Expansion Highlights</h3>
<p>Our recent expansion includes:</p>
<ul>
<li>Entry into Scandinavian markets with premium citrus fruits</li>
<li>New partnerships in Southeast Asian countries</li>
<li>Expanded presence in Middle Eastern markets</li>
<li>Growing demand for our frozen fruit products in European markets</li>
</ul>

<h3>Quality Assurance</h3>
<p>Our success in these new markets is built on our unwavering commitment to quality:</p>
<ul>
<li>International certifications including ISO 22000 and HACCP</li>
<li>Advanced cold chain logistics ensuring product freshness</li>
<li>Rigorous quality control at every stage of production</li>
<li>Compliance with international food safety standards</li>
</ul>

<p>We look forward to serving our new customers with the same dedication to quality and service that has made us a trusted partner in agricultural exports.</p>''',
                'content_ar': '''<p>نحن متحمسون للإعلان أن إمداد جلوبال قد دخلت بنجاح عدة أسواق دولية جديدة، مما يمثل معلمًا مهمًا في استراتيجية التوسع العالمي. هذا الإنجاز يعكس التزامنا بجلب التميز الزراعي المصري للعملاء في جميع أنحاء العالم.</p>

<h3>أبرز نقاط توسع السوق</h3>
<p>يشمل توسعنا الأخير:</p>
<ul>
<li>الدخول في الأسواق الاسكندنافية بثمار الحمضيات الممتازة</li>
<li>شراكات جديدة في دول جنوب شرق آسيا</li>
<li>حضور موسع في أسواق الشرق الأوسط</li>
<li>طلب متزايد على منتجات الفواكه المجمدة في الأسواق الأوروبية</li>
</ul>

<h3>ضمان الجودة</h3>
<p>نجاحنا في هذه الأسواق الجديدة مبني على التزامنا الثابت بالجودة:</p>
<ul>
<li>الشهادات الدولية بما في ذلك ISO 22000 و HACCP</li>
<li>لوجستيات سلسلة التبريد المتقدمة لضمان نضارة المنتج</li>
<li>مراقبة الجودة الصارمة في كل مرحلة من مراحل الإنتاج</li>
<li>الامتثال لمعايير سلامة الغذاء الدولية</li>
</ul>

<p>نتطلع إلى خدمة عملائنا الجدد بنفس التفاني في الجودة والخدمة التي جعلتنا شريكًا موثوقًا في الصادرات الزراعية.</p>''',
                'status': 'published',
                'featured': False,
                'publish_at': datetime.utcnow() - timedelta(days=20),
                'tags': 'export,markets,international,expansion'
            }
        ]

        # Map news to sample images
        news_images = {
            'emdad-global-expands-new-markets-2024': 'expansion.svg',
            'sustainable-farming-practices-emdad-global': 'sustainability.svg',
            'new-export-markets-expansion': 'export-markets.svg'
        }

        for news_item in news_data:
            # Set sample image
            cover_image = news_images.get(news_item['slug'], 'expansion.svg')

            news = News(
                title_en=news_item['title_en'],
                title_ar=news_item['title_ar'],
                slug=news_item['slug'],
                excerpt_en=news_item['excerpt_en'],
                excerpt_ar=news_item['excerpt_ar'],
                content_en=news_item['content_en'],
                content_ar=news_item['content_ar'],
                status=news_item['status'],
                featured=news_item['featured'],
                publish_at=news_item['publish_at'],
                tags=news_item['tags'],
                cover_image=cover_image
            )
            db.session.add(news)

        print("✅ News articles created successfully!")
    else:
        print("✅ News articles already exist")

def create_company_info(db):
    """Create company information sections"""
    from app.models import CompanyInfo

    if CompanyInfo.query.count() == 0:
        print("Creating company information...")

        company_info_data = [
            {
                'key': 'about_intro',
                'title_en': 'About Emdad Global',
                'title_ar': 'عن إمداد جلوبال',
                'content_en': 'Emdad Global is a leading Egyptian export company specializing in premium agricultural products. With over 25 years of experience, we have built a reputation for delivering the highest quality fresh and frozen fruits and vegetables to markets worldwide. Our commitment to excellence, combined with state-of-the-art facilities and international certifications, ensures that our products meet the strictest quality standards demanded by global markets.',
                'content_ar': 'إمداد جلوبال هي شركة تصدير مصرية رائدة متخصصة في المنتجات الزراعية الممتازة. مع أكثر من 25 عاماً من الخبرة، بنينا سمعة في تقديم أعلى جودة من الفواكه والخضروات الطازجة والمجمدة إلى الأسواق في جميع أنحاء العالم. التزامنا بالتميز، إلى جانب المرافق الحديثة والشهادات الدولية، يضمن أن منتجاتنا تلبي أصرم معايير الجودة التي تتطلبها الأسواق العالمية.',
                'sort_order': 1,
                'is_active': True
            },
            {
                'key': 'why_choose_us',
                'title_en': 'Why Choose Emdad Global?',
                'title_ar': 'لماذا تختار إمداد جلوبال؟',
                'content_en': 'Our success is built on three pillars: uncompromising quality, reliable supply chains, and exceptional customer service. We work directly with carefully selected farms across Egypt, ensuring traceability and quality control from farm to fork. Our modern facilities, international certifications, and experienced team guarantee that every shipment meets the highest standards of freshness, safety, and quality.',
                'content_ar': 'نجاحنا مبني على ثلاث ركائز: الجودة بلا تنازل، وسلاسل التوريد الموثوقة، وخدمة العملاء الاستثنائية. نعمل مباشرة مع المزارع المختارة بعناية في جميع أنحاء مصر، مما يضمن إمكانية التتبع ومراقبة الجودة من المزرعة إلى المائدة. مرافقنا الحديثة والشهادات الدولية والفريق ذو الخبرة يضمن أن كل شحنة تلبي أعلى معايير النضارة والسلامة والجودة.',
                'sort_order': 2,
                'is_active': True
            }
        ]

        for info_data in company_info_data:
            company_info = CompanyInfo(
                key=info_data['key'],
                title_en=info_data['title_en'],
                title_ar=info_data['title_ar'],
                content_en=info_data['content_en'],
                content_ar=info_data['content_ar'],
                sort_order=info_data['sort_order'],
                is_active=info_data['is_active']
            )
            db.session.add(company_info)

        print("✅ Company information created successfully!")
    else:
        print("✅ Company information already exists")

def copy_sample_images():
    """Copy sample images to upload directories"""
    import shutil
    import os

    try:
        print("Copying sample images...")

        # Create upload directories
        upload_dirs = [
            'uploads/products',
            'uploads/categories',
            'uploads/news',
            'instance/uploads/products',
            'instance/uploads/categories',
            'instance/uploads/news'
        ]

        for upload_dir in upload_dirs:
            os.makedirs(upload_dir, exist_ok=True)

        # Copy category images
        if os.path.exists('static/images/samples/categories'):
            for filename in os.listdir('static/images/samples/categories'):
                if filename.endswith('.svg'):
                    src = f'static/images/samples/categories/{filename}'
                    for dest_dir in ['uploads/categories', 'instance/uploads/categories']:
                        dest = f'{dest_dir}/{filename}'
                        shutil.copy2(src, dest)
                        print(f"✅ Copied category image: {filename}")

        # Copy product images
        if os.path.exists('static/images/samples/products'):
            for filename in os.listdir('static/images/samples/products'):
                if filename.endswith('.svg'):
                    src = f'static/images/samples/products/{filename}'
                    for dest_dir in ['uploads/products', 'instance/uploads/products']:
                        dest = f'{dest_dir}/{filename}'
                        shutil.copy2(src, dest)
                        print(f"✅ Copied product image: {filename}")

        # Copy news images
        if os.path.exists('static/images/samples/news'):
            for filename in os.listdir('static/images/samples/news'):
                if filename.endswith('.svg'):
                    src = f'static/images/samples/news/{filename}'
                    for dest_dir in ['uploads/news', 'instance/uploads/news']:
                        dest = f'{dest_dir}/{filename}'
                        shutil.copy2(src, dest)
                        print(f"✅ Copied news image: {filename}")

        print("✅ Sample images copied successfully!")

    except Exception as e:
        print(f"⚠️ Error copying sample images: {e}")
        # Continue anyway - not critical

def init_database():
    """Initialize database for production with complete sample data"""
    try:
        import os
        import sys

        # Ensure temp directory is writable
        os.makedirs('/tmp', exist_ok=True)

        # Test write permissions and set appropriate database URL
        db_paths = [
            '/tmp/emdad_global.db',
            './emdad_global.db',
            'emdad_global.db'
        ]

        database_url = None
        for db_path in db_paths:
            try:
                # Test if we can create a file in this location
                test_path = db_path.replace('.db', '_test.db')
                with open(test_path, 'w') as f:
                    f.write('test')
                os.remove(test_path)
                database_url = f'sqlite:///{db_path}'
                print(f"✅ Using database path: {db_path}")
                break
            except Exception as e:
                print(f"⚠️ Cannot write to {db_path}: {e}")
                continue

        if database_url:
            os.environ['DATABASE_URL'] = database_url
        else:
            # Last resort - in-memory database
            os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
            print("⚠️ Using in-memory database as fallback")

        print("Creating Flask app...")
        from app import create_app
        app = create_app('production')

        print("Initializing database...")
        with app.app_context():
            from app.models import db
            # Import all models to ensure they're registered
            import app.models  # noqa: F401

            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")

            # Create all sample data
            try:
                print("Creating sample data...")

                # Create sample images first
                copy_sample_images()

                # Create admin user
                create_admin_user(db)
                db.session.commit()

                # Create categories
                create_categories(db)
                db.session.commit()

                # Create products
                create_products(db)
                db.session.commit()

                # Create news articles
                create_news(db)
                db.session.commit()

                # Create company information
                create_company_info(db)
                db.session.commit()

                print("✅ All sample data created successfully!")

            except Exception as data_error:
                print(f"⚠️ Sample data creation error: {data_error}")
                import traceback
                traceback.print_exc()
                # Continue anyway - basic tables are created

            print("✅ Database initialization completed!")
            return True

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import sys
    success = init_database()
    sys.exit(0 if success else 1)
