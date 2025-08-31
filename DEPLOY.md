# دليل النشر على Render - Emdad Global

## المتطلبات المسبقة

1. حساب على [Render.com](https://render.com)
2. حساب GitHub مع المستودع
3. التأكد من أن جميع الملفات موجودة في المستودع

## الملفات المطلوبة للنشر

تأكد من وجود هذه الملفات في مستودعك:

- ✅ `requirements.txt` - متطلبات Python
- ✅ `render.yaml` - تكوين Render
- ✅ `Procfile` - أوامر التشغيل
- ✅ `runtime.txt` - إصدار Python
- ✅ `gunicorn.conf.py` - تكوين Gunicorn
- ✅ `app.py` - نقطة دخول التطبيق
- ✅ `config.py` - إعدادات التطبيق
- ✅ `build.sh` - سكريبت البناء

## خطوات النشر

### 1. رفع الكود إلى GitHub

```bash
git add .
git commit -m "feat: prepare for Render deployment"
git push origin master
```

### 2. إنشاء خدمة على Render

1. اذهب إلى [Render Dashboard](https://dashboard.render.com)
2. اضغط على "New" → "Web Service"
3. اختر "Build and deploy from a Git repository"
4. اربط حساب GitHub الخاص بك
5. اختر مستودع `emdad`

### 3. تكوين الخدمة

#### الإعدادات الأساسية:
- **Name**: `emdad-global`
- **Environment**: `Python`
- **Region**: اختر الأقرب لك
- **Branch**: `master`
- **Root Directory**: اتركه فارغاً

#### أوامر البناء والتشغيل:
- **Build Command**: 
  ```bash
  pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && mkdir -p uploads/news uploads/products uploads/gallery instance/uploads && python -c "from app import create_app; from app.models import db; import os; app = create_app('production'); app.app_context().push(); db.create_all(); print('Database initialized!')"
  ```

- **Start Command**:
  ```bash
  gunicorn app:app --config gunicorn.conf.py
  ```

#### الخطة:
- **Plan**: Free (أو Starter للأداء الأفضل)

### 4. إعداد قاعدة البيانات

1. في نفس الصفحة، اضغط على "Add Database"
2. اختر "PostgreSQL"
3. **Database Name**: `emdad-global-db`
4. **Plan**: Free
5. اضغط "Create Database"

### 5. متغيرات البيئة

سيتم تكوين هذه المتغيرات تلقائياً من ملف `render.yaml`:

```
FLASK_ENV=production
SECRET_KEY=[auto-generated]
DATABASE_URL=[auto-configured]
SITE_URL=https://emdad-global.onrender.com
COMPANY_NAME=Emdad Global
COMPANY_EMAIL=info@emdadglobal.com
COMPANY_PHONE=+20-xxx-xxx-xxxx
COMPANY_WHATSAPP=+20-xxx-xxx-xxxx
COMPANY_ADDRESS=Cairo, Egypt
SITE_NAME=Emdad Global - Egyptian Agricultural Exports
```

### 6. إعداد التخزين

سيتم إنشاء قرص للملفات المرفوعة تلقائياً:
- **Name**: `uploads`
- **Mount Path**: `/opt/render/project/src/uploads`
- **Size**: 1GB

### 7. النشر

1. اضغط "Create Web Service"
2. انتظر حتى يكتمل البناء (5-10 دقائق)
3. ستحصل على رابط مثل: `https://emdad-global.onrender.com`

## التحقق من النشر

### 1. فحص الصحة العامة

```bash
curl https://emdad-global.onrender.com
```

### 2. فحص صفحة الإدارة

```bash
curl https://emdad-global.onrender.com/admin/login
```

### 3. تشغيل فحص الصحة

```bash
python healthcheck.py
```

## بيانات الدخول الافتراضية

- **البريد الإلكتروني**: admin@emdadglobal.com
- **كلمة المرور**: admin123

**⚠️ مهم**: غيّر كلمة المرور فوراً بعد أول تسجيل دخول!

## استكشاف الأخطاء

### مشكلة في البناء

1. تحقق من سجلات البناء في Render Dashboard
2. تأكد من أن `requirements.txt` صحيح
3. تحقق من أن Python 3.11.7 مدعوم

### مشكلة في قاعدة البيانات

1. تحقق من أن PostgreSQL تم إنشاؤها
2. تأكد من أن `DATABASE_URL` مُعرّف
3. تحقق من سجلات التطبيق

### مشكلة في الملفات المرفوعة

1. تأكد من أن القرص مُعرّف في `render.yaml`
2. تحقق من أن المجلدات تم إنشاؤها
3. تأكد من الصلاحيات

## التحديثات

لتحديث التطبيق:

1. ادفع التغييرات إلى GitHub:
   ```bash
   git add .
   git commit -m "update: description of changes"
   git push origin master
   ```

2. سيتم إعادة النشر تلقائياً

## النسخ الاحتياطي

### قاعدة البيانات

```bash
# تصدير قاعدة البيانات
pg_dump $DATABASE_URL > backup.sql

# استيراد قاعدة البيانات
psql $DATABASE_URL < backup.sql
```

### الملفات المرفوعة

استخدم Render Dashboard لتحميل نسخة احتياطية من القرص.

## الأمان

1. **غيّر كلمة مرور الإدارة**
2. **استخدم HTTPS دائماً**
3. **راقب السجلات بانتظام**
4. **حدّث التبعيات دورياً**

## الدعم

للمساعدة:
- تحقق من [Render Documentation](https://render.com/docs)
- راجع سجلات التطبيق في Dashboard
- تواصل مع فريق الدعم

---

**نصيحة**: احتفظ بنسخة من هذا الدليل للرجوع إليه لاحقاً!
