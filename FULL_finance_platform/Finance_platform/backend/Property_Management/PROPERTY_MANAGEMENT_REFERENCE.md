# Property Management System - Quick Reference Guide

**Fast lookup for formulas, KPIs, and system details**

---

## 📊 Dashboard KPIs - Quick Reference

### Portfolio Summary

| Metric | Formula | Target |
|--------|---------|---------|
| **Total Properties** | `=COUNTA('Property Master'!B4:B1000)` | - |
| **Total Units** | `=SUM('Property Master'!H4:H1000)` | - |
| **Occupied Units** | `=SUM('Unit Inventory'!L4:L1000)` | - |
| **Physical Occupancy Rate** | `=Occupied/Total Units` | >95% |
| **Portfolio Value** | `=SUM('Property Master'!I4:I1000)` | - |
| **Total Equity** | `=SUM('ROI Analysis'!E4:E1000)` | - |

### Financial Performance (Monthly)

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **Gross Potential Rent** | `=SUM('Rent Roll'!J4:J1000)` | - |
| **Vacancy Loss** | `=SUM('Income Statement'!D4:D1000)` | <5% of GPR |
| **Effective Gross Income** | `=GPR + Other Income - Vacancy` | - |
| **Total Operating Expenses** | `=SUM('Income Statement'!H4:H1000)` | 40-50% of EGI |
| **Net Operating Income** | `=EGI - OpEx` | >0 |
| **Portfolio Cap Rate** | `=(NOI × 12) / Portfolio Value` | 5-8% |

### Key Alerts

| Alert | Formula | Action Threshold |
|-------|---------|------------------|
| **Leases Expiring in 60 Days** | `=COUNTIFS('Lease Schedule'!E4:E1000,"<="&(TODAY()+60),'Lease Schedule'!E4:E1000,">="&TODAY())` | Start renewals at 90 days |
| **Vacant Units** | `=COUNTIF('Unit Inventory'!E4:E1000,"Vacant")` | Keep <5% |
| **Open Maintenance** | `=COUNTIF('Maintenance Tracker'!G4:G1000,"Open")` | Prioritize emergencies |
| **Below Target Occupancy** | `=COUNTIF('ROI Analysis'!G4:G1000,"<0.9")` | Investigate if <90% |

---

## 🏢 Property-Level Formulas

### Income Statement

| Line Item | Formula | Notes |
|-----------|---------|-------|
| **Gross Potential Rent** | `=SUMIF('Rent Roll'!A:A,PropertyID,'Rent Roll'!J:J)` | Sum all scheduled rent |
| **Vacancy Loss** | `=SUMIFS('Unit Inventory'!I:I,'Unit Inventory'!A:A,PropertyID,'Unit Inventory'!E:E,"Vacant")` | Sum market rent of vacant units (negative) |
| **Effective Gross Income** | `=GPR + Other Income + Vacancy Loss` | Net realizable income |
| **Net Operating Income** | `=EGI - Total OpEx` | Before debt service |
| **Cash Flow Before Tax** | `=NOI - Debt Service` | Actual cash to equity |

### ROI Calculations

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Appreciation** | `=Current Value - Purchase Price` | Capital gain |
| **Total Return** | `=Appreciation + Cumulative Cash Flow` | Total profit |
| **Cash-on-Cash Return** | `=Annual Cash Flow / Total Equity` | Annual cash yield |
| **Total ROI** | `=Total Return / Total Equity` | Lifetime return |
| **IRR (Approximate)** | `=((Current Value + Annual CF) / Equity)^(1/Years) - 1` | Annualized return |
| **Years Held** | `=(TODAY() - Purchase Date) / 365` | Holding period |

### Unit-Level Calculations

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Occupied** | `=IF(Status="Occupied",1,0)` | Binary flag |
| **Days Vacant** | `=IF(Status="Vacant",TODAY()-LastOccupiedDate,0)` | Vacancy duration |
| **Loss-to-Lease** | `=Market Rent - Current Rent` | Opportunity to raise rent |
| **Occupancy Rate** | `=SUM(Occupied) / COUNT(Units)` | % leased |

---

## 💰 Financial Metrics - Industry Standards

### Occupancy Metrics

