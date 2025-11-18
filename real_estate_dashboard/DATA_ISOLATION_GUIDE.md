# Data Isolation Guide

## Overview

The Real Estate Dashboard uses a **multi-tenant architecture** where each company has its own isolated workspace with separate data. This guide explains what data is company-specific and what data is shared across all companies.

## ✅ What's Been Implemented

### 1. Database Schema Fix
- **Fixed**: Properties table now has `company_id` column
- **Migration**: `fix_properties_company_id` migration applied successfully
- **Result**: All properties are now properly isolated by company

### 2. Data Validation Endpoint
- **Endpoint**: `GET /api/v1/companies/{company_id}/data-stats`
- **Purpose**: Verify that new companies have zero data
- **Usage**: Call this endpoint after creating a company to confirm data isolation

Example Response:
```json
{
    "company_id": "2308adec-bbfb-459e-af4c-222b16f24892",
    "company_name": "Test Company - Clean Data Check",
    "company_specific_data": {
        "properties": 0,
        "deals": 0,
        "legal_documents": 0,
        "compliance_items": 0,
        "brokers": 0,
        "accounting_profiles": 0
    },
    "is_empty": true,
    "message": "✅ Company has zero data - ready for use!",
    "note": "Market intelligence data is intentionally shared across all companies"
}
```

### 3. Frontend Data Isolation
- **localStorage keys**: Changed from `portfolioProperties` to `portfolioProperties_{company_id}`
- **Hardcoded data removed**: All demo data (e.g., "Sunset Apartments") removed from components
- **Company-specific loading**: Components now load data based on selected company
- **Auto-cleanup**: Legacy localStorage data automatically cleaned on app load

### 4. Data Management UI
- **Location**: `/admin/data-management`
- **Features**:
  - View current localStorage state
  - Clear legacy data (old non-company-specific keys)
  - Clear current company data
  - Clear all browser data
  - Debug localStorage contents in console

## 📊 Data Types

### Company-Specific Data (Isolated by company_id)

These tables have `company_id` foreign keys and data is **NOT shared** between companies:

#### Core Business Data
- **Properties** - Real estate properties owned/managed by the company
- **Deals** - Deal pipeline and transactions
- **Brokers** - Company's broker contacts
- **Funds** - Investment funds managed by the company
- **Limited Partners** - LPs invested in the company's funds

#### Property Management
- **Units** - Individual units within properties (linked via property)
- **Leases** - Rental agreements (linked via property)
- **Maintenance Requests** - Property maintenance tracking

#### Financial & Accounting
- **Accounting Profiles** - Company accounting configuration
- **Valuations** - Property valuations and appraisals
- **DCF Models** - Discounted cash flow models
- **LBO Models** - Leveraged buyout models
- **Loans** - Debt and financing records

#### Legal & Compliance
- **Legal Documents** - Company's legal documents and contracts
- **Legal Deadlines** - Legal calendar and deadlines
- **Compliance Items** - Regulatory compliance tracking
- **Risk Assessments** - Property risk assessments
- **Contract Reviews** - Contract review workflow

#### Analytics & Reporting
- **Generated Reports** - Custom reports created by the company
- **Dashboards** - Custom dashboard configurations
- **Custom KPIs** - Company-defined metrics
- **Model Templates** - Saved financial model templates

**Total: 46+ tables with company_id**

### Global/Shared Data (No company_id)

These tables contain reference/market data that is **shared across ALL companies**:

#### Market Intelligence
- **geographic_economic_indicators** - ~101,557 records - Economic data by geography
- **real_estate_market_data** - ~58,294 records - Market trends and pricing
- **neighborhood_scores** - ~29,716 records - Neighborhood quality metrics
- **hot_zone_markets** - ~19,218 records - High-growth market identification
- **comparable_transactions** - ~13,079 records - Comparable sales data
- **time_series_indicators** - ~4,374 records - Time-series market data

#### Economic Data
- **market_data** - ~122 records - General market data
- **economic_indicators** - ~105 records - Macro economic indicators
- **fred_indicators** - Federal Reserve economic data
- **census_data** - US Census demographic data

#### Property Intelligence
- **property_tax_assessments** - ~1,500 records - Tax assessment data
- **zoning_districts** - ~615 records - Zoning information
- **development_pipeline** - ~270 records - Upcoming developments
- **str_performance_metrics** - Short-term rental performance data
- **tenant_credit_quality** - Credit quality metrics

**Total: 18+ tables with ~240,000+ shared reference records**

## 🎯 What This Means for Users

### When Creating a New Company:

✅ **You WILL see:**
- Market intelligence data (economic indicators, market trends, etc.)
- Reference data (zoning, tax assessments, comparable sales)
- This data is **intentionally shared** to help you analyze deals

❌ **You WON'T see:**
- Other companies' properties
- Other companies' deals
- Other companies' financial models
- Other companies' reports or documents
- Any company-specific records

### Verification Steps:

1. **Create a new company** via the frontend or API
2. **Call the data stats endpoint**:
   ```bash
   curl http://localhost:8001/api/v1/companies/{company_id}/data-stats
   ```
3. **Verify all counts are zero**:
   - properties: 0
   - deals: 0
   - legal_documents: 0
   - compliance_items: 0
   - brokers: 0
   - accounting_profiles: 0

4. **Confirm `is_empty: true`** in the response

### Using the Data Management UI:

