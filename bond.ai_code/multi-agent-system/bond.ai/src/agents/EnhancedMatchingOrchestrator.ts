/**
 * Enhanced Matching Orchestrator
 *
 * Integrates all matching agents into a cohesive, intelligent system that can
 * handle ANY type of matching request dynamically.
 *
 * This is the main entry point for intelligent matching that replaces
 * scenario-specific agents with a dynamic, adaptive approach.
 */

import { Contact, Match } from '../types';
import { IntelligenceEngine } from '../intelligence/IntelligenceEngine';
import { DynamicMatchingStrategySelector, MatchingRequest } from './DynamicMatchingStrategySelector';
import { ContextUnderstandingAgent, MatchingContext } from './ContextUnderstandingAgent';
import { MultiCriteriaOptimizationAgent, OptimizationObjective, OptimizationConstraint } from './MultiCriteriaOptimizationAgent';
import { ProfileVerificationAgent } from './ProfileVerificationAgent';

export interface EnhancedMatchingRequest {
  seeker: Contact;
  query?: string;
  candidates?: Contact[];
  requirements?: {
    must: Record<string, any>;
    should: Record<string, any>;
  };
  optimization?: {
    objectives?: OptimizationObjective[];
    diversityWeight?: number;
  };
  options?: {
    maxResults?: number;
    minConfidence?: number;
    explainResults?: boolean;
  };
}

export interface EnhancedMatchingResult {
  candidate: Contact;
  score: number;
  confidence: number;
  matchType: string;
  explanation: {
    strategies: Array<{ name: string; contribution: number }>;
    context: MatchingContext;
    tradeoffs: string[];
    recommendations: string[];
  };
  verification: {
    verificationLevel: string;
    risks: string[];
  };
}

export class EnhancedMatchingOrchestrator {
  private intelligenceEngine: IntelligenceEngine;
  private strategySelector: DynamicMatchingStrategySelector;
  private contextAgent: ContextUnderstandingAgent;
  private optimizationAgent: MultiCriteriaOptimizationAgent;
  private verificationAgent: ProfileVerificationAgent;

  constructor() {
    this.intelligenceEngine = new IntelligenceEngine();
    this.strategySelector = new DynamicMatchingStrategySelector(this.intelligenceEngine);
    this.contextAgent = new ContextUnderstandingAgent();
    this.optimizationAgent = new MultiCriteriaOptimizationAgent();
    this.verificationAgent = new ProfileVerificationAgent();
  }

