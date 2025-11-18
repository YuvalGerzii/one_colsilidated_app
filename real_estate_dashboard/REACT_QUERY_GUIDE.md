# React Query Integration Guide

**Date:** 2025-11-11
**Status:** ✅ Implemented

---

## Overview

React Query has been integrated into the application to provide:
- **Automatic caching** - Reduce unnecessary API calls
- **Background refetching** - Keep data fresh automatically
- **Loading & error states** - Built-in state management
- **Request deduplication** - Multiple components can share the same query
- **Optimistic updates** - Update UI before server response
- **DevTools** - Visual debugging of queries and cache

---

## What's Been Added

### 1. React Query Setup ✅

**Files:**
- `/frontend/src/lib/react-query.ts` - QueryClient configuration & query keys
- `/frontend/src/App.tsx` - QueryClientProvider integration
- `/frontend/src/components/ErrorBoundary.tsx` - Global error handling

**Configuration:**
```typescript
// Stale time: 5 minutes (data is fresh)
// Cache time: 10 minutes (garbage collection)
// Auto-retry on network errors
// No refetch on window focus (can be enabled per-query)
```

### 2. Custom Hooks ✅

**Created:**
- `/frontend/src/hooks/useProperties.ts` - Property management queries/mutations
- `/frontend/src/hooks/useIntegrations.ts` - Integration status queries
- `/frontend/src/hooks/useMarketIntelligence.ts` - Market data queries

---

## Usage Examples

### Basic Query

**Before (manual state management):**
```typescript
const [properties, setProperties] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  const fetchProperties = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/property-management/properties');
      setProperties(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };
  fetchProperties();
}, []);
```

**After (with React Query):**
```typescript
import { useProperties } from '@/hooks/useProperties';

const { data: properties, isLoading, error } = useProperties();
```

**Benefits:**
- ✅ No manual state management
- ✅ Automatic caching (subsequent renders use cached data)
- ✅ Background refetching
- ✅ Request deduplication (multiple components share the same query)

---

### Query with Parameters

```typescript
import { useProperty } from '@/hooks/useProperties';

function PropertyDetail({ propertyId }: { propertyId: string }) {
  const { data: property, isLoading, error } = useProperty(propertyId);

  if (isLoading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error.message}</Alert>;

  return <div>{property.name}</div>;
}
```

---

### Mutations (Create/Update/Delete)

**Creating a property:**
```typescript
import { useCreateProperty } from '@/hooks/useProperties';

function AddPropertyForm() {
  const createProperty = useCreateProperty();

  const handleSubmit = (formData) => {
    createProperty.mutate(formData, {
      onSuccess: () => {
        console.log('Property created!');
        // Cache automatically invalidated - list refetches
      },
      onError: (error) => {
        console.error('Failed to create:', error);
      },
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <Button
        type="submit"
        disabled={createProperty.isPending}
      >
        {createProperty.isPending ? 'Creating...' : 'Create Property'}
      </Button>
    </form>
  );
}
```

**Updating a property:**
```typescript
import { useUpdateProperty } from '@/hooks/useProperties';

function EditPropertyForm({ propertyId, initialData }) {
  const updateProperty = useUpdateProperty();

  const handleSubmit = (formData) => {
    updateProperty.mutate(
      { id: propertyId, data: formData },
      {
        onSuccess: () => {
          console.log('Property updated!');
        },
      }
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <Button disabled={updateProperty.isPending}>
        Save Changes
      </Button>
    </form>
  );
}
```

**Deleting a property:**
```typescript
import { useDeleteProperty } from '@/hooks/useProperties';

function PropertyActions({ propertyId }) {
  const deleteProperty = useDeleteProperty();

  const handleDelete = () => {
    if (confirm('Are you sure?')) {
      deleteProperty.mutate(propertyId, {
        onSuccess: () => {
          console.log('Property deleted!');
        },
      });
    }
  };

  return (
    <Button
      onClick={handleDelete}
      disabled={deleteProperty.isPending}
    >
      Delete
    </Button>
  );
}
```

---

### Manual Refetching

```typescript
import { useProperties } from '@/hooks/useProperties';

function PropertiesList() {
  const { data: properties, isLoading, refetch } = useProperties();

  return (
    <div>
      <Button onClick={() => refetch()}>
        <RefreshIcon /> Refresh
      </Button>
      {/* List properties */}
    </div>
  );
}
```

---

### Loading & Error States

```typescript
import { useProperties } from '@/hooks/useProperties';

function PropertiesList() {
  const {
    data: properties,
    isLoading,
    isError,
    error,
    isFetching, // True when background refetching
  } = useProperties();

  if (isLoading) {
    return <CircularProgress />;
  }

  if (isError) {
    return (
      <Alert severity="error">
        Error loading properties: {error.message}
      </Alert>
    );
  }

  return (
    <div>
      {isFetching && <LinearProgress />}
      {properties.map(property => (
        <PropertyCard key={property.id} property={property} />
      ))}
    </div>
  );
}
```

