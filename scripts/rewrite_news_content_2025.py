from datetime import datetime, timedelta
import os, sys
# Ensure repository root is on sys.path when running as a script from scripts/
CURRENT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


from app import create_app, db
from app.models import News

"""
Rewrite the content of the three current news articles with SEO-optimized, bilingual (EN/AR) long-form content.
- Prefer updating known slugs from seed; otherwise fallback to latest 3 published items.
- Keep slugs unchanged to avoid breaking links.
- Update titles, excerpts, HTML content, SEO fields, tags, featured flags, show_on_homepage, and publish dates (2025).
"""

# Helper data: prepared content blocks (do not print to console)

ARTICLES = {
    # Seeded primary article: keep slug, update content to 2025
    "emdad-global-expands-new-markets-2025": {
        "en": {
            "title": "Emdad Global Expands to New Markets in 2025",
            "excerpt": (
                "Emdad Global announces strategic expansion across Europe and Asia in 2025, "
                "strengthening partnerships, logistics, and premium agricultural exports."
            ),
            "focus_keyword": "Emdad Global expansion 2025",
            "seo_title": "Emdad Global Expansion 2025: New Markets Across Europe and Asia",
            "seo_description": (
                "Discover how Emdad Global is expanding in 2025 into key European and Asian markets, "
                "with stronger supply chains, certifications, and premium agricultural exports."
            ),
            "og_title": "Emdad Global Expansion 2025",
            "og_description": "New markets, stronger logistics, and certified quality in 2025.",
            "twitter_title": "Emdad Global Expands in 2025",
            "twitter_description": "Entering new markets with certified quality and reliable logistics.",
            "tags": "expansion,markets,international,growth,logistics,certifications",
            "content": (
                """
                <p>Emdad Global is proud to mark 2025 with a strategic expansion into new European and Asian markets.
                Building on our quality-first approach and robust supply networks, we are partnering with leading distributors
                to deliver premium Egyptian citrus, fresh produce, IQF fruit, dates, and spices at scale.</p>

                <h3>Why 2025 Is a Breakthrough Year</h3>
                <ul>
                  <li>Expanded coverage in Scandinavia, Central Europe, the Gulf, and Southeast Asia</li>
                  <li>Enhanced cold-chain logistics and integrated traceability</li>
                  <li>Certified processes aligned with ISO 22000 and HACCP standards</li>
                  <li>Stronger grower partnerships and capacity scaling for peak seasons</li>
                </ul>

                <h3>Customer Benefits</h3>
                <p>Buyers benefit from faster lead times, consistent product quality, and flexible programs tailored to retail,
                wholesale, and food-service channels. Our supply teams coordinate harvest schedules, packing, and export
                documentation to ensure reliability and compliance across markets.</p>

                <h3>Key Product Focus</h3>
                <ul>
                  <li>Fresh citrus and table grapes</li>
                  <li>IQF mango, strawberries, and mixed fruit</li>
                  <li>Premium dates and date derivatives</li>
                  <li>Spices and herbs with rigorous sorting and microbiological standards</li>
                </ul>

                <h3>What’s Next</h3>
                <p>We continue to invest in quality systems, sustainability programs, and data-driven operations.
                If you are developing seasonal programs or private label lines in 2025, our team will help design a solution
                that fits your volumes, certifications, and packaging preferences.</p>

                <p><strong>Ready to collaborate?</strong> Contact our exports team to plan your 2025 sourcing pipeline.</p>
                """
            ),
        },
        "ar": {
            "title": "إمداد جلوبال تتوسع في أسواق جديدة في عام 2025",
            "excerpt": (
                "تعلن إمداد جلوبال عن توسع استراتيجي في أوروبا وآسيا خلال 2025 مع شراكات أقوى ولوجستيات متقدمة وجودة معتمدة."
            ),
            "focus_keyword": "توسع إمداد جلوبال 2025",
            "seo_title": "توسع إمداد جلوبال 2025: أسواق جديدة في أوروبا وآسيا",
            "seo_description": (
                "تعرف على توسع إمداد جلوبال في 2025 إلى أسواق أوروبية وآسيوية رئيسية بجودة معتمدة وسلاسل إمداد موثوقة."
            ),
            "og_title": "توسع إمداد جلوبال 2025",
            "og_description": "أسواق جديدة ولوجستيات أقوى وجودة معتمدة في 2025.",
            "twitter_title": "إمداد جلوبال تتوسع في 2025",
            "twitter_description": "دخول أسواق جديدة بجودة معتمدة ولوجستيات موثوقة.",
            "tags": "توسع,أسواق,دولي,نمو,لوجستيات,اعتمادات",
            "content": (
                """
                <p>تفخر إمداد جلوبال ببدء عام 2025 بخطة توسع استراتيجية نحو أسواق أوروبية وآسيوية جديدة.
                وبالاعتماد على نهج الجودة أولاً وشبكات الإمداد القوية، نعزّز شراكاتنا مع كبار الموزعين لتقديم
                أفضل المنتجات الزراعية المصرية من حمضيات وخضروات طازجة وفواكه IQF وتمور وتوابل.</p>

                <h3>لماذا يُعد 2025 عاماً مفصلياً</h3>
                <ul>
                  <li>تغطية أوسع في إسكندنافيا ووسط أوروبا والخليج وجنوب شرق آسيا</li>
                  <li>سلاسل تبريد مُحسّنة وتتبع متكامل</li>
                  <li>عمليات معتمدة وفق معايير ISO 22000 وHACCP</li>
                  <li>شراكات أقوى مع المزارعين وزيادة الطاقة خلال مواسم الذروة</li>
                </ul>

                <h3>قيمة مضافة للعملاء</h3>
                <p>نقدّم أزمنة توريد أسرع وجودة ثابتة وبرامج مرنة تناسب التجزئة والجملة وخدمات الطعام. كما ننسّق جداول الحصاد
                والتعبئة والمستندات التصديرية لضمان الالتزام والموثوقية في مختلف الأسواق.</p>

                <h3>تركيز المنتجات</h3>
                <ul>
                  <li>الحمضيات والفواكه الطازجة</li>
                  <li>مانجو وفراولة ومزيج فواكه IQF</li>
                  <li>التمور ومنتجاتها</li>
                  <li>التوابل والأعشاب وفق مواصفات فرز ومعايير ميكروبيولوجية دقيقة</li>
                </ul>

                <h3>الخطوة التالية</h3>
                <p>نواصل الاستثمار في نظم الجودة والاستدامة والعمليات المعتمدة على البيانات. إذا كنت تطوّر برامج توريد موسمية
                أو علامات خاصة في 2025، فسيسعد فريقنا بتصميم حل يناسب أحجامك واعتماداتك وتفضيلات التغليف.</p>

                <p><strong>جاهز للتعاون؟</strong> تواصل مع فريق التصدير لدينا لتخطيط سلسلة توريدك لعام 2025.</p>
                """
            ),
        },
        "featured": True,
        "show_on_homepage": True,
    },
    # Sustainable practices article (featured)
    "sustainable-farming-practices-emdad-global": {
        "en": {
            "title": "Sustainable Farming at Emdad Global: 2025 Programs and KPIs",
            "excerpt": "Our 2025 sustainability framework improves water, soil, and energy efficiency with measurable KPIs.",
            "focus_keyword": "sustainable farming 2025 Egypt",
            "seo_title": "Emdad Global Sustainability 2025: Water, Soil, Energy KPIs",
            "seo_description": "Explore our 2025 sustainable farming programs with water-saving, soil health, and energy KPIs.",
            "og_title": "Sustainable Farming 2025",
            "og_description": "Water-saving, soil health, and efficiency in focus.",
            "twitter_title": "Emdad Global Sustainability 2025",
            "twitter_description": "2025 programs: water, soil, energy efficiency.",
            "tags": "sustainability,environment,farming,organic,efficiency,ESG",
            "content": (
                """
                <p>In 2025, Emdad Global advances its sustainability roadmap with measurable initiatives that enhance
                water use, soil health, and energy efficiency—without compromising product quality.</p>

                <h3>2025 Sustainability Pillars</h3>
                <ul>
                  <li><strong>Water:</strong> Drip systems, moisture sensors, and recovery targets (up to 40% savings)</li>
                  <li><strong>Soil:</strong> Composting, rotation, and minimal tillage for long-term fertility</li>
                  <li><strong>Energy:</strong> Optimized cold-chain operations and reduced transport emissions</li>
                </ul>

                <h3>Traceability and Quality</h3>
                <p>We integrate digital traceability across harvest, packing, and export, aligning with international
                standards and customer-specific specifications.</p>

                <h3>Impact in Markets</h3>
                <p>Buyers benefit from predictable specs, clear documentation, and reliable delivery windows.
                Our programs support long-term sourcing partnerships.</p>
                """
            ),
        },
        "ar": {
            "title": "الزراعة المستدامة في إمداد جلوبال: برامج ومؤشرات 2025",
            "excerpt": "إطار الاستدامة 2025 يطوّر كفاءة المياه والتربة والطاقة بمؤشرات أداء قابلة للقياس.",
            "focus_keyword": "الزراعة المستدامة 2025 مصر",
            "seo_title": "استدامة إمداد جلوبال 2025: مياه وتربة وطاقة",
            "seo_description": "تعرف على برامج الاستدامة 2025 لدينا مع حفظ المياه وصحة التربة وكفاءة الطاقة.",
            "og_title": "الزراعة المستدامة 2025",
            "og_description": "حفظ المياه وصحة التربة وكفاءة التشغيل.",
            "twitter_title": "استدامة إمداد جلوبال 2025",
            "twitter_description": "برامج 2025: مياه وتربة وكفاءة طاقة.",
            "tags": "استدامة,بيئة,زراعة,عضوي,كفاءة,ESG",
            "content": (
                """
                <p>في عام 2025، تعزز إمداد جلوبال خارطة طريق الاستدامة بمبادرات قابلة للقياس تُحسّن استخدام المياه
                وصحة التربة وكفاءة الطاقة، مع الحفاظ على جودة المنتج.</p>

                <h3>ركائز الاستدامة 2025</h3>
                <ul>
                  <li><strong>المياه:</strong> ري بالتنقيط ومستشعرات رطوبة وأهداف استرجاع (حتى 40% توفير)</li>
                  <li><strong>التربة:</strong> تسميد عضوي ودوران محاصيل وحراثة دنيا للحفاظ على الخصوبة</li>
                  <li><strong>الطاقة:</strong> تحسين تشغيل سلسلة التبريد وتقليل الانبعاثات</li>
                </ul>

                <h3>التتبع والجودة</h3>
                <p>نطبق تتبعاً رقمياً عبر الحصاد والتعبئة والتصدير بما يتوافق مع المعايير الدولية
                ومواصفات العملاء.</p>

                <h3>الأثر في الأسواق</h3>
                <p>يستفيد المشترون من مواصفات واضحة ووثائق متكاملة ونوافذ توريد موثوقة.
                تدعم برامجنا شراكات توريد طويلة الأمد.</p>
                """
            ),
        },
        "featured": True,
        "show_on_homepage": True,
    },
    # Markets expansion short article (non-featured)
    "new-export-markets-expansion": {
        "en": {
            "title": "New Export Markets in 2025: Strengthening Global Reach",
            "excerpt": "Our 2025 market development reinforces presence in Europe, MENA, and Asia with reliable supply programs.",
            "focus_keyword": "export markets 2025 Emdad",
            "seo_title": "Export Markets 2025: Europe, MENA, Asia",
            "seo_description": "Emdad Global strengthens export coverage in 2025 with reliable programs and quality assurance.",
            "og_title": "Export Markets 2025",
            "og_description": "Expanding reach with reliable programs and QA.",
            "twitter_title": "Export Markets 2025",
            "twitter_description": "Stronger programs and quality in key regions.",
            "tags": "exports,programs,quality,markets,Europe,Asia,MENA",
            "content": (
                """
                <p>Emdad Global continues to grow in 2025 by expanding programs across Europe, MENA, and Asia.
                Our teams synchronize harvest, packing, inspections, and logistics to align with seasonal demand and quality goals.</p>

                <h3>Program Design</h3>
                <ul>
                  <li>Flexible volumes and packaging (retail and food service)</li>
                  <li>Specification-driven sorting and documentation</li>
                  <li>Predictable schedules with cold-chain integrity</li>
                </ul>

                <p>We welcome partnerships for private label, seasonal promotions, and category development in 2025.</p>
                """
            ),
        },
        "ar": {
            "title": "أسواق تصدير جديدة في 2025: تعزيز الحضور العالمي",
            "excerpt": "تعزز إمداد جلوبال حضورها في أوروبا والشرق الأوسط وآسيا في 2025 ببرامج توريد موثوقة.",
            "focus_keyword": "أسواق التصدير 2025 إمداد",
            "seo_title": "أسواق التصدير 2025: أوروبا والشرق الأوسط وآسيا",
            "seo_description": "تعزّز إمداد جلوبال تغطية التصدير في 2025 ببرامج موثوقة وضمان جودة.",
            "og_title": "أسواق التصدير 2025",
            "og_description": "توسّع الحضور ببرامج موثوقة وضمان جودة.",
            "twitter_title": "أسواق التصدير 2025",
            "twitter_description": "برامج أقوى وجودة في مناطق رئيسية.",
            "tags": "تصدير,برامج,جودة,أسواق,أوروبا,آسيا,الشرق الأوسط",
            "content": (
                """
                <p>تواصل إمداد جلوبال النمو في 2025 بتوسيع برامجها عبر أوروبا والشرق الأوسط وآسيا.
                ينسّق فريقنا الحصاد والتعبئة والفحص واللوجستيات بما يتماشى مع الطلب الموسمي وأهداف الجودة.</p>

                <h3>تصميم البرامج</h3>
                <ul>
                  <li>أحجام وتغليف مرنان (تجزئة وخدمات طعام)</li>
                  <li>فرز قائم على المواصفات وتوثيق متكامل</li>
                  <li>جداول متوقعة مع سلامة سلسلة التبريد</li>
                </ul>

                <p>نرحب بالشراكات للعلامات الخاصة والعروض الموسمية وتطوير الفئة في 2025.</p>
                """
            ),
        },
        "featured": False,
        "show_on_homepage": True,
    },
}

