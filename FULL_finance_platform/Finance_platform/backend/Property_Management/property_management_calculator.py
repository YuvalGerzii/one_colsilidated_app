"""
Property Management System - Python Calculator
Replicates all Excel functionality from Property_Management_System.xlsx

This module provides comprehensive property management calculations including:
- Portfolio-level metrics (occupancy, NOI, cap rate)
- Property-level financials (income statement, cash flow)
- Unit-level tracking (vacancy, loss-to-lease)
- Lease management (expiration risk scoring)
- ROI analysis (cash-on-cash, IRR, total returns)
- Budget variance analysis
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from decimal import Decimal
from enum import Enum
import math


class PropertyType(str, Enum):
    """Property type classifications"""
    MULTIFAMILY = "Multifamily"
    SINGLE_FAMILY = "Single Family"
    COMMERCIAL_OFFICE = "Commercial Office"
    RETAIL = "Retail"
    INDUSTRIAL = "Industrial"
    MIXED_USE = "Mixed-Use"
    HOTEL_HOSPITALITY = "Hotel/Hospitality"


class OwnershipModel(str, Enum):
    """Ownership structure models"""
    FULL_OWNERSHIP = "Full Ownership"
    MASTER_LEASE = "Master Lease"
    SUBLEASE = "Sublease"
    RENTAL_ARBITRAGE = "Rental Arbitrage (Airbnb/VRBO)"
    JOINT_VENTURE = "Joint Venture"
    MANAGEMENT_ONLY = "Management Contract Only"
    GROUND_LEASE = "Ground Lease"


class PropertyStatus(str, Enum):
    """Property status"""
    ACTIVE = "Active"
    UNDER_CONTRACT = "Under Contract"
    SOLD = "Sold"
    INACTIVE = "Inactive"


class UnitStatus(str, Enum):
    """Unit occupancy status"""
    OCCUPIED = "Occupied"
    VACANT = "Vacant"
    UNDER_RENOVATION = "Under Renovation"
    OFF_MARKET = "Off-Market"


class MaintenancePriority(str, Enum):
    """Maintenance request priority levels"""
    EMERGENCY = "Emergency"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MaintenanceStatus(str, Enum):
    """Maintenance request status"""
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class LeaseRiskLevel(str, Enum):
    """Lease expiration risk levels"""
    CRITICAL = "CRITICAL"  # <60 days
    HIGH = "HIGH"  # 60-120 days
    MODERATE = "MODERATE"  # 120-180 days
    LOW = "LOW"  # 180+ days


@dataclass
class Property:
    """Property master record"""
    property_id: str
    property_name: str
    address: str
    city: str
    state: str
    property_type: PropertyType
    ownership_model: OwnershipModel
    total_units: int
    purchase_price: Decimal
    purchase_date: date
    current_value: Decimal
    status: PropertyStatus = PropertyStatus.ACTIVE
    notes: Optional[str] = None


@dataclass
class OwnershipDetails:
    """Ownership model details"""
    property_id: str
    ownership_type: OwnershipModel
    details: Optional[str] = None
    master_lease_amount: Optional[Decimal] = None
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    landlord_approval: Optional[bool] = None
    special_terms: Optional[str] = None
    profit_split_percent: Optional[Decimal] = None


@dataclass
class Unit:
    """Unit inventory record"""
    property_id: str
    unit_number: str
    unit_type: str
    status: UnitStatus
    beds: int
    baths: Decimal
    square_footage: int
    market_rent: Decimal
    current_rent: Decimal = Decimal('0')
    tenant_name: Optional[str] = None
    days_vacant: int = 0
    renovation_budget: Decimal = Decimal('0')
    last_occupied_date: Optional[date] = None

    @property
    def is_occupied(self) -> bool:
        """Check if unit is occupied"""
        return self.status == UnitStatus.OCCUPIED

    @property
    def loss_to_lease(self) -> Decimal:
        """Calculate loss-to-lease (market rent - current rent)"""
        return self.market_rent - self.current_rent


@dataclass
class Lease:
    """Rent roll / lease record"""
    property_id: str
    unit_number: str
    tenant_name: str
    lease_start_date: date
    lease_end_date: date
    monthly_rent: Decimal
    security_deposit: Decimal = Decimal('0')
    credit_score: Optional[int] = None
    notes: Optional[str] = None

    @property
    def annual_rent(self) -> Decimal:
        """Calculate annual rent"""
        return self.monthly_rent * 12

    @property
    def days_until_expiration(self) -> int:
        """Calculate days until lease expiration"""
        today = date.today()
        delta = self.lease_end_date - today
        return delta.days

    @property
    def risk_level(self) -> LeaseRiskLevel:
        """Determine lease expiration risk level"""
        days = self.days_until_expiration
        if days < 0:
            return LeaseRiskLevel.CRITICAL
        elif days < 60:
            return LeaseRiskLevel.CRITICAL
        elif days < 120:
            return LeaseRiskLevel.HIGH
        elif days < 180:
            return LeaseRiskLevel.MODERATE
        else:
            return LeaseRiskLevel.LOW

    @property
    def action_required(self) -> str:
        """Determine required action based on risk level"""
        days = self.days_until_expiration
        if days < 0:
            return "EXPIRED - Immediate Action"
        elif days < 60:
            return "Contact Tenant Immediately"
        elif days < 120:
            return "Start Renewal Process"
        elif days < 180:
            return "Plan Renewal Discussion"
        else:
            return "Monitor"


@dataclass
class IncomeStatement:
    """Monthly income statement for a property"""
    property_id: str
    month: date
    gross_potential_rent: Decimal
    vacancy_loss: Decimal  # Negative value
    other_income: Decimal = Decimal('0')
    operating_expenses: Decimal = Decimal('0')
    debt_service: Decimal = Decimal('0')

    @property
    def effective_gross_income(self) -> Decimal:
        """Calculate EGI = GPR + Other Income - Vacancy"""
        return self.gross_potential_rent + self.other_income + self.vacancy_loss

    @property
    def net_operating_income(self) -> Decimal:
        """Calculate NOI = EGI - OpEx"""
        return self.effective_gross_income - self.operating_expenses

    @property
    def cash_flow_before_tax(self) -> Decimal:
        """Calculate cash flow = NOI - Debt Service"""
        return self.net_operating_income - self.debt_service


@dataclass
class MaintenanceRequest:
    """Maintenance tracker record"""
    request_id: str
    property_id: str
    unit_number: Optional[str]
    category: str
    description: str
    status: MaintenanceStatus
    priority: MaintenancePriority
    date_reported: date
    date_completed: Optional[date] = None
    cost: Decimal = Decimal('0')
    vendor: Optional[str] = None
    notes: Optional[str] = None

    @property
    def days_open(self) -> int:
        """Calculate days the request has been open"""
        if self.status == MaintenanceStatus.COMPLETED and self.date_completed:
            delta = self.date_completed - self.date_reported
        else:
            delta = date.today() - self.date_reported
        return delta.days


@dataclass
class BudgetVsActual:
    """Budget variance analysis"""
    property_id: str
    expense_category: str
    budget_monthly: Decimal
    actual_monthly: Decimal

    @property
    def variance_dollars(self) -> Decimal:
        """Calculate variance in dollars"""
        return self.actual_monthly - self.budget_monthly

    @property
    def variance_percent(self) -> Decimal:
        """Calculate variance as percentage"""
        if self.budget_monthly == 0:
            return Decimal('0')
        return (self.variance_dollars / self.budget_monthly) * 100

    @property
    def status(self) -> str:
        """Determine budget status"""
        variance_pct = abs(self.variance_percent)
        if variance_pct < 5:
            return "On Track"
        elif self.variance_dollars < 0:
            return "Under Budget"
        else:
            return "Over Budget"


class PropertyManagementCalculator:
    """Main calculator class for property management metrics"""

    def __init__(self):
        self.properties: List[Property] = []
        self.units: List[Unit] = []
        self.leases: List[Lease] = []
        self.income_statements: List[IncomeStatement] = []
        self.maintenance_requests: List[MaintenanceRequest] = []
        self.ownership_details: List[OwnershipDetails] = []
        self.budget_items: List[BudgetVsActual] = []

    # Portfolio-level calculations

    def total_properties(self) -> int:
        """Count total active properties"""
        return len([p for p in self.properties if p.status == PropertyStatus.ACTIVE])

    def total_units(self) -> int:
        """Count total units across all properties"""
        return len(self.units)

    def occupied_units(self) -> int:
        """Count occupied units"""
        return len([u for u in self.units if u.is_occupied])

    def vacant_units(self) -> int:
        """Count vacant units"""
        return len([u for u in self.units if u.status == UnitStatus.VACANT])

    def physical_occupancy_rate(self) -> Decimal:
        """Calculate physical occupancy rate"""
        total = self.total_units()
        if total == 0:
            return Decimal('0')
        occupied = self.occupied_units()
        return Decimal(occupied) / Decimal(total)

    def portfolio_value(self) -> Decimal:
        """Calculate total portfolio value"""
        return sum(p.current_value for p in self.properties
                  if p.status == PropertyStatus.ACTIVE)

    def total_equity(self) -> Decimal:
        """Calculate total equity invested (from properties with full ownership)"""
        # This would come from ROI analysis data in a full implementation
        # For now, we'll calculate based on purchase prices for owned properties
        return sum(p.purchase_price for p in self.properties
                  if p.ownership_model == OwnershipModel.FULL_OWNERSHIP
                  and p.status == PropertyStatus.ACTIVE)

    def gross_potential_rent_monthly(self) -> Decimal:
        """Calculate total GPR across all properties"""
        return sum(u.market_rent for u in self.units)

    def vacancy_loss_monthly(self) -> Decimal:
        """Calculate total vacancy loss"""
        return sum(u.market_rent for u in self.units
                  if u.status == UnitStatus.VACANT)

    def effective_gross_income_monthly(self) -> Decimal:
        """Calculate portfolio-level EGI"""
        gpr = self.gross_potential_rent_monthly()
        vacancy = self.vacancy_loss_monthly()
        # In a full implementation, would add other income
        return gpr - vacancy

    def net_operating_income_monthly(self) -> Decimal:
        """Calculate portfolio-level NOI"""
        return sum(stmt.net_operating_income for stmt in self.income_statements)

    def portfolio_cap_rate(self) -> Decimal:
        """Calculate portfolio cap rate = (Annual NOI / Portfolio Value)"""
        portfolio_val = self.portfolio_value()
        if portfolio_val == 0:
            return Decimal('0')
        annual_noi = self.net_operating_income_monthly() * 12
        return (annual_noi / portfolio_val) * 100

    # Property-level calculations

    def property_units(self, property_id: str) -> List[Unit]:
        """Get all units for a specific property"""
        return [u for u in self.units if u.property_id == property_id]

    def property_occupancy_rate(self, property_id: str) -> Decimal:
        """Calculate occupancy rate for a specific property"""
        units = self.property_units(property_id)
        if not units:
            return Decimal('0')
        occupied = len([u for u in units if u.is_occupied])
        return Decimal(occupied) / Decimal(len(units))

    def property_gpr(self, property_id: str) -> Decimal:
        """Calculate GPR for a specific property"""
        units = self.property_units(property_id)
        return sum(u.market_rent for u in units)

    def property_vacancy_loss(self, property_id: str) -> Decimal:
        """Calculate vacancy loss for a specific property"""
        units = self.property_units(property_id)
        return sum(u.market_rent for u in units if u.status == UnitStatus.VACANT)

    # Lease management

    def leases_expiring_soon(self, days: int = 60) -> List[Lease]:
        """Get leases expiring within specified days"""
        return [l for l in self.leases if 0 <= l.days_until_expiration <= days]

    def critical_leases(self) -> List[Lease]:
        """Get all critical risk leases"""
        return [l for l in self.leases if l.risk_level == LeaseRiskLevel.CRITICAL]

    def high_risk_leases(self) -> List[Lease]:
        """Get all high risk leases"""
        return [l for l in self.leases if l.risk_level == LeaseRiskLevel.HIGH]

    # Maintenance tracking

    def open_maintenance_requests(self) -> List[MaintenanceRequest]:
        """Get all open maintenance requests"""
        return [m for m in self.maintenance_requests
                if m.status in [MaintenanceStatus.OPEN, MaintenanceStatus.IN_PROGRESS]]

    def emergency_maintenance(self) -> List[MaintenanceRequest]:
        """Get all emergency maintenance requests"""
        return [m for m in self.maintenance_requests
                if m.priority == MaintenancePriority.EMERGENCY
                and m.status != MaintenanceStatus.COMPLETED]

    def total_maintenance_cost(self, property_id: Optional[str] = None) -> Decimal:
        """Calculate total maintenance costs"""
        requests = self.maintenance_requests
        if property_id:
            requests = [m for m in requests if m.property_id == property_id]
        return sum(m.cost for m in requests)

    # ROI calculations

    def calculate_cash_on_cash_return(
        self,
        annual_cash_flow: Decimal,
        total_equity: Decimal
    ) -> Decimal:
        """Calculate cash-on-cash return = Annual CF / Total Equity"""
        if total_equity == 0:
            return Decimal('0')
        return (annual_cash_flow / total_equity) * 100

    def calculate_total_roi(
        self,
        total_return: Decimal,
        total_equity: Decimal
    ) -> Decimal:
        """Calculate total ROI = Total Return / Total Equity"""
        if total_equity == 0:
            return Decimal('0')
        return (total_return / total_equity) * 100

    def calculate_approximate_irr(
        self,
        current_value: Decimal,
        annual_cash_flow: Decimal,
        total_equity: Decimal,
        years_held: Decimal
    ) -> Decimal:
        """Calculate approximate IRR"""
        if total_equity == 0 or years_held == 0:
            return Decimal('0')

        # Approximate IRR = ((Current Value + Annual CF) / Equity)^(1/Years) - 1
        try:
            ratio = float((current_value + annual_cash_flow) / total_equity)
            if ratio <= 0:
                return Decimal('0')
            exponent = 1.0 / float(years_held)
            irr = (ratio ** exponent) - 1.0
            return Decimal(str(irr * 100))
        except (ValueError, ZeroDivisionError):
            return Decimal('0')

    def calculate_years_held(
        self,
        purchase_date: date,
        current_date: Optional[date] = None
    ) -> Decimal:
        """Calculate years held"""
        if current_date is None:
            current_date = date.today()
        days_held = (current_date - purchase_date).days
        return Decimal(days_held) / Decimal('365.25')

    # Dashboard alerts

    def get_dashboard_alerts(self) -> Dict[str, Any]:
        """Get all dashboard alerts"""
        return {
            'leases_expiring_60_days': len(self.leases_expiring_soon(60)),
            'critical_leases': len(self.critical_leases()),
            'high_risk_leases': len(self.high_risk_leases()),
            'vacant_units': self.vacant_units(),
            'open_maintenance': len(self.open_maintenance_requests()),
            'emergency_maintenance': len(self.emergency_maintenance()),
        }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get complete portfolio summary"""
        return {
            'total_properties': self.total_properties(),
            'total_units': self.total_units(),
            'occupied_units': self.occupied_units(),
            'vacant_units': self.vacant_units(),
            'physical_occupancy_rate': float(self.physical_occupancy_rate() * 100),
            'portfolio_value': float(self.portfolio_value()),
            'total_equity': float(self.total_equity()),
            'monthly_gpr': float(self.gross_potential_rent_monthly()),
            'monthly_vacancy_loss': float(self.vacancy_loss_monthly()),
            'monthly_egi': float(self.effective_gross_income_monthly()),
            'monthly_noi': float(self.net_operating_income_monthly()),
            'portfolio_cap_rate': float(self.portfolio_cap_rate()),
            'alerts': self.get_dashboard_alerts(),
        }


