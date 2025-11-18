/**
 * Advanced Financial Calculations Utility
 * Based on advanced-finance skill specifications
 *
 * Includes:
 * - DCF (Discounted Cash Flow) Valuation
 * - WACC (Weighted Average Cost of Capital)
 * - IRR (Internal Rate of Return) & MIRR (Modified IRR)
 * - NPV (Net Present Value)
 * - Cap Rate & NOI calculations
 * - Monte Carlo Simulations
 * - Scenario Analysis
 */

export interface CashFlow {
  year: number;
  amount: number;
}

export interface DCFInputs {
  cashFlows: number[];
  discountRate: number;
  terminalGrowthRate?: number;
}

export interface DCFResult {
  presentValueCashFlows: number[];
  sumPVCashFlows: number;
  terminalValue: number;
  presentValueTerminalValue: number;
  enterpriseValue: number;
}

export interface WACCInputs {
  equityValue: number;
  debtValue: number;
  costOfEquity: number;
  costOfDebt: number;
  taxRate: number;
}

export interface IRRResult {
  irr: number;
  npv: number;
  converged: boolean;
  iterations: number;
}

export interface ScenarioInputs {
  pessimisticGrowth: number;
  baseGrowth: number;
  optimisticGrowth: number;
  cashFlows: number[];
  discountRate: number;
}

export interface MonteCarloInputs {
  baseCashFlow: number;
  years: number;
  growthMean: number;
  growthStdDev: number;
  discountRate: number;
  simulations: number;
}

/**
 * DCF Valuation Model
 * Calculates enterprise value using discounted cash flow method
 */
export function calculateDCF(inputs: DCFInputs): DCFResult {
  const { cashFlows, discountRate, terminalGrowthRate = 0.02 } = inputs;
  const nYears = cashFlows.length;

  // Calculate present value of each cash flow
  const presentValueCashFlows = cashFlows.map((cf, index) => {
    const year = index + 1;
    return cf / Math.pow(1 + discountRate, year);
  });

  const sumPVCashFlows = presentValueCashFlows.reduce((sum, pv) => sum + pv, 0);

  // Terminal Value using Gordon Growth Model
  const terminalCashFlow = cashFlows[nYears - 1] * (1 + terminalGrowthRate);
  const terminalValue = terminalCashFlow / (discountRate - terminalGrowthRate);
  const presentValueTerminalValue = terminalValue / Math.pow(1 + discountRate, nYears);

  const enterpriseValue = sumPVCashFlows + presentValueTerminalValue;

  return {
    presentValueCashFlows,
    sumPVCashFlows,
    terminalValue,
    presentValueTerminalValue,
    enterpriseValue,
  };
}

/**
 * WACC Calculation
 * Weighted Average Cost of Capital
 */
export function calculateWACC(inputs: WACCInputs): number {
  const { equityValue, debtValue, costOfEquity, costOfDebt, taxRate } = inputs;
  const totalValue = equityValue + debtValue;

  const equityWeight = equityValue / totalValue;
  const debtWeight = debtValue / totalValue;

  const wacc =
    (equityWeight * costOfEquity) +
    (debtWeight * costOfDebt * (1 - taxRate));

  return wacc;
}

/**
 * NPV Calculation
 * Net Present Value
 */
export function calculateNPV(
  cashFlows: number[],
  discountRate: number,
  initialInvestment: number = 0
): number {
  const pv = cashFlows.reduce((sum, cf, index) => {
    return sum + cf / Math.pow(1 + discountRate, index + 1);
  }, 0);

  return pv - initialInvestment;
}

/**
 * IRR Calculation using Newton-Raphson method
 * Internal Rate of Return
 */
export function calculateIRR(
  cashFlows: number[],
  guess: number = 0.1,
  maxIterations: number = 100,
  tolerance: number = 0.0001
): IRRResult {
  let rate = guess;
  let iterations = 0;
  let converged = false;

  for (let i = 0; i < maxIterations; i++) {
    iterations++;

    // Calculate NPV at current rate
    const npv = cashFlows.reduce((sum, cf, index) => {
      return sum + cf / Math.pow(1 + rate, index);
    }, 0);

    // Calculate derivative of NPV
    const derivative = cashFlows.reduce((sum, cf, index) => {
      return sum - (index * cf) / Math.pow(1 + rate, index + 1);
    }, 0);

    // Newton-Raphson iteration
    const newRate = rate - npv / derivative;

    // Check convergence
    if (Math.abs(newRate - rate) < tolerance) {
      converged = true;
      rate = newRate;
      break;
    }

    rate = newRate;
  }

  const npv = cashFlows.reduce((sum, cf, index) => {
    return sum + cf / Math.pow(1 + rate, index);
  }, 0);

  return {
    irr: rate,
    npv,
    converged,
    iterations,
  };
}

