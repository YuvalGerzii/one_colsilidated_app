# Skills Roadmap for Portfolio Dashboard Project

A strategic plan for building 9 additional Claude skills to supercharge your private equity portfolio management platform.

---

## 🎯 Skill Creation Strategy

### Why Multiple Skills?

**Composability:** Skills work together automatically. Claude can use 2-3 skills simultaneously for complex tasks.

**Example:**
```
User: "Generate DCF models for all companies, validate the data, and create an LP report"

Claude automatically uses:
1. PE Excel Model Generator skill → Generate models
2. Data Validation skill → Check accuracy
3. LP Reporting skill → Create summary
```

### Priority Framework

Each skill is rated on:
- **Impact:** How much it improves your workflow (🔥 = High, ⭐ = Medium, 💡 = Low)
- **Effort:** Time to create (Low = <2 hours, Medium = 2-4 hours, High = 4+ hours)
- **Dependencies:** What needs to exist first

---

## 📋 Skills Roadmap

### ✅ COMPLETED

**1. PE Excel Model Generator** (Current skill)
- Status: ✅ Complete and delivered
- Impact: 🔥🔥🔥
- Integration: Ready to use

---

### 🚀 PHASE 1: Foundation Skills (Week 1-2)

These establish core standards and patterns for all future work.

#### Skill 2: PE Financial Modeling Standards

**Priority:** CRITICAL ⚠️
**Impact:** 🔥🔥🔥 (Ensures all models follow Big 4 standards)
**Effort:** Low (2-3 hours)
**Dependencies:** None

**What it includes:**
```markdown
---
name: PE Financial Modeling Standards
description: Apply private equity financial modeling standards and conventions to DCF, LBO, merger models, and valuations. Use when building or validating financial models.
version: 1.0.0
---

## Formula Library

### Valuation Formulas
- NPV: `=NPV(discount_rate, cashflows) + initial_investment`
- IRR: `=IRR(cashflows, [guess])`
- XIRR: `=XIRR(cashflows, dates, [guess])`
- WACC: `=(E/V)*Re + (D/V)*Rd*(1-Tc)`

### Returns Metrics
- MOIC: `=exit_proceeds / invested_capital`
- DPI: `=distributions / paid_in_capital`
- TVPI: `=(distributions + nav) / paid_in_capital`

### Operating Metrics
- Revenue Growth: `=(revenue_t1 / revenue_t0) - 1`
- EBITDA Margin: `=ebitda / revenue`
- Rule of 40: `=revenue_growth + ebitda_margin`

## Industry Benchmarks

### Software/SaaS
- Entry Multiple: 8-12x EBITDA
- Exit Multiple: 10-15x EBITDA
- Target IRR: 25-30%
- EBITDA Margin: 15-25%

### Healthcare
- Entry Multiple: 7-10x EBITDA
- Exit Multiple: 8-12x EBITDA
- Target IRR: 20-25%

### Manufacturing
- Entry Multiple: 5-8x EBITDA
- Exit Multiple: 6-9x EBITDA
- Target IRR: 18-22%

## Error Checking Patterns

### Common Errors to Detect
1. Circular references
2. #REF! errors (broken references)
3. Hardcoded values in formula cells
4. Inconsistent date formats
5. Balance sheet doesn't balance
6. Cash flow doesn't reconcile

## Code Example

```python
def validate_dcf_model(workbook):
    """Validate DCF model follows standards"""
    checks = {
        'wacc_calculation': check_wacc_formula(workbook),
        'npv_calculation': check_npv_formula(workbook),
        'terminal_value': check_terminal_value(workbook),
        'sensitivity_table': check_sensitivity(workbook)
    }
    return all(checks.values())
```
```

**Files to create:**
- `SKILL.md` - Main instructions
- `FORMULA_LIBRARY.md` - Complete formula reference
- `BENCHMARKS.md` - Industry multiples and metrics
- `VALIDATION_RULES.py` - Validation code
- `requirements.txt` - Dependencies (if any)

---

#### Skill 3: Database Schema & Query Patterns

**Priority:** HIGH 🔥
**Impact:** 🔥🔥 (Makes all database work easier)
**Effort:** Low (1-2 hours)
**Dependencies:** None

