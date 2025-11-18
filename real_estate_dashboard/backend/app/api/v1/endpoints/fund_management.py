"""
Fund Management API Endpoints

This module provides REST API endpoints for PE/VC fund management including:
- Fund CRUD operations
- LP management
- Capital calls tracking
- Distribution management
- Waterfall calculations
- Fee calculations
- Performance metrics
"""

from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.api.deps import get_db
from app.core.auth import get_current_user_with_company
from app.models.user import User
from app.models.company import Company
from app.models.fund_management import (
    Fund, FundType, FundStatus,
    LimitedPartner,
    FundCommitment,
    CapitalCall, CapitalCallItem, CapitalCallStatus,
    Distribution, DistributionItem, DistributionType,
    PortfolioInvestment
)
from app.services.fund_metrics_service import (
    fund_metrics_service,
    waterfall_calculator,
    performance_tracker
)

router = APIRouter()


# ========================================
# PYDANTIC SCHEMAS
# ========================================

class FundCreate(BaseModel):
    """Schema for creating a fund"""
    name: str = Field(..., description="Fund name")
    fund_number: Optional[str] = Field(None, description="Fund number")
    fund_type: FundType = Field(FundType.PRIVATE_EQUITY, description="Fund type")
    description: Optional[str] = None
    target_size: Decimal = Field(..., description="Target fund size")
    currency: str = Field("USD", description="Currency code")
    vintage_year: Optional[str] = None
    inception_date: Optional[date] = None
    management_fee_rate: Decimal = Field(Decimal("0.02"), description="Management fee rate")
    carried_interest_rate: Decimal = Field(Decimal("0.20"), description="Carried interest rate")
    preferred_return_rate: Decimal = Field(Decimal("0.08"), description="Preferred return rate")


class FundUpdate(BaseModel):
    """Schema for updating a fund"""
    name: Optional[str] = None
    fund_type: Optional[FundType] = None
    status: Optional[FundStatus] = None
    description: Optional[str] = None
    target_size: Optional[Decimal] = None
    management_fee_rate: Optional[Decimal] = None
    carried_interest_rate: Optional[Decimal] = None
    preferred_return_rate: Optional[Decimal] = None


class FundResponse(BaseModel):
    """Schema for fund response"""
    id: str
    name: str
    fund_number: Optional[str]
    fund_type: FundType
    status: FundStatus
    target_size: Decimal
    committed_capital: Decimal
    total_called: Decimal
    total_distributed: Decimal
    nav: Decimal
    irr: Optional[Decimal]
    moic: Optional[Decimal]
    dpi: Optional[Decimal]
    rvpi: Optional[Decimal]
    tvpi: Optional[Decimal]
    management_fee_rate: Decimal
    carried_interest_rate: Decimal
    preferred_return_rate: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class LPCreate(BaseModel):
    """Schema for creating an LP"""
    name: str
    legal_name: Optional[str] = None
    lp_type: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class LPResponse(BaseModel):
    """Schema for LP response"""
    id: str
    name: str
    legal_name: Optional[str]
    lp_type: Optional[str]
    contact_person: Optional[str]
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CommitmentCreate(BaseModel):
    """Schema for creating a fund commitment"""
    fund_id: str
    lp_id: str
    commitment_amount: Decimal
    commitment_date: Optional[date] = None


class CommitmentResponse(BaseModel):
    """Schema for commitment response"""
    id: str
    fund_id: str
    lp_id: str
    commitment_amount: Decimal
    called_amount: Decimal
    distributed_amount: Decimal
    unfunded_commitment: Decimal
    commitment_date: Optional[date]

    class Config:
        from_attributes = True


class CapitalCallCreate(BaseModel):
    """Schema for creating a capital call"""
    fund_id: str
    call_number: Optional[str] = None
    call_date: date
    due_date: date
    total_call_amount: Decimal
    purpose: Optional[str] = None


class CapitalCallResponse(BaseModel):
    """Schema for capital call response"""
    id: str
    fund_id: str
    call_number: Optional[str]
    call_date: date
    due_date: date
    status: CapitalCallStatus
    total_call_amount: Decimal
    total_funded_amount: Decimal

    class Config:
        from_attributes = True


class DistributionCreate(BaseModel):
    """Schema for creating a distribution"""
    fund_id: str
    distribution_number: Optional[str] = None
    distribution_date: date
    distribution_type: DistributionType
    total_distribution_amount: Decimal
    source_description: Optional[str] = None


class DistributionResponse(BaseModel):
    """Schema for distribution response"""
    id: str
    fund_id: str
    distribution_number: Optional[str]
    distribution_date: date
    distribution_type: DistributionType
    total_distribution_amount: Decimal

    class Config:
        from_attributes = True


