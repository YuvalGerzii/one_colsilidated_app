# CALCULATOR ROUTING DETAILS - CODE REFERENCES

## FRONTEND APP.tsx Routes

**File:** `/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/frontend/src/App.tsx`

### Calculator Route Imports (Lines 20-31)
```typescript
import { FixAndFlipPage } from './pages/RealEstate/FixAndFlipPage';
import { SingleFamilyRentalPage } from './pages/RealEstate/SingleFamilyRentalPage';
import { SmallMultifamilyPage } from './pages/RealEstate/SmallMultifamilyPage';
import { ExtendedMultifamilyPage } from './pages/RealEstate/ExtendedMultifamilyPage';
import { HotelPage } from './pages/RealEstate/HotelPage';
import { MixedUsePage } from './pages/RealEstate/MixedUsePage';
import { SubdivisionPage } from './pages/RealEstate/SubdivisionPage';
import { SmallMultifamilyAcquisitionPage } from './pages/RealEstate/SmallMultifamilyAcquisitionPage';
import { LeaseAnalyzerPage } from './pages/RealEstate/LeaseAnalyzerPage';
import { RenovationBudgetPage } from './pages/RealEstate/RenovationBudgetPage';
import { TaxStrategyPage } from './pages/RealEstate/TaxStrategyPage';
```

### Calculator Routes in Router (Lines 155-166)
```typescript
<Route path="/real-estate-models/fix-and-flip" element={<FixAndFlipPage />} />
<Route path="/real-estate-models/single-family-rental" element={<SingleFamilyRentalPage />} />
<Route path="/real-estate-models/small-multifamily" element={<SmallMultifamilyPage />} />
<Route path="/real-estate-models/extended-multifamily" element={<ExtendedMultifamilyPage />} />
<Route path="/real-estate-models/hotel" element={<HotelPage />} />
<Route path="/real-estate-models/mixed-use" element={<MixedUsePage />} />
<Route path="/real-estate-models/subdivision" element={<SubdivisionPage />} />
<Route path="/real-estate-models/small-multifamily-acquisition" element={<SmallMultifamilyAcquisitionPage />} />
<Route path="/real-estate-models/lease-analyzer" element={<LeaseAnalyzerPage />} />
<Route path="/real-estate-models/renovation-budget" element={<RenovationBudgetPage />} />
<Route path="/real-estate-models/tax-strategy" element={<TaxStrategyPage />} />
```

---

## BACKEND MODEL_REGISTRY

**File:** `/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/backend/app/api/v1/endpoints/real_estate_tools.py`

### KEY Registry Entries (Lines 154-290)

```python
MODEL_REGISTRY = {
    "fix_and_flip": {
        "label": "Fix & Flip",
        "defaults": FIX_DEFAULTS,
        "fields": FIX_FIELDS,
        "prepare": fix_prepare_inputs,
        "db_model": FixAndFlipModel,
    },
    "single_family_rental": {
        "label": "Single-Family Rental",
        "defaults": SFR_DEFAULTS,
        "fields": SFR_FIELDS,
        "prepare": sfr_prepare_inputs,
        "db_model": SingleFamilyRentalModel,
    },
    # ... [continues for all models]
    "tax_strategy": {
        "label": "Tax Strategy Integration",
        "defaults": TAX_DEFAULTS,
        "fields": TAX_FIELDS,
        "prepare": tax_prepare_inputs,
        "db_model": TaxStrategyModel,
    },
    # MISSING: "small_multifamily_acquisition" entry
}
```

### Required Imports for Missing Calculator (Lines 29-108)

Missing imports that would be needed:

```python
# NOT PRESENT - Would need to add:
from app.scripts.real_estate.small_multifamily_acquisition_cli import (
    DEFAULT_INPUTS as SMALL_MULTI_ACQ_DEFAULTS,
    FORM_FIELDS as SMALL_MULTI_ACQ_FIELDS,
    build_chart_specs as small_multi_acq_chart_specs,
    build_projection as small_multi_acq_build_projection,
    build_report_tables as small_multi_acq_tables,
    prepare_inputs as small_multi_acq_prepare_inputs,
)
```

### POST Endpoint for Calculations (Line ~373)

