"""
Comprehensive Accounting Guides and Best Practices

Expert-level guides covering accounting principles, tax strategies,
compliance requirements, and industry best practices.
"""

from typing import Dict, List, Any


# ============================================================================
# COMPREHENSIVE ACCOUNTING GUIDES
# ============================================================================

ACCOUNTING_FUNDAMENTALS_GUIDE = {
    "title": "Accounting Fundamentals - Expert Guide",
    "chapters": {
        "chapter_1_double_entry": {
            "title": "Double-Entry Bookkeeping Mastery",
            "content": {
                "introduction": """
                Double-entry bookkeeping is the foundation of modern accounting. Every transaction
                affects at least two accounts, with total debits always equaling total credits.
                """,
                "debit_credit_rules": {
                    "assets": {
                        "normal_balance": "Debit",
                        "increase": "Debit",
                        "decrease": "Credit",
                        "examples": ["Cash", "Accounts Receivable", "Inventory", "Equipment"]
                    },
                    "liabilities": {
                        "normal_balance": "Credit",
                        "increase": "Credit",
                        "decrease": "Debit",
                        "examples": ["Accounts Payable", "Loans Payable", "Unearned Revenue"]
                    },
                    "equity": {
                        "normal_balance": "Credit",
                        "increase": "Credit",
                        "decrease": "Debit",
                        "examples": ["Common Stock", "Retained Earnings", "Owner's Capital"]
                    },
                    "revenue": {
                        "normal_balance": "Credit",
                        "increase": "Credit",
                        "decrease": "Debit",
                        "examples": ["Sales Revenue", "Service Revenue", "Rental Income"]
                    },
                    "expenses": {
                        "normal_balance": "Debit",
                        "increase": "Debit",
                        "decrease": "Credit",
                        "examples": ["Rent Expense", "Salaries Expense", "Utilities Expense"]
                    }
                },
                "common_transactions": [
                    {
                        "description": "Purchase inventory with cash",
                        "debit": "Inventory",
                        "credit": "Cash",
                        "explanation": "Asset (inventory) increases, asset (cash) decreases"
                    },
                    {
                        "description": "Borrow money from bank",
                        "debit": "Cash",
                        "credit": "Loan Payable",
                        "explanation": "Asset increases, liability increases"
                    },
                    {
                        "description": "Pay rent",
                        "debit": "Rent Expense",
                        "credit": "Cash",
                        "explanation": "Expense increases (reduces equity), asset decreases"
                    },
                    {
                        "description": "Provide services on credit",
                        "debit": "Accounts Receivable",
                        "credit": "Service Revenue",
                        "explanation": "Asset increases, revenue increases (equity up)"
                    }
                ],
                "pro_tips": [
                    "Memorize: DEALER (Dividends, Expenses, Assets = Debit to increase; Liabilities, Equity, Revenue = Credit to increase)",
                    "Always check that debits = credits before posting",
                    "Use T-accounts to visualize account activity",
                    "Post to subsidiary ledgers first, then general ledger",
                    "Reconcile all balance sheet accounts monthly"
                ]
            }
        },

        "chapter_2_accrual_vs_cash": {
            "title": "Accrual vs Cash Accounting",
            "content": {
                "accrual_accounting": {
                    "definition": "Recognize revenue when earned and expenses when incurred, regardless of cash flow",
                    "advantages": [
                        "Matches revenues with related expenses (matching principle)",
                        "More accurate picture of financial performance",
                        "Required by GAAP for companies over $25M revenue",
                        "Better for financial analysis and decision-making"
                    ],
                    "example": "Provide $10K service in December, receive payment in January. Accrual: Recognize $10K revenue in December."
                },
                "cash_accounting": {
                    "definition": "Recognize revenue when cash received and expenses when cash paid",
                    "advantages": [
                        "Simpler to maintain",
                        "Better for tax planning (can defer income)",
                        "Matches cash flow",
                        "Allowed for small businesses under $25M revenue"
                    ],
                    "example": "Provide $10K service in December, receive payment in January. Cash: Recognize $10K revenue in January."
                },
                "expert_guidance": {
                    "when_to_use_accrual": [
                        "Company has inventory",
                        "Provides services on credit",
                        "Needs bank financing (lenders require GAAP)",
                        "Planning to sell business (higher valuation with accrual)",
                        "Revenue over $25M (required)"
                    ],
                    "when_cash_is_acceptable": [
                        "Small service business under $25M",
                        "Simple operations",
                        "Don't carry inventory",
                        "Limited A/R and A/P"
                    ],
                    "hybrid_approach": "Many businesses use accrual for GAAP financial statements but cash basis for tax (where allowed)"
                }
            }
        },

        "chapter_3_revenue_recognition": {
            "title": "Revenue Recognition (ASC 606)",
            "content": {
                "five_step_model": {
                    "step_1": {
                        "title": "Identify the Contract",
                        "description": "Must have approval, rights and payment terms are identified, commercial substance, and probable collection",
                        "example": "Signed agreement to provide consulting services for $100K over 6 months"
                    },
                    "step_2": {
                        "title": "Identify Performance Obligations",
                        "description": "Distinct goods or services promised to customer",
                        "example": "Software license (delivered upfront) + 12 months support (over time) = 2 performance obligations"
                    },
                    "step_3": {
                        "title": "Determine Transaction Price",
                        "description": "Amount entity expects to receive, including variable consideration",
                        "example": "$100K fixed fee + potential $20K bonus = $115K if bonus is probable"
                    },
                    "step_4": {
                        "title": "Allocate Price to Performance Obligations",
                        "description": "Based on standalone selling prices",
                        "example": "Software $80K standalone, Support $40K standalone. Allocate $100K contract: Software $67K, Support $33K"
                    },
                    "step_5": {
                        "title": "Recognize Revenue",
                        "description": "When (or as) performance obligation is satisfied",
                        "timing": {
                            "point_in_time": "Transfer of control occurs (e.g., product delivery)",
                            "over_time": "Continuous transfer (e.g., subscription services)"
                        }
                    }
                },
                "common_scenarios": {
                    "software_saas": {
                        "recognition": "Ratably over subscription period",
                        "example": "$12K annual subscription = $1K/month revenue",
                        "deferred_revenue": "Upfront payment creates liability, released monthly"
                    },
                    "construction": {
                        "method": "Percentage of completion (costs incurred / total estimated costs)",
                        "example": "$10M contract, 40% complete = Recognize $4M revenue",
                        "requires": "Reliable cost estimates, progress measurement"
                    },
                    "real_estate_sales": {
                        "timing": "When control transfers (usually at closing)",
                        "considerations": ["Buyer financing approved", "All contingencies removed", "Title transfer"]
                    },
                    "rental_income": {
                        "recognition": "Straight-line over lease term (or per lease if rent is level)",
                        "free_rent_periods": "Average rent over entire lease term including free periods"
                    }
                }
            }
        },

        "chapter_4_internal_controls": {
            "title": "Internal Controls and Fraud Prevention",
            "content": {
                "coso_framework": {
                    "components": [
                        "Control Environment - Tone at the top, ethics, competence",
                        "Risk Assessment - Identify and analyze risks",
                        "Control Activities - Policies and procedures",
                        "Information & Communication - Right info to right people",
                        "Monitoring - Assess quality of controls over time"
                    ]
                },
                "key_controls": {
                    "segregation_of_duties": {
                        "principle": "Separate authorization, recordkeeping, and custody of assets",
                        "examples": [
                            "Different people approve purchases, receive goods, and pay invoices",
                            "Different people open mail/receive payments and record receivables",
                            "Different people have access to inventory vs. inventory records"
                        ],
                        "small_business_workaround": "Owner review and approval of key transactions"
                    },
                    "authorization_controls": {
                        "examples": [
                            "Approval limits ($500 supervisor, $5K manager, $50K+ director)",
                            "Dual signatures on checks over threshold",
                            "Written policies for employee reimbursements"
                        ]
                    },
                    "physical_controls": {
                        "examples": [
                            "Locked storage for inventory and supplies",
                            "Limited access to cash/check stock",
                            "Security cameras in cash handling areas",
                            "IT controls (passwords, access rights, backups)"
                        ]
                    },
                    "reconciliation_controls": {
                        "monthly_requirements": [
                            "Bank reconciliations (reviewed by someone independent)",
                            "Credit card reconciliations",
                            "Accounts receivable aging review",
                            "Inventory cycle counts",
                            "Fixed asset physical verification (annually)"
                        ]
                    }
                },
                "fraud_red_flags": [
                    "Living beyond means",
                    "Financial difficulties",
                    "Unusually close relationship with vendors/customers",
                    "Control issues or unwillingness to share duties",
                    "Wheeler-dealer attitude",
                    "Never takes vacation (can't let someone else see their work)",
                    "Excessive journal entries near period end",
                    "Unexplained inventory shortages",
                    "Customer complaints about payments not credited"
                ],
                "best_practices": [
                    "Require all employees to take vacation",
                    "Rotate duties periodically",
                    "Conduct surprise audits",
                    "Review expense reports for reasonableness",
                    "Monitor payroll changes",
                    "Review all bank and credit card statements personally",
                    "Implement whistleblower hotline",
                    "Background checks on employees handling cash/finances"
                ]
            }
        }
    }
}