# Utility functions

def calculate_debt_service_coverage_ratio(noi: Decimal, debt_service: Decimal) -> Decimal:
    """Calculate DSCR = NOI / Debt Service"""
    if debt_service == 0:
        return Decimal('0')
    return noi / debt_service


def calculate_economic_occupancy(
    collected_rent: Decimal,
    gross_potential_rent: Decimal
) -> Decimal:
    """Calculate economic occupancy = Collected Rent / GPR"""
    if gross_potential_rent == 0:
        return Decimal('0')
    return (collected_rent / gross_potential_rent) * 100


def calculate_rent_growth_yoy(
    current_rent: Decimal,
    prior_rent: Decimal
) -> Decimal:
    """Calculate year-over-year rent growth"""
    if prior_rent == 0:
        return Decimal('0')
    return ((current_rent - prior_rent) / prior_rent) * 100


def calculate_operating_expense_ratio(
    operating_expenses: Decimal,
    effective_gross_income: Decimal
) -> Decimal:
    """Calculate OpEx ratio = Total OpEx / EGI"""
    if effective_gross_income == 0:
        return Decimal('0')
    return (operating_expenses / effective_gross_income) * 100


# Example usage
if __name__ == "__main__":
    # Create calculator instance
    calc = PropertyManagementCalculator()

    # Add sample property
    property1 = Property(
        property_id="PROP-001",
        property_name="Maple Apartments",
        address="123 Maple Street",
        city="Portland",
        state="OR",
        property_type=PropertyType.MULTIFAMILY,
        ownership_model=OwnershipModel.FULL_OWNERSHIP,
        total_units=24,
        purchase_price=Decimal('3000000'),
        purchase_date=date(2023, 1, 15),
        current_value=Decimal('3200000'),
        status=PropertyStatus.ACTIVE
    )
    calc.properties.append(property1)

    # Add sample units
    for i in range(1, 25):
        unit = Unit(
            property_id="PROP-001",
            unit_number=f"{i}A",
            unit_type="1BR/1BA",
            status=UnitStatus.OCCUPIED if i <= 22 else UnitStatus.VACANT,
            beds=1,
            baths=Decimal('1'),
            square_footage=650,
            market_rent=Decimal('2500'),
            current_rent=Decimal('2400') if i <= 22 else Decimal('0'),
            tenant_name=f"Tenant {i}" if i <= 22 else None,
            days_vacant=0 if i <= 22 else 15
        )
        calc.units.append(unit)

    # Add sample lease
    lease = Lease(
        property_id="PROP-001",
        unit_number="1A",
        tenant_name="John Smith",
        lease_start_date=date(2024, 3, 1),
        lease_end_date=date(2025, 2, 28),
        monthly_rent=Decimal('2400'),
        security_deposit=Decimal('2400'),
        credit_score=720
    )
    calc.leases.append(lease)

    # Add income statement
    income_stmt = IncomeStatement(
        property_id="PROP-001",
        month=date(2024, 11, 1),
        gross_potential_rent=Decimal('60000'),
        vacancy_loss=Decimal('-5000'),
        other_income=Decimal('500'),
        operating_expenses=Decimal('22000'),
        debt_service=Decimal('15000')
    )
    calc.income_statements.append(income_stmt)

    # Generate portfolio summary
    summary = calc.get_portfolio_summary()

    print("=== PORTFOLIO SUMMARY ===")
    print(f"Total Properties: {summary['total_properties']}")
    print(f"Total Units: {summary['total_units']}")
    print(f"Occupancy Rate: {summary['physical_occupancy_rate']:.1f}%")
    print(f"Portfolio Value: ${summary['portfolio_value']:,.0f}")
    print(f"Monthly NOI: ${summary['monthly_noi']:,.0f}")
    print(f"Portfolio Cap Rate: {summary['portfolio_cap_rate']:.2f}%")
    print(f"\nAlerts:")
    print(f"  - Vacant Units: {summary['alerts']['vacant_units']}")
    print(f"  - Leases Expiring (60 days): {summary['alerts']['leases_expiring_60_days']}")
    print(f"  - Open Maintenance: {summary['alerts']['open_maintenance']}")
