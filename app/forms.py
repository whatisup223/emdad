from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from wtforms.widgets import TextArea
from app.models import User, Category

class RFQForm(FlaskForm):
    """Request for Quote form."""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    company = StringField('Company Name', validators=[Optional(), Length(max=200)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    
    category_key = SelectField('Product Category', validators=[DataRequired()], choices=[])
    product_name = StringField('Specific Product', validators=[Optional(), Length(max=200)])
    quantity = StringField('Required Quantity', validators=[Optional(), Length(max=100)])
    packaging_preference = StringField('Packaging Preference', validators=[Optional(), Length(max=200)])
    
    message = TextAreaField('Message/Requirements', validators=[DataRequired(), Length(min=10, max=2000)])
    attachment = FileField('Attachment (Optional)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'Only PDF, DOC, DOCX, and image files allowed!')
    ])
    
    def __init__(self, *args, **kwargs):
        super(RFQForm, self).__init__(*args, **kwargs)
        # Populate category choices
        self.category_key.choices = [('', 'Select a category')] + [
            (cat.key, cat.name_en) for cat in Category.query.filter_by(is_active=True).order_by(Category.sort_order)
        ]

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
    parent_id = SelectField('Parent Category', validators=[Optional()], coerce=lambda x: int(x) if x else None, choices=[])
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
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
                    self.specifications_en.data = specs['en']
                if 'ar' in specs:
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
    """News/Blog management form."""
    title_en = StringField('Title (English)', validators=[DataRequired(), Length(max=200)])
    title_ar = StringField('Title (Arabic)', validators=[Optional(), Length(max=200)])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=200)])
    excerpt_en = TextAreaField('Excerpt (English)', validators=[Optional(), Length(max=500)])
    excerpt_ar = TextAreaField('Excerpt (Arabic)', validators=[Optional(), Length(max=500)])
    content_en = TextAreaField('Content (English)', validators=[Optional()], widget=TextArea())
    content_ar = TextAreaField('Content (Arabic)', validators=[Optional()], widget=TextArea())
    tags = StringField('Tags', validators=[Optional(), Length(max=500)], 
                      render_kw={"placeholder": "Separate tags with commas"})
    
    # SEO fields
    seo_title_en = StringField('SEO Title (English)', validators=[Optional(), Length(max=200)])
    seo_title_ar = StringField('SEO Title (Arabic)', validators=[Optional(), Length(max=200)])
    seo_description_en = TextAreaField('SEO Description (English)', validators=[Optional(), Length(max=300)])
    seo_description_ar = TextAreaField('SEO Description (Arabic)', validators=[Optional(), Length(max=300)])
    
    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ])
    featured = BooleanField('Featured Article')
    publish_at = DateTimeField('Publish Date', validators=[Optional()], format='%Y-%m-%d %H:%M')
    
    cover_image = FileField('Cover Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

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
    sort_order = IntegerField('Sort Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    image = FileField('Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])

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
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin')
    ])
    is_active = BooleanField('Active', default=True)
