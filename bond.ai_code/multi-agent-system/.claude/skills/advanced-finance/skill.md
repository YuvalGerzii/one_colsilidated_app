---
name: Advanced Finance Expert
description: Provides sophisticated financial analysis, valuation models, investment strategies, and corporate finance expertise for real estate ventures and technology companies
---

# Advanced Finance Expert

## Overview

This skill enables Claude to perform advanced financial analysis, create comprehensive financial models, and provide strategic financial guidance. It combines corporate finance principles, real estate finance, valuation methodologies, and investment analysis to support data-driven financial decision-making.

## When to Use This Skill

Invoke this skill when:
- Building financial models and projections
- Performing valuation analysis (DCF, comparable analysis, etc.)
- Analyzing investment opportunities
- Creating capital structure and financing strategies
- Conducting scenario and sensitivity analysis
- Preparing investor presentations and financial reports
- Optimizing portfolio allocation and risk management
- Evaluating M&A opportunities
- Forecasting revenue and expenses
- Analyzing unit economics and profitability

## Core Finance Frameworks

### 1. Real Estate Financial Modeling

**Property Pro Forma:**
```typescript
interface PropertyProForma {
  // Revenue streams
  revenue: {
    gross_rental_income: number;
    vacancy_loss: number;          // Typically 5-10%
    effective_gross_income: number; // GRI - Vacancy
    other_income: {
      parking: number;
      laundry: number;
      pet_fees: number;
      late_fees: number;
      other: number;
    };
    total_revenue: number;
  };

  // Operating expenses
  operating_expenses: {
    property_management: number;   // 8-12% of EGI
    maintenance_repairs: number;
    utilities: number;
    insurance: number;
    property_taxes: number;
    marketing_leasing: number;
    legal_accounting: number;
    payroll: number;
    administrative: number;
    reserves: number;              // 3-5% of EGI
    total_opex: number;
  };

  // Net Operating Income
  noi: number;                     // Total Revenue - Total OpEx

  // Capital expenses (not in NOI)
  capex: {
    roof_replacement: number;
    hvac: number;
    appliances: number;
    flooring: number;
    exterior_painting: number;
    total: number;
  };

  // Debt service
  debt_service: {
    loan_amount: number;
    interest_rate: number;
    term_years: number;
    monthly_payment: number;
    annual_debt_service: number;
  };

  // Cash flow metrics
  cash_flow: {
    before_tax_cash_flow: number;  // NOI - Debt Service - CapEx
    tax_benefits: number;          // Depreciation, interest deduction
    after_tax_cash_flow: number;
  };

  // Return metrics
  returns: {
    cap_rate: number;              // NOI / Purchase Price
    cash_on_cash: number;          // BTCF / Equity Invested
    irr: number;                   // Internal Rate of Return
    equity_multiple: number;       // Total Returns / Equity Invested
    dscr: number;                  // NOI / Debt Service
  };

  // Exit assumptions
  exit: {
    holding_period_years: number;
    exit_cap_rate: number;
    terminal_value: number;        // Year N NOI / Exit Cap Rate
    selling_costs: number;         // 2-3% of sale price
    net_proceeds: number;
  };
}
```

**Multi-Year Projection:**
```python
def build_10year_proforma(property_data, assumptions):
    """
    Build detailed 10-year financial projection
    """
    years = range(1, 11)
    projection = []

    for year in years:
        # Revenue growth assumptions
        rent_growth_rate = assumptions['rent_growth'][year]
        vacancy_rate = assumptions['vacancy_rate'][year]

        # Calculate revenue
        gross_rental_income = property_data['base_rent'] * (1 + rent_growth_rate) ** year
        vacancy_loss = gross_rental_income * vacancy_rate
        effective_gross_income = gross_rental_income - vacancy_loss
        other_income = property_data['other_income'] * (1.02 ** year)  # 2% growth
        total_revenue = effective_gross_income + other_income

        # Operating expenses (typically grow with inflation)
        opex_growth = 0.03  # 3% annual increase
        operating_expenses = property_data['base_opex'] * (1 + opex_growth) ** year

        # NOI
        noi = total_revenue - operating_expenses

        # Debt service (fixed if fixed-rate loan)
        debt_service = property_data['annual_debt_service']

        # CapEx reserves
        capex = total_revenue * 0.05  # 5% of revenue

        # Cash flow
        cash_flow = noi - debt_service - capex

        projection.append({
            'year': year,
            'revenue': total_revenue,
            'opex': operating_expenses,
            'noi': noi,
            'debt_service': debt_service,
            'capex': capex,
            'cash_flow': cash_flow,
            'cumulative_cash_flow': sum(p['cash_flow'] for p in projection) + cash_flow
        })

    return projection
```

