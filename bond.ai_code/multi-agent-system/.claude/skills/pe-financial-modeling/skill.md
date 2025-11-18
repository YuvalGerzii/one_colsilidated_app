---
skill_name: PE Financial Modeling Standards
description: Validates private equity financial models, formulas, and metrics to ensure accuracy and industry compliance
version: 1.0.0
author: Real Estate Dashboard Team
tags: [finance, private-equity, validation, modeling]
---

# PE Financial Modeling Standards Skill

This skill provides authoritative standards for private equity financial modeling, ensuring all calculations follow industry best practices and use correct formulas.

## When to Use This Skill

Invoke when:
- Creating or validating DCF models
- Building LBO (Leveraged Buyout) models
- Calculating fund-level returns (IRR, MOIC, TVPI, DPI)
- Performing comparable company analysis
- Validating WACC calculations
- Creating merger models
- Reviewing financial model outputs

## Core PE Financial Metrics

### 1. Discounted Cash Flow (DCF) Analysis

```
Enterprise Value = Σ(FCF_t / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n

Where:
- FCF = Free Cash Flow (EBIT × (1 - Tax Rate) + D&A - CapEx - ΔNWC)
- WACC = Weighted Average Cost of Capital
- Terminal Value = Final Year FCF × (1 + g) / (WACC - g)  [Gordon Growth Method]
- Or: Terminal Value = Final Year EBITDA × Exit Multiple  [Exit Multiple Method]
```

**Key Components:**

**Free Cash Flow (FCF):**
```
FCF = EBIT × (1 - Tax Rate)
      + Depreciation & Amortization
      - Capital Expenditures
      - Δ Net Working Capital

Alternative (from EBITDA):
FCF = EBITDA
      - CapEx
      - Taxes
      - Δ Net Working Capital
```

**Terminal Value Methods:**
```
Method 1: Gordon Growth Model
Terminal Value = FCF_final × (1 + g) / (WACC - g)
Where g = perpetual growth rate (typically 2-3%)

Method 2: Exit Multiple
Terminal Value = EBITDA_final × Exit Multiple
Where Exit Multiple = Industry median EV/EBITDA
```

**Validation Rules:**
- Perpetual growth rate (g) must be ≤ GDP growth (typically 2-3%)
- Exit multiple should be within industry range ±20%
- WACC typically 8-12% for mature companies
- Discount rate increases for riskier investments

### 2. Weighted Average Cost of Capital (WACC)

```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 - Tax Rate))

Where:
- E = Market Value of Equity
- D = Market Value of Debt
- V = E + D (Total Capital)
- Tax Rate = Corporate tax rate

Cost of Equity (CAPM):
Cost of Equity = Risk-Free Rate + β × (Market Risk Premium)

Cost of Debt:
Cost of Debt = Interest Expense / Total Debt
Or: Yield to Maturity on company's bonds
```

**Component Ranges:**
| Component | Typical Range | Notes |
|-----------|---------------|-------|
| Risk-Free Rate | 3-5% | 10-Year Treasury yield |
| Market Risk Premium | 5-7% | Historical average |
| Beta (β) | 0.8-1.5 | <1 = defensive, >1 = volatile |
| Cost of Debt | 4-8% | Depends on credit rating |
| Tax Rate | 21-25% | US federal + state |

**Example Calculation:**
```
Company:
- Market Cap: $500M (Equity)
- Debt: $300M
- Risk-Free Rate: 4%
- Beta: 1.2
- Market Risk Premium: 6%
- Cost of Debt: 5%
- Tax Rate: 25%

Cost of Equity = 4% + 1.2 × 6% = 11.2%
After-Tax Cost of Debt = 5% × (1 - 0.25) = 3.75%

WACC = (500/800 × 11.2%) + (300/800 × 3.75%)
WACC = 7.0% + 1.41% = 8.41%
```

### 3. Internal Rate of Return (IRR)

```
NPV = 0 = Σ(CF_t / (1 + IRR)^t)

IRR is the discount rate where Net Present Value equals zero.
```

