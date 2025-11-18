# HOTEL FINANCIAL MODEL - QUICK REFERENCE CARD

## ðŸ"Š **ONE-PAGE GUIDE**

---

## ðŸŽ¯ MODEL FILES
- **Main Model**: `Hotel_Model_Comprehensive.xlsx`
- **User Guide**: `HOTEL_MODEL_USER_GUIDE.md`
- **Status**: âœ… 478 formulas, 0 errors

---

## ðŸ"‹ SHEET OVERVIEW

| # | Sheet | Purpose |
|---|-------|---------|
| 1 | **Executive Summary** | Dashboard - All key metrics |
| 2 | **Inputs** | â­ ALL ASSUMPTIONS - Change BLUE cells only |
| 3 | **Pro Forma** | 10-year revenue & expense projections |
| 4 | **Cash Flow Analysis** | Investment cash flows & debt service |
| 5 | **Returns Analysis** | IRR, equity multiple, exit value |
| 6 | **Segment Benchmarks** | Industry data by hotel type |

---

## âš¡ QUICK START (10 MINUTES)

### 1. Property Basics (Inputs Sheet, Rows 4-9)
```
Property Name: [Your Hotel Name]
Hotel Type: Luxury | Upper Upscale | Upscale | Midscale | Economy
Location: [City/Market]
Opening Date: [MM/DD/YYYY]
Number of Rooms: [50-1,000+]
Average Room Size: [250-700 SF]
```

### 2. Revenue Assumptions (Inputs Sheet, Rows 13-37)

**Rooms Revenue:**
```
Year 1 ADR: $_____ (see benchmarks below)
Stabilized Occupancy: __% (68-75% typical)
Ramp-Up Period: ___ months (12-24 typical)
ADR Growth: __% (2.5-4.0% typical)
```

**Brand/Franchise:**
```
Brand: [Marriott, Hilton, Hyatt, IHG, etc.]
Operating Structure: Franchise | Management Agreement
Royalty Fee: 4-6% of rooms revenue
Marketing Fee: 2-4% of rooms revenue
Technology Fee: 1-2% of rooms revenue
```

**F&B Revenue:**
```
Outlet Revenue/Room/Day: $_____
Banquet Revenue/Group Room Night: $_____
Group % of Total Rooms: 30-40%
```

### 3. Operating Expenses (Inputs Sheet, Rows 41-50)
```
Rooms Dept OpEx: 20-35% of rooms revenue
F&B Dept OpEx: 60-75% of F&B revenue
Other Dept OpEx: 30-40% of other revenue
Undistributed OpEx: $6,000-12,000 per room/year
```

### 4. Development Costs (Inputs Sheet, Rows 54-60)
```
Land Cost: $_____
Hard Costs/Room: $_____ (see benchmarks)
Soft Costs: 15-25% of hard costs
FF&E/Room: $_____ (see benchmarks)
Pre-Opening/Room: $6,000-10,000
Contingency: 5% minimum
```

### 5. Financing (Inputs Sheet, Rows 64-67)
```
Loan-to-Cost: 55-70%
Interest Rate: 6.0-7.5%
Loan Term: 5-30 years
Amortization: 25-30 years
```

### 6. Exit Assumptions (Inputs Sheet, Rows 71-73)
```
Hold Period: 5-10 years
Exit Cap Rate: __% (see benchmarks)
Selling Costs: 2.0-3.0%
```

---

## 📊 2024 INDUSTRY BENCHMARKS BY SEGMENT

### ADR (Average Daily Rate)

| Segment | ADR Range | 2024 US Avg |
|---------|-----------|-------------|
| **Luxury** | $300-$500 | $380 |
| **Upper Upscale** | $200-$300 | $227 |
| **Upscale** | $120-$200 | $186 |
| **Midscale** | $70-$120 | $95 |
| **Economy** | $50-$90 | $70 |

### Occupancy Rates

| Segment | Target Range |
|---------|--------------|
| **Luxury** | 68-75% |
| **Upper Upscale** | 68-72% |
| **Upscale** | 68-72% |
| **Midscale** | 58-65% |
| **Economy** | 55-63% |

### RevPAR (Revenue Per Available Room)

| Segment | RevPAR Range | Formula |
|---------|--------------|---------|
| **Luxury** | $200-$375 | ADR × Occ% |
| **Upper Upscale** | $135-$215 | |
| **Upscale** | $80-$145 | |
| **Midscale** | $40-$75 | |
| **Economy** | $30-$55 | |