# Global long-form suffix to boost depth, keywords, and internal links
LONG_SUFFIX_EN = """
<h2>Quality, Certifications, and Compliance</h2>
<p>All sourcing and packing processes are aligned with <strong>ISO 22000</strong> and <strong>HACCP</strong>, with
full traceability from farm to export. We maintain strict microbiological limits for <a href="/products?cat=spices">spices</a>
and <a href="/products?cat=dried-herbs">dried herbs</a>, and robust cold-chain control for <a href="/products?cat=fresh-fruit">fresh fruit</a>
and <a href="/products?cat=iqf-fruit">IQF fruit</a>.</p>

<h2>Categories and Internal Links</h2>
<ul>
  <li>Fresh Fruit: <a href="/products?cat=fresh-fruit">category</a> — key items:
    <a href="/product/oranges">oranges</a>, strawberries (<a href="/product/strawberries">fresh</a>), table grapes</li>
  <li>IQF Fruit: <a href="/products?cat=iqf-fruit">category</a> — spotlight:
    <a href="/product/iqf-mango">IQF mango</a>, IQF strawberries, custom blends</li>
  <li>Dates: <a href="/products?cat=dates">category</a> — e.g., <a href="/product/dates-whole">dates whole</a></li>
  <li>Spices: <a href="/products?cat=spices">category</a> — e.g., <a href="/product/cumin-seed">cumin seed</a>,
      <a href="/product/coriander-seed">coriander seed</a>, <a href="/product/fennel-seed">fennel seed</a></li>
  <li>Dried Herbs: <a href="/products?cat=dried-herbs">category</a> — basil, marjoram, mint, parsley</li>
  <li>Vegetables & Roots: <a href="/products?cat=vegetables-roots">category</a> — potatoes, onions, garlic</li>
  <li>Oil Seeds: <a href="/products?cat=oil-seeds">category</a> — <a href="/product/sesame-seeds">sesame seeds</a>, flax seeds</li>
</ul>

<h2>Packaging and Specifications</h2>
<ul>
  <li>Retail: clamshells, flow-pack, net bags, punnets, doypacks, sleeves</li>
  <li>Food Service & Industry: cartons (10–18 kg), poly-lined bags, aseptic packaging</li>
  <li>Custom labeling: GTIN/UPC/EAN, batch codes, harvest/packing dates, storage instructions</li>
  <li>Documents: Health certificates, CoO, phytosanitary, SGS/Intertek when required</li>
</ul>

<h2>Seasonality and Availability</h2>
<p>Consult the <a href="/calendar">Seasonality Calendar</a> to plan <em>peak</em>, <em>available</em>, and <em>limited</em> periods.
Where continuity is required, consider <a href="/products?cat=iqf-fruit">IQF alternatives</a> with stable specs year-round.</p>

<h2>Logistics and Incoterms</h2>
<p>We support EXW, FCA, FOB, and CIF across major ports and airports with temperature-controlled lanes.
Transit-time planning is aligned with product shelf life and destination QA protocols.</p>

<h2>FAQs</h2>
<p><strong>Q:</strong> Can you develop private label lines?<br>
<strong>A:</strong> Yes. We handle artwork, barcodes, and packaging compliance.</p>
<p><strong>Q:</strong> Do you provide microbiology reports for spices and herbs?<br>
<strong>A:</strong> Yes, upon request. We adhere to strict sorting and sterilization protocols where applicable.</p>

<h2>Call to Action</h2>
<p><a href="/contact" class="btn btn-primary btn-lg me-2">Request a Quote</a>
<a href="/products" class="btn btn-outline-success btn-lg">Browse Products</a></p>
"""

