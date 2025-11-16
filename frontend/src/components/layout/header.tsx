'use client';

import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';

import { fetchMe } from '@/lib/api';
import { Button } from '@/components/ui/button';

const navItems = [
  { href: '/', label: 'الرئيسية' },
  { href: '/properties', label: 'العقارات' },
  { href: '/halls', label: 'صالات المناسبات' },
  { href: '/investor', label: 'لوحة المستثمر' },
];

export const Header = () => {
  const router = useRouter();
  const pathname = usePathname();
  const { data: user } = useQuery({
    queryKey: ['me'],
    queryFn: fetchMe,
    retry: false,
  });

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-2xl font-bold text-blue-700">
          منصة الحجوزات الليبية
        </Link>

        <nav className="hidden gap-6 text-sm font-medium text-gray-700 md:flex">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={item.href === pathname ? 'text-blue-600' : 'hover:text-blue-600'}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          {user ? (
            <span className="text-sm text-gray-700">مرحباً، {user.first_name || user.username}</span>
          ) : (
            <Button variant="secondary" onClick={() => router.push('/auth/login')}>
              تسجيل الدخول
            </Button>
          )}
          <Button onClick={() => router.push('/properties')}>ابدأ بالحجز</Button>
        </div>
      </div>
    </header>
  );
};

