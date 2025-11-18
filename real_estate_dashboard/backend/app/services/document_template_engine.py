"""
Document Template Engine - Internal Implementation
Provides template-based document generation without external APIs
"""

from typing import Dict, List, Optional, Any
from datetime import date, datetime
import re
from enum import Enum


class TemplateCategory(str, Enum):
    """Categories of document templates"""
    PURCHASE_AGREEMENT = "purchase_agreement"
    LEASE_AGREEMENT = "lease_agreement"
    NDA = "nda"
    OPERATING_AGREEMENT = "operating_agreement"
    PROMISSORY_NOTE = "promissory_note"
    DEED = "deed"
    DISCLOSURE = "disclosure"
    ADDENDUM = "addendum"
    ASSIGNMENT = "assignment"
    OPTION_AGREEMENT = "option_agreement"


class ConditionalLogic:
    """Handles conditional logic in templates"""

    @staticmethod
    def evaluate_condition(condition: str, variables: Dict[str, Any]) -> bool:
        """
        Evaluate a conditional expression

        Supported conditions:
        - {{IF variable}} - checks if variable exists and is truthy
        - {{IF variable == value}} - equality check
        - {{IF variable > value}} - comparison
        """
        condition = condition.strip()

        # Simple existence check
        if '==' not in condition and '>' not in condition and '<' not in condition:
            return bool(variables.get(condition))

        # Equality check
        if '==' in condition:
            parts = condition.split('==')
            var_name = parts[0].strip()
            value = parts[1].strip().strip('"\'')
            return str(variables.get(var_name, '')) == value

        # Greater than
        if '>' in condition:
            parts = condition.split('>')
            var_name = parts[0].strip()
            value = float(parts[1].strip())
            return float(variables.get(var_name, 0)) > value

        # Less than
        if '<' in condition:
            parts = condition.split('<')
            var_name = parts[0].strip()
            value = float(parts[1].strip())
            return float(variables.get(var_name, 0)) < value

        return False


