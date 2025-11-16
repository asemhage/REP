#!/bin/bash

# سكريبت النشر التلقائي على سيرفر Ubuntu
# الاستخدام: ./scripts/deploy_ubuntu.sh

set -e  # إيقاف عند أي خطأ

echo "🚀 بدء عملية النشر على Ubuntu..."

# الألوان للرسائل
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# التحقق من أن السكريبت يعمل كـ root أو sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  يرجى تشغيل السكريبت باستخدام sudo${NC}"
    exit 1
fi

# 1. تحديث النظام
echo -e "${GREEN}📦 تحديث النظام...${NC}"
apt update
apt upgrade -y

# 2. تثبيت المتطلبات الأساسية
echo -e "${GREEN}📦 تثبيت المتطلبات الأساسية...${NC}"
apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw

# 3. تثبيت Docker
echo -e "${GREEN}🐳 تثبيت Docker...${NC}"
if ! command -v docker &> /dev/null; then
    # إزالة إصدارات قديمة
    apt-get remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # إضافة مفتاح Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    
    # إضافة مستودع Docker
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # تثبيت Docker
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo -e "${YELLOW}Docker مثبت بالفعل${NC}"
fi

# 4. إعداد جدار الحماية
echo -e "${GREEN}🔥 إعداد جدار الحماية...${NC}"
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 5. استنساخ المشروع (إذا لم يكن موجوداً)
PROJECT_DIR="/opt/REP"
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${GREEN}📥 استنساخ المشروع...${NC}"
    git clone https://github.com/asemhage/REP.git $PROJECT_DIR
else
    echo -e "${YELLOW}المشروع موجود بالفعل في $PROJECT_DIR${NC}"
    cd $PROJECT_DIR
    git pull origin main || true
fi

cd $PROJECT_DIR

# 6. إعداد ملفات البيئة
echo -e "${GREEN}⚙️  إعداد ملفات البيئة...${NC}"
if [ ! -f "config/.env.backend" ]; then
    cp config/backend.env.example config/.env.backend
    echo -e "${YELLOW}⚠️  تم إنشاء config/.env.backend - يرجى تعديله!${NC}"
fi

if [ ! -f "config/.env.frontend" ]; then
    cp config/frontend.env.example config/.env.frontend
    echo -e "${YELLOW}⚠️  تم إنشاء config/.env.frontend - يرجى تعديله!${NC}"
fi

# 7. إنشاء SECRET_KEY إذا لم يكن موجوداً
if ! grep -q "SECRET_KEY=" config/.env.backend || grep -q "SECRET_KEY=replace-me" config/.env.backend; then
    SECRET_KEY=$(openssl rand -hex 32)
    if grep -q "SECRET_KEY=" config/.env.backend; then
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" config/.env.backend
    else
        echo "SECRET_KEY=$SECRET_KEY" >> config/.env.backend
    fi
    echo -e "${GREEN}✅ تم إنشاء SECRET_KEY تلقائياً${NC}"
fi

# 8. بناء وتشغيل الخدمات
echo -e "${GREEN}🔨 بناء صور Docker...${NC}"
cd infrastructure
docker compose -f docker-compose.staging.yml build

echo -e "${GREEN}▶️  تشغيل الخدمات...${NC}"
docker compose -f docker-compose.staging.yml up -d

# 9. انتظار قاعدة البيانات
echo -e "${YELLOW}⏳ انتظار قاعدة البيانات...${NC}"
sleep 15

# 10. تشغيل الهجرات
echo -e "${GREEN}📊 تشغيل هجرات قاعدة البيانات...${NC}"
docker compose -f docker-compose.staging.yml exec -T backend python manage.py migrate || true

# 11. جمع الملفات الثابتة
echo -e "${GREEN}📦 جمع الملفات الثابتة...${NC}"
docker compose -f docker-compose.staging.yml exec -T backend python manage.py collectstatic --noinput || true

# 12. التحقق من الحالة
echo -e "${GREEN}✅ التحقق من حالة الخدمات...${NC}"
docker compose -f docker-compose.staging.yml ps

echo ""
echo -e "${GREEN}✅ اكتمل النشر!${NC}"
echo ""
echo -e "${YELLOW}⚠️  خطوات مهمة:${NC}"
echo "   1. قم بتعديل config/.env.backend و config/.env.frontend"
echo "   2. تأكد من ALLOWED_HOSTS يحتوي على النطاق أو IP"
echo "   3. أنشئ مستخدم إداري:"
echo "      docker compose -f $PROJECT_DIR/infrastructure/docker-compose.staging.yml exec backend python manage.py createsuperuser"
echo ""
echo -e "${GREEN}📍 الوصول إلى الخدمات:${NC}"
echo "   - Frontend: http://$(hostname -I | awk '{print $1}'):3000"
echo "   - Backend API: http://$(hostname -I | awk '{print $1}'):8000"
echo "   - API Docs: http://$(hostname -I | awk '{print $1}'):8000/api/docs/"
echo ""
echo -e "${YELLOW}📋 لعرض السجلات:${NC}"
echo "   docker compose -f $PROJECT_DIR/infrastructure/docker-compose.staging.yml logs -f"
echo ""

