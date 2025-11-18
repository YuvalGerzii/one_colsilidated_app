"""
Big-4 Accounting Firm Reporting Standards and Templates

Professional financial reporting templates following standards used by:
- Deloitte
- PwC (PricewaterhouseCoopers)
- EY (Ernst & Young)
- KPMG

These templates follow GAAP, IFRS, and SEC reporting requirements.
"""

from typing import Dict, List, Any
from datetime import datetime


# ============================================================================
# BIG-4 FINANCIAL STATEMENT TEMPLATES
# ============================================================================

BALANCE_SHEET_TEMPLATE = {
    "name": "Statement of Financial Position (Balance Sheet)",
    "standard": "GAAP/IFRS",
    "structure": {
        "assets": {
            "current_assets": {
                "order": 1,
                "accounts": [
                    {"code": "1000", "name": "Cash and Cash Equivalents", "description": "Bank accounts, money market funds"},
                    {"code": "1010", "name": "Restricted Cash", "description": "Cash with withdrawal limitations"},
                    {"code": "1100", "name": "Accounts Receivable", "description": "Trade receivables"},
                    {"code": "1105", "name": "Allowance for Doubtful Accounts", "description": "Contra-asset for uncollectible receivables"},
                    {"code": "1200", "name": "Notes Receivable - Current", "description": "Short-term notes receivable"},
                    {"code": "1300", "name": "Inventory", "description": "At lower of cost or market"},
                    {"code": "1400", "name": "Prepaid Expenses", "description": "Prepaid insurance, rent, etc."},
                    {"code": "1500", "name": "Other Current Assets", "description": ""}
                ],
                "subtotal": "Total Current Assets"
            },
            "non_current_assets": {
                "order": 2,
                "sections": {
                    "investments": {
                        "accounts": [
                            {"code": "1600", "name": "Long-term Investments", "description": "Securities held for investment"},
                            {"code": "1610", "name": "Investment in Affiliates", "description": "Equity method investments"}
                        ]
                    },
                    "property_plant_equipment": {
                        "accounts": [
                            {"code": "1700", "name": "Land", "description": "At cost, not depreciated"},
                            {"code": "1710", "name": "Buildings and Improvements", "description": "At cost"},
                            {"code": "1720", "name": "Machinery and Equipment", "description": "At cost"},
                            {"code": "1730", "name": "Furniture and Fixtures", "description": "At cost"},
                            {"code": "1740", "name": "Vehicles", "description": "At cost"},
                            {"code": "1750", "name": "Leasehold Improvements", "description": "At cost"},
                            {"code": "1760", "name": "Construction in Progress", "description": "Assets under construction"},
                            {"code": "1799", "name": "Accumulated Depreciation", "description": "Contra-asset"}
                        ],
                        "subtotal": "Property, Plant and Equipment, Net"
                    },
                    "intangible_assets": {
                        "accounts": [
                            {"code": "1800", "name": "Goodwill", "description": "Not amortized, tested for impairment"},
                            {"code": "1810", "name": "Patents", "description": "Amortized over useful life"},
                            {"code": "1820", "name": "Trademarks", "description": "Amortized if definite life"},
                            {"code": "1830", "name": "Customer Lists", "description": "Amortized over useful life"},
                            {"code": "1899", "name": "Accumulated Amortization", "description": "Contra-asset"}
                        ],
                        "subtotal": "Intangible Assets, Net"
                    },
                    "other_non_current": {
                        "accounts": [
                            {"code": "1900", "name": "Deferred Tax Assets", "description": "Future tax benefits"},
                            {"code": "1910", "name": "Security Deposits", "description": "Long-term deposits"},
                            {"code": "1990", "name": "Other Non-Current Assets", "description": ""}
                        ]
                    }
                },
                "subtotal": "Total Non-Current Assets"
            }
        },
        "total_assets": "TOTAL ASSETS",

        "liabilities": {
            "current_liabilities": {
                "order": 3,
                "accounts": [
                    {"code": "2000", "name": "Accounts Payable", "description": "Trade payables"},
                    {"code": "2100", "name": "Accrued Expenses", "description": "Wages, interest, etc."},
                    {"code": "2110", "name": "Accrued Payroll", "description": "Unpaid wages and salaries"},
                    {"code": "2120", "name": "Accrued Interest", "description": "Interest payable"},
                    {"code": "2200", "name": "Short-term Debt", "description": "Notes payable within 1 year"},
                    {"code": "2210", "name": "Current Portion of Long-term Debt", "description": "Due within 1 year"},
                    {"code": "2300", "name": "Unearned Revenue", "description": "Advance payments from customers"},
                    {"code": "2400", "name": "Taxes Payable", "description": "Income taxes owed"},
                    {"code": "2500", "name": "Other Current Liabilities", "description": ""}
                ],
                "subtotal": "Total Current Liabilities"
            },
            "non_current_liabilities": {
                "order": 4,
                "accounts": [
                    {"code": "2600", "name": "Long-term Debt", "description": "Loans payable after 1 year"},
                    {"code": "2610", "name": "Mortgage Payable", "description": "Secured by real estate"},
                    {"code": "2700", "name": "Bonds Payable", "description": "Corporate bonds"},
                    {"code": "2710", "name": "Premium/Discount on Bonds", "description": "Bond issuance adjustments"},
                    {"code": "2800", "name": "Deferred Tax Liabilities", "description": "Future tax obligations"},
                    {"code": "2900", "name": "Pension Liability", "description": "Unfunded pension obligations"},
                    {"code": "2990", "name": "Other Non-Current Liabilities", "description": ""}
                ],
                "subtotal": "Total Non-Current Liabilities"
            }
        },
        "total_liabilities": "TOTAL LIABILITIES",

        "equity": {
            "order": 5,
            "accounts": [
                {"code": "3000", "name": "Common Stock", "description": "Par value"},
                {"code": "3010", "name": "Additional Paid-in Capital", "description": "Excess over par"},
                {"code": "3100", "name": "Preferred Stock", "description": "If applicable"},
                {"code": "3200", "name": "Retained Earnings", "description": "Accumulated profits"},
                {"code": "3300", "name": "Treasury Stock", "description": "Contra-equity (repurchased shares)"},
                {"code": "3400", "name": "Accumulated Other Comprehensive Income", "description": "Unrealized gains/losses"},
                {"code": "3500", "name": "Non-controlling Interest", "description": "Minority interest in subsidiaries"}
            ],
            "subtotal": "Total Equity"
        },
        "total_liabilities_equity": "TOTAL LIABILITIES AND EQUITY"
    },

    "presentation_requirements": {
        "classification": "Current vs Non-Current (12-month operating cycle)",
        "valuation": "Historical cost except where fair value required",
        "disclosure_notes": [
            "Summary of Significant Accounting Policies",
            "Basis of Presentation",
            "Revenue Recognition",
            "Property, Plant and Equipment",
            "Goodwill and Intangible Assets",
            "Debt Obligations",
            "Commitments and Contingencies",
            "Subsequent Events"
        ]
    }
}

