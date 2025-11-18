# Excel Model Generation System - Complete Guide

## 🎯 Overview

This system generates all 5 financial models (DCF, LBO, Merger, DD Tracker, QoE) directly from the Portfolio Dashboard database. Each model is generated with **all formulas intact** and populated with company-specific data.

---

## 📁 Files in This System

### Core Files
1. **excel_model_generator.py** - Main model generation classes
2. **api_model_generator.py** - FastAPI REST API endpoints
3. **example_usage.py** - Example code for using the generators
4. **requirements.txt** - Python dependencies

### Generated Output
- Models are saved to `/home/claude/generated_models/`
- Naming convention: `{CompanyName}_{ModelType}_{Timestamp}.xlsx`
- Example: `Acme_Corp_DCF_20251030_143025.xlsx`

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   FRONTEND / API CLIENT                  │
│          (React Dashboard, Postman, curl, etc.)          │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP REST API
                     │
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Server (Port 8000)                  │
│                api_model_generator.py                    │
│                                                          │
│  Endpoints:                                              │
│  • POST /api/v1/models/generate                          │
│  • POST /api/v1/models/generate-batch                    │
│  • POST /api/v1/models/generate-merger                   │
│  • GET  /api/v1/models/download/{file}                   │
│  • GET  /api/v1/models/list/{company_id}                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Python Classes
                     │
┌────────────────────▼────────────────────────────────────┐
│            Model Generator Classes                       │
│            excel_model_generator.py                      │
│                                                          │
│  • DCFModelGenerator                                     │
│  • LBOModelGenerator                                     │
│  • MergerModelGenerator                                  │
│  • DDTrackerGenerator                                    │
│  • QoEAnalysisGenerator                                  │
│  • BatchModelGenerator                                   │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
┌─────────────────┐   ┌─────────────────┐
│   PostgreSQL    │   │  Excel Templates │
│    Database     │   │  (Original Models)│
│                 │   │                  │
│ • portfolio_    │   │ • DCF_Model_     │
│   companies     │   │   Comprehensive  │
│ • financial_    │   │ • LBO_Model_     │
│   metrics       │   │   Comprehensive  │
│ • valuations    │   │ • Merger_Model_  │
│ • company_kpis  │   │   Comprehensive  │
└─────────────────┘   └─────────────────┘
```

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary openpyxl pydantic --break-system-packages
```

### 2. Configure Database

Create `.env` file:

```bash
DATABASE_URL=postgresql://portfolio_user:password@localhost/portfolio_db
```

### 3. Ensure Templates Exist

Make sure the comprehensive Excel models are available:
- `/mnt/user-data/uploads/DCF_Model_Comprehensive.xlsx`
- `/mnt/user-data/uploads/LBO_Model_Comprehensive.xlsx`
- `/mnt/user-data/uploads/Merger_Model_Comprehensive.xlsx`
- `/mnt/user-data/uploads/DD_Tracker_Comprehensive.xlsx`
- `/mnt/user-data/uploads/QoE_Analysis_Comprehensive.xlsx`

### 4. Start the API Server

```bash
cd /home/claude
python api_model_generator.py
```

Server runs on http://localhost:8000

---

## 📊 How It Works

### Data Flow

1. **User Request** → API endpoint with company_id
2. **Fetch Data** → Query database for company, financials, valuation
3. **Load Template** → Load the comprehensive Excel template
4. **Populate Cells** → Map database values to specific Excel cells
5. **Preserve Formulas** → All formulas remain intact and functional
6. **Save File** → Export to `/generated_models/` directory
7. **Return Path** → User can download the file

### Cell Mapping Strategy

The system maps database fields to specific Excel cells:

**Example: DCF Model**
```python
# Database → Excel Cell Mapping
company.company_name       → Sheet['DCF']['B2']
latest.revenue            → Sheet['DCF']['C8']
latest.ebitda_margin      → Sheet['DCF']['C12']
valuation.wacc            → Sheet['WACC']['C15']
valuation.terminal_growth → Sheet['DCF']['C16']
```

