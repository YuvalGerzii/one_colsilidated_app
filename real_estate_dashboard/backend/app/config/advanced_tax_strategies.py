"""
Advanced Tax Strategies, Loopholes, and Expert Accountant Tips

This module contains comprehensive tax optimization strategies, legal loopholes,
and expert-level accounting techniques used by Big-4 firms and tax professionals.

WARNING: These strategies should be implemented with professional tax advice.
Always consult with a licensed CPA or tax attorney before implementation.
"""

from typing import Dict, List, Any


# ============================================================================
# ADVANCED REAL ESTATE TAX STRATEGIES
# ============================================================================

REAL_ESTATE_TAX_STRATEGIES = {
    "cost_segregation_advanced": {
        "name": "Advanced Cost Segregation with Bonus Depreciation",
        "category": "Real Estate",
        "complexity": "High",
        "potential_savings": "20-40% of property value in year 1",
        "description": "Identify and reclassify personal property components of buildings to accelerate depreciation",
        "strategy": [
            "Hire cost segregation specialist to perform detailed engineering study",
            "Identify 5, 7, and 15-year property components (carpets, lighting, landscaping, parking lot)",
            "Reclassify from 27.5/39-year to shorter depreciation periods",
            "Apply 100% bonus depreciation (if property acquired before 2023)",
            "Generate immediate tax deductions instead of spreading over decades"
        ],
        "irs_code": "IRC §168(k) - Bonus Depreciation, Rev. Proc. 2011-14",
        "best_for": ["Commercial properties over $1M", "Properties with significant tenant improvements"],
        "timing": "First year of service or after major renovation",
        "risks": "IRS scrutiny if study is not detailed and defensible",
        "tips": [
            "Cost segregation studies typically cost $5K-$15K but can generate $100K+ in tax savings",
            "Can be applied retroactively with 3115 form for prior year acquisitions",
            "Most valuable for high-income taxpayers in top tax brackets",
            "Consider impact on state taxes (some states don't conform to federal bonus depreciation)"
        ]
    },

    "section_1031_reverse_exchange": {
        "name": "Reverse 1031 Exchange",
        "category": "Real Estate",
        "complexity": "High",
        "potential_savings": "Defer 100% of capital gains",
        "description": "Buy replacement property BEFORE selling relinquished property",
        "strategy": [
            "Use Exchange Accommodation Titleholder (EAT) to park new property",
            "Close on replacement property within 45 days",
            "Sell old property within 180 days of parking arrangement",
            "Complete exchange without triggering capital gains tax"
        ],
        "irs_code": "Revenue Procedure 2000-37",
        "best_for": ["Hot markets where you find perfect replacement first", "Time-sensitive opportunities"],
        "timing": "When replacement property must be secured before selling current property",
        "risks": "Higher costs due to EAT fees, financing complexities",
        "tips": [
            "Must use qualified intermediary - cannot take possession",
            "All cash flow from old property must go into replacement",
            "Can combine with improvement exchange for even more flexibility",
            "Works best when you have cash or credit line for down payment on new property"
        ]
    },

    "improvement_exchange": {
        "name": "1031 Improvement/Build-to-Suit Exchange",
        "category": "Real Estate",
        "complexity": "Very High",
        "potential_savings": "Defer gains + improve property value",
        "description": "Use exchange proceeds to improve replacement property",
        "strategy": [
            "Identify replacement property that needs improvements",
            "Use EAT to hold property during 180-day exchange period",
            "Direct exchange funds to make improvements",
            "Complete improvements before exchange period ends"
        ],
        "irs_code": "Revenue Procedure 2000-37",
        "best_for": ["Value-add investors", "Properties needing renovation"],
        "requirements": [
            "Improvements must be completed within 180 days",
            "Cannot receive personal use of property during exchange",
            "Must reinvest all proceeds plus debt to avoid boot"
        ],
        "tips": [
            "Plan improvements before starting exchange",
            "Get contractor bids lined up in advance",
            "Consider construction timeline carefully - must finish in 180 days",
            "Can add significant value while deferring all gains"
        ]
    },

    "opportunity_zone_investment": {
        "name": "Qualified Opportunity Zone Investment",
        "category": "Real Estate",
        "complexity": "High",
        "potential_savings": "Permanent elimination of gains + tax-free appreciation",
        "description": "Invest capital gains in designated Opportunity Zones for massive tax benefits",
        "benefits": [
            "Defer capital gains until 2026 (or when QOZ investment is sold)",
            "Reduce original gain by 10% if held 5+ years (must invest by 2021)",
            "100% exclusion of QOZ appreciation if held 10+ years"
        ],
        "strategy": [
            "Invest realized capital gains (from any source) within 180 days",
            "Invest through Qualified Opportunity Fund (QOF)",
            "Hold QOF investment for 10+ years to eliminate all appreciation tax",
            "Can stack with 1031 exchange by selling replacement property and investing gains in QOZ"
        ],
        "irs_code": "IRC §1400Z-2, Tax Cuts and Jobs Act",
        "best_for": ["Long-term real estate investors", "High capital gains events"],
        "example": "Invest $1M gain in QOZ, hold 10 years. Original $1M gain taxed in 2026. If QOZ grows to $3M, the $2M appreciation is tax-free forever.",
        "tips": [
            "Focus on designated Opportunity Zones with strong growth potential",
            "Can invest stock market gains, business sale proceeds, any capital gain",
            "Must invest gains within 180 days of sale",
            "10-year hold requirement for full benefit - plan accordingly"
        ]
    },

    "real_estate_professional_status": {
        "name": "Real Estate Professional Status (REPS)",
        "category": "Real Estate",
        "complexity": "Medium",
        "potential_savings": "Unlimited passive loss deductions",
        "description": "Qualify as real estate professional to deduct unlimited rental losses against ordinary income",
        "requirements": [
            "Spend 750+ hours per year in real property trades/businesses",
            "More than 50% of personal services in real property trades",
            "Materially participate in each rental activity (100+ hours/year per property)"
        ],
        "strategy": [
            "Track all time spent on real estate activities meticulously",
            "Document property visits, tenant meetings, repairs, research",
            "If married, only one spouse needs to qualify",
            "Combine with cost segregation for massive first-year losses"
        ],
        "irs_code": "IRC §469(c)(7)",
        "best_for": ["Full-time real estate investors", "Spouses of high-earners"],
        "example": "W-2 earning $500K + spouse is REPS with $200K rental loss from cost segregation = $300K taxable income",
        "tips": [
            "Keep detailed time logs - IRS frequently audits REPS claims",
            "Use time-tracking apps for documentation",
            "Include time for education, research, property search",
            "Can still have a job as long as real estate is more than 50% of working time",
            "If both spouses work, have lower-earning spouse become REPS"
        ]
    },

    "short_term_rental_loophole": {
        "name": "Short-Term Rental Tax Loophole",
        "category": "Real Estate",
        "complexity": "Medium",
        "potential_savings": "Deduct losses against W-2 income without REPS",
        "description": "Average rental stays under 7 days to avoid passive loss limitations",
        "strategy": [
            "Rent property on Airbnb/VRBO with average stay under 7 days",
            "Provide substantial services (cleaning, concierge, breakfast)",
            "Materially participate (500+ hours/year or meet other tests)",
            "Losses become non-passive and deductible against W-2 income"
        ],
        "requirements": [
            "Average rental period ≤ 7 days, OR",
            "Average rental period ≤ 30 days AND significant personal services provided",
            "Material participation in the activity"
        ],
        "irs_code": "IRC §469(c)(7), Temp. Reg. 1.469-1T(e)(3)(ii)",
        "best_for": ["W-2 employees who can't qualify for REPS", "Vacation rental owners"],
        "example": "Doctor earning $400K with STR generating $50K loss from cost segregation = $350K taxable income",
        "tips": [
            "Track average length of stay carefully",
            "Document substantial services provided",
            "Keep time logs showing material participation",
            "Combine with cost segregation in year 1 for massive deductions",
            "Can have multiple STRs and aggregate hours for material participation"
        ]
    },

    "primary_residence_exclusion": {
        "name": "Primary Residence Sale Exclusion + Rental Conversion",
        "category": "Real Estate",
        "complexity": "Medium",
        "potential_savings": "$250K-$500K gain exclusion",
        "description": "Convert rental back to primary residence to claim tax-free gains",
        "strategy": [
            "Live in property 2 of last 5 years before sale",
            "Exclude $250K gain (single) or $500K gain (married)",
            "Pro-rate exclusion for years as rental (post-2008)",
            "Recapture depreciation taken as rental at 25% rate"
        ],
        "irs_code": "IRC §121",
        "best_for": ["Converting former primary residence to rental", "House hacking investors"],
        "example": "Buy house $300K, live 2 years, rent 3 years, sell $800K. Depreciate $30K as rental. Gain: $500K qualified, $30K depreciation recapture.",
        "calculation": [
            "Total gain: $500K",
            "Qualified gain: $500K × (2 years primary / 5 years owned) = $200K",
            "Taxable: $300K non-qualified + $30K depreciation recapture"
        ],
        "tips": [
            "Move back into rental property before selling if you can exclude more gain",
            "Can use multiple times (not limited to once per lifetime)",
            "Must own and live in property for 2 years (not necessarily consecutive)",
            "Can't have used exclusion in prior 2 years",
            "Pro-ration rule only applies to non-qualified use after 2008"
        ]
    },

    "installment_sale_strategy": {
        "name": "Installment Sale Tax Deferral",
        "category": "Real Estate",
        "complexity": "Medium",
        "potential_savings": "Spread capital gains over multiple years",
        "description": "Seller financing to defer capital gains recognition",
        "strategy": [
            "Sell property with owner financing",
            "Receive payments over multiple years",
            "Pay capital gains tax only as payments received",
            "Charge interest to buyers (which is ordinary income)"
        ],
        "irs_code": "IRC §453",
        "best_for": ["Sellers with large gains", "Reducing Medicare taxes", "Staying in lower tax bracket"],
        "benefits": [
            "Avoid triggering high income year with all gains at once",
            "May qualify for lower capital gains rates in future years",
            "Collect interest income in addition to sale proceeds",
            "Buyer may pay premium for seller financing"
        ],
        "tips": [
            "Minimum interest rate = AFR (Applicable Federal Rate) to avoid imputed interest",
            "Can combine with 1031 exchange for partial proceeds",
            "Consider life insurance to protect against buyer default",
            "Structure as wrap-around mortgage if existing loan in place"
        ]
    }
}

