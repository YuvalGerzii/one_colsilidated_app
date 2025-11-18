# Quick Fixes for Integration Issues

## 🔴 CRITICAL: Fix These NOW (10 minutes)

### Issue #1: Wrong Port Number
**File:** `frontend/src/services/apiClient.ts`
**Line:** 15

**Change from:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';
```

**Change to:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
```

---

### Issue #2: Wrong Token Key
**File:** `frontend/src/services/apiClient.ts`
**Line:** 37

**Change from:**
```typescript
const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken');
};
```

**Change to:**
```typescript
const getAuthToken = (): string | null => {
  return localStorage.getItem('auth_token');
};
```

---

## Test After Fixing

1. Start backend:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload --port 8000
   ```

2. Start frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Test these pages (should now work):
   - Property Management → Add Property
   - Accounting → Entity Comparison
   - Accounting → Compliance Calendar
   - Accounting → Depreciation Calculator
   - Accounting → Audit Risk Assessment

---

## What Was Broken?

- **Property Management**: Couldn't add properties (connection refused)
- **All Accounting Tools**: No data loading (connection refused + auth failed)

## What Gets Fixed?

✅ API calls will connect to correct port (8000)
✅ Authentication tokens will be found
✅ All 6 broken pages will work
✅ No more "Network Error" or "401 Unauthorized"

---

## Next Steps (After Quick Fixes)

See `INTEGRATION_ISSUES_ANALYSIS.md` for:
- Consolidating duplicate API clients
- Adding React Query for better caching
- Adding error boundaries
- Type safety improvements
- Rate limiting
- And more...

---

**Time to fix:** 2 minutes
**Impact:** Unblocks 6 pages
**Risk:** None (simple configuration fixes)
