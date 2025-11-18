// src/hooks/useFinancials.ts
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { financialService } from '../services/financials';
import { FinancialMetric, FinancialMetricCreate } from '../types/financial';

export const useFinancials = (companyId: string) => {
  const queryClient = useQueryClient();

  const { data: financials, isLoading, error } = useQuery<FinancialMetric[]>(
    ['financials', companyId],
    () => financialService.getByCompany(companyId),
    {
      enabled: !!companyId,
      staleTime: 5 * 60 * 1000,
    }
  );

  const createMutation = useMutation(
    (data: FinancialMetricCreate) => financialService.create(companyId, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['financials', companyId]);
      },
    }
  );

  const updateMutation = useMutation(
    ({ period, data }: { period: string; data: Partial<FinancialMetricCreate> }) =>
      financialService.update(companyId, period, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['financials', companyId]);
      },
    }
  );

  return {
    financials: financials || [],
    loading: isLoading,
    error,
    addFinancial: createMutation.mutate,
    updateFinancial: updateMutation.mutate,
  };
};
