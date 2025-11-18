"""
Deadline Calculator - Internal Implementation
Calculates legal deadlines based on statutes of limitations and transaction milestones
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import date, datetime, timedelta
import calendar


class DeadlineType(str, Enum):
    """Types of legal deadlines"""
    CONTRACT = "contract"
    STATUTE_OF_LIMITATIONS = "statute_of_limitations"
    REGULATORY = "regulatory"
    FILING = "filing"
    NOTICE = "notice"
    INSPECTION = "inspection"
    FINANCING = "financing"


class ClaimType(str, Enum):
    """Types of legal claims for statute of limitations"""
    BREACH_OF_CONTRACT = "breach_of_contract"
    FRAUD = "fraud"
    NEGLIGENCE = "negligence"
    PERSONAL_INJURY = "personal_injury"
    PROPERTY_DAMAGE = "property_damage"
    CONSTRUCTION_DEFECT = "construction_defect"
    PROFESSIONAL_MALPRACTICE = "professional_malpractice"
    WRONGFUL_TERMINATION = "wrongful_termination"


@dataclass
class Deadline:
    """Represents a calculated deadline"""
    name: str
    deadline_type: DeadlineType
    deadline_date: date
    trigger_date: date
    trigger_event: str
    days_from_trigger: int
    business_days: bool = False
    statute_reference: Optional[str] = None
    consequences_of_missing: str = ""
    reminder_days_before: int = 7


class DeadlineCalculator:
    """
    Service for calculating legal and transaction deadlines
    No external APIs required
    """

    # Statute of limitations periods by state (in years)
    STATUTE_OF_LIMITATIONS = {
        "California": {
            ClaimType.BREACH_OF_CONTRACT: 4,  # Written contract
            ClaimType.FRAUD: 3,
            ClaimType.NEGLIGENCE: 2,
            ClaimType.PERSONAL_INJURY: 2,
            ClaimType.PROPERTY_DAMAGE: 3,
            ClaimType.CONSTRUCTION_DEFECT: 4,  # From substantial completion
            ClaimType.PROFESSIONAL_MALPRACTICE: 1,  # Or 3 years from injury, whichever is first
        },
        "New York": {
            ClaimType.BREACH_OF_CONTRACT: 6,  # Written contract
            ClaimType.FRAUD: 6,
            ClaimType.NEGLIGENCE: 3,
            ClaimType.PERSONAL_INJURY: 3,
            ClaimType.PROPERTY_DAMAGE: 3,
            ClaimType.CONSTRUCTION_DEFECT: 6,
            ClaimType.PROFESSIONAL_MALPRACTICE: 3,
        },
        "Florida": {
            ClaimType.BREACH_OF_CONTRACT: 5,  # Written contract
            ClaimType.FRAUD: 4,
            ClaimType.NEGLIGENCE: 4,
            ClaimType.PERSONAL_INJURY: 4,
            ClaimType.PROPERTY_DAMAGE: 4,
            ClaimType.CONSTRUCTION_DEFECT: 4,  # From substantial completion, max 10 years
            ClaimType.PROFESSIONAL_MALPRACTICE: 2,
        },
        "Texas": {
            ClaimType.BREACH_OF_CONTRACT: 4,  # Written contract
            ClaimType.FRAUD: 4,
            ClaimType.NEGLIGENCE: 2,
            ClaimType.PERSONAL_INJURY: 2,
            ClaimType.PROPERTY_DAMAGE: 2,
            ClaimType.CONSTRUCTION_DEFECT: 4,
            ClaimType.PROFESSIONAL_MALPRACTICE: 2,
        },
        "Illinois": {
            ClaimType.BREACH_OF_CONTRACT: 10,  # Written contract
            ClaimType.FRAUD: 5,
            ClaimType.NEGLIGENCE: 2,
            ClaimType.PERSONAL_INJURY: 2,
            ClaimType.PROPERTY_DAMAGE: 5,
            ClaimType.CONSTRUCTION_DEFECT: 4,
            ClaimType.PROFESSIONAL_MALPRACTICE: 2,
        }
    }

    def __init__(self):
        """Initialize deadline calculator"""
        pass

    def add_business_days(self, start_date: date, days: int) -> date:
        """
        Add business days (excluding weekends) to a date

        Args:
            start_date: Starting date
            days: Number of business days to add

        Returns:
            Calculated date
        """
        current_date = start_date
        days_added = 0

        while days_added < days:
            current_date += timedelta(days=1)
            # Skip weekends (5 = Saturday, 6 = Sunday)
            if current_date.weekday() < 5:
                days_added += 1

        return current_date

    def add_calendar_days(self, start_date: date, days: int) -> date:
        """Add calendar days to a date"""
        return start_date + timedelta(days=days)

    def calculate_statute_of_limitations(
        self,
        claim_type: ClaimType,
        state: str,
        trigger_date: date,
        trigger_event: str = "Date of incident"
    ) -> Deadline:
        """
        Calculate statute of limitations deadline

        Args:
            claim_type: Type of legal claim
            state: State where claim arises
            trigger_date: Date when claim accrued
            trigger_event: Description of triggering event

        Returns:
            Deadline object
        """
        # Get statute period for state and claim type
        state_statutes = self.STATUTE_OF_LIMITATIONS.get(state, {})
        years = state_statutes.get(claim_type, 4)  # Default to 4 years

        # Calculate deadline
        deadline_date = date(
            trigger_date.year + years,
            trigger_date.month,
            trigger_date.day
        )

        # Adjust if falls on weekend
        while deadline_date.weekday() >= 5:
            deadline_date += timedelta(days=1)

        return Deadline(
            name=f"Statute of Limitations - {claim_type.value.replace('_', ' ').title()}",
            deadline_type=DeadlineType.STATUTE_OF_LIMITATIONS,
            deadline_date=deadline_date,
            trigger_date=trigger_date,
            trigger_event=trigger_event,
            days_from_trigger=years * 365,
            business_days=False,
            consequences_of_missing="Claim will be time-barred and cannot be filed",
            reminder_days_before=90
        )

    def calculate_1031_exchange_deadlines(
        self,
        relinquished_property_closing_date: date
    ) -> List[Deadline]:
        """
        Calculate deadlines for 1031 exchange

        Args:
            relinquished_property_closing_date: Date when relinquished property closes

        Returns:
            List of deadline objects
        """
        deadlines = []

        # 45-day identification period
        identification_deadline = self.add_calendar_days(
            relinquished_property_closing_date, 45
        )

        deadlines.append(Deadline(
            name="1031 Exchange - 45-Day Identification Period",
            deadline_type=DeadlineType.REGULATORY,
            deadline_date=identification_deadline,
            trigger_date=relinquished_property_closing_date,
            trigger_event="Closing of relinquished property",
            days_from_trigger=45,
            business_days=False,
            statute_reference="IRC §1031(a)(3)(A)",
            consequences_of_missing="Exchange will fail; capital gains tax will be owed",
            reminder_days_before=14
        ))

        # 180-day exchange period
        exchange_deadline = self.add_calendar_days(
            relinquished_property_closing_date, 180
        )

        deadlines.append(Deadline(
            name="1031 Exchange - 180-Day Exchange Period",
            deadline_type=DeadlineType.REGULATORY,
            deadline_date=exchange_deadline,
            trigger_date=relinquished_property_closing_date,
            trigger_event="Closing of relinquished property",
            days_from_trigger=180,
            business_days=False,
            statute_reference="IRC §1031(a)(3)(B)",
            consequences_of_missing="Exchange will fail; capital gains tax will be owed",
            reminder_days_before=30
        ))

        return deadlines

    def calculate_opportunity_zone_deadlines(
        self,
        capital_gain_realization_date: date
    ) -> List[Deadline]:
        """
        Calculate deadlines for Opportunity Zone investment

        Args:
            capital_gain_realization_date: Date when capital gain was realized

        Returns:
            List of deadline objects
        """
        deadlines = []

        # 180-day investment period
        investment_deadline = self.add_calendar_days(
            capital_gain_realization_date, 180
        )

        deadlines.append(Deadline(
            name="Opportunity Zone - 180-Day Investment Period",
            deadline_type=DeadlineType.REGULATORY,
            deadline_date=investment_deadline,
            trigger_date=capital_gain_realization_date,
            trigger_event="Realization of capital gain",
            days_from_trigger=180,
            business_days=False,
            statute_reference="IRC §1400Z-2(a)(1)(A)",
            consequences_of_missing="Cannot defer capital gain through Opportunity Zone investment",
            reminder_days_before=30
        ))

        # 5-year holding milestone (10% basis step-up - no longer available for new investments)
        five_year = date(
            capital_gain_realization_date.year + 5,
            capital_gain_realization_date.month,
            capital_gain_realization_date.day
        )

        # 7-year holding milestone (15% total basis step-up - no longer available for new investments)
        seven_year = date(
            capital_gain_realization_date.year + 7,
            capital_gain_realization_date.month,
            capital_gain_realization_date.day
        )

        # 10-year holding milestone (permanent exclusion of appreciation)
        ten_year = date(
            capital_gain_realization_date.year + 10,
            capital_gain_realization_date.month,
            capital_gain_realization_date.day
        )

        deadlines.append(Deadline(
            name="Opportunity Zone - 10-Year Holding Period for Full Benefit",
            deadline_type=DeadlineType.REGULATORY,
            deadline_date=ten_year,
            trigger_date=capital_gain_realization_date,
            trigger_event="Investment in Qualified Opportunity Fund",
            days_from_trigger=3650,
            business_days=False,
            statute_reference="IRC §1400Z-2(c)",
            consequences_of_missing="Cannot exclude appreciation from capital gains",
            reminder_days_before=90
        ))

        return deadlines

    def calculate_purchase_contract_deadlines(
        self,
        contract_date: date,
        contingencies: Dict[str, int]
    ) -> List[Deadline]:
        """
        Calculate deadlines for purchase contract contingencies

        Args:
            contract_date: Date contract was executed
            contingencies: Dictionary of contingency names and periods (in days)
                Example: {"inspection": 10, "financing": 30, "appraisal": 15}

        Returns:
            List of deadline objects
        """
        deadlines = []

        for contingency_name, days in contingencies.items():
            deadline_date = self.add_calendar_days(contract_date, days)

            deadlines.append(Deadline(
                name=f"{contingency_name.title()} Contingency",
                deadline_type=DeadlineType.CONTRACT,
                deadline_date=deadline_date,
                trigger_date=contract_date,
                trigger_event="Contract execution",
                days_from_trigger=days,
                business_days=False,
                consequences_of_missing=f"{contingency_name.title()} contingency will be waived",
                reminder_days_before=3
            ))

        return deadlines

    def calculate_lease_notice_deadlines(
        self,
        lease_end_date: date,
        notice_period_days: int,
        notice_type: str = "Lease Non-Renewal"
    ) -> Deadline:
        """
        Calculate notice deadline for lease termination/renewal

        Args:
            lease_end_date: Date when lease expires
            notice_period_days: Required notice period in days
            notice_type: Type of notice

        Returns:
            Deadline object
        """
        notice_deadline = lease_end_date - timedelta(days=notice_period_days)

        return Deadline(
            name=f"{notice_type} Notice Deadline",
            deadline_type=DeadlineType.NOTICE,
            deadline_date=notice_deadline,
            trigger_date=lease_end_date,
            trigger_event="Lease expiration date",
            days_from_trigger=-notice_period_days,  # Negative because it's before lease end
            business_days=False,
            consequences_of_missing="Lease may automatically renew or convert to month-to-month",
            reminder_days_before=14
        )

    def calculate_firpta_deadline(
        self,
        closing_date: date
    ) -> Deadline:
        """
        Calculate FIRPTA filing deadline

        Args:
            closing_date: Date of property closing

        Returns:
            Deadline object
        """
        filing_deadline = self.add_calendar_days(closing_date, 20)

        return Deadline(
            name="FIRPTA Withholding Filing (Forms 8288/8288-A)",
            deadline_type=DeadlineType.FILING,
            deadline_date=filing_deadline,
            trigger_date=closing_date,
            trigger_event="Property closing with foreign seller",
            days_from_trigger=20,
            business_days=False,
            statute_reference="IRC §1445(e)",
            consequences_of_missing="Penalties and interest may apply; buyer may be liable for unpaid tax",
            reminder_days_before=7
        )

    def calculate_inspection_deadlines(
        self,
        contract_date: date,
        inspection_period_days: int
    ) -> List[Deadline]:
        """
        Calculate inspection-related deadlines

        Args:
            contract_date: Contract execution date
            inspection_period_days: Inspection period in days

        Returns:
            List of deadline objects
        """
        deadlines = []

        # Inspection completion deadline
        inspection_deadline = self.add_calendar_days(contract_date, inspection_period_days)

        deadlines.append(Deadline(
            name="Property Inspection Period",
            deadline_type=DeadlineType.INSPECTION,
            deadline_date=inspection_deadline,
            trigger_date=contract_date,
            trigger_event="Contract execution",
            days_from_trigger=inspection_period_days,
            business_days=False,
            consequences_of_missing="Inspection contingency waived",
            reminder_days_before=3
        ))

        # Typically, repair request deadline is same as inspection period
        deadlines.append(Deadline(
            name="Repair Request Deadline",
            deadline_type=DeadlineType.INSPECTION,
            deadline_date=inspection_deadline,
            trigger_date=contract_date,
            trigger_event="Contract execution",
            days_from_trigger=inspection_period_days,
            business_days=False,
            consequences_of_missing="Cannot request repairs; must accept property as-is",
            reminder_days_before=3
        ))

        return deadlines

    def days_until_deadline(self, deadline_date: date) -> int:
        """Calculate days remaining until deadline"""
        today = date.today()
        delta = deadline_date - today
        return delta.days

    def is_approaching(self, deadline: Deadline) -> bool:
        """Check if deadline is approaching (within reminder period)"""
        days_until = self.days_until_deadline(deadline.deadline_date)
        return 0 <= days_until <= deadline.reminder_days_before

    def is_overdue(self, deadline: Deadline) -> bool:
        """Check if deadline has passed"""
        return self.days_until_deadline(deadline.deadline_date) < 0

    def get_deadline_status(self, deadline: Deadline) -> str:
        """Get status string for deadline"""
        days_until = self.days_until_deadline(deadline.deadline_date)

        if days_until < 0:
            return f"OVERDUE by {abs(days_until)} days"
        elif days_until == 0:
            return "DUE TODAY"
        elif days_until <= deadline.reminder_days_before:
            return f"APPROACHING - {days_until} days remaining"
        else:
            return f"{days_until} days remaining"


# Singleton instance
deadline_calculator = DeadlineCalculator()
