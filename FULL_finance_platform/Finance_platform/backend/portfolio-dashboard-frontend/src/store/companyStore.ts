// src/store/companyStore.ts
import create from 'zustand';
import { Company } from '../types/company';

interface CompanyState {
  selectedCompany: Company | null;
  setSelectedCompany: (company: Company | null) => void;
  
  companyFilter: {
    sector?: string;
    status?: string;
    fundId?: string;
  };
  setCompanyFilter: (filter: any) => void;
  clearCompanyFilter: () => void;
}

export const useCompanyStore = create<CompanyState>((set) => ({
  selectedCompany: null,
  setSelectedCompany: (company) => set({ selectedCompany: company }),
  
  companyFilter: {},
  setCompanyFilter: (filter) =>
    set((state) => ({ companyFilter: { ...state.companyFilter, ...filter } })),
  clearCompanyFilter: () => set({ companyFilter: {} }),
}));
