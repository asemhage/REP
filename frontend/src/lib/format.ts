import { CurrencyCode } from '@/types';

export const formatCurrency = (value: number, currency: CurrencyCode = 'LYD', locale = 'ar-LY') => {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
  }).format(value);
};

export const formatDate = (value: string | Date, locale = 'ar-LY', timeZone = 'Africa/Tripoli') => {
  const date = typeof value === 'string' ? new Date(value) : value;
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone,
  }).format(date);
};