**What it includes:**
```markdown
---
name: PE Database Schema
description: Design and query databases for private equity portfolio management. Use when creating tables, writing SQL queries, or modeling data relationships.
version: 1.0.0
---

## Complete Schema

```sql
-- From Portfolio_Dashboard_Database_Schema.md
CREATE TABLE portfolio_companies (
    company_id UUID PRIMARY KEY,
    fund_id UUID NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    ...
);
```

## Common Query Patterns

### Get Latest Financials
```sql
SELECT DISTINCT ON (company_id) *
FROM financial_metrics
WHERE company_id = $1
ORDER BY company_id, period_date DESC;
```

### Top Performers by IRR
```sql
SELECT c.company_name, t.realized_irr
FROM portfolio_companies c
JOIN transactions t ON c.company_id = t.company_id
WHERE t.status = 'Exited'
ORDER BY t.realized_irr DESC
LIMIT 10;
```

### Portfolio Summary by Fund
```sql
SELECT 
    f.fund_name,
    COUNT(c.company_id) as num_companies,
    SUM(c.equity_invested) as total_invested,
    AVG(CASE WHEN t.status = 'Exited' 
        THEN t.realized_irr END) as avg_irr
FROM funds f
JOIN portfolio_companies c ON f.fund_id = c.fund_id
LEFT JOIN transactions t ON c.company_id = t.company_id
GROUP BY f.fund_id, f.fund_name;
```

## Indexing Strategy

```sql
-- Performance indexes
CREATE INDEX idx_financial_metrics_company_date 
    ON financial_metrics(company_id, period_date DESC);

CREATE INDEX idx_portfolio_companies_fund_status
    ON portfolio_companies(fund_id, company_status);

CREATE INDEX idx_transactions_status_date
    ON transactions(status, transaction_date DESC);
```

## SQLAlchemy Patterns

```python
# Efficient querying with joins
companies = session.query(PortfolioCompany)\
    .options(joinedload(PortfolioCompany.financials))\
    .options(joinedload(PortfolioCompany.valuation))\
    .filter(PortfolioCompany.fund_id == fund_id)\
    .all()

# Aggregate queries
from sqlalchemy import func

fund_summary = session.query(
    Fund.fund_name,
    func.count(PortfolioCompany.company_id).label('num_companies'),
    func.sum(PortfolioCompany.equity_invested).label('total_invested')
).join(PortfolioCompany)\
 .group_by(Fund.fund_id)\
 .all()
```
```

**Files to create:**
- `SKILL.md` - Main instructions
- `COMPLETE_SCHEMA.sql` - Full DDL
- `QUERY_LIBRARY.sql` - Common queries
- `OPTIMIZATION_GUIDE.md` - Indexing and performance
- `SQLALCHEMY_PATTERNS.py` - ORM examples

---

### 💡 PHASE 2: Automation Skills (Week 3-4)

These automate manual processes and data entry.

#### Skill 4: Financial PDF Extraction

**Priority:** HIGH 🔥
**Impact:** 🔥🔥🔥 (70% time savings on data entry)
**Effort:** Medium (3-4 hours)
**Dependencies:** None

**What it includes:**
```markdown
---
name: Financial Document Parser
description: Extract financial data from PDFs including balance sheets, P&Ls, cash flow statements, and audit reports. Use when processing portfolio company financials or uploaded financial statements.
version: 1.0.0
dependencies:
  - pdfplumber>=0.9.0
  - pytesseract>=0.3.10
  - pillow>=10.0.0
  - pandas>=2.0.0
---

## Table Detection

```python
def extract_financial_tables(pdf_path):
    """Extract tables from financial PDFs"""
    import pdfplumber
    
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract tables
            page_tables = page.extract_tables()
            
            for table in page_tables:
                # Identify if it's P&L, Balance Sheet, or Cash Flow
                table_type = identify_financial_statement(table)
                
                if table_type:
                    parsed = parse_financial_table(table, table_type)
                    tables.append({
                        'type': table_type,
                        'data': parsed,
                        'page': page.page_number
                    })
    
    return tables
