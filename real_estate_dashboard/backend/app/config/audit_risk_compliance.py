"""
IRS Audit Risk Assessment and Compliance Tools

Tools to assess audit risk and ensure tax compliance.
"""

from typing import Dict, List, Any
from datetime import datetime, date
from decimal import Decimal


# ============================================================================
# IRS AUDIT RISK ASSESSMENT
# ============================================================================

class AuditRiskAssessment:
    """Assess IRS audit risk based on tax return characteristics"""

    @staticmethod
    def assess_risk(
        income: Decimal,
        business_type: str,
        deductions: Dict[str, Decimal],
        filing_status: str,
        has_schedule_c: bool = False,
        has_rental_properties: int = 0,
        claims_reps: bool = False,
        has_foreign_accounts: bool = False,
        large_charitable: Decimal = Decimal('0'),
        home_office: bool = False,
        large_losses: Decimal = Decimal('0')
    ) -> Dict[str, Any]:
        """
        Calculate audit risk score and provide recommendations

        Returns:
            Dictionary with risk score, risk level, red flags, and recommendations
        """
        risk_score = 0
        red_flags = []
        warnings = []
        recommendations = []

        # Base audit rates by income (IRS statistics)
        if income < Decimal('25000'):
            base_rate = 0.4
        elif income < Decimal('50000'):
            base_rate = 0.5
        elif income < Decimal('75000'):
            base_rate = 0.6
        elif income < Decimal('100000'):
            base_rate = 0.7
        elif income < Decimal('200000'):
            base_rate = 1.0
        elif income < Decimal('500000'):
            base_rate = 2.0
        elif income < Decimal('1000000'):
            base_rate = 3.0
        elif income < Decimal('5000000'):
            base_rate = 5.0
        else:
            base_rate = 10.0  # High earners ($5M+) have highest audit rates

        risk_score += base_rate

        # Schedule C (Self-Employment) - Higher audit risk
        if has_schedule_c:
            risk_score += 3.0
            warnings.append("Schedule C businesses have 3x higher audit rates")

            # Specific Schedule C red flags
            if business_type in ['cash_intensive']:
                risk_score += 5.0
                red_flags.append("Cash-intensive business (restaurants, bars, car washes) - high audit risk")

            # Round numbers suspicious
            total_deductions = sum(deductions.values())
            if total_deductions > 0 and total_deductions % 1000 == 0:
                risk_score += 2.0
                red_flags.append("Round number deductions appear estimated rather than actual")
                recommendations.append("Use actual amounts, not rounded estimates")

            # Losses on Schedule C
            if large_losses > Decimal('0'):
                risk_score += 4.0
                red_flags.append(f"Schedule C loss of ${large_losses:,.2f} may trigger audit")
                recommendations.append("Ensure business is profit-motivated, not a hobby")

            # Excessive deductions relative to income
            if business_type == 'consulting' and total_deductions > income * Decimal('0.8'):
                risk_score += 3.0
                red_flags.append("Deductions exceed 80% of income - verify all are legitimate")

        # Real Estate Professional Status (REPS) - Medium-high audit risk
        if claims_reps:
            risk_score += 4.0
            red_flags.append("REPS claim triggers IRS scrutiny - ensure detailed time logs")
            recommendations.append("Maintain contemporaneous time tracking logs (750+ hours)")
            recommendations.append("Document all real estate activities: repairs, tenant meetings, property search")
            recommendations.append("Keep evidence of material participation in each rental property")

        # Rental properties
        if has_rental_properties > 0:
            risk_score += has_rental_properties * 0.5

            if has_rental_properties > 5:
                risk_score += 2.0
                warnings.append(f"Multiple rental properties ({has_rental_properties}) increases complexity")

        # Home office deduction
        if home_office:
            risk_score += 2.0
            warnings.append("Home office deduction frequently audited")
            recommendations.append("Ensure office is used regularly and exclusively for business")
            recommendations.append("Take photos of dedicated office space")
            recommendations.append("Calculate square footage accurately")

        # Foreign accounts
        if has_foreign_accounts:
            risk_score += 3.0
            red_flags.append("Foreign accounts require FBAR filing")
            recommendations.append("File FinCEN Form 114 (FBAR) if total balance > $10,000")
            recommendations.append("Report foreign income on Form 8938 if required")
            warnings.append("Failure to report foreign accounts carries severe penalties")

        # Large charitable contributions
        if large_charitable > Decimal('0'):
            # Suspicious if > 30% of income
            if large_charitable > income * Decimal('0.3'):
                risk_score += 3.0
                red_flags.append(f"Charitable contributions (${large_charitable:,.2f}) exceed 30% of income")
                recommendations.append("Obtain written acknowledgment for donations > $250")
                recommendations.append("Get qualified appraisal for property donations > $5,000")

        # Analyze specific deductions for red flags
        if 'meals_entertainment' in deductions:
            meals = deductions['meals_entertainment']
            # 50% limitation - verify compliance
            if meals > income * Decimal('0.1'):
                risk_score += 2.0
                warnings.append("High meals & entertainment deductions")
                recommendations.append("Keep detailed records: date, business purpose, attendees")

        if 'travel' in deductions:
            travel = deductions['travel']
            if travel > income * Decimal('0.15'):
                risk_score += 2.0
                warnings.append("High travel deductions relative to income")
                recommendations.append("Document business purpose of all trips")

        if 'vehicle' in deductions:
            vehicle = deductions['vehicle']
            if vehicle > Decimal('15000'):
                risk_score += 1.5
                warnings.append("High vehicle deductions")
                recommendations.append("Maintain mileage log with business purpose for each trip")

        # Determine risk level
        if risk_score < 5:
            risk_level = "LOW"
            risk_description = "Low audit risk - typical return"
        elif risk_score < 10:
            risk_level = "MODERATE"
            risk_description = "Moderate risk - some red flags present"
        elif risk_score < 15:
            risk_level = "HIGH"
            risk_description = "High risk - multiple audit triggers"
        else:
            risk_level = "VERY HIGH"
            risk_description = "Very high risk - expect possible audit"

        # General recommendations
        recommendations.extend([
            "Keep all receipts and documentation for 7 years",
            "Never round numbers - use actual amounts",
            "Document business purpose for all deductions",
            "Consider professional tax preparation",
            "File on time even if you can't pay",
            "Respond promptly to any IRS correspondence"
        ])

        return {
            'risk_score': float(risk_score),
            'risk_level': risk_level,
            'risk_description': risk_description,
            'audit_probability': min(risk_score, 25.0),  # Cap at 25%
            'red_flags': red_flags,
            'warnings': warnings,
            'recommendations': recommendations,
            'base_rate': base_rate,
            'income_level': str(income),
            'filing_status': filing_status
        }


