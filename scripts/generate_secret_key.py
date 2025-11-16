#!/usr/bin/env python3
"""
سكريبت توليد SECRET_KEY للمنصة العقارية

الاستخدام:
    python scripts/generate_secret_key.py
    python scripts/generate_secret_key.py --add-to-env
    python scripts/generate_secret_key.py --env-file config/.env.backend
"""

import secrets
import argparse
import os
import sys


def generate_secret_key(length=32):
    """
    توليد SECRET_KEY عشوائي آمن
    
    Args:
        length: طول المفتاح بالبايت (الافتراضي: 32)
    
    Returns:
        str: SECRET_KEY بصيغة hexadecimal
    """
    return secrets.token_hex(length)


def add_to_env_file(secret_key, env_file):
    """
    إضافة SECRET_KEY إلى ملف البيئة
    
    Args:
        secret_key: المفتاح المراد إضافته
        env_file: مسار ملف البيئة
    """
    env_file = os.path.abspath(env_file)
    
    # التحقق من وجود الملف
    if not os.path.exists(env_file):
        print(f"⚠️  الملف {env_file} غير موجود. سيتم إنشاؤه.")
        os.makedirs(os.path.dirname(env_file), exist_ok=True)
    
    # قراءة الملف الحالي
    lines = []
    secret_key_exists = False
    
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # التحقق من وجود SECRET_KEY
        for i, line in enumerate(lines):
            if line.strip().startswith('SECRET_KEY='):
                secret_key_exists = True
                # تحديث السطر الموجود
                lines[i] = f'SECRET_KEY={secret_key}\n'
                break
    
    # إضافة SECRET_KEY إذا لم يكن موجوداً
    if not secret_key_exists:
        lines.append(f'SECRET_KEY={secret_key}\n')
    
    # كتابة الملف
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"✅ تم إضافة SECRET_KEY إلى {env_file}")


def main():
    parser = argparse.ArgumentParser(
        description='توليد SECRET_KEY آمن للمنصة العقارية',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  # توليد SECRET_KEY فقط
  python scripts/generate_secret_key.py
  
  # توليد وإضافة إلى ملف البيئة الافتراضي
  python scripts/generate_secret_key.py --add-to-env
  
  # توليد وإضافة إلى ملف محدد
  python scripts/generate_secret_key.py --env-file config/.env.backend
  
  # توليد مفتاح بطول مختلف
  python scripts/generate_secret_key.py --length 64
        """
    )
    
    parser.add_argument(
        '--length',
        type=int,
        default=32,
        help='طول المفتاح بالبايت (الافتراضي: 32)'
    )
    
    parser.add_argument(
        '--add-to-env',
        action='store_true',
        help='إضافة SECRET_KEY إلى ملف البيئة الافتراضي (config/.env.backend)'
    )
    
    parser.add_argument(
        '--env-file',
        type=str,
        default='config/.env.backend',
        help='مسار ملف البيئة (الافتراضي: config/.env.backend)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='عرض المفتاح فقط بدون رسائل إضافية'
    )
    
    args = parser.parse_args()
    
    # توليد SECRET_KEY
    secret_key = generate_secret_key(args.length)
    
    # عرض المفتاح
    if not args.quiet:
        print("🔐 SECRET_KEY المولد:")
        print("-" * 64)
    
    print(secret_key)
    
    if not args.quiet:
        print("-" * 64)
        print(f"📏 الطول: {len(secret_key)} حرف ({args.length} بايت)")
    
    # إضافة إلى ملف البيئة إذا طُلب
    if args.add_to_env or args.env_file != 'config/.env.backend':
        try:
            add_to_env_file(secret_key, args.env_file)
        except Exception as e:
            print(f"❌ خطأ في إضافة SECRET_KEY إلى الملف: {e}", file=sys.stderr)
            sys.exit(1)
    
    if not args.quiet:
        print("\n💡 نصيحة: احفظ هذا المفتاح في مكان آمن ولا تشاركه مع أحد!")
        print("💡 نصيحة: استخدم SECRET_KEY مختلف لكل بيئة (تطوير، اختبار، إنتاج)")


if __name__ == '__main__':
    main()

