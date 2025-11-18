/**
 * Sensitivity Analysis API Service
 *
 * Provides API calls for comprehensive sensitivity analysis:
 * - One-way sensitivity (tornado charts)
 * - Two-way sensitivity (heat maps)
 * - Monte Carlo simulations
 * - Scenario analysis
 * - Break-even analysis
 *
 * All analysis is FREE - no API keys required.
 */

import { apiClient } from './apiClient';

// ========================================
// TYPE DEFINITIONS
// ========================================

export interface Variable {
  name: string;
  label: string;
  base_value: number;
  min: number;
  max: number;
  unit?: string;
}

export interface Scenario {
  name: string;
  description: string;
  adjustments: Record<string, any>;
}

export interface OneWaySensitivityRequest {
  base_inputs: Record<string, number>;
  variables: Variable[];
  metric_type: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  metric_name: string;
}

export interface TwoWaySensitivityRequest {
  base_inputs: Record<string, number>;
  metric_type: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  x_variable: Variable;
  y_variable: Variable;
  steps?: number;
}

export interface MonteCarloRequest {
  base_inputs: Record<string, number>;
  variables: Variable[];
  metric_type: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  iterations?: number;
  distribution?: 'normal' | 'uniform' | 'triangular';
}

export interface ScenarioAnalysisRequest {
  base_inputs: Record<string, number>;
  metric_type: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  scenarios: Scenario[];
}

export interface BreakEvenRequest {
  base_inputs: Record<string, number>;
  variables: Variable[];
  metric_type: 'cash_on_cash' | 'cap_rate' | 'dscr' | 'irr';
  target_metric: number;
}

// Response types
export interface SensitivityVariableResult {
  variable_name: string;
  variable_label: string;
  base_value: number;
  min_value: number;
  max_value: number;
  metric_at_min: number;
  metric_at_max: number;
  metric_range: number;
  impact_percentage: number;
  rank: number;
}

export interface OneWaySensitivityResponse {
  success: boolean;
  data: {
    base_metric: number;
    metric_name: string;
    variables: SensitivityVariableResult[];
  };
  metric_type: string;
}

export interface TwoWaySensitivityResponse {
  success: boolean;
  data: {
    x_variable: { name: string; label: string; values: number[] };
    y_variable: { name: string; label: string; values: number[] };
    results: number[][];
    statistics: {
      min: number;
      max: number;
      mean: number;
      range: number;
    };
  };
  metric_type: string;
}

export interface MonteCarloResponse {
  success: boolean;
  data: {
    statistics: {
      mean: number;
      median: number;
      std: number;
      percentile_5: number;
      percentile_25: number;
      percentile_50: number;
      percentile_75: number;
      percentile_95: number;
      coefficient_of_variation: number;
    };
    risk_metrics: {
      probability_of_loss: number;
      value_at_risk_95: number;
      expected_shortfall: number;
    };
    histogram: { bin_start: number; bin_end: number; count: number; bin_center: number }[];
    iterations: number;
    distribution: string;
  };
  metric_type: string;
}

export interface ScenarioResult {
  name: string;
  description: string;
  metric_value: number;
  vs_base: number;
  vs_base_pct: number;
  adjustments_applied: Record<string, any>;
}

export interface ScenarioAnalysisResponse {
  success: boolean;
  data: {
    base_case: { name: string; metric_value: number };
    scenarios: ScenarioResult[];
  };
  metric_type: string;
}

export interface BreakEvenResult {
  variable_name: string;
  variable_label: string;
  base_value: number;
  break_even_value: number;
  change_required: number;
  change_required_pct: number;
  difficulty: string;
  achievable: boolean;
}

export interface BreakEvenResponse {
  success: boolean;
  data: {
    target_metric: number;
    base_metric: number;
    variables: BreakEvenResult[];
  };
  metric_type: string;
}

export interface PropertyTemplate {
  success: boolean;
  property_type: string;
  template: {
    variables: Variable[];
    scenarios?: Scenario[];
  };
}

// ========================================
// API FUNCTIONS
// ========================================

export const sensitivityAnalysisApi = {
  /**
   * One-Way Sensitivity Analysis (Tornado Chart)
   * Shows which variables have the biggest impact on the output
   */
  oneWaySensitivity: async (request: OneWaySensitivityRequest): Promise<OneWaySensitivityResponse> => {
    const response = await apiClient.post('/sensitivity-analysis/one-way', request);
    return response.data;
  },

  /**
   * Two-Way Sensitivity Analysis (Heat Map)
   * Shows interaction between two variables
   */
  twoWaySensitivity: async (request: TwoWaySensitivityRequest): Promise<TwoWaySensitivityResponse> => {
    const response = await apiClient.post('/sensitivity-analysis/two-way', request);
    return response.data;
  },

  /**
   * Monte Carlo Simulation
   * Runs thousands of simulations with random variations
   */
  monteCarlo: async (request: MonteCarloRequest): Promise<MonteCarloResponse> => {
    const response = await apiClient.post('/sensitivity-analysis/monte-carlo', request);
    return response.data;
  },

  /**
   * Scenario Analysis
   * Compare predefined scenarios (Base, Optimistic, Pessimistic, etc.)
   */
  scenarios: async (request: ScenarioAnalysisRequest): Promise<ScenarioAnalysisResponse> => {
    const response = await apiClient.post('/sensitivity-analysis/scenarios', request);
    return response.data;
  },

  /**
   * Break-Even Analysis
   * Find exact values needed to hit target metric
   */
  breakEven: async (request: BreakEvenRequest): Promise<BreakEvenResponse> => {
    const response = await apiClient.post('/sensitivity-analysis/break-even', request);
    return response.data;
  },

  /**
   * Get Property Template
   * Pre-configured variables for common property types
   */
  getTemplate: async (propertyType: 'multifamily' | 'single_family' | 'commercial' | 'fix_and_flip'): Promise<PropertyTemplate> => {
    const response = await apiClient.get(`/sensitivity-analysis/templates/${propertyType}`);
    return response.data;
  },
};
