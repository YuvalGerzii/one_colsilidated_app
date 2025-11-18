/**
 * React Query Hooks for Property Management
 *
 * Custom hooks for fetching, creating, updating, and deleting properties
 * with automatic caching, refetching, and error handling.
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient';
import { queryKeys } from '../config/react-query';

// Types
interface Property {
  id: string;
  name: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  property_type: string;
  units: number;
  total_sqft?: number;
  year_built?: number;
  purchase_price?: number;
  current_value?: number;
}

// ============================================================================
// Query Hooks
// ============================================================================

/**
 * Fetch all properties
 *
 * Usage:
 *   const { data: properties, isLoading, error } = useProperties();
 */
export const useProperties = () => {
  return useQuery({
    queryKey: queryKeys.properties.lists(),
    queryFn: async () => {
      const response = await apiClient.instance.get('/property-management/properties');
      return response.data as Property[];
    },
  });
};

/**
 * Fetch a single property by ID
 *
 * Usage:
 *   const { data: property, isLoading } = useProperty(propertyId);
 */
export const useProperty = (id: string) => {
  return useQuery({
    queryKey: queryKeys.properties.detail(id),
    queryFn: async () => {
      const response = await apiClient.instance.get(`/property-management/properties/${id}`);
      return response.data as Property;
    },
    enabled: !!id, // Only run query if id is provided
  });
};

/**
 * Fetch property occupancy
 *
 * Usage:
 *   const { data: occupancy } = usePropertyOccupancy(propertyId);
 */
export const usePropertyOccupancy = (propertyId: string) => {
  return useQuery({
    queryKey: [...queryKeys.properties.detail(propertyId), 'occupancy'],
    queryFn: async () => {
      const response = await apiClient.instance.get(
        `/property-management/properties/${propertyId}/occupancy`
      );
      return response.data;
    },
    enabled: !!propertyId,
  });
};

// ============================================================================
// Mutation Hooks
// ============================================================================

/**
 * Create a new property
 *
 * Usage:
 *   const createProperty = useCreateProperty();
 *   createProperty.mutate(newPropertyData, {
 *     onSuccess: () => console.log('Created!'),
 *     onError: (error) => console.error(error),
 *   });
 */
export const useCreateProperty = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: Partial<Property>) => {
      const response = await apiClient.instance.post('/property-management/properties', data);
      return response.data as Property;
    },
    onSuccess: () => {
      // Invalidate properties list to trigger refetch
      queryClient.invalidateQueries({ queryKey: queryKeys.properties.lists() });
    },
  });
};

/**
 * Update an existing property
 *
 * Usage:
 *   const updateProperty = useUpdateProperty();
 *   updateProperty.mutate({ id: '123', data: updatedData });
 */
export const useUpdateProperty = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<Property> }) => {
      const response = await apiClient.instance.patch(
        `/property-management/properties/${id}`,
        data
      );
      return response.data as Property;
    },
    onSuccess: (_, variables) => {
      // Invalidate both the property detail and the properties list
      queryClient.invalidateQueries({ queryKey: queryKeys.properties.detail(variables.id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.properties.lists() });
    },
  });
};

/**
 * Delete a property
 *
 * Usage:
 *   const deleteProperty = useDeleteProperty();
 *   deleteProperty.mutate(propertyId);
 */
export const useDeleteProperty = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      await apiClient.instance.delete(`/property-management/properties/${id}`);
    },
    onSuccess: (_, id) => {
      // Remove from cache and refetch list
      queryClient.removeQueries({ queryKey: queryKeys.properties.detail(id) });
      queryClient.invalidateQueries({ queryKey: queryKeys.properties.lists() });
    },
  });
};
