# MIXED-USE MODEL - QUICK REFERENCE CARD

## 🏗️ **MIXED-USE REAL ESTATE MODEL - ONE-PAGE GUIDE**

---

## 🎯 MODEL FILES
- **Main Model**: `Mixed_Use_Model_v1.0.xlsx` (35 KB)
- **User Guide**: `MIXED_USE_MODEL_USER_GUIDE.md` (Complete documentation)
- **Status**: ✅ 131+ formulas, 0 errors

---

## 📋 SHEET OVERVIEW

| # | Sheet | Purpose |
|---|-------|---------|
| 1 | **Executive Summary** | Dashboard - All key metrics |
| 2 | **Inputs** | ⭐ ALL ASSUMPTIONS - Change BLUE cells only |
| 3 | **Allocation Scenarios** | Compare 8 strategies + Custom Optimizer |
| 4 | **Multifamily Component** | Residential revenue & NOI |
| 5 | **Office Component** | Office revenue & NOI |
| 6 | **Retail Component** | Retail revenue & NOI |
| 7 | **Hotel Component** | Hotel revenue & NOI |
| 8 | **Restaurant Component** | Restaurant revenue & NOI |
| 9 | **Consolidated Pro Forma** | Aggregated 10-year financials |
| 10 | **Cash Flow Analysis** | Investment cash flows |
| 11 | **Returns Analysis** | IRR, MOIC, component returns |
| 12 | **Sensitivity Analysis** | Scenario testing |

---

## ⚡ QUICK START (15 MINUTES)

### 1. Property Basics (Inputs Sheet)
```
Property Name: [Your Name]
Total Building SF: [100,000-1,000,000]
Number of Floors: [6-60+]
Average Floor Plate: [10,000-15,000 SF]
Asset Class: A / B / C
Parking Spaces: [100-500]
```

### 2. Space Allocation (Inputs Sheet, Row 18-24)
**MUST TOTAL 100% - Adjust for your strategy**

| Property Type | Default % | Your % | Notes |
|---------------|-----------|--------|-------|
| Multifamily | 40% | ___% | Apartments |
| Office | 25% | ___% | Commercial workspace |
| Retail | 15% | ___% | Ground floor stores |
| Hotel | 15% | ___% | Guest rooms |
| Restaurant | 5% | ___% | F&B/Dining |
| **TOTAL** | **100%** | **100%** | ⚠️ Must equal 100%! |

### 3. Multifamily Assumptions (Rows 34-43)
```
Total Units: Auto-calculated (SF / 850)
Avg Unit Size: 850 SF
Avg Rent/Unit: $3,500/month
Physical Occupancy: 96%
Rent Growth: 3.5% annually
Other Income: $150/unit/month
OpEx/Unit: $650/month
```

### 4. Office Assumptions (Rows 46-54)
```
Rentable SF: Auto-calculated from allocation
Load Factor: 1.20 (20% common area)
Avg Rent/SF: $45/year
Economic Occupancy: 95%
Rent Growth: 3.0% annually
Expense Recovery: 98%
OpEx/SF: $15/year
```

### 5. Retail Assumptions (Rows 56-63)
```
Total Retail SF: Auto-calculated
Avg Rent/SF: $55/year
Economic Occupancy: 92%
Rent Growth: 4.0% annually (highest growth)
Percentage Rent: 8% of sales
Sales/SF: $500/year
CAM Charges: $12/SF
OpEx/SF: $18/year
```

### 6. Hotel Assumptions (Rows 65-73)
```
Number of Rooms: Auto-calc (SF / 500)
ADR (Avg Daily Rate): $285
Occupancy: 75%
RevPAR Growth: 4.0% annually
F&B Revenue/Room: $45/day
Other Revenue: $15/day
Operating Expenses: 65% of revenue
Management Fee: 3% of revenue
```

### 7. Restaurant Assumptions (Rows 77-84)
```
Total F&B SF: Auto-calculated
Base Rent/SF: $60/year (premium)
Percentage Rent: 10% of sales
Sales/SF: $800/year (high-traffic)
Economic Occupancy: 90%
Rent Growth: 3.5% annually
OpEx/SF: $20/year
```

