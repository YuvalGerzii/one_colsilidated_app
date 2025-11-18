// src/services/financials.ts
import { apiClient } from './api';
import { FinancialMetric, FinancialMetricCreate } from '../types/financial';

export const financialService = {
  // Get financial metrics for a company
  getByCompany: async (
    companyId: string,
    startDate?: string,
    endDate?: string
  ): Promise<FinancialMetric[]> => {
    const params: any = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    return apiClient.get<FinancialMetric[]>(
      `/companies/${companyId}/financials`,
      { params }
    );
  },

  // Get single period
  getByPeriod: async (
    companyId: string,
    period: string
  ): Promise<FinancialMetric> => {
    return apiClient.get<FinancialMetric>(
      `/companies/${companyId}/financials/${period}`
    );
  },

  // Create financial metric
  create: async (
    companyId: string,
    data: FinancialMetricCreate
  ): Promise<FinancialMetric> => {
    return apiClient.post<FinancialMetric>(
      `/companies/${companyId}/financials`,
      data
    );
  },

  // Update financial metric
  update: async (
    companyId: string,
    period: string,
    data: Partial<FinancialMetricCreate>
  ): Promise<FinancialMetric> => {
    return apiClient.put<FinancialMetric>(
      `/companies/${companyId}/financials/${period}`,
      data
    );
  },

  // Delete financial metric
  delete: async (companyId: string, period: string): Promise<void> => {
    return apiClient.delete<void>(
      `/companies/${companyId}/financials/${period}`
    );
  },

  // Bulk upload from CSV
  uploadCSV: async (
    companyId: string,
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<{ imported: number; errors: string[] }> => {
    return apiClient.upload(
      `/companies/${companyId}/financials/upload`,
      file,
      onProgress
    );
  },
};