| Metric | Formula | Target | Industry Benchmark |
|--------|---------|---------|-------------------|
| **Physical Occupancy** | Occupied Units / Total Units | >95% | 90-95% |
| **Economic Occupancy** | Collected Rent / GPR | >93% | 88-93% |
| **Vacancy Rate** | 1 - Occupancy Rate | <5% | 5-10% |
| **Average Days Vacant** | Days Vacant / Vacant Units | <30 days | 30-60 days |

### Revenue Metrics

| Metric | Formula | Good | Excellent |
|--------|---------|------|-----------|
| **Rent Growth YoY** | (Current Rent - Prior Rent) / Prior Rent | 2-3% | >5% |
| **Rent Collection Rate** | Collected / Scheduled | >95% | >98% |
| **Loss-to-Lease %** | Total LTL / Total Market Rent | 3-5% | <3% |
| **Other Income %** | Other Income / Total Revenue | 3-5% | >5% |

### Expense Metrics

| Metric | Formula | Target Range | Notes |
|--------|---------|--------------|-------|
| **Operating Expense Ratio** | Total OpEx / EGI | 40-50% | Multifamily |
| **Maintenance per Unit** | Maintenance $ / Total Units | $500-1000/yr | Varies by age |
| **Property Tax Rate** | Taxes / Property Value | 0.5-2.5% | Varies by location |
| **Management Fee %** | Mgmt Fee / EGI | 5-10% | Varies by size |

### Return Metrics

| Metric | Formula | Good | Excellent | Notes |
|--------|---------|------|-----------|-------|
| **Cap Rate** | (NOI × 12) / Value | 5-7% | 7-10% | Higher = higher risk |
| **Cash-on-Cash** | Annual CF / Equity | 7-10% | >12% | Annual cash yield |
| **Total ROI** | Total Return / Equity | 15-20% | >25% | Lifetime return |
| **IRR** | Annualized return | 12-15% | >18% | Time-adjusted |
| **Debt Service Coverage** | NOI / Debt Service | >1.25 | >1.40 | Lender requirement |

---

## 📅 Lease Management - Risk Levels

### Expiration Risk Matrix

| Days Until Expiration | Risk Level | Action Required | Timeline |
|----------------------|------------|-----------------|----------|
| **<60 days** | CRITICAL | Contact tenant immediately | Start 90 days out |
| **60-120 days** | HIGH | Begin renewal process | Send renewal offer |
| **120-180 days** | MODERATE | Monitor and plan | Initial discussion |
| **180+ days** | LOW | Track only | No action yet |

### Lease Decision Tree

```
Lease Expiring?
├─ <60 days
│  ├─ Tenant wants to renew → Process renewal
│  ├─ Tenant leaving → Market unit immediately
│  └─ Uncertain → Offer incentive
├─ 60-120 days
│  ├─ Good tenant → Offer early renewal discount
│  ├─ Problem tenant → Plan to not renew
│  └─ Market rent tenant → Send renewal at market rate
└─ >120 days
   └─ Monitor only
```

---

## 🔧 Maintenance - Priority Matrix

### Priority Levels

| Priority | Response Time | Examples | Cost Impact |
|----------|--------------|----------|-------------|
| **Emergency** | <4 hours | No heat/AC, water leak, gas leak, security | High |
| **High** | <24 hours | Appliance broken, electrical issue, plumbing | Medium |
| **Medium** | 3-7 days | Minor repairs, cosmetic issues | Low |
| **Low** | 14-30 days | Preventive maintenance, upgrades | Variable |

### Category Benchmarks

| Category | % of Total Expenses | Notes |
|----------|-------------------|-------|
| Property Taxes | 20-30% | Fixed, location-dependent |
| Insurance | 5-10% | Varies by coverage |
| Utilities | 5-15% | If landlord-paid |
| Repairs & Maintenance | 15-25% | Age-dependent |
| Management | 5-10% | If third-party |
| Landscaping | 2-5% | Seasonal |
| Marketing | 1-3% | For vacancies |

---

## 📈 ROI Analysis - Comparison Framework

### Property Comparison Matrix

When comparing multiple properties:

| Metric | Weight | Use Case |
|--------|---------|----------|
| **Cash-on-Cash** | High | Current income |
| **IRR** | High | Time-adjusted returns |
| **Total ROI** | Medium | Lifetime performance |
| **Occupancy Rate** | High | Risk indicator |
| **Cap Rate** | Medium | Market comparison |
| **Appreciation %** | Medium | Market appreciation |

### Decision Rules

**When to hold:**
- Cash-on-Cash >8%
- Occupancy >90%
- Appreciation potential exists
- Below-market rents (LTL opportunity)

