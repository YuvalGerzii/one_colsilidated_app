"""
Advanced Tax Strategy Calculators

This module provides sophisticated tax planning calculators for high net worth individuals,
businesses, and real estate investors. These strategies should be implemented with professional
guidance from licensed tax attorneys and CPAs.

WARNING: Many of these strategies are under IRS scrutiny. Always consult qualified professionals.
"""

from decimal import Decimal
from typing import Dict, List, Any, Optional
from datetime import datetime


class Section179BonusOptimizer:
    """
    Optimize between Section 179 expensing and Bonus Depreciation for maximum tax benefit.

    2024 Limits:
    - Section 179: $1,220,000 max, phaseout starts at $3,050,000
    - Bonus Depreciation: 60% (2024), 40% (2025), 20% (2026), 0% (2027+)

    2025 Limits:
    - Section 179: $1,250,000 max, phaseout starts at $3,130,000
    - Bonus Depreciation: 40%
    """

    @staticmethod
    def optimize_depreciation(
        asset_purchases: List[Dict[str, Any]],
        business_income: float,
        tax_year: int = 2024,
        state_bonus_conformity: bool = True
    ) -> Dict[str, Any]:
        """
        Optimize depreciation strategy across multiple assets.

        Args:
            asset_purchases: List of assets with cost, type, class_life
            business_income: Taxable income before depreciation
            tax_year: 2024 or 2025
            state_bonus_conformity: Does state conform to bonus depreciation?

        Returns:
            Optimization recommendation with tax savings
        """
        # Set limits based on year
        if tax_year == 2024:
            section_179_max = 1_220_000
            phaseout_threshold = 3_050_000
            bonus_rate = 0.60
        elif tax_year == 2025:
            section_179_max = 1_250_000
            phaseout_threshold = 3_130_000
            bonus_rate = 0.40
        else:
            section_179_max = 1_290_000  # Estimated inflation adjustment
            phaseout_threshold = 3_220_000
            bonus_rate = 0.20

        total_purchases = sum(asset['cost'] for asset in asset_purchases)

        # Calculate Section 179 phaseout
        if total_purchases > phaseout_threshold:
            phaseout_amount = total_purchases - phaseout_threshold
            section_179_available = max(0, section_179_max - phaseout_amount)
        else:
            section_179_available = section_179_max

        # Section 179 cannot exceed business income
        section_179_available = min(section_179_available, business_income)

        # Strategy 1: Maximize Section 179 first
        strategy_179_first = {
            'strategy_name': 'Section 179 First',
            'section_179_expense': 0,
            'bonus_depreciation': 0,
            'macrs_depreciation': 0,
            'total_year_1_deduction': 0,
            'assets_allocation': []
        }

        remaining_179 = section_179_available
        for asset in sorted(asset_purchases, key=lambda x: x.get('class_life', 39), reverse=True):
            if remaining_179 > 0:
                amount_179 = min(asset['cost'], remaining_179)
                remaining_cost = asset['cost'] - amount_179
                amount_bonus = remaining_cost * bonus_rate
                amount_macrs = remaining_cost * (1 - bonus_rate)

                strategy_179_first['section_179_expense'] += amount_179
                strategy_179_first['bonus_depreciation'] += amount_bonus
                strategy_179_first['macrs_depreciation'] += amount_macrs

                remaining_179 -= amount_179

                strategy_179_first['assets_allocation'].append({
                    'asset': asset['name'],
                    'cost': asset['cost'],
                    '179_amount': amount_179,
                    'bonus_amount': amount_bonus,
                    'macrs_amount': amount_macrs,
                    'year_1_deduction': amount_179 + amount_bonus + (amount_macrs * 0.1429)  # Half-year convention estimate
                })
            else:
                amount_bonus = asset['cost'] * bonus_rate
                amount_macrs = asset['cost'] * (1 - bonus_rate)

                strategy_179_first['bonus_depreciation'] += amount_bonus
                strategy_179_first['macrs_depreciation'] += amount_macrs

                strategy_179_first['assets_allocation'].append({
                    'asset': asset['name'],
                    'cost': asset['cost'],
                    '179_amount': 0,
                    'bonus_amount': amount_bonus,
                    'macrs_amount': amount_macrs,
                    'year_1_deduction': amount_bonus + (amount_macrs * 0.1429)
                })

        strategy_179_first['total_year_1_deduction'] = (
            strategy_179_first['section_179_expense'] +
            strategy_179_first['bonus_depreciation'] +
            (strategy_179_first['macrs_depreciation'] * 0.1429)
        )

        # Strategy 2: Use bonus first to create loss
        strategy_bonus_first = {
            'strategy_name': 'Bonus Depreciation First (Create Tax Loss)',
            'section_179_expense': 0,
            'bonus_depreciation': total_purchases * bonus_rate,
            'macrs_depreciation': total_purchases * (1 - bonus_rate),
            'total_year_1_deduction': 0
        }

        strategy_bonus_first['total_year_1_deduction'] = (
            strategy_bonus_first['bonus_depreciation'] +
            (strategy_bonus_first['macrs_depreciation'] * 0.1429)
        )

        # Calculate tax impact (assuming 37% federal + 5% state)
        federal_rate = 0.37
        state_rate = 0.05 if state_bonus_conformity else 0.00

        tax_savings_179_first = strategy_179_first['total_year_1_deduction'] * (federal_rate + state_rate)
        tax_savings_bonus_first = strategy_bonus_first['total_year_1_deduction'] * (federal_rate + state_rate)

        # Recommendation
        if business_income < section_179_available:
            recommendation = {
                'preferred_strategy': 'Bonus Depreciation First',
                'reason': f'Business income (${business_income:,.0f}) limits Section 179. Use bonus depreciation to create loss carryforward.',
                'year_1_savings': tax_savings_bonus_first,
                'nol_carryforward': max(0, strategy_bonus_first['total_year_1_deduction'] - business_income)
            }
        elif not state_bonus_conformity:
            recommendation = {
                'preferred_strategy': 'Section 179 First',
                'reason': 'State does not conform to bonus depreciation. Maximize Section 179 for state tax benefits.',
                'year_1_savings': tax_savings_179_first,
                'nol_carryforward': 0
            }
        else:
            recommendation = {
                'preferred_strategy': 'Section 179 First',
                'reason': 'Maximize current year deduction while preserving bonus depreciation for future years.',
                'year_1_savings': tax_savings_179_first,
                'nol_carryforward': 0
            }

        return {
            'total_asset_purchases': total_purchases,
            'business_income': business_income,
            'section_179_available': section_179_available,
            'bonus_rate': bonus_rate,
            'strategy_179_first': strategy_179_first,
            'strategy_bonus_first': strategy_bonus_first,
            'recommendation': recommendation,
            'warnings': [
                'Section 179 election must be made on original tax return',
                'Bonus depreciation can be elected out on an asset-class basis',
                'Consider state conformity before finalizing strategy',
                f'Bonus depreciation rate decreases to {int((bonus_rate - 0.20) * 100)}% in {tax_year + 1}'
            ]
        }


