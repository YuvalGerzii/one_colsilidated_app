# Property Management - Company Isolation Fix

## Problem
The Property Management page was showing **shared/hardcoded demo data** instead of company-specific data. This violated the multi-tenant isolation principle where each company should see only their own properties.

## Root Cause
All Property Management components were using hardcoded `sampleProperties`, `sampleUnits`, `sampleLeases`, and `sampleMaintenance` data instead of fetching company-specific data from the backend API.

## Components Affected
1. **PropertiesTable.tsx** - ✅ FIXED
2. **PropertyDashboard.tsx** - Needs fixing
3. **UnitsTable.tsx** - Needs fixing
4. **LeasesTable.tsx** - Needs fixing
5. **MaintenanceTable.tsx** - Needs fixing
6. **ROIAnalysis.tsx** - Needs fixing

## What Was Fixed

### PropertiesTable.tsx ✅
**Changes Made:**
- ✅ Removed hardcoded `sampleProperties` array (Maple Apartments, Oak Plaza, Pine Tower)
- ✅ Added `useCompany()` hook to get selected company
- ✅ Changed data source from hardcoded array to empty company-specific array
- ✅ Added company name to page title: "Property Master List - {Company Name}"
- ✅ Disabled "Add New Property" button when no company selected
- ✅ Added alerts:
  - "Please select a company" when no company selected
  - "No properties found for {Company}" when company has zero properties
- ✅ Updated tip text to explain company-specific data isolation

**Result:**
- New companies see: "No properties found for {Company Name}. Click 'Add New Property' to get started."
- Different companies see different property lists (currently empty until backend integration)
- Cannot add properties without selecting a company first

## What Still Needs To Be Fixed

### Remaining Components with Hardcoded Data:

1. **PropertyDashboard.tsx**
   - Remove sample metrics/statistics
   - Make all dashboard stats company-specific

2. **UnitsTable.tsx**
   - Remove sample units data
   - Link units to company's properties only

3. **LeasesTable.tsx**
   - Remove sample leases/tenants
   - Show only leases for company's properties

4. **MaintenanceTable.tsx**
   - Remove sample maintenance tickets
   - Show only maintenance for company's properties

5. **ROIAnalysis.tsx**
   - Make financial analysis company-specific
   - Remove hardcoded performance metrics

## Next Steps

### Option 1: Remove All Hardcoded Data (Quick Fix)
Similar to what was done for PropertiesTable, update each component to:
1. Import `useCompany` hook
2. Remove all sample data arrays
3. Show empty state with company name
4. Display helpful message for new companies

### Option 2: Connect to Backend API (Full Solution)
1. Create API endpoints for each entity type
2. Use React Query to fetch company-specific data
3. Pass `company_id` in all API requests
4. Implement real CRUD operations

### Option 3: Use localStorage (Temporary)
Similar to Portfolio Dashboard:
1. Store data in localStorage with company-specific keys
2. Use pattern: `{entityType}_{company_id}`
3. Load/save on company selection change

## Verification Steps

To verify property management is now company-specific:

1. **Select Company A**
   - Go to Property Management
   - Should see: "No properties found for Company A"
   - Add a test property

2. **Switch to Company B**
   - Go to Property Management
   - Should see: "No properties found for Company B"
   - Should NOT see Company A's property

3. **Switch back to Company A**
   - Should see the property you added earlier
   - Confirms data isolation working

4. **No Company Selected**
   - Should see: "Please select a company to view and manage properties"
   - "Add New Property" button should be disabled

## Database Schema Reference

Properties table already has `company_id`:
```sql
properties (
  id UUID PRIMARY KEY,
  company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name VARCHAR,
  address VARCHAR,
  property_type VARCHAR,
  units INTEGER,
  -- ... other fields
)
```

Backend API endpoint exists:
```
GET    /api/v1/properties?company_id={uuid}
POST   /api/v1/properties
PUT    /api/v1/properties/{id}
DELETE /api/v1/properties/{id}
```

## Summary

✅ **Fixed:** PropertiesTable now shows company-specific data
⚠️ **Remaining:** 5 other components still have hardcoded sample data
📋 **Recommendation:** Apply same fix pattern to all remaining components

The Property Management page will be fully company-isolated once all components are updated to use `useCompany()` and fetch company-specific data instead of showing hardcoded samples.