```

## Statement Recognition Patterns

### P&L Indicators
- Keywords: Revenue, Sales, Cost of Goods Sold, EBITDA, Net Income
- Structure: Sequential top to bottom
- Validation: Revenue > 0, Net Income can be negative

### Balance Sheet Indicators
- Keywords: Assets, Liabilities, Equity, Total Assets
- Structure: Assets = Liabilities + Equity
- Validation: Balance check passes

### Cash Flow Indicators
- Keywords: Operating Activities, Investing, Financing
- Structure: Three sections
- Validation: Net change + opening = closing cash

## Validation Rules

```python
def validate_financial_statement(data, statement_type):
    """Validate extracted financial data"""
    
    if statement_type == 'balance_sheet':
        # Assets = Liabilities + Equity
        tolerance = 0.01  # 1% tolerance for rounding
        assets = data['total_assets']
        liab_eq = data['total_liabilities'] + data['shareholders_equity']
        
        if abs(assets - liab_eq) / assets > tolerance:
            return False, "Balance sheet doesn't balance"
    
    elif statement_type == 'income_statement':
        # Gross Profit = Revenue - COGS
        if 'revenue' in data and 'cogs' in data:
            calculated_gp = data['revenue'] - data['cogs']
            if abs(calculated_gp - data.get('gross_profit', 0)) > 1000:
                return False, "Gross profit calculation error"
    
    return True, "Valid"
```

## OCR for Scanned Documents

```python
def extract_from_scanned_pdf(pdf_path):
    """Use OCR for scanned documents"""
    from pdf2image import convert_from_path
    import pytesseract
    
    images = convert_from_path(pdf_path)
    
    extracted_text = []
    for image in images:
        # Preprocess for better OCR
        image = preprocess_image(image)
        
        # Extract text
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)
    
    return '\n'.join(extracted_text)

def preprocess_image(image):
    """Improve OCR accuracy"""
    # Convert to grayscale
    # Increase contrast
    # Denoise
    # Threshold
    return processed_image
```
```

**Files to create:**
- `SKILL.md` - Main instructions
- `pdf_extractor.py` - Core extraction code
- `statement_patterns.json` - Recognition patterns
- `VALIDATION_RULES.md` - Data quality checks
- `example_extraction.py` - Usage examples

---

#### Skill 5: Data Validation for Finance

**Priority:** MEDIUM ⭐
**Impact:** 🔥🔥 (Catches errors early)
**Effort:** Medium (2-3 hours)
**Dependencies:** Database Schema skill

**What it includes:**
- Balance sheet validation (Assets = L + E)
- Cash flow reconciliation
- Ratio reasonableness checks
- Outlier detection algorithms
- Industry-specific validation rules

---

### 📊 PHASE 3: Reporting Skills (Month 2)

These generate investor reports and dashboards.

#### Skill 6: LP Reporting Automation

**Priority:** MEDIUM ⭐
**Impact:** 🔥🔥 (Saves 10+ hours per quarter)
**Effort:** Medium (3-4 hours)
**Dependencies:** Excel Model Generator, Database Schema

**What it includes:**
```markdown
---
name: LP Report Generator
description: Generate quarterly and annual LP reports with standardized formats including portfolio summaries, fund performance, and capital call notices. Use when creating investor reports or board materials.
version: 1.0.0
---

## Report Templates

### Quarterly Report Structure
1. Executive Summary
   - Fund overview
   - Quarter highlights
   - Key metrics (TVPI, DPI, IRR)
   
2. Portfolio Company Updates
   - Performance by company
   - Operational milestones
   - Financial metrics
   
3. New Investments
   - Deal descriptions
   - Investment thesis
   - Initial metrics
   
4. Exits & Distributions
   - Exit summaries
   - Returns analysis
   - Distribution schedule

### Standard KPI Definitions

```python
def calculate_lp_metrics(fund_data):
    """Calculate standard LP reporting metrics"""
    
    metrics = {
        # Total Value to Paid-In
        'tvpi': (distributions + nav) / paid_in_capital,
        
        # Distributions to Paid-In
        'dpi': distributions / paid_in_capital,
        
        # Residual Value to Paid-In
        'rvpi': nav / paid_in_capital,
        
        # Internal Rate of Return
        'irr': calculate_irr(cash_flows, dates),
        
        # Multiple of Invested Capital
        'moic': (exit_proceeds + current_value) / invested_capital
    }
    
    return metrics
