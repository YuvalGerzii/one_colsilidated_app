/**
 * Bond.AI - Advanced Matching Example
 *
 * This example demonstrates advanced matching capabilities:
 * - Large network with multiple degrees of separation
 * - Different match types
 * - Custom configuration
 * - Advanced filtering and prioritization
 */

import { BondAI, Contact, Connection, RelationshipType, MatchType, Priority } from '../src/BondAI';

async function main() {
  console.log('🔥 Bond.AI - Advanced Matching Example\n');

  // Initialize with custom configuration
  console.log('Initializing Bond.AI with advanced configuration...');
  const bondAI = new BondAI('founder-001', {
    maxDegreeOfSeparation: 3,
    minCompatibilityScore: 0.5,
    minRelationshipStrength: 0.2,
    enabledMatchTypes: [
      'complementary_needs' as MatchType,
      'business_opportunity' as MatchType,
      'skill_match' as MatchType,
      'industry_synergy' as MatchType
    ],
    priorityWeights: {
      valuePotential: 0.4,      // Prioritize high-value opportunities
      successProbability: 0.3,  // Consider likelihood of success
      trustLevel: 0.2,          // Factor in trust
      timing: 0.1               // Less weight on timing
    },
    intelligenceConfig: {
      enableNeedsInference: true,
      enablePersonalityAnalysis: true,
      enableBehavioralPrediction: true
    }
  });
  console.log('✓ Configured\n');

  // Create a realistic network scenario: Startup founder looking for investors
  console.log('Building network scenario: AI Startup Founder...\n');

  // The founder (user)
  const contacts: Contact[] = [
    // First Degree - Direct connections
    {
      id: 'mentor-1',
      name: 'Dr. Emily Chen',
      title: 'Professor & AI Researcher',
      company: 'Stanford University',
      industry: 'Education',
      bio: 'Leading AI researcher with extensive industry connections. Mentor to many successful founders.',
      skills: ['Machine Learning', 'Academic Research', 'Mentorship'],
      interests: ['AI ethics', 'education', 'startups'],
      offerings: ['mentorship', 'academic connections', 'research collaboration'],
      needs: ['industry partnerships', 'research funding']
    },
    {
      id: 'cofounder-1',
      name: 'Alex Rivera',
      title: 'CTO',
      company: 'Our AI Startup',
      industry: 'Technology',
      bio: 'Technical co-founder with expertise in distributed systems and ML infrastructure.',
      skills: ['System Architecture', 'ML Engineering', 'Team Leadership'],
      interests: ['scalable systems', 'AI infrastructure', 'open source'],
      offerings: ['technical expertise', 'engineering leadership'],
      needs: ['product strategy', 'go-to-market expertise']
    },
    {
      id: 'friend-1',
      name: 'Jamie Park',
      title: 'Product Manager',
      company: 'Big Tech Corp',
      industry: 'Technology',
      bio: 'Product leader at major tech company. Well connected in the tech ecosystem.',
      skills: ['Product Management', 'User Experience', 'Strategy'],
      interests: ['product design', 'user research', 'technology trends'],
      offerings: ['product advice', 'tech industry connections'],
      needs: ['startup opportunities', 'equity upside']
    },

    // Second Degree - Connected through first degree
    {
      id: 'investor-1',
      name: 'Michael Chang',
      title: 'General Partner',
      company: 'AI Ventures Fund',
      industry: 'Venture Capital',
      bio: 'Thesis-driven investor focused exclusively on AI/ML companies. $500M AUM.',
      skills: ['Investment Strategy', 'AI Market Analysis', 'Board Service'],
      interests: ['artificial intelligence', 'deep tech', 'enterprise software'],
      needs: ['high-quality AI deal flow', 'technical due diligence'],
      offerings: ['seed to Series A funding', 'go-to-market support', 'portfolio network']
    },
    {
      id: 'investor-2',
      name: 'Sarah Williams',
      title: 'Managing Director',
      company: 'Growth Equity Partners',
      industry: 'Private Equity',
      bio: 'Growth stage investor with focus on B2B SaaS and AI. Former operator.',
      skills: ['Growth Strategy', 'Operational Excellence', 'M&A'],
      interests: ['SaaS', 'AI applications', 'business models'],
      needs: ['series B+ opportunities', 'proven revenue models'],
      offerings: ['growth capital', 'operational expertise', 'acquisition opportunities']
    },
    {
      id: 'executive-1',
      name: 'David Kim',
      title: 'VP of Engineering',
      company: 'Fortune 500 Tech',
      industry: 'Technology',
      bio: 'Engineering leader managing 500+ person org. Evaluating AI solutions.',
      skills: ['Engineering Leadership', 'Enterprise Architecture', 'Vendor Management'],
      interests: ['enterprise AI', 'team building', 'innovation'],
      needs: ['AI automation tools', 'ML infrastructure solutions'],
      offerings: ['enterprise contracts', 'pilot programs', 'case studies']
    },
    {
      id: 'advisor-1',
      name: 'Lisa Thompson',
      title: 'Former CEO',
      company: 'Successful Exit Inc (Acquired)',
      industry: 'Technology',
      bio: 'Serial entrepreneur. Built and sold AI company for $200M. Now advising.',
      skills: ['Go-to-Market', 'Fundraising', 'M&A'],
      interests: ['entrepreneurship', 'AI', 'advising'],
      needs: ['interesting advisory opportunities', 'equity upside'],
      offerings: ['strategic advice', 'investor introductions', 'M&A expertise']
    },

    // Third Degree - Extended network
    {
      id: 'investor-3',
      name: 'Robert Zhang',
      title: 'Partner',
      company: 'Top Tier VC',
      industry: 'Venture Capital',
      bio: 'Premier early-stage investor. Portfolio includes multiple unicorns.',
      skills: ['Pattern Recognition', 'Network Building', 'Strategic Guidance'],
      interests: ['breakthrough innovation', 'AI', 'platforms'],
      needs: ['exceptional founding teams', 'transformative opportunities'],
      offerings: ['prestigious capital', 'deep network', 'brand value']
    },
    {
      id: 'ceo-1',
      name: 'Amanda Foster',
      title: 'CEO',
      company: 'Enterprise AI Leader',
      industry: 'Technology',
      bio: 'Running fast-growing enterprise AI company. $100M ARR.',
      skills: ['Enterprise Sales', 'Strategic Partnerships', 'Scaling'],
      interests: ['enterprise software', 'partnerships', 'industry transformation'],
      needs: ['complementary technology', 'distribution partners'],
      offerings: ['partnership opportunities', 'customer introductions', 'acquisition interest']
    }
  ];

  // Add all contacts
  contacts.forEach(contact => bondAI.addContact(contact));
  console.log(`✓ Added ${contacts.length} contacts\n`);

  // Create realistic connection graph
  const connections: Connection[] = [
    // First degree
    {
      id: 'c1',
      fromContactId: 'founder-001',
      toContactId: 'mentor-1',
      relationshipType: RelationshipType.MENTOR,
      strength: 0.9,
      trustLevel: 0.95,
      interactionFrequency: 4,
      lastInteraction: new Date('2025-11-12')
    },
    {
      id: 'c2',
      fromContactId: 'founder-001',
      toContactId: 'cofounder-1',
      relationshipType: RelationshipType.PARTNER,
      strength: 1.0,
      trustLevel: 1.0,
      interactionFrequency: 20,
      lastInteraction: new Date('2025-11-15')
    },
    {
      id: 'c3',
      fromContactId: 'founder-001',
      toContactId: 'friend-1',
      relationshipType: RelationshipType.FRIEND,
      strength: 0.8,
      trustLevel: 0.9,
      interactionFrequency: 6,
      lastInteraction: new Date('2025-11-10')
    },

    // Second degree - through mentor
    {
      id: 'c4',
      fromContactId: 'mentor-1',
      toContactId: 'investor-1',
      relationshipType: RelationshipType.COLLEAGUE,
      strength: 0.7,
      trustLevel: 0.85,
      interactionFrequency: 3,
      lastInteraction: new Date('2025-10-20')
    },
    {
      id: 'c5',
      fromContactId: 'mentor-1',
      toContactId: 'advisor-1',
      relationshipType: RelationshipType.COLLEAGUE,
      strength: 0.8,
      trustLevel: 0.8,
      interactionFrequency: 2,
      lastInteraction: new Date('2025-09-15')
    },

    // Second degree - through friend
    {
      id: 'c6',
      fromContactId: 'friend-1',
      toContactId: 'executive-1',
      relationshipType: RelationshipType.COLLEAGUE,
      strength: 0.6,
      trustLevel: 0.7,
      interactionFrequency: 4,
      lastInteraction: new Date('2025-11-01')
    },
    {
      id: 'c7',
      fromContactId: 'friend-1',
      toContactId: 'investor-2',
      relationshipType: RelationshipType.ACQUAINTANCE,
      strength: 0.5,
      trustLevel: 0.6,
      interactionFrequency: 1,
      lastInteraction: new Date('2025-08-10')
    },

    // Third degree - through investor-1
    {
      id: 'c8',
      fromContactId: 'investor-1',
      toContactId: 'investor-3',
      relationshipType: RelationshipType.COLLEAGUE,
      strength: 0.7,
      trustLevel: 0.75,
      interactionFrequency: 2,
      lastInteraction: new Date('2025-10-01')
    },

    // Third degree - through advisor-1
    {
      id: 'c9',
      fromContactId: 'advisor-1',
      toContactId: 'ceo-1',
      relationshipType: RelationshipType.COLLEAGUE,
      strength: 0.8,
      trustLevel: 0.85,
      interactionFrequency: 3,
      lastInteraction: new Date('2025-10-15')
    }
  ];

  connections.forEach(conn => bondAI.addConnection(conn));
  console.log(`✓ Created ${connections.length} connections\n`);

  // Build network
  bondAI.buildNetwork();
  const stats = bondAI.getNetworkStats();
  console.log('Network Statistics:');
  console.log(`  Total Contacts: ${stats.totalContacts}`);
  console.log(`  Total Connections: ${stats.totalConnections}`);
  console.log('  Contacts by Degree:', stats.contactsByDegree);
  console.log('');

  // Discover matches
  console.log('Discovering matches...');
  const allMatches = await bondAI.discoverMatches();
  console.log(`✓ Found ${allMatches.length} total matches\n`);

  // Analyze matches by priority
  console.log('📊 Matches by Priority:');
  console.log('─'.repeat(80));
  const priorities = [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW];

  for (const priority of priorities) {
    const matches = bondAI.getMatchesByPriority(priority);
    console.log(`\n${priority.toUpperCase()}: ${matches.length} matches`);

    matches.slice(0, 3).forEach(match => {
      console.log(`  • ${match.targetContact.name} (${match.targetContact.title})`);
      console.log(`    Score: ${(match.overallScore * 100).toFixed(0)}% | ` +
                  `Type: ${match.matchType.replace(/_/g, ' ')} | ` +
                  `Path: ${match.shortestPath.contacts.length - 1} hops`);
    });
  }
  console.log('\n' + '─'.repeat(80) + '\n');

  // Deep dive into top 3 opportunities
  console.log('🎯 Top 3 Critical Opportunities:');
  console.log('═'.repeat(80));

  const criticalMatches = bondAI.getMatchesByPriority(Priority.CRITICAL).slice(0, 3);

  criticalMatches.forEach((match, index) => {
    console.log(`\n${index + 1}. OPPORTUNITY: ${match.targetContact.name}`);
    console.log('─'.repeat(80));
    console.log(`   Role: ${match.targetContact.title} at ${match.targetContact.company}`);
    console.log(`   Match Type: ${match.matchType.replace(/_/g, ' ').toUpperCase()}`);
    console.log('');
    console.log('   SCORES:');
    console.log(`   ├─ Overall: ${(match.overallScore * 100).toFixed(0)}%`);
    console.log(`   ├─ Compatibility: ${(match.compatibilityScore * 100).toFixed(0)}%`);
    console.log(`   ├─ Value Potential: ${(match.valuePotential * 100).toFixed(0)}%`);
    console.log(`   ├─ Success Probability: ${(match.successProbability * 100).toFixed(0)}%`);
    console.log(`   └─ Trust Level: ${(match.shortestPath.trustScore * 100).toFixed(0)}%`);
    console.log('');
    console.log('   CONNECTION PATH:');
    const pathNames = match.shortestPath.contacts.map(c => c.name);
    console.log(`   ${pathNames.join(' → ')}`);
    console.log('');
    console.log('   KEY REASONS:');
    match.reasons.forEach(reason => {
      console.log(`   • ${reason.description} (${(reason.score * 100).toFixed(0)}%)`);
      if (reason.evidence.length > 0) {
        reason.evidence.slice(0, 2).forEach(evidence => {
          console.log(`     - ${evidence}`);
        });
      }
    });
    console.log('');
  });

  console.log('═'.repeat(80) + '\n');

  // Create and preview introduction for top match
  if (criticalMatches.length > 0) {
    const topMatch = criticalMatches[0];
    console.log('📧 Creating Introduction for Top Match...\n');

    const introduction = await bondAI.createIntroduction(topMatch.id);

    console.log('INTRODUCTION PREVIEW:');
    console.log('═'.repeat(80));
    console.log(introduction.message);
    console.log('═'.repeat(80));
    console.log('\nCONVERSATION STARTERS:');
    introduction.conversationStarters.forEach((starter, i) => {
      console.log(`${i + 1}. "${starter}"`);
    });
    console.log('\nCONTEXT:');
    console.log(introduction.context);
    console.log('═'.repeat(80) + '\n');

    // Simulate the introduction flow
    console.log('Simulating introduction flow...');
    await bondAI.sendIntroduction(introduction.id);
    console.log('✓ Introduction sent');

    setTimeout(() => {
      bondAI.acceptIntroduction(introduction.id);
      console.log('✓ Introduction accepted');

      bondAI.recordInteraction(
        topMatch.sourceContact.id,
        topMatch.targetContact.id,
        'Initial meeting - discussed funding requirements and vision'
      );
      console.log('✓ First interaction recorded');

      bondAI.recordInteraction(
        topMatch.sourceContact.id,
        topMatch.targetContact.id,
        'Follow-up call - reviewed pitch deck and financials'
      );
      console.log('✓ Second interaction recorded');

      bondAI.recordBusinessValue(
        topMatch.sourceContact.id,
        topMatch.targetContact.id,
        2000000,
        'Series A term sheet signed - $2M at $10M valuation'
      );
      console.log('✓ Business value recorded: $2,000,000\n');

      // Final analytics
      displayFinalAnalytics(bondAI);
    }, 100);
  }
}

