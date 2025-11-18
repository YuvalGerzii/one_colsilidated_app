/**
 * Calculator Storage Service
 *
 * Handles saving, loading, and managing calculator results.
 * Replaces localStorage with database persistence via API.
 */

import api from './api';

export enum CalculationType {
  FIX_AND_FLIP = 'fix_and_flip',
  SINGLE_FAMILY_RENTAL = 'single_family_rental',
  SMALL_MULTIFAMILY = 'small_multifamily',
  SMALL_MULTIFAMILY_ACQUISITION = 'small_multifamily_acquisition',
  HIGH_RISE_MULTIFAMILY = 'high_rise_multifamily',
  HOTEL_FINANCIAL = 'hotel_financial',
  MIXED_USE_DEVELOPMENT = 'mixed_use_development',
  LEASE_ANALYZER = 'lease_analyzer',
  RENOVATION_BUDGET = 'renovation_budget',
  SUBDIVISION = 'subdivision',
  TAX_STRATEGY = 'tax_strategy',
  PORTFOLIO_DASHBOARD = 'portfolio_dashboard',
}

export interface SavedCalculation {
  id: string;
  calculation_type: string;
  property_name: string;
  property_address?: string;
  version: number;
  is_current_version: boolean;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  notes?: string;
  tags?: string[];
  is_favorite: boolean;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface SaveCalculationRequest {
  calculation_type: CalculationType | string;
  property_name: string;
  property_address?: string;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  notes?: string;
  tags?: string[];
  is_favorite?: boolean;
}

export interface UpdateCalculationRequest {
  property_name?: string;
  property_address?: string;
  input_data?: Record<string, any>;
  output_data?: Record<string, any>;
  notes?: string;
  tags?: string[];
  is_favorite?: boolean;
  is_archived?: boolean;
}

export interface ListCalculationsParams {
  calculation_type?: CalculationType | string;
  is_favorite?: boolean;
  is_archived?: boolean;
  tags?: string;
  search?: string;
  skip?: number;
  limit?: number;
}

export interface CalculationsSummary {
  total_calculations: number;
  favorites: number;
  by_type: Record<string, number>;
}

class CalculatorService {
  /**
   * Save a new calculation
   */
  async saveCalculation(data: SaveCalculationRequest): Promise<SavedCalculation> {
    const response = await api.post<SavedCalculation>('/calculations/', data);
    return response.data;
  }

  /**
   * List all calculations with optional filters
   */
  async listCalculations(params?: ListCalculationsParams): Promise<SavedCalculation[]> {
    const response = await api.get<SavedCalculation[]>('/calculations/', { params });
    return response.data;
  }

  /**
   * Get a specific calculation by ID
   */
  async getCalculation(id: string): Promise<SavedCalculation> {
    const response = await api.get<SavedCalculation>(`/calculations/${id}`);
    return response.data;
  }

  /**
   * Update an existing calculation
   */
  async updateCalculation(
    id: string,
    data: UpdateCalculationRequest,
    createVersion: boolean = false
  ): Promise<SavedCalculation> {
    const response = await api.put<SavedCalculation>(
      `/calculations/${id}`,
      data,
      { params: { create_version: createVersion } }
    );
    return response.data;
  }

  /**
   * Delete a calculation
   */
  async deleteCalculation(id: string): Promise<void> {
    await api.delete(`/calculations/${id}`);
  }

  /**
   * Get version history for a calculation
   */
  async getCalculationVersions(id: string): Promise<SavedCalculation[]> {
    const response = await api.get<SavedCalculation[]>(`/calculations/${id}/versions`);
    return response.data;
  }

  /**
   * Bulk save calculations (useful for migration from localStorage)
   */
  async bulkSaveCalculations(calculations: SaveCalculationRequest[]): Promise<SavedCalculation[]> {
    const response = await api.post<SavedCalculation[]>('/calculations/bulk-save', calculations);
    return response.data;
  }

  /**
   * Get summary statistics
   */
  async getCalculationsSummary(): Promise<CalculationsSummary> {
    const response = await api.get<CalculationsSummary>('/calculations/stats/summary');
    return response.data;
  }

  // ===== Helper Methods for Specific Calculator Types =====

  /**
   * Save Fix & Flip calculation
   */
  async saveFixAndFlip(
    propertyName: string,
    inputData: any,
    outputData: any,
    options?: { address?: string; notes?: string; tags?: string[] }
  ): Promise<SavedCalculation> {
    return this.saveCalculation({
      calculation_type: CalculationType.FIX_AND_FLIP,
      property_name: propertyName,
      property_address: options?.address,
      input_data: inputData,
      output_data: outputData,
      notes: options?.notes,
      tags: options?.tags,
    });
  }

  /**
   * Get all Fix & Flip calculations
   */
  async getFixAndFlipCalculations(): Promise<SavedCalculation[]> {
    return this.listCalculations({
      calculation_type: CalculationType.FIX_AND_FLIP,
    });
  }

  /**
   * Save Single Family Rental calculation
   */
  async saveSingleFamilyRental(
    propertyName: string,
    inputData: any,
    outputData: any,
    options?: { address?: string; notes?: string; tags?: string[] }
  ): Promise<SavedCalculation> {
    return this.saveCalculation({
      calculation_type: CalculationType.SINGLE_FAMILY_RENTAL,
      property_name: propertyName,
      property_address: options?.address,
      input_data: inputData,
      output_data: outputData,
      notes: options?.notes,
      tags: options?.tags,
    });
  }

  /**
   * Get all Single Family Rental calculations
   */
  async getSingleFamilyRentalCalculations(): Promise<SavedCalculation[]> {
    return this.listCalculations({
      calculation_type: CalculationType.SINGLE_FAMILY_RENTAL,
    });
  }

  /**
   * Toggle favorite status
   */
  async toggleFavorite(id: string, isFavorite: boolean): Promise<SavedCalculation> {
    return this.updateCalculation(id, { is_favorite: isFavorite });
  }

  /**
   * Archive a calculation
   */
  async archiveCalculation(id: string): Promise<SavedCalculation> {
    return this.updateCalculation(id, { is_archived: true });
  }

  /**
   * Unarchive a calculation
   */
  async unarchiveCalculation(id: string): Promise<SavedCalculation> {
    return this.updateCalculation(id, { is_archived: false });
  }

  /**
   * Add tags to a calculation
   */
  async addTags(id: string, tags: string[]): Promise<SavedCalculation> {
    const calculation = await this.getCalculation(id);
    const existingTags = calculation.tags || [];
    const newTags = [...new Set([...existingTags, ...tags])];
    return this.updateCalculation(id, { tags: newTags });
  }

  /**
   * Search calculations by property name or address
   */
  async searchCalculations(query: string): Promise<SavedCalculation[]> {
    return this.listCalculations({ search: query });
  }

  /**
   * Get favorite calculations
   */
  async getFavoriteCalculations(): Promise<SavedCalculation[]> {
    return this.listCalculations({ is_favorite: true });
  }

  /**
   * Get calculations by type
   */
  async getCalculationsByType(type: CalculationType | string): Promise<SavedCalculation[]> {
    return this.listCalculations({ calculation_type: type });
  }
}

export const calculatorService = new CalculatorService();
export default calculatorService;