INCOME_STATEMENT_TEMPLATE = {
    "name": "Statement of Comprehensive Income (P&L)",
    "standard": "GAAP Multi-Step Format",
    "structure": {
        "revenue": {
            "order": 1,
            "accounts": [
                {"code": "4000", "name": "Revenue from Contracts with Customers", "description": "ASC 606"},
                {"code": "4010", "name": "Product Sales", "description": ""},
                {"code": "4020", "name": "Service Revenue", "description": ""},
                {"code": "4030", "name": "Rental Income", "description": ""},
                {"code": "4100", "name": "Sales Returns and Allowances", "description": "Contra-revenue"}
            ],
            "subtotal": "Net Revenue"
        },
        "cost_of_revenue": {
            "order": 2,
            "accounts": [
                {"code": "5000", "name": "Cost of Goods Sold", "description": "Direct product costs"},
                {"code": "5010", "name": "Cost of Services", "description": "Direct service costs"},
                {"code": "5100", "name": "Depreciation - Production", "description": "Depreciation of production assets"}
            ],
            "subtotal": "Total Cost of Revenue"
        },
        "gross_profit": "Gross Profit",

        "operating_expenses": {
            "order": 3,
            "sections": {
                "selling_expenses": {
                    "accounts": [
                        {"code": "6000", "name": "Sales Salaries and Commissions", "description": ""},
                        {"code": "6010", "name": "Advertising and Marketing", "description": ""},
                        {"code": "6020", "name": "Sales Travel and Entertainment", "description": ""},
                        {"code": "6030", "name": "Shipping and Delivery", "description": ""}
                    ],
                    "subtotal": "Total Selling Expenses"
                },
                "general_administrative": {
                    "accounts": [
                        {"code": "6100", "name": "Officer Salaries", "description": ""},
                        {"code": "6110", "name": "Office Salaries", "description": ""},
                        {"code": "6120", "name": "Employee Benefits", "description": "Health insurance, 401k match"},
                        {"code": "6130", "name": "Payroll Taxes", "description": "Employer portion"},
                        {"code": "6200", "name": "Rent Expense", "description": "Office and facility rent"},
                        {"code": "6210", "name": "Utilities", "description": "Electric, gas, water"},
                        {"code": "6220", "name": "Insurance", "description": "General liability, property"},
                        {"code": "6300", "name": "Professional Fees", "description": "Legal, accounting, consulting"},
                        {"code": "6310", "name": "Audit and Tax Preparation", "description": ""},
                        {"code": "6400", "name": "Office Supplies", "description": ""},
                        {"code": "6410", "name": "Technology and Software", "description": ""},
                        {"code": "6500", "name": "Depreciation and Amortization", "description": "Non-production assets"},
                        {"code": "6600", "name": "Bad Debt Expense", "description": "Provision for uncollectible accounts"},
                        {"code": "6700", "name": "Other G&A Expenses", "description": ""}
                    ],
                    "subtotal": "Total General and Administrative"
                },
                "research_development": {
                    "accounts": [
                        {"code": "6800", "name": "Research and Development", "description": "Product development costs"}
                    ],
                    "subtotal": "Total R&D Expenses"
                }
            },
            "subtotal": "Total Operating Expenses"
        },
        "operating_income": "Operating Income (EBIT)",

        "other_income_expense": {
            "order": 4,
            "accounts": [
                {"code": "7000", "name": "Interest Income", "description": ""},
                {"code": "7010", "name": "Dividend Income", "description": ""},
                {"code": "7100", "name": "Interest Expense", "description": ""},
                {"code": "7200", "name": "Gain (Loss) on Sale of Assets", "description": ""},
                {"code": "7300", "name": "Foreign Currency Gain (Loss)", "description": ""},
                {"code": "7400", "name": "Other Non-Operating Income (Expense)", "description": ""}
            ],
            "subtotal": "Total Other Income (Expense)"
        },
        "income_before_tax": "Income Before Income Taxes",

        "income_tax": {
            "order": 5,
            "accounts": [
                {"code": "8000", "name": "Current Income Tax Expense", "description": ""},
                {"code": "8010", "name": "Deferred Income Tax Expense (Benefit)", "description": ""}
            ],
            "subtotal": "Total Income Tax Expense"
        },
        "net_income": "Net Income",

        "earnings_per_share": {
            "basic_eps": "Basic Earnings Per Share",
            "diluted_eps": "Diluted Earnings Per Share"
        },

        "other_comprehensive_income": {
            "accounts": [
                {"code": "8100", "name": "Unrealized Gain (Loss) on Securities", "description": "Available-for-sale"},
                {"code": "8110", "name": "Foreign Currency Translation Adjustment", "description": ""},
                {"code": "8120", "name": "Pension Liability Adjustment", "description": ""}
            ],
            "subtotal": "Other Comprehensive Income (Loss)"
        },
        "comprehensive_income": "Comprehensive Income"
    }
}

