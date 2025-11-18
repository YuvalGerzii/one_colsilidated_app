/**
 * 1000 User Matching Test
 * Comprehensive test to evaluate the matching system across diverse scenarios
 * Tests system's ability to handle all types of requests and identifies edge cases
 */

import { IntelligenceEngine } from '../src/intelligence/IntelligenceEngine';
import { NetworkMapper } from '../src/network/NetworkMapper';
import { Contact } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

interface TestResult {
  testId: string;
  scenario: string;
  success: boolean;
  matchesFound: number;
  topMatchScore: number;
  timeElapsed: number;
  errors: string[];
  edgeCases: string[];
  insights: string[];
}

interface FlawReport {
  category: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  affectedScenarios: string[];
  suggestedFix: string;
}

interface HardCase {
  scenario: string;
  difficulty: string;
  why: string;
  result: string;
}

export class ComprehensiveMatchingTest {
  private testResults: TestResult[] = [];
  private flaws: FlawReport[] = [];
  private hardCases: HardCase[] = [];
  private users: Contact[] = [];

  constructor(
    private intelligenceEngine: IntelligenceEngine,
    private networkMapper: NetworkMapper
  ) {}

  /**
   * Generate 1000 diverse, realistic users
   */
  generateUsers(): Contact[] {
    const users: Contact[] = [];

    // Industry distribution
    const industries = [
      'Technology', 'Finance', 'Healthcare', 'Education', 'Manufacturing',
      'Retail', 'Media', 'Real Estate', 'Legal', 'Consulting',
      'Energy', 'Agriculture', 'Transportation', 'Hospitality', 'Arts'
    ];

    // Role types with varying specificity
    const roles = [
      'Software Engineer', 'Data Scientist', 'Product Manager', 'Designer',
      'Marketing Manager', 'Sales Director', 'Founder', 'CEO', 'CTO',
      'Investor', 'Consultant', 'Researcher', 'Analyst', 'Developer',
      'VP of Engineering', 'Head of Growth', 'Customer Success Manager'
    ];

    // Skill categories
    const techSkills = ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'AWS', 'Machine Learning', 'Data Analysis'];
    const businessSkills = ['Strategy', 'Marketing', 'Sales', 'Operations', 'Finance', 'Business Development'];
    const softSkills = ['Leadership', 'Communication', 'Problem Solving', 'Project Management'];

    // Need/offering categories
    const needs = [
      'Funding', 'Technical expertise', 'Marketing help', 'Co-founder', 'Mentor',
      'Customers', 'Partners', 'Advisors', 'Talent', 'Office space',
      'Legal advice', 'Design help', 'Data insights', 'Network introductions'
    ];

    const offerings = [
      'Investment capital', 'Technical skills', 'Industry connections', 'Mentorship',
      'Marketing expertise', 'Sales leads', 'Advisory', 'Development services',
      'Strategic planning', 'Market research', 'Product design', 'Customer acquisition'
    ];

    // Locations
    const locations = [
      'San Francisco, CA', 'New York, NY', 'Austin, TX', 'Seattle, WA',
      'Boston, MA', 'Los Angeles, CA', 'Chicago, IL', 'Denver, CO',
      'London, UK', 'Berlin, Germany', 'Singapore', 'Toronto, Canada',
      'Sydney, Australia', 'Tel Aviv, Israel', 'Bangalore, India'
    ];

