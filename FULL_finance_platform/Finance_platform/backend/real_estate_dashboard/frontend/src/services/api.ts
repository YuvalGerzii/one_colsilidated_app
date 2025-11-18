import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication if needed
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Property Management API calls
export const propertyManagementApi = {
  // Properties
  getProperties: () => api.get('/property-management/properties'),
  getProperty: (id: string) => api.get(`/property-management/properties/${id}`),
  createProperty: (data: any) => api.post('/property-management/properties', data),
  updateProperty: (id: string, data: any) => api.patch(`/property-management/properties/${id}`, data),
  deleteProperty: (id: string) => api.delete(`/property-management/properties/${id}`),

  // Units
  getUnits: (propertyId?: string) => api.get('/property-management/units', { params: { property_id: propertyId } }),
  getUnit: (id: string) => api.get(`/property-management/units/${id}`),
  createUnit: (data: any) => api.post('/property-management/units', data),
  updateUnit: (id: string, data: any) => api.patch(`/property-management/units/${id}`, data),

  // Leases
  getLeases: (propertyId?: string) => api.get('/property-management/leases', { params: { property_id: propertyId } }),
  getLease: (id: string) => api.get(`/property-management/leases/${id}`),
  createLease: (data: any) => api.post('/property-management/leases', data),
  updateLease: (id: string, data: any) => api.patch(`/property-management/leases/${id}`, data),
  getExpiringLeases: (days: number = 60) => api.get(`/property-management/leases/expiring?days=${days}`),

  // Maintenance
  getMaintenanceRequests: (propertyId?: string) =>
    api.get('/property-management/maintenance', { params: { property_id: propertyId } }),
  getMaintenanceRequest: (id: string) => api.get(`/property-management/maintenance/${id}`),
  createMaintenanceRequest: (data: any) => api.post('/property-management/maintenance', data),
  updateMaintenanceRequest: (id: string, data: any) =>
    api.patch(`/property-management/maintenance/${id}`, data),

  // Dashboard
  getDashboardSummary: () => api.get('/property-management/dashboard/summary'),
  getDashboardAlerts: () => api.get('/property-management/dashboard/alerts'),
  getPropertyOccupancy: (propertyId: string) =>
    api.get(`/property-management/properties/${propertyId}/occupancy`),
};

// Real Estate Tools API calls
export const realEstateToolsApi = {
  getModels: () => api.get('/real-estate/tools'),
  runModel: (modelSlug: string, values: any) =>
    api.post('/real-estate/tools/run', { model: modelSlug, values }),
};
