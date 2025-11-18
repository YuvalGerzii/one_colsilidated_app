import { BaseSavedReport } from '../types/calculatorTypes';

/**
 * Format number as currency (USD)
 */
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

/**
 * Format number as percentage
 */
export const formatPercent = (value: number, decimals: number = 2): string => {
  return `${value.toFixed(decimals)}%`;
};

/**
 * Calculate annuity payment (PMT function)
 * @param principal - Loan amount
 * @param annualRate - Annual interest rate (as decimal, e.g., 0.065 for 6.5%)
 * @param years - Loan term in years
 * @returns Monthly payment amount
 */
export const annuityPayment = (
  principal: number,
  annualRate: number,
  years: number
): number => {
  if (principal === 0 || annualRate === 0) return 0;

  const monthlyRate = annualRate / 12;
  const numPayments = years * 12;

  const payment =
    (principal * monthlyRate * Math.pow(1 + monthlyRate, numPayments)) /
    (Math.pow(1 + monthlyRate, numPayments) - 1);

  return payment;
};

/**
 * Calculate remaining loan balance after N payments
 * @param principal - Original loan amount
 * @param annualRate - Annual interest rate (as decimal)
 * @param termYears - Total loan term in years
 * @param paymentsMade - Number of monthly payments made
 * @returns Remaining balance
 */
export const remainingBalance = (
  principal: number,
  annualRate: number,
  termYears: number,
  paymentsMade: number
): number => {
  if (principal === 0 || annualRate === 0 || paymentsMade === 0) return principal;

  const monthlyRate = annualRate / 12;
  const totalPayments = termYears * 12;

  if (paymentsMade >= totalPayments) return 0;

  const monthlyPayment = annuityPayment(principal, annualRate, termYears);

  const remainingPayments = totalPayments - paymentsMade;
  const balance =
    (monthlyPayment / monthlyRate) *
    (1 - Math.pow(1 + monthlyRate, -remainingPayments));

  return Math.max(0, balance);
};

/**
 * Calculate Internal Rate of Return (IRR) using Newton-Raphson method
 * @param cashFlows - Array of cash flows (negative for investments, positive for returns)
 * @returns IRR as decimal (e.g., 0.15 for 15%)
 */
export const calculateIRR = (cashFlows: number[]): number => {
  if (cashFlows.length < 2) return 0;

  // Check if there are any positive cash flows
  const hasPositive = cashFlows.some((cf) => cf > 0);
  const hasNegative = cashFlows.some((cf) => cf < 0);
  if (!hasPositive || !hasNegative) return 0;

  // Newton-Raphson method
  let guess = 0.1; // Initial guess of 10%
  const maxIterations = 100;
  const tolerance = 0.000001;

  for (let i = 0; i < maxIterations; i++) {
    let npv = 0;
    let dnpv = 0; // Derivative of NPV

    for (let t = 0; t < cashFlows.length; t++) {
      npv += cashFlows[t] / Math.pow(1 + guess, t);
      if (t > 0) {
        dnpv += (-t * cashFlows[t]) / Math.pow(1 + guess, t + 1);
      }
    }

    const newGuess = guess - npv / dnpv;

    if (Math.abs(newGuess - guess) < tolerance) {
      return newGuess;
    }

    guess = newGuess;

    // Prevent infinite loops with invalid values
    if (isNaN(guess) || !isFinite(guess)) {
      return 0;
    }
  }

  return guess;
};

/**
 * Calculate Net Present Value (NPV)
 * @param cashFlows - Array of cash flows
 * @param discountRate - Discount rate as decimal
 * @returns NPV
 */
export const calculateNPV = (
  cashFlows: number[],
  discountRate: number
): number => {
  return cashFlows.reduce((npv, cf, t) => {
    return npv + cf / Math.pow(1 + discountRate, t);
  }, 0);
};

/**
 * Save report to localStorage
 * @param modelType - Type of model (e.g., 'fix-flip', 'single-family-rental')
 * @param report - Report data to save
 */
export const saveToLocalStorage = (
  modelType: string,
  report: Omit<BaseSavedReport, 'id' | 'date' | 'modelType'>
): void => {
  const savedReport: BaseSavedReport = {
    id: Date.now().toString(),
    modelType,
    date: new Date().toISOString(),
    ...report,
  };

  // Get existing reports
  const existing = localStorage.getItem('savedReports');
  const reports: BaseSavedReport[] = existing ? JSON.parse(existing) : [];

  // Add new report to the beginning
  reports.unshift(savedReport);

  // Save back to localStorage
  localStorage.setItem('savedReports', JSON.stringify(reports));
};

