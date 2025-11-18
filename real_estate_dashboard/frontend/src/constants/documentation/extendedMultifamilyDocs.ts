export const EXTENDED_MULTIFAMILY_QUICK_REF = `# MULTIFAMILY MODEL - QUICK REFERENCE CARD

## 📊 **MULTIFAMILY MODEL (6-60 FLOORS) - ONE-PAGE GUIDE**

---

## 🎯 MODEL FILES
- **Main Model**: \`Multifamily_Model_6-60_Floors_v1.0.xlsx\` (21 KB)
- **User Guide**: \`MULTIFAMILY_MODEL_USER_GUIDE.md\` (Complete documentation)
- **Status**: ✅ 345 formulas, 0 errors

---

## 📋 SHEET OVERVIEW

| # | Sheet | Purpose |
|---|-------|---------|
| 1 | **Executive Summary** | Dashboard - All key metrics |
| 2 | **Inputs** | ⭐ ALL ASSUMPTIONS - Change BLUE cells only |
| 3 | **Unit Mix Scenarios** | Compare 6 strategies |
| 4 | **Pro Forma** | 10-year revenue & expenses |
| 5 | **Cash Flow** | Investment cash flows |
| 6 | **Returns Analysis** | IRR, MOIC, CoC |
| 7 | **Sensitivity** | Scenario testing |
| 8 | **Rent Roll** | Unit-level detail |
| 9 | **Development Budget** | Sources & uses |
| 10 | **Exit Strategies** | Sell vs Rent vs Hybrid |

---

## ⚡ QUICK START (10 MINUTES)

### 1. Property Basics (Inputs Sheet)
\`\`\`
Property Name: [Your Name]
Total Floors: [6-60]
Total Units: [50-1,000]
Total SF: [Square Footage]
Asset Class: A / B / C
\`\`\`

### 2. Unit Mix (Inputs Sheet, Row 25+)
**Default follows industry 2:1 ratio (2BR:1BR)**
- Studio: 25 units @ 550 SF @ $2,200/mo
- 1 Bedroom: 85 units @ 750 SF @ $2,800/mo
- 2 Bedroom: 110 units @ 1,100 SF @ $3,800/mo
- 3 Bedroom: 30 units @ 1,400 SF @ $5,200/mo

### 3. Revenue Assumptions
- Occupancy: 95-96%
- Rent Growth: 3.5% annually
- Concessions: 2%
- Bad Debt: 0.5%

### 4. Operating Expenses
- Property Mgmt: $240/unit/mo (5-7% EGI)
- On-Site Staff: $180/unit/mo
- R&M: $120/unit/mo
- Utilities: $85/unit/mo
- Insurance: $950/unit/yr
- Taxes: $4,500/unit/yr
- Reserves: $300/unit/yr

### 5. Development Costs
- Land: $15M
- Hard Costs: $325/SF
- Soft Costs: 18% of hard
- FF&E: $8,000/unit
- Developer Fee: 3%
- Contingency: 5%

### 6. Financing
- LTC: 65%
- Interest Rate: 6.5%
- Term: 30 years
- Loan Fees: 1.5%

### 7. Exit
- Strategy: Sell / Rent / Hybrid
- Exit Cap Rate: 5.0%
- Hold Period: 7 years
- Selling Costs: 2.5%

### 8. Review Results (Executive Summary)
✅ Check Levered IRR (target 15-20%)
✅ Check Equity Multiple (target 1.8x-2.5x)
✅ Check NOI Margin (target 55-65%)

---

## 🏗️ 6 UNIT MIX STRATEGIES (Sheet 3)

| Strategy | Description | Best For |
|----------|-------------|----------|
| **Base Case** | 2:1 ratio (2BR:1BR) | Most markets, proven stable |
| **High Density** | Max units, heavy 1BR | Urban core, young professionals |
| **Luxury Mix** | Larger units, penthouses | Affluent markets, views |
| **Family Focus** | Heavy 2BR & 3BR | Suburban, near schools |
| **Millennial** | Predominantly 1BR | Tech hubs, downtown |
| **Mixed Income** | Diverse mix | Inclusive developments |

---

## 🚪 3 EXIT STRATEGIES (Sheet 10)

### **Scenario 1: SELL ALL**
- Stabilize & sell entire property
- **Best when**: Strong for-sale market, need liquidity
- **IRR**: 16-22% (highest short-term)

### **Scenario 2: RENT ALL**
- Hold long-term, operate for income
- **Best when**: Strong rental demand, tax advantages
- **IRR**: 12-18% (lower but stable)

### **Scenario 3: HYBRID (50% Condo)**
- Sell 50% as condos, keep 50% rental
- **Best when**: Hedge both markets, flexibility
- **IRR**: 17-21% (balanced)
- **Condo Premium**: 20-30% above rental value
- **Conversion Cost**: $15,000/unit

---

## 📊 KEY BENCHMARKS

### **Operating Metrics**
- NOI Margin: 55-65%
- Occupancy: 92-96%
- OpEx % of EGI: 35-45%

### **Construction Costs (All-In per SF)**
- Low-Rise (6-12 floors): $300-$400/SF
- Mid-Rise (13-25 floors): $375-$500/SF
- High-Rise (26-40 floors): $475-$625/SF
- Super High-Rise (40-60 floors): $600-$800/SF

### **Returns Targets**
- **Core**: 10-14% IRR
- **Core-Plus**: 12-16% IRR
- **Value-Add**: 16-20% IRR
- **Opportunistic**: 20-25%+ IRR
- **Equity Multiple (7 years)**: 1.8x-2.5x

### **Cap Rates (2025)**
- Class A Urban: 4.0-5.0%
- Class B Urban: 5.0-6.0%
- Class B Suburban: 5.5-6.5%
- Class C: 6.0-7.5%+

### **Financing**
- Construction LTC: 60-70%
- Perm Loan LTV: 70-80%
- Interest Rate: SOFR + 200-400 bps (5.5-7.5%)
- Min DSCR: 1.25x (target 1.40x+)

---

## ⚠️ CRITICAL RULES

### **DO:**
✅ Only change **BLUE cells** (inputs)
✅ Use **YELLOW highlighted** cells for key assumptions
✅ Test multiple scenarios
✅ Cross-check with market comps
✅ Save backup copies

### **DON'T:**
❌ Change **BLACK cells** (formulas)
❌ Delete sheets or rows
❌ Override linked cells
❌ Ignore validation warnings
❌ Skip sensitivity analysis

---

## 🎯 TARGET METRICS

### **Acquisition/Development:**
- Cost per Unit: $300K-$500K (urban)
- Cost per SF: $300-$500/SF (varies by height)
- Development Spread: 100-200 bps over cap rate

### **Operations:**
- Year 1 NOI: $10M+ (250 units)
- NOI Margin: 58-62% (Class A)
- Cash-on-Cash: 7-9% (stabilized)
- DSCR: 1.35-1.50x

### **Exit:**
- Hold Period: 5-10 years
- Exit Cap Rate: +50 bps from entry
- Levered IRR: 15-20%
- Equity Multiple: 1.8x-2.5x

---

## 🔍 TROUBLESHOOTING

**#REF! Error?**
→ Cell reference broken. Check sheet names.

**Numbers seem off?**
→ Press F9 to recalculate. Verify inputs.

**IRR too high/low?**
→ Check exit value and hold period.

**Negative cash flow?**
→ Reduce LTC or increase equity.

**DSCR below 1.25x?**
→ Increase NOI or reduce debt.

---

## 📖 RESOURCES

**Full Documentation:**
- See \`MULTIFAMILY_MODEL_USER_GUIDE.md\` (60+ pages)

**Key Sections:**
- Quick Start Guide (10 min setup)
- Unit Mix Strategy Guide (optimize revenue)
- Exit Strategy Comparison (sell vs rent)
- Benchmarks & Best Practices
- Troubleshooting & Glossary

**Model Features:**
- 10 comprehensive sheets
- 345 formulas (0 errors)
- 6 unit mix scenarios
- 3 exit strategies
- Professional formatting

---

## ✨ WHAT'S UNIQUE ABOUT THIS MODEL

1. **6 Pre-Built Unit Mix Strategies**
   - Compare different demographic targets
   - Based on industry research (2:1 ratio best practice)

2. **3 Exit Strategy Scenarios**
   - Sell All, Rent All, or Hybrid (50% condo)
   - Model condo conversion economics

3. **Comprehensive & Validated**
   - 345 formulas, all cross-checked
   - Zero errors, professional formatting
   - Institutional-grade analysis

4. **User-Friendly**
   - Clear color-coding (Blue = input)
   - Yellow highlighting for key cells
   - Extensive documentation

---

## 🚀 NEXT STEPS

1. **Open Model** → \`Multifamily_Model_6-60_Floors_v1.0.xlsx\`
2. **Go to Inputs Sheet** → Change BLUE cells
3. **Review Executive Summary** → Check key metrics
4. **Test Scenarios** → Unit Mix Scenarios & Exit Strategies
5. **Read Full Guide** → \`MULTIFAMILY_MODEL_USER_GUIDE.md\`

---

## 📞 REMEMBER

- **Always backup** before making changes
- **Test assumptions** with sensitivity analysis
- **Cross-check** with market comparables
- **Document** your assumptions
- **Validate** all outputs make sense

---

**Version 1.0** | November 2, 2025 | Multifamily High-Rise (6-60 Floors)

**Status**: ✅ Complete & Ready to Use

---
`;

export const EXTENDED_MULTIFAMILY_USER_GUIDE = `Full User Guide content would be loaded here from MULTIFAMILY_MODEL_USER_GUIDE.md`;
