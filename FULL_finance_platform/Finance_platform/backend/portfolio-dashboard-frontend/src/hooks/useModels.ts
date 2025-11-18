// src/hooks/useModels.ts
import { useState } from 'react';
import { useMutation } from 'react-query';
import { modelService, ModelGenerationRequest } from '../services/models';

export const useModelGeneration = () => {
  const [progress, setProgress] = useState(0);

  const mutation = useMutation(
    (request: ModelGenerationRequest) => modelService.generate(request),
    {
      onMutate: () => {
        setProgress(0);
      },
      onSuccess: () => {
        setProgress(100);
      },
    }
  );

  return {
    generate: mutation.mutate,
    loading: mutation.isLoading,
    error: mutation.error,
    data: mutation.data,
    progress,
    reset: mutation.reset,
  };
};
