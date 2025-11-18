---
name: Real Estate Dashboard Code Quality
description: Ensures code follows best practices for this FastAPI/React TypeScript real estate project, including type safety, API design, and financial accuracy
---

# Real Estate Dashboard Code Quality Skill

This skill ensures all code written for the real estate dashboard follows project-specific best practices, maintains consistency, and meets quality standards.

## When to Use This Skill

Invoke this skill when:
- Writing new features or components
- Reviewing or refactoring existing code
- Before committing changes
- When adding new API endpoints
- Creating new financial calculation models

## Code Quality Standards

### Backend (FastAPI/Python)

#### 1. API Endpoint Design
```python
# ✅ GOOD - Clear naming, proper response models, error handling
@router.post("/properties", response_model=PropertyResponse, status_code=201)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
) -> PropertyResponse:
    """Create a new property with comprehensive validation."""
    try:
        # Validate financial inputs
        if property_data.purchase_price <= 0:
            raise HTTPException(400, "Purchase price must be positive")

        property_obj = Property(**property_data.dict())
        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)
        return property_obj
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(409, f"Property already exists: {str(e)}")

# ❌ BAD - Generic naming, no error handling, no validation
@router.post("/add")
async def add_thing(data: dict):
    return data
```

#### 2. Pydantic Models - Comprehensive Validation
```python
# ✅ GOOD - Field validation, descriptive fields, examples
class PropertyCreate(BaseModel):
    address: str = Field(..., min_length=5, max_length=200, description="Property address")
    purchase_price: Decimal = Field(..., gt=0, description="Purchase price in dollars")
    units: int = Field(..., ge=1, le=1000, description="Number of units")
    monthly_rent: Decimal = Field(..., ge=0, description="Monthly rental income")

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Main St, City, ST 12345",
                "purchase_price": 500000,
                "units": 4,
                "monthly_rent": 3000
            }
        }

    @validator('monthly_rent')
    def validate_rent_to_price_ratio(cls, v, values):
        """Ensure monthly rent is reasonable relative to purchase price."""
        if 'purchase_price' in values:
            annual_rent = v * 12
            ratio = annual_rent / values['purchase_price']
            if ratio < 0.01 or ratio > 0.3:
                raise ValueError(f"Rent-to-price ratio {ratio:.2%} is unrealistic")
        return v

# ❌ BAD - No validation, vague fields
class Property(BaseModel):
    data: dict
```

#### 3. Financial Calculations - Accuracy & Documentation
```python
# ✅ GOOD - Clear formulas, documented assumptions, proper types
def calculate_irr(
    initial_investment: Decimal,
    cash_flows: List[Decimal],
    holding_period_years: int
) -> Decimal:
    """
    Calculate Internal Rate of Return using Newton-Raphson method.

    Args:
        initial_investment: Initial cash outlay (negative value expected)
        cash_flows: Annual cash flows during holding period
        holding_period_years: Investment duration in years

    Returns:
        IRR as decimal (0.15 = 15%)

    Formula: NPV = Σ(CF_t / (1 + IRR)^t) = 0
    """
    if len(cash_flows) != holding_period_years:
        raise ValueError("Cash flows must match holding period")

    # Newton-Raphson iteration for IRR
    guess = Decimal('0.1')  # 10% initial guess
    tolerance = Decimal('0.0001')
    max_iterations = 1000

    for i in range(max_iterations):
        npv = initial_investment
        derivative = Decimal(0)

        for t, cf in enumerate(cash_flows, start=1):
            discount_factor = (1 + guess) ** t
            npv += cf / discount_factor
            derivative -= t * cf / (discount_factor * (1 + guess))

        if abs(npv) < tolerance:
            return round(guess, 4)

        if derivative == 0:
            raise ValueError("IRR calculation failed - derivative is zero")

        guess = guess - (npv / derivative)

    raise ValueError("IRR did not converge")

# ❌ BAD - No documentation, unclear logic, no validation
def calc(nums):
    result = 0
    for n in nums:
        result += n / 1.1
    return result
```

#### 4. Database Models - Relationships & Constraints
```python
# ✅ GOOD - Clear relationships, constraints, indexes
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(200), nullable=False, unique=True, index=True)
    purchase_price = Column(Numeric(12, 2), nullable=False)
    purchase_date = Column(Date, nullable=False)
    property_type = Column(Enum(PropertyType), nullable=False, index=True)

    # Relationships with cascade delete
    units = relationship("Unit", back_populates="property", cascade="all, delete-orphan")
    leases = relationship("Lease", back_populates="property", cascade="all, delete-orphan")
    maintenance = relationship("Maintenance", back_populates="property")

    # Constraints
    __table_args__ = (
        CheckConstraint('purchase_price > 0', name='positive_price'),
        Index('idx_property_location', 'city', 'state'),
    )

    def calculate_noi(self, year: int) -> Decimal:
        """Calculate Net Operating Income for specified year."""
        income = sum(lease.annual_rent for lease in self.active_leases(year))
        expenses = sum(m.cost for m in self.expenses(year))
        return income - expenses

# ❌ BAD - No constraints, unclear relationships
class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    data = Column(JSON)
```

