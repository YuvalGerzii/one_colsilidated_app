/**
 * Contextual Needs Agent
 * Analyzes needs with deep context understanding
 * Determines urgency, importance, complexity, scope, and appropriate helper tier
 */

import {
  Contact,
  ContextualNeedsAnalysis,
  UrgencyLevel,
  ImportanceLevel,
  ComplexityLevel,
  ScopeLevel,
  TimeHorizon,
  ResourceRequirements,
  ProfessionalTier,
  AgentType,
  AgentCapability
} from '../types';
import { v4 as uuidv4 } from 'uuid';

export class ContextualNeedsAgent {
  private agentType = AgentType.ANALYZER;
  private capabilities = [AgentCapability.ANALYZE, AgentCapability.EVALUATE];

  /**
   * Analyze a need with full context
   */
  async analyzeNeed(
    need: string,
    contact: Contact,
    context?: string
  ): Promise<ContextualNeedsAnalysis> {
    const needDescription = need;
    const combinedText = `${need} ${context || ''} ${contact.bio || ''}`;

    // Analyze multiple dimensions
    const urgency = this.analyzeUrgency(combinedText);
    const importance = this.analyzeImportance(combinedText, contact);
    const complexity = this.analyzeComplexity(combinedText);
    const scope = this.analyzeScope(combinedText, contact);
    const timeHorizon = this.analyzeTimeHorizon(combinedText);
    const resourceRequirements = this.analyzeResourceRequirements(combinedText);
    const keywords = this.extractKeywords(need);
    const relatedDomains = this.identifyDomains(need);
    const preferredHelperTier = this.determinePreferredHelperTier(
      complexity,
      scope,
      importance,
      contact
    );
    const successCriteria = this.extractSuccessCriteria(combinedText);

    return {
      needId: uuidv4(),
      needDescription,
      urgency,
      importance,
      complexity,
      scope,
      timeHorizon,
      resourceRequirements,
      successCriteria,
      keywords,
      relatedDomains,
      preferredHelperTier
    };
  }

  /**
   * Analyze all needs for a contact
   */
  async analyzeAllNeeds(contact: Contact): Promise<ContextualNeedsAnalysis[]> {
    if (!contact.needs || contact.needs.length === 0) {
      return [];
    }

    const analyses = await Promise.all(
      contact.needs.map(need => this.analyzeNeed(need, contact))
    );

    return analyses;
  }

  /**
   * Analyze urgency level
   */
  private analyzeUrgency(text: string): UrgencyLevel {
    const lowerText = text.toLowerCase();

    // Critical urgency indicators
    const criticalPatterns = [
      /\b(urgent|asap|immediately|emergency|critical|time.?sensitive|deadline.*today|right now)\b/i,
      /\b(crisis|breaking|failing|down|outage)\b/i
    ];

    if (criticalPatterns.some(p => p.test(lowerText))) {
      return UrgencyLevel.CRITICAL;
    }

    // High urgency
    const highPatterns = [
      /\b(soon|quickly|fast|this week|within.*days?|deadline.*week)\b/i,
      /\b(pressing|time.?critical)\b/i
    ];

    if (highPatterns.some(p => p.test(lowerText))) {
      return UrgencyLevel.HIGH;
    }

    // Medium urgency
    const mediumPatterns = [
      /\b(this month|within.*weeks?|upcoming|near.?term)\b/i,
      /\b(moderately urgent|prefer soon)\b/i
    ];

    if (mediumPatterns.some(p => p.test(lowerText))) {
      return UrgencyLevel.MEDIUM;
    }

    // Default to low urgency
    return UrgencyLevel.LOW;
  }

  /**
   * Analyze importance level
   */
  private analyzeImportance(text: string, contact: Contact): ImportanceLevel {
    const lowerText = text.toLowerCase();

    // Critical importance indicators
    const criticalPatterns = [
      /\b(critical|essential|vital|mission.?critical|must.?have|survival|existential)\b/i,
      /\b(make or break|business.?critical|core|fundamental)\b/i,
      /\b(company.*depends|revenue.*at.*stake)\b/i
    ];

    if (criticalPatterns.some(p => p.test(lowerText))) {
      return ImportanceLevel.CRITICAL;
    }

    // High importance
    const highPatterns = [
      /\b(important|significant|major|key|priority|strategic|crucial)\b/i,
      /\b(high.?impact|game.?changer|transformative)\b/i,
      /\b(competitive.*advantage|differentiat)\b/i
    ];

    if (highPatterns.some(p => p.test(lowerText))) {
      return ImportanceLevel.HIGH;
    }

    // Medium importance
    const mediumPatterns = [
      /\b(meaningful|valuable|beneficial|useful|helpful)\b/i,
      /\b(moderate.*impact|incremental)\b/i
    ];

    if (mediumPatterns.some(p => p.test(lowerText))) {
      return ImportanceLevel.MEDIUM;
    }

    // Default to low
    return ImportanceLevel.LOW;
  }