### 2. Discounted Cash Flow (DCF) Valuation

**DCF Model:**
```python
import numpy as np

def dcf_valuation(cash_flows, discount_rate, terminal_growth_rate=0.02):
    """
    Comprehensive DCF valuation model

    Args:
        cash_flows: List of projected cash flows
        discount_rate: WACC or required rate of return
        terminal_growth_rate: Perpetual growth rate (typically 2-3%)

    Returns:
        Enterprise value and per-share value
    """

    # Discount projected cash flows
    n_years = len(cash_flows)
    pv_cash_flows = []

    for i, cf in enumerate(cash_flows, start=1):
        pv = cf / ((1 + discount_rate) ** i)
        pv_cash_flows.append(pv)

    # Terminal value (Gordon Growth Model)
    terminal_cash_flow = cash_flows[-1] * (1 + terminal_growth_rate)
    terminal_value = terminal_cash_flow / (discount_rate - terminal_growth_rate)

    # Discount terminal value to present
    pv_terminal_value = terminal_value / ((1 + discount_rate) ** n_years)

    # Enterprise value
    enterprise_value = sum(pv_cash_flows) + pv_terminal_value

    return {
        'pv_projected_cf': sum(pv_cash_flows),
        'pv_terminal_value': pv_terminal_value,
        'enterprise_value': enterprise_value,
        'terminal_value': terminal_value,
        'breakdown': {
            f'year_{i}': pv for i, pv in enumerate(pv_cash_flows, start=1)
        }
    }

# Example usage
cash_flows = [100000, 110000, 121000, 133100, 146410]  # Growing at 10%
discount_rate = 0.12  # 12% WACC
valuation = dcf_valuation(cash_flows, discount_rate)
```

**Weighted Average Cost of Capital (WACC):**
```python
def calculate_wacc(equity_value, debt_value, cost_of_equity, cost_of_debt, tax_rate):
    """
    Calculate WACC

    WACC = (E/V × Re) + (D/V × Rd × (1-Tc))

    Where:
        E = Market value of equity
        D = Market value of debt
        V = E + D (Total value)
        Re = Cost of equity
        Rd = Cost of debt
        Tc = Corporate tax rate
    """
    total_value = equity_value + debt_value
    equity_weight = equity_value / total_value
    debt_weight = debt_value / total_value

    wacc = (equity_weight * cost_of_equity) + \
           (debt_weight * cost_of_debt * (1 - tax_rate))

    return {
        'wacc': wacc,
        'equity_weight': equity_weight,
        'debt_weight': debt_weight,
        'after_tax_cost_of_debt': cost_of_debt * (1 - tax_rate)
    }

# Cost of Equity (CAPM)
def calculate_cost_of_equity(risk_free_rate, beta, market_return):
    """
    Capital Asset Pricing Model (CAPM)

    Re = Rf + β(Rm - Rf)
    """
    return risk_free_rate + beta * (market_return - risk_free_rate)
```

### 3. Investment Analysis

**Internal Rate of Return (IRR) Calculation:**
```python
def calculate_irr(cash_flows, initial_investment):
    """
    Calculate IRR using Newton-Raphson method

    IRR is the discount rate where NPV = 0
    """
    from scipy.optimize import newton

    # Insert initial investment as negative cash flow
    all_cash_flows = [-initial_investment] + cash_flows

    def npv(rate):
        return sum(cf / (1 + rate) ** i for i, cf in enumerate(all_cash_flows))

    def npv_derivative(rate):
        return sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(all_cash_flows))

    # Find IRR
    irr = newton(npv, x0=0.1, fprime=npv_derivative)

    return irr

# Example
initial_investment = 1000000
cash_flows = [150000, 175000, 200000, 225000, 1500000]  # Last includes exit
irr = calculate_irr(cash_flows, initial_investment)
print(f"IRR: {irr:.2%}")
```

