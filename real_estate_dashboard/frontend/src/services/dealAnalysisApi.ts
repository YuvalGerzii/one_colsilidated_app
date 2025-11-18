/**
 * Deal Analysis API Service
 *
 * Provides API calls for comprehensive deal analysis:
 * - Comprehensive deal scoring
 * - Multi-deal comparison
 * - Break-even occupancy
 * - Quick scoring
 *
 * All analysis is FREE - no API keys required.
 */

import { apiClient } from './apiClient';

// ========================================
// TYPE DEFINITIONS
// ========================================

export interface DealInputs {
  purchase_price: number;
  annual_income: number;
  annual_expenses: number;
  down_payment_pct?: number;
  interest_rate?: number;
  loan_term_years?: number;
  closing_costs?: number;
  rehab_costs?: number;
  vacancy_rate?: number;
  location_quality?: number;
  market_growth_rate?: number;
}

export interface InvestorCriteria {
  min_cap_rate?: number;
  min_cash_on_cash?: number;
  min_dscr?: number;
  max_down_payment_pct?: number;
}

export interface DealAnalysisRequest {
  deal_inputs: DealInputs;
  property_type?: string;
  investor_criteria?: InvestorCriteria;
}

export interface KeyMetrics {
  cap_rate: number;
  cash_on_cash_return: number;
  dscr: number;
  noi: number;
  annual_debt_service: number;
  total_cash_invested: number;
}

export interface Scores {
  financial_score: number;
  risk_score: number;
  market_score: number;
}

export interface CriteriaCheck {
  all_criteria_met: boolean;
  details: Record<string, any>;
  summary: string;
}

export interface DealAnalysisResult {
  overall_score: number;
  rating: string;
  recommendation: string;
  emoji: string;
  scores: Scores;
  key_metrics: KeyMetrics;
  criteria_check: CriteriaCheck;
  strengths: string[];
  weaknesses: string[];
  property_type: string;
}

export interface DealAnalysisResponse {
  success: boolean;
  data: DealAnalysisResult;
  property_type: string;
}

export interface Deal {
  name: string;
  deal_inputs: DealInputs;
  property_type: string;
  investor_criteria?: InvestorCriteria;
}

export interface MultiDealComparisonRequest {
  deals: Deal[];
}

export interface DealComparisonResult {
  name: string;
  analysis: DealAnalysisResult;
}

export interface ComparisonStatistics {
  avg_overall_score: number;
  avg_cap_rate: number;
  avg_cash_on_cash: number;
  avg_dscr: number;
  score_range: number;
}

export interface MultiDealComparisonResponse {
  success: boolean;
  data: {
    deals: DealComparisonResult[];
    best_deal: DealComparisonResult;
    rankings: { rank: number; name: string; overall_score: number }[];
    statistics: ComparisonStatistics;
  };
}

export interface BreakEvenOccupancyRequest {
  annual_income: number;
  annual_expenses: number;
  annual_debt_service: number;
  current_occupancy?: number;
}

export interface BreakEvenOccupancyResponse {
  success: boolean;
  data: {
    break_even_occupancy: number;
    current_occupancy: number;
    safety_margin: number;
    risk_level: string;
    monthly_cushion: number;
  };
}

export interface QuickScoreRequest {
  cap_rate: number;
  cash_on_cash: number;
  dscr: number;
  property_type?: string;
}

export interface QuickScoreResponse {
  success: boolean;
  data: {
    overall_score: number;
    rating: string;
    emoji: string;
    metrics: {
      cap_rate: number;
      cash_on_cash: number;
      dscr: number;
    };
    strengths: string[];
    weaknesses: string[];
    property_type: string;
  };
}

export interface DealTemplate {
  success: boolean;
  property_type: string;
  template: {
    deal_inputs: DealInputs;
    property_type: string;
    investor_criteria?: InvestorCriteria;
    notes?: string;
  };
}

// ========================================
// API FUNCTIONS
// ========================================

export const dealAnalysisApi = {
  /**
   * Comprehensive Deal Analysis
   * Analyzes a real estate deal and provides scores, metrics, and recommendations
   */
  analyzeDeal: async (request: DealAnalysisRequest): Promise<DealAnalysisResponse> => {
    const response = await apiClient.post('/deal-analysis/analyze', request);
    return response.data;
  },

  /**
   * Multi-Deal Comparison
   * Compare multiple deals side-by-side
   */
  compareDeals: async (request: MultiDealComparisonRequest): Promise<MultiDealComparisonResponse> => {
    const response = await apiClient.post('/deal-analysis/compare', request);
    return response.data;
  },

  /**
   * Break-Even Occupancy Calculator
   * Calculate minimum occupancy needed to cover expenses and debt
   */
  breakEvenOccupancy: async (request: BreakEvenOccupancyRequest): Promise<BreakEvenOccupancyResponse> => {
    const response = await apiClient.post('/deal-analysis/break-even', request);
    return response.data;
  },

  /**
   * Quick Deal Score
   * Fast scoring when you only have basic metrics
   */
  quickScore: async (params: QuickScoreRequest): Promise<QuickScoreResponse> => {
    const response = await apiClient.post('/deal-analysis/quick-score', null, { params });
    return response.data;
  },

  /**
   * Get Deal Template
   * Pre-configured deal templates for common property types
   */
  getTemplate: async (propertyType: 'multifamily' | 'single_family' | 'commercial' | 'fix_and_flip'): Promise<DealTemplate> => {
    const response = await apiClient.get(`/deal-analysis/templates/${propertyType}`);
    return response.data;
  },
};