CASH_FLOW_STATEMENT_TEMPLATE = {
    "name": "Statement of Cash Flows",
    "standard": "GAAP Indirect Method",
    "structure": {
        "operating_activities": {
            "order": 1,
            "reconciliation": [
                {"line": "Net Income", "source": "Income Statement"},
                {"line": "Adjustments to reconcile net income to cash:", "type": "header"},
                {"line": "  Depreciation and Amortization", "type": "add_back"},
                {"line": "  Amortization of Bond Premium/Discount", "type": "add_back"},
                {"line": "  Bad Debt Expense", "type": "add_back"},
                {"line": "  Stock-Based Compensation", "type": "add_back"},
                {"line": "  Deferred Income Taxes", "type": "add_back"},
                {"line": "  Gain on Sale of Assets", "type": "subtract"},
                {"line": "  Loss on Sale of Assets", "type": "add_back"},
                {"line": "Changes in operating assets and liabilities:", "type": "header"},
                {"line": "  (Increase) Decrease in Accounts Receivable", "type": "change"},
                {"line": "  (Increase) Decrease in Inventory", "type": "change"},
                {"line": "  (Increase) Decrease in Prepaid Expenses", "type": "change"},
                {"line": "  Increase (Decrease) in Accounts Payable", "type": "change"},
                {"line": "  Increase (Decrease) in Accrued Expenses", "type": "change"},
                {"line": "  Increase (Decrease) in Unearned Revenue", "type": "change"}
            ],
            "subtotal": "Net Cash Provided by (Used in) Operating Activities"
        },
        "investing_activities": {
            "order": 2,
            "line_items": [
                {"line": "Purchase of Property, Plant and Equipment", "type": "outflow"},
                {"line": "Proceeds from Sale of Property, Plant and Equipment", "type": "inflow"},
                {"line": "Purchase of Investments", "type": "outflow"},
                {"line": "Proceeds from Sale/Maturity of Investments", "type": "inflow"},
                {"line": "Acquisition of Business, Net of Cash Acquired", "type": "outflow"},
                {"line": "Other Investing Activities", "type": "both"}
            ],
            "subtotal": "Net Cash Provided by (Used in) Investing Activities"
        },
        "financing_activities": {
            "order": 3,
            "line_items": [
                {"line": "Proceeds from Issuance of Common Stock", "type": "inflow"},
                {"line": "Proceeds from Issuance of Preferred Stock", "type": "inflow"},
                {"line": "Proceeds from Long-term Debt", "type": "inflow"},
                {"line": "Repayment of Long-term Debt", "type": "outflow"},
                {"line": "Proceeds from (Repayment of) Short-term Debt, Net", "type": "both"},
                {"line": "Purchase of Treasury Stock", "type": "outflow"},
                {"line": "Cash Dividends Paid", "type": "outflow"},
                {"line": "Payment of Financing Costs", "type": "outflow"},
                {"line": "Other Financing Activities", "type": "both"}
            ],
            "subtotal": "Net Cash Provided by (Used in) Financing Activities"
        },
        "summary": [
            "Net Increase (Decrease) in Cash and Cash Equivalents",
            "Cash and Cash Equivalents - Beginning of Period",
            "Cash and Cash Equivalents - End of Period"
        ],
        "supplemental_disclosures": [
            "Cash Paid for Interest",
            "Cash Paid for Income Taxes",
            "Non-Cash Investing and Financing Activities"
        ]
    }
}

