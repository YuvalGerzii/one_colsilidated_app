# PROPERTY COMPARISON TOOL - QUICK REFERENCE CARD

**Version 1.0** | November 4, 2025 | One-Page Guide

---

## ⚡ QUICK START (5 MINUTES)

### 1. Create Comparison
```bash
POST /api/comparisons
Body: {"comparison_name": "Q4 Pipeline", "primary_metric": "levered_irr"}
```

### 2. Import Deals
```bash
POST /api/comparisons/{id}/deals/import
Files: model.xlsx | Data: {"property_type": "Multifamily"}
```

### 3. View Dashboard
```
Navigate to: /comparisons/{id}
```

### 4. Export IC Memo
```
Click: "Export IC Memo" button → Downloads .docx
```

---

## 📊 SUPPORTED MODELS

| Model Type | File Pattern | Key Metrics |
|------------|--------------|-------------|
| **Multifamily** | Multifamily_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate, NOI |
| **Mixed-Use** | Mixed_Use_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate, NOI |
| **Hotel** | Hotel_*.xlsx | IRR, MOIC, CoC, DSCR, ADR, RevPAR |
| **SFR** | SFR_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate |
| **House Flip** | House_Flipping_*.xlsx | IRR, MOIC, Hold Period, Profit |

---

## 🎯 KEY METRICS

### Returns (40% Weight)
- **Levered IRR** - Target: 15-25%
- **Equity Multiple (MOIC)** - Target: 1.6-2.5x
- **Cash-on-Cash Y1** - Target: 5-12%

### Risk (30% Weight)
- **DSCR Y1** - Target: 1.25-1.50x
- **LTV** - Target: 65-75%
- **Cap Rate Spread** - Target: 50-150 bps

### Operations (30% Weight)
- **NOI Margin** - Target: 55-70%
- **Occupancy** - Target: 90-96%

---

## 🎨 HEATMAP COLOR GUIDE

| Color | Score Range | Performance | Example |
|-------|-------------|-------------|---------|
| 🟢 **Green** | 80-100 | Excellent | IRR >25%, DSCR >1.50x |
| 🟡 **Yellow** | 60-79 | Good | IRR 15-25%, DSCR 1.25-1.50x |
| 🔴 **Red** | 0-59 | Poor | IRR <15%, DSCR <1.25x |

---

## 🏆 SCORING SYSTEM

**Overall Score = Σ (Metric Score × Weight)**

### Default Weights
| Category | Criteria | Weight |
|----------|----------|--------|
| Returns | Levered IRR | 25% |
| Returns | Equity Multiple | 10% |
| Returns | Cash-on-Cash Y1 | 5% |
| Risk | DSCR Y1 | 15% |
| Risk | LTV (inverse) | 10% |
| Risk | Cap Rate Spread | 5% |
| Operations | NOI Margin | 15% |
| Operations | Occupancy | 15% |
| **TOTAL** | | **100%** |

---

## 📄 IC MEMO SECTIONS

1. **Title Page** - Comparison name, date
2. **Executive Summary** - Top 3 deals, key metrics
3. **Deal Summaries** - 1 page per deal
4. **Comparison Matrix** - All deals side-by-side
5. **Ranking Analysis** - Top performers by category
6. **Risk Assessment** - Risk-adjusted rankings
7. **Recommendation** - Top deal recommendation
8. **Appendix** - Full metrics table

**Average Length: 12-15 pages**

---

## 🔧 COMMON TASKS

### Import Multiple Deals (Python)
```python
import requests

comparison_id = 'your-id'
files = ['model1.xlsx', 'model2.xlsx', 'model3.xlsx']

for f in files:
    with open(f, 'rb') as file:
        requests.post(
            f'/api/comparisons/{comparison_id}/deals/import',
            files={'file': file},
            data={'property_type': 'Multifamily'}
        )
```

### Get Top 5 Deals
```python
response = requests.get(f'/api/comparisons/{comparison_id}/deals')
deals = sorted(response.json()['deals'], 
               key=lambda x: x['overall_score'], 
               reverse=True)[:5]
```

### Update Scoring Weight
```sql
UPDATE scoring_criteria
SET weight = 0.30
WHERE criteria_name = 'Levered IRR';
```

---

## ⚠️ TROUBLESHOOTING

