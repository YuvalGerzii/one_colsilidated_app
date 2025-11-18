/**
 * Unified API Client with Automatic Company Filtering & Token Refresh
 *
 * This service provides a wrapper around axios that:
 * - Automatically injects company_id into requests
 * - Handles authentication with token refresh on 401
 * - Supports dev mode bypass for local development
 * - Provides consistent error handling
 *
 * Usage:
 *   import { apiClient } from '@/services/apiClient';
 *   const data = await apiClient.get('/financial-models/dcf');
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios';

// Possible backend ports to try (in order of preference)
const BACKEND_PORTS = [8001, 8000, 8002, 3001];
const API_SUFFIX = '/api/v1';

// Check if running in development mode
const isDevelopment = import.meta.env.DEV || window.location.hostname === 'localhost';

/**
 * Auto-detect which port the backend is running on
 */
let detectedBackendUrl: string | null = null;
const detectBackendPort = async (): Promise<string> => {
  // If already detected, use cached value
  if (detectedBackendUrl) {
    return detectedBackendUrl;
  }

  // If explicitly configured via env var, use that
  if (import.meta.env.VITE_API_BASE_URL) {
    detectedBackendUrl = import.meta.env.VITE_API_BASE_URL;
    console.log(`[API Client] Using configured backend: ${detectedBackendUrl}`);
    return detectedBackendUrl;
  }

  console.log('[API Client] Auto-detecting backend port...');

  // Try each port to find a responding backend
  for (const port of BACKEND_PORTS) {
    const testUrl = `http://localhost:${port}`;
    try {
      const response = await axios.get(`${testUrl}/health`, {
        timeout: 2000,
        validateStatus: () => true // Accept any status code
      });
      if (response.status === 200 || response.status === 404) {
        // 200 = health endpoint exists
        // 404 = server responding but no health endpoint (still valid)
        detectedBackendUrl = `${testUrl}${API_SUFFIX}`;
        console.log(`[API Client] ✅ Backend detected on port ${port}: ${detectedBackendUrl}`);
        return detectedBackendUrl;
      }
    } catch (error) {
      // This port didn't work, try next one
      continue;
    }
  }

  // No backend found, use default and warn
  const fallbackUrl = `http://localhost:8001${API_SUFFIX}`;
  console.warn(`[API Client] ⚠️ Could not detect backend on any port. Using fallback: ${fallbackUrl}`);
  detectedBackendUrl = fallbackUrl;
  return fallbackUrl;
};

// Initialize with a default, will be updated by detectBackendPort
let API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

/**
 * Get the selected company ID from localStorage
 */
const getSelectedCompanyId = (): string | null => {
  try {
    const selectedCompanyStr = localStorage.getItem('selectedCompany');
    if (selectedCompanyStr) {
      const company = JSON.parse(selectedCompanyStr);
      return company?.id || null;
    }
  } catch (error) {
    console.error('Failed to get selected company:', error);
  }
  return null;
};

/**
 * Get auth token from localStorage
 */
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

/**
 * Create axios instance with base configuration
 */
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Start auto-detection in background
detectBackendPort().then(url => {
  API_BASE_URL = url;
  // Update axios instance baseURL
  axiosInstance.defaults.baseURL = url;
  console.log('[API Client] Backend URL set to:', url);
}).catch(err => {
  console.error('[API Client] Backend detection failed:', err);
});

console.log('[API Client] Module initialized with baseURL:', API_BASE_URL);

/**
 * Request interceptor: Add auth token and company_id to all requests
 */
