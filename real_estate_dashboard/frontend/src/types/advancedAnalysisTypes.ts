// Advanced Analysis Types for Real Estate Calculators

export interface BreakEvenMetrics {
  occupancyBreakEven: number; // Minimum occupancy to cover debt service
  rentBreakEven: number; // Minimum rent for target IRR
  exitCapBreakEven: number; // Maximum exit cap for positive returns
  yearsToBreakEven: number; // Years until cumulative cash flow > 0
  currentOccupancy?: number; // Current value for comparison
  currentRent?: number; // Current value for comparison
  currentExitCap?: number; // Current value for comparison
  safetyMargins: {
    occupancy: number; // % above break-even
    rent: number; // % above break-even
    exitCap: number; // % below break-even
  };
}

export interface StressScenario {
  id: string;
  name: string;
  description: string;
  icon?: string;
  color: string;
  adjustments: {
    rentGrowth?: number; // % change (e.g., -0.02 means -2%)
    vacancyRate?: number; // % point change (e.g., 0.05 means +5 percentage points)
    exitCapRate?: number; // % point change (e.g., 0.02 means +200 bps)
    expenseGrowth?: number; // % change (e.g., 0.04 means +4%)
    interestRate?: number; // % point change (e.g., 0.02 means +200 bps)
    renovationCosts?: number; // % change
    adrGrowth?: number; // % change (for hotels)
    occupancyRate?: number; // % point change (for hotels)
    propertyValueAdjustment?: number; // % change (e.g., -0.30 means -30%)
  };
}

export interface ScenarioResult {
  scenarioId: string;
  scenarioName: string;
  irr: number;
  equityMultiple: number;
  exitValue: number;
  noi: number;
  cashFlow: number;
  dscr: number;
  metrics: {
    [key: string]: number | string;
  };
}

export interface TornadoChartData {
  variable: string;
  displayName: string;
  lowValue: number;
  baseValue: number;
  highValue: number;
  range: number;
  impact: number;
}

export interface StressTestResults {
  baseCase: ScenarioResult;
  scenarios: ScenarioResult[];
  worstCase: ScenarioResult;
  bestCase: ScenarioResult;
  sensitivityRanking: TornadoChartData[];
}

export interface WaterfallData {
  label: string;
  value: number;
  cumulative: number;
  color: string;
  category: 'start' | 'increase' | 'decrease' | 'total';
  details?: {
    description: string;
    tooltip: string;
  };
}

export interface WaterfallConfig {
  type: 'returns' | 'noi' | 'cashflow';
  showCumulative: boolean;
  colorScheme: 'default' | 'custom';
}

export interface MonteCarloVariable {
  name: string;
  displayName: string;
  baseValue: number;
  distribution: 'normal' | 'triangular' | 'uniform' | 'beta';
  params: {
    // Normal: mean, stdDev
    // Triangular: min, mode, max
    // Uniform: min, max
    // Beta: alpha, beta, min, max
    [key: string]: number;
  };
  enabled: boolean;
  unit: string; // '%' | '$' | 'years'
}

export interface MonteCarloConfig {
  numSimulations: number;
  randomSeed?: number;
  variables: MonteCarloVariable[];
  correlations?: Array<{
    var1: string;
    var2: string;
    correlation: number; // -1 to 1
  }>;
  targetMetrics: string[]; // e.g., ['irr', 'exitValue', 'equityMultiple']
}

export interface MonteCarloSimulationResult {
  simulationId: number;
  inputs: { [variableName: string]: number };
  outputs: { [metricName: string]: number };
}

export interface MonteCarloResults {
  config: MonteCarloConfig;
  simulationResults: MonteCarloSimulationResult[];
  statistics: {
    [metricName: string]: {
      mean: number;
      median: number;
      stdDev: number;
      min: number;
      max: number;
      p10: number; // 10th percentile
      p25: number;
      p75: number;
      p90: number; // 90th percentile
      p95: number;
    };
  };
  sensitivityAnalysis: Array<{
    variable: string;
    correlation: number; // Correlation with target metric (e.g., IRR)
    impact: number; // Standardized impact score
    rank: number;
  }>;
  probabilityAnalysis: {
    [condition: string]: number; // e.g., 'irr > 15%': 0.85 (85% probability)
  };
  histogramData: Array<{
    bin: string;
    count: number;
    frequency: number;
  }>;
}

export interface DistributionParams {
  normal: { mean: number; stdDev: number };
  triangular: { min: number; mode: number; max: number };
  uniform: { min: number; max: number };
  beta: { alpha: number; beta: number; min: number; max: number };
}

// Helper type for scenario comparison
export interface ScenarioComparison {
  scenarios: ScenarioResult[];
  comparisonMetrics: string[];
  relativeDifferences: {
    [scenarioId: string]: {
      [metric: string]: number; // % difference from base case
    };
  };
}
