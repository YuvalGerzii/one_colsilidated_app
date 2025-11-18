# Comprehensive DCF Valuation Model - User Guide

## 📊 Overview

This is a professional-grade DCF (Discounted Cash Flow) valuation model with 13 integrated worksheets and advanced features for comprehensive company analysis.

---

## 🎨 Color Coding System

**CRITICAL:** Follow this color coding throughout the model:

- 🔵 **Blue text with yellow highlight** = **INPUT CELLS** (values you need to enter)
- ⚫ **Black text** = **FORMULAS** (automatically calculated)
- 🟢 **Green text** = **LINKS** to other worksheets

---

## 📑 Worksheet Guide

### 1. **Executive Summary** ⭐
**Purpose:** High-level dashboard with key outputs and investment recommendation

**Features:**
- Company overview and current valuation
- Comparison of valuation methods (DCF, Comps, Transactions, Scenarios)
- Key financial metrics summary
- Credit metrics overview
- Investment returns (IRR, MOIC)
- Automated buy/sell recommendation

**Inputs Required:** NONE - All linked from other sheets

---

### 2. **DCF (Discounted Cash Flow)** 🎯
**Purpose:** Core valuation model with cash flow projections

**Key Sections:**
- Company information and assumptions
- Bridge to equity value
- 5-year cash flow projections
- Terminal value calculation
- Valuation output

**INPUTS REQUIRED:**

**Company Info (Cells D8-D14):**
- D8: Company Name
- D9: Ticker Symbol
- D10: Current Share Price
- D13: Effective Tax Rate (%)
- D14: Number of Projection Years (default: 5)

**Balance Sheet Items (Cells D19-D22):**
- D19: Cash & Cash Equivalents ($M)
- D20: Total Debt ($M)
- D21: Preferred Stock ($M)
- D22: Minority Interest ($M)

**Terminal Value (Cells H10-H12):**
- H10: Terminal Growth Rate (%)
- H11: OR Terminal EBITDA Multiple (x)
- H12: Method Selection ("Growth" or "Multiple")

**Cash Flow Projections:**
- D37-D37: Historical and Base Year Revenue
- E38-I38: Revenue Growth Rates (Years 1-5)
- E42-I42: EBITDA Margins (%)
- E45-I45: D&A % of Revenue
- E55-I55: CapEx % of Revenue
- E58-I58: NWC % of Revenue

**Shares Outstanding:**
- D48: Diluted Shares Outstanding (Millions)

---

### 3. **WACC (Weighted Average Cost of Capital)** 💰
**Purpose:** Calculate discount rate for DCF

**INPUTS REQUIRED:**

**Cost of Equity (Cells F7-F9):**
- F7: Risk-Free Rate (%)
- F8: Equity Risk Premium (%)
- F9: Beta (Levered)

**Cost of Debt (Cell F15):**
- F15: Pre-Tax Cost of Debt (%)

**Capital Structure (Cells F22-F23):**
- F22: Market Value of Equity ($M)
- F23: Market Value of Debt ($M)

**Unlevered Beta Calculation (Optional):**
If calculating beta from comparables:
- C42-C46: Comparable company names
- D42-D46: Levered Betas
- E42-E46: Debt/Equity Ratios
- F42-F46: Tax Rates

**Output:** F35 (WACC) automatically links to DCF sheet

---

### 4. **Sensitivity Analysis** 📈
**Purpose:** Test how valuation changes with different assumptions

**Features:**
- WACC vs Terminal Growth Rate sensitivity
- WACC vs Terminal EBITDA Multiple sensitivity
- Revenue CAGR vs EBITDA Margin sensitivity

**Inputs Required:** NONE - All calculated from DCF assumptions

**How to Read:**
- Find intersection of your assumptions
- See range of implied share prices
- Identify key value drivers

---

### 5. **Scenario Analysis** 🎭
**Purpose:** Bull/Base/Bear case analysis

