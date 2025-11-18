# Property Management System - User Guide

**A practical guide to managing your property portfolio with Excel**

---

## 📘 Quick Navigation

- [Getting Started](#getting-started) - First 15 minutes
- [Daily Operations](#daily-operations) - What to do each day
- [Adding Properties](#adding-properties) - Step-by-step
- [Managing Tenants](#managing-tenants) - Leases and rent roll
- [Financial Tracking](#financial-tracking) - Income and expenses
- [Analyzing Performance](#analyzing-performance) - ROI and metrics
- [Common Scenarios](#common-scenarios) - Real-world examples

---

## Getting Started

### Your First 15 Minutes

**Goal:** Add one property and see it on the Dashboard

#### Step 1: Open the File
- Open `Property_Management_System.xlsx`
- Don't worry about the formulas - just enter data in blue text

#### Step 2: Add Your First Property
Go to the **Property Master** sheet:

1. **Row 4** is a sample - you can overwrite it
2. Enter your property details:
   - **Property ID:** Give it a unique code (e.g., "MAIN-APT")
   - **Property Name:** The name you'll use (e.g., "Main Street Apartments")
   - **Address:** Full street address
   - **City, State:** Location
   - **Type:** Multifamily, Commercial Office, etc.
   - **Ownership Model:** How you own it (see [Ownership Models](#ownership-models))
   - **Total Units:** How many rentable spaces
   - **Purchase Price:** What you paid (or current market value if you don't own)
   - **Purchase Date:** When you acquired it
   - **Current Value:** Today's estimated value
   - **Status:** Usually "Active"

**Example:**
```
Property ID: MAPLE-001
Property Name: Maple Apartments
Address: 123 Maple Street
City: Portland
State: OR
Type: Multifamily
Ownership Model: Full Ownership
Total Units: 24
Purchase Price: $3,000,000
Purchase Date: 01/15/2023
Current Value: $3,200,000
Status: Active
```

#### Step 3: Add One Unit
Go to the **Unit Inventory** sheet:

1. Enter the property ID you just created
2. Fill in unit details:
   - **Unit Number:** How you identify it (e.g., "1A", "101", "Suite 200")
   - **Unit Type:** Description (e.g., "1BR/1BA", "Office")
   - **Status:** Occupied or Vacant
   - **Beds, Baths:** Number of bedrooms and bathrooms
   - **Sq Ft:** Square footage
   - **Market Rent:** What you could charge today
   - **Current Rent:** What tenant pays (or $0 if vacant)

**Example:**
```
Property ID: MAPLE-001
Unit Number: 1A
Unit Type: 1BR/1BA
Status: Occupied
Beds: 1
Baths: 1
Sq Ft: 650
Market Rent: $2,500
Current Rent: $2,400
Tenant Name: John Smith
```

#### Step 4: Check the Dashboard
Go to the **Dashboard** sheet:
- You should see your property counted
- Total units should show 1
- Financial metrics will calculate automatically

**🎉 Congratulations!** You've added your first property.

---

## Daily Operations

### Morning Routine (5 minutes)

1. **Open Dashboard**
   - Check "KEY ALERTS" section
   - Note any leases expiring soon
   - Check vacant units count
   - Review open maintenance requests

2. **Review Lease Schedule**
   - Go to Lease Schedule sheet
   - Sort by "Days Until Expiration"
   - Take action on anything marked "CRITICAL"

3. **Check Maintenance**
   - Go to Maintenance Tracker
   - Follow up on "Open" requests
   - Update status for completed work

### Weekly Tasks (30 minutes)

**Monday:**
- Review Dashboard alerts
- Update any lease changes from weekend
- Process new maintenance requests

**Wednesday:**
- Review Budget vs Actual
- Check for properties over budget
- Investigate variances >10%

**Friday:**
- Update Maintenance Tracker
- Close completed work orders
- Enter costs for completed work
- Review upcoming lease expirations (60-day window)

---

## Adding Properties

### Scenario: You Just Bought a New Building

**Property:** Oak Plaza, a 12-unit apartment building  
**Purchase Price:** $1,800,000  
**Your Equity:** $450,000 (25% down)  
**Occupied Units:** 10 of 12

#### Step 1: Property Master Sheet

Add the building:
```
Property ID: OAK-001
Property Name: Oak Plaza
Address: 456 Oak Avenue
City: Denver
State: CO
Type: Multifamily
Ownership Model: Full Ownership
Total Units: 12
Purchase Price: $1,800,000
Purchase Date: [Today's date]
Current Value: $1,800,000
Status: Active
```

#### Step 2: Ownership Models Sheet

Document the financing:
```
Property ID: OAK-001
Property Name: [Will auto-link from Property Master]
Ownership Type: Full Ownership
Details: 75% financed, 25% equity
Master Lease Amount: [Leave blank]
Special Terms: 30-year mortgage, 5.5% interest
```

#### Step 3: Unit Inventory Sheet

Add all 12 units (one row per unit):

**Occupied units (10):**
```
Property ID: OAK-001
Unit Number: 101
Unit Type: 2BR/1BA
Status: Occupied
Beds: 2
Baths: 1
Sq Ft: 850
Market Rent: $1,800
Current Rent: $1,750
Tenant Name: [Tenant's name]
```

Repeat for units 102, 103, 201, 202, 203, 301, 302, 303, 304

**Vacant units (2):**
```
Property ID: OAK-001
Unit Number: 401
Unit Type: 2BR/1BA
Status: Vacant
Beds: 2
Baths: 1
Sq Ft: 850
Market Rent: $1,800
Current Rent: $0
Days Vacant: 15
Renovation Budget: $2,500
```

Repeat for unit 402

#### Step 4: Rent Roll Sheet

Add the 10 occupied leases:
```
Property ID: OAK-001
Unit: 101
Tenant Name: [Name]
Lease Start: 03/01/2024
Lease End: 02/28/2025
Monthly Rent: $1,750
Security Deposit: $1,750
Credit Score: 720
[Other fields auto-calculate]
```

Repeat for remaining 9 occupied units

#### Step 5: Income Statement

Add monthly expenses:
```
Property ID: OAK-001
Property Name: [Auto-links]
Gross Potential Rent: [Auto-calculates from Rent Roll]
Vacancy Loss: [Auto-calculates from vacant units]
Other Income: 300 (laundry & parking)
Operating Expenses: 4,500 (all expenses)
Debt Service: 8,500 (monthly mortgage)
```

#### Step 6: ROI Analysis

Document your investment:
```
Property ID: OAK-001
Ownership Model: [Auto-links]
Purchase Price: [Auto-links]
Total Equity: $450,000 (your down payment)
Current Value: [Auto-links]
[All other fields auto-calculate]
```

#### Step 7: Verify on Dashboard

Go back to Dashboard:
- Total Properties should increase by 1
- Total Units should increase by 12
- Occupied Units should increase by 10
- Physical Occupancy Rate should update
- Portfolio Value should include $1,800,000

---

## Managing Tenants

### Scenario: New Tenant Move-In

**Unit:** 401 at Oak Plaza (previously vacant)  
**Tenant:** Jane Doe  
**Move-In Date:** December 1  
**Rent:** $1,800/month

#### Step 1: Update Unit Inventory
Go to Unit Inventory, find unit 401:
- Change **Status** from "Vacant" to "Occupied"
- Update **Current Rent** to $1,800
- Update **Tenant Name** to "Jane Doe"
- Clear **Days Vacant** (will auto-calculate to 0)
- Clear **Renovation Budget** if renovations done

#### Step 2: Add to Rent Roll
Go to Rent Roll, add new row:
```
Property ID: OAK-001
Unit: 401
Tenant Name: Jane Doe
Lease Start: 12/01/2025
Lease End: 11/30/2026
Monthly Rent: $1,800
Security Deposit: $1,800
Credit Score: 740
```

#### Step 3: Verify Calculations
- Income Statement should show reduced vacancy loss
- Lease Schedule will auto-populate with new lease
- Dashboard occupancy rate should increase

### Scenario: Tenant Move-Out

**Unit:** 101 at Oak Plaza  
**Tenant:** Moving out  
**Move-Out Date:** January 31

#### Step 1: Remove from Rent Roll
- Go to Rent Roll
- Find the tenant's row
- Delete the entire row (or mark as inactive)

#### Step 2: Update Unit Inventory
- Go to Unit Inventory, find unit 101
- Change **Status** to "Vacant"
- Update **Current Rent** to $0
- Clear **Tenant Name**
- **Days Vacant** will start counting automatically

#### Step 3: Plan Renovation (if needed)
- Enter **Renovation Budget** if unit needs work
- Change **Status** to "Under Renovation" if extensive work

---

## Financial Tracking

### Monthly Close Process

**Do this on the 1st of each month for the previous month's data**

#### Step 1: Update Rent Collections (Cash Flow Sheet)

Go to Cash Flow sheet:
- Find your property row
- Enter actual rent collected in the previous month's column
- Example: If November, enter October's collections

**Tip:** Enter actual collections, not scheduled rent
- If tenant pays late, show it in the month received
- If tenant doesn't pay, show $0

#### Step 2: Enter Operating Expenses (Income Statement)

Go to Income Statement:
- Find your property
- Update **Operating Expenses** with actual total
- This is your monthly OpEx (all categories combined)

**Common expense categories:**
- Property taxes
- Insurance
- Utilities (if you pay)
- Repairs & maintenance
- Property management fees
- Landscaping
- Snow removal
- Pest control
- HOA fees

#### Step 3: Update Budget vs Actual

Go to Budget vs Actual:
- Enter **Actual** expenses by category
- Compare to **Budget**
- Note any variances >10%

**Example:**
```
Property ID: OAK-001
Category: Maintenance
Budget: $1,200
Actual: $1,850
Variance: $650 (54% over budget)
Status: Over Budget
```

Investigate why maintenance was over budget

#### Step 4: Update Maintenance Costs

Go to Maintenance Tracker:
- Find completed work orders
- Enter **Cost** for each
- Change **Status** to "Completed"
- Enter **Date Completed**

---

## Analyzing Performance

### Monthly Performance Review

**Do this monthly to track portfolio health**

#### Step 1: Review Dashboard Metrics

Go to Dashboard:

**Check Occupancy:**
- Target: 95%
- If below 90%, investigate why
- Are units priced correctly?
- Is marketing effective?

**Check Financial Performance:**
- Is NOI positive and growing?
- Is portfolio cap rate in line with expectations?
- Compare to budget

**Check Alerts:**
- How many leases expiring soon?
- How many vacant units?
- How many open maintenance requests?

#### Step 2: Property-by-Property Analysis

Go to ROI Analysis:

**Sort by Cash-on-Cash Return:**
- Which properties perform best?
- Which properties underperform?
- Should you invest more in top performers?
- Should you sell underperformers?

**Example Insights:**
```
Top Performer:
MAPLE-001: 12.5% CoC, 18% ROI, 85% occupancy

Underperformer:
OAK-001: 4.2% CoC, 6% ROI, 78% occupancy
Action: Investigate low occupancy, review rents
```

#### Step 3: Identify Opportunities

Go to Unit Inventory:

**Find Loss-to-Lease Opportunities:**
- Sort by "Market Rent" minus "Current Rent"
- Properties with large gaps = opportunity to raise rents at renewal

**Example:**
```
Unit 203, OAK-001:
Current Rent: $1,600
Market Rent: $1,800
Loss-to-Lease: $200/month = $2,400/year
Action: Raise rent to $1,750 at renewal
```

#### Step 4: Risk Assessment

Go to Lease Schedule:

**Review Rollover Risk:**
- How much rent expires in next 90 days?
- What's renewal probability?
- Calculate potential vacancy loss if tenants leave

**Example:**
```
Next 90 Days:
3 leases expiring = $5,400/month at risk
Average renewal probability: 70%
Expected vacancy loss: $1,620/month
Action: Start renewal conversations now
```

---

## Common Scenarios

### Scenario 1: Rental Arbitrage (Airbnb)

**Situation:** You lease an apartment for $3,000/month and Airbnb it

#### Setup:

**Property Master:**
```
Property ID: AIRBNB-001
Property Name: Downtown Studio
Ownership Model: Rental Arbitrage (Airbnb/VRBO)
Total Units: 1
Purchase Price: $0 (you don't own it)
```

**Ownership Models:**
```
Property ID: AIRBNB-001
Ownership Type: Rental Arbitrage (Airbnb/VRBO)
Details: Master lease to landlord, sublease on Airbnb
Master Lease Amount: $3,000/month
Lease Start: 01/01/2025
Lease End: 12/31/2025
Landlord Approval: Yes
Special Terms: Landlord receives 10% of profit above base rent
```

**Income Statement:**
```
Property ID: AIRBNB-001
Gross Potential Rent: $6,000 (avg $200/night × 30 nights)
Other Income: $0
Effective Gross Income: $6,000
Operating Expenses: $3,000 (master lease to landlord)
  + $300 (cleaning after each guest)
  + $200 (supplies, amenities)
  + $180 (Airbnb fees ~3%)
  Total OpEx: $3,680
Net Operating Income: $2,320
```

**ROI Analysis:**
```
Property ID: AIRBNB-001
Total Equity: $6,000 (first/last/security)
Annual Cash Flow: $27,840 ($2,320 × 12)
Cash-on-Cash Return: 464% (!!)
```

**Key Metrics to Track:**
- Average nightly rate
- Occupancy percentage
- Cleaning cost per turnover
- Guest rating (maintain 4.8+)

### Scenario 2: Master Lease

**Situation:** You lease an entire 20-unit building and sublease the units

#### Setup:

**Property Master:**
```
Property ID: MASTER-001
Property Name: Riverside Complex
Ownership Model: Master Lease
Total Units: 20
Purchase Price: $0 (you don't own it)
```

**Ownership Models:**
```
Property ID: MASTER-001
Ownership Type: Master Lease
Details: 5-year master lease with landlord
Master Lease Amount: $40,000/month
Lease Start: 01/01/2024
Lease End: 12/31/2028
Special Terms: Annual 2% escalation, responsible for all maintenance
```

**Unit Inventory:**
- Add all 20 units
- Track market rent per unit
- Track occupancy per unit

**Income Statement:**
```
Property ID: MASTER-001
Gross Potential Rent: $50,000 (20 units × $2,500 avg)
Vacancy Loss: $(2,500) (1 vacant unit)
Other Income: $500 (parking)
Effective Gross Income: $48,000
Operating Expenses: $40,000 (master lease payment)
  + $3,000 (maintenance, utilities)
  + $1,000 (management)
  Total OpEx: $44,000
Net Operating Income: $4,000/month
```

**Profit Calculation:**
```
Monthly Spread: $4,000
Annual Profit: $48,000
Return on Investment: Depends on improvements made
```

### Scenario 3: Mixed Portfolio

**Situation:** You have multiple property types with different ownership models

#### Example Portfolio:

**Property 1: Full Ownership - Multifamily**
- 24 units owned outright
- Traditional buy and hold
- Track appreciation + cash flow

**Property 2: Master Lease - Commercial**
- Lease office building, sublease to tenants
- Track spread between master lease and subleases

**Property 3: Rental Arbitrage - Vacation Rental**
- 2 condos leased long-term, Airbnb short-term
- Track occupancy, nightly rate, profit margin

**Dashboard View:**
```
Total Properties: 3
Total Units: 27 (24 + 1 + 2)
Portfolio Value: $3,000,000 (only owned property counts)
Total Equity: $750,000 (only Property 1)
Monthly NOI: $12,500 (combined from all three)
Portfolio Cash-on-Cash: 20% (annual CF / total equity)
```

**Analysis:**
- Property 1: Stable, long-term appreciation
- Property 2: Higher cash flow, higher risk
- Property 3: Highest returns, most management-intensive

---

## Tips & Tricks

### Time-Saving Tips

**1. Use Filters**
- Click on header row (row 3) on any sheet
- Go to Data → Filter
- Filter by property, status, or date range

**2. Sort for Insights**
- Sort Lease Schedule by "Days Until Expiration"
- Sort ROI Analysis by "Cash-on-Cash Return"
- Sort Unit Inventory by "Status" to see all vacancies

**3. Copy Properties**
- To add multiple similar properties:
  - Copy an existing row
  - Paste in new row
  - Update Property ID and name
  - Update financial details

**4. Monthly Templates**
- Save a copy at month-end: "Property_Management_2025-11.xlsx"
- Start next month from current file
- Keep monthly archives for historical tracking

### Power User Features

**1. Conditional Formatting**
- Highlight cells based on values
- Example: Color cells red if Days Vacant > 30
- Example: Color cells green if Cash-on-Cash > 10%

**2. Pivot Tables**
- Analyze across multiple properties
- Example: Total NOI by property type
- Example: Average occupancy by ownership model

**3. Charts**
- Create visual dashboards
- Example: Pie chart of properties by type
- Example: Line chart of monthly cash flow

**4. Data Validation**
- Create dropdown lists for consistency
- Example: Status field → dropdown of "Occupied, Vacant, Under Renovation"
- Example: Property Type → dropdown from Settings sheet

---

## Troubleshooting

### Common Questions

**Q: Can I add more than 997 properties?**  
A: Current template supports rows 4-1000 (997 properties). For larger portfolios, consider database solution or multiple files.

**Q: Can multiple people edit the file?**  
A: Not simultaneously in Excel. Options:
- Use Excel Online for basic collaboration
- Take turns editing
- Move to database (Portfolio Dashboard platform)

**Q: How do I handle properties I manage but don't own?**  
A: Use "Management Contract Only" ownership model. Enter $0 for purchase price and equity.

**Q: Can I track properties in multiple currencies?**  
A: Not automatically. Choose one currency for all entries. Note exchange rates in Notes field if needed.

**Q: How do I delete a property?**  
A: Don't delete rows (breaks formulas). Instead:
- Change Status to "Sold"
- Move row to bottom of sheet
- Keep for historical tracking

**Q: What if I have units with different lease dates?**  
A: That's normal! Rent Roll tracks each lease separately. Stagger renewals to avoid multiple vacancies at once.

---

## Next Steps

### You've Mastered the Basics. Now:

**Level 2: Optimization**
- Review all properties monthly
- Optimize rent pricing using market data
- Improve occupancy rates
- Reduce operating expenses

**Level 3: Growth**
- Use ROI Analysis to identify best deals
- Replicate successful strategies
- Scale to more properties
- Consider property management software

**Level 4: Integration**
- Export data to Portfolio Dashboard
- Automate reporting
- Connect to accounting system
- Build custom dashboards

---

## Getting Help

**For questions about:**
- **The template:** See README.md
- **Formulas:** See Reference Guide
- **Integration:** See Portfolio Dashboard docs
- **Real estate:** Consult with CPA or real estate attorney

---

**Happy property managing! 🏠💼**

You now have everything you need to manage a professional property portfolio. Start small, be consistent, and scale up!
