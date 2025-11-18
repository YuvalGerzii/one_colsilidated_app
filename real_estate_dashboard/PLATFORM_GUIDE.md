# RE Capital Analytics - Platform Guide

## Overview

RE Capital Analytics is a comprehensive real estate investment and management platform with **18+ integrated modules** covering everything from property management to institutional-grade financial modeling.

Version: **2.4.1**

---

## Multi-Company Architecture

### What's New
The platform now supports **multi-company/multi-tenant** functionality, allowing you to:
- Manage multiple companies from one account
- Isolate data completely between companies
- Switch between companies seamlessly
- Share users across companies

### How It Works
1. **Select Company**: Use the company selector in the header (top-right)
2. **Automatic Filtering**: All API requests automatically filter by your selected company
3. **Data Isolation**: Each company's data is completely isolated from others

### For Developers
We've implemented a centralized API client that automatically handles company filtering:

```typescript
// Import the centralized API client
import { apiClient } from '@/services/apiClient';

// All requests automatically include company context
const models = await apiClient.get('/financial-models/dcf');
const newModel = await apiClient.post('/financial-models/dcf', data);
```

No need to manually add `company_id` to every request - it's handled automatically!

---

## Platform Modules

### 1. Core Operations

#### Property Management
**Path**: `/property-management`
- Track unlimited properties and units
- Lease management with expiration alerts
- Maintenance tracking and work orders
- ROI analysis and performance metrics

#### Accounting & Bookkeeping
**Path**: `/accounting`
- Chart of accounts management
- Journal entries and transactions
- Financial statements (P&L, Balance Sheet, Cash Flow)
- Account reconciliation
- **New Module**

#### Deal Pipeline & CRM
**Path**: `/crm/deals`
- Deal tracking and stage management
- Broker relationship management
- Comparable properties (comps)
- Pipeline analytics
- Email templates and automation

---

### 2. Financial Analysis

#### Real Estate Models (12+ Models)
**Path**: `/real-estate-tools`

Property-level models include:
1. **Fix & Flip** - Renovation and resale analysis
2. **Single-Family Rental** - SFR cash flow modeling
3. **Small Multifamily** (2-10 units) - Small apartment buildings
4. **Extended Multifamily** (10+ units) - Large apartment complexes
5. **Hotel Development** - Hospitality projects
6. **Mixed-Use** - Commercial + Residential
7. **Subdivision** - Land development
8. **Small Multifamily Acquisition** - Acquisition analysis
9. **Lease Analyzer** - Lease structure optimization
10. **Renovation Budget** - Detailed renovation planning
11. **Tax Strategy** - Tax-optimized structuring
12. **Market Intelligence** - Market data integration

#### Company Financial Analysis
**Path**: `/financial-models`

Institutional-grade models:
1. **DCF (Discounted Cash Flow)** - Intrinsic valuation
2. **LBO (Leveraged Buyout)** - Private equity analysis
3. **M&A / Merger Model** - Accretion/dilution analysis
4. **Due Diligence** - Comprehensive DD framework
5. **Comparable Company Analysis** - Trading comps

#### Portfolio Dashboard
**Path**: `/portfolio-dashboard`
- Portfolio-level analytics
- Geographic performance analysis
- Risk metrics and scenarios
- Performance attribution

---

### 3. Capital & Legal

#### Fund Management
**Path**: `/fund-management`
- Limited Partner (LP) management
- Capital calls and distributions
- Waterfall calculations (preferred return, catch-up, carry)
- MOIC and IRR tracking
- Fund performance reporting

#### Debt Management
**Path**: `/debt-management`
- Loan tracking and amortization
- Debt service coverage ratio (DSCR)
- Refinancing analysis
- Loan comparison tools
- Interest rate scenarios

#### Legal Services
**Path**: `/legal-services`
- Contract analysis and extraction
- Compliance tracking and audits
- Document templates
- Clause analysis
- Risk assessment

---

### 4. Data & Intelligence

#### Market Intelligence
**Path**: `/market-intelligence`
- Market data integration
- Trend analysis
- Competitive intelligence
- Geographic insights
- **Beta Feature**

#### Tax Strategy
**Path**: `/tax-strategy`

