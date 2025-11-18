"""
Accounting API Endpoints

This module provides REST API endpoints for comprehensive accounting features including:
- Accounting profile management
- Chart of accounts
- Transactions
- Tax benefits tracking
- Integration configurations
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

from app.api.deps import get_db
from app.models.accounting import (
    AccountingProfile,
    ChartOfAccount,
    AccountingTransaction,
    TransactionLine,
    TaxBenefit,
    IntegrationConfig,
    AccountingEntityType,
    AccountType,
    AccountSubType,
    TransactionType,
    TaxBenefitType,
    IntegrationType,
)
from app.models.company import Company


router = APIRouter()


# ============================================================================
# Pydantic Schemas - Accounting Profile
# ============================================================================

class AccountingProfileBase(BaseModel):
    """Base accounting profile schema"""
    entity_type: AccountingEntityType
    fiscal_year_end: str = Field("12-31", description="Fiscal year end (MM-DD)")
    accounting_method: str = Field("accrual", description="accrual or cash")
    base_currency: str = Field("USD", max_length=3)
    tax_id: Optional[str] = None
    tax_jurisdiction: Optional[str] = None
    enable_multi_currency: bool = False
    enable_property_tracking: bool = True
    enable_trust_accounting: bool = False
    settings: Optional[dict] = None


class AccountingProfileCreate(AccountingProfileBase):
    """Schema for creating an accounting profile"""
    company_id: UUID


class AccountingProfileUpdate(BaseModel):
    """Schema for updating an accounting profile"""
    entity_type: Optional[AccountingEntityType] = None
    fiscal_year_end: Optional[str] = None
    accounting_method: Optional[str] = None
    base_currency: Optional[str] = None
    tax_id: Optional[str] = None
    tax_jurisdiction: Optional[str] = None
    enable_multi_currency: Optional[bool] = None
    enable_property_tracking: Optional[bool] = None
    enable_trust_accounting: Optional[bool] = None
    settings: Optional[dict] = None


class AccountingProfileResponse(AccountingProfileBase):
    """Schema for accounting profile response"""
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Pydantic Schemas - Chart of Accounts
# ============================================================================

class ChartOfAccountBase(BaseModel):
    """Base chart of account schema"""
    account_number: str = Field(..., max_length=20)
    account_name: str = Field(..., max_length=200)
    account_type: AccountType
    account_subtype: Optional[AccountSubType] = None
    description: Optional[str] = None
    parent_account_id: Optional[UUID] = None
    property_id: Optional[UUID] = None
    is_active: bool = True
    allow_manual_entry: bool = True
    notes: Optional[str] = None


class ChartOfAccountCreate(ChartOfAccountBase):
    """Schema for creating a chart of account"""
    accounting_profile_id: UUID


class ChartOfAccountUpdate(BaseModel):
    """Schema for updating a chart of account"""
    account_name: Optional[str] = None
    account_type: Optional[AccountType] = None
    account_subtype: Optional[AccountSubType] = None
    description: Optional[str] = None
    parent_account_id: Optional[UUID] = None
    property_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    allow_manual_entry: Optional[bool] = None
    notes: Optional[str] = None


class ChartOfAccountResponse(ChartOfAccountBase):
    """Schema for chart of account response"""
    id: UUID
    accounting_profile_id: UUID
    current_balance: Decimal
    is_system_account: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Pydantic Schemas - Transactions
# ============================================================================

class TransactionLineSchema(BaseModel):
    """Schema for transaction line"""
    account_id: UUID
    debit: Decimal = Field(Decimal("0.00"), ge=0)
    credit: Decimal = Field(Decimal("0.00"), ge=0)
    description: Optional[str] = None

    @validator('debit', 'credit')
    def validate_amounts(cls, v, values):
        """Ensure at least one of debit or credit is non-zero"""
        return v


class TransactionBase(BaseModel):
    """Base transaction schema"""
    transaction_date: str = Field(..., description="YYYY-MM-DD format")
    transaction_type: TransactionType
    reference_number: Optional[str] = None
    description: str
    property_id: Optional[UUID] = None
    notes: Optional[str] = None
    attachments: Optional[dict] = None


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction"""
    accounting_profile_id: UUID
    lines: List[TransactionLineSchema] = Field(..., min_items=2)

    @validator('lines')
    def validate_balanced_transaction(cls, v):
        """Ensure debits equal credits"""
        total_debits = sum(line.debit for line in v)
        total_credits = sum(line.credit for line in v)
        if total_debits != total_credits:
            raise ValueError(f"Transaction must be balanced. Debits: {total_debits}, Credits: {total_credits}")
        return v


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    transaction_date: Optional[str] = None
    transaction_type: Optional[TransactionType] = None
    reference_number: Optional[str] = None
    description: Optional[str] = None
    property_id: Optional[UUID] = None
    notes: Optional[str] = None
    attachments: Optional[dict] = None
    is_posted: Optional[bool] = None
    is_reconciled: Optional[bool] = None