### Frontend (React/TypeScript)

#### 5. TypeScript - Strict Typing
```typescript
// ✅ GOOD - Proper interfaces, no 'any', comprehensive types
interface PropertyFormData {
  address: string;
  purchasePrice: number;
  units: number;
  monthlyRent: number;
  propertyType: 'single_family' | 'multifamily' | 'mixed_use';
}

interface CalculationResult {
  irr: number;
  cashOnCashReturn: number;
  capRate: number;
  noi: number;
  errors?: string[];
}

const calculateMetrics = (property: PropertyFormData): CalculationResult => {
  const annualRent = property.monthlyRent * 12;
  const capRate = (annualRent / property.purchasePrice) * 100;

  return {
    irr: 0, // Placeholder for complex calculation
    cashOnCashReturn: 0,
    capRate: parseFloat(capRate.toFixed(2)),
    noi: annualRent
  };
};

// ❌ BAD - Using 'any', unclear types
const calc = (data: any): any => {
  return data.price * 0.1;
};
```

#### 6. React Components - Clean & Reusable
```typescript
// ✅ GOOD - Proper props interface, error handling, loading states
interface PropertyCardProps {
  property: Property;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
  loading?: boolean;
}

export const PropertyCard: React.FC<PropertyCardProps> = ({
  property,
  onEdit,
  onDelete,
  loading = false
}) => {
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    try {
      await api.deleteProperty(property.id);
      onDelete?.(property.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed');
    }
  };

  return (
    <Card>
      <CardContent>
        {error && <Alert severity="error">{error}</Alert>}
        {loading ? (
          <Skeleton variant="rectangular" height={200} />
        ) : (
          <>
            <Typography variant="h6">{property.address}</Typography>
            <Typography>Price: ${property.purchasePrice.toLocaleString()}</Typography>
            <Typography>Cap Rate: {property.capRate}%</Typography>
          </>
        )}
      </CardContent>
      {!loading && (
        <CardActions>
          {onEdit && <Button onClick={() => onEdit(property.id)}>Edit</Button>}
          {onDelete && <Button onClick={handleDelete} color="error">Delete</Button>}
        </CardActions>
      )}
    </Card>
  );
};

// ❌ BAD - No types, no error handling
export const Card = (props) => {
  return <div onClick={props.onClick}>{props.data.name}</div>;
};
```

#### 7. API Integration - Error Handling & Types
```typescript
// ✅ GOOD - Typed responses, comprehensive error handling, retries
interface ApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

class RealEstateApi {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: { 'Content-Type': 'application/json' }
    });

    this.client.interceptors.response.use(
      response => response,
      this.handleError
    );
  }

  private handleError = (error: AxiosError<ApiError>): Promise<never> => {
    if (error.response) {
      // Server responded with error
      const apiError: ApiError = error.response.data;
      throw new Error(`API Error: ${apiError.message} (${apiError.code})`);
    } else if (error.request) {
      // Request made but no response
      throw new Error('Network error - please check your connection');
    } else {
      throw new Error(`Request failed: ${error.message}`);
    }
  };

  async getProperty(id: number): Promise<Property> {
    const response = await this.client.get<Property>(`/properties/${id}`);
    return response.data;
  }

  async calculateIRR(data: IRRInput): Promise<IRRResult> {
    try {
      const response = await this.client.post<IRRResult>('/calculate/irr', data);
      return response.data;
    } catch (error) {
      console.error('IRR calculation failed:', error);
      throw error;
    }
  }
}

// ❌ BAD - No error handling, no types
const getData = async (id) => {
  const res = await axios.get(`/api/${id}`);
  return res.data;
};
```

## Real Estate Domain-Specific Standards

### 8. Financial Formulas - Must Use Industry Standards
```python
# ✅ CORRECT Real Estate Formulas

# Cap Rate = NOI / Purchase Price
cap_rate = (noi / purchase_price) * 100

# Cash-on-Cash Return = Annual Pre-Tax Cash Flow / Total Cash Invested
cash_on_cash = (annual_cash_flow / cash_invested) * 100

# Debt Service Coverage Ratio = NOI / Annual Debt Service
dscr = noi / annual_debt_service

# Gross Rent Multiplier = Purchase Price / Gross Annual Rent
grm = purchase_price / gross_annual_rent

# 1% Rule - Monthly rent should be ≥ 1% of purchase price
meets_one_percent_rule = monthly_rent >= (purchase_price * 0.01)

# ❌ WRONG - Do not invent custom formulas
fake_metric = (rent * price) / units  # No real estate meaning
```