/**
 * Load all saved reports from localStorage
 * @returns Array of saved reports
 */
export const loadAllReports = (): BaseSavedReport[] => {
  const saved = localStorage.getItem('savedReports');
  return saved ? JSON.parse(saved) : [];
};

/**
 * Load saved reports for a specific model type
 * @param modelType - Type of model to filter by
 * @returns Array of saved reports for that model
 */
export const loadReportsByModelType = (modelType: string): BaseSavedReport[] => {
  const allReports = loadAllReports();
  return allReports.filter((report) => report.modelType === modelType);
};

/**
 * Delete a saved report
 * @param id - ID of report to delete
 */
export const deleteReport = (id: string): void => {
  const reports = loadAllReports();
  const updated = reports.filter((r) => r.id !== id);
  localStorage.setItem('savedReports', JSON.stringify(updated));
};

/**
 * Calculate equity multiple
 * @param totalReturns - Sum of all positive cash flows
 * @param initialInvestment - Initial investment (negative)
 * @returns Equity multiple (e.g., 2.5x)
 */
export const calculateEquityMultiple = (
  totalReturns: number,
  initialInvestment: number
): number => {
  if (initialInvestment === 0) return 0;
  return totalReturns / Math.abs(initialInvestment);
};

/**
 * Calculate Cap Rate
 * @param noi - Net Operating Income
 * @param propertyValue - Property value or purchase price
 * @returns Cap rate as decimal
 */
export const calculateCapRate = (noi: number, propertyValue: number): number => {
  if (propertyValue === 0) return 0;
  return noi / propertyValue;
};

/**
 * Calculate Cash-on-Cash Return
 * @param annualCashFlow - Annual cash flow
 * @param cashInvested - Total cash invested
 * @returns Cash-on-cash return as decimal
 */
export const calculateCashOnCash = (
  annualCashFlow: number,
  cashInvested: number
): number => {
  if (cashInvested === 0) return 0;
  return annualCashFlow / cashInvested;
};

/**
 * Calculate Debt Service Coverage Ratio (DSCR)
 * @param noi - Net Operating Income
 * @param annualDebtService - Annual debt service
 * @returns DSCR ratio
 */
export const calculateDSCR = (
  noi: number,
  annualDebtService: number
): number => {
  if (annualDebtService === 0) return 0;
  return noi / annualDebtService;
};

/**
 * Calculate Loan-to-Value ratio
 * @param loanAmount - Loan amount
 * @param propertyValue - Property value
 * @returns LTV as decimal
 */
export const calculateLTV = (
  loanAmount: number,
  propertyValue: number
): number => {
  if (propertyValue === 0) return 0;
  return loanAmount / propertyValue;
};

/**
 * Apply growth rate over multiple years
 * @param baseValue - Starting value
 * @param growthRate - Annual growth rate as decimal
 * @param years - Number of years
 * @returns Projected value
 */
export const applyGrowth = (
  baseValue: number,
  growthRate: number,
  years: number
): number => {
  return baseValue * Math.pow(1 + growthRate, years);
};

/**
 * Calculate effective gross income
 * @param grossIncome - Gross potential income
 * @param vacancyRate - Vacancy rate as decimal
 * @param otherIncome - Other income sources
 * @returns Effective gross income
 */
export const calculateEffectiveGrossIncome = (
  grossIncome: number,
  vacancyRate: number,
  otherIncome: number
): number => {
  const vacancyLoss = grossIncome * vacancyRate;
  return grossIncome - vacancyLoss + otherIncome;
};

/**
 * Calculate NOI (Net Operating Income)
 * @param effectiveGrossIncome - Effective gross income
 * @param operatingExpenses - Total operating expenses
 * @returns NOI
 */
export const calculateNOI = (
  effectiveGrossIncome: number,
  operatingExpenses: number
): number => {
  return effectiveGrossIncome - operatingExpenses;
};

/**
 * Calculate simple payback period
 * @param initialInvestment - Initial investment amount
 * @param annualCashFlow - Annual cash flow
 * @returns Years to payback
 */
export const calculatePaybackPeriod = (
  initialInvestment: number,
  annualCashFlow: number
): number => {
  if (annualCashFlow === 0) return Infinity;
  return Math.abs(initialInvestment) / annualCashFlow;
};

/**
 * Round number to specified decimal places
 * @param value - Number to round
 * @param decimals - Number of decimal places
 * @returns Rounded number
 */
export const roundTo = (value: number, decimals: number = 2): number => {
  const multiplier = Math.pow(10, decimals);
  return Math.round(value * multiplier) / multiplier;
};
