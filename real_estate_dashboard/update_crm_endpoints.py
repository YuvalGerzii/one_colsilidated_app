#!/usr/bin/env python3
"""
Script to update remaining CRM endpoints with company filtering.
This script will add the user_company dependency to all remaining endpoints in crm.py
"""

import re
from pathlib import Path

CRM_FILE = Path("backend/app/api/v1/endpoints/crm.py")

# Endpoints that need to verify parent Deal ownership (deal-related resources)
DEAL_RELATED_ENDPOINTS = [
    # Pattern: (function_name, has_deal_id_param)
    ("create_deal_task", True),
    ("update_task", False),  # Uses task_id
    ("delete_task", False),  # Uses task_id
    ("get_deal_documents", True),
    ("create_deal_document", True),
    ("update_document", False),  # Uses document_id
    ("get_deal_activity", True),
    ("get_deal_score", True),
    ("calculate_deal_score", True),
    ("get_deal_score_history", True),
    ("transition_deal_stage", True),
    ("check_transition_eligibility", True),
    ("create_due_diligence_checklist", True),
    ("pull_comps_for_deal", True),
    ("create_dd_model", True),
    ("get_dd_model", True),
    ("sync_dd_progress", True),
    ("add_dd_finding", True),
]

# Endpoints that work with company-level resources
COMPANY_LEVEL_ENDPOINTS = [
    "get_automation_rules",
    "create_automation_rule",
    "update_automation_rule",
    "delete_automation_rule",
    "get_email_templates",
    "create_email_template",
]

def main():
    content = CRM_FILE.read_text()

    print("CRM Endpoints Update Summary:")
    print("=" * 70)

    # Count total endpoints
    total_endpoints = len(re.findall(r'@router\.(get|post|put|delete|patch)\(', content))

    # Count endpoints with company filtering
    company_filtered = content.count("user_company: tuple[User, Optional[Company]]")

    print(f"Total endpoints: {total_endpoints}")
    print(f"Already updated: {company_filtered}")
    print(f"Remaining: {total_endpoints - company_filtered}")
    print()

    print("Remaining endpoints to update:")
    print("-" * 70)

    # Find all endpoint function names
    endpoint_pattern = r'async def (\w+)\([^)]*db: Session = Depends\(get_db\)[^)]*\)'
    remaining = re.findall(endpoint_pattern, content)

    for i, func_name in enumerate(remaining, 1):
        print(f"{i}. {func_name}")

    print("\nNote: Deal-related endpoints need to verify parent Deal ownership first.")
    print("Company-level endpoints need direct company filtering on their models.")

if __name__ == "__main__":
    main()