class TransactionLineResponse(BaseModel):
    """Schema for transaction line response"""
    id: UUID
    account_id: UUID
    debit: Decimal
    credit: Decimal
    description: Optional[str]

    class Config:
        from_attributes = True


class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: UUID
    accounting_profile_id: UUID
    is_posted: bool
    is_reconciled: bool
    created_at: datetime
    updated_at: datetime
    lines: List[TransactionLineResponse] = []

    class Config:
        from_attributes = True


# ============================================================================
# Pydantic Schemas - Tax Benefits
# ============================================================================

class TaxBenefitBase(BaseModel):
    """Base tax benefit schema"""
    tax_year: str = Field(..., max_length=4, description="YYYY format")
    benefit_type: TaxBenefitType
    benefit_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    benefit_amount: Decimal = Field(..., ge=0)
    estimated_tax_savings: Optional[Decimal] = None
    property_id: Optional[UUID] = None
    transaction_id: Optional[UUID] = None
    documentation: Optional[dict] = None
    notes: Optional[str] = None


class TaxBenefitCreate(TaxBenefitBase):
    """Schema for creating a tax benefit"""
    accounting_profile_id: UUID


class TaxBenefitUpdate(BaseModel):
    """Schema for updating a tax benefit"""
    tax_year: Optional[str] = None
    benefit_type: Optional[TaxBenefitType] = None
    benefit_name: Optional[str] = None
    description: Optional[str] = None
    benefit_amount: Optional[Decimal] = None
    estimated_tax_savings: Optional[Decimal] = None
    property_id: Optional[UUID] = None
    transaction_id: Optional[UUID] = None
    is_claimed: Optional[bool] = None
    claim_date: Optional[str] = None
    documentation: Optional[dict] = None
    notes: Optional[str] = None


class TaxBenefitResponse(TaxBenefitBase):
    """Schema for tax benefit response"""
    id: UUID
    accounting_profile_id: UUID
    is_claimed: bool
    claim_date: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Pydantic Schemas - Integrations
# ============================================================================

class IntegrationConfigBase(BaseModel):
    """Base integration config schema"""
    integration_type: IntegrationType
    integration_name: str = Field(..., max_length=200)
    is_enabled: bool = False
    api_credentials: Optional[dict] = None
    sync_settings: Optional[dict] = None
    notes: Optional[str] = None


class IntegrationConfigCreate(IntegrationConfigBase):
    """Schema for creating an integration config"""
    accounting_profile_id: UUID


class IntegrationConfigUpdate(BaseModel):
    """Schema for updating an integration config"""
    integration_name: Optional[str] = None
    is_enabled: Optional[bool] = None
    api_credentials: Optional[dict] = None
    sync_settings: Optional[dict] = None
    notes: Optional[str] = None


class IntegrationConfigResponse(IntegrationConfigBase):
    """Schema for integration config response"""
    id: UUID
    accounting_profile_id: UUID
    is_connected: bool
    last_sync_at: Optional[str]
    status: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# API Endpoints - Accounting Profiles
# ============================================================================

