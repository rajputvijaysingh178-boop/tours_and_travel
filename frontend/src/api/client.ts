import type { Cart } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export type ApiRecord = Record<string, any>;

async function request<T>(path: string, options: RequestInit = {}, tokenKey = 'access_token'): Promise<T> {
  const token = localStorage.getItem(tokenKey);
  const headers = new Headers(options.headers);
  if (!(options.body instanceof FormData)) headers.set('Content-Type', 'application/json');
  if (token) headers.set('Authorization', `Bearer ${token}`);

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    if (response.status === 401 && path !== '/auth/admin/login') {
      const adminSession = tokenKey === 'admin_access_token';
      localStorage.removeItem(adminSession ? 'admin_access_token' : 'access_token');
      if (!adminSession) localStorage.removeItem('refresh_token');
      window.dispatchEvent(new CustomEvent('travelease:session-expired'));
      window.location.assign(adminSession ? '/admin/login?session_expired=1' : '/login?session_expired=1');
    }
    const message = typeof body?.detail === 'string' ? body.detail : 'Something went wrong. Please try again.';
    throw new Error(message);
  }
  return body as T;
}

const get = <T>(path: string) => request<T>(path);
const send = <T>(path: string, method: string, body?: unknown) => request<T>(path, { method, body: body ? JSON.stringify(body) : undefined });
const uniqueRecords = (items: ApiRecord[], field: string) => Array.from(new Map(items.map(item => [String(item[field] || item.id || item._id), item])).values());
const adminGet = <T>(path: string) => request<T>(path, {}, 'admin_access_token');
const adminSend = <T>(path: string, method: string, body?: unknown) => request<T>(path, { method, body: body === undefined ? undefined : JSON.stringify(body) }, 'admin_access_token');

export const api = {
  auth: {
    login: (body: ApiRecord) => send<ApiRecord>('/auth/login', 'POST', body),
    register: (body: ApiRecord) => send<ApiRecord>('/auth/register', 'POST', body),
  },
  admin: {
    login: (body: ApiRecord) => request<ApiRecord>('/auth/admin/login', { method: 'POST', body: JSON.stringify(body) }, 'admin_access_token'),
    session: () => adminGet<ApiRecord>('/admin/session'),
    overview: () => adminGet<ApiRecord>('/admin/overview'),
    records: (resource: string, search = '') => adminGet<ApiRecord[]>(`/admin/records/${resource}${search ? `?search=${encodeURIComponent(search)}` : ''}`),
    create: (resource: string, body: ApiRecord, hotelId?: string) => adminSend<ApiRecord>(resource === 'rooms' ? `/hotels/${hotelId}/rooms` : `/${resource}`, 'POST', body),
    update: (resource: string, id: string, body: ApiRecord) => {
      const path = resource === 'hotels' || resource === 'rooms'
        ? `/admin/${resource}/${id}`
        : `/${resource}/${id}`;
      return adminSend<ApiRecord>(path, resource === 'destinations' || resource === 'packages' || resource === 'activities' || resource === 'guides' || resource === 'vehicles' ? 'PUT' : 'PATCH', body);
    },
    uploadImage: (file: File) => {
      const body = new FormData();
      body.append('file', file);
      return request<ApiRecord>('/admin/images/upload', { method: 'POST', body }, 'admin_access_token');
    },
  },
  destinations: {
    list: () => get<ApiRecord[]>('/destinations').then(items => uniqueRecords(items, 'destination_id')),
    byId: (id: string) => get<ApiRecord>(`/destinations/${id}`),
  },
  packages: {
    list: () => get<ApiRecord[]>('/packages').then(items => uniqueRecords(items, 'package_id')),
    byId: (id: string) => get<ApiRecord>(`/packages/${id}`),
  },
  hotels: {
    list: (destinationId = localStorage.getItem('active_destination_id') || undefined) => get<ApiRecord[]>(destinationId ? `/hotels?destination_id=${destinationId}` : '/hotels').then(items => uniqueRecords(items, 'hotel_id')),
    rooms: (hotelId: string) => get<ApiRecord[]>(`/hotels/${hotelId}/availability`).then(items => uniqueRecords(items, 'room_id')),
  },
  activities: { list: (destinationId?: string) => get<ApiRecord[]>(destinationId ? `/activities?destination_id=${destinationId}` : '/activities').then(items => uniqueRecords(items, 'activity_id')) },
  guides: { list: (destinationId?: string) => get<ApiRecord[]>(destinationId ? `/guides?destination_id=${destinationId}` : '/guides').then(items => uniqueRecords(items, 'guide_id')) },
  vehicles: { list: (destinationId?: string) => get<ApiRecord[]>(destinationId ? `/vehicles?destination_id=${destinationId}` : '/vehicles').then(items => uniqueRecords(items, 'vehicle_id')) },
  carts: {
      create: async (body: ApiRecord) => {
        const cart = await send<Cart>('/trip-carts', 'POST', body);
        if (cart.destination_id) localStorage.setItem('active_destination_id', String(cart.destination_id));
        return cart;
      },
    get: (id: string) => get<Cart>(`/trip-carts/${id}`),
    selectHotel: (id: string, hotel_id: string) => send<Cart>(`/trip-carts/${id}/hotel`, 'PATCH', { hotel_id }),
    selectRoom: (id: string, room_id: string) => send<Cart>(`/trip-carts/${id}/room`, 'PATCH', { room_id }),
    selectActivities: (id: string, activity_ids: string[]) => send<Cart>(`/trip-carts/${id}/activities`, 'PATCH', { activity_ids }),
    selectGuide: (id: string, guide_id: string | null) => send<Cart>(`/trip-carts/${id}/guide`, 'PATCH', { guide_id }),
    selectVehicle: (id: string, vehicle_id: string | null) => send<Cart>(`/trip-carts/${id}/vehicle`, 'PATCH', { vehicle_id }),
    passengers: (id: string, passengers: ApiRecord[]) => send<Cart>(`/trip-carts/${id}/passengers`, 'PUT', { passengers }),
    review: (id: string) => send<ApiRecord>(`/trip-carts/${id}/review`, 'POST', { confirmed: true }),
  },
  checkout: {
    lock: (id: string) => send<ApiRecord>(`/checkout/${id}/lock`, 'POST'),
    payment: (id: string) => send<ApiRecord>(`/checkout/${id}/payment`, 'POST'),
    verify: (id: string, body: ApiRecord) => send<ApiRecord>(`/checkout/${id}/verify`, 'POST', body),
  },
  bookings: {
    list: () => get<ApiRecord[]>('/bookings'),
    cancel: (id: string, body: ApiRecord) => send<ApiRecord>(`/bookings/${encodeURIComponent(id)}/cancel`, 'POST', body),
  },
};
