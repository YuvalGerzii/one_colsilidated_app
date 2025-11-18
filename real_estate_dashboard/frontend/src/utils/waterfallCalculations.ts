import { WaterfallData } from '../types/advancedAnalysisTypes';

/**
 * Calculate returns waterfall showing how value flows from equity to total return
 * @param equityInvested Initial equity investment
 * @param totalCashFlows Sum of all operating cash flows during hold period
 * @param debtPaydown Amount of loan principal paid down
 * @param appreciation Property value increase
 * @param exitProceeds Net proceeds from sale
 * @returns Array of waterfall data for visualization
 */
export function calculateReturnsWaterfall(
  equityInvested: number,
  totalCashFlows: number,
  debtPaydown: number,
  appreciation: number,
  exitProceeds: number
): WaterfallData[] {
  const waterfall: WaterfallData[] = [];
  let cumulative = 0;

  // Starting point - Equity Investment (negative, it's an outflow)
  waterfall.push({
    label: 'Equity Invested',
    value: -equityInvested,
    cumulative: -equityInvested,
    color: '#ef4444',
    category: 'start',
    details: {
      description: 'Initial capital invested',
      tooltip: `Down payment + closing costs + renovation costs`,
    },
  });
  cumulative = -equityInvested;

  // Operating Cash Flows
  if (totalCashFlows !== 0) {
    cumulative += totalCashFlows;
    waterfall.push({
      label: 'Operating Cash Flow',
      value: totalCashFlows,
      cumulative,
      color: totalCashFlows >= 0 ? '#10b981' : '#ef4444',
      category: totalCashFlows >= 0 ? 'increase' : 'decrease',
      details: {
        description: 'Cumulative cash flow from operations',
        tooltip: `NOI minus debt service over ${Math.round(totalCashFlows / 12)} years`,
      },
    });
  }

  // Debt Paydown (equity buildup)
  if (debtPaydown > 0) {
    cumulative += debtPaydown;
    waterfall.push({
      label: 'Debt Paydown',
      value: debtPaydown,
      cumulative,
      color: '#3b82f6',
      category: 'increase',
      details: {
        description: 'Principal reduction builds equity',
        tooltip: `Loan balance reduced from ${formatCurrency(debtPaydown)} to less`,
      },
    });
  }

  // Property Appreciation
  if (appreciation !== 0) {
    cumulative += appreciation;
    waterfall.push({
      label: 'Appreciation',
      value: appreciation,
      cumulative,
      color: appreciation >= 0 ? '#8b5cf6' : '#f59e0b',
      category: appreciation >= 0 ? 'increase' : 'decrease',
      details: {
        description: appreciation >= 0 ? 'Property value increase' : 'Property value decrease',
        tooltip: `Value change from NOI growth and cap rate movement`,
      },
    });
  }

  // Total Return
  waterfall.push({
    label: 'Total Return',
    value: cumulative,
    cumulative,
    color: cumulative >= 0 ? '#10b981' : '#ef4444',
    category: 'total',
    details: {
      description: 'Net profit after sale',
      tooltip: `Total gain on ${formatCurrency(equityInvested)} invested`,
    },
  });

  return waterfall;
}

/**
 * Calculate NOI buildup waterfall showing revenue → expenses → NOI
 */
export function calculateNoiBuildupWaterfall(
  grossPotentialRent: number,
  otherIncome: number,
  vacancyLoss: number,
  operatingExpenses: number
): WaterfallData[] {
  const waterfall: WaterfallData[] = [];
  let cumulative = 0;

  // Gross Potential Rent
  cumulative = grossPotentialRent;
  waterfall.push({
    label: 'Gross Potential Rent',
    value: grossPotentialRent,
    cumulative,
    color: '#10b981',
    category: 'start',
    details: {
      description: 'Maximum rent at 100% occupancy',
      tooltip: 'Total rent if fully leased year-round',
    },
  });

  // Other Income
  if (otherIncome > 0) {
    cumulative += otherIncome;
    waterfall.push({
      label: 'Other Income',
      value: otherIncome,
      cumulative,
      color: '#3b82f6',
      category: 'increase',
      details: {
        description: 'Parking, laundry, pet fees, etc.',
        tooltip: 'Ancillary revenue streams',
      },
    });
  }

  // Vacancy Loss
  if (vacancyLoss > 0) {
    cumulative -= vacancyLoss;
    waterfall.push({
      label: 'Vacancy Loss',
      value: -vacancyLoss,
      cumulative,
      color: '#f59e0b',
      category: 'decrease',
      details: {
        description: 'Lost rent from vacant units',
        tooltip: 'Economic vacancy and bad debt',
      },
    });
  }

  // Operating Expenses
  cumulative -= operatingExpenses;
  waterfall.push({
    label: 'Operating Expenses',
    value: -operatingExpenses,
    cumulative,
    color: '#ef4444',
    category: 'decrease',
    details: {
      description: 'Property management, maintenance, taxes, insurance',
      tooltip: 'All costs to operate the property',
    },
  });

  // NOI (final result)
  waterfall.push({
    label: 'Net Operating Income',
    value: cumulative,
    cumulative,
    color: cumulative >= 0 ? '#10b981' : '#ef4444',
    category: 'total',
    details: {
      description: 'Revenue minus operating expenses',
      tooltip: 'Cash available for debt service',
    },
  });

  return waterfall;
}