class DocumentTemplateEngine:
    """
    Template engine for generating legal documents
    Uses variable substitution and conditional logic
    """

    # Built-in templates
    TEMPLATES = {
        TemplateCategory.NDA: """
NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement ("Agreement") is entered into as of {{effective_date}}, by and between:

{{IF party_type == "company"}}
{{party1_company_name}}, a {{party1_state}} {{party1_entity_type}} ("Disclosing Party")
{{ENDIF}}
{{IF party_type == "individual"}}
{{party1_name}}, an individual ("Disclosing Party")
{{ENDIF}}

and

{{party2_company_name}}, a {{party2_state}} {{party2_entity_type}} ("Receiving Party")

WHEREAS, the Disclosing Party possesses certain confidential information related to {{purpose}};

WHEREAS, the Receiving Party desires to receive such confidential information for the purpose of {{intended_use}};

NOW, THEREFORE, in consideration of the mutual covenants and agreements contained herein, the parties agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION

"Confidential Information" means all information disclosed by the Disclosing Party to the Receiving Party, including but not limited to:
   a) Business plans, strategies, and financial information
   b) Customer and supplier lists
   c) Technical data, trade secrets, and know-how
   d) Real estate investment strategies and property analyses
   e) {{additional_confidential_items}}

2. OBLIGATIONS OF RECEIVING PARTY

The Receiving Party agrees to:
   a) Hold all Confidential Information in strict confidence
   b) Use the Confidential Information solely for {{intended_use}}
   c) Not disclose Confidential Information to third parties without prior written consent
   d) Protect Confidential Information with the same degree of care used for its own confidential information

3. TERM

This Agreement shall remain in effect for {{term_years}} years from the effective date.

{{IF includes_non_compete}}
4. NON-COMPETE

The Receiving Party agrees not to compete with the Disclosing Party in {{non_compete_territory}} for a period of {{non_compete_duration}} following termination of this Agreement.
{{ENDIF}}

{{IF includes_non_solicitation}}
5. NON-SOLICITATION

The Receiving Party agrees not to solicit employees, customers, or suppliers of the Disclosing Party for a period of {{non_solicitation_duration}}.
{{ENDIF}}

6. GOVERNING LAW

This Agreement shall be governed by the laws of the State of {{governing_state}}.

IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written above.

DISCLOSING PARTY:                    RECEIVING PARTY:

{{IF party_type == "company"}}
{{party1_company_name}}              {{party2_company_name}}
{{ENDIF}}

By: _________________________        By: _________________________
Name: {{party1_signer_name}}        Name: {{party2_signer_name}}
Title: {{party1_signer_title}}      Title: {{party2_signer_title}}
Date: ___________________            Date: ___________________
""",

        TemplateCategory.LEASE_AGREEMENT: """
RESIDENTIAL LEASE AGREEMENT

This Lease Agreement ("Lease") is entered into as of {{effective_date}}, between:

LANDLORD: {{landlord_name}}
Address: {{landlord_address}}

TENANT: {{tenant_name}}
Address: {{tenant_current_address}}

PROPERTY ADDRESS: {{property_address}}

1. TERM

The term of this Lease shall be for {{lease_term_months}} months, commencing on {{start_date}} and ending on {{end_date}}.

2. RENT

Tenant agrees to pay monthly rent of ${{monthly_rent}}, due on the {{rent_due_day}} day of each month.

{{IF includes_security_deposit}}
Security Deposit: ${{security_deposit_amount}}
The security deposit shall be held in accordance with {{state}} law and returned within {{deposit_return_days}} days of lease termination.
{{ENDIF}}

{{IF includes_late_fee}}
Late Fee: ${{late_fee_amount}} if rent is not received by the {{late_fee_grace_days}} day of the month.
{{ENDIF}}

3. UTILITIES

{{IF landlord_pays_utilities}}
Landlord shall be responsible for: {{landlord_utilities_list}}
{{ENDIF}}

{{IF tenant_pays_utilities}}
Tenant shall be responsible for: {{tenant_utilities_list}}
{{ENDIF}}

4. USE OF PROPERTY

The Property shall be used exclusively for residential purposes. Tenant shall not:
   a) Sublease the Property without written consent
   b) Conduct any business on the premises{{IF no_pets}}
   c) Keep any pets on the Property{{ENDIF}}{{IF pets_allowed}}
   c) Keep more than {{max_pets}} pets, with a pet deposit of ${{pet_deposit}}{{ENDIF}}
   d) Make alterations without written consent

{{IF includes_parking}}
5. PARKING

Tenant is assigned {{parking_spaces}} parking space(s) at {{parking_location}}.
{{ENDIF}}

{{IF includes_maintenance}}
6. MAINTENANCE AND REPAIRS

Landlord shall maintain: {{landlord_maintenance_items}}
Tenant shall maintain: {{tenant_maintenance_items}}
{{ENDIF}}

7. GOVERNING LAW

This Lease shall be governed by the laws of the State of {{state}}.

LANDLORD:                           TENANT:

_________________________          _________________________
{{landlord_name}}                  {{tenant_name}}
Date: ___________________          Date: ___________________
""",

        TemplateCategory.PURCHASE_AGREEMENT: """
REAL ESTATE PURCHASE AGREEMENT

This Purchase Agreement ("Agreement") is made as of {{effective_date}}, by and between:

SELLER: {{seller_name}}
Address: {{seller_address}}

BUYER: {{buyer_name}}
Address: {{buyer_address}}

PROPERTY: {{property_address}}
Legal Description: {{legal_description}}

1. PURCHASE PRICE

The total purchase price for the Property is ${{purchase_price}}.

Payment Terms:
   a) Earnest Money Deposit: ${{earnest_money}} due within {{earnest_money_days}} days
   b) Down Payment: ${{down_payment}} ({{down_payment_percent}}%)
   {{IF includes_financing}}
   c) Financing: ${{loan_amount}} to be obtained by Buyer
   {{ENDIF}}
   d) Balance due at closing: ${{balance_due}}

{{IF includes_financing}}
2. FINANCING CONTINGENCY

This Agreement is contingent upon Buyer obtaining financing of ${{loan_amount}} at an interest rate not to exceed {{max_interest_rate}}% within {{financing_contingency_days}} days.
{{ENDIF}}

{{IF includes_inspection}}
3. INSPECTION CONTINGENCY

Buyer shall have {{inspection_period_days}} days to conduct inspections. Seller agrees to make repairs up to ${{repair_limit}}.
{{ENDIF}}

{{IF includes_appraisal}}
4. APPRAISAL CONTINGENCY

This Agreement is contingent upon the Property appraising for at least ${{minimum_appraisal_value}}.
{{ENDIF}}

5. CLOSING

Closing shall occur on or before {{closing_date}} at {{closing_location}}.

{{IF seller_pays_closing}}
Seller shall pay: {{seller_closing_costs_list}}
{{ENDIF}}

{{IF buyer_pays_closing}}
Buyer shall pay: {{buyer_closing_costs_list}}
{{ENDIF}}

{{IF includes_title_insurance}}
6. TITLE INSURANCE

Seller shall provide clear title and {{title_insurance_party}} shall pay for title insurance in the amount of ${{title_insurance_amount}}.
{{ENDIF}}

{{IF includes_survey}}
7. SURVEY

A survey of the Property shall be completed at {{survey_party}}'s expense.
{{ENDIF}}

{{IF includes_fixtures}}
8. FIXTURES AND PERSONAL PROPERTY

The following items shall be included in the sale:
{{fixtures_list}}
{{ENDIF}}

9. DISCLOSURES

{{IF lead_paint_disclosure}}
Lead Paint Disclosure: Property was built {{IF built_before_1978}}before{{ENDIF}}{{IF built_after_1978}}after{{ENDIF}} 1978. {{lead_paint_statement}}
{{ENDIF}}

{{IF flood_zone}}
Flood Zone: Property is located in Flood Zone {{flood_zone_designation}}.
{{ENDIF}}

10. GOVERNING LAW

This Agreement shall be governed by the laws of the State of {{state}}.

SELLER:                             BUYER:

_________________________          _________________________
{{seller_name}}                    {{buyer_name}}
Date: ___________________          Date: ___________________
""",

        TemplateCategory.PROMISSORY_NOTE: """
PROMISSORY NOTE

Principal Amount: ${{principal_amount}}
Date: {{note_date}}

FOR VALUE RECEIVED, {{borrower_name}} ("Borrower"), promises to pay to {{lender_name}} ("Lender"), or order, the principal sum of ${{principal_amount}}, together with interest on the unpaid principal balance.

1. INTEREST RATE

Interest shall accrue at the rate of {{interest_rate}}% per annum.

2. PAYMENT TERMS

{{IF payment_type == "monthly"}}
Borrower shall make {{total_payments}} monthly payments of ${{monthly_payment}} beginning on {{first_payment_date}} and continuing on the {{payment_day}} day of each month thereafter until paid in full.
{{ENDIF}}

{{IF payment_type == "balloon"}}
Borrower shall make interest-only payments of ${{interest_payment}} beginning on {{first_payment_date}}. The entire principal balance of ${{principal_amount}} plus any accrued interest shall be due on {{balloon_date}}.
{{ENDIF}}

{{IF payment_type == "lump_sum"}}
The entire amount of ${{total_amount_due}} shall be due and payable on {{maturity_date}}.
{{ENDIF}}

3. PREPAYMENT

{{IF allows_prepayment}}
Borrower may prepay this Note in whole or in part without penalty.
{{ENDIF}}

{{IF prepayment_penalty}}
Prepayment within {{prepayment_penalty_period}} months shall incur a penalty of {{prepayment_penalty_percent}}% of the prepaid amount.
{{ENDIF}}

4. DEFAULT

{{IF includes_late_fee}}
Payments not received within {{grace_period_days}} days of due date shall incur a late fee of ${{late_fee_amount}}.
{{ENDIF}}

Upon default, the entire unpaid balance shall become immediately due and payable. Lender may pursue all legal remedies including foreclosure.

5. SECURITY

{{IF secured}}
This Note is secured by {{security_description}} as described in the {{security_instrument_type}} dated {{security_instrument_date}}.
{{ENDIF}}

{{IF unsecured}}
This Note is unsecured.
{{ENDIF}}

6. GOVERNING LAW

This Note shall be governed by the laws of the State of {{state}}.

BORROWER:

_________________________
{{borrower_name}}
Date: ___________________

{{IF requires_guarantor}}
GUARANTOR:

_________________________
{{guarantor_name}}
Date: ___________________
{{ENDIF}}
"""
    }

    def __init__(self):
        """Initialize the template engine"""
        self.custom_templates: Dict[str, str] = {}

    def add_custom_template(self, name: str, template: str):
        """Add a custom template"""
        self.custom_templates[name] = template

    def substitute_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """
        Substitute variables in template

        Supports:
        - {{variable}} - simple variable substitution
        - {{IF condition}}...{{ENDIF}} - conditional blocks
        """
        result = template

        # Process conditional blocks
        result = self._process_conditionals(result, variables)

        # Substitute simple variables
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            # Format dates
            if isinstance(value, (date, datetime)):
                value = value.strftime("%B %d, %Y")
            # Format numbers
            elif isinstance(value, (int, float)) and '.' not in str(key):
                value = f"{value:,.2f}"

            result = result.replace(placeholder, str(value))

        return result

    def _process_conditionals(self, template: str, variables: Dict[str, Any]) -> str:
        """Process conditional blocks in template"""
        result = template

        # Find all conditional blocks
        pattern = r'\{\{IF\s+([^}]+)\}\}(.*?)\{\{ENDIF\}\}'

        while True:
            match = re.search(pattern, result, re.DOTALL)
            if not match:
                break

            condition = match.group(1)
            block_content = match.group(2)

            # Evaluate condition
            should_include = ConditionalLogic.evaluate_condition(condition, variables)

            # Replace block with content or empty string
            replacement = block_content if should_include else ""
            result = result[:match.start()] + replacement + result[match.end():]

        return result

    def generate_document(
        self,
        template_type: TemplateCategory,
        variables: Dict[str, Any],
        custom_template: Optional[str] = None
    ) -> str:
        """
        Generate a document from template

        Args:
            template_type: Type of template to use
            variables: Dictionary of variables to substitute
            custom_template: Optional custom template string

        Returns:
            Generated document text
        """
        # Get template
        if custom_template:
            template = custom_template
        elif template_type in self.custom_templates:
            template = self.custom_templates[template_type]
        else:
            template = self.TEMPLATES.get(template_type, "")

        if not template:
            raise ValueError(f"No template found for {template_type}")

        # Generate document
        return self.substitute_variables(template, variables)

    def get_template_variables(self, template_type: TemplateCategory) -> List[str]:
        """Extract all variable names from a template"""
        template = self.TEMPLATES.get(template_type, "")

        # Find all {{variable}} patterns
        pattern = r'\{\{([^}IF|ENDIF]+)\}\}'
        matches = re.findall(pattern, template)

        # Clean up and deduplicate
        variables = set()
        for match in matches:
            var = match.strip()
            if var and not var.startswith('IF') and var != 'ENDIF':
                variables.add(var)

        return sorted(list(variables))

    def validate_variables(
        self,
        template_type: TemplateCategory,
        variables: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Validate that all required variables are provided

        Returns:
            Dictionary with 'missing' and 'provided' keys
        """
        required = set(self.get_template_variables(template_type))
        provided = set(variables.keys())

        return {
            'missing': sorted(list(required - provided)),
            'provided': sorted(list(provided)),
            'extra': sorted(list(provided - required))
        }


# Singleton instance
template_engine = DocumentTemplateEngine()