# Additional deep-dive sections to extend word count and SEO
DETAILS_EN = """
<h2>Buyer Programs and Category Strategy</h2>
<p>We co-build category strategies with retailers and importers focused on shelf presence, repeat purchase, and
waste reduction. Programs include forecast alignment, SKU rationalization, and promo calendars.</p>

<h2>Food Safety and Documentation</h2>
<p>Our QA team maintains SOPs for sampling, pesticide residue checks where applicable, and supplier audits.
Documentation packages are tailored to destination regulations.</p>

<h2>Sustainability and Social Impact</h2>
<p>We invest in water stewardship, soil health improvements, and worker training. These initiatives support long-term
productivity while meeting buyer ESG expectations.</p>
"""

DETAILS_AR = """
<h2>برامج المشتري واستراتيجية الفئة</h2>
<p>نبني استراتيجيات الفئات بالتعاون مع تجار التجزئة والمستوردين مع التركيز على الحضور على الرف والتكرار الشرائي وتقليل الهدر.
تشمل البرامج مواءمة التوقعات وترشيد رموز المنتجات وجدولة العروض الترويجية.</p>

<h2>سلامة الغذاء والمستندات</h2>
<p>يحافظ فريق ضبط الجودة على إجراءات تشغيل قياسية لأخذ العينات وفحوصات متبقيات المبيدات عند اللزوم ومراجعات الموردين.
تُكيَّف حزم المستندات وفق لوائح بلد الوصول.</p>

<h2>الاستدامة والأثر الاجتماعي</h2>
<p>نستثمر في إدارة المياه وتحسين صحة التربة وتدريب العمال. تدعم هذه المبادرات الإنتاجية طويلة الأمد وتلبي توقعات ESG لدى المشترين.</p>
"""