```python
@router.post("/tools/run")
async def run_model(payload: RunModelRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Run a real estate calculator model
    
    Parameters:
    - payload.model: must be a key in MODEL_REGISTRY
    
    Currently supports:
    - "fix_and_flip"
    - "single_family_rental"
    - "small_multifamily"
    - "extended_multifamily"
    - "hotel"
    - "mixed_use"
    - "lease_analyzer"
    - "renovation_budget"
    - "subdivision"
    - "tax_strategy"
    
    Missing:
    - "small_multifamily_acquisition"  ← WOULD RETURN 404 ERROR
    """
    if payload.model not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Model {payload.model} not found")
```

---

## DATABASE MODELS

**File:** `/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/backend/app/models/real_estate.py`

### Existing Models (Base class at top)

```python
class RealEstateModelBase(Base, UUIDMixin, TimestampMixin):
    """Common columns shared by all real estate model records."""
    __abstract__ = True
    # Common fields...
```

### Models Defined (11 total)
```python
✓ class FixAndFlipModel(RealEstateModelBase):
    __tablename__ = "fix_and_flip_models"

✓ class SingleFamilyRentalModel(RealEstateModelBase):
    __tablename__ = "single_family_rental_models"

✓ class SmallMultifamilyModel(RealEstateModelBase):
    __tablename__ = "small_multifamily_models"

✓ class HighRiseMultifamilyModel(RealEstateModelBase):
    __tablename__ = "high_rise_multifamily_models"

✓ class HotelFinancialModel(RealEstateModelBase):
    __tablename__ = "hotel_financial_models"

✓ class MixedUseDevelopmentModel(RealEstateModelBase):
    __tablename__ = "mixed_use_development_models"

✓ class LeaseAnalyzerModel(RealEstateModelBase):
    __tablename__ = "lease_analyzer_models"

✓ class RenovationBudgetModel(RealEstateModelBase):
    __tablename__ = "renovation_budget_models"

✓ class SubdivisionModel(RealEstateModelBase):
    __tablename__ = "subdivision_models"

✓ class TaxStrategyModel(RealEstateModelBase):
    __tablename__ = "tax_strategy_models"

✓ class PortfolioModel(RealEstateModelBase):
    __tablename__ = "portfolio_models"

✗ SmallMultifamilyAcquisitionModel - NOT DEFINED
```

### Missing Model Template

Would need to add:
```python
class SmallMultifamilyAcquisitionModel(RealEstateModelBase):
    """Small multifamily acquisition analysis model snapshot."""

    __tablename__ = "small_multifamily_acquisition_models"

    property_type = Column(String(100), nullable=True, comment="Property type (Quadplex, Triplex, etc.)")
    num_units = Column(Integer, nullable=True, comment="Number of units in the property")
    conversion_allowed = Column(Boolean, nullable=True, comment="Whether conversion is allowed by local zoning")
```

---

## FRONTEND SERVICE LAYER

**File:** `/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/frontend/src/services/calculatorService.ts`

### CalculationType Enum (Lines ~5-12)

```typescript
export enum CalculationType {
  FIX_AND_FLIP = 'fix_and_flip',
  SINGLE_FAMILY_RENTAL = 'single_family_rental',
  SMALL_MULTIFAMILY = 'small_multifamily',
  HIGH_RISE_MULTIFAMILY = 'high_rise_multifamily',
  HOTEL_FINANCIAL = 'hotel_financial',
  MIXED_USE_DEVELOPMENT = 'mixed_use_development',
  LEASE_ANALYZER = 'lease_analyzer',
  RENOVATION_BUDGET = 'renovation_budget',
  // MISSING:
  // SUBDIVISION = 'subdivision',
  // TAX_STRATEGY = 'tax_strategy',
  // SMALL_MULTIFAMILY_ACQUISITION = 'small_multifamily_acquisition',
}
```

### Missing Helper Methods

Need to add to CalculatorService class:
```typescript
// Would need methods like:
async saveSubdivision(propertyName: string, ...): Promise<SavedCalculation> {
  return this.saveCalculation({
    calculation_type: CalculationType.SUBDIVISION,  // ← enum doesn't exist yet
    property_name: propertyName,
    // ...
  });
}

async getSubdivisionCalculations(): Promise<SavedCalculation[]> {
  return this.listCalculations({
    calculation_type: CalculationType.SUBDIVISION,  // ← enum doesn't exist yet
  });
}
```

---

## FRONTEND MODEL CONFIG

**File:** `/Users/yuvalgerzi/Documents/personal projects/real_estate_dashboard/frontend/src/config/modelConfig.ts`

### MODEL_CONFIGS Object (Lines ~35-...)

