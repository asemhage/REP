# سكريبت النشر التجريبي للمنصة العقارية (Windows PowerShell)
# الاستخدام: .\scripts\deploy_staging.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 بدء عملية النشر التجريبي..." -ForegroundColor Green

# التحقق من وجود Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker غير مثبت. يرجى تثبيته أولاً." -ForegroundColor Red
    exit 1
}

# التحقق من وجود Docker Compose
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose غير مثبت. يرجى تثبيته أولاً." -ForegroundColor Red
    exit 1
}

# التحقق من وجود ملفات البيئة
if (-not (Test-Path "config\.env.backend")) {
    Write-Host "⚠️  ملف config\.env.backend غير موجود." -ForegroundColor Yellow
    Write-Host "📝 إنشاء ملف من المثال..." -ForegroundColor Yellow
    Copy-Item "config\backend.env.example" "config\.env.backend"
    Write-Host "⚠️  يرجى تعديل config\.env.backend قبل المتابعة!" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path "config\.env.frontend")) {
    Write-Host "⚠️  ملف config\.env.frontend غير موجود." -ForegroundColor Yellow
    Write-Host "📝 إنشاء ملف من المثال..." -ForegroundColor Yellow
    Copy-Item "config\frontend.env.example" "config\.env.frontend"
    Write-Host "⚠️  يرجى تعديل config\.env.frontend قبل المتابعة!" -ForegroundColor Yellow
    exit 1
}

# الانتقال إلى مجلد infrastructure
Set-Location infrastructure

# إيقاف الخدمات القديمة (إن وجدت)
Write-Host "🛑 إيقاف الخدمات القديمة..." -ForegroundColor Yellow
docker compose -f docker-compose.staging.yml down 2>$null

# بناء الصور
Write-Host "🔨 بناء صور Docker..." -ForegroundColor Cyan
docker compose -f docker-compose.staging.yml build --no-cache

# تشغيل الخدمات
Write-Host "▶️  تشغيل الخدمات..." -ForegroundColor Cyan
docker compose -f docker-compose.staging.yml up -d

# انتظار قاعدة البيانات
Write-Host "⏳ انتظار قاعدة البيانات..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# تشغيل الهجرات
Write-Host "📊 تشغيل هجرات قاعدة البيانات..." -ForegroundColor Cyan
docker compose -f docker-compose.staging.yml exec -T backend python manage.py migrate

# جمع الملفات الثابتة
Write-Host "📦 جمع الملفات الثابتة..." -ForegroundColor Cyan
docker compose -f docker-compose.staging.yml exec -T backend python manage.py collectstatic --noinput

# التحقق من حالة الخدمات
Write-Host "✅ التحقق من حالة الخدمات..." -ForegroundColor Green
docker compose -f docker-compose.staging.yml ps

Write-Host ""
Write-Host "✅ اكتمل النشر!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 الوصول إلى الخدمات:" -ForegroundColor Cyan
Write-Host "   - Frontend: http://localhost:3000"
Write-Host "   - Backend API: http://localhost:8000"
Write-Host "   - API Docs: http://localhost:8000/api/docs/"
Write-Host "   - Admin: http://localhost:8000/admin/"
Write-Host ""
Write-Host "📝 لإنشاء مستخدم إداري:" -ForegroundColor Yellow
Write-Host "   docker compose -f infrastructure\docker-compose.staging.yml exec backend python manage.py createsuperuser"
Write-Host ""
Write-Host "📋 لعرض السجلات:" -ForegroundColor Yellow
Write-Host "   docker compose -f infrastructure\docker-compose.staging.yml logs -f"
Write-Host ""

Set-Location ..

