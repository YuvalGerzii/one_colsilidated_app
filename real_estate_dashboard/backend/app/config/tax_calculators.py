"""
Advanced Tax Calculators and Financial Planning Tools

Interactive calculators for tax planning, entity structure optimization,
and financial decision-making.
"""

from typing import Dict, List, Any, Optional
from decimal import Decimal
from datetime import datetime


# ============================================================================
# DEPRECIATION CALCULATORS
# ============================================================================

class DepreciationCalculator:
    """Calculate depreciation using various methods"""

    @staticmethod
    def macrs_gds_residential(cost: Decimal, year: int) -> Decimal:
        """
        Calculate MACRS GDS depreciation for residential rental property (27.5 years)

        Args:
            cost: Depreciable basis (building cost excluding land)
            year: Year of depreciation (1-28)

        Returns:
            Depreciation amount for the year
        """
        if year < 1 or year > 28:
            return Decimal('0')

        # Mid-month convention percentages for 27.5-year property
        percentages = {
            1: Decimal('3.485'),  # First year (mid-month convention)
            2: Decimal('3.636'),
        }

        # Years 2-27 are full years
        for y in range(2, 28):
            percentages[y] = Decimal('3.636')

        percentages[28] = Decimal('1.970')  # Last year

        return cost * percentages.get(year, Decimal('0')) / Decimal('100')

    @staticmethod
    def macrs_gds_commercial(cost: Decimal, year: int) -> Decimal:
        """
        Calculate MACRS GDS depreciation for commercial property (39 years)
        """
        if year < 1 or year > 40:
            return Decimal('0')

        # Mid-month convention percentages for 39-year property
        if year == 1:
            return cost * Decimal('2.461') / Decimal('100')
        elif year <= 39:
            return cost * Decimal('2.564') / Decimal('100')
        else:  # year 40
            return cost * Decimal('0.107') / Decimal('100')

    @staticmethod
    def cost_segregation_analysis(
        building_cost: Decimal,
        land_cost: Decimal,
        property_type: str = 'commercial'
    ) -> Dict[str, Any]:
        """
        Estimate cost segregation potential

        Args:
            building_cost: Total building cost
            land_cost: Land value (non-depreciable)
            property_type: 'residential' or 'commercial'

        Returns:
            Dictionary with segregated components and depreciation
        """
        total_cost = building_cost + land_cost

        # Typical cost segregation percentages
        segregation = {
            '5_year': {
                'percentage': Decimal('15'),  # Carpet, appliances, decorative items
                'description': 'Personal property (5-year)',
                'items': ['Carpet', 'Appliances', 'Decorative lighting', 'Window treatments']
            },
            '7_year': {
                'percentage': Decimal('5'),  # Office furniture, equipment
                'description': 'Equipment and fixtures (7-year)',
                'items': ['Furniture', 'Office equipment', 'Some fixtures']
            },
            '15_year': {
                'percentage': Decimal('15'),  # Land improvements
                'description': 'Land improvements (15-year)',
                'items': ['Parking lot', 'Sidewalks', 'Landscaping', 'Fencing', 'Exterior lighting']
            },
            'building': {
                'percentage': Decimal('65'),  # Remaining building
                'description': '27.5-year or 39-year building',
                'items': ['Structure', 'HVAC', 'Plumbing', 'Electrical']
            }
        }

        # Calculate allocated costs
        results = {}
        for category, data in segregation.items():
            allocated_cost = building_cost * data['percentage'] / Decimal('100')

            # Calculate first-year depreciation
            if category == '5_year':
                # 20% bonus depreciation (if applicable) or 20% regular
                first_year_depr = allocated_cost * Decimal('20') / Decimal('100')
            elif category == '7_year':
                first_year_depr = allocated_cost * Decimal('14.29') / Decimal('100')
            elif category == '15_year':
                first_year_depr = allocated_cost * Decimal('5') / Decimal('100')
            else:  # building
                if property_type == 'residential':
                    first_year_depr = allocated_cost * Decimal('3.485') / Decimal('100')
                else:
                    first_year_depr = allocated_cost * Decimal('2.461') / Decimal('100')

            results[category] = {
                'allocated_cost': allocated_cost,
                'percentage': data['percentage'],
                'description': data['description'],
                'items': data['items'],
                'first_year_depreciation': first_year_depr
            }

        # Calculate totals
        total_first_year_without_seg = building_cost * (
            Decimal('3.485') if property_type == 'residential' else Decimal('2.461')
        ) / Decimal('100')

        total_first_year_with_seg = sum(
            r['first_year_depreciation'] for r in results.values()
        )

        return {
            'total_cost': total_cost,
            'building_cost': building_cost,
            'land_cost': land_cost,
            'segregated_components': results,
            'first_year_depreciation_without_segregation': total_first_year_without_seg,
            'first_year_depreciation_with_segregation': total_first_year_with_seg,
            'additional_first_year_deduction': total_first_year_with_seg - total_first_year_without_seg,
            'estimated_study_cost': Decimal('7500'),  # Typical cost
            'estimated_roi': (total_first_year_with_seg - total_first_year_without_seg) / Decimal('7500')
        }