**INPUTS REQUIRED:**

**Scenario Assumptions (Cells D8-F17):**
Adjust these for each scenario:
- Row 8: Revenue CAGR (Years 1-5)
- Row 9: Terminal Revenue Growth Rate
- Row 10: EBITDA Margin (Year 5)
- Row 11: Terminal EBITDA Margin
- Row 12: CapEx % of Revenue
- Row 13: NWC % of Revenue
- Row 14: Tax Rate
- Row 15: WACC
- Row 16: Terminal Growth Rate
- Row 17: Terminal EBITDA Multiple

**Probability Weights (Cells D38-F38):**
- D38: Bear Case Probability (default: 25%)
- E38: Base Case Probability (default: 50%)
- F38: Bull Case Probability (default: 25%)

**Note:** Probabilities should sum to 100%

---

### 6. **Historical Financials** 📊
**Purpose:** Track 3-5 years of historical performance

**INPUTS REQUIRED:**

**Income Statement (Years -3 to Last Year):**
- C9-F9: Revenue
- C12-F12: Cost of Goods Sold (COGS)
- C18-F20: Operating Expenses (SG&A, R&D, Other)
- C27-F27: Depreciation & Amortization
- C33-F34: Interest Expense and Other Income
- C37-F37: Income Tax Expense

**Balance Sheet:**
- C47-F50: Current Assets (Cash, A/R, Inventory, Other)
- C53-F56: Long-Term Assets (PP&E, Intangibles, Goodwill, Other)
- C60-F62: Current Liabilities (A/P, Short-Term Debt, Other)
- C65-F66: Long-Term Liabilities (LT Debt, Other)
- C69-F69: Shareholders' Equity

**Cash Flow Statement:**
- C78-F79: Operating Activities (Change in NWC, Other)
- C83-F84: Investing Activities (CapEx, Other)
- C88-F90: Financing Activities (Debt, Equity, Dividends)

**Output:** Automatic calculation of growth rates, margins, and CAGRs

---

### 7. **Trading Comps** 🏢
**Purpose:** Comparable company valuation

**INPUTS REQUIRED:**

**Comparable Companies (Rows 6-15):**
For each of 10 comparables, enter:
- Column B: Company Name
- Column C: Ticker Symbol
- Column D: Market Capitalization ($M)
- Column E: Enterprise Value ($M)
- Column F: Revenue LTM ($M)
- Column G: EBITDA LTM ($M)
- Column H: EBIT LTM ($M)
- Column I: Net Income ($M)
- Column N: Revenue Growth Rate (%)

**Output:**
- Automatic calculation of multiples (EV/Revenue, EV/EBITDA, EV/EBIT, P/E)
- Summary statistics (Mean, Median, Quartiles)
- Implied valuation of target company

---

### 8. **Working Capital** 💼
**Purpose:** Detailed NWC analysis and cash conversion cycle

**INPUTS REQUIRED:**

**Historical Working Capital (Columns C-D):**
- C12, D12: Accounts Receivable
- C15, D15: Inventory
- C18, D18: Prepaid Expenses & Other
- C26, D26: Accounts Payable
- C29, D29: Accrued Expenses & Other

**Projected Assumptions (Columns E-I):**
- E13-I13: Days Sales Outstanding (DSO)
- E16-I16: Days Inventory Outstanding (DIO)
- E27-I27: Days Payable Outstanding (DPO)
- E19-I19: Prepaid Expenses % of Revenue
- E30-I30: Accrued Expenses % of Revenue

**Output:**
- Net Working Capital by year
- Change in NWC (for DCF)
- Cash Conversion Cycle (Days)

---

### 9. **Debt Schedule** 💳
**Purpose:** Track debt tranches and interest expense

**INPUTS REQUIRED:**

