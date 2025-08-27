# Emdad Global - Agricultural Export Website

A comprehensive Flask web application for Emdad Global, an Egyptian agricultural export company specializing in premium fruits and vegetables.

## Features

### Public Website
- **Homepage**: Hero section, featured categories, products, and news
- **Product Catalog**: Organized by categories (Citrus, Fresh Fruits, Vegetables, Frozen)
- **Product Details**: Specifications, seasonality, packaging options, certifications
- **RFQ System**: Request for Quote form with file uploads and email notifications
- **Company Pages**: About, certifications, services, gallery
- **News/Blog**: Latest updates and industry insights
- **Contact**: Multi-channel contact information and inquiry form
- **Multilingual**: English and Arabic support (ready for implementation)

### Admin Dashboard
- **User Management**: Role-based access (Admin, Editor, Viewer)
- **Content Management**: Products, categories, news, gallery, company info
- **RFQ Management**: View, assign, track, and export inquiries
- **Audit Logging**: Track all admin actions
- **File Management**: Image uploads for products, gallery, news

### Technical Features
- **Responsive Design**: Bootstrap 5 with custom styling
- **SEO Optimized**: Meta tags, structured data, sitemap
- **Security**: CSRF protection, rate limiting, secure file uploads
- **Performance**: Optimized queries, caching ready
- **Email Integration**: SMTP support for notifications
- **Database**: SQLAlchemy ORM with migration support

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.3+
- **Database**: MySQL/PostgreSQL (SQLite for development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login with role-based permissions
- **Forms**: Flask-WTF with CSRF protection
- **Email**: Flask-Mail for SMTP integration
- **Migrations**: Flask-Migrate (Alembic)
- **Internationalization**: Flask-Babel (ready)

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd emdad
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration (Optional)

Create a `.env` file for custom configuration:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///emdad_global.db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
COMPANY_EMAIL=info@emdadglobal.com
```

### 5. Initialize Database

```bash
python init_db.py
```

This creates the database and populates it with sample data including:
- Admin user (admin@emdadglobal.com / admin123)
- Product categories (Citrus, Fresh Fruits, Vegetables, Frozen)
- Sample products with specifications
- Certifications (GlobalG.A.P., HACCP, ISO 22000, etc.)
- Services (FOB/CIF shipping, cold chain, packaging)
- Company information sections
- Sample news articles

### 6. Run the Application

```bash
python run.py
```

Visit `http://localhost:5000` to view the website.

### 7. Access Admin Panel

Visit `http://localhost:5000/admin` and login with:
- **Email**: admin@emdadglobal.com
- **Password**: admin123

⚠️ **Important**: Change the default admin password in production!

## Admin Access

Default admin credentials (change in production):
- **Email**: admin@emdadglobal.com
- **Password**: admin123

Access admin panel at: `http://localhost:5000/admin`

## Project Structure

```
emdad/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms definitions
│   ├── main/              # Public website blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/             # Admin panel blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   └── api/               # API endpoints blueprint
│       ├── __init__.py
│       └── routes.py
├── templates/
│   ├── base.html          # Base template
│   ├── main/              # Public templates
│   │   ├── index.html
│   │   ├── products.html
│   │   └── contact.html
│   └── admin/             # Admin templates
│       └── login.html
├── static/
│   ├── css/
│   │   └── style.css      # Custom styles
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/            # Static images
├── uploads/               # User uploaded files
├── config.py              # Configuration settings
├── app.py                 # Application entry point
├── init_db.py             # Database initialization
├── requirements.txt       # Python dependencies
└── README.md
```

## Database Models

### Core Models
- **User**: Admin users with role-based permissions
- **Category**: Product categories (hierarchical)
- **Product**: Product information with multilingual support
- **ProductImage**: Product image gallery
- **Certification**: Quality certifications
- **Service**: Company services
- **News**: Blog/news articles
- **Gallery**: Image gallery
- **RFQ**: Request for Quote submissions
- **CompanyInfo**: Dynamic company content
- **AuditLog**: Admin action tracking

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `DATABASE_URL` | Database connection string | SQLite |
| `MAIL_SERVER` | SMTP server | localhost |
| `MAIL_USERNAME` | SMTP username | None |
| `MAIL_PASSWORD` | SMTP password | None |
| `COMPANY_EMAIL` | Company email | info@emdadglobal.com |
| `COMPANY_PHONE` | Company phone | +20-xxx-xxx-xxxx |

### Database Configuration

For production, use MySQL or PostgreSQL:

```env
# MySQL
DATABASE_URL=mysql+pymysql://username:password@localhost/emdad_global

# PostgreSQL
DATABASE_URL=postgresql://username:password@localhost/emdad_global
```

## Deployment

### Production Checklist

1. **Security**:
   - Change default admin password
   - Set strong `SECRET_KEY`
   - Configure HTTPS
   - Set up firewall rules

2. **Database**:
   - Use production database (MySQL/PostgreSQL)
   - Set up regular backups
   - Configure connection pooling

3. **Email**:
   - Configure SMTP settings
   - Test email delivery
   - Set up email templates

4. **Files**:
   - Configure file upload limits
   - Set up CDN for static files
   - Implement backup strategy

5. **Monitoring**:
   - Set up logging
   - Configure error tracking
   - Monitor performance

### Sample Nginx Configuration

```nginx
server {
    listen 80;
    server_name emdadglobal.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/emdad/static;
        expires 1y;
    }
    
    location /uploads {
        alias /path/to/emdad/uploads;
        expires 1y;
    }
}
```

## Development

### Adding New Features

1. **Models**: Add to `app/models.py`
2. **Forms**: Add to `app/forms.py`
3. **Routes**: Add to appropriate blueprint
4. **Templates**: Create in `templates/` directory
5. **Migrations**: Run `flask db migrate` and `flask db upgrade`

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep templates organized and well-commented

## Support

For technical support or questions:
- Email: admin@emdadglobal.com
- Documentation: See inline code comments
- Issues: Create GitHub issues for bugs/features

## License

Proprietary software for Emdad Global. All rights reserved.
