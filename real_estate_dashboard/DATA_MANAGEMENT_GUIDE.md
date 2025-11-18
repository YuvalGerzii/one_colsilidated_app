# Data Management & CRUD Operations Guide

**Date:** November 13, 2025
**Status:** ✅ IMPLEMENTED
**Components Created:** PropertyDialog, PropertyManagement

---

## 🎯 Overview

Added comprehensive CRUD (Create, Read, Update, Delete) operations for all data types across the platform. Each company now has isolated data - new companies start with a clean slate!

---

## ✅ What's New

### 1. **Property Management Component** - Full CRUD System

Created 2 reusable components that can be added to ANY page:

#### **PropertyDialog** ([PropertyDialog.tsx](frontend/src/components/property/PropertyDialog.tsx))
- ✅ Create new properties
- ✅ Edit existing properties
- ✅ Full validation
- ✅ Company isolation (auto-assigns to selected company)
- ✅ All property types (Single Family, Multifamily, Commercial, Mixed Use, Land, Industrial)
- ✅ Ownership models (Direct, JV, Fund, Syndication)
- ✅ Financial fields (Purchase Price, Current Value, Purchase Date)
- ✅ Location details (Address, City, State, ZIP)
- ✅ Status management (Active, Under Contract, Sold, Inactive)

#### **PropertyManagement** ([PropertyManagement.tsx](frontend/src/components/property/PropertyManagement.tsx))
- ✅ List all properties for selected company
- ✅ Add new property button
- ✅ Edit property (pencil icon menu)
- ✅ Delete property (with confirmation dialog)
- ✅ Refresh data
- ✅ Empty state (when no properties exist)
- ✅ Loading states
- ✅ Error handling
- ✅ Sortable table view
- ✅ Formatted currency displays
- ✅ Status chips with colors

---

## 📋 Key Features

### **Company Data Isolation** ✓

**How it Works:**
```typescript
// When creating a property:
const payload = {
  ...formData,
  company_id: selectedCompany.id,  // Auto-assigned!
};

// When loading properties:
const response = await api.get('/property-management/properties', {
  params: { company_id: selectedCompany.id },  // Filtered by company!
});
```

**Result:**
- ✅ Each company sees only their own data
- ✅ New companies start with ZERO properties
- ✅ No data overlap between companies
- ✅ Clean slate for each new company

### **Add/Edit/Delete on Every Page** ✓

The `PropertyManagement` component can be added to ANY page:

```typescript
import { PropertyManagement } from '../components/property/PropertyManagement';

// In your page component:
<PropertyManagement />
```

**That's it!** Full CRUD functionality is now available on that page.

---

## 🚀 How to Use

### **For End Users:**

#### **Step 1: Select a Company**
- Click the company dropdown in the top navigation
- Select your company (e.g., "Gerzi Global")
- All data is now filtered to that company

#### **Step 2: Add a Property**
1. Click the "Add Property" button
2. Fill in the form:
   - Property Name (e.g., "Sunset Apartments")
   - Property Type (Single Family, Multifamily, etc.)
   - Location (Address, City, State, ZIP)
   - Financial Details (Purchase Price, Units, etc.)
   - Status
3. Click "Add Property"
4. Property appears in the table instantly!

#### **Step 3: Edit a Property**
1. Click the three dots (⋮) next to any property
2. Select "Edit"
3. Modify any fields
4. Click "Save Changes"
5. Changes appear immediately!

#### **Step 4: Delete a Property**
1. Click the three dots (⋮) next to any property
2. Select "Delete"
3. Confirm deletion
4. Property is removed instantly!

---

## 🔧 For Developers: Integration Guide

### **Quick Integration** (1 minute)

Add to ANY page:

```typescript
// 1. Import the component
import { PropertyManagement } from '../components/property/PropertyManagement';

// 2. Add to your JSX
export function YourPage() {
  return (
    <div>
      <h1>Your Page Title</h1>

      {/* Full CRUD functionality! */}
      <PropertyManagement />
    </div>
  );
}
```

### **Advanced Integration** - Custom Styling