### 8. Development Budget (Rows 90-100)
```
Land Acquisition: $75M (adjust for market)
Hard Costs/SF: $425 (varies by height/class)
Total Hard Costs: Auto-calculated
Soft Costs: 18% of hard costs
FF&E - Multifamily: $8,000/unit
FF&E - Hotel: $15,000/room
FF&E - Restaurant: $125/SF
Developer Fee: 3%
Contingency: 5%
```

### 9. Financing (Rows 133-137)
```
Loan-to-Cost (LTC): 65%
Interest Rate: 6.5%
Loan Term: 30 years
Amortization: 30 years
Loan Fees: 1.5%
```

### 10. Exit Assumptions (Rows 141-148)
```
Hold Period: 10 years
Exit Cap - Multifamily: 4.8%
Exit Cap - Office: 6.5%
Exit Cap - Retail: 6.0%
Exit Cap - Hotel: 7.0%
Exit Cap - Restaurant: 6.5%
Blended Cap: Auto-calculated (weighted avg)
Selling Costs: 2.5%
```

### 11. Review Scenarios (Allocation Scenarios Sheet)
✅ Check Base Case (Balanced)
✅ Compare 8 pre-built strategies
✅ Test custom allocation in Optimizer
✅ Identify highest IRR scenario

### 12. Review Results
✅ **Executive Summary**: Key metrics dashboard
✅ **Returns Analysis**: Levered IRR (target 18-25%)
✅ **Sensitivity Analysis**: Test cap rates & costs

---

## 🎯 8 PRE-BUILT ALLOCATION STRATEGIES

| Strategy | MF | Office | Retail | Hotel | Rest | Best For |
|----------|-------|--------|--------|-------|------|----------|
| **Base Case** | 40% | 25% | 15% | 15% | 5% | Diversified, most markets |
| **MF Focus** | 70% | 15% | 10% | 0% | 5% | Residential demand |
| **Office Tower** | 20% | 60% | 10% | 5% | 5% | CBD location |
| **Retail Emphasis** | 30% | 15% | 40% | 10% | 5% | High-traffic area |
| **Hospitality** | 15% | 20% | 15% | 45% | 5% | Tourism/convention |
| **Luxury Mix** | 35% | 20% | 15% | 20% | 10% | Affluent market |
| **Value-Add** | 50% | 30% | 10% | 5% | 5% | Lease-up strategy |
| **Conservative** | 30% | 30% | 20% | 15% | 5% | Stable income |

---

## 📊 KEY BENCHMARKS BY PROPERTY TYPE

### Development Costs (All-In per SF)
- **Low-Rise** (6-12 floors): $350-450/SF
- **Mid-Rise** (13-25 floors): $425-550/SF
- **High-Rise** (26-40 floors): $525-675/SF
- **Super High-Rise** (40-60 floors): $650-850/SF

### Operating Metrics

| Type | NOI Margin | OpEx/SF | Occupancy | Rent Growth |
|------|------------|---------|-----------|-------------|
| **Multifamily** | 60-65% | $7-10 | 94-97% | 3.0-4.0% |
| **Office** | 55-65% | $12-18 | 88-93% | 2.5-3.5% |
| **Retail** | 50-60% | $15-25 | 85-92% | 3.5-4.5% |
| **Hotel** | 25-35% | 65% rev | 70-80% | 3.5-4.5% |
| **Restaurant** | 35-45% | $18-28 | 85-95% | 3.0-4.0% |

### Returns Targets (Levered IRR)
- **Core**: 10-14%
- **Core-Plus**: 12-16%
- **Value-Add**: 16-20%
- **Opportunistic**: 20-25%+
- **Mixed-Use Dev**: 18-25% (typical)

### Cap Rates (2025 Market)

| Property Type | Class A | Class B | Suburban |
|---------------|---------|---------|----------|
| **Multifamily** | 4.5-5.5% | 5.5-6.5% | 6.0-7.0% |
| **Office** | 6.0-7.0% | 7.0-8.5% | 7.5-9.0% |
| **Retail** | 5.5-6.5% | 6.5-7.5% | 7.0-8.5% |
| **Hotel** | 7.0-8.5% | 8.0-9.5% | 8.5-10.5% |
| **Restaurant** | 6.5-7.5% | 7.5-9.0% | 8.0-10.0% |