REAL_ESTATE_ACCOUNTING_GUIDE = {
    "title": "Real Estate Accounting - Advanced Guide",
    "chapters": {
        "rental_property_accounting": {
            "title": "Rental Property Accounting Best Practices",
            "content": {
                "property_level_tracking": {
                    "importance": "Track income and expenses separately for each property",
                    "methods": [
                        "Create class/division per property in accounting software",
                        "Use sub-accounts with property codes (e.g., 4000-Property1, 4000-Property2)",
                        "Maintain separate bank accounts per property (best practice)"
                    ],
                    "benefits": [
                        "Analyze profitability by property",
                        "Support for refinancing or sale",
                        "Easier tax reporting (Schedule E)",
                        "Track performance vs. budget by property"
                    ]
                },
                "security_deposits": {
                    "accounting_treatment": "Liability (not income) until earned or forfeited",
                    "entry_received": {
                        "debit": "Cash (or Security Deposit Trust Account)",
                        "credit": "Tenant Security Deposits Liability"
                    },
                    "entry_forfeited": {
                        "debit": "Tenant Security Deposits Liability",
                        "credit": "Other Income (or offset to expense if for damages)"
                    },
                    "trust_accounting": {
                        "required_states": ["California", "Florida", "New York (>6 units)", "Many others"],
                        "requirements": "Separate bank account, no commingling, interest bearing in some states",
                        "reconciliation": "Monthly reconcile trust liability to trust bank balance"
                    }
                },
                "prepaid_vs_accrued_rent": {
                    "advance_rent": {
                        "definition": "Rent received before period covered",
                        "accounting": "Liability (Unearned Rent) until earned",
                        "tax_treatment": "Taxable when received (cash or accrual)"
                    },
                    "rent_receivable": {
                        "definition": "Rent earned but not yet received",
                        "accounting": "Asset (Rent Receivable) + Revenue",
                        "tax_treatment_accrual": "Taxable when earned",
                        "tax_treatment_cash": "Not taxable until received"
                    }
                },
                "capital_vs_repairs": {
                    "capital_improvements": {
                        "definition": "Betterments, adaptations, or restorations that increase value or extend life",
                        "examples": ["New roof", "HVAC replacement", "Room additions", "Major kitchen remodel"],
                        "accounting": "Capitalize (add to building cost) and depreciate",
                        "tax_treatment": "Depreciate over 27.5 years (residential) or 39 years (commercial)"
                    },
                    "repairs_maintenance": {
                        "definition": "Keeps property in ordinary operating condition, doesn't add value or extend life",
                        "examples": ["Paint", "Minor plumbing/electrical fixes", "Appliance repairs", "Landscaping"],
                        "accounting": "Expense immediately",
                        "tax_treatment": "Fully deductible in year incurred"
                    },
                    "safe_harbor_elections": {
                        "de_minimis": {
                            "limit": "$2,500 per invoice/item (with applicable financial statement) or $500 without",
                            "benefit": "Expense items that might otherwise be capitalized",
                            "election": "Attach statement to tax return"
                        },
                        "routine_maintenance": {
                            "definition": "Recurring activities expected more than once during 10-year period",
                            "examples": ["HVAC tune-ups", "Roof inspections and minor repairs"],
                            "benefit": "Deduct even if work adds value"
                        }
                    }
                }
            }
        },

        "depreciation_mastery": {
            "title": "Real Estate Depreciation Strategies",
            "content": {
                "basic_depreciation": {
                    "residential_rental": {
                        "period": "27.5 years",
                        "method": "Straight-line",
                        "basis": "Building only (not land)",
                        "calculation": "Building Cost / 27.5 = Annual Depreciation",
                        "example": "$300K purchase, $50K land = $250K building / 27.5 = $9,091/year"
                    },
                    "commercial_property": {
                        "period": "39 years",
                        "method": "Straight-line",
                        "basis": "Building and improvements",
                        "calculation": "Building Cost / 39 = Annual Depreciation"
                    },
                    "land_allocation": {
                        "methods": [
                            "Tax assessed value ratio (land vs building)",
                            "Appraisal allocation",
                            "Typical ratio for area (often 20-30% land)"
                        ],
                        "importance": "Land is never depreciable - only building and improvements"
                    }
                },
                "cost_segregation_detailed": {
                    "definition": "Engineering study to identify components depreciable over shorter lives",
                    "components": {
                        "5_year_property": [
                            "Carpet and flooring",
                            "Appliances",
                            "Decorative lighting",
                            "Window treatments"
                        ],
                        "7_year_property": [
                            "Office furniture and fixtures",
                            "Some equipment"
                        ],
                        "15_year_property": [
                            "Land improvements (parking lot, sidewalks, landscaping)",
                            "Fencing",
                            "Exterior lighting"
                        ],
                        "27.5_or_39_year": [
                            "Building structure",
                            "HVAC",
                            "Plumbing",
                            "Electrical (unless specifically serving 5/7/15-year property)"
                        ]
                    },
                    "process": {
                        "step_1": "Hire cost segregation specialist (engineer + tax professional)",
                        "step_2": "Provide purchase documents, building plans, photos",
                        "step_3": "Specialist allocates costs to appropriate classes",
                        "step_4": "File Form 3115 (change in accounting method) if prior year acquisition",
                        "step_5": "Take catch-up depreciation in current year (479 adjustment)"
                    },
                    "example_results": {
                        "property": "$2M commercial building",
                        "without_cost_seg": "$2M / 39 years = $51,282/year",
                        "with_cost_seg": [
                            "5-year: $300K × 20% (bonus) = $60K year 1",
                            "7-year: $150K × 14.29% = $21,435 year 1",
                            "15-year: $250K × 5% = $12,500 year 1",
                            "39-year: $1.3M / 39 = $33,333 year 1",
                            "Total Year 1: $127,268 (vs $51,282 without)"
                        ]
                    },
                    "roi": {
                        "study_cost": "$5K-$15K",
                        "typical_benefit": "$50K-$200K+ additional first-year deductions",
                        "payback": "Immediate (tax savings far exceed cost)"
                    }
                }
            }
        }
    }
}

