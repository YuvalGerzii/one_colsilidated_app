# DCF Model - Complete Input Reference Guide

## 🎨 Quick Reference: All Blue Input Cells

This document lists EVERY input cell (blue text with yellow highlight) in the model.

---

## 📑 DCF Sheet

### Company Information
| Cell | Input | Example |
|------|-------|---------|
| D8 | Company Name | "Apple Inc." |
| D9 | Ticker Symbol | "AAPL" |
| D10 | Current Share Price | 150.00 |
| D13 | Effective Tax Rate | 25% |
| D14 | Projection Years | 5 |

### Balance Sheet Items
| Cell | Input | Example |
|------|-------|---------|
| D19 | Cash & Cash Equivalents ($M) | 50,000 |
| D20 | Total Debt ($M) | 100,000 |
| D21 | Preferred Stock ($M) | 0 |
| D22 | Minority Interest ($M) | 5,000 |

### Terminal Value Assumptions
| Cell | Input | Example |
|------|-------|---------|
| H10 | Terminal Growth Rate | 2.5% |
| H11 | Terminal EBITDA Multiple | 10.0x |
| H12 | Method ("Growth" or "Multiple") | "Growth" |

### Revenue Projections
| Cell | Input | Example |
|------|-------|---------|
| C37 | Historical Revenue ($M) | 300,000 |
| D37 | Base Year Revenue ($M) | 320,000 |
| E38-I38 | Revenue Growth Rates (Years 1-5) | 5%, 5%, 4%, 4%, 3% |

### Operating Assumptions
| Cells | Input | Example |
|-------|-------|---------|
| E42-I42 | EBITDA Margin (%) | 20%, 21%, 22%, 23%, 24% |
| E45-I45 | D&A % of Revenue | 3%, 3%, 3%, 3%, 3% |
| E55-I55 | CapEx % of Revenue | 4%, 4%, 3.5%, 3.5%, 3% |
| E58-I58 | NWC % of Revenue | 10%, 10%, 10%, 10%, 10% |

### Shares Outstanding
| Cell | Input | Example |
|------|-------|---------|
| D48 | Diluted Shares Outstanding (M) | 16,000 |

---

## 💰 WACC Sheet

### Cost of Equity
| Cell | Input | Example |
|------|-------|---------|
| F7 | Risk-Free Rate | 3.0% |
| F8 | Equity Risk Premium | 5.0% |
| F9 | Beta (Levered) | 1.2 |

### Cost of Debt
| Cell | Input | Example |
|------|-------|---------|
| F15 | Pre-Tax Cost of Debt | 4.0% |

### Capital Structure
| Cell | Input | Example |
|------|-------|---------|
| F22 | Market Value of Equity ($M) | 2,400,000 |
| F23 | Market Value of Debt ($M) | 100,000 |

### Unlevered Beta Calculation (Optional)
| Cells | Input | Example |
|-------|-------|---------|
| C42-C46 | Comparable Company Names | "Microsoft", "Google", etc. |
| D42-D46 | Levered Betas | 1.1, 1.0, 1.2, 0.9, 1.1 |
| E42-E46 | Debt/Equity Ratios | 0.2, 0.1, 0.3, 0.15, 0.25 |
| F42-F46 | Tax Rates | 25%, 25%, 22%, 24%, 25% |

---

## 🎭 Scenario Analysis Sheet

### Bear Case Assumptions (Column D)
| Row | Input | Example |
|-----|-------|---------|
| D8 | Revenue CAGR | 2% |
| D9 | Terminal Revenue Growth | 1.5% |
| D10 | EBITDA Margin (Year 5) | 15% |
| D11 | Terminal EBITDA Margin | 15% |
| D12 | CapEx % of Revenue | 5% |
| D13 | NWC % of Revenue | 12% |
| D14 | Tax Rate | 28% |
| D15 | WACC | 9% |
| D16 | Terminal Growth Rate | 2% |
| D17 | Terminal EBITDA Multiple | 9x |

### Base Case Assumptions (Column E)
| Row | Input | Note |
|-----|-------|------|
| E8-E17 | Same structure as Bear | Typically links to DCF |

### Bull Case Assumptions (Column F)
| Row | Input | Example |
|-----|-------|---------|
| F8 | Revenue CAGR | 8% |
| F9 | Terminal Revenue Growth | 3.5% |
| F10 | EBITDA Margin (Year 5) | 25% |
| F11 | Terminal EBITDA Margin | 25% |
| F12 | CapEx % of Revenue | 3% |
| F13 | NWC % of Revenue | 8% |
| F14 | Tax Rate | 22% |
| F15 | WACC | 6% |
| F16 | Terminal Growth Rate | 3% |
| F17 | Terminal EBITDA Multiple | 13x |

