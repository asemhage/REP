import Link from 'next/link';
import { HydrationBoundary, dehydrate, QueryClient } from '@tanstack/react-query';

import { fetchFeaturedProperties } from '@/lib/api';
import { PropertySummary } from '@/types';
import { PropertyCard } from '@/components/property/property-card';
import { HomeHero } from '@/components/sections/home-hero';

async function loadFeaturedProperties() {
  try {
    return await fetchFeaturedProperties();
  } catch (error) {
    console.error('Failed to fetch featured properties', error);
    return [];
  }
}

export default async function HomePage() {
  const featured = await loadFeaturedProperties();
  const queryClient = new QueryClient();
  queryClient.setQueryData<PropertySummary[]>(['featured-properties'], featured);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <div className="space-y-16 pb-16">
        <HomeHero />
        <section className="mx-auto max-w-7xl px-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">عقارات مميزة</h2>
            <Link href="/properties" className="text-blue-600 hover:text-blue-700">
              عرض جميع العقارات
            </Link>
          </div>
          <PropertyGrid initialData={featured} />
        </section>
      </div>
    </HydrationBoundary>
  );
}

const PropertyGrid = ({ initialData }: { initialData: PropertySummary[] }) => (
  <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
    {initialData.map((property) => (
      <PropertyCard key={property.id} property={property} />
    ))}
    {initialData.length === 0 && <p className="text-gray-500">لا توجد عقارات متاحة حالياً.</p>}
  </div>
);
