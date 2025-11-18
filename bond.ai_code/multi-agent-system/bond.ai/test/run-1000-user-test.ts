/**
 * Runner script for 1000 user test
 * Executes comprehensive matching test and generates analysis report
 */

import { ComprehensiveMatchingTest } from './1000-user-matching-test';
import { IntelligenceEngine } from '../src/intelligence/IntelligenceEngine';
import { NetworkMapper } from '../src/network/NetworkMapper';
import { MatchingEngine } from '../src/matching/MatchingEngine';
import { Contact } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

interface MatchAnalysis {
  totalMatches: number;
  forcedConnections: number;
  pureMatches: number;
  averageMatchQuality: number;
  biases: Array<{
    type: string;
    description: string;
    severity: 'high' | 'medium' | 'low';
  }>;
  recommendations: string[];
}

async function runTest() {
  console.log('='.repeat(60));
  console.log('BOND.AI: 1000 RANDOM USER MATCHING TEST');
  console.log('='.repeat(60));
  console.log('\n');

  // Initialize engines
  const networkMapper = new NetworkMapper();
  const intelligenceEngine = new IntelligenceEngine();

  // Create test instance
  const test = new ComprehensiveMatchingTest(intelligenceEngine, networkMapper);

  console.log('Step 1: Generating 1000 random users...\n');
  const users = test.generateUsers();
  console.log(`✓ Generated ${users.length} diverse users\n`);

  // Add users to network
  users.forEach(user => networkMapper.addContact(user));

  console.log('Step 2: Running comprehensive test suite...\n');
  await test.runTests();

  console.log('\n\nStep 3: Analyzing matches for forced connections...\n');
  const matchingEngine = new MatchingEngine(networkMapper, intelligenceEngine);
  const analysis = await analyzeMatchingQuality(users, matchingEngine);

  printMatchAnalysis(analysis);
  saveMatchAnalysis(analysis);

  console.log('\n\n✓ Test complete! Check test-reports directory for detailed results.\n');
}

async function analyzeMatchingQuality(
  users: Contact[],
  matchingEngine: MatchingEngine
): Promise<MatchAnalysis> {
  const analysis: MatchAnalysis = {
    totalMatches: 0,
    forcedConnections: 0,
    pureMatches: 0,
    averageMatchQuality: 0,
    biases: [],
    recommendations: []
  };

  let totalScore = 0;
  const allMatches: any[] = [];

  // Analyze matches for sample of users (to avoid excessive computation)
  const sampleSize = Math.min(50, users.length);
  const sampleUsers = users.slice(0, sampleSize);

  console.log(`Analyzing matches for ${sampleSize} sample users...`);

  for (const user of sampleUsers) {
    try {
      const matches = await matchingEngine.findMatches(user);
      analysis.totalMatches += matches.length;

      for (const match of matches) {
        totalScore += match.overallScore;
        allMatches.push(match);

        // Detect forced connections
        // A connection is "forced" if:
        // 1. Low compatibility score but high overall score (weighted unfairly)
        // 2. Match exists despite no complementary needs
        // 3. Industry or location bias overrides actual fit

        const isForced = detectForcedConnection(match);
        if (isForced) {
          analysis.forcedConnections++;
        } else {
          analysis.pureMatches++;
        }
      }
    } catch (error) {
      console.error(`Error analyzing matches for user ${user.id}:`, error);
    }
  }

  analysis.averageMatchQuality = totalScore / Math.max(analysis.totalMatches, 1);

  // Detect biases
  analysis.biases = detectBiases(allMatches);

  // Generate recommendations
  analysis.recommendations = generateRecommendations(analysis);

  return analysis;
}

function detectForcedConnection(match: any): boolean {
  const flags: string[] = [];

  // Flag 1: Low compatibility but high overall score
  // This suggests the algorithm is weighting other factors too heavily
  if (match.compatibilityScore < 0.5 && match.overallScore > 0.7) {
    return true;
  }

  // Flag 2: No complementary needs match
  // If needsMatch dimension is very low but match exists, it's likely forced
  if (match.reasons) {
    const hasComplementaryNeeds = match.reasons.some(
      (r: any) => r.type === 'complementary_needs' && r.score > 0.4
    );

    if (!hasComplementaryNeeds && match.overallScore > 0.6) {
      return true; // Forced - no real need alignment
    }
  }

  // Flag 3: Only matched on superficial criteria (industry/location)
  // without substance
  const hasSubstantiveMatch = match.reasons?.some(
    (r: any) => ['complementary_needs', 'skill_match', 'business_opportunity'].includes(r.type)
  );

  if (!hasSubstantiveMatch && match.overallScore > 0.5) {
    return true; // Forced - only superficial matching
  }

  return false;
}