# ============================================================================
# ENTITY STRUCTURE CALCULATOR
# ============================================================================

class EntityStructureCalculator:
    """Compare tax implications of different business structures"""

    @staticmethod
    def compare_structures(
        net_income: Decimal,
        reasonable_salary: Optional[Decimal] = None,
        state_tax_rate: Decimal = Decimal('5'),
        filing_status: str = 'married'
    ) -> Dict[str, Any]:
        """
        Compare LLC (default taxation), S-Corp, and C-Corp

        Args:
            net_income: Annual net business income
            reasonable_salary: Salary for S-Corp (default 40% of net income)
            state_tax_rate: State income tax rate percentage
            filing_status: 'single' or 'married'

        Returns:
            Comparison of tax obligations under each structure
        """
        if reasonable_salary is None:
            reasonable_salary = net_income * Decimal('0.4')

        # Tax rates (2024)
        se_tax_rate = Decimal('15.3')  # Self-employment tax
        medicare_surtax_threshold = Decimal('250000') if filing_status == 'married' else Decimal('200000')

        # LLC (default - taxed as sole proprietorship or partnership)
        llc_se_tax = min(net_income, Decimal('160200')) * se_tax_rate / Decimal('100')
        if net_income > Decimal('160200'):
            # Only Medicare portion (2.9%) applies above Social Security wage base
            llc_se_tax += (net_income - Decimal('160200')) * Decimal('2.9') / Decimal('100')

        # Additional Medicare tax if above threshold
        if net_income > medicare_surtax_threshold:
            llc_se_tax += (net_income - medicare_surtax_threshold) * Decimal('0.9') / Decimal('100')

        # Deduct 50% of SE tax for income tax calculation
        llc_adjusted_income = net_income - (llc_se_tax / Decimal('2'))

        # QBI deduction (20% of qualified business income)
        llc_qbi_deduction = min(llc_adjusted_income * Decimal('0.2'), llc_adjusted_income)
        llc_taxable_income = llc_adjusted_income - llc_qbi_deduction

        # Estimate federal income tax (simplified marginal rates)
        llc_fed_tax = EntityStructureCalculator._calculate_income_tax(llc_taxable_income, filing_status)
        llc_state_tax = llc_taxable_income * state_tax_rate / Decimal('100')
        llc_total_tax = llc_se_tax + llc_fed_tax + llc_state_tax

        # S-CORP
        distribution = net_income - reasonable_salary

        # Payroll taxes on salary only
        scorp_fica = reasonable_salary * se_tax_rate / Decimal('100')

        # Income tax on all income (salary + distribution)
        scorp_qbi_deduction = distribution * Decimal('0.2')  # QBI only on distributions
        scorp_taxable_income = net_income - scorp_qbi_deduction
        scorp_fed_tax = EntityStructureCalculator._calculate_income_tax(scorp_taxable_income, filing_status)
        scorp_state_tax = scorp_taxable_income * state_tax_rate / Decimal('100')
        scorp_total_tax = scorp_fica + scorp_fed_tax + scorp_state_tax

        # Savings vs LLC
        scorp_savings = llc_total_tax - scorp_total_tax

        # C-CORP (for comparison)
        ccorp_tax_rate = Decimal('21')  # Flat federal corporate rate
        ccorp_corporate_tax = net_income * ccorp_tax_rate / Decimal('100')

        # If taking salary
        ccorp_salary_fica = reasonable_salary * se_tax_rate / Decimal('100')
        ccorp_personal_income_tax = EntityStructureCalculator._calculate_income_tax(reasonable_salary, filing_status)

        # Remaining profit stays in corporation (no immediate personal tax)
        ccorp_retained_earnings = net_income - reasonable_salary - ccorp_corporate_tax

        ccorp_total_tax = ccorp_corporate_tax + ccorp_salary_fica + ccorp_personal_income_tax

        return {
            'llc': {
                'structure': 'LLC (Default Taxation)',
                'self_employment_tax': llc_se_tax,
                'federal_income_tax': llc_fed_tax,
                'state_income_tax': llc_state_tax,
                'qbi_deduction': llc_qbi_deduction,
                'total_tax': llc_total_tax,
                'effective_rate': (llc_total_tax / net_income * Decimal('100')),
                'net_after_tax': net_income - llc_total_tax,
                'pros': [
                    'Simple administration',
                    'No payroll requirements',
                    'Full QBI deduction available',
                    'Pass-through taxation'
                ],
                'cons': [
                    'Full self-employment tax on all income',
                    'Higher total tax if income over $60K',
                    'No salary/distribution split'
                ]
            },
            's_corp': {
                'structure': 'S-Corporation',
                'salary': reasonable_salary,
                'distribution': distribution,
                'payroll_tax': scorp_fica,
                'federal_income_tax': scorp_fed_tax,
                'state_income_tax': scorp_state_tax,
                'qbi_deduction': scorp_qbi_deduction,
                'total_tax': scorp_total_tax,
                'effective_rate': (scorp_total_tax / net_income * Decimal('100')),
                'net_after_tax': net_income - scorp_total_tax,
                'savings_vs_llc': scorp_savings,
                'annual_compliance_cost': Decimal('2000'),  # Payroll + accounting
                'net_benefit': scorp_savings - Decimal('2000'),
                'pros': [
                    f'Save ${scorp_savings:,.2f} vs LLC',
                    'Avoid SE tax on distributions',
                    'Still get QBI deduction',
                    'Pass-through taxation'
                ],
                'cons': [
                    'Payroll compliance required',
                    'Must pay reasonable salary',
                    'Higher accounting costs',
                    'More IRS scrutiny on salary'
                ]
            },
            'c_corp': {
                'structure': 'C-Corporation',
                'corporate_tax': ccorp_corporate_tax,
                'salary_payroll_tax': ccorp_salary_fica,
                'personal_income_tax': ccorp_personal_income_tax,
                'total_current_tax': ccorp_total_tax,
                'retained_earnings': ccorp_retained_earnings,
                'effective_rate': (ccorp_total_tax / net_income * Decimal('100')),
                'pros': [
                    'Flat 21% corporate rate',
                    'Can retain earnings in business',
                    'More deductible fringe benefits',
                    'Easier to raise capital'
                ],
                'cons': [
                    'Double taxation on distributions',
                    'No QBI deduction',
                    'More complex compliance',
                    'Dividends taxed at 15-20%'
                ],
                'note': 'Tax shown is current year only. Distributions will trigger additional personal tax.'
            },
            'recommendation': EntityStructureCalculator._get_recommendation(
                net_income, scorp_savings, filing_status
            )
        }

    @staticmethod
    def _calculate_income_tax(taxable_income: Decimal, filing_status: str) -> Decimal:
        """Simplified federal income tax calculation using 2024 brackets"""
        if filing_status == 'married':
            brackets = [
                (Decimal('22000'), Decimal('10')),
                (Decimal('89075'), Decimal('12')),
                (Decimal('190750'), Decimal('22')),
                (Decimal('364200'), Decimal('24')),
                (Decimal('462500'), Decimal('32')),
                (Decimal('693750'), Decimal('35')),
                (Decimal('999999999'), Decimal('37'))
            ]
        else:  # single
            brackets = [
                (Decimal('11000'), Decimal('10')),
                (Decimal('44725'), Decimal('12')),
                (Decimal('95375'), Decimal('22')),
                (Decimal('182100'), Decimal('24')),
                (Decimal('231250'), Decimal('32')),
                (Decimal('578125'), Decimal('35')),
                (Decimal('999999999'), Decimal('37'))
            ]

        tax = Decimal('0')
        remaining = taxable_income
        prev_limit = Decimal('0')

        for limit, rate in brackets:
            if remaining <= 0:
                break

            taxable_in_bracket = min(remaining, limit - prev_limit)
            tax += taxable_in_bracket * rate / Decimal('100')
            remaining -= taxable_in_bracket
            prev_limit = limit

        return tax

    @staticmethod
    def _get_recommendation(net_income: Decimal, scorp_savings: Decimal, filing_status: str) -> str:
        """Provide recommendation based on analysis"""
        if net_income < Decimal('60000'):
            return "LLC recommended - S-Corp savings don't justify compliance costs at this income level"
        elif scorp_savings > Decimal('3000'):
            return f"S-Corp recommended - Save ${scorp_savings:,.2f} annually vs LLC"
        else:
            return "LLC or S-Corp both viable - choose based on administrative preference"