| Issue | Quick Fix |
|-------|-----------|
| **Metrics show N/A** | Verify Excel model structure, check sheet names |
| **Incorrect ranking** | Review scoring weights, check for missing data |
| **Export fails** | Ensure ≥1 deal imported, check file permissions |
| **Colors wrong** | Refresh browser, verify thresholds in DB |

---

## 📐 METRIC TARGETS BY STRATEGY

### Core / Core-Plus
- IRR: 10-15%
- MOIC: 1.4-1.8x
- DSCR: 1.40x+
- LTV: 70-75%

### Value-Add
- IRR: 15-20%
- MOIC: 1.8-2.3x
- DSCR: 1.30-1.40x
- LTV: 65-70%

### Opportunistic
- IRR: 20-25%+
- MOIC: 2.3-3.0x+
- DSCR: 1.25-1.35x
- LTV: 60-70%

---

## 🔑 API ENDPOINTS

```
POST   /api/comparisons                    # Create comparison
GET    /api/comparisons/{id}               # Get details
POST   /api/comparisons/{id}/deals/import  # Import deal
GET    /api/comparisons/{id}/deals         # List deals
GET    /api/comparisons/{id}/heatmap       # Heatmap data
GET    /api/comparisons/{id}/ic-memo       # Download memo
```

**Base URL:** `http://localhost:8000` (dev)

---

## 💡 PRO TIPS

✅ **Import Strategy**
- Import all deals at once for consistent comparison
- Use batch script for 10+ deals
- Verify metrics immediately after import

✅ **Comparison Best Practices**
- Compare similar property types together
- Use filters to create sub-comparisons (e.g., "All Multifamily")
- Review both overall and risk-adjusted rankings

✅ **IC Memo Tips**
- Generate 24-48 hours before IC meeting
- Customize recommendations section
- Add firm branding and property photos
- Include executive summary on first page

✅ **Scoring Customization**
- Adjust weights based on investment strategy
- Conservative: Increase DSCR/LTV weights
- Aggressive: Increase IRR/MOIC weights
- Location-focused: Add custom location score

❌ **Common Mistakes**
- Comparing deals across different time periods
- Ignoring property-specific risks
- Relying solely on automated scores without manual review
- Forgetting to verify source Excel data

---

## 📞 SUPPORT

**Documentation:** PROPERTY_COMPARISON_USER_GUIDE.md (50 pages)  
**API Docs:** http://localhost:8000/docs (Swagger)  
**Schema:** property_comparison_schema.sql  

**Contact:**
- Technical: techsupport@yourfirm.com
- Product: productteam@yourfirm.com

---

## 🚀 INTEGRATION POINTS

### Portfolio Dashboard
- Deals sync to `portfolio_companies` table
- Metrics feed `financial_metrics` table
- Links to master property database

### Excel Models
- Direct import from all 5 model types
- Preserves source file reference
- Bi-directional sync available

### CRM / Pipeline
- Export deal list to CRM
- Track IC decision status
- Update pipeline probabilities

---

## 📊 SAMPLE COMPARISON MATRIX

```
Rank | Property           | Type        | IRR    | MOIC  | CoC   | DSCR  | Score
-----|-------------------|-------------|--------|-------|-------|-------|-------
  #1 | 123 Main St       | Multifamily | 22.5% 🟢 | 2.1x 🟡 | 8.5% 🟡 | 1.45x 🟡 | 85 🟢
  #2 | 456 Oak Ave       | Mixed-Use   | 21.0% 🟡 | 2.3x 🟢 | 7.2% 🟡 | 1.38x 🟡 | 82 🟢
  #3 | 789 Park Blvd     | Hotel       | 19.5% 🟡 | 2.0x 🟡 | 6.8% 🟡 | 1.52x 🟢 | 79 🟡
  #4 | 321 Elm St        | SFR         | 18.0% 🟡 | 1.9x 🟡 | 6.2% 🟡 | 1.42x 🟡 | 75 🟡
  #5 | 654 Pine Dr       | Multifamily | 16.5% 🟡 | 1.8x 🟡 | 5.8% 🟡 | 1.35x 🟡 | 71 🟡
```

---

## ⏱️ TIME SAVINGS

**Before:** 4-6 hours per IC memo
- Manual data entry
- Copy/paste to PowerPoint
- Reconcile different formats
- Create comparison tables

**After:** 15 minutes per IC memo
- Automated import
- Instant scoring
- One-click export
- Standardized format

**ROI: 94% time reduction**

---

**🎯 Remember: This tool accelerates analysis, but professional judgment is still essential for investment decisions.**