# ============================================================================
# ADVANCED BUSINESS TAX STRATEGIES
# ============================================================================

BUSINESS_TAX_STRATEGIES = {
    "s_corp_election": {
        "name": "S-Corp Election for Self-Employment Tax Savings",
        "category": "Business Structure",
        "complexity": "Medium",
        "potential_savings": "15.3% on distributions above reasonable salary",
        "description": "Elect S-Corp to split income into salary + distributions and save on SE tax",
        "strategy": [
            "Form LLC or C-Corp and elect S-Corp status (Form 2553)",
            "Pay yourself reasonable salary (subject to payroll taxes)",
            "Take remaining profits as distributions (no SE tax)",
            "Save 15.3% SE tax on distribution portion"
        ],
        "example": "$200K profit → $100K salary (pay SE tax) + $100K distribution (no SE tax) = $15,300 savings",
        "best_for": ["Self-employed making $60K+", "Single-member LLCs"],
        "requirements": [
            "Must pay reasonable salary for work performed",
            "Additional payroll tax filings (941, W-2, W-3)",
            "State payroll taxes may apply"
        ],
        "tips": [
            "IRS watches for unreasonably low salaries",
            "Benchmark salary against industry standards",
            "Usually makes sense at $60K+ net income",
            "Consider costs of payroll service ($500-2000/year)",
            "Can elect retroactively within 2.5 months of year start"
        ]
    },

    "qualified_business_income_deduction": {
        "name": "199A Qualified Business Income (QBI) Deduction Optimization",
        "category": "Business Deductions",
        "complexity": "High",
        "potential_savings": "Up to 20% of qualified business income",
        "description": "Maximize the 199A pass-through deduction through strategic planning",
        "base_rule": "Deduct 20% of QBI from pass-through entities (LLC, S-Corp, partnership)",
        "income_limits_2025": {
            "single": {"phase_in": 191900, "phase_out": 241900},
            "married": {"phase_in": 383800, "phase_out": 483800}
        },
        "strategies": [
            "Keep taxable income below threshold to avoid limitations",
            "If over threshold, increase W-2 wages to employees",
            "Purchase qualifying property to meet unadjusted basis test",
            "Separate specified service trade/business (SSTB) income",
            "Use multiple entities to manage income levels"
        ],
        "sstb_exceptions": [
            "Engineering and architecture (not SSTB)",
            "Real estate brokerage and development (not SSTB)",
            "Insurance and real estate agents (not SSTB if receive 1099-MISC)"
        ],
        "optimization_tips": [
            "Pay family members reasonable wages to increase W-2 wages",
            "Buy equipment before year-end to increase qualified property",
            "Defer income to next year if close to phase-out threshold",
            "Accelerate deductions to stay below threshold",
            "Consider Roth conversions to fill up lower brackets while taking 199A"
        ]
    },

    "augusta_rule": {
        "name": "Augusta Rule - Tax-Free Home Rental Income",
        "category": "Business Deductions",
        "complexity": "Low",
        "potential_savings": "$2,000 - $10,000+ tax-free",
        "description": "Rent your home to your business for up to 14 days tax-free",
        "strategy": [
            "Business rents your home for meetings, events, retreats",
            "Charge fair market rate (compare to local venues)",
            "Business deducts rent as ordinary expense",
            "You receive rent tax-free (not reported on personal return)",
            "Limited to 14 days per year"
        ],
        "irs_code": "IRC §280A(g)",
        "documentation_required": [
            "Board meeting minutes authorizing rental",
            "Rental agreement between business and homeowner",
            "Proof of actual business use (agendas, attendee lists)",
            "Comparable rental rates from similar venues"
        ],
        "best_for": ["Business owners with home offices", "S-Corp owners", "Professional corporations"],
        "example": "Rent home for 12 board meetings at $500/day = $6,000 tax-free income + $6,000 business deduction (save ~$2,500 total)",
        "tips": [
            "Document everything - IRS audits this frequently",
            "Use for genuine business purposes (board meetings, strategy sessions)",
            "Charge rates comparable to hotels or conference centers",
            "Don't exceed 14 days or all income becomes taxable",
            "Can stack with home office deduction"
        ]
    },

    "accountable_plan": {
        "name": "Accountable Plan for Tax-Free Employee Reimbursements",
        "category": "Business Deductions",
        "complexity": "Low",
        "potential_savings": "Convert personal expenses to tax-free business reimbursements",
        "description": "Establish formal accountable plan to reimburse employees for business expenses",
        "requirements": [
            "Expenses must have business connection",
            "Employee must adequately account within reasonable time (60 days)",
            "Employee must return excess reimbursements within reasonable time (120 days)"
        ],
        "reimbursable_expenses": [
            "Mileage at IRS rate ($0.67/mile for 2024)",
            "Home office expenses",
            "Cell phone usage (business portion)",
            "Internet service (business portion)",
            "Continuing education",
            "Professional subscriptions",
            "Business travel and meals"
        ],
        "strategy": [
            "Draft accountable plan policy",
            "Track all business use of personal assets",
            "Submit expense reports with receipts",
            "Receive tax-free reimbursements",
            "Business deducts as ordinary expense"
        ],
        "example": "Reimburse employee-shareholder $15K/year for home office, mileage, cell phone = $15K tax-free vs $15K raise (taxable)",
        "tips": [
            "Must be actual reimbursement, not flat allowance",
            "Keep detailed records and receipts",
            "Submit reports at least quarterly",
            "Works for S-Corp owners who are employees",
            "More restrictive for 2%+ S-Corp shareholders"
        ]
    },

    "defined_benefit_pension": {
        "name": "Defined Benefit Pension Plan for High-Income Earners",
        "category": "Retirement",
        "complexity": "Very High",
        "potential_savings": "Contribute $100K-$300K+ annually (tax-deductible)",
        "description": "Set up pension plan allowing massive tax-deductible contributions for older, high-income owners",
        "best_for": [
            "Age 50+ business owners",
            "Consistent high income ($200K+)",
            "Few or no employees",
            "Want to contribute more than 401(k) limits"
        ],
        "contribution_limits": "Based on actuarial calculations, can exceed $200K annually",
        "strategy": [
            "Hire actuary to design plan based on age and income",
            "Older you are, higher the contribution limits",
            "Must contribute to employees if you have them",
            "Deduct contributions as business expense",
            "Tax-deferred growth until retirement"
        ],
        "example": "55-year-old with $500K income can contribute $180K to DB plan vs $69K to SEP-IRA",
        "costs": "Setup: $2K-5K, Annual admin: $2K-5K",
        "tips": [
            "Best if you're older than your employees",
            "Requires annual contributions (not flexible like 401k)",
            "Can combine with 401(k) for even more contributions",
            "Need consistent income to meet annual funding requirements",
            "Consider cash balance plan variation for more flexibility"
        ]
    },

    "captive_insurance_company": {
        "name": "Captive Insurance Company (831(b) Election)",
        "category": "Advanced Planning",
        "complexity": "Very High",
        "potential_savings": "$1.2M+ tax-deferred over time",
        "description": "Form your own insurance company to insure business risks and defer taxes",
        "strategy": [
            "Form insurance company (usually offshore in Montana, Vermont, or Cayman Islands)",
            "Business pays premiums to captive (tax-deductible)",
            "Captive receives premiums tax-free under 831(b) election",
            "Insure against legitimate business risks",
            "Investment income grows tax-deferred"
        ],
        "irs_code": "IRC §831(b)",
        "premium_limit_2025": "$2.8M annually (indexed for inflation)",
        "legitimate_risks_to_insure": [
            "Cybersecurity breaches",
            "Key employee loss",
            "Business interruption",
            "Product liability",
            "Regulatory changes",
            "Pandemic-related losses"
        ],
        "requirements": [
            "Must insure legitimate business risks",
            "Premiums must be actuarially sound",
            "Cannot be used primarily for tax avoidance",
            "Must have risk distribution (multiple insureds or policies)"
        ],
        "warnings": [
            "IRS listed transaction - high audit risk if not structured properly",
            "Must use reputable advisors (not promoter-driven schemes)",
            "Setup costs: $25K-50K, Annual costs: $10K-25K",
            "Works best for businesses with $1M+ income"
        ],
        "tips": [
            "Use for legitimate risk management, not just tax savings",
            "Hire independent actuary to determine appropriate premiums",
            "Insure actual business risks with written policies",
            "Keep captive separate from operating business",
            "File all required forms (8886, 8832)"
        ]
    }
}