function detectBiases(matches: any[]): Array<{
  type: string;
  description: string;
  severity: 'high' | 'medium' | 'low';
}> {
  const biases = [];

  // Check for industry bias
  const industryMatches = matches.filter(m =>
    m.reasons?.some((r: any) => r.type === 'industry_synergy')
  );

  if (industryMatches.length / matches.length > 0.6) {
    biases.push({
      type: 'Industry Bias',
      description: `${(industryMatches.length / matches.length * 100).toFixed(0)}% of matches heavily weighted by same industry, potentially ignoring cross-industry opportunities`,
      severity: 'high' as const
    });
  }

  // Check for executive bias
  const executiveMatches = matches.filter(m =>
    m.valuePotential > 0.8 &&
    (m.sourceContact.title?.toLowerCase().includes('executive') ||
     m.targetContact.title?.toLowerCase().includes('ceo'))
  );

  if (executiveMatches.length / matches.length > 0.4) {
    biases.push({
      type: 'Executive/Title Bias',
      description: 'Algorithm disproportionately favors executive titles regardless of actual fit',
      severity: 'high' as const
    });
  }

  // Check for skill overlap bias
  const skillOnlyMatches = matches.filter(m =>
    m.reasons?.length === 1 &&
    m.reasons[0].type === 'skill_match'
  );

  if (skillOnlyMatches.length > matches.length * 0.3) {
    biases.push({
      type: 'Skill Overlap Bias',
      description: 'Too many matches based solely on skill overlap without considering actual needs',
      severity: 'medium' as const
    });
  }

  // Check for minimum threshold issues
  const lowQualityMatches = matches.filter(m => m.overallScore < 0.4);

  if (lowQualityMatches.length / matches.length > 0.3) {
    biases.push({
      type: 'Low Quality Threshold',
      description: `${(lowQualityMatches.length / matches.length * 100).toFixed(0)}% of matches are low quality (score < 0.4), threshold may be too low`,
      severity: 'medium' as const
    });
  }

  return biases;
}

function generateRecommendations(analysis: MatchAnalysis): string[] {
  const recommendations: string[] = [];

  if (analysis.forcedConnections / Math.max(analysis.totalMatches, 1) > 0.2) {
    recommendations.push(
      'CRITICAL: Over 20% of connections appear forced. Increase weight on complementary needs and reduce superficial matching criteria.'
    );
  }

  if (analysis.averageMatchQuality < 0.6) {
    recommendations.push(
      'LOW QUALITY: Average match quality is below 60%. Consider raising minimum thresholds and improving matching algorithms.'
    );
  }

  if (analysis.biases.some(b => b.severity === 'high')) {
    recommendations.push(
      'BIAS DETECTED: High-severity biases found. Rebalance weights to prioritize value/need alignment over status indicators.'
    );
  }

  recommendations.push(
    'ENHANCEMENT: Implement mutual benefit scoring that requires BOTH parties to have complementary needs/offerings.'
  );

  recommendations.push(
    'ENHANCEMENT: Add explicit "match reasoning" that explains WHY two users match based on their stated needs.'
  );

  recommendations.push(
    'ENHANCEMENT: Implement bidirectional matching - A->B should have similar score as B->A for pure matches.'
  );

  return recommendations;
}

function printMatchAnalysis(analysis: MatchAnalysis): void {
  console.log('='.repeat(60));
  console.log('MATCH QUALITY ANALYSIS');
  console.log('='.repeat(60));
  console.log('');

  console.log(`Total Matches Analyzed: ${analysis.totalMatches}`);
  console.log(`Pure Matches (need-based): ${analysis.pureMatches} (${(analysis.pureMatches / Math.max(analysis.totalMatches, 1) * 100).toFixed(1)}%)`);
  console.log(`Forced Connections: ${analysis.forcedConnections} (${(analysis.forcedConnections / Math.max(analysis.totalMatches, 1) * 100).toFixed(1)}%)`);
  console.log(`Average Match Quality: ${(analysis.averageMatchQuality * 100).toFixed(1)}%`);
  console.log('');

  console.log('BIASES DETECTED:');
  console.log('-'.repeat(60));
  if (analysis.biases.length === 0) {
    console.log('No significant biases detected.');
  } else {
    analysis.biases.forEach((bias, idx) => {
      console.log(`${idx + 1}. [${bias.severity.toUpperCase()}] ${bias.type}`);
      console.log(`   ${bias.description}`);
      console.log('');
    });
  }

  console.log('RECOMMENDATIONS:');
  console.log('-'.repeat(60));
  analysis.recommendations.forEach((rec, idx) => {
    console.log(`${idx + 1}. ${rec}`);
    console.log('');
  });
}

function saveMatchAnalysis(analysis: MatchAnalysis): void {
  const reportsDir = path.join(__dirname, '../test-reports');

  if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

  fs.writeFileSync(
    path.join(reportsDir, `match-analysis-${timestamp}.json`),
    JSON.stringify(analysis, null, 2)
  );

  console.log(`\nMatch analysis saved to: ${reportsDir}/match-analysis-${timestamp}.json`);
}

// Run the test
runTest().catch(error => {
  console.error('Test failed:', error);
  process.exit(1);
});