**Calculation Method (Newton-Raphson):**
```python
def calculate_irr(cash_flows: List[float], guess: float = 0.1) -> float:
    """
    Calculate IRR using Newton-Raphson iteration.

    Args:
        cash_flows: List of cash flows (first should be negative)
        guess: Initial guess for IRR (default 10%)

    Returns:
        IRR as decimal (0.15 = 15%)
    """
    tolerance = 0.0001
    max_iterations = 1000

    for i in range(max_iterations):
        npv = sum(cf / (1 + guess) ** t for t, cf in enumerate(cash_flows))
        derivative = sum(-t * cf / (1 + guess) ** (t + 1)
                        for t, cf in enumerate(cash_flows))

        if abs(npv) < tolerance:
            return round(guess, 4)

        if derivative == 0:
            raise ValueError("IRR calculation failed")

        guess = guess - (npv / derivative)

    raise ValueError("IRR did not converge")
```

**IRR Benchmarks:**
| Investment Type | Target IRR | Notes |
|-----------------|------------|-------|
| Venture Capital | 25-40% | High risk, high reward |
| Growth Equity | 20-30% | Moderate risk |
| Buyout (LBO) | 20-25% | Leveraged returns |
| Real Estate (Value-Add) | 15-20% | Property improvement |
| Real Estate (Core) | 8-12% | Stable income |
| Infrastructure | 8-15% | Long-term, stable |

### 4. Multiple on Invested Capital (MOIC)

```
MOIC = Total Value / Total Invested Capital

Where:
- Total Value = Distributions + Residual Value
- Total Invested Capital = All equity contributions
```

**Interpretation:**
- MOIC < 1.0x = Loss of capital
- MOIC = 1.0x = Break-even
- MOIC = 2.0x = Doubled money
- MOIC = 3.0x = Tripled money (excellent)

**Relationship with IRR:**
| Holding Period | MOIC | Approximate IRR |
|----------------|------|-----------------|
| 3 years | 2.0x | 26% |
| 5 years | 2.0x | 15% |
| 10 years | 2.0x | 7% |
| 5 years | 3.0x | 25% |
| 5 years | 5.0x | 38% |

**Note:** MOIC doesn't account for time - IRR does.

### 5. Fund-Level Metrics

**TVPI (Total Value to Paid-In Capital):**
```
TVPI = (Distributions + Residual Value) / Paid-In Capital

Example:
Fund raised: $500M
Called: $400M (Paid-In Capital)
Distributions: $350M
Remaining portfolio value: $200M

TVPI = (350M + 200M) / 400M = 1.375x
```

**DPI (Distributed to Paid-In Capital):**
```
DPI = Cumulative Distributions / Paid-In Capital

Using above example:
DPI = 350M / 400M = 0.875x

DPI measures actual cash returned (realized gains)
```

**RVPI (Residual Value to Paid-In Capital):**
```
RVPI = Residual Portfolio Value / Paid-In Capital

Using above example:
RVPI = 200M / 400M = 0.50x

RVPI measures unrealized gains
```

**Validation Check:**
```
TVPI = DPI + RVPI
1.375x = 0.875x + 0.50x ✓
```

**Fund Performance Benchmarks:**
| Quartile | Vintage 2010-2020 IRR | TVPI (10-year) |
|----------|----------------------|----------------|
| Top Quartile | >20% | >2.5x |
| 2nd Quartile | 15-20% | 2.0-2.5x |
| 3rd Quartile | 10-15% | 1.5-2.0x |
| Bottom Quartile | <10% | <1.5x |

### 6. Leveraged Buyout (LBO) Model

**Core LBO Formula:**
```
Equity Return = (Exit Value - Remaining Debt) / Initial Equity Investment

Entry:
Purchase Price = Enterprise Value_entry
Initial Debt = Purchase Price × Leverage %
Initial Equity = Purchase Price - Initial Debt

Exit (Year 5):
EBITDA_exit = EBITDA_initial × (1 + growth)^5
Enterprise Value_exit = EBITDA_exit × Exit Multiple
Debt Paydown = Annual Free Cash Flow applied to debt
Remaining Debt = Initial Debt - Cumulative Debt Paydown
Equity Value = Enterprise Value_exit - Remaining Debt

Equity Multiple = Equity Value / Initial Equity
```

**LBO Returns Attribution:**
```
Total Return = Multiple Expansion + EBITDA Growth + Debt Paydown

Example:
Entry EV/EBITDA: 8.0x
Exit EV/EBITDA: 10.0x
EBITDA Growth: 30% (5 years, 5.4% CAGR)
Debt Paydown: 50% of initial debt

Multiple Expansion: (10.0/8.0) - 1 = 25% gain
EBITDA Growth: 30% gain
Deleveraging: Adds ~20-30% to equity returns
Total: ~75-85% total return → 2.0x MOIC
```