**Debt Tranche 1 (Cells C9-C14):**
- C9: Facility Name
- C10: Interest Rate (%)
- C11: Maturity (Years)
- C12: Annual Amortization (%)
- C14: Beginning Balance ($M)

**Debt Tranche 2 (Cells C20-C25):**
- C20: Facility Name
- C21: Interest Rate (%)
- C22: Maturity (Years)
- C23: Annual Amortization (%)
- C25: Beginning Balance ($M)

**Capital Leases (Cells C40-I40):**
- Enter capital/operating lease obligations

**Output:**
- Debt amortization schedule
- Interest expense by period
- Total debt balance

---

### 10. **Credit Analysis** 📉
**Purpose:** Leverage and coverage ratios

**Inputs Required:** NONE - All linked from other sheets

**Output Metrics:**
- Net Debt / EBITDA
- Total Debt / EBITDA
- EBITDA / Interest
- EBIT / Interest
- FCF / Interest
- Debt Service Coverage Ratio
- Implied credit rating (S&P equivalent)

---

### 11. **Returns Analysis** 💹
**Purpose:** Calculate IRR and MOIC for investors

**INPUTS REQUIRED:**

**Investment Parameters:**
- D9: Number of Shares Purchased
- C21-C24: Annual Dividends/Distributions (if any)

**Output:**
- Total Return ($  and %)
- MOIC (Multiple on Invested Capital)
- IRR (Internal Rate of Return)
- Annualized Return
- Payback Period
- Scenario comparison table

---

### 12. **Precedent Transactions** 🤝
**Purpose:** M&A transaction comparables

**INPUTS REQUIRED:**

**Transaction Data (Rows 6-15):**
For each of 10 transactions, enter:
- Column B: Date (MM/DD/YYYY)
- Column C: Target Company
- Column D: Acquirer
- Column E: Deal Value ($M)
- Column F: Target Revenue LTM ($M)
- Column G: Target EBITDA LTM ($M)
- Column J: Premium Paid (%)

**Output:**
- EV/Revenue and EV/EBITDA multiples
- Summary statistics
- Implied M&A valuation

---

### 13. **Management Case** 📋
**Purpose:** Compare your estimates to management guidance

**INPUTS REQUIRED:**

**Management Guidance:**
- C8: Year 1 Revenue (Management)
- C9-H9: Revenue Growth Rates (Management)
- C11-H11: EBITDA Margins (Management)
- C13-H13: CapEx % of Revenue (Management)

**Output:**
- Variance analysis ($ and %)
- Side-by-side comparison with your estimates

---

## 🚀 Quick Start Guide

### Step 1: Company Basics
1. Go to **DCF** sheet
2. Fill in company name, ticker, current price (D8-D10)
3. Enter shares outstanding (D48)
4. Enter balance sheet items (D19-D22)

### Step 2: Historical Data
1. Go to **Historical Financials** sheet
2. Enter 3-4 years of historical income statement data
3. Enter balance sheet and cash flow data
4. Review calculated CAGRs to validate data

### Step 3: Cost of Capital
1. Go to **WACC** sheet
2. Enter risk-free rate, equity risk premium, beta (F7-F9)
3. Enter cost of debt (F15)
4. Enter market cap and debt (F22-F23)
5. Verify WACC in F35 (typically 6-12%)

### Step 4: Projections
1. Return to **DCF** sheet
2. Enter revenue growth rates (E38-I38)
3. Enter EBITDA margins (E42-I42)
4. Enter D&A, CapEx, NWC assumptions
5. Choose terminal value method and rate

### Step 5: Review Output
1. Go to **Executive Summary**
2. Review implied price and upside
3. Check valuation across methods
4. Review recommendation

### Step 6: Enhance (Optional)
- Add comparable companies in **Trading Comps**
- Run scenarios in **Scenario Analysis**
- Add M&A data in **Precedent Transactions**
- Review sensitivity tables

---

## ✅ Validation Checklist

Before finalizing your model:

