#!/bin/bash

# سكريبت إعداد ملفات البيئة للنشر التجريبي
# الاستخدام: ./scripts/setup_env.sh

set -e  # إيقاف عند أي خطأ

echo "🔧 بدء إعداد ملفات البيئة..."

# الألوان
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# IP السيرفر الفعلي
SERVER_IP="102.213.180.235"

# محاولة الحصول على IP تلقائياً (إذا كان مختلفاً)
if command -v hostname &> /dev/null; then
    AUTO_IP=$(hostname -I | awk '{print $1}')
    if [ ! -z "$AUTO_IP" ] && [ "$AUTO_IP" != "$SERVER_IP" ]; then
        echo -e "${YELLOW}⚠️  IP المكتشف تلقائياً ($AUTO_IP) يختلف عن IP المحدد ($SERVER_IP)${NC}"
        read -p "هل تريد استخدام IP المكتشف تلقائياً؟ (y/n) [n]: " USE_AUTO
        if [ "$USE_AUTO" = "y" ] || [ "$USE_AUTO" = "Y" ]; then
            SERVER_IP=$AUTO_IP
        fi
    fi
fi

echo -e "${GREEN}📍 IP السيرفر: $SERVER_IP${NC}"

# إنشاء مجلد config إذا لم يكن موجوداً
mkdir -p config

# توليد SECRET_KEY
echo -e "${GREEN}🔐 توليد SECRET_KEY...${NC}"
if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 scripts/generate_secret_key.py --quiet 2>/dev/null || openssl rand -hex 32)
else
    SECRET_KEY=$(openssl rand -hex 32)
fi

# إعداد .env.backend
echo -e "${GREEN}📝 إنشاء config/.env.backend...${NC}"
cat > config/.env.backend << EOF
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
EOF

# إعداد .env.frontend
echo -e "${GREEN}📝 إنشاء config/.env.frontend...${NC}"
cat > config/.env.frontend << EOF
# API Configuration
NEXT_PUBLIC_API_URL=http://$SERVER_IP:8000

# Localization
NEXT_PUBLIC_APP_LOCALE=ar-LY
NEXT_PUBLIC_DEFAULT_CURRENCY=LYD
NEXT_PUBLIC_TIMEZONE=Africa/Tripoli
EOF

echo ""
echo -e "${GREEN}✅ تم إعداد ملفات البيئة بنجاح!${NC}"
echo ""
echo -e "${YELLOW}📋 الملفات المنشأة:${NC}"
echo "   - config/.env.backend"
echo "   - config/.env.frontend"
echo ""
echo -e "${YELLOW}⚠️  ملاحظات مهمة:${NC}"
echo "   1. تأكد من مراجعة الملفات قبل النشر"
echo "   2. IP السيرفر: $SERVER_IP"
echo "   3. كلمة مرور قاعدة البيانات: Asem_4011"
echo "   4. SECRET_KEY تم توليده تلقائياً"
echo ""
echo -e "${GREEN}🚀 جاهز للنشر!${NC}"