# ============================================================================
# ALTERNATIVE MINIMUM TAX (AMT) CALCULATOR
# ============================================================================

class AMTCalculator:
    """Calculate Alternative Minimum Tax exposure"""

    @staticmethod
    def calculate_amt(
        regular_taxable_income: Decimal,
        adjustments: Dict[str, Decimal],
        filing_status: str = 'married'
    ) -> Dict[str, Any]:
        """
        Calculate AMT and compare to regular tax

        Args:
            regular_taxable_income: Income under regular tax system
            adjustments: Dictionary of AMT adjustments/preferences
            filing_status: 'single', 'married', or 'head_of_household'

        Returns:
            AMT calculation and comparison
        """
        # AMT exemptions (2024)
        exemptions = {
            'single': Decimal('81300'),
            'married': Decimal('126500'),
            'head_of_household': Decimal('81300')
        }

        exemption_phaseout_thresholds = {
            'single': Decimal('578150'),
            'married': Decimal('1156300'),
            'head_of_household': Decimal('578150')
        }

        # Calculate AMT income (AMTI)
        amti = regular_taxable_income

        # Add back common AMT adjustments
        for item, amount in adjustments.items():
            amti += amount

        # Calculate exemption (phases out at 25 cents per dollar over threshold)
        exemption = exemptions[filing_status]
        threshold = exemption_phaseout_thresholds[filing_status]

        if amti > threshold:
            phaseout = (amti - threshold) * Decimal('0.25')
            exemption = max(Decimal('0'), exemption - phaseout)

        # Calculate AMT base
        amt_base = max(Decimal('0'), amti - exemption)

        # AMT rates: 26% up to threshold, 28% above
        amt_threshold = Decimal('220700') if filing_status == 'married' else Decimal('110350')

        if amt_base <= amt_threshold:
            tentative_amt = amt_base * Decimal('0.26')
        else:
            tentative_amt = (amt_threshold * Decimal('0.26') +
                           (amt_base - amt_threshold) * Decimal('0.28'))

        return {
            'amti': amti,
            'exemption': exemption,
            'amt_base': amt_base,
            'tentative_amt': tentative_amt,
            'adjustments_total': sum(adjustments.values()),
            'adjustment_details': adjustments,
            'subject_to_amt': tentative_amt > Decimal('0'),
            'exemption_phased_out': exemptions[filing_status] != exemption
        }


