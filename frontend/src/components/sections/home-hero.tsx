import Link from 'next/link';
import { Button } from '@/components/ui/button';

export const HomeHero = () => (
  <section className="relative overflow-hidden bg-gradient-to-br from-blue-900 via-blue-800 to-blue-700 text-white">
    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.15),_rgba(0,0,0,0))] opacity-70" />
    <div className="relative mx-auto flex max-w-7xl flex-col gap-8 px-6 py-16 lg:flex-row lg:items-center">
      <div className="flex-1 space-y-6">
        <span className="rounded-full bg-white/10 px-4 py-1 text-sm font-medium">
          حجوزات آمنة وسريعة في جميع مدن ليبيا
        </span>
        <h1 className="text-4xl font-bold leading-tight lg:text-5xl">
          اكتشف أفضل العقارات وصالات المناسبات لحجوزاتك اليومية والشهرية
        </h1>
        <p className="text-lg text-blue-100">
          منصة متكاملة للمستأجرين والمستثمرين مع دعم العربون النقدي والبطاقات المحلية، وتقارير أداء فورية.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link href="/properties">
            <Button size="lg">استعرض العقارات</Button>
          </Link>
          <Link href="/investor/signup">
            <Button size="lg" variant="secondary" className="bg-white text-blue-800 hover:bg-blue-50">
              انضم كمستثمر
            </Button>
          </Link>
        </div>
        <div className="flex flex-wrap gap-6 text-sm text-blue-100">
          <FeatureItem label="إدارة العربون النقدي والإلكتروني" />
          <FeatureItem label="لوحة تحكم للمستثمرين بالتقارير المالية" />
          <FeatureItem label="رسائل صوتية ومتابعة فورية للحجوزات" />
        </div>
      </div>
      <div className="flex-1">
        <div className="mx-auto max-w-lg rounded-3xl border border-white/20 bg-white/10 p-6 shadow-2xl backdrop-blur">
          <ul className="space-y-3 text-left text-sm text-blue-100">
            <li>• عرض التقويم بالأيام والفترات للصالة المختارة.</li>
            <li>• قبول أو رفض الحجز مع استعراض الرسائل الصوتية.</li>
            <li>• تتبع العربون وإشعارات الدخول والخروج في الوقت الفعلي.</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
);

const FeatureItem = ({ label }: { label: string }) => (
  <div className="flex items-center gap-2">
    <span className="h-2 w-2 rounded-full bg-emerald-400" />
    <span>{label}</span>
  </div>
);

