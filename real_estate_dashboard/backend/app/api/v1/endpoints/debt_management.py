"""
Debt Management API Endpoints

Provides endpoints for:
- Loan management (CRUD)
- Debt covenant tracking
- Amortization schedules
- DSCR calculations
- Refinancing analysis
- Loan comparison
- Interest rate sensitivity
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field
from decimal import Decimal

from app.core.database import get_db
from app.core.auth import get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.debt_management import (
    Loan, DebtCovenant, AmortizationScheduleEntry, LoanComparison,
    LoanType, LoanStatus, InterestRateType, AmortizationType, CovenantType
)
from app.services.debt_calculations_service import debt_calculations_service

router = APIRouter()


# ====================
# Pydantic Schemas
# ====================

class LoanCreate(BaseModel):
    loan_name: str
    loan_number: Optional[str] = None
    loan_type: LoanType
    status: LoanStatus = LoanStatus.PENDING
    lender_name: str
    lender_contact: Optional[str] = None
    lender_phone: Optional[str] = None
    lender_email: Optional[str] = None
    property_address: Optional[str] = None
    property_value: Optional[float] = None
    original_loan_amount: float
    current_balance: float
    interest_rate: float
    interest_rate_type: InterestRateType
    index_rate: Optional[str] = None
    margin: Optional[float] = None
    rate_floor: Optional[float] = None
    rate_cap: Optional[float] = None
    origination_date: date
    maturity_date: date
    term_months: int
    amortization_type: AmortizationType
    amortization_months: Optional[int] = None
    interest_only_months: Optional[int] = 0
    balloon_payment: Optional[float] = None
    monthly_payment: Optional[float] = None
    payment_frequency: str = "Monthly"
    next_payment_date: Optional[date] = None
    origination_fee: Optional[float] = 0
    closing_costs: Optional[float] = 0
    prepayment_penalty: bool = False
    prepayment_penalty_details: Optional[str] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None


class LoanUpdate(BaseModel):
    loan_name: Optional[str] = None
    status: Optional[LoanStatus] = None
    current_balance: Optional[float] = None
    interest_rate: Optional[float] = None
    next_payment_date: Optional[date] = None
    property_value: Optional[float] = None
    notes: Optional[str] = None


class LoanResponse(BaseModel):
    id: str
    loan_name: str
    loan_number: Optional[str]
    loan_type: str
    status: str
    lender_name: str
    original_loan_amount: float
    current_balance: float
    interest_rate: float
    interest_rate_type: str
    origination_date: date
    maturity_date: date
    term_months: int
    amortization_type: str
    monthly_payment: Optional[float]
    ltv_ratio: Optional[float]
    dscr: Optional[float]
    debt_yield: Optional[float]
    created_at: str

    class Config:
        from_attributes = True


class DebtCovenantCreate(BaseModel):
    loan_id: str
    covenant_type: CovenantType
    covenant_name: str
    required_value: float
    current_value: Optional[float] = None
    measurement_frequency: str = "Quarterly"
    next_measurement_date: Optional[date] = None
    last_measurement_date: Optional[date] = None
    in_compliance: bool = True
    breach_consequences: Optional[str] = None
    notes: Optional[str] = None


class DebtCovenantUpdate(BaseModel):
    current_value: Optional[float] = None
    in_compliance: Optional[bool] = None
    last_measurement_date: Optional[date] = None
    next_measurement_date: Optional[date] = None
    notes: Optional[str] = None


class DebtCovenantResponse(BaseModel):
    id: str
    loan_id: str
    covenant_type: str
    covenant_name: str
    required_value: float
    current_value: Optional[float]
    in_compliance: bool
    measurement_frequency: str
    next_measurement_date: Optional[date]

    class Config:
        from_attributes = True


class AmortizationRequest(BaseModel):
    loan_amount: float
    annual_rate: float
    term_months: int
    start_date: date
    interest_only_months: Optional[int] = 0
    balloon_months: Optional[int] = None


class DSCRCalculationRequest(BaseModel):
    net_operating_income: float
    annual_debt_service: float


class RefinancingAnalysisRequest(BaseModel):
    current_loan: dict
    proposed_loan: dict


class InterestRateSensitivityRequest(BaseModel):
    loan_amount: float
    base_rate: float
    term_months: int
    rate_variations: Optional[List[float]] = None


class LoanComparisonRequest(BaseModel):
    comparison_name: str
    loan_scenarios: List[dict]


# ====================
# Loan Endpoints
# ====================

@router.post("/loans", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan: LoanCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new loan"""
    current_user, company = user_company

    try:
        db_loan = Loan(
            **loan.dict(),
            company_id=company.id if company else None
        )

        # Calculate metrics if property value provided
        if loan.property_value:
            db_loan.ltv_ratio = debt_calculations_service.calculate_ltv(
                Decimal(str(loan.original_loan_amount)),
                Decimal(str(loan.property_value))
            )

        db.add(db_loan)
        db.commit()
        db.refresh(db_loan)

        return db_loan
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create loan: {str(e)}")