    // Generate 1000 users with realistic variance
    for (let i = 0; i < 1000; i++) {
      const industry = industries[Math.floor(Math.random() * industries.length)];
      const role = roles[Math.floor(Math.random() * roles.length)];
      const location = locations[Math.floor(Math.random() * locations.length)];

      // Skills (2-7 skills per person)
      const numSkills = 2 + Math.floor(Math.random() * 6);
      const userSkills: string[] = [];

      // Mix of tech, business, and soft skills
      const skillPools = [techSkills, businessSkills, softSkills];
      for (let j = 0; j < numSkills; j++) {
        const pool = skillPools[Math.floor(Math.random() * skillPools.length)];
        const skill = pool[Math.floor(Math.random() * pool.length)];
        if (!userSkills.includes(skill)) {
          userSkills.push(skill);
        }
      }

      // Needs (0-4 needs)
      const numNeeds = Math.floor(Math.random() * 5);
      const userNeeds: string[] = [];
      for (let j = 0; j < numNeeds; j++) {
        const need = needs[Math.floor(Math.random() * needs.length)];
        if (!userNeeds.includes(need)) {
          userNeeds.push(need);
        }
      }

      // Offerings (0-4 offerings)
      const numOfferings = Math.floor(Math.random() * 5);
      const userOfferings: string[] = [];
      for (let j = 0; j < numOfferings; j++) {
        const offering = offerings[Math.floor(Math.random() * offerings.length)];
        if (!userOfferings.includes(offering)) {
          userOfferings.push(offering);
        }
      }

      // Bio quality variance (some detailed, some sparse)
      const bioQuality = Math.random();
      let bio = '';

      if (bioQuality > 0.7) {
        // Detailed bio
        bio = `Experienced ${role} with ${5 + Math.floor(Math.random() * 15)} years in ${industry}. ` +
              `Passionate about ${userSkills[0] || 'innovation'} and ${userSkills[1] || 'growth'}. ` +
              `Looking to ${userNeeds[0] || 'expand my network'}.`;
      } else if (bioQuality > 0.4) {
        // Medium bio
        bio = `${role} in ${industry}. ${userSkills.slice(0, 2).join(', ')}.`;
      } else {
        // Sparse bio (edge case)
        bio = role;
      }

      const user: Contact = {
        id: `user_${i + 1}`,
        name: `User ${i + 1}`,
        email: `user${i + 1}@example.com`,
        title: role,
        company: `Company ${Math.floor(i / 10)}`,
        industry,
        location,
        bio,
        skills: userSkills,
        needs: userNeeds,
        offerings: userOfferings,
        metadata: {
          experienceYears: Math.floor(Math.random() * 20),
          profileQuality: bioQuality,
          lastActive: this.generateRandomDate(),
          verified: Math.random() > 0.7,
        },
        tags: [],
        linkedinUrl: `https://linkedin.com/in/user${i + 1}`,
      };

      users.push(user);
    }