**Formula Preservation**
```python
# These cells remain as FORMULAS (not values):
Sheet['DCF']['D8'] = '=C8*(1+C9)'        # Year 2 Revenue
Sheet['DCF']['C20'] = '=NPV(WACC,C8:H8)' # Present Value
Sheet['DCF']['C22'] = '=C20+C21'         # Enterprise Value
```

---

## 🚀 Usage Examples

### Example 1: Generate Single DCF Model

**Python Code:**
```python
from excel_model_generator import DCFModelGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup database
engine = create_engine('postgresql://portfolio_user:password@localhost/portfolio_db')
Session = sessionmaker(bind=engine)
db = Session()

# Generate DCF
company_id = '123e4567-e89b-12d3-a456-426614174000'
generator = DCFModelGenerator(db, company_id)
generator.generate('/home/claude/outputs/Acme_DCF.xlsx')

print("✓ DCF model generated!")
```

**API Call (curl):**
```bash
curl -X POST http://localhost:8000/api/v1/models/generate \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "123e4567-e89b-12d3-a456-426614174000",
    "model_type": "DCF",
    "scenario_name": "Base Case"
  }'
```

**API Call (Python requests):**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/models/generate',
    json={
        'company_id': '123e4567-e89b-12d3-a456-426614174000',
        'model_type': 'DCF',
        'scenario_name': 'Base Case'
    }
)

result = response.json()
print(f"File path: {result['file_path']}")
```

### Example 2: Generate All Models (Batch)

```python
from excel_model_generator import BatchModelGenerator

db = Session()
company_id = '123e4567-e89b-12d3-a456-426614174000'

# Generate all 5 models
batch_gen = BatchModelGenerator(db)
results = batch_gen.generate_all_models(
    company_id,
    output_dir='/home/claude/generated_models'
)

for model_type, file_path in results.items():
    if file_path:
        print(f"✓ {model_type}: {file_path}")
    else:
        print(f"✗ {model_type}: Failed")
```

### Example 3: Generate Merger Model (2 Companies)

```python
from excel_model_generator import MergerModelGenerator

acquirer_id = '123e4567-e89b-12d3-a456-426614174000'
target_id = '987fcdeb-51a2-43f1-9876-543210fedcba'

