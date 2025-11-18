/**
 * Custom React Hooks for Portfolio Dashboard API Integration
 * 
 * These hooks provide easy-to-use interfaces for API operations with:
 * - Automatic loading states
 * - Error handling
 * - Toast notifications
 * - Data caching (via React Query)
 */

import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient, UseQueryOptions } from 'react-query';
import companyService, { Company, CompanyCreate, CompanyUpdate } from '../services/companyService';
import financialService, { FinancialMetric, FinancialMetricCreate } from '../services/financialService';
import modelService, { ModelGenerationRequest, BatchModelRequest } from '../services/modelService';

// ======================
// COMPANY HOOKS
// ======================

/**
 * Hook to fetch all companies
 */
export function useCompanies(filters?: {
  fund_id?: string;
  status?: string;
  sector?: string;
}) {
  return useQuery(
    ['companies', filters],
    () => companyService.getCompanies(filters),
    {
      staleTime: 30000, // Consider data fresh for 30 seconds
      cacheTime: 300000, // Keep in cache for 5 minutes
    }
  );
}

/**
 * Hook to fetch single company
 */
export function useCompany(companyId: string) {
  return useQuery(
    ['company', companyId],
    () => companyService.getCompany(companyId),
    {
      enabled: !!companyId, // Only fetch if companyId is provided
    }
  );
}

/**
 * Hook to create a company
 */
export function useCreateCompany() {
  const queryClient = useQueryClient();

  return useMutation(
    (company: CompanyCreate) => companyService.createCompany(company),
    {
      onSuccess: () => {
        // Invalidate companies list to refetch
        queryClient.invalidateQueries(['companies']);
      },
    }
  );
}

/**
 * Hook to update a company
 */
export function useUpdateCompany() {
  const queryClient = useQueryClient();

  return useMutation(
    ({ companyId, updates }: { companyId: string; updates: CompanyUpdate }) =>
      companyService.updateCompany(companyId, updates),
    {
      onSuccess: (data, variables) => {
        // Invalidate specific company and companies list
        queryClient.invalidateQueries(['company', variables.companyId]);
        queryClient.invalidateQueries(['companies']);
      },
    }
  );
}

/**
 * Hook to delete a company
 */
export function useDeleteCompany() {
  const queryClient = useQueryClient();

  return useMutation(
    (companyId: string) => companyService.deleteCompany(companyId),
    {
      onSuccess: () => {
        // Invalidate companies list
        queryClient.invalidateQueries(['companies']);
      },
    }
  );
}

/**
 * Hook to get company summary statistics
 */
export function useCompanySummary(fundId?: string) {
  return useQuery(
    ['company-summary', fundId],
    () => companyService.getCompanySummary(fundId)
  );
}

// ======================
// FINANCIAL HOOKS
// ======================

/**
 * Hook to fetch financial metrics
 */
export function useFinancials(params: {
  company_id: string;
  period_type?: 'Quarterly' | 'Annual' | 'TTM';
  start_date?: string;
  end_date?: string;
  limit?: number;
}) {
  return useQuery(
    ['financials', params],
    () => financialService.getFinancials(params),
    {
      enabled: !!params.company_id,
    }
  );
}

/**
 * Hook to fetch single financial metric
 */
export function useFinancialMetric(metricId: string) {
  return useQuery(
    ['financial-metric', metricId],
    () => financialService.getFinancialMetric(metricId),
    {
      enabled: !!metricId,
    }
  );
}

/**
 * Hook to create financial metric
 */
export function useCreateFinancial() {
  const queryClient = useQueryClient();

  return useMutation(
    (financial: FinancialMetricCreate) => financialService.createFinancial(financial),
    {
      onSuccess: (data) => {
        // Invalidate financials for this company
        queryClient.invalidateQueries(['financials', { company_id: data.company_id }]);
      },
    }
  );
}

/**
 * Hook to update financial metric
 */
export function useUpdateFinancial() {
  const queryClient = useQueryClient();

  return useMutation(
    ({ metricId, updates }: { metricId: string; updates: Partial<FinancialMetric> }) =>
      financialService.updateFinancial(metricId, updates),
    {
      onSuccess: (data) => {
        // Invalidate specific metric and all financials for this company
        queryClient.invalidateQueries(['financial-metric', data.metric_id]);
        queryClient.invalidateQueries(['financials', { company_id: data.company_id }]);
      },
    }
  );
}

/**
 * Hook to delete financial metric
 */
export function useDeleteFinancial() {
  const queryClient = useQueryClient();

  return useMutation(
    (metricId: string) => financialService.deleteFinancial(metricId),
    {
      onSuccess: () => {
        // Invalidate all financial queries
        queryClient.invalidateQueries(['financials']);
      },
    }
  );
}

/**
 * Hook to batch create financials
 */
export function useBatchCreateFinancials() {
  const queryClient = useQueryClient();

  return useMutation(
    (financials: FinancialMetricCreate[]) => financialService.batchCreateFinancials(financials),
    {
      onSuccess: (data) => {
        // Get unique company IDs and invalidate their financials
        const companyIds = [...new Set(data.map(f => f.company_id))];
        companyIds.forEach(id => {
          queryClient.invalidateQueries(['financials', { company_id: id }]);
        });
      },
    }
  );
}

// ======================
// MODEL GENERATION HOOKS
// ======================

/**
 * Hook to generate a single model
 */
export function useGenerateModel() {
  return useMutation(
    (request: ModelGenerationRequest) => modelService.generateModel(request)
  );
}

/**
 * Hook to generate batch models
 */