  /**
   * Main entry point: Find matches using comprehensive intelligent system
   */
  async findMatches(request: EnhancedMatchingRequest): Promise<EnhancedMatchingResult[]> {
    console.log('🧠 Enhanced Matching Orchestrator: Starting intelligent matching...\n');

    // Step 1: Understand context
    console.log('📊 Step 1: Analyzing context...');
    const context = await this.contextAgent.analyzeContext(
      request.seeker,
      request.query,
      request.requirements
    );

    console.log(`  Context: ${context.strategic.primaryGoal}`);
    console.log(`  Urgency: ${context.temporal.urgency}`);
    console.log(`  Relationship: ${context.social.relationshipType}\n`);

    // Step 2: Verify seeker profile
    console.log('✓ Step 2: Verifying seeker profile...');
    const seekerVerification = this.verificationAgent.verifyProfile(request.seeker);
    console.log(`  Verification Level: ${seekerVerification.verificationLevel}`);
    console.log(`  Profile Quality: ${(seekerVerification.overall * 100).toFixed(0)}%\n`);

    // Step 3: Get candidates (or use provided ones)
    let candidates = request.candidates || [];
    if (candidates.length === 0) {
      console.log('⚠️  No candidates provided - would fetch from database in production\n');
      return [];
    }

    // Step 4: Filter by verification level if needed
    console.log('🔍 Step 3: Filtering and verifying candidates...');
    const minVerificationLevel = request.options?.minConfidence || 0.4;
    const verifiedCandidates = candidates.filter(candidate => {
      const verification = this.verificationAgent.verifyProfile(candidate);
      return verification.overall >= minVerificationLevel;
    });

    console.log(`  Filtered: ${candidates.length} → ${verifiedCandidates.length} candidates\n`);

    // Step 5: Use strategy selector for initial matching
    console.log('🎯 Step 4: Applying dynamic matching strategies...');
    const matchingRequest: MatchingRequest = {
      seeker: request.seeker,
      query: request.query,
      constraints: {
        maxResults: request.options?.maxResults || 20,
        minConfidence: request.options?.minConfidence || 0.4,
        ...this.extractConstraintsFromContext(context)
      },
      context: {
        urgency: context.temporal.urgency,
        relationship: context.temporal.timeHorizon === 'long' ? 'long-term' : 'one-time',
        formality: context.social.communicationStyle === 'formal' ? 'formal' : 'professional'
      }
    };

    const strategyResults = await this.strategySelector.findMatches(
      matchingRequest,
      verifiedCandidates
    );

    console.log(`  Found ${strategyResults.length} matches using dynamic strategies\n`);

    // Step 6: Apply multi-criteria optimization if objectives specified
    let optimizedResults = strategyResults;

    if (request.optimization?.objectives) {
      console.log('⚡ Step 5: Applying multi-criteria optimization...');

      const objectives = request.optimization.objectives.length > 0
        ? request.optimization.objectives
        : this.optimizationAgent.createStandardObjectives();

      const constraints = this.optimizationAgent.createStandardConstraints(
        request.requirements || {}
      );

      const optResults = await this.optimizationAgent.optimizeMatches(
        request.seeker,
        strategyResults.map(r => r.candidate),
        objectives,
        constraints,
        {
          maxResults: request.options?.maxResults,
          diversityConfig: request.optimization.diversityWeight ? {
            diversityWeight: request.optimization.diversityWeight,
            diversityDimensions: ['industry', 'location', 'experience']
          } : undefined
        }
      );

      console.log(`  Optimized: ${optResults.length} Pareto-optimal solutions found\n`);

      // Merge strategy results with optimization results
      optimizedResults = this.mergeResults(strategyResults, optResults);
    }

    // Step 7: Generate comprehensive explanations
    console.log('📝 Step 6: Generating explanations and recommendations...\n');

    const enhancedResults: EnhancedMatchingResult[] = optimizedResults.map(result => {
      const candidateVerification = this.verificationAgent.verifyProfile(result.candidate);
      const contextualRecommendations = this.contextAgent.generateContextualRecommendations(context);

      return {
        candidate: result.candidate,
        score: result.score,
        confidence: result.confidence,
        matchType: result.matchType,
        explanation: {
          strategies: result.strategies,
          context: context,
          tradeoffs: result.explanations || [],
          recommendations: [
            ...result.explanations,
            ...contextualRecommendations.slice(0, 2)
          ]
        },
        verification: {
          verificationLevel: candidateVerification.verificationLevel,
          risks: candidateVerification.risks
        }
      };
    });

    // Step 8: Sort by combined score (match score + verification quality)
    enhancedResults.sort((a, b) => {
      const scoreA = a.score * 0.7 + (this.getVerificationScore(a.verification.verificationLevel) * 0.3);
      const scoreB = b.score * 0.7 + (this.getVerificationScore(b.verification.verificationLevel) * 0.3);
      return scoreB - scoreA;
    });

    console.log('✅ Matching complete!\n');
    console.log(`📊 Results Summary:`);
    console.log(`   Total matches: ${enhancedResults.length}`);
    console.log(`   Excellent matches (>80%): ${enhancedResults.filter(r => r.score > 0.8).length}`);
    console.log(`   Good matches (60-80%): ${enhancedResults.filter(r => r.score >= 0.6 && r.score <= 0.8).length}`);
    console.log(`   Average confidence: ${(enhancedResults.reduce((sum, r) => sum + r.confidence, 0) / enhancedResults.length * 100).toFixed(0)}%\n`);

    return enhancedResults;
  }

  /**
   * Simplified API for quick matching (backward compatible)
   */
  async quickMatch(
    seeker: Contact,
    candidates: Contact[],
    query?: string
  ): Promise<EnhancedMatchingResult[]> {
    return this.findMatches({
      seeker,
      candidates,
      query,
      options: { maxResults: 10 }
    });
  }

  /**
   * Advanced API with full customization
   */
  async advancedMatch(
    seeker: Contact,
    candidates: Contact[],
    options: {
      query?: string;
      objectives?: OptimizationObjective[];
      constraints?: OptimizationConstraint[];
      diversityWeight?: number;
      maxResults?: number;
      minConfidence?: number;
    }
  ): Promise<EnhancedMatchingResult[]> {
    return this.findMatches({
      seeker,
      candidates,
      query: options.query,
      optimization: {
        objectives: options.objectives,
        diversityWeight: options.diversityWeight
      },
      options: {
        maxResults: options.maxResults,
        minConfidence: options.minConfidence,
        explainResults: true
      }
    });
  }

  /**
   * Example: Natural language matching
   */
  async matchFromNaturalLanguage(
    seekerProfile: Partial<Contact>,
    naturalLanguageQuery: string,
    candidates: Contact[]
  ): Promise<EnhancedMatchingResult[]> {
    // Parse natural language into structured request
    const parsedRequest = this.parseNaturalLanguage(naturalLanguageQuery);

    const seeker: Contact = {
      id: seekerProfile.id || 'temp_id',
      name: seekerProfile.name || 'Seeker',
      email: seekerProfile.email || 'seeker@example.com',
      ...seekerProfile,
      needs: parsedRequest.needs,
      offerings: parsedRequest.offerings,
      skills: seekerProfile.skills || [],
      tags: [],
      linkedinUrl: '',
      metadata: {
        ...seekerProfile.metadata,
        ...parsedRequest.metadata,
      }
    };

    return this.findMatches({
      seeker,
      candidates,
      query: naturalLanguageQuery,
      requirements: parsedRequest.requirements,
      options: { maxResults: 15, explainResults: true }
    });
  }