/**
 * Calculate cash flow waterfall: NOI → Debt Service → Cash Flow
 */
export function calculateCashFlowWaterfall(
  noi: number,
  debtService: number,
  capex: number = 0
): WaterfallData[] {
  const waterfall: WaterfallData[] = [];
  let cumulative = noi;

  // Starting with NOI
  waterfall.push({
    label: 'Net Operating Income',
    value: noi,
    cumulative,
    color: '#10b981',
    category: 'start',
    details: {
      description: 'Annual NOI',
      tooltip: 'Cash available before debt service',
    },
  });

  // Debt Service
  cumulative -= debtService;
  waterfall.push({
    label: 'Debt Service',
    value: -debtService,
    cumulative,
    color: '#ef4444',
    category: 'decrease',
    details: {
      description: 'Annual mortgage payments',
      tooltip: 'Principal + interest payments',
    },
  });

  // CapEx (if applicable)
  if (capex > 0) {
    cumulative -= capex;
    waterfall.push({
      label: 'CapEx Reserves',
      value: -capex,
      cumulative,
      color: '#f59e0b',
      category: 'decrease',
      details: {
        description: 'Capital expenditure reserves',
        tooltip: 'Set aside for major repairs',
      },
    });
  }

  // Cash Flow (final result)
  waterfall.push({
    label: 'Cash Flow',
    value: cumulative,
    cumulative,
    color: cumulative >= 0 ? '#10b981' : '#ef4444',
    category: 'total',
    details: {
      description: 'Net cash to investors',
      tooltip: 'Annual distributable cash',
    },
  });

  return waterfall;
}

/**
 * Calculate development cost waterfall (for development projects)
 */
export function calculateDevelopmentCostWaterfall(
  landCost: number,
  hardCosts: number,
  softCosts: number,
  financing: number,
  contingency: number
): WaterfallData[] {
  const waterfall: WaterfallData[] = [];
  let cumulative = 0;

  // Land
  cumulative = landCost;
  waterfall.push({
    label: 'Land Acquisition',
    value: landCost,
    cumulative,
    color: '#8b5cf6',
    category: 'start',
    details: {
      description: 'Land purchase price',
      tooltip: 'Site acquisition cost',
    },
  });

  // Hard Costs
  cumulative += hardCosts;
  waterfall.push({
    label: 'Hard Costs',
    value: hardCosts,
    cumulative,
    color: '#3b82f6',
    category: 'increase',
    details: {
      description: 'Construction & materials',
      tooltip: 'Brick and mortar costs',
    },
  });

  // Soft Costs
  cumulative += softCosts;
  waterfall.push({
    label: 'Soft Costs',
    value: softCosts,
    cumulative,
    color: '#f59e0b',
    category: 'increase',
    details: {
      description: 'Architecture, permits, fees',
      tooltip: 'Professional services and permits',
    },
  });

  // Financing
  cumulative += financing;
  waterfall.push({
    label: 'Financing Costs',
    value: financing,
    cumulative,
    color: '#ef4444',
    category: 'increase',
    details: {
      description: 'Loan fees and interest',
      tooltip: 'Lender fees and carry costs',
    },
  });

  // Contingency
  cumulative += contingency;
  waterfall.push({
    label: 'Contingency',
    value: contingency,
    cumulative,
    color: '#f97316',
    category: 'increase',
    details: {
      description: 'Reserve for overruns',
      tooltip: 'Buffer for unexpected costs',
    },
  });

  // Total
  waterfall.push({
    label: 'Total Project Cost',
    value: cumulative,
    cumulative,
    color: '#6b7280',
    category: 'total',
    details: {
      description: 'All-in development cost',
      tooltip: 'Complete project budget',
    },
  });

  return waterfall;
}

/**
 * Format currency for display
 */
function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Math.abs(value));
}

/**
 * Calculate equity multiple from waterfall data
 */
export function calculateEquityMultipleFromWaterfall(waterfall: WaterfallData[]): number {
  const equityInvested = Math.abs(waterfall[0]?.value || 0);
  const totalReturn = waterfall[waterfall.length - 1]?.value || 0;

  if (equityInvested === 0) return 0;
  return (totalReturn + equityInvested) / equityInvested;
}