TAX_PLANNING_GUIDE = {
    "title": "Year-Round Tax Planning Strategies",
    "timeline": {
        "january_march": {
            "tasks": [
                "Gather prior year tax documents",
                "Make prior year retirement contributions (by April 15 or extension deadline)",
                "File prior year tax returns",
                "Make Q1 estimated tax payment (April 15)",
                "Review prior year return for planning opportunities",
                "Set up tax software/systems for current year"
            ],
            "planning_opportunities": [
                "Make deductible IRA contribution for prior year",
                "Contribute to HSA for prior year (until April 15)",
                "Complete prior year SEP-IRA or solo 401(k) contributions (by extension deadline)"
            ]
        },
        "april_june": {
            "tasks": [
                "Make Q2 estimated tax payment (June 15)",
                "Review Q1 financials and adjust estimates",
                "Plan mid-year tax strategies"
            ],
            "planning_opportunities": [
                "Project full year income and tax liability",
                "Evaluate Roth conversion opportunity",
                "Consider purchasing equipment before year-end (plan ahead)",
                "Review estimated tax payments for accuracy"
            ]
        },
        "july_september": {
            "tasks": [
                "Make Q3 estimated tax payment (September 15)",
                "Mid-year tax projection",
                "Plan Q4 strategies"
            ],
            "planning_opportunities": [
                "Execute Roth conversions in lower-income years",
                "Harvest capital losses to offset gains",
                "Prepay state/local taxes if beneficial (SALT cap)",
                "Review and adjust estimated payments"
            ]
        },
        "october_december": {
            "tasks": [
                "Year-end tax planning meeting",
                "Make Q4 estimated payment (January 15 of next year)",
                "Execute year-end strategies",
                "Finalize retirement contributions"
            ],
            "critical_year_end_moves": [
                "Max out 401(k) contributions (payroll deduction by Dec 31)",
                "Make charitable contributions by Dec 31",
                "Harvest tax losses by Dec 31",
                "Pay estimated state taxes by Dec 31 (if itemizing)",
                "Purchase and place equipment in service by Dec 31 (Section 179, bonus depreciation)",
                "Pay January rent in December (if cash basis)",
                "Defer income to next year if possible",
                "Prepay expenses to current year if beneficial"
            ]
        }
    },
    "quarterly_estimated_taxes": {
        "who_must_pay": [
            "Self-employed individuals",
            "S-Corp owners receiving distributions",
            "Landlords with rental income",
            "Anyone with income not subject to withholding"
        ],
        "safe_harbor_rules": {
            "pay_110_percent": "Pay 110% of prior year tax (if AGI > $150K) to avoid penalty",
            "pay_100_percent": "Pay 100% of prior year tax (if AGI ≤ $150K)",
            "pay_90_percent": "Pay 90% of current year tax",
            "choose_highest": "Use whichever safe harbor is most beneficial"
        },
        "calculation_method": {
            "simple": "Prior year tax / 4 = Quarterly payment",
            "annualized": "Calculate income to date, annualize, calculate tax, pay installment (allows for uneven income)",
            "best_practice": "Use annualized method if income is seasonal or lumpy"
        },
        "penalties": {
            "rate": "IRS interest rate (varies quarterly, typically 5-8%)",
            "waiver": "Can request waiver for casualty, disaster, or first-time filer",
            "tip": "Underpayment penalty is usually small - focus on minimizing actual tax, not penalty"
        }
    }
}