# Extra mega section to significantly extend word count and cover keywords/internal links
LONG_MEGA_EN = """
<h2>Category-by-Category Buying Guide (2025)</h2>
<p>Use this guide to plan your <strong>fresh fruit</strong>, <strong>IQF fruit</strong>, <strong>dates</strong>,
<strong>spices</strong>, <strong>dried herbs</strong>, <strong>vegetables & roots</strong>, and <strong>oil seeds</strong> sourcing.</p>

<h3>Fresh Fruit</h3>
<ul>
  <li><a href="/product/oranges">Oranges</a> — Valencia/Navel; brix, size, color, packing; retail and juicing use-cases</li>
  <li><a href="/product/strawberries">Strawberries</a> — hand-picked; cold-chain integrity; dessert and bakery programs</li>
  <li>Table Grapes — sizing and firmness options; shelf-life optimization</li>
</ul>

<h3>IQF Fruit</h3>
<ul>
  <li><a href="/product/iqf-mango">IQF Mango</a> — slices/dice; smoothie bars; industrial formulations</li>
  <li>IQF Strawberries — whole/sliced; dessert toppings; year-round continuity</li>
  <li>Custom Mixes — balanced bricks; specification documentation available</li>
</ul>

<h3>Dates</h3>
<ul>
  <li><a href="/product/dates-whole">Dates Whole</a> — premium grades; snacking, baking, industrial syrups</li>
  <li>Date Derivatives — paste, dices; clean label sweetening</li>
</ul>

<h3>Spices and Dried Herbs</h3>
<ul>
  <li><a href="/product/cumin-seed">Cumin Seed</a>, <a href="/product/coriander-seed">Coriander</a>, <a href="/product/fennel-seed">Fennel</a> — cleaned/graded</li>
  <li>Basil, Marjoram, Mint, Dill, Parsley — aroma retention; microbiology thresholds</li>
</ul>

<h3>Vegetables & Roots</h3>
<ul>
  <li>Potatoes, Onions, Garlic — storage programs; calibrated sizes; food-service packs</li>
</ul>

<h3>Oil Seeds</h3>
<ul>
  <li><a href="/product/sesame-seeds">Sesame Seeds</a>, Flax Seeds — bakery and oil extraction applications</li>
</ul>

<h2>Specifications and QC</h2>
<ul>
  <li>Sorting: defect thresholds, foreign-matter controls, metal detection where applicable</li>
  <li>Microbiology: APC, yeast & mold targets for <a href="/products?cat=spices">spices</a> and <a href="/products?cat=dried-herbs">dried herbs</a></li>
  <li>Pesticide Residues: aligned with destination MRLs when testing is requested</li>
  <li>Traceability: batch and farm-level data mapping</li>
</ul>

<h2>Programs and Forecasting</h2>
<p>Provide monthly volumes and packaging forecasts to lock in capacity. We adjust plans using rolling forecasts</p>
<p>and reserve export slots to maintain continuity in peak months.</p>

<h2>Case Studies</h2>
<ul>
  <li>Retailer A: citrus and herbs category uplift with consistent displays and QA documentation</li>
  <li>Juice chain B: seamless switchover between fresh and IQF berries to maintain menu consistency</li>
</ul>

<h2>Next Actions</h2>
<p>Explore categories: <a href="/products?cat=fresh-fruit">Fresh</a>, <a href="/products?cat=iqf-fruit">IQF</a>, <a href="/products?cat=dates">Dates</a>,
<a href="/products?cat=spices">Spices</a>, <a href="/products?cat=dried-herbs">Dried Herbs</a>, <a href="/products?cat=vegetables-roots">Vegetables & Roots</a>,
<a href="/products?cat=oil-seeds">Oil Seeds</a>. Plan with the <a href="/calendar">Seasonality Calendar</a> and <a href="/contact">request a quote</a>.</p>
"""