/**
 * MIRR Calculation
 * Modified Internal Rate of Return
 */
export function calculateMIRR(
  cashFlows: number[],
  financeRate: number,
  reinvestRate: number
): number {
  const n = cashFlows.length - 1;

  // Separate positive and negative cash flows
  const negativeCFs = cashFlows.map(cf => cf < 0 ? cf : 0);
  const positiveCFs = cashFlows.map(cf => cf > 0 ? cf : 0);

  // Present value of negative cash flows (financing costs)
  const pvNegative = negativeCFs.reduce((sum, cf, index) => {
    return sum + cf / Math.pow(1 + financeRate, index);
  }, 0);

  // Future value of positive cash flows (reinvestment)
  const fvPositive = positiveCFs.reduce((sum, cf, index) => {
    return sum + cf * Math.pow(1 + reinvestRate, n - index);
  }, 0);

  // MIRR formula
  const mirr = Math.pow(-fvPositive / pvNegative, 1 / n) - 1;

  return mirr;
}

/**
 * Cap Rate Calculation
 * Capitalization Rate = NOI / Property Value
 */
export function calculateCapRate(noi: number, propertyValue: number): number {
  return noi / propertyValue;
}

/**
 * NOI Calculation
 * Net Operating Income = Gross Income - Operating Expenses
 */
export function calculateNOI(
  grossIncome: number,
  operatingExpenses: number,
  vacancyRate: number = 0
): number {
  const effectiveGrossIncome = grossIncome * (1 - vacancyRate);
  return effectiveGrossIncome - operatingExpenses;
}

/**
 * Cash on Cash Return
 * Annual Cash Flow / Total Cash Invested
 */
export function calculateCashOnCashReturn(
  annualCashFlow: number,
  totalCashInvested: number
): number {
  return annualCashFlow / totalCashInvested;
}

/**
 * Debt Service Coverage Ratio
 * NOI / Annual Debt Service
 */
export function calculateDSCR(noi: number, annualDebtService: number): number {
  return noi / annualDebtService;
}

/**
 * Loan to Value Ratio
 * Loan Amount / Property Value
 */
export function calculateLTV(loanAmount: number, propertyValue: number): number {
  return loanAmount / propertyValue;
}

/**
 * Scenario Analysis
 * Calculate DCF under different growth scenarios
 */
export function scenarioAnalysis(inputs: ScenarioInputs) {
  const { cashFlows, discountRate, pessimisticGrowth, baseGrowth, optimisticGrowth } = inputs;

  // Adjust cash flows for each scenario
  const adjustCashFlows = (growthRate: number) => {
    return cashFlows.map((cf, index) => cf * Math.pow(1 + growthRate, index));
  };

  const pessimisticCFs = adjustCashFlows(pessimisticGrowth);
  const baseCFs = adjustCashFlows(baseGrowth);
  const optimisticCFs = adjustCashFlows(optimisticGrowth);

  return {
    pessimistic: calculateDCF({
      cashFlows: pessimisticCFs,
      discountRate,
      terminalGrowthRate: pessimisticGrowth,
    }),
    base: calculateDCF({
      cashFlows: baseCFs,
      discountRate,
      terminalGrowthRate: baseGrowth,
    }),
    optimistic: calculateDCF({
      cashFlows: optimisticCFs,
      discountRate,
      terminalGrowthRate: optimisticGrowth,
    }),
  };
}

/**
 * Monte Carlo Simulation for DCF
 * Generates probability distribution of valuations
 */