---

### Optimistic Updates

Update UI immediately before server response:

```typescript
import { useUpdateProperty } from '@/hooks/useProperties';
import { useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/lib/react-query';

function PropertyName({ propertyId, initialName }) {
  const queryClient = useQueryClient();
  const updateProperty = useUpdateProperty();
  const [name, setName] = useState(initialName);

  const handleUpdate = () => {
    // Optimistically update UI
    queryClient.setQueryData(
      queryKeys.properties.detail(propertyId),
      (old: any) => ({ ...old, name })
    );

    // Send to server
    updateProperty.mutate(
      { id: propertyId, data: { name } },
      {
        onError: () => {
          // Revert on error
          setName(initialName);
        },
      }
    );
  };

  return (
    <TextField
      value={name}
      onChange={(e) => setName(e.target.value)}
      onBlur={handleUpdate}
    />
  );
}
```

---

## Available Hooks

### Property Management

```typescript
import {
  useProperties,      // Fetch all properties
  useProperty,        // Fetch single property
  usePropertyOccupancy, // Fetch occupancy data
  useCreateProperty,  // Create property
  useUpdateProperty,  // Update property
  useDeleteProperty,  // Delete property
} from '@/hooks/useProperties';
```

### Integrations

```typescript
import {
  useIntegrationsStatus, // Fetch integration status
  useTestIntegration,    // Test integration connection
  useRefreshIntegrations, // Refresh all integrations
} from '@/hooks/useIntegrations';
```

### Market Intelligence

```typescript
import {
  useGentrificationScore, // Fetch gentrification risk score
  useMarketSummary,       // Fetch market summary
  useMarketData,          // Fetch specific market indicator
} from '@/hooks/useMarketIntelligence';
```

---

## Creating New Hooks

### Step 1: Define Query Key

Add to `/frontend/src/lib/react-query.ts`:

```typescript
export const queryKeys = {
  // ... existing keys

  yourFeature: {
    all: ['your-feature'] as const,
    lists: () => [...queryKeys.yourFeature.all, 'list'] as const,
    list: (filters?: any) => [...queryKeys.yourFeature.lists(), filters] as const,
    details: () => [...queryKeys.yourFeature.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.yourFeature.details(), id] as const,
  },
};
```

### Step 2: Create Hook File

Create `/frontend/src/hooks/useYourFeature.ts`:

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../services/apiClient';
import { queryKeys } from '../lib/react-query';

// Query hook
export const useYourData = () => {
  return useQuery({
    queryKey: queryKeys.yourFeature.lists(),
    queryFn: async () => {
      const response = await apiClient.instance.get('/your-endpoint');
      return response.data;
    },
  });
};

// Mutation hook
export const useCreateYourData = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: any) => {
      const response = await apiClient.instance.post('/your-endpoint', data);
      return response.data;
    },
    onSuccess: () => {
      // Invalidate to trigger refetch
      queryClient.invalidateQueries({
        queryKey: queryKeys.yourFeature.lists()
      });
    },
  });
};
```

---

## Query Configuration Options

### Per-Query Configuration

```typescript
const { data } = useYourQuery({
  // Cache configuration
  staleTime: 5 * 60 * 1000,    // 5 minutes - data stays fresh
  gcTime: 10 * 60 * 1000,      // 10 minutes - cache persistence

  // Refetch configuration
  refetchOnWindowFocus: true,   // Refetch when window regains focus
  refetchOnReconnect: true,     // Refetch when reconnecting
  refetchOnMount: true,         // Refetch on component mount
  refetchInterval: 30000,       // Refetch every 30 seconds

  // Retry configuration
  retry: 3,                     // Retry 3 times on error
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),

  // Conditional fetching
  enabled: !!userId,            // Only run if userId exists

  // Callbacks
  onSuccess: (data) => console.log('Success:', data),
  onError: (error) => console.error('Error:', error),
});
```

---

## React Query DevTools

The DevTools are automatically available in development mode:

**Features:**
- View all queries and their cache status
- Inspect query data
- Manually trigger refetch
- Clear cache
- View query dependencies

**Access:**
- Click the React Query icon in the bottom-right corner (only in dev mode)
- Or press `Ctrl+Shift+D` (configurable)

---

## Best Practices

### 1. Use Query Keys Consistently

```typescript
// ✅ Good - use query key factory
const { data } = useQuery({
  queryKey: queryKeys.properties.detail(id),
  queryFn: () => fetchProperty(id),
});