COMPLIANCE_CHECKLIST = {
    "monthly_tasks": {
        "bookkeeping": [
            "Record all revenue and expenses",
            "Reconcile bank accounts",
            "Reconcile credit card accounts",
            "Review accounts receivable aging",
            "Review accounts payable aging",
            "Record depreciation (if using accrual)",
            "Review and approve journal entries",
            "Run financial reports (P&L, Balance Sheet, Cash Flow)"
        ],
        "payroll": [
            "Process payroll",
            "Remit payroll taxes (semi-weekly or monthly)",
            "Record payroll journal entries"
        ]
    },
    "quarterly_tasks": {
        "tax_filings": [
            "Form 941 - Employer's Quarterly Federal Tax Return",
            "State quarterly payroll tax returns",
            "Estimated tax payments (Form 1040-ES)",
            "State estimated tax payments"
        ],
        "reviews": [
            "Review quarterly financial statements",
            "Variance analysis (actual vs budget)",
            "Cash flow projection update",
            "Review accounts receivable for collectibility",
            "Physical inventory count (if material)",
            "Update depreciation schedules"
        ]
    },
    "annual_tasks": {
        "tax_filings": [
            "Form 1040 - Individual Income Tax Return",
            "Schedule C - Business Income (Sole Proprietor)",
            "Schedule E - Rental Income",
            "Form 1120-S - S-Corporation Return",
            "Form 1065 - Partnership Return",
            "Form 1120 - C-Corporation Return",
            "Form 990 - Non-profit Information Return",
            "W-2s and 1099s (due January 31)",
            "Form 940 - Employer's Annual Federal Unemployment Tax",
            "State income tax returns",
            "Property tax returns (if applicable)",
            "Sales/use tax returns (if applicable)"
        ],
        "compliance": [
            "Audit financial statements (if required)",
            "Update corporate minutes and resolutions",
            "File annual report with state",
            "Renew business licenses",
            "Review and renew insurance policies",
            "Update operating agreements/bylaws",
            "Beneficial ownership reporting (FinCEN - new requirement)"
        ],
        "planning": [
            "Prepare annual budget for next year",
            "Tax planning meeting",
            "Review business entity structure",
            "Update succession/exit plan",
            "Review and update internal controls"
        ]
    }
}


def get_guide(guide_type: str) -> Dict[str, Any]:
    """Get specific accounting guide"""
    guides = {
        "fundamentals": ACCOUNTING_FUNDAMENTALS_GUIDE,
        "real_estate": REAL_ESTATE_ACCOUNTING_GUIDE,
        "tax_planning": TAX_PLANNING_GUIDE,
        "compliance": COMPLIANCE_CHECKLIST
    }
    return guides.get(guide_type, {})


__all__ = [
    "ACCOUNTING_FUNDAMENTALS_GUIDE",
    "REAL_ESTATE_ACCOUNTING_GUIDE",
    "TAX_PLANNING_GUIDE",
    "COMPLIANCE_CHECKLIST",
    "get_guide"
]
