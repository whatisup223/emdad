from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import json

# Association table for many-to-many relationship between products and certifications
product_certifications = db.Table('product_certifications',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
    db.Column('certification_id', db.Integer, db.ForeignKey('certification.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """User model for admin authentication."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')  # admin, editor, viewer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    assigned_rfqs = db.relationship('RFQ', backref='assigned_user', lazy='dynamic')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic')

    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        """Check if user has specific permission."""
        permissions = {
            'admin': ['create', 'read', 'update', 'delete', 'manage_users'],
            'editor': ['create', 'read', 'update'],
            'viewer': ['read']
        }
        return permission in permissions.get(self.role, [])

    def __repr__(self):
        return f'<User {self.email}>'

class Category(db.Model):
    """Product categories model."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False, index=True)  # citrus, fresh-fruits, etc.
    name_en = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    show_on_homepage = db.Column(db.Boolean, default=True)  # New field for homepage display
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Self-referential relationship for subcategories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))

    # Relationship with products
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def get_name(self, language='en'):
        """Get category name in specified language."""
        return getattr(self, f'name_{language}', self.name_en)

    def get_description(self, language='en'):
        """Get category description in specified language."""
        return getattr(self, f'description_{language}', self.description_en)

    def __repr__(self):
        return f'<Category {self.key}>'

class Product(db.Model):
    """Products model."""
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(200), nullable=False)
    name_ar = db.Column(db.String(200))
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    # HS Code for customs and trade
    hs_code = db.Column(db.String(20), nullable=True)

    # Content
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    short_description_en = db.Column(db.String(500))
    short_description_ar = db.Column(db.String(500))

    # JSON fields for flexible data
    specifications = db.Column(db.Text)  # JSON string
    seasonality = db.Column(db.Text)     # JSON string
    packaging_options = db.Column(db.Text)  # JSON string
    applications = db.Column(db.Text)  # JSON string for applications/use cases

    # SEO
    seo_title_en = db.Column(db.String(200))
    seo_title_ar = db.Column(db.String(200))
    seo_description_en = db.Column(db.String(300))
    seo_description_ar = db.Column(db.String(300))

    # Status and ordering
    status = db.Column(db.String(20), default='active')  # active, inactive, draft
    featured = db.Column(db.Boolean, default=False)
    show_on_homepage = db.Column(db.Boolean, default=False)  # New field for homepage display
    sort_order = db.Column(db.Integer, default=0)

    # Main image path (for backward compatibility)
    image_path = db.Column(db.String(255))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    certifications = db.relationship('Certification', secondary=product_certifications, backref='products')

    def get_name(self, language='en'):
        """Get product name in specified language."""
        return getattr(self, f'name_{language}', self.name_en)

    def get_description(self, language='en'):
        """Get product description in specified language."""
        return getattr(self, f'description_{language}', self.description_en)

    def get_short_description(self, language='en'):
        """Get product short description in specified language."""
        return getattr(self, f'short_description_{language}', self.short_description_en)

    def get_specifications(self):
        """Get raw specifications JSON as dictionary (may contain language keys)."""
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except json.JSONDecodeError:
                return {}
        return {}

    def get_specifications_lang(self, language='en'):
        """Return specifications for the given language.
        Supports two shapes and ALWAYS returns a dict safe for templates:
        - {'en': '{...json...}', 'ar': '{...json...}'} (textarea-stored JSON strings per language)
        - {'brix': '12-14', 'sizes': ['S','M']} (direct dict for all languages)
        """
        data = self.get_specifications()
        if not data:
            return {}
        # If language-keyed
        if isinstance(data, dict) and ('en' in data or 'ar' in data):
            val = data.get(language) or data.get('en') or data.get('ar')
            if isinstance(val, str):
                # Try parse the inner JSON string
                try:
                    parsed = json.loads(val)
                    return parsed if isinstance(parsed, dict) else {'notes': parsed}
                except Exception:
                    # Fallback to a single-note field
                    return {'notes': val}
            # If already a dict, return it; otherwise wrap as note
            return val if isinstance(val, dict) else {'notes': val}
        # Already direct dict
        return data if isinstance(data, dict) else {}

    def set_specifications(self, specs_dict):
        """Set specifications from dictionary."""
        self.specifications = json.dumps(specs_dict) if specs_dict else None

    def get_seasonality(self):
        """Get raw seasonality JSON as dictionary (may contain language keys)."""
        if self.seasonality:
            try:
                return json.loads(self.seasonality)
            except json.JSONDecodeError:
                return {}
        return {}

    def get_seasonality_lang(self, language='en'):
        """Return seasonality for the given language if language-keyed, else raw dict."""
        data = self.get_seasonality()
        if not data:
            return {}
        if isinstance(data, dict) and ('en' in data or 'ar' in data):
            val = data.get(language) or data.get('en') or data.get('ar')
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except Exception:
                    return {'notes': val}
            return val if isinstance(val, dict) else {}
        return data if isinstance(data, dict) else {}

    def get_packaging_options(self):
        """Get raw packaging options JSON as dictionary (may contain language keys)."""
        if self.packaging_options:
            try:
                return json.loads(self.packaging_options)
            except json.JSONDecodeError:
                return {}
        return {}

    def get_packaging_options_lang(self, language='en'):
        """Return packaging options for the given language if language-keyed, else raw dict."""
        data = self.get_packaging_options()
        if not data:
            return {}
        if isinstance(data, dict) and ('en' in data or 'ar' in data):
            val = data.get(language) or data.get('en') or data.get('ar')
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except Exception:
                    return {'notes': val}
            return val if isinstance(val, dict) else {}
        return data if isinstance(data, dict) else {}

    def set_packaging_options(self, packaging_dict):
        """Set packaging options from dictionary."""
        self.packaging_options = json.dumps(packaging_dict) if packaging_dict else None

    # Applications / Use Cases helpers (same pattern as packaging/specifications)
    def get_applications(self):
        """Get raw applications JSON as dictionary (may contain language keys)."""
        if self.applications:
            try:
                return json.loads(self.applications)
            except json.JSONDecodeError:
                return {}
        return {}

    def get_applications_lang(self, language='en'):
        """Return applications for the given language if language-keyed, else raw dict."""
        data = self.get_applications()
        if not data:
            return {}
        if isinstance(data, dict) and ('en' in data or 'ar' in data):
            val = data.get(language) or data.get('en') or data.get('ar')
            if isinstance(val, str):
                try:
                    return json.loads(val)
                except Exception:
                    return {'notes': val}
            return val if isinstance(val, dict) else {}
        return data if isinstance(data, dict) else {}

    def set_applications(self, applications_dict):
        """Set applications from dictionary."""
        self.applications = json.dumps(applications_dict) if applications_dict else None

    def get_main_image(self):
        """Get the main product image."""
        return self.images.filter_by(is_main=True).first() or self.images.first()

    def get_hs_code_formatted(self):
        """Get HS code in formatted display format (HS:XXXXXX)."""
        if self.hs_code:
            return f"HS:{self.hs_code}"
        return None

    def get_hs_code_description(self, language='en'):
        """Get HS code description in specified language."""
        if not self.hs_code:
            return None

        try:
            from app.utils.hs_codes import get_hs_code_description
            return get_hs_code_description(self.hs_code, language)
        except ImportError:
            return None

    def get_hs_code_display(self, language='en'):
        """Get HS code with description for display."""
        if not self.hs_code:
            return None

        try:
            from app.utils.hs_codes import format_hs_code_display
            return format_hs_code_display(self.hs_code, language)
        except ImportError:
            return self.hs_code

    def __repr__(self):
        return f'<Product {self.slug}>'

class ProductImage(db.Model):
    """Product images model."""
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    alt_text_en = db.Column(db.String(200))
    alt_text_ar = db.Column(db.String(200))
    is_main = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_alt_text(self, language='en'):
        """Get alt text in specified language."""
        return getattr(self, f'alt_text_{language}', self.alt_text_en)

    def __repr__(self):
        return f'<ProductImage {self.filename}>'

class Certification(db.Model):
    """Certifications model."""
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100))
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    logo_path = db.Column(db.String(255))
    website_url = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_name(self, language='en'):
        """Get certification name in specified language."""
        return getattr(self, f'name_{language}', self.name_en)

    def get_description(self, language='en'):
        """Get certification description in specified language."""
        return getattr(self, f'description_{language}', self.description_en)

    def __repr__(self):
        return f'<Certification {self.name_en}>'

class Service(db.Model):
    """Services model."""
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200))
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    icon = db.Column(db.String(100))  # Font Awesome icon class
    image_path = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_title(self, language='en'):
        """Get service title in specified language."""
        return getattr(self, f'title_{language}', self.title_en)

    def get_description(self, language='en'):
        """Get service description in specified language."""
        return getattr(self, f'description_{language}', self.description_en)

    def __repr__(self):
        return f'<Service {self.title_en}>'

class News(db.Model):
    """Enhanced News/Blog model with advanced SEO features."""
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200))
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    excerpt_en = db.Column(db.String(500))
    excerpt_ar = db.Column(db.String(500))
    content_en = db.Column(db.Text)
    content_ar = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    tags = db.Column(db.String(500))  # Comma-separated tags

    # Enhanced Keywords
    focus_keyword_en = db.Column(db.String(100))
    focus_keyword_ar = db.Column(db.String(100))

    # Enhanced SEO
    seo_title_en = db.Column(db.String(70))
    seo_title_ar = db.Column(db.String(70))
    seo_description_en = db.Column(db.String(160))
    seo_description_ar = db.Column(db.String(160))

    # Open Graph
    og_title_en = db.Column(db.String(95))
    og_title_ar = db.Column(db.String(95))
    og_description_en = db.Column(db.String(200))
    og_description_ar = db.Column(db.String(200))
    og_image = db.Column(db.String(255))

    # Twitter Card
    twitter_title_en = db.Column(db.String(70))
    twitter_title_ar = db.Column(db.String(70))
    twitter_description_en = db.Column(db.String(200))
    twitter_description_ar = db.Column(db.String(200))

    # Schema.org
    article_type = db.Column(db.String(50), default='Article')

    # Publishing
    status = db.Column(db.String(20), default='draft')  # draft, published, scheduled, archived
    featured = db.Column(db.Boolean, default=False)
    show_on_homepage = db.Column(db.Boolean, default=False)  # New field for homepage display
    publish_at = db.Column(db.DateTime)

    # Content metadata
    estimated_reading_time = db.Column(db.Integer)  # in minutes
    content_difficulty = db.Column(db.String(20), default='intermediate')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_title(self, language='en'):
        """Get news title in specified language."""
        return getattr(self, f'title_{language}', self.title_en)

    def get_excerpt(self, language='en'):
        """Get news excerpt in specified language."""
        return getattr(self, f'excerpt_{language}', self.excerpt_en)

    def get_content(self, language='en'):
        """Get news content in specified language."""
        return getattr(self, f'content_{language}', self.content_en)

    def get_tags_list(self):
        """Get tags as a list."""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

    def get_seo_title(self, language='en'):
        """Get SEO title in specified language."""
        seo_title = getattr(self, f'seo_title_{language}', None)
        return seo_title if seo_title else self.get_title(language)

    def get_seo_description(self, language='en'):
        """Get SEO description in specified language."""
        seo_desc = getattr(self, f'seo_description_{language}', None)
        return seo_desc if seo_desc else self.get_excerpt(language)

    def get_reading_time(self, language='en'):
        """Estimate reading time in minutes."""
        content = self.get_content(language)
        if not content:
            return 1

        # Remove HTML tags for word count
        import re
        text = re.sub(r'<[^>]+>', '', content)
        word_count = len(text.split())

        # Average reading speed: 200 words per minute
        reading_time = max(1, round(word_count / 200))
        return reading_time

    def is_published(self):
        """Check if news article is published."""
        return (self.status == 'published' and
                self.publish_at and
                self.publish_at <= datetime.utcnow())

    def __repr__(self):
        return f'<News {self.slug}>'

class Gallery(db.Model):
    """Gallery model for images."""
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ar = db.Column(db.String(200))
    description_en = db.Column(db.Text)
    description_ar = db.Column(db.Text)
    image_path = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50))  # farms, packing, storage, exports
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_title(self, language='en'):
        """Get gallery title in specified language."""
        return getattr(self, f'title_{language}', self.title_en)

    def get_description(self, language='en'):
        """Get gallery description in specified language."""
        return getattr(self, f'description_{language}', self.description_en)


class GalleryCategory(db.Model):
    """Optional metadata for gallery categories (for custom categories)."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), unique=True, nullable=False)
    name_en = db.Column(db.String(200))
    name_ar = db.Column(db.String(200))
    icon_class = db.Column(db.String(80), default='fa-tags')
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryCategory {self.key}>'

class RFQ(db.Model):
    """Request for Quote model."""
    id = db.Column(db.Integer, primary_key=True)

    # Contact information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(200))
    country = db.Column(db.String(100))

    # Product information
    category_key = db.Column(db.String(50))  # citrus, fresh-fruits, etc.
    product_name = db.Column(db.String(200))
    quantity = db.Column(db.String(100))
    packaging_preference = db.Column(db.String(200))
    # Optional planning information
    delivery_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.String(100), nullable=True)

    # Message and attachments
    message = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(255))

    # Management
    status = db.Column(db.String(20), default='new')  # new, in_review, quoted, closed, cancelled
    priority = db.Column(db.String(10), default='normal')  # low, normal, high, urgent
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    internal_notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_status_label(self):
        """Get human-readable status label."""
        status_labels = {
            'new': 'New',
            'in_review': 'In Review',
            'quoted': 'Quoted',
            'closed': 'Closed',
            'cancelled': 'Cancelled'
        }
        return status_labels.get(self.status, self.status.title())

    def get_priority_label(self):
        """Get human-readable priority label."""
        priority_labels = {
            'low': 'Low',
            'normal': 'Normal',
            'high': 'High',
            'urgent': 'Urgent'
        }
        return priority_labels.get(self.priority, self.priority.title())

    def __repr__(self):
        return f'<RFQ {self.id} - {self.name}>'

