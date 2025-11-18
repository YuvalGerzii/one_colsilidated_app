import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Smart Match Filters & Preferences Service
 *
 * Implements AI-driven filtering with machine learning-based recommendations
 * Based on best practices from 2025 research:
 * - Auto-apply filters for immediate feedback
 * - ML-based filter suggestions from user behavior
 * - Multi-dimensional compatibility scoring
 * - Transparent match scores
 */

export interface FilterCriteria {
  // Location filters
  location?: {
    cities?: string[];
    countries?: string[];
    radius?: number; // km
    remote?: boolean;
  };

  // Industry & expertise filters
  industries?: string[];
  expertiseAreas?: string[];
  skillLevels?: ('beginner' | 'intermediate' | 'expert')[];

  // Network filters
  degreeOfSeparation?: number; // 1, 2, 3
  mutualConnections?: number; // minimum
  trustLevel?: number; // 0-1

  // Match type filters
  matchTypes?: string[];
  minCompatibilityScore?: number; // 0-1

  // Need/offering filters
  needCategories?: string[];
  offeringCategories?: string[];
  priority?: ('low' | 'medium' | 'high' | 'critical')[];

  // Availability filters
  responseTime?: ('immediate' | 'hours' | 'days' | 'flexible');
  availability?: string[]; // e.g., ['weekdays', 'evenings']

  // Business filters
  companySize?: ('startup' | 'small' | 'medium' | 'enterprise')[];
  fundingStage?: ('pre-seed' | 'seed' | 'series-a' | 'series-b+' | 'public')[];
  revenue?: { min?: number; max?: number };

  // Behavioral filters
  communicationStyle?: ('formal' | 'casual' | 'technical' | 'collaborative')[];
  decisionStyle?: ('data-driven' | 'intuitive' | 'consensus' | 'authoritative')[];

  // Custom filters (user-defined)
  customFilters?: Record<string, any>;
}

export interface FilterPreferences {
  userId: string;
  criteria: FilterCriteria;
  autoApply: boolean;
  saveAsDefault: boolean;
  name?: string; // For saved filter sets
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface FilterSuggestion {
  filterKey: string;
  filterValue: any;
  reason: string;
  confidence: number; // 0-1
  basedOn: 'behavior' | 'similar_users' | 'success_patterns' | 'ml_model';
}

export interface FilteredMatch {
  matchId: string;
  compatibilityScore: number;
  matchedCriteria: string[];
  unmatchedCriteria: string[];
  recommendationReason: string;
}

export class SmartFilterService {
  private pool: Pool;
  private redis: Redis;

  constructor(pool: Pool, redis: Redis) {
    this.pool = pool;
    this.redis = redis;
  }

  /**
   * Apply filters to match candidates
   * Implements auto-apply pattern for immediate feedback
   */
  async applyFilters(
    userId: string,
    criteria: FilterCriteria,
    limit: number = 50
  ): Promise<FilteredMatch[]> {
    const client = await this.pool.connect();

    try {
      // Build dynamic SQL query based on criteria
      const query = this.buildFilterQuery(userId, criteria);

      const result = await client.query(query.sql, query.params);

      // Calculate match scores and reasons
      const matches = await Promise.all(
        result.rows.map(row => this.enrichMatchData(row, criteria))
      );

      // Sort by compatibility score
      matches.sort((a, b) => b.compatibilityScore - a.compatibilityScore);

      // Track filter usage for ML recommendations
      await this.trackFilterUsage(userId, criteria, matches.length);

      return matches.slice(0, limit);
    } finally {
      client.release();
    }
  }