```

## Waterfall Calculations

```python
def calculate_waterfall(fund, distributions):
    """Calculate GP/LP waterfall with carried interest"""
    
    # Return of capital
    lp_return = min(distributions, fund.lp_contributions)
    remaining = distributions - lp_return
    
    # Preferred return (8%)
    pref_return = fund.lp_contributions * 0.08 * years_held
    lp_pref = min(remaining, pref_return)
    remaining -= lp_pref
    
    # GP catch-up (until GP gets 20% of total)
    gp_catchup = min(remaining, (lp_return + lp_pref) * 0.25)
    remaining -= gp_catchup
    
    # Carry split (80/20)
    lp_carry = remaining * 0.80
    gp_carry = remaining * 0.20
    
    return {
        'lp_total': lp_return + lp_pref + lp_carry,
        'gp_total': gp_catchup + gp_carry,
        'details': {...}
    }
```
```

---

#### Skill 7: Dashboard Design Patterns

**Priority:** LOW 💡
**Impact:** ⭐ (Improves UI consistency)
**Effort:** Low (1-2 hours)
**Dependencies:** None

**What it includes:**
- High-density layout patterns
- Color coding standards
- Drill-down navigation
- Mobile-responsive designs
- Example screenshots

---

### 🛠️ PHASE 4: Advanced Skills (Month 3)

These add AI-powered features and integrations.

#### Skill 8: Deal Analysis Framework

**Priority:** MEDIUM ⭐
**Impact:** 🔥 (Speeds up IC prep)
**Effort:** High (4-5 hours)
**Dependencies:** PE Modeling Standards, Database Schema

**What it includes:**
- IC memo template
- Red flags checklist
- Comparable company analysis
- Risk scoring framework
- Investment decision tree

---

#### Skill 9: Market Data Integration

**Priority:** LOW 💡
**Impact:** ⭐ (Enables comps analysis)
**Effort:** High (4-5 hours)
**Dependencies:** Database Schema

**What it includes:**
- Capital IQ API patterns
- Yahoo Finance integration
- Comparable company selection
- Public market data normalization
- Rate limiting strategies

---

#### Skill 10: API Development Standards

**Priority:** MEDIUM ⭐
**Impact:** 🔥 (Improves backend quality)
**Effort:** Medium (2-3 hours)
**Dependencies:** Database Schema

**What it includes:**
```markdown
---
name: Financial API Builder
description: Build REST APIs for financial data with proper validation, authentication, and documentation. Use when creating backend endpoints for portfolio dashboard.
version: 1.0.0
---

## FastAPI Patterns

### Standard Endpoint Structure

```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

app = FastAPI(title="Portfolio Dashboard API")

class CompanyResponse(BaseModel):
    company_id: uuid.UUID
    company_name: str
    sector: str
    revenue: Optional[float] = Field(None, ge=0)
    ebitda: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "company_name": "Acme Corp",
                "sector": "Software",
                "revenue": 50000000.00,
                "ebitda": 12000000.00
            }
        }