axiosInstance.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = getAuthToken();
    if (token && token !== 'dev-access-token') {
      // Only add real tokens to API requests
      // Dev tokens are just placeholders and shouldn't be sent
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Add company_id to params for GET requests or data for POST/PUT/PATCH
    const companyId = getSelectedCompanyId();
    if (companyId) {
      // For GET/DELETE requests, add to params
      if (config.method === 'get' || config.method === 'delete') {
        config.params = {
          ...config.params,
          company_id: companyId,
        };
      }
      // For POST/PUT/PATCH requests, can optionally add to body if needed
      // (Note: Backend handles company filtering via auth dependency, so this is optional)
    }

    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor: Handle errors globally with token refresh
 */
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // Handle 401 Unauthorized with token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // In dev mode, don't redirect or clear auth
      if (isDevelopment) {
        console.log('[DEV MODE] 401 response ignored');
        return Promise.reject(error);
      }

      try {
        // Try to refresh the token
        const { authService } = await import('./authService');
        await authService.refreshToken();

        // Retry the original request with new token
        const token = authService.getAccessToken();
        if (token && originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${token}`;
        }
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // Refresh failed, clear auth and redirect
        const { authService } = await import('./authService');
        authService.clearAuth();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Handle 403 Forbidden
    if (error.response?.status === 403) {
      console.error('Access forbidden:', error.response.data);
    }

    // Handle 404 Not Found
    if (error.response?.status === 404) {
      console.error('Resource not found:', error.response.data);
    }

    // Handle 500 Server Error
    if (error.response?.status === 500) {
      console.error('Server error:', error.response.data);
    }

    return Promise.reject(error);
  }
);

/**
 * Centralized API client with typed methods
 */
export const apiClient = {
  /**
   * GET request
   */
  get: async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.get<T>(url, config);
    return response.data;
  },

  /**
   * POST request
   */
  post: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.post<T>(url, data, config);
    return response.data;
  },

  /**
   * PUT request
   */
  put: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.put<T>(url, data, config);
    return response.data;
  },

  /**
   * PATCH request
   */
  patch: async <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.patch<T>(url, data, config);
    return response.data;
  },

  /**
   * DELETE request
   */
  delete: async <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.delete<T>(url, config);
    return response.data;
  },

  /**
   * Get the raw axios instance for advanced use cases
   */
  instance: axiosInstance,
};

/**
 * Example usage:
 *
 * // GET request
 * const dcfModels = await apiClient.get('/financial-models/dcf');
 *
 * // POST request
 * const newModel = await apiClient.post('/financial-models/dcf', {
 *   name: 'My DCF Model',
 *   ticker: 'AAPL',
 * });
 *
 * // PUT request
 * const updatedModel = await apiClient.put(`/financial-models/dcf/${id}`, {
 *   name: 'Updated Name',
 * });
 *
 * // DELETE request
 * await apiClient.delete(`/financial-models/dcf/${id}`);
 */

// ============================================================================
// BACKWARD COMPATIBILITY: Legacy API exports
// ============================================================================

/**
 * Property Management API calls (backward compatible)
 * @deprecated Use apiClient directly instead
 */
export const propertyManagementApi = {
  // Properties
  getProperties: () => axiosInstance.get('/property-management/properties'),
  getProperty: (id: string) => axiosInstance.get(`/property-management/properties/${id}`),
  createProperty: (data: any) => axiosInstance.post('/property-management/properties', data),
  updateProperty: (id: string, data: any) => axiosInstance.patch(`/property-management/properties/${id}`, data),
  deleteProperty: (id: string) => axiosInstance.delete(`/property-management/properties/${id}`),

  // Units
  getUnits: (propertyId?: string) => axiosInstance.get('/property-management/units', { params: { property_id: propertyId } }),
  getUnit: (id: string) => axiosInstance.get(`/property-management/units/${id}`),
  createUnit: (data: any) => axiosInstance.post('/property-management/units', data),
  updateUnit: (id: string, data: any) => axiosInstance.patch(`/property-management/units/${id}`, data),

  // Leases
  getLeases: (propertyId?: string) => axiosInstance.get('/property-management/leases', { params: { property_id: propertyId } }),
  getLease: (id: string) => axiosInstance.get(`/property-management/leases/${id}`),
  createLease: (data: any) => axiosInstance.post('/property-management/leases', data),
  updateLease: (id: string, data: any) => axiosInstance.patch(`/property-management/leases/${id}`, data),
  getExpiringLeases: (days: number = 60) => axiosInstance.get(`/property-management/leases/expiring?days=${days}`),

  // Maintenance
  getMaintenanceRequests: (propertyId?: string) =>
    axiosInstance.get('/property-management/maintenance', { params: { property_id: propertyId } }),
  getMaintenanceRequest: (id: string) => axiosInstance.get(`/property-management/maintenance/${id}`),
  createMaintenanceRequest: (data: any) => axiosInstance.post('/property-management/maintenance', data),
  updateMaintenanceRequest: (id: string, data: any) =>
    axiosInstance.patch(`/property-management/maintenance/${id}`, data),

  // Dashboard
  getDashboardSummary: () => axiosInstance.get('/property-management/dashboard/summary'),
  getDashboardAlerts: () => axiosInstance.get('/property-management/dashboard/alerts'),
  getPropertyOccupancy: (propertyId: string) =>
    axiosInstance.get(`/property-management/properties/${propertyId}/occupancy`),
};

/**
 * Real Estate Tools API calls (backward compatible)
 * @deprecated Use apiClient directly instead
 */
export const realEstateToolsApi = {
  getModels: () => axiosInstance.get('/real-estate/tools'),
  runModel: (modelSlug: string, values: any) =>
    axiosInstance.post('/real-estate/tools/run', { model: modelSlug, values }),
};

/**
 * Export API base URL for backward compatibility
 */
export { API_BASE_URL };

/**
 * Raw axios instance for advanced use cases
 * @deprecated Use apiClient.instance instead
 */
export const api = axiosInstance;

export default apiClient;
