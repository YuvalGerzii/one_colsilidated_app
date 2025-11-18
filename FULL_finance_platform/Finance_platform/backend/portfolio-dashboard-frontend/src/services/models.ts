// src/services/models.ts
import { API_BASE_URL, apiClient } from './api';

export interface ModelGenerationRequest {
  company_id: string;
  models: {
    dcf?: boolean;
    lbo?: boolean;
    merger?: boolean;
    dd?: boolean;
    qoe?: boolean;
  };
  scenario?: 'base' | 'upside' | 'downside';
}

export interface ModelGenerationResponse {
  dcf?: string;
  lbo?: string;
  merger?: string;
  dd?: string;
  qoe?: string;
  generation_time: number;
}

export const modelService = {
  // Generate models
  generate: async (
    request: ModelGenerationRequest
  ): Promise<ModelGenerationResponse> => {
    return apiClient.post<ModelGenerationResponse>(
      '/models/generate-batch',
      request
    );
  },

  // Generate single model
  generateSingle: async (
    companyId: string,
    modelType: string,
    scenario?: string
  ): Promise<{ file_path: string }> => {
    return apiClient.post<{ file_path: string }>('/models/generate', {
      company_id: companyId,
      model_type: modelType,
      scenario,
    });
  },

  // List generated models
  list: async (companyId: string): Promise<any[]> => {
    return apiClient.get<any[]>(`/models/list/${companyId}`);
  },

  // Download model
  downloadUrl: (filePath: string): string => {
    const baseUrl = API_BASE_URL.replace(/\/+$/, '');
    if (baseUrl.startsWith('http')) {
      const match = baseUrl.match(/(.*)\/api\/v1$/i);
      const origin = match ? match[1] : baseUrl;
      return `${origin.replace(/\/+$/, '')}/api/v1/models/download/${filePath}`;
    }

    const relativeBase = baseUrl.length > 0 ? baseUrl : '/api/v1';
    return `${relativeBase.replace(/\/+$/, '')}/models/download/${filePath}`;
  },
};
