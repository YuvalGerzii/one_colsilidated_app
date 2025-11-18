"""
Accounting Templates and Configurations

This module provides default chart of accounts templates and tax benefit guides
for different entity types and industries.
"""

from typing import Dict, List, Any


# ============================================================================
# Chart of Accounts Templates
# ============================================================================

CHART_OF_ACCOUNTS_TEMPLATES = {
    "small_business": {
        "name": "Small Business - Standard",
        "description": "Basic chart of accounts for small businesses",
        "accounts": [
            # Assets (1000-1999)
            {"number": "1000", "name": "Cash", "type": "asset", "subtype": "cash"},
            {"number": "1010", "name": "Checking Account", "type": "asset", "subtype": "cash", "parent": "1000"},
            {"number": "1020", "name": "Savings Account", "type": "asset", "subtype": "cash", "parent": "1000"},
            {"number": "1100", "name": "Accounts Receivable", "type": "asset", "subtype": "accounts_receivable"},
            {"number": "1200", "name": "Inventory", "type": "asset", "subtype": "inventory"},
            {"number": "1500", "name": "Fixed Assets", "type": "asset", "subtype": "fixed_asset"},
            {"number": "1510", "name": "Equipment", "type": "asset", "subtype": "fixed_asset", "parent": "1500"},
            {"number": "1520", "name": "Furniture", "type": "asset", "subtype": "fixed_asset", "parent": "1500"},

            # Liabilities (2000-2999)
            {"number": "2000", "name": "Accounts Payable", "type": "liability", "subtype": "accounts_payable"},
            {"number": "2100", "name": "Credit Cards", "type": "liability", "subtype": "current_liability"},
            {"number": "2500", "name": "Loans Payable", "type": "liability", "subtype": "loans_payable"},
            {"number": "2600", "name": "Mortgage Payable", "type": "liability", "subtype": "mortgage_payable"},

            # Equity (3000-3999)
            {"number": "3000", "name": "Owner's Equity", "type": "equity", "subtype": "owner_equity"},
            {"number": "3900", "name": "Retained Earnings", "type": "equity", "subtype": "retained_earnings"},

            # Revenue (4000-4999)
            {"number": "4000", "name": "Sales Revenue", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4100", "name": "Service Revenue", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4900", "name": "Other Income", "type": "revenue", "subtype": "other_income"},

            # Expenses (5000-9999)
            {"number": "5000", "name": "Cost of Goods Sold", "type": "expense", "subtype": "cost_of_goods_sold"},
            {"number": "6000", "name": "Operating Expenses", "type": "expense", "subtype": "operating_expense"},
            {"number": "6100", "name": "Salaries & Wages", "type": "expense", "subtype": "operating_expense"},
            {"number": "6200", "name": "Rent Expense", "type": "expense", "subtype": "operating_expense"},
            {"number": "6300", "name": "Utilities", "type": "expense", "subtype": "utilities"},
            {"number": "6400", "name": "Insurance", "type": "expense", "subtype": "insurance"},
            {"number": "6500", "name": "Advertising & Marketing", "type": "expense", "subtype": "advertising"},
            {"number": "6600", "name": "Professional Fees", "type": "expense", "subtype": "legal_professional"},
            {"number": "6700", "name": "Depreciation Expense", "type": "expense", "subtype": "depreciation"},
        ]
    },

    "property_management": {
        "name": "Property Management - Comprehensive",
        "description": "Chart of accounts optimized for property management companies",
        "accounts": [
            # Assets (1000-1999)
            {"number": "1000", "name": "Operating Cash", "type": "asset", "subtype": "cash"},
            {"number": "1050", "name": "Trust Account - Security Deposits", "type": "asset", "subtype": "security_deposits"},
            {"number": "1100", "name": "Rent Receivable", "type": "asset", "subtype": "accounts_receivable"},
            {"number": "1200", "name": "Prepaid Expenses", "type": "asset", "subtype": "prepaid_expenses"},
            {"number": "1500", "name": "Real Estate Properties", "type": "asset", "subtype": "fixed_asset"},
            {"number": "1510", "name": "Building & Improvements", "type": "asset", "subtype": "fixed_asset", "parent": "1500"},
            {"number": "1520", "name": "Land", "type": "asset", "subtype": "fixed_asset", "parent": "1500"},
            {"number": "1530", "name": "Equipment & Appliances", "type": "asset", "subtype": "fixed_asset", "parent": "1500"},

            # Liabilities (2000-2999)
            {"number": "2000", "name": "Accounts Payable", "type": "liability", "subtype": "accounts_payable"},
            {"number": "2100", "name": "Tenant Security Deposits", "type": "liability", "subtype": "tenant_deposits"},
            {"number": "2200", "name": "Tenant Advance Rent", "type": "liability", "subtype": "current_liability"},
            {"number": "2500", "name": "Mortgage Payable", "type": "liability", "subtype": "mortgage_payable"},
            {"number": "2600", "name": "Property Loans", "type": "liability", "subtype": "loans_payable"},

            # Equity (3000-3999)
            {"number": "3000", "name": "Owner's Capital", "type": "equity", "subtype": "owner_equity"},
            {"number": "3900", "name": "Retained Earnings", "type": "equity", "subtype": "retained_earnings"},

            # Revenue (4000-4999)
            {"number": "4000", "name": "Rental Income", "type": "revenue", "subtype": "rental_income"},
            {"number": "4010", "name": "Residential Rental Income", "type": "revenue", "subtype": "rental_income", "parent": "4000"},
            {"number": "4020", "name": "Commercial Rental Income", "type": "revenue", "subtype": "rental_income", "parent": "4000"},
            {"number": "4100", "name": "Late Fees", "type": "revenue", "subtype": "late_fees"},
            {"number": "4200", "name": "Application Fees", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4300", "name": "Parking Revenue", "type": "revenue", "subtype": "rental_income"},
            {"number": "4400", "name": "Laundry Revenue", "type": "revenue", "subtype": "rental_income"},
            {"number": "4900", "name": "Other Income", "type": "revenue", "subtype": "other_income"},

            # Operating Expenses (5000-7999)
            {"number": "5000", "name": "Property Taxes", "type": "expense", "subtype": "property_tax"},
            {"number": "5100", "name": "Insurance - Property", "type": "expense", "subtype": "insurance"},
            {"number": "5200", "name": "Utilities", "type": "expense", "subtype": "utilities"},
            {"number": "5210", "name": "Water & Sewer", "type": "expense", "subtype": "utilities", "parent": "5200"},
            {"number": "5220", "name": "Electricity", "type": "expense", "subtype": "utilities", "parent": "5200"},
            {"number": "5230", "name": "Gas", "type": "expense", "subtype": "utilities", "parent": "5200"},
            {"number": "5240", "name": "Trash Removal", "type": "expense", "subtype": "utilities", "parent": "5200"},
            {"number": "5300", "name": "Maintenance & Repairs", "type": "expense", "subtype": "maintenance"},
            {"number": "5310", "name": "HVAC Maintenance", "type": "expense", "subtype": "maintenance", "parent": "5300"},
            {"number": "5320", "name": "Plumbing Repairs", "type": "expense", "subtype": "repairs", "parent": "5300"},
            {"number": "5330", "name": "Electrical Repairs", "type": "expense", "subtype": "repairs", "parent": "5300"},
            {"number": "5340", "name": "Appliance Repairs", "type": "expense", "subtype": "repairs", "parent": "5300"},
            {"number": "5400", "name": "Landscaping & Groundskeeping", "type": "expense", "subtype": "landscaping"},
            {"number": "5500", "name": "Cleaning & Janitorial", "type": "expense", "subtype": "operating_expense"},
            {"number": "5600", "name": "Pest Control", "type": "expense", "subtype": "operating_expense"},
            {"number": "5700", "name": "Security Services", "type": "expense", "subtype": "operating_expense"},
            {"number": "6000", "name": "Management Fees", "type": "expense", "subtype": "management_fees"},
            {"number": "6100", "name": "Legal & Professional Fees", "type": "expense", "subtype": "legal_professional"},
            {"number": "6200", "name": "Advertising & Marketing", "type": "expense", "subtype": "advertising"},
            {"number": "6300", "name": "Office Expenses", "type": "expense", "subtype": "operating_expense"},
            {"number": "6400", "name": "HOA Fees", "type": "expense", "subtype": "operating_expense"},
            {"number": "7000", "name": "Mortgage Interest", "type": "expense", "subtype": "operating_expense"},
            {"number": "7100", "name": "Depreciation - Building", "type": "expense", "subtype": "depreciation"},
            {"number": "7200", "name": "Depreciation - Equipment", "type": "expense", "subtype": "depreciation"},
        ]
    },

    "high_net_worth": {
        "name": "High Net Worth Individual",
        "description": "Chart of accounts for high net worth individuals with investment tracking",
        "accounts": [
            # Assets (1000-1999)
            {"number": "1000", "name": "Cash & Cash Equivalents", "type": "asset", "subtype": "cash"},
            {"number": "1100", "name": "Investment Accounts", "type": "asset", "subtype": "current_asset"},
            {"number": "1110", "name": "Brokerage Accounts", "type": "asset", "subtype": "current_asset", "parent": "1100"},
            {"number": "1120", "name": "Municipal Bonds", "type": "asset", "subtype": "current_asset", "parent": "1100"},
            {"number": "1200", "name": "Real Estate Holdings", "type": "asset", "subtype": "fixed_asset"},
            {"number": "1210", "name": "Primary Residence", "type": "asset", "subtype": "fixed_asset", "parent": "1200"},
            {"number": "1220", "name": "Investment Properties", "type": "asset", "subtype": "fixed_asset", "parent": "1200"},
            {"number": "1230", "name": "Vacation Properties", "type": "asset", "subtype": "fixed_asset", "parent": "1200"},
            {"number": "1300", "name": "Retirement Accounts", "type": "asset", "subtype": "current_asset"},
            {"number": "1310", "name": "401(k) / IRA", "type": "asset", "subtype": "current_asset", "parent": "1300"},
            {"number": "1400", "name": "Business Interests", "type": "asset", "subtype": "current_asset"},
            {"number": "1500", "name": "Trust Assets", "type": "asset", "subtype": "current_asset"},

            # Liabilities (2000-2999)
            {"number": "2000", "name": "Credit Cards", "type": "liability", "subtype": "current_liability"},
            {"number": "2100", "name": "Mortgages", "type": "liability", "subtype": "mortgage_payable"},
            {"number": "2200", "name": "Investment Loans", "type": "liability", "subtype": "loans_payable"},
            {"number": "2300", "name": "Estate Tax Liability", "type": "liability", "subtype": "long_term_liability"},

            # Equity (3000-3999)
            {"number": "3000", "name": "Net Worth", "type": "equity", "subtype": "owner_equity"},

            # Income (4000-4999)
            {"number": "4000", "name": "Salary & Wages", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4100", "name": "Rental Income", "type": "revenue", "subtype": "rental_income"},
            {"number": "4200", "name": "Investment Income", "type": "revenue", "subtype": "other_income"},
            {"number": "4210", "name": "Dividends", "type": "revenue", "subtype": "other_income", "parent": "4200"},
            {"number": "4220", "name": "Interest Income", "type": "revenue", "subtype": "other_income", "parent": "4200"},
            {"number": "4230", "name": "Capital Gains", "type": "revenue", "subtype": "other_income", "parent": "4200"},
            {"number": "4300", "name": "Business Income", "type": "revenue", "subtype": "service_revenue"},

            # Expenses (5000-9999)
            {"number": "5000", "name": "Living Expenses", "type": "expense", "subtype": "operating_expense"},
            {"number": "5100", "name": "Property Expenses", "type": "expense", "subtype": "operating_expense"},
            {"number": "5110", "name": "Property Taxes", "type": "expense", "subtype": "property_tax", "parent": "5100"},
            {"number": "5120", "name": "Property Insurance", "type": "expense", "subtype": "insurance", "parent": "5100"},
            {"number": "5130", "name": "Property Maintenance", "type": "expense", "subtype": "maintenance", "parent": "5100"},
            {"number": "5200", "name": "Mortgage Interest", "type": "expense", "subtype": "operating_expense"},
            {"number": "5300", "name": "Investment Management Fees", "type": "expense", "subtype": "operating_expense"},
            {"number": "5400", "name": "Professional Services", "type": "expense", "subtype": "legal_professional"},
            {"number": "5410", "name": "Legal Fees", "type": "expense", "subtype": "legal_professional", "parent": "5400"},
            {"number": "5420", "name": "Accounting & Tax Prep", "type": "expense", "subtype": "legal_professional", "parent": "5400"},
            {"number": "5430", "name": "Estate Planning", "type": "expense", "subtype": "legal_professional", "parent": "5400"},
            {"number": "5500", "name": "Charitable Contributions", "type": "expense", "subtype": "operating_expense"},
            {"number": "6000", "name": "Depreciation", "type": "expense", "subtype": "depreciation"},
        ]
    },

    "financial_institution": {
        "name": "Financial Institution",
        "description": "Chart of accounts for financial institutions and fund managers",
        "accounts": [
            # Assets (1000-1999)
            {"number": "1000", "name": "Cash", "type": "asset", "subtype": "cash"},
            {"number": "1100", "name": "Investment Portfolio", "type": "asset", "subtype": "current_asset"},
            {"number": "1200", "name": "Loans Receivable", "type": "asset", "subtype": "accounts_receivable"},
            {"number": "1300", "name": "Real Estate Assets", "type": "asset", "subtype": "fixed_asset"},
            {"number": "1400", "name": "Office & Equipment", "type": "asset", "subtype": "fixed_asset"},

            # Liabilities (2000-2999)
            {"number": "2000", "name": "Client Deposits", "type": "liability", "subtype": "current_liability"},
            {"number": "2100", "name": "Borrowed Funds", "type": "liability", "subtype": "loans_payable"},
            {"number": "2200", "name": "Investment Liabilities", "type": "liability", "subtype": "current_liability"},

            # Equity (3000-3999)
            {"number": "3000", "name": "Partners' Capital", "type": "equity", "subtype": "owner_equity"},
            {"number": "3900", "name": "Retained Earnings", "type": "equity", "subtype": "retained_earnings"},

            # Revenue (4000-4999)
            {"number": "4000", "name": "Management Fees", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4100", "name": "Performance Fees", "type": "revenue", "subtype": "service_revenue"},
            {"number": "4200", "name": "Investment Income", "type": "revenue", "subtype": "other_income"},
            {"number": "4300", "name": "Interest Income", "type": "revenue", "subtype": "other_income"},

            # Expenses (5000-9999)
            {"number": "5000", "name": "Operating Expenses", "type": "expense", "subtype": "operating_expense"},
            {"number": "5100", "name": "Compensation & Benefits", "type": "expense", "subtype": "operating_expense"},
            {"number": "5200", "name": "Professional Fees", "type": "expense", "subtype": "legal_professional"},
            {"number": "5300", "name": "Technology & Systems", "type": "expense", "subtype": "operating_expense"},
            {"number": "5400", "name": "Compliance & Regulatory", "type": "expense", "subtype": "legal_professional"},
        ]
    }
}


# ============================================================================
# Tax Benefit Templates and Guides
# ============================================================================

TAX_BENEFIT_TEMPLATES = {
    "property_management": [
        {
            "type": "depreciation",
            "name": "Residential Property Depreciation",
            "description": "Depreciate residential rental property over 27.5 years",
            "formula": "Building Value / 27.5 years",
            "irs_reference": "IRS Publication 527",
        },
        {
            "type": "depreciation",
            "name": "Commercial Property Depreciation",
            "description": "Depreciate commercial rental property over 39 years",
            "formula": "Building Value / 39 years",
            "irs_reference": "IRS Publication 946",
        },
        {
            "type": "cost_segregation",
            "name": "Cost Segregation Study",
            "description": "Accelerate depreciation by segregating property components",
            "benefit": "Can accelerate 20-40% of building cost to 5-15 year recovery periods",
            "irs_reference": "IRS Audit Technique Guide",
        },
        {
            "type": "mortgage_interest",
            "name": "Mortgage Interest Deduction",
            "description": "Deduct mortgage interest paid on rental properties",
            "irs_reference": "Schedule E, Line 13",
        },
        {
            "type": "property_tax_deduction",
            "name": "Property Tax Deduction",
            "description": "Deduct property taxes paid on rental properties",
            "irs_reference": "Schedule E, Line 16",
        },
        {
            "type": "repair_deduction",
            "name": "Repairs & Maintenance",
            "description": "Deduct costs of repairs that maintain property condition",
            "note": "Improvements must be capitalized and depreciated",
            "irs_reference": "IRS Publication 527",
        },
        {
            "type": "section_1031_exchange",
            "name": "1031 Like-Kind Exchange",
            "description": "Defer capital gains taxes by exchanging investment properties",
            "requirements": "Must be like-kind, identify within 45 days, close within 180 days",
            "irs_reference": "IRC Section 1031",
        },
    ],

    "high_net_worth": [
        {
            "type": "charitable_contribution",
            "name": "Charitable Giving - Appreciated Securities",
            "description": "Donate appreciated securities to avoid capital gains tax",
            "benefit": "Tax deduction for fair market value + avoid capital gains",
            "limit": "30% of AGI for appreciated assets to public charities",
        },
        {
            "type": "municipal_bonds",
            "name": "Tax-Free Municipal Bonds",
            "description": "Interest from municipal bonds is exempt from federal tax",
            "benefit": "Tax-free interest income, may also be state tax-free",
        },
        {
            "type": "tax_loss_harvesting",
            "name": "Tax-Loss Harvesting",
            "description": "Sell securities at a loss to offset capital gains",
            "limit": "$3,000 annual deduction against ordinary income",
            "wash_sale_rule": "Cannot rebuy same security within 30 days",
        },
        {
            "type": "estate_planning",
            "name": "Annual Gift Tax Exclusion",
            "description": "Give up to annual limit per person without gift tax",
            "amount_2025": "$19,000 per recipient",
            "benefit": "Reduces taxable estate",
        },
        {
            "type": "estate_planning",
            "name": "Irrevocable Trust",
            "description": "Transfer assets to trust to reduce estate tax",
            "benefit": "Removes assets from taxable estate",
        },
        {
            "type": "retirement_contribution",
            "name": "401(k) & IRA Contributions",
            "description": "Tax-deductible retirement contributions",
            "limit_401k_2025": "$23,500 ($31,000 if age 50+)",
            "limit_ira_2025": "$7,000 ($8,000 if age 50+)",
        },
        {
            "type": "hsa_contribution",
            "name": "Health Savings Account (HSA)",
            "description": "Triple tax advantage - deductible, tax-free growth, tax-free withdrawals for medical",
            "limit_2025_individual": "$4,300",
            "limit_2025_family": "$8,550",
        },
        {
            "type": "home_office_deduction",
            "name": "Home Office Deduction",
            "description": "Deduct portion of home expenses for business use",
            "requirements": "Regular and exclusive business use",
            "methods": "Simplified ($5/sq ft up to 300 sq ft) or Actual expenses",
        },
    ],

    "small_business": [
        {
            "type": "depreciation",
            "name": "Section 179 Deduction",
            "description": "Immediate expensing of qualifying equipment and software",
            "limit_2025": "$1,220,000",
            "phase_out": "$3,050,000",
        },
        {
            "type": "depreciation",
            "name": "Bonus Depreciation",
            "description": "First-year depreciation for qualifying property",
            "rate": "100% through 2022, phasing down thereafter",
        },
        {
            "type": "home_office_deduction",
            "name": "Home Office Deduction",
            "description": "Deduct portion of home expenses for business use",
        },
        {
            "type": "travel_deduction",
            "name": "Business Travel & Meals",
            "description": "Deduct business travel, lodging, and 50% of meals",
        },
        {
            "type": "retirement_contribution",
            "name": "SEP IRA or Solo 401(k)",
            "description": "Tax-deductible retirement contributions for self-employed",
            "sep_limit": "25% of compensation up to $69,000",
            "solo_401k_limit": "$69,000 ($76,500 if age 50+)",
        },
    ]
}


# ============================================================================
# Integration Configuration Templates
# ============================================================================

INTEGRATION_TEMPLATES = {
    "quickbooks": {
        "name": "QuickBooks Online",
        "description": "Sync transactions and chart of accounts with QuickBooks",
        "auth_method": "OAuth 2.0",
        "api_base_url": "https://quickbooks.api.intuit.com/v3",
        "required_credentials": ["client_id", "client_secret", "redirect_uri"],
        "sync_capabilities": ["chart_of_accounts", "transactions", "customers", "vendors"],
    },
    "xero": {
        "name": "Xero Accounting",
        "description": "Sync financial data with Xero",
        "auth_method": "OAuth 2.0",
        "api_base_url": "https://api.xero.com/api.xro/2.0",
        "required_credentials": ["client_id", "client_secret"],
        "sync_capabilities": ["chart_of_accounts", "invoices", "bills", "bank_transactions"],
    },
    "yardi": {
        "name": "Yardi Voyager",
        "description": "Property management platform integration",
        "auth_method": "API Key",
        "required_credentials": ["api_key", "platform_id", "entity_id"],
        "sync_capabilities": ["properties", "units", "leases", "tenants", "financials"],
    },
    "appfolio": {
        "name": "AppFolio Property Manager",
        "description": "Property management software integration",
        "auth_method": "OAuth 2.0",
        "required_credentials": ["client_id", "client_secret"],
        "sync_capabilities": ["properties", "leases", "rent_roll", "work_orders"],
    },
    "docusign": {
        "name": "DocuSign",
        "description": "E-signature integration for lease agreements and documents",
        "auth_method": "OAuth 2.0",
        "api_base_url": "https://demo.docusign.net/restapi",
        "required_credentials": ["integration_key", "secret_key"],
    },
    "dropbox": {
        "name": "Dropbox",
        "description": "Document storage and management",
        "auth_method": "OAuth 2.0",
        "api_base_url": "https://api.dropboxapi.com/2",
        "required_credentials": ["app_key", "app_secret"],
    },
    "box": {
        "name": "Box",
        "description": "Enterprise document management",
        "auth_method": "OAuth 2.0",
        "api_base_url": "https://api.box.com/2.0",
        "required_credentials": ["client_id", "client_secret"],
    },
}


# ============================================================================
# Helper Functions
# ============================================================================

def get_template(entity_type: str) -> Dict[str, Any]:
    """
    Get chart of accounts template for an entity type.

    Args:
        entity_type: The type of entity (small_business, property_management, etc.)

    Returns:
        Template dictionary with chart of accounts structure
    """
    return CHART_OF_ACCOUNTS_TEMPLATES.get(entity_type, CHART_OF_ACCOUNTS_TEMPLATES["small_business"])


def get_tax_benefits_guide(entity_type: str) -> List[Dict[str, Any]]:
    """
    Get tax benefits guide for an entity type.

    Args:
        entity_type: The type of entity

    Returns:
        List of tax benefit templates
    """
    return TAX_BENEFIT_TEMPLATES.get(entity_type, [])


def get_integration_config(integration_type: str) -> Dict[str, Any]:
    """
    Get integration configuration template.

    Args:
        integration_type: The type of integration (quickbooks, xero, etc.)

    Returns:
        Integration configuration dictionary
    """
    return INTEGRATION_TEMPLATES.get(integration_type, {})


__all__ = [
    "CHART_OF_ACCOUNTS_TEMPLATES",
    "TAX_BENEFIT_TEMPLATES",
    "INTEGRATION_TEMPLATES",
    "get_template",
    "get_tax_benefits_guide",
    "get_integration_config",
]
