# LBO Model - Complete Input Reference Guide

## 🎨 Quick Reference: All Blue Input Cells

This document lists EVERY input cell (blue text with yellow highlight) in the model.

---

## 📑 Transaction Assumptions Sheet

### Company Information
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C7 | Company Name | "Target Company Inc." | Name of acquisition target |
| C8 | Industry | "Consumer Products" | Industry sector |
| C9 | Transaction Date | 1/1/2025 | LBO closing date |
| C10 | Holding Period (Years) | 5 | Typical PE hold period: 3-7 years |

### Entry Valuation
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C16 | LTM Revenue ($M) | 500.0 | Last twelve months revenue |
| C17 | LTM EBITDA ($M) | 100.0 | Last twelve months EBITDA |
| C20 | Entry EV / Revenue Multiple | 2.0x | Typically 1.0x to 3.0x |
| C21 | Entry EV / EBITDA Multiple | 10.0x | PRIMARY: Typically 8.0x to 12.0x |

### Financing Assumptions
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C28 | Total Leverage (Debt / EBITDA) | 5.0x | Total debt, typically 4.0x to 6.0x |
| C29 | Senior Leverage (Senior / EBITDA) | 4.0x | Bank debt only, typically 3.0x to 4.5x |

### Transaction Costs
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C37 | M&A Advisory Fees (% of EV) | 1.5% | Typically 1.0% to 2.0% |
| C38 | Legal & Other Fees ($M) | 3.0 | Lump sum for legal, due diligence |
| C39 | Financing Fees (% of Debt) | 2.0% | Typically 1.5% to 3.0% |

### Exit Assumptions
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C48 | Exit EV / EBITDA Multiple | 10.0x | Conservative = entry multiple |

---

## 💰 Sources & Uses Sheet

### Debt Financing
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C9 | Revolving Credit Facility | $0 | Usually undrawn at close |
| C10 | Term Loan A | $200M | Senior secured debt |
| C11 | Term Loan B | $200M | Senior secured debt |
| C12 | Subordinated Debt | $100M | Junior/mezzanine debt |

### Equity Financing
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C17 | Sponsor Equity | $450M | PE firm investment |
| C18 | Management Rollover | $50M | Management's equity |

### Uses Adjustments
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| F10 | Less: Existing Cash | $0 | Target's cash (if cash-free deal) |
| F11 | Plus: Existing Debt Payoff | $0 | Refinancing existing debt |

---

## 📊 Debt Schedule Sheet

### Revolving Credit Facility
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C12 | Interest Rate (% p.a.) | 5.0% | As of Oct 2025: SOFR + 200-250bps |
| C13 | Undrawn Fee (%) | 0.5% | Typical: 0.25% to 0.50% |

### Term Loan A
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C18 | Interest Rate (% p.a.) | 6.0% | As of Oct 2025: SOFR + 300-350bps |
| C19 | Mandatory Amortization (%) | 5.0% | % of original principal, annually |
| C20 | Cash Sweep (%) | 100% | % of excess cash to TLA paydown |

### Term Loan B
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C24 | Interest Rate (% p.a.) | 7.5% | As of Oct 2025: SOFR + 450-500bps |
| C25 | Mandatory Amortization (%) | 1.0% | Usually 0% to 1% |
| C26 | Cash Sweep (%) | 50% | After TLA paid off |

### Subordinated Debt
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C30 | Interest Rate (% p.a.) | 10.0% | Typically 10% to 14% |

### Cash Sweep Parameters
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C70 | Minimum Cash Balance ($M) | $20M | Required operating cash |

---

## 📈 Financial Statements Sheet

### Revenue Projections
| Cells | Input | Example | Notes |
|-------|-------|---------|-------|
| D11-K11 | Revenue Growth % (Years 1-7) | 5% each year | Typical: 3% to 10% annually |

### EBITDA Projections
| Cells | Input | Example | Notes |
|-------|-------|---------|-------|
| D14-K14 | EBITDA Margin % (Years 1-7) | 22% each year | Target margin expansion |

