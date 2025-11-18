"""
Tax Shelters and Corporate Structures Analysis

This module provides analysis tools for evaluating legitimate tax shelters and corporate structures.
All strategies must comply with IRS regulations and substance-over-form doctrine.

WARNING: This is for educational and planning purposes. Always consult licensed tax professionals.
"""

from typing import Dict, List, Any, Optional
from decimal import Decimal
from datetime import datetime


class TaxShelterEvaluator:
    """
    Evaluate and score various tax shelter strategies for legitimacy and risk.

    Under IRS scrutiny: Listed transactions, reportable transactions, tax avoidance schemes.
    """

    # IRS Listed Transactions (must be reported on Form 8886)
    LISTED_TRANSACTIONS = {
        'syndicated_conservation_easements': {
            'name': 'Syndicated Conservation Easements',
            'irs_notice': '2017-10',
            'risk_level': 'EXTREME',
            'description': 'Partnership deductions >2.5x investment',
            'final_regs_date': '2024-10-08',
            'reporting': 'Form 8886 required',
            'penalty': '$200,000+ for failure to disclose'
        },
        'abusive_micro_captives': {
            'name': 'Abusive Micro-Captive Insurance (831(b))',
            'irs_notice': '2016-66',
            'risk_level': 'EXTREME',
            'description': 'Loss ratio <30% with financing arrangements',
            'final_regs_date': '2025-01-10',
            'reporting': 'Form 8886 required if meets both tests',
            'penalty': 'Up to 75% penalty on understatement'
        },
        'abusive_charitable_remainder_annuity_trusts': {
            'name': 'Monetized Installment Sale / CRAT',
            'irs_notice': '2003-56',
            'risk_level': 'HIGH',
            'description': 'Using CRAT to monetize installment sale',
            'reporting': 'Form 8886 required',
            'penalty': 'Transaction disallowed + penalties'
        }
    }

    @staticmethod
    def evaluate_tax_shelter(
        strategy_name: str,
        investment_amount: float,
        expected_deduction: float,
        expected_loss: float,
        years_to_breakeven: int,
        has_economic_substance: bool,
        has_business_purpose: bool,
        promoter_fees_pct: float,
        involves_tax_haven: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate tax shelter for legitimacy and IRS risk.

        Args:
            strategy_name: Name of tax shelter strategy
            investment_amount: Cash invested
            expected_deduction: Total expected tax deductions
            expected_loss: Expected tax losses
            years_to_breakeven: Years to economic breakeven
            has_economic_substance: Has profit motive aside from tax benefits?
            has_business_purpose: Legitimate business purpose?
            promoter_fees_pct: Promoter fees as % of investment
            involves_tax_haven: Uses offshore tax haven?

        Returns:
            Risk assessment and IRS scrutiny score
        """
        risk_score = 0
        risk_factors = []
        red_flags = []

        # Economic Substance Doctrine
        if not has_economic_substance:
            risk_score += 40
            red_flags.append('FAILS Economic Substance Doctrine - No pre-tax profit motive')

        if not has_business_purpose:
            risk_score += 35
            red_flags.append('FAILS Business Purpose Test - Sole purpose is tax avoidance')

        # Deduction-to-Investment Ratio
        deduction_ratio = expected_deduction / investment_amount if investment_amount > 0 else 0

        if deduction_ratio > 4.0:
            risk_score += 25
            red_flags.append(f'Excessive deduction ratio: {deduction_ratio:.1f}x (>4x is abusive)')
        elif deduction_ratio > 2.5:
            risk_score += 15
            risk_factors.append(f'High deduction ratio: {deduction_ratio:.1f}x (2.5-4x requires scrutiny)')

        # Years to economic breakeven
        if years_to_breakeven > 20:
            risk_score += 20
            red_flags.append(f'Unrealistic breakeven: {years_to_breakeven} years')
        elif years_to_breakeven > 10:
            risk_score += 10
            risk_factors.append(f'Long breakeven period: {years_to_breakeven} years')

        # Promoter fees (IRS views high fees as indicator of abusive shelter)
        if promoter_fees_pct > 0.20:
            risk_score += 15
            red_flags.append(f'Excessive promoter fees: {promoter_fees_pct*100:.0f}% (>20%)')
        elif promoter_fees_pct > 0.10:
            risk_score += 8
            risk_factors.append(f'High promoter fees: {promoter_fees_pct*100:.0f}% (10-20%)')

        # Tax haven involvement
        if involves_tax_haven:
            risk_score += 20
            risk_factors.append('Involves offshore tax haven jurisdiction')

        # Loss-to-investment ratio
        loss_ratio = expected_loss / investment_amount if investment_amount > 0 else 0
        if loss_ratio > 2.0:
            risk_score += 15
            red_flags.append(f'Abusive loss ratio: {loss_ratio:.1f}x investment')

        # Determine risk level
        if risk_score >= 75:
            risk_level = 'EXTREME - Likely Abusive Tax Shelter'
            irs_action_expected = 'Audit + Disallowance + Penalties (20-40%)'
            recommendation = 'DO NOT PROCEED - High risk of IRS challenge'
        elif risk_score >= 50:
            risk_level = 'VERY HIGH - Reportable Transaction'
            irs_action_expected = 'Audit probable, Form 8886 disclosure required'
            recommendation = 'Consult tax attorney before proceeding'
        elif risk_score >= 30:
            risk_level = 'HIGH - Enhanced Scrutiny'
            irs_action_expected = 'Increased audit risk, prepare robust documentation'
            recommendation = 'Requires strong economic substance documentation'
        elif risk_score >= 15:
            risk_level = 'MODERATE'
            irs_action_expected = 'Standard audit risk if selected'
            recommendation = 'Maintain good records, ensure business purpose'
        else:
            risk_level = 'LOW'
            irs_action_expected = 'Minimal additional scrutiny'
            recommendation = 'Appears to be legitimate tax planning'

        # Calculate net economic benefit
        tax_rate = 0.37  # Top federal rate
        tax_benefit = (expected_deduction + expected_loss) * tax_rate
        promoter_fees = investment_amount * promoter_fees_pct
        net_benefit = tax_benefit - investment_amount - promoter_fees

        # IRS Penalties if disallowed
        potential_penalties = {
            'accuracy_related_20_pct': expected_deduction * tax_rate * 0.20,
            'substantial_understatement_20_pct': expected_deduction * tax_rate * 0.20,
            'gross_valuation_misstatement_40_pct': expected_deduction * tax_rate * 0.40 if deduction_ratio > 4 else 0,
            'reportable_transaction_penalty': 200_000 if risk_score >= 50 else 0,
            'interest_at_6_pct_annual': expected_deduction * tax_rate * 0.06 * 3  # 3 years assumed
        }

        total_downside_risk = sum(potential_penalties.values())

        return {
            'strategy': strategy_name,
            'risk_assessment': {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'irs_action_expected': irs_action_expected,
                'recommendation': recommendation
            },
            'economic_analysis': {
                'investment': investment_amount,
                'expected_deduction': expected_deduction,
                'expected_loss': expected_loss,
                'deduction_ratio': deduction_ratio,
                'loss_ratio': loss_ratio,
                'tax_benefit': tax_benefit,
                'promoter_fees': promoter_fees,
                'net_economic_benefit': net_benefit,
                'years_to_breakeven': years_to_breakeven
            },
            'doctrine_tests': {
                'economic_substance': 'PASS' if has_economic_substance else 'FAIL',
                'business_purpose': 'PASS' if has_business_purpose else 'FAIL',
                'substance_over_form': 'Analysis Required',
                'step_transaction': 'Analysis Required'
            },
            'red_flags': red_flags,
            'risk_factors': risk_factors,
            'potential_penalties': potential_penalties,
            'total_downside_risk': total_downside_risk,
            'risk_reward_ratio': total_downside_risk / max(net_benefit, 1) if net_benefit > 0 else float('inf'),
            'reporting_requirements': {
                'form_8886': risk_score >= 50,
                'form_8275_disclosure': risk_score >= 30,
                'maintain_documentation': True,
                'contemporaneous_business_purpose_memo': risk_score >= 15
            }
        }

    @staticmethod
    def compare_legitimate_shelters() -> Dict[str, Any]:
        """
        Compare legitimate tax shelters with risk/reward profiles.
        """
        legitimate_strategies = {
            'real_estate_depreciation': {
                'name': 'Real Estate Depreciation & Cost Segregation',
                'irs_risk': 'LOW',
                'deduction_ratio': 0.3,
                'legitimacy': 'Fully legitimate, established IRS guidance',
                'requirements': 'Professional cost seg study, actual rental activity',
                'best_for': 'Real estate investors with depreciation >$100K'
            },
            'retirement_accounts': {
                'name': 'Qualified Retirement Plans (401k, Defined Benefit)',
                'irs_risk': 'LOW',
                'deduction_ratio': 1.0,
                'legitimacy': 'Explicitly encouraged by tax code',
                'requirements': 'Qualified plan documents, annual administration',
                'best_for': 'Business owners with W-2 income'
            },
            'opportunity_zones': {
                'name': 'Qualified Opportunity Zones',
                'irs_risk': 'LOW-MODERATE',
                'deduction_ratio': 0.15,
                'legitimacy': 'Created by 2017 Tax Cuts and Jobs Act',
                'requirements': 'Investment in designated QOZ, 10-year hold',
                'best_for': 'Capital gains deferral and step-up'
            },
            'charitable_giving': {
                'name': 'Charitable Remainder Trust (CRT)',
                'irs_risk': 'LOW',
                'deduction_ratio': 0.4,
                'legitimacy': 'Long-established estate planning tool',
                'requirements': 'Qualified charity, proper trust administration',
                'best_for': 'Highly appreciated assets, charitable intent'
            },
            'conservation_easements_legitimate': {
                'name': 'Individual Conservation Easements',
                'irs_risk': 'MODERATE',
                'deduction_ratio': 0.8,
                'legitimacy': 'Legitimate if properly valued and not syndicated',
                'requirements': 'Qualified appraisal, actual conservation purpose',
                'best_for': 'Landowners with preservation goals'
            },
            'dst_1031_exchanges': {
                'name': 'Delaware Statutory Trust 1031 Exchanges',
                'irs_risk': 'LOW',
                'deduction_ratio': 0.0,
                'legitimacy': 'IRS Rev. Rul. 2004-86 approval',
                'requirements': '1031 exchange rules, revenue ruling compliance',
                'best_for': 'Deferring capital gains on investment property'
            }
        }

        return legitimate_strategies


class ShelfCompanyAnalyzer:
    """
    Analyze shelf companies (aged corporations) for legitimate uses and risks.

    Shelf companies can be legitimate but are often used for questionable purposes.
    """

    FORMATION_STATES = {
        'delaware': {
            'corporate_tax': 'None on out-of-state income',
            'franchise_tax': '$300+ annual',
            'privacy': 'High - nominees permitted',
            'reputation': 'Gold standard for corporations',
            'best_for': 'C-corps, venture-backed startups'
        },
        'wyoming': {
            'corporate_tax': 'None',
            'franchise_tax': '$60 annual',
            'privacy': 'Highest - no beneficial owner disclosure',
            'reputation': 'Privacy-focused',
            'best_for': 'LLCs, asset protection'
        },
        'nevada': {
            'corporate_tax': 'None',
            'franchise_tax': '$500+ annual',
            'privacy': 'High - nominees permitted',
            'reputation': 'Tax-friendly, privacy',
            'best_for': 'Asset protection, privacy'
        },
        'montana': {
            'corporate_tax': '6.75%',
            'franchise_tax': '$20 annual',
            'privacy': 'Medium',
            'reputation': 'Vehicle registration loophole',
            'best_for': 'Montana LLC for vehicle registration'
        }
    }

    @staticmethod
    def analyze_shelf_company(
        purchase_price: float,
        company_age_years: int,
        has_credit_history: bool,
        intended_use: str,
        formation_state: str = 'delaware'
    ) -> Dict[str, Any]:
        """
        Analyze shelf company purchase for risks and benefits.

        Args:
            purchase_price: Cost to purchase shelf company
            company_age_years: Age of corporation
            has_credit_history: Does company have established credit?
            intended_use: Reason for purchasing (business_credit, contract_bidding, etc.)
            formation_state: State of incorporation

        Returns:
            Shelf company analysis
        """
        # Legitimate uses
        legitimate_uses = {
            'contract_bidding': {
                'legitimacy': 'HIGH',
                'description': 'Qualify for contracts requiring X years in business',
                'risk': 'LOW if company never operated'
            },
            'business_credit': {
                'legitimacy': 'MEDIUM',
                'description': 'Establish business credit history',
                'risk': 'MEDIUM - Creditors scrutinize shelf companies'
            },
            'time_savings': {
                'legitimacy': 'HIGH',
                'description': 'Immediate entity formation',
                'risk': 'LOW'
            },
            'tender_offers': {
                'legitimacy': 'HIGH',
                'description': 'Meet age requirements for bids',
                'risk': 'LOW if disclosed'
            },
            'bank_account': {
                'legitimacy': 'HIGH',
                'description': 'Open business bank account quickly',
                'risk': 'LOW'
            }
        }

        # Questionable uses (high risk)
        questionable_uses = {
            'credit_fraud': {
                'legitimacy': 'ILLEGAL',
                'description': 'Misrepresent credit history',
                'risk': 'EXTREME - Federal crime'
            },
            'tax_evasion': {
                'legitimacy': 'ILLEGAL',
                'description': 'Hide income or assets from IRS',
                'risk': 'EXTREME - Federal crime'
            },
            'liability_shell_game': {
                'legitimacy': 'ILLEGAL',
                'description': 'Evade existing liabilities',
                'risk': 'EXTREME - Piercing corporate veil'
            },
            'money_laundering': {
                'legitimacy': 'ILLEGAL',
                'description': 'Obscure source of funds',
                'risk': 'EXTREME - Federal crime'
            }
        }

        # Check if intended use is legitimate
        use_analysis = legitimate_uses.get(intended_use, questionable_uses.get(intended_use, {
            'legitimacy': 'UNKNOWN',
            'description': 'Use case not categorized',
            'risk': 'UNKNOWN'
        }))

        # Tax benefit analysis
        tax_benefits = {
            'section_179_deduction': {
                'available': False,
                'reason': 'Shelf companies may not qualify - must be NEW property'
            },
            'bonus_depreciation': {
                'available': False,
                'reason': 'Shelf companies may not qualify for bonus depreciation incentives'
            },
            'net_operating_loss_carryforward': {
                'available': False,
                'reason': 'NOLs belong to previous activity, not transferable without business acquisition'
            },
            'state_tax_benefits': {
                'available': True if formation_state in ['wyoming', 'nevada', 'delaware'] else False,
                'description': 'Some states offer favorable tax treatment'
            }
        }

        # Risks and warnings
        risks = [
            'Banks and lenders scrutinize shelf companies',
            'Credit card companies may deny applications',
            'Using for fraudulent credit purposes is federal crime',
            'IRS scrutinizes shelf companies in tax audits',
            'Corporate veil may be pierced if misused',
            'Previous liabilities may exist (perform due diligence)',
            'Anti-money laundering regulations require beneficial owner disclosure',
            'FinCEN requires disclosure of beneficial owners (2024 Corporate Transparency Act)'
        ]

        # Compliance requirements
        compliance = {
            'due_diligence': 'REQUIRED - Review all prior filings and liabilities',
            'name_change': 'RECOMMENDED - Change DBA and business name',
            'new_ein': 'REQUIRED - Apply for new EIN',
            'state_reinstatement': 'Check if company in good standing',
            'registered_agent': 'Update to your registered agent',
            'beneficial_owner_report': 'FILE with FinCEN (2024 Corporate Transparency Act)',
            'bank_disclosure': 'Disclose shelf company status to banks'
        }

        # Cost-benefit analysis
        alternative_cost = 500  # Cost to form new company
        time_saved_weeks = 4
        value_of_time = time_saved_weeks * 500  # $500/week value

        is_worthwhile = (
            purchase_price < (alternative_cost + value_of_time) and
            use_analysis['legitimacy'] in ['HIGH', 'MEDIUM']
        )

        return {
            'shelf_company_details': {
                'purchase_price': purchase_price,
                'age_years': company_age_years,
                'has_credit_history': has_credit_history,
                'formation_state': formation_state,
                'state_benefits': self.FORMATION_STATES.get(formation_state, {})
            },
            'intended_use_analysis': use_analysis,
            'tax_benefits': tax_benefits,
            'risks': risks,
            'compliance_requirements': compliance,
            'cost_benefit': {
                'purchase_price': purchase_price,
                'alternative_new_entity_cost': alternative_cost,
                'time_saved_value': value_of_time,
                'net_benefit': value_of_time - (purchase_price - alternative_cost),
                'is_worthwhile': is_worthwhile
            },
            'recommendation': {
                'proceed': use_analysis['legitimacy'] == 'HIGH' and is_worthwhile,
                'risk_level': use_analysis['risk'],
                'advice': self._get_recommendation(use_analysis, is_worthwhile, intended_use)
            },
            'legitimate_alternatives': [
                'Form new entity in desired state ($200-$800)',
                'Use registered agent service for privacy ($100-$300/year)',
                'Build business credit organically (6-12 months)',
                'Joint venture with established company',
                'Get bonded/insured to meet contract requirements'
            ]
        }

    @staticmethod
    def _get_recommendation(use_analysis: Dict, is_worthwhile: bool, intended_use: str) -> str:
        """Generate recommendation text."""
        if use_analysis['legitimacy'] == 'ILLEGAL':
            return f'DO NOT PROCEED - {intended_use} is illegal and carries severe penalties.'

        if use_analysis['legitimacy'] == 'HIGH' and is_worthwhile:
            return 'May proceed with appropriate due diligence and legal compliance.'

        if use_analysis['legitimacy'] == 'MEDIUM':
            return 'Proceed with caution. Consult attorney and disclose to financial institutions.'

        if not is_worthwhile:
            return 'Not cost-effective. Consider forming new entity instead.'

        return 'Consult attorney before proceeding.'


class InternationalTaxPlanner:
    """
    International tax planning strategies (LEGAL implementations only).

    WARNING: Highly complex area. Requires international tax attorney.
    """

    TAX_TREATY_COUNTRIES = {
        'ireland': {
            'corporate_rate': 0.125,  # 12.5%
            'tax_treaty': 'Yes - Extensive US treaty',
            'withholding_on_dividends': 0.05,  # 5%
            'ip_benefits': 'Knowledge Development Box - 6.25% on IP',
            'substance_required': 'Yes - Employees, office, real activity',
            'best_for': 'Tech companies, IP holding'
        },
        'netherlands': {
            'corporate_rate': 0.256,  # 25.6%
            'tax_treaty': 'Yes',
            'withholding_on_dividends': 0.00,  # 0% with treaty
            'ip_benefits': 'Innovation Box - 9% on qualified IP',
            'substance_required': 'Yes - Real economic substance',
            'best_for': 'Holding companies, IP structures'
        },
        'singapore': {
            'corporate_rate': 0.17,  # 17%
            'tax_treaty': 'Yes',
            'withholding_on_dividends': 0.00,  # 0% on dividends
            'ip_benefits': 'IP regime with 5-10% rates',
            'substance_required': 'Yes - Directors, employees',
            'best_for': 'Asian operations, IP'
        },
        'puerto_rico': {
            'corporate_rate': 0.04,  # 4% under Act 60
            'tax_treaty': 'No treaty - US territory',
            'withholding_on_dividends': 0.00,  # 0% - US citizen treatment',
            'ip_benefits': 'Act 60 export services 4%',
            'substance_required': 'Yes - 183 days residency, office',
            'best_for': 'US citizens, service businesses, crypto'
        }
    }

    @staticmethod
    def analyze_international_structure(
        us_business_income: float,
        foreign_operations_income: float,
        has_real_foreign_operations: bool,
        employees_abroad: int,
        target_country: str = 'ireland'
    ) -> Dict[str, Any]:
        """
        Analyze international tax planning structure for LEGAL implementation.

        Critical: Must have REAL economic substance, not just tax benefits.

        Args:
            us_business_income: Income from US operations
            foreign_operations_income: Income from genuine foreign operations
            has_real_foreign_operations: Real business activity abroad?
            employees_abroad: Number of foreign employees
            target_country: Target foreign jurisdiction

        Returns:
            International structure analysis
        """
        country_data = InternationalTaxPlanner.TAX_TREATY_COUNTRIES.get(target_country, {})

        # Substance requirements analysis
        has_substance = (
            has_real_foreign_operations and
            employees_abroad >= 2 and
            foreign_operations_income > 0
        )

        if not has_substance:
            return {
                'recommendation': 'DO NOT PROCEED',
                'reason': 'Lacks economic substance. IRS will disregard structure (Gregory v. Helvering doctrine)',
                'alternatives': [
                    'Grow US business first',
                    'Establish real foreign operations before seeking tax benefits',
                    'Use domestic tax strategies instead'
                ]
            }

        # Calculate tax savings (simplified)
        us_corp_rate = 0.21
        foreign_rate = country_data.get('corporate_rate', 0.21)

        # Only foreign-source income can benefit
        us_tax_on_foreign_income = foreign_operations_income * us_corp_rate
        foreign_tax_on_foreign_income = foreign_operations_income * foreign_rate

        # Foreign Tax Credit
        ftc = foreign_tax_on_foreign_income
        net_us_tax = max(0, us_tax_on_foreign_income - ftc)

        annual_tax_savings = us_tax_on_foreign_income - (foreign_tax_on_foreign_income + net_us_tax)

        # GILTI (Global Intangible Low-Taxed Income) calculation
        gilti_exemption = foreign_operations_income * 0.10  # 10% deemed return on tangible assets
        gilti_income = max(0, foreign_operations_income - gilti_exemption)
        gilti_tax = gilti_income * 0.1050  # 10.5% effective rate

        # Setup and compliance costs
        annual_costs = {
            'foreign_entity_formation': 5000 / 5,  # Amortized over 5 years
            'foreign_accounting': 15000,
            'us_international_tax_compliance': 25000,
            'transfer_pricing_study': 20000,
            'legal_fees': 15000,
            'total': 80000
        }

        net_benefit = annual_tax_savings - annual_costs['total']

        return {
            'target_jurisdiction': target_country,
            'jurisdiction_profile': country_data,
            'substance_analysis': {
                'has_economic_substance': has_substance,
                'real_foreign_operations': has_real_foreign_operations,
                'employees_abroad': employees_abroad,
                'meets_requirements': has_substance
            },
            'income_analysis': {
                'us_source_income': us_business_income,
                'foreign_source_income': foreign_operations_income,
                'total_income': us_business_income + foreign_operations_income
            },
            'tax_analysis': {
                'us_tax_without_structure': us_tax_on_foreign_income,
                'foreign_tax': foreign_tax_on_foreign_income,
                'foreign_tax_credit': ftc,
                'net_us_tax_after_ftc': net_us_tax,
                'gilti_tax': gilti_tax,
                'annual_tax_savings': annual_tax_savings
            },
            'compliance_costs': annual_costs,
            'net_annual_benefit': net_benefit,
            'years_to_breakeven': abs(50000 / net_benefit) if net_benefit != 0 else float('inf'),
            'compliance_requirements': {
                'form_5471': 'Information Return of US Persons With Respect to Certain Foreign Corporations',
                'form_8992': 'GILTI computation',
                'form_1118': 'Foreign Tax Credit',
                'form_8938': 'FATCA reporting of foreign assets',
                'fbar': 'FinCEN Form 114 if foreign account >$10K',
                'transfer_pricing_docs': 'Arm\'s length pricing documentation',
                'economic_substance': 'Maintain real business operations'
            },
            'irs_scrutiny_factors': [
                'Check-the-box elections',
                'Transfer pricing',
                'GILTI calculations',
                'Subpart F income',
                'Earnings stripping',
                'Base erosion and anti-abuse tax (BEAT)'
            ],
            'recommendation': {
                'proceed': has_substance and net_benefit > 100000,
                'reason': 'Economically viable with proper substance' if net_benefit > 100000
                         else 'Compliance costs exceed tax savings',
                'min_revenue_threshold': 2_000_000,
                'actual_revenue': foreign_operations_income
            },
            'warnings': [
                'Requires real economic substance - not just a mailbox company',
                'IRS challenges foreign structures without legitimate business purpose',
                'Transfer pricing must be arm\'s length',
                'GILTI may tax low-taxed foreign income',
                'Repatriation to US triggers additional tax',
                'Constant regulatory changes require ongoing compliance',
                'Foreign tax authorities may also scrutinize structure'
            ]
        }
