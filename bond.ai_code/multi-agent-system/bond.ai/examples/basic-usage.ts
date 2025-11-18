/**
 * Bond.AI - Basic Usage Example
 *
 * This example demonstrates the core features of Bond.AI:
 * - Adding contacts and connections
 * - Building your network
 * - Finding matches
 * - Creating introductions
 */

import { BondAI, Contact, Connection, RelationshipType } from '../src/BondAI';

async function main() {
  console.log('🚀 Bond.AI - Basic Usage Example\n');

  // Step 1: Initialize Bond.AI
  console.log('Step 1: Initializing Bond.AI...');
  const bondAI = new BondAI('user-123', {
    maxDegreeOfSeparation: 3,
    minCompatibilityScore: 0.6
  });
  console.log('✓ Bond.AI initialized\n');

  // Step 2: Add your first-degree connections
  console.log('Step 2: Adding first-degree connections...');

  const alice: Contact = {
    id: 'alice',
    name: 'Alice Johnson',
    email: 'alice@techinnovations.com',
    company: 'Tech Innovations Inc',
    title: 'CEO & Founder',
    industry: 'Technology',
    bio: 'Passionate entrepreneur building AI-powered solutions. Looking for strategic partnerships and growth capital.',
    skills: ['AI', 'Machine Learning', 'Product Strategy', 'Team Building'],
    interests: ['artificial intelligence', 'startups', 'innovation'],
    needs: ['seed funding', 'technical co-founder', 'enterprise clients'],
    offerings: ['AI consulting', 'mentorship', 'industry connections'],
    socialProfiles: {
      linkedin: 'linkedin.com/in/alicejohnson',
      twitter: '@alicetech'
    }
  };

  const bob: Contact = {
    id: 'bob',
    name: 'Bob Smith',
    email: 'bob@vcpartners.com',
    company: 'Venture Capital Partners',
    title: 'Managing Partner',
    industry: 'Venture Capital',
    bio: 'Experienced investor focused on AI and deep tech startups. Actively seeking innovative AI companies.',
    skills: ['Investment Strategy', 'Startup Mentoring', 'Financial Analysis'],
    interests: ['venture capital', 'artificial intelligence', 'startups'],
    needs: ['deal flow', 'AI startups', 'technical due diligence'],
    offerings: ['seed funding', 'strategic advice', 'network introductions'],
    socialProfiles: {
      linkedin: 'linkedin.com/in/bobsmith'
    }
  };

  const carol: Contact = {
    id: 'carol',
    name: 'Carol Martinez',
    email: 'carol@enterprise.com',
    company: 'Enterprise Solutions Corp',
    title: 'Chief Technology Officer',
    industry: 'Enterprise Software',
    bio: 'Leading digital transformation initiatives. Seeking innovative technology partners.',
    skills: ['Enterprise Architecture', 'Digital Transformation', 'AI Integration'],
    interests: ['enterprise software', 'digital transformation', 'innovation'],
    needs: ['AI solutions', 'technology partners', 'innovation consultants'],
    offerings: ['enterprise contracts', 'pilot opportunities', 'references'],
    socialProfiles: {
      linkedin: 'linkedin.com/in/carolmartinez'
    }
  };

  bondAI.addContact(alice);
  bondAI.addContact(bob);
  bondAI.addContact(carol);
  console.log('✓ Added 3 contacts\n');

  // Step 3: Add connections
  console.log('Step 3: Creating connections...');

  // You know Alice (strong relationship)
  bondAI.addConnection({
    id: 'conn-user-alice',
    fromContactId: 'user-123',
    toContactId: 'alice',
    relationshipType: RelationshipType.COLLEAGUE,
    strength: 0.9,
    trustLevel: 0.95,
    interactionFrequency: 8, // 8 interactions per month
    lastInteraction: new Date('2025-11-10')
  });

  // Alice knows Bob (good relationship)
  bondAI.addConnection({
    id: 'conn-alice-bob',
    fromContactId: 'alice',
    toContactId: 'bob',
    relationshipType: RelationshipType.ACQUAINTANCE,
    strength: 0.7,
    trustLevel: 0.75,
    interactionFrequency: 2,
    lastInteraction: new Date('2025-10-15')
  });

  // You know Carol (acquaintance)
  bondAI.addConnection({
    id: 'conn-user-carol',
    fromContactId: 'user-123',
    toContactId: 'carol',
    relationshipType: RelationshipType.CLIENT,
    strength: 0.6,
    trustLevel: 0.7,
    interactionFrequency: 3,
    lastInteraction: new Date('2025-11-05')
  });

  console.log('✓ Created 3 connections\n');

  // Step 4: Build network graph
  console.log('Step 4: Building network graph...');
  bondAI.buildNetwork();

  const stats = bondAI.getNetworkStats();
  console.log('✓ Network built successfully');
  console.log(`  Total contacts: ${stats.totalContacts}`);
  console.log(`  Total connections: ${stats.totalConnections}`);
  console.log(`  Contacts by degree:`, stats.contactsByDegree);
  console.log('');

  // Step 5: Analyze contacts
  console.log('Step 5: Analyzing contacts with AI...');

  const aliceAnalysis = await bondAI.analyzeContact('alice');
  console.log('✓ Alice Analysis:');
  console.log(`  Career Stage: ${aliceAnalysis.profileAnalysis.careerStage}`);
  console.log(`  Expertise: ${aliceAnalysis.profileAnalysis.expertiseAreas.join(', ')}`);
  console.log(`  Needs: ${aliceAnalysis.needsAnalysis.explicit.join(', ')}`);
  console.log('');

  // Step 6: Discover matches
  console.log('Step 6: Discovering matches...');
  const matches = await bondAI.discoverMatches();
  console.log(`✓ Found ${matches.length} potential matches\n`);

  // Step 7: Display top matches
  console.log('Step 7: Top Matches:');
  console.log('─'.repeat(80));

  const topMatches = bondAI.getTopMatches(5);
  topMatches.forEach((match, index) => {
    console.log(`\n${index + 1}. ${match.sourceContact.name} ⟷ ${match.targetContact.name}`);
    console.log(`   Overall Score: ${(match.overallScore * 100).toFixed(0)}% | Priority: ${match.priority.toUpperCase()}`);
    console.log(`   Match Type: ${match.matchType.replace(/_/g, ' ')}`);
    console.log(`   Compatibility: ${(match.compatibilityScore * 100).toFixed(0)}%`);
    console.log(`   Value Potential: ${(match.valuePotential * 100).toFixed(0)}%`);
    console.log(`   Success Probability: ${(match.successProbability * 100).toFixed(0)}%`);
    console.log(`   Connection Path: ${match.shortestPath.contacts.map(c => c.name).join(' → ')}`);
    console.log(`   Key Reasons:`);
    match.reasons.slice(0, 2).forEach(reason => {
      console.log(`   • ${reason.description}`);
    });
  });
  console.log('\n' + '─'.repeat(80) + '\n');

  // Step 8: Create an introduction
  if (topMatches.length > 0) {
    console.log('Step 8: Creating introduction for top match...');
    const topMatch = topMatches[0];

    const introduction = await bondAI.createIntroduction(topMatch.id);
    console.log('✓ Introduction created\n');

    console.log('Introduction Preview:');
    console.log('─'.repeat(80));
    console.log(introduction.message);
    console.log('─'.repeat(80));
    console.log('\nConversation Starters:');
    introduction.conversationStarters.forEach((starter, i) => {
      console.log(`${i + 1}. ${starter}`);
    });
    console.log('\n' + '─'.repeat(80) + '\n');

    // Step 9: Send introduction
    console.log('Step 9: Sending introduction...');
    await bondAI.sendIntroduction(introduction.id);
    console.log('✓ Introduction sent\n');

    // Step 10: Simulate acceptance and track success
    console.log('Step 10: Tracking relationship...');
    bondAI.acceptIntroduction(introduction.id);
    console.log('✓ Introduction accepted');

    // Record some interactions
    bondAI.recordInteraction(
      topMatch.sourceContact.id,
      topMatch.targetContact.id,
      'Had initial coffee chat - great alignment on AI vision'
    );
    console.log('✓ Recorded interaction');

    // Record business value
    bondAI.recordBusinessValue(
      topMatch.sourceContact.id,
      topMatch.targetContact.id,
      50000,
      'Secured seed funding commitment'
    );
    console.log('✓ Recorded business value: $50,000\n');
  }

  // Step 11: View analytics
  console.log('Step 11: Viewing Analytics...');
  console.log('─'.repeat(80));

  const analytics = bondAI.getAnalytics();
  console.log('\n📊 Network Analytics:');
  console.log(`   Total Contacts: ${analytics.network.totalContacts}`);
  console.log(`   Total Reach: ${analytics.network.reach} people`);
  console.log(`   Network Density: ${analytics.network.averageConnectionsPerContact.toFixed(2)} connections/contact`);

  console.log('\n🎯 Match Analytics:');
  console.log(`   Total Matches: ${analytics.matches.total}`);
  console.log(`   Critical Opportunities: ${analytics.matches.byPriority.critical}`);
  console.log(`   High Priority: ${analytics.matches.byPriority.high}`);
  console.log(`   Average Compatibility: ${(analytics.matches.averageCompatibility * 100).toFixed(0)}%`);

  console.log('\n🤝 Introduction Analytics:');
  console.log(`   Total Introductions: ${analytics.introductions.totalIntroductions}`);
  console.log(`   Success Rate: ${(analytics.introductions.successRate * 100).toFixed(0)}%`);
  console.log(`   Active Relationships: ${analytics.introductions.activeRelationships}`);
  console.log(`   Business Value Generated: $${analytics.introductions.businessValueGenerated.toLocaleString()}`);
  console.log('');

  // Step 12: View ROI
  const roi = bondAI.getROI();
  console.log('💰 ROI Metrics:');
  console.log(`   Total Introductions: ${roi.totalIntroductions}`);
  console.log(`   Successful Connections: ${roi.successfulConnections}`);
  console.log(`   Business Value: $${roi.businessValueGenerated.toLocaleString()}`);
  console.log(`   Average Value per Introduction: $${roi.averageValuePerIntroduction.toLocaleString()}`);
  console.log('');

  // Step 13: View Dashboard
  const dashboard = bondAI.getDashboard();
  console.log('📈 Dashboard Summary:');
  console.log(`   Network Size: ${dashboard.networkSize} contacts`);
  console.log(`   Total Reach: ${dashboard.totalReach} people`);
  console.log(`   Active Matches: ${dashboard.activeMatches}`);
  console.log(`   Critical Opportunities: ${dashboard.criticalOpportunities}`);
  console.log(`   Pending Introductions: ${dashboard.pendingIntroductions}`);
  console.log(`   Active Relationships: ${dashboard.activeRelationships}`);
  console.log(`   Business Value: $${dashboard.businessValue.toLocaleString()}`);

  console.log('\n' + '─'.repeat(80));
  console.log('\n✅ Basic usage example completed successfully!\n');
}

// Run the example
main().catch(console.error);