**Modified Internal Rate of Return (MIRR):**
```python
def calculate_mirr(cash_flows, initial_investment, finance_rate, reinvestment_rate):
    """
    MIRR addresses IRR's reinvestment assumption

    More realistic for comparing investments
    """
    n = len(cash_flows)

    # Future value of positive cash flows (at reinvestment rate)
    fv_positive = sum(
        cf * (1 + reinvestment_rate) ** (n - i)
        for i, cf in enumerate(cash_flows, start=1)
        if cf > 0
    )

    # Present value of negative cash flows (at finance rate)
    pv_negative = initial_investment + sum(
        abs(cf) / (1 + finance_rate) ** i
        for i, cf in enumerate(cash_flows, start=1)
        if cf < 0
    )

    # MIRR
    mirr = (fv_positive / pv_negative) ** (1 / n) - 1

    return mirr
```

**Profitability Index:**
```python
def profitability_index(cash_flows, initial_investment, discount_rate):
    """
    PI = PV of future cash flows / Initial investment

    PI > 1: Accept project
    PI < 1: Reject project

    Useful for capital rationing decisions
    """
    pv_cash_flows = sum(
        cf / (1 + discount_rate) ** i
        for i, cf in enumerate(cash_flows, start=1)
    )

    pi = pv_cash_flows / initial_investment

    return {
        'profitability_index': pi,
        'npv': pv_cash_flows - initial_investment,
        'decision': 'Accept' if pi > 1 else 'Reject'
    }
```

### 4. Scenario and Sensitivity Analysis

**Three-Scenario Analysis:**
```python
def scenario_analysis(base_assumptions):
    """
    Best case, base case, worst case scenarios
    """
    scenarios = {
        'pessimistic': {
            'rent_growth': base_assumptions['rent_growth'] - 0.02,
            'vacancy_rate': base_assumptions['vacancy_rate'] + 0.05,
            'exit_cap_rate': base_assumptions['exit_cap_rate'] + 0.01,
            'opex_growth': base_assumptions['opex_growth'] + 0.01
        },
        'base': base_assumptions,
        'optimistic': {
            'rent_growth': base_assumptions['rent_growth'] + 0.02,
            'vacancy_rate': base_assumptions['vacancy_rate'] - 0.03,
            'exit_cap_rate': base_assumptions['exit_cap_rate'] - 0.01,
            'opex_growth': base_assumptions['opex_growth'] - 0.01
        }
    }

    results = {}
    for scenario_name, assumptions in scenarios.items():
        # Run financial model with these assumptions
        projection = build_10year_proforma(property_data, assumptions)
        irr = calculate_irr(...)
        equity_multiple = calculate_equity_multiple(...)

        results[scenario_name] = {
            'irr': irr,
            'equity_multiple': equity_multiple,
            'total_cash_flow': sum(p['cash_flow'] for p in projection)
        }

    return results
```

**Sensitivity Analysis (Tornado Chart):**
```python
def sensitivity_analysis(base_model, variables_to_test):
    """
    Analyze sensitivity to key variables

    Returns data for tornado chart visualization
    """
    base_irr = calculate_irr(base_model)

    sensitivity_results = []

    for var_name, (low_value, high_value) in variables_to_test.items():
        # Test low value
        model_low = base_model.copy()
        model_low[var_name] = low_value
        irr_low = calculate_irr(model_low)

        # Test high value
        model_high = base_model.copy()
        model_high[var_name] = high_value
        irr_high = calculate_irr(model_high)

        sensitivity_results.append({
            'variable': var_name,
            'base_irr': base_irr,
            'irr_low': irr_low,
            'irr_high': irr_high,
            'range': abs(irr_high - irr_low),
            'impact': abs(irr_high - irr_low) / base_irr  # % change
        })

    # Sort by impact (most sensitive first)
    sensitivity_results.sort(key=lambda x: x['range'], reverse=True)

    return sensitivity_results

# Example
variables = {
    'rent_growth_rate': (0.02, 0.05),      # 2% to 5%
    'vacancy_rate': (0.03, 0.10),          # 3% to 10%
    'exit_cap_rate': (0.05, 0.08),         # 5% to 8%
    'purchase_price': (900000, 1100000)    # ±10%
}
```

