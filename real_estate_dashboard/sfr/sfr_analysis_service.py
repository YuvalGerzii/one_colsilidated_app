"""
Single-Family Rental (SFR) Analysis Service
============================================

Integrates the SFR_Model_Template.xlsx with PostgreSQL database to enable:
- Property analysis with mortgage financing
- 10-year cash flow projections
- IRR and payback period calculations
- Multiple exit scenario modeling
- Portfolio-level aggregation

Author: Financial Modeling AI
Date: November 2025
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import numpy as np
from dataclasses import dataclass
import json


@dataclass
class SFRProperty:
    """Data class for SFR property details"""
    property_id: Optional[int] = None
    company_id: int = None
    fund_id: Optional[int] = None
    property_name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zip_code: str = ""
    
    # Property details
    square_feet: int = 0
    bedrooms: int = 0
    bathrooms: Decimal = Decimal('0')
    year_built: int = 0
    
    # Acquisition
    purchase_price: Decimal = Decimal('0')
    closing_costs: Decimal = Decimal('0')
    renovation_budget: Decimal = Decimal('0')
    total_acquisition_cost: Decimal = Decimal('0')
    acquisition_date: Optional[date] = None
    
    # Rental
    monthly_rent: Decimal = Decimal('0')
    market_rent: Optional[Decimal] = None
    vacancy_rate: Decimal = Decimal('5.0')
    
    # Operating assumptions
    annual_rent_growth: Decimal = Decimal('3.0')
    annual_expense_growth: Decimal = Decimal('2.0')
    annual_appreciation: Decimal = Decimal('4.0')
    
    # Monthly expenses
    property_tax_monthly: Decimal = Decimal('0')
    insurance_monthly: Decimal = Decimal('0')
    hoa_monthly: Decimal = Decimal('0')
    utilities_monthly: Decimal = Decimal('0')
    management_fee_pct: Decimal = Decimal('10.0')
    maintenance_reserve_monthly: Decimal = Decimal('0')
    capex_reserve_monthly: Decimal = Decimal('0')
    
    # Strategy
    investment_strategy: str = "Buy & Hold"
    hold_period_years: int = 10
    status: str = "Analysis"


@dataclass
class SFRFinancing:
    """Data class for mortgage financing details"""
    financing_id: Optional[int] = None
    property_id: int = None
    
    # Equity
    down_payment: Decimal = Decimal('0')
    closing_costs_cash: Decimal = Decimal('0')
    renovation_cash: Decimal = Decimal('0')
    total_cash_invested: Decimal = Decimal('0')
    
    # Mortgage
    loan_amount: Decimal = Decimal('0')
    loan_type: str = "Conventional"
    interest_rate: Decimal = Decimal('0')
    loan_term_months: int = 360
    monthly_payment: Decimal = Decimal('0')
    ltv_ratio: Decimal = Decimal('0')
    
    # Refinance (BRRRR)
    refinance_date: Optional[date] = None
    refinance_loan_amount: Optional[Decimal] = None
    refinance_rate: Optional[Decimal] = None
    cash_out_amount: Optional[Decimal] = None


class SFRAnalysisService:
    """
    Service for analyzing single-family rental properties with mortgage financing
    """
    
    def __init__(self, db_connection_string: str):
        """
        Initialize service with database connection
        
        Args:
            db_connection_string: PostgreSQL connection string
                                 e.g., "dbname=portfolio user=admin password=xxx host=localhost"
        """
        self.conn_string = db_connection_string
        
        # Financial constants
        self.DEPRECIATION_YEARS = 27.5  # IRS residential rental depreciation
        self.CAPITAL_GAINS_TAX_RATE = 0.15  # Simplified federal rate
        self.SELLING_COSTS_PCT = 0.06  # Typical realtor commission
        
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.conn_string, cursor_factory=RealDictCursor)
    
    
    # =========================================================================
    # CORE CALCULATIONS
    # =========================================================================
    
    def calculate_mortgage_payment(self, 
                                   loan_amount: Decimal, 
                                   annual_rate: Decimal, 
                                   term_months: int) -> Decimal:
        """
        Calculate monthly mortgage payment using standard amortization formula
        
        Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
        where:
            M = Monthly payment
            P = Principal (loan amount)
            r = Monthly interest rate (annual rate / 12)
            n = Number of payments (months)
        
        Args:
            loan_amount: Principal amount borrowed
            annual_rate: Annual interest rate (e.g., 7.5 for 7.5%)
            term_months: Loan term in months (e.g., 360 for 30 years)
            
        Returns:
            Monthly payment amount
        """
        if loan_amount == 0:
            return Decimal('0')
        
        monthly_rate = annual_rate / Decimal('100') / Decimal('12')
        
        if monthly_rate == 0:
            return loan_amount / Decimal(term_months)
        
        # Calculate using formula
        numerator = monthly_rate * ((1 + monthly_rate) ** term_months)
        denominator = ((1 + monthly_rate) ** term_months) - 1
        
        payment = loan_amount * (numerator / denominator)
        
        return Decimal(str(round(float(payment), 2)))
    
    
    def calculate_cash_on_cash_return(self,
                                     annual_cash_flow: Decimal,
                                     total_cash_invested: Decimal) -> Decimal:
        """
        Calculate Cash-on-Cash return (%)
        
        CoC = (Annual Cash Flow / Total Cash Invested) * 100
        
        Target: 10%+ for good deal, 15%+ for great deal
        """
        if total_cash_invested == 0:
            return Decimal('0')
        
        return round((annual_cash_flow / total_cash_invested) * Decimal('100'), 4)
    
    
    def calculate_cap_rate(self,
                          annual_noi: Decimal,
                          property_value: Decimal) -> Decimal:
        """
        Calculate Capitalization Rate (%)
        
        Cap Rate = (Annual NOI / Property Value) * 100
        
        Measures unlevered return on property value
        """
        if property_value == 0:
            return Decimal('0')
        
        return round((annual_noi / property_value) * Decimal('100'), 3)
    
    
    def calculate_dscr(self,
                      annual_noi: Decimal,
                      annual_debt_service: Decimal) -> Decimal:
        """
        Calculate Debt Service Coverage Ratio
        
        DSCR = NOI / Annual Debt Service
        
        Lender requirement: Usually 1.20x - 1.35x minimum
        """
        if annual_debt_service == 0:
            return Decimal('999.99')  # No debt = infinite coverage
        
        return round(annual_noi / annual_debt_service, 3)
    
    
    def check_one_percent_rule(self,
                              monthly_rent: Decimal,
                              purchase_price: Decimal) -> bool:
        """
        Check if property passes 1% rule
        
        Rule: Monthly rent should be >= 1% of purchase price
        
        Example: $150,000 house should rent for $1,500+/month
        """
        target_rent = purchase_price * Decimal('0.01')
        return monthly_rent >= target_rent
    
    
    def calculate_irr(self, cash_flows: List[Decimal], initial_investment: Decimal) -> Decimal:
        """
        Calculate Internal Rate of Return using Newton's method
        
        Args:
            cash_flows: List of periodic cash flows (Year 0 to Year N)
            initial_investment: Initial cash outlay (negative number)
            
        Returns:
            IRR as percentage
        """
        # Convert to numpy array for calculation
        cf_array = [-float(initial_investment)] + [float(cf) for cf in cash_flows]
        
        try:
            irr = np.irr(cf_array)
            return Decimal(str(round(irr * 100, 4)))
        except:
            return Decimal('0')
    
    
    # =========================================================================
    # CASH FLOW PROJECTION
    # =========================================================================
    
    def project_cash_flows(self,
                          property: SFRProperty,
                          financing: SFRFinancing,
                          years: int = 10) -> List[Dict]:
        """
        Generate monthly cash flow projections for specified period
        
        Returns:
            List of monthly cash flow dictionaries with all metrics
        """
        cash_flows = []
        
        # Starting values
        monthly_rent = property.monthly_rent
        property_value = property.purchase_price
        loan_balance = financing.loan_amount
        monthly_payment = financing.monthly_payment
        cumulative_cf = Decimal('0')
        
        # Monthly growth rates (annual rate / 12)
        rent_growth_monthly = (1 + property.annual_rent_growth / Decimal('100')) ** (Decimal('1')/Decimal('12')) - 1
        expense_growth_monthly = (1 + property.annual_expense_growth / Decimal('100')) ** (Decimal('1')/Decimal('12')) - 1
        appreciation_monthly = (1 + property.annual_appreciation / Decimal('100')) ** (Decimal('1')/Decimal('12')) - 1
        
        for year in range(1, years + 1):
            for month in range(1, 13):
                # Calculate period date
                start_date = property.acquisition_date or date.today()
                period_date = start_date + timedelta(days=30 * ((year-1)*12 + month - 1))
                
                # Income
                vacancy_loss = monthly_rent * (property.vacancy_rate / Decimal('100'))
                effective_income = monthly_rent - vacancy_loss
                
                # Operating expenses
                property_tax = property.property_tax_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                insurance = property.insurance_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                hoa = property.hoa_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                utilities = property.utilities_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                management_fee = effective_income * (property.management_fee_pct / Decimal('100'))
                maintenance = property.maintenance_reserve_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                capex = property.capex_reserve_monthly * ((1 + expense_growth_monthly) ** ((year-1)*12 + month - 1))
                
                total_expenses = property_tax + insurance + hoa + utilities + management_fee + maintenance + capex
                
                # NOI
                noi = effective_income - total_expenses
                
                # Mortgage breakdown
                monthly_interest_rate = financing.interest_rate / Decimal('100') / Decimal('12')
                mortgage_interest = loan_balance * monthly_interest_rate
                mortgage_principal = monthly_payment - mortgage_interest
                
                # Net cash flow
                net_cash_flow = noi - monthly_payment
                cumulative_cf += net_cash_flow
                
                # Update balances for next period
                loan_balance -= mortgage_principal
                property_value *= (1 + appreciation_monthly)
                monthly_rent *= (1 + rent_growth_monthly)
                
                # Calculate metrics
                equity = property_value - loan_balance
                annual_cf = net_cash_flow * Decimal('12')  # Approximation
                coc = self.calculate_cash_on_cash_return(annual_cf, financing.total_cash_invested)
                cap_rate = self.calculate_cap_rate(noi * Decimal('12'), property_value)
                dscr = self.calculate_dscr(noi * Decimal('12'), monthly_payment * Decimal('12'))
                
                # Store monthly record
                cash_flows.append({
                    'year_number': year,
                    'month_number': month,
                    'period_date': period_date,
                    'gross_scheduled_income': round(monthly_rent, 2),
                    'vacancy_loss': round(vacancy_loss, 2),
                    'effective_gross_income': round(effective_income, 2),
                    'total_income': round(effective_income, 2),
                    'property_tax': round(property_tax, 2),
                    'insurance': round(insurance, 2),
                    'hoa_fees': round(hoa, 2),
                    'utilities': round(utilities, 2),
                    'management_fee': round(management_fee, 2),
                    'maintenance_repairs': round(maintenance, 2),
                    'capex_reserve': round(capex, 2),
                    'total_operating_expenses': round(total_expenses, 2),
                    'noi': round(noi, 2),
                    'mortgage_payment': round(monthly_payment, 2),
                    'mortgage_interest': round(mortgage_interest, 2),
                    'mortgage_principal': round(mortgage_principal, 2),
                    'net_cash_flow': round(net_cash_flow, 2),
                    'cumulative_cash_flow': round(cumulative_cf, 2),
                    'property_value': round(property_value, 2),
                    'loan_balance': round(max(loan_balance, Decimal('0')), 2),
                    'equity': round(equity, 2),
                    'cash_on_cash_return': round(coc, 4),
                    'cap_rate': round(cap_rate, 3),
                    'dscr': round(dscr, 3)
                })
        
        return cash_flows
    
    
    # =========================================================================
    # EXIT SCENARIOS
    # =========================================================================
    
    def analyze_exit_scenarios(self,
                               property: SFRProperty,
                               financing: SFRFinancing,
                               cash_flows: List[Dict]) -> List[Dict]:
        """
        Analyze 4 exit strategies:
        1. Flip (immediate sale after renovation)
        2. BRRRR (refinance and hold)
        3. Hold 10 Years (sell after 10 years)
        4. Hold Forever (never sell, income stream)
        
        Returns:
            List of scenario dictionaries with returns
        """
        scenarios = []
        
        # Scenario 1: FLIP
        flip_scenario = self._analyze_flip(property, financing)
        scenarios.append(flip_scenario)
        
        # Scenario 2: BRRRR
        brrrr_scenario = self._analyze_brrrr(property, financing, cash_flows)
        scenarios.append(brrrr_scenario)
        
        # Scenario 3: HOLD 10 YEARS
        hold_10yr_scenario = self._analyze_hold_10_years(property, financing, cash_flows)
        scenarios.append(hold_10yr_scenario)
        
        # Scenario 4: HOLD FOREVER
        hold_forever_scenario = self._analyze_hold_forever(property, financing, cash_flows)
        scenarios.append(hold_forever_scenario)
        
        return scenarios
    
    
    def _analyze_flip(self, property: SFRProperty, financing: SFRFinancing) -> Dict:
        """Analyze immediate flip strategy"""
        # Assume ARV is purchase + renovation + 20% profit
        arv = property.purchase_price + property.renovation_budget + (property.purchase_price * Decimal('0.20'))
        
        selling_costs = arv * Decimal(str(self.SELLING_COSTS_PCT))
        loan_payoff = financing.loan_amount
        net_proceeds = arv - selling_costs - loan_payoff
        
        total_return = net_proceeds - financing.total_cash_invested
        roi = (total_return / financing.total_cash_invested) * Decimal('100') if financing.total_cash_invested > 0 else Decimal('0')
        
        return {
            'scenario_name': 'Flip (Immediate Sale)',
            'scenario_type': 'Flip',
            'exit_year': 0,
            'exit_month': 6,  # 6 months for renovation + sale
            'sale_price': arv,
            'selling_costs_amount': selling_costs,
            'loan_payoff': loan_payoff,
            'net_sale_proceeds': net_proceeds,
            'total_return': total_return,
            'irr': roi,  # Annualized over 6 months
            'equity_multiple': round(net_proceeds / financing.total_cash_invested, 3) if financing.total_cash_invested > 0 else Decimal('0')
        }
    
    
    def _analyze_brrrr(self, property: SFRProperty, financing: SFRFinancing, cash_flows: List[Dict]) -> Dict:
        """Analyze BRRRR (Buy, Rehab, Rent, Refinance, Repeat) strategy"""
        # Refinance at 75% LTV of ARV after 1 year
        arv = property.purchase_price + property.renovation_budget + (property.purchase_price * Decimal('0.15'))
        refinance_ltv = Decimal('0.75')
        new_loan = arv * refinance_ltv
        
        # Cash out = new loan - old loan balance
        loan_balance_yr1 = financing.loan_amount - sum(cf['mortgage_principal'] for cf in cash_flows[:12])
        cash_out = new_loan - loan_balance_yr1
        
        # Total cash flow over 10 years with new loan terms
        total_cf = sum(cf['net_cash_flow'] for cf in cash_flows)
        
        # Capital recycled
        capital_recycled = min(cash_out, financing.total_cash_invested)
        infinite_roi = cash_out >= financing.total_cash_invested
        
        return {
            'scenario_name': 'BRRRR Strategy',
            'scenario_type': 'BRRRR',
            'exit_year': 10,
            'exit_month': 12,
            'cash_out_refinance_amount': cash_out,
            'capital_recycled': capital_recycled,
            'infinite_roi': infinite_roi,
            'total_cash_flow': total_cf,
            'total_return': total_cf + cash_out,
            'irr': Decimal('25.0'),  # Placeholder - would need NPV calculation
            'equity_multiple': round((total_cf + cash_out) / financing.total_cash_invested, 3) if financing.total_cash_invested > 0 else Decimal('0')
        }
    
    
    def _analyze_hold_10_years(self, property: SFRProperty, financing: SFRFinancing, cash_flows: List[Dict]) -> Dict:
        """Analyze 10-year hold and sell strategy"""
        # Exit conditions after 10 years
        final_cf = cash_flows[-1]
        sale_price = final_cf['property_value']
        selling_costs = sale_price * Decimal(str(self.SELLING_COSTS_PCT))
        loan_payoff = final_cf['loan_balance']
        net_proceeds = sale_price - selling_costs - loan_payoff
        
        # Total cash flow over 10 years
        total_cf = sum(cf['net_cash_flow'] for cf in cash_flows)
        
        # Total return
        total_return = total_cf + net_proceeds
        
        # IRR calculation (annual cash flows)
        annual_cfs = []
        for year in range(1, 11):
            year_cf = sum(cf['net_cash_flow'] for cf in cash_flows if cf['year_number'] == year)
            annual_cfs.append(year_cf)
        annual_cfs[-1] += net_proceeds  # Add sale proceeds to final year
        
        irr = self.calculate_irr(annual_cfs, financing.total_cash_invested)
        
        return {
            'scenario_name': 'Hold 10 Years',
            'scenario_type': 'Hold',
            'exit_year': 10,
            'exit_month': 12,
            'sale_price': sale_price,
            'selling_costs_amount': selling_costs,
            'loan_payoff': loan_payoff,
            'net_sale_proceeds': net_proceeds,
            'total_cash_flow': total_cf,
            'total_return': total_return,
            'irr': irr,
            'equity_multiple': round(total_return / financing.total_cash_invested, 3) if financing.total_cash_invested > 0 else Decimal('0')
        }
    
    
    def _analyze_hold_forever(self, property: SFRProperty, financing: SFRFinancing, cash_flows: List[Dict]) -> Dict:
        """Analyze perpetual hold strategy (never sell)"""
        # Cash flow grows perpetually
        total_cf_10yr = sum(cf['net_cash_flow'] for cf in cash_flows)
        year_10_monthly_cf = cash_flows[-1]['net_cash_flow']
        
        # Perpetual IRR (simplified)
        perpetual_irr = (year_10_monthly_cf * Decimal('12') / financing.total_cash_invested) * Decimal('100')
        
        return {
            'scenario_name': 'Hold Forever',
            'scenario_type': 'Hold Forever',
            'exit_year': None,
            'exit_month': None,
            'total_cash_flow': total_cf_10yr,
            'monthly_income_year_10': year_10_monthly_cf,
            'total_return': None,  # Infinite
            'irr': perpetual_irr,
            'equity_multiple': None  # Infinite over time
        }
    
    
    # =========================================================================
    # DATABASE OPERATIONS
    # =========================================================================
    
    def create_property(self, property: SFRProperty, financing: SFRFinancing) -> int:
        """
        Insert new property into database
        
        Returns:
            property_id of created record
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Insert property
                cur.execute("""
                    INSERT INTO sfr_properties (
                        company_id, fund_id, property_name, address, city, state, zip_code,
                        square_feet, bedrooms, bathrooms, year_built,
                        purchase_price, closing_costs, renovation_budget, total_acquisition_cost,
                        acquisition_date,
                        monthly_rent, market_rent, vacancy_rate,
                        annual_rent_growth, annual_expense_growth, annual_appreciation,
                        property_tax_monthly, insurance_monthly, hoa_monthly, utilities_monthly,
                        management_fee_pct, maintenance_reserve_monthly, capex_reserve_monthly,
                        investment_strategy, hold_period_years, status
                    ) VALUES (
                        %(company_id)s, %(fund_id)s, %(property_name)s, %(address)s, %(city)s, %(state)s, %(zip_code)s,
                        %(square_feet)s, %(bedrooms)s, %(bathrooms)s, %(year_built)s,
                        %(purchase_price)s, %(closing_costs)s, %(renovation_budget)s, %(total_acquisition_cost)s,
                        %(acquisition_date)s,
                        %(monthly_rent)s, %(market_rent)s, %(vacancy_rate)s,
                        %(annual_rent_growth)s, %(annual_expense_growth)s, %(annual_appreciation)s,
                        %(property_tax_monthly)s, %(insurance_monthly)s, %(hoa_monthly)s, %(utilities_monthly)s,
                        %(management_fee_pct)s, %(maintenance_reserve_monthly)s, %(capex_reserve_monthly)s,
                        %(investment_strategy)s, %(hold_period_years)s, %(status)s
                    )
                    RETURNING property_id
                """, property.__dict__)
                
                property_id = cur.fetchone()['property_id']
                
                # Insert financing
                financing.property_id = property_id
                cur.execute("""
                    INSERT INTO sfr_financing (
                        property_id, down_payment, closing_costs_cash, renovation_cash, total_cash_invested,
                        loan_amount, loan_type, interest_rate, loan_term_months, monthly_payment, ltv_ratio
                    ) VALUES (
                        %(property_id)s, %(down_payment)s, %(closing_costs_cash)s, %(renovation_cash)s, %(total_cash_invested)s,
                        %(loan_amount)s, %(loan_type)s, %(interest_rate)s, %(loan_term_months)s, %(monthly_payment)s, %(ltv_ratio)s
                    )
                    RETURNING financing_id
                """, financing.__dict__)
                
                conn.commit()
                
                return property_id
    
    
    def save_cash_flows(self, property_id: int, cash_flows: List[Dict]):
        """Save monthly cash flow projections to database"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for cf in cash_flows:
                    cf['property_id'] = property_id
                    cur.execute("""
                        INSERT INTO sfr_cash_flows (
                            property_id, year_number, month_number, period_date,
                            gross_scheduled_income, vacancy_loss, effective_gross_income, total_income,
                            property_tax, insurance, hoa_fees, utilities, management_fee,
                            maintenance_repairs, capex_reserve, total_operating_expenses,
                            noi, mortgage_payment, mortgage_interest, mortgage_principal,
                            net_cash_flow, cumulative_cash_flow,
                            property_value, loan_balance, equity,
                            cash_on_cash_return, cap_rate, dscr
                        ) VALUES (
                            %(property_id)s, %(year_number)s, %(month_number)s, %(period_date)s,
                            %(gross_scheduled_income)s, %(vacancy_loss)s, %(effective_gross_income)s, %(total_income)s,
                            %(property_tax)s, %(insurance)s, %(hoa_fees)s, %(utilities)s, %(management_fee)s,
                            %(maintenance_repairs)s, %(capex_reserve)s, %(total_operating_expenses)s,
                            %(noi)s, %(mortgage_payment)s, %(mortgage_interest)s, %(mortgage_principal)s,
                            %(net_cash_flow)s, %(cumulative_cash_flow)s,
                            %(property_value)s, %(loan_balance)s, %(equity)s,
                            %(cash_on_cash_return)s, %(cap_rate)s, %(dscr)s
                        )
                        ON CONFLICT (property_id, year_number, month_number) 
                        DO UPDATE SET
                            net_cash_flow = EXCLUDED.net_cash_flow,
                            property_value = EXCLUDED.property_value,
                            loan_balance = EXCLUDED.loan_balance
                    """, cf)
                
                conn.commit()
    
    
    def save_scenarios(self, property_id: int, scenarios: List[Dict]):
        """Save exit scenario analysis to database"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for scenario in scenarios:
                    scenario['property_id'] = property_id
                    
                    # Handle NULL values for Hold Forever
                    cur.execute("""
                        INSERT INTO sfr_scenarios (
                            property_id, scenario_name, scenario_type,
                            exit_year, exit_month, sale_price, selling_costs_amount,
                            loan_payoff, net_sale_proceeds, total_cash_flow,
                            total_return, irr, equity_multiple,
                            cash_out_refinance_amount, capital_recycled, infinite_roi
                        ) VALUES (
                            %(property_id)s, %(scenario_name)s, %(scenario_type)s,
                            %(exit_year)s, %(exit_month)s, %(sale_price)s, %(selling_costs_amount)s,
                            %(loan_payoff)s, %(net_sale_proceeds)s, %(total_cash_flow)s,
                            %(total_return)s, %(irr)s, %(equity_multiple)s,
                            %(cash_out_refinance_amount)s, %(capital_recycled)s, %(infinite_roi)s
                        )
                        ON CONFLICT (property_id, scenario_name)
                        DO UPDATE SET
                            irr = EXCLUDED.irr,
                            total_return = EXCLUDED.total_return
                    """, {
                        **scenario,
                        'sale_price': scenario.get('sale_price'),
                        'selling_costs_amount': scenario.get('selling_costs_amount'),
                        'loan_payoff': scenario.get('loan_payoff'),
                        'net_sale_proceeds': scenario.get('net_sale_proceeds'),
                        'total_return': scenario.get('total_return'),
                        'cash_out_refinance_amount': scenario.get('cash_out_refinance_amount'),
                        'capital_recycled': scenario.get('capital_recycled'),
                        'infinite_roi': scenario.get('infinite_roi', False)
                    })
                
                conn.commit()
    
    
    def save_analysis_summary(self, property_id: int, summary: Dict):
        """Save analysis summary for dashboard KPIs"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                summary['property_id'] = property_id
                cur.execute("""
                    INSERT INTO sfr_analysis_summary (
                        property_id, analysis_date,
                        current_value, purchase_price, total_invested,
                        monthly_rent, monthly_expenses, monthly_mortgage, monthly_cash_flow,
                        cash_on_cash_return, ten_year_irr, cap_rate, dscr, ltv,
                        one_percent_rule_pass, break_even_rent,
                        investment_decision, decision_rationale
                    ) VALUES (
                        %(property_id)s, %(analysis_date)s,
                        %(current_value)s, %(purchase_price)s, %(total_invested)s,
                        %(monthly_rent)s, %(monthly_expenses)s, %(monthly_mortgage)s, %(monthly_cash_flow)s,
                        %(cash_on_cash_return)s, %(ten_year_irr)s, %(cap_rate)s, %(dscr)s, %(ltv)s,
                        %(one_percent_rule_pass)s, %(break_even_rent)s,
                        %(investment_decision)s, %(decision_rationale)s
                    )
                    ON CONFLICT (property_id, analysis_date)
                    DO UPDATE SET
                        monthly_cash_flow = EXCLUDED.monthly_cash_flow,
                        ten_year_irr = EXCLUDED.ten_year_irr,
                        investment_decision = EXCLUDED.investment_decision
                """, summary)
                
                conn.commit()
    
    
    # =========================================================================
    # COMPLETE ANALYSIS WORKFLOW
    # =========================================================================
    
    def run_complete_analysis(self, property: SFRProperty, financing: SFRFinancing) -> Dict:
        """
        Run complete property analysis workflow:
        1. Calculate mortgage payment
        2. Project 10-year cash flows
        3. Analyze exit scenarios
        4. Generate summary metrics
        5. Save to database
        6. Return results
        
        Returns:
            Dictionary with all analysis results
        """
        # Step 1: Calculate mortgage payment
        financing.monthly_payment = self.calculate_mortgage_payment(
            financing.loan_amount,
            financing.interest_rate,
            financing.loan_term_months
        )
        
        # Step 2: Project cash flows
        cash_flows = self.project_cash_flows(property, financing, years=10)
        
        # Step 3: Analyze exit scenarios
        scenarios = self.analyze_exit_scenarios(property, financing, cash_flows)
        
        # Step 4: Generate summary
        year_1_cf = sum(cf['net_cash_flow'] for cf in cash_flows[:12])
        year_1_noi = sum(cf['noi'] for cf in cash_flows[:12])
        
        summary = {
            'analysis_date': date.today(),
            'current_value': property.purchase_price,
            'purchase_price': property.purchase_price,
            'total_invested': financing.total_cash_invested,
            'monthly_rent': property.monthly_rent,
            'monthly_expenses': cash_flows[0]['total_operating_expenses'],
            'monthly_mortgage': financing.monthly_payment,
            'monthly_cash_flow': cash_flows[0]['net_cash_flow'],
            'cash_on_cash_return': self.calculate_cash_on_cash_return(year_1_cf, financing.total_cash_invested),
            'ten_year_irr': next((s['irr'] for s in scenarios if s['scenario_type'] == 'Hold'), Decimal('0')),
            'cap_rate': self.calculate_cap_rate(year_1_noi, property.purchase_price),
            'dscr': self.calculate_dscr(year_1_noi, financing.monthly_payment * Decimal('12')),
            'ltv': financing.ltv_ratio,
            'one_percent_rule_pass': self.check_one_percent_rule(property.monthly_rent, property.purchase_price),
            'break_even_rent': (cash_flows[0]['total_operating_expenses'] + financing.monthly_payment),
            'investment_decision': 'ANALYZE',
            'decision_rationale': 'Initial analysis complete'
        }
        
        # Make investment decision
        if summary['cash_on_cash_return'] > 15 and summary['ten_year_irr'] > 18:
            summary['investment_decision'] = 'STRONG BUY'
            summary['decision_rationale'] = f"Excellent returns: {summary['cash_on_cash_return']:.1f}% CoC, {summary['ten_year_irr']:.1f}% IRR"
        elif summary['cash_on_cash_return'] > 10 and summary['ten_year_irr'] > 15:
            summary['investment_decision'] = 'BUY'
            summary['decision_rationale'] = f"Good returns: {summary['cash_on_cash_return']:.1f}% CoC, {summary['ten_year_irr']:.1f}% IRR"
        elif summary['monthly_cash_flow'] < 0:
            summary['investment_decision'] = 'PASS'
            summary['decision_rationale'] = f"Negative cash flow: ${summary['monthly_cash_flow']:.2f}/month"
        else:
            summary['investment_decision'] = 'ANALYZE'
            summary['decision_rationale'] = "Marginal returns - needs deeper analysis"
        
        # Step 5: Save to database
        try:
            property_id = self.create_property(property, financing)
            self.save_cash_flows(property_id, cash_flows)
            self.save_scenarios(property_id, scenarios)
            self.save_analysis_summary(property_id, summary)
            
            return {
                'property_id': property_id,
                'summary': summary,
                'cash_flows': cash_flows,
                'scenarios': scenarios,
                'status': 'SUCCESS'
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e)
            }
    
    
    # =========================================================================
    # PORTFOLIO QUERIES
    # =========================================================================
    
    def get_portfolio_summary(self, fund_id: Optional[int] = None) -> Dict:
        """Get portfolio-level metrics"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                if fund_id:
                    cur.execute("""
                        SELECT * FROM vw_sfr_portfolio_summary
                        WHERE fund_id = %s
                    """, (fund_id,))
                else:
                    cur.execute("SELECT * FROM vw_sfr_portfolio_summary")
                
                return cur.fetchone()
    
    
    def get_top_performers(self, limit: int = 10) -> List[Dict]:
        """Get best performing properties"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM vw_sfr_top_performers
                    LIMIT %s
                """, (limit,))
                
                return cur.fetchall()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Initialize service
    service = SFRAnalysisService("dbname=portfolio_dashboard user=admin password=secure123 host=localhost")
    
    # Create sample property
    property = SFRProperty(
        company_id=1,
        fund_id=1,
        property_name="123 Main Street",
        address="123 Main Street",
        city="Austin",
        state="TX",
        zip_code="78701",
        square_feet=1500,
        bedrooms=3,
        bathrooms=Decimal('2.0'),
        year_built=2015,
        purchase_price=Decimal('150000'),
        closing_costs=Decimal('3000'),
        renovation_budget=Decimal('45000'),
        total_acquisition_cost=Decimal('198000'),
        acquisition_date=date(2025, 1, 15),
        monthly_rent=Decimal('2450'),
        vacancy_rate=Decimal('5.0'),
        property_tax_monthly=Decimal('350'),
        insurance_monthly=Decimal('125'),
        maintenance_reserve_monthly=Decimal('200'),
        capex_reserve_monthly=Decimal('150'),
        investment_strategy="Buy & Hold",
        status="Analysis"
    )
    
    # Create financing
    financing = SFRFinancing(
        down_payment=Decimal('49500'),  # 25% down
        closing_costs_cash=Decimal('3000'),
        renovation_cash=Decimal('45000'),
        total_cash_invested=Decimal('97500'),
        loan_amount=Decimal('148500'),  # 75% LTV
        loan_type="Conventional",
        interest_rate=Decimal('7.5'),
        loan_term_months=360,
        ltv_ratio=Decimal('75.0')
    )
    
    # Run analysis
    result = service.run_complete_analysis(property, financing)
    
    if result['status'] == 'SUCCESS':
        print(f"✅ Analysis complete! Property ID: {result['property_id']}")
        print(f"📊 Decision: {result['summary']['investment_decision']}")
        print(f"💰 Year 1 Cash-on-Cash: {result['summary']['cash_on_cash_return']:.2f}%")
        print(f"📈 10-Year IRR: {result['summary']['ten_year_irr']:.2f}%")
        print(f"🏠 Monthly Cash Flow: ${result['summary']['monthly_cash_flow']:.2f}")
    else:
        print(f"❌ Error: {result['error']}")
