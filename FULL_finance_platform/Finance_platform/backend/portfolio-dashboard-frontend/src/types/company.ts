// src/types/company.ts
export interface Company {
  company_id: string;
  fund_id: string;
  company_name: string;
  company_legal_name?: string;
  ticker_symbol?: string;
  website?: string;
  
  // Investment details
  investment_date: string;
  deal_type: 'LBO' | 'Growth' | 'Minority' | 'Venture' | 'Other';
  sector: string;
  industry?: string;
  sub_sector?: string;
  business_description?: string;
  
  // Location
  headquarters_city?: string;
  headquarters_state?: string;
  headquarters_country?: string;
  
  // Financial snapshot
  entry_revenue?: number;
  entry_ebitda?: number;
  entry_multiple?: number;
  purchase_price?: number;
  equity_invested?: number;
  debt_raised?: number;
  ownership_percentage?: number;
  
  // Status
  company_status: 'Active' | 'Exited' | 'Written Off';
  exit_date?: string;
  exit_type?: string;
  exit_multiple?: number;
  realized_irr?: number;
  realized_moic?: number;
  
  // Metadata
  created_at: string;
  updated_at: string;
}

export interface CompanyCreate {
  fund_id: string;
  company_name: string;
  investment_date: string;
  deal_type: string;
  sector: string;
  equity_invested: number;
  ownership_percentage: number;
  [key: string]: any;
}

export interface CompanyUpdate {
  [key: string]: any;
}