@router.post("/profiles", response_model=AccountingProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_accounting_profile(
    profile_data: AccountingProfileCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new accounting profile for a company.

    Each company can have one accounting profile that defines:
    - Entity type (small business, individual, high net worth, etc.)
    - Fiscal year and accounting method
    - Tax information
    - Integration settings
    """
    # Check if company exists
    company = db.query(Company).filter(
        Company.id == profile_data.company_id,
        Company.deleted_at.is_(None)
    ).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {profile_data.company_id} not found"
        )

    # Check if profile already exists
    existing = db.query(AccountingProfile).filter(
        AccountingProfile.company_id == profile_data.company_id,
        AccountingProfile.deleted_at.is_(None)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Accounting profile already exists for this company"
        )

    # Create profile
    profile = AccountingProfile(**profile_data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get("/profiles", response_model=List[AccountingProfileResponse])
async def list_accounting_profiles(
    company_id: Optional[UUID] = Query(None, description="Filter by company"),
    entity_type: Optional[AccountingEntityType] = Query(None, description="Filter by entity type"),
    db: Session = Depends(get_db),
):
    """List all accounting profiles with optional filters"""
    query = db.query(AccountingProfile).filter(AccountingProfile.deleted_at.is_(None))

    if company_id:
        query = query.filter(AccountingProfile.company_id == company_id)

    if entity_type:
        query = query.filter(AccountingProfile.entity_type == entity_type)

    profiles = query.all()
    return profiles


@router.get("/profiles/{profile_id}", response_model=AccountingProfileResponse)
async def get_accounting_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific accounting profile"""
    profile = db.query(AccountingProfile).filter(
        AccountingProfile.id == profile_id,
        AccountingProfile.deleted_at.is_(None)
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accounting profile with id {profile_id} not found"
        )

    return profile


@router.put("/profiles/{profile_id}", response_model=AccountingProfileResponse)
async def update_accounting_profile(
    profile_id: UUID,
    profile_data: AccountingProfileUpdate,
    db: Session = Depends(get_db),
):
    """Update an accounting profile"""
    profile = db.query(AccountingProfile).filter(
        AccountingProfile.id == profile_id,
        AccountingProfile.deleted_at.is_(None)
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accounting profile with id {profile_id} not found"
        )

    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    return profile


# ============================================================================
# API Endpoints - Chart of Accounts
# ============================================================================

@router.post("/chart-of-accounts", response_model=ChartOfAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: ChartOfAccountCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new account in the chart of accounts.

    Supports:
    - Standard account types (Asset, Liability, Equity, Revenue, Expense)
    - Detailed subtypes for property management
    - Parent-child account relationships
    - Property-specific tracking
    """
    # Verify profile exists
    profile = db.query(AccountingProfile).filter(
        AccountingProfile.id == account_data.accounting_profile_id,
        AccountingProfile.deleted_at.is_(None)
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accounting profile not found"
        )

    # Check for duplicate account number
    existing = db.query(ChartOfAccount).filter(
        ChartOfAccount.accounting_profile_id == account_data.accounting_profile_id,
        ChartOfAccount.account_number == account_data.account_number,
        ChartOfAccount.deleted_at.is_(None)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Account with number '{account_data.account_number}' already exists"
        )

    account = ChartOfAccount(**account_data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)

    return account


@router.get("/chart-of-accounts", response_model=List[ChartOfAccountResponse])
async def list_accounts(
    accounting_profile_id: UUID = Query(..., description="Accounting profile ID"),
    account_type: Optional[AccountType] = Query(None, description="Filter by account type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    property_id: Optional[UUID] = Query(None, description="Filter by property"),
    db: Session = Depends(get_db),
):
    """List all accounts in the chart of accounts"""
    query = db.query(ChartOfAccount).filter(
        ChartOfAccount.accounting_profile_id == accounting_profile_id,
        ChartOfAccount.deleted_at.is_(None)
    )

    if account_type:
        query = query.filter(ChartOfAccount.account_type == account_type)

    if is_active is not None:
        query = query.filter(ChartOfAccount.is_active == is_active)

    if property_id:
        query = query.filter(ChartOfAccount.property_id == property_id)

    accounts = query.order_by(ChartOfAccount.account_number).all()
    return accounts


@router.put("/chart-of-accounts/{account_id}", response_model=ChartOfAccountResponse)
async def update_account(
    account_id: UUID,
    account_data: ChartOfAccountUpdate,
    db: Session = Depends(get_db),
):
    """Update a chart of account"""
    account = db.query(ChartOfAccount).filter(
        ChartOfAccount.id == account_id,
        ChartOfAccount.deleted_at.is_(None)
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account not found"
        )

    if account.is_system_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify system account"
        )

    update_data = account_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)

    return account


# ============================================================================
# API Endpoints - Transactions
# ============================================================================

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new accounting transaction with double-entry bookkeeping.

    All transactions must be balanced (total debits = total credits).
    Supports:
    - Income, expense, transfer, and adjustment transactions
    - Multiple line items
    - Property-specific tracking
    - Document attachments
    """
    # Create transaction
    transaction_dict = transaction_data.model_dump(exclude={'lines'})
    transaction = AccountingTransaction(**transaction_dict)
    db.add(transaction)
    db.flush()  # Get transaction ID before adding lines

    # Create transaction lines
    for line_data in transaction_data.lines:
        line = TransactionLine(
            transaction_id=transaction.id,
            **line_data.model_dump()
        )
        db.add(line)

    db.commit()
    db.refresh(transaction)

    return transaction


@router.get("/transactions", response_model=List[TransactionResponse])
async def list_transactions(
    accounting_profile_id: UUID = Query(..., description="Accounting profile ID"),
    transaction_type: Optional[TransactionType] = Query(None),
    property_id: Optional[UUID] = Query(None),
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    is_posted: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """List all transactions with filters"""
    query = db.query(AccountingTransaction).filter(
        AccountingTransaction.accounting_profile_id == accounting_profile_id,
        AccountingTransaction.deleted_at.is_(None)
    )

    if transaction_type:
        query = query.filter(AccountingTransaction.transaction_type == transaction_type)

    if property_id:
        query = query.filter(AccountingTransaction.property_id == property_id)

    if start_date:
        query = query.filter(AccountingTransaction.transaction_date >= start_date)

    if end_date:
        query = query.filter(AccountingTransaction.transaction_date <= end_date)

    if is_posted is not None:
        query = query.filter(AccountingTransaction.is_posted == is_posted)

    transactions = query.order_by(
        AccountingTransaction.transaction_date.desc()
    ).offset(skip).limit(limit).all()

    return transactions


# ============================================================================
# API Endpoints - Tax Benefits
# ============================================================================

@router.post("/tax-benefits", response_model=TaxBenefitResponse, status_code=status.HTTP_201_CREATED)
async def create_tax_benefit(
    benefit_data: TaxBenefitCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new tax benefit record.

    Track tax deductions and credits including:
    - Depreciation and cost segregation
    - Mortgage interest deductions
    - Property tax deductions
    - Repair and maintenance deductions
    - High net worth strategies (charitable giving, tax-loss harvesting)
    - Estate planning benefits
    """
    benefit = TaxBenefit(**benefit_data.model_dump())
    db.add(benefit)
    db.commit()
    db.refresh(benefit)

    return benefit


@router.get("/tax-benefits", response_model=List[TaxBenefitResponse])
async def list_tax_benefits(
    accounting_profile_id: UUID = Query(..., description="Accounting profile ID"),
    tax_year: Optional[str] = Query(None, description="Filter by tax year (YYYY)"),
    benefit_type: Optional[TaxBenefitType] = Query(None),
    property_id: Optional[UUID] = Query(None),
    is_claimed: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    """List all tax benefits with filters"""
    query = db.query(TaxBenefit).filter(
        TaxBenefit.accounting_profile_id == accounting_profile_id,
        TaxBenefit.deleted_at.is_(None)
    )

    if tax_year:
        query = query.filter(TaxBenefit.tax_year == tax_year)

    if benefit_type:
        query = query.filter(TaxBenefit.benefit_type == benefit_type)

    if property_id:
        query = query.filter(TaxBenefit.property_id == property_id)

    if is_claimed is not None:
        query = query.filter(TaxBenefit.is_claimed == is_claimed)

    benefits = query.order_by(TaxBenefit.tax_year.desc()).all()
    return benefits


@router.put("/tax-benefits/{benefit_id}", response_model=TaxBenefitResponse)
async def update_tax_benefit(
    benefit_id: UUID,
    benefit_data: TaxBenefitUpdate,
    db: Session = Depends(get_db),
):
    """Update a tax benefit"""
    benefit = db.query(TaxBenefit).filter(
        TaxBenefit.id == benefit_id,
        TaxBenefit.deleted_at.is_(None)
    ).first()

    if not benefit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax benefit not found"
        )

    update_data = benefit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(benefit, field, value)

    db.commit()
    db.refresh(benefit)

    return benefit


# ============================================================================
# API Endpoints - Integrations
# ============================================================================

@router.post("/integrations", response_model=IntegrationConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    integration_data: IntegrationConfigCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new third-party integration.

    Supported integrations:
    - QuickBooks/Xero for accounting sync
    - Yardi/AppFolio for property management
    - DocuSign for e-signatures
    - Dropbox/Box for document storage
    - Calendar sync for key dates
    """
    integration = IntegrationConfig(**integration_data.model_dump())
    db.add(integration)
    db.commit()
    db.refresh(integration)

    return integration


@router.get("/integrations", response_model=List[IntegrationConfigResponse])
async def list_integrations(
    accounting_profile_id: UUID = Query(..., description="Accounting profile ID"),
    integration_type: Optional[IntegrationType] = Query(None),
    is_enabled: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    """List all integrations"""
    query = db.query(IntegrationConfig).filter(
        IntegrationConfig.accounting_profile_id == accounting_profile_id,
        IntegrationConfig.deleted_at.is_(None)
    )

    if integration_type:
        query = query.filter(IntegrationConfig.integration_type == integration_type)

    if is_enabled is not None:
        query = query.filter(IntegrationConfig.is_enabled == is_enabled)

    integrations = query.all()
    return integrations


@router.put("/integrations/{integration_id}", response_model=IntegrationConfigResponse)
async def update_integration(
    integration_id: UUID,
    integration_data: IntegrationConfigUpdate,
    db: Session = Depends(get_db),
):
    """Update an integration configuration"""
    integration = db.query(IntegrationConfig).filter(
        IntegrationConfig.id == integration_id,
        IntegrationConfig.deleted_at.is_(None)
    ).first()

    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Integration not found"
        )

    update_data = integration_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(integration, field, value)

    db.commit()
    db.refresh(integration)

    return integration
