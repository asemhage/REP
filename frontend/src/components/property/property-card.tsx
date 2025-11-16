import Image from 'next/image';
import Link from 'next/link';

import { PropertySummary } from '@/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { formatCurrency } from '@/lib/format';

interface PropertyCardProps {
  property: PropertySummary;
}

export const PropertyCard = ({ property }: PropertyCardProps) => {
  const mediaItems = property.media ?? [];
  const primaryImage = mediaItems.find((media) => media.is_primary) ?? mediaItems[0];

  return (
    <Card>
      {primaryImage ? (
        <div className="relative h-48 w-full overflow-hidden rounded-t-xl">
          <Image
            src={primaryImage.file}
            alt={property.title}
            fill
            className="object-cover transition-transform hover:scale-105"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 33vw, 400px"
          />
        </div>
      ) : (
        <div className="flex h-48 items-center justify-center rounded-t-xl bg-slate-100 text-slate-500">
          صورة غير متوفرة
        </div>
      )}
      <CardHeader>
        <CardTitle className="flex items-center justify-between text-lg">
          <span>{property.title}</span>
          {property.daily_rate && (
            <span className="text-sm text-blue-600">
              {formatCurrency(Number(property.daily_rate))}/اليوم
            </span>
          )}
        </CardTitle>
        <p className="text-sm text-gray-500">
          {property.city} • {property.property_type}
        </p>
      </CardHeader>
      <CardContent className="flex items-center justify-between text-sm text-gray-600">
        <span className="rounded-full bg-green-50 px-3 py-1 text-green-700">{property.status}</span>
        <Link href={`/properties/${property.id}`} className="text-blue-600 hover:text-blue-700">
          التفاصيل
        </Link>
      </CardContent>
    </Card>
  );
};