  /**
   * Build dynamic SQL query from filter criteria
   */
  private buildFilterQuery(userId: string, criteria: FilterCriteria): { sql: string; params: any[] } {
    const conditions: string[] = [];
    const params: any[] = [userId];
    let paramIndex = 2;

    let sql = `
      SELECT
        mc.*,
        up.needs,
        up.offerings,
        up.preferences,
        up.location,
        up.industry,
        up.expertise_areas,
        u.metadata
      FROM match_candidates mc
      JOIN agents a ON mc.agent_id = a.id
      JOIN user_profiles up ON a.user_id = up.user_id
      JOIN users u ON up.user_id = u.id
      WHERE mc.initiator_agent_id IN (
        SELECT id FROM agents WHERE user_id = $1
      )
      AND mc.status = 'active'
    `;

    // Location filters
    if (criteria.location) {
      if (criteria.location.cities && criteria.location.cities.length > 0) {
        conditions.push(`up.location->>'city' = ANY($${paramIndex})`);
        params.push(criteria.location.cities);
        paramIndex++;
      }

      if (criteria.location.countries && criteria.location.countries.length > 0) {
        conditions.push(`up.location->>'country' = ANY($${paramIndex})`);
        params.push(criteria.location.countries);
        paramIndex++;
      }

      if (criteria.location.remote !== undefined) {
        conditions.push(`(up.location->>'remote')::boolean = $${paramIndex}`);
        params.push(criteria.location.remote);
        paramIndex++;
      }
    }

    // Industry filters
    if (criteria.industries && criteria.industries.length > 0) {
      conditions.push(`up.industry = ANY($${paramIndex})`);
      params.push(criteria.industries);
      paramIndex++;
    }

    // Expertise filters
    if (criteria.expertiseAreas && criteria.expertiseAreas.length > 0) {
      conditions.push(`up.expertise_areas && $${paramIndex}`);
      params.push(criteria.expertiseAreas);
      paramIndex++;
    }

    // Network filters
    if (criteria.degreeOfSeparation !== undefined) {
      conditions.push(`(mc.metadata->>'degreeOfSeparation')::int <= $${paramIndex}`);
      params.push(criteria.degreeOfSeparation);
      paramIndex++;
    }

    if (criteria.trustLevel !== undefined) {
      conditions.push(`(mc.metadata->>'trustLevel')::float >= $${paramIndex}`);
      params.push(criteria.trustLevel);
      paramIndex++;
    }

    // Match type filters
    if (criteria.matchTypes && criteria.matchTypes.length > 0) {
      conditions.push(`mc.match_type = ANY($${paramIndex})`);
      params.push(criteria.matchTypes);
      paramIndex++;
    }

    // Compatibility score filter
    if (criteria.minCompatibilityScore !== undefined) {
      conditions.push(`mc.compatibility_score >= $${paramIndex}`);
      params.push(criteria.minCompatibilityScore);
      paramIndex++;
    }

    // Need category filters
    if (criteria.needCategories && criteria.needCategories.length > 0) {
      conditions.push(`
        EXISTS (
          SELECT 1 FROM jsonb_array_elements(up.needs) AS need
          WHERE need->>'category' = ANY($${paramIndex})
        )
      `);
      params.push(criteria.needCategories);
      paramIndex++;
    }

    // Offering category filters
    if (criteria.offeringCategories && criteria.offeringCategories.length > 0) {
      conditions.push(`
        EXISTS (
          SELECT 1 FROM jsonb_array_elements(up.offerings) AS offering
          WHERE offering->>'category' = ANY($${paramIndex})
        )
      `);
      params.push(criteria.offeringCategories);
      paramIndex++;
    }

    // Company size filter
    if (criteria.companySize && criteria.companySize.length > 0) {
      conditions.push(`u.metadata->>'companySize' = ANY($${paramIndex})`);
      params.push(criteria.companySize);
      paramIndex++;
    }

    // Funding stage filter
    if (criteria.fundingStage && criteria.fundingStage.length > 0) {
      conditions.push(`u.metadata->>'fundingStage' = ANY($${paramIndex})`);
      params.push(criteria.fundingStage);
      paramIndex++;
    }

    // Communication style filter
    if (criteria.communicationStyle && criteria.communicationStyle.length > 0) {
      conditions.push(`up.preferences->>'communicationStyle' = ANY($${paramIndex})`);
      params.push(criteria.communicationStyle);
      paramIndex++;
    }

    if (conditions.length > 0) {
      sql += ' AND ' + conditions.join(' AND ');
    }

    sql += ' ORDER BY mc.compatibility_score DESC';

    return { sql, params };
  }

