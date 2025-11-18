/**
 * Hybrid Matching Agent
 * Combines TypeScript algorithmic matching with Python psychometric analysis
 * for superior match quality
 */

import { Contact, Match, MatchType, Priority, MatchStatus } from '../types';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';
import { NetworkMapper } from '../network/NetworkMapper';
import { pythonAgentService } from '../../server/services/PythonAgentService';

export interface HybridMatchConfig {
  usePythonAgents: boolean;
  pythonWeight: number; // 0-1, weight for Python agent scores
  algorithmicWeight: number; // 0-1, weight for algorithmic scores
  minHybridScore: number; // minimum score threshold
  enableDimensionalAnalysis: boolean;
}

export interface HybridMatchResult {
  match: Match;
  algorithmicScore: number;
  pythonScore?: number;
  hybridScore: number;
  improvement: number;
  dimensionalBreakdown?: {
    semantic: number;
    personality: number;
    communication: number;
    interests: number;
    skills: number;
    values: number;
  };
  recommendations: string[];
  confidence: number;
}

export class HybridMatchingAgent {
  private intelligenceEngine: IntelligenceEngine;
  private networkMapper: NetworkMapper;
  private config: HybridMatchConfig;

  constructor(
    intelligenceEngine: IntelligenceEngine,
    networkMapper: NetworkMapper,
    config?: Partial<HybridMatchConfig>
  ) {
    this.intelligenceEngine = intelligenceEngine;
    this.networkMapper = networkMapper;
    this.config = {
      usePythonAgents: config?.usePythonAgents ?? true,
      pythonWeight: config?.pythonWeight ?? 0.6,
      algorithmicWeight: config?.algorithmicWeight ?? 0.4,
      minHybridScore: config?.minHybridScore ?? 0.7,
      enableDimensionalAnalysis: config?.enableDimensionalAnalysis ?? true,
    };
  }

  /**
   * Calculate hybrid match using both algorithmic and psychometric analysis
   */
  async calculateHybridMatch(
    contact1: Contact,
    contact2: Contact,
    baseMatch: Match
  ): Promise<HybridMatchResult> {
    const algorithmicScore = baseMatch.compatibilityScore;
    let pythonScore: number | undefined;
    let dimensionalBreakdown: any;
    let recommendations: string[] = [];
    let confidence = 0.85; // Base confidence for algorithmic matching

    // Try to get Python agent enhancement
    if (this.config.usePythonAgents) {
      try {
        const enhancement = await pythonAgentService.enhanceMatchScore(
          contact1,
          contact2,
          algorithmicScore
        );

        if (enhancement) {
          pythonScore = enhancement.enhancedScore;
          dimensionalBreakdown = this.buildDimensionalBreakdown(enhancement.dimensions);
          recommendations = enhancement.recommendations;
          confidence = 0.92; // Higher confidence with Python agents
        }
      } catch (error) {
        console.warn('Python agents unavailable, using algorithmic matching only:', error);
      }
    }

    // Calculate hybrid score
    const hybridScore = pythonScore
      ? (algorithmicScore * this.config.algorithmicWeight) +
        (pythonScore * this.config.pythonWeight)
      : algorithmicScore;

    const improvement = pythonScore ? hybridScore - algorithmicScore : 0;

    // Update match with hybrid score
    const enhancedMatch: Match = {
      ...baseMatch,
      compatibilityScore: hybridScore,
      overallScore: this.recalculateOverallScore(baseMatch, hybridScore),
      priority: this.determinePriority(hybridScore),
      metadata: {
        ...baseMatch.metadata,
        hybridMatch: true,
        algorithmicScore,
        pythonScore,
        improvement,
        dimensionalBreakdown,
        enhancedRecommendations: recommendations,
      },
    };

    return {
      match: enhancedMatch,
      algorithmicScore,
      pythonScore,
      hybridScore,
      improvement,
      dimensionalBreakdown,
      recommendations,
      confidence,
    };
  }

  /**
   * Find hybrid matches for a contact with enhanced scoring
   */
  async findHybridMatches(
    sourceContact: Contact,
    candidates: Contact[],
    baseMatches: Match[]
  ): Promise<HybridMatchResult[]> {
    const hybridResults: HybridMatchResult[] = [];

    // If Python agents available, use bulk matching for efficiency
    if (this.config.usePythonAgents) {
      try {
        const available = await pythonAgentService.isAvailable();

        if (available && candidates.length > 5) {
          // Use bulk matching for better performance
          const bulkResults = await pythonAgentService.bulkMatch(
            sourceContact,
            candidates,
            candidates.length
          );

          if (bulkResults) {
            // Map bulk results to hybrid matches
            for (const baseMatch of baseMatches) {
              const pythonMatch = bulkResults.top_matches.find(
                m => m.candidate_id === baseMatch.targetContact.id
              );

              if (pythonMatch) {
                const hybridScore =
                  (baseMatch.compatibilityScore * this.config.algorithmicWeight) +
                  (pythonMatch.score * this.config.pythonWeight);

                hybridResults.push({
                  match: {
                    ...baseMatch,
                    compatibilityScore: hybridScore,
                    overallScore: this.recalculateOverallScore(baseMatch, hybridScore),
                    metadata: {
                      ...baseMatch.metadata,
                      pythonScore: pythonMatch.score,
                      dimensionalBreakdown: pythonMatch.dimensions,
                      recommendations: pythonMatch.recommendations,
                    },
                  },
                  algorithmicScore: baseMatch.compatibilityScore,
                  pythonScore: pythonMatch.score,
                  hybridScore,
                  improvement: hybridScore - baseMatch.compatibilityScore,
                  dimensionalBreakdown: pythonMatch.dimensions,
                  recommendations: pythonMatch.recommendations,
                  confidence: pythonMatch.confidence,
                });
              } else {
                // Fallback to algorithmic only
                hybridResults.push(await this.calculateHybridMatch(
                  sourceContact,
                  baseMatch.targetContact,
                  baseMatch
                ));
              }
            }

            return hybridResults;
          }
        }
      } catch (error) {
        console.warn('Bulk matching failed, falling back to individual matches:', error);
      }
    }

    // Fallback: Individual matching
    for (const baseMatch of baseMatches) {
      const result = await this.calculateHybridMatch(
        sourceContact,
        baseMatch.targetContact,
        baseMatch
      );
      hybridResults.push(result);
    }

    return hybridResults;
  }

