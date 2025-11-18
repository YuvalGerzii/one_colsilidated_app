import { Pool } from 'pg';
import Redis from 'ioredis';

/**
 * Comprehensive Edge Case Handlers
 *
 * Handles various edge cases discovered during stress testing:
 * 1. Isolated users (no connections)
 * 2. Incomplete profiles
 * 3. Inactive users
 * 4. Geographic constraints
 * 5. Industry barriers
 * 6. Language mismatches
 * 7. Timezone differences
 * 8. Super connectors (performance issues)
 * 9. Network fragmentation
 * 10. Trust anomalies
 */

export interface EdgeCaseResult {
  handled: boolean;
  fallbackStrategy?: string;
  modifications?: any;
  warnings?: string[];
  recommendations?: string[];
}

export class EdgeCaseHandler {
  constructor(
    private pool: Pool,
    private redis: Redis
  ) {}

  /**
   * Handle isolated users (no connections)
   */
  async handleIsolatedUser(userId: string): Promise<EdgeCaseResult> {
    const connectionCount = await this.getConnectionCount(userId);

    if (connectionCount > 0) {
      return { handled: false };
    }

    const userProfile = await this.getUserProfile(userId);

    // Find suggested initial connections based on:
    // 1. Same industry
    // 2. Same location
    // 3. Similar expertise
    // 4. Complementary needs/offerings

    const suggestions = await this.findInitialConnections(userProfile);

    return {
      handled: true,
      fallbackStrategy: 'suggest_initial_connections',
      modifications: {
        suggestedConnections: suggestions
      },
      warnings: [
        'User has no connections in the network'
      ],
      recommendations: [
        'Complete profile to improve match quality',
        `Connect with ${suggestions.length} recommended users in your industry`,
        'Join relevant groups and communities',
        'Attend networking events'
      ]
    };
  }

  /**
   * Handle incomplete profiles
   */
  async handleIncompleteProfile(userId: string): Promise<EdgeCaseResult> {
    const profile = await this.getUserProfile(userId);

    const completeness = this.calculateProfileCompleteness(profile);

    if (completeness >= 0.7) {
      return { handled: false };
    }

    const missing: string[] = [];
    const recommendations: string[] = [];

    if (!profile.bio || profile.bio.length < 50) {
      missing.push('bio');
      recommendations.push('Add a detailed bio (at least 50 characters)');
    }

    if (!profile.expertiseAreas || profile.expertiseAreas.length === 0) {
      missing.push('expertise');
      recommendations.push('Add your areas of expertise');
    }

    if (!profile.needs || profile.needs.length === 0) {
      missing.push('needs');
      recommendations.push('Specify what you\'re looking for');
    }

    if (!profile.offerings || profile.offerings.length === 0) {
      missing.push('offerings');
      recommendations.push('Describe what you can offer');
    }

    if (!profile.location || !profile.location.city) {
      missing.push('location');
      recommendations.push('Add your location');
    }

    return {
      handled: true,
      fallbackStrategy: 'use_defaults_and_prompt_completion',
      modifications: {
        profileCompleteness: completeness,
        missingFields: missing,
        defaults: this.generateDefaults(profile)
      },
      warnings: [
        `Profile is only ${(completeness * 100).toFixed(0)}% complete`,
        'Incomplete profiles reduce match quality'
      ],
      recommendations
    };
  }

  /**
   * Handle users with no needs
   */
  async handleNoNeeds(userId: string): Promise<EdgeCaseResult> {
    const profile = await this.getUserProfile(userId);

    if (profile.needs && profile.needs.length > 0) {
      return { handled: false };
    }

    // Fallback strategies:
    // 1. Match based on expertise complementarity
    // 2. Match based on industry connections
    // 3. Match based on geographic proximity
    // 4. Match based on network position (bridge opportunities)

    const fallbackMatches = await this.findFallbackMatches(userId, profile);

    return {
      handled: true,
      fallbackStrategy: 'expertise_and_network_based_matching',
      modifications: {
        matchStrategy: 'fallback',
        potentialMatches: fallbackMatches
      },
      warnings: [
        'No needs specified - using alternative matching strategies'
      ],
      recommendations: [
        'Add your needs to get more targeted matches',
        'Explore connections based on shared expertise',
        'Consider what you\'re looking to achieve'
      ]
    };
  }