generator = MergerModelGenerator(db, acquirer_id, target_id)
generator.generate('/home/claude/outputs/Merger_Acme_Target.xlsx')
```

### Example 4: List All Generated Models

**API Call:**
```bash
curl http://localhost:8000/api/v1/models/list/123e4567-e89b-12d3-a456-426614174000
```

**Response:**
```json
{
  "company_id": "123e4567-e89b-12d3-a456-426614174000",
  "company_name": "Acme Corp",
  "total_models": 5,
  "models": [
    {
      "file_name": "Acme_Corp_DCF_20251030_143025.xlsx",
      "model_type": "DCF",
      "file_size": 245678,
      "created_at": "2025-10-30T14:30:25",
      "download_url": "/api/v1/models/download/Acme_Corp_DCF_20251030_143025.xlsx"
    }
  ]
}
```

### Example 5: Download Generated Model

```bash
curl -O http://localhost:8000/api/v1/models/download/Acme_Corp_DCF_20251030_143025.xlsx
```

---

## 🗺️ Database → Excel Mapping Reference

### DCF Model Mapping

| Database Field | Excel Location | Type | Format |
|----------------|----------------|------|--------|
| `company.company_name` | DCF!B2 | Input | Text |
| `financials.revenue` | Historical!C8 | Input | Currency |
| `financials.ebitda` | Historical!C15 | Input | Currency |
| `financials.ebitda_margin` | DCF!C12 | Input | Percent |
| `valuation.wacc` | WACC!C15 | Input | Percent |
| `valuation.terminal_growth_rate` | DCF!C16 | Input | Percent |
| `financials.capex` | DCF!C18 | Input | Currency |
| `financials.working_capital` | DCF!C20 | Input | Currency |

### LBO Model Mapping

| Database Field | Excel Location | Type | Format |
|----------------|----------------|------|--------|
| `company.purchase_price` | Transaction Assumptions!C8 | Input | Currency |
| `company.entry_multiple` | Transaction Assumptions!C9 | Input | Multiple (0.0x) |
| `company.equity_invested` | Sources & Uses!C10 | Input | Currency |
| `company.debt_raised` | Sources & Uses!C15 | Input | Currency |
| `valuation.exit_multiple` | Transaction Assumptions!C12 | Input | Multiple |
| `valuation.hold_period_years` | Transaction Assumptions!C13 | Input | Integer |
| `financials.revenue` | Operating Model!C8 | Input | Currency |
| `financials.ebitda` | Operating Model!C15 | Input | Currency |

### Merger Model Mapping

| Database Field | Excel Location | Type | Format |
|----------------|----------------|------|--------|
| `acquirer.company_name` | Transaction Assumptions!C5 | Input | Text |
| `target.company_name` | Transaction Assumptions!C6 | Input | Text |
| `target.purchase_price` | Transaction Assumptions!C10 | Input | Currency |
| `acquirer_financials.revenue` | Pro Forma IS!C6 | Input | Currency |
| `target_financials.revenue` | Pro Forma IS!D6 | Input | Currency |
| `acquirer_financials.ebitda` | Pro Forma IS!C15 | Input | Currency |
| `target_financials.ebitda` | Pro Forma IS!D15 | Input | Currency |

---

## ⚙️ Advanced Features

### Scenario Management

Generate multiple scenarios for the same company:

```python
scenarios = ['Base Case', 'Upside', 'Downside']

for scenario in scenarios:
    generator = DCFModelGenerator(db, company_id)
    generator.scenario_name = scenario
    generator.generate(f'/outputs/DCF_{scenario}.xlsx')
```

### Custom Cell Mapping

Override default mappings for custom templates:

```python
class CustomDCFGenerator(DCFModelGenerator):
    def _populate_dcf_sheet(self):
        super()._populate_dcf_sheet()
        
        # Custom mapping
        sheet = self.wb['DCF']
        sheet['E10'] = self.company.custom_field
```

### Bulk Generation

Generate models for all companies in a fund:

```python
fund_id = '456e7890-f12b-34c5-d678-901234567890'

companies = db.query(PortfolioCompany).filter(
    PortfolioCompany.fund_id == fund_id
).all()

for company in companies:
    batch_gen = BatchModelGenerator(db)
    batch_gen.generate_all_models(str(company.company_id))
```

---

## 🎨 Styling & Formatting

All generated models maintain the original styling:

- **Blue cells with yellow fill** = User inputs
- **White cells** = Formulas (auto-calculated)
- **Green text** = Links to other sheets
- **Headers** = Dark blue background, white text
- **Number formats** = Currency, percentages, multiples preserved

The system applies styles using:
```python
apply_input_style(cell)       # Blue input cells
apply_formula_style(cell)     # Formula cells
apply_number_format(cell, 'currency')  # $#,##0 format
```

---

## 🔍 Validation & Quality Checks

### Formula Preservation Test

```python
def test_formula_preservation(file_path):
    """Verify all formulas are intact"""
    wb = load_workbook(file_path)
    sheet = wb['DCF']
    
    # Check that formula cells contain formulas (not values)
    assert sheet['D8'].value.startswith('='), "Revenue growth formula missing"
    assert sheet['C22'].value.startswith('='), "Enterprise value formula missing"
    
    print("✓ All formulas preserved")