**Typical LBO Structure:**
| Component | Range | Notes |
|-----------|-------|-------|
| Purchase Price | 6-12x EBITDA | Varies by industry |
| Leverage (Debt/EBITDA) | 4-6x | Highly leveraged |
| Equity % | 30-50% | Rest is debt |
| Senior Debt | 60-70% | Lower interest |
| Subordinated Debt | 10-20% | Higher interest |
| Equity | 20-30% | Highest return |

### 7. Comparable Company Analysis (Comps)

**Valuation Multiples:**

**Enterprise Value Multiples:**
```
EV/Revenue = Enterprise Value / Annual Revenue
EV/EBITDA = Enterprise Value / EBITDA
EV/EBIT = Enterprise Value / EBIT

Where:
Enterprise Value = Market Cap + Debt - Cash
```

**Equity Value Multiples:**
```
P/E Ratio = Price per Share / Earnings per Share
P/B Ratio = Price per Share / Book Value per Share
P/S Ratio = Market Cap / Revenue
```

**Industry Benchmarks:**

| Industry | EV/Revenue | EV/EBITDA | P/E Ratio |
|----------|------------|-----------|-----------|
| Software/SaaS | 6-15x | 20-40x | 30-60x |
| Technology Hardware | 2-4x | 10-15x | 15-25x |
| Healthcare Services | 2-3x | 10-15x | 20-30x |
| Manufacturing | 1-2x | 8-12x | 12-18x |
| Retail | 0.5-1.5x | 6-10x | 10-20x |
| Real Estate | N/A | 12-18x | 15-25x |
| Financial Services | N/A | N/A | 10-15x |

**Valuation Range Calculation:**
```
Target Company EBITDA: $50M
Comparable Companies EV/EBITDA: 10x, 11x, 12x, 13x, 14x

Remove outliers, calculate median: 12x
Apply 25th-75th percentile range: 11x - 13x

Valuation Range:
Low: $50M × 11x = $550M
Mid: $50M × 12x = $600M
High: $50M × 13x = $650M
```

### 8. Merger Model

**Accretion/Dilution Analysis:**
```
Pro Forma EPS = (Acquirer Net Income + Target Net Income - Synergies + Integration Costs - Interest on New Debt) / Pro Forma Shares Outstanding

Accretion/Dilution % = (Pro Forma EPS - Standalone EPS) / Standalone EPS

Accretive: Pro Forma EPS > Standalone EPS (Good for acquirer)
Dilutive: Pro Forma EPS < Standalone EPS (Bad for acquirer)
```

**Exchange Ratio:**
```
Exchange Ratio = Offer Price per Target Share / Acquirer Share Price

Example:
Acquirer stock price: $50
Target stock price: $30
Premium: 30%
Offer price: $30 × 1.30 = $39

Exchange Ratio = $39 / $50 = 0.78 shares
(Target shareholders get 0.78 acquirer shares per share held)
```

**Synergy Valuation:**
```
Synergy NPV = Σ(Annual Synergies / (1 + Discount Rate)^t) - Integration Costs

Types of Synergies:
- Revenue synergies: Cross-selling, market expansion
- Cost synergies: Economies of scale, headcount reduction
- Tax synergies: NOL utilization, tax structure optimization
```

## Financial Model Validation Rules

### Input Validation
1. **Growth Rates:**
   - Revenue growth: -5% to +30% (mature vs. high-growth)
   - EBITDA margin: 5% to 50% (varies by industry)
   - Terminal growth: 2-3% (≤ GDP growth)

2. **Multiples:**
   - EV/EBITDA: 4x to 20x (varies significantly by sector)
   - P/E Ratio: 5x to 50x
   - Must be within industry norms ±30%

3. **Discount Rates:**
   - WACC: 6% to 15%
   - Cost of Equity: 8% to 18%
   - Risk-free rate: Use current 10-year Treasury

4. **Leverage:**
   - Debt/EBITDA: 0x to 6x (6x+ is very aggressive)
   - Interest Coverage (EBITDA/Interest): ≥2.0x (lender requirement)
   - Debt/Equity: 0.5x to 3.0x

### Formula Accuracy Checks

**✅ Correct Formulas:**
```python
# DCF
enterprise_value = sum(fcf[t] / (1 + wacc)**t for t in range(1, n+1)) + terminal_value / (1 + wacc)**n

# WACC
wacc = (equity_value / total_value) * cost_of_equity + (debt_value / total_value) * cost_of_debt * (1 - tax_rate)

# Free Cash Flow
fcf = ebit * (1 - tax_rate) + depreciation - capex - change_in_nwc

# MOIC
moic = (total_distributions + residual_value) / total_invested_capital

# Cap Rate (Real Estate)
cap_rate = noi / purchase_price
```