### Probability Weights
| Cell | Input | Example |
|------|-------|---------|
| D38 | Bear Case Probability | 25% |
| E38 | Base Case Probability | 50% |
| F38 | Bull Case Probability | 25% |

---

## 📊 Historical Financials Sheet

### Income Statement (3-4 Years Historical)
| Cells | Input | Description |
|-------|-------|-------------|
| C9-F9 | Revenue ($M) | Years -3 to Last Year |
| C12-F12 | COGS ($M) | Cost of Goods Sold |
| C18-F18 | SG&A ($M) | Selling, General & Admin |
| C19-F19 | R&D ($M) | Research & Development |
| C20-F20 | Other OpEx ($M) | Other Operating Expenses |
| C27-F27 | D&A ($M) | Depreciation & Amortization |
| C33-F33 | Interest Expense ($M) | Interest paid |
| C34-F34 | Other Income/(Expense) ($M) | Non-operating items |
| C37-F37 | Income Tax Expense ($M) | Taxes paid |

### Balance Sheet
| Cells | Input | Description |
|-------|-------|-------------|
| C47-F47 | Cash & Equivalents ($M) | Cash on hand |
| C48-F48 | Accounts Receivable ($M) | A/R |
| C49-F49 | Inventory ($M) | Inventory |
| C50-F50 | Other Current Assets ($M) | Prepaid, etc. |
| C53-F53 | PP&E ($M) | Property, Plant & Equipment |
| C54-F54 | Intangible Assets ($M) | Patents, etc. |
| C55-F55 | Goodwill ($M) | Goodwill |
| C56-F56 | Other LT Assets ($M) | Long-term assets |
| C60-F60 | Accounts Payable ($M) | A/P |
| C61-F61 | Short-Term Debt ($M) | Current portion of debt |
| C62-F62 | Other Current Liabilities ($M) | Accrued expenses |
| C65-F65 | Long-Term Debt ($M) | Non-current debt |
| C66-F66 | Other LT Liabilities ($M) | Pensions, etc. |
| C69-F69 | Shareholders' Equity ($M) | Book equity |

### Cash Flow Statement
| Cells | Input | Description |
|-------|-------|-------------|
| C78-F78 | Change in Working Capital ($M) | △NWC |
| C79-F79 | Other Operating Activities ($M) | Stock comp, etc. |
| C83-F83 | Capital Expenditures ($M) | CapEx (negative) |
| C84-F84 | Other Investing Activities ($M) | Acquisitions, etc. |
| C88-F88 | Debt Issued / (Repaid) ($M) | Net debt change |
| C89-F89 | Equity Issued / (Repurchased) ($M) | Net equity change |
| C90-F90 | Dividends Paid ($M) | Dividends (negative) |

---

## 🏢 Trading Comps Sheet

### Comparable Companies (10 Companies, Rows 6-15)
| Columns | Input | Description |
|---------|-------|-------------|
| B6-B15 | Company Names | "Microsoft Corp", etc. |
| C6-C15 | Ticker Symbols | "MSFT", etc. |
| D6-D15 | Market Cap ($M) | Market capitalization |
| E6-E15 | Enterprise Value ($M) | EV |
| F6-F15 | Revenue LTM ($M) | Last 12 months revenue |
| G6-G15 | EBITDA LTM ($M) | Last 12 months EBITDA |
| H6-H15 | EBIT LTM ($M) | Last 12 months EBIT |
| I6-I15 | Net Income ($M) | Net income |
| N6-N15 | Revenue Growth (%) | YoY growth rate |

---

## 💼 Working Capital Sheet

### Historical Working Capital (Years -1 and Base)
| Cells | Input | Description |
|-------|-------|-------------|
| C12, D12 | Accounts Receivable ($M) | A/R |
| C15, D15 | Inventory ($M) | Inventory |
| C18, D18 | Prepaid & Other ($M) | Prepaid expenses |
| C26, D26 | Accounts Payable ($M) | A/P |
| C29, D29 | Accrued Expenses ($M) | Accrued liabilities |

