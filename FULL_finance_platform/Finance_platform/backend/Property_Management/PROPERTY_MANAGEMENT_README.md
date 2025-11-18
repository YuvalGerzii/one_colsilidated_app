# Property Management System - Excel Template

**Version:** 1.0  
**Date:** November 2025  
**Author:** Portfolio Dashboard Team  
**File:** Property_Management_System.xlsx

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What This System Does](#what-this-system-does)
3. [Key Features](#key-features)
4. [System Architecture](#system-architecture)
5. [Sheet-by-Sheet Guide](#sheet-by-sheet-guide)
6. [Getting Started](#getting-started)
7. [Integration with Portfolio Dashboard](#integration-with-portfolio-dashboard)
8. [Best Practices](#best-practices)
9. [Maintenance & Updates](#maintenance--updates)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The **Property Management System** is a comprehensive Excel template designed for private equity firms, real estate investors, and property managers to track and analyze their property portfolios. This institutional-grade tool supports multiple ownership models (full ownership, master lease, sublease, Airbnb/rental arbitrage, and more) and provides real-time performance analytics.

### What Makes This Different

Unlike basic property tracking spreadsheets, this system:
- **Supports multiple ownership models** (own, lease, sublease, Airbnb, etc.)
- **Tracks both inventory and operations** (vacant units, maintenance, leases)
- **Calculates sophisticated ROI metrics** (IRR, cash-on-cash, NOI)
- **Integrates with existing Portfolio Dashboard** (feeds into your PE platform)
- **Provides actionable alerts** (expiring leases, vacant units, maintenance)

---

## What This System Does

### Core Capabilities

**1. Portfolio Management**
- Track unlimited properties across multiple asset classes
- Support for 7+ ownership models (full ownership, master lease, sublease, Airbnb, etc.)
- Monitor property values, equity, and appreciation

**2. Unit-Level Tracking**
- Individual unit inventory (bed/bath, sq ft, status)
- Vacant vs. occupied tracking
- Days vacant and renovation budgets
- Market rent vs. in-place rent (loss-to-lease)

**3. Financial Operations**
- Monthly income statements by property
- Rent roll management
- Cash flow tracking (monthly and annual)
- Budget vs. actual variance analysis

**4. Lease Management**
- Complete lease schedule with expiration tracking
- Automated risk flagging (60/120/180 day alerts)
- Renewal probability analysis
- Security deposit tracking

**5. Maintenance Operations**
- Work order tracking
- Vendor management
- Cost tracking by category
- Status monitoring (open/in progress/completed)

**6. ROI Analytics**
- Cash-on-Cash returns
- Total ROI with appreciation
- Approximate IRR calculation
- Comparison across properties

**7. Executive Dashboard**
- Real-time portfolio summary
- Key performance indicators (KPIs)
- Critical alerts and action items
- Occupancy and financial metrics

---

## Key Features

### Multi-Model Ownership Support

The system tracks these ownership structures:

| Model | Use Case | Key Metrics |
|-------|----------|-------------|
| **Full Ownership** | Traditional buy-and-hold | Equity, appreciation, NOI |
| **Master Lease** | Lease entire building, sublease units | Spread between master lease & sublease income |
| **Sublease** | Rent from tenant, re-lease to others | Profit margin, landlord approval |
| **Rental Arbitrage** | Lease long-term, Airbnb short-term | Occupancy %, nightly rate, profit margin |
| **Joint Venture** | Partnership structure | Equity split, waterfall returns |
| **Management Only** | Third-party management | Management fee %, no capital at risk |
| **Ground Lease** | Own building, lease land | Ground rent, improvement ownership |

### Automated Calculations

**All formulas are built-in:**
- Occupancy rates (physical & economic)
- NOI and cash flow by property
- Portfolio-level aggregation
- Lease expiration risk scoring
- Budget variance analysis
- ROI metrics (CoC, IRR, total return)

### Color-Coded System

Following institutional standards:
- **Blue Text** = User inputs (change these)
- **Black Text** = Formulas (auto-calculated)
- **Green Text** = Cross-sheet links (pull from other sheets)
- **Yellow Background** = Important assumptions (review carefully)

---

## System Architecture

### Data Flow

```
Property Master (source of truth)
    ↓
Unit Inventory → Rent Roll → Income Statement → ROI Analysis
    ↓                ↓              ↓
Ownership Models  Lease Schedule  Budget vs Actual
    ↓
Dashboard (aggregates all data)
```

### Key Relationships

- **One Property** → Many Units
- **One Unit** → One Active Lease (if occupied)
- **One Lease** → Pulls from Unit Inventory
- **All Sheets** → Feed into Dashboard

---

## Sheet-by-Sheet Guide

### 1. Dashboard (Executive Summary)

**Purpose:** Real-time portfolio snapshot

**Key Metrics:**
- Total properties, units, occupancy rate
- Portfolio value and equity invested
- Monthly financial performance (GPR, EGI, NOI)
- Portfolio cap rate
- Critical alerts (expiring leases, vacancies, maintenance)

**Usage:** Start here every day to check portfolio health

---

### 2. Property Master (Property Database)

**Purpose:** Master list of all properties

**Key Fields:**
- Property ID (unique identifier)
- Name, address, city, state
- Property type (multifamily, commercial, etc.)
- Ownership model
- Total units
- Purchase price, date, current value
- Status (active, under contract, sold)

**Usage:** Add new properties here first

**Tips:**
- Use consistent Property IDs (e.g., PROP-001, PROP-002)
- Update current value quarterly
- Mark sold properties as "Sold" but keep for historical tracking

---

### 3. Ownership Models (Ownership Tracking)

**Purpose:** Track how each property is held/operated

**Key Fields:**
- Property ID and name (links to Property Master)
- Ownership type (from Settings dropdown)
- Details (description of structure)
- Master lease amount (if applicable)
- Lease start/end dates
- Landlord approval status
- Special terms and profit split %

**Usage:** Document complex ownership structures

**Example Use Cases:**
- **Rental Arbitrage:** Master lease = $3,000/mo, sublease to Airbnb at average $150/night
- **Master Lease:** Lease building for $50K/mo, sublease units for $60K/mo total
- **Full Ownership:** Document all equity investors and ownership %

---

### 4. Unit Inventory (Unit-Level Tracking)

**Purpose:** Track every rentable unit/space

**Key Fields:**
- Property ID (links to Property Master)
- Unit number (e.g., 1A, 2B, Suite 300)
- Unit type (1BR/1BA, office, retail)
- Status (occupied, vacant, under renovation, off-market)
- Beds, baths, square footage
- Market rent (what you could charge)
- Current rent (what tenant pays, or $0 if vacant)
- Tenant name
- Days vacant
- Renovation budget

**Usage:** Update status when units turn over

**Key Formulas:**
- **Occupied** = Calculates if status = "Occupied"
- **Days Vacant** = Auto-calculates if vacant

**Tips:**
- Update market rent quarterly based on comps
- Track renovation budgets for value-add analysis
- Use "Off-Market" for units held for personal use

---

### 5. Rent Roll (Tenant Roster)

**Purpose:** Current tenant list and lease terms

**Key Fields:**
- Property ID, unit number
- Tenant name
- Lease start and end dates
- Monthly rent
- Security deposit
- Credit score
- Annual rent (auto-calculated)
- Lease status

**Usage:** Central record of all active leases

**Key Formulas:**
- **Annual Rent** = Monthly Rent × 12
- **Totals Row** = Sums all rents for portfolio

**Tips:**
- Update when leases renew
- Remove tenants who move out
- Keep security deposits current

---

### 6. Income Statement (P&L by Property)

**Purpose:** Monthly financial performance

**Key Fields:**
- Gross Potential Rent (from Rent Roll)
- Vacancy Loss (from vacant units)
- Other Income (parking, laundry, pet fees)
- Effective Gross Income (GPR + other - vacancy)
- Operating Expenses (by category)
- Total OpEx
- Net Operating Income (EGI - OpEx)
- Debt Service (mortgage payment)
- Cash Flow Before Tax (NOI - debt service)

**Usage:** Monthly financial reporting

**Key Formulas:**
- **GPR** = SUMIF from Rent Roll
- **Vacancy Loss** = Sum of market rents for vacant units
- **EGI** = GPR + Other Income - Vacancy
- **NOI** = EGI - Total OpEx
- **Cash Flow** = NOI - Debt Service

**Tips:**
- Enter operating expenses monthly
- Update "Other Income" for ancillary revenue
- Compare NOI to budget (see Budget vs Actual sheet)

---

### 7. Cash Flow (Monthly Tracking)

**Purpose:** Track cash in/out by month

**Key Fields:**
- Property ID
- Monthly columns (Jan-Dec)
- Annual total (auto-calculated)

**Usage:** Cash flow forecasting and tracking

**Tips:**
- Enter actual rent collections (not just scheduled rent)
- Track seasonal patterns for Airbnb properties
- Compare actual vs. pro forma

---

### 8. Lease Schedule (Expiration Tracking)

**Purpose:** Monitor lease expirations and renewal risk

**Key Fields:**
- Property, unit, tenant (links from Rent Roll)
- Lease end date
- Days until expiration (auto-calculated)
- Monthly and annual rent
- Renewal probability (your estimate)
- Risk level (CRITICAL/HIGH/MODERATE/LOW)
- Action required (automated recommendation)

**Usage:** Proactive lease management

**Key Formulas:**
- **Days Until Expiration** = Lease End - TODAY()
- **Risk Level:**
  - <60 days = CRITICAL
  - 60-120 days = HIGH
  - 120-180 days = MODERATE
  - 180+ days = LOW
- **Action Required:**
  - <60 days = "Contact Tenant"
  - 60-120 days = "Start Renewal Process"
  - 180+ days = "Monitor"

**Tips:**
- Review weekly for CRITICAL and HIGH risk leases
- Start renewal conversations 90-120 days out
- Track renewal probability based on tenant satisfaction

---

### 9. Maintenance Tracker (Work Orders)

**Purpose:** Track maintenance requests and costs

**Key Fields:**
- Request ID (unique identifier)
- Property, unit
- Category (plumbing, electrical, HVAC, etc.)
- Description
- Status (open, in progress, completed)
- Priority (emergency, high, medium, low)
- Date reported and completed
- Cost
- Vendor
- Notes

**Usage:** Centralized maintenance management

**Tips:**
- Update status as work progresses
- Track costs for budget variance analysis
- Use priority field to triage requests
- Create recurring entries for preventive maintenance

---

### 10. ROI Analysis (Performance Metrics)

**Purpose:** Calculate returns by property

**Key Fields:**
- Property ID and name
- Ownership model
- Purchase price
- Total equity (your investment)
- Current value
- Annual NOI (from Income Statement)
- Annual cash flow (NOI - debt service)
- Appreciation (current value - purchase price)
- Total return (appreciation + cumulative cash flow)
- **Cash-on-Cash Return** (annual CF / equity)
- **ROI** (total return / equity)
- **IRR (approximate)** (annualized return)
- Years held

**Usage:** Compare property performance

**Key Formulas:**
- **Appreciation** = Current Value - Purchase Price
- **Cash-on-Cash** = Annual Cash Flow / Total Equity
- **ROI** = Total Return / Total Equity
- **IRR (Approx)** = ((Current Value + Annual CF) / Equity)^(1/Years) - 1

**Tips:**
- Update current values quarterly (appraisals or comps)
- Use IRR to compare properties held different lengths of time
- Sort by Cash-on-Cash to identify best performers

---

### 11. Budget vs Actual (Variance Analysis)

**Purpose:** Track spending against budget

**Key Fields:**
- Property ID
- Expense category
- Budget (monthly)
- Actual (monthly)
- Variance $ (actual - budget)
- Variance % (variance / budget)
- YTD budget, actual, variance
- Status (on track, under budget, over budget)

**Usage:** Control costs and identify issues

**Key Formulas:**
- **Variance $** = Actual - Budget
- **Variance %** = Variance $ / Budget
- **YTD** = Monthly × 12
- **Status:**
  - <5% variance = "On Track"
  - Negative variance = "Under Budget"
  - Positive variance = "Over Budget"

**Tips:**
- Set realistic budgets based on historical data
- Investigate variances >10%
- Update budgets annually

---

### 12. Settings (Configuration)

**Purpose:** Global assumptions and reference data

**Key Sections:**

**Global Assumptions** (Yellow highlighted - review carefully):
- Default vacancy rate (5%)
- Target occupancy rate (95%)
- Annual rent growth (3%)
- Maintenance reserve (5% of rent)
- Management fee (8%)
- Default cap rate (6%)

**Property Types:**
- Multifamily
- Single Family
- Commercial Office
- Retail
- Industrial
- Mixed-Use
- Hotel/Hospitality

**Ownership Models:**
- Full Ownership
- Master Lease
- Sublease
- Rental Arbitrage (Airbnb/VRBO)
- Joint Venture
- Management Contract Only
- Ground Lease

**Color Coding Legend:**
- Explanation of blue/black/green/yellow color system

**Usage:**
- Review assumptions quarterly
- Use dropdown lists from Settings (in future versions)
- Adjust assumptions for market changes

---

## Getting Started

### Quick Start (5 Minutes)

1. **Open the file:** Property_Management_System.xlsx
2. **Go to Property Master:** Add your first property
   - Enter Property ID (e.g., PROP-001)
   - Fill in basic info (name, address, type)
   - Enter purchase price and date
3. **Go to Unit Inventory:** Add units
   - Enter each unit number
   - Set status (occupied/vacant)
   - Enter market rents
4. **Go to Rent Roll:** Add tenants (if occupied)
   - Enter tenant names
   - Enter lease dates and monthly rent
5. **Go to Dashboard:** See your portfolio summary!

### Full Setup (30 Minutes)

**Step 1: Configure Settings**
- Review global assumptions
- Adjust for your market (vacancy rate, rent growth, etc.)

**Step 2: Add All Properties**
- Property Master sheet
- One row per property
- Use consistent naming (PROP-001, PROP-002, etc.)

**Step 3: Document Ownership**
- Ownership Models sheet
- Specify how each property is held
- Add master lease details if applicable

**Step 4: Add All Units**
- Unit Inventory sheet
- One row per rentable unit
- Include vacant and off-market units

**Step 5: Add Active Leases**
- Rent Roll sheet
- Only for currently occupied units
- Include all lease terms

**Step 6: Enter Financials**
- Income Statement: Enter monthly operating expenses
- Budget vs Actual: Set expense budgets

**Step 7: Add Maintenance History**
- Maintenance Tracker
- Optional: Add recent work orders

**Step 8: Review Dashboard**
- Check all calculations
- Verify formulas are pulling correctly
- Note any alerts

---

## Integration with Portfolio Dashboard

This Excel template is designed to integrate with the **Portfolio Company Dashboard** platform:

### Export to Database

Key tables for integration:
- `properties` table ← Property Master sheet
- `units` table ← Unit Inventory sheet
- `leases` table ← Rent Roll sheet
- `transactions` table ← Income Statement + Cash Flow
- `work_orders` table ← Maintenance Tracker
- `roi_metrics` table ← ROI Analysis sheet

### Data Flow

```
Excel Template
    ↓ (CSV export or API)
PostgreSQL Database
    ↓
Portfolio Dashboard Backend (FastAPI)
    ↓
React Frontend Dashboard
```

### Integration Benefits

- **Real-time dashboards** in web interface
- **Portfolio-level aggregation** across all companies
- **LP reporting automation**
- **Mobile access** via web app
- **Multi-user access** with permissions
- **Historical tracking** in database

### Next Steps

See `Portfolio_Dashboard_Implementation_Plan.md` for:
- Database schema details
- API endpoint specifications
- Frontend component architecture

---

## Best Practices

### Data Entry

**Do:**
- ✅ Use consistent Property IDs (PROP-001, PROP-002)
- ✅ Update Dashboard frequently (weekly at minimum)
- ✅ Enter actual data, not projections (except in Budget)
- ✅ Review lease schedule weekly
- ✅ Document ownership structures in Ownership Models
- ✅ Keep current value estimates updated quarterly

**Don't:**
- ❌ Delete formulas (blue = inputs, black = formulas)
- ❌ Skip unit inventory (even for vacant units)
- ❌ Forget to update lease expirations
- ❌ Mix properties (one property per row)
- ❌ Use different units (always monthly for Income Statement)

### Formula Protection

**Critical Rules:**
- **NEVER delete black or green text** (these are formulas)
- **ONLY change blue text** (these are inputs)
- If a formula breaks, restore from backup
- Use "Undo" immediately if you delete a formula

### Monthly Routine

**Day 1 of Month:**
1. Update Rent Roll (new leases, move-outs)
2. Update Unit Inventory (status changes)
3. Enter previous month's actual expenses (Income Statement)
4. Record rent collections (Cash Flow)
5. Update maintenance tracker (close completed requests)

**Mid-Month:**
1. Review Lease Schedule for upcoming expirations
2. Check vacancy alerts on Dashboard
3. Review maintenance requests (prioritize emergencies)

**End of Month:**
1. Finalize expenses (Budget vs Actual)
2. Generate monthly reports
3. Update property values (if new appraisals)

### Quarterly Tasks

1. **Update market rents** (Unit Inventory)
2. **Update property values** (Property Master)
3. **Review assumptions** (Settings sheet)
4. **Conduct portfolio review** (ROI Analysis)
5. **Budget adjustment** (Budget vs Actual)

---

## Maintenance & Updates

### Version Control

**Recommended approach:**
- Save monthly backups: `Property_Management_System_2025-11.xlsx`
- Keep master version for current month
- Archive old versions for historical reference

### Adding Properties

**To add a new property:**
1. Go to Property Master
2. Copy row 4 (or last property row)
3. Paste in next empty row
4. Update all blue fields
5. Verify formulas copied correctly
6. Add units to Unit Inventory
7. Document ownership in Ownership Models

### Removing Properties

**When selling a property:**
- DO NOT delete the row
- Change status to "Sold"
- Update "Current Value" to sale price
- Move to bottom of sheet (optional)
- Keep for historical ROI tracking

### Expanding the System

**Can be extended with:**
- Additional property types (Student Housing, Storage)
- More detailed expense categories
- Tenant payment tracking
- Vendor database
- Document links (lease PDFs, inspection reports)
- Capital expenditure tracking
- Debt schedule management

---

## Troubleshooting

### Common Issues

**Problem:** Dashboard shows #REF! error  
**Solution:** Check that Property Master has at least one property

**Problem:** Totals seem wrong  
**Solution:** Verify all Property IDs match across sheets (case-sensitive)

**Problem:** Lease Schedule shows negative days  
**Solution:** Leases have expired; update or remove from Rent Roll

**Problem:** Occupancy rate shows >100%  
**Solution:** Check Unit Inventory - more occupied than total units

**Problem:** ROI calculations seem off  
**Solution:** Verify Total Equity in ROI Analysis matches actual investment

**Problem:** Formulas not calculating  
**Solution:** Check Excel calculation mode (should be Automatic)

### Formula Reference

**If you need to rebuild a formula:**

**Dashboard Metrics:**
```excel
Total Properties = =COUNTA('Property Master'!B4:B1000)
Total Units = =SUM('Property Master'!H4:H1000)
Occupied Units = =SUM('Unit Inventory'!L4:L1000)
Physical Occupancy = =IF(D6>0,D7/D6,0)
```

**Income Statement:**
```excel
GPR = =SUMIF('Rent Roll'!A:A,A4,'Rent Roll'!J:J)
Vacancy Loss = =SUMIFS('Unit Inventory'!I:I,'Unit Inventory'!A:A,A4,'Unit Inventory'!E:E,"Vacant")
EGI = =C4+D4+E4
NOI = =F4-H4
Cash Flow = =I4-J4
```

**ROI Analysis:**
```excel
Cash-on-Cash = =IF(E4>0,H4/E4,0)
ROI = =IF(E4>0,J4/E4,0)
IRR (Approx) = =IF(E4>0,(POWER((F4+H4)/E4,1/N4)-1),0)
```

### Getting Help

**For technical questions:**
- Review this README
- Check User Guide (PROPERTY_MANAGEMENT_USER_GUIDE.md)
- Check Reference Guide (PROPERTY_MANAGEMENT_REFERENCE.md)

**For integration with Portfolio Dashboard:**
- See Portfolio_Dashboard_Implementation_Plan.md
- Review DATABASE_SCHEMA.md

---

## Technical Specifications

### File Format

- **Format:** Excel 2007+ (.xlsx)
- **Sheets:** 12
- **Formulas:** 460+
- **Maximum Properties:** 997 (rows 4-1000)
- **Maximum Units:** 997 per property
- **Color Standard:** Institutional (blue inputs, black formulas, green links)

### Performance

- **File Size:** ~500 KB (empty template)
- **Calculation Speed:** <1 second for 50 properties
- **Recommended Limits:**
  - Up to 100 properties: Excellent performance
  - 100-500 properties: Good performance
  - 500+ properties: Consider database solution

### Compatibility

- **Excel:** 2016 or later (Windows/Mac)
- **Google Sheets:** Limited (some formulas may not work)
- **LibreOffice Calc:** Fully compatible
- **Numbers (Mac):** Limited (formatting may vary)

---

## License & Credits

**Author:** Portfolio Dashboard Team  
**License:** Proprietary - For use by license holders only  
**Version:** 1.0  
**Last Updated:** November 2025

**Part of the Portfolio Dashboard ecosystem:**
- DCF Model
- LBO Model
- Merger Model
- Due Diligence Tracker
- Quality of Earnings Analysis
- **→ Property Management System** (this file)

---

## Changelog

### Version 1.0 (November 2025)
- Initial release
- 12 sheets with 460+ formulas
- Support for 7 ownership models
- Comprehensive ROI analytics
- Integration-ready for Portfolio Dashboard

---

## Next Steps

1. **Start using the template** - Add your first property
2. **Customize assumptions** - Update Settings sheet for your market
3. **Review regularly** - Make it part of your weekly routine
4. **Plan integration** - Consider connecting to Portfolio Dashboard
5. **Provide feedback** - Help us improve future versions

**Questions?** See the User Guide and Reference Guide for additional help.

---

**Happy Property Managing! 🏢📊**
