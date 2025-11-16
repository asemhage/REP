export type Locale = 'ar' | 'en';

export type CurrencyCode = 'LYD' | 'USD' | 'EUR';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'admin' | 'investor' | 'tenant';
  phone_number: string;
  language: Locale;
  currency: CurrencyCode;
  timezone: string;
  is_identity_verified: boolean;
}

export interface PropertySummary {
  id: number;
  title: string;
  city: string;
  property_type: string;
  daily_rate: string | null;
  monthly_rate: string | null;
  status: string;
  media?: Array<{ id: number; file: string; is_primary: boolean }>;
  rating?: number;
}

export interface ApiError {
  detail?: string;
  [key: string]: unknown;
}