  /**
   * Enrich match data with detailed scoring
   */
  private async enrichMatchData(row: any, criteria: FilterCriteria): Promise<FilteredMatch> {
    const matchedCriteria: string[] = [];
    const unmatchedCriteria: string[] = [];

    // Analyze which criteria matched
    if (criteria.location?.cities && criteria.location.cities.includes(row.location?.city)) {
      matchedCriteria.push('location');
    }

    if (criteria.industries && criteria.industries.includes(row.industry)) {
      matchedCriteria.push('industry');
    }

    if (criteria.minCompatibilityScore && row.compatibility_score >= criteria.minCompatibilityScore) {
      matchedCriteria.push('compatibility_score');
    }

    // Generate recommendation reason
    const reason = this.generateRecommendationReason(matchedCriteria, row);

    return {
      matchId: row.id,
      compatibilityScore: row.compatibility_score,
      matchedCriteria,
      unmatchedCriteria,
      recommendationReason: reason
    };
  }

  /**
   * Generate human-readable recommendation reason
   */
  private generateRecommendationReason(matchedCriteria: string[], row: any): string {
    const reasons: string[] = [];

    if (matchedCriteria.includes('location')) {
      reasons.push('same location');
    }

    if (matchedCriteria.includes('industry')) {
      reasons.push('industry match');
    }

    if (matchedCriteria.includes('compatibility_score')) {
      reasons.push('high compatibility');
    }

    if (reasons.length === 0) {
      return 'Matches your general preferences';
    }

    return `Recommended: ${reasons.join(', ')}`;
  }

  /**
   * Save filter preferences for a user
   */
  async saveFilterPreferences(preferences: FilterPreferences): Promise<void> {
    const client = await this.pool.connect();

    try {
      await client.query(
        `INSERT INTO filter_preferences (user_id, criteria, auto_apply, save_as_default, name, is_active)
         VALUES ($1, $2, $3, $4, $5, $6)
         ON CONFLICT (user_id, name)
         DO UPDATE SET
           criteria = $2,
           auto_apply = $3,
           save_as_default = $4,
           is_active = $6,
           updated_at = NOW()`,
        [
          preferences.userId,
          JSON.stringify(preferences.criteria),
          preferences.autoApply,
          preferences.saveAsDefault,
          preferences.name || 'default',
          preferences.isActive
        ]
      );

      // Cache in Redis for fast access
      await this.redis.setex(
        `filter:${preferences.userId}`,
        3600,
        JSON.stringify(preferences)
      );
    } finally {
      client.release();
    }
  }

  /**
   * Get filter preferences for a user
   */
  async getFilterPreferences(userId: string): Promise<FilterPreferences | null> {
    // Try cache first
    const cached = await this.redis.get(`filter:${userId}`);
    if (cached) {
      return JSON.parse(cached);
    }

    const client = await this.pool.connect();

    try {
      const result = await client.query(
        `SELECT * FROM filter_preferences
         WHERE user_id = $1 AND is_active = true
         ORDER BY save_as_default DESC, updated_at DESC
         LIMIT 1`,
        [userId]
      );

      if (result.rows.length === 0) {
        return null;
      }

      const row = result.rows[0];
      const preferences: FilterPreferences = {
        userId: row.user_id,
        criteria: row.criteria,
        autoApply: row.auto_apply,
        saveAsDefault: row.save_as_default,
        name: row.name,
        isActive: row.is_active,
        createdAt: row.created_at,
        updatedAt: row.updated_at
      };

      // Cache for future use
      await this.redis.setex(
        `filter:${userId}`,
        3600,
        JSON.stringify(preferences)
      );

      return preferences;
    } finally {
      client.release();
    }
  }