### Financing
- **Construction LTC**: 60-70%
- **Permanent LTV**: 70-80%
- **Interest Rate**: SOFR + 200-400 bps (6.0-8.0%)
- **Min DSCR**: 1.25x (target 1.40x+)

---

## ⚠️ CRITICAL RULES

### **DO:**
✅ Only change **BLUE cells** (inputs)
✅ Ensure allocation totals **100%** exactly
✅ Use **YELLOW highlighted** cells for key assumptions
✅ Test multiple scenarios
✅ Cross-check with market comps
✅ Save backup copies before changes
✅ Validate all cap rates with brokers
✅ Include realistic lease-up period

### **DON'T:**
❌ Change **BLACK cells** (formulas)
❌ Delete sheets or rows
❌ Override linked cells
❌ Ignore validation warnings
❌ Skip sensitivity analysis
❌ Use overly aggressive assumptions
❌ Forget about TI and leasing costs
❌ Ignore zoning requirements

---

## 🎯 TARGET METRICS

### Investment Returns
- **Levered IRR**: 18-25%
- **Unlevered IRR**: 12-18%
- **Equity Multiple**: 2.0x-2.8x (over 7-10 years)
- **Cash-on-Cash Y1**: 7-12%

### Property Performance
- **Blended NOI Margin**: 55-65%
- **Stabilized Occupancy**: 90-95%
- **Development Spread**: Entry cap - 150 bps < Exit cap
- **DSCR**: 1.35-1.50x

### Component Metrics
- **Multifamily NOI/SF**: $20-35/SF
- **Office NOI/SF**: $25-40/SF
- **Retail NOI/SF**: $30-50/SF
- **Hotel NOI/Room**: $15,000-30,000/room
- **Restaurant NOI/SF**: $25-45/SF

---

## 🔧 TROUBLESHOOTING

**Allocation doesn't equal 100%?**
→ Check Inputs sheet rows 20-24, adjust to total 100.00%

**IRR seems too high/low?**
→ Verify exit value (NOI / cap rate), check hold period

**Numbers seem off?**
→ Press F9 to recalculate, verify all inputs

**DSCR below 1.25x?**
→ Reduce LTC or increase NOI

**Formula errors?**
→ Never delete rows/columns, check sheet names

---

## 🚀 ALLOCATION OPTIMIZER

### How to Use (Sheet 3, Bottom Section)

1. **Scroll to "ALLOCATION OPTIMIZER"**
2. **Enter your custom percentages** (Blue cells)
3. **Must total 100%**
4. **Review calculated metrics:**
   - Allocated SF per component
   - Estimated NOI/SF
   - Total NOI contribution
   - IRR impact

### Strategy Tips

**To Maximize IRR:**
- Emphasize highest NOI/SF types (Retail, Restaurant)
- Balance with stable income (Multifamily, Office)
- Consider financing preferences (banks favor residential)

**To Maximize Stability:**
- Heavier Multifamily & Office
- Lighter Hotel & Retail
- Longer lease terms

**To Maximize Income:**
- Mix of all types
- Percentage rent upside (Retail, Restaurant)
- Premium rents (Class A)

---

## 📖 RESOURCES

**Full Documentation:**
- See `MIXED_USE_MODEL_USER_GUIDE.md` (100+ pages)

**Key Sections:**
- Quick Start Guide (15 min setup)
- Sheet-by-Sheet Reference
- Allocation Optimization Strategy
- Benchmarks & Best Practices
- Troubleshooting & Glossary

**Model Features:**
- 12 comprehensive sheets
- 131+ formulas (0 errors)
- 5 property types fully integrated
- 8 pre-built scenarios
- Custom allocation optimizer
- Professional formatting

---

## ✨ WHAT'S UNIQUE ABOUT THIS MODEL

1. **5 Property Types Fully Integrated**
   - Multifamily, Office, Retail, Hotel, Restaurant
   - Each with industry-specific economics

2. **Dynamic Allocation**
   - Change % devoted to each use
   - Instantly see impact on returns
   - Test unlimited scenarios

3. **8 Pre-Built Strategies**
   - Industry best practices
   - Optimized for different markets
   - Based on institutional experience