  /**
   * Analyze complexity level
   */
  private analyzeComplexity(text: string): ComplexityLevel {
    const lowerText = text.toLowerCase();
    let complexityScore = 0;

    // Technical complexity indicators
    const technicalPatterns = [
      /\b(algorithm|architecture|system.*design|distributed|scalable|optimization)\b/i,
      /\b(machine learning|ai|blockchain|quantum|advanced.*analytics)\b/i,
      /\b(enterprise|integration|migration|transformation)\b/i
    ];

    complexityScore += technicalPatterns.filter(p => p.test(lowerText)).length * 2;

    // Multi-dimensional indicators
    if (lowerText.match(/\b(multiple|various|several|cross.?functional|interdisciplinary)\b/i)) {
      complexityScore += 2;
    }

    // Expertise requirements
    if (lowerText.match(/\b(expert|specialist|deep.*knowledge|advanced|sophisticated)\b/i)) {
      complexityScore += 2;
    }

    // Simplicity indicators
    if (lowerText.match(/\b(simple|basic|straightforward|easy|quick.*question)\b/i)) {
      complexityScore -= 3;
    }

    // Determine level
    if (complexityScore >= 6) return ComplexityLevel.HIGHLY_COMPLEX;
    if (complexityScore >= 3) return ComplexityLevel.COMPLEX;
    if (complexityScore >= 1) return ComplexityLevel.MODERATE;
    return ComplexityLevel.SIMPLE;
  }

  /**
   * Analyze scope level
   */
  private analyzeScope(text: string, contact: Contact): ScopeLevel {
    const lowerText = text.toLowerCase();

    // Transformational scope
    const transformationalPatterns = [
      /\b(transform|revolution|industry.?wide|ecosystem|paradigm.*shift)\b/i,
      /\b(company.?wide|organization.?wide|enterprise.?level)\b/i,
      /\b(strategic.*initiative|major.*overhaul)\b/i
    ];

    if (transformationalPatterns.some(p => p.test(lowerText))) {
      return ScopeLevel.TRANSFORMATIONAL;
    }

    // Strategic scope
    const strategicPatterns = [
      /\b(strategic|long.?term|vision|roadmap|direction)\b/i,
      /\b(department|division|business.*unit)\b/i,
      /\b(multi.?year|platform|foundation)\b/i
    ];

    if (strategicPatterns.some(p => p.test(lowerText))) {
      return ScopeLevel.STRATEGIC;
    }

    // Operational scope
    const operationalPatterns = [
      /\b(team|project|process|workflow|operations?)\b/i,
      /\b(improve|optimize|streamline|enhance)\b/i
    ];

    if (operationalPatterns.some(p => p.test(lowerText))) {
      return ScopeLevel.OPERATIONAL;
    }

    // Default to tactical
    return ScopeLevel.TACTICAL;
  }

  /**
   * Analyze time horizon
   */
  private analyzeTimeHorizon(text: string): TimeHorizon {
    const lowerText = text.toLowerCase();

    // Immediate
    if (lowerText.match(/\b(today|tomorrow|this week|asap|immediately|now)\b/i)) {
      return TimeHorizon.IMMEDIATE;
    }

    // Short term
    if (lowerText.match(/\b(this month|next.*weeks?|1.?2.*weeks?|short.?term)\b/i)) {
      return TimeHorizon.SHORT_TERM;
    }

    // Medium term
    if (lowerText.match(/\b(quarter|2.?3.*months?|next.*months?|medium.?term)\b/i)) {
      return TimeHorizon.MEDIUM_TERM;
    }

    // Long term (default for strategic needs)
    if (lowerText.match(/\b(year|long.?term|future|strategic|roadmap)\b/i)) {
      return TimeHorizon.LONG_TERM;
    }

    // Default to medium term
    return TimeHorizon.MEDIUM_TERM;
  }

