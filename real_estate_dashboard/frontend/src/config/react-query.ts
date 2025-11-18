/**
 * React Query Configuration
 *
 * Centralized configuration for React Query including:
 * - QueryClient setup with sensible defaults
 * - Custom error handling
 * - Retry logic
 * - Cache configuration
 */

import { QueryClient } from '@tanstack/react-query';

/**
 * Global error handler for React Query
 */
const onError = (error: unknown) => {
  console.error('[React Query Error]:', error);

  // You can add additional error handling here:
  // - Send to error tracking service (Sentry, etc.)
  // - Show toast notifications
  // - Log to analytics
};

/**
 * Create and configure QueryClient
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Stale time: 5 minutes
      // Data is considered fresh for 5 minutes before refetching
      staleTime: 5 * 60 * 1000,

      // Cache time: 10 minutes
      // Unused data will be garbage collected after 10 minutes
      gcTime: 10 * 60 * 1000,

      // Retry failed requests
      retry: (failureCount, error: any) => {
        // Don't retry on 4xx errors (client errors)
        if (error?.response?.status >= 400 && error?.response?.status < 500) {
          return false;
        }
        // Retry up to 2 times for other errors
        return failureCount < 2;
      },

      // Retry delay with exponential backoff
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),

      // Refetch on window focus (can be disabled per-query)
      refetchOnWindowFocus: false,

      // Refetch on reconnect
      refetchOnReconnect: true,

      // Refetch on mount if data is stale
      refetchOnMount: true,
    },
    mutations: {
      // Retry mutations once on network errors
      retry: (failureCount, error: any) => {
        // Only retry network errors
        if (error?.message?.includes('Network Error')) {
          return failureCount < 1;
        }
        return false;
      },

      // Error handling
      onError,
    },
  },
});

/**
 * Query keys factory for consistent key management
 *
 * Usage:
 *   queryKeys.properties.all
 *   queryKeys.properties.detail(id)
 *   queryKeys.properties.list(filters)
 */
export const queryKeys = {
  // Authentication
  auth: {
    user: ['auth', 'user'] as const,
  },

  // Property Management
  properties: {
    all: ['properties'] as const,
    lists: () => ['properties', 'list'] as const,
    list: (filters?: Record<string, any>) =>
      ['properties', 'list', filters] as const,
    details: () => ['properties', 'detail'] as const,
    detail: (id: string) => ['properties', 'detail', id] as const,
  },

  units: {
    all: ['units'] as const,
    lists: () => ['units', 'list'] as const,
    list: (propertyId?: string) =>
      ['units', 'list', { propertyId }] as const,
    details: () => ['units', 'detail'] as const,
    detail: (id: string) => ['units', 'detail', id] as const,
  },

  leases: {
    all: ['leases'] as const,
    lists: () => ['leases', 'list'] as const,
    list: (propertyId?: string) =>
      ['leases', 'list', { propertyId }] as const,
    expiring: (days: number) =>
      ['leases', 'expiring', days] as const,
    details: () => ['leases', 'detail'] as const,
    detail: (id: string) => ['leases', 'detail', id] as const,
  },

  maintenance: {
    all: ['maintenance'] as const,
    lists: () => ['maintenance', 'list'] as const,
    list: (propertyId?: string) =>
      ['maintenance', 'list', { propertyId }] as const,
    details: () => ['maintenance', 'detail'] as const,
    detail: (id: string) => ['maintenance', 'detail', id] as const,
  },

  // Integrations
  integrations: {
    all: ['integrations'] as const,
    status: () => ['integrations', 'status'] as const,
  },

  // Financial Models
  financialModels: {
    all: ['financial-models'] as const,
    dcf: {
      all: ['financial-models', 'dcf'] as const,
      lists: () => ['financial-models', 'dcf', 'list'] as const,
      list: (filters?: Record<string, any>) =>
        ['financial-models', 'dcf', 'list', filters] as const,
      details: () => ['financial-models', 'dcf', 'detail'] as const,
      detail: (id: string) =>
        ['financial-models', 'dcf', 'detail', id] as const,
    },
  },

  // Market Intelligence
  marketIntelligence: {
    all: ['market-intelligence'] as const,
    gentrification: (location?: string) =>
      ['market-intelligence', 'gentrification', { location }] as const,
    summary: () => ['market-intelligence', 'summary'] as const,
  },

  // Debt Management
  debtManagement: {
    all: ['debt-management'] as const,
    loans: {
      all: ['debt-management', 'loans'] as const,
      lists: () => ['debt-management', 'loans', 'list'] as const,
      list: (filters?: Record<string, any>) =>
        ['debt-management', 'loans', 'list', filters] as const,
    },
  },

  // Fund Management
  fundManagement: {
    all: ['fund-management'] as const,
    funds: {
      all: ['fund-management', 'funds'] as const,
      lists: () => ['fund-management', 'funds', 'list'] as const,
      list: (filters?: Record<string, any>) =>
        ['fund-management', 'funds', 'list', filters] as const,
    },
    lps: {
      all: ['fund-management', 'lps'] as const,
      lists: () => ['fund-management', 'lps', 'list'] as const,
    },
  },

  // Project Tracking
  projectTracking: {
    all: ['project-tracking'] as const,
    projects: {
      all: ['project-tracking', 'projects'] as const,
      lists: () => ['project-tracking', 'projects', 'list'] as const,
    },
    tasks: {
      all: ['project-tracking', 'tasks'] as const,
      lists: () => ['project-tracking', 'tasks', 'list'] as const,
    },
  },

  // Reports
  reports: {
    all: ['reports'] as const,
    deals: {
      all: ['reports', 'deals'] as const,
      lists: () => ['reports', 'deals', 'list'] as const,
    },
  },
};

/**
 * Helper to invalidate related queries
 *
 * Usage:
 *   await invalidateQueries(queryClient, 'properties')
 */
export const invalidateQueries = async (
  client: QueryClient,
  key: keyof typeof queryKeys
) => {
  const keyConfig = queryKeys[key] as any;
  if (keyConfig.all) {
    await client.invalidateQueries({ queryKey: keyConfig.all });
  } else {
    // For keys without 'all', invalidate using the key name
    await client.invalidateQueries({ queryKey: [key] });
  }
};