**Monte Carlo Simulation:**
```python
import numpy as np

def monte_carlo_simulation(n_simulations=10000):
    """
    Monte Carlo simulation for investment returns

    Provides probability distribution of outcomes
    """
    results = []

    for _ in range(n_simulations):
        # Randomly sample from distributions
        rent_growth = np.random.normal(0.03, 0.01)      # Mean 3%, std 1%
        vacancy_rate = np.random.uniform(0.05, 0.10)    # 5-10%
        exit_cap_rate = np.random.normal(0.065, 0.005)  # Mean 6.5%, std 0.5%
        opex_growth = np.random.normal(0.03, 0.005)

        # Run model with sampled parameters
        assumptions = {
            'rent_growth': rent_growth,
            'vacancy_rate': vacancy_rate,
            'exit_cap_rate': exit_cap_rate,
            'opex_growth': opex_growth
        }

        irr = calculate_investment_irr(assumptions)
        results.append(irr)

    # Analyze distribution
    results_array = np.array(results)

    return {
        'mean': np.mean(results_array),
        'median': np.median(results_array),
        'std_dev': np.std(results_array),
        'percentiles': {
            '5th': np.percentile(results_array, 5),
            '25th': np.percentile(results_array, 25),
            '50th': np.percentile(results_array, 50),
            '75th': np.percentile(results_array, 75),
            '95th': np.percentile(results_array, 95)
        },
        'probability_positive': np.sum(results_array > 0) / n_simulations,
        'probability_above_hurdle': np.sum(results_array > 0.15) / n_simulations  # 15% hurdle
    }
```

### 5. Portfolio Optimization

**Modern Portfolio Theory (Markowitz):**
```python
import numpy as np
from scipy.optimize import minimize

def portfolio_optimization(expected_returns, cov_matrix, risk_free_rate=0.03):
    """
    Find optimal portfolio weights using MPT

    Maximizes Sharpe ratio
    """
    n_assets = len(expected_returns)

    def portfolio_stats(weights):
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        return portfolio_return, portfolio_volatility, sharpe_ratio

    def negative_sharpe(weights):
        return -portfolio_stats(weights)[2]

    # Constraints: weights sum to 1
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]

    # Bounds: 0 <= weight <= 40% (diversification)
    bounds = tuple((0, 0.4) for _ in range(n_assets))

    # Initial guess (equal weights)
    initial_weights = np.ones(n_assets) / n_assets

    # Optimize
    result = minimize(
        negative_sharpe,
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    optimal_weights = result.x
    port_return, port_vol, sharpe = portfolio_stats(optimal_weights)

    return {
        'weights': optimal_weights,
        'expected_return': port_return,
        'volatility': port_vol,
        'sharpe_ratio': sharpe
    }
```

**Efficient Frontier:**
```python
def generate_efficient_frontier(expected_returns, cov_matrix, n_portfolios=100):
    """
    Generate efficient frontier curve
    """
    n_assets = len(expected_returns)

    results = []
    target_returns = np.linspace(
        expected_returns.min(),
        expected_returns.max(),
        n_portfolios
    )

    for target_return in target_returns:
        # Minimize volatility for target return
        def portfolio_volatility(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.dot(x, expected_returns) - target_return}
        ]

        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_weights = np.ones(n_assets) / n_assets

        result = minimize(
            portfolio_volatility,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )

        if result.success:
            results.append({
                'return': target_return,
                'volatility': result.fun,
                'weights': result.x
            })

    return results
```

### 6. Corporate Finance Metrics

**SaaS Metrics (for real estate tech platform):**
```typescript
interface SaaSMetrics {
  revenue: {
    mrr: number;                     // Monthly Recurring Revenue
    arr: number;                     // Annual Recurring Revenue (MRR × 12)
    new_mrr: number;                 // From new customers
    expansion_mrr: number;           // Upsells, upgrades
    contraction_mrr: number;         // Downgrades
    churned_mrr: number;
    net_new_mrr: number;             // New + Expansion - Contraction - Churn
  };

  growth: {
    mrr_growth_rate: number;         // (Net New MRR / Prior MRR) × 100
    arr_growth_rate: number;
    customer_growth_rate: number;
    yoy_growth: number;              // Year-over-year
  };

  unit_economics: {
    arpu: number;                    // Average Revenue Per User
    arpa: number;                    // Average Revenue Per Account
    cac: number;                     // Customer Acquisition Cost
    ltv: number;                     // Customer Lifetime Value
    ltv_cac_ratio: number;           // Should be > 3
    cac_payback_months: number;      // Should be < 12 months
  };

  retention: {
    gross_retention_rate: number;    // % of revenue retained (excluding expansion)
    net_retention_rate: number;      // % including expansion (target > 100%)
    logo_retention_rate: number;     // % of customers retained
    monthly_churn_rate: number;      // % churning per month
    annual_churn_rate: number;
  };

  efficiency: {
    magic_number: number;            // Net New ARR / Sales & Marketing Spend (target > 0.75)
    rule_of_40: number;              // Growth Rate + Profit Margin (target ≥ 40%)
    burn_multiple: number;           // Net Burn / Net New ARR (lower is better)
    runway_months: number;           // Cash / Monthly Burn Rate
  };
}
```