LONG_MEGA_AR = """
<h2>دليل الشراء حسب الفئات (2025)</h2>
<p>استخدم هذا الدليل لتخطيط التوريد عبر <strong>الفواكه الطازجة</strong> و<strong>فواكه IQF</strong> و<strong>التمور</strong>
و<strong>التوابل</strong> و<strong>الأعشاب المجففة</strong> و<strong>الخضروات والجذور</strong> و<strong>البذور الزيتية</strong>.</p>

<h3>الفواكه الطازجة</h3>
<ul>
  <li><a href="/product/oranges">برتقال</a> — فالنسيا/نافيل؛ بمتطلبات بكس، مقاس، لون، وتعبئة؛ استخدامات للتجزئة والعصير</li>
  <li><a href="/product/strawberries">فراولة</a> — قطف يدوي؛ سلامة سلسلة التبريد؛ برامج حلويات ومخبوزات</li>
  <li>عنب مائدة — خيارات قياس وتماسك؛ تحسين العمر التخزيني</li>
</ul>

<h3>فواكه IQF</h3>
<ul>
  <li><a href="/product/iqf-mango">مانجو IQF</a> — شرائح/مكعبات؛ عصائر؛ تصنيعات غذائية</li>
  <li>فراولة IQF — صحيحة/مقطعة؛ إضافات حلويات؛ استمرارية على مدار العام</li>
  <li>خلطات مخصصة — قوالب متوازنة؛ وثائق مواصفات متاحة</li>
</ul>

<h3>التمور</h3>
<ul>
  <li><a href="/product/dates-whole">تمور كاملة</a> — درجات متميزة؛ للتناول والخبز ومركزات صناعية</li>
  <li>مشتقات التمور — معجون ومكعبات؛ تحلية بملصقات نظيفة</li>
</ul>

<h3>التوابل والأعشاب المجففة</h3>
<ul>
  <li><a href="/product/cumin-seed">كمون</a>، <a href="/product/coriander-seed">كزبرة</a>، <a href="/product/fennel-seed">شمر</a> — تنظيف وتصنيف</li>
  <li>ريحان، مردقوش، نعناع، شبت، بقدونس — احتفاظ بالعطر؛ حدود ميكروبيولوجية</li>
</ul>

<h3>الخضروات والجذور</h3>
<ul>
  <li>بطاطس وبصل وثوم — برامج تخزين؛ معايرة أحجام؛ عبوات خدمات طعام</li>
</ul>

<h3>البذور الزيتية</h3>
<ul>
  <li><a href="/product/sesame-seeds">سمسم</a>، بذور كتان — مخبوزات واستخلاص زيوت</li>
</ul>

<h2>المواصفات وضبط الجودة</h2>
<ul>
  <li>الفرز: حدود العيوب، التحكم في الأجسام الغريبة، والكشف المعدني عند اللزوم</li>
  <li>الميكروبيولوجي: أهداف العدّ البكتيري والخمائر/العفن لفئة <a href="/products?cat=spices">التوابل</a> و<a href="/products?cat=dried-herbs">الأعشاب المجففة</a></li>
  <li>متبقيات المبيدات: بما يتماشى مع حدود الدولة المستقبِلة عند طلب الاختبار</li>
  <li>التتبّع: بيانات الدفعة والمزرعة</li>
</ul>

<h2>البرامج والتوقعات</h2>
<p>قدّم أحجاماً شهرية وتوقعات للتعبئة لحجز الطاقة الاستيعابية. نضبط الخطط بتوقعات متحركة</p>
<p>ونحجز مسارات الشحن لضمان الاستمرارية خلال أشهر الذروة.</p>

<h2>دراسات حالة</h2>
<ul>
  <li>تاجر تجزئة أ: نمو فئة الحمضيات والأعشاب مع عروض ثابتة ووثائق جودة</li>
  <li>سلسلة عصائر ب: انتقال سلس بين الفراولة الطازجة وIQF للحفاظ على ثبات القوائم</li>
</ul>

<h2>الخطوات التالية</h2>
<p>استكشف الفئات: <a href="/products?cat=fresh-fruit">طازجة</a>، <a href="/products?cat=iqf-fruit">IQF</a>، <a href="/products?cat=dates">تمور</a>،
<a href="/products?cat=spices">توابل</a>، <a href="/products?cat=dried-herbs">أعشاب مجففة</a>، <a href="/products?cat=vegetables-roots">خضروات وجذور</a>،
<a href="/products?cat=oil-seeds">بذور زيتية</a>. خطط باستخدام <a href="/calendar">تقويم الموسمية</a> ثم <a href="/contact">اطلب عرض سعر</a>.</p>
"""