Currently has 8 entries:
```typescript
export const MODEL_CONFIGS: Record<string, ModelConfig> = {
  ✓ fix_and_flip: { ... },
  ✓ single_family_rental: { ... },
  ✓ small_multifamily: { ... },
  ✓ extended_multifamily: { ... },
  ✓ hotel: { ... },
  ✓ mixed_use: { ... },
  ✓ lease_analyzer: { ... },
  ✓ renovation_budget: { ... },
  // MISSING 3:
  // subdivision: { ... },
  // tax_strategy: { ... },
  // small_multifamily_acquisition: { ... },
};
```

### Missing Config Template

Would need entries like:
```typescript
subdivision: {
  id: 'subdivision',
  label: 'Subdivision / Condo Conversion',
  icon: LandscapeIcon,
  path: '/real-estate-models/subdivision',
  color: '#84cc16',
  category: 'tools',
  description: 'Analyze multi-unit subdivision and condo conversion opportunities...',
  quickStartGuide: `...`,
  keyMetrics: [
    { name: 'IRR', target: '18-25%', formula: 'Internal Rate of Return' },
    // ...
  ],
},
```

---

## ROUTING FLOW EXAMPLES

### Complete Flow (Fix & Flip)

```
1. User navigates to /real-estate-models/fix-and-flip
   ↓
2. App.tsx matches route:
   <Route path="/real-estate-models/fix-and-flip" element={<FixAndFlipPage />} />
   ↓
3. FixAndFlipPage.tsx renders:
   export const FixAndFlipPage: React.FC = () => {
     return <FixFlipCalculator />;
   };
   ↓
4. FixFlipCalculator.tsx full implementation with UI
   ↓
5. User clicks "Save" button
   ↓
6. Calls: calculatorService.saveFixAndFlip(name, inputs, outputs)
   ↓
7. Service calls: api.post('/calculations/', {
      calculation_type: CalculationType.FIX_AND_FLIP,
      property_name: name,
      input_data: inputs,
      output_data: outputs,
   })
   ↓
8. API received at backend /calculations/ endpoint
   ↓
9. Data saved to fix_and_flip_models table
   ✓ COMPLETE
```

### Broken Flow (SmallMultifamilyAcquisition)

```
1. User navigates to /real-estate-models/small-multifamily-acquisition
   ↓
2. App.tsx matches route:
   <Route path="/real-estate-models/small-multifamily-acquisition" element={<SmallMultifamilyAcquisitionPage />} />
   ✓ Route exists
   ↓
3. SmallMultifamilyAcquisitionPage.tsx renders:
   export const SmallMultifamilyAcquisitionPage: React.FC = () => {
     return <SmallMultifamilyAcquisitionCalculator />;
   };
   ✓ Page exists
   ↓
4. SmallMultifamilyAcquisitionCalculator.tsx full implementation
   ✓ Component exists and works
   ↓
5. User clicks "Save" button
   ↓
6. Tries to call: calculatorService.saveSmallMultifamilyAcquisition(...)
   ✗ METHOD DOESN'T EXIST
   
   Alternative: Tries generic save without type
   ↓
7. Service calls: api.post('/calculations/', {
      calculation_type: 'small_multifamily_acquisition',  // String, not typed
      // ...
   })
   ↓
8. API saves with generic handler
   ↓
9. If frontend tries to use /real-estate/tools/run endpoint:
   - Backend checks if "small_multifamily_acquisition" in MODEL_REGISTRY
   ✗ NOT FOUND
   - Returns 404 error
   ✗ BACKEND PROCESSING FAILS
   
10. Data cannot be saved to specific database model
    ✗ PERSISTENCE FAILS
    
Result: ✗ INCOMPLETE - Client-side only, no server processing or persistence
```

---

## SUMMARY TABLE

| Component | Status | File | Details |
|---|---|---|---|
| Routes | ✓ 11/11 | App.tsx | All defined |
| Components | ✓ 11/11 | components/calculators/ | All implemented |
| Pages | ✓ 11/11 | pages/RealEstate/ | All implemented |
| Backend Models | ✗ 10/11 | app/api/v1/endpoints/real_estate_tools.py | Missing SmallMultifamilyAcquisition |
| DB Models | ✗ 10/11 | app/models/real_estate.py | Missing SmallMultifamilyAcquisition |
| Service Types | ✗ 8/11 | services/calculatorService.ts | Missing 3 enums |
| Service Configs | ✗ 8/11 | config/modelConfig.ts | Missing 3 configs |

