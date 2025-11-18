// src/types/valuation.ts
export interface Valuation {
  valuation_id: string;
  company_id: string;
  valuation_date: string;
  valuation_method: 'DCF' | 'Comparable Companies' | 'Precedent Transactions' | 'LBO';
  
  // Valuation outputs
  enterprise_value?: number;
  equity_value?: number;
  implied_share_price?: number;
  
  // DCF inputs
  wacc?: number;
  terminal_growth_rate?: number;
  projection_years?: number;
  
  // Market multiples
  ev_revenue_multiple?: number;
  ev_ebitda_multiple?: number;
  pe_ratio?: number;
  
  // Metadata
  scenario?: 'Base' | 'Upside' | 'Downside';
  notes?: string;
  created_at: string;
  updated_at: string;
}