# ============================================================================
# BIG-4 AUDIT AND TAX WORKPAPER TEMPLATES
# ============================================================================

AUDIT_WORKPAPER_TEMPLATES = {
    "lead_schedule": {
        "name": "Lead Schedule Template",
        "purpose": "Summary of account balances with tie to GL and supporting schedules",
        "columns": [
            "Account Number",
            "Account Description",
            "Beginning Balance",
            "Debits",
            "Credits",
            "Ending Balance",
            "Adjustments",
            "Adjusted Balance",
            "Workpaper Reference"
        ],
        "footer": [
            "Prepared by: ___________  Date: ___________",
            "Reviewed by: ___________  Date: ___________",
            "Tick Mark Legend"
        ]
    },

    "account_analysis": {
        "name": "Account Analysis Template",
        "purpose": "Detailed analysis of account activity",
        "sections": [
            "Account Information",
            "Beginning Balance",
            "Activity Detail (Date, Description, Debit, Credit)",
            "Ending Balance",
            "Audit Procedures Performed",
            "Findings and Conclusions",
            "Cross-References"
        ]
    },

    "reconciliation": {
        "name": "Bank/Account Reconciliation",
        "purpose": "Reconcile book balance to bank/external statement",
        "format": [
            "Balance per Books",
            "Add: Items",
            "Less: Items",
            "Balance per Bank/Statement",
            "Outstanding Items Detail",
            "Reconciliation Complete (Check)"
        ]
    },

    "rollforward": {
        "name": "Rollforward Schedule",
        "purpose": "Track changes in account from beginning to end of period",
        "columns": [
            "Description",
            "Beginning Balance",
            "Additions",
            "Disposals/Reductions",
            "Ending Balance"
        ],
        "common_uses": ["PP&E", "Intangible Assets", "Debt", "Equity"]
    }
}