1. **Navigate to**: `/admin/data-management`
2. **Check current state**: See number of localStorage keys and detect legacy data
3. **Clear legacy data**: If you see "Legacy data detected" warning, click "Clear Legacy Data"
4. **Clear company data**: Remove all localStorage for the currently selected company
5. **Clear all data**: Nuclear option - removes ALL localStorage (use with caution)
6. **Debug**: Click "View localStorage in Console" to see all stored data

## 🔒 Data Isolation Guarantees

### Database Level
- All company-specific tables have `company_id` foreign key with `NOT NULL` constraint
- Foreign key constraints use `ON DELETE CASCADE` to maintain referential integrity
- PostgreSQL row-level isolation ensures data separation

### API Level
- All endpoints filter by `company_id` automatically
- No API endpoint can access another company's data without explicit company_id
- CompanyContext in frontend ensures only selected company's data is shown

### Application Level
- React CompanyContext manages selected company state
- All API calls include company_id in the request
- Frontend components filter/display only company-specific data

### localStorage Isolation
- Company-specific keys use pattern: `{key}_{company_id}`
- Legacy non-company-specific keys are auto-cleaned on app load
- Manual cleanup UI available at `/admin/data-management`

## 📝 Common Questions

### Q: Why do I see market data when I create a new company?
**A:** Market intelligence data (economic indicators, comparable sales, etc.) is intentionally shared across all companies. This is reference data that helps you analyze potential deals, not company-specific records.

### Q: How do I know if a table is company-specific?
**A:** Check if the table has a `company_id` column. You can verify this in the database:
```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'your_table_name'
AND column_name = 'company_id';
```

### Q: I still see old data when switching companies. What do I do?
**A:** Navigate to `/admin/data-management` and click "Clear Legacy Data". This will remove old non-company-specific localStorage keys and reload the page.

### Q: Can I migrate data between companies?
**A:** Yes, but it requires explicit admin action. Data is isolated for security and you cannot accidentally access other companies' data.

### Q: What happens to data when I delete a company?
**A:**
- **Soft delete** (default): Company and all related data are marked as deleted but retained in database
- **Hard delete** (if specified): Company and all related data are permanently removed (CASCADE delete)

## 🛠️ Technical Implementation

### Files Modified/Created

#### Backend:
1. **`/backend/alembic/versions/fix_properties_company_id.py`** - Migration to add company_id to properties table
2. **`/backend/app/api/v1/endpoints/companies.py`** - Added `/companies/{id}/data-stats` endpoint
3. **`/backend/app/models/crm.py`** - Removed duplicate Deal class

#### Frontend:
1. **`/frontend/src/pages/PortfolioDashboard/PortfolioDashboard.tsx`** - Company-specific localStorage
2. **`/frontend/src/pages/OperateSummary.tsx`** - Removed hardcoded demo data
3. **`/frontend/src/App.tsx`** - Added auto-cleanup and DataManagement route
4. **`/frontend/src/utils/clearOldData.ts`** - Created cleanup utilities
5. **`/frontend/src/components/admin/DataManagement.tsx`** - Created data management UI

### Migration Applied
- **File**: `backend/alembic/versions/fix_properties_company_id.py`
- **Changes**: Added `company_id` column to `properties` table
- **Status**: ✅ Applied successfully

### New Endpoint
- **Route**: `GET /api/v1/companies/{company_id}/data-stats`
- **Purpose**: Validate company data isolation
- **Response**: Returns counts of all company-specific records

### localStorage Key Pattern
**Old (deprecated):**
```
portfolioProperties
savedReports
```

**New (company-specific):**
```
portfolioProperties_{company_id}
savedReports_{company_id}
```

### Auto-Cleanup on App Load
Location: `/frontend/src/App.tsx` - `useEffect` hook
```typescript
useEffect(() => {
  const cleared = clearLegacyLocalStorage();
  if (cleared > 0) {
    console.log(`[App] Cleaned up ${cleared} legacy localStorage keys`);
  }
}, []);
```

## 🎉 Summary

**New companies are guaranteed to start with ZERO company-specific data.**

The only data you'll see is:
1. **Shared market intelligence** (economic data, market trends, etc.)
2. **Reference data** (zoning, tax info, comparable sales)

This is **by design** and helps you:
- Analyze potential deals using market data
- Make informed decisions with economic indicators
- Compare properties using historical transaction data

All of your company's actual business data (properties, deals, financials, etc.) remains **100% isolated** from other companies.

## 🔧 Troubleshooting

### Issue: I see "Sunset Apartments" or other demo data for a new company

**Solution**:
1. Go to `/admin/data-management`
2. Click "Clear Legacy Data (Recommended)"
3. Page will auto-reload with clean data

**Why it happens**: You had old localStorage data from before company-specific isolation was implemented.

### Issue: Data isn't saving for my company

**Solution**:
1. Check that a company is selected (look for company name in header)
2. Open browser console (F12) and run: `localStorage`
3. Verify you see keys like `portfolioProperties_{company_id}`
4. If not, try clicking "Debug localStorage" in Data Management UI

### Issue: Data appears for wrong company

**Solution**:
1. Clear browser cache and localStorage
2. Go to `/admin/data-management`
3. Click "Clear All Browser Data"
4. Reload and re-select your company

## 📞 Support

If you encounter any data isolation issues:
1. Check this guide first
2. Use the Data Management UI at `/admin/data-management`
3. Call the data-stats endpoint to verify isolation
4. Check browser console for error messages