# ============================================================================
# RETIREMENT CONTRIBUTION OPTIMIZER
# ============================================================================

class RetirementOptimizer:
    """Optimize retirement contributions across all available vehicles"""

    @staticmethod
    def maximize_contributions(
        age: int,
        w2_income: Decimal,
        self_employment_income: Decimal,
        spouse_income: Decimal = Decimal('0'),
        has_hdhp: bool = False
    ) -> Dict[str, Any]:
        """
        Calculate maximum retirement contributions across all vehicles

        Args:
            age: Age of taxpayer
            w2_income: W-2 wage income
            self_employment_income: Self-employment income
            spouse_income: Spouse's income
            has_hdhp: Whether covered by High Deductible Health Plan

        Returns:
            Maximum contribution amounts and tax savings
        """
        is_50_plus = age >= 50

        contributions = {}

        # 401(k) / 403(b) - Employee deferrals
        if w2_income > 0:
            employee_limit = Decimal('23000') if not is_50_plus else Decimal('30500')
            contributions['401k_employee'] = {
                'limit': employee_limit,
                'description': '401(k) employee deferrals',
                'tax_treatment': 'Pre-tax (traditional) or after-tax (Roth)'
            }

            # Employer match (assumed 50% up to 6% of salary)
            employer_match = min(w2_income * Decimal('0.06') * Decimal('0.5'), Decimal('20000'))
            contributions['401k_employer'] = {
                'limit': employer_match,
                'description': '401(k) employer match (estimated)',
                'tax_treatment': 'Pre-tax'
            }

        # Solo 401(k) or SEP IRA for self-employed
        if self_employment_income > 0:
            # Employee deferral
            employee_limit = Decimal('23000') if not is_50_plus else Decimal('30500')

            # Employer contribution (25% of compensation)
            # Compensation = SE income - 50% SE tax
            se_tax = self_employment_income * Decimal('0.9235') * Decimal('0.153')
            net_se_income = self_employment_income - se_tax
            employer_limit = net_se_income * Decimal('0.25')

            # Total cannot exceed $69,000 ($76,500 if 50+)
            total_limit = Decimal('69000') if not is_50_plus else Decimal('76500')
            total_solo_401k = min(employee_limit + employer_limit, total_limit)

            contributions['solo_401k'] = {
                'employee_portion': min(employee_limit, total_solo_401k),
                'employer_portion': min(employer_limit, total_solo_401k - employee_limit),
                'total': total_solo_401k,
                'description': 'Solo 401(k) for self-employed',
                'tax_treatment': 'Pre-tax'
            }

        # Traditional or Roth IRA
        ira_limit = Decimal('7000') if not is_50_plus else Decimal('8000')
        contributions['ira'] = {
            'limit': ira_limit,
            'description': 'Traditional or Roth IRA',
            'tax_treatment': 'Pre-tax (Traditional) or after-tax (Roth)',
            'note': 'Deductibility phases out at higher incomes'
        }

        # Spouse IRA (if applicable)
        if spouse_income > 0 or (w2_income + self_employment_income) > ira_limit:
            contributions['spouse_ira'] = {
                'limit': ira_limit,
                'description': 'Spouse IRA (Traditional or Roth)',
                'tax_treatment': 'Pre-tax (Traditional) or after-tax (Roth)'
            }

        # HSA (if eligible)
        if has_hdhp:
            hsa_limit = Decimal('4150')  # Family coverage
            if age >= 55:
                hsa_limit += Decimal('1000')  # Catch-up

            contributions['hsa'] = {
                'limit': hsa_limit,
                'description': 'Health Savings Account (Triple tax advantage)',
                'tax_treatment': 'Pre-tax contribution, tax-free growth, tax-free withdrawals for medical',
                'note': 'Can invest and grow for retirement'
            }

        # Calculate totals
        total_contributions = Decimal('0')
        total_tax_savings = Decimal('0')

        marginal_rate = Decimal('24')  # Assumed marginal tax rate

        for key, data in contributions.items():
            if 'total' in data:
                amount = data['total']
            elif 'limit' in data:
                amount = data['limit']
            else:
                continue

            total_contributions += amount

            # Most contributions are pre-tax
            if 'after-tax' not in data.get('tax_treatment', ''):
                total_tax_savings += amount * marginal_rate / Decimal('100')

        return {
            'contributions': contributions,
            'total_max_contributions': total_contributions,
            'estimated_tax_savings': total_tax_savings,
            'effective_cost': total_contributions - total_tax_savings,
            'age': age,
            'is_50_plus': is_50_plus,
            'recommendations': RetirementOptimizer._get_recommendations(
                age, w2_income, self_employment_income, has_hdhp
            )
        }

    @staticmethod
    def _get_recommendations(
        age: int,
        w2_income: Decimal,
        self_employment_income: Decimal,
        has_hdhp: bool
    ) -> List[str]:
        """Generate personalized recommendations"""
        recs = []

        if age >= 50:
            recs.append("✅ Maximize catch-up contributions - you're 50+")

        if self_employment_income > Decimal('100000'):
            recs.append("💡 Consider Defined Benefit Pension for larger contributions")

        if not has_hdhp:
            recs.append("💡 Consider High Deductible Health Plan to qualify for HSA")

        if w2_income > Decimal('100000'):
            recs.append("✅ Max out 401(k) before contributing to IRA")

        if age < 40:
            recs.append("💡 Consider Roth IRA/401(k) - tax-free growth for decades")

        recs.append("📅 Make contributions by December 31 for 401(k), April 15 for IRA/HSA")

        return recs


def get_calculator(calculator_type: str):
    """Factory function to get calculator instance"""
    calculators = {
        'depreciation': DepreciationCalculator,
        'entity_structure': EntityStructureCalculator,
        'amt': AMTCalculator,
        'retirement': RetirementOptimizer
    }
    return calculators.get(calculator_type)


__all__ = [
    'DepreciationCalculator',
    'EntityStructureCalculator',
    'AMTCalculator',
    'RetirementOptimizer',
    'get_calculator'
]