export function useGenerateBatchModels() {
  return useMutation(
    (request: BatchModelRequest) => modelService.generateBatchModels(request)
  );
}

/**
 * Hook to get model generation history
 */
export function useModelHistory(companyId: string) {
  return useQuery(
    ['model-history', companyId],
    () => modelService.getModelHistory(companyId),
    {
      enabled: !!companyId,
    }
  );
}

/**
 * Hook to download model with automatic browser download
 */
export function useDownloadModel() {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const downloadModel = useCallback(async (filePath: string, fileName: string) => {
    setDownloading(true);
    setError(null);

    try {
      const blob = await modelService.downloadModel(filePath);
      modelService.downloadModelFile(blob, fileName);
    } catch (err: any) {
      setError(err.message || 'Download failed');
      throw err;
    } finally {
      setDownloading(false);
    }
  }, []);

  return { downloadModel, downloading, error };
}

// ======================
// COMBINED HOOKS
// ======================

/**
 * Hook to manage complete company workflow
 * Includes company data + financials + models
 */
export function useCompanyWorkflow(companyId: string) {
  const company = useCompany(companyId);
  const financials = useFinancials({ company_id: companyId });
  const modelHistory = useModelHistory(companyId);

  return {
    company: company.data,
    companyLoading: company.isLoading,
    companyError: company.error,
    
    financials: financials.data,
    financialsLoading: financials.isLoading,
    financialsError: financials.error,
    
    models: modelHistory.data,
    modelsLoading: modelHistory.isLoading,
    modelsError: modelHistory.error,
    
    isLoading: company.isLoading || financials.isLoading || modelHistory.isLoading,
    hasError: !!company.error || !!financials.error || !!modelHistory.error,
    
    refetchAll: () => {
      company.refetch();
      financials.refetch();
      modelHistory.refetch();
    },
  };
}

/**
 * Hook for form state management with API integration
 */
export function useApiForm<T, R = any>(
  apiCall: (data: T) => Promise<R>,
  options?: {
    onSuccess?: (data: R) => void;
    onError?: (error: any) => void;
  }
) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<R | null>(null);

  const submit = useCallback(async (formData: T) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await apiCall(formData);
      setData(result);
      options?.onSuccess?.(result);
      return result;
    } catch (err: any) {
      const errorMessage = err.message || 'An error occurred';
      setError(errorMessage);
      options?.onError?.(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiCall, options]);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setData(null);
  }, []);

  return {
    submit,
    reset,
    loading,
    error,
    data,
  };
}

// ======================
// UTILITIES
// ======================

/**
 * Hook for handling errors with toast notifications
 */
export function useApiError() {
  const handleError = useCallback((error: any, customMessage?: string) => {
    const message = customMessage || error.message || 'An error occurred';
    
    // Log to console in development
    if (import.meta.env.DEV) {
      console.error('API Error:', error);
    }

    // You can integrate with a toast notification library here
    // For example, with react-hot-toast:
    // toast.error(message);

    // Or with Material-UI Snackbar:
    // enqueueSnackbar(message, { variant: 'error' });

    return message;
  }, []);

  return { handleError };
}

/**
 * Hook for success messages
 */
export function useApiSuccess() {
  const handleSuccess = useCallback((message: string) => {
    // You can integrate with a toast notification library here
    // toast.success(message);
    
    if (import.meta.env.DEV) {
      console.log('✅ Success:', message);
    }
  }, []);

  return { handleSuccess };
}

// ======================
// EXAMPLE USAGE
// ======================

/*
// In a React component:

function CompanyDetail({ companyId }) {
  // Fetch company data
  const { data: company, isLoading, error } = useCompany(companyId);
  
  // Update company mutation
  const updateCompany = useUpdateCompany();
  
  // Handle update
  const handleUpdate = async (updates) => {
    try {
      await updateCompany.mutateAsync({ companyId, updates });
      toast.success('Company updated successfully');
    } catch (error) {
      toast.error('Failed to update company');
    }
  };
  
  if (isLoading) return <CircularProgress />;
  if (error) return <Alert severity="error">Error loading company</Alert>;
  
  return (
    <div>
      <h1>{company.company_name}</h1>
      // ... rest of component
    </div>
  );
}

// Using the workflow hook:

function CompanyWorkflow({ companyId }) {
  const {
    company,
    financials,
    models,
    isLoading,
    hasError,
    refetchAll
  } = useCompanyWorkflow(companyId);
  
  if (isLoading) return <CircularProgress />;
  
  return (
    <div>
      <CompanyInfo company={company} />
      <FinancialsChart data={financials} />
      <ModelsList models={models} />
      <Button onClick={refetchAll}>Refresh All</Button>
    </div>
  );
}

// Using form hook:

function CreateCompanyForm() {
  const createCompanyForm = useApiForm(
    companyService.createCompany,
    {
      onSuccess: (company) => {
        toast.success(`Company ${company.company_name} created!`);
        navigate(`/companies/${company.company_id}`);
      },
      onError: (error) => {
        toast.error('Failed to create company');
      }
    }
  );
  
  const handleSubmit = (formData) => {
    createCompanyForm.submit(formData);
  };
  
  return (
    <form onSubmit={handleSubmit}>
      // ... form fields
      <Button 
        type="submit" 
        disabled={createCompanyForm.loading}
      >
        {createCompanyForm.loading ? 'Creating...' : 'Create Company'}
      </Button>
      {createCompanyForm.error && (
        <Alert severity="error">{createCompanyForm.error}</Alert>
      )}
    </form>
  );
}
*/