# Ultra-long sections to substantially increase depth and cover advanced buyer topics
LONG_ULTRA_EN = """
<h2>EU/UK/GCC/Asia Market Requirements</h2>
<p>Across the EU and UK, buyers expect precise documentation, clear pesticide residue statements when required, and
consistent grading. GCC markets emphasize freshness, clean labeling, and reliable cold-chain. In Asia, importers
value strong category plans, predictable lead times, and packaging tailored to local formats. We align our
commercial, logistics, and QA processes to these expectations, providing specification sheets, photos, and
pre-shipment reports as needed.</p>

<h2>Quality KPIs and Acceptance Criteria</h2>
<p>For <a href="/products?cat=fresh-fruit">fresh fruit</a>, we agree on brix, size, external color, and permissible
cosmetic variances by SKU. For <a href="/products?cat=spices">spices</a> and <a href="/products?cat=dried-herbs">dried herbs</a>,
we confirm moisture, purity, ash, volatile oil (where applicable), and microbiology thresholds. For
<a href="/products?cat=iqf-fruit">IQF fruit</a>, we define piece size, breakage, glaze percentage, and organoleptic parameters.</p>

<h2>Pricing and RFQ Process</h2>
<p>Pricing reflects grade, packing, volume, documentation, and logistics terms. To receive a tailored quotation,
please include monthly volumes, packaging format, destination, certifications, and required documents. Our team will
respond within 24 hours with an offer aligned to your buying program and seasonality.</p>

<h2>Private Label Implementation</h2>
<p>We support private label from artwork to barcode verification and carton specs. We provide mockups and
pre-production samples when required, ensuring on-shelf differentiation and operational feasibility. Our packaging
partners can produce retail-ready packs and food-service cartons with consistent quality.</p>

<h2>End-to-End Traceability</h2>
<p>From farm to final loading, each batch is traceable. We capture harvest dates, farm origin, packing lines, lot IDs,
and inspection records. This data is available in summaries and can be integrated into your QA systems upon request.</p>
"""