# ============================================================================
# HIGH NET WORTH TAX STRATEGIES
# ============================================================================

HIGH_NET_WORTH_STRATEGIES = {
    "spousal_lifetime_access_trust": {
        "name": "Spousal Lifetime Access Trust (SLAT)",
        "category": "Estate Planning",
        "complexity": "Very High",
        "potential_savings": "Remove millions from taxable estate",
        "description": "Irrevocable trust for spouse that removes assets from estate while maintaining indirect access",
        "strategy": [
            "Create irrevocable trust for benefit of spouse (and children)",
            "Gift assets to trust using lifetime exemption ($13.61M per person in 2024)",
            "Spouse can receive distributions (removes assets from your estate)",
            "Assets grow outside your estate",
            "At spouse's death, assets pass to beneficiaries estate-tax-free"
        ],
        "benefits": [
            "Use lifetime gift tax exemption before it sunsets (2026)",
            "Assets removed from estate but spouse can access",
            "Future appreciation excluded from estate",
            "Creditor protection",
            "Can include life insurance for tax-free death benefit"
        ],
        "risks": [
            "If spouse dies first or you divorce, you lose access",
            "Irrevocable - cannot change mind",
            "Reciprocal trust doctrine if both spouses create identical SLATs"
        ],
        "tips": [
            "Use different terms if both spouses create SLATs (avoid reciprocal trust doctrine)",
            "Fund with appreciating assets for maximum benefit",
            "Consider before 2026 when exemption may drop to $7M",
            "Include spendthrift provisions for asset protection"
        ]
    },

    "intentionally_defective_grantor_trust": {
        "name": "Intentionally Defective Grantor Trust (IDGT)",
        "category": "Estate Planning",
        "complexity": "Very High",
        "potential_savings": "Transfer unlimited wealth with minimal gift tax",
        "description": "Sell assets to trust, freezing estate value while shifting appreciation to beneficiaries",
        "strategy": [
            "Create irrevocable grantor trust for beneficiaries",
            "Gift 10% of sale value to trust (seed money)",
            "Sell appreciating assets to trust in exchange for promissory note",
            "Trust pays you back with interest at AFR (low rate)",
            "All appreciation above AFR passes to beneficiaries estate-tax-free",
            "You pay income taxes on trust income (further gift to beneficiaries)"
        ],
        "example": "Sell $10M business to IDGT for promissory note at 5% AFR. Business grows to $50M over time. $40M appreciation passes to heirs gift/estate tax-free.",
        "benefits": [
            "Use small gift ($1M) to transfer much larger value ($10M+)",
            "All appreciation excluded from estate",
            "Paying trust's taxes is tax-free gift",
            "Can buy back assets if trust needs liquidity"
        ],
        "best_for": [
            "Business owners with rapidly appreciating assets",
            "Real estate developers",
            "Families with estates over exemption amount"
        ],
        "tips": [
            "AFR must be reasonable - IRS can recharacterize sale",
            "Trust must have substance (seed gift + note)",
            "Best with assets likely to appreciate above AFR",
            "Can swap assets in and out during your lifetime"
        ]
    },

    "grantor_retained_annuity_trust": {
        "name": "Grantor Retained Annuity Trust (GRAT)",
        "category": "Estate Planning",
        "complexity": "High",
        "potential_savings": "Transfer appreciation tax-free",
        "description": "Transfer appreciating assets while retaining annuity payments, passing excess to heirs gift-tax-free",
        "strategy": [
            "Transfer assets to GRAT for specified term (2-10 years)",
            "Receive annual annuity payments based on IRS 7520 rate",
            "At end of term, remaining assets pass to beneficiaries",
            "If assets appreciate above 7520 rate, excess passes gift-tax-free"
        ],
        "example": "Fund GRAT with $10M, 2-year term, 7520 rate 5.6%. Receive back $5.4M/year. Assets grow 20% = $14.4M. Keep $10.8M annuity, pass $3.6M to heirs gift-tax-free.",
        "structures": [
            "Zeroed-out GRAT: Annuity = initial value + 7520 rate (minimal gift tax)",
            "Rolling GRATs: Create new GRAT each year with annuity payments",
            "Walton GRAT: Backload annuity payments to maximize growth"
        ],
        "best_for": [
            "Volatile assets likely to outperform 7520 rate",
            "Pre-IPO stock",
            "Rapidly appreciating real estate",
            "Private equity interests"
        ],
        "risks": "If you die during GRAT term, assets included in estate",
        "tips": [
            "Use short terms (2 years) to reduce mortality risk",
            "Create multiple GRATs instead of one long GRAT",
            "Works best in low interest rate environment",
            "Can use for minority interest discounts on business interests"
        ]
    },

    "charitable_remainder_trust": {
        "name": "Charitable Remainder Trust (CRT)",
        "category": "Charitable Planning",
        "complexity": "High",
        "potential_savings": "Avoid capital gains + income stream + estate deduction",
        "description": "Donate appreciated assets to trust, receive income for life, remainder to charity",
        "strategy": [
            "Transfer highly appreciated assets to CRT",
            "CRT sells assets (no capital gains tax paid)",
            "Receive income for life (5-50% of trust value annually)",
            "Get immediate charitable deduction for remainder interest",
            "At death, remainder passes to charity",
            "Use income to buy life insurance to replace wealth for heirs"
        ],
        "types": [
            "CRUT (Charitable Remainder Unitrust): Variable payments based on % of annual value",
            "CRAT (Charitable Remainder Annuity Trust): Fixed payments"
        ],
        "example": "$5M stock with $200K basis. Donate to CRT. Save $1.2M capital gains tax + $2M charitable deduction. Receive $250K/year income. Use $100K to buy $5M life insurance for heirs.",
        "benefits": [
            "Avoid capital gains tax on highly appreciated assets",
            "Immediate income tax deduction (30-50% of value)",
            "Income for life or term of years",
            "Reduce estate taxes",
            "Satisfy charitable intent"
        ],
        "tips": [
            "Best for assets with large gains relative to basis",
            "NIMCRUT variation allows deferring distributions when young",
            "Can name family foundation as remainder beneficiary",
            "Use wealth replacement trust (life insurance) to benefit heirs"
        ]
    },

    "family_limited_partnership": {
        "name": "Family Limited Partnership (FLP) with Valuation Discounts",
        "category": "Estate Planning",
        "complexity": "High",
        "potential_savings": "20-40% valuation discounts on gifts",
        "description": "Transfer wealth to family members at discounted values using FLP structure",
        "strategy": [
            "Create FLP and contribute assets (real estate, investments, business)",
            "Retain 1% general partner interest (control)",
            "Gift limited partner interests to family (no control)",
            "Apply discounts for lack of control (15-25%) and lack of marketability (15-25%)",
            "Combined discount: 30-40% on gifted value"
        ],
        "example": "FLP owns $10M real estate. Gift 49% LP interests to children. Value with 35% discount = $3.185M gift instead of $4.9M. Save $1.7M gift tax.",
        "benefits": [
            "Leverage gift tax exemption with discounts",
            "Maintain control as GP",
            "Centralize asset management",
            "Creditor protection for limited partners",
            "Income splitting with family members"
        ],
        "irs_scrutiny": [
            "Must have legitimate business purpose beyond tax savings",
            "Cannot be formed on deathbed (IRS will include in estate)",
            "Must respect partnership formalities",
            "Need independent appraisal for discounts"
        ],
        "tips": [
            "Form early and build operating history",
            "Don't gift 100% (retain control)",
            "Make sure partnership serves non-tax purpose",
            "Get qualified appraisal for discount substantiation",
            "Alternative: LLC instead of LP (more flexible)"
        ]
    },

    "private_placement_life_insurance": {
        "name": "Private Placement Life Insurance (PPLI)",
        "category": "Advanced Planning",
        "complexity": "Very High",
        "potential_savings": "Tax-free growth on millions of investments",
        "description": "Variable life insurance wrapper for sophisticated investments with tax-free growth",
        "strategy": [
            "Purchase variable universal life insurance policy",
            "Fund policy with large premium ($250K-$5M minimum)",
            "Direct underlying investments (hedge funds, PE, real estate)",
            "Investments grow tax-deferred inside policy",
            "Access cash value tax-free via policy loans",
            "Death benefit passes income and estate tax-free"
        ],
        "benefits": [
            "Tax-free growth on alternative investments",
            "No 1099s on investment income",
            "Tax-free access via loans",
            "Estate tax-free death benefit",
            "Creditor protection in most states"
        ],
        "requirements": [
            "Minimum investment: $250K-$5M",
            "Must meet investor protection test (no self-dealing)",
            "Insurance company must control investments",
            "Need insurance need (not purely investment)"
        ],
        "best_for": [
            "Ultra-high net worth ($10M+ net worth)",
            "Sophisticated investors with hedge fund access",
            "International investors seeking US tax efficiency"
        ],
        "tips": [
            "Use offshore insurance company for maximum flexibility",
            "Structure in irrevocable trust to exclude from estate",
            "Choose low-cost, high-quality carrier",
            "Ensure legitimate insurance need"
        ]
    }
}