**❌ Common Mistakes:**
```python
# Wrong: Not discounting terminal value
enterprise_value = sum(fcf) + terminal_value  # Missing discount

# Wrong: Forgetting tax shield on debt
wacc = (e/v) * cost_equity + (d/v) * cost_debt  # Missing (1-tax_rate)

# Wrong: Including debt service in FCF
fcf = ebit - capex - debt_service  # FCF is before debt service

# Wrong: Confusing MOIC with IRR
moic = irr * holding_period  # MOIC ≠ IRR × time

# Wrong: Not subtracting debt from EV to get equity value
equity_value = enterprise_value  # Must subtract net debt
```

### Output Reasonableness Checks

1. **Sanity Checks:**
   - IRR should be 5-40% for most PE investments
   - MOIC should be 1.5x-5.0x for successful deals
   - WACC should be lower than IRR (creating value)
   - Terminal value shouldn't exceed 80% of total value
   - Debt should be fully payable from cash flows

2. **Internal Consistency:**
   - Balance sheet must balance (Assets = Liabilities + Equity)
   - Cash flow statement ties to balance sheet changes
   - Income statement flows into equity section
   - Returns calculations use same time periods

3. **Cross-Checks:**
   - Implied exit multiple vs. entry multiple (within 20%)
   - Year 5 metrics vs. industry benchmarks
   - Debt paydown schedule achievable from FCF
   - Working capital assumptions reasonable (% of revenue)

## Industry-Specific Benchmarks

### Software/SaaS
- ARR Growth: 30-100%+ (high growth)
- EBITDA Margin: 20-40% (at scale)
- Rule of 40: Growth % + EBITDA Margin % ≥ 40%
- Churn: <5% annual (net revenue retention >100%)
- CAC Payback: <12 months
- LTV/CAC: >3x

### Healthcare
- EBITDA Margin: 15-30%
- Regulatory risk: Higher discount rate (+2-3%)
- Reimbursement risk: Model multiple scenarios
- Patient volume growth: 3-8%

### Manufacturing
- EBITDA Margin: 10-20%
- CapEx: 3-5% of revenue
- Working capital: 15-25% of revenue
- Cyclicality: Stress test with downturn scenarios

### Real Estate
- NOI Margin: 60-75% (after OpEx)
- Cap Rates: 4-10% (varies by asset class)
- Leverage: 50-75% LTV
- Rent Growth: 2-5% annually

## Model Documentation Standards

Every financial model must include:

1. **Assumptions Tab:**
   - All key drivers documented
   - Source for each assumption
   - Sensitivity ranges
   - Date assumptions were made

2. **Executive Summary:**
   - Investment thesis (1 paragraph)
   - Key metrics: IRR, MOIC, payback period
   - Risk factors (top 3-5)
   - Base/upside/downside cases

3. **Formula Documentation:**
   - Complex calculations explained
   - Industry benchmarks cited
   - Formula verification examples

4. **Version Control:**
   - Model version number
   - Date of last update
   - Changes log

## Error Prevention

### Color Coding (Excel/Sheets)
- **Blue**: Hardcoded inputs
- **Black**: Formulas
- **Green**: Links from other sheets
- **Red**: Links from other files

### Formula Best Practices
- Use named ranges for key assumptions
- Avoid circular references (enable iterative calculation if required)
- Use error checks: IFERROR, ISERROR
- Document unusual formulas with comments
- Use consistent time periods (all monthly or all annual)

### Common Pitfalls
1. Forgetting to convert monthly to annual (or vice versa)
2. Mixing nominal and real (inflation-adjusted) values
3. Double-counting debt in EV calculations
4. Using wrong tax rate (marginal vs. effective)
5. Neglecting working capital changes in FCF
6. Using wrong number of shares (basic vs. diluted)

## Execution Instructions

When this skill is invoked:

1. **Verify formulas** match industry standards above
2. **Check assumptions** are within reasonable ranges
3. **Validate outputs** using reasonableness checks
4. **Ensure consistency** across all calculations
5. **Document** all assumptions and sources
6. **Stress test** with sensitivity analysis
7. **Compare** against industry benchmarks

Always prioritize:
- Accuracy over complexity
- Transparency over black boxes
- Conservative over aggressive assumptions
- Documented over undocumented calculations
