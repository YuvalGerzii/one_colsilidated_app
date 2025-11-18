import { Pool } from 'pg';
import bcrypt from 'bcryptjs';

/**
 * Advanced Seed Data Generator
 *
 * Creates 100+ diverse users with edge cases to test system robustness:
 * - Isolated users (no connections)
 * - Super connectors (100+ connections)
 * - Users with conflicting needs/offerings
 * - Users with incomplete profiles
 * - Users in rare industries/locations
 * - Users with extreme trust levels
 * - Users with overlapping expertise
 * - International users with different timezones
 */

interface AdvancedUserData {
  name: string;
  email: string;
  password: string;
  industry: string;
  bio: string;
  location: {
    city: string;
    country: string;
    remote: boolean;
    timezone?: string;
  };
  expertiseAreas: string[];
  needs: Array<{
    category: string;
    description: string;
    priority: 'low' | 'medium' | 'high' | 'critical';
    urgency: 'flexible' | 'weeks' | 'days' | 'immediate';
    flexibility: number;
  }>;
  offerings: Array<{
    category: string;
    description: string;
    value: string;
    capacity: 'limited' | 'moderate' | 'high' | 'unlimited';
  }>;
  profile?: {
    responseTime?: string;
    languages?: string[];
    certifications?: string[];
    yearsExperience?: number;
  };
  tags?: string[];
  connectionStrategy?: 'isolated' | 'normal' | 'super_connector' | 'selective';
}

// Expanded industries including niche/rare ones
const EXTENDED_INDUSTRIES = [
  'Technology', 'Finance', 'Healthcare', 'Education', 'Retail',
  'Manufacturing', 'Real Estate', 'Consulting', 'Marketing', 'Media',
  'Entertainment', 'Energy', 'Agriculture', 'Transportation', 'Telecommunications',
  'Biotechnology', 'Aerospace', 'Robotics', 'Quantum Computing', 'Nanotechnology',
  'Environmental Services', 'Food & Beverage', 'Fashion', 'Gaming', 'E-Sports',
  'Cryptocurrency', 'NFT/Web3', 'Space Technology', 'Clean Energy', 'EdTech',
  'FinTech', 'HealthTech', 'Legal Tech', 'PropTech', 'AgriTech',
  'Maritime', 'Mining', 'Luxury Goods', 'Tourism', 'Hospitality'
];

// Expanded expertise areas including specialized/rare skills
const EXTENDED_EXPERTISE = [
  'Software Development', 'Data Science', 'Machine Learning', 'Blockchain',
  'Cybersecurity', 'Cloud Computing', 'DevOps', 'Mobile Development',
  'Product Management', 'UX Design', 'Digital Marketing', 'Sales',
  'Business Strategy', 'Financial Planning', 'Legal', 'HR Management',
  'Supply Chain', 'Operations', 'Customer Success', 'Public Relations',
  'Quantum Algorithms', 'Bioinformatics', 'Neuroscience', 'Genomics',
  'Robotics Engineering', 'Computer Vision', 'Natural Language Processing', 'Edge Computing',
  'Smart Contracts', 'DeFi Development', 'AR/VR Development', 'Game Design',
  'Sustainable Architecture', 'Carbon Trading', 'Impact Investing', 'Microfinance',
  'Patent Law', 'M&A Advisory', 'Crisis Management', 'Change Management',
  'Influencer Marketing', 'Growth Hacking', 'Community Building', 'Brand Strategy',
  'Ethical Hacking', 'Penetration Testing', 'Forensic Analysis', 'Compliance',
  'Clinical Trials', 'Regulatory Affairs', 'Medical Devices', 'Telemedicine'
];