  /**
   * Get ML-based filter suggestions for a user
   * Based on behavior patterns and similar users
   */
  async getFilterSuggestions(userId: string): Promise<FilterSuggestion[]> {
    const suggestions: FilterSuggestion[] = [];

    const client = await this.pool.connect();

    try {
      // Analyze user's successful matches
      const successfulMatches = await client.query(
        `SELECT mc.match_type, mc.metadata, up.industry, up.location
         FROM match_candidates mc
         JOIN agents a ON mc.agent_id = a.id
         JOIN user_profiles up ON a.user_id = up.user_id
         WHERE mc.initiator_agent_id IN (
           SELECT id FROM agents WHERE user_id = $1
         )
         AND mc.status = 'accepted'
         ORDER BY mc.created_at DESC
         LIMIT 20`,
        [userId]
      );

      if (successfulMatches.rows.length > 0) {
        // Find common patterns in successful matches
        const industries = new Map<string, number>();
        const matchTypes = new Map<string, number>();

        successfulMatches.rows.forEach(row => {
          if (row.industry) {
            industries.set(row.industry, (industries.get(row.industry) || 0) + 1);
          }
          if (row.match_type) {
            matchTypes.set(row.match_type, (matchTypes.get(row.match_type) || 0) + 1);
          }
        });

        // Suggest most common industry
        const topIndustry = Array.from(industries.entries())
          .sort((a, b) => b[1] - a[1])[0];

        if (topIndustry && topIndustry[1] >= 3) {
          suggestions.push({
            filterKey: 'industries',
            filterValue: [topIndustry[0]],
            reason: `${topIndustry[1]} of your successful matches are in ${topIndustry[0]}`,
            confidence: Math.min(topIndustry[1] / successfulMatches.rows.length, 0.9),
            basedOn: 'success_patterns'
          });
        }

        // Suggest most common match type
        const topMatchType = Array.from(matchTypes.entries())
          .sort((a, b) => b[1] - a[1])[0];

        if (topMatchType && topMatchType[1] >= 3) {
          suggestions.push({
            filterKey: 'matchTypes',
            filterValue: [topMatchType[0]],
            reason: `You've had ${topMatchType[1]} successful ${topMatchType[0]} matches`,
            confidence: Math.min(topMatchType[1] / successfulMatches.rows.length, 0.9),
            basedOn: 'success_patterns'
          });
        }
      }

      // Find similar users and their filter preferences
      const similarUsers = await client.query(
        `SELECT fp.criteria, fp.user_id
         FROM filter_preferences fp
         JOIN user_profiles up1 ON fp.user_id = up1.user_id
         JOIN user_profiles up2 ON up2.user_id = $1
         WHERE fp.user_id != $1
         AND up1.industry = up2.industry
         AND fp.is_active = true
         LIMIT 10`,
        [userId]
      );

      if (similarUsers.rows.length > 0) {
        // Analyze common filters used by similar users
        const commonFilters = new Map<string, number>();

        similarUsers.rows.forEach(row => {
          const criteria = row.criteria as FilterCriteria;
          if (criteria.minCompatibilityScore) {
            commonFilters.set('minCompatibilityScore',
              (commonFilters.get('minCompatibilityScore') || 0) + 1);
          }
          if (criteria.degreeOfSeparation) {
            commonFilters.set('degreeOfSeparation',
              (commonFilters.get('degreeOfSeparation') || 0) + 1);
          }
        });

        if (commonFilters.get('minCompatibilityScore') &&
            commonFilters.get('minCompatibilityScore')! >= 3) {
          suggestions.push({
            filterKey: 'minCompatibilityScore',
            filterValue: 0.7,
            reason: 'Similar users find success with higher compatibility thresholds',
            confidence: 0.6,
            basedOn: 'similar_users'
          });
        }
      }

      return suggestions;
    } finally {
      client.release();
    }
  }

  /**
   * Track filter usage for ML learning
   */
  private async trackFilterUsage(
    userId: string,
    criteria: FilterCriteria,
    resultCount: number
  ): Promise<void> {
    try {
      await this.pool.query(
        `INSERT INTO filter_usage_log (user_id, criteria, result_count, timestamp)
         VALUES ($1, $2, $3, NOW())`,
        [userId, JSON.stringify(criteria), resultCount]
      );
    } catch (error) {
      // Log but don't fail the request
      console.error('Error tracking filter usage:', error);
    }
  }

  /**
   * Get popular filter combinations
   */
  async getPopularFilters(limit: number = 5): Promise<FilterCriteria[]> {
    const client = await this.pool.connect();

    try {
      const result = await client.query(
        `SELECT criteria, COUNT(*) as usage_count
         FROM filter_preferences
         WHERE is_active = true
         GROUP BY criteria
         ORDER BY usage_count DESC
         LIMIT $1`,
        [limit]
      );

      return result.rows.map(row => row.criteria);
    } finally {
      client.release();
    }
  }
}