// ❌ Bad - hardcoded keys
const { data } = useQuery({
  queryKey: ['property', id],
  queryFn: () => fetchProperty(id),
});
```

### 2. Invalidate Related Queries

```typescript
// When updating a property, invalidate both detail and list
onSuccess: (_, variables) => {
  queryClient.invalidateQueries({
    queryKey: queryKeys.properties.detail(variables.id)
  });
  queryClient.invalidateQueries({
    queryKey: queryKeys.properties.lists()
  });
}
```

### 3. Handle Loading States

```typescript
// ✅ Good - handle all states
if (isLoading) return <Skeleton />;
if (isError) return <ErrorMessage />;
if (!data) return <EmptyState />;
return <DataView data={data} />;

// ❌ Bad - missing states
return <div>{data.name}</div>; // Crashes if data is undefined
```

### 4. Use Enabled Option for Dependent Queries

```typescript
// Only fetch property details after user is loaded
const { data: user } = useUser();
const { data: property } = useProperty(user?.propertyId, {
  enabled: !!user?.propertyId,
});
```

### 5. Deduplicate Requests

```typescript
// Multiple components using the same query key will share the request
function Component1() {
  const { data } = useProperties(); // First request
}

function Component2() {
  const { data } = useProperties(); // Reuses first request
}
```

---

## Migration Checklist

To migrate an existing component to use React Query:

- [ ] 1. Identify API calls in the component
- [ ] 2. Check if a hook exists in `/frontend/src/hooks/`
- [ ] 3. If not, create a new hook following the pattern
- [ ] 4. Add query key to `/frontend/src/lib/react-query.ts`
- [ ] 5. Replace `useState` + `useEffect` with query hook
- [ ] 6. Replace manual loading/error states with hook states
- [ ] 7. Update mutations to use mutation hooks
- [ ] 8. Test caching behavior
- [ ] 9. Test error handling
- [ ] 10. Remove manual state management code

---

## Common Patterns

### Pagination

```typescript
const [page, setPage] = useState(1);

const { data } = useQuery({
  queryKey: ['properties', 'list', { page }],
  queryFn: () => fetchProperties({ page }),
  keepPreviousData: true, // Keep old data while fetching new page
});
```

### Infinite Scroll

```typescript
const {
  data,
  fetchNextPage,
  hasNextPage,
  isFetchingNextPage,
} = useInfiniteQuery({
  queryKey: ['properties', 'infinite'],
  queryFn: ({ pageParam = 1 }) => fetchProperties({ page: pageParam }),
  getNextPageParam: (lastPage, pages) => lastPage.nextPage,
});
```

### Prefetching

```typescript
import { useQueryClient } from '@tanstack/react-query';

function PropertyCard({ propertyId }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    // Prefetch property details on hover
    queryClient.prefetchQuery({
      queryKey: queryKeys.properties.detail(propertyId),
      queryFn: () => fetchProperty(propertyId),
    });
  };

  return <div onMouseEnter={handleMouseEnter}>...</div>;
}
```

---

## Troubleshooting

### Query Not Refetching

**Problem:** Data is stale but not refetching

**Solution:**
```typescript
// Option 1: Reduce stale time
const { data } = useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  staleTime: 0, // Always consider stale
});

// Option 2: Manual refetch
const { refetch } = useQuery({ ... });
refetch();

// Option 3: Invalidate cache
queryClient.invalidateQueries({ queryKey: ['data'] });
```

### Memory Leaks

**Problem:** Queries continue after component unmounts

**Solution:** React Query handles cleanup automatically. If you need manual cleanup:
```typescript
useEffect(() => {
  return () => {
    // Cleanup if needed
    queryClient.cancelQueries({ queryKey: ['data'] });
  };
}, []);
```

### Duplicate Requests

**Problem:** Same query called multiple times

**Solution:** React Query automatically deduplicates. Check your query keys:
```typescript
// ✅ Same query key - deduplicated
useQuery({ queryKey: ['properties'], ... });
useQuery({ queryKey: ['properties'], ... });

// ❌ Different keys - separate requests
useQuery({ queryKey: ['properties', Date.now()], ... });
```

---

## Resources

- **Official Docs:** https://tanstack.com/query/latest/docs/react/overview
- **Query Keys Guide:** https://tkdodo.eu/blog/effective-react-query-keys
- **Common Mistakes:** https://tkdodo.eu/blog/react-query-render-optimizations
- **DevTools:** https://tanstack.com/query/latest/docs/react/devtools

---

**Next Steps:**
1. Test the existing hooks with your pages
2. Create additional hooks as needed
3. Gradually migrate manual API calls to React Query
4. Monitor cache behavior with DevTools
5. Optimize query configurations based on usage patterns