### Projected Assumptions (Years 1-5)
| Cells | Input | Description |
|-------|-------|-------------|
| E13-I13 | Days Sales Outstanding | Target DSO (days) |
| E16-I16 | Days Inventory Outstanding | Target DIO (days) |
| E27-I27 | Days Payable Outstanding | Target DPO (days) |
| E19-I19 | Prepaid % of Revenue | Prepaid as % of revenue |
| E30-I30 | Accrued Expenses % of Revenue | Accrued as % of revenue |

---

## 💳 Debt Schedule Sheet

### Debt Tranche 1
| Cell | Input | Example |
|------|-------|---------|
| C9 | Facility Name | "Term Loan A" |
| C10 | Interest Rate | 4.5% |
| C11 | Maturity (Years) | 5 |
| C12 | Annual Amortization (%) | 20% |
| C14 | Beginning Balance ($M) | 50,000 |

### Debt Tranche 2
| Cell | Input | Example |
|------|-------|---------|
| C20 | Facility Name | "Senior Notes" |
| C21 | Interest Rate | 5.5% |
| C22 | Maturity (Years) | 7 |
| C23 | Annual Amortization (%) | 0% |
| C25 | Beginning Balance ($M) | 50,000 |

### Capital Leases
| Cells | Input | Description |
|-------|-------|-------------|
| C40-I40 | Capital Lease Obligations ($M) | Lease liabilities by year |

---

## 💹 Returns Analysis Sheet

### Investment Parameters
| Cell | Input | Example |
|------|-------|---------|
| D9 | Shares Purchased | 1,000 |
| C21-C24 | Annual Dividends/Distributions ($) | Interim cash flows if any |

---

## 🤝 Precedent Transactions Sheet

### Transaction Data (10 Transactions, Rows 6-15)
| Columns | Input | Description |
|---------|-------|-------------|
| B6-B15 | Transaction Date | "MM/DD/YYYY" |
| C6-C15 | Target Company | Company being acquired |
| D6-D15 | Acquirer | Buyer |
| E6-E15 | Deal Value ($M) | Transaction value |
| F6-F15 | Target Revenue LTM ($M) | Revenue of target |
| G6-G15 | Target EBITDA LTM ($M) | EBITDA of target |
| J6-J15 | Premium Paid (%) | Premium over trading price |

---

## 📋 Management Case Sheet

### Management Guidance
| Cells | Input | Description |
|-------|-------|-------------|
| C8 | Year 1 Revenue (Mgmt) ($M) | Management's Year 1 revenue forecast |
| C9-H9 | Revenue Growth Rates (%) | Management's growth rates |
| C11-H11 | EBITDA Margins (%) | Management's margin targets |
| C13-H13 | CapEx % of Revenue | Management's CapEx guidance |

---

## 📝 Summary: Total Input Requirements

| Sheet | # of Input Cells | Time to Complete |
|-------|------------------|------------------|
| DCF | 25-30 | 15-20 min |
| WACC | 5-10 | 5-10 min |
| Scenario Analysis | 30 | 10-15 min |
| Historical Financials | 100+ | 30-45 min |
| Trading Comps | 100 | 20-30 min |
| Working Capital | 15-20 | 10-15 min |
| Debt Schedule | 10-15 | 10 min |
| Returns Analysis | 5-10 | 5 min |
| Precedent Transactions | 60 | 15-20 min |
| Management Case | 20 | 10 min |

**Total Estimated Time:** 2-3 hours for comprehensive completion

---

## 🎯 Minimum Viable Model

If you're short on time, complete these sheets in this order:

1. **DCF** (25 inputs) - CRITICAL
2. **WACC** (5 inputs) - CRITICAL
3. **Historical Financials** (Income Statement only: ~40 inputs) - Validates assumptions
4. **Trading Comps** (5 companies minimum: ~50 inputs) - Cross-check

This gives you a functional model in ~45-60 minutes.

---

## ✅ Input Validation Tips

### Check Your Inputs
- Revenue growth: Typically 0-15% annually
- EBITDA margin: Compare to industry averages (10-30% typical)
- Tax rate: Check company's effective rate in recent filings (20-30% typical)
- WACC: Usually 6-12% for most companies
- Terminal growth: Should be ≤ GDP growth (2-3%)
- Shares outstanding: Verify on Yahoo Finance or company filings

### Common Data Sources
- **Company Filings:** 10-K, 10-Q (SEC.gov)
- **Financial Data:** Bloomberg, FactSet, CapIQ
- **Free Sources:** Yahoo Finance, Google Finance, Seeking Alpha
- **Industry Data:** IBISWorld, Statista
- **Comparable Company Data:** Screener.co, Finviz

---

**END OF INPUT REFERENCE**