@app.get("/api/v1/companies/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get company details by ID"""
    
    company = db.query(PortfolioCompany).filter(
        PortfolioCompany.company_id == company_id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company
```

## Input Validation

```python
from pydantic import BaseModel, validator, Field
from decimal import Decimal

class FinancialMetricCreate(BaseModel):
    company_id: uuid.UUID
    period_date: date
    revenue: Decimal = Field(..., ge=0, description="Must be non-negative")
    ebitda: Optional[Decimal] = None
    ebitda_margin: Optional[Decimal] = Field(None, ge=-1, le=1)
    
    @validator('ebitda_margin')
    def validate_margin(cls, v, values):
        """Ensure margin is reasonable"""
        if v is not None and abs(v) > 1:
            raise ValueError("EBITDA margin must be between -100% and 100%")
        return v
    
    @validator('ebitda')
    def validate_ebitda_vs_revenue(cls, v, values):
        """EBITDA should not exceed revenue significantly"""
        if v and 'revenue' in values:
            if v > values['revenue'] * 1.5:
                raise ValueError("EBITDA cannot be > 150% of revenue")
        return v
```

## Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Validate JWT token and return user"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/v1/companies")
async def list_companies(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Protected endpoint - requires authentication"""
    # User is authenticated, proceed with query
    ...
```

## Rate Limiting

```python
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/generate-model")
@limiter.limit("10/minute")  # Max 10 model generations per minute
async def generate_model(
    request: Request,
    model_request: ModelRequest
):
    """Rate-limited endpoint for expensive operations"""
    ...
```
```

---

## 📅 Implementation Timeline

### Week 1
- Day 1-2: PE Financial Modeling Standards skill
- Day 3-4: Database Schema skill
- Day 5: Test both skills together

### Week 2
- Day 1-3: Financial PDF Extraction skill
- Day 4-5: Data Validation skill

### Week 3
- Day 1-3: LP Reporting skill
- Day 4-5: Dashboard Design Patterns skill

### Week 4
- Day 1-2: Deal Analysis skill
- Day 3-4: Market Data Integration skill
- Day 5: API Development Standards skill

### Week 5
- Integration testing
- Documentation
- Team training

---

## 🎯 Quick Start Template

Use this as a starting point for any new skill:

```markdown
---
name: Your Skill Name
description: Clear explanation of when Claude should use this (max 200 chars)
version: 1.0.0
dependencies:
  - python>=3.8
  - any-required-packages>=1.0.0
---

# Skill Name

## Overview
Brief description of what this skill does and why it's useful.

## When to Use This Skill
Claude should invoke this skill when:
- User asks to [specific action 1]
- User mentions [keyword 1], [keyword 2]
- User needs to [specific task]

**Do NOT use for:**
- [Scenarios where this skill doesn't apply]

## Core Principles
1. **Principle 1** - Explanation
2. **Principle 2** - Explanation
3. **Principle 3** - Explanation

## Code Examples

### Example 1: Basic Usage
```python
# Complete, runnable code example
def example_function():
    pass
```

### Example 2: Advanced Usage
```python
# More complex example
def advanced_example():
    pass
```

## Common Pitfalls
### Pitfall 1: Description
**Problem:** What goes wrong
**Solution:** How to fix it

## Best Practices
1. ✅ Do this
2. ✅ Also do this
3. ❌ Don't do this

## Integration Points
How this skill works with:
- Other skills
- Your project
- External systems

## Resources
- REFERENCE.md - Detailed reference
- code_file.py - Implementation
- examples.py - Usage examples
```

---

## 💡 Pro Tips for Skill Creation

### 1. Start Small
Don't try to make the perfect skill. Start with:
- Basic SKILL.md
- One code example
- Simple description
Then iterate based on usage.

### 2. Test Incrementally
After each addition:
- Upload to Claude
- Test with a prompt
- Check if Claude uses it correctly
- Refine description if needed

### 3. Use Real Examples
The best examples come from actual use:
- Save successful Claude conversations
- Extract the good code patterns
- Add to your skill

### 4. Version Control
Keep track of changes:
- Update version number in SKILL.md
- Save old ZIPs as backups
- Document what changed

### 5. Measure Impact
Track:
- How often skill is invoked
- Time saved per use
- Error rate reduction
- User satisfaction

---

## 🎓 Learning Resources

### Anthropic Documentation
- [Skill Authoring Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Example Skills Repository](https://github.com/anthropics/skills)

### Your Project Docs
- Portfolio_Dashboard_Implementation_Plan.md
- MODEL_GENERATION_GUIDE.md
- DCF_MODEL_GUIDE.md
- LBO_MODEL_GUIDE.md

### This Skill
- Study the PE Excel Model Generator skill structure
- See how SKILL.md, REFERENCE.md, and code files work together
- Copy the patterns that work

---

## ✅ Checklist for Each New Skill

Before uploading:

- [ ] SKILL.md has valid YAML frontmatter
- [ ] `name` is descriptive and ≤64 characters
- [ ] `description` clearly explains when to use (≤200 chars)
- [ ] At least 3 code examples included
- [ ] Common pitfalls documented
- [ ] Best practices listed
- [ ] ZIP structure is correct (folder at root)
- [ ] Tested locally (if applicable)
- [ ] README.md explains usage
- [ ] Integration with project explained

---

## 🚀 Ready to Build?

Start with **Skill 2: PE Financial Modeling Standards** this week. It's:
- ✅ Low effort (2-3 hours)
- ✅ High impact (ensures consistency)
- ✅ No dependencies
- ✅ Complements Excel Generator skill

Just say: **"Let's create the PE Financial Modeling Standards skill"**

I'll help you:
1. Structure the SKILL.md file
2. Extract formulas from your models
3. Document industry benchmarks
4. Create validation rules
5. Package and test

---

**Next skill creation time: 2-3 hours**
**Total time to create all 9 skills: 25-30 hours**
**Time savings after completion: 200+ hours per quarter**

Let's build the skill library that will transform your portfolio management platform! 🚀