### Depreciation & Amortization
| Cells | Input | Example | Notes |
|-------|-------|---------|-------|
| C16-K16 | D&A Expense ($M) | $15M each year | Typically 2% to 5% of revenue |

### Tax Rate
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C25 | Tax Rate % | 25% | US federal: 21%, state: 4-7% |

### Capital Expenditures
| Cells | Input | Example | Notes |
|-------|-------|---------|-------|
| C36-K36 | CapEx % of Revenue | 3% each year | Maintenance: 2-4%, Growth: +1-3% |

### Net Working Capital
| Cells | Input | Example | Notes |
|-------|-------|---------|-------|
| C39-K39 | NWC % of Revenue | 10% each year | Varies by business model |

---

## 💹 Returns Analysis Sheet

**No inputs required** - all calculations link from other sheets

**Key Outputs:**
- Equity IRR: Target 20-30%
- MOIC: Target 2.5x-3.0x for 5-year hold
- Total Cash Return ($)
- Total % Return

---

## 💧 Distribution Waterfall Sheet

### Waterfall Assumptions
| Cell | Input | Example | Notes |
|------|-------|---------|-------|
| C8 | Preferred Return (IRR Hurdle) | 8.0% | Typically 7% to 10% |
| C9 | GP Catch-Up % | 100% | Usually 100% or 50% |
| C10 | Carried Interest % | 20% | Typically 15% to 25% |

---

## ⚡ Sensitivity Analysis Sheet

**No inputs required** - sensitivity tables are auto-populated

**Tables Provided:**
1. Exit Multiple vs Entry Multiple
2. EBITDA Growth vs Exit Multiple

---

## 📝 Summary: Total Input Requirements

| Sheet | # of Input Cells | Time to Complete |
|-------|------------------|------------------|
| Transaction Assumptions | 10 | 10 min |
| Sources & Uses | 8 | 10 min |
| Debt Schedule | 9 | 10 min |
| Financial Statements | 30+ | 20 min |
| Distribution Waterfall | 3 | 5 min |
| **TOTAL** | **60+** | **55-60 min** |

---

## 🎯 Minimum Viable Model (30 Minutes)

To get a functional LBO model quickly:

### Phase 1: Deal Structure (15 min)
1. **Transaction Assumptions** (10 min)
   - C7-C10: Company info and dates
   - C16-C17: LTM Revenue and EBITDA
   - C21: Entry multiple
   - C28-C29: Leverage ratios
   - C48: Exit multiple

2. **Sources & Uses** (5 min)
   - C10-C12: Debt tranches
   - C17-C18: Equity amounts

### Phase 2: Operating Model (10 min)
1. **Debt Schedule** (5 min)
   - C12, C18, C24, C30: Interest rates
   - C19, C25: Amortization %
   - C20, C26: Cash sweep %

2. **Financial Statements** (5 min)
   - D11-K11: Revenue growth (use 5% for all)
   - D14-K14: EBITDA margin (use 22% for all)
   - C36-K36: CapEx % (use 3% for all)
   - C39-K39: NWC % (use 10% for all)

### Phase 3: Review (5 min)
1. **Executive Summary**
   - Check IRR and MOIC
   - Validate leverage ratios
   - Review interest coverage

This gives you a working model with reasonable assumptions that you can refine later.

---

## ✅ Input Validation Tips

### Entry Valuation
- **EV/EBITDA Multiple:** Compare to publicly traded comps and recent M&A deals
  - Software: 10-15x
  - Healthcare: 8-12x
  - Manufacturing: 6-9x
  - Retail: 5-8x
- **Leverage:** Higher for stable, recurring revenue businesses
  - Software/SaaS: 5-7x
  - Healthcare: 4-6x
  - Manufacturing: 3-5x
  - Retail: 3-4x

### Operating Assumptions
- **Revenue Growth:** Should exceed GDP growth (2-3%) but be achievable
  - Mature markets: 3-5%
  - Growth markets: 6-10%
  - Transformation story: 10%+
- **EBITDA Margins:** Compare to industry averages and historical performance
  - Can model 100-300bps of margin expansion over 5 years
  - Validate with specific operational initiatives
