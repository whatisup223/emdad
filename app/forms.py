from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError, NumberRange
from wtforms.widgets import TextArea
from app.models import User, Category
from flask_babel import lazy_gettext as _l
from flask import session

class RFQForm(FlaskForm):
    """Request for Quote form."""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    company = StringField('Company Name', validators=[Optional(), Length(max=200)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])

    category_key = SelectField('Product Category', validators=[DataRequired()], choices=[])
    # Keep as SelectField but allow values populated client-side (avoid "Not a valid choice")
    product_name = SelectField('Specific Product', validators=[Optional(), Length(max=200)], choices=[], validate_choice=False)
    quantity = StringField('Required Quantity', validators=[Optional(), Length(max=100)])
    packaging_preference = StringField('Packaging Preference', validators=[Optional(), Length(max=200)])
    delivery_date = DateTimeField('Delivery Date', format='%Y-%m-%d', validators=[Optional()])
    budget = StringField('Budget', validators=[Optional(), Length(max=100)])

    message = TextAreaField('Message/Requirements', validators=[DataRequired(), Length(min=10, max=2000)])
    attachment = FileField('Attachment (Optional)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'Only PDF, DOC, DOCX, and image files allowed!')
    ])

    def __init__(self, *args, **kwargs):
        super(RFQForm, self).__init__(*args, **kwargs)
        # Determine language from session, default to 'en'
        lang = session.get('language', 'en')
        # Populate localized category choices using admin-provided translations
        categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
        self.category_key.choices = [
            ('', 'اختر الفئة' if lang == 'ar' else 'Select a category')
        ] + [
            (cat.key, (cat.name_ar or cat.name_en) if lang == 'ar' else (cat.name_en or cat.name_ar))
            for cat in categories
        ]
        # Initialize product_name with a placeholder option; will be filled dynamically client-side
        self.product_name.choices = [('', 'اختر التصنيف أولاً' if lang == 'ar' else 'Select a category first')]

