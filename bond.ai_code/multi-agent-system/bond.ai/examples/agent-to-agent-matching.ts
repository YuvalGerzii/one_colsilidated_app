/**
 * Bond.AI - Agent-to-Agent Matching Example
 *
 * Demonstrates the advanced agent-based matching system where:
 * 1. Each user has a representative agent
 * 2. Agents negotiate with each other before making matches
 * 3. Matches are based on "what I need" and "what I give"
 * 4. Domain-specific matchers optimize for different partnership types
 */

import { BondAI_Enhanced } from '../src/BondAI_Enhanced';
import {
  UserProfile,
  NeedCategory,
  OfferingCategory,
  Priority,
  Urgency,
  CompanySize
} from '../src/agents/types';
import { Contact } from '../src/types';

async function main() {
  console.log('🤖 Bond.AI - Agent-to-Agent Matching System\n');
  console.log('═'.repeat(80));
  console.log('DEMONSTRATION: How agents negotiate matches on behalf of users');
  console.log('═'.repeat(80) + '\n');

  // Initialize Enhanced Bond.AI
  const bondAI = new BondAI_Enhanced('platform-admin');

  console.log('Scenario: AI Startup Ecosystem - Finding Perfect Matches\n');

  // ==========================================
  // User 1: Startup Founder seeking funding
  // ==========================================
  console.log('👤 Registering User 1: Startup Founder\n');

  const founderContact: Contact = {
    id: 'founder-sarah',
    name: 'Sarah Chen',
    email: 'sarah@aistarting.com',
    company: 'AI Starting Inc',
    title: 'CEO & Founder',
    industry: 'Artificial Intelligence',
    bio: 'Building next-generation AI platform for enterprise automation. MIT PhD, 10 years ML research.',
    skills: ['Machine Learning', 'Product Strategy', 'Team Building', 'Technical Architecture'],
    interests: ['AI research', 'entrepreneurship', 'scaling teams'],
    socialProfiles: {
      linkedin: 'linkedin.com/in/sarahchen',
      twitter: '@sarahchen_ai'
    }
  };

  const founderProfile: UserProfile = {
    needs: [
      {
        id: 'need-1',
        category: NeedCategory.FUNDING,
        description: 'Seed funding $2-3M for product development and initial go-to-market',
        priority: Priority.CRITICAL,
        urgency: Urgency.SHORT_TERM,
        flexibility: 0.3,
        quantifiable: {
          metric: 'capital',
          min: 2000000,
          max: 3000000,
          target: 2500000
        }
      },
      {
        id: 'need-2',
        category: NeedCategory.EXPERTISE,
        description: 'Enterprise sales expertise and go-to-market strategy',
        priority: Priority.HIGH,
        urgency: Urgency.MEDIUM_TERM,
        flexibility: 0.6
      },
      {
        id: 'need-3',
        category: NeedCategory.NETWORK,
        description: 'Introductions to Fortune 500 CTOs and AI decision-makers',
        priority: Priority.HIGH,
        urgency: Urgency.MEDIUM_TERM,
        flexibility: 0.5
      }
    ],
    offerings: [
      {
        id: 'offering-1',
        category: OfferingCategory.TECHNOLOGY,
        description: 'Cutting-edge AI platform with proven accuracy improvements',
        value: {
          type: 'strategic',
          estimated: 1000000
        },
        capacity: 0.9
      },
      {
        id: 'offering-2',
        category: OfferingCategory.KNOWLEDGE,
        description: 'Deep ML expertise and technical advisory',
        value: {
          type: 'expertise',
          estimated: 500000
        },
        capacity: 0.4
      },
      {
        id: 'offering-3',
        category: OfferingCategory.SKILLS,
        description: 'Equity stake in high-growth AI startup',
        value: {
          type: 'strategic',
          range: { min: 2000000, max: 10000000 }
        },
        capacity: 0.2
      }
    ],
    preferences: {
      preferredIndustries: ['Venture Capital', 'AI', 'Enterprise Software'],
      preferredCompanySizes: [CompanySize.STARTUP, CompanySize.MEDIUM],
      mustHaves: ['AI/ML expertise', 'enterprise connections'],
      dealBreakers: ['over 25% equity requirement', 'board control requirements']
    },
    constraints: {
      timeAvailability: 15, // hours per week for partnership activities
      budgetConstraints: { max: 0 }, // Seeking capital, not spending
      exclusivityRequirements: ['No competing portfolio companies in AI automation']
    },
    goals: [
      {
        id: 'goal-1',
        description: 'Raise seed round and achieve product-market fit',
        timeframe: Urgency.SHORT_TERM,
        successCriteria: [
          'Close $2.5M seed round',
          '10 enterprise pilot customers',
          'Product launch within 6 months'
        ],
        metrics: [
          { name: 'Funding', target: 2500000, current: 0, unit: 'USD' },
          { name: 'Customers', target: 10, current: 0, unit: 'count' }
        ]
      }
    ]
  };

  await bondAI.registerUserForAgentMatching(
    'founder-sarah',
    founderContact,
    founderProfile
  );

  // ==========================================
  // User 2: AI-Focused Investor
  // ==========================================
  console.log('\n👤 Registering User 2: AI Investor\n');

  const investorContact: Contact = {
    id: 'investor-michael',
    name: 'Michael Zhang',
    email: 'michael@aifund.vc',
    company: 'AI Ventures Fund',
    title: 'General Partner',
    industry: 'Venture Capital',
    bio: 'Thesis-driven AI investor. Former Google AI lead. $500M AUM focused on enterprise AI.',
    skills: ['Investment Strategy', 'AI Market Analysis', 'Due Diligence', 'Portfolio Support'],
    interests: ['enterprise AI', 'machine learning', 'startup mentoring'],
    socialProfiles: {
      linkedin: 'linkedin.com/in/michaelzhang'
    }
  };

  const investorProfile: UserProfile = {
    needs: [
      {
        id: 'need-1',
        category: NeedCategory.PARTNERSHIPS,
        description: 'High-quality AI deal flow with technical differentiation',
        priority: Priority.CRITICAL,
        urgency: Urgency.IMMEDIATE,
        flexibility: 0.4
      },
      {
        id: 'need-2',
        category: NeedCategory.TECHNOLOGY,
        description: 'Innovative AI solutions for portfolio company integration',
        priority: Priority.MEDIUM,
        urgency: Urgency.MEDIUM_TERM,
        flexibility: 0.7
      }
    ],
    offerings: [
      {
        id: 'offering-1',
        category: OfferingCategory.CAPITAL,
        description: 'Seed to Series A funding ($1-5M)',
        value: {
          type: 'monetary',
          range: { min: 1000000, max: 5000000 }
        },
        capacity: 0.8
      },
      {
        id: 'offering-2',
        category: OfferingCategory.CONNECTIONS,
        description: 'Network of Fortune 500 AI executives and decision-makers',
        value: {
          type: 'access',
          estimated: 2000000
        },
        capacity: 0.9
      },
      {
        id: 'offering-3',
        category: OfferingCategory.GUIDANCE,
        description: 'Go-to-market strategy and enterprise sales expertise',
        value: {
          type: 'expertise',
          estimated: 500000
        },
        capacity: 0.7
      },
      {
        id: 'offering-4',
        category: OfferingCategory.CONNECTIONS,
        description: 'Introductions to follow-on investors for Series A',
        value: {
          type: 'strategic',
          estimated: 1000000
        },
        capacity: 0.8
      }
    ],
    preferences: {
      preferredIndustries: ['Artificial Intelligence', 'Enterprise Software', 'ML Infrastructure'],
      mustHaves: ['Technical differentiation', 'Experienced technical founder', 'Large market opportunity'],
      dealBreakers: ['Consumer-only products', 'Unproven founding team']
    },
    constraints: {
      timeAvailability: 20,
      budgetConstraints: { min: 1000000, max: 5000000 },
      legalConstraints: ['Standard VC terms', 'Board seat for investments >$2M']
    },
    goals: [
      {
        id: 'goal-1',
        description: 'Deploy $20M in exceptional AI startups this year',
        timeframe: Urgency.MEDIUM_TERM,
        successCriteria: [
          'Invest in 4-6 AI companies',
          'Average ownership 15-20%',
          'Portfolio includes 1+ unicorn potential'
        ]
      }
    ]
  };

  await bondAI.registerUserForAgentMatching(
    'investor-michael',
    investorContact,
    investorProfile
  );

  // ==========================================
  // User 3: Enterprise CTO (Potential Client)
  // ==========================================
  console.log('\n👤 Registering User 3: Enterprise CTO\n');

  const ctoContact: Contact = {
    id: 'cto-david',
    name: 'David Park',
    email: 'david.park@megacorp.com',
    company: 'MegaCorp Industries',
    title: 'Chief Technology Officer',
    industry: 'Manufacturing',
    bio: 'Leading digital transformation. Managing 1000+ person tech org. Budget $200M annually.',
    skills: ['Enterprise Architecture', 'Digital Transformation', 'Vendor Management', 'Team Leadership'],
    interests: ['AI adoption', 'automation', 'innovation']
  };

  const ctoProfile: UserProfile = {
    needs: [
      {
        id: 'need-1',
        category: NeedCategory.TECHNOLOGY,
        description: 'AI automation solutions for manufacturing operations',
        priority: Priority.HIGH,
        urgency: Urgency.SHORT_TERM,
        flexibility: 0.5
      },
      {
        id: 'need-2',
        category: NeedCategory.EXPERTISE,
        description: 'AI implementation consulting and change management',
        priority: Priority.MEDIUM,
        urgency: Urgency.MEDIUM_TERM,
        flexibility: 0.6
      }
    ],
    offerings: [
      {
        id: 'offering-1',
        category: OfferingCategory.CLIENTS,
        description: 'Enterprise pilot program with $500K budget',
        value: {
          type: 'monetary',
          estimated: 500000
        },
        capacity: 0.7
      },
      {
        id: 'offering-2',
        category: OfferingCategory.COLLABORATION,
        description: 'Reference customer and case study opportunities',
        value: {
          type: 'strategic',
          estimated: 300000
        },
        capacity: 0.8
      },
      {
        id: 'offering-3',
        category: OfferingCategory.CONNECTIONS,
        description: 'Introductions to other Fortune 500 CTOs',
        value: {
          type: 'access',
          estimated: 400000
        },
        capacity: 0.5
      }
    ],
    preferences: {
      mustHaves: ['Proven technology', 'Strong security', 'Enterprise support'],
      dealBreakers: ['Unproven vendors', 'No enterprise SLA']
    },
    constraints: {
      timeAvailability: 5,
      budgetConstraints: { min: 100000, max: 2000000 },
      legalConstraints: ['Standard enterprise MSA', 'Data privacy compliance']
    },
    goals: [
      {
        id: 'goal-1',
        description: 'Implement AI automation across 3 major production facilities',
        timeframe: Urgency.MEDIUM_TERM,
        successCriteria: [
          '30% reduction in manual processing',
          'ROI within 18 months',
          'Zero security incidents'
        ]
      }
    ]
  };

  await bondAI.registerUserForAgentMatching(
    'cto-david',
    ctoContact,
    ctoProfile
  );

  // ==========================================
  // RUN AGENT-BASED MATCHING
  // ==========================================
  console.log('\n' + '█'.repeat(80));
  console.log('PHASE 1: AGENT-BASED MATCHING FOR FOUNDER');
  console.log('█'.repeat(80) + '\n');

  const result = await bondAI.runAgentBasedMatching('founder-sarah', 2);

  // ==========================================
  // DISPLAY RESULTS
  // ==========================================
  console.log('\n' + '═'.repeat(80));
  console.log('MATCHING RESULTS SUMMARY');
  console.log('═'.repeat(80) + '\n');

  console.log(`📊 Candidates Found: ${result.candidates.length}`);
  console.log(`🤝 Negotiations Conducted: ${result.negotiations.length}`);
  console.log(`✅ Agreements Reached: ${result.agreements.length}\n`);

  // Display all candidates
  if (result.candidates.length > 0) {
    console.log('All Match Candidates:');
    console.log('─'.repeat(80));
    result.candidates.forEach((candidate, i) => {
      console.log(`\n${i + 1}. ${candidate.agent2.userContact.name} (${candidate.agent2.userContact.title})`);
      console.log(`   Domain: ${candidate.domain}`);
      console.log(`   Overall Score: ${(candidate.overallScore * 100).toFixed(0)}%`);
      console.log(`   Recommended: ${candidate.recommended ? '✓ YES' : '✗ NO'}`);
      console.log(`   Key Factors:`);
      candidate.keyFactors.forEach(factor => {
        console.log(`     • ${factor}`);
      });
      if (candidate.risks.length > 0) {
        console.log(`   Risks:`);
        candidate.risks.forEach(risk => {
          console.log(`     ⚠ ${risk}`);
        });
      }
    });
    console.log('\n' + '─'.repeat(80) + '\n');
  }

  // Display negotiations
  if (result.negotiations.length > 0) {
    console.log('\nNegotiation Outcomes:');
    console.log('─'.repeat(80));
    result.negotiations.forEach((neg, i) => {
      console.log(`\n${i + 1}. ${neg.candidate.agent1.userContact.name} ⟷ ${neg.candidate.agent2.userContact.name}`);
      console.log(`   Result: ${neg.outcome.success ? '✅ SUCCESS' : '❌ NO AGREEMENT'}`);
      console.log(`   Duration: ${(neg.outcome.metrics.duration / 1000).toFixed(2)}s`);
      console.log(`   Messages: ${neg.outcome.metrics.messagesExchanged}`);
      console.log(`   Proposals: ${neg.outcome.metrics.proposalsConsidered}`);

      if (neg.outcome.success && neg.outcome.agreement) {
        const agreement = neg.outcome.agreement;
        console.log(`\n   📋 Agreement Terms:`);
        console.log(`   ${founderContact.name} Gets:`);
        agreement.finalTerms.whatAgent1Gets.forEach(item => {
          console.log(`     ✓ ${item}`);
        });
        console.log(`   ${founderContact.name} Gives:`);
        agreement.finalTerms.whatAgent1Gives.forEach(item => {
          console.log(`     → ${item}`);
        });
        console.log(`\n   Mutual Benefit Score: ${(agreement.mutualBenefit.overallScore * 100).toFixed(0)}%`);
        console.log(`   Balance Score: ${(agreement.mutualBenefit.balanceScore * 100).toFixed(0)}%`);
      } else if (!neg.outcome.success) {
        console.log(`\n   Reason: ${neg.outcome.reason}`);
        if (neg.outcome.improvementSuggestions) {
          console.log(`   Suggestions:`);
          neg.outcome.improvementSuggestions.forEach(suggestion => {
            console.log(`     • ${suggestion}`);
          });
        }
      }
    });
    console.log('\n' + '─'.repeat(80) + '\n');
  }

  // Display successful agreements
  if (result.agreements.length > 0) {
    console.log('\n✅ SUCCESSFUL AGREEMENTS:\n');
    console.log('═'.repeat(80));

    result.agreements.forEach((agreement, i) => {
      console.log(`\nAgreement ${i + 1}: ${agreement.agent1.userContact.name} ⟷ ${agreement.agent2.userContact.name}`);
      console.log('═'.repeat(80));

      console.log('\n📝 Final Terms:');
      console.log('\nValue Exchange:');
      console.log(`\n${agreement.agent1.userContact.name} receives:`);
      agreement.finalTerms.whatAgent1Gets.forEach(item => {
        console.log(`  ✓ ${item}`);
      });

      console.log(`\n${agreement.agent1.userContact.name} provides:`);
      agreement.finalTerms.whatAgent1Gives.forEach(item => {
        console.log(`  → ${item}`);
      });

      console.log(`\n${agreement.agent2.userContact.name} receives:`);
      agreement.finalTerms.whatAgent2Gets.forEach(item => {
        console.log(`  ✓ ${item}`);
      });

      console.log(`\n${agreement.agent2.userContact.name} provides:`);
      agreement.finalTerms.whatAgent2Gives.forEach(item => {
        console.log(`  → ${item}`);
      });

      if (agreement.finalTerms.conditions && agreement.finalTerms.conditions.length > 0) {
        console.log('\n📋 Conditions:');
        agreement.finalTerms.conditions.forEach(condition => {
          console.log(`  • ${condition}`);
        });
      }

      if (agreement.finalTerms.timeline) {
        console.log(`\n⏱️  Timeline: ${agreement.finalTerms.timeline}`);
      }

      console.log('\n📊 Agreement Metrics:');
      console.log(`  Compatibility Score: ${(agreement.compatibilityScore * 100).toFixed(0)}%`);
      console.log(`  Mutual Benefit: ${(agreement.mutualBenefit.overallScore * 100).toFixed(0)}%`);
      console.log(`  Balance Score: ${(agreement.mutualBenefit.balanceScore * 100).toFixed(0)}%`);

      console.log('\n🎯 Next Steps:');
      agreement.nextSteps.forEach((step, j) => {
        console.log(`  ${j + 1}. ${step}`);
      });

      console.log('\n' + '═'.repeat(80));
    });
  }

  // ==========================================
  // PLATFORM ANALYTICS
  // ==========================================
  console.log('\n\n' + '█'.repeat(80));
  console.log('PLATFORM ANALYTICS');
  console.log('█'.repeat(80) + '\n');

  const analytics = bondAI.getEnhancedAnalytics();

  console.log('📈 Agent-Based Matching Statistics:');
  console.log(`  Total Users: ${analytics.agentBased.totalUsers}`);
  console.log(`  Total Matches Found: ${analytics.agentBased.totalMatches}`);
  console.log(`  Negotiations Conducted: ${analytics.agentBased.totalNegotiations}`);
  console.log(`  Agreements Reached: ${analytics.agentBased.totalAgreements}`);
  console.log(`  Success Rate: ${(analytics.agentBased.successRate * 100).toFixed(0)}%`);
  console.log(`  Average Match Score: ${(analytics.agentBased.averageMatchScore * 100).toFixed(0)}%\n`);

  console.log('📊 Agreements by Domain:');
  Object.entries(analytics.agentBased.agreementsByDomain).forEach(([domain, count]) => {
    console.log(`  ${domain}: ${count}`);
  });

  // Top performers
  const topPerformers = bondAI.getTopPerformers(3);
  if (topPerformers.length > 0) {
    console.log('\n🏆 Top Performers:');
    topPerformers.forEach((performer, i) => {
      console.log(`  ${i + 1}. ${performer.userName}`);
      console.log(`     Agreements: ${performer.agreementCount}`);
      console.log(`     Avg Satisfaction: ${(performer.averageSatisfaction * 100).toFixed(0)}%`);
    });
  }

  console.log('\n' + '█'.repeat(80));
  console.log('✅ Agent-to-Agent Matching Demo Complete!');
  console.log('█'.repeat(80) + '\n');

  console.log('Key Takeaways:');
  console.log('  • Agents represent users and negotiate on their behalf');
  console.log('  • Matching is based on explicit needs and offerings from registration');
  console.log('  • Domain-specific matchers optimize for different partnership types');
  console.log('  • Agents conduct multi-round negotiations to find mutual value');
  console.log('  • Agreements are balanced and include clear terms and conditions');
  console.log('  • Platform tracks success metrics and continuously improves\n');
}

// Run the demo
main().catch(console.error);
