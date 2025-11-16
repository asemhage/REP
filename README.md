# منصة الحجوزات العقارية الليبية

منصة متكاملة لإدارة حجوزات العقارات اليومية والشهرية والصالات في ليبيا.

## 🏗️ البنية التقنية

- **Backend:** Django REST Framework (Python)
- **Frontend:** Next.js (React + TypeScript)
- **Mobile:** Flutter (Dart)
- **Database:** PostgreSQL
- **Cache/Queue:** Redis + Celery
- **Containerization:** Docker Compose

## 📋 الميزات الرئيسية

### للمستثمرين
- إدارة العقارات والصالات
- تتبع الحجوزات والإيرادات
- إدارة العربون والمدفوعات
- تقارير مالية

### للمستأجرين
- تصفح العقارات المتاحة
- طلب الحجز مع العربون
- متابعة حالة الحجز
- تأكيد الدخول/الخروج

### للمدراء
- لوحة تحكم إدارية
- إدارة المستخدمين والصلاحيات
- مراقبة المعاملات والأمان

## 🚀 البدء السريع

### المتطلبات الأساسية
- Python 3.11+
- Node.js 18+
- Flutter 3.38+
- Docker & Docker Compose

### الإعداد

#### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Mobile
```bash
cd mobile
flutter pub get
flutter run -d windows  # أو المحاكي
```

#### Docker (البيئة الكاملة)
```bash
docker-compose -f infrastructure/docker-compose.yml up
```

## 🚀 النشر التجريبي

للنشر على بيئة تجريبية (Staging) للاختبار:

### النشر السريع:
```bash
# Windows
.\scripts\deploy_staging.ps1

# Linux/Mac
./scripts/deploy_staging.sh
```

### دليل النشر الكامل:
- [دليل النشر السريع - جاهز للاستخدام](docs/deployment/DEPLOY_NOW.md) 🚀 **للنشر الفوري على Ubuntu**
- [دليل النشر السريع - IP فقط](docs/deployment/QUICK_START_IP.md) ⚡ **للاختبار السريع**
- [دليل النشر السريع](docs/deployment/QUICK_START.md)
- [دليل النشر على Ubuntu](docs/deployment/ubuntu_deployment.md) ⭐
- [دليل النشر التفصيلي](docs/deployment/staging_deployment.md)

### الخيارات المتاحة:
- ✅ النشر المحلي (Docker Compose)
- ✅ VPS (Ubuntu/Debian)
- ✅ Render.com (مجاني)
- ✅ Railway.app
- ✅ DigitalOcean App Platform

## 🔒 الأمان

- JWT Authentication
- CSRF Protection
- Rate Limiting
- Input Validation
- Role-Based Access Control (RBAC)

## 📝 الوثائق

- [API Documentation](docs/core/api_endpoints.md)
- [Development Phases](real_estate_platform_docs/docs/core/2025-11-12_development_phases.md)
- [Architecture Decisions](real_estate_platform_docs/docs/core/architecture_decisions.yaml)

## 🧪 الاختبارات

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests (عند الإعداد)
cd frontend
npm test

# Mobile tests (عند الإعداد)
cd mobile
flutter test
```

## 📦 البنية

```
.
├── backend/          # Django REST API
├── frontend/         # Next.js Web App
├── mobile/           # Flutter Mobile App
├── infrastructure/   # Docker Compose configs
├── config/           # Environment & config files
├── docs/             # General documentation
└── real_estate_platform_docs/  # Project-specific docs
```

## 🌍 التوطين

- اللغة: العربية (RTL) / الإنجليزية
- العملة: الدينار الليبي (LYD)
- التوقيت: UTC+2 (ليبا)

## 📄 الترخيص

[حدد الترخيص هنا]

## 👥 المساهمون

[قائمة المساهمين]