**When to sell:**
- Cash-on-Cash <5%
- Chronic occupancy issues
- Major CapEx needed
- Better opportunities available

**When to improve:**
- Loss-to-Lease >10%
- Below-market condition
- Renovation ROI >20%
- Can justify rent increase

---

## 🔢 Ownership Model Formulas

### Full Ownership

```
Total Return = Appreciation + Cumulative Cash Flow
ROI = Total Return / Total Equity Invested
Annual Return = Cash Flow + (Appreciation / Years Held)
```

### Master Lease

```
Monthly Profit = Total Sublease Rent - Master Lease Payment - Operating Costs
Annual ROI = (Annual Profit / Initial Capital) × 100
Break-Even Occupancy = Master Lease / (Total Units × Avg Rent per Unit)
```

### Rental Arbitrage (Airbnb)

```
Monthly Revenue = Nightly Rate × Avg Nights Booked × (1 - Platform Fee %)
Monthly Costs = Master Lease + Cleaning + Supplies + Platform Fees
Monthly Profit = Revenue - Costs
Break-Even Occupancy % = (Master Lease + Fixed Costs) / (Nightly Rate × 30)
```

### Sublease

```
Monthly Spread = Sublease Income - Master Rent Paid
Annual Cash Flow = Monthly Spread × 12
ROI = Annual CF / (Security Deposits + Improvements)
```

---

## 🎯 Performance Targets by Property Type

### Multifamily

| Metric | Target | Notes |
|--------|---------|-------|
| Occupancy | 95%+ | Industry standard |
| Turnover Rate | <30%/year | Stabilized properties |
| OpEx Ratio | 40-50% | Varies by location |
| Cap Rate | 5-7% | Core markets |
| Cash-on-Cash | 7-10% | Levered |

### Single Family Rental

| Metric | Target | Notes |
|--------|---------|-------|
| Occupancy | 98%+ | Low turnover |
| Maintenance | $100-150/mo | Age-dependent |
| OpEx Ratio | 30-40% | Lower than MF |
| Cap Rate | 6-8% | Varies widely |
| Cash-on-Cash | 8-12% | Higher leverage |

### Commercial Office

| Metric | Target | Notes |
|--------|---------|-------|
| Occupancy | 90%+ | Slower absorption |
| Lease Term | 3-5 years | Longer stability |
| OpEx Ratio | 25-35% | NNN structure |
| Cap Rate | 6-9% | Class dependent |
| WALT | 36+ months | Risk metric |

### Retail

| Metric | Target | Notes |
|--------|---------|-------|
| Occupancy | 92%+ | Traffic-dependent |
| Lease Term | 5-10 years | Long-term |
| OpEx Ratio | 20-30% | NNN common |
| Cap Rate | 7-10% | Higher risk |
| Tenant Credit | >BBB | Critical |

---

## 🔐 Color Coding Reference

### Text Colors

| Color | RGB | Meaning | Action |
|-------|-----|---------|--------|
| **Blue** | 0, 0, 255 | User inputs | Change these |
| **Black** | 0, 0, 0 | Formulas | Don't touch |
| **Green** | 0, 128, 0 | Cross-sheet links | Auto-updates |
| **Red** | 255, 0, 0 | External links | Verify source |

### Cell Backgrounds

| Color | RGB | Meaning | Action |
|-------|-----|---------|--------|
| **Yellow** | 255, 255, 0 | Important assumptions | Review carefully |
| **White** | 255, 255, 255 | Normal cells | Standard |
| **Light Blue** | 220, 230, 241 | Section headers | Informational |

### Cell Protection

| Type | Editable | Protection |
|------|----------|------------|
| Blue text | ✅ Yes | User can change |
| Black text | ❌ No | Formula cells |
| Green text | ❌ No | Linked cells |

---

## 📋 Sheet Reference - Quick Navigation

| Sheet Name | Purpose | Update Frequency | Key Users |
|------------|---------|------------------|-----------|
| **Dashboard** | Executive summary | Real-time | Everyone |
| **Property Master** | Property database | When adding properties | Property managers |
| **Ownership Models** | Ownership structures | At acquisition | Finance team |
| **Unit Inventory** | Unit-level tracking | When status changes | Leasing agents |
| **Rent Roll** | Tenant list | When leases change | Property managers |
| **Income Statement** | P&L by property | Monthly | Accountants |
| **Cash Flow** | Monthly cash tracking | Monthly | Finance team |
| **Lease Schedule** | Expiration tracking | Auto-updates | Leasing agents |
| **Maintenance Tracker** | Work orders | Daily | Maintenance team |
| **ROI Analysis** | Performance metrics | Quarterly | Executives |
| **Budget vs Actual** | Variance analysis | Monthly | Controllers |
| **Settings** | Assumptions | Quarterly | Analysts |