# ============================================================================
# INTERNATIONAL TAX STRATEGIES
# ============================================================================

INTERNATIONAL_TAX_STRATEGIES = {
    "puerto_rico_act_60": {
        "name": "Puerto Rico Act 60 - 4% Corporate Tax + 0% Capital Gains",
        "category": "International",
        "complexity": "High",
        "potential_savings": "87% tax reduction for qualifying income",
        "description": "Move to Puerto Rico to pay 4% corporate tax and 0% capital gains on PR-source income",
        "requirements": [
            "Become bona fide resident of Puerto Rico",
            "Pass 3-year presence test (183+ days/year in PR)",
            "File Form 8898 with IRS",
            "Obtain Act 60 decree from PR government"
        ],
        "benefits": [
            "4% corporate tax on export services (vs 21% federal + state)",
            "0% tax on capital gains and dividends from PR sources",
            "100% tax exemption on distributions from Act 60 businesses",
            "No federal income tax on PR-source income (if bona fide resident)"
        ],
        "qualifying_businesses": [
            "Software development and SaaS",
            "Consulting services to non-PR clients",
            "Investment management",
            "Trading (stocks, crypto, etc.)",
            "Research and development"
        ],
        "example": "$1M in consulting income: US tax ~$370K vs PR tax $40K = $330K savings annually",
        "tips": [
            "Must establish bona fide residence BEFORE generating income",
            "Capital gains on assets owned before move are still taxed by IRS",
            "Need closer connection to PR than any US state",
            "Consider quality of life, hurricanes, infrastructure"
        ]
    },

    "foreign_earned_income_exclusion": {
        "name": "Foreign Earned Income Exclusion (FEIE)",
        "category": "International",
        "complexity": "Medium",
        "potential_savings": "Exclude $120K+ of foreign earned income",
        "description": "Live abroad and exclude foreign earned income from US taxes",
        "exclusion_2025": "$126,500 per person (indexed for inflation)",
        "requirements": [
            "Tax home in foreign country",
            "Pass bona fide residence test (full tax year abroad), OR",
            "Pass physical presence test (330 days in 12-month period abroad)"
        ],
        "strategy": [
            "Move abroad and establish tax home",
            "Work for foreign employer or run business serving foreign clients",
            "Exclude up to $126K earned income per person",
            "Couple can exclude $253K combined",
            "Stack with foreign housing exclusion"
        ],
        "example": "Digital nomad earning $120K working from Portugal pays $0 US tax on earned income",
        "does_not_apply_to": [
            "Investment income (interest, dividends, capital gains)",
            "Rental income",
            "Pension income",
            "US source income"
        ],
        "tips": [
            "Time move carefully to maximize exclusion",
            "Keep careful records of days abroad",
            "Can still pay into Social Security via self-employment tax",
            "Combine with foreign tax credit for income over exclusion"
        ]
    }
}