### 9. Naming Conventions
```python
# ✅ Use standard real estate terminology
noi = calculate_net_operating_income()
capex = estimate_capital_expenditures()
opex = calculate_operating_expenses()
dscr = debt_service_coverage_ratio()
ltv = loan_to_value_ratio()

# ❌ Don't use unclear abbreviations
nip = calc_stuff()  # What is 'nip'?
val = get_val()     # Too vague
```

## Code Review Checklist

Before committing code, verify:

### Backend Checklist
- [ ] All endpoints have proper type hints and response models
- [ ] Input validation with Pydantic models and custom validators
- [ ] Database queries use proper SQLAlchemy patterns (no raw SQL without parameterization)
- [ ] Financial calculations are documented with formulas
- [ ] Error handling for all database operations with rollback
- [ ] API endpoints return appropriate HTTP status codes
- [ ] No sensitive data in logs or error messages

### Frontend Checklist
- [ ] No `any` types (use `unknown` if type is truly unknown, then narrow)
- [ ] Props interfaces defined for all components
- [ ] Loading and error states handled
- [ ] API calls wrapped in try/catch
- [ ] Forms have validation
- [ ] Numbers formatted with proper decimals and thousand separators
- [ ] Accessibility: proper labels, ARIA attributes, keyboard navigation

### Real Estate Domain Checklist
- [ ] Financial calculations match industry standards
- [ ] Currency values use appropriate precision (2 decimals)
- [ ] Percentages clearly indicated (15% or 0.15 - be consistent)
- [ ] Dates handled properly (timezone-aware where needed)
- [ ] Edge cases handled (zero values, negative returns, etc.)

## Common Anti-Patterns to Avoid

### 1. Magic Numbers
```python
# ❌ BAD
monthly_payment = principal * 0.00417

# ✅ GOOD
MONTHLY_INTEREST_RATE = annual_rate / 12
monthly_payment = principal * MONTHLY_INTEREST_RATE
```

### 2. Silent Failures
```python
# ❌ BAD
def get_property(id):
    try:
        return db.query(Property).filter(Property.id == id).first()
    except:
        return None

# ✅ GOOD
def get_property(id: int) -> Property:
    try:
        property = db.query(Property).filter(Property.id == id).first()
        if not property:
            raise HTTPException(404, f"Property {id} not found")
        return property
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching property {id}: {e}")
        raise HTTPException(500, "Database error")
```

### 3. Inconsistent State Management
```typescript
// ❌ BAD - Multiple sources of truth
const [property, setProperty] = useState<Property | null>(null);
const [propertyCache, setPropertyCache] = useState<Property | null>(null);

// ✅ GOOD - Single source of truth
const [property, setProperty] = useState<Property | null>(null);
```

## Testing Requirements

All new code should include:

### Backend Tests
```python
# Test financial calculations
def test_calculate_irr_positive_returns():
    result = calculate_irr(-100000, [10000, 10000, 120000], 3)
    assert 0.08 <= result <= 0.12  # Reasonable IRR range

def test_calculate_irr_invalid_input():
    with pytest.raises(ValueError):
        calculate_irr(-100000, [10000], 3)  # Mismatched periods
```

### Frontend Tests
```typescript
// Test component rendering and interactions
describe('PropertyCard', () => {
  it('displays property information correctly', () => {
    const property = { address: '123 Main St', purchasePrice: 500000 };
    render(<PropertyCard property={property} />);
    expect(screen.getByText('123 Main St')).toBeInTheDocument();
    expect(screen.getByText(/\$500,000/)).toBeInTheDocument();
  });
});
```

## Performance Guidelines

### Database Queries
- Use `select_related()` and `prefetch_related()` to avoid N+1 queries
- Add indexes on frequently queried fields
- Limit result sets with pagination

### Frontend
- Memoize expensive calculations with `useMemo`
- Debounce input handlers for search/filter
- Lazy load components and routes
- Optimize re-renders with `React.memo` for expensive components

## Documentation Standards

Every new feature must include:
1. **Docstrings** - All functions and classes (Google style for Python)
2. **Type hints** - All function signatures
3. **Examples** - In docstrings for complex calculations
4. **Comments** - For non-obvious business logic only
5. **README updates** - If adding new models or major features

## Execution Instructions

When this skill is invoked:

1. **Before writing code**: Review these standards and confirm approach
2. **During coding**: Apply patterns and conventions consistently
3. **Before completion**: Run through relevant checklist items
4. **On completion**: Suggest tests to add for the new code

Always prioritize:
- Type safety over flexibility
- Explicit over implicit
- Documented over clever
- Tested over "it works on my machine"