  /**
   * Analyze resource requirements
   */
  private analyzeResourceRequirements(text: string): ResourceRequirements {
    const lowerText = text.toLowerCase();

    // Time commitment
    let timeCommitment = 'Unknown';
    const timeMatch = lowerText.match(/(\d+)\s*(hour|minute|day|week|month)/i);
    if (timeMatch) {
      timeCommitment = timeMatch[0];
    } else if (lowerText.match(/\b(quick|brief|short)\b/i)) {
      timeCommitment = '30 minutes';
    } else if (lowerText.match(/\b(ongoing|continuous|long.?term)\b/i)) {
      timeCommitment = 'Ongoing commitment';
    } else if (lowerText.match(/\b(mentor|advise|guide)\b/i)) {
      timeCommitment = 'Regular sessions';
    }

    // Financial investment
    let financialInvestment: string | undefined;
    const moneyMatch = lowerText.match(/\$[\d,]+[kmb]?/i);
    if (moneyMatch) {
      financialInvestment = moneyMatch[0];
    } else if (lowerText.match(/\b(investment|funding|budget|capital)\b/i)) {
      financialInvestment = 'Investment required';
    }

    // Extract expertise requirements
    const expertise = this.extractExpertiseRequirements(text);

    // Network access
    let networkAccess: string[] | undefined;
    if (lowerText.match(/\b(introduction|connect.*with|access.*to)\b/i)) {
      networkAccess = ['Professional network'];
    }

    return {
      timeCommitment,
      financialInvestment,
      expertise,
      networkAccess
    };
  }

  /**
   * Extract expertise requirements
   */
  private extractExpertiseRequirements(text: string): string[] {
    const expertise: string[] = [];
    const lowerText = text.toLowerCase();

    // Technical domains
    const domains = [
      'machine learning', 'ai', 'data science', 'engineering',
      'product management', 'marketing', 'sales', 'finance',
      'operations', 'strategy', 'design', 'legal', 'hr',
      'blockchain', 'cloud', 'security', 'devops'
    ];

    for (const domain of domains) {
      if (lowerText.includes(domain)) {
        expertise.push(domain);
      }
    }

    // Extract from "need expert in X" patterns
    const expertMatch = lowerText.match(/expert.*in\s+([a-z\s]+)/i);
    if (expertMatch) {
      expertise.push(expertMatch[1].trim());
    }

    return expertise.length > 0 ? expertise : ['General expertise'];
  }

  /**
   * Extract success criteria
   */
  private extractSuccessCriteria(text: string): string[] {
    const criteria: string[] = [];
    const lowerText = text.toLowerCase();

    // Look for explicit goals
    const goalPatterns = [
      /goal.*is\s+to\s+([^.]+)/gi,
      /success.*means\s+([^.]+)/gi,
      /achieve\s+([^.]+)/gi,
      /looking.*to\s+([^.]+)/gi
    ];

    for (const pattern of goalPatterns) {
      const matches = text.matchAll(pattern);
      for (const match of matches) {
        criteria.push(match[1].trim());
      }
    }

    // Infer from context
    if (lowerText.includes('increase') || lowerText.includes('grow')) {
      criteria.push('Measurable growth');
    }
    if (lowerText.includes('reduce') || lowerText.includes('optimize')) {
      criteria.push('Efficiency improvement');
    }
    if (lowerText.includes('launch') || lowerText.includes('ship')) {
      criteria.push('Successful launch');
    }

    return criteria.length > 0 ? criteria : ['Successful resolution'];
  }