# ============================================================================
# COMPLIANCE & AUDIT DEFENSE STRATEGIES
# ============================================================================

COMPLIANCE_STRATEGIES = {
    "audit_proof_documentation": {
        "name": "IRS Audit-Proof Documentation Standards",
        "category": "Compliance",
        "description": "Best practices for maintaining records that withstand IRS scrutiny",
        "documentation_requirements": {
            "business_expenses": [
                "Receipt or invoice",
                "Proof of payment (cancelled check, credit card statement)",
                "Business purpose (who, what, when, where, why)",
                "For meals: names of attendees and business discussed"
            ],
            "mileage": [
                "Date of trip",
                "Starting and ending locations",
                "Business purpose",
                "Odometer readings or GPS tracking"
            ],
            "home_office": [
                "Square footage of office and total home",
                "Photos of dedicated office space",
                "Evidence of regular and exclusive business use",
                "Utility bills and mortgage statements"
            ],
            "time_tracking": [
                "Contemporary time logs (not reconstructed)",
                "Specific activities performed",
                "Hours spent per activity",
                "For REPS: 750+ hours of real estate activities documented"
            ]
        },
        "retention_periods": {
            "tax_returns": "Forever (legally 7 years, practically forever)",
            "supporting_documents": "7 years from filing",
            "employment_tax_records": "4 years from due date or payment date",
            "property_records": "7 years after property sold",
            "retirement_plan_records": "Permanently"
        },
        "tips": [
            "Use accounting software that tracks everything",
            "Photograph receipts and store in cloud",
            "Keep business and personal expenses completely separate",
            "Document contemporaneously - not after the fact",
            "When in doubt, over-document"
        ]
    },

    "statute_of_limitations_management": {
        "name": "Managing IRS Statute of Limitations",
        "category": "Compliance",
        "description": "Understanding when IRS can audit and assess taxes",
        "general_rule": "3 years from filing or due date (whichever is later)",
        "extended_periods": {
            "substantial_understatement": "6 years if you omit 25%+ of gross income",
            "fraud": "Unlimited - no statute of limitations",
            "unfiled_return": "Unlimited - clock never starts",
            "foreign_income": "6 years if $5K+ foreign income not reported"
        },
        "tips": [
            "File on time even if you can't pay (starts statute clock)",
            "Don't extend statute of limitations without good reason",
            "Keep records for at least 7 years to be safe",
            "If you made mistake, file amended return within 3 years",
            "Foreign account holders: file FBAR or face unlimited statute"
        ]
    }
}

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def get_all_strategies() -> Dict[str, Any]:
    """Get all tax strategies organized by category"""
    return {
        "real_estate": REAL_ESTATE_TAX_STRATEGIES,
        "business": BUSINESS_TAX_STRATEGIES,
        "high_net_worth": HIGH_NET_WORTH_STRATEGIES,
        "international": INTERNATIONAL_TAX_STRATEGIES,
        "compliance": COMPLIANCE_STRATEGIES
    }

