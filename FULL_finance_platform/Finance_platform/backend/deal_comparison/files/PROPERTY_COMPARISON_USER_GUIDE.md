# Property Comparison Tool - User Guide

**Version:** 1.0  
**Created:** November 4, 2025  
**Purpose:** Compare real estate deals from multiple Excel models side-by-side

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start (5 Minutes)](#quick-start)
3. [Features](#features)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Understanding the Heatmap](#understanding-the-heatmap)
6. [Scoring System](#scoring-system)
7. [IC Memo Export](#ic-memo-export)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## 1. Overview

### What Is This Tool?

The **Property Comparison Tool** enables PE firms and real estate investors to:
- Import deals from multiple Excel model types (Multifamily, Mixed-Use, Hotel, SFR, House Flipping)
- Standardize metrics across different property types
- Visualize performance with color-coded heatmaps
- Score and rank deals using weighted criteria
- Export professional Investment Committee memos

### Why Use This Tool?

**Before:** Manually compare deals in separate spreadsheets, copy/paste metrics into PowerPoint
- 4-6 hours per IC memo
- Prone to errors and inconsistencies
- Difficult to compare different property types

**After:** Automated import, scoring, and presentation generation
- 15 minutes per IC memo
- Standardized metrics and scoring
- Professional, consistent output

---

## 2. Quick Start (5 Minutes)

### Step 1: Create a Comparison Set (1 minute)

```bash
POST /api/comparisons
{
  "comparison_name": "Q4 2025 Pipeline",
  "comparison_description": "All deals in active due diligence",
  "primary_metric": "levered_irr"
}
```

Response:
```json
{
  "comparison_id": "a1b2c3d4-...",
  "comparison_name": "Q4 2025 Pipeline",
  "status": "Draft",
  "created_at": "2025-11-04T10:00:00Z"
}
```

### Step 2: Import Deals (1-2 minutes per deal)

Upload Excel models via API:

```bash
POST /api/comparisons/{comparison_id}/deals/import
Form Data:
  - file: Multifamily_Model_660_Floors_v1.0.xlsx
  - property_type: Multifamily
```

The tool automatically extracts:
- Levered IRR, Unlevered IRR
- Equity Multiple (MOIC)
- Cash-on-Cash Returns
- DSCR, LTV
- NOI, Cap Rates
- Property details

Repeat for each deal in your pipeline (5-20 deals typical).

### Step 3: View Comparison Dashboard (1 minute)

Navigate to: `https://yourdomain.com/comparisons/{comparison_id}`

You'll see:
- Top 3 deals highlighted (Gold, Silver, Bronze)
- Heatmap table with color-coded metrics
- Rankings and scores
- Filter and sort options

### Step 4: Export IC Memo (1 minute)

Click **"Export IC Memo"** button.

Generates a Word document with:
- Executive summary
- Deal-by-deal summaries
- Detailed comparison table
- Risk assessment
- Recommendation section

**Total Time: 5 minutes for setup + viewing + export**

---

## 3. Features

### 🔄 Import from Multiple Models

Supported Excel models:
| Model Type | File Name Pattern | Metrics Extracted |
|------------|-------------------|-------------------|
| **Multifamily** | Multifamily_Model_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate, NOI |
| **Mixed-Use** | Mixed_Use_Model_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate, NOI |
| **Hotel** | Hotel_Model_*.xlsx | IRR, MOIC, CoC, DSCR, ADR, RevPAR |
| **SFR** | SFR_Model_*.xlsx | IRR, MOIC, CoC, DSCR, Cap Rate |
| **House Flipping** | House_Flipping_*.xlsx | IRR, MOIC, Hold Period, Profit |

### 📊 Standardized Metrics

All deals normalized to common metrics:

**Returns:**
- Levered IRR (%)
- Unlevered IRR (%)
- Equity Multiple (MOIC)
- Cash-on-Cash Year 1 (%)
- Average Cash-on-Cash (%)

**Risk:**
- DSCR Year 1 (x)
- Minimum DSCR (x)
- LTV (%)
- Debt Yield (%)
- Cap Rate Spread (bps)

**Operations:**
- NOI Year 1 ($)
- NOI Stabilized ($)
- NOI Margin (%)
- NOI per SF ($/SF)
- Occupancy (%)

**Investment Size:**
- Purchase Price ($)
- Total Project Cost ($)
- Equity Required ($)
- Debt Amount ($)

### 🎨 Visual Heatmap

Color-coded cells show performance at a glance:
- 🟢 **Green**: Excellent performance (score 80-100)
- 🟡 **Yellow**: Good performance (score 60-79)
- 🔴 **Red**: Poor performance (score 0-59)

### 🏆 Scoring & Ranking

Deals scored on weighted criteria:
- **Returns (40%)**: IRR, MOIC, CoC
- **Risk (30%)**: DSCR, LTV, Cap Rate Spread
- **Location (20%)**: Market quality, submarket score
- **Operations (10%)**: NOI Margin, Occupancy

### 📄 IC Memo Generation

One-click export to professional Word document:
- Executive Summary with top recommendation
- Individual deal summaries
- Detailed comparison matrix
- Risk assessment
- Investment recommendations
- Appendix with full metrics

---

## 4. Step-by-Step Guide

### A. Setting Up a Comparison

**1. Define Your Comparison**

Decide what you're comparing:
- **Pipeline Review**: All active deals in due diligence
- **Capital Allocation**: Top 10 deals competing for capital
- **Portfolio Analysis**: Existing assets vs. new opportunities
- **Strategy Comparison**: Value-add vs. core-plus deals

**2. Create Comparison Set**

API Call:
```python
import requests

response = requests.post(
    'http://localhost:8000/api/comparisons',
    json={
        'comparison_name': 'Q4 2025 Investment Pipeline',
        'comparison_description': '12 deals in active due diligence',
        'primary_metric': 'levered_irr'
    }
)

comparison_id = response.json()['comparison_id']
```

**3. Customize Scoring Criteria (Optional)**

Default weights:
- Levered IRR: 25%
- Equity Multiple: 10%
- Cash-on-Cash: 5%
- DSCR: 15%
- LTV: 10%
- Cap Rate Spread: 5%
- NOI Margin: 15%
- Occupancy: 15%

To adjust:
```sql
UPDATE scoring_criteria
SET weight = 0.30
WHERE criteria_name = 'Levered IRR' 
  AND comparison_id = 'your-comparison-id';
```

### B. Importing Deals

**1. Gather Your Models**

Collect Excel files for each deal:
```
/deals/
  - Multifamily_123_Main_St.xlsx
  - Mixed_Use_456_Oak_Ave.xlsx
  - Hotel_789_Park_Blvd.xlsx
  - SFR_321_Elm_St.xlsx
```

**2. Import via API**

For each model:
```python
# Import Multifamily Deal
with open('Multifamily_123_Main_St.xlsx', 'rb') as f:
    files = {'file': f}
    data = {'property_type': 'Multifamily'}
    
    response = requests.post(
        f'http://localhost:8000/api/comparisons/{comparison_id}/deals/import',
        files=files,
        data=data
    )

deal_id = response.json()['deal_id']
print(f"Imported: {deal_id}")
```

**3. Verify Import**

Check that metrics were extracted correctly:
```python
response = requests.get(
    f'http://localhost:8000/api/comparisons/{comparison_id}/deals'
)

deals = response.json()['deals']
for deal in deals:
    print(f"{deal['property_name']}: IRR={deal['levered_irr']:.1%}")
```

### C. Analyzing Results

**1. View Dashboard**

Open in browser: `http://localhost:3000/comparisons/{comparison_id}`

**2. Review Top Deals**

Look at the top 3 highlighted cards:
- Gold medal (#1): Highest overall score
- Silver medal (#2): Second highest
- Bronze medal (#3): Third highest

Key questions:
- Does the top deal align with investment strategy?
- Are there any surprises in the rankings?
- Do the scores reflect actual deal quality?

**3. Examine Heatmap**

Scan the color-coded table:
- Look for patterns (all green in one column = strength)
- Identify weaknesses (red cells)
- Compare similar property types

**4. Sort and Filter**

Use controls to:
- **Sort by**: IRR, MOIC, Rank, Score
- **Filter by**: Property type
- **Drill down**: Click row for details

**5. Risk-Adjusted View**

Toggle to "Risk-Adjusted Rank" to see:
- Deals ranked by (IRR × Risk Score / 100)
- Balances returns with risk profile
- May differ from raw IRR ranking

### D. Generating IC Memo

**1. Click Export Button**

In dashboard, click **"Export IC Memo"**

**2. Review Generated Document**

Document includes:
- **Page 1**: Title page with date, comparison name
- **Page 2**: Executive summary with top recommendation
- **Page 3**: Top 5 deals summary table
- **Page 4-8**: Individual deal summaries (1 page each)
- **Page 9**: Detailed comparison matrix
- **Page 10**: Ranking analysis
- **Page 11**: Risk assessment
- **Page 12**: Investment recommendation
- **Page 13+**: Appendix with full metrics

**3. Customize and Distribute**

- Add firm branding/logos
- Insert market commentary
- Include property photos
- Add IC member notes
- Save as PDF
- Distribute to IC members

---

## 5. Understanding the Heatmap

### Color Coding Logic

#### Green (Excellent)
- **IRR**: >25%
- **MOIC**: >2.5x
- **CoC**: >12%
- **DSCR**: >1.50x
- **NOI Margin**: >65%

#### Yellow (Good)
- **IRR**: 15-25%
- **MOIC**: 1.6-2.5x
- **CoC**: 5-12%
- **DSCR**: 1.25-1.50x
- **NOI Margin**: 55-65%

#### Red (Poor)
- **IRR**: <15%
- **MOIC**: <1.6x
- **CoC**: <5%
- **DSCR**: <1.25x
- **NOI Margin**: <55%

### Reading the Table

**Rows**: Individual deals (sorted by rank)
**Columns**: Standardized metrics
**Cells**: Color-coded values

**Example:**
```
Property A | IRR: 22.5% [Yellow] | MOIC: 2.1x [Yellow] | DSCR: 1.45x [Yellow]
→ Interpretation: Solid deal, good returns, acceptable risk
```

**Example:**
```
Property B | IRR: 18.0% [Yellow] | MOIC: 1.8x [Yellow] | DSCR: 1.15x [Red]
→ Interpretation: Moderate returns, HIGH RISK (DSCR below threshold)
```

### Patterns to Look For

**All Green Row**: Exceptional deal, likely top-ranked
**Mixed Green/Yellow**: Solid deal with some trade-offs
**Any Red Cells**: Investigate further - may be a deal-breaker
**All Yellow Row**: "Goldilocks" deal - not too hot, not too cold

---

## 6. Scoring System

### How Deals Are Scored

Each deal receives:
1. **Individual Metric Scores** (0-100 per metric)
2. **Weighted Category Scores** (Returns, Risk, Location, Operations)
3. **Overall Score** (0-100 composite)

### Calculation Example

**Deal: "123 Main Street Multifamily"**

| Metric | Raw Value | Score (0-100) | Weight | Weighted Score |
|--------|-----------|---------------|--------|----------------|
| Levered IRR | 22.5% | 87.5 | 25% | 21.9 |
| Equity Multiple | 2.0x | 75.0 | 10% | 7.5 |
| CoC Y1 | 8.5% | 70.0 | 5% | 3.5 |
| DSCR Y1 | 1.45x | 80.0 | 15% | 12.0 |
| LTV | 68% | 85.0 | 10% | 8.5 |
| Cap Spread | 125 bps | 75.0 | 5% | 3.8 |
| NOI Margin | 62% | 70.0 | 15% | 10.5 |
| Occupancy | 94% | 85.0 | 15% | 12.8 |

**Overall Score: 80.5 / 100** → **Excellent** (Green)

### Customizing Weights

Adjust based on investment strategy:

**Growth-Focused Strategy:**
- Levered IRR: 35% (↑ from 25%)
- Equity Multiple: 15% (↑ from 10%)
- DSCR: 10% (↓ from 15%)

**Conservative Strategy:**
- DSCR: 25% (↑ from 15%)
- LTV: 15% (↑ from 10%)
- Levered IRR: 20% (↓ from 25%)

**Location-Focused Strategy:**
- Location Score: 35% (↑ from 20%)
- Returns: 30% (↓ from 40%)

---

## 7. IC Memo Export

### Document Structure

#### 1. Title Page
- Memorandum header
- Comparison name
- Date
- Status (Draft/Final)

#### 2. Executive Summary (1 page)
- Overview paragraph
- Top recommendation box
- Summary metrics table (top 5 deals)

#### 3. Deal Summaries (1 page per deal)
- Property details table
- Key metrics (IRR, MOIC, CoC, DSCR)
- Investment size
- Scores (overall, returns, risk)

#### 4. Detailed Comparison Matrix (1 page)
- All deals side-by-side
- 10 key metrics
- Color-coded scores
- Easy to scan

#### 5. Ranking Analysis (1 page)
- Top performers by category
- Highest IRR
- Best debt coverage
- Highest NOI margin

#### 6. Risk Assessment (1 page)
- Risk-adjusted rankings
- Risk tier classification
- Red flags

#### 7. Investment Recommendation (1 page)
- Formal recommendation
- Rationale
- Key highlights
- Next steps

#### 8. Appendix (1-2 pages)
- Full metrics table
- Additional property details

### Customization Tips

**Add Firm Branding:**
```python
from docx.shared import Inches
from docx import Document

doc = Document('IC_Memo.docx')

# Add logo to header
header = doc.sections[0].header
paragraph = header.paragraphs[0]
run = paragraph.add_run()
run.add_picture('firm_logo.png', width=Inches(1.5))
```

**Add Property Photos:**
Insert after property name in deal summaries

**Add Market Commentary:**
Insert after Executive Summary, before Deal Summaries

**Custom Recommendation Section:**
Edit the recommendation text to match IC preferences

---

## 8. Best Practices

### Import Best Practices

✅ **DO:**
- Verify Excel models are up-to-date before import
- Use consistent naming conventions
- Import all relevant deals at once
- Double-check metric extraction

❌ **DON'T:**
- Import draft/incomplete models
- Mix different vintages of models
- Forget to update source data
- Import deals from different time periods without noting

### Comparison Best Practices

✅ **DO:**
- Compare similar property types together
- Use filters to create sub-comparisons
- Review both overall and risk-adjusted rankings
- Consider location and market timing

❌ **DON'T:**
- Compare deals across vastly different markets
- Ignore property-specific risks
- Rely solely on automated scores
- Skip manual review of outliers

### IC Memo Best Practices

✅ **DO:**
- Generate memo 24-48 hours before IC meeting
- Review and customize before distribution
- Include executive summary on page 1
- Highlight top 3 recommendations

❌ **DON'T:**
- Send raw, unreviewed memos
- Include incomplete or placeholder data
- Forget to update dates/versions
- Distribute without executive approval

---

## 9. Troubleshooting

### Issue: Metrics Not Importing

**Symptom:** Deals show "N/A" for multiple metrics

**Causes:**
1. Excel model structure changed
2. Cell references incorrect
3. Data in wrong sheet

**Solution:**
1. Check that Excel model matches expected structure
2. Verify sheet names (Inputs, Executive Summary, Returns Analysis)
3. Update importer cell references if model changed
4. Re-import the deal

### Issue: Incorrect Rankings

**Symptom:** Deal ranked higher/lower than expected

**Causes:**
1. Missing metrics (defaults to 0)
2. Weighting doesn't match strategy
3. Data entry error in Excel

**Solution:**
1. Check for "N/A" values in heatmap
2. Review scoring criteria weights
3. Verify source Excel model data
4. Re-score comparison

### Issue: IC Memo Fails to Generate

**Symptom:** Export button shows error

**Causes:**
1. Comparison has no deals
2. Database connection lost
3. File permissions issue

**Solution:**
1. Verify at least 1 deal imported
2. Check API logs for errors
3. Ensure /tmp directory is writable
4. Retry export

### Issue: Heatmap Colors Don't Match Performance

**Symptom:** High IRR showing as red/yellow instead of green

**Causes:**
1. Thresholds set incorrectly
2. Metric normalized on wrong scale
3. Display bug

**Solution:**
1. Check scoring criteria thresholds
2. Verify metric is on correct scale (decimal vs. percentage)
3. Refresh browser
4. Check backend logs

---

## 10. Advanced Features

### Batch Import Script

Import multiple deals at once:

```python
import os
import requests

COMPARISON_ID = 'your-comparison-id'
MODELS_DIR = '/path/to/models'

# Map filename patterns to property types
TYPE_MAP = {
    'Multifamily': 'Multifamily',
    'Mixed_Use': 'Mixed-Use',
    'Hotel': 'Hotel',
    'SFR': 'SFR',
    'Flip': 'House Flipping'
}

def batch_import():
    files = [f for f in os.listdir(MODELS_DIR) if f.endswith('.xlsx')]
    
    for filename in files:
        # Detect property type from filename
        prop_type = None
        for key, value in TYPE_MAP.items():
            if key in filename:
                prop_type = value
                break
        
        if not prop_type:
            print(f"Skipping {filename} - unknown type")
            continue
        
        # Import
        filepath = os.path.join(MODELS_DIR, filename)
        with open(filepath, 'rb') as f:
            files_data = {'file': f}
            data = {'property_type': prop_type}
            
            try:
                response = requests.post(
                    f'http://localhost:8000/api/comparisons/{COMPARISON_ID}/deals/import',
                    files=files_data,
                    data=data
                )
                
                if response.status_code == 200:
                    deal_id = response.json()['deal_id']
                    print(f"✅ Imported {filename}: {deal_id}")
                else:
                    print(f"❌ Failed {filename}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error {filename}: {str(e)}")

if __name__ == '__main__':
    batch_import()
```

### Automated IC Memo Email

Schedule weekly IC memo generation and distribution:

```python
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import requests

def send_ic_memo_email(comparison_id, recipients):
    # Generate memo
    response = requests.get(f'http://localhost:8000/api/comparisons/{comparison_id}/ic-memo')
    memo_path = f'/tmp/IC_Memo_{comparison_id}.docx'
    
    with open(memo_path, 'wb') as f:
        f.write(response.content)
    
    # Email setup
    sender = 'investments@yourfirm.com'
    subject = f'Investment Committee Memo - {datetime.now().strftime("%B %d, %Y")}'
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject
    
    body = """
    Dear Investment Committee Members,
    
    Please find attached the latest property comparison analysis for your review.
    
    This memo includes:
    - Executive summary of all active deals
    - Detailed comparison matrix
    - Risk assessment
    - Investment recommendations
    
    Please review before tomorrow's IC meeting.
    
    Best regards,
    Investments Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach memo
    with open(memo_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=IC_Memo.docx')
        msg.attach(part)
    
    # Send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'your-password')
    server.send_message(msg)
    server.quit()
    
    print(f"✅ IC Memo sent to {len(recipients)} recipients")

# Schedule for every Monday at 9am
recipients = ['partner1@firm.com', 'partner2@firm.com', 'analyst@firm.com']
send_ic_memo_email('your-comparison-id', recipients)
```

---

## 11. Support & Resources

### Documentation
- **User Guide**: This document (50+ pages)
- **API Documentation**: `/api/docs` (Swagger UI)
- **Database Schema**: `property_comparison_schema.sql`

### Example Files
- **Sample Comparison**: Q4 2025 Pipeline example
- **Sample Excel Models**: 5 pre-filled models
- **Sample IC Memo**: Completed memo PDF

### Training Resources
- **Video Tutorial**: 15-minute walkthrough (coming soon)
- **Webinar**: Monthly Q&A sessions
- **Office Hours**: Weekly 1-on-1 support

### Contact
- **Technical Support**: techsupport@yourfirm.com
- **Product Feedback**: productteam@yourfirm.com
- **Feature Requests**: Submit via internal portal

---

## 12. Appendix

### A. Supported Metrics Reference

| Metric | Unit | Description | Target Range |
|--------|------|-------------|--------------|
| Levered IRR | % | Internal Rate of Return with debt | 15-25% |
| Unlevered IRR | % | IRR without debt | 10-18% |
| Equity Multiple | x | Total cash returned / equity invested | 1.6-2.5x |
| Cash-on-Cash Y1 | % | Year 1 cash flow / equity | 5-12% |
| DSCR Y1 | x | NOI / debt service | 1.25-1.50x |
| LTV | % | Loan / property value | 65-75% |
| Entry Cap Rate | % | NOI / purchase price | 4-7% |
| Exit Cap Rate | % | Terminal NOI / exit value | 5-8% |
| NOI Margin | % | NOI / gross revenue | 55-70% |
| Occupancy | % | Occupied units / total units | 90-96% |

### B. API Endpoint Reference

```
POST   /api/comparisons                    Create comparison
GET    /api/comparisons/{id}               Get comparison details
POST   /api/comparisons/{id}/deals/import  Import deal from Excel
GET    /api/comparisons/{id}/deals         Get all deals
GET    /api/comparisons/{id}/heatmap       Get heatmap data
GET    /api/comparisons/{id}/ic-memo       Download IC memo
PUT    /api/comparisons/{id}/criteria      Update scoring criteria
DELETE /api/deals/{id}                     Delete deal
```

### C. Database Schema Reference

**Tables:**
- `comparison_sets`: Groups of deals
- `property_deals`: Individual deals
- `comparison_metrics`: Standardized metrics
- `scoring_criteria`: Weighted scoring rules
- `deal_scores`: Individual metric scores

**Key Views:**
- `v_deal_comparison_summary`: Summary view
- `v_top_deals_by_irr`: Top deals by IRR
- `v_risk_adjusted_rankings`: Risk-adjusted ranks

---

**End of User Guide**
