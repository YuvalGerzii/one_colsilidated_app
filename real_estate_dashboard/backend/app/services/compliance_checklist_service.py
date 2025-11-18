"""
Compliance Checklist Service - Internal Implementation
Generates state-specific and transaction-type compliance checklists
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import date, timedelta


class TransactionType(str, Enum):
    """Types of real estate transactions"""
    PURCHASE = "purchase"
    SALE = "sale"
    LEASE = "lease"
    REFINANCE = "refinance"
    DEVELOPMENT = "development"
    SYNDICATION = "syndication"
    EXCHANGE_1031 = "1031_exchange"
    OPPORTUNITY_ZONE = "opportunity_zone"
    FOREIGN_INVESTMENT = "foreign_investment"


class ChecklistItemStatus(str, Enum):
    """Status of checklist items"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    NOT_APPLICABLE = "not_applicable"


class ChecklistItemPriority(str, Enum):
    """Priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ChecklistItem:
    """Individual checklist item"""
    title: str
    description: str
    category: str
    priority: ChecklistItemPriority
    required: bool
    estimated_days: int
    dependencies: List[str]
    state_specific: bool = False
    statute_reference: Optional[str] = None
    deadline_offset_days: Optional[int] = None  # Days from transaction start


@dataclass
class ComplianceChecklist:
    """Complete compliance checklist"""
    transaction_type: TransactionType
    state: str
    items: List[ChecklistItem]
    estimated_total_days: int
    critical_path: List[str]


class ComplianceChecklistService:
    """
    Service for generating compliance checklists
    Includes state-specific requirements
    """

    # State-specific disclosure requirements
    STATE_DISCLOSURES = {
        "California": [
            ChecklistItem(
                title="Natural Hazard Disclosure",
                description="Provide Natural Hazard Disclosure (NHD) Statement including earthquake, flood, fire, and environmental hazards",
                category="Disclosures",
                priority=ChecklistItemPriority.CRITICAL,
                required=True,
                estimated_days=3,
                dependencies=[],
                state_specific=True,
                statute_reference="California Civil Code §1103",
                deadline_offset_days=5
            ),
            ChecklistItem(
                title="Mello-Roos Disclosure",
                description="Disclose Mello-Roos special tax assessments and Community Facilities Districts",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=2,
                dependencies=[],
                state_specific=True,
                statute_reference="California Government Code §53341"
            ),
            ChecklistItem(
                title="Transfer Disclosure Statement (TDS)",
                description="Complete Transfer Disclosure Statement for residential 1-4 units",
                category="Disclosures",
                priority=ChecklistItemPriority.CRITICAL,
                required=True,
                estimated_days=3,
                dependencies=[],
                state_specific=True,
                statute_reference="California Civil Code §1102"
            ),
            ChecklistItem(
                title="Water Conserving Fixtures",
                description="Certify installation of water-conserving plumbing fixtures",
                category="Compliance",
                priority=ChecklistItemPriority.MEDIUM,
                required=True,
                estimated_days=1,
                dependencies=[],
                state_specific=True,
                statute_reference="California Civil Code §1101.1-1101.9"
            )
        ],
        "New York": [
            ChecklistItem(
                title="Property Condition Disclosure Statement",
                description="Complete Property Condition Disclosure Statement (PCDS)",
                category="Disclosures",
                priority=ChecklistItemPriority.CRITICAL,
                required=True,
                estimated_days=3,
                dependencies=[],
                state_specific=True,
                statute_reference="NY Real Property Law §462"
            ),
            ChecklistItem(
                title="Cooperative/Condo Offering Plan",
                description="Provide offering plan and board approval requirements",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=5,
                dependencies=[],
                state_specific=True,
                statute_reference="NY General Business Law §352-e"
            ),
            ChecklistItem(
                title="NYC HPD Violations",
                description="Disclose all Department of Housing Preservation & Development violations",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=2,
                dependencies=[],
                state_specific=True
            )
        ],
        "Florida": [
            ChecklistItem(
                title="Property Tax Disclosure",
                description="Provide property tax disclosure summary as required by Florida law",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=2,
                dependencies=[],
                state_specific=True,
                statute_reference="Florida Statutes §689.261"
            ),
            ChecklistItem(
                title="Radon Gas Disclosure",
                description="Provide radon gas hazard information statement",
                category="Disclosures",
                priority=ChecklistItemPriority.MEDIUM,
                required=True,
                estimated_days=1,
                dependencies=[],
                state_specific=True,
                statute_reference="Florida Statutes §404.056"
            ),
            ChecklistItem(
                title="Homeowners Association Disclosure",
                description="Provide HOA/condominium documents and governing documents",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=3,
                dependencies=[],
                state_specific=True,
                statute_reference="Florida Statutes §720.401"
            )
        ],
        "Texas": [
            ChecklistItem(
                title="Seller's Disclosure Notice",
                description="Complete Seller's Disclosure of Property Condition (TREC form)",
                category="Disclosures",
                priority=ChecklistItemPriority.CRITICAL,
                required=True,
                estimated_days=3,
                dependencies=[],
                state_specific=True,
                statute_reference="Texas Property Code §5.008"
            ),
            ChecklistItem(
                title="Addendum for Property Subject to Mandatory Membership",
                description="Disclose property owner's association requirements and fees",
                category="Disclosures",
                priority=ChecklistItemPriority.HIGH,
                required=True,
                estimated_days=2,
                dependencies=[],
                state_specific=True,
                statute_reference="Texas Property Code §207.003"
            ),
            ChecklistItem(
                title="Coastal Area Property Disclosure",
                description="Provide disclosure for properties in coastal areas (if applicable)",
                category="Disclosures",
                priority=ChecklistItemPriority.MEDIUM,
                required=False,
                estimated_days=1,
                dependencies=[],
                state_specific=True,
                statute_reference="Texas Natural Resources Code §33.135"
            )
        ]
    }

    # Universal checklist items for purchase transactions
    UNIVERSAL_PURCHASE_ITEMS = [
        ChecklistItem(
            title="Title Search and Examination",
            description="Conduct comprehensive title search and examination for liens, encumbrances, and defects",
            category="Title",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=7,
            dependencies=[],
            deadline_offset_days=10
        ),
        ChecklistItem(
            title="Title Insurance Commitment",
            description="Obtain title insurance commitment and review all exceptions",
            category="Title",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=5,
            dependencies=["Title Search and Examination"]
        ),
        ChecklistItem(
            title="Survey",
            description="Order and review current ALTA survey showing boundaries, easements, and improvements",
            category="Due Diligence",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=10,
            dependencies=[],
            deadline_offset_days=15
        ),
        ChecklistItem(
            title="Phase I Environmental Assessment",
            description="Conduct Phase I Environmental Site Assessment for environmental contamination",
            category="Due Diligence",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=14,
            dependencies=[],
            deadline_offset_days=20
        ),
        ChecklistItem(
            title="Property Inspection",
            description="Complete comprehensive property inspection including structural, mechanical, and electrical systems",
            category="Due Diligence",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=5,
            dependencies=[],
            deadline_offset_days=10
        ),
        ChecklistItem(
            title="Zoning Verification",
            description="Verify current zoning and confirm intended use is permitted",
            category="Compliance",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=3,
            dependencies=[]
        ),
        ChecklistItem(
            title="Certificate of Occupancy",
            description="Verify valid certificate of occupancy for all buildings",
            category="Compliance",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=2,
            dependencies=[]
        ),
        ChecklistItem(
            title="Financial Records Review",
            description="Review operating statements, rent rolls, and property financials for past 3 years",
            category="Financial Due Diligence",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=7,
            dependencies=[]
        ),
        ChecklistItem(
            title="Lease Review",
            description="Review all tenant leases and service contracts",
            category="Legal",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=5,
            dependencies=[]
        ),
        ChecklistItem(
            title="Lead Paint Disclosure",
            description="Provide lead-based paint disclosure for properties built before 1978",
            category="Disclosures",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=[],
            statute_reference="42 U.S.C. §4852d"
        ),
        ChecklistItem(
            title="Financing Approval",
            description="Obtain loan commitment and satisfy all lending conditions",
            category="Financing",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=30,
            dependencies=["Property Inspection", "Phase I Environmental Assessment"],
            deadline_offset_days=45
        ),
        ChecklistItem(
            title="Insurance Binders",
            description="Obtain property and liability insurance binders",
            category="Insurance",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=3,
            dependencies=[]
        ),
        ChecklistItem(
            title="Entity Formation",
            description="Form acquisition entity (LLC/LP) if applicable",
            category="Legal",
            priority=ChecklistItemPriority.HIGH,
            required=False,
            estimated_days=7,
            dependencies=[]
        ),
        ChecklistItem(
            title="Estoppel Certificates",
            description="Obtain tenant estoppel certificates",
            category="Legal",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=10,
            dependencies=["Lease Review"]
        ),
        ChecklistItem(
            title="SNDA Agreements",
            description="Obtain subordination, non-disturbance, and attornment agreements from major tenants",
            category="Legal",
            priority=ChecklistItemPriority.MEDIUM,
            required=False,
            estimated_days=14,
            dependencies=["Lease Review"]
        ),
        ChecklistItem(
            title="Purchase Agreement",
            description="Draft and negotiate purchase and sale agreement",
            category="Legal",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=5,
            dependencies=[],
            deadline_offset_days=3
        ),
        ChecklistItem(
            title="Closing Documents",
            description="Prepare all closing documents including deed, bill of sale, and assignment and assumption agreements",
            category="Closing",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=7,
            dependencies=["Purchase Agreement"]
        )
    ]

    # 1031 Exchange specific items
    EXCHANGE_1031_ITEMS = [
        ChecklistItem(
            title="Qualified Intermediary Engagement",
            description="Engage qualified intermediary (QI) before closing on relinquished property",
            category="1031 Exchange",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=3,
            dependencies=[],
            deadline_offset_days=0,
            statute_reference="IRC §1031"
        ),
        ChecklistItem(
            title="Exchange Agreement",
            description="Execute exchange agreement with qualified intermediary",
            category="1031 Exchange",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=2,
            dependencies=["Qualified Intermediary Engagement"],
            deadline_offset_days=0
        ),
        ChecklistItem(
            title="45-Day Identification",
            description="Identify replacement property(ies) within 45 days of closing on relinquished property",
            category="1031 Exchange",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=["Exchange Agreement"],
            deadline_offset_days=45,
            statute_reference="IRC §1031(a)(3)(A)"
        ),
        ChecklistItem(
            title="180-Day Exchange Period",
            description="Complete acquisition of replacement property within 180 days or tax return due date, whichever is earlier",
            category="1031 Exchange",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=["45-Day Identification"],
            deadline_offset_days=180,
            statute_reference="IRC §1031(a)(3)(B)"
        ),
        ChecklistItem(
            title="Like-Kind Verification",
            description="Verify replacement property qualifies as like-kind property",
            category="1031 Exchange",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=2,
            dependencies=[]
        ),
        ChecklistItem(
            title="Boot Calculation",
            description="Calculate and minimize any boot (cash or non-like-kind property received)",
            category="1031 Exchange",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=2,
            dependencies=[]
        ),
        ChecklistItem(
            title="Form 8824",
            description="Prepare Form 8824 (Like-Kind Exchanges) for tax filing",
            category="1031 Exchange",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=3,
            dependencies=["180-Day Exchange Period"]
        )
    ]

    # Opportunity Zone investment items
    OPPORTUNITY_ZONE_ITEMS = [
        ChecklistItem(
            title="Qualified Opportunity Zone Verification",
            description="Verify property is located in a designated Qualified Opportunity Zone",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=[],
            statute_reference="IRC §1400Z-2"
        ),
        ChecklistItem(
            title="QOF Formation",
            description="Form Qualified Opportunity Fund (QOF) entity - corporation or partnership",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=7,
            dependencies=[],
            deadline_offset_days=30
        ),
        ChecklistItem(
            title="180-Day Investment Period",
            description="Invest capital gains in QOF within 180 days of gain realization",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=["QOF Formation"],
            deadline_offset_days=180,
            statute_reference="IRC §1400Z-2(a)(1)(A)"
            ),
        ChecklistItem(
            title="90% Asset Test",
            description="Ensure QOF holds at least 90% of assets in qualified opportunity zone property",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=2,
            dependencies=["QOF Formation"]
        ),
        ChecklistItem(
            title="Substantial Improvement Requirement",
            description="Verify property improvement plan meets substantial improvement requirement (double basis within 30 months)",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=5,
            dependencies=[]
        ),
        ChecklistItem(
            title="Form 8996",
            description="File Form 8996 (Qualified Opportunity Fund) annually",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=2,
            dependencies=["QOF Formation"]
        ),
        ChecklistItem(
            title="Form 8997",
            description="File Form 8997 (Initial and Annual Statement of Qualified Opportunity Fund Investments)",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.HIGH,
            required=True,
            estimated_days=2,
            dependencies=["180-Day Investment Period"]
        ),
        ChecklistItem(
            title="10-Year Holding Period Tracking",
            description="Establish tracking system for 5, 7, and 10-year holding period milestones",
            category="Opportunity Zone",
            priority=ChecklistItemPriority.MEDIUM,
            required=True,
            estimated_days=1,
            dependencies=["180-Day Investment Period"]
        )
    ]

    # Foreign investment (FIRPTA) items
    FOREIGN_INVESTMENT_ITEMS = [
        ChecklistItem(
            title="Foreign Person Status Determination",
            description="Determine if seller is a foreign person under FIRPTA",
            category="FIRPTA",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=2,
            dependencies=[],
            statute_reference="IRC §1445"
        ),
        ChecklistItem(
            title="Withholding Certificate Application",
            description="Apply for withholding certificate if reduced/no withholding is appropriate",
            category="FIRPTA",
            priority=ChecklistItemPriority.HIGH,
            required=False,
            estimated_days=90,
            dependencies=["Foreign Person Status Determination"]
        ),
        ChecklistItem(
            title="15% Withholding Calculation",
            description="Calculate 15% withholding requirement on gross sales price (or 10% if under $1M residential)",
            category="FIRPTA",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=1,
            dependencies=["Foreign Person Status Determination"]
        ),
        ChecklistItem(
            title="Form 8288 and 8288-A",
            description="Prepare and file Forms 8288 and 8288-A with IRS within 20 days of closing",
            category="FIRPTA",
            priority=ChecklistItemPriority.CRITICAL,
            required=True,
            estimated_days=3,
            dependencies=["15% Withholding Calculation"],
            deadline_offset_days=20,
            statute_reference="IRC §1445(e)"
        ),
        ChecklistItem(
            title="FinCEN Reporting",
            description="File FinCEN Form 8300 if cash payments exceed $10,000",
            category="FIRPTA",
            priority=ChecklistItemPriority.HIGH,
            required=False,
            estimated_days=2,
            dependencies=[],
            deadline_offset_days=15
        )
    ]

    def __init__(self):
        """Initialize compliance checklist service"""
        pass

    def generate_checklist(
        self,
        transaction_type: TransactionType,
        state: str,
        include_optional: bool = False
    ) -> ComplianceChecklist:
        """
        Generate compliance checklist for a transaction

        Args:
            transaction_type: Type of transaction
            state: State where transaction occurs
            include_optional: Whether to include optional items

        Returns:
            Complete compliance checklist
        """
        items = []

        # Add universal items based on transaction type
        if transaction_type == TransactionType.PURCHASE:
            items.extend(self.UNIVERSAL_PURCHASE_ITEMS)

        # Add transaction-specific items
        if transaction_type == TransactionType.EXCHANGE_1031:
            items.extend(self.UNIVERSAL_PURCHASE_ITEMS)
            items.extend(self.EXCHANGE_1031_ITEMS)

        if transaction_type == TransactionType.OPPORTUNITY_ZONE:
            items.extend(self.UNIVERSAL_PURCHASE_ITEMS)
            items.extend(self.OPPORTUNITY_ZONE_ITEMS)

        if transaction_type == TransactionType.FOREIGN_INVESTMENT:
            items.extend(self.UNIVERSAL_PURCHASE_ITEMS)
            items.extend(self.FOREIGN_INVESTMENT_ITEMS)

        # Add state-specific items
        if state in self.STATE_DISCLOSURES:
            items.extend(self.STATE_DISCLOSURES[state])

        # Filter optional items if requested
        if not include_optional:
            items = [item for item in items if item.required]

        # Calculate estimated timeline
        estimated_days = self._calculate_timeline(items)

        # Determine critical path
        critical_path = self._find_critical_path(items)

        return ComplianceChecklist(
            transaction_type=transaction_type,
            state=state,
            items=items,
            estimated_total_days=estimated_days,
            critical_path=critical_path
        )

    def _calculate_timeline(self, items: List[ChecklistItem]) -> int:
        """Calculate total estimated timeline"""
        # Build dependency graph
        item_dict = {item.title: item for item in items}
        completion_times = {}

        def calculate_completion_time(item_title: str) -> int:
            if item_title in completion_times:
                return completion_times[item_title]

            item = item_dict.get(item_title)
            if not item:
                return 0

            # Calculate based on dependencies
            max_dependency_time = 0
            for dep in item.dependencies:
                dep_time = calculate_completion_time(dep)
                max_dependency_time = max(max_dependency_time, dep_time)

            total_time = max_dependency_time + item.estimated_days
            completion_times[item_title] = total_time
            return total_time

        # Calculate for all items
        for item in items:
            calculate_completion_time(item.title)

        # Return the maximum completion time
        return max(completion_times.values()) if completion_times else 0

    def _find_critical_path(self, items: List[ChecklistItem]) -> List[str]:
        """Find critical path through checklist items"""
        # Build dependency graph
        item_dict = {item.title: item for item in items}
        completion_times = {}
        paths = {}

        def calculate_path(item_title: str) -> tuple[int, List[str]]:
            if item_title in paths:
                return completion_times[item_title], paths[item_title]

            item = item_dict.get(item_title)
            if not item:
                return 0, []

            # Find longest path through dependencies
            max_time = 0
            longest_path = []

            for dep in item.dependencies:
                dep_time, dep_path = calculate_path(dep)
                if dep_time > max_time:
                    max_time = dep_time
                    longest_path = dep_path.copy()

            total_time = max_time + item.estimated_days
            current_path = longest_path + [item_title]

            completion_times[item_title] = total_time
            paths[item_title] = current_path

            return total_time, current_path

        # Find the longest path
        longest_time = 0
        critical_path = []

        for item in items:
            time, path = calculate_path(item.title)
            if time > longest_time:
                longest_time = time
                critical_path = path

        return critical_path

    def get_state_specific_requirements(self, state: str) -> List[ChecklistItem]:
        """Get state-specific requirements for a state"""
        return self.STATE_DISCLOSURES.get(state, [])

    def calculate_deadlines(
        self,
        checklist: ComplianceChecklist,
        start_date: date
    ) -> Dict[str, date]:
        """
        Calculate actual deadlines for checklist items

        Args:
            checklist: The compliance checklist
            start_date: Transaction start/contract date

        Returns:
            Dictionary mapping item titles to deadline dates
        """
        deadlines = {}

        for item in checklist.items:
            if item.deadline_offset_days is not None:
                deadline = start_date + timedelta(days=item.deadline_offset_days)
                deadlines[item.title] = deadline

        return deadlines


# Singleton instance
compliance_checklist_service = ComplianceChecklistService()