// Global cities including emerging markets
const GLOBAL_CITIES = [
  { city: 'San Francisco', country: 'USA', timezone: 'America/Los_Angeles' },
  { city: 'New York', country: 'USA', timezone: 'America/New_York' },
  { city: 'London', country: 'UK', timezone: 'Europe/London' },
  { city: 'Berlin', country: 'Germany', timezone: 'Europe/Berlin' },
  { city: 'Singapore', country: 'Singapore', timezone: 'Asia/Singapore' },
  { city: 'Tel Aviv', country: 'Israel', timezone: 'Asia/Jerusalem' },
  { city: 'Toronto', country: 'Canada', timezone: 'America/Toronto' },
  { city: 'Sydney', country: 'Australia', timezone: 'Australia/Sydney' },
  { city: 'Tokyo', country: 'Japan', timezone: 'Asia/Tokyo' },
  { city: 'Paris', country: 'France', timezone: 'Europe/Paris' },
  { city: 'Amsterdam', country: 'Netherlands', timezone: 'Europe/Amsterdam' },
  { city: 'Dubai', country: 'UAE', timezone: 'Asia/Dubai' },
  { city: 'Stockholm', country: 'Sweden', timezone: 'Europe/Stockholm' },
  { city: 'Bangalore', country: 'India', timezone: 'Asia/Kolkata' },
  { city: 'São Paulo', country: 'Brazil', timezone: 'America/Sao_Paulo' },
  { city: 'Shanghai', country: 'China', timezone: 'Asia/Shanghai' },
  { city: 'Seoul', country: 'South Korea', timezone: 'Asia/Seoul' },
  { city: 'Mexico City', country: 'Mexico', timezone: 'America/Mexico_City' },
  { city: 'Lagos', country: 'Nigeria', timezone: 'Africa/Lagos' },
  { city: 'Nairobi', country: 'Kenya', timezone: 'Africa/Nairobi' },
  { city: 'Buenos Aires', country: 'Argentina', timezone: 'America/Argentina/Buenos_Aires' },
  { city: 'Istanbul', country: 'Turkey', timezone: 'Europe/Istanbul' },
  { city: 'Mumbai', country: 'India', timezone: 'Asia/Kolkata' },
  { city: 'Hong Kong', country: 'Hong Kong', timezone: 'Asia/Hong_Kong' },
  { city: 'Cape Town', country: 'South Africa', timezone: 'Africa/Johannesburg' }
];

// Expanded need and offering categories
const EXTENDED_NEEDS = [
  'Funding', 'Technical Expertise', 'Mentorship', 'Marketing Support',
  'Legal Advice', 'Partnership', 'Talent Acquisition', 'Customer Introductions',
  'Office Space', 'Technology Infrastructure', 'Strategic Guidance',
  'Sales Support', 'Design Services', 'Operational Support', 'Investment Opportunities',
  'Research Collaboration', 'Patent Filing', 'Regulatory Compliance', 'Market Research',
  'Crisis Management', 'Rebranding', 'International Expansion', 'Supply Chain Optimization',
  'Data Analytics', 'Cybersecurity Audit', 'Cloud Migration', 'API Integration',
  'User Testing', 'Content Creation', 'SEO Optimization', 'Community Management'
];

const EXTENDED_OFFERINGS = [
  'Capital Investment', 'Technical Skills', 'Business Mentorship', 'Marketing Expertise',
  'Legal Services', 'Strategic Partnerships', 'Recruitment', 'Network Introductions',
  'Co-working Space', 'Cloud Infrastructure', 'Business Advice',
  'Sales Expertise', 'Design Skills', 'Operations Management', 'Industry Connections',
  'Research Facilities', 'Patent Portfolio', 'Regulatory Knowledge', 'Market Data',
  'Crisis Response Team', 'Brand Agency', 'International Network', 'Logistics Network',
  'Data Platform', 'Security Team', 'Cloud Credits', 'API Access',
  'Beta Testers', 'Content Team', 'SEO Tools', 'Community Platform'
];

// Languages
const LANGUAGES = [
  'English', 'Spanish', 'Mandarin', 'French', 'German', 'Portuguese',
  'Arabic', 'Hindi', 'Japanese', 'Korean', 'Russian', 'Italian'
];

/**
 * Generate 100+ advanced test users with edge cases
 */