TAX_WORKPAPER_TEMPLATES = {
    "m1_reconciliation": {
        "name": "Schedule M-1 - Book to Tax Reconciliation",
        "purpose": "Reconcile book income to taxable income",
        "structure": {
            "start": "Net Income per Books",
            "additions": [
                "Federal Income Tax Expense",
                "Excess Capital Loss",
                "Income Recorded on Books Not on Return",
                "Expenses Recorded on Books Not on Return (Meals & Entertainment 50%, etc.)"
            ],
            "subtractions": [
                "Income Recorded on Return Not on Books",
                "Deductions on Return Not on Books (Depreciation Differences, etc.)"
            ],
            "result": "Taxable Income per Return"
        }
    },

    "depreciation_schedule": {
        "name": "Depreciation and Amortization Schedule",
        "purpose": "Track tax depreciation for all assets",
        "columns": [
            "Asset Description",
            "Date Placed in Service",
            "Cost/Basis",
            "Recovery Period",
            "Method",
            "Convention",
            "Prior Depreciation",
            "Current Year Depreciation",
            "Accumulated Depreciation",
            "Remaining Basis"
        ],
        "methods": ["MACRS GDS", "MACRS ADS", "Straight-Line", "Section 179", "Bonus Depreciation"]
    },

    "nol_schedule": {
        "name": "Net Operating Loss (NOL) Carryforward",
        "purpose": "Track NOLs and utilization",
        "columns": [
            "Tax Year Generated",
            "Original NOL Amount",
            "Utilized in Prior Years",
            "Utilized Current Year",
            "Remaining Carryforward",
            "Expiration Year"
        ]
    }
}

# ============================================================================
# BIG-4 FINANCIAL ANALYSIS RATIOS
# ============================================================================

FINANCIAL_RATIOS = {
    "liquidity_ratios": {
        "current_ratio": {
            "formula": "Current Assets / Current Liabilities",
            "interpretation": "Measures ability to pay short-term obligations. > 1.0 is generally good.",
            "industry_benchmarks": {"manufacturing": 1.5, "retail": 1.2, "services": 1.3}
        },
        "quick_ratio": {
            "formula": "(Current Assets - Inventory) / Current Liabilities",
            "interpretation": "More conservative than current ratio. Excludes inventory.",
            "industry_benchmarks": {"manufacturing": 1.0, "retail": 0.5, "services": 1.0}
        },
        "cash_ratio": {
            "formula": "Cash and Cash Equivalents / Current Liabilities",
            "interpretation": "Most conservative liquidity measure. > 0.5 is strong."
        }
    },

    "profitability_ratios": {
        "gross_margin": {
            "formula": "Gross Profit / Revenue",
            "interpretation": "Percentage of revenue after direct costs. Higher is better.",
            "industry_benchmarks": {"software": 0.80, "retail": 0.30, "manufacturing": 0.35}
        },
        "operating_margin": {
            "formula": "Operating Income / Revenue",
            "interpretation": "Profit before interest and taxes. Measures operational efficiency."
        },
        "net_margin": {
            "formula": "Net Income / Revenue",
            "interpretation": "Bottom-line profitability. Compare to industry peers."
        },
        "return_on_assets": {
            "formula": "Net Income / Total Assets",
            "interpretation": "How efficiently assets generate profit. > 5% is good."
        },
        "return_on_equity": {
            "formula": "Net Income / Shareholder Equity",
            "interpretation": "Return to equity investors. > 15% is excellent."
        }
    },

    "leverage_ratios": {
        "debt_to_equity": {
            "formula": "Total Debt / Total Equity",
            "interpretation": "Capital structure. < 1.0 is conservative, < 2.0 is moderate.",
            "industry_benchmarks": {"utilities": 2.5, "technology": 0.3, "real_estate": 3.0}
        },
        "debt_to_assets": {
            "formula": "Total Debt / Total Assets",
            "interpretation": "Percentage of assets financed by debt. < 0.5 is conservative."
        },
        "interest_coverage": {
            "formula": "EBIT / Interest Expense",
            "interpretation": "Ability to pay interest. > 3.0 is healthy, > 5.0 is strong."
        },
        "debt_service_coverage": {
            "formula": "Net Operating Income / Total Debt Service",
            "interpretation": "Cash flow available to service debt. > 1.25 is acceptable."
        }
    },

    "efficiency_ratios": {
        "asset_turnover": {
            "formula": "Revenue / Total Assets",
            "interpretation": "How efficiently assets generate revenue. Higher is better."
        },
        "inventory_turnover": {
            "formula": "Cost of Goods Sold / Average Inventory",
            "interpretation": "How quickly inventory is sold. Higher generally better.",
            "industry_benchmarks": {"grocery": 12, "furniture": 5, "jewelry": 2}
        },
        "days_sales_outstanding": {
            "formula": "(Accounts Receivable / Revenue) × 365",
            "interpretation": "Average collection period. Lower is better. < 45 days is good."
        },
        "days_inventory_outstanding": {
            "formula": "(Inventory / COGS) × 365",
            "interpretation": "Days to sell inventory. Industry-specific."
        }
    }
}