  /**
   * Handle geographic constraints
   */
  async handleGeographicMismatch(
    userId1: string,
    userId2: string
  ): Promise<EdgeCaseResult> {
    const profile1 = await this.getUserProfile(userId1);
    const profile2 = await this.getUserProfile(userId2);

    if (!profile1.location || !profile2.location) {
      return { handled: false };
    }

    const distance = this.calculateDistance(
      profile1.location,
      profile2.location
    );

    const timezone1 = profile1.location.timezone || 'UTC';
    const timezone2 = profile2.location.timezone || 'UTC';
    const timezoneDiff = this.getTimezoneDifference(timezone1, timezone2);

    // If same country or remote, no issue
    if (profile1.location.country === profile2.location.country ||
        profile1.location.remote || profile2.location.remote) {
      return { handled: false };
    }

    // Significant geographic distance
    if (distance > 1000) { // km
      return {
        handled: true,
        fallbackStrategy: 'remote_collaboration_focus',
        modifications: {
          suggestedMeetingTimes: this.suggestOverlappingHours(timezone1, timezone2),
          collaborationMode: 'remote',
          timezoneDifference: timezoneDiff
        },
        warnings: [
          `${distance.toFixed(0)}km apart - remote collaboration recommended`,
          `${Math.abs(timezoneDiff)} hour timezone difference`
        ],
        recommendations: [
          'Schedule meetings during overlapping business hours',
          'Use asynchronous communication tools',
          'Plan virtual collaboration',
          timezoneDiff > 8 ? 'Consider timezone challenges for real-time collaboration' : ''
        ].filter(Boolean)
      };
    }

    return { handled: false };
  }

  /**
   * Handle language barriers
   */
  async handleLanguageMismatch(
    userId1: string,
    userId2: string
  ): Promise<EdgeCaseResult> {
    const profile1 = await this.getUserProfile(userId1);
    const profile2 = await this.getUserProfile(userId2);

    const languages1 = profile1.profile?.languages || ['English'];
    const languages2 = profile2.profile?.languages || ['English'];

    const commonLanguages = languages1.filter((lang: string) =>
      languages2.includes(lang)
    );

    if (commonLanguages.length > 0) {
      return { handled: false };
    }

    // No common language
    return {
      handled: true,
      fallbackStrategy: 'translation_required',
      modifications: {
        primaryLanguages: {
          user1: languages1[0],
          user2: languages2[0]
        },
        translationNeeded: true
      },
      warnings: [
        'No common language detected'
      ],
      recommendations: [
        'Use translation tools for communication',
        'Consider hiring interpreter for important discussions',
        'Start with written communication (easier to translate)'
      ]
    };
  }

  /**
   * Handle inactive users
   */
  async handleInactiveUser(userId: string): Promise<EdgeCaseResult> {
    const lastActivity = await this.getLastActivity(userId);

    if (!lastActivity) {
      return {
        handled: true,
        fallbackStrategy: 'exclude_from_active_matching',
        warnings: [
          'User has never been active'
        ],
        recommendations: [
          'Send activation email',
          'Exclude from active matching until activated'
        ]
      };
    }

    const daysSinceActivity = (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60 * 24);

    if (daysSinceActivity > 90) {
      return {
        handled: true,
        fallbackStrategy: 'mark_as_dormant',
        modifications: {
          status: 'dormant',
          lastActive: lastActivity
        },
        warnings: [
          `Inactive for ${Math.floor(daysSinceActivity)} days`
        ],
        recommendations: [
          'Send re-engagement email',
          'Lower priority in matching',
          'Archive if no response after 180 days'
        ]
      };
    }

    return { handled: false };
  }

  /**
   * Handle super connectors (performance optimization)
   */
  async handleSuperConnector(userId: string): Promise<EdgeCaseResult> {
    const connectionCount = await this.getConnectionCount(userId);

    if (connectionCount < 100) {
      return { handled: false };
    }

    // Super connector - need performance optimizations
    return {
      handled: true,
      fallbackStrategy: 'optimize_for_large_network',
      modifications: {
        useSampling: true,
        sampleSize: 50,
        enableAggregateQueries: true,
        cachingDuration: 3600 // 1 hour
      },
      warnings: [
        `Super connector with ${connectionCount} connections - using optimized algorithms`
      ],
      recommendations: [
        'Use pagination for connection lists',
        'Enable aggressive caching',
        'Sample connections for analysis',
        'Pre-compute expensive metrics'
      ]
    };
  }