**Financial Ratios:**
```python
def calculate_financial_ratios(financials):
    """
    Comprehensive financial ratio analysis
    """
    return {
        # Liquidity ratios
        'current_ratio': financials['current_assets'] / financials['current_liabilities'],
        'quick_ratio': (financials['current_assets'] - financials['inventory']) / financials['current_liabilities'],
        'cash_ratio': financials['cash'] / financials['current_liabilities'],

        # Profitability ratios
        'gross_margin': (financials['revenue'] - financials['cogs']) / financials['revenue'],
        'operating_margin': financials['operating_income'] / financials['revenue'],
        'net_margin': financials['net_income'] / financials['revenue'],
        'roa': financials['net_income'] / financials['total_assets'],  # Return on Assets
        'roe': financials['net_income'] / financials['shareholders_equity'],  # Return on Equity

        # Leverage ratios
        'debt_to_equity': financials['total_debt'] / financials['shareholders_equity'],
        'debt_to_assets': financials['total_debt'] / financials['total_assets'],
        'interest_coverage': financials['ebit'] / financials['interest_expense'],

        # Efficiency ratios
        'asset_turnover': financials['revenue'] / financials['total_assets'],
        'inventory_turnover': financials['cogs'] / financials['avg_inventory'],
        'days_sales_outstanding': (financials['accounts_receivable'] / financials['revenue']) * 365
    }
```

### 7. Cap Table and Fundraising

**Capitalization Table:**
```typescript
interface CapTable {
  shareholders: {
    name: string;
    type: 'founder' | 'employee' | 'angel' | 'vc' | 'strategic';
    shares: {
      common: number;
      preferred: number;
      options: number;
    };
    ownership_percentage: number;
    fully_diluted_percentage: number;
  }[];

  funding_rounds: {
    round: 'seed' | 'series_a' | 'series_b' | 'series_c';
    date: Date;
    amount_raised: number;
    pre_money_valuation: number;
    post_money_valuation: number;
    price_per_share: number;
    shares_issued: number;
    lead_investor: string;
  }[];

  option_pool: {
    size: number;                    // Total options authorized
    allocated: number;               // Options granted
    available: number;               // Remaining for future grants
    percentage_of_fully_diluted: number;
  };

  waterfall_analysis: {
    exit_value: number;
    shareholder_proceeds: {
      [shareholder: string]: {
        proceeds: number;
        multiple: number;            // Return on investment
      };
    };
  };
}
```

**Fundraising Metrics:**
```typescript
interface FundraisingMetrics {
  valuation: {
    pre_money: number;
    post_money: number;
    implied_share_price: number;
  };

  dilution: {
    founder_dilution: number;        // % ownership decrease
    employee_pool_dilution: number;
    new_money_ownership: number;     // % to new investors
  };

  terms: {
    liquidation_preference: number;  // Typically 1x
    participation: boolean;          // Participating vs non-participating preferred
    anti_dilution: 'full_ratchet' | 'weighted_average' | 'none';
    board_seats: number;
    pro_rata_rights: boolean;
  };

  use_of_funds: {
    category: 'product_development' | 'sales_marketing' | 'operations' | 'hiring';
    amount: number;
    percentage: number;
  }[];

  runway: {
    months: number;
    monthly_burn_rate: number;
    milestones: string[];            // Milestones to achieve before next round
  };
}
```

## Best Practices

### ✅ DO:

1. **Build Conservative Models**
   - Use conservative assumptions
   - Stress test with downside scenarios
   - Include appropriate contingency reserves
   - Document all assumptions clearly