### GOP (Gross Operating Profit) Margins

| Segment | GOP Margin | What It Means |
|---------|------------|---------------|
| **Luxury** | 35-45% | Highest margins, highest costs |
| **Upper Upscale** | 35-42% | Strong balance |
| **Upscale** | 30-40% | Good efficiency |
| **Midscale** | 25-35% | Lean operations |
| **Economy** | 20-30% | Cost-focused |

### Development Costs (per room)

| Segment | Construction | FF&E | Room Size |
|---------|--------------|------|-----------|
| **Luxury** | $500k-$1M+ | $35k-$75k | 500-700 SF |
| **Upper Upscale** | $350k-$500k | $25k-$40k | 450-550 SF |
| **Upscale** | $250k-$350k | $15k-$25k | 400-450 SF |
| **Midscale** | $150k-$250k | $10k-$15k | 300-400 SF |
| **Economy** | $80k-$150k | $5k-$10k | 250-350 SF |

### F&B Revenue (Full-Service Hotels)

| Segment | Outlet $/Room/Day | Banquet $/Group Room |
|---------|-------------------|----------------------|
| **Luxury** | $50-$80 | $150-$200 |
| **Upper Upscale** | $35-$50 | $90-$120 |
| **Upscale** | $25-$40 | $50-$80 |
| **Midscale** | $15-$25 | $30-$50 |

### Exit Cap Rates

| Segment | Cap Rate Range |
|---------|----------------|
| **Luxury** | 6.0-7.5% |
| **Upper Upscale** | 6.5-7.5% |
| **Upscale** | 7.0-8.0% |
| **Midscale** | 7.5-8.5% |
| **Economy** | 8.0-9.0% |

---

## ðŸ"' KEY FORMULA REFERENCE

### Revenue Calculations
```
Rooms Revenue = Occupied Room Nights × ADR
RevPAR = ADR × Occupancy%
F&B Outlet Revenue = Occupied Rooms × $/Room/Day × 365
Banquet Revenue = Group Room Nights × $/Group Room
```

### Profitability Metrics
```
GOP = Total Revenue - Operating Expenses
GOP Margin = GOP / Total Revenue
NOI = GOP (simplified in this model)
```

### Investment Returns
```
Exit Value = Year 10 NOI / Exit Cap Rate
Net Proceeds = Exit Value - Selling Costs - Loan Balance
IRR = Internal rate of return on equity cash flows
Equity Multiple = Total Cash Returned / Equity Invested
```

### Debt Service
```
Annual Payment = PMT(Interest Rate, Amortization Years, -Loan Amount)
```

---

## ðŸ"Š KEY METRICS DASHBOARD

### Operating Metrics
- **ADR**: Average price per occupied room
- **Occupancy**: % of rooms sold
- **RevPAR**: Revenue productivity (ADR × Occ%)
- **GOP Margin**: Operating profit %

### Investment Metrics
- **Yield on Cost**: NOI / Total Development Cost
- **Cash-on-Cash**: Annual cash flow / Equity invested
- **Levered IRR**: Time-adjusted return (target: 15-25%)
- **Equity Multiple**: Total return multiple (target: 2.0-3.0x)

---

## 🎯 TARGET RETURNS BY STRATEGY

| Strategy | Risk | IRR Target | Multiple | Hold Period |
|----------|------|------------|----------|-------------|
| **Development** | Highest | 20-25%+ | 2.5-3.5x | 7-10 years |
| **Value-Add** | Moderate-High | 18-22% | 2.0-2.5x | 5-7 years |
| **Core-Plus** | Moderate | 15-18% | 1.8-2.2x | 5-7 years |
| **Core** | Low-Moderate | 12-15% | 1.5-2.0x | 5-10 years |

---

## 🌟 MAJOR HOTEL BRANDS BY SEGMENT

### Luxury
- Ritz-Carlton, Four Seasons, St. Regis, Waldorf Astoria, Rosewood

### Upper Upscale
- Marriott Hotels, Hilton, Hyatt Regency, Westin, Sheraton

### Upscale
- Courtyard, Hilton Garden Inn, Hyatt Place, Aloft, AC Hotels

### Midscale
- Hampton Inn, Fairfield Inn, Holiday Inn Express, Comfort Inn, La Quinta

### Economy
- Super 8, Days Inn, Motel 6, Red Roof Inn, Microtel

---

## ⚠ï¸ CRITICAL ASSUMPTIONS TO VERIFY

