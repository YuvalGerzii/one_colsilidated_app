import { StressScenario } from '../types/advancedAnalysisTypes';

/**
 * Preset stress testing scenarios for sensitivity analysis
 * Each scenario adjusts key variables to test investment performance under different market conditions
 */

export const STRESS_SCENARIOS: StressScenario[] = [
  {
    id: 'base-case',
    name: 'Base Case',
    description: 'Current assumptions with no adjustments',
    color: '#3b82f6',
    adjustments: {},
  },
  {
    id: 'recession',
    name: 'Recession',
    description: 'Economic downturn: 30% property value drop, 20% occupancy decline, negative rent growth',
    color: '#ef4444',
    adjustments: {
      rentGrowth: -0.02, // -2% rent growth
      vacancyRate: 0.20, // +20% vacancy (e.g., 5% becomes 25%)
      exitCapRate: 0.02, // +200 bps exit cap (e.g., 5% becomes 7%)
      expenseGrowth: 0.04, // +4% expense growth
      propertyValueAdjustment: -0.30, // -30% property value
    },
  },
  {
    id: 'high-inflation',
    name: 'High Inflation',
    description: 'Elevated inflation: Expenses surge 6%, interest rates up, moderate rent growth',
    color: '#f59e0b',
    adjustments: {
      rentGrowth: 0.04, // +4% rent growth (lags inflation)
      expenseGrowth: 0.06, // +6% expense growth
      interestRate: 0.02, // +200 bps interest rate
      exitCapRate: 0.015, // +150 bps exit cap
      vacancyRate: 0.05, // +5% vacancy
    },
  },
  {
    id: 'market-downturn',
    name: 'Market Downturn',
    description: 'Weak demand: Stagnant rents, elevated vacancy, compressed cap rates',
    color: '#f97316',
    adjustments: {
      rentGrowth: 0, // 0% rent growth
      vacancyRate: 0.15, // +15% vacancy
      exitCapRate: 0.015, // +150 bps exit cap
      expenseGrowth: 0.03, // +3% expense growth
      propertyValueAdjustment: -0.15, // -15% property value
    },
  },
  {
    id: 'stagflation',
    name: 'Stagflation',
    description: 'Worst case: Stagnant economy with high inflation, rising costs, weak demand',
    color: '#dc2626',
    adjustments: {
      rentGrowth: -0.01, // -1% rent growth
      vacancyRate: 0.15, // +15% vacancy
      expenseGrowth: 0.07, // +7% expense growth
      interestRate: 0.025, // +250 bps interest rate
      exitCapRate: 0.025, // +250 bps exit cap
      propertyValueAdjustment: -0.25, // -25% property value
    },
  },
  {
    id: 'moderate-stress',
    name: 'Moderate Stress',
    description: 'Mild headwinds: Slower growth, slightly elevated costs and vacancy',
    color: '#fb923c',
    adjustments: {
      rentGrowth: 0.015, // +1.5% rent growth
      vacancyRate: 0.08, // +8% vacancy
      expenseGrowth: 0.04, // +4% expense growth
      exitCapRate: 0.01, // +100 bps exit cap
    },
  },
  {
    id: 'best-case',
    name: 'Best Case',
    description: 'Strong economy: Robust rent growth, low vacancy, favorable cap rate compression',
    color: '#10b981',
    adjustments: {
      rentGrowth: 0.06, // +6% rent growth
      vacancyRate: -0.03, // -3% vacancy (improved occupancy)
      expenseGrowth: 0.02, // +2% expense growth (controlled costs)
      exitCapRate: -0.01, // -100 bps exit cap (cap rate compression)
      propertyValueAdjustment: 0.20, // +20% property value
    },
  },
];

/**
 * Get a scenario by ID
 */
export const getScenarioById = (id: string): StressScenario | undefined => {
  return STRESS_SCENARIOS.find(scenario => scenario.id === id);
};

/**
 * Get all scenarios except base case
 */
export const getStressScenarios = (): StressScenario[] => {
  return STRESS_SCENARIOS.filter(scenario => scenario.id !== 'base-case');
};

/**
 * Get scenario color by ID
 */
export const getScenarioColor = (id: string): string => {
  const scenario = getScenarioById(id);
  return scenario?.color || '#6b7280';
};

/**
 * Format adjustment value for display
 */
export const formatAdjustment = (value: number, type: 'percent' | 'bps' | 'multiplier'): string => {
  switch (type) {
    case 'percent':
      return `${value > 0 ? '+' : ''}${(value * 100).toFixed(1)}%`;
    case 'bps':
      return `${value > 0 ? '+' : ''}${(value * 10000).toFixed(0)} bps`;
    case 'multiplier':
      return `${value > 0 ? '+' : ''}${(value * 100).toFixed(0)}%`;
    default:
      return value.toString();
  }
};