class DSTAnalyzer:
    """
    Delaware Statutory Trust (DST) analysis for 1031 exchanges.

    IRS Revenue Ruling 2004-86 allows DST interests to qualify as replacement property.
    """

    @staticmethod
    def analyze_dst_investment(
        relinquished_property_value: float,
        debt_on_relinquished: float,
        capital_gains_rate: float = 0.20,
        depreciation_recapture_rate: float = 0.25,
        dst_properties: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze DST investment for 1031 exchange compliance and tax deferral.

        Args:
            relinquished_property_value: Sale price of property being sold
            debt_on_relinquished: Mortgage/debt being released
            capital_gains_rate: Long-term capital gains rate
            depreciation_recapture_rate: Section 1250 recapture rate (25%)
            dst_properties: List of DST properties to invest in

        Returns:
            DST investment analysis
        """
        equity = relinquished_property_value - debt_on_relinquished

        # 1031 Exchange Requirements
        min_replacement_value = relinquished_property_value  # Equal or greater value
        min_debt_replacement = debt_on_relinquished  # Equal or greater debt

        # Calculate tax deferral
        assumed_basis = relinquished_property_value * 0.40  # Assume 40% basis
        capital_gain = relinquished_property_value - assumed_basis
        depreciation_recapture = assumed_basis * 0.30  # Assume 30% is recaptured depreciation

        deferred_capital_gains_tax = capital_gain * capital_gains_rate
        deferred_recapture_tax = depreciation_recapture * depreciation_recapture_rate
        total_tax_deferred = deferred_capital_gains_tax + deferred_recapture_tax

        # DST Benefits
        dst_benefits = {
            'passive_management': 'No landlord responsibilities',
            'institutional_grade_assets': 'Access to $20M+ properties',
            'diversification': 'Invest across multiple properties/markets',
            'partial_exchanges': 'Can invest partial proceeds in DST',
            'fractional_ownership': 'Lower minimum investment ($100k-$500k typical)',
            'professional_management': 'Experienced sponsors handle operations',
            '45_day_identification': 'Pre-packaged, immediately available',
            'estate_planning': 'Can divide among heirs'
        }

        # DST Risks
        dst_risks = {
            'illiquidity': 'Typically hold 5-10 years until sponsor sells',
            'no_control': 'Cannot vote on property decisions',
            'sponsor_risk': 'Dependent on sponsor financial strength',
            'securities_registration': 'Must purchase through broker-dealer',
            'fees': 'Upfront fees 3-5%, ongoing management fees',
            'future_1031_complexity': 'May own interests in multiple DSTs',
            'irs_ruling_risk': 'IRS could change position (unlikely)',
            'market_risk': '2008 financial crisis caused significant DST losses'
        }

        # Sample allocation if dst_properties provided
        allocation = []
        if dst_properties:
            remaining_equity = equity
            for dst in dst_properties:
                investment_amount = min(dst.get('max_investment', equity), remaining_equity)
                allocation.append({
                    'property_name': dst['name'],
                    'property_type': dst['type'],
                    'location': dst['location'],
                    'investment': investment_amount,
                    'projected_annual_return': dst.get('cash_on_cash', 0.05) * 100,
                    'hold_period': dst.get('hold_period', '5-7 years')
                })
                remaining_equity -= investment_amount
                if remaining_equity <= 0:
                    break

        # 7 Critical Rules from Revenue Ruling 2004-86
        irs_requirements = {
            'rule_1': 'Once the DST is formed, there can be no contributions to the trust',
            'rule_2': 'The trustee cannot renegotiate the terms of existing loans, or borrow new funds',
            'rule_3': 'The trustee cannot reinvest sale proceeds, except for temporary investments',
            'rule_4': 'The trustee cannot enter into new leases or renegotiate existing leases',
            'rule_5': 'All cash must be distributed currently',
            'rule_6': 'Trustee can only make limited capital expenditures',
            'rule_7': 'Any reserves must be established at DST formation'
        }

        return {
            'exchange_requirements': {
                'relinquished_value': relinquished_property_value,
                'equity': equity,
                'debt_on_relinquished': debt_on_relinquished,
                'min_replacement_value': min_replacement_value,
                'min_debt_replacement': min_debt_replacement
            },
            'tax_deferral': {
                'capital_gains_deferred': capital_gain,
                'recapture_deferred': depreciation_recapture,
                'total_tax_deferred': total_tax_deferred,
                'deferred_capital_gains_tax': deferred_capital_gains_tax,
                'deferred_recapture_tax': deferred_recapture_tax
            },
            'dst_benefits': dst_benefits,
            'dst_risks': dst_risks,
            'irs_requirements': irs_requirements,
            'allocation': allocation,
            'recommendation': {
                'suitable_for': [
                    'Investors tired of active management',
                    'Partial 1031 exchange scenarios',
                    'Portfolio diversification across markets',
                    'Estate planning with multiple beneficiaries',
                    'Access to institutional-grade assets'
                ],
                'not_suitable_for': [
                    'Investors wanting control over property decisions',
                    'Those who need liquidity within 5 years',
                    'Investors uncomfortable with sponsor dependency',
                    'Those seeking to avoid securities regulations'
                ]
            }
        }


class CaptiveInsuranceCalculator:
    """
    831(b) Micro-Captive Insurance Calculator

    WARNING: Under intense IRS scrutiny. Final regulations issued January 2025.
    Listed transaction if Loss Ratio < 30% AND meets Financing Factor test.
    """

    @staticmethod
    def calculate_831b_feasibility(
        annual_premium: float,
        operating_company_revenue: float,
        loss_ratio_5yr: float,
        has_financing_arrangement: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate feasibility and risk of 831(b) micro-captive.

        Args:
            annual_premium: Premium paid to captive (max $2.8M for 2024)
            operating_company_revenue: Operating company annual revenue
            loss_ratio_5yr: Claims paid / Premiums received over 5 years
            has_financing_arrangement: Loans/guarantees back to insured?

        Returns:
            Feasibility analysis with IRS risk assessment
        """
        max_premium_2024 = 2_800_000
        max_premium_2025 = 2_900_000  # Estimated with inflation adjustment

        # IRS Listed Transaction Tests
        listed_transaction_risk = False
        risk_factors = []

        # Test 1: Loss Ratio < 30%
        if loss_ratio_5yr < 0.30:
            risk_factors.append(f'Loss Ratio Factor FAILED: {loss_ratio_5yr:.1%} is below 30% threshold')
            listed_transaction_risk = True

        # Test 2: Financing Factor
        if has_financing_arrangement:
            risk_factors.append('Financing Factor FAILED: Captive has loan/guarantee arrangement with insured')
            listed_transaction_risk = True

        # Premium reasonableness test
        reasonable_premium_pct = 0.10  # 10% of revenue is upper reasonable limit
        max_reasonable_premium = operating_company_revenue * reasonable_premium_pct

        if annual_premium > max_reasonable_premium:
            risk_factors.append(
                f'Premium of ${annual_premium:,.0f} exceeds reasonable 10% of revenue '
                f'(${max_reasonable_premium:,.0f}). IRS may challenge as excessive.'
            )

        # Calculate tax benefit
        top_tax_rate = 0.37
        state_tax_rate = 0.05
        effective_rate = top_tax_rate + state_tax_rate

        operating_company_deduction = annual_premium * effective_rate
        captive_income_tax = 0  # 831(b) captive pays no tax on underwriting income

        net_tax_savings = operating_company_deduction - captive_income_tax

        # Calculate investment income taxation
        assumed_investment_return = 0.04
        captive_investment_income = annual_premium * assumed_investment_return
        captive_investment_tax = captive_investment_income * 0.21  # C-corp rate

        # Compliance costs
        annual_compliance_costs = {
            'captive_manager': 15000,
            'actuarial_study': 8000,
            'tax_preparation': 5000,
            'legal_fees': 5000,
            'formation_costs_amortized': 10000 / 5,  # $50k formation over 5 years
            'total': 35000
        }

        # Warnings based on recent IRS actions
        warnings = [
            'IRS issued final regulations January 2025 making some arrangements "listed transactions"',
            'Recent Tax Court cases (Keating, Swift) ruled against captives with poor documentation',
            'Loss ratio must be >30% over 5-year period to avoid listed transaction designation',
            'No loans, guarantees, or financing arrangements back to insured permitted',
            'Must have actual insurance risk transfer and risk distribution',
            'Requires formal underwriting, claims processing, and actuarial analysis',
            'Premium must be reasonable for actual risks insured',
            'Captive must function as real insurance company, not tax shelter'
        ]

        # Risk assessment
        if listed_transaction_risk:
            irs_risk_level = 'EXTREME - Listed Transaction'
            audit_probability = 95
        elif loss_ratio_5yr < 0.40:
            irs_risk_level = 'VERY HIGH'
            audit_probability = 75
        elif annual_premium > max_reasonable_premium:
            irs_risk_level = 'HIGH'
            audit_probability = 60
        else:
            irs_risk_level = 'MODERATE'
            audit_probability = 30

        return {
            'premium_limits': {
                '2024_max': max_premium_2024,
                '2025_max': max_premium_2025,
                'annual_premium': annual_premium,
                'within_limits': annual_premium <= max_premium_2024
            },
            'listed_transaction_analysis': {
                'is_listed_transaction': listed_transaction_risk,
                'loss_ratio_test': 'PASS' if loss_ratio_5yr >= 0.30 else 'FAIL',
                'financing_test': 'PASS' if not has_financing_arrangement else 'FAIL',
                'risk_factors': risk_factors
            },
            'tax_benefit': {
                'operating_company_deduction': operating_company_deduction,
                'captive_income_tax': captive_income_tax,
                'net_tax_savings': net_tax_savings,
                'captive_investment_income': captive_investment_income,
                'captive_investment_tax': captive_investment_tax,
                'net_annual_benefit': net_tax_savings - annual_compliance_costs['total'] - captive_investment_tax
            },
            'compliance_costs': annual_compliance_costs,
            'irs_risk': {
                'risk_level': irs_risk_level,
                'audit_probability': audit_probability,
                'recent_enforcement': 'IRS has won multiple Tax Court cases in 2024',
                'priority_guidance': 'Included in IRS 2024-2025 Priority Guidance Plan'
            },
            'warnings': warnings,
            'recommendation': {
                'proceed': not listed_transaction_risk and loss_ratio_5yr >= 0.40,
                'reason': 'Listed transaction designation REQUIRES Form 8886 reporting' if listed_transaction_risk
                         else 'Loss ratio too low, IRS audit risk very high' if loss_ratio_5yr < 0.40
                         else 'May be viable if properly structured with legitimate insurance purpose',
                'alternatives': [
                    'Increase claims paid to improve loss ratio above 40%',
                    'Use commercial insurance instead',
                    'Consider group captive or rent-a-captive',
                    'Explore other tax planning strategies with lower IRS risk'
                ]
            }
        }


class CRTCalculator:
    """
    Charitable Remainder Trust (CRT) / Charitable Remainder Unitrust (CRUT) Calculator

    Allows tax-free sale of appreciated assets while generating income and charitable deduction.
    """

    @staticmethod
    def calculate_crt_benefits(
        asset_value: float,
        cost_basis: float,
        annual_payout_rate: float,
        term_years: int,
        beneficiary_age: int,
        is_unitrust: bool = True,
        section_7520_rate: float = 0.054
    ) -> Dict[str, Any]:
        """
        Calculate Charitable Remainder Trust benefits.

        Args:
            asset_value: Current FMV of asset to donate
            cost_basis: Original cost basis
            annual_payout_rate: Payout rate (5%-50%, typically 5-6%)
            term_years: Term in years (max 20) or 0 for life
            beneficiary_age: Age of income beneficiary
            is_unitrust: True for CRUT, False for CRAT
            section_7520_rate: IRS Section 7520 rate (changes monthly)

        Returns:
            CRT benefit analysis
        """
        capital_gain = asset_value - cost_basis
        capital_gains_rate = 0.20 if asset_value > 500_000 else 0.15
        net_investment_income_tax = 0.038  # 3.8% NIIT for high earners
        total_cg_rate = capital_gains_rate + net_investment_income_tax

        # Tax if sold directly
        tax_on_direct_sale = capital_gain * total_cg_rate
        proceeds_after_tax = asset_value - tax_on_direct_sale

        # CRT structure - no tax on sale inside trust
        crt_asset_value = asset_value  # No tax paid

        # Annual income calculation
        if is_unitrust:
            # CRUT: revalues annually
            year_1_income = crt_asset_value * annual_payout_rate
            trust_type = 'CRUT (Charitable Remainder Unitrust)'
            income_note = 'Revalued annually based on trust assets'
        else:
            # CRAT: fixed payment
            year_1_income = crt_asset_value * annual_payout_rate
            trust_type = 'CRAT (Charitable Remainder Annuity Trust)'
            income_note = 'Fixed dollar amount each year'

        # Estimate charitable deduction (simplified)
        # Actual calculation requires present value of remainder interest
        life_expectancy = 85 - beneficiary_age if term_years == 0 else term_years
        total_expected_payouts = year_1_income * life_expectancy
        estimated_remainder = max(0, asset_value - total_expected_payouts)

        # Charitable deduction is present value of remainder
        discount_factor = (1 + section_7520_rate) ** life_expectancy
        charitable_deduction = estimated_remainder / discount_factor

        # AGI limitation
        agi_limit_pct = 0.60 if is_unitrust else 0.30
        max_deduction_year_1 = charitable_deduction  # Simplified

        tax_savings_from_deduction = charitable_deduction * 0.37  # Top bracket

        # Total benefit comparison
        crt_total_benefit = (
            (year_1_income * life_expectancy) +  # Total income received
            tax_savings_from_deduction +  # Upfront deduction
            (tax_on_direct_sale)  # Capital gains tax avoided
        )

        direct_sale_benefit = (
            proceeds_after_tax * 0.04 * life_expectancy  # Investment income at 4%
        )

        return {
            'trust_structure': {
                'type': trust_type,
                'payout_rate': annual_payout_rate * 100,
                'term': f'{life_expectancy} years ({"lifetime" if term_years == 0 else "fixed term"})',
                'minimum_payout': '5%',
                'maximum_payout': '50%',
                'revaluation': 'Annual' if is_unitrust else 'None'
            },
            'asset_details': {
                'current_value': asset_value,
                'cost_basis': cost_basis,
                'capital_gain': capital_gain,
                'appreciation': (capital_gain / cost_basis) * 100 if cost_basis > 0 else 0
            },
            'direct_sale_comparison': {
                'asset_value': asset_value,
                'capital_gains_tax': tax_on_direct_sale,
                'niit_tax': capital_gain * net_investment_income_tax,
                'proceeds_after_tax': proceeds_after_tax,
                'investment_income_generated': proceeds_after_tax * 0.04 * life_expectancy
            },
            'crt_benefits': {
                'asset_value_in_trust': crt_asset_value,
                'capital_gains_tax_avoided': tax_on_direct_sale,
                'annual_income': year_1_income,
                'income_note': income_note,
                'total_income_expected': year_1_income * life_expectancy,
                'charitable_deduction': charitable_deduction,
                'tax_savings_from_deduction': tax_savings_from_deduction,
                'agi_limit': f'{agi_limit_pct * 100}% (carryforward 5 years)',
                'estate_reduction': asset_value,
                'total_crt_benefit': crt_total_benefit
            },
            'advantage_crt_vs_direct_sale': crt_total_benefit - direct_sale_benefit,
            'best_use_cases': [
                'Highly appreciated stock or real estate (low basis)',
                'Want income stream for retirement',
                'Charitably inclined',
                'Want to diversify concentrated position tax-free',
                'High income earner needing deduction',
                'Estate planning to reduce taxable estate'
            ],
            'requirements': {
                'minimum_funding': 'Typically $100,000+',
                'annual_admin_costs': '$2,000 - $5,000',
                'trustee_required': 'Yes (bank or trust company)',
                'irrevocable': 'Yes - cannot change once established',
                'qualified_charity': 'Must name 501(c)(3) as remainder beneficiary'
            },
            'taxation_of_distributions': {
                'tier_1': 'Ordinary income (interest, rent, non-qualified dividends)',
                'tier_2': 'Capital gains (short-term, then long-term)',
                'tier_3': 'Other income',
                'tier_4': 'Return of principal (tax-free)',
                'note': 'Distributions taxed based on trust accounting income'
            },
            'section_7520_rate': {
                'current_rate': section_7520_rate * 100,
                'impact': 'Higher rates = larger charitable deduction',
                'note': 'Rate changes monthly, locked in at creation'
            }
        }


class OilGasInvestmentCalculator:
    """
    Oil & Gas Investment Tax Benefits Calculator

    Intangible Drilling Costs (IDCs) provide significant first-year deductions.
    """

    @staticmethod
    def calculate_oil_gas_benefits(
        investment_amount: float,
        idc_percentage: float = 0.75,
        tangible_percentage: float = 0.15,
        working_interest: bool = True,
        income_phase: float = 0.85
    ) -> Dict[str, Any]:
        """
        Calculate oil & gas investment tax benefits.

        Args:
            investment_amount: Total investment in drilling project
            idc_percentage: Percentage classified as IDC (typically 70-85%)
            tangible_percentage: Percentage for tangible equipment (15-25%)
            working_interest: True for working interest (deductible), False for royalty
            income_phase: Production income multiplier (85% typical after costs)

        Returns:
            Oil & gas investment analysis
        """
        # Cost allocation
        idc_costs = investment_amount * idc_percentage
        tangible_costs = investment_amount * tangible_percentage
        lease_costs = investment_amount * (1 - idc_percentage - tangible_percentage)

        # Year 1 deductions
        if working_interest:
            year_1_idc_deduction = idc_costs * 1.00  # 100% deductible Year 1
            year_1_tangible_deduction = tangible_costs * 0.20  # 7-year MACRS
            year_1_lease_deduction = lease_costs * 0.03  # Amortized
        else:
            # Royalty interest - passive income limitations apply
            year_1_idc_deduction = idc_costs * 0.30  # Limited
            year_1_tangible_deduction = tangible_costs * 0.20
            year_1_lease_deduction = lease_costs * 0.03

        total_year_1_deduction = year_1_idc_deduction + year_1_tangible_deduction + year_1_lease_deduction

        # Tax savings
        top_tax_rate = 0.37
        state_tax_rate = 0.05
        tax_savings_year_1 = total_year_1_deduction * (top_tax_rate + state_tax_rate)

        # Depletion allowance (when productive)
        assumed_annual_revenue = investment_amount * 0.15  # 15% annual return
        gross_income_depletion = assumed_annual_revenue * 0.15  # 15% of gross
        cost_depletion = idc_costs / 10  # Assume 10-year life
        depletion_deduction = max(gross_income_depletion, cost_depletion)

        # Net economic benefit
        net_investment_after_tax_savings = investment_amount - tax_savings_year_1

        return {
            'investment_structure': {
                'total_investment': investment_amount,
                'interest_type': 'Working Interest (Active)' if working_interest else 'Royalty Interest (Passive)',
                'idc_costs': idc_costs,
                'tangible_costs': tangible_costs,
                'lease_costs': lease_costs
            },
            'year_1_deductions': {
                'idc_deduction': year_1_idc_deduction,
                'tangible_deduction': year_1_tangible_deduction,
                'lease_deduction': year_1_lease_deduction,
                'total_year_1_deduction': total_year_1_deduction,
                'deduction_percentage': (total_year_1_deduction / investment_amount) * 100
            },
            'tax_savings': {
                'year_1_tax_savings': tax_savings_year_1,
                'federal_savings': total_year_1_deduction * top_tax_rate,
                'state_savings': total_year_1_deduction * state_tax_rate,
                'effective_net_cost': net_investment_after_tax_savings,
                'roi_needed': (net_investment_after_tax_savings / investment_amount) * 100
            },
            'depletion_allowance': {
                'annual_revenue_assumed': assumed_annual_revenue,
                'percentage_depletion_15_pct': gross_income_depletion,
                'cost_depletion': cost_depletion,
                'depletion_deduction': depletion_deduction,
                'annual_tax_savings_from_depletion': depletion_deduction * (top_tax_rate + state_tax_rate)
            },
            'benefits': [
                f'Deduct up to {(total_year_1_deduction / investment_amount) * 100:.0f}% of investment in Year 1',
                'Percentage depletion allows deductions >100% of investment over time',
                'Working interest losses offset W-2 income (not passive)',
                'Exempt from Alternative Minimum Tax (AMT)',
                'Can offset up to $500K income ($1M married) even with passive loss rules'
            ],
            'risks': [
                'Dry hole risk - may produce no revenue',
                'Commodity price volatility',
                'Regulatory and environmental risks',
                'Typically illiquid investment',
                'High upfront costs',
                'Geological uncertainty'
            ],
            'irs_requirements': {
                'working_interest': 'Must be actual working interest, not limited partnership',
                'at_risk_rules': 'Must have capital at risk',
                'material_participation': 'Not required for working interest deduction',
                'form_6198': 'At-Risk Limitations must be filed',
                'idc_election': 'Make IDC election on first return'
            },
            'alternative_minimum_tax': {
                'amt_preference_item': 'NO - Oil & gas working interest exempt from AMT',
                'advantage': 'Unlike other tax shelters, IDCs not added back for AMT'
            },
            'recommendation': {
                'best_for': [
                    'High income earners (37% bracket)',
                    'Accredited investors ($200K+ income or $1M+ net worth)',
                    'Those seeking active income offsets',
                    'Diversification into commodities',
                    'Long-term hold horizon (7-15 years)'
                ],
                'not_suitable_for': [
                    'Risk-averse investors',
                    'Those needing liquidity',
                    'Passive investors (unless can demonstrate participation)',
                    'Small investment amounts (<$25K)'
                ]
            }
        }
