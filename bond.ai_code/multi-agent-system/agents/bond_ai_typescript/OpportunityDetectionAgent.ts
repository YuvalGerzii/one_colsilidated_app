import { Pool } from 'pg';
import Redis from 'ioredis';
import { MatchQualityAgent } from './MatchQualityAgent';
import { CommunityDetectionAgent } from './CommunityDetectionAgent';
import { SerendipityAgent } from './SerendipityAgent';

/**
 * Opportunity Detection Agent
 *
 * Proactively detects and surfaces collaboration, introduction,
 * hiring, and investment opportunities in user networks.
 */

export interface Opportunity {
  id: string;
  type: 'collaboration' | 'introduction' | 'hiring' | 'investment' | 'knowledge_exchange' | 'event';
  title: string;
  description: string;

  participants: string[];
  participantNames: string[];

  score: number; // 0-100
  confidence: number; // 0-1

  reasoning: string[];
  potentialValue: number; // 0-1

  timeframe: 'immediate' | 'short_term' | 'medium_term' | 'long_term';
  effort: 'low' | 'medium' | 'high';

  nextSteps: string[];
  risks: string[];
}

export class OpportunityDetectionAgent {
  constructor(
    private pool: Pool,
    private redis: Redis,
    private matchQuality: MatchQualityAgent,
    private community: CommunityDetectionAgent,
    private serendipity: SerendipityAgent
  ) {}

  async detectOpportunities(
    userId: string,
    type?: 'collaboration' | 'introduction' | 'hiring' | 'investment' | 'all'
  ): Promise<Opportunity[]> {
    const opportunities: Opportunity[] = [];

    if (!type || type === 'all' || type === 'collaboration') {
      opportunities.push(...await this.detectCollaborationOpportunities(userId));
    }

    if (!type || type === 'all' || type === 'introduction') {
      opportunities.push(...await this.detectIntroductionOpportunities(userId));
    }

    return opportunities.sort((a, b) => b.score - a.score).slice(0, 10);
  }

  private async detectCollaborationOpportunities(userId: string): Promise<Opportunity[]> {
    const serendipityMatches = await this.serendipity.findSerendipitousMatches(userId, 20);

    return serendipityMatches.slice(0, 5).map((match, i) => ({
      id: `collab_${userId}_${match.targetId}_${Date.now()}_${i}`,
      type: 'collaboration' as const,
      title: `Collaborate with ${match.targetName}`,
      description: match.insight,
      participants: [userId, match.targetId],
      participantNames: ['You', match.targetName],
      score: Math.round(match.serendipityScore * 100),
      confidence: match.serendipityScore,
      reasoning: match.reasons.map(r => r.description),
      potentialValue: match.bridgeValue,
      timeframe: 'short_term' as const,
      effort: 'medium' as const,
      nextSteps: ['Reach out with collaboration idea', 'Schedule intro call'],
      risks: [],
    }));
  }

  private async detectIntroductionOpportunities(userId: string): Promise<Opportunity[]> {
    // Simplified implementation
    return [];
  }
}
