/**
 * React Query Hooks for Integrations
 *
 * Custom hooks for fetching integration status and testing connections
 * with automatic caching and error handling.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient';
import { queryKeys } from '../config/react-query';

// Types
interface Integration {
  name: string;
  category: string;
  status: string;
  is_free: boolean;
  available: boolean;
}

interface IntegrationStatus {
  integrations: Record<string, Integration>;
  total_count: number;
  active_count: number;
  inactive_count: number;
  error_count: number;
  categories: Record<string, number>;
}

interface TestConnectionResponse {
  integration: string;
  status: string;
  message: string;
  response_time_ms: number;
  data?: any;
}

// ============================================================================
// Query Hooks
// ============================================================================

/**
 * Fetch integrations status
 *
 * Usage:
 *   const { data: status, isLoading, error, refetch } = useIntegrationsStatus();
 */
export const useIntegrationsStatus = () => {
  return useQuery({
    queryKey: queryKeys.integrations.status(),
    queryFn: async () => {
      const response = await apiClient.instance.get('/integrations/status');
      return response.data as IntegrationStatus;
    },
    staleTime: 2 * 60 * 1000, // 2 minutes - integrations status doesn't change often
    retry: 2, // Retry twice on failure
  });
};

// ============================================================================
// Mutation Hooks
// ============================================================================

/**
 * Test integration connection
 *
 * Usage:
 *   const testConnection = useTestIntegration();
 *   testConnection.mutate('fred', {
 *     onSuccess: (result) => console.log('Test result:', result),
 *     onError: (error) => console.error('Test failed:', error),
 *   });
 */
export const useTestIntegration = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (integrationName: string) => {
      const response = await apiClient.instance.post('/integrations/test', {
        integration: integrationName,
      });
      return response.data as TestConnectionResponse;
    },
    onSuccess: () => {
      // Invalidate integrations status to get updated data
      queryClient.invalidateQueries({ queryKey: queryKeys.integrations.status() });
    },
  });
};

/**
 * Refresh all integrations status
 *
 * Usage:
 *   const refreshIntegrations = useRefreshIntegrations();
 *   refreshIntegrations.mutate();
 */
export const useRefreshIntegrations = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      // Invalidate and refetch
      await queryClient.invalidateQueries({ queryKey: queryKeys.integrations.all });
      const response = await apiClient.instance.get('/integrations/status');
      return response.data as IntegrationStatus;
    },
  });
};