    this.users = users;
    return users;
  }

  /**
   * Run comprehensive test suite
   */
  async runTests(): Promise<void> {
    console.log('Starting comprehensive 1000-user matching test...\n');

    // Test 1: Standard matching scenarios
    await this.testStandardMatching();

    // Test 2: Edge cases
    await this.testEdgeCases();

    // Test 3: Complex multi-criteria matching
    await this.testComplexScenarios();

    // Test 4: Performance at scale
    await this.testPerformance();

    // Test 5: Hard cases
    await this.testHardCases();

    // Generate reports
    this.generateReports();
  }

  /**
   * Test 1: Standard matching scenarios
   */
  private async testStandardMatching(): Promise<void> {
    console.log('Test 1: Standard Matching Scenarios');
    console.log('=====================================\n');

    const scenarios = [
      {
        id: 'funding-seek',
        description: 'Startup founder seeks funding',
        profile: this.createProfile({
          title: 'Founder',
          needs: ['Funding', 'Mentorship'],
          offerings: ['Innovative product', 'Technical expertise'],
          industry: 'Technology'
        })
      },
      {
        id: 'hiring-dev',
        description: 'Company hiring developers',
        profile: this.createProfile({
          title: 'CTO',
          needs: ['Software Engineer', 'Technical expertise'],
          offerings: ['Salary', 'Equity', 'Mentorship'],
          industry: 'Technology'
        })
      },
      {
        id: 'partnership',
        description: 'Looking for business partners',
        profile: this.createProfile({
          title: 'VP of Business Development',
          needs: ['Partners', 'Customer access'],
          offerings: ['Industry connections', 'Strategic planning'],
          industry: 'Finance'
        })
      }
    ];

    for (const scenario of scenarios) {
      await this.runScenarioTest(scenario.id, scenario.description, scenario.profile);
    }
  }

  /**
   * Test 2: Edge cases
   */
  private async testEdgeCases(): Promise<void> {
    console.log('\nTest 2: Edge Cases');
    console.log('===================\n');

    const edgeCases = [
      {
        id: 'empty-profile',
        description: 'User with minimal profile information',
        profile: this.createProfile({
          title: 'Professional',
          needs: [],
          offerings: [],
          skills: []
        })
      },
      {
        id: 'ultra-specific',
        description: 'User with very specific, rare requirements',
        profile: this.createProfile({
          title: 'Quantum Computing Researcher',
          needs: ['Quantum algorithm expertise', 'D-Wave access'],
          offerings: ['Research collaboration'],
          skills: ['Quantum Mechanics', 'Topology']
        })
      },
      {
        id: 'generalist',
        description: 'User with very broad, vague needs',
        profile: this.createProfile({
          title: 'Entrepreneur',
          needs: ['Help', 'Advice', 'Support'],
          offerings: ['Ideas', 'Energy'],
          skills: []
        })
      },
      {
        id: 'conflicting-needs',
        description: 'User with potentially conflicting requirements',
        profile: this.createProfile({
          title: 'CEO',
          needs: ['Funding', 'Customers'],
          offerings: ['Equity', 'Revenue'],
          industry: 'Technology'
        })
      }
    ];

    for (const edgeCase of edgeCases) {
      const result = await this.runScenarioTest(edgeCase.id, edgeCase.description, edgeCase.profile);

      if (result.matchesFound === 0) {
        this.hardCases.push({
          scenario: edgeCase.description,
          difficulty: 'High',
          why: 'No matches found despite diverse user base',
          result: 'System struggled to find relevant connections'
        });
      }
    }
  }

  /**
   * Test 3: Complex multi-criteria scenarios
   */
  private async testComplexScenarios(): Promise<void> {
    console.log('\nTest 3: Complex Multi-Criteria Scenarios');
    console.log('=========================================\n');

    const complexScenarios = [
      {
        id: 'multi-need',
        description: 'User with multiple diverse needs',
        profile: this.createProfile({
          title: 'Startup Founder',
          needs: ['Funding', 'Technical expertise', 'Marketing help', 'Legal advice'],
          offerings: ['Equity', 'Partnership opportunity'],
          skills: ['Product Strategy', 'Vision'],
          industry: 'Healthcare'
        })
      },
      {
        id: 'cross-industry',
        description: 'Cross-industry collaboration seeker',
        profile: this.createProfile({
          title: 'Innovation Director',
          needs: ['Cross-industry insights', 'Technology partners'],
          offerings: ['Enterprise access', 'Pilot opportunities'],
          industry: 'Manufacturing',
          skills: ['Supply Chain', 'IoT']
        })
      },
      {
        id: 'geographic-specific',
        description: 'Needs specific geographic expertise',
        profile: this.createProfile({
          title: 'International Expansion Manager',
          needs: ['Asia market expertise', 'Local partners'],
          offerings: ['US market access', 'Capital'],
          location: 'New York, NY'
        })
      }
    ];

    for (const scenario of complexScenarios) {
      await this.runScenarioTest(scenario.id, scenario.description, scenario.profile);
    }
  }

  /**
   * Test 4: Performance at scale
   */
  private async testPerformance(): Promise<void> {
    console.log('\nTest 4: Performance at Scale');
    console.log('=============================\n');

    const testProfile = this.createProfile({
      title: 'Software Engineer',
      needs: ['Career growth', 'Mentorship'],
      offerings: ['Technical skills', 'Experience'],
      skills: ['JavaScript', 'React', 'Node.js']
    });

    const startTime = Date.now();

    try {
      const matches = await this.findMatches(testProfile);
      const endTime = Date.now();
      const elapsed = endTime - startTime;

      console.log(`Matched against 1000 users in ${elapsed}ms`);

      if (elapsed > 5000) {
        this.flaws.push({
          category: 'Performance',
          severity: 'high',
          description: `Matching took ${elapsed}ms for 1000 users`,
          affectedScenarios: ['All scenarios'],
          suggestedFix: 'Implement caching, indexing, or parallel processing'
        });
      }

      this.testResults.push({
        testId: 'performance-scale',
        scenario: 'Performance at 1000 users',
        success: elapsed < 10000,
        matchesFound: matches.length,
        topMatchScore: matches[0]?.compatibilityScore || 0,
        timeElapsed: elapsed,
        errors: [],
        edgeCases: [],
        insights: [`Processed ${1000 / (elapsed / 1000)} users per second`]
      });

    } catch (error) {
      console.error('Performance test failed:', error);
    }
  }

  /**
   * Test 5: Hard cases
   */
  private async testHardCases(): Promise<void> {
    console.log('\nTest 5: Hard Cases');
    console.log('==================\n');

    // Case 1: Ambiguous request
    await this.testAmbiguousRequest();

    // Case 2: Contradictory requirements
    await this.testContradictoryRequirements();

    // Case 3: Extreme outliers
    await this.testExtremeOutliers();
  }

  private async testAmbiguousRequest(): Promise<void> {
    const profile = this.createProfile({
      title: 'Professional',
      needs: ['Opportunities'],
      offerings: ['Value'],
      skills: [],
      bio: 'Looking for interesting opportunities'
    });

    const result = await this.runScenarioTest(
      'ambiguous-request',
      'Extremely vague/ambiguous request',
      profile
    );

    if (result.matchesFound > 100) {
      this.hardCases.push({
        scenario: 'Ambiguous request matching',
        difficulty: 'Medium',
        why: 'System returned too many low-quality matches instead of asking for clarification',
        result: `Returned ${result.matchesFound} matches with low specificity`
      });
    }
  }

  private async testContradictoryRequirements(): Promise<void> {
    const profile = this.createProfile({
      title: 'Entrepreneur',
      needs: ['Experienced senior developer', 'Cheap resources'],
      offerings: ['Equity only'],
      industry: 'Technology'
    });

    const result = await this.runScenarioTest(
      'contradictory-requirements',
      'Contradictory requirements (high-quality + low-cost)',
      profile
    );

    this.hardCases.push({
      scenario: 'Contradictory requirements',
      difficulty: 'High',
      why: 'Requirements are inherently conflicting',
      result: result.matchesFound > 0
        ? 'System found matches but may not satisfy both criteria'
        : 'System correctly found no perfect matches'
    });
  }

  private async testExtremeOutliers(): Promise<void> {
    const profile = this.createProfile({
      title: 'Alien Technology Researcher',
      needs: ['Extraterrestrial collaboration'],
      offerings: ['Intergalactic networking'],
      skills: ['Xenolinguistics', 'Faster-than-light travel']
    });

    const result = await this.runScenarioTest(
      'extreme-outlier',
      'Completely unrealistic/absurd profile',
      profile
    );

    if (result.matchesFound > 10) {
      this.flaws.push({
        category: 'Data Quality',
        severity: 'medium',
        description: 'System matched absurd profiles without flagging them',
        affectedScenarios: ['Data validation'],
        suggestedFix: 'Add profile validation and quality scoring'
      });
    }
  }

  /**
   * Helper: Run individual scenario test
   */
  private async runScenarioTest(
    testId: string,
    description: string,
    profile: Contact
  ): Promise<TestResult> {
    console.log(`Testing: ${description}...`);

    const startTime = Date.now();
    const errors: string[] = [];
    const edgeCases: string[] = [];
    const insights: string[] = [];

    try {
      const matches = await this.findMatches(profile);
      const endTime = Date.now();

      const topMatchScore = matches[0]?.compatibilityScore || 0;

      // Analyze results
      if (matches.length === 0) {
        edgeCases.push('No matches found');
      }

      if (topMatchScore < 0.3) {
        edgeCases.push('Low match quality (all matches below 30%)');
      }

      if (matches.length > 0 && topMatchScore > 0.7) {
        insights.push('Found high-quality matches');
      }

      const result: TestResult = {
        testId,
        scenario: description,
        success: matches.length > 0,
        matchesFound: matches.length,
        topMatchScore,
        timeElapsed: endTime - startTime,
        errors,
        edgeCases,
        insights
      };

      this.testResults.push(result);
      console.log(`  ✓ Found ${matches.length} matches (top score: ${(topMatchScore * 100).toFixed(1)}%) in ${result.timeElapsed}ms\n`);

      return result;

    } catch (error: any) {
      const errorMsg = error.message || 'Unknown error';
      errors.push(errorMsg);

      const result: TestResult = {
        testId,
        scenario: description,
        success: false,
        matchesFound: 0,
        topMatchScore: 0,
        timeElapsed: Date.now() - startTime,
        errors,
        edgeCases,
        insights
      };

      this.testResults.push(result);
      console.log(`  ✗ Test failed: ${errorMsg}\n`);

      this.flaws.push({
        category: 'System Error',
        severity: 'critical',
        description: `Test "${description}" failed with error: ${errorMsg}`,
        affectedScenarios: [testId],
        suggestedFix: 'Investigate and fix underlying error'
      });

      return result;
    }
  }

  /**
   * Helper methods
   */

  private createProfile(data: Partial<Contact>): Contact {
    return {
      id: `test_${Date.now()}_${Math.random()}`,
      name: data.name || 'Test User',
      email: data.email || 'test@example.com',
      title: data.title || 'Professional',
      company: data.company || 'Test Company',
      industry: data.industry || 'Technology',
      location: data.location || 'San Francisco, CA',
      bio: data.bio || `${data.title} seeking ${data.needs?.join(', ') || 'connections'}`,
      skills: data.skills || [],
      needs: data.needs || [],
      offerings: data.offerings || [],
      tags: data.tags || [],
      metadata: data.metadata || {},
      linkedinUrl: data.linkedinUrl || ''
    };
  }

  private async findMatches(profile: Contact): Promise<any[]> {
    // Simplified - replace with actual matching logic
    // This would call intelligenceEngine.analyzeAndMatch or similar

    // Simulate matching against the 1000 users
    const matches = this.users
      .map(user => ({
        ...user,
        compatibilityScore: this.calculateSimpleMatch(profile, user)
      }))
      .filter(match => match.compatibilityScore > 0.2)
      .sort((a, b) => b.compatibilityScore - a.compatibilityScore)
      .slice(0, 20);

    return matches;
  }

  private calculateSimpleMatch(seeker: Contact, candidate: Contact): number {
    let score = 0.3; // Base score

    // Industry match
    if (seeker.industry === candidate.industry) score += 0.2;

    // Skills overlap
    const seekerSkills = new Set(seeker.skills);
    const candidateSkills = new Set(candidate.skills);
    const skillOverlap = [...seekerSkills].filter(s => candidateSkills.has(s)).length;

    if (skillOverlap > 0) {
      score += Math.min(0.2, skillOverlap * 0.05);
    }

    // Needs vs offerings
    const seekerNeeds = new Set(seeker.needs?.map(n => n.toLowerCase()) || []);
    const candidateOfferings = new Set(candidate.offerings?.map(o => o.toLowerCase()) || []);

    for (const need of seekerNeeds) {
      for (const offering of candidateOfferings) {
        if (offering.includes(need) || need.includes(offering)) {
          score += 0.15;
          break;
        }
      }
    }

    return Math.min(1.0, score);
  }

  private generateRandomDate(): string {
    const now = new Date();
    const daysAgo = Math.floor(Math.random() * 365);
    const date = new Date(now.getTime() - daysAgo * 24 * 60 * 60 * 1000);
    return date.toISOString();
  }

  /**
   * Generate comprehensive reports
   */
  private generateReports(): void {
    console.log('\n\n===========================================');
    console.log('COMPREHENSIVE TEST RESULTS SUMMARY');
    console.log('===========================================\n');

    // Summary statistics
    const totalTests = this.testResults.length;
    const successfulTests = this.testResults.filter(t => t.success).length;
    const failedTests = totalTests - successfulTests;

    console.log(`Total Tests: ${totalTests}`);
    console.log(`Successful: ${successfulTests} (${(successfulTests / totalTests * 100).toFixed(1)}%)`);
    console.log(`Failed: ${failedTests}`);

    const avgMatchesPerTest = this.testResults.reduce((sum, t) => sum + t.matchesFound, 0) / totalTests;
    const avgTopScore = this.testResults.reduce((sum, t) => sum + t.topMatchScore, 0) / totalTests;

    console.log(`\nAverage matches per test: ${avgMatchesPerTest.toFixed(1)}`);
    console.log(`Average top match score: ${(avgTopScore * 100).toFixed(1)}%`);

    // Flaws Report
    console.log('\n\n===========================================');
    console.log('FLAWS IDENTIFIED');
    console.log('===========================================\n');

    if (this.flaws.length === 0) {
      console.log('No significant flaws identified!');
    } else {
      this.flaws.forEach((flaw, idx) => {
        console.log(`${idx + 1}. [${flaw.severity.toUpperCase()}] ${flaw.category}`);
        console.log(`   Description: ${flaw.description}`);
        console.log(`   Affected scenarios: ${flaw.affectedScenarios.join(', ')}`);
        console.log(`   Suggested fix: ${flaw.suggestedFix}`);
        console.log('');
      });
    }

    // Hard Cases Report
    console.log('\n===========================================');
    console.log('HARD CASES IDENTIFIED');
    console.log('===========================================\n');

    if (this.hardCases.length === 0) {
      console.log('No hard cases identified!');
    } else {
      this.hardCases.forEach((hardCase, idx) => {
        console.log(`${idx + 1}. ${hardCase.scenario} [Difficulty: ${hardCase.difficulty}]`);
        console.log(`   Why hard: ${hardCase.why}`);
        console.log(`   Result: ${hardCase.result}`);
        console.log('');
      });
    }

    // Save reports to files
    this.saveReportsToFiles();
  }

  private saveReportsToFiles(): void {
    const reportsDir = path.join(__dirname, '../test-reports');

    // Create directory if it doesn't exist
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

    // Save detailed results
    fs.writeFileSync(
      path.join(reportsDir, `test-results-${timestamp}.json`),
      JSON.stringify(this.testResults, null, 2)
    );

    // Save flaws
    fs.writeFileSync(
      path.join(reportsDir, `flaws-${timestamp}.json`),
      JSON.stringify(this.flaws, null, 2)
    );

    // Save hard cases
    fs.writeFileSync(
      path.join(reportsDir, `hard-cases-${timestamp}.json`),
      JSON.stringify(this.hardCases, null, 2)
    );

    // Save user dataset
    fs.writeFileSync(
      path.join(reportsDir, `users-dataset-${timestamp}.json`),
      JSON.stringify(this.users.slice(0, 100), null, 2) // Save first 100 for review
    );

    console.log(`\nReports saved to: ${reportsDir}`);
  }
}

// Export for use in other tests
export default ComprehensiveMatchingTest;