- **CapEx:** Distinguish between maintenance and growth
  - Maintenance: Replace aging assets (typically 2-4% of revenue)
  - Growth: Expand capacity (add 1-3%)
- **NWC:** Match to business model
  - SaaS: 0-5% (negative NWC common due to deferred revenue)
  - Distribution: 10-15%
  - Manufacturing: 15-20%
  - Retail: 20-25%

### Debt Terms (As of October 2025)
- **Revolver:** SOFR + 200-250 bps (5.0-5.5%)
- **Term Loan A:** SOFR + 300-350 bps (6.0-6.5%)
- **Term Loan B:** SOFR + 450-500 bps (7.5-8.0%)
- **Subordinated:** 10-14% (fixed rate)
- **Mezzanine:** 12-16% (with equity kickers)

### Return Targets
- **Minimum IRR:** 15% (below PE hurdle)
- **Target IRR:** 20-30% (standard PE target)
- **Exceptional IRR:** 35%+ (home runs)
- **MOIC Benchmarks:**
  - 3-year hold: 2.0x = 26% IRR
  - 5-year hold: 2.5x = 20% IRR
  - 7-year hold: 3.0x = 17% IRR

### Credit Metrics
- **Total Leverage (Debt/EBITDA):**
  - Maximum at entry: 6.0-7.0x
  - Target at exit: 3.0-4.0x
- **Interest Coverage (EBITDA/Interest):**
  - Minimum: 2.0x
  - Target: 2.5-3.0x
  - Comfortable: 3.5x+

---

## 🔍 Common Data Sources

### Public Information
- **SEC Filings (sec.gov):** 10-K, 10-Q, 8-K for public targets
- **Capital IQ / Bloomberg:** Comparable company data
- **PitchBook / FactSet:** M&A transaction multiples
- **S&P LCD:** Leveraged loan market terms
- **FRED (Federal Reserve):** SOFR rates, economic data

### Industry Research
- **IBISWorld:** Industry analysis and benchmarks
- **Gartner / Forrester:** Technology sector analysis
- **McKinsey / BCG / Bain:** Strategy consulting reports
- **Trade Publications:** Industry-specific data

### PE Market Data
- **Preqin:** Historical PE fund performance
- **PEI (Private Equity International):** Market trends
- **Bain Global Private Equity Report:** Annual PE trends
- **Cambridge Associates:** PE benchmark returns

---

## 🎓 Learning Resources

### For Beginners
1. Start with Transaction Assumptions (understand the deal)
2. Then Sources & Uses (understand the capital structure)
3. Then Debt Schedule (understand the financing)
4. Finally Financial Statements (understand the business)

### For Intermediate Users
1. Focus on sensitivity analysis (what drives returns?)
2. Model different exit scenarios (timing and multiple)
3. Stress test leverage (what if EBITDA drops 20%?)
4. Compare to historical deals (is this market?)

### For Advanced Users
1. Add complexity (PIK toggle, OID, warrants)
2. Model bolt-on acquisitions
3. Add dividend recaps
4. Model management equity rollovers with different terms
5. Add working capital revolver dynamics

---

## 💡 Pro Tips

### Input Efficiency
1. **Template Assumptions:** Save a "base case" template with standard assumptions for your industry
2. **Scenario Manager:** Use Excel's Scenario Manager to save Bear/Base/Bull cases
3. **Data Validation:** Set up dropdown lists for industry-standard inputs
4. **Named Ranges:** Name key input cells for easier reference

### Assumption Setting
1. **Start Conservative:** Better to beat expectations than miss them
2. **Triangulate:** Use multiple methods to validate assumptions (comps, historicals, management)
3. **Probability Weight:** Don't just model 3 scenarios - weight them by probability
4. **Sanity Check:** Does the deal make sense at these assumptions?

### Model Maintenance
1. **Update Market Data:** Interest rates, multiples, and leverage standards change quarterly
2. **Track Actuals:** Compare model to actual results and adjust assumptions
3. **Document Changes:** Note when and why you changed key assumptions
4. **Version Control:** Save dated versions of the model

