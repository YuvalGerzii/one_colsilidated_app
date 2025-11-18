---
name: Real Estate Domain Expert
description: Validates real estate calculations, terminology, and ensures financial models follow industry standards and best practices
---

# Real Estate Domain Expert Skill

This skill provides domain expertise for real estate investment analysis, ensuring all calculations, terminology, and assumptions align with industry standards.

## When to Use This Skill

Invoke when:
- Creating or modifying financial calculation models
- Validating investment metrics and formulas
- Reviewing property analysis outputs
- Ensuring real estate terminology is used correctly
- Checking assumptions for reasonableness

## Core Real Estate Metrics & Formulas

### 1. Capitalization Rate (Cap Rate)
```
Cap Rate = Net Operating Income (NOI) / Purchase Price

Example: $50,000 NOI / $500,000 Price = 10% Cap Rate

Typical Ranges by Property Type:
- Class A Multifamily: 4-6%
- Class B Multifamily: 6-8%
- Class C Multifamily: 8-10%
- Single Family Rental: 6-9%
- Retail: 6-8%
- Office: 5-8%
- Industrial: 5-7%
```

**Important**: Cap rate does NOT include debt service. It's a property-level metric, not investor-level.

### 2. Net Operating Income (NOI)
```
NOI = Gross Potential Income
      - Vacancy Loss
      - Operating Expenses
      (Does NOT include debt service, depreciation, or capex)

Components:
+ Gross Rental Income
+ Other Income (laundry, parking, pet fees, etc.)
- Vacancy & Credit Loss (typically 5-10%)
- Operating Expenses:
  • Property Management (8-10% of gross income)
  • Property Taxes
  • Insurance
  • Utilities (if owner-paid)
  • Repairs & Maintenance (1-2% of property value annually)
  • HOA/Condo Fees (if applicable)
  • Marketing & Advertising
  • Legal & Accounting

DO NOT DEDUCT:
✗ Mortgage payments (debt service)
✗ Capital expenditures (roof, HVAC replacement)
✗ Depreciation
```

### 3. Cash-on-Cash Return (CoC)
```
Cash-on-Cash = Annual Pre-Tax Cash Flow / Total Cash Invested

Total Cash Invested includes:
- Down payment
- Closing costs
- Immediate repairs/renovations
- Reserves

Annual Pre-Tax Cash Flow = NOI - Annual Debt Service

Example:
NOI: $40,000
Debt Service: $28,000
Cash Flow: $12,000
Total Investment: $120,000
CoC = $12,000 / $120,000 = 10%

Target Range: 8-12% is good, 12%+ is excellent
```

### 4. Internal Rate of Return (IRR)
```
IRR is the discount rate where NPV of all cash flows equals zero.

NPV = Σ (CFₜ / (1 + IRR)ᵗ) = 0

Includes:
- Initial investment (negative)
- Annual cash flows (years 1-N)
- Sale proceeds (year N)

Target Range: 15-20% for value-add, 10-15% for stable
```

### 5. Debt Service Coverage Ratio (DSCR)
```
DSCR = Net Operating Income / Annual Debt Service

Lender Requirements:
- Minimum: 1.20x (most commercial loans)
- Preferred: 1.25x - 1.35x
- Below 1.0x: Property cannot cover debt (danger!)

Example:
NOI: $60,000
Annual Debt Service: $48,000
DSCR = $60,000 / $48,000 = 1.25x ✓ (acceptable)
```

### 6. Loan-to-Value (LTV) & Loan-to-Cost (LTC)
```
LTV = Loan Amount / Property Value (for purchases/refinances)
LTC = Loan Amount / Total Project Cost (for construction/development)

Typical LTV by Property Type:
- Residential (owner-occupied): Up to 97%
- Single Family Rental: 75-80%
- Small Multifamily (2-4 units): 75-85%
- Multifamily (5+ units): 70-80%
- Commercial: 65-75%
- Fix & Flip: 70-80% (of ARV)
```

### 7. Gross Rent Multiplier (GRM)
```
GRM = Purchase Price / Gross Annual Rent

Example: $600,000 / $72,000 = 8.33 GRM

Typical Ranges:
- Single Family: 8-12
- Multifamily: 6-10
- Lower GRM = potentially better deal
```

### 8. Break-Even Occupancy
```
Break-Even Occupancy = (Operating Expenses + Debt Service) / Gross Potential Income

Example:
OpEx: $30,000
Debt Service: $35,000
Total: $65,000
Gross Income: $80,000
BEO = $65,000 / $80,000 = 81.25%

If occupancy falls below 81.25%, property loses money.
```

### 9. Price Per Unit / Price Per SF
```
Price Per Unit = Purchase Price / Number of Units
Price Per SF = Purchase Price / Gross Square Footage

Useful for comparing similar properties in same market.

Example Multifamily:
$2M purchase / 20 units = $100,000 per unit
$2M purchase / 15,000 SF = $133 per SF
```

## Investment Analysis Models

### Fix & Flip Analysis
```
Purchase Price:              $200,000
Rehab Costs:                 $50,000
Holding Costs (6 months):    $8,000
  - Loan Interest
  - Property Taxes
  - Insurance
  - Utilities
Selling Costs (8% of ARV):   $24,000
─────────────────────────────────────
Total Investment:            $282,000

After Repair Value (ARV):    $300,000
Net Profit:                  $18,000
ROI:                         6.4%

70% Rule Check: ARV × 0.70 - Rehab = Max Purchase
$300,000 × 0.70 - $50,000 = $160,000 max offer
(Actual purchase: $200,000 - FAILS 70% rule)
```

