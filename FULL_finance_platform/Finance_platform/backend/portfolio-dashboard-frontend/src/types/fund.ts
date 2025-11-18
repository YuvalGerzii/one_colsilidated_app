// src/types/fund.ts
export interface Fund {
  fund_id: string;
  fund_name: string;
  fund_number?: number;
  vintage_year: number;
  fund_size: number;
  committed_capital: number;
  drawn_capital: number;
  distributed_capital: number;
  target_irr?: number;
  fund_strategy?: string;
  sector_focus?: string[];
  geographic_focus?: string[];
  fund_status: 'Fundraising' | 'Active' | 'Harvesting' | 'Closed';
  inception_date?: string;
  close_date?: string;
  final_close_date?: string;
  created_at: string;
  updated_at: string;
}