Advanced tax modules:
1. **1031 Exchange** - Like-kind exchange planning
2. **Cost Segregation** - Accelerated depreciation
3. **QSBS Analysis** - Qualified Small Business Stock
4. **Section 179 Optimizer** - Equipment deduction planning
5. **Opportunity Zones** - OZ investment analysis

#### PDF Extraction
**Path**: `/pdf-extraction`
- Extract data from rent rolls
- Parse T-12 operating statements
- Extract financial statements
- Automated data capture

---

### 5. Management & Reporting

#### Project Tracking
**Path**: `/project-tracking`
- Development project management
- Renovation tracking
- Capital improvement plans
- Budget vs actual analysis
- Timeline management

#### Reports & Documents
**Path**: `/saved-reports`
- Generate professional reports
- Custom templates
- Export to PDF/Excel
- Report library and version control

#### Integrations
**Path**: `/integrations`
- External API connections
- Data synchronization
- Third-party services
- Custom webhooks

---

## Quick Start Guide

### Step 1: Select Your Company
1. Click the **Company Selector** in the top-right header
2. Select your company from the dropdown
3. Or create a new company with **"Add New Company"**

### Step 2: Explore Modules
From the **homepage** (`/`), browse all 18+ modules organized by category:
- **Core Operations** - Property, Accounting, CRM
- **Financial Analysis** - Models, Portfolio, Analytics
- **Capital & Legal** - Funds, Debt, Legal
- **Data & Intelligence** - Market, Tax, PDF Extraction
- **Management & Reporting** - Projects, Reports, Integrations

### Step 3: Start Building
Each module provides comprehensive tools for its domain:
- **Forms** - Input data with validated forms
- **Calculators** - Run financial models and scenarios
- **Dashboards** - View analytics and KPIs
- **Exports** - Download reports and data

---

## API Usage (For Developers)

### Centralized API Client

```typescript
// Import once
import { apiClient } from '@/services/apiClient';

// GET request
const data = await apiClient.get('/financial-models/dcf');

// POST request
const created = await apiClient.post('/financial-models/dcf', {
  name: 'My DCF Model',
  ticker: 'AAPL',
});

// PUT request
const updated = await apiClient.put(`/financial-models/dcf/${id}`, {
  name: 'Updated Name',
});

// DELETE request
await apiClient.delete(`/financial-models/dcf/${id}`);
```

### Automatic Features
- Auth token automatically attached to all requests
- Company ID automatically included for proper data filtering
- Global error handling (401, 403, 404, 500)
- Request/response interceptors
- 30-second timeout

### Using Company Context

```typescript
import { useCompany } from '@/context/CompanyContext';

function MyComponent() {
  const { selectedCompany, companies, selectCompany } = useCompany();

  // Access selected company
  console.log(selectedCompany?.name);

  // List all companies
  console.log(companies);

  // Switch companies
  selectCompany(anotherCompany);
}
```

---

## Platform Statistics

- **18+ Platform Modules**
- **17+ Financial Models**
- **Multi-Company Support** with isolated data
- **Institutional-Grade** analysis and reporting
- **Real-time Updates** across all dashboards
- **Professional Exports** to PDF and Excel

---

## Tech Stack

### Backend
- **FastAPI** (Python) - High-performance async API
- **PostgreSQL** - Relational database with UUID keys
- **SQLAlchemy** - ORM with soft delete support
- **Alembic** - Database migrations
- **JWT Authentication** - Secure token-based auth

### Frontend
- **React 18** with TypeScript
- **Material-UI (MUI)** - Component library
- **React Router** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Context API** - State management

### Architecture
- **Multi-tenancy** - Row-level data isolation by company_id
- **Soft Deletes** - Data retained with deleted_at timestamps
- **Audit Trail** - created_at and updated_at on all records
- **Foreign Keys** - Referential integrity with CASCADE deletes

---

## Next Steps

1. **Update Remaining API Endpoints**
   - CRM endpoints (~47 endpoints)
   - Reports endpoints
   - Debt Management endpoints
   - Fund Management endpoints
   - See implementation guide in previous session

2. **Testing**
   - Multi-company data isolation
   - Cross-company access prevention
   - API client automatic filtering

3. **Documentation**
   - API documentation
   - User guides per module
   - Video tutorials

---

## Support

For questions or issues:
- GitHub: [Your Repo]
- Documentation: This guide
- Platform Version: 2.4.1

---

Last Updated: 2025-11-11