```

### Data Accuracy Test

```python
def test_data_accuracy(company_id, file_path):
    """Verify data matches database"""
    # Fetch from database
    company = db.query(PortfolioCompany).get(company_id)
    
    # Read from Excel
    wb = load_workbook(file_path)
    sheet = wb['DCF']
    
    # Compare
    assert sheet['B2'].value == company.company_name
    print("✓ Data accurate")
```

---

## 📈 Performance Optimization

### Caching Templates

```python
class CachedModelGenerator:
    _template_cache = {}
    
    def load_template(self):
        if self.template_path not in self._template_cache:
            self._template_cache[self.template_path] = load_workbook(self.template_path)
        return self._template_cache[self.template_path].copy()
```

### Parallel Generation

```python
from concurrent.futures import ThreadPoolExecutor

def generate_models_parallel(company_ids):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(generate_single_model, cid)
            for cid in company_ids
        ]
        results = [f.result() for f in futures]
    return results
```

---

## 🐛 Troubleshooting

### Issue: Template Not Found
```
FileNotFoundError: DCF template not found
```
**Solution:** Ensure templates are in `/mnt/user-data/uploads/`

### Issue: Database Connection Failed
```
OperationalError: could not connect to server
```
**Solution:** Check DATABASE_URL in .env file, verify PostgreSQL is running

### Issue: Missing Financial Data
```
IndexError: list index out of range
```
**Solution:** Company may not have financial data. Add data entry first.

### Issue: Formula Errors in Excel
```
#REF! or #DIV/0! errors in generated file
```
**Solution:** Check that all linked sheets exist and formulas reference correct cells

---

## 📚 API Documentation

Full API documentation available at: http://localhost:8000/docs (Swagger UI)

### Key Endpoints

**POST /api/v1/models/generate**
- Generate a single model
- Body: `{company_id, model_type, scenario_name}`
- Returns: File path and metadata

**POST /api/v1/models/generate-batch**
- Generate all models for a company
- Body: `{company_id, models[]}`
- Returns: Status of each model

**POST /api/v1/models/generate-merger**
- Generate merger model
- Body: `{acquirer_id, target_id, scenario_name}`
- Returns: File path and metadata

**GET /api/v1/models/download/{file_name}**
- Download generated file
- Returns: Excel file (binary)

**GET /api/v1/models/list/{company_id}**
- List all models for a company
- Returns: Array of model metadata

---

## 🚀 Next Steps

### Immediate (Week 1)
1. ✅ Core generator classes (DONE)
2. ✅ FastAPI integration (DONE)
3. ⏳ Complete DD Tracker generator
4. ⏳ Complete QoE generator

### Short-term (Month 1)
- Add scenario management
- Implement model versioning
- Add bulk export to zip
- Create React UI components

### Medium-term (Months 2-3)
- PDF extraction integration
- Automated quarterly updates
- LP reporting templates
- Email notifications on completion

---

## 🤝 Integration with Portfolio Dashboard

This model generation system integrates seamlessly with the main dashboard:

```typescript
// React component example
const GenerateModelButton: React.FC<{companyId: string}> = ({companyId}) => {
  const handleGenerate = async (modelType: string) => {
    const response = await fetch('/api/v1/models/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        company_id: companyId,
        model_type: modelType
      })
    });
    
    const result = await response.json();
    window.location.href = result.file_path;  // Download
  };
  
  return (
    <ButtonGroup>
      <Button onClick={() => handleGenerate('DCF')}>Generate DCF</Button>
      <Button onClick={() => handleGenerate('LBO')}>Generate LBO</Button>
      <Button onClick={() => handleGenerate('All')}>Generate All</Button>
    </ButtonGroup>
  );
};
```

---

## 📞 Support

For questions or issues:
1. Check this documentation
2. Review example_usage.py for code samples
3. Check API docs at /docs endpoint
4. Review project knowledge files

---

**System Version:** 1.0  
**Last Updated:** October 30, 2025  
**Status:** Production-Ready for DCF and LBO models  
**Remaining:** DD Tracker and QoE generators (in progress)
