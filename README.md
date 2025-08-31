# Emdad Global - Egyptian Agricultural Exports

A modern, bilingual (Arabic/English) Flask web application for agricultural export business.

## Features

- **Bilingual Support**: Full Arabic and English localization
- **Product Management**: Comprehensive product catalog with categories
- **News System**: Dynamic news and updates management
- **Admin Panel**: Complete administrative interface
- **Contact Forms**: RFQ (Request for Quotation) system
- **SEO Optimized**: Meta tags, structured data, and search engine friendly
- **Responsive Design**: Mobile-first responsive layout
- **Image Management**: Optimized image upload and processing

## Technology Stack

- **Backend**: Flask 3.0, SQLAlchemy, Flask-Migrate
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: Bootstrap 5, Custom CSS, JavaScript
- **Internationalization**: Flask-Babel
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Production Server**: Gunicorn

## Deployment on Render

This application is configured for easy deployment on Render.com:

### Prerequisites

1. GitHub repository with your code
2. Render.com account

### Deployment Steps

1. **Fork/Clone this repository**
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service**:
   - **Name**: `emdad-global`
   - **Environment**: `Python`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or paid for better performance)

4. **Environment Variables** (Auto-configured via render.yaml):
   - `FLASK_ENV=production`
   - `SECRET_KEY` (auto-generated)
   - `DATABASE_URL` (auto-configured with PostgreSQL)

5. **Deploy**: Click "Create Web Service"

### Manual Environment Variables (if needed)

If not using render.yaml, set these environment variables:

```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
SITE_URL=https://your-app.onrender.com
COMPANY_NAME=Emdad Global
COMPANY_EMAIL=info@emdadglobal.com
```

## Local Development

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd emdad
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**:
   ```bash
   python init_db.py
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

### Default Admin Credentials

- **Email**: admin@emdadglobal.com
- **Password**: admin123

**⚠️ Change these credentials immediately after first login!**

## Project Structure

```
emdad/
├── app/                    # Application package
│   ├── __init__.py        # App factory
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms
│   ├── main/              # Main blueprint
│   ├── admin/             # Admin blueprint
│   └── api/               # API blueprint
├── migrations/            # Database migrations
├── static/               # Static files (CSS, JS, images)
├── templates/            # Jinja2 templates
├── translations/         # Babel translations
├── uploads/              # User uploaded files
├── config.py             # Configuration
├── app.py                # Application entry point
├── requirements.txt      # Python dependencies
├── render.yaml           # Render deployment config
├── Procfile              # Process file for deployment
├── runtime.txt           # Python version specification
└── gunicorn.conf.py      # Gunicorn configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary software for Emdad Global.

## Support

For support, email info@emdadglobal.com or create an issue in the repository.
