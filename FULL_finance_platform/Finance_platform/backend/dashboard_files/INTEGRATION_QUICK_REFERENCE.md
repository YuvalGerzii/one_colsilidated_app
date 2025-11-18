# Financial Models Integration - Quick Reference

## 📋 One-Page Integration Cheat Sheet

---

## File Structure
```
Deal_Folder/
├── DCF_Model_Comprehensive.xlsx
├── LBO_Model_Comprehensive.xlsx
├── Merger_Model_Comprehensive.xlsx
├── DD_Tracker_Comprehensive.xlsx
└── Integrated_Models_Dashboard.xlsx ← NEW!
```

---

## Dashboard Sheets

| Sheet | Purpose | Update Frequency |
|-------|---------|------------------|
| Master Dashboard | Executive summary | Daily |
| Cross-Model Validation | Consistency checks | After each model update |
| DD Tracker Integration | DD findings → adjustments | As findings emerge |
| Scenario Analysis | Bear/Base/Bull comparison | Before IC |
| Integration Instructions | How-to guide | Reference only |

---

## Integration Workflow

```
1. DD TRACKER → Identify findings and risks
              ↓
2. DD TRACKER INTEGRATION → Log value impacts and required adjustments
              ↓
3. UPDATE MODELS → Adjust DCF/LBO/Merger assumptions
              ↓
4. VALIDATE → Check Cross-Model Validation sheet
              ↓
5. SCENARIOS → Run Bear/Base/Bull cases
              ↓
6. IC PREP → Review Master Dashboard
```

---

## Key Links to Create

### Master Dashboard Links:

| Cell | Description | Link To |
|------|-------------|---------|
| B11 | DCF EV | `=[DCF_Model_Comprehensive.xlsx]Valuation!B25` |
| B12 | DCF Equity | `=[DCF_Model_Comprehensive.xlsx]Valuation!B30` |
| C13 | LBO IRR | `=[LBO_Model_Comprehensive.xlsx]Returns!B10` |
| C14 | LBO MOIC | `=[LBO_Model_Comprehensive.xlsx]Returns!B11` |
| D15 | Merger Accr | `=[Merger_Model_Comprehensive.xlsx]Accretion!B15` |
| E19 | DD Complete | `=[DD_Tracker_Comprehensive.xlsx]Dashboard!B5` |

### Cross-Model Validation Links:

| Row | Assumption | DCF | LBO | Merger |
|-----|------------|-----|-----|--------|
| 5 | Revenue | `=[DCF]Assumptions!B10` | `=[LBO]Assumptions!B10` | `=[Merger]Assumptions!B10` |
| 6 | Growth | `=[DCF]Assumptions!B15` | `=[LBO]Assumptions!B15` | `=[Merger]Assumptions!B15` |
| 7 | EBITDA % | `=[DCF]Assumptions!B20` | `=[LBO]Assumptions!B20` | `=[Merger]Assumptions!B20` |
| 8 | Tax Rate | `=[DCF]Assumptions!B25` | `=[LBO]Assumptions!B25` | `=[Merger]Assumptions!B25` |

---

## DD Finding → Model Adjustment Examples

### Finding 1: Customer Concentration
- **Issue:** Top 3 customers = 60% of revenue
- **Risk:** High
- **Impact:** -$100M
- **DCF:** Reduce revenue growth 8% → 6%
- **LBO:** Reduce revenue growth 8% → 6%
- **Merger:** Reduce pro forma growth 8% → 6%

### Finding 2: Quality of Earnings Add-Backs
- **Issue:** $2M of legitimate add-backs identified
- **Risk:** Low
- **Impact:** +$10M
- **DCF:** Increase normalized EBITDA by $2M
- **LBO:** Increase entry EBITDA by $2M
- **Merger:** Increase target EBITDA by $2M

### Finding 3: Deferred Maintenance
- **Issue:** Equipment needs replacement
- **Risk:** Medium
- **Impact:** -$20M
- **DCF:** Add $20M one-time CapEx in Year 1
- **LBO:** Increase CapEx in Sources & Uses
- **Merger:** Add to integration costs

---

## Color Coding Standard

| Color | Meaning | Use For |
|-------|---------|---------|
| 🔵 Blue Text | Hard-coded inputs | User changes for scenarios |
| ⚫ Black Text | Formulas | Calculated values |
| 🟢 Green Text | Internal links | Links to other sheets |
| 🔴 Red Text | External links | Links to other files |
| 🟡 Yellow Fill | Attention needed | Items to update/review |
| 🟢 Green Fill | Low risk | Pass/OK status |
| 🟡 Yellow Fill | Medium risk | Review required |
| 🔴 Red Fill | High risk | Action required |

---

## Pre-IC Validation Checklist