### Formula Integrity
- [ ] No #DIV/0! errors
- [ ] No #REF! errors
- [ ] No #VALUE! errors
- [ ] All blue cells have inputs

### Reasonableness Checks
- [ ] WACC between 6-12%
- [ ] Revenue growth rates realistic (typically < 15%)
- [ ] EBITDA margins consistent with industry
- [ ] Terminal growth rate < GDP growth (2-3%)
- [ ] Debt/Equity ratios reasonable

### Cross-Checks
- [ ] DCF value vs Trading Comps within reasonable range
- [ ] Implied multiples vs industry averages
- [ ] Historical margins vs projected margins
- [ ] Working capital assumptions vs historical

---

## 📊 Best Practices

1. **Start Conservative:** Use conservative assumptions initially
2. **Validate with History:** Compare projections to historical performance
3. **Multiple Methods:** Use DCF + Comps + Transactions for triangulation
4. **Sensitivity Testing:** Understand what drives value
5. **Document Assumptions:** Add notes explaining key assumptions
6. **Regular Updates:** Update with actual results and new guidance

---

## 🎯 Common Use Cases

### For Equity Research
- Complete DCF and Trading Comps
- Add 3+ comparable companies
- Run Bull/Base/Bear scenarios
- Provide price target range

### For Private Equity / M&A
- Complete all sheets including Precedent Transactions
- Focus on Returns Analysis (IRR/MOIC)
- Stress test leverage ratios
- Model multiple exit scenarios

### For Credit Analysis
- Emphasize Debt Schedule and Credit Analysis sheets
- Focus on leverage and coverage ratios
- Model debt paydown scenarios
- Check covenant compliance

### For Management/Board
- Focus on Executive Summary
- Compare to Management Case
- Highlight key value drivers
- Show sensitivity to assumptions

---

## 🔧 Troubleshooting

**Issue:** Valuation seems too high/low
- Check shares outstanding (common error)
- Verify debt and cash balances
- Review WACC calculation
- Check terminal value assumptions

**Issue:** #DIV/0! errors
- Check for zero values in denominators
- Verify shares outstanding is entered
- Ensure revenue has values

**Issue:** Circular reference warnings
- This model has no circular references
- If you see this, check for manual formula edits

**Issue:** Formulas not calculating
- Press F9 to recalculate
- Check if calculation is set to Automatic
- Verify Excel is not in edit mode

---

## 📞 Support

For questions about specific features or formulas:
1. Check the Instructions sheet in the Excel file
2. Review relevant section of this guide
3. Verify color coding (blue = input, black = formula)
4. Check that all prerequisite inputs are filled

---

## 📝 Version History

**Version 1.0 - Comprehensive Model**
- 13 integrated worksheets
- Zero formula errors
- Professional color coding
- Complete automation

**Features Included:**
✅ DCF with 5-year projections
✅ WACC with unlevered beta calculation
✅ Sensitivity analysis (3 tables)
✅ Scenario analysis (Bull/Base/Bear)
✅ Historical financials (3 statements)
✅ Trading comps analysis
✅ Working capital schedule
✅ Debt schedule (2 tranches)
✅ Credit analysis & ratios
✅ Returns analysis (IRR/MOIC)
✅ Precedent transactions
✅ Management case reconciliation
✅ Executive summary dashboard

---

## 🎓 Advanced Tips

1. **Terminal Value:** Most DCF value comes from terminal value. Spend extra time validating this assumption.

2. **WACC Accuracy:** A 1% change in WACC can significantly impact valuation. Use multiple methods to validate.

3. **Working Capital:** For retail/manufacturing companies, working capital can be a major cash drain. Model it carefully.

4. **Scenario Probability Weighting:** Don't just use equal weights. Think about likelihood of each scenario.

5. **Comparable Selection:** Quality over quantity. 3-5 truly comparable companies beat 10 loosely related ones.

---

**END OF GUIDE**