class WaterfallCalculationRequest(BaseModel):
    """Schema for waterfall calculation request"""
    distribution_amount: Decimal
    total_invested: Decimal
    total_distributed_to_date: Decimal
    preferred_return_rate: Decimal
    carried_interest_rate: Decimal
    waterfall_type: str = Field("american", description="'american' or 'european'")


class FundMetricsResponse(BaseModel):
    """Schema for fund metrics response"""
    fund_id: str
    fund_name: str
    irr: Optional[Decimal]
    moic: Optional[Decimal]
    dpi: Optional[Decimal]
    rvpi: Optional[Decimal]
    tvpi: Optional[Decimal]
    total_called: Decimal
    total_distributed: Decimal
    nav: Decimal
    committed_capital: Decimal


# ========================================
# FUND ENDPOINTS
# ========================================

@router.post("/funds", response_model=FundResponse, status_code=status.HTTP_201_CREATED)
def create_fund(
    fund: FundCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new fund"""
    current_user, company = user_company

    db_fund = Fund(
        **fund.dict(),
        company_id=company.id if company else None
    )
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


@router.get("/funds", response_model=List[FundResponse])
def get_funds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    fund_type: Optional[FundType] = None,
    status: Optional[FundStatus] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get all funds with optional filtering"""
    current_user, company = user_company

    query = db.query(Fund).filter(Fund.deleted_at == None)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(Fund.company_id == company.id)

    if fund_type:
        query = query.filter(Fund.fund_type == fund_type)
    if status:
        query = query.filter(Fund.status == status)

    funds = query.order_by(desc(Fund.created_at)).offset(skip).limit(limit).all()
    return funds


@router.get("/funds/{fund_id}", response_model=FundResponse)
def get_fund(
    fund_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get a specific fund by ID"""
    current_user, company = user_company

    filters = [Fund.id == fund_id, Fund.deleted_at == None]

    if company:
        filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund


@router.put("/funds/{fund_id}", response_model=FundResponse)
def update_fund(
    fund_id: str,
    fund_update: FundUpdate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Update a fund"""
    current_user, company = user_company

    filters = [Fund.id == fund_id, Fund.deleted_at == None]

    if company:
        filters.append(Fund.company_id == company.id)

    db_fund = db.query(Fund).filter(*filters).first()
    if not db_fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    update_data = fund_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fund, field, value)

    db.commit()
    db.refresh(db_fund)
    return db_fund


@router.delete("/funds/{fund_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fund(
    fund_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Soft delete a fund"""
    current_user, company = user_company

    filters = [Fund.id == fund_id, Fund.deleted_at == None]

    if company:
        filters.append(Fund.company_id == company.id)

    db_fund = db.query(Fund).filter(*filters).first()
    if not db_fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    db_fund.deleted_at = datetime.utcnow()
    db.commit()
    return None


# ========================================
# LIMITED PARTNER ENDPOINTS
# ========================================

@router.post("/lps", response_model=LPResponse, status_code=status.HTTP_201_CREATED)
def create_lp(
    lp: LPCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new limited partner"""
    current_user, company = user_company

    db_lp = LimitedPartner(
        **lp.dict(),
        company_id=company.id if company else None
    )
    db.add(db_lp)
    db.commit()
    db.refresh(db_lp)
    return db_lp


@router.get("/lps", response_model=List[LPResponse])
def get_lps(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get all limited partners"""
    current_user, company = user_company

    query = db.query(LimitedPartner).filter(LimitedPartner.deleted_at == None)

    # Filter by company_id if user has a company
    if company:
        query = query.filter(LimitedPartner.company_id == company.id)

    lps = query.order_by(desc(LimitedPartner.created_at)).offset(skip).limit(limit).all()
    return lps


@router.get("/lps/{lp_id}", response_model=LPResponse)
def get_lp(
    lp_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get a specific LP by ID"""
    current_user, company = user_company

    filters = [LimitedPartner.id == lp_id, LimitedPartner.deleted_at == None]

    if company:
        filters.append(LimitedPartner.company_id == company.id)

    lp = db.query(LimitedPartner).filter(*filters).first()
    if not lp:
        raise HTTPException(status_code=404, detail="LP not found")
    return lp


# ========================================
# COMMITMENT ENDPOINTS
# ========================================

@router.post("/commitments", response_model=CommitmentResponse, status_code=status.HTTP_201_CREATED)
def create_commitment(
    commitment: CommitmentCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new fund commitment"""
    current_user, company = user_company

    # Verify fund exists and user has access to it
    fund_filters = [Fund.id == commitment.fund_id]
    if company:
        fund_filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*fund_filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Verify LP exists and user has access to it
    lp_filters = [LimitedPartner.id == commitment.lp_id]
    if company:
        lp_filters.append(LimitedPartner.company_id == company.id)

    lp = db.query(LimitedPartner).filter(*lp_filters).first()
    if not lp:
        raise HTTPException(status_code=404, detail="LP not found")

    # Create commitment
    db_commitment = FundCommitment(**commitment.dict())
    db_commitment.unfunded_commitment = commitment.commitment_amount

    # Update fund's committed capital
    fund.committed_capital += commitment.commitment_amount

    db.add(db_commitment)
    db.commit()
    db.refresh(db_commitment)
    return db_commitment


@router.get("/commitments", response_model=List[CommitmentResponse])
def get_commitments(
    fund_id: Optional[str] = None,
    lp_id: Optional[str] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get fund commitments with optional filtering"""
    current_user, company = user_company

    query = db.query(FundCommitment).filter(FundCommitment.deleted_at == None)

    # Filter by company through the fund relationship
    if company:
        query = query.join(Fund).filter(Fund.company_id == company.id)

    if fund_id:
        query = query.filter(FundCommitment.fund_id == fund_id)
    if lp_id:
        query = query.filter(FundCommitment.lp_id == lp_id)

    commitments = query.all()
    return commitments


# ========================================
# CAPITAL CALL ENDPOINTS
# ========================================

@router.post("/capital-calls", response_model=CapitalCallResponse, status_code=status.HTTP_201_CREATED)
def create_capital_call(
    capital_call: CapitalCallCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new capital call"""
    current_user, company = user_company

    # Verify fund exists and user has access to it
    fund_filters = [Fund.id == capital_call.fund_id]
    if company:
        fund_filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*fund_filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Create capital call
    db_call = CapitalCall(**capital_call.dict())
    db.add(db_call)
    db.flush()

    # Create capital call items for each LP commitment
    commitments = db.query(FundCommitment).filter(
        FundCommitment.fund_id == capital_call.fund_id,
        FundCommitment.deleted_at == None
    ).all()

    total_commitments = sum(c.commitment_amount for c in commitments)

    for commitment in commitments:
        pro_rata_share = commitment.commitment_amount / total_commitments
        lp_call_amount = capital_call.total_call_amount * pro_rata_share

        call_item = CapitalCallItem(
            capital_call_id=db_call.id,
            commitment_id=commitment.id,
            called_amount=lp_call_amount
        )
        db.add(call_item)

    db.commit()
    db.refresh(db_call)
    return db_call


@router.get("/capital-calls", response_model=List[CapitalCallResponse])
def get_capital_calls(
    fund_id: Optional[str] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get capital calls with optional filtering"""
    current_user, company = user_company

    query = db.query(CapitalCall).filter(CapitalCall.deleted_at == None)

    # Filter by company through the fund relationship
    if company:
        query = query.join(Fund).filter(Fund.company_id == company.id)

    if fund_id:
        query = query.filter(CapitalCall.fund_id == fund_id)

    calls = query.order_by(desc(CapitalCall.call_date)).all()
    return calls


# ========================================
# DISTRIBUTION ENDPOINTS
# ========================================

@router.post("/distributions", response_model=DistributionResponse, status_code=status.HTTP_201_CREATED)
def create_distribution(
    distribution: DistributionCreate,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Create a new distribution"""
    current_user, company = user_company

    # Verify fund exists and user has access to it
    fund_filters = [Fund.id == distribution.fund_id]
    if company:
        fund_filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*fund_filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Create distribution
    db_distribution = Distribution(**distribution.dict())
    db.add(db_distribution)
    db.flush()

    # Calculate waterfall and create distribution items
    commitments = db.query(FundCommitment).filter(
        FundCommitment.fund_id == distribution.fund_id,
        FundCommitment.deleted_at == None
    ).all()

    # Use American waterfall for calculation
    waterfall_result = waterfall_calculator.calculate_american_waterfall(
        distribution_amount=distribution.total_distribution_amount,
        total_invested=fund.total_called,
        total_distributed_to_date=fund.total_distributed,
        preferred_return_rate=fund.preferred_return_rate,
        carried_interest_rate=fund.carried_interest_rate,
        lp_share=Decimal("1") - fund.carried_interest_rate
    )

    # Allocate to LPs pro-rata
    total_commitments = sum(c.commitment_amount for c in commitments)
    lp_total = waterfall_result['lp_total']

    for commitment in commitments:
        pro_rata_share = commitment.commitment_amount / total_commitments
        lp_distribution = lp_total * pro_rata_share

        dist_item = DistributionItem(
            distribution_id=db_distribution.id,
            commitment_id=commitment.id,
            total_distribution=lp_distribution,
            return_of_capital=waterfall_result['lp_return_of_capital'] * pro_rata_share,
            preferred_return=waterfall_result['lp_preferred_return'] * pro_rata_share,
            remaining_profit=waterfall_result.get('lp_remaining_profit', Decimal("0")) * pro_rata_share
        )
        db.add(dist_item)

        # Update commitment's distributed amount
        commitment.distributed_amount += lp_distribution

    # Update fund's total distributed
    fund.total_distributed += distribution.total_distribution_amount

    db.commit()
    db.refresh(db_distribution)
    return db_distribution


@router.get("/distributions", response_model=List[DistributionResponse])
def get_distributions(
    fund_id: Optional[str] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get distributions with optional filtering"""
    current_user, company = user_company

    query = db.query(Distribution).filter(Distribution.deleted_at == None)

    # Filter by company through the fund relationship
    if company:
        query = query.join(Fund).filter(Fund.company_id == company.id)

    if fund_id:
        query = query.filter(Distribution.fund_id == fund_id)

    distributions = query.order_by(desc(Distribution.distribution_date)).all()
    return distributions


# ========================================
# CALCULATION ENDPOINTS
# ========================================

@router.post("/calculate/waterfall")
def calculate_waterfall(request: WaterfallCalculationRequest):
    """Calculate distribution waterfall"""
    if request.waterfall_type == "american":
        result = waterfall_calculator.calculate_american_waterfall(
            distribution_amount=request.distribution_amount,
            total_invested=request.total_invested,
            total_distributed_to_date=request.total_distributed_to_date,
            preferred_return_rate=request.preferred_return_rate,
            carried_interest_rate=request.carried_interest_rate,
            lp_share=Decimal("1") - request.carried_interest_rate
        )
    else:
        result = waterfall_calculator.calculate_european_waterfall(
            distribution_amount=request.distribution_amount,
            total_invested=request.total_invested,
            total_distributed_to_date=request.total_distributed_to_date,
            preferred_return_rate=request.preferred_return_rate,
            carried_interest_rate=request.carried_interest_rate
        )

    return {
        "waterfall_type": request.waterfall_type,
        "calculation": {k: float(v) for k, v in result.items()}
    }


@router.get("/funds/{fund_id}/metrics", response_model=FundMetricsResponse)
def get_fund_metrics(
    fund_id: str,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Get comprehensive fund performance metrics"""
    current_user, company = user_company

    filters = [Fund.id == fund_id, Fund.deleted_at == None]

    if company:
        filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Calculate metrics
    metrics = {
        'total_called': fund.total_called,
        'total_distributed': fund.total_distributed,
        'nav': fund.nav,
        'cash_flows': []  # Would need to build from capital calls and distributions
    }

    calculated_metrics = performance_tracker.update_fund_metrics(metrics)

    return FundMetricsResponse(
        fund_id=fund.id,
        fund_name=fund.name,
        irr=calculated_metrics.get('irr'),
        moic=calculated_metrics.get('moic'),
        dpi=calculated_metrics.get('dpi'),
        rvpi=calculated_metrics.get('rvpi'),
        tvpi=calculated_metrics.get('tvpi'),
        total_called=fund.total_called,
        total_distributed=fund.total_distributed,
        nav=fund.nav,
        committed_capital=fund.committed_capital
    )


@router.get("/funds/{fund_id}/lp-report")
def get_lp_report(
    fund_id: str,
    lp_id: Optional[str] = None,
    user_company: tuple[User, Optional[Company]] = Depends(get_current_user_with_company),
    db: Session = Depends(get_db)
):
    """Generate LP report for a fund"""
    current_user, company = user_company

    filters = [Fund.id == fund_id, Fund.deleted_at == None]

    if company:
        filters.append(Fund.company_id == company.id)

    fund = db.query(Fund).filter(*filters).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    # Get commitments
    query = db.query(FundCommitment).filter(
        FundCommitment.fund_id == fund_id,
        FundCommitment.deleted_at == None
    )

    if lp_id:
        query = query.filter(FundCommitment.lp_id == lp_id)

    commitments = query.all()

    lp_reports = []
    for commitment in commitments:
        lp = commitment.limited_partner

        # Get capital calls for this LP
        capital_calls = db.query(CapitalCallItem).join(CapitalCall).filter(
            CapitalCallItem.commitment_id == commitment.id
        ).all()

        # Get distributions for this LP
        distributions = db.query(DistributionItem).join(Distribution).filter(
            DistributionItem.commitment_id == commitment.id
        ).all()

        lp_reports.append({
            'lp_name': lp.name,
            'commitment_amount': float(commitment.commitment_amount),
            'called_amount': float(commitment.called_amount),
            'distributed_amount': float(commitment.distributed_amount),
            'unfunded_commitment': float(commitment.unfunded_commitment),
            'total_capital_calls': len(capital_calls),
            'total_distributions': len(distributions),
            'net_cash_flow': float(commitment.distributed_amount - commitment.called_amount)
        })

    return {
        'fund_name': fund.name,
        'fund_vintage': fund.vintage_year,
        'report_date': datetime.utcnow().isoformat(),
        'lp_reports': lp_reports
    }
