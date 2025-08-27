# Emdad Global - Agricultural Export Website

A modern, bilingual (Arabic/English) website for Emdad Global, an Egyptian agricultural export company specializing in premium fresh and frozen fruits and vegetables.

## 🌟 Features

### 🌐 Bilingual Support
- **Full Arabic and English localization** with RTL layout support
- **Dynamic language switching** with persistent user preferences
- **Culturally appropriate typography** and design elements

### 📱 Responsive Design
- **Mobile-first approach** with Bootstrap 5
- **Touch-friendly interface** optimized for all devices
- **Progressive enhancement** for better performance

### 🛠️ Admin Panel
- **Complete content management system**
- **Product and category management**
- **News and blog administration**
- **User management and permissions**
- **File upload and gallery management**

### 🛍️ Product Catalog
- **Organized product categories** with detailed views
- **Square grid layout** (3 products per row)
- **High-quality product images** with zoom functionality
- **Detailed specifications** and seasonal information

### 📰 News System
- **Blog-style news and updates**
- **Featured articles** and categorization
- **SEO-optimized article pages**

### 📞 Contact System
- **Multiple contact forms** with validation
- **RFQ (Request for Quote) system**
- **Email integration** for notifications

### 🖼️ Gallery
- **Image gallery** for company and product photos
- **Lightbox functionality** for enhanced viewing
- **Category-based organization**

### 🔍 SEO Optimized
- **Meta tags and Open Graph** support
- **Structured data** for search engines
- **Search engine friendly URLs**
- **Sitemap generation**

## 🚀 Technology Stack

- **Backend**: Python Flask 2.3+
- **Database**: SQLAlchemy with SQLite (PostgreSQL ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript ES6+
- **Internationalization**: Flask-Babel for translations
- **Security**: CSRF protection, rate limiting, secure headers
- **Performance**: Image optimization, asset minification

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/whatisup223/emdad.git
cd emdad
```

2. **Create a virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Initialize the database:**
```bash
python init_db.py
```

5. **Run the application:**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 🔐 Default Admin Credentials

- **Email**: admin@emdadglobal.com
- **Password**: admin123

⚠️ **Important**: Change the admin password immediately in production!

## ⚙️ Configuration

Copy `.env.example` to `.env` and update the configuration values:

```bash
cp .env.example .env
```

### Key Configuration Options:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///emdad.db
FLASK_ENV=development
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

## ✨ Key Features

### 🎨 Frontend Features
- **Dynamic Hero Section** with customizable overlay
- **Square Product Grid** (3 products per row)
- **Responsive Navigation** with mobile hamburger menu
- **Smooth Language Switching** with RTL support
- **Contact Forms** with real-time validation
- **Image Gallery** with lightbox functionality
- **News Blog** with featured articles

### 🔧 Admin Features
- **Dashboard** with site statistics
- **Product Management** with image uploads
- **Category Management** with hierarchical structure
- **News Management** with rich text editor
- **User Administration** with role-based access
- **File Manager** for uploads and gallery
- **Site Settings** and configuration

### 🛡️ Technical Features
- **SEO Optimization** with meta tags and structured data
- **Security** with CSRF protection and rate limiting
- **Performance** with optimized images and caching
- **Accessibility** with ARIA labels and semantic HTML
- **Mobile Responsive** with touch-friendly interface

## 🎮 Keyboard Shortcuts

- **Ctrl+Shift+O**: Toggle hero section overlay intensity
- **Ctrl+Shift+P**: Toggle product layout (square/rectangular)

## 🎨 Customization

### Color Scheme
```css
:root {
  --primary-color: #689b8a;      /* Main green */
  --primary-dark: #5a7c6f;       /* Dark green */
  --secondary-color: #f9cb99;    /* Main orange */
  --secondary-light: #f5d7b0;    /* Light orange */
}
```

### Typography
- **Headings**: Poppins (Google Fonts)
- **Body Text**: System font stack for optimal performance
- **Arabic Text**: Optimized Arabic font stack with proper RTL support

## 🚀 Deployment

### Production Setup
1. **Environment**: Set `FLASK_ENV=production`
2. **Database**: Use PostgreSQL or MySQL
3. **Web Server**: Deploy with Gunicorn + Nginx
4. **SSL**: Enable HTTPS with Let's Encrypt
5. **Monitoring**: Set up logging and error tracking

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** your changes: `git commit -m "Add feature"`
4. **Push** to the branch: `git push origin feature-name`
5. **Submit** a pull request

## 📄 License

This project is proprietary software developed for Emdad Global.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🏆 Credits

Developed with ❤️ for **Emdad Global** - Premium Egyptian Agricultural Exports

---

### 🌾 About Emdad Global
**Quality** • **Global Reach** • **Trusted Partnership**

Emdad Global is a leading Egyptian export company specializing in premium agricultural products with over 25 years of experience serving customers across 50+ countries worldwide.