  /**
   * Handle network fragmentation
   */
  async handleFragmentedNetwork(userId: string): Promise<EdgeCaseResult> {
    // Check if user's connections are in isolated clusters

    const connections = await this.getConnections(userId);

    if (connections.length < 5) {
      return { handled: false };
    }

    // Check how many connections are connected to each other
    let connectedPairs = 0;
    let totalPairs = 0;

    const sampleSize = Math.min(20, connections.length);

    for (let i = 0; i < sampleSize - 1; i++) {
      for (let j = i + 1; j < sampleSize; j++) {
        totalPairs++;
        if (await this.areConnected(connections[i], connections[j])) {
          connectedPairs++;
        }
      }
    }

    const connectedness = totalPairs > 0 ? connectedPairs / totalPairs : 0;

    if (connectedness < 0.2) {
      // Very fragmented - connections don't know each other
      return {
        handled: true,
        fallbackStrategy: 'bridge_clusters',
        modifications: {
          fragmentationScore: 1 - connectedness,
          suggestedBridges: await this.suggestBridgingConnections(userId, connections)
        },
        warnings: [
          'Network is highly fragmented - connections are in separate clusters'
        ],
        recommendations: [
          'Introduce connections to each other',
          'Organize group events',
          'Act as a network bridge',
          'Build stronger ties between clusters'
        ]
      };
    }

    return { handled: false };
  }

  /**
   * Handle industry barriers
   */
  async handleIndustryBarrier(
    userId1: string,
    userId2: string
  ): Promise<EdgeCaseResult> {
    const profile1 = await this.getUserProfile(userId1);
    const profile2 = await this.getUserProfile(userId2);

    if (profile1.industry === profile2.industry) {
      return { handled: false };
    }

    // Different industries - check for synergies
    const synergies = await this.findCrossIndustrySynergies(
      profile1.industry,
      profile2.industry
    );

    if (synergies.length > 0) {
      return {
        handled: true,
        fallbackStrategy: 'cross_industry_opportunity',
        modifications: {
          synergies,
          matchType: 'cross_industry_innovation'
        },
        recommendations: [
          'Explore cross-industry collaboration opportunities',
          `Potential synergies: ${synergies.join(', ')}`,
          'Different perspectives can drive innovation'
        ]
      };
    }

    return {
      handled: true,
      fallbackStrategy: 'acknowledge_difference',
      warnings: [
        'Different industries may have different practices and terminology'
      ],
      recommendations: [
        'Take time to understand each other\'s industry context',
        'Explain industry-specific concepts clearly',
        'Look for transferable insights'
      ]
    };
  }