# ============================================================================
# COMPLIANCE CALENDAR
# ============================================================================

class ComplianceCalendar:
    """Generate compliance calendar with all tax deadlines"""

    @staticmethod
    def get_annual_calendar(year: int = 2025) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all tax deadlines and compliance tasks for a year

        Args:
            year: Tax year

        Returns:
            Dictionary organized by month with all deadlines
        """
        calendar = {}

        # January
        calendar['january'] = [
            {
                'date': f'{year}-01-15',
                'task': 'Q4 Estimated Tax Payment (Prior Year)',
                'form': 'Form 1040-ES',
                'who': 'Self-employed, rental income',
                'penalty_for_missing': 'Underpayment penalty',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-01-31',
                'task': 'Issue W-2s to Employees',
                'form': 'Form W-2',
                'who': 'Employers',
                'penalty_for_missing': '$50-$280 per form',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-01-31',
                'task': 'Issue 1099-NEC for Contractor Payments',
                'form': 'Form 1099-NEC',
                'who': 'Businesses that paid contractors $600+',
                'penalty_for_missing': '$50-$280 per form',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-01-31',
                'task': 'Issue 1099-MISC, 1099-INT, 1099-DIV',
                'form': 'Various 1099 forms',
                'who': 'Businesses, banks, brokerages',
                'penalty_for_missing': '$50-$280 per form',
                'priority': 'HIGH'
            }
        ]

        # February
        calendar['february'] = [
            {
                'date': f'{year}-02-28',
                'task': 'File W-2s with SSA',
                'form': 'Form W-2 + W-3',
                'who': 'Employers',
                'penalty_for_missing': '$50-$280 per form',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-02-28',
                'task': 'File 1099s with IRS',
                'form': '1099-NEC, 1099-MISC, etc.',
                'who': 'Businesses',
                'penalty_for_missing': '$50-$280 per form',
                'priority': 'HIGH'
            }
        ]

        # March
        calendar['march'] = [
            {
                'date': f'{year}-03-15',
                'task': 'S-Corporation Tax Return Due',
                'form': 'Form 1120-S',
                'who': 'S-Corporations',
                'penalty_for_missing': '$220/month per shareholder',
                'priority': 'HIGH',
                'note': 'Can extend to September 15 with Form 7004'
            },
            {
                'date': f'{year}-03-15',
                'task': 'Partnership Tax Return Due',
                'form': 'Form 1065',
                'who': 'Partnerships, Multi-member LLCs',
                'penalty_for_missing': '$220/month per partner',
                'priority': 'HIGH',
                'note': 'Can extend to September 15 with Form 7004'
            }
        ]

        # April
        calendar['april'] = [
            {
                'date': f'{year}-04-15',
                'task': 'Individual Income Tax Return Due',
                'form': 'Form 1040',
                'who': 'All individual taxpayers',
                'penalty_for_missing': '5% per month up to 25% of tax owed',
                'priority': 'CRITICAL',
                'note': 'Can extend to October 15 with Form 4868'
            },
            {
                'date': f'{year}-04-15',
                'task': 'Q1 Estimated Tax Payment',
                'form': 'Form 1040-ES',
                'who': 'Self-employed, rental income',
                'penalty_for_missing': 'Underpayment penalty',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-04-15',
                'task': 'Prior Year IRA Contribution Deadline',
                'form': 'N/A',
                'who': 'Anyone eligible for IRA',
                'penalty_for_missing': 'Miss tax deduction',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-04-15',
                'task': 'Prior Year HSA Contribution Deadline',
                'form': 'N/A',
                'who': 'HDHP participants',
                'penalty_for_missing': 'Miss tax deduction',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-04-15',
                'task': 'C-Corporation Tax Return Due',
                'form': 'Form 1120',
                'who': 'C-Corporations',
                'penalty_for_missing': '5% per month up to 25%',
                'priority': 'HIGH',
                'note': 'Can extend to October 15 with Form 7004'
            },
            {
                'date': f'{year}-04-30',
                'task': 'Form 941 - Q1 Payroll Taxes',
                'form': 'Form 941',
                'who': 'Employers',
                'penalty_for_missing': '5% per month',
                'priority': 'HIGH'
            }
        ]

        # May
        calendar['may'] = [
            {
                'date': f'{year}-05-15',
                'task': 'Non-profit Tax Return Due (Calendar Year)',
                'form': 'Form 990, 990-EZ, 990-N',
                'who': 'Non-profit organizations',
                'penalty_for_missing': '$20-$100/day, up to $50,000',
                'priority': 'HIGH'
            }
        ]

        # June
        calendar['june'] = [
            {
                'date': f'{year}-06-15',
                'task': 'Q2 Estimated Tax Payment',
                'form': 'Form 1040-ES',
                'who': 'Self-employed, rental income',
                'penalty_for_missing': 'Underpayment penalty',
                'priority': 'HIGH'
            }
        ]

        # July
        calendar['july'] = [
            {
                'date': f'{year}-07-31',
                'task': 'Form 941 - Q2 Payroll Taxes',
                'form': 'Form 941',
                'who': 'Employers',
                'penalty_for_missing': '5% per month',
                'priority': 'HIGH'
            }
        ]

        # September
        calendar['september'] = [
            {
                'date': f'{year}-09-15',
                'task': 'Q3 Estimated Tax Payment',
                'form': 'Form 1040-ES',
                'who': 'Self-employed, rental income',
                'penalty_for_missing': 'Underpayment penalty',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-09-15',
                'task': 'Extended S-Corp & Partnership Returns Due',
                'form': 'Form 1120-S, Form 1065',
                'who': 'S-Corps, Partnerships (if extended)',
                'penalty_for_missing': '$220/month per owner',
                'priority': 'HIGH'
            }
        ]

        # October
        calendar['october'] = [
            {
                'date': f'{year}-10-15',
                'task': 'Extended Individual Tax Returns Due',
                'form': 'Form 1040',
                'who': 'Individuals (if extended)',
                'penalty_for_missing': '5% per month up to 25%',
                'priority': 'CRITICAL'
            },
            {
                'date': f'{year}-10-15',
                'task': 'Extended C-Corp Returns Due',
                'form': 'Form 1120',
                'who': 'C-Corporations (if extended)',
                'penalty_for_missing': '5% per month up to 25%',
                'priority': 'HIGH'
            },
            {
                'date': f'{year}-10-31',
                'task': 'Form 941 - Q3 Payroll Taxes',
                'form': 'Form 941',
                'who': 'Employers',
                'penalty_for_missing': '5% per month',
                'priority': 'HIGH'
            }
        ]

        # December
        calendar['december'] = [
            {
                'date': f'{year}-12-31',
                'task': 'Max Out 401(k) Contributions',
                'form': 'N/A',
                'who': 'All employees',
                'penalty_for_missing': 'Miss tax deduction',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-12-31',
                'task': 'Place Equipment in Service (Section 179, Bonus Depreciation)',
                'form': 'N/A',
                'who': 'Business owners',
                'penalty_for_missing': 'Miss current year deduction',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-12-31',
                'task': 'Harvest Tax Losses',
                'form': 'N/A',
                'who': 'Investors',
                'penalty_for_missing': 'Miss tax savings opportunity',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-12-31',
                'task': 'Make Charitable Contributions',
                'form': 'N/A',
                'who': 'All taxpayers',
                'penalty_for_missing': 'Miss current year deduction',
                'priority': 'MEDIUM'
            },
            {
                'date': f'{year}-12-31',
                'task': 'Pay Q4 State Estimated Taxes (if itemizing)',
                'form': 'State forms vary',
                'who': 'Itemizers',
                'penalty_for_missing': 'Miss current year deduction',
                'priority': 'LOW'
            }
        ]

        return calendar

    @staticmethod
    def get_upcoming_deadlines(days_ahead: int = 90) -> List[Dict[str, Any]]:
        """Get upcoming deadlines for next N days"""
        today = date.today()
        year = today.year

        all_deadlines = []
        calendar = ComplianceCalendar.get_annual_calendar(year)

        for month, items in calendar.items():
            all_deadlines.extend(items)

        # Filter to upcoming deadlines
        upcoming = []
        for item in all_deadlines:
            deadline_date = datetime.strptime(item['date'], '%Y-%m-%d').date()

            days_until = (deadline_date - today).days

            if 0 <= days_until <= days_ahead:
                item['days_until'] = days_until
                item['status'] = 'URGENT' if days_until <= 7 else 'UPCOMING'
                upcoming.append(item)

        # Sort by date
        upcoming.sort(key=lambda x: x['date'])

        return upcoming


__all__ = [
    'AuditRiskAssessment',
    'ComplianceCalendar'
]