LONG_ULTRA_AR = """
<h2>متطلبات أسواق الاتحاد الأوروبي/المملكة المتحدة/الخليج/آسيا</h2>
<p>يتوقع المشترون في الاتحاد الأوروبي والمملكة المتحدة وثائق دقيقة وتصريحات واضحة لمتبقيات المبيدات عند اللزوم وتصنيفاً
متسقاً. تركز أسواق الخليج على الطزاجة والملصقات النظيفة وسلامة سلسلة التبريد. وفي آسيا، يقدّر المستوردون خطط الفئة
القوية ومواعيد التسليم المتوقعة وتغليفاً مناسباً للتنسيقات المحلية. نُوائم عملياتنا التجارية واللوجستية وضبط الجودة مع هذه
التوقعات، ونوفر نشرات المواصفات والصور وتقارير ما قبل الشحن عند الحاجة.</p>

<h2>مؤشرات الجودة ومعايير القبول</h2>
<p>بالنسبة لـ<a href="/products?cat=fresh-fruit">الفواكه الطازجة</a>، نتفق على مؤشرات البكس والمقاس واللون الخارجي ونِسب
العيوب الشكلية المسموح بها لكل منتج. ولـ<a href="/products?cat=spices">التوابل</a> و<a href="/products?cat=dried-herbs">الأعشاب المجففة</a>،
نُثبت حدود الرطوبة والنقاء والرماد والزيوت العطرية (عند اللزوم) والحدود الميكروبيولوجية. أما <a href="/products?cat=iqf-fruit">فواكه IQF</a>
فنحدد مقاس القطع ونسبة التكسّر ونِسبة التزليج والمعايير الحسية.</p>

<h2>التسعير وعملية طلب عرض السعر</h2>
<p>يعكس السعر الدرجة والتعبئة والحجم والوثائق وشروط اللوجستيات. للحصول على عرض سعر مخصص، يُرجى تضمين الأحجام الشهرية ونوع
التعبئة والوجهة والاعتمادات المطلوبة والمستندات اللازمة. سيردّ فريقنا خلال 24 ساعة بعرض متوافق مع برنامج الشراء والموسمية.</p>

<h2>تنفيذ العلامة الخاصة</h2>
<p>ندعم العلامة الخاصة من التصميم إلى التحقق من الباركود ومواصفات الصناديق. نوفر نماذج أولية وعينات ما قبل الإنتاج عند
الحاجة، لضمان تميّز الرفوف وقابلية التشغيل. يمكن لشركائنا إنتاج عبوات جاهزة للتجزئة وكرتون خدمات طعام بجودة متسقة.</p>

<h2>التتبّع الشامل</h2>
<p>من المزرعة وحتى التحميل النهائي، كل دفعة قابلة للتتبّع. نُسجّل تواريخ الحصاد ومصدر المزرعة وخطوط التعبئة وأرقام الدُفعات
وسجلات الفحص. تتوفر هذه البيانات في ملخصات ويمكن دمجها في أنظمة الجودة لديكم عند الطلب.</p>
"""


LONG_SUFFIX_AR = """
<h2>الجودة والاعتمادات والامتثال</h2>
<p>تتوافق عمليات التوريد والتعبئة لدينا مع معايير <strong>ISO 22000</strong> و<strong>HACCP</strong> مع
تتبّع كامل من المزرعة حتى التصدير. نحافظ على حدود ميكروبيولوجية صارمة في <a href="/products?cat=spices">التوابل</a>
و<a href="/products?cat=dried-herbs">الأعشاب المجففة</a>، وسيطرة قوية على سلسلة التبريد لفئة <a href="/products?cat=fresh-fruit">الفواكه الطازجة</a>
وفئة <a href="/products?cat=iqf-fruit">الفواكه المجمدة IQF</a>.</p>

<h2>الفئات والروابط الداخلية</h2>
<ul>
  <li>الفواكه الطازجة: <a href="/products?cat=fresh-fruit">الفئة</a> — أبرز المنتجات:
    <a href="/product/oranges">برتقال</a>، فراولة (<a href="/product/strawberries">طازجة</a>)، عنب مائدة</li>
  <li>فواكه IQF: <a href="/products?cat=iqf-fruit">الفئة</a> — مثل:
    <a href="/product/iqf-mango">مانجو IQF</a>، فراولة IQF، وخليط فواكه حسب الطلب</li>
  <li>التمور: <a href="/products?cat=dates">الفئة</a> — مثال: <a href="/product/dates-whole">تمور كاملة</a></li>
  <li>التوابل: <a href="/products?cat=spices">الفئة</a> — مثل <a href="/product/cumin-seed">كمون</a>،
      <a href="/product/coriander-seed">كزبرة</a>، <a href="/product/fennel-seed">شمر</a></li>
  <li>الأعشاب المجففة: <a href="/products?cat=dried-herbs">الفئة</a> — ريحان، مردقوش، نعناع، بقدونس</li>
  <li>الخضروات والجذور: <a href="/products?cat=vegetables-roots">الفئة</a> — بطاطس، بصل، ثوم</li>
  <li>البذور الزيتية: <a href="/products?cat=oil-seeds">الفئة</a> — <a href="/product/sesame-seeds">سمسم</a>، بذور كتان</li>
</ul>

<h2>التعبئة والمواصفات</h2>
<ul>
  <li>التجزئة: علب شفافة، تعبئة فلو-باك، شبك، صناديق صغيرة، أكياس وقوف</li>
  <li>الخدمات الغذائية والصناعة: كراتين (10–18 كجم)، أكياس مبطنة، تعبئة معقمة</li>
  <li>وسم مخصص: GTIN/UPC/EAN، أكواد الدُفعات، تواريخ الحصاد/التعبئة، تعليمات التخزين</li>
  <li>المستندات: شهادات صحية، منشأ، زراعية صحية، وتقارير SGS/Intertek عند الطلب</li>
</ul>

<h2>الموسمية والتوفر</h2>
<p>اطّلع على <a href="/calendar">تقويم الموسمية</a> لتخطيط فترات <em>الذروة</em> و<em>التوفر</em> و<em>المحدودية</em>.
وعند الحاجة للاستمرارية، فكّر في بدائل <a href="/products?cat=iqf-fruit">IQF</a> بثبات المواصفات طوال العام.</p>

<h2>اللوجستيات والإنكوترمز</h2>
<p>ندعم EXW وFCA وFOB وCIF عبر الموانئ والمطارات الرئيسية مع مسارات مُبرّدة.
يتم مواءمة زمن العبور مع العمر التخزيني ومتطلبات الجودة في الوجهة.</p>

<h2>أسئلة متكررة</h2>
<p><strong>س:</strong> هل يمكن تطوير علامات خاصة؟<br>
<strong>ج:</strong> نعم، ندير التصميم والباركود ومتطلبات المطابقة.</p>
<p><strong>س:</strong> هل توفرون تقارير ميكروبيولوجية للتوابل والأعشاب؟<br>
<strong>ج:</strong> نعم عند الطلب، مع بروتوكولات فرز وتعقيم صارمة عند الحاجة.</p>

<h2>دعوة لاتخاذ إجراء</h2>
<p><a href="/contact" class="btn btn-primary btn-lg me-2">اطلب عرض سعر</a>
<a href="/products" class="btn btn-outline-success btn-lg">تصفح المنتجات</a></p>
"""

