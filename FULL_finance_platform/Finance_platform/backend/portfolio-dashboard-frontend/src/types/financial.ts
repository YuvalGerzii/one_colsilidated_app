// src/types/financial.ts
export interface FinancialMetric {
  metric_id: string;
  company_id: string;
  period: string;
  period_start_date: string;
  period_end_date: string;
  
  // Income Statement
  revenue: number;
  cogs?: number;
  gross_profit?: number;
  operating_expenses?: number;
  ebitda?: number;
  depreciation?: number;
  amortization?: number;
  ebit?: number;
  interest_expense?: number;
  taxes?: number;
  net_income?: number;
  
  // Margins
  gross_margin?: number;
  ebitda_margin?: number;
  net_margin?: number;
  
  // Balance Sheet
  cash?: number;
  accounts_receivable?: number;
  inventory?: number;
  current_assets?: number;
  ppe?: number;
  total_assets?: number;
  accounts_payable?: number;
  current_liabilities?: number;
  long_term_debt?: number;
  total_liabilities?: number;
  shareholders_equity?: number;
  
  // Cash Flow
  operating_cash_flow?: number;
  capex?: number;
  free_cash_flow?: number;
  
  // Metadata
  created_at: string;
  updated_at: string;
}

export interface FinancialMetricCreate {
  period: string;
  period_start_date: string;
  period_end_date: string;
  revenue: number;
  [key: string]: any;
}
