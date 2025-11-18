// src/services/companies.ts
import { apiClient } from './api';
import { Company, CompanyCreate, CompanyUpdate } from '../types/company';

export const companyService = {
  // Get all companies
  getAll: async (fundId?: string): Promise<Company[]> => {
    const params = fundId ? { fund_id: fundId } : {};
    return apiClient.get<Company[]>('/companies', { params });
  },

  // Get single company
  getById: async (companyId: string): Promise<Company> => {
    return apiClient.get<Company>(`/companies/${companyId}`);
  },

  // Create company
  create: async (data: CompanyCreate): Promise<Company> => {
    return apiClient.post<Company>('/companies', data);
  },

  // Update company
  update: async (companyId: string, data: CompanyUpdate): Promise<Company> => {
    return apiClient.put<Company>(`/companies/${companyId}`, data);
  },

  // Delete company
  delete: async (companyId: string): Promise<void> => {
    return apiClient.delete<void>(`/companies/${companyId}`);
  },

  // Get company KPIs
  getKPIs: async (companyId: string): Promise<any> => {
    return apiClient.get<any>(`/companies/${companyId}/kpis`);
  },

  // Get company valuation history
  getValuations: async (companyId: string): Promise<any[]> => {
    return apiClient.get<any[]>(`/companies/${companyId}/valuations`);
  },
};