@router.get("/loans", response_model=List[LoanResponse])
def get_loans(
    skip: int = 0,
    limit: int = 100,
    status: Optional[LoanStatus] = None,
    loan_type: Optional[LoanType] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get all loans with optional filtering"""
    current_user, company = user_company

    query = db.query(Loan).filter(Loan.deleted_at.is_(None))

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Loan.company_id == company.id)

    if status:
        query = query.filter(Loan.status == status)

    if loan_type:
        query = query.filter(Loan.loan_type == loan_type)

    loans = query.order_by(Loan.created_at.desc()).offset(skip).limit(limit).all()
    return loans


@router.get("/loans/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get a specific loan by ID"""
    current_user, company = user_company

    filters = [Loan.id == loan_id, Loan.deleted_at.is_(None)]

    if company:
        filters.append(Loan.company_id == company.id)

    loan = db.query(Loan).filter(*filters).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.put("/loans/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: str,
    loan_update: LoanUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Update a loan"""
    current_user, company = user_company

    filters = [Loan.id == loan_id, Loan.deleted_at.is_(None)]

    if company:
        filters.append(Loan.company_id == company.id)

    loan = db.query(Loan).filter(*filters).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    try:
        for key, value in loan_update.dict(exclude_unset=True).items():
            setattr(loan, key, value)

        db.commit()
        db.refresh(loan)
        return loan
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update loan: {str(e)}")


@router.delete("/loans/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(
    loan_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Delete a loan (soft delete)"""
    current_user, company = user_company

    filters = [Loan.id == loan_id, Loan.deleted_at.is_(None)]

    if company:
        filters.append(Loan.company_id == company.id)

    loan = db.query(Loan).filter(*filters).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    try:
        from datetime import datetime
        loan.deleted_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete loan: {str(e)}")


# ====================
# Debt Covenant Endpoints
# ====================

@router.post("/covenants", response_model=DebtCovenantResponse, status_code=status.HTTP_201_CREATED)
def create_covenant(
    covenant: DebtCovenantCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new debt covenant"""
    current_user, company = user_company

    # Verify parent loan ownership
    loan_filters = [Loan.id == covenant.loan_id, Loan.deleted_at.is_(None)]
    if company:
        loan_filters.append(Loan.company_id == company.id)

    loan = db.query(Loan).filter(*loan_filters).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    try:
        db_covenant = DebtCovenant(**covenant.dict())
        db.add(db_covenant)
        db.commit()
        db.refresh(db_covenant)
        return db_covenant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create covenant: {str(e)}")


@router.get("/covenants", response_model=List[DebtCovenantResponse])
def get_covenants(
    loan_id: Optional[str] = None,
    in_compliance: Optional[bool] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get all covenants with optional filtering"""
    current_user, company = user_company

    query = db.query(DebtCovenant).filter(DebtCovenant.deleted_at.is_(None))

    # If loan_id is provided, verify ownership
    if loan_id:
        loan_filters = [Loan.id == loan_id, Loan.deleted_at.is_(None)]
        if company:
            loan_filters.append(Loan.company_id == company.id)

        loan = db.query(Loan).filter(*loan_filters).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        query = query.filter(DebtCovenant.loan_id == loan_id)
    elif company:
        # Filter by company through loan relationship
        query = query.join(Loan).filter(Loan.company_id == company.id, Loan.deleted_at.is_(None))

    if in_compliance is not None:
        query = query.filter(DebtCovenant.in_compliance == in_compliance)

    covenants = query.all()
    return covenants


@router.put("/covenants/{covenant_id}", response_model=DebtCovenantResponse)
def update_covenant(
    covenant_id: str,
    covenant_update: DebtCovenantUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Update a covenant"""
    current_user, company = user_company

    covenant = db.query(DebtCovenant).filter(
        DebtCovenant.id == covenant_id,
        DebtCovenant.deleted_at.is_(None)
    ).first()
    if not covenant:
        raise HTTPException(status_code=404, detail="Covenant not found")

    # Verify parent loan ownership
    loan_filters = [Loan.id == covenant.loan_id, Loan.deleted_at.is_(None)]
    if company:
        loan_filters.append(Loan.company_id == company.id)

    loan = db.query(Loan).filter(*loan_filters).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Covenant not found")

    try:
        for key, value in covenant_update.dict(exclude_unset=True).items():
            setattr(covenant, key, value)

        db.commit()
        db.refresh(covenant)
        return covenant
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update covenant: {str(e)}")


# ====================
# Calculation Endpoints
# ====================

@router.post("/calculate/amortization")
def calculate_amortization(request: AmortizationRequest):
    """Generate amortization schedule"""
    try:
        schedule = debt_calculations_service.generate_amortization_schedule(
            loan_amount=Decimal(str(request.loan_amount)),
            annual_rate=Decimal(str(request.annual_rate)),
            term_months=request.term_months,
            start_date=request.start_date,
            interest_only_months=request.interest_only_months or 0,
            balloon_months=request.balloon_months
        )

        return {
            "success": True,
            "schedule": schedule,
            "summary": {
                "total_payments": sum(p["payment_amount"] for p in schedule),
                "total_principal": sum(p["principal_payment"] for p in schedule),
                "total_interest": sum(p["interest_payment"] for p in schedule)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate amortization: {str(e)}")


@router.post("/calculate/dscr")
def calculate_dscr(request: DSCRCalculationRequest):
    """Calculate Debt Service Coverage Ratio"""
    try:
        dscr = debt_calculations_service.calculate_dscr(
            net_operating_income=Decimal(str(request.net_operating_income)),
            annual_debt_service=Decimal(str(request.annual_debt_service))
        )

        if dscr is None:
            raise HTTPException(status_code=400, detail="Cannot calculate DSCR with zero debt service")

        return {
            "success": True,
            "dscr": float(dscr),
            "interpretation": (
                "Strong" if dscr >= Decimal("1.25") else
                "Adequate" if dscr >= Decimal("1.15") else
                "Marginal" if dscr >= Decimal("1.0") else
                "Insufficient"
            )
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate DSCR: {str(e)}")


@router.post("/calculate/refinancing")
def calculate_refinancing(request: RefinancingAnalysisRequest):
    """Analyze refinancing opportunity"""
    try:
        analysis = debt_calculations_service.calculate_refinancing_analysis(
            current_loan=request.current_loan,
            proposed_loan=request.proposed_loan
        )

        return {
            "success": True,
            **analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze refinancing: {str(e)}")


@router.post("/calculate/rate-sensitivity")
def calculate_rate_sensitivity(request: InterestRateSensitivityRequest):
    """Calculate interest rate sensitivity"""
    try:
        rate_variations = None
        if request.rate_variations:
            rate_variations = [Decimal(str(r)) for r in request.rate_variations]

        analysis = debt_calculations_service.calculate_interest_rate_sensitivity(
            loan_amount=Decimal(str(request.loan_amount)),
            base_rate=Decimal(str(request.base_rate)),
            term_months=request.term_months,
            rate_variations=rate_variations
        )

        return {
            "success": True,
            **analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate rate sensitivity: {str(e)}")


@router.post("/compare-loans")
def compare_loans(request: LoanComparisonRequest):
    """Compare multiple loan scenarios"""
    try:
        comparison = debt_calculations_service.compare_loans(
            loan_scenarios=request.loan_scenarios
        )

        return {
            "success": True,
            "comparison_name": request.comparison_name,
            **comparison
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compare loans: {str(e)}")


# ====================
# Loan Summary/Metrics
# ====================

@router.get("/summary")
def get_debt_summary(db: Session = Depends(get_db)):
    """Get debt portfolio summary"""
    try:
        loans = db.query(Loan).filter(
            Loan.deleted_at.is_(None),
            Loan.status == LoanStatus.ACTIVE
        ).all()

        total_debt = sum(float(loan.current_balance) for loan in loans)
        total_monthly_payments = sum(float(loan.monthly_payment or 0) for loan in loans)
        avg_interest_rate = sum(float(loan.interest_rate) for loan in loans) / len(loans) if loans else 0

        # Calculate average DSCR
        dscr_values = [float(loan.dscr) for loan in loans if loan.dscr is not None]
        avg_dscr = sum(dscr_values) / len(dscr_values) if dscr_values else None

        # Count loans by type
        loans_by_type = {}
        for loan in loans:
            loan_type = loan.loan_type.value
            loans_by_type[loan_type] = loans_by_type.get(loan_type, 0) + 1

        # Count loans by maturity
        from datetime import datetime, timedelta
        today = datetime.now().date()
        maturing_soon = sum(1 for loan in loans if loan.maturity_date <= today + timedelta(days=365))

        return {
            "success": True,
            "summary": {
                "total_loans": len(loans),
                "total_debt": total_debt,
                "total_monthly_payments": total_monthly_payments,
                "avg_interest_rate": avg_interest_rate,
                "avg_dscr": avg_dscr,
                "loans_by_type": loans_by_type,
                "maturing_within_year": maturing_soon
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get summary: {str(e)}")