export function monteCarloSimulation(inputs: MonteCarloInputs) {
  const { baseCashFlow, years, growthMean, growthStdDev, discountRate, simulations } = inputs;

  const results: number[] = [];

  for (let sim = 0; sim < simulations; sim++) {
    const cashFlows: number[] = [];

    for (let year = 1; year <= years; year++) {
      // Generate random growth rate using Box-Muller transform for normal distribution
      const u1 = Math.random();
      const u2 = Math.random();
      const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
      const randomGrowth = growthMean + z * growthStdDev;

      const cashFlow = baseCashFlow * Math.pow(1 + randomGrowth, year);
      cashFlows.push(cashFlow);
    }

    const dcf = calculateDCF({
      cashFlows,
      discountRate,
      terminalGrowthRate: growthMean,
    });

    results.push(dcf.enterpriseValue);
  }

  // Calculate statistics
  results.sort((a, b) => a - b);

  const mean = results.reduce((sum, val) => sum + val, 0) / results.length;
  const variance = results.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / results.length;
  const stdDev = Math.sqrt(variance);

  const percentile = (p: number) => {
    const index = Math.floor(results.length * p);
    return results[index];
  };

  return {
    results,
    mean,
    stdDev,
    median: percentile(0.5),
    percentile5: percentile(0.05),
    percentile25: percentile(0.25),
    percentile75: percentile(0.75),
    percentile95: percentile(0.95),
    min: results[0],
    max: results[results.length - 1],
  };
}

/**
 * Mortgage Payment Calculator
 * Monthly payment for a loan
 */
export function calculateMortgagePayment(
  principal: number,
  annualRate: number,
  years: number
): {
  monthlyPayment: number;
  totalPayment: number;
  totalInterest: number;
} {
  const monthlyRate = annualRate / 12;
  const numberOfPayments = years * 12;

  const monthlyPayment = principal *
    (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
    (Math.pow(1 + monthlyRate, numberOfPayments) - 1);

  const totalPayment = monthlyPayment * numberOfPayments;
  const totalInterest = totalPayment - principal;

  return {
    monthlyPayment,
    totalPayment,
    totalInterest,
  };
}

/**
 * Amortization Schedule Generator
 */
export function generateAmortizationSchedule(
  principal: number,
  annualRate: number,
  years: number
): Array<{
  month: number;
  payment: number;
  principal: number;
  interest: number;
  balance: number;
}> {
  const { monthlyPayment } = calculateMortgagePayment(principal, annualRate, years);
  const monthlyRate = annualRate / 12;
  const numberOfPayments = years * 12;

  const schedule = [];
  let balance = principal;

  for (let month = 1; month <= numberOfPayments; month++) {
    const interest = balance * monthlyRate;
    const principalPayment = monthlyPayment - interest;
    balance -= principalPayment;

    schedule.push({
      month,
      payment: monthlyPayment,
      principal: principalPayment,
      interest,
      balance: Math.max(0, balance), // Avoid negative balance due to rounding
    });
  }

  return schedule;
}

/**
 * Break-Even Analysis
 * Calculate when cumulative cash flows turn positive
 */
export function calculateBreakEven(cashFlows: number[]): {
  breakEvenPeriod: number | null;
  cumulativeCashFlows: number[];
} {
  const cumulativeCashFlows: number[] = [];
  let cumulative = 0;
  let breakEvenPeriod: number | null = null;

  cashFlows.forEach((cf, index) => {
    cumulative += cf;
    cumulativeCashFlows.push(cumulative);

    if (breakEvenPeriod === null && cumulative > 0) {
      breakEvenPeriod = index + 1;
    }
  });

  return {
    breakEvenPeriod,
    cumulativeCashFlows,
  };
}

/**
 * Sensitivity Analysis
 * Analyze how changes in variables affect valuation
 */
export function sensitivityAnalysis(
  baseCashFlows: number[],
  baseDiscountRate: number,
  variableRanges: {
    discountRateRange: number[];
    growthRateRange: number[];
  }
) {
  const results: Array<{
    discountRate: number;
    growthRate: number;
    enterpriseValue: number;
  }> = [];

  variableRanges.discountRateRange.forEach(dr => {
    variableRanges.growthRateRange.forEach(gr => {
      const dcf = calculateDCF({
        cashFlows: baseCashFlows,
        discountRate: dr,
        terminalGrowthRate: gr,
      });

      results.push({
        discountRate: dr,
        growthRate: gr,
        enterpriseValue: dcf.enterpriseValue,
      });
    });
  });

  return results;
}

export default {
  calculateDCF,
  calculateWACC,
  calculateNPV,
  calculateIRR,
  calculateMIRR,
  calculateCapRate,
  calculateNOI,
  calculateCashOnCashReturn,
  calculateDSCR,
  calculateLTV,
  scenarioAnalysis,
  monteCarloSimulation,
  calculateMortgagePayment,
  generateAmortizationSchedule,
  calculateBreakEven,
  sensitivityAnalysis,
};