  /**
   * Get personality compatibility for a match
   */
  async getPersonalityCompatibility(
    contact1: Contact,
    contact2: Contact
  ): Promise<{
    score: number;
    type1: string;
    type2: string;
    analysis: string;
  } | null> {
    if (!this.config.usePythonAgents) return null;

    try {
      const result = await pythonAgentService.getPersonalityMatch(contact1, contact2);

      if (result) {
        return {
          score: result.score,
          type1: result.type1,
          type2: result.type2,
          analysis: `${result.type1} and ${result.type2} pairing shows ${
            result.compatibility > 0.8 ? 'excellent' :
            result.compatibility > 0.7 ? 'good' :
            result.compatibility > 0.6 ? 'moderate' : 'limited'
          } compatibility`,
        };
      }
    } catch (error) {
      console.error('Error getting personality compatibility:', error);
    }

    return null;
  }

  /**
   * Build dimensional breakdown from Python agent response
   */
  private buildDimensionalBreakdown(dimensions: any): any {
    return {
      semantic: dimensions.semantic_similarity || 0,
      personality: dimensions.personality_compatibility || 0,
      communication: dimensions.communication_compatibility || 0,
      interests: dimensions.interest_overlap || 0,
      skills: dimensions.skills_complementarity || 0,
      values: dimensions.value_alignment || 0,
    };
  }

  /**
   * Recalculate overall score with new compatibility score
   */
  private recalculateOverallScore(baseMatch: Match, newCompatibilityScore: number): number {
    // Weighted combination: compatibility, value, success probability, trust
    return (
      newCompatibilityScore * 0.35 +
      baseMatch.valuePotential * 0.25 +
      baseMatch.successProbability * 0.20 +
      baseMatch.shortestPath.trustScore * 0.20
    );
  }

  /**
   * Determine priority based on hybrid score
   */
  private determinePriority(score: number): Priority {
    if (score >= 0.85) return Priority.CRITICAL;
    if (score >= 0.75) return Priority.HIGH;
    if (score >= 0.65) return Priority.MEDIUM;
    return Priority.LOW;
  }

  /**
   * Get detailed match analysis with all dimensions
   */
  async getDetailedAnalysis(
    contact1: Contact,
    contact2: Contact
  ): Promise<{
    dimensions: Map<string, number>;
    strengths: string[];
    concerns: string[];
    recommendations: string[];
    overallAssessment: string;
  }> {
    const strengths: string[] = [];
    const concerns: string[] = [];
    const recommendations: string[] = [];
    const dimensions = new Map<string, number>();

    // Get Python agent analysis if available
    if (this.config.usePythonAgents) {
      try {
        const pythonMatch = await pythonAgentService.calculateMatch(contact1, contact2);

        if (pythonMatch) {
          // Store dimensional scores
          Object.entries(pythonMatch.dimensions).forEach(([key, value]) => {
            dimensions.set(key, value as number);
          });

          // Analyze dimensions for strengths and concerns
          if (pythonMatch.dimensions.personality_compatibility > 0.8) {
            strengths.push('Excellent personality compatibility');
          }
          if (pythonMatch.dimensions.value_alignment > 0.85) {
            strengths.push('Strong value alignment for long-term collaboration');
          }
          if (pythonMatch.dimensions.communication_compatibility > 0.75) {
            strengths.push('Compatible communication styles');
          }

          if (pythonMatch.dimensions.interest_overlap < 0.3) {
            concerns.push('Limited shared interests - may need to build common ground');
          }
          if (pythonMatch.dimensions.communication_compatibility < 0.6) {
            concerns.push('Different communication styles - may require adaptation');
          }

          recommendations.push(...pythonMatch.recommendations);
        }
      } catch (error) {
        console.error('Error getting detailed analysis:', error);
      }
    }

    // Generate overall assessment
    const avgScore = Array.from(dimensions.values()).reduce((a, b) => a + b, 0) / dimensions.size;
    const overallAssessment = this.generateAssessment(avgScore, strengths, concerns);

    return {
      dimensions,
      strengths,
      concerns,
      recommendations,
      overallAssessment,
    };
  }

  /**
   * Generate overall assessment text
   */
  private generateAssessment(
    avgScore: number,
    strengths: string[],
    concerns: string[]
  ): string {
    const rating = avgScore > 0.85 ? 'Exceptional' :
                   avgScore > 0.75 ? 'Excellent' :
                   avgScore > 0.65 ? 'Good' :
                   avgScore > 0.55 ? 'Moderate' : 'Limited';

    return `${rating} overall compatibility (${(avgScore * 100).toFixed(0)}%). ` +
           `${strengths.length} key strengths identified. ` +
           `${concerns.length > 0 ? `${concerns.length} areas for consideration.` : 'No major concerns.'}`;
  }
}