# ============================================================================
# REPORT INPUT REQUIREMENTS
# ============================================================================

BIG4_REPORT_INPUT_REQUIREMENTS = {
    "balance_sheet": {
        "required_inputs": [
            {"field": "reporting_period_end", "type": "date", "description": "As of date"},
            {"field": "reporting_entity", "type": "text", "description": "Legal entity name"},
            {"field": "currency", "type": "select", "options": ["USD", "EUR", "GBP"], "default": "USD"},
            {"field": "presentation_currency", "type": "select", "options": ["actual", "thousands", "millions"]},
            {"field": "comparative_period", "type": "boolean", "description": "Include prior year comparative"}
        ],
        "account_inputs": "All balance sheet accounts with current and prior year balances"
    },

    "income_statement": {
        "required_inputs": [
            {"field": "period_start", "type": "date"},
            {"field": "period_end", "type": "date"},
            {"field": "reporting_entity", "type": "text"},
            {"field": "number_of_shares_basic", "type": "number", "description": "For EPS calculation"},
            {"field": "number_of_shares_diluted", "type": "number", "description": "For diluted EPS"},
            {"field": "format", "type": "select", "options": ["single_step", "multi_step"], "default": "multi_step"}
        ]
    },

    "cash_flow": {
        "required_inputs": [
            {"field": "period_start", "type": "date"},
            {"field": "period_end", "type": "date"},
            {"field": "method", "type": "select", "options": ["indirect", "direct"], "default": "indirect"},
            {"field": "cash_paid_interest", "type": "number", "description": "Supplemental disclosure"},
            {"field": "cash_paid_taxes", "type": "number", "description": "Supplemental disclosure"}
        ],
        "required_schedules": [
            "Balance Sheet - Beginning and End",
            "Income Statement for Period",
            "Detail of PP&E Additions/Disposals",
            "Detail of Debt Issuance/Repayment"
        ]
    }
}


def get_report_template(report_type: str) -> Dict[str, Any]:
    """Get specific report template"""
    templates = {
        "balance_sheet": BALANCE_SHEET_TEMPLATE,
        "income_statement": INCOME_STATEMENT_TEMPLATE,
        "cash_flow": CASH_FLOW_STATEMENT_TEMPLATE
    }
    return templates.get(report_type, {})


def get_required_inputs(report_type: str) -> Dict[str, Any]:
    """Get required inputs for report generation"""
    return BIG4_REPORT_INPUT_REQUIREMENTS.get(report_type, {})


def calculate_financial_ratio(ratio_name: str, inputs: Dict[str, float]) -> Dict[str, Any]:
    """Calculate financial ratio and return result with interpretation"""
    # Implementation would calculate specific ratio based on inputs
    pass


__all__ = [
    "BALANCE_SHEET_TEMPLATE",
    "INCOME_STATEMENT_TEMPLATE",
    "CASH_FLOW_STATEMENT_TEMPLATE",
    "AUDIT_WORKPAPER_TEMPLATES",
    "TAX_WORKPAPER_TEMPLATES",
    "FINANCIAL_RATIOS",
    "BIG4_REPORT_INPUT_REQUIREMENTS",
    "get_report_template",
    "get_required_inputs",
    "calculate_financial_ratio"
]
