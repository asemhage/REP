#!/bin/bash

# سكريبت النشر التجريبي للمنصة العقارية
# الاستخدام: ./scripts/deploy_staging.sh

set -e  # إيقاف عند أي خطأ

echo "🚀 بدء عملية النشر التجريبي..."

# التحقق من وجود Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

# التحقق من وجود Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose غير مثبت. يرجى تثبيته أولاً."
    exit 1
fi

# التحقق من وجود ملفات البيئة
if [ ! -f "config/.env.backend" ]; then
    echo "⚠️  ملف config/.env.backend غير موجود."
    echo "📝 إنشاء ملف من المثال..."
    cp config/backend.env.example config/.env.backend
    echo "⚠️  يرجى تعديل config/.env.backend قبل المتابعة!"
    exit 1
fi

if [ ! -f "config/.env.frontend" ]; then
    echo "⚠️  ملف config/.env.frontend غير موجود."
    echo "📝 إنشاء ملف من المثال..."
    cp config/frontend.env.example config/.env.frontend
    echo "⚠️  يرجى تعديل config/.env.frontend قبل المتابعة!"
    exit 1
fi

# الانتقال إلى مجلد infrastructure
cd infrastructure

# إيقاف الخدمات القديمة (إن وجدت)
echo "🛑 إيقاف الخدمات القديمة..."
docker compose -f docker-compose.staging.yml down 2>/dev/null || true

# بناء الصور
echo "🔨 بناء صور Docker..."
docker compose -f docker-compose.staging.yml build --no-cache

# تشغيل الخدمات
echo "▶️  تشغيل الخدمات..."
docker compose -f docker-compose.staging.yml up -d

# انتظار قاعدة البيانات
echo "⏳ انتظار قاعدة البيانات..."
sleep 10

# تشغيل الهجرات
echo "📊 تشغيل هجرات قاعدة البيانات..."
docker compose -f docker-compose.staging.yml exec -T backend python manage.py migrate

# جمع الملفات الثابتة
echo "📦 جمع الملفات الثابتة..."
docker compose -f docker-compose.staging.yml exec -T backend python manage.py collectstatic --noinput

# التحقق من حالة الخدمات
echo "✅ التحقق من حالة الخدمات..."
docker compose -f docker-compose.staging.yml ps

echo ""
echo "✅ اكتمل النشر!"
echo ""
echo "📍 الوصول إلى الخدمات:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/api/docs/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
echo "📝 لإنشاء مستخدم إداري:"
echo "   docker compose -f infrastructure/docker-compose.staging.yml exec backend python manage.py createsuperuser"
echo ""
echo "📋 لعرض السجلات:"
echo "   docker compose -f infrastructure/docker-compose.staging.yml logs -f"
echo ""