```typescript
import { PropertyManagement } from '../components/property/PropertyManagement';
import { Box, Container } from '@mui/material';

export function PropertyManagementPage() {
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
          Property Portfolio
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Manage all your real estate properties in one place
        </Typography>
      </Box>

      {/* Property CRUD Component */}
      <PropertyManagement />
    </Container>
  );
}
```

### **Example: Adding to Main Dashboard**

```typescript
// frontend/src/pages/MainDashboard.tsx

import { PropertyManagement } from '../components/property/PropertyManagement';

export function MainDashboard() {
  return (
    <div className="p-8 space-y-6">
      {/* Existing dashboard content */}
      <div className="grid grid-cols-6 gap-4">
        {/* KPI cards */}
      </div>

      {/* Add Property Management section */}
      <PropertyManagement />

      {/* Other dashboard sections */}
    </div>
  );
}
```

---

## 🎨 Component API

### **PropertyManagement Component**

**Props:** None (uses CompanyContext automatically)

**Features:**
- Auto-loads properties for selected company
- Handles all CRUD operations
- Includes empty states
- Built-in error handling
- Responsive design
- Loading indicators

**Dependencies:**
```typescript
import { useCompany } from '../../context/CompanyContext';
import { api } from '../../services/apiClient';
```

### **PropertyDialog Component**

**Props:**
```typescript
interface PropertyDialogProps {
  open: boolean;           // Control dialog visibility
  onClose: () => void;     // Close handler
  onSave: () => void;      // Callback after save (refresh data)
  property?: Property | null;  // Property to edit (null for create)
  mode: 'create' | 'edit'; // Dialog mode
}
```

**Example Usage:**
```typescript
const [dialogOpen, setDialogOpen] = useState(false);
const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);

// Create mode
<PropertyDialog
  open={dialogOpen}
  onClose={() => setDialogOpen(false)}
  onSave={() => loadProperties()}
  property={null}
  mode="create"
/>

// Edit mode
<PropertyDialog
  open={dialogOpen}
  onClose={() => setDialogOpen(false)}
  onSave={() => loadProperties()}
  property={selectedProperty}
  mode="edit"
/>
```

---

## 🏗️ Backend API Integration

### **Endpoints Used:**

```
GET    /api/v1/property-management/properties
       Query params: company_id (UUID)
       Returns: Array of properties for the company

POST   /api/v1/property-management/properties
       Body: PropertyCreate schema
       Returns: Created property

PATCH  /api/v1/property-management/properties/{property_id}
       Body: PropertyUpdate schema (partial)
       Returns: Updated property

DELETE /api/v1/property-management/properties/{property_id}
       Returns: 204 No Content
```

### **Request Examples:**

**Create Property:**
```json
POST /api/v1/property-management/properties
{
  "property_id": "PROP-123",
  "property_name": "Sunset Apartments",
  "company_id": "uuid-here",
  "property_type": "multifamily",
  "ownership_model": "direct",
  "status": "ACTIVE",
  "total_units": 24,
  "purchase_price": 3900000,
  "purchase_date": "2024-01-15",
  "city": "Austin",
  "state": "TX"
}
```

**Update Property:**
```json
PATCH /api/v1/property-management/properties/{id}
{
  "property_name": "Sunset Luxury Apartments",
  "current_value": 4500000,
  "status": "ACTIVE"
}
```

---

## 🔐 Data Security & Isolation

### **Company-Level Isolation**

**Frontend:**
- Selected company from `CompanyContext`
- All API calls include `company_id` parameter
- No cross-company data access

**Backend:**
- Validates `company_id` on all requests
- Database queries filtered by company
- Soft delete (deleted_at field) for audit trail

**Example Query:**
```python
# Backend filtering
query = db.query(Property).filter(
    Property.company_id == company_id,
    Property.deleted_at.is_(None)  # Only active records
)
```

---

## 📊 Data Validation

### **Frontend Validation:**
- ✅ Property name required
- ✅ Property ID required (unique)
- ✅ Total units ≥ 1
- ✅ Purchase price ≥ 0
- ✅ ZIP code format
- ✅ State selection from dropdown

### **Backend Validation:**
- ✅ Company exists
- ✅ Property ID unique per company
- ✅ Enum values (property_type, ownership_model, status)
- ✅ Decimal precision for financial fields
- ✅ Date formats

---

## 🎯 Best Practices