### BRRRR Strategy (Buy, Rehab, Rent, Refinance, Repeat)
```
1. Buy:           $150,000 purchase + $10,000 closing
2. Rehab:         $40,000 renovations
3. Rent:          $1,800/month = $21,600/year
4. Refinance:     75% LTV of new appraised value $240,000
                  Loan: $180,000 (pays back initial $200,000)
5. Cash Left In:  $200,000 invested - $180,000 refinance = $20,000
6. Cash Flow:     $21,600 - $14,400 debt service = $7,200/year
7. Cash-on-Cash:  $7,200 / $20,000 = 36% (excellent!)
```

### Multifamily Underwriting
```
Gross Potential Rent:        $120,000
+ Other Income:              $3,000 (laundry, parking)
- Vacancy (7%):              $8,610
= Effective Gross Income:    $114,390

Operating Expenses:
- Property Management (8%):  $9,600
- Property Tax:              $8,000
- Insurance:                 $4,000
- Utilities:                 $6,000
- Repairs & Maintenance:     $5,000
- Landscaping:               $2,000
- Pest Control:              $600
- Legal/Accounting:          $1,200
────────────────────────────────────
Total OpEx:                  $36,400
OpEx Ratio: 32% (good - typically 35-45%)

Net Operating Income:        $77,990

Purchase Price:              $1,000,000
Cap Rate: 7.8% (good for Class B)

Financing:
Loan Amount (75% LTV):       $750,000
Interest Rate:               6.0%
Term:                        30 years
Annual Debt Service:         $53,916

Cash Flow:                   $24,074
Cash Invested:               $250,000 (down payment)
Cash-on-Cash:                9.6% (strong)
DSCR:                        1.45x (excellent)
```

## Common Assumptions & Industry Standards

### Vacancy Rates
- Class A: 5%
- Class B: 7-8%
- Class C: 10-12%
- Single Family: 8% (one month vacant per year)

### Expense Ratios (% of Gross Income)
- Multifamily: 35-45%
- Single Family: 40-50% (higher due to less efficiency)
- Triple Net (NNN) Commercial: 5-15% (tenant pays most)

### Management Fees
- Self-managed: 0% (but factor in your time!)
- Third-party: 8-10% of collected rent
- Small portfolio (<5 units): 10-12%

### Rent Growth
- Conservative: 2-3% annually
- Market-dependent: 3-5%
- Hot markets: 5-8%

### Property Appreciation
- Conservative: 2-3% (inflation)
- Moderate: 3-4%
- Aggressive: 5%+
- **Never assume appreciation in deals** (bonus if it happens)

### Capital Expenditures (CapEx)
- Reserve: 5-10% of gross rent annually
- Roof replacement: Every 20-30 years
- HVAC: Every 15-20 years
- Water heater: Every 10-15 years
- Appliances: Every 7-10 years
- Flooring: Every 10-15 years

### Holding Period
- Fix & Flip: 3-12 months
- BRRRR: 6-18 months to refinance
- Buy & Hold: 5+ years
- Syndication: 5-7 years typical
- Development: 3-10 years

## Red Flags & Warning Signs

### Deal Killers
- Cap rate below market by 2%+ (overpriced)
- DSCR below 1.20x (tight cash flow)
- Major deferred maintenance (roof, foundation, HVAC)
- Vacancy rate 2x market average (problem property)
- Seller won't provide rent roll or financials (hiding issues)
- Property taxes appealed but increased significantly
- Environmental issues (mold, asbestos, contamination)

### Unrealistic Assumptions
- 0% vacancy (always budget 5% minimum)
- No maintenance expenses (budget 1-2% of value)
- Rent increases >10% without justification
- OpEx ratio <30% for multifamily (too optimistic)
- Assuming appreciation for returns

## Validation Questions to Ask

When reviewing a model or calculation:

1. **Are all revenue sources included?** (rent, parking, laundry, pet fees, storage)
2. **Is vacancy realistic for the market and property class?**
3. **Are operating expenses complete?** (common miss: reserves, management, capex)
4. **Is debt service excluded from NOI?** (common mistake)
5. **Does the cap rate match market comps?**
6. **Is DSCR above 1.20x?** (lender requirement)
7. **Are assumptions documented?** (rent growth, vacancy, etc.)
8. **Is the exit strategy clear?** (hold, refinance, sell)
9. **Are closing costs included?** (3-5% of purchase typically)
10. **Is insurance adequate?** (property, liability, flood if needed)

## Terminology Correctness

### Correct Usage
- **NOI** = property performance metric (before debt)
- **Cash Flow** = investor metric (after debt)
- **Cap Rate** = NOI / Price (property metric)
- **CoC Return** = Cash Flow / Cash Invested (investor metric)
- **IRR** = time-weighted return (includes appreciation)

### Incorrect Usage
- ❌ "Cap rate after debt service" (contradiction - cap rate never includes debt)
- ❌ "NOI after mortgage payment" (NOI is always before debt)
- ❌ "Cash-on-cash IRR" (different metrics - don't conflate)
- ❌ "Gross rent multiplier with expenses" (GRM uses gross income only)

## Execution Instructions

When this skill is invoked:

1. **Review all financial formulas** against the standards above
2. **Validate assumptions** are within industry norms
3. **Check terminology** is used correctly
4. **Flag unrealistic projections** (0% vacancy, 10% rent growth, etc.)
5. **Verify calculations** match the exact formulas
6. **Suggest improvements** to make analysis more robust
7. **Consider market context** (some variations are market-specific)

Always prioritize conservative assumptions and realistic projections over optimistic scenarios.
