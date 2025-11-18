/**
 * Python Agent Service
 * Integrates TypeScript Bond.AI with Python psychometric agents
 */

import axios, { AxiosInstance } from 'axios';
import { Contact } from '../../src/types';

interface PythonProfile {
  id: string;
  name: string;
  bio?: string;
  title?: string;
  company?: string;
  skills?: string[];
  interests?: string[];
  needs?: string[];
  offerings?: string[];
  metadata?: Record<string, any>;
}

interface MatchDimensions {
  semantic_similarity?: number;
  personality_compatibility?: number;
  communication_compatibility?: number;
  interest_overlap?: number;
  skills_complementarity?: number;
  value_alignment?: number;
}

interface PythonMatchResponse {
  overall_score: number;
  confidence: number;
  dimensions: MatchDimensions;
  recommendations: string[];
  personality_match?: {
    profile1_type: string;
    profile2_type: string;
    compatibility: number;
  };
  communication_compatibility?: {
    style_similarity: number;
    effectiveness_prediction: number;
  };
  value_alignment?: {
    score: number;
  };
}

interface BulkMatchResponse {
  total_candidates: number;
  matches_analyzed: number;
  top_matches: Array<{
    candidate_id: string;
    candidate_name: string;
    score: number;
    confidence: number;
    dimensions: MatchDimensions;
    recommendations: string[];
  }>;
}

export class PythonAgentService {
  private client: AxiosInstance;
  private baseURL: string;
  private enabled: boolean;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || process.env.PYTHON_AGENTS_URL || 'http://localhost:8005';
    this.enabled = process.env.ENABLE_PYTHON_AGENTS === 'true';

    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 seconds
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Check if Python agents are available
   */
  async isAvailable(): Promise<boolean> {
    if (!this.enabled) return false;

    try {
      const response = await this.client.get('/health', { timeout: 5000 });
      return response.data.status === 'healthy';
    } catch (error) {
      console.warn('Python agents not available:', error.message);
      return false;
    }
  }

  /**
   * Convert Bond.AI Contact to Python Profile format
   */
  private contactToProfile(contact: Contact): PythonProfile {
    return {
      id: contact.id,
      name: contact.name,
      bio: contact.bio,
      title: contact.title,
      company: contact.company,
      skills: contact.skills || [],
      interests: contact.interests || [],
      needs: contact.needs || [],
      offerings: contact.offerings || [],
      metadata: contact.metadata || {},
    };
  }

  /**
   * Calculate enhanced psychometric match between two contacts
   */
  async calculateMatch(
    contact1: Contact,
    contact2: Contact,
    dimensions: string[] = ['all']
  ): Promise<PythonMatchResponse | null> {
    if (!this.enabled) {
      console.log('Python agents disabled, skipping enhanced matching');
      return null;
    }

    try {
      const response = await this.client.post<PythonMatchResponse>('/match', {
        profile1: this.contactToProfile(contact1),
        profile2: this.contactToProfile(contact2),
        dimensions,
      });

      return response.data;
    } catch (error) {
      console.error('Error calling Python match API:', error.message);
      return null;
    }
  }

  /**
   * Find top matches for a contact from a list of candidates
   */
  async bulkMatch(
    sourceContact: Contact,
    candidates: Contact[],
    topN: number = 10,
    dimensions: string[] = ['all']
  ): Promise<BulkMatchResponse | null> {
    if (!this.enabled) {
      console.log('Python agents disabled, skipping bulk matching');
      return null;
    }

    try {
      const response = await this.client.post<BulkMatchResponse>('/match/bulk', {
        source_profile: this.contactToProfile(sourceContact),
        candidate_profiles: candidates.map(c => this.contactToProfile(c)),
        dimensions,
        top_n: topN,
      });

      return response.data;
    } catch (error) {
      console.error('Error calling Python bulk match API:', error.message);
      return null;
    }
  }

  /**
   * Get list of available Python agents
   */
  async listAgents(): Promise<any> {
    if (!this.enabled) return null;

    try {
      const response = await this.client.get('/agents');
      return response.data;
    } catch (error) {
      console.error('Error listing Python agents:', error.message);
      return null;
    }
  }

  /**
   * Get specific dimension score for a match
   */
  async getDimensionScore(
    contact1: Contact,
    contact2: Contact,
    dimension: 'semantic' | 'personality' | 'communication' | 'interests' | 'skills' | 'values'
  ): Promise<number | null> {
    const match = await this.calculateMatch(contact1, contact2, [dimension]);

    if (!match) return null;

    const dimensionKey = `${dimension}_${
      dimension === 'interests' ? 'overlap' :
      dimension === 'skills' ? 'complementarity' :
      dimension === 'values' ? 'alignment' :
      'compatibility'
    }`;

    return match.dimensions[dimensionKey] || null;
  }

  /**
   * Get personality compatibility with detailed analysis
   */
  async getPersonalityMatch(
    contact1: Contact,
    contact2: Contact
  ): Promise<{
    score: number;
    type1: string;
    type2: string;
    compatibility: number;
  } | null> {
    const match = await this.calculateMatch(contact1, contact2, ['personality']);

    if (!match || !match.personality_match) return null;

    return {
      score: match.dimensions.personality_compatibility || 0,
      type1: match.personality_match.profile1_type,
      type2: match.personality_match.profile2_type,
      compatibility: match.personality_match.compatibility,
    };
  }

  /**
   * Enhance existing match score with Python agents
   */
  async enhanceMatchScore(
    contact1: Contact,
    contact2: Contact,
    baseScore: number
  ): Promise<{
    enhancedScore: number;
    improvement: number;
    dimensions: MatchDimensions;
    recommendations: string[];
  } | null> {
    const pythonMatch = await this.calculateMatch(contact1, contact2);

    if (!pythonMatch) {
      return {
        enhancedScore: baseScore,
        improvement: 0,
        dimensions: {},
        recommendations: [],
      };
    }

    // Combine base score with Python agent score (weighted)
    const enhancedScore = (baseScore * 0.4) + (pythonMatch.overall_score * 0.6);
    const improvement = enhancedScore - baseScore;

    return {
      enhancedScore,
      improvement,
      dimensions: pythonMatch.dimensions,
      recommendations: pythonMatch.recommendations,
    };
  }
}

// Export singleton instance
export const pythonAgentService = new PythonAgentService();
