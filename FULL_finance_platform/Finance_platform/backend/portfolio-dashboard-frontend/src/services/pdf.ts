// src/services/pdf.ts
import { apiClient } from './api';

export interface PDFExtractionResult {
  company_id: string;
  extraction_id: string;
  status: 'processing' | 'completed' | 'failed';
  confidence_score: number;
  extracted_data: {
    revenue?: number;
    ebitda?: number;
    net_income?: number;
    assets?: number;
    liabilities?: number;
    [key: string]: any;
  };
  requires_review: boolean;
  errors?: string[];
}

export const pdfService = {
  // Upload and extract
  extract: async (
    companyId: string,
    file: File,
    documentType: 'financial_statement' | 'management_report' | 'other',
    onProgress?: (progress: number) => void
  ): Promise<PDFExtractionResult> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    formData.append('company_id', companyId);

    return apiClient.upload<PDFExtractionResult>(
      '/pdf/extract',
      file,
      onProgress
    );
  },

  // Get extraction status
  getStatus: async (extractionId: string): Promise<PDFExtractionResult> => {
    return apiClient.get<PDFExtractionResult>(`/pdf/status/${extractionId}`);
  },

  // Approve extraction
  approve: async (
    extractionId: string,
    data: any
  ): Promise<void> => {
    return apiClient.post<void>(`/pdf/approve/${extractionId}`, data);
  },

  // Reject and manually enter
  reject: async (extractionId: string): Promise<void> => {
    return apiClient.post<void>(`/pdf/reject/${extractionId}`);
  },
};