class AuditLog(db.Model):
    """Audit log for tracking admin actions."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # create, update, delete, login, logout
    entity_type = db.Column(db.String(50))  # product, category, user, etc.
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)  # JSON string with additional details
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_details(self):
        """Get details as dictionary."""
        if self.details:
            try:
                return json.loads(self.details)
            except json.JSONDecodeError:
                return {}
        return {}

    def set_details(self, details_dict):
        """Set details from dictionary."""
        self.details = json.dumps(details_dict) if details_dict else None

    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>'

class CompanyInfo(db.Model):
    """Company information model for dynamic content management."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)  # about_mission, about_vision, etc.
    title_en = db.Column(db.String(200))
    title_ar = db.Column(db.String(200))
    content_en = db.Column(db.Text)
    content_ar = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_title(self, language='en'):
        """Get title in specified language."""
        return getattr(self, f'title_{language}', self.title_en)

    def get_content(self, language='en'):
        """Get content in specified language."""
        return getattr(self, f'content_{language}', self.content_en)

    def __repr__(self):
        return f'<CompanyInfo {self.key}>'


class AppMeta(db.Model):
    """Simple key/value store for app data migrations or one-time flags."""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get(key):
        return AppMeta.query.filter_by(key=key).first()

    @staticmethod
    def set(key, value="1"):
        row = AppMeta.get(key)
        if not row:
            row = AppMeta(key=key, value=value)
            db.session.add(row)
        else:
            row.value = value
        return row
