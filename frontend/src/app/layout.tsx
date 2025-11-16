import './globals.css';
import type { Metadata } from 'next';
import { Noto_Kufi_Arabic } from 'next/font/google';

import { ReactQueryProvider } from '@/components/providers/react-query-provider';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';

const noto = Noto_Kufi_Arabic({
  subsets: ['arabic'],
  weight: ['400', '600', '700'],
  variable: '--font-arabic',
});

export const metadata: Metadata = {
  title: 'منصة الحجوزات الليبية',
  description: 'منصة متكاملة لحجوزات العقارات والصالات في ليبيا.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${noto.variable} min-h-screen bg-slate-50 font-sans`}>
        <ReactQueryProvider>
          <div className="flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
        </ReactQueryProvider>
      </body>
    </html>
  );
}