---

## 🎯 Model Validation Checklist

Before presenting your LBO model:

### Structural Checks
- [ ] All blue input cells have values (no zeros unless intentional)
- [ ] Sources = Uses (Sources & Uses sheet check = 0)
- [ ] All formulas calculate correctly (no #REF!, #DIV/0!, #VALUE!)
- [ ] Years are consistent across all sheets
- [ ] Currency formatting is consistent ($M throughout)

### Reasonableness Checks
- [ ] Entry multiple is market (compare to recent deals)
- [ ] Leverage ratios are achievable (compare to rating agency guidelines)
- [ ] Interest rates reflect current market (check SOFR + spreads)
- [ ] Revenue growth is defensible (compare to GDP, industry, historicals)
- [ ] EBITDA margins are realistic (compare to peers, historicals)
- [ ] Exit multiple is conservative (generally = entry multiple)

### Returns Checks
- [ ] IRR meets minimum hurdle (typically 20%+)
- [ ] MOIC is appropriate for hold period (typically 2.5x+ for 5 years)
- [ ] Returns are not solely dependent on multiple expansion
- [ ] Downside scenario still generates acceptable returns (15%+ IRR)
- [ ] Leverage paydown is reasonable (3-4x remaining at exit)

### Credit Checks
- [ ] Interest coverage > 2.0x in all years
- [ ] Leverage ratio declines over time
- [ ] Free cash flow is positive in all years
- [ ] Minimum cash balance is maintained
- [ ] No covenant breaches projected

### Documentation Checks
- [ ] Key assumptions are clearly marked (blue = input)
- [ ] Formulas are transparent (no circular references)
- [ ] Links between sheets work correctly (green = link)
- [ ] Sensitivity tables are set up correctly
- [ ] Distribution waterfall calculates correctly (check = 0)

---

## 🚨 Common Mistakes to Avoid

### Deal Structure Mistakes
1. **Over-Leveraging:** Using leverage > 6.0x without justification
2. **Unrealistic Terms:** Assuming TLB at TLA pricing
3. **Ignoring Covenants:** Not modeling debt covenant compliance
4. **Circular Logic:** Equity = Sources - Debt, but Debt = EBITDA × Leverage

### Operating Assumption Mistakes
1. **Hockey Sticks:** Showing dramatic margin expansion without clear plan
2. **Perpetual Growth:** Using 10%+ revenue growth for all years
3. **Ignoring Cyclicality:** Not modeling economic downturns
4. **CapEx Too Low:** Not enough CapEx to support revenue growth

### Returns Mistakes
1. **Multiple Expansion Dependency:** Relying on exit multiple > entry multiple
2. **Ignoring Time Value:** Looking at MOIC without considering holding period
3. **Forgetting Fees:** Not accounting for transaction costs, financing fees
4. **No Downside Case:** Only modeling upside scenarios

### Technical Mistakes
1. **Hardcoding Values:** Typing numbers into formula cells (should be blue inputs)
2. **Broken Links:** Links to other sheets that don't work
3. **Inconsistent Periods:** Mixing annual and quarterly data
4. **Wrong References:** Formula pulling from wrong cell/sheet

---

## 📧 Support & Resources

### Quick Help
- Review the User Guide for detailed explanations
- Check this Input Reference for every required input
- Validate assumptions against industry benchmarks
- Model multiple scenarios (Bear/Base/Bull)

### Model Updates
This model reflects:
- **Market Conditions:** October 2025
- **Interest Rates:** SOFR-based (post-LIBOR transition)
- **Leverage Standards:** Post-2008 financial crisis norms
- **PE Return Expectations:** Current LP expectations

### Continuous Learning
- Follow PE firms' annual reports for return expectations
- Monitor S&P LCD for debt market trends
- Read PEI and Preqin for transaction data
- Attend industry conferences (SuperReturn, etc.)

---

**END OF INPUT REFERENCE**

**Model Version:** 1.0 (October 2025)
**Last Updated:** October 29, 2025
**Compatible Versions:** Excel 2016+, Google Sheets (with limitations)