### Cross-Model Consistency:
- [ ] Revenue assumptions match across all models
- [ ] EBITDA margins consistent
- [ ] Tax rates identical
- [ ] Debt/leverage assumptions aligned
- [ ] Share counts consistent (DCF & Merger)

### Valuation Sanity Checks:
- [ ] DCF value vs. price within ±20%
- [ ] LBO IRR ≥ 20% (or your firm's hurdle)
- [ ] LBO MOIC ≥ 2.5x (for 5-year hold)
- [ ] Merger accretion ≥ 3% (Year 1)
- [ ] Synergies realistic and achievable

### Due Diligence:
- [ ] Critical items 100% complete
- [ ] High risks have mitigation plans
- [ ] Value impacts quantified
- [ ] All findings reflected in models

### Technical:
- [ ] Zero formula errors (no #REF!, #DIV/0!)
- [ ] External links working
- [ ] All inputs in blue, formulas in black
- [ ] Sensitivity analysis complete

---

## Scenario Building Guide

### Base Case (Most Likely):
- Management projections adjusted for DD
- Realistic exit multiples
- Achievable synergies
- Market-standard assumptions

### Bear Case (Downside):
- Revenue growth -2% to -3%
- Margins compress 1-2%
- Exit multiple -1.0x to -2.0x
- Synergies at 70% of plan
- Integration costs +20%

### Bull Case (Upside):
- Revenue growth +3% to +4%
- Margin expansion 1-2%
- Exit multiple +1.0x to +2.0x
- Synergies at 120% of plan
- Integration faster/cheaper

### DD Adjusted Case:
- Start with Base Case
- Apply all DD findings
- Use most conservative assumptions where uncertain
- This becomes your recommendation

---

## Common Formulas

### Link to External File:
```excel
='[Filename.xlsx]SheetName'!CellReference
```

### Variance Check:
```excel
=IF(Cell1=Cell2,"✓","✗")
```

### Pass/Fail Status:
```excel
=IF(VarianceCell="✓","Pass","FAIL")
```

### Premium Calculation:
```excel
=(TransactionPrice-DCFValue)/DCFValue
```

### Conditional Formatting for Risk:
```excel
=IF(Value>Threshold,"High",IF(Value>Threshold2,"Medium","Low"))
```

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| #REF! errors | Edit → Links → Change Source → Update path |
| Values not updating | Ctrl+Alt+F9 (force recalculation) |
| Inconsistent assumptions | Review Cross-Model Validation sheet |
| Broken links | Keep all files in same folder |
| Circular reference | Formula → Error Checking → Find & Fix |

---

## File Saving Protocol

### Daily Saves:
- Save all files when making changes
- Use Ctrl+S frequently
- Keep all files open together

### Version Control:
- Before major changes: Save As with date
- Format: `Deal_Analysis_YYYY-MM-DD.xlsx`
- Keep last 3-5 versions

### Backup Strategy:
- Use OneDrive/SharePoint for team access
- Export to PDF before IC
- Save final version after approval

---

## Meeting Preparation

### Weekly DD Update (15 min):
1. Review DD Tracker completion %
2. Log new findings in DD Integration sheet
3. Update Master Dashboard
4. Discuss any red flags

### Pre-IC Review (1 hour):
1. Validate all assumptions consistent
2. Run all three scenarios
3. Review Cross-Model Validation
4. Prepare Q&A materials
5. Export key charts

### IC Presentation (Use Dashboard):
1. Master Dashboard = Executive Summary
2. DD Integration = Risk Assessment
3. Scenario Analysis = Sensitivity
4. Validation = Quality Assurance

---

## Key Contacts & Resources

### Documentation:
- `DCF_MODEL_GUIDE.md` - 50 pages
- `LBO_MODEL_GUIDE.md` - 60 pages
- `MERGER_MODEL_USER_GUIDE.md` - 50 pages
- `DD_TRACKER_USER_GUIDE.md` - 30 pages
- `MODEL_INTEGRATION_GUIDE.md` - 30 pages
- `INTEGRATION_IMPLEMENTATION_GUIDE.md` - 45 pages (detailed)

### Model Ownership Template:
- DCF Model: _______________
- LBO Model: _______________
- Merger Model: _______________
- DD Tracker: _______________
- Integration Dashboard: _______________

---

## Success Metrics

### A successful integration means:

✅ Zero formula errors across all files
✅ All assumptions consistent where they should be
✅ DD findings quantified and reflected
✅ Scenarios all modeled and compared
✅ IC materials ready and validated
✅ Team aligned on recommendation
✅ Ready to present with confidence

---

## Critical Reminder

**The dashboard is only as good as the underlying models.**

- Garbage in = Garbage out
- Validate source data
- Document assumptions
- Review calculations
- Cross-check everything
- Trust but verify

---

**Quick Reference Version 1.0**
**Print this page and keep at your desk!**

For detailed instructions, see: `INTEGRATION_IMPLEMENTATION_GUIDE.md`