---

## 🔄 Monthly Checklist

### Day 1
- [ ] Update Rent Roll (new leases, move-outs)
- [ ] Update Unit Inventory (status changes)
- [ ] Enter prior month's expenses (Income Statement)

### Day 2-5
- [ ] Record actual rent collections (Cash Flow)
- [ ] Update Maintenance Tracker (close completed items)
- [ ] Review Budget vs Actual

### Day 6-10
- [ ] Review Dashboard alerts
- [ ] Check Lease Schedule for expirations
- [ ] Follow up on CRITICAL risk leases

### Mid-Month
- [ ] Review occupancy rates
- [ ] Update property values (if changes)
- [ ] Process maintenance invoices

### Month-End
- [ ] Finalize all expense entries
- [ ] Generate reports
- [ ] Archive month-end file
- [ ] Plan for next month

---

## ⚠️ Common Formula Errors

### #REF! Error
**Cause:** Cell reference deleted or moved  
**Fix:** Restore deleted cells or update formula

### #DIV/0! Error
**Cause:** Division by zero (empty denominator)  
**Fix:** Add IF statement: `=IF(denominator>0,numerator/denominator,0)`

### #VALUE! Error
**Cause:** Wrong data type (text in number formula)  
**Fix:** Check for text in numeric cells, use VALUE() function

### #N/A Error
**Cause:** Lookup value not found  
**Fix:** Add IFERROR wrapper: `=IFERROR(VLOOKUP(...),0)`

### #NAME? Error
**Cause:** Excel doesn't recognize formula name  
**Fix:** Check spelling, ensure no spaces in formula

---

## 📞 Quick Support Reference

### For Technical Issues
- Formula errors → See formula reference above
- Calculation issues → Check Excel calculation mode (File → Options → Formulas → Automatic)
- Formatting issues → Reapply from Settings sheet

### For Financial Questions
- ROI calculation → See ROI Analysis formulas
- Occupancy metrics → See Financial Metrics section
- Industry benchmarks → See Performance Targets section

### For Integration
- Database export → See README.md
- API endpoints → See Portfolio Dashboard docs
- Data migration → See Implementation Plan

---

## 📊 Excel Tips

### Keyboard Shortcuts

| Action | Windows | Mac |
|--------|---------|-----|
| Calculate now | F9 | ⌘= |
| Go to cell | Ctrl+G | ⌘G |
| Find | Ctrl+F | ⌘F |
| Sort | Alt+D+S | N/A |
| Filter | Ctrl+Shift+L | ⌘⇧F |
| Insert row | Ctrl+Shift++ | ⌘⇧+ |

### Power Features

**Named Ranges:**
- Define key cells with names
- Use names in formulas for clarity
- Example: `=PropertyValue / TotalEquity`

**Conditional Formatting:**
- Highlight based on values
- Example: Red if Days Vacant > 30
- Example: Green if Cash-on-Cash > 10%

**Data Validation:**
- Create dropdown lists
- Prevent invalid entries
- Example: Status field → "Occupied, Vacant, Under Renovation"

---

## 📖 Glossary

| Term | Definition |
|------|------------|
| **Cap Rate** | Net Operating Income / Property Value (annual return without financing) |
| **Cash-on-Cash** | Annual Cash Flow / Equity Invested (annual cash yield) |
| **DSCR** | Debt Service Coverage Ratio (NOI / Debt Service) |
| **EGI** | Effective Gross Income (GPR - Vacancy + Other Income) |
| **GPR** | Gross Potential Rent (maximum rent if 100% occupied) |
| **IRR** | Internal Rate of Return (time-weighted annual return) |
| **Loss-to-Lease** | Gap between market rent and in-place rent |
| **NOI** | Net Operating Income (EGI - Operating Expenses) |
| **OpEx** | Operating Expenses (all costs except debt service) |
| **WALT** | Weighted Average Lease Term (average time remaining on leases) |

---

**💡 Pro Tip:** Bookmark this page for quick reference while using the system!