def get_strategies_by_complexity(complexity: str) -> List[Dict[str, Any]]:
    """Filter strategies by complexity level"""
    all_strategies = get_all_strategies()
    filtered = []

    for category, strategies in all_strategies.items():
        for key, strategy in strategies.items():
            if strategy.get("complexity", "").lower() == complexity.lower():
                filtered.append({**strategy, "key": key, "category": category})

    return filtered

def get_strategies_for_entity_type(entity_type: str) -> List[Dict[str, Any]]:
    """Get recommended strategies for specific entity type"""
    all_strategies = get_all_strategies()
    recommended = []

    mapping = {
        "small_business": ["business", "real_estate"],
        "property_management": ["real_estate", "business"],
        "high_net_worth": ["high_net_worth", "real_estate", "international"],
        "financial_institution": ["business", "high_net_worth"]
    }

    relevant_categories = mapping.get(entity_type, [])

    for category in relevant_categories:
        if category in all_strategies:
            for key, strategy in all_strategies[category].items():
                recommended.append({**strategy, "key": key, "category": category})

    return recommended


__all__ = [
    "REAL_ESTATE_TAX_STRATEGIES",
    "BUSINESS_TAX_STRATEGIES",
    "HIGH_NET_WORTH_STRATEGIES",
    "INTERNATIONAL_TAX_STRATEGIES",
    "COMPLIANCE_STRATEGIES",
    "get_all_strategies",
    "get_strategies_by_complexity",
    "get_strategies_for_entity_type"
]
