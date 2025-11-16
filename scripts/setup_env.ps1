# سكريبت إعداد ملفات البيئة للنشر التجريبي (PowerShell)
# الاستخدام: .\scripts\setup_env.ps1

Write-Host "🔧 بدء إعداد ملفات البيئة..." -ForegroundColor Green

# الحصول على IP السيرفر
$SERVER_IP = $null
try {
    $SERVER_IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -ne "127.0.0.1" } | Select-Object -First 1).IPAddress
} catch {
    Write-Host "⚠️  لم يتم العثور على IP السيرفر تلقائياً" -ForegroundColor Yellow
    $SERVER_IP = Read-Host "يرجى إدخال IP السيرفر"
}

if ([string]::IsNullOrEmpty($SERVER_IP)) {
    Write-Host "❌ خطأ: يجب إدخال IP السيرفر" -ForegroundColor Red
    exit 1
}

Write-Host "📍 IP السيرفر: $SERVER_IP" -ForegroundColor Green

# إنشاء مجلد config إذا لم يكن موجوداً
if (-not (Test-Path "config")) {
    New-Item -ItemType Directory -Path "config" | Out-Null
}

# توليد SECRET_KEY
Write-Host "🔐 توليد SECRET_KEY..." -ForegroundColor Green
$SECRET_KEY = $null

# محاولة استخدام Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    try {
        $SECRET_KEY = python scripts/generate_secret_key.py --quiet 2>$null
    } catch {
        # إذا فشل، استخدم OpenSSL
    }
}

# إذا لم يتم توليد SECRET_KEY، استخدم OpenSSL أو PowerShell
if ([string]::IsNullOrEmpty($SECRET_KEY)) {
    if (Get-Command openssl -ErrorAction SilentlyContinue) {
        $SECRET_KEY = openssl rand -hex 32
    } else {
        # توليد باستخدام PowerShell
        $bytes = New-Object byte[] 32
        [System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
        $SECRET_KEY = ($bytes | ForEach-Object { $_.ToString("x2") }) -join ""
    }
}

# إعداد .env.backend
Write-Host "📝 إنشاء config/.env.backend..." -ForegroundColor Green
$backendContent = @"
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings
SECRET_KEY=$SECRET_KEY
DEBUG=0

# Hosts & Security
ALLOWED_HOSTS=$SERVER_IP,localhost,127.0.0.1

# Database
DATABASE_URL=postgres://realestate:Asem_4011@db:5432/realestate

# Redis
REDIS_URL=redis://redis:6379/0

# CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS=http://$SERVER_IP:3000,http://$SERVER_IP:8000

# CSRF (Cross-Site Request Forgery)
CSRF_TRUSTED_ORIGINS=http://$SERVER_IP,http://$SERVER_IP:3000,http://$SERVER_IP:8000

# Localization
DEFAULT_CURRENCY=LYD
TIME_ZONE=Africa/Tripoli
APP_LANGUAGE=ar
"@

$backendContent | Out-File -FilePath "config/.env.backend" -Encoding utf8 -NoNewline

# إعداد .env.frontend
Write-Host "📝 إنشاء config/.env.frontend..." -ForegroundColor Green
$frontendContent = @"
# API Configuration
NEXT_PUBLIC_API_URL=http://$SERVER_IP:8000

# Localization
NEXT_PUBLIC_APP_LOCALE=ar-LY
NEXT_PUBLIC_DEFAULT_CURRENCY=LYD
NEXT_PUBLIC_TIMEZONE=Africa/Tripoli
"@

$frontendContent | Out-File -FilePath "config/.env.frontend" -Encoding utf8 -NoNewline

Write-Host ""
Write-Host "✅ تم إعداد ملفات البيئة بنجاح!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 الملفات المنشأة:" -ForegroundColor Yellow
Write-Host "   - config/.env.backend"
Write-Host "   - config/.env.frontend"
Write-Host ""
Write-Host "⚠️  ملاحظات مهمة:" -ForegroundColor Yellow
Write-Host "   1. تأكد من مراجعة الملفات قبل النشر"
Write-Host "   2. IP السيرفر: $SERVER_IP"
Write-Host "   3. كلمة مرور قاعدة البيانات: Asem_4011"
Write-Host "   4. SECRET_KEY تم توليده تلقائياً"
Write-Host ""
Write-Host "🚀 جاهز للنشر!" -ForegroundColor Green