# Backward-compatibility: if DB still has 2024 slug, map it to 2025 content without changing slug
ARTICLES["emdad-global-expands-new-markets-2024"] = ARTICLES["emdad-global-expands-new-markets-2025"]


def apply_updates():
    app = create_app()
    with app.app_context():
        from datetime import timezone
        now = datetime.now(timezone.utc)

        # Try known slugs first (seeded). If missing, fallback to latest 3 published.
        slug_order = [
            "emdad-global-expands-new-markets-2025",
            "sustainable-farming-practices-emdad-global",
            "new-export-markets-expansion",
        ]

        # Collect target articles by priority order, then fill to 3 with latest published
        targets: list[News] = []
        seen = set()
        for slug in slug_order:
            n = News.query.filter_by(slug=slug).first()
            if n and n.id not in seen:
                targets.append(n)
                seen.add(n.id)
        if len(targets) < 3:
            fillers = (News.query.filter_by(status='published')
                       .order_by(News.publish_at.desc())
                       .limit(6).all() or [])
            for n in fillers:
                if n.id not in seen:
                    targets.append(n)
                    seen.add(n.id)
                if len(targets) >= 3:
                    break

        # Ensure we only process up to 3
        targets = targets[:3]

        # Map target to content sets in order
        for idx, n in enumerate(targets):
            # Choose article key: prefer matching slug key, else take by index mapping
            key = n.slug if n.slug in ARTICLES else slug_order[idx] if idx < len(slug_order) else None
            if not key or key not in ARTICLES:
                continue

            payload = ARTICLES[key]
            en = payload["en"]
            ar = payload["ar"]

            # Core fields
            n.title_en = en["title"]
            n.title_ar = ar["title"]
            n.excerpt_en = en["excerpt"]
            n.excerpt_ar = ar["excerpt"]
            # Compose long-form content by appending deep details and long suffix blocks
            n.content_en = (en["content"].strip() + "\n" + LONG_MEGA_EN + "\n" + LONG_ULTRA_EN + "\n" + DETAILS_EN + "\n" + LONG_SUFFIX_EN).strip()
            n.content_ar = (ar["content"].strip() + "\n" + LONG_MEGA_AR + "\n" + LONG_ULTRA_AR + "\n" + DETAILS_AR + "\n" + LONG_SUFFIX_AR).strip()

            # SEO fields
            n.focus_keyword_en = en["focus_keyword"]
            n.focus_keyword_ar = ar["focus_keyword"]
            n.seo_title_en = en["seo_title"][:70]
            n.seo_title_ar = ar["seo_title"][:70]
            n.seo_description_en = en["seo_description"][:160]
            n.seo_description_ar = ar["seo_description"][:160]
            n.og_title_en = en["og_title"][:95]
            n.og_title_ar = ar["og_title"][:95]
            n.og_description_en = en["og_description"][:200]
            n.og_description_ar = ar["og_description"][:200]
            n.twitter_title_en = en["twitter_title"][:70]
            n.twitter_title_ar = ar["twitter_title"][:70]
            n.twitter_description_en = en["twitter_description"][:200]
            n.twitter_description_ar = ar["twitter_description"][:200]

            # Tags and flags
            n.tags = payload.get("tags", en.get("tags")) or en.get("tags")
            n.featured = bool(payload.get("featured", False))
            n.show_on_homepage = bool(payload.get("show_on_homepage", True))
            n.status = 'published'

            # Publish dates in 2025 spaced out
            offset_days = 4 + idx * 7
            n.publish_at = now - timedelta(days=offset_days)
            n.updated_at = now

            # Estimated reading time (roughly 200 wpm, strip HTML tags for count)
            def estimate_minutes(html_text: str) -> int:
                import re
                text = re.sub(r"<[^>]+>", " ", html_text)
                words = max(1, len(text.split()))
                return max(1, round(words / 200))

            n.estimated_reading_time = estimate_minutes(n.content_en)
            n.content_difficulty = 'intermediate'

            db.session.add(n)

        db.session.commit()
        print(f"Updated {len(targets)} news articles with 2025 SEO-optimized content.")


if __name__ == "__main__":
    apply_updates()