  /**
   * Helper: Parse natural language into structured requirements
   * Enhanced to include free text details in metadata
   */
  private parseNaturalLanguage(query: string): {
    needs: string[];
    offerings: string[];
    requirements: any;
    metadata?: Record<string, any>;
  } {
    const lowerQuery = query.toLowerCase();
    const needs: string[] = [];
    const offerings: string[] = [];
    const requirements: any = { must: {}, should: {} };
    const metadata: Record<string, any> = {
      needsDetails: query, // Store full query as additional context
    };

    // Extract needs
    if (lowerQuery.includes('need') || lowerQuery.includes('looking for')) {
      const needPatterns = [
        /need (?:a |an )?([^,.]+)/gi,
        /looking for (?:a |an )?([^,.]+)/gi,
        /seeking (?:a |an )?([^,.]+)/gi
      ];

      for (const pattern of needPatterns) {
        const matches = lowerQuery.matchAll(pattern);
        for (const match of matches) {
          needs.push(match[1].trim());
        }
      }
    }

    // Extract skills/expertise requirements
    if (lowerQuery.includes('expert') || lowerQuery.includes('experienced')) {
      needs.push('expertise');
    }

    if (lowerQuery.includes('developer') || lowerQuery.includes('engineer')) {
      needs.push('technical expertise');
      requirements.should.skills = ['JavaScript', 'Python', 'React'];
    }

    if (lowerQuery.includes('designer')) {
      needs.push('design expertise');
      requirements.should.skills = ['Figma', 'UI Design', 'UX'];
    }

    if (lowerQuery.includes('marketing')) {
      needs.push('marketing expertise');
      requirements.should.skills = ['Marketing', 'Growth', 'SEO'];
    }

    return { needs, offerings, requirements, metadata };
  }

  /**
   * Helper: Extract constraints from context
   */
  private extractConstraintsFromContext(context: MatchingContext): any {
    const constraints: any = {};

    if (context.temporal.urgency === 'immediate' || context.temporal.urgency === 'high') {
      // Prioritize recently active candidates
      constraints.recentActivityRequired = true;
    }

    if (context.economic.budgetConstraints === 'tight') {
      // Focus on non-monetary value exchange
      constraints.preferNonMonetary = true;
    }

    if (context.strategic.strategicPriority === 'quality') {
      // Higher quality threshold
      constraints.minQualityScore = 0.7;
    }

    return constraints;
  }

  /**
   * Helper: Merge strategy and optimization results
   */
  private mergeResults(strategyResults: any[], optResults: any[]): any[] {
    // Create a map of optimization results by candidate ID
    const optMap = new Map(optResults.map(r => [r.candidate.id, r]));

    // Merge data
    return strategyResults.map(strategyResult => {
      const optResult = optMap.get(strategyResult.candidate.id);

      if (optResult) {
        return {
          ...strategyResult,
          score: (strategyResult.score * 0.6) + (optResult.overallScore * 0.4),
          explanations: [
            ...strategyResult.explanations,
            ...optResult.tradeoffs
          ]
        };
      }

      return strategyResult;
    });
  }

  /**
   * Helper: Get numeric score from verification level
   */
  private getVerificationScore(level: string): number {
    const scores: Record<string, number> = {
      'premium': 1.0,
      'verified': 0.8,
      'basic': 0.6,
      'unverified': 0.4
    };
    return scores[level] || 0.5;
  }

  /**
   * Get system statistics
   */
  getStats(): {
    agentsActive: number;
    capabilities: string[];
    version: string;
  } {
    return {
      agentsActive: 5,
      capabilities: [
        'Dynamic Strategy Selection',
        'Context Understanding',
        'Multi-Criteria Optimization',
        'Profile Verification',
        'Natural Language Processing',
        'Pareto Optimization',
        'Diversity Optimization',
        'Trade-off Analysis'
      ],
      version: '2.0.0-enhanced'
    };
  }
}

// Example usage
export async function exampleUsage() {
  const orchestrator = new EnhancedMatchingOrchestrator();

  // Example 1: Simple natural language request
  const result1 = await orchestrator.matchFromNaturalLanguage(
    {
      name: 'Startup Founder',
      title: 'CEO',
      industry: 'Technology'
    },
    'I need an experienced full-stack developer who can help build my MVP quickly',
    [] // Would provide candidate list
  );

  // Example 2: Complex multi-criteria matching
  const seeker: Contact = {
    id: 'user123',
    name: 'Jane Doe',
    email: 'jane@example.com',
    title: 'CTO',
    industry: 'FinTech',
    needs: ['Senior Backend Engineer', 'Startup Experience'],
    offerings: ['Equity', 'Mentorship', 'Flexible Work'],
    skills: ['Leadership', 'Architecture'],
    tags: [],
    linkedinUrl: ''
  };

  const result2 = await orchestrator.findMatches({
    seeker,
    candidates: [], // Would provide list
    query: 'Looking for technical co-founder with fintech background',
    optimization: {
      objectives: orchestrator.optimizationAgent.createStandardObjectives(),
      diversityWeight: 0.3
    },
    options: {
      maxResults: 10,
      minConfidence: 0.7,
      explainResults: true
    }
  });

  console.log('Enhanced matching complete!');
  console.log(orchestrator.getStats());
}