2. **Focus on Cash Flow**
   - Cash is king, not accounting profit
   - Model cash flow timing accurately
   - Account for working capital needs
   - Plan for seasonal variations

3. **Validate Assumptions**
   - Cross-reference with market data
   - Compare to industry benchmarks
   - Get input from domain experts
   - Update models with actual results

4. **Perform Sensitivity Analysis**
   - Identify key value drivers
   - Test impact of assumption changes
   - Understand break-even points
   - Quantify downside risk

5. **Use Appropriate Discount Rates**
   - Match risk to discount rate
   - Consider project-specific risks
   - Adjust for leverage
   - Document rate selection rationale

6. **Maintain Flexibility**
   - Build modular, flexible models
   - Use scenarios and toggles
   - Enable easy assumption updates
   - Version control models

### ❌ DON'T:

1. **Over-Complicate Models**
   - Complexity doesn't equal accuracy
   - Keep models transparent and auditable
   - Avoid unnecessary precision

2. **Cherry-Pick Assumptions**
   - Don't only model optimistic scenarios
   - Include realistic downside cases
   - Be honest about risks

3. **Ignore Time Value of Money**
   - Always discount future cash flows
   - Consider opportunity cost
   - Account for inflation

4. **Forget Tax Implications**
   - Model after-tax cash flows
   - Consider tax-advantaged structures
   - Include depreciation benefits

5. **Rely Solely on IRR**
   - Use multiple metrics (IRR, NPV, payback, etc.)
   - Understand IRR limitations
   - Consider absolute returns, not just percentages

## Key Formulas Reference

```
Cap Rate = NOI / Property Value

Cash-on-Cash Return = Annual Pre-Tax Cash Flow / Total Cash Invested

Debt Service Coverage Ratio (DSCR) = NOI / Annual Debt Service

Loan-to-Value (LTV) = Loan Amount / Property Value

Gross Rent Multiplier (GRM) = Purchase Price / Gross Annual Rent

Net Present Value (NPV) = Σ [CFt / (1 + r)^t] - Initial Investment

Equity Multiple = Total Cash Distributions / Total Equity Invested

Break-Even Occupancy = (Operating Expenses + Debt Service) / Gross Potential Rent

Operating Expense Ratio = Operating Expenses / Effective Gross Income

Price-to-Earnings (P/E) Ratio = Market Price per Share / Earnings per Share

Enterprise Value = Market Cap + Debt - Cash

EBITDA Multiple = Enterprise Value / EBITDA
```

## Execution Instructions

When this skill is invoked:

1. **Understand the Objective**
   - Clarify the financial question or decision
   - Identify required outputs (valuation, returns, etc.)
   - Gather necessary data and assumptions

2. **Build the Model**
   - Structure logical, transparent calculations
   - Use clear variable names and labels
   - Document all assumptions
   - Build in flexibility for scenarios

3. **Validate and Test**
   - Check formulas for accuracy
   - Cross-reference with benchmarks
   - Test edge cases
   - Perform sensitivity analysis

4. **Analyze Results**
   - Calculate key metrics
   - Run scenario analysis
   - Identify value drivers
   - Assess risks and opportunities

5. **Present Findings**
   - Summarize key takeaways
   - Visualize results effectively
   - Provide clear recommendations
   - Include supporting detail

6. **Document Thoroughly**
   - Explain methodology
   - List all assumptions
   - Show calculations
   - Enable reproducibility

## Integration with Other Skills

- **Data Analysis**: Analyze historical financial data
- **Data Science**: Build predictive financial models
- **Manager/CEO**: Frame financial analysis for strategic decisions
- **Marketing**: Analyze marketing ROI and unit economics

## Deliverable Checklist

Before completing financial analysis:
- [ ] Objective clearly defined
- [ ] All assumptions documented
- [ ] Model structure is logical and transparent
- [ ] Calculations validated for accuracy
- [ ] Sensitivity analysis performed
- [ ] Multiple scenarios analyzed
- [ ] Key metrics calculated (IRR, NPV, etc.)
- [ ] Results benchmarked against comparables
- [ ] Risks and limitations identified
- [ ] Recommendations are actionable and supported
- [ ] Model is flexible and can be updated
- [ ] Presentation is clear and professional

