# VALUE-ADD RENOVATION BUDGET BUILDER
## Portfolio Dashboard Integration Guide

**Version 1.0 | November 2025**  
**Technical Documentation for Platform Integration**

---

## 📋 TABLE OF CONTENTS

1. [Integration Overview](#integration-overview)
2. [Database Schema Mapping](#database-schema-mapping)
3. [API Integration Specifications](#api-integration-specifications)
4. [Data Flow Architecture](#data-flow-architecture)
5. [Automated Import/Export](#automated-import-export)
6. [Real-Time Synchronization](#real-time-synchronization)
7. [Implementation Roadmap](#implementation-roadmap)

---

## INTEGRATION OVERVIEW

### Purpose

The Value-Add Renovation Budget Builder integrates with the **Portfolio Dashboard** platform to enable:

1. **Centralized storage** of renovation budgets for 10-100+ properties
2. **Automated PDF extraction** of contractor bids and property data
3. **Real-time budget tracking** with actual vs projected costs
4. **Multi-property portfolio analysis** with aggregated metrics
5. **LP reporting** with renovation ROI across all properties

### Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    PORTFOLIO DASHBOARD                       │
│                     (PostgreSQL Database)                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴──────────┐
                │                      │
        ┌───────▼────────┐    ┌───────▼────────┐
        │  Python API    │    │  Excel Models  │
        │  (FastAPI)     │    │   (openpyxl)   │
        └───────┬────────┘    └───────┬────────┘
                │                      │
        ┌───────▼──────────────────────▼────────┐
        │    Value-Add Renovation Builder       │
        │     (Excel Template + Database)       │
        └───────────────────────────────────────┘
```

### Integration Methods

1. **Manual Import**: Upload Excel file via UI → Parse → Store in database
2. **API Generation**: Create Excel from database via openpyxl → Download
3. **Real-Time Sync**: Update database when Excel changes detected
4. **PDF Automation**: Extract contractor bids → Populate Excel → Save to database

---

## DATABASE SCHEMA MAPPING

### Table 1: `renovation_projects`

**Purpose**: Store master renovation project data

```sql
CREATE TABLE renovation_projects (
    project_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_company_id UUID REFERENCES portfolio_companies(company_id),
    property_name VARCHAR(255) NOT NULL,
    property_address TEXT,
    total_units INTEGER NOT NULL,
    building_class VARCHAR(10), -- 'Class A', 'Class B', 'Class C'
    avg_unit_size_sf INTEGER,
    
    -- Current & Pro Forma
    current_monthly_rent DECIMAL(12,2),
    proforma_monthly_rent DECIMAL(12,2),
    monthly_rent_increase DECIMAL(12,2),
    
    -- Value Creation
    exit_cap_rate DECIMAL(5,4),
    noi_margin DECIMAL(5,4) DEFAULT 0.60,
    
    -- Timeline
    project_start_date DATE,
    project_duration_months INTEGER,
    units_per_phase INTEGER,
    days_per_unit INTEGER,
    lost_rent_days_per_unit INTEGER,
    
    -- Holding Costs
    monthly_debt_service DECIMAL(12,2),
    monthly_operating_expenses DECIMAL(12,2),
    monthly_management_fee DECIMAL(12,2),
    
    -- Budget Summary
    base_renovation_cost DECIMAL(15,2),
    contingency_percentage DECIMAL(5,4) DEFAULT 0.10,
    total_budget DECIMAL(15,2),
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by_user_id UUID REFERENCES users(user_id),
    status VARCHAR(50) DEFAULT 'Planning', -- 'Planning', 'In Progress', 'Complete'
    
    CONSTRAINT fk_portfolio_company 
        FOREIGN KEY (portfolio_company_id) 
        REFERENCES portfolio_companies(company_id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_renovation_projects_company ON renovation_projects(portfolio_company_id);
CREATE INDEX idx_renovation_projects_status ON renovation_projects(status);
```

**Excel Mapping**:
- `Inputs!B2` → `property_name`
- `Inputs!B3` → `property_address`
- `Inputs!B4` → `total_units`
- `Inputs!B5` → `building_class`
- `Inputs!B6` → `avg_unit_size_sf`
- `Inputs!B10` → `current_monthly_rent`
- `Inputs!B11` → `proforma_monthly_rent`
- `Inputs!B15` → `exit_cap_rate`
- `Inputs!B16` → `noi_margin`
- `Unit-Level Budget!C100` → `base_renovation_cost`
- `Unit-Level Budget!C104` → `total_budget`

---

### Table 2: `renovation_unit_budgets`

**Purpose**: Store unit-by-unit renovation costs

```sql
CREATE TABLE renovation_unit_budgets (
    budget_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES renovation_projects(project_id) ON DELETE CASCADE,
    unit_number VARCHAR(20) NOT NULL,
    unit_type VARCHAR(20), -- '1BR', '2BR', '3BR'
    
    -- Cost Categories
    kitchen_cost DECIMAL(10,2),
    bathroom_cost DECIMAL(10,2),
    flooring_cost DECIMAL(10,2),
    paint_cost DECIMAL(10,2),
    fixtures_cost DECIMAL(10,2),
    total_unit_cost DECIMAL(10,2),
    
    -- Phasing
    phase_number INTEGER,
    phase_start_date DATE,
    renovation_status VARCHAR(50) DEFAULT 'Planned', -- 'Planned', 'In Progress', 'Complete'
    
    -- Actual Costs (for tracking)
    actual_kitchen_cost DECIMAL(10,2),
    actual_bathroom_cost DECIMAL(10,2),
    actual_flooring_cost DECIMAL(10,2),
    actual_paint_cost DECIMAL(10,2),
    actual_fixtures_cost DECIMAL(10,2),
    actual_total_cost DECIMAL(10,2),
    
    completion_date DATE,
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_renovation_project 
        FOREIGN KEY (project_id) 
        REFERENCES renovation_projects(project_id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_unit_budgets_project ON renovation_unit_budgets(project_id);
CREATE INDEX idx_unit_budgets_phase ON renovation_unit_budgets(phase_number);
CREATE INDEX idx_unit_budgets_status ON renovation_unit_budgets(renovation_status);
```

**Excel Mapping** (per row in Unit-Level Budget sheet):
- `Unit-Level Budget!A7:A56` → `unit_number`
- `Unit-Level Budget!B7:B56` → `unit_type`
- `Unit-Level Budget!C7:C56` → `kitchen_cost`
- `Unit-Level Budget!D7:D56` → `bathroom_cost`
- `Unit-Level Budget!E7:E56` → `flooring_cost`
- `Unit-Level Budget!F7:F56` → `paint_cost`
- `Unit-Level Budget!G7:G56` → `fixtures_cost`
- `Unit-Level Budget!H7:H56` → `total_unit_cost`
- `Unit-Level Budget!I7:I56` → `phase_number`
- `Unit-Level Budget!J7:J56` → `phase_start_date`
- `Unit-Level Budget!K7:K56` → `renovation_status`

---

### Table 3: `renovation_phases`

**Purpose**: Track renovation phasing and cash flow

```sql
CREATE TABLE renovation_phases (
    phase_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES renovation_projects(project_id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    phase_start_date DATE,
    phase_end_date DATE,
    
    -- Budget
    units_in_phase INTEGER,
    phase_renovation_cost DECIMAL(12,2),
    phase_lost_rent DECIMAL(12,2),
    phase_holding_costs DECIMAL(12,2),
    total_phase_cash_out DECIMAL(12,2),
    
    -- Actuals (for tracking)
    actual_renovation_cost DECIMAL(12,2),
    actual_lost_rent DECIMAL(12,2),
    actual_holding_costs DECIMAL(12,2),
    actual_total_cash_out DECIMAL(12,2),
    
    phase_status VARCHAR(50) DEFAULT 'Planned', -- 'Planned', 'Active', 'Complete'
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_renovation_project_phase 
        FOREIGN KEY (project_id) 
        REFERENCES renovation_projects(project_id) 
        ON DELETE CASCADE
);

CREATE INDEX idx_phases_project ON renovation_phases(project_id);
CREATE INDEX idx_phases_number ON renovation_phases(phase_number);
```

**Excel Mapping** (per row in Renovation Phasing sheet):
- `Renovation Phasing!A14:A18` → `phase_number`
- `Renovation Phasing!B14:B18` → `phase_start_date`
- `Renovation Phasing!C14:C18` → `phase_end_date`
- `Renovation Phasing!D14:D18` → `units_in_phase`
- `Renovation Phasing!E14:E18` → `phase_renovation_cost`
- `Renovation Phasing!F14:F18` → `phase_lost_rent`
- `Renovation Phasing!G14:G18` → `phase_holding_costs`
- `Renovation Phasing!H14:H18` → `total_phase_cash_out`

---

### Table 4: `renovation_roi_metrics`

**Purpose**: Store calculated ROI and value creation metrics

```sql
CREATE TABLE renovation_roi_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES renovation_projects(project_id) ON DELETE CASCADE,
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Investment
    total_capital_required DECIMAL(15,2),
    base_renovation_cost DECIMAL(15,2),
    contingency_amount DECIMAL(15,2),
    total_lost_rent DECIMAL(15,2),
    total_holding_costs DECIMAL(15,2),
    
    -- Revenue Impact
    annual_rent_increase_per_unit DECIMAL(10,2),
    total_annual_revenue_increase DECIMAL(12,2),
    rent_increase_percentage DECIMAL(5,4),
    
    -- NOI & Value
    annual_noi_increase DECIMAL(12,2),
    property_value_created DECIMAL(15,2),
    net_gain DECIMAL(15,2),
    
    -- Return Metrics
    roi_percentage DECIMAL(5,4),
    value_creation_multiple DECIMAL(5,2),
    cash_on_cash_return_yr1 DECIMAL(5,4),
    payback_period_years DECIMAL(5,2),
    
    -- Per Unit Metrics
    cost_per_unit DECIMAL(10,2),
    value_creation_per_unit DECIMAL(10,2),
    net_gain_per_unit DECIMAL(10,2),
    cost_per_sf DECIMAL(8,2),
    value_creation_per_sf DECIMAL(8,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_roi_metrics_project ON renovation_roi_metrics(project_id);
CREATE INDEX idx_roi_metrics_date ON renovation_roi_metrics(calculation_date);
```

**Excel Mapping** (from ROI Calculator sheet):
- `ROI Calculator!B10` → `total_capital_required`
- `ROI Calculator!B5` → `base_renovation_cost`
- `ROI Calculator!B6` → `contingency_amount`
- `ROI Calculator!B7` → `total_lost_rent`
- `ROI Calculator!B8` → `total_holding_costs`
- `ROI Calculator!B20` → `total_annual_revenue_increase`
- `ROI Calculator!B26` → `rent_increase_percentage`
- `ROI Calculator!B30` → `annual_noi_increase`
- `ROI Calculator!B33` → `property_value_created`
- `ROI Calculator!B36` → `net_gain`
- `ROI Calculator!B47` → `roi_percentage`
- `ROI Calculator!B48` → `value_creation_multiple`
- `ROI Calculator!B49` → `cash_on_cash_return_yr1`
- `ROI Calculator!B50` → `payback_period_years`

---

### Table 5: `renovation_cost_database`

**Purpose**: Store reference pricing for renovation items

```sql
CREATE TABLE renovation_cost_database (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category VARCHAR(100) NOT NULL, -- 'Kitchen', 'Bathroom', 'Flooring', etc.
    item_name VARCHAR(255) NOT NULL,
    
    -- Pricing by Class
    class_a_cost DECIMAL(10,2),
    class_b_cost DECIMAL(10,2),
    class_c_cost DECIMAL(10,2),
    
    unit_type VARCHAR(50), -- 'per kitchen', 'per SF', 'per unit', etc.
    notes TEXT,
    
    -- Market Adjustments
    market_region VARCHAR(100),
    effective_date DATE DEFAULT CURRENT_DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_cost_db_category ON renovation_cost_database(category);
CREATE INDEX idx_cost_db_active ON renovation_cost_database(is_active);
```

**Excel Mapping** (from Cost Database sheet):
- Bulk import from `Cost Database!A5:F150` (all rows)
- Column A → `item_name`
- Column B → `class_a_cost`
- Column C → `class_b_cost`
- Column D → `class_c_cost`
- Column E → `unit_type`
- Column F → `notes`
- Category extracted from section headers

---

## API INTEGRATION SPECIFICATIONS

### Python API Structure (FastAPI)

```python
# File: renovation_api.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
import openpyxl
from openpyxl.styles import Font, PatternFill

app = FastAPI()

# ==================== DATA MODELS ====================

class RenovationProjectCreate(BaseModel):
    portfolio_company_id: UUID
    property_name: str
    property_address: str
    total_units: int
    building_class: str
    avg_unit_size_sf: int
    current_monthly_rent: float
    proforma_monthly_rent: float
    exit_cap_rate: float
    noi_margin: float = 0.60
    project_duration_months: int
    units_per_phase: int

class UnitBudget(BaseModel):
    unit_number: str
    unit_type: str
    kitchen_cost: float
    bathroom_cost: float
    flooring_cost: float
    paint_cost: float
    fixtures_cost: float

class RenovationPhase(BaseModel):
    phase_number: int
    phase_start_date: date
    phase_end_date: date
    units_in_phase: int
    phase_renovation_cost: float
    phase_lost_rent: float
    phase_holding_costs: float

class ROIMetrics(BaseModel):
    total_capital_required: float
    annual_noi_increase: float
    property_value_created: float
    roi_percentage: float
    payback_period_years: float

# ==================== ENDPOINTS ====================

@app.post("/api/v1/renovations/projects", status_code=201)
async def create_renovation_project(project: RenovationProjectCreate):
    """
    Create a new renovation project in the database
    Returns: project_id
    """
    # Insert into renovation_projects table
    # Generate Excel file from database
    # Return project_id and Excel download link
    pass

@app.post("/api/v1/renovations/projects/{project_id}/upload-excel")
async def upload_excel_model(project_id: UUID, file: UploadFile = File(...)):
    """
    Upload Excel file and parse into database
    Extracts data from all sheets and populates tables
    """
    # Load Excel with openpyxl
    wb = openpyxl.load_workbook(file.file)
    
    # Extract Inputs sheet
    ws_inputs = wb['Inputs']
    property_data = {
        'property_name': ws_inputs['B2'].value,
        'property_address': ws_inputs['B3'].value,
        'total_units': ws_inputs['B4'].value,
        # ... extract all inputs
    }
    
    # Extract Unit-Level Budget
    ws_units = wb['Unit-Level Budget']
    unit_budgets = []
    for row in range(7, 57):  # Units 1-50
        unit_budgets.append({
            'unit_number': ws_units[f'A{row}'].value,
            'unit_type': ws_units[f'B{row}'].value,
            'kitchen_cost': ws_units[f'C{row}'].value,
            # ... extract all costs
        })
    
    # Insert into database
    # Update renovation_projects, renovation_unit_budgets, renovation_phases
    # Calculate and store ROI metrics
    
    return {"status": "success", "project_id": project_id}

@app.get("/api/v1/renovations/projects/{project_id}/generate-excel")
async def generate_excel_from_database(project_id: UUID):
    """
    Generate Excel file from database records
    Returns: Download link to Excel file
    """
    # Query database for project data
    # Create Excel workbook with openpyxl
    # Populate all sheets with formulas
    # Save to /tmp and return download link
    pass

@app.get("/api/v1/renovations/projects/{project_id}/roi")
async def get_roi_metrics(project_id: UUID):
    """
    Get calculated ROI metrics for a project
    """
    # Query renovation_roi_metrics table
    # Return latest metrics
    pass

@app.put("/api/v1/renovations/projects/{project_id}/units/{unit_number}/actual-costs")
async def update_actual_costs(project_id: UUID, unit_number: str, actual_costs: UnitBudget):
    """
    Update actual costs for variance tracking
    """
    # Update renovation_unit_budgets.actual_* fields
    # Recalculate variance
    # Update phase actuals
    pass

@app.get("/api/v1/renovations/portfolio/{fund_id}/summary")
async def get_portfolio_renovation_summary(fund_id: UUID):
    """
    Get aggregated renovation metrics across all properties in a fund
    """
    # Join renovation_projects with portfolio_companies
    # Aggregate total_budget, value_created, roi across all projects
    # Return portfolio-level summary
    pass

@app.get("/api/v1/renovations/cost-database")
async def get_cost_database(category: Optional[str] = None, building_class: Optional[str] = None):
    """
    Get renovation cost reference data
    """
    # Query renovation_cost_database
    # Filter by category and/or building_class if provided
    # Return pricing data
    pass

# ==================== EXCEL GENERATION ====================

def create_excel_from_database(project_data: dict, unit_budgets: list, phases: list):
    """
    Generate Value-Add Renovation Excel file from database records
    """
    wb = openpyxl.Workbook()
    
    # Create Inputs sheet
    ws_inputs = wb.create_sheet('Inputs', 0)
    ws_inputs['B2'] = project_data['property_name']
    ws_inputs['B3'] = project_data['property_address']
    ws_inputs['B4'] = project_data['total_units']
    # ... populate all inputs
    
    # Create Unit-Level Budget sheet
    ws_units = wb.create_sheet('Unit-Level Budget', 3)
    for idx, unit in enumerate(unit_budgets, start=7):
        ws_units[f'A{idx}'] = unit['unit_number']
        ws_units[f'B{idx}'] = unit['unit_type']
        ws_units[f'C{idx}'] = unit['kitchen_cost']
        # ... populate all unit data
        
        # Add formulas
        ws_units[f'H{idx}'] = f'=SUM(C{idx}:G{idx})'
    
    # Add formatting
    blue_font = Font(color='0000FF')
    for cell in ws_inputs['B2:B26']:
        cell[0].font = blue_font
    
    # Save workbook
    filename = f"/tmp/renovation_{project_data['project_id']}.xlsx"
    wb.save(filename)
    return filename

# ==================== PDF EXTRACTION ====================

@app.post("/api/v1/renovations/projects/{project_id}/upload-contractor-bid")
async def upload_contractor_bid_pdf(project_id: UUID, file: UploadFile = File(...)):
    """
    Extract line items from contractor bid PDF
    Use GPT-4 Vision or pdfplumber to parse costs
    Automatically populate unit budget or cost database
    """
    # Save PDF
    # Extract text/tables with pdfplumber
    # Use GPT-4 to parse line items
    # Map to cost categories
    # Update renovation_unit_budgets or suggest costs
    pass
```

---

## DATA FLOW ARCHITECTURE

### Flow 1: Create New Renovation Project

```
1. User clicks "New Renovation Project" in Portfolio Dashboard UI
2. Form with property details → POST /api/v1/renovations/projects
3. API creates record in renovation_projects table
4. API generates blank Excel template with property info pre-filled
5. User downloads Excel → "Download_Maple_Gardens_Renovation.xlsx"
6. User fills in unit budgets, costs, timeline
7. User uploads completed Excel → POST /api/v1/renovations/projects/{id}/upload-excel
8. API parses Excel → Populates renovation_unit_budgets, renovation_phases tables
9. API calculates ROI → Stores in renovation_roi_metrics
10. Dashboard updates with project summary
```

### Flow 2: Update Actual Costs (Variance Tracking)

```
1. Property manager updates unit status to "Complete"
2. PM enters actual costs via UI or mobile app
3. PUT /api/v1/renovations/projects/{id}/units/{unit#}/actual-costs
4. API updates actual_* fields in renovation_unit_budgets
5. API recalculates variance (Actual - Budget)
6. Dashboard shows red/green variance indicators
7. Phase summary updates with actual costs
8. Portfolio-level reports reflect updated actuals
```

### Flow 3: Portfolio-Level Reporting

```
1. LP requests quarterly renovation ROI report
2. User navigates to Portfolio Dashboard → "Renovation Summary"
3. GET /api/v1/renovations/portfolio/{fund_id}/summary
4. API aggregates across all renovation_projects for fund
5. Returns:
   - Total capital deployed: $15.2M
   - Total value created: $28.5M
   - Blended ROI: 87.5%
   - Number of properties: 8
   - Units renovated: 420
6. Dashboard generates PDF report for LP
```

---

## AUTOMATED IMPORT/EXPORT

### Excel → Database (Import)

```python
def import_excel_to_database(excel_file_path: str, project_id: UUID):
    """
    Parse Excel file and populate database tables
    """
    wb = openpyxl.load_workbook(excel_file_path)
    
    # 1. Extract Inputs Sheet
    ws_inputs = wb['Inputs']
    project_update = {
        'property_name': ws_inputs['B2'].value,
        'total_units': ws_inputs['B4'].value,
        'current_monthly_rent': ws_inputs['B10'].value,
        # ... all inputs
    }
    # UPDATE renovation_projects WHERE project_id = project_id
    
    # 2. Extract Unit-Level Budget
    ws_units = wb['Unit-Level Budget']
    for row in range(7, ws_units.max_row):
        if ws_units[f'A{row}'].value:  # Has unit number
            unit_budget = {
                'project_id': project_id,
                'unit_number': ws_units[f'A{row}'].value,
                'unit_type': ws_units[f'B{row}'].value,
                'kitchen_cost': ws_units[f'C{row}'].value,
                'bathroom_cost': ws_units[f'D{row}'].value,
                'flooring_cost': ws_units[f'E{row}'].value,
                'paint_cost': ws_units[f'F{row}'].value,
                'fixtures_cost': ws_units[f'G{row}'].value,
                'phase_number': ws_units[f'I{row}'].value,
                'renovation_status': ws_units[f'K{row}'].value,
            }
            # INSERT INTO renovation_unit_budgets
    
    # 3. Extract Renovation Phasing
    ws_phasing = wb['Renovation Phasing']
    for row in range(14, 19):  # 5 phases
        phase = {
            'project_id': project_id,
            'phase_number': ws_phasing[f'A{row}'].value,
            'phase_start_date': ws_phasing[f'B{row}'].value,
            'phase_end_date': ws_phasing[f'C{row}'].value,
            'units_in_phase': ws_phasing[f'D{row}'].value,
            'phase_renovation_cost': ws_phasing[f'E{row}'].value,
            'phase_lost_rent': ws_phasing[f'F{row}'].value,
            'phase_holding_costs': ws_phasing[f'G{row}'].value,
        }
        # INSERT INTO renovation_phases
    
    # 4. Extract ROI Metrics
    ws_roi = wb['ROI Calculator']
    roi_metrics = {
        'project_id': project_id,
        'total_capital_required': ws_roi['B10'].value,
        'annual_noi_increase': ws_roi['B30'].value,
        'property_value_created': ws_roi['B33'].value,
        'roi_percentage': ws_roi['B47'].value,
        # ... all metrics
    }
    # INSERT INTO renovation_roi_metrics
    
    return {"status": "success", "units_imported": len(unit_budgets)}
```

### Database → Excel (Export)

```python
def export_database_to_excel(project_id: UUID) -> str:
    """
    Generate Excel file from database records
    Recreate all sheets with formulas intact
    """
    # Query database
    project = db.query(RenovationProject).filter_by(project_id=project_id).first()
    units = db.query(RenovationUnitBudget).filter_by(project_id=project_id).all()
    phases = db.query(RenovationPhase).filter_by(project_id=project_id).all()
    
    # Create workbook
    wb = openpyxl.Workbook()
    
    # Populate Inputs sheet (with BLUE font for inputs)
    ws_inputs = wb.create_sheet('Inputs', 0)
    ws_inputs['B2'] = project.property_name
    ws_inputs['B2'].font = Font(color='0000FF')
    # ... all inputs with blue font
    
    # Populate Unit-Level Budget with formulas
    ws_units = wb.create_sheet('Unit-Level Budget', 3)
    for idx, unit in enumerate(units, start=7):
        ws_units[f'A{idx}'] = unit.unit_number
        ws_units[f'C{idx}'] = unit.kitchen_cost
        ws_units[f'C{idx}'].font = Font(color='0000FF')
        # ... all costs
        
        # Add formulas (not hardcoded values)
        ws_units[f'H{idx}'] = f'=SUM(C{idx}:G{idx})'
        ws_units[f'I{idx}'] = f'=ROUNDUP(A{idx}/Inputs!$B$20,0)'
    
    # Save and return path
    filename = f"/tmp/renovation_export_{project_id}.xlsx"
    wb.save(filename)
    return filename
```

---

## REAL-TIME SYNCHRONIZATION

### Option 1: Webhook-Based Sync

```python
@app.post("/api/v1/renovations/projects/{project_id}/sync")
async def sync_excel_changes(project_id: UUID):
    """
    Detect changes in Excel file and sync to database
    Called when user clicks "Sync to Database" button in UI
    """
    # Compare Excel file timestamp with last_synced_at in database
    # Parse Excel → Identify changed cells
    # Update only changed records in database
    # Return sync summary (10 units updated, 2 phases modified)
    pass
```

### Option 2: File Watching (Advanced)

```python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ExcelFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.xlsx'):
            # File was modified
            project_id = extract_project_id_from_filename(event.src_path)
            import_excel_to_database(event.src_path, project_id)
            print(f"Synced changes for project {project_id}")

# Monitor /shared/renovation_models directory
observer = Observer()
observer.schedule(ExcelFileHandler(), path='/shared/renovation_models', recursive=False)
observer.start()
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: Core Database Integration (Month 1)

**Week 1-2**:
- Create database tables (renovation_projects, renovation_unit_budgets, renovation_phases, renovation_roi_metrics)
- Write SQL migrations
- Set up foreign key relationships with portfolio_companies

**Week 3-4**:
- Build Python API endpoints (POST create, GET retrieve, PUT update)
- Implement Excel → Database import function
- Implement Database → Excel export function
- Unit test all CRUD operations

**Deliverable**: Working API that can store/retrieve renovation projects

---

### Phase 2: Excel Integration (Month 2)

**Week 1-2**:
- Build openpyxl-based Excel generator
- Ensure all formulas are preserved (not hardcoded values)
- Apply color coding (blue inputs, black formulas, green links)
- Test with sample data

**Week 3-4**:
- Build Excel parser for upload functionality
- Handle edge cases (missing data, invalid formulas, extra sheets)
- Implement validation (e.g., total units must match unit count)
- Create UI for upload/download

**Deliverable**: Users can upload/download Excel models via dashboard

---

### Phase 3: Portfolio Reporting (Month 3)

**Week 1-2**:
- Build aggregation queries (portfolio-level ROI, total capital deployed)
- Create summary dashboard page
- Implement drill-down (portfolio → property → unit)

**Week 3-4**:
- Build PDF report generator for LPs
- Create charts (renovation timeline, ROI by property, cost variance)
- Implement email distribution

**Deliverable**: Automated quarterly renovation reports for LPs

---

### Phase 4: Real-Time Sync & Automation (Month 4+)

**Week 1-2**:
- Implement variance tracking (actual vs budget)
- Build mobile app for property managers to update status
- Real-time cost alerts (e.g., "Phase 2 is 15% over budget")

**Week 3-4**:
- PDF contractor bid extraction (GPT-4 Vision or pdfplumber)
- Automated cost database updates
- Integration with accounting system (import actuals)

**Deliverable**: Fully automated renovation tracking with minimal manual entry

---

## APPENDIX: Sample SQL Queries

### Query 1: Get All Renovation Projects for a Fund

```sql
SELECT 
    rp.project_id,
    rp.property_name,
    pc.company_name,
    rp.total_units,
    rp.total_budget,
    rp.status,
    rm.roi_percentage,
    rm.property_value_created
FROM renovation_projects rp
JOIN portfolio_companies pc ON rp.portfolio_company_id = pc.company_id
JOIN portfolio_funds pf ON pc.fund_id = pf.fund_id
LEFT JOIN renovation_roi_metrics rm ON rp.project_id = rm.project_id
WHERE pf.fund_id = '123e4567-e89b-12d3-a456-426614174000'
ORDER BY rp.created_at DESC;
```

### Query 2: Calculate Portfolio-Wide Renovation ROI

```sql
SELECT 
    COUNT(DISTINCT rp.project_id) as total_projects,
    SUM(rp.total_units) as total_units_renovated,
    SUM(rm.total_capital_required) as total_capital_deployed,
    SUM(rm.property_value_created) as total_value_created,
    SUM(rm.net_gain) as total_net_gain,
    AVG(rm.roi_percentage) as avg_roi_percentage,
    AVG(rm.payback_period_years) as avg_payback_years
FROM renovation_projects rp
JOIN portfolio_companies pc ON rp.portfolio_company_id = pc.company_id
JOIN renovation_roi_metrics rm ON rp.project_id = rm.project_id
WHERE pc.fund_id = '123e4567-e89b-12d3-a456-426614174000'
AND rp.status IN ('In Progress', 'Complete');
```

### Query 3: Get Renovation Pipeline by Phase

```sql
SELECT 
    rp.property_name,
    ph.phase_number,
    ph.phase_status,
    ph.phase_start_date,
    ph.units_in_phase,
    ph.phase_renovation_cost,
    ph.actual_renovation_cost,
    (ph.actual_renovation_cost - ph.phase_renovation_cost) as variance,
    CASE 
        WHEN ph.actual_renovation_cost > ph.phase_renovation_cost * 1.10 THEN 'Over Budget'
        WHEN ph.actual_renovation_cost < ph.phase_renovation_cost * 0.95 THEN 'Under Budget'
        ELSE 'On Track'
    END as budget_status
FROM renovation_phases ph
JOIN renovation_projects rp ON ph.project_id = rp.project_id
WHERE rp.status = 'In Progress'
ORDER BY ph.phase_start_date ASC;
```

---

**Document Version**: 1.0  
**Last Updated**: November 2025  
**Integration Status**: Ready for Implementation  
**Contact**: See Portfolio Dashboard technical documentation

---

## 🚀 NEXT STEPS FOR DEVELOPERS

1. **Review database schema** - Ensure compatibility with existing portfolio_companies structure
2. **Set up Python FastAPI environment** - Install openpyxl, psycopg2, pydantic
3. **Create database tables** - Run SQL migrations in PostgreSQL
4. **Build core API endpoints** - Start with POST /projects and GET /projects/{id}
5. **Test Excel generation** - Verify formulas are preserved, not hardcoded
6. **Build upload parser** - Handle Excel file upload and parsing
7. **Create dashboard UI** - Add "Renovations" section to Portfolio Dashboard
8. **Test end-to-end** - Upload → Database → Download → Verify integrity

**Questions?** Refer to Portfolio Dashboard main documentation or contact the development team.