export function generateAdvancedUsers(count: number = 100): AdvancedUserData[] {
  const users: AdvancedUserData[] = [];

  const firstNames = [
    'Aiden', 'Bella', 'Carlos', 'Diana', 'Ethan', 'Fiona', 'Gabriel', 'Hannah',
    'Isaac', 'Julia', 'Kevin', 'Luna', 'Marcus', 'Nina', 'Oscar', 'Priya',
    'Quinn', 'Rafael', 'Sophia', 'Thomas', 'Uma', 'Vincent', 'Willow', 'Xavier',
    'Yuki', 'Zara', 'Aaliyah', 'Bjorn', 'Chloe', 'Diego', 'Elena', 'Finn',
    'Gianna', 'Hassan', 'Ivy', 'Javier', 'Kai', 'Leila', 'Miguel', 'Nora',
    'Omar', 'Penelope', 'Quincy', 'Rosa', 'Sebastian', 'Tara', 'Umar', 'Vera',
    'Wei', 'Xiomara', 'Yasmin', 'Zion', 'Amara', 'Bruno', 'Camila', 'Dante',
    'Elara', 'Felix', 'Gemma', 'Hugo', 'Iris', 'Jasper', 'Kira', 'Luca',
    'Maya', 'Noah', 'Olivia', 'Pablo', 'Qing', 'Ravi', 'Sara', 'Theo',
    'Ula', 'Vito', 'Wanda', 'Xander', 'Yana', 'Zeke', 'Aria', 'Blake',
    'Clara', 'Darius', 'Eva', 'Fabian', 'Grace', 'Henry', 'Isla', 'Jose',
    'Keira', 'Leon', 'Mila', 'Nico', 'Opal', 'Pietro', 'Queenie', 'Roman',
    'Stella', 'Tomas', 'Una', 'Valentina'
  ];

  const lastNames = [
    'Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Fischer', 'Garcia', 'Hall',
    'Ibrahim', 'Johnson', 'Kim', 'Lee', 'Martinez', 'Nguyen', 'O\'Brien', 'Patel',
    'Quinn', 'Rodriguez', 'Smith', 'Taylor', 'Ueda', 'Vargas', 'Williams', 'Xu',
    'Yang', 'Zhang', 'Ahmed', 'Baker', 'Cooper', 'Diaz', 'Edwards', 'Foster',
    'Green', 'Harris', 'Jackson', 'Jones', 'Khan', 'Lewis', 'Moore', 'Nelson',
    'Parker', 'Robinson', 'Singh', 'Thompson', 'Walker', 'White', 'Wilson', 'Young',
    'Adams', 'Clark', 'Campbell', 'Desai', 'El-Amin', 'Fernandez', 'Gupta', 'Hansen',
    'Ivanov', 'Jensen', 'Kowalski', 'Lopez', 'Murphy', 'Nakamura', 'Olsen', 'Petrov',
    'Qian', 'Rossi', 'Sato', 'Tanaka', 'Ulrich', 'Varga', 'Wang', 'Xiang',
    'Yamamoto', 'Zhou', 'Ali', 'Berg', 'Costa', 'Dubois', 'Eriksson', 'Flores',
    'Goldman', 'Hoffman', 'Ito', 'Johansson', 'Kumar', 'Larsson', 'Meyer', 'Nielsen',
    'Orozco', 'Pham', 'Qureshi', 'Ramirez', 'Santos', 'Tran', 'Usman', 'Vidal'
  ];

  for (let i = 0; i < count; i++) {
    const firstName = firstNames[i % firstNames.length];
    const lastName = lastNames[Math.floor(i / firstNames.length) % lastNames.length];
    const name = `${firstName} ${lastName}`;
    const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}.${i}@bondai-test.com`;

    const location = GLOBAL_CITIES[i % GLOBAL_CITIES.length];
    const industry = EXTENDED_INDUSTRIES[i % EXTENDED_INDUSTRIES.length];

    // Determine connection strategy based on user type
    let connectionStrategy: 'isolated' | 'normal' | 'super_connector' | 'selective';
    if (i < 5) {
      connectionStrategy = 'isolated'; // First 5 users are isolated
    } else if (i < 15) {
      connectionStrategy = 'super_connector'; // Next 10 are super connectors
    } else if (i < 25) {
      connectionStrategy = 'selective'; // Next 10 are selective
    } else {
      connectionStrategy = 'normal';
    }

    // Select expertise (1-5 areas, some with rare skills)
    const expertiseCount = i < 10 ? 1 : (i < 30 ? 5 : 2 + (i % 3));
    const expertiseAreas = [];
    for (let j = 0; j < expertiseCount; j++) {
      const idx = (i * 7 + j * 3) % EXTENDED_EXPERTISE.length;
      expertiseAreas.push(EXTENDED_EXPERTISE[idx]);
    }

    // Generate needs (0-4, some users with no needs, some with many)
    const needCount = i < 10 ? 0 : i < 20 ? 4 : 1 + (i % 3);
    const needs = [];
    const priorities: ('low' | 'medium' | 'high' | 'critical')[] = ['low', 'medium', 'high', 'critical'];
    const urgencies: ('flexible' | 'weeks' | 'days' | 'immediate')[] = ['flexible', 'weeks', 'days', 'immediate'];

    for (let j = 0; j < needCount; j++) {
      const idx = (i * 5 + j * 2) % EXTENDED_NEEDS.length;
      const category = EXTENDED_NEEDS[idx];

      needs.push({
        category,
        description: `${i < 20 ? 'Urgently ' : ''}Looking for ${category.toLowerCase()} to ${i % 3 === 0 ? 'rapidly scale' : i % 3 === 1 ? 'optimize' : 'expand'} our ${industry.toLowerCase()} operations`,
        priority: i < 15 ? 'critical' : priorities[j % priorities.length],
        urgency: i < 15 ? 'immediate' : urgencies[j % urgencies.length],
        flexibility: i < 10 ? 0.1 : i < 20 ? 0.9 : 0.3 + (i % 7) * 0.1
      });
    }

    // Generate offerings (0-4, some users with no offerings)
    const offeringCount = i < 15 ? 0 : i < 25 ? 4 : 1 + (i % 3);
    const offerings = [];
    const capacities: ('limited' | 'moderate' | 'high' | 'unlimited')[] = ['limited', 'moderate', 'high', 'unlimited'];

    for (let j = 0; j < offeringCount; j++) {
      const idx = (i * 3 + j * 5) % EXTENDED_OFFERINGS.length;
      const category = EXTENDED_OFFERINGS[idx];

      offerings.push({
        category,
        description: `Providing ${category.toLowerCase()} with ${expertiseAreas[0]?.toLowerCase() || 'extensive'} background and ${10 + (i % 15)} years experience`,
        value: `${10 + (i % 15)} years of experience in ${industry}${i % 5 === 0 ? ' with Fortune 500 companies' : ''}`,
        capacity: i < 10 ? 'unlimited' : capacities[j % capacities.length]
      });
    }

    // Generate bio (some incomplete, some very detailed)
    let bio = '';
    if (i < 5) {
      bio = `${name} works in ${industry}.`; // Minimal bio
    } else if (i < 15) {
      bio = `${name} is a highly connected ${industry} professional with expertise in ${expertiseAreas.join(', ')}. ` +
            `Based in ${location.city}, ${location.country}. Available for partnerships, mentorship, and strategic collaborations globally.`; // Super connector bio
    } else if (i < 20) {
      bio = ''; // Empty bio - edge case
    } else {
      bio = `${name} is a ${industry} ${i % 2 === 0 ? 'leader' : 'expert'} with expertise in ${expertiseAreas.join(', ')}. ` +
            `Based in ${location.city}, ${location.country}, ${firstName} is ${i % 3 === 0 ? 'actively' : 'selectively'} ${needs.length > 0 ? `seeking ${needs[0].category.toLowerCase()}` : 'open to opportunities'}${offerings.length > 0 ? ` and offering ${offerings[0].category.toLowerCase()}` : ''}.`;
    }

    // Select languages (1-4)
    const languageCount = 1 + (i % 4);
    const languages = [];
    for (let j = 0; j < languageCount; j++) {
      languages.push(LANGUAGES[(i + j) % LANGUAGES.length]);
    }

    // Additional profile data
    const profile = i < 10 ? undefined : {
      responseTime: i < 30 ? '< 1 hour' : i < 60 ? '< 24 hours' : '< 3 days',
      languages,
      certifications: i % 3 === 0 ? [`Certified ${expertiseAreas[0]} Professional`] : [],
      yearsExperience: 5 + (i % 20)
    };

    // Tags for additional categorization
    const tags = [];
    if (i < 15) tags.push('early-adopter');
    if (connectionStrategy === 'super_connector') tags.push('influencer');
    if (needs.some(n => n.urgency === 'immediate')) tags.push('urgent');
    if (offerings.some(o => o.capacity === 'unlimited')) tags.push('high-capacity');
    if (i % 10 === 0) tags.push('verified');
    if (i % 7 === 0) tags.push('premium');

    users.push({
      name,
      email,
      password: 'Test@1234', // All test users have same password
      industry,
      bio,
      location: {
        ...location,
        remote: i % 4 === 0 // Every 4th user is remote
      },
      expertiseAreas,
      needs,
      offerings,
      profile,
      tags,
      connectionStrategy
    });
  }

  return users;
}

/**
 * Seed advanced users into database
 */
export async function seedAdvancedUsers(pool: Pool, users: AdvancedUserData[]): Promise<Map<string, string>> {
  const client = await pool.connect();
  const userIdMap = new Map<string, string>(); // email -> userId

  try {
    console.log(`Starting advanced user seeding (${users.length} users)...`);

    for (const user of users) {
      // Hash password
      const passwordHash = await bcrypt.hash(user.password, 10);

      // Create user
      const userResult = await client.query(
        `INSERT INTO users (name, email, password_hash, industry, bio, metadata, created_at)
         VALUES ($1, $2, $3, $4, $5, $6, NOW())
         RETURNING id`,
        [
          user.name,
          user.email,
          passwordHash,
          user.industry,
          user.bio,
          JSON.stringify({
            location: user.location,
            expertiseAreas: user.expertiseAreas,
            profile: user.profile,
            tags: user.tags,
            connectionStrategy: user.connectionStrategy
          })
        ]
      );

      const userId = userResult.rows[0].id;
      userIdMap.set(user.email, userId);

      // Create user profile
      await client.query(
        `INSERT INTO user_profiles (
          user_id, needs, offerings, preferences, location, industry, expertise_areas
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [
          userId,
          JSON.stringify(user.needs),
          JSON.stringify(user.offerings),
          JSON.stringify({ connectionStrategy: user.connectionStrategy }),
          JSON.stringify(user.location),
          user.industry,
          user.expertiseAreas
        ]
      );

      // Create individual need records
      for (const need of user.needs) {
        await client.query(
          `INSERT INTO user_needs (
            user_id, category, description, priority, urgency, flexibility, status
          )
          VALUES ($1, $2, $3, $4, $5, $6, 'active')`,
          [userId, need.category, need.description, need.priority, need.urgency, need.flexibility]
        );
      }

      // Create individual offering records
      for (const offering of user.offerings) {
        await client.query(
          `INSERT INTO user_offerings (
            user_id, category, description, value, capacity, status
          )
          VALUES ($1, $2, $3, $4, $5, 'available')`,
          [userId, offering.category, offering.description, offering.value, offering.capacity]
        );
      }

      // Create agent for user with varying risk tolerance
      const riskTolerance = user.connectionStrategy === 'super_connector' ? 0.9 :
                           user.connectionStrategy === 'selective' ? 0.3 :
                           user.connectionStrategy === 'isolated' ? 0.1 :
                           0.5 + (users.indexOf(user) % 5) * 0.1;

      await client.query(
        `INSERT INTO agents (
          user_id, agent_type, capabilities, negotiation_style, risk_tolerance, metadata
        )
        VALUES ($1, 'user_representative', $2, $3, $4, $5)`,
        [
          userId,
          JSON.stringify(['negotiate', 'analyze', 'match', 'network_traverse']),
          user.connectionStrategy === 'super_connector' ? 'aggressive' :
          user.connectionStrategy === 'selective' ? 'conservative' :
          'collaborative',
          riskTolerance,
          JSON.stringify({
            minAcceptableScore: user.connectionStrategy === 'selective' ? 0.8 : 0.6,
            learningEnabled: true,
            connectionStrategy: user.connectionStrategy
          })
        ]
      );

      if ((users.indexOf(user) + 1) % 20 === 0) {
        console.log(`  Created ${users.indexOf(user) + 1}/${users.length} users...`);
      }
    }

    console.log(`\n✅ Successfully seeded ${users.length} advanced users`);
    return userIdMap;

  } catch (error) {
    console.error('Error seeding advanced users:', error);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Create advanced connections based on connection strategies
 */
export async function seedAdvancedConnections(
  pool: Pool,
  userIdMap: Map<string, string>,
  users: AdvancedUserData[]
): Promise<void> {
  const client = await pool.connect();

  try {
    console.log('\nCreating advanced connections...');

    const userIds = Array.from(userIdMap.values());
    const userEmails = Array.from(userIdMap.keys());
    let connectionCount = 0;

    for (let i = 0; i < userIds.length; i++) {
      const userId = userIds[i];
      const userEmail = userEmails[i];
      const user = users.find(u => u.email === userEmail)!;

      // Determine number of connections based on strategy
      let connectionsToCreate = 0;
      switch (user.connectionStrategy) {
        case 'isolated':
          connectionsToCreate = 0; // No connections
          break;
        case 'selective':
          connectionsToCreate = 3 + (i % 3); // 3-5 connections
          break;
        case 'super_connector':
          connectionsToCreate = 50 + (i % 50); // 50-99 connections
          break;
        default:
          connectionsToCreate = 5 + (i % 11); // 5-15 connections
      }

      for (let j = 0; j < connectionsToCreate; j++) {
        const targetIdx = (i + j + 1) % userIds.length;
        const targetUserId = userIds[targetIdx];

        // Skip self-connections
        if (targetUserId === userId) continue;

        // Create contact
        const contactResult = await client.query(
          `INSERT INTO contacts (
            user_id, name, email, company, relationship_type, source
          )
          SELECT $1, u.name, u.email, $3, $4, 'platform'
          FROM users u WHERE u.id = $2
          RETURNING id`,
          [userId, targetUserId, 'Bond.AI Platform', 'professional']
        );

        const contactId = contactResult.rows[0].id;

        // Calculate trust level based on strategies
        let trustLevel = 0.4 + (Math.random() * 0.5); // Base: 0.4-0.9
        if (user.connectionStrategy === 'selective') {
          trustLevel = Math.max(trustLevel, 0.7); // Selective users have high trust
        } else if (user.connectionStrategy === 'super_connector') {
          trustLevel = 0.3 + (Math.random() * 0.4); // Super connectors have varied trust
        }

        const connectionStrength = user.connectionStrategy === 'selective' ?
          0.7 + (Math.random() * 0.3) : // 0.7-1.0 for selective
          0.3 + (Math.random() * 0.6); // 0.3-0.9 for others

        const degreeOfSeparation = j < 5 ? 1 : j < 20 ? 2 : j < 50 ? 3 : Math.min(4 + Math.floor(j / 50), 6);

        // Create connection
        await client.query(
          `INSERT INTO connections (
            user_id, contact_id, relationship_type, connection_strength,
            trust_level, degree_of_separation
          )
          VALUES ($1, $2, 'professional', $3, $4, $5)`,
          [userId, contactId, connectionStrength, trustLevel, degreeOfSeparation]
        );

        connectionCount++;
      }

      if ((i + 1) % 20 === 0) {
        console.log(`  Created connections for ${i + 1}/${userIds.length} users...`);
      }
    }

    console.log(`\n✅ Created ${connectionCount} advanced connections`);

  } catch (error) {
    console.error('Error seeding advanced connections:', error);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Clean advanced test data
 */
export async function cleanAdvancedTestData(pool: Pool): Promise<void> {
  const client = await pool.connect();

  try {
    console.log('Cleaning existing advanced test data...');

    // Delete all test users (cascade will delete related records)
    await client.query(
      `DELETE FROM users WHERE email LIKE '%@bondai-test.com'`
    );

    console.log('✅ Cleaned advanced test data');

  } catch (error) {
    console.error('Error cleaning advanced test data:', error);
    throw error;
  } finally {
    client.release();
  }
}
