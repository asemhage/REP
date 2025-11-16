import axios from 'axios';
import { PropertySummary, User } from '@/types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000/api/v1',
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
  }
  return config;
});

export const fetchMe = async (): Promise<User> => {
  const response = await api.get<User>('/accounts/users/me/');
  return response.data;
};

export const fetchFeaturedProperties = async (): Promise<PropertySummary[]> => {
  const response = await api.get<PropertySummary[]>('/listings/properties', {
    params: {
      status: 'available',
      limit: 6,
    },
  });
  return response.data;
};

export default api;