class LoginForm(FlaskForm):
    """Admin login form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class UserForm(FlaskForm):
    """User management form."""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin')
    ])
    is_active = BooleanField('Active')

    def __init__(self, user=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, email):
        if self.user and self.user.email == email.data:
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address already registered.')

class CategoryForm(FlaskForm):
    """Category management form."""
    key = StringField('Category Key', validators=[DataRequired(), Length(min=2, max=50)])
    name_en = StringField('Name (English)', validators=[DataRequired(), Length(max=100)])
    name_ar = StringField('Name (Arabic)', validators=[Optional(), Length(max=100)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=100)])
    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    parent_id = SelectField('Parent Category (Optional)', validators=[Optional()], coerce=lambda x: int(x) if x and x != '' and x != 'None' else None, choices=[])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    show_on_homepage = BooleanField('Show on Homepage', default=True)
    image = FileField('Category Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

    def __init__(self, category=None, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.category = category
        # Populate parent category choices
        self.parent_id.choices = [(None, 'No Parent')] + [
            (cat.id, cat.name_en) for cat in Category.query.filter_by(is_active=True).order_by(Category.sort_order)
            if not category or cat.id != category.id  # Exclude self from parent options
        ]

class ProductForm(FlaskForm):
    """Product management form."""
    name_en = StringField('Name (English)', validators=[DataRequired(), Length(max=200)])
    name_ar = StringField('Name (Arabic)', validators=[Optional(), Length(max=200)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=200)])
    category_id = SelectField('Category', validators=[DataRequired()], coerce=int, choices=[])
    hs_code = StringField('HS Code', validators=[Optional(), Length(max=20)],
                         render_kw={"placeholder": "e.g., 080510"})

    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    short_description_en = TextAreaField('Short Description (English)', validators=[Optional(), Length(max=500)])
    short_description_ar = TextAreaField('Short Description (Arabic)', validators=[Optional(), Length(max=500)])
    specifications_en = TextAreaField('Specifications (English)', validators=[Optional()])
    specifications_ar = TextAreaField('Specifications (Arabic)', validators=[Optional()])

    # SEO fields
    seo_title_en = StringField('SEO Title (English)', validators=[Optional(), Length(max=200)])
    seo_title_ar = StringField('SEO Title (Arabic)', validators=[Optional(), Length(max=200)])
    seo_description_en = TextAreaField('SEO Description (English)', validators=[Optional(), Length(max=300)])
    seo_description_ar = TextAreaField('SEO Description (Arabic)', validators=[Optional(), Length(max=300)])

    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('draft', 'Draft')
    ])
    featured = BooleanField('Featured Product')
    show_on_homepage = BooleanField('Show on Homepage', default=False)
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    image = FileField('Product Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

    def __init__(self, obj=None, *args, **kwargs):
        super(ProductForm, self).__init__(obj=obj, *args, **kwargs)
        # Populate category choices
        self.category_id.choices = [
            (cat.id, cat.name_en) for cat in Category.query.filter_by(is_active=True).order_by(Category.sort_order)
        ]

        # If editing existing product, populate specifications fields
        if obj and obj.specifications:
            try:
                import json
                specs = json.loads(obj.specifications)
                if 'en' in specs:
                    # If it's a dict, convert to JSON string for editing
                    if isinstance(specs['en'], dict):
                        self.specifications_en.data = json.dumps(specs['en'], indent=2, ensure_ascii=False)
                    else:
                        self.specifications_en.data = specs['en']
                if 'ar' in specs:
                    # If it's a dict, convert to JSON string for editing
                    if isinstance(specs['ar'], dict):
                        self.specifications_ar.data = json.dumps(specs['ar'], indent=2, ensure_ascii=False)
                    else:
                        self.specifications_ar.data = specs['ar']
            except (json.JSONDecodeError, TypeError):
                pass

class CertificationForm(FlaskForm):
    """Certification management form."""
    name_en = StringField('Name (English)', validators=[DataRequired(), Length(max=100)])
    name_ar = StringField('Name (Arabic)', validators=[Optional(), Length(max=100)])
    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    website_url = StringField('Website URL', validators=[Optional(), Length(max=255)])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    logo = FileField('Logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

class ServiceForm(FlaskForm):
    """Service management form."""
    title_en = StringField('Title (English)', validators=[DataRequired(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Optional(), Length(max=200)])
    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    icon = StringField('Icon Class', validators=[Optional(), Length(max=100)],
                      render_kw={"placeholder": "e.g., fas fa-shipping-fast"})
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    image = FileField('Service Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

class NewsForm(FlaskForm):
    """Enhanced News/Blog management form with advanced SEO features."""

    # Basic Information
    title_en = StringField(_l('Title (English)'), validators=[DataRequired(), Length(max=200)])
    title_ar = StringField(_l('Title (Arabic)'), validators=[Optional(), Length(max=200)])
    slug = StringField(_l('URL Slug'), validators=[DataRequired(), Length(max=200)])
    excerpt_en = TextAreaField(_l('Excerpt (English)'), validators=[Optional(), Length(max=500)])
    excerpt_ar = TextAreaField(_l('Excerpt (Arabic)'), validators=[Optional(), Length(max=500)])
    content_en = TextAreaField(_l('Content (English)'), validators=[Optional()], widget=TextArea())
    content_ar = TextAreaField(_l('Content (Arabic)'), validators=[Optional()], widget=TextArea())

    # Enhanced Tags and Keywords
    tags = StringField(_l('Tags'), validators=[Optional(), Length(max=500)],
                      render_kw={"placeholder": "Separate tags with commas"})
    focus_keyword_en = StringField(_l('Focus Keyword (English)'), validators=[Optional(), Length(max=100)],
                                  render_kw={"placeholder": "Primary keyword for SEO"})
    focus_keyword_ar = StringField(_l('Focus Keyword (Arabic)'), validators=[Optional(), Length(max=100)],
                                  render_kw={"placeholder": "الكلمة المفتاحية الأساسية"})

    # Enhanced SEO fields
    seo_title_en = StringField('SEO Title (English)', validators=[Optional(), Length(max=70)])
    seo_title_ar = StringField('SEO Title (Arabic)', validators=[Optional(), Length(max=70)])
    seo_description_en = TextAreaField('SEO Description (English)', validators=[Optional(), Length(max=160)])
    seo_description_ar = TextAreaField('SEO Description (Arabic)', validators=[Optional(), Length(max=160)])

    # Open Graph and Social Media
    og_title_en = StringField('Open Graph Title (English)', validators=[Optional(), Length(max=95)])
    og_title_ar = StringField('Open Graph Title (Arabic)', validators=[Optional(), Length(max=95)])
    og_description_en = TextAreaField('Open Graph Description (English)', validators=[Optional(), Length(max=200)])
    og_description_ar = TextAreaField('Open Graph Description (Arabic)', validators=[Optional(), Length(max=200)])

    # Twitter Card
    twitter_title_en = StringField('Twitter Title (English)', validators=[Optional(), Length(max=70)])
    twitter_title_ar = StringField('Twitter Title (Arabic)', validators=[Optional(), Length(max=70)])
    twitter_description_en = TextAreaField('Twitter Description (English)', validators=[Optional(), Length(max=200)])
    twitter_description_ar = TextAreaField('Twitter Description (Arabic)', validators=[Optional(), Length(max=200)])

    # Schema.org structured data
    article_type = SelectField('Article Type', choices=[
        ('Article', 'Article'),
        ('NewsArticle', 'News Article'),
        ('BlogPosting', 'Blog Post'),
        ('TechArticle', 'Technical Article'),
        ('Report', 'Report')
    ], default='Article')

    # Publishing options
    status = SelectField(_l('Status'), validators=[DataRequired()], choices=[])
    featured = BooleanField(_l('Featured Article'))
    show_on_homepage = BooleanField(_l('Show on Homepage'), default=False)
    publish_at = DateTimeField(_l('Publish Date'), validators=[Optional()], format='%Y-%m-%d %H:%M:%S')

    # Enhanced file uploads
    cover_image = FileField(_l('Cover Image'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    og_image = FileField(_l('Open Graph Image'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])

    # Reading time and difficulty
    estimated_reading_time = IntegerField(_l('Estimated Reading Time (minutes)'),
                                        validators=[Optional(), NumberRange(min=1, max=120)])
    content_difficulty = SelectField(_l('Content Difficulty'), choices=[], default='intermediate')

    submit = SubmitField(_l('Save Article'))

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        # Set dynamic choices for status field
        self.status.choices = [
            ('draft', _l('Draft')),
            ('published', _l('Published')),
            ('scheduled', _l('Scheduled')),
            ('archived', _l('Archived'))
        ]

        # Set dynamic choices for content difficulty
        self.content_difficulty.choices = [
            ('beginner', _l('Beginner')),
            ('intermediate', _l('Intermediate')),
            ('advanced', _l('Advanced')),
            ('expert', _l('Expert'))
        ]

class GalleryForm(FlaskForm):
    """Gallery management form."""
    title_en = StringField('Title (English)', validators=[DataRequired(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Optional(), Length(max=200)])
    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('farms', 'Farms'),
        ('packing', 'Packing Houses'),
        ('storage', 'Cold Storage'),
        ('exports', 'Exports')
    ])
    new_category = StringField('New Category (optional)', validators=[Optional(), Length(max=50)])
    new_category_ar = StringField('اسم الفئة بالعربية (اختياري)', validators=[Optional(), Length(max=100)])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    image = FileField('Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

class GalleryEditForm(FlaskForm):
    """Gallery edit form (image optional)."""
    title_en = StringField('Title (English)', validators=[Optional(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Optional(), Length(max=200)])
    description_en = TextAreaField('Description (English)', validators=[Optional()])
    description_ar = TextAreaField('Description (Arabic)', validators=[Optional()])
    category = SelectField('Category', validators=[Optional()])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')])

class CompanyInfoForm(FlaskForm):
    """Company information management form."""
    key = StringField('Key', validators=[DataRequired(), Length(max=50)])
    title_en = StringField('Title (English)', validators=[Optional(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Optional(), Length(max=200)])
    content_en = TextAreaField('Content (English)', validators=[Optional()])
    content_ar = TextAreaField('Content (Arabic)', validators=[Optional()])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

class UserForm(FlaskForm):
    """User management form."""
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin')
    ])
    is_active = BooleanField('Active', default=True)
