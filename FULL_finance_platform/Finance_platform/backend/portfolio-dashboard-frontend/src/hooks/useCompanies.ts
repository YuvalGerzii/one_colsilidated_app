// src/hooks/useCompanies.ts
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { companyService } from '../services/companies';
import { Company, CompanyCreate, CompanyUpdate } from '../types/company';

export const useCompanies = (fundId?: string) => {
  const queryClient = useQueryClient();

  const { data: companies, isLoading, error, refetch } = useQuery<Company[]>(
    ['companies', fundId],
    () => companyService.getAll(fundId),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
    }
  );

  const createMutation = useMutation(
    (data: CompanyCreate) => companyService.create(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['companies']);
      },
    }
  );

  const updateMutation = useMutation(
    ({ id, data }: { id: string; data: CompanyUpdate }) =>
      companyService.update(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['companies']);
      },
    }
  );

  const deleteMutation = useMutation(
    (id: string) => companyService.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['companies']);
      },
    }
  );

  return {
    companies: companies || [],
    loading: isLoading,
    error,
    refetch,
    createCompany: createMutation.mutate,
    updateCompany: updateMutation.mutate,
    deleteCompany: deleteMutation.mutate,
  };
};

export const useCompany = (companyId: string) => {
  const { data: company, isLoading, error } = useQuery<Company>(
    ['company', companyId],
    () => companyService.getById(companyId),
    {
      enabled: !!companyId,
      staleTime: 5 * 60 * 1000,
    }
  );

  return {
    company,
    loading: isLoading,
    error,
  };
};
