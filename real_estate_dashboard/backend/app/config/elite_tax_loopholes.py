"""
Elite Tax Loopholes and Work-Arounds

This module contains lesser-known but 100% legal tax strategies that sophisticated
tax planners use. These are the "secrets" that wealthy individuals and businesses
leverage to minimize tax liability within IRS regulations.

WARNING: These strategies require meticulous documentation and professional implementation.
"""

from typing import Dict, List, Any, Optional
from decimal import Decimal
from datetime import datetime, date


class QSBSCalculator:
    """
    Qualified Small Business Stock (Section 1202) - 0% Capital Gains

    One of the most powerful tax benefits: 100% exclusion of capital gains up to
    $10M or 10x basis, whichever is greater.
    """

    @staticmethod
    def calculate_qsbs_benefit(
        acquisition_date: str,
        sale_date: str,
        sale_price: float,
        cost_basis: float,
        company_assets_at_issuance: float,
        is_qualified_business: bool = True,
        acquired_at_original_issue: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate QSBS Section 1202 tax exclusion benefits.

        Args:
            acquisition_date: Date stock acquired (YYYY-MM-DD)
            sale_date: Date stock sold (YYYY-MM-DD)
            sale_price: Sale price of stock
            cost_basis: Original purchase price
            company_assets_at_issuance: Company gross assets when stock issued
            is_qualified_business: Not in excluded industries?
            acquired_at_original_issue: Acquired directly from company?

        Returns:
            QSBS analysis with tax savings
        """
        acq_date = datetime.strptime(acquisition_date, '%Y-%m-%d')
        sale_dt = datetime.strptime(sale_date, '%Y-%m-%d')

        # Calculate holding period
        holding_days = (sale_dt - acq_date).days
        holding_years = holding_days / 365.25

        # Determine exclusion percentage based on acquisition date
        if acq_date >= datetime(2010, 9, 28):
            exclusion_pct = 1.00  # 100% exclusion
        elif acq_date >= datetime(2009, 2, 18):
            exclusion_pct = 0.75  # 75% exclusion
        else:
            exclusion_pct = 0.50  # 50% exclusion

        # Calculate capital gain
        capital_gain = sale_price - cost_basis

        # Determine exclusion cap
        # Greater of $10M or 10x basis
        exclusion_cap_10m = 10_000_000
        exclusion_cap_10x = cost_basis * 10
        exclusion_cap = max(exclusion_cap_10m, exclusion_cap_10x)

        # Check all requirements
        qualifications = {
            'holding_period_5_years': holding_years > 5,
            'c_corporation': True,  # Assumed
            'gross_assets_under_50m': company_assets_at_issuance <= 50_000_000,
            'acquired_at_original_issue': acquired_at_original_issue,
            'active_business_80_pct': True,  # Assumed if is_qualified_business
            'not_excluded_industry': is_qualified_business,
            'us_corporation': True  # Assumed
        }

        all_requirements_met = all(qualifications.values())

        # Calculate tax savings
        if all_requirements_met and holding_years > 5:
            excluded_gain = min(capital_gain * exclusion_pct, exclusion_cap)
            taxable_gain = max(0, capital_gain - excluded_gain)

            # Normal capital gains tax (20% + 3.8% NIIT)
            normal_cap_gains_rate = 0.238
            normal_tax = capital_gain * normal_cap_gains_rate

            # QSBS tax (on remaining taxable gain only)
            qsbs_tax = taxable_gain * normal_cap_gains_rate

            tax_savings = normal_tax - qsbs_tax
        else:
            excluded_gain = 0
            taxable_gain = capital_gain
            normal_tax = capital_gain * 0.238
            qsbs_tax = normal_tax
            tax_savings = 0

        # Section 1045 rollover option (if held 6+ months but <5 years)
        section_1045_eligible = (holding_years >= 0.5 and holding_years < 5)

        excluded_industries = [
            'Health services',
            'Law',
            'Engineering',
            'Architecture',
            'Accounting',
            'Actuarial science',
            'Performing arts',
            'Consulting',
            'Athletics',
            'Financial services',
            'Brokerage services',
            'Banking',
            'Insurance',
            'Leasing',
            'Farming',
            'Hotels/Restaurants',
            'Mining'
        ]

        return {
            'qualified_for_qsbs': all_requirements_met and holding_years > 5,
            'holding_period': {
                'days': holding_days,
                'years': round(holding_years, 2),
                'meets_5_year_requirement': holding_years > 5
            },
            'exclusion_details': {
                'exclusion_percentage': exclusion_pct * 100,
                'exclusion_cap': exclusion_cap,
                'capital_gain': capital_gain,
                'excluded_gain': excluded_gain,
                'taxable_gain': taxable_gain
            },
            'tax_comparison': {
                'normal_capital_gains_tax': normal_tax,
                'qsbs_tax': qsbs_tax,
                'tax_savings': tax_savings,
                'effective_rate_without_qsbs': 23.8,
                'effective_rate_with_qsbs': (qsbs_tax / capital_gain * 100) if capital_gain > 0 else 0
            },
            'requirements': qualifications,
            'section_1045_rollover': {
                'eligible': section_1045_eligible,
                'description': 'Defer gain by rolling into new QSBS within 60 days' if section_1045_eligible else 'Not eligible - must hold 6+ months but less than 5 years',
                'benefit': 'Defer tax until new QSBS sold' if section_1045_eligible else None
            },
            'strategies': [
                'Stacking: Multiple founders can each exclude $10M+',
                'Section 1045 rollovers: Chain multiple QSBS investments',
                'Gift to family: Donee gets fresh 5-year holding period',
                'Estate planning: Stepped-up basis + QSBS benefits',
                'Trust planning: GRATs can hold QSBS',
                'Timing: Ensure 5-year holding before acquisition/exit'
            ],
            'excluded_industries': excluded_industries,
            'warnings': [
                'Redemptions within 2 years before/after issuance can disqualify',
                'Acquire at original issue, not secondary market',
                'Personal holding company rules apply',
                'State conformity varies (CA does NOT conform)',
                'Maintain contemporaneous records of asset test',
                'Active business requirement throughout holding period',
                'Section 1202(e)(3): 80% asset use test'
            ]
        }


class AugustaRuleCalculator:
    """
    Augusta Rule (Section 280A) - Rent Your Home to Your Business Tax-Free

    Rent your home to your business for up to 14 days/year. Business deducts rent,
    you don't report income. Named after Augusta, GA residents during Masters Tournament.
    """

    @staticmethod
    def calculate_augusta_rule_benefit(
        rental_days: int,
        daily_rate: float,
        comparable_venue_rate: float,
        business_structure: str = 's_corp',
        business_tax_rate: float = 0.21,
        personal_tax_rate: float = 0.37
    ) -> Dict[str, Any]:
        """
        Calculate Augusta Rule (Section 280A) benefits.

        Args:
            rental_days: Days home rented to business (max 14)
            daily_rate: Daily rental rate charged
            comparable_venue_rate: What local venues charge
            business_structure: Entity type (s_corp, c_corp, partnership, llc)
            business_tax_rate: Business tax rate
            personal_tax_rate: Owner's personal tax rate

        Returns:
            Augusta Rule benefit analysis
        """
        # Validate requirements
        is_valid = rental_days <= 14 and business_structure != 'sole_prop'

        if not is_valid:
            return {
                'valid': False,
                'reason': 'Rental days > 14' if rental_days > 14 else 'Not available for sole proprietors',
                'recommendation': 'Consider restructuring as S-Corp or LLC taxed as partnership'
            }

        # Calculate rental income
        total_rental_income = rental_days * daily_rate

        # Check if rate is reasonable
        rate_reasonable = daily_rate <= (comparable_venue_rate * 1.2)  # Allow 20% premium

        # Tax savings calculation
        business_deduction_value = total_rental_income * business_tax_rate
        personal_income_tax_avoided = total_rental_income * personal_tax_rate
        self_employment_tax_avoided = total_rental_income * 0.153  # 15.3% SE tax

        # Total benefit depends on structure
        if business_structure in ['s_corp', 'partnership', 'llc']:
            # Flow-through entity: Business deducts, owner pays no tax
            total_tax_savings = business_deduction_value + self_employment_tax_avoided
        else:  # c_corp
            # C-corp: Corporate deduction, no income to owner
            total_tax_savings = business_deduction_value

        # Documentation requirements
        documentation = {
            'required': [
                'Board minutes approving rental',
                'Written rental agreement',
                'Invoice from owner to business',
                'Payment receipt/cancelled check',
                'Meeting agenda and attendance',
                'Comparable venue rate research',
                'Photos of business use',
                'Business purpose documentation'
            ],
            'best_practices': [
                'Hold legitimate business meetings (not entertainment)',
                'Annual planning meetings',
                'Board meetings',
                'Strategic planning sessions',
                'Quarterly business reviews',
                'Team building (with business purpose)',
                'Client presentations'
            ]
        }

        # Common mistakes
        red_flags = []
        if daily_rate > (comparable_venue_rate * 1.5):
            red_flags.append(f'Daily rate ${daily_rate:,.0f} significantly exceeds market ${comparable_venue_rate:,.0f}')
        if rental_days > 14:
            red_flags.append('Exceeds 14-day limit - entire strategy disallowed')
        if business_structure == 'sole_prop':
            red_flags.append('Not available for sole proprietors')

        return {
            'valid': is_valid and rate_reasonable,
            'rental_details': {
                'days_rented': rental_days,
                'daily_rate': daily_rate,
                'total_rental_income': total_rental_income,
                'comparable_rate': comparable_venue_rate,
                'rate_is_reasonable': rate_reasonable
            },
            'tax_benefits': {
                'business_deduction': total_rental_income,
                'business_tax_savings': business_deduction_value,
                'personal_income_tax_avoided': personal_income_tax_avoided,
                'self_employment_tax_avoided': self_employment_tax_avoided if business_structure != 'c_corp' else 0,
                'total_tax_savings': total_tax_savings,
                'effective_tax_rate': 0  # No tax on rental income
            },
            'documentation': documentation,
            'red_flags': red_flags,
            'eligible_structures': {
                's_corp': True,
                'c_corp': True,
                'partnership': True,
                'multi_member_llc': True,
                'sole_proprietorship': False,
                'single_member_llc': False
            },
            'strategies': [
                'Use for high-value planning sessions (justify higher rates)',
                'Research luxury home rental rates in area',
                'Consider commercial space rates as comparables',
                'Max out 14 days with quarterly meetings',
                'Combine with meals (additional deduction)',
                'Virtual attendees still count as business meeting',
                'Can include spouse if employee/shareholder'
            ],
            'warnings': [
                'IRS scrutiny increased after 2018 Tax Cuts and Jobs Act',
                'Courts require "reasonable" rent - not "extravagant"',
                'Cannot be primarily for entertainment',
                'Must be legitimate business purpose',
                'Document contemporaneously (not after the fact)',
                'Cannot rent to yourself as sole proprietor',
                'Mixed use (personal + rental) exceeding 14 days triggers reporting',
                'Some states may not conform to federal treatment'
            ]
        }


class REPSCalculator:
    """
    Real Estate Professional Status (REPS) - Convert Passive Losses to Active

    Unlock unlimited rental real estate losses against W-2 and business income.
    Requires 750+ hours annually and >50% of time in real estate.
    """

    @staticmethod
    def calculate_reps_qualification(
        real_estate_hours: int,
        total_work_hours: int,
        rental_properties: int,
        rental_losses: float,
        w2_income: float = 0,
        make_grouping_election: bool = True,
        properties_material_participation: List[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Calculate Real Estate Professional Status qualification and tax benefits.

        Args:
            real_estate_hours: Hours in real estate activities
            total_work_hours: Total work hours all activities
            rental_properties: Number of rental properties owned
            rental_losses: Total rental losses from all properties
            w2_income: W-2 income to offset
            make_grouping_election: Elect to group all rentals as single activity?
            properties_material_participation: Hours per property for material participation

        Returns:
            REPS qualification analysis
        """
        # Test 1: 750 hours in real property trades or businesses
        meets_750_hours = real_estate_hours >= 750

        # Test 2: More than 50% of personal services in real estate
        real_estate_percentage = (real_estate_hours / total_work_hours * 100) if total_work_hours > 0 else 0
        meets_50_percent = real_estate_percentage > 50

        # Qualifies as Real Estate Professional
        qualifies_as_reps = meets_750_hours and meets_50_percent

        # Material Participation Tests (need to pass 1 of 7)
        material_participation_tests = {
            'test_1_500_hours': 'Participate > 500 hours in activity',
            'test_2_substantially_all': 'Do substantially all work (>80%)',
            'test_3_100_hours_no_one_more': 'Participate >100 hours and no one else more',
            'test_4_significant_participation': 'Multiple activities >100 hours each, >500 total',
            'test_5_material_5_of_10': 'Materially participated 5 of last 10 years',
            'test_6_personal_service_activity': 'Personal service activity materially participated 3 years',
            'test_7_facts_and_circumstances': 'Facts and circumstances + >100 hours'
        }

        # If grouping election made, treat all rentals as one activity
        if make_grouping_election:
            # With grouping, all RE hours count toward material participation
            meets_material_participation = real_estate_hours >= 500  # Test 1
            material_participation_method = 'Grouping Election + 500+ hours' if meets_material_participation else 'Need 500+ hours with grouping election'
        else:
            # Without grouping, must meet material participation for EACH property
            if properties_material_participation:
                properties_meeting_mp = sum(
                    1 for prop in properties_material_participation
                    if prop.get('hours', 0) >= 500
                )
                meets_material_participation = properties_meeting_mp == rental_properties
                material_participation_method = f'{properties_meeting_mp}/{rental_properties} properties meet 500-hour test'
            else:
                meets_material_participation = False
                material_participation_method = 'Must track hours per property'

        # Calculate tax savings
        if qualifies_as_reps and meets_material_participation:
            # Losses are active, can offset W-2 and business income
            offsettable_losses = min(abs(rental_losses), w2_income) if rental_losses < 0 else 0
            tax_rate = 0.37 + 0.153  # Top rate + SE tax
            tax_savings = offsettable_losses * tax_rate
            loss_treatment = 'ACTIVE'
        else:
            # Losses are passive, subject to PAL rules
            offsettable_losses = 0
            tax_savings = 0
            loss_treatment = 'PASSIVE'

        # Grouping election pros/cons
        grouping_election_analysis = {
            'pros': [
                'Easier to meet 500-hour material participation test',
                'Aggregate all RE hours across properties',
                'Simpler record-keeping',
                'One activity vs tracking multiple'
            ],
            'cons': [
                'Irrevocable binding election',
                'Continues even if no longer REPS',
                'Passive activity credits affected',
                'Property sales may trigger ordinary income',
                'Cannot segregate profitable vs loss properties'
            ],
            'recommended': rental_properties > 3
        }

        # Documentation requirements
        documentation = {
            'required_records': [
                'Contemporaneous time logs (daily/weekly)',
                'Appointment calendars',
                'Mileage logs',
                'Correspondence with tenants/vendors',
                'Property management activities log',
                'Repair/maintenance supervision records',
                'Form 8582 (Passive Activity Loss Limitations)',
                'Grouping election statement (if applicable)'
            ],
            'qualifying_activities': [
                'Property showings and tenant screenings',
                'Lease negotiations',
                'Rent collection',
                'Supervising repairs/maintenance',
                'Property management',
                'Marketing vacant units',
                'Financial analysis and reporting',
                'Bookkeeping and accounting',
                'Time spent traveling between properties'
            ],
            'non_qualifying': [
                'Time as investor (not trade/business)',
                'Passive ownership activities',
                'Time in different trade/business',
                'W-2 employee time (unless real estate)'
            ]
        }

        return {
            'qualifies_as_reps': qualifies_as_reps,
            'reps_tests': {
                'test_1_750_hours': {
                    'required': 750,
                    'actual': real_estate_hours,
                    'meets': meets_750_hours
                },
                'test_2_50_percent_time': {
                    'required': '>50%',
                    'actual': f'{real_estate_percentage:.1f}%',
                    'meets': meets_50_percent
                }
            },
            'material_participation': {
                'qualifies': meets_material_participation,
                'method': material_participation_method,
                'grouping_election_made': make_grouping_election,
                'tests': material_participation_tests
            },
            'tax_impact': {
                'rental_losses': rental_losses,
                'loss_treatment': loss_treatment,
                'offsettable_against_w2': offsettable_losses,
                'tax_savings': tax_savings,
                'effective_tax_rate_on_losses': 0 if loss_treatment == 'ACTIVE' else None
            },
            'grouping_election': grouping_election_analysis,
            'documentation': documentation,
            'strategies': [
                'Spouse can qualify even if other spouse has W-2',
                'Short-term rentals may qualify without REPS (>7 day average stay + substantial services)',
                'Track ALL time including travel, phone calls, emails',
                'Combine W-2 real estate job + rental to meet hours',
                'Real estate agent/broker qualifies for REPS hours',
                'Property manager hours count',
                'House hacking: live in one unit, rent others',
                'Use detailed time tracking app (not estimates)'
            ],
            'warnings': [
                'IRS closely scrutinizes REPS claims',
                'Gajewski v. Commissioner (2014) - inadequate records',
                'Contemporaneous records required (not reconstructed)',
                'Suspended passive losses remain if lose REPS status',
                'Grouping election is irrevocable',
                'Each spouse must separately qualify',
                'Personal time in property maintenance does not count',
                'Real estate investment (not trade/business) does not count'
            ]
        }


class MegaBackdoorRothCalculator:
    """
    Mega Backdoor Roth - Contribute $46K+ Beyond Normal 401k Limits

    Use after-tax 401k contributions and convert to Roth. No income limits.
    Requires specific plan features (only 11% of plans allow this).
    """

    @staticmethod
    def calculate_mega_backdoor_roth(
        age: int,
        current_401k_deferrals: float,
        employer_match: float,
        plan_allows_after_tax: bool = True,
        plan_allows_in_service_conversion: bool = True,
        tax_year: int = 2024
    ) -> Dict[str, Any]:
        """
        Calculate Mega Backdoor Roth contribution capacity.

        Args:
            age: Current age
            current_401k_deferrals: Pre-tax + Roth 401k contributions
            employer_match: Employer match + profit sharing
            plan_allows_after_tax: Does plan allow after-tax contributions?
            plan_allows_in_service_conversion: In-service distributions allowed?
            tax_year: 2024 or 2025

        Returns:
            Mega backdoor Roth analysis
        """
        # 2024 vs 2025 limits
        if tax_year == 2024:
            deferral_limit = 23_000
            catch_up = 7_500 if age >= 50 else 0
            total_limit = 69_000
            total_limit_with_catchup = 76_500 if age >= 50 else 69_000
        else:  # 2025
            deferral_limit = 23_500
            catch_up = 7_500 if age >= 50 else 0
            total_limit = 70_000
            total_limit_with_catchup = 77_500 if age >= 50 else 70_000

        # Check plan eligibility
        plan_eligible = plan_allows_after_tax and plan_allows_in_service_conversion

        if not plan_eligible:
            return {
                'eligible': False,
                'reason': 'Plan does not allow after-tax contributions' if not plan_allows_after_tax
                         else 'Plan does not allow in-service conversions',
                'recommendation': 'Ask HR to add these plan features or switch providers',
                'percentage_of_plans': '11% (as of 2023)'
            }

        # Calculate available room for after-tax contributions
        used_so_far = current_401k_deferrals + employer_match
        remaining_room = total_limit_with_catchup - used_so_far

        # After-tax contribution capacity
        after_tax_capacity = max(0, remaining_room)

        # Tax savings calculation (future)
        assumed_future_tax_rate = 0.37
        assumed_growth_30_years = after_tax_capacity * 5  # 5x growth assumption
        future_roth_distribution = assumed_growth_30_years
        tax_if_traditional = (future_roth_distribution - after_tax_capacity) * assumed_future_tax_rate

        return {
            'eligible': plan_eligible,
            'contribution_limits': {
                'employee_deferral_limit': deferral_limit,
                'catch_up_contribution': catch_up,
                'total_415c_limit': total_limit_with_catchup,
                'current_deferrals': current_401k_deferrals,
                'employer_contributions': employer_match,
                'used': used_so_far,
                'after_tax_capacity': after_tax_capacity
            },
            'mega_backdoor_potential': {
                'additional_annual_roth': after_tax_capacity,
                'additional_monthly': after_tax_capacity / 12,
                'vs_standard_roth_ira': f'+{after_tax_capacity - 7000:,.0f}' if after_tax_capacity > 7000 else 'Less than Roth IRA',
                'no_income_limits': True
            },
            'conversion_options': {
                'roth_401k': {
                    'method': 'In-plan Roth conversion',
                    'pros': 'Stays in 401k, creditor protection',
                    'cons': 'RMDs apply, less investment options'
                },
                'roth_ira': {
                    'method': 'In-service distribution to Roth IRA',
                    'pros': 'No RMDs, more investment options, estate planning',
                    'cons': 'May have waiting periods, out of 401k'
                }
            },
            'tax_treatment': {
                'after_tax_contributions': 'Not taxable on conversion',
                'earnings_on_after_tax': 'Taxable on conversion (minimize by converting frequently)',
                'future_withdrawals': 'Tax-free after age 59.5 + 5-year rule',
                'estimated_future_tax_savings': tax_if_traditional
            },
            'strategies': [
                'Convert immediately after contribution (minimize earnings)',
                'Automate: contribute after-tax + convert monthly',
                'Combine with regular Roth 401k for max Roth savings',
                'No income limits unlike direct Roth IRA',
                'Pro-rata rule does NOT apply (unlike backdoor Roth IRA)',
                'Can do even if have traditional IRA',
                'Estate planning: Roth IRA has no RMDs during life'
            ],
            'plan_requirements': {
                'after_tax_contributions': plan_allows_after_tax,
                'in_service_distributions_or_conversions': plan_allows_in_service_conversion,
                'non_discrimination_testing': 'Plan must pass (highly compensated employee rules)',
                'typical_waiting_period': '0-60 days depending on plan'
            },
            'warnings': [
                'Only 11% of 401k plans allow this (2023 data)',
                'Earnings between contribution and conversion are taxable',
                'Some plans require 2-year wait for in-service distributions',
                'Record-keeping critical for basis tracking',
                'Consult tax advisor before implementation',
                'May trigger non-discrimination testing failures',
                'Not available in SIMPLE IRA or SEP IRA plans'
            ],
            'alternatives_if_not_available': [
                'Regular backdoor Roth IRA ($7,000 limit)',
                'Spousal Roth IRA',
                'Taxable brokerage with tax-loss harvesting',
                'Cash value life insurance (PPLI)',
                'Ask employer to update 401k plan'
            ]
        }


class CashBalancePlanCalculator:
    """
    Cash Balance Plan + 401k Combo - Deduct $300K+ Annually

    Combine 401k ($69K limit) with Cash Balance Plan (up to $280K) for massive
    tax-deductible retirement contributions. Best for business owners 50+.
    """

    @staticmethod
    def calculate_cash_balance_plan(
        age: int,
        w2_compensation: float,
        business_net_income: float,
        current_401k_contribution: float = 0,
        employees_count: int = 0,
        target_retirement_age: int = 65
    ) -> Dict[str, Any]:
        """
        Calculate Cash Balance Plan contribution limits and tax savings.

        Args:
            age: Current age
            w2_compensation: W-2 wages (up to $345K limit)
            business_net_income: Net business income
            current_401k_contribution: Current 401k contributions
            employees_count: Number of employees (affects cost)
            target_retirement_age: Desired retirement age

        Returns:
            Cash Balance Plan analysis
        """
        # 2024 limits
        max_compensation = 345_000
        max_annual_benefit_at_65 = 275_000
        max_lump_sum_at_62 = 3_417_000

        # Capped compensation
        compensation_capped = min(w2_compensation, max_compensation)

        # 401k limits for 2024
        max_401k = 69_000 if age < 50 else 76_500

        # Cash Balance Plan contribution based on age
        # Older = larger contributions to reach same retirement benefit
        years_to_retirement = target_retirement_age - age

        if age >= 60:
            cb_contribution_rate = 0.45  # 45% of compensation
        elif age >= 55:
            cb_contribution_rate = 0.35  # 35%
        elif age >= 50:
            cb_contribution_rate = 0.25  # 25%
        elif age >= 45:
            cb_contribution_rate = 0.18  # 18%
        else:
            cb_contribution_rate = 0.12  # 12%

        # Calculate CB contribution
        cb_annual_contribution = compensation_capped * cb_contribution_rate
        cb_annual_contribution = min(cb_annual_contribution, 280_000)  # Practical limit

        # Total retirement contribution
        total_401k_cb = current_401k_contribution + cb_annual_contribution

        # Tax savings
        combined_tax_rate = 0.37 + 0.05  # Federal + State
        annual_tax_savings = total_401k_cb * combined_tax_rate

        # Employee cost (if applicable)
        if employees_count > 0:
            # Typically 5-7.5% of payroll for employees
            estimated_employee_cost_pct = 0.06
            employee_payroll_estimate = employees_count * 50_000  # Assume $50K avg
            employee_cost = employee_payroll_estimate * estimated_employee_cost_pct
        else:
            employee_cost = 0

        # Setup and admin costs
        setup_cost = 2_500
        annual_admin_cost = 2_000 + (employees_count * 100)

        # Net benefit
        net_annual_benefit = annual_tax_savings - employee_cost - annual_admin_cost

        # Accumulation over time (simplified)
        years_of_contributions = min(years_to_retirement, 20)  # Typical plan lifespan
        total_contributions = total_401k_cb * years_of_contributions
        assumed_growth_rate = 0.07
        future_value = total_contributions * ((1 + assumed_growth_rate) ** years_of_contributions)

        return {
            'contribution_analysis': {
                '401k_contribution': current_401k_contribution,
                'cash_balance_contribution': cb_annual_contribution,
                'total_annual_contribution': total_401k_cb,
                'contribution_as_pct_income': (total_401k_cb / business_net_income * 100) if business_net_income > 0 else 0
            },
            'tax_benefits': {
                'annual_tax_deduction': total_401k_cb,
                'annual_tax_savings': annual_tax_savings,
                'tax_savings_over_career': annual_tax_savings * years_of_contributions,
                'effective_contribution_cost': total_401k_cb - annual_tax_savings
            },
            'costs': {
                'setup_cost': setup_cost,
                'annual_administration': annual_admin_cost,
                'employee_contributions_required': employee_cost,
                'total_first_year_cost': setup_cost + annual_admin_cost + employee_cost,
                'ongoing_annual_cost': annual_admin_cost + employee_cost
            },
            'net_benefit': {
                'year_1_net': annual_tax_savings - setup_cost - annual_admin_cost - employee_cost,
                'annual_ongoing_net': net_annual_benefit,
                'break_even': 'Immediate if tax savings > costs'
            },
            'accumulation_projections': {
                'years_to_retirement': years_to_retirement,
                'total_contributions': total_contributions,
                'projected_retirement_value': future_value,
                'max_lump_sum_allowed': max_lump_sum_at_62
            },
            'plan_design': {
                'interest_credit_rate': '5% (typical safe harbor)',
                'vesting_schedule': '3-year cliff or 6-year graded',
                'contribution_formula': f'{cb_contribution_rate * 100:.0f}% of compensation (age-weighted)',
                'retirement_age': target_retirement_age,
                'lump_sum_available': True
            },
            'requirements': {
                'business_structure': 'Any (Sole prop, LLC, S-Corp, C-Corp, Partnership)',
                'minimum_employees': '0 (Solo 401k + CB works)',
                'irs_filing': 'Form 5500 required',
                'actuarial_certification': 'Required annually',
                'non_discrimination_testing': 'Must pass if employees exist'
            },
            'strategies': [
                'Max out 401k first, then add Cash Balance',
                'Best for ages 50+ (larger contributions)',
                'Combine with profit sharing for flexibility',
                'Defined benefit + defined contribution combo',
                'Use in high-income years before retirement',
                'Can have different contribution formulas for owners vs employees',
                'Cross-tested plans favor older owners',
                'Age-weighted profit sharing as simpler alternative'
            ],
            'warnings': [
                'Mandatory annual contributions (not discretionary)',
                'Must fund minimum even in loss years',
                'Expensive if many employees',
                'Non-discrimination testing can be complex',
                'Penalties for early termination',
                'Requires actuary and TPA',
                'Not suitable for unstable income businesses',
                'PBGC premiums may apply (rare for CB plans)',
                'Must continue for 3+ years ideally'
            ],
            'comparison': {
                'vs_sep_ira': f'+{cb_annual_contribution - (compensation_capped * 0.25):,.0f} more per year',
                'vs_simple_ira': f'+{cb_annual_contribution - 16_000:,.0f} more per year',
                'vs_solo_401k': f'+{cb_annual_contribution:,.0f} (CB is additive to 401k)'
            }
        }


class SCorpSalaryOptimizer:
    """
    S-Corp Reasonable Compensation Optimization

    Balance between salary (subject to payroll tax) and distributions (no payroll tax).
    Too low = IRS audit. Optimal = minimize payroll tax while staying "reasonable".
    """

    @staticmethod
    def calculate_optimal_salary(
        net_business_income: float,
        industry: str,
        years_in_business: int,
        business_duties: str = 'owner_operator',
        geographic_area: str = 'national_avg'
    ) -> Dict[str, Any]:
        """
        Calculate reasonable and optimal S-Corp salary to minimize payroll taxes.

        Args:
            net_business_income: Net income after expenses
            industry: Industry type
            years_in_business: Years operating
            business_duties: owner_operator, manager, executive
            geographic_area: Location for salary comparables

        Returns:
            Salary optimization analysis
        """
        # IRS "reasonable compensation" factors
        # Courts have used 30-50% of net income as safe harbor
        
        # Industry benchmarks (simplified)
        industry_multiples = {
            'consulting': 0.45,
            'professional_services': 0.45,
            'real_estate': 0.35,
            'retail': 0.30,
            'technology': 0.40,
            'healthcare': 0.50,
            'construction': 0.35,
            'manufacturing': 0.40,
            'services': 0.35
        }
        
        base_multiple = industry_multiples.get(industry, 0.40)
        
        # Adjustment factors
        if business_duties == 'executive':
            duty_multiplier = 1.2
        elif business_duties == 'manager':
            duty_multiplier = 1.0
        else:  # owner_operator
            duty_multiplier = 0.9
            
        # Experience adjustment
        if years_in_business >= 10:
            experience_multiplier = 1.1
        elif years_in_business >= 5:
            experience_multiplier = 1.0
        else:
            experience_multiplier = 0.9
            
        # Calculate salary ranges
        adjusted_multiple = base_multiple * duty_multiplier * experience_multiplier
        
        conservative_salary = net_business_income * (adjusted_multiple + 0.05)
        optimal_salary = net_business_income * adjusted_multiple
        aggressive_salary = net_business_income * (adjusted_multiple - 0.05)
        
        # Cap at net income
        conservative_salary = min(conservative_salary, net_business_income * 0.60)
        optimal_salary = min(optimal_salary, net_business_income * 0.50)
        aggressive_salary = min(aggressive_salary, net_business_income * 0.40)
        
        # Calculate tax impact for each scenario
        def calculate_taxes(salary, distribution):
            # Payroll taxes (15.3% on salary)
            payroll_tax = salary * 0.153
            
            # Income tax (simplified 37% top bracket)
            income_tax = (salary + distribution) * 0.37
            
            total_tax = payroll_tax + income_tax
            return {
                'salary': salary,
                'distribution': distribution,
                'payroll_tax': payroll_tax,
                'income_tax': income_tax,
                'total_tax': total_tax
            }
        
        conservative_scenario = calculate_taxes(
            conservative_salary, 
            net_business_income - conservative_salary
        )
        optimal_scenario = calculate_taxes(
            optimal_salary,
            net_business_income - optimal_salary
        )
        aggressive_scenario = calculate_taxes(
            aggressive_salary,
            net_business_income - aggressive_salary
        )
        
        # All salary scenario (for comparison)
        all_salary_scenario = calculate_taxes(net_business_income, 0)
        
        return {
            'recommendations': {
                'conservative': {
                    **conservative_scenario,
                    'risk_level': 'LOW',
                    'description': 'Safe harbor, minimal IRS risk'
                },
                'optimal': {
                    **optimal_scenario,
                    'risk_level': 'LOW-MODERATE',
                    'description': 'Balanced approach, generally defensible'
                },
                'aggressive': {
                    **aggressive_scenario,
                    'risk_level': 'MODERATE-HIGH',
                    'description': 'Higher tax savings, increased audit risk'
                }
            },
            'tax_savings_vs_all_salary': {
                'conservative': all_salary_scenario['total_tax'] - conservative_scenario['total_tax'],
                'optimal': all_salary_scenario['total_tax'] - optimal_scenario['total_tax'],
                'aggressive': all_salary_scenario['total_tax'] - aggressive_scenario['total_tax']
            },
            'irs_factors': [
                'Training and experience',
                'Duties and responsibilities',
                'Time and effort devoted',
                'Dividend history',
                'Payments to non-shareholder employees',
                'Timing and manner of paying bonuses',
                'What comparable businesses pay',
                'Compensation agreements',
                'Use of formula to determine compensation'
            ],
            'documentation': {
                'required': [
                    'Board meeting minutes approving salary',
                    'Industry salary surveys (BLS, Glassdoor, Salary.com)',
                    'Job description documenting duties',
                    'Time tracking (if also distributions)',
                    'Written compensation policy',
                    'Comparable position salaries in area'
                ],
                'court_cases': [
                    'Watson v. Commissioner (2010) - 70/30 split upheld',
                    'Radtke v. Commissioner (1990) - established factors',
                    'Dunn and Clark, P.A. v. Commissioner (1981)'
                ]
            },
            'strategies': [
                'Pay salary monthly, take distributions quarterly',
                'Consider bonus structure (still subject to payroll tax)',
                'S-corp distributions must be proportional to ownership',
                'Retain earnings for growth (no distribution required)',
                'Review and adjust salary annually',
                'Health insurance premiums for >2% owners are wages',
                'Retirement plan contributions separate from salary calc'
            ],
            'red_flags': [
                'Zero or minimal salary with large distributions',
                'Salary below industry minimum for position',
                'Consistent ratio over multiple years (looks formulaic)',
                'No documentation of compensation decision',
                'Salary lower than employees with similar duties',
                'Business showing consistent losses while taking distributions'
            ]
        }


class EstatePlanningCalculator:
    """
    Advanced Estate Planning Strategies (GRATs, IDGTs, SLATs)

    Sophisticated wealth transfer techniques used by ultra-high-net-worth families
    to minimize estate and gift taxes.
    """

    @staticmethod
    def calculate_grat(
        asset_value: float,
        grat_term_years: int,
        section_7520_rate: float = 0.054,
        expected_appreciation_rate: float = 0.10,
        annual_annuity_percentage: float = None
    ) -> Dict[str, Any]:
        """
        Calculate Grantor Retained Annuity Trust (GRAT) wealth transfer.

        Args:
            asset_value: FMV of asset transferred to GRAT
            grat_term_years: GRAT term (2-10 years typical)
            section_7520_rate: IRS Section 7520 rate
            expected_appreciation_rate: Expected asset appreciation
            annual_annuity_percentage: Annual payment % (if None, calculates zeroed-out)

        Returns:
            GRAT analysis
        """
        # Zeroed-out GRAT: Annuity = asset value + assumed growth
        # This results in zero taxable gift
        
        if annual_annuity_percentage is None:
            # Calculate zeroed-out GRAT annuity payment
            # Formula: Annuity = Asset Value / PVAF
            # PVAF = Present Value Annuity Factor
            pvaf = (1 - (1 + section_7520_rate) ** -grat_term_years) / section_7520_rate
            annual_annuity = asset_value / pvaf
        else:
            annual_annuity = asset_value * annual_annuity_percentage
        
        total_annuity_paid = annual_annuity * grat_term_years
        
        # Future value of asset
        future_value = asset_value * ((1 + expected_appreciation_rate) ** grat_term_years)
        
        # Remainder to beneficiaries
        remainder_value = future_value - total_annuity_paid
        
        # Gift tax paid (on present value of remainder)
        # Zeroed-out GRAT = minimal/no gift tax
        pv_remainder = remainder_value / ((1 + section_7520_rate) ** grat_term_years)
        gift_tax_on_remainder = pv_remainder * 0.40  # 40% gift tax rate
        
        # Estate tax saved
        estate_tax_rate = 0.40
        estate_tax_saved = remainder_value * estate_tax_rate
        
        return {
            'grat_structure': {
                'initial_funding': asset_value,
                'grat_term_years': grat_term_years,
                'annual_annuity_payment': annual_annuity,
                'total_annuity_returned': total_annuity_paid,
                'annuity_percentage': (annual_annuity / asset_value) * 100
            },
            'assumptions': {
                'section_7520_rate': section_7520_rate * 100,
                'expected_appreciation': expected_appreciation_rate * 100,
                'hurdle_rate': section_7520_rate * 100,
                'excess_return': (expected_appreciation_rate - section_7520_rate) * 100
            },
            'wealth_transfer': {
                'asset_future_value': future_value,
                'annuity_returned_to_grantor': total_annuity_paid,
                'remainder_to_beneficiaries': remainder_value,
                'gift_tax_paid': gift_tax_on_remainder,
                'estate_tax_saved': estate_tax_saved,
                'net_transfer': remainder_value - gift_tax_on_remainder
            },
            'strategies': [
                'Zeroed-out GRAT: Annuity = asset value (no gift tax)',
                'Rolling GRATs: Chain multiple 2-year GRATs',
                'Walton GRAT: Delay payments (better for fast appreciation)',
                'Use assets expected to outperform 7520 rate',
                'Best assets: Closely-held business, pre-IPO stock, real estate',
                'Grantor survives term or GRAT fails (estate inclusion)',
                'Can use discount valuation for FLP/LLC interests',
                'Successive GRATs to compound tax-free transfers'
            ],
            'requirements': {
                'minimum_term': 'None (but 2+ years practical)',
                'annual_payments': 'Must be made to grantor',
                'qualified_annuity': 'Fixed dollar amount or percentage',
                'termination': 'Remainder passes to beneficiaries',
                'grantor_survives_term': 'Must survive or assets back in estate',
                'irs_filing': 'Form 709 (even if zeroed out)'
            },
            'mortality_risk': {
                'description': 'If grantor dies during term, assets pull back into estate',
                'mitigation': 'Short 2-year terms, purchase life insurance',
                'probability_survival': f'{(1 - 0.01) ** grat_term_years * 100:.1f}% (assumes 1% annual mortality)'
            },
            'warnings': [
                'Must survive GRAT term or strategy fails',
                'Annuity payments back to grantor (income tax implications)',
                'Low 7520 rates = larger annuities needed',
                'Assets must appreciate above 7520 rate to succeed',
                'Cannot swap assets during term',
                'State law variations exist',
                'Professional drafting required ($5K-$15K)'
            ]
        }

    @staticmethod
    def calculate_idgt_slat(
        asset_value: float,
        gift_tax_exemption_used: float,
        trust_term_years: int,
        expected_appreciation_rate: float = 0.08,
        grantor_pays_income_tax: bool = True
    ) -> Dict[str, Any]:
        """
        Calculate Intentionally Defective Grantor Trust (IDGT) or 
        Spousal Lifetime Access Trust (SLAT) wealth transfer.

        Args:
            asset_value: Value of asset gifted to trust
            gift_tax_exemption_used: Amount of gift tax exemption used
            trust_term_years: Trust duration (or lifetime)
            expected_appreciation_rate: Expected asset appreciation
            grantor_pays_income_tax: Grantor pays trust's income tax?

        Returns:
            IDGT/SLAT analysis
        """
        # Calculate gift tax
        gift_amount = asset_value
        exemption_remaining = 13_990_000 - gift_tax_exemption_used  # 2025 exemption
        
        if gift_amount <= exemption_remaining:
            gift_tax_paid = 0
            exemption_used = gift_amount
        else:
            taxable_gift = gift_amount - exemption_remaining
            gift_tax_paid = taxable_gift * 0.40
            exemption_used = exemption_remaining
        
        # Future value of asset in trust
        future_value = asset_value * ((1 + expected_appreciation_rate) ** trust_term_years)
        
        # If grantor pays income tax, trust grows tax-free (additional wealth transfer)
        if grantor_pays_income_tax:
            # Assume 8% return, 37% tax on income
            annual_income_tax_on_trust = asset_value * 0.08 * 0.37
            total_income_tax_paid = annual_income_tax_on_trust * trust_term_years
            
            # This is additional tax-free gift
            tax_free_transfer_value = total_income_tax_paid
        else:
            total_income_tax_paid = 0
            tax_free_transfer_value = 0
        
        # Estate tax savings
        estate_tax_saved = future_value * 0.40
        
        return {
            'gift_to_trust': {
                'asset_value': asset_value,
                'gift_tax_exemption_used': exemption_used,
                'gift_tax_paid': gift_tax_paid,
                'remaining_exemption': max(0, exemption_remaining - gift_amount)
            },
            'trust_characteristics': {
                'grantor_trust_status': 'Intentionally Defective (grantor pays income tax)',
                'estate_inclusion': 'Excluded from grantor estate',
                'beneficiary_access': 'Beneficiaries/Spouse (SLAT) can access principal',
                'term': f'{trust_term_years} years or lifetime',
                'creditor_protection': 'Yes (for beneficiaries)'
            },
            'wealth_transfer': {
                'initial_gift': asset_value,
                'future_value_in_trust': future_value,
                'growth_outside_estate': future_value - asset_value,
                'income_tax_paid_by_grantor': total_income_tax_paid,
                'additional_tax_free_transfer': tax_free_transfer_value,
                'total_estate_tax_saved': estate_tax_saved,
                'total_wealth_transferred': future_value + tax_free_transfer_value
            },
            'idgt_features': {
                'defects': [
                    'Power to substitute assets of equivalent value',
                    'Power to borrow without adequate security',
                    'Retained administrative powers',
                    'Power to add beneficiaries from limited class'
                ],
                'income_tax_treatment': 'Grantor pays income tax on trust income',
                'estate_tax_treatment': 'Assets excluded from estate',
                'benefit': 'Tax-free gift via grantor paying income tax'
            },
            'slat_specific': {
                'spousal_access': 'Spouse can receive distributions',
                'divorce_risk': 'May lose access if divorced',
                'reciprocal_trust_doctrine': 'Avoid identical reciprocal SLATs',
                'common_uses': 'Utilize expiring gift exemption before sunset'
            },
            'strategies': [
                'Front-load gifts before exemption sunsets (2026)',
                'Use leveraged assets (pre-IPO, FLP interests)',
                'Seed with low-basis assets (avoid capital gains)',
                'Installment sale to IDGT (further leverage)',
                'Combine with valuation discounts (30-40%)',
                'Grantor can rent assets from trust',
                'Life insurance inside IDGT (income tax-free growth)'
            ],
            '2026_sunset_warning': {
                'current_exemption_2025': 13_990_000,
                'post_sunset_exemption_2026': '~7,000,000 (estimated)',
                'clawback_protection': 'IRS says no clawback on pre-2026 gifts',
                'urgency': 'ACT BEFORE 12/31/2025 to lock in high exemption'
            },
            'warnings': [
                'Reciprocal trust doctrine (SLATs) - avoid identical trusts',
                'Divorce can eliminate spousal access (SLAT)',
                'Grantor must pay income tax on trust income',
                'Cannot be revocable',
                'Professional drafting required ($10K-$25K)',
                'State income tax implications vary',
                'Must maintain defects for grantor trust status'
            ]
        }


class TaxLossHarvestingCalculator:
    """
    Tax Loss Harvesting and Wash Sale Rule Optimization

    Harvest investment losses to offset gains while avoiding wash sale rules.
    Includes cryptocurrency, substantially identical securities, and timing strategies.
    """

    @staticmethod
    def calculate_tax_loss_harvesting(
        capital_gains_realized: float,
        available_losses: float,
        ordinary_income: float,
        holding_period: str = 'long_term',
        has_carryforward_losses: float = 0
    ) -> Dict[str, Any]:
        """
        Calculate tax loss harvesting benefits.

        Args:
            capital_gains_realized: Capital gains realized this year
            available_losses: Unrealized losses available to harvest
            ordinary_income: Ordinary income (W-2, business)
            holding_period: short_term or long_term
            has_carryforward_losses: Prior year loss carryforwards

        Returns:
            Tax loss harvesting analysis
        """
        # Tax rates
        ltcg_rate = 0.20  # Long-term capital gains
        stcg_rate = 0.37  # Short-term = ordinary income rate
        niit_rate = 0.038  # Net Investment Income Tax
        
        # Total gains
        total_gains = capital_gains_realized
        
        # Apply carryforward losses first
        gains_after_carryforward = max(0, total_gains - has_carryforward_losses)
        carryforward_used = min(total_gains, has_carryforward_losses)
        
        # Apply harvested losses
        gains_after_harvesting = max(0, gains_after_carryforward - available_losses)
        harvested_losses_used = min(gains_after_carryforward, available_losses)
        
        # If losses exceed gains, can offset $3K ordinary income
        excess_losses = available_losses - harvested_losses_used
        ordinary_income_offset = min(excess_losses, 3000)
        
        # Remaining losses carryforward indefinitely
        new_loss_carryforward = excess_losses - ordinary_income_offset
        
        # Tax savings calculation
        if holding_period == 'long_term':
            gains_tax_rate = ltcg_rate + niit_rate
        else:
            gains_tax_rate = stcg_rate + niit_rate
        
        tax_on_gains_without_harvesting = total_gains * gains_tax_rate
        tax_on_gains_with_harvesting = gains_after_harvesting * gains_tax_rate
        ordinary_income_tax_savings = ordinary_income_offset * stcg_rate
        
        total_tax_savings = (
            (tax_on_gains_without_harvesting - tax_on_gains_with_harvesting) +
            ordinary_income_tax_savings
        )
        
        # Wash sale rule
        wash_sale_rules = {
            'rule': 'Cannot buy substantially identical security 30 days before or after sale',
            'period': '61 days total (30 before + day of + 30 after)',
            'substantially_identical': [
                'Same stock/ETF',
                'Options on same stock',
                'Convertible bonds/preferred',
                'Warrants on same stock'
            ],
            'not_substantially_identical': [
                'Different company stock (even same sector)',
                'Different ETF tracking same index (VTI vs ITOT)',
                'Futures vs ETF',
                'Individual stocks vs index ETF',
                'Options vs stock (30+ days expiry difference)'
            ]
        }
        
        return {
            'loss_utilization': {
                'capital_gains': total_gains,
                'carryforward_losses_applied': carryforward_used,
                'harvested_losses_applied': harvested_losses_used,
                'ordinary_income_offset': ordinary_income_offset,
                'new_loss_carryforward': new_loss_carryforward
            },
            'tax_savings': {
                'tax_without_harvesting': tax_on_gains_without_harvesting,
                'tax_with_harvesting': tax_on_gains_with_harvesting,
                'capital_gains_tax_saved': tax_on_gains_without_harvesting - tax_on_gains_with_harvesting,
                'ordinary_income_tax_saved': ordinary_income_tax_savings,
                'total_current_year_savings': total_tax_savings,
                'future_value_of_carryforward': new_loss_carryforward * gains_tax_rate
            },
            'wash_sale_rules': wash_sale_rules,
            'strategies': [
                'Harvest losses in December, reinvest in similar (not identical) ETF',
                'Use different ETF tracking same index (VTI → ITOT)',
                'Wait 31 days to repurchase identical security',
                'Buy similar stock in same sector',
                'Crypto: No wash sale rules (harvest anytime)',
                'Tax gain harvesting in low-income years (0% LTCG bracket)',
                'Pair losses with high-basis stock sales',
                'Harvest losses across taxable accounts'
            ],
            'cryptocurrency_advantage': {
                'wash_sale_applies': False,
                'description': 'Crypto not subject to wash sale rules (IRS property)',
                'strategy': 'Sell and immediately repurchase same crypto',
                'best_for': 'Bitcoin/Ethereum high volatility years'
            },
            'timing_strategies': {
                'year_end_harvesting': 'December for current year benefit',
                'post_earnings_volatility': 'Harvest after negative earnings',
                'market_corrections': '10%+ drawdowns provide opportunities',
                'tax_gain_harvesting': 'Realize gains in 0% LTCG bracket years',
                'bunching': 'Harvest multiple years losses in one year if needed'
            },
            'warnings': [
                'Wash sale rule disallows loss if identical security purchased 30 days before/after',
                'Applies across all accounts (IRA purchases can trigger)',
                'Spouse accounts included',
                'Cost basis adjusts upward for disallowed loss',
                'Trading costs can exceed tax savings',
                'Short-term losses offset short-term gains first (higher rate)',
                'State conformity varies'
            ]
        }