function displayFinalAnalytics(bondAI: BondAI) {
  console.log('📈 FINAL ANALYTICS REPORT:');
  console.log('═'.repeat(80));

  const dashboard = bondAI.getDashboard();
  const roi = bondAI.getROI();
  const analytics = bondAI.getAnalytics();

  console.log('\n💼 NETWORK OVERVIEW:');
  console.log(`   Network Size: ${dashboard.networkSize} contacts`);
  console.log(`   Total Reach: ${dashboard.totalReach} people`);
  console.log(`   Network Density: ${analytics.network.averageConnectionsPerContact.toFixed(2)} connections/contact`);

  console.log('\n🎯 OPPORTUNITY PIPELINE:');
  console.log(`   Active Matches: ${dashboard.activeMatches}`);
  console.log(`   Critical Opportunities: ${dashboard.criticalOpportunities}`);
  console.log(`   High Priority: ${analytics.matches.byPriority.high}`);
  console.log(`   Medium Priority: ${analytics.matches.byPriority.medium}`);
  console.log(`   Average Compatibility: ${(analytics.matches.averageCompatibility * 100).toFixed(0)}%`);

  console.log('\n🤝 RELATIONSHIP METRICS:');
  console.log(`   Total Introductions: ${roi.totalIntroductions}`);
  console.log(`   Successful Connections: ${roi.successfulConnections}`);
  console.log(`   Success Rate: ${(analytics.introductions.successRate * 100).toFixed(0)}%`);
  console.log(`   Active Relationships: ${dashboard.activeRelationships}`);
  console.log(`   Avg Response Time: ${analytics.introductions.averageResponseTime.toFixed(1)} days`);

  console.log('\n💰 BUSINESS VALUE:');
  console.log(`   Total Value Generated: $${roi.businessValueGenerated.toLocaleString()}`);
  console.log(`   Avg Value per Introduction: $${roi.averageValuePerIntroduction.toLocaleString()}`);
  console.log(`   Network Growth Rate: ${(roi.networkGrowthRate * 100).toFixed(0)}%`);

  console.log('\n' + '═'.repeat(80));
  console.log('\n✅ Advanced matching example completed successfully!\n');
}

// Run the example
main().catch(console.error);