### Must Research for Your Market
1. **ADR**: Check STR reports or OTA pricing for comp set
2. **Occupancy**: Get market penetration data
3. **Construction Costs**: Get local contractor bids
4. **Land Cost**: Research recent comps
5. **Property Taxes**: Check local assessor rates
6. **Labor Costs**: Adjust for local wage rates

### Common Pitfalls to Avoid
❌ Using peak ADR as Year 1 assumption
âœ… Start conservative, ramp to stabilized

❌ Showing full occupancy in Year 1
âœ… Model 12-24 month ramp-up period

❌ Forgetting franchise fees (7-12% of rooms revenue)
âœ… Include all brand fees in operating expenses

❌ Omitting FF&E reserve (4% of revenue)
âœ… Include capital reserve for renovations

❌ Using Year 1 NOI for exit value
âœ… Use Year 10 NOI (or year after exit)

---

## 💡 PRO TIPS

### Sensitivity Testing
Test these variables:
- ADR: ±10%, ±20%
- Occupancy: ±5 points
- Development Cost: +10%, +20%
- Exit Cap Rate: ±0.5%, ±1.0%

### Three Scenarios
1. **Base Case**: Most likely (median assumptions)
2. **Upside**: Optimistic (75th percentile)
3. **Downside**: Conservative (25th percentile)

### Optimization Levers
- **Increase ADR**: Premium brand, better location, add amenities
- **Improve Occupancy**: Strong sales team, OTA strategy, loyalty program
- **Reduce OpEx**: Energy efficiency, labor productivity, procurement
- **Lower Development Cost**: Value engineering, competitive bids

---

## 📈 MARKET TIMING CONSIDERATIONS

### Best Time to Develop
- Low construction costs (recession)
- Hotel supply declining (limited competition)
- Demand projected to grow (economic expansion)
- 2-3 years before market peak

### Best Time to Sell
- Peak occupancy and ADR
- Low cap rates (high valuations)
- Strong buyer demand
- Before oversupply hits market

---

## 🔧 QUICK TROUBLESHOOTING

**Problem**: IRR seems too low
- Check if exit value includes Year 10 NOI
- Verify loan balance is subtracted from exit proceeds
- Ensure Year 0 equity is negative (cash outflow)

**Problem**: GOP margin seems off
- Compare to Segment Benchmarks sheet
- Check if franchise fees are included
- Verify labor costs are reasonable for segment

**Problem**: Development cost per room too high/low
- Check all components (land, hard, soft, FF&E, pre-opening, fees)
- Add contingency (5% minimum)
- Compare to benchmark ranges

---

## 📚 DATA SOURCES (2024)

- **STR**: US hotel industry data (ADR: $159, Occ: 63%, RevPAR: $100)
- **CoStar**: Market performance by segment
- **CBRE Hotels Research**: GOP margins, operating ratios
- **HVS**: Franchise fees, development costs
- **Lodging Econometrics**: Supply pipeline data

---

## 📞 NEED MORE DETAIL?

See the full **HOTEL_MODEL_USER_GUIDE.md** for:
- Detailed sheet-by-sheet explanations
- Step-by-step usage instructions
- Advanced sensitivity analysis
- Common mistakes and solutions
- FAQs and best practices
- Hotel investment strategies
- Success metrics and KPIs

---

## âš ï¸ DISCLAIMER

This model is for **educational and analytical purposes only**. All investment decisions should be made with professional advice and thorough due diligence. Hotel investments carry significant risk. Past performance does not guarantee future results.

**Model Version**: 1.0  
**Last Updated**: November 2025  
**Industry Data**: 2024 calendar year

---

## ✅ FINAL CHECKLIST

Before presenting your analysis:

- [ ] Verified ADR matches market research
- [ ] Occupancy assumptions realistic for segment
- [ ] Ramp-up period modeled (Year 1 lower than stabilized)
- [ ] All franchise/brand fees included in expenses
- [ ] FF&E reserve (4% of revenue) included
- [ ] Development cost includes all components + contingency
- [ ] Financing terms match lender quotes
- [ ] Exit cap rate validated with broker/appraiser
- [ ] Loan balance subtracted from exit proceeds
- [ ] IRR and equity multiple calculated correctly
- [ ] Compared all assumptions to Segment Benchmarks sheet
- [ ] Created sensitivity scenarios (base, upside, downside)

---

**BLUE cells** = Your inputs | **BLACK cells** = Formulas | **GREEN cells** = Links to other sheets

**Remember**: Garbage in = Garbage out. Quality of analysis depends on quality of assumptions!