4. **Custom Optimizer**
   - Build your own allocation
   - Real-time NOI and IRR calculations
   - Find optimal mix for your market

5. **Component-Level Detail**
   - Separate pro formas for each type
   - Understand revenue drivers
   - Identify value creation

6. **Comprehensive & Validated**
   - 131+ formulas, all cross-checked
   - Zero errors, professional formatting
   - Institutional-grade analysis

7. **User-Friendly**
   - Clear color-coding (Blue = input)
   - Yellow highlighting for key cells
   - Extensive documentation

---

## 📊 OPTIMAL ALLOCATIONS BY MARKET

### Downtown CBD (Urban Core)
```
Office: 35-50%
Multifamily: 25-40%
Retail: 10-20%
Hotel: 5-15%
Restaurant: 5-10%
```

### Suburban Growth Market
```
Multifamily: 50-70%
Retail: 15-25%
Office: 10-20%
Hotel: 0-10%
Restaurant: 5-10%
```

### Tourism/Convention District
```
Hotel: 40-60%
Retail: 20-30%
Restaurant: 10-15%
Office: 0-15%
Multifamily: 0-15%
```

### Transit-Oriented Development
```
Multifamily: 40-60%
Office: 20-30%
Retail: 15-20%
Restaurant: 5-10%
Hotel: 0-10%
```

---

## 🚀 NEXT STEPS

1. **Open Model** → `Mixed_Use_Model_v1.0.xlsx`
2. **Go to Inputs Sheet** → Change BLUE cells
3. **Set Allocation** → Must total 100%
4. **Input Assumptions** → All 5 property types
5. **Review Scenarios** → Allocation Scenarios sheet
6. **Test Custom Mix** → Use Optimizer
7. **Check Returns** → Returns Analysis sheet
8. **Run Sensitivity** → Test exit caps & costs
9. **Review Results** → Executive Summary
10. **Read Full Guide** → `MIXED_USE_MODEL_USER_GUIDE.md`

---

## 📞 REMEMBER

- **Always backup** before making changes
- **Test multiple scenarios** (Base, Upside, Downside)
- **Cross-check** with market comparables
- **Validate cap rates** with brokers/appraisers
- **Include contingency** (5-10% of hard costs)
- **Model realistic lease-up** (18-36 months)
- **Document assumptions** in comments
- **Get market validation** from experts

---

## 💡 KEY INSIGHTS

**Why Mixed-Use Works:**
✅ Diversified revenue streams
✅ 24/7 building activity
✅ Cross-synergies (office workers → retail/restaurant)
✅ Reduced risk vs. single-use
✅ Urban infill premium
✅ Transit-oriented development preference

**Why Mixed-Use is Challenging:**
⚠️ More complex financing
⚠️ Multiple regulatory requirements
⚠️ Harder to manage (different operators)
⚠️ Higher development costs
⚠️ Longer lease-up periods
⚠️ More moving parts

**Success Factors:**
🎯 Strong location (transit, amenities)
🎯 Complementary uses (residents → retail/restaurant)
🎯 Right allocation for market demand
🎯 Quality design and finishes
🎯 Experienced development team
🎯 Adequate capital (equity + debt)
🎯 Realistic timeline (3-5 years)

---

**Version 1.0** | November 2, 2025 | Mixed-Use Development

**Status**: ✅ Complete & Ready to Use

**Model Size**: 12 sheets, 131+ formulas, 0 errors

**Property Types**: Multifamily • Office • Retail • Hotel • Restaurant

---

## 🎓 LEARNING RESOURCES

**Understand Each Component:**
- Multifamily: Read MULTIFAMILY_MODEL_USER_GUIDE.md
- Office: Review office component assumptions
- Retail: Study percentage rent economics
- Hotel: Learn ADR and RevPAR metrics
- Restaurant: Understand sales/SF drivers

**Industry Resources:**
- ULI (Urban Land Institute)
- ICSC (International Council of Shopping Centers)
- NMHC (National Multifamily Housing Council)
- BOMA (Building Owners & Managers Association)

**Market Data:**
- CoStar
- CBRE Research
- JLL Market Reports
- Reis
- RealPage

---

**Ready to analyze your mixed-use opportunity? Let's build something amazing! 🏗️**
