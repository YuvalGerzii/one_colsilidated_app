# API Client Migration Guide

## Overview

This guide helps migrate from direct axios calls to the centralized `apiClient` for automatic company filtering and improved error handling.

## Why Migrate?

### Before (Manual Company Handling) ❌
```typescript
import axios from 'axios';
import { useCompany } from '@/context/CompanyContext';

// Every component needs to:
const { selectedCompany } = useCompany();

// Manually add company_id to every request
const response = await axios.get(
  `${API_BASE_URL}/financial-models/dcf?company_id=${selectedCompany?.id}`
);

// Handle auth tokens manually
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
```

### After (Automatic) ✅
```typescript
import { apiClient } from '@/services/apiClient';

// No company context needed!
// No manual company_id handling!
// Auth token automatically included!
const data = await apiClient.get('/financial-models/dcf');
```

## Migration Steps

### Step 1: Replace Imports

**Before:**
```typescript
import axios from 'axios';
```

**After:**
```typescript
import { apiClient } from '../../../services/apiClient';
// Adjust path based on your file location
```

### Step 2: Remove Company Context (If Only Used for API Calls)

**Before:**
```typescript
import { useCompany } from '@/context/CompanyContext';

function MyComponent() {
  const { selectedCompany } = useCompany();
  // ... uses selectedCompany only for API calls
}
```

**After:**
```typescript
// Remove useCompany import if only used for API calls
function MyComponent() {
  // No need for selectedCompany anymore!
}
```

### Step 3: Replace API Calls

#### GET Requests

**Before:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

const response = await axios.get(
  `${API_BASE_URL}/financial-models/dcf?company_id=${selectedCompany?.id}`
);
const data = response.data;
```

**After:**
```typescript
const data = await apiClient.get('/financial-models/dcf');
```

#### POST Requests

**Before:**
```typescript
const response = await axios.post(
  `${API_BASE_URL}/financial-models/dcf`,
  {
    ...modelData,
    company_id: selectedCompany?.id,
  }
);
const created = response.data;
```

**After:**
```typescript
// No need to add company_id manually!
const created = await apiClient.post('/financial-models/dcf', modelData);
```

#### PUT Requests

**Before:**
```typescript
const response = await axios.put(
  `${API_BASE_URL}/financial-models/dcf/${id}?company_id=${selectedCompany?.id}`,
  updateData
);
const updated = response.data;
```

**After:**
```typescript
const updated = await apiClient.put(`/financial-models/dcf/${id}`, updateData);
```

#### DELETE Requests

**Before:**
```typescript
await axios.delete(
  `${API_BASE_URL}/financial-models/dcf/${id}?company_id=${selectedCompany?.id}`
);
```

**After:**
```typescript
await apiClient.delete(`/financial-models/dcf/${id}`);
```

### Step 4: Remove Manual Error Handling (Optional)

The apiClient already handles common errors (401, 403, 404, 500) globally.

**Before:**
```typescript
try {
  const response = await axios.get(url);
  return response.data;
} catch (error: any) {
  if (error.response?.status === 401) {
    // Redirect to login
  } else if (error.response?.status === 404) {
    // Handle not found
  }
  throw error;
}
```

**After:**
```typescript
try {
  return await apiClient.get(url);
} catch (error) {
  // Only handle component-specific errors
  // Global errors (401, 403, 404, 500) handled automatically
  console.error('Component-specific error:', error);
}
```

## Complete Example

### Before

```typescript
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useCompany } from '@/context/CompanyContext';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

export const MyComponent: React.FC = () => {
  const { selectedCompany } = useCompany();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('authToken');

        const response = await axios.get(
          `${API_BASE_URL}/financial-models/dcf?company_id=${selectedCompany?.id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setData(response.data);
      } catch (error: any) {
        if (error.response?.status === 401) {
          window.location.href = '/login';
        }
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    if (selectedCompany) {
      fetchData();
    }
  }, [selectedCompany]);

  const handleCreate = async (formData: any) => {
    try {
      const token = localStorage.getItem('authToken');

      await axios.post(
        `${API_BASE_URL}/financial-models/dcf`,
        {
          ...formData,
          company_id: selectedCompany?.id,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Refresh data
      // ... fetch again
    } catch (error) {
      console.error('Error creating:', error);
    }
  };

  return (
    <div>
      {/* Component UI */}
    </div>
  );
};
```

### After

```typescript
import React, { useState, useEffect } from 'react';
import { apiClient } from '../../services/apiClient';

export const MyComponent: React.FC = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Company filtering and auth happen automatically!
        const models = await apiClient.get('/financial-models/dcf');
        setData(models);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // No dependency on selectedCompany needed!

  const handleCreate = async (formData: any) => {
    try {
      // No need to add company_id or auth token!
      await apiClient.post('/financial-models/dcf', formData);

      // Refresh data
      const models = await apiClient.get('/financial-models/dcf');
      setData(models);
    } catch (error) {
      console.error('Error creating:', error);
    }
  };

  return (
    <div>
      {/* Component UI */}
    </div>
  );
};
```

## Benefits Summary

1. **No Manual Company Filtering** - Automatic company_id injection
2. **No Manual Auth** - Automatic auth token handling
3. **Global Error Handling** - 401/403/404/500 handled centrally
4. **Cleaner Code** - 30-50% less boilerplate
5. **Consistent API** - Same pattern across all pages
6. **Type Safety** - TypeScript support built-in
7. **Easier Testing** - Mock apiClient once, not axios everywhere

## Files to Migrate

Based on the search, these files currently use axios directly:

1. `/frontend/src/pages/Accounting/EntityComparisonTool.tsx`
2. `/frontend/src/pages/Accounting/ComplianceCalendar.tsx`
3. `/frontend/src/pages/Accounting/DepreciationCalculator.tsx`
4. `/frontend/src/pages/Accounting/AuditRiskAssessment.tsx`
5. `/frontend/src/pages/PropertyManagement/components/AddPropertyModal.tsx`

Plus any other files with axios imports in:
- `/frontend/src/components/**`
- `/frontend/src/services/**` (except apiClient.ts itself)
- `/frontend/src/hooks/**`

## Quick Migration Checklist

For each file:

- [ ] Replace `import axios from 'axios'` with `import { apiClient } from '@/services/apiClient'`
- [ ] Remove `useCompany()` if only used for API calls
- [ ] Remove `API_BASE_URL` constant
- [ ] Replace `axios.get()` → `apiClient.get()`
- [ ] Replace `axios.post()` → `apiClient.post()`
- [ ] Replace `axios.put()` → `apiClient.put()`
- [ ] Replace `axios.delete()` → `apiClient.delete()`
- [ ] Remove manual `company_id` parameters
- [ ] Remove manual `Authorization` headers
- [ ] Remove `.data` access (apiClient returns data directly)
- [ ] Simplify error handling (remove 401/403/404 handling)
- [ ] Test the component

## Testing After Migration

1. **Switch Companies**: Select different companies and verify data changes
2. **Test CRUD Operations**: Create, Read, Update, Delete
3. **Test Auth**: Logout and verify redirect to login on 401
4. **Check Network Tab**: Verify company_id is in requests
5. **Check Console**: No errors related to company filtering

## Need Help?

- See [apiClient.ts](frontend/src/services/apiClient.ts) for implementation details
- See [CompanyContext.tsx](frontend/src/context/CompanyContext.tsx) for company state
- See [PLATFORM_GUIDE.md](PLATFORM_GUIDE.md) for architecture overview

---

**Last Updated**: 2025-11-11
**Author**: RE Capital Analytics Team