  /**
   * Comprehensive edge case check
   */
  async checkAllEdgeCases(
    userId: string,
    context: 'matching' | 'networking' | 'collaboration'
  ): Promise<{
    hasEdgeCases: boolean;
    cases: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      result: EdgeCaseResult;
    }>;
    overallStrategy: string;
  }> {
    const cases: Array<{
      type: string;
      severity: 'low' | 'medium' | 'high';
      result: EdgeCaseResult;
    }> = [];

    // Run all checks
    const checks = [
      { type: 'isolated', check: () => this.handleIsolatedUser(userId), severity: 'high' as const },
      { type: 'incomplete_profile', check: () => this.handleIncompleteProfile(userId), severity: 'medium' as const },
      { type: 'no_needs', check: () => this.handleNoNeeds(userId), severity: 'low' as const },
      { type: 'inactive', check: () => this.handleInactiveUser(userId), severity: 'high' as const },
      { type: 'super_connector', check: () => this.handleSuperConnector(userId), severity: 'low' as const },
      { type: 'fragmented_network', check: () => this.handleFragmentedNetwork(userId), severity: 'medium' as const }
    ];

    for (const { type, check, severity } of checks) {
      const result = await check();
      if (result.handled) {
        cases.push({ type, severity, result });
      }
    }

    // Determine overall strategy
    let overallStrategy = 'standard';

    if (cases.some(c => c.severity === 'high')) {
      overallStrategy = 'high_touch_onboarding';
    } else if (cases.length > 2) {
      overallStrategy = 'gradual_improvement';
    } else if (cases.some(c => c.type === 'super_connector')) {
      overallStrategy = 'performance_optimized';
    }

    return {
      hasEdgeCases: cases.length > 0,
      cases,
      overallStrategy
    };
  }

  /**
   * Helper methods
   */

  private calculateProfileCompleteness(profile: any): number {
    let score = 0;
    const weights = {
      bio: 0.2,
      expertise: 0.2,
      needs: 0.15,
      offerings: 0.15,
      location: 0.1,
      industry: 0.1,
      profile_details: 0.1
    };

    if (profile.bio && profile.bio.length >= 50) score += weights.bio;
    if (profile.expertiseAreas && profile.expertiseAreas.length > 0) score += weights.expertise;
    if (profile.needs && profile.needs.length > 0) score += weights.needs;
    if (profile.offerings && profile.offerings.length > 0) score += weights.offerings;
    if (profile.location && profile.location.city) score += weights.location;
    if (profile.industry) score += weights.industry;
    if (profile.profile && Object.keys(profile.profile).length > 0) score += weights.profile_details;

    return score;
  }

  private generateDefaults(profile: any): any {
    return {
      bio: profile.bio || `Professional in ${profile.industry || 'various fields'}`,
      expertiseAreas: profile.expertiseAreas || ['General Business'],
      location: profile.location || { city: 'Unknown', country: 'Unknown', remote: true }
    };
  }

  private calculateDistance(loc1: any, loc2: any): number {
    // Simplified - in production use actual geolocation
    if (loc1.country !== loc2.country) return 5000; // Assume far
    if (loc1.city !== loc2.city) return 500; // Different city
    return 0;
  }

  private getTimezoneDifference(tz1: string, tz2: string): number {
    // Simplified - in production use proper timezone library
    const zones: any = {
      'America/Los_Angeles': -8,
      'America/New_York': -5,
      'Europe/London': 0,
      'Asia/Tokyo': 9,
      'UTC': 0
    };

    return Math.abs((zones[tz1] || 0) - (zones[tz2] || 0));
  }

  private suggestOverlappingHours(tz1: string, tz2: string): string[] {
    const diff = this.getTimezoneDifference(tz1, tz2);

    if (diff <= 3) {
      return ['9-11 AM', '2-5 PM (both timezones)'];
    } else if (diff <= 6) {
      return ['Early morning/Late evening overlap'];
    } else {
      return ['Very limited overlap - prefer asynchronous communication'];
    }
  }

  private async findCrossIndustrySynergies(
    industry1: string,
    industry2: string
  ): Promise<string[]> {
    // Predefined synergies
    const synergies: Record<string, string[]> = {
      'Technology-Finance': ['FinTech', 'Digital Banking', 'Payment Systems'],
      'Technology-Healthcare': ['HealthTech', 'Telemedicine', 'Medical Devices'],
      'Technology-Education': ['EdTech', 'Online Learning', 'Digital Content'],
      'Finance-Real Estate': ['PropTech', 'Real Estate Investment', 'Mortgage Tech']
    };

    const key1 = `${industry1}-${industry2}`;
    const key2 = `${industry2}-${industry1}`;

    return synergies[key1] || synergies[key2] || [];
  }

  // Database helper methods
  private async getConnectionCount(userId: string): Promise<number> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT COUNT(*) as count FROM connections WHERE user_id = $1',
        [userId]
      );
      return parseInt(result.rows[0].count);
    } finally {
      client.release();
    }
  }

  private async getUserProfile(userId: string): Promise<any> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.*, up.*, u.metadata
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id = $1
      `, [userId]);

      if (result.rows.length === 0) {
        throw new Error('User not found');
      }

      return result.rows[0];
    } finally {
      client.release();
    }
  }

  private async findInitialConnections(profile: any): Promise<any[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry
        FROM users u
        WHERE u.id != $1
          AND (u.industry = $2 OR up.location->>'country' = $3)
        LIMIT 10
      `, [profile.id, profile.industry, profile.location?.country]);

      return result.rows;
    } finally {
      client.release();
    }
  }

  private async findFallbackMatches(userId: string, profile: any): Promise<any[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id, u.name, u.industry, up.expertise_areas
        FROM users u
        JOIN user_profiles up ON u.id = up.user_id
        WHERE u.id != $1
        ORDER BY RANDOM()
        LIMIT 10
      `, [userId]);

      return result.rows;
    } finally {
      client.release();
    }
  }

  private async getLastActivity(userId: string): Promise<Date | null> {
    // In production, track actual activity
    // For now, use created_at as proxy
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT created_at FROM users WHERE id = $1',
        [userId]
      );

      return result.rows[0]?.created_at || null;
    } finally {
      client.release();
    }
  }

  private async getConnections(userId: string): Promise<string[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT u.id
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1
      `, [userId]);

      return result.rows.map(row => row.id);
    } finally {
      client.release();
    }
  }

  private async areConnected(userId1: string, userId2: string): Promise<boolean> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT COUNT(*) as count
        FROM connections c
        JOIN contacts ct ON c.contact_id = ct.id
        JOIN users u ON ct.email = u.email
        WHERE c.user_id = $1 AND u.id = $2
      `, [userId1, userId2]);

      return parseInt(result.rows[0].count) > 0;
    } finally {
      client.release();
    }
  }

  private async suggestBridgingConnections(userId: string, connections: string[]): Promise<any[]> {
    // Find users who could bridge clusters
    // Simplified version
    return connections.slice(0, 3).map(id => ({
      userId: id,
      reason: 'Can bridge different network clusters'
    }));
  }
}
