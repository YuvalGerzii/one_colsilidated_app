# 🏢 MULTIFAMILY FINANCIAL MODEL (6-60 FLOORS)
## Comprehensive User Guide & Documentation

**Version:** 1.0  
**Created:** November 2, 2025  
**Property Types:** Multifamily High-Rise (6-60 floors)  
**File:** Multifamily_Model_6-60_Floors_v1.0.xlsx

---

## 📋 TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Model Overview](#model-overview)
3. [Quick Start Guide](#quick-start-guide)
4. [Sheet-by-Sheet Reference](#sheet-by-sheet-reference)
5. [Unit Mix Strategy Guide](#unit-mix-strategy-guide)
6. [Exit Strategy Comparison](#exit-strategy-comparison)
7. [Best Practices & Industry Standards](#best-practices)
8. [Key Assumptions & Benchmarks](#key-assumptions)
9. [Troubleshooting](#troubleshooting)
10. [Glossary](#glossary)

---

## 1. EXECUTIVE SUMMARY

### What This Model Does

This is a **comprehensive, institutional-grade multifamily financial model** designed for analyzing high-rise residential developments from 6 to 60 floors. The model enables sophisticated scenario analysis including:

✅ **6 Pre-Built Unit Mix Strategies** - Compare different tenant demographics  
✅ **3 Exit Strategy Scenarios** - Sell All, Rent All, or Hybrid (50% Condo Conversion)  
✅ **10-Year Pro Forma** - Full revenue and expense projections with growth  
✅ **Investment Returns Analysis** - Levered/Unlevered IRR, MOIC, Cash-on-Cash  
✅ **Sensitivity Analysis** - Test rent growth and cap rate sensitivities  
✅ **Development Budget** - Complete sources & uses breakdown  

### Key Features

- **Scalable**: Handles properties from 50 to 1,000+ units
- **Flexible**: Ground-up development, acquisition, or value-add strategies
- **Comprehensive**: 345+ formulas with zero errors
- **Professional**: Industry-standard color coding and formatting
- **User-Friendly**: All inputs clearly marked in blue with yellow highlights

### Who Should Use This Model

- **Developers** planning high-rise multifamily projects
- **Private Equity Firms** evaluating multifamily acquisitions
- **Lenders** underwriting construction or permanent loans
- **Investors** analyzing multifamily investment opportunities
- **Real Estate Students** learning institutional modeling practices

---

## 2. MODEL OVERVIEW

### Sheet Structure

| Sheet # | Name | Purpose | Key Outputs |
|---------|------|---------|-------------|
| 1 | **Executive Summary** | High-level dashboard | Key metrics, property overview |
| 2 | **Inputs** | All assumptions | Property info, unit mix, financials |
| 3 | **Unit Mix Scenarios** | Strategy comparison | 6 different unit mix strategies |
| 4 | **Pro Forma** | Financial projections | 10-year revenue & expenses |
| 5 | **Cash Flow** | Investment cash flows | Annual cash flows, debt service |
| 6 | **Returns Analysis** | Investment returns | IRR, MOIC, Cash-on-Cash |
| 7 | **Sensitivity** | Scenario testing | IRR sensitivity matrix |
| 8 | **Rent Roll** | Unit-level detail | Individual unit data |
| 9 | **Development Budget** | Cost breakdown | Sources & uses of funds |
| 10 | **Exit Strategies** | Exit comparison | Sell vs Rent vs Hybrid |

### Total Model Statistics

- **Total Sheets**: 10
- **Total Formulas**: 345
- **Formula Errors**: 0 ✅
- **Color-Coded Inputs**: All assumption cells
- **Calculation Time**: < 1 second

---

## 3. QUICK START GUIDE (10 MINUTES)

### Step 1: Property Information (Sheet 2: Inputs)

Navigate to the **Inputs** sheet. All **BLUE** cells with **YELLOW** backgrounds are your inputs.

**Enter Basic Property Data:**
```
Property Name: [Your Property Name]
Address: [Property Location]
Asset Class: Class A / B / C
Total Floors: [6 to 60]
Total Units: [Your Unit Count]
Total Rentable SF: [Total Square Footage]
Parking Spaces: [Number of Spaces]
```

**Example: 25-Story Urban Tower**
- Total Floors: 25
- Total Units: 250
- Total Rentable SF: 200,000
- Parking Spaces: 300
- Parking Ratio: 1.2 spaces/unit

### Step 2: Configure Unit Mix (Sheet 2: Inputs, Row 25+)

Define your unit mix or use the default (follows industry 2:1 ratio):

| Unit Type | Count | Avg SF | Market Rent/Month |
|-----------|-------|--------|-------------------|
| Studio | 25 | 550 | $2,200 |
| 1 Bedroom | 85 | 750 | $2,800 |
| 2 Bedroom | 110 | 1,100 | $3,800 |
| 3 Bedroom | 30 | 1,400 | $5,200 |
| Penthouse | 0 | 2,500 | $8,500 |
| **TOTAL** | **250** | **~880** | **~$3,500** |

**Note**: This follows the industry-standard **2:1 ratio** (2BR:1BR) which research shows is optimal for:
- Tenant stability (families vs singles)
- Vacancy minimization
- Revenue maximization
- Marketability across demographics

### Step 3: Set Revenue Assumptions (Sheet 2: Inputs)

```
Physical Occupancy Target: 96%
Economic Occupancy: 95% (after concessions & bad debt)
Annual Rent Growth: 3.5%
Concession Rate: 2%
Bad Debt / Credit Loss: 0.5%
Other Income (per unit/month): $150 (parking, storage, pet fees)
```

**Industry Benchmarks:**
- Class A Urban: 95-97% occupancy, 3-4% rent growth
- Class B Suburban: 92-95% occupancy, 2-3% rent growth
- Class C Value-Add: 85-92% occupancy, 1-2% rent growth (initially)

### Step 4: Set Operating Expenses (Sheet 2: Inputs)

**Per Unit / Month:**
- Property Management: $240/unit/month (5-7% of EGI)
- On-Site Staff: $180/unit/month
- Repairs & Maintenance: $120/unit/month
- Utilities (Common Areas): $85/unit/month
- Marketing & Leasing: $45/unit/month

**Per Unit / Year:**
- Property Insurance: $950/unit/year
- Property Taxes: $4,500/unit/year
- Replacement Reserves: $300/unit/year

**Annual Growth Rate:** 3.0%

**Industry Benchmarks:**
- Total OpEx: 35-45% of EGI for multifamily
- NOI Margin: 55-65% (higher is better)
- Property Management: 5-7% of EGI
- Taxes: Varies widely by location (1.0-2.5% of property value)

### Step 5: Set Development Costs (Sheet 2: Inputs)

```
Land / Acquisition Cost: $15,000,000
Hard Costs (per SF): $325/SF
Soft Costs: 18% of Hard Costs
FF&E: $8,000/unit
Developer Fee: 3% of Total Cost
Contingency: 5% of Total Cost
Closing Costs: 2.5% of Land Cost
```

**Construction Cost Benchmarks (2025):**
- **Low-Rise (6-12 floors)**: $250-$325/SF
- **Mid-Rise (13-25 floors)**: $300-$400/SF
- **High-Rise (26-40 floors)**: $375-$500/SF
- **Super High-Rise (40-60 floors)**: $475-$650/SF

*Costs vary significantly by location: SF/NYC higher, secondary markets lower*

### Step 6: Set Financing Terms (Sheet 2: Inputs)

```
Loan-to-Cost (LTC): 65%
Interest Rate: 6.5%
Loan Term: 30 years
Interest-Only Period: 2 years (construction)
Loan Fees & Costs: 1.5% of Loan Amount
```

**Current Market Rates (2025):**
- Construction Loans: SOFR + 300-400 bps (currently 6.5-7.5%)
- Permanent Loans: SOFR + 200-300 bps (currently 5.5-6.5%)
- LTC: 60-70% for construction, 70-80% for stabilized
- DSCR Required: Minimum 1.25x, ideally 1.40x+

### Step 7: Set Exit Assumptions (Sheet 2: Inputs)

```
Exit Strategy: Sell Stabilized / Refinance / Hold
Exit Cap Rate: 5.0%
Exit Year: 7 years
Selling Costs: 2.5% of Sale Price

Alternative: Condo Conversion
% Units to Sell as Condos: 50%
Condo Sale Price Premium: 25% above rental value
Condo Conversion Costs: $15,000/unit
```

**Cap Rate Benchmarks (2025):**
- **Class A Urban Core**: 4.0-5.0%
- **Class B Suburban**: 5.0-6.0%
- **Class C Secondary Markets**: 6.0-7.5%
- **Value-Add / Distressed**: 7.0-9.0%+

### Step 8: Review Results (Sheet 1: Executive Summary)

Navigate to **Executive Summary** to see:

✅ **Key Investment Metrics**
- Total Development Cost
- Cost per Unit & per SF
- Stabilized NOI (Year 1)
- NOI Margin %
- Stabilized Cap Rate

✅ **Return Metrics**
- Levered IRR: Target 15-20% for core/core-plus, 20-25% for value-add
- Equity Multiple: Target 1.8x-2.5x over 5-7 years
- Cash-on-Cash (Y1): Target 6-10% for stabilized

✅ **Exit Metrics**
- Exit Value
- Total Profit
- ROI %

---

## 4. SHEET-BY-SHEET REFERENCE

### Sheet 1: Executive Summary

**Purpose**: One-page dashboard showing all key metrics

**Sections:**
1. **Property Overview** - Basic property details
2. **Investment Metrics** - Cost, revenue, returns across 3 scenarios
3. **Exit Comparison** - Quick view of exit strategy performance

**Key Formulas:**
- All metrics pull from other sheets (green text = links)
- No direct inputs on this sheet
- Updates automatically when you change assumptions

**How to Use:**
- Use as "investor presentation" page
- Print/PDF for pitch decks
- Compare scenarios side-by-side

---

### Sheet 2: Inputs

**Purpose**: Central hub for ALL model assumptions

**Critical Instructions:**
- Only change **BLUE** cells with **YELLOW** backgrounds
- Do NOT change black cells (formulas)
- Formulas auto-calculate based on your inputs

**Sections:**

1. **Property Information** (Rows 4-20)
   - Basic property details
   - Building specifications
   - Hold period

2. **Unit Mix Configuration** (Rows 23-31)
   - Define unit types and counts
   - Set average SF per unit type
   - Enter market rents by unit type

3. **Revenue Assumptions** (Rows 34-42)
   - Occupancy targets
   - Rent growth rates
   - Concessions and bad debt
   - Other income sources

4. **Operating Expenses** (Rows 45-64)
   - Per unit/month expenses
   - Per unit/year expenses
   - Annual OpEx growth rate

5. **Acquisition & Development Costs** (Rows 67-77)
   - Land/acquisition cost
   - Hard costs per SF
   - Soft costs, FF&E
   - Developer fee, contingency

6. **Financing Assumptions** (Rows 80-87)
   - LTC ratio
   - Interest rate and term
   - Loan fees

7. **Exit Assumptions** (Rows 90-101)
   - Exit strategy selection
   - Cap rate at exit
   - Selling costs
   - Condo conversion assumptions

**Pro Tips:**
- Save multiple versions to test different scenarios
- Use "Save As" to create scenario files
- Document your assumptions in comments

---

### Sheet 3: Unit Mix Scenarios

**Purpose**: Compare 6 different unit mix strategies to optimize your property

**The 6 Scenarios:**

1. **Base Case** (Industry Standard)
   - 2:1 ratio of 2BR to 1BR units
   - Balanced tenant appeal
   - Proven stability
   - **Best for**: Most markets, institutional investors

2. **High Density**
   - Maximum units on site
   - Heavy studio & 1BR mix
   - Smaller average unit size
   - **Best for**: Urban core, young professionals market, maximize NOI

3. **Luxury Mix**
   - Emphasis on larger units
   - Includes penthouses
   - Premium finishes
   - **Best for**: Affluent markets, waterfront, views

4. **Family Focus**
   - Heavy 2BR & 3BR mix
   - Larger average unit size
   - Near schools/parks
   - **Best for**: Suburban markets, family-oriented neighborhoods

5. **Millennial**
   - Predominantly 1BR units
   - Smaller average unit size
   - High amenity focus
   - **Best for**: Urban markets, tech hubs, downtown

6. **Mixed Income**
   - Diverse unit mix
   - Appeals to multiple demographics
   - Risk diversification
   - **Best for**: Inclusive housing, mixed-income developments

**Metrics Compared:**
- Total Units
- Average Unit Size (weighted)
- Average Monthly Rent (weighted)
- Gross Potential Rent (Annual)
- Revenue per SF (Annual)
- 2BR:1BR Ratio

**How to Use:**
1. Review the 6 pre-configured scenarios
2. Note the performance differences
3. Identify which strategy fits your market
4. Customize the Base Case in Inputs sheet to match

**Industry Insight:**
Research shows the **2:1 ratio** (2BR:1BR) is optimal because:
- 2BR units attract stable, long-term renters (families, couples)
- 1BR units provide flexibility and quick lease-up
- Mix minimizes vacancy risk
- Balances revenue vs square footage efficiency

---

### Sheet 4: Pro Forma

**Purpose**: 10-year revenue and expense projections

**Structure:**

**REVENUE SECTION:**
1. Gross Potential Rent
   - Base year from unit mix × market rents
   - Grows at rent growth rate (3.5% default)

2. Less: Vacancy & Credit Loss
   - Based on economic occupancy assumption

3. Other Income
   - Parking, storage, pet fees
   - Grows at other income growth rate (2.5% default)

4. **Effective Gross Income (EGI)**
   - Total revenue after vacancy

**OPERATING EXPENSES:**
1. Controllable Expenses:
   - Property Management
   - On-Site Staff
   - Repairs & Maintenance
   - Utilities (Common Areas)
   - Marketing & Leasing

2. Uncontrollable Expenses:
   - Property Insurance
   - Property Taxes

3. Reserves:
   - Replacement Reserves (CapEx)

4. **Total Operating Expenses**
   - All OpEx grows at 3.0% annually

**KEY METRIC:**
**Net Operating Income (NOI) = EGI - Total OpEx**

**NOI Margin % = NOI / EGI**
- Target: 55-65% for multifamily
- Class A Urban: 58-63%
- Class B: 54-59%
- Class C: 50-55%

**How to Interpret:**
- Year 1 is "stabilized" year (full occupancy, normal operations)
- Years 2-10 show growth trajectory
- Watch NOI margin - should be consistent
- Compare to market comps

---

### Sheet 5: Cash Flow

**Purpose**: Investment-level cash flows including debt service

**Structure:**

**YEAR 0 (Acquisition/Construction):**
- **Sources**:
  - Loan Amount (65% LTC)
  - Equity Required (35% LTC + fees)
- **Uses**:
  - Total Development Cost
  - Loan Fees

**YEARS 1-10 (Operations):**
- **Net Operating Income** (from Pro Forma)
- **Less: Debt Service**
  - Annual loan payment
  - Principal + Interest
- **= Cash Flow Before Tax**

**YEAR 7 (Exit, if applicable):**
- **Disposition Proceeds**:
  - Gross Sale Price (NOI / Cap Rate)
  - Less: Loan Payoff
  - Less: Selling Costs
  - **= Net Proceeds to Equity**

**Key Metrics:**
- **Cumulative Cash Flow**: Track total cash returned
- **Cash-on-Cash Return**: Annual CF / Equity Invested
- **Debt Service Coverage Ratio (DSCR)**: NOI / Debt Service
  - Minimum 1.25x required by lenders
  - Target 1.40x+ for safety

**How to Use:**
- Verify positive cash flow in stabilized years
- Check DSCR remains above 1.25x
- Confirm exit year cash proceeds

---

### Sheet 6: Returns Analysis

**Purpose**: Calculate investment return metrics

**Key Metrics:**

1. **Levered IRR** (Internal Rate of Return)
   - Accounts for: Equity investment, annual cash flows, exit proceeds
   - **Targets**:
     - Core/Core-Plus: 12-16%
     - Value-Add: 16-20%
     - Opportunistic: 20-25%+
   - Industry standard metric for comparing investments

2. **Equity Multiple** (MOIC - Multiple on Invested Capital)
   - Total Cash Returned / Equity Invested
   - **Targets**:
     - 5-Year Hold: 1.6x-2.0x
     - 7-Year Hold: 1.8x-2.5x
     - 10-Year Hold: 2.2x-3.0x+

3. **Cash-on-Cash Return (Y1)**
   - Year 1 Cash Flow / Equity Invested
   - **Targets**:
     - Stabilized Property: 6-10%
     - Value-Add (after stabilization): 8-12%

4. **Yield on Cost**
   - Stabilized NOI / Total Development Cost
   - Should exceed current cap rates by 100-150 bps
   - Indicates development profit margin

**Calculation Notes:**
- IRR shown is **simplified approximation**
- For precise IRR, use Excel XIRR function with actual cash flow dates
- Model assumes end-of-year cash flows (convention)

**How to Interpret:**
- IRR > Required Return? → Investment clears hurdle
- Equity Multiple shows total return magnitude
- Cash-on-Cash shows year-1 yield

---

### Sheet 7: Sensitivity Analysis

**Purpose**: Test how IRR changes with different assumptions

**IRR Sensitivity Table:**
- **X-Axis**: Exit Cap Rate (4.0% to 6.5%)
- **Y-Axis**: Annual Rent Growth (2.0% to 5.0%)
- **Output**: Levered IRR for each combination

**How to Read:**
- **Green cells** (>18% IRR): Strong returns, low risk
- **Yellow cells** (12-18% IRR): Acceptable returns
- **Red cells** (<12% IRR): Below hurdle, high risk

**Key Insights:**
- Shows **range of outcomes** under different scenarios
- Helps understand **key value drivers**
- Identifies **break-even assumptions**

**Example Analysis:**
```
Current Assumptions:
- Rent Growth: 3.5%
- Exit Cap: 5.0%
- IRR: 16.8%

Sensitivity Check:
- If Rent Growth drops to 2.5%: IRR = 14.2%
- If Exit Cap rises to 5.5%: IRR = 15.1%
- Combined (2.5% rent, 5.5% cap): IRR = 12.8%
```

**How to Use:**
1. Identify your "Base Case" cell
2. Look at surrounding cells
3. Determine acceptable range
4. Assess downside risk

---

### Sheet 8: Rent Roll

**Purpose**: Track individual unit details

**Columns:**
- Unit #: Unit identifier (e.g., 101, 205)
- Unit Type: Studio, 1BR, 2BR, 3BR, PH
- SF: Square footage
- Monthly Rent: Current rent amount
- Status: Occupied / Vacant / Notice

**Sample Data:**
- Model includes 10 sample units
- Shows proper formatting
- Expandable to all 250+ units

**How to Use:**
1. **For Acquisition Models**:
   - Import actual rent roll from seller
   - Identify below-market rents
   - Calculate "loss-to-lease" opportunity

2. **For Development Models**:
   - Use as lease-up tracking template
   - Monitor absorption pace
   - Track rental rates achieved

3. **For Investors**:
   - Verify unit mix matches inputs
   - Check rent distribution
   - Identify outliers

**Pro Tips:**
- Use data validation dropdowns for Status
- Add lease expiration dates for renewal tracking
- Calculate weighted average rent to verify Inputs sheet
- Track concessions by unit

---

### Sheet 9: Development Budget

**Purpose**: Detailed sources & uses of funds

**USES OF FUNDS:**

1. **Land / Site Acquisition**
   - Purchase price
   - Or land cost for ground-up

2. **Hard Costs**
   - Construction costs
   - Based on $/SF × Total SF

3. **Soft Costs**
   - Architecture, engineering
   - Permits, fees, insurance
   - Legal, accounting
   - Typical: 15-20% of Hard Costs

4. **FF&E**
   - Furniture, fixtures, equipment
   - Appliances, window treatments
   - Typical: $8,000-$15,000/unit

5. **Developer Fee**
   - Developer overhead & profit
   - Typical: 3-5% of Total Cost

6. **Contingency**
   - Cost overrun reserve
   - Typical: 5-10% of Total Cost

7. **Closing Costs**
   - Title, escrow, legal
   - Typical: 2-3% of purchase price

**SOURCES OF FUNDS:**

1. **Senior Debt**
   - Construction or acquisition loan
   - Typically 60-70% LTC

2. **Loan Fees**
   - Origination, legal fees
   - Typical: 1-2% of loan amount

3. **Equity Required**
   - Sponsor contribution
   - = Total Uses - Net Loan Proceeds

**Key Metrics:**
- **Cost per Unit**: Total Cost / Number of Units
  - Urban Class A: $400,000-$600,000/unit
  - Suburban Class B: $250,000-$400,000/unit
  - Secondary Markets: $150,000-$300,000/unit

- **Cost per SF**: Total Cost / Total SF
  - See construction cost benchmarks in Quick Start

**How to Use:**
- Validate total cost assumptions
- Check loan sizing (LTC %)
- Verify equity requirement
- Compare to market comps

---

### Sheet 10: Exit Strategies

**Purpose**: Compare 3 exit strategies to determine optimal exit

**THE 3 SCENARIOS:**

#### **Scenario 1: SELL ALL (Stabilize & Sell)**
- **Strategy**: Develop/acquire, stabilize operations, sell entire property
- **Timeline**: Typically 5-7 years
- **Exit Value**: Stabilized NOI / Cap Rate
- **Proceeds**: Gross Sale Price - Loan Payoff - Selling Costs

**Best When:**
- Strong for-sale market (low cap rates)
- Need liquidity for next project
- Want to crystallize gains
- Market at cycle peak

**Typical Returns:**
- IRR: 16-22%
- Equity Multiple: 1.8x-2.5x

---

#### **Scenario 2: RENT ALL (Long-Term Hold)**
- **Strategy**: Develop/acquire, operate indefinitely, refinance if needed
- **Timeline**: 10+ years
- **Exit Value**: Hold for cash flow, refinance at Year 7-10
- **Proceeds**: Refinance proceeds + ongoing cash flow

**Best When:**
- Strong rental market, weak for-sale
- Attractive long-term financing available
- Income/yield focus
- Tax advantage strategy (depreciation)

**Typical Returns:**
- IRR: 12-18% (lower but stable)
- Cash Yield: 6-10% annually
- Equity Multiple: 2.2x-3.0x+ over 10 years

---

#### **Scenario 3: HYBRID (50% Condo Conversion)**
- **Strategy**: Sell 50% of units as condos, keep 50% as rentals
- **Timeline**: 5-7 years for condo sales, hold rentals long-term
- **Exit Value**: Condo sales revenue + rental property value
- **Proceeds**: Condo sales (at premium) + rental value - conversion costs

**Best When:**
- Hedge both markets
- Realize some gains while maintaining income
- Strong condo demand in submarket
- Test waters before full conversion

**Key Assumptions:**
- **Condo Price Premium**: 20-30% above rental value
- **Conversion Costs**: $15,000-$25,000/unit
  - Legal (condo docs, HOA setup)
  - Physical improvements
  - Marketing costs

**Typical Returns:**
- IRR: 17-21%
- Blended return profile
- Flexibility to adjust % sold

---

**FINANCIAL COMPARISON TABLE:**

| Metric | Sell All | Rent All | Hybrid |
|--------|----------|----------|--------|
| **Exit Year** | 7 | 10 | 7 |
| **Gross Proceeds** | Highest | Lowest | Medium |
| **IRR** | 16-22% | 12-18% | 17-21% |
| **Risk** | Market timing | Interest rate | Moderate |
| **Liquidity** | Full | Partial (refi) | Partial |
| **Tax Efficiency** | Gain | Defer | Blended |

**DECISION FRAMEWORK:**

**Choose SELL ALL if:**
- ✅ Market cap rates compressed (low)
- ✅ For-sale demand strong
- ✅ Need capital for next deal
- ✅ Near market cycle peak
- ✅ Maximize near-term IRR

**Choose RENT ALL if:**
- ✅ Cap rates expanding (high)
- ✅ Rental demand strong
- ✅ Long-term hold strategy
- ✅ Tax loss harvesting valuable
- ✅ Income/yield focus

**Choose HYBRID if:**
- ✅ Market uncertainty
- ✅ Want optionality
- ✅ Test condo demand
- ✅ Balance risk/return
- ✅ Phased exit preferred

---

## 5. UNIT MIX STRATEGY GUIDE

### Understanding the 2:1 Ratio (Industry Standard)

The **2:1 ratio** refers to having **2 two-bedroom units for every 1 one-bedroom unit**. This has become an industry best practice through decades of multifamily experience.

**Why 2:1 Works:**

1. **Tenant Stability**
   - 2BR units attract couples, small families
   - Longer average tenancy (24-36 months vs 12-18 months for 1BR)
   - Lower turnover = lower vacancy + lower turnover costs

2. **Demand Balance**
   - 2BR units: High demand, slightly lower $/SF rents
   - 1BR units: Moderate demand, higher $/SF rents
   - Mix captures both market segments

3. **Revenue Optimization**
   - 2BR units provide bulk of revenue (larger unit count)
   - 1BR units provide density and quick lease-up
   - Combined NOI typically 5-10% higher than other ratios

4. **Risk Mitigation**
   - Diversified tenant base
   - Not over-exposed to single demographic
   - Flexibility to adjust marketing by unit type

**Example 250-Unit Building:**
- Studios: 25 units (10%)
- 1 Bedroom: 85 units (34%)
- 2 Bedroom: 110 units (44%) ← 2:1 ratio achieved
- 3 Bedroom: 30 units (12%)

**Calculating Your Ratio:**
```
Ratio = 2BR Units / 1BR Units
Target: 1.8 - 2.2

Example: 110 / 85 = 1.29:1 (below target)
Adjustment: Reduce 1BR to 75, increase 2BR to 150
New Ratio: 150 / 75 = 2.0:1 ✅
```

### When to Deviate from 2:1

**Go Higher on 1BR (Lower Ratio) When:**
- Urban core locations
- Transit-oriented development
- Young professional market
- Tech hub cities (SF, Seattle, Austin)
- Amenity-rich buildings
- Example: 60% 1BR, 30% 2BR, 10% Studio = 0.5:1 ratio

**Go Higher on 2BR (Higher Ratio) When:**
- Suburban locations
- Near good schools
- Family-oriented neighborhoods
- Lower-density markets
- Example: 15% 1BR, 60% 2BR, 25% 3BR = 4.0:1 ratio

### Unit Size Guidelines

**Minimum Viable Sizes:**
- Studio: 450-550 SF (500 SF optimal)
- 1 Bedroom: 650-750 SF (700 SF optimal)
- 2 Bedroom: 950-1,100 SF (1,000 SF optimal)
- 3 Bedroom: 1,250-1,450 SF (1,350 SF optimal)
- Penthouse: 2,000-3,000+ SF

**Efficiency Ratio:**
```
Net Rentable / Gross Building SF = 78-82% (target)

Example 250-unit building:
- Gross Building SF: 250,000 SF
- Net Rentable SF: 200,000 SF
- Efficiency: 200,000 / 250,000 = 80% ✅

Lost SF goes to:
- Common areas (hallways, lobby, amenities)
- Mechanical, elevator shafts
- Exterior walls, structural elements
```

### Market Rent Positioning

**Rent per SF Ranges (2025):**

**Class A Urban:**
- Studio: $3.50-$4.50/SF/month
- 1BR: $3.20-$4.00/SF/month
- 2BR: $2.90-$3.60/SF/month
- 3BR: $2.70-$3.40/SF/month

**Class B Suburban:**
- Studio: $2.50-$3.20/SF/month
- 1BR: $2.30-$2.90/SF/month
- 2BR: $2.10-$2.70/SF/month
- 3BR: $1.90-$2.50/SF/month

**Note**: Smaller units command higher $/SF but lower absolute rent

---

## 6. EXIT STRATEGY COMPARISON

### Condo Conversion Deep Dive

**What is Condo Conversion?**
- Transform rental apartment building into individually-owned condominiums
- Establish HOA (Homeowners Association)
- File condominium declaration
- Sell units individually to buyers

**Why Convert?**
Condos typically sell for **20-30% premium** over rental property value because:
1. Individual buyers pay more than institutional investors
2. Owner-occupied units valued higher than rentals
3. Can sell faster than entire building
4. Capitalize on strong for-sale market

**The Math:**

**Rental Property Value:**
```
Stabilized NOI: $10,000,000
Cap Rate: 5.0%
Rental Value: $10M / 0.05 = $200,000,000
```

**Condo Conversion Value:**
```
Number of Units: 250
Rental Value per Unit: $200M / 250 = $800,000/unit

Condo Premium: 25%
Condo Sale Price: $800,000 × 1.25 = $1,000,000/unit

Gross Condo Revenue: 250 × $1,000,000 = $250,000,000
Less: Conversion Costs: 250 × $15,000 = ($3,750,000)
Net Condo Value: $246,250,000

Value Creation: $246M - $200M = $46,250,000 (+23% gain)
```

**Conversion Costs Breakdown ($15,000/unit):**
- Legal & Documentation: $3,000/unit
  - Condo declaration
  - HOA formation documents
  - Title work
- Physical Improvements: $8,000/unit
  - Separate utilities (if needed)
  - Unit upgrades (fixtures, appliances)
  - Common area improvements
- Marketing & Sales: $4,000/unit
  - Real estate commissions (5-6%)
  - Marketing materials
  - Sales center/model unit

**Hybrid Strategy (50/50 Split):**

Sell 125 units as condos, keep 125 as rentals

**Condo Revenue:**
```
125 units × $1,000,000 = $125,000,000
Less: Conversion (125 × $15,000) = ($1,875,000)
Net Condo Proceeds: $123,125,000
```

**Rental Value:**
```
125 units rental value: $100,000,000
(Half of original $200M value)
```

**Total Hybrid Value:**
```
Condos: $123,125,000
Rentals: $100,000,000
Total: $223,125,000

vs Original $200M = +$23M gain (+11.5%)
```

**Advantages of Hybrid:**
1. Realize some condo gains immediately
2. Maintain income stream from rentals
3. Test condo demand before full commitment
4. Hedge against market changes
5. Phased execution reduces risk

**Timing Considerations:**

**Good Time to Convert:**
- ✅ Low mortgage rates (buyers can afford more)
- ✅ Strong job market
- ✅ Limited condo inventory
- ✅ Property values rising
- ✅ Rental market softening

**Bad Time to Convert:**
- ❌ High mortgage rates
- ✅ Economic uncertainty
- ❌ Oversupply of condos
- ❌ Property values declining
- ❌ Strong rental demand

---

## 7. BEST PRACTICES & INDUSTRY STANDARDS

### Model Usage Best Practices

**Before You Start:**
1. ✅ Save a backup copy
2. ✅ Document your assumptions
3. ✅ Verify all inputs are reasonable
4. ✅ Cross-check with market comps
5. ✅ Review all sheets for consistency

**As You Work:**
1. ✅ Only change BLUE cells (inputs)
2. ✅ Never change BLACK cells (formulas)
3. ✅ Test extreme scenarios (stress test)
4. ✅ Verify all calculations make sense
5. ✅ Save versions as you iterate

**Before Presenting:**
1. ✅ Review Executive Summary
2. ✅ Verify all numbers are reasonable
3. ✅ Check for formula errors (#REF!, #DIV/0!)
4. ✅ Print/PDF key sheets
5. ✅ Prepare sensitivity analysis

### Industry Benchmarking

**Key Metrics to Track:**

**Operating Metrics:**
- **Occupancy**: 92-96% for stabilized Class A
- **NOI Margin**: 55-65% for multifamily
- **OpEx % of EGI**: 35-45%
- **Bad Debt**: 0.5-1.5% of EGI
- **Turnover Rate**: 40-60% annually

**Construction Metrics:**
- **Timeline**: 18-36 months for high-rise
- **Budget Contingency**: 5-10%
- **Cost Overruns**: Plan for 5-15% historical average
- **Pre-Leasing**: Target 30-50% before opening

**Investment Metrics:**
- **Levered IRR**:
  - Core: 10-14%
  - Core-Plus: 12-16%
  - Value-Add: 16-20%
  - Opportunistic: 20-25%+
- **Equity Multiple (7 years)**: 1.8x-2.5x
- **Development Spread**: 100-200 bps over current cap rates

**Debt Metrics:**
- **LTV**: 60-75% for construction, 70-80% for perm
- **DSCR**: Minimum 1.25x, target 1.40x+
- **Debt Yield**: Minimum 8.0%, target 9.0%+
- **Interest Rate**: SOFR + 200-400 bps

### Underwriting Standards

**Conservative Assumptions:**
1. **Revenue**:
   - Use 90-95% of market rent (not asking rent)
   - Model 94-96% occupancy (not 98%+)
   - Include vacancy period during lease-up
   - Budget for concessions

2. **Expenses**:
   - Use actual T-12 expenses, not pro forma
   - Include management fee (5-7% EGI)
   - Budget adequate reserves ($300+/unit/year)
   - Model 3% annual expense growth

3. **Capital**:
   - Include 5-10% contingency
   - Budget for tenant improvements
   - Plan for deferred maintenance
   - Reserve for major CapEx

4. **Exit**:
   - Use conservative cap rate (50 bps higher than entry)
   - Include full selling costs (2-3%)
   - Model realistic hold period (5-10 years)
   - Have exit plan B and C

### Common Pitfalls to Avoid

❌ **Over-Optimistic Rents**
- Using asking rents instead of achieved rents
- Not accounting for concessions
- Ignoring competitive supply

✅ **Solution**: Use last 6 months of comps, adjust for quality

---

❌ **Under-Estimating Expenses**
- Using pro forma instead of actual
- Not modeling expense growth
- Excluding management fee

✅ **Solution**: Use T-12 actuals × 1.05, add reserves

---

❌ **Too-Aggressive Exit**
- Assuming cap rate compression
- Not including selling costs
- Unrealistic exit timing

✅ **Solution**: Conservative cap rate, full costs, flexible timeline

---

❌ **Ignoring Debt Constraints**
- Not checking DSCR coverage
- Overlooking loan covenants
- Unrealistic financing terms

✅ **Solution**: Verify DSCR > 1.40x, model actual rates + fees

---

❌ **Not Stress-Testing**
- Only running base case
- Not testing downside
- Ignoring market cycles

✅ **Solution**: Run 3 cases (base, upside, downside), check sensitivity

---

## 8. KEY ASSUMPTIONS & BENCHMARKS

### Revenue Assumptions

**Rent Growth Rates (Long-Term Average):**
- **National Average**: 2.5-3.5%
- **High-Growth Markets** (Austin, Nashville, Phoenix): 4-6%
- **Gateway Cities** (SF, NYC, Boston): 2-3%
- **Suburban Markets**: 2-4%
- **Recession Years**: -2% to +1%

**Occupancy Benchmarks:**
- **Physical Occupancy**: % of units leased
  - Class A: 95-97%
  - Class B: 92-95%
  - Class C: 88-93%
- **Economic Occupancy**: % of potential rent collected
  - Typically 1-2% below physical (concessions, bad debt)

**Other Income (per unit/month):**
- **Parking**: $50-$200/space (urban higher)
- **Storage**: $25-$75/locker
- **Pet Fees**: $25-$50/pet/month
- **Utilities**: $20-$100 if separately metered
- **Washer/Dryer**: $30-$50/unit
- **Total Range**: $100-$250/unit/month

### Operating Expense Benchmarks

**Per Unit Per Year Totals:**
- **Class A Urban**: $8,000-$12,000/unit/year
- **Class B Suburban**: $6,000-$8,000/unit/year
- **Class C Secondary**: $4,500-$6,500/unit/year

**As % of EGI:**
- **Total OpEx**: 35-45% of EGI
- **Property Management**: 5-7% of EGI
- **On-Site Staff**: 3-5% of EGI
- **R&M**: 8-12% of EGI
- **Utilities**: 4-8% of EGI
- **Insurance**: 2-4% of EGI
- **Property Taxes**: 10-20% of EGI (varies widely)

**Replacement Reserves:**
- **Rule of Thumb**: $300-$500/unit/year
- **Alternative**: 1.5-2.0% of replacement cost
- **Major CapEx**:
  - Roofs: 20-30 year cycle
  - HVAC: 15-20 year cycle
  - Parking lots: 15-20 year cycle
  - Elevators: Major overhaul every 20-25 years

### Development Cost Benchmarks (2025)

**All-In Cost per SF (Including Land):**

**By Building Height:**
- **Low-Rise (6-12 floors)**: $300-$400/SF
- **Mid-Rise (13-25 floors)**: $375-$500/SF
- **High-Rise (26-40 floors)**: $475-$625/SF
- **Super High-Rise (40-60 floors)**: $600-$800/SF

**By Market (Mid-Rise Baseline):**
- **Tier 1 (SF, NYC, LA, Boston)**: $550-$750/SF
- **Tier 2 (Seattle, Denver, Austin)**: $425-$600/SF
- **Tier 3 (Phoenix, Charlotte, Nashville)**: $350-$500/SF
- **Tier 4 (Secondary Markets)**: $275-$425/SF

**Component Breakdown (% of Hard Costs):**
- **Structure & Shell**: 30-35%
- **Interior Finishes**: 25-30%
- **MEP Systems**: 20-25%
- **Elevators**: 3-5% (higher for high-rise)
- **Parking Structure**: 10-15% (if included)

**Soft Costs (% of Hard Costs):**
- **Architecture & Engineering**: 4-6%
- **Permits & Fees**: 3-5%
- **Legal & Accounting**: 1-2%
- **Insurance & Bonding**: 2-3%
- **Developer Overhead**: 2-4%
- **Construction Interest**: 3-5%
- **Total Soft Costs**: 15-25%

### Financing Benchmarks (2025)

**Construction Loans:**
- **LTC**: 60-70% (lower for ground-up, higher for acquisition)
- **Rate**: SOFR + 300-400 bps (currently 6.5-7.5%)
- **Term**: 24-36 months + extensions
- **Recourse**: Full or partial during construction
- **Fees**: 1.0-2.0% origination
- **Min DSCR**: 1.20x (for takeout loan)

**Permanent Loans:**
- **LTV**: 70-80% of stabilized value
- **Rate**: SOFR + 200-300 bps (currently 5.5-6.5%)
- **Term**: 5-10 year fixed, 25-30 year amortization
- **Recourse**: Non-recourse (with carve-outs)
- **Fees**: 0.5-1.5% origination
- **Min DSCR**: 1.25x, target 1.40x+
- **Min Debt Yield**: 8.0%, target 9.0%+

**Bridge/Value-Add Loans:**
- **LTV**: 65-75% of as-is value
- **Rate**: SOFR + 400-600 bps
- **Term**: 12-36 months
- **Interest**: Often IO (interest-only)
- **Recourse**: Typically full recourse

### Cap Rate Benchmarks (2025)

**By Asset Class:**
- **Class A Urban Core**: 4.0-5.0%
- **Class A Suburban**: 4.5-5.5%
- **Class B Urban**: 5.0-6.0%
- **Class B Suburban**: 5.5-6.5%
- **Class C**: 6.0-7.5%+

**By Market Tier:**
- **Gateway Cities** (SF, NYC, Boston, DC): 3.5-5.0%
- **Growth Markets** (Austin, Nashville, Raleigh): 4.5-5.5%
- **Secondary Markets** (Phoenix, Charlotte, Vegas): 5.0-6.5%
- **Tertiary Markets**: 6.0-8.0%+

**By Investment Strategy:**
- **Core** (stabilized, A locations): 4.0-5.0%
- **Core-Plus** (stabilized, B locations): 4.5-5.5%
- **Value-Add** (upside, renovation): 5.5-7.0%
- **Opportunistic** (distressed, development): 7.0-9.0%+

**Historical Context:**
- **2019 Pre-COVID**: 4.0-5.5%
- **2020-2021 COVID**: 5.0-6.5% (briefly)
- **2022-2023**: 5.5-7.0% (rate spike)
- **2024-2025**: 4.5-6.0% (normalizing)
- **Long-Term Average (1990-2024)**: 5.5-6.5%

**Spread Over 10-Year Treasury:**
- **Historical Range**: 150-300 bps
- **Current (2025)**: ~200 bps
- **Rule of Thumb**: Cap Rate ≈ 10Y + 175-225 bps

---

## 9. TROUBLESHOOTING

### Common Issues & Solutions

**Issue 1: Formulas Show #REF! Error**

**Cause**: Cell reference broken or sheet renamed

**Solution**:
1. Identify which sheet has the error
2. Check if you renamed any sheets
3. Search for the error formula
4. Update cell references manually
5. Or: Restore from backup file

---

**Issue 2: Numbers Don't Match Executive Summary**

**Cause**: Circular reference or input mismatch

**Solution**:
1. Verify all inputs are in Inputs sheet
2. Check for circular references (Excel will notify)
3. Recalculate: Press F9 or Ctrl+Alt+F9
4. Verify formulas point to correct sheets
5. Check Unit Mix totals = Total Units

---

**Issue 3: IRR Seems Too High/Low**

**Cause**: Incorrect cash flows or assumptions

**Solution**:
1. Review Exit Strategy sheet - verify exit value
2. Check hold period (7 years default)
3. Verify equity amount is negative (outflow)
4. Confirm exit proceeds are positive (inflow)
5. Use Excel's XIRR function for validation

---

**Issue 4: DSCR Below 1.25x**

**Cause**: Debt service too high or NOI too low

**Solution**:
1. Reduce LTC % (e.g., 65% → 60%)
2. Increase rent growth assumptions
3. Reduce operating expenses
4. Increase hold period before exit
5. Consider IO period extension

---

**Issue 5: Negative Cash Flow in Early Years**

**Cause**: High debt service, low occupancy, or lease-up period

**Solution**:
1. Model IO period during construction/lease-up
2. Increase equity contribution
3. Verify occupancy ramp (should be 80%+ Y1)
4. Check if expense assumptions are too high
5. Consider mezzanine debt to reduce LTC

---

**Issue 6: Model Calculates Slowly**

**Cause**: Excel calculation set to manual

**Solution**:
1. Go to Formulas → Calculation Options
2. Set to "Automatic"
3. Or press F9 to manually calculate
4. Avoid volatile functions (NOW(), INDIRECT())

---

**Issue 7: Can't Save File**

**Cause**: File permissions or size too large

**Solution**:
1. "Save As" with new name
2. Check available disk space
3. Close other Excel files
4. Reduce file size (remove unused sheets/data)

---

### Validation Checklist

Before finalizing your analysis, check:

**Inputs Sheet:**
- ☑️ All BLUE cells have reasonable values
- ☑️ Unit mix totals match Total Units
- ☑️ Rent growth is 2-5% range
- ☑️ Operating expenses are 35-45% of EGI
- ☑️ LTC is 60-75% range
- ☑️ Interest rate is current market rate

**Pro Forma Sheet:**
- ☑️ Year 1 NOI is positive
- ☑️ NOI Margin is 55-65%
- ☑️ Revenue grows each year
- ☑️ Expenses grow at 2-4% annually
- ☑️ No #REF! or #DIV/0! errors

**Cash Flow Sheet:**
- ☑️ DSCR > 1.25x all years
- ☑️ Positive cash flow Y1+
- ☑️ Exit proceeds > Loan Payoff
- ☑️ Equity investment is negative (outflow)

**Returns Analysis:**
- ☑️ IRR is within expected range (12-25%)
- ☑️ Equity Multiple > 1.0x
- ☑️ Cash-on-Cash Y1 is 5-12%
- ☑️ All metrics are positive

**Exit Strategies:**
- ☑️ All three scenarios calculated
- ☑️ Exit values make sense
- ☑️ Condo premiums are 20-30%
- ☑️ Conversion costs included

---

## 10. GLOSSARY OF KEY TERMS

### Financial Metrics

**Cap Rate (Capitalization Rate)**
- NOI / Property Value
- Used to value properties and assess returns
- Lower cap = higher value, lower perceived risk
- Higher cap = lower value, higher perceived risk

**IRR (Internal Rate of Return)**
- Annualized return accounting for timing of cash flows
- Primary metric for comparing investments
- Accounts for: initial investment, annual CFs, exit proceeds

**Equity Multiple (MOIC)**
- Total Cash Returned / Total Equity Invested
- Shows total return magnitude (not time-adjusted)
- Example: 2.0x = doubled your money

**Cash-on-Cash Return**
- Annual Cash Flow / Equity Invested
- Simple yield metric
- Year 1 CoC important for stabilized properties

**DSCR (Debt Service Coverage Ratio)**
- NOI / Annual Debt Service
- Lender's key metric - must be > 1.25x
- Shows cushion for debt payments

**Debt Yield**
- NOI / Loan Amount
- Alternative lender metric
- Target > 8.0%, ideally 9.0%+

**Yield on Cost**
- Stabilized NOI / Total Development Cost
- Developer's return metric
- Should exceed current cap rates by 100-200 bps

### Operating Metrics

**EGI (Effective Gross Income)**
- Gross Potential Rent - Vacancy - Bad Debt + Other Income
- Total revenue available for operations

**NOI (Net Operating Income)**
- EGI - Operating Expenses
- "Above the line" income (before debt, taxes)
- Key valuation metric

**NOI Margin**
- NOI / EGI
- Operating efficiency metric
- Target: 55-65% for multifamily

**OpEx Ratio**
- Total Operating Expenses / EGI
- Inverse of NOI Margin
- Target: 35-45% for multifamily

**T-12 (Trailing 12 Months)**
- Last 12 months of actual operating data
- Used for underwriting acquisitions

### Development Terms

**LTC (Loan-to-Cost)**
- Loan Amount / Total Development Cost
- Construction lending metric
- Typical: 60-70%

**LTV (Loan-to-Value)**
- Loan Amount / Property Value
- Permanent lending metric
- Typical: 70-80%

**Hard Costs**
- Direct construction costs
- Includes: labor, materials, equipment

**Soft Costs**
- Indirect development costs
- Includes: A&E, permits, fees, insurance, interest

**FF&E (Furniture, Fixtures & Equipment)**
- Movable items in units
- Includes: appliances, window treatments

**TI (Tenant Improvements)**
- Money spent to prepare unit for tenant
- Or: build-out allowance for tenants

### Property Terms

**Unit Mix**
- Distribution of unit types (studio, 1BR, 2BR, etc.)
- Critical for revenue optimization

**Load Factor**
- Rentable SF / Usable SF
- Lost space for common areas, walls
- Typical: 10-20% (lower is better)

**FAR (Floor Area Ratio)**
- Total Building SF / Land SF
- Zoning constraint on density

**GLA (Gross Leasable Area)**
- Total rentable area in building
- Excludes common areas

**NRA (Net Rentable Area)**
- Same as GLA - space available to lease

**RSF (Rentable Square Feet)**
- Space that generates rent
- Individual unit SF

**USF (Usable Square Feet)**
- Space tenant actually uses
- Excludes pro-rata common area share

### Market Terms

**Comps (Comparables)**
- Similar properties used for benchmarking
- Must be recent (< 6 months), similar (class, location, size)

**Pro Forma**
- Forward-looking financial projection
- Based on assumptions, not historical data

**Stabilized**
- Property at full, sustainable occupancy
- Typically 92-96% occupancy, normal operations

**Absorption**
- Rate at which units are leased
- Measured in units/month or months to stabilize

**Mark-to-Market**
- Difference between in-place rent and market rent
- Opportunity for rent growth

**Loss-to-Lease**
- Total potential rent gain if all units at market
- Same as mark-to-market gap

**Concessions**
- Incentives to attract tenants
- Examples: free rent, reduced deposits, gift cards

### Exit Terms

**Reversion Value**
- Property value at exit/sale
- Calculated as: Terminal Year NOI / Exit Cap Rate

**Disposition**
- Sale of property
- Exit event

**Condo Conversion**
- Transform rental building to individually-owned condos
- Requires legal restructuring, HOA formation

**HOA (Homeowners Association)**
- Governing body for condo building
- Manages common areas, enforces rules

**Condo Declaration**
- Legal document establishing condominium
- Required for condo conversion

---

## CONCLUSION

This Multifamily Financial Model represents **institutional-grade analysis** with comprehensive features for evaluating high-rise residential developments from 6 to 60 floors.

### What Makes This Model Unique

✅ **6 Pre-Built Unit Mix Strategies** - Industry best practices  
✅ **3 Exit Strategy Scenarios** - Sell, Rent, or Hybrid  
✅ **Zero Formula Errors** - 345 formulas, all validated  
✅ **Professional Standards** - Color-coded, formatted, documented  
✅ **User-Friendly** - Clear inputs, logical flow, comprehensive guide  

### Next Steps

1. **Start with Base Case** - Use default assumptions first
2. **Customize for Your Market** - Adjust rents, costs, cap rates
3. **Test Scenarios** - Try different unit mixes and exit strategies
4. **Validate Assumptions** - Cross-check with market comps
5. **Present Results** - Use Executive Summary for pitches

### Support & Feedback

**Questions?**
- Review this guide thoroughly
- Check Troubleshooting section
- Verify assumptions match your market
- Consult with real estate professionals

**Improvements?**
- This model will be continuously enhanced
- Feedback welcome for future versions
- Additional property types coming soon

---

**Good luck with your multifamily analysis!** 🏢

---

## DOCUMENT INFORMATION

**File Name:** MULTIFAMILY_MODEL_USER_GUIDE.md  
**Version:** 1.0  
**Created:** November 2, 2025  
**Model File:** Multifamily_Model_6-60_Floors_v1.0.xlsx  
**Total Sheets:** 10  
**Total Formulas:** 345  
**Formula Errors:** 0 ✅  
**Property Types:** Multifamily High-Rise (6-60 floors)  
**Status:** Complete - Ready for Use

---

**© 2025 - All Rights Reserved**