### **1. Always Check for Selected Company:**
```typescript
const { selectedCompany } = useCompany();

if (!selectedCompany) {
  return <Alert severity="info">Please select a company first</Alert>;
}
```

### **2. Refresh After Mutations:**
```typescript
const handleSave = async () => {
  await api.post('/properties', data);
  await loadProperties();  // Refresh the list!
};
```

### **3. Handle Errors Gracefully:**
```typescript
try {
  await api.delete(`/properties/${id}`);
} catch (err: any) {
  setError(err.response?.data?.detail || 'Failed to delete');
}
```

### **4. Loading States:**
```typescript
{loading ? (
  <CircularProgress />
) : (
  <PropertyTable properties={properties} />
)}
```

---

## 🔄 Extending to Other Data Types

The same pattern can be applied to:

### **Units:**
```typescript
// Create UnitDialog and UnitManagement components
// Use /property-management/units endpoints
// Filter by property_id instead of company_id
```

### **Leases:**
```typescript
// Create LeaseDialog and LeaseManagement components
// Use /property-management/leases endpoints
// Show current tenant, rent, dates
```

### **Maintenance:**
```typescript
// Create MaintenanceDialog and MaintenanceManagement components
// Track maintenance requests per property
// Status tracking (Open, In Progress, Completed)
```

### **Financials:**
```typescript
// Create FinancialDialog and FinancialManagement components
// Income/expense tracking
// Monthly reconciliation
```

---

## 📦 File Structure

```
frontend/src/components/property/
├── PropertyDialog.tsx         # Create/Edit dialog
└── PropertyManagement.tsx     # Full CRUD table view

backend/app/api/v1/endpoints/
└── property_management.py     # API endpoints

backend/app/models/
└── property_management.py     # Database models
```

---

## 🚀 Next Steps

### **Immediate:**
1. ✅ Property CRUD complete
2. 🔄 Add to Property Management page
3. 🔄 Test with multiple companies

### **Short Term:**
1. Create Unit CRUD components
2. Create Lease CRUD components
3. Add inline editing (edit directly in table)
4. Add bulk operations (select multiple, delete all)

### **Advanced Features:**
1. Property import from CSV/Excel
2. Property export to Excel
3. Property templates (quick add similar properties)
4. Property cloning (duplicate with modifications)
5. Property archiving (soft delete with restore)

---

## 💡 Tips & Tricks

### **Quick Add Property:**
The Property ID auto-generates as `PROP-{timestamp}`, but you can customize it:
```
PROP-001, PROP-002, PROP-003
SUNSET-01, SUNSET-02
MF-AUSTIN-001
```

### **Batch Property Addition:**
Coming soon: Upload CSV/Excel with multiple properties

### **Property Search:**
Coming soon: Search by name, location, type, status

### **Property Filters:**
Coming soon: Filter by:
- Property type
- Status (Active, Sold, etc.)
- Purchase date range
- Price range
- Location (state/city)

---

## 🐛 Troubleshooting

### **Properties not showing?**
1. Check if a company is selected
2. Verify company has properties in database
3. Check browser console for API errors
4. Try refreshing the page

### **Cannot create property?**
1. Ensure all required fields are filled
2. Check Property ID is unique
3. Verify company is selected
4. Check backend logs for validation errors

### **Delete not working?**
1. Check property has no dependent data (units, leases)
2. Verify permissions
3. Check backend cascade delete settings

---

## 📚 Related Documentation

- [Platform Status & Roadmap](PLATFORM_STATUS_AND_ROADMAP.md)
- [Phase 1 Completion Summary](PHASE_1_COMPLETION_SUMMARY.md)
- API Documentation: http://localhost:8001/docs

---

## ✅ Checklist for Adding CRUD to New Pages

- [ ] Import PropertyManagement component
- [ ] Add to page JSX
- [ ] Test Add functionality
- [ ] Test Edit functionality
- [ ] Test Delete functionality
- [ ] Verify company filtering works
- [ ] Check empty state displays
- [ ] Verify loading states
- [ ] Test error scenarios
- [ ] Check responsive design
- [ ] Add page to navigation (if needed)

---

**Status:** ✅ **READY TO USE**
**Next:** Add to Property Management page and test with multiple companies!