  /**
   * Extract keywords from need
   */
  private extractKeywords(need: string): string[] {
    const words = need.toLowerCase().split(/\s+/);

    // Filter out common words
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                               'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                               'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                               'could', 'may', 'might', 'can', 'i', 'you', 'we', 'they', 'it', 'this',
                               'that', 'these', 'those', 'need', 'want', 'help', 'looking']);

    const keywords = words
      .filter(w => w.length > 3 && !stopWords.has(w))
      .filter((w, i, arr) => arr.indexOf(w) === i); // unique

    return keywords.slice(0, 10); // Top 10 keywords
  }

  /**
   * Identify related domains
   */
  private identifyDomains(need: string): string[] {
    const lowerNeed = need.toLowerCase();
    const domains: string[] = [];

    const domainKeywords = {
      'Technology': ['software', 'tech', 'engineering', 'development', 'ai', 'ml', 'data'],
      'Business': ['business', 'strategy', 'growth', 'revenue', 'sales', 'market'],
      'Product': ['product', 'design', 'user', 'feature', 'roadmap'],
      'Finance': ['finance', 'funding', 'investment', 'capital', 'budget'],
      'Marketing': ['marketing', 'brand', 'content', 'seo', 'advertising'],
      'Operations': ['operations', 'process', 'efficiency', 'logistics'],
      'HR': ['hiring', 'recruitment', 'talent', 'culture', 'team'],
      'Legal': ['legal', 'compliance', 'regulation', 'contract'],
      'Design': ['design', 'ux', 'ui', 'visual', 'creative']
    };

    for (const [domain, keywords] of Object.entries(domainKeywords)) {
      if (keywords.some(kw => lowerNeed.includes(kw))) {
        domains.push(domain);
      }
    }

    return domains.length > 0 ? domains : ['General'];
  }

  /**
   * Determine preferred helper tier based on need characteristics
   */
  private determinePreferredHelperTier(
    complexity: ComplexityLevel,
    scope: ScopeLevel,
    importance: ImportanceLevel,
    contact: Contact
  ): ProfessionalTier[] {
    const tiers: ProfessionalTier[] = [];

    // Highly complex needs require senior expertise
    if (complexity === ComplexityLevel.HIGHLY_COMPLEX) {
      tiers.push(ProfessionalTier.SENIOR, ProfessionalTier.EXECUTIVE);
    }

    // Transformational or strategic scope
    if (scope === ScopeLevel.TRANSFORMATIONAL) {
      tiers.push(ProfessionalTier.C_LEVEL, ProfessionalTier.FOUNDER_CEO, ProfessionalTier.EXECUTIVE);
    } else if (scope === ScopeLevel.STRATEGIC) {
      tiers.push(ProfessionalTier.EXECUTIVE, ProfessionalTier.SENIOR);
    }

    // Critical importance
    if (importance === ImportanceLevel.CRITICAL) {
      if (!tiers.includes(ProfessionalTier.EXECUTIVE)) {
        tiers.push(ProfessionalTier.EXECUTIVE);
      }
    }

    // Moderate/simple can be helped by mid-level
    if (complexity === ComplexityLevel.MODERATE || complexity === ComplexityLevel.SIMPLE) {
      if (scope === ScopeLevel.TACTICAL || scope === ScopeLevel.OPERATIONAL) {
        tiers.push(ProfessionalTier.MID_LEVEL, ProfessionalTier.SENIOR);
      }
    }

    // Default to at least senior
    if (tiers.length === 0) {
      tiers.push(ProfessionalTier.SENIOR, ProfessionalTier.MID_LEVEL);
    }

    // Remove duplicates and sort by seniority
    const uniqueTiers = [...new Set(tiers)];
    const tierOrder = [
      ProfessionalTier.MID_LEVEL,
      ProfessionalTier.SENIOR,
      ProfessionalTier.EXECUTIVE,
      ProfessionalTier.C_LEVEL,
      ProfessionalTier.FOUNDER_CEO,
      ProfessionalTier.LUMINARY
    ];

    return uniqueTiers.sort((a, b) => tierOrder.indexOf(a) - tierOrder.indexOf(b));
  }

  /**
   * Calculate alignment score between two contextual needs
   */
  calculateNeedsAlignment(
    need1: ContextualNeedsAnalysis,
    need2: ContextualNeedsAnalysis
  ): number {
    let alignment = 0;

    // Domain overlap
    const domainOverlap = need1.relatedDomains.filter(d =>
      need2.relatedDomains.includes(d)
    ).length;
    alignment += (domainOverlap / Math.max(need1.relatedDomains.length, 1)) * 30;

    // Keyword overlap
    const keywordOverlap = need1.keywords.filter(k =>
      need2.keywords.includes(k)
    ).length;
    alignment += (keywordOverlap / Math.max(need1.keywords.length, 1)) * 25;

    // Complexity match (similar complexity works well)
    const complexityMatch = need1.complexity === need2.complexity ? 15 : 0;
    alignment += complexityMatch;

    // Urgency compatibility
    const urgencyMatch = need1.urgency === need2.urgency ? 10 : 5;
    alignment += urgencyMatch;

    // Scope alignment
    const scopeMatch = need1.scope === need2.scope ? 10 : 5;
    alignment += scopeMatch;

    return Math.min(100, Math.round(alignment));
  }
}
