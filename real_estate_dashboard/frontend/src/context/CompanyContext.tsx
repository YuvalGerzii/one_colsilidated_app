import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api/v1';

// Types
export interface Company {
  id: string;
  name: string;
  details?: string;
  region?: string;
  contact_info?: string;
  logo_url?: string;
  created_at: string;
  updated_at: string;
  property_count: number;
}

export interface CompanySummary {
  id: string;
  name: string;
  region?: string;
}

interface CompanyContextValue {
  selectedCompany: Company | null;
  companies: CompanySummary[];
  loading: boolean;
  error: string | null;
  selectCompany: (company: Company | null) => void;
  refreshCompanies: () => Promise<void>;
  createCompany: (data: CreateCompanyData) => Promise<Company>;
}

export interface CreateCompanyData {
  name: string;
  details?: string;
  region?: string;
  contact_info?: string;
  logo_url?: string;
}

// Create context with undefined default
const CompanyContext = createContext<CompanyContextValue | undefined>(undefined);

// LocalStorage key
const SELECTED_COMPANY_KEY = 'selectedCompany';

// Provider component
export const CompanyProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [companies, setCompanies] = useState<CompanySummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load companies from API
  const refreshCompanies = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get<CompanySummary[]>(`${API_BASE_URL}/companies/summary`);
      setCompanies(response.data);
    } catch (err) {
      console.error('Failed to load companies:', err);
      setError('Failed to load companies');
    } finally {
      setLoading(false);
    }
  };

  // Create a new company
  const createCompany = async (data: CreateCompanyData): Promise<Company> => {
    try {
      const response = await axios.post<Company>(`${API_BASE_URL}/companies/`, data);
      await refreshCompanies(); // Refresh the list
      return response.data;
    } catch (err: any) {
      console.error('Failed to create company:', err);
      throw new Error(err.response?.data?.detail || 'Failed to create company');
    }
  };

  // Select a company and persist to localStorage
  const selectCompany = (company: Company | null) => {
    setSelectedCompany(company);
    if (company) {
      localStorage.setItem(SELECTED_COMPANY_KEY, JSON.stringify(company));
    } else {
      localStorage.removeItem(SELECTED_COMPANY_KEY);
    }
  };

  // Initialize: Load companies and restore selected company from localStorage
  useEffect(() => {
    const init = async () => {
      await refreshCompanies();

      // Try to restore selected company from localStorage
      const savedCompanyStr = localStorage.getItem(SELECTED_COMPANY_KEY);
      if (savedCompanyStr) {
        try {
          const savedCompany: Company = JSON.parse(savedCompanyStr);
          // Fetch fresh data for the saved company
          const response = await axios.get<Company>(`${API_BASE_URL}/companies/${savedCompany.id}`);
          setSelectedCompany(response.data);
        } catch (err) {
          console.error('Failed to restore company:', err);
          localStorage.removeItem(SELECTED_COMPANY_KEY);
        }
      }
    };

    init();
  }, []);

  const value: CompanyContextValue = {
    selectedCompany,
    companies,
    loading,
    error,
    selectCompany,
    refreshCompanies,
    createCompany,
  };

  return <CompanyContext.Provider value={value}>{children}</CompanyContext.Provider>;
};

// Custom hook for using the company context
export const useCompany = (): CompanyContextValue => {
  const context = useContext(CompanyContext);
  if (context === undefined) {
    throw new Error('useCompany must be used within a CompanyProvider');
  }
  return context;
};
