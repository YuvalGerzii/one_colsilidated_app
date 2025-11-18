import { Pool } from 'pg';
import bcrypt from 'bcryptjs';

/**
 * Seed Data Generator
 *
 * Creates 50 diverse users with realistic profiles, needs, and offerings
 * to demonstrate the Bond.AI platform capabilities
 */

interface UserData {
  name: string;
  email: string;
  password: string;
  industry: string;
  bio: string;
  location: {
    city: string;
    country: string;
    remote: boolean;
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
}

// Industries
const INDUSTRIES = [
  'Technology', 'Finance', 'Healthcare', 'Education', 'Retail',
  'Manufacturing', 'Real Estate', 'Consulting', 'Marketing', 'Media',
  'Entertainment', 'Energy', 'Agriculture', 'Transportation', 'Telecommunications'
];

// Expertise areas
const EXPERTISE_AREAS = [
  'Software Development', 'Data Science', 'Machine Learning', 'Blockchain',
  'Cybersecurity', 'Cloud Computing', 'DevOps', 'Mobile Development',
  'Product Management', 'UX Design', 'Digital Marketing', 'Sales',
  'Business Strategy', 'Financial Planning', 'Legal', 'HR Management',
  'Supply Chain', 'Operations', 'Customer Success', 'Public Relations'
];

// Cities
const CITIES = [
  { city: 'San Francisco', country: 'USA' },
  { city: 'New York', country: 'USA' },
  { city: 'London', country: 'UK' },
  { city: 'Berlin', country: 'Germany' },
  { city: 'Singapore', country: 'Singapore' },
  { city: 'Tel Aviv', country: 'Israel' },
  { city: 'Toronto', country: 'Canada' },
  { city: 'Sydney', country: 'Australia' },
  { city: 'Tokyo', country: 'Japan' },
  { city: 'Paris', country: 'France' },
  { city: 'Amsterdam', country: 'Netherlands' },
  { city: 'Dubai', country: 'UAE' },
  { city: 'Stockholm', country: 'Sweden' },
  { city: 'Bangalore', country: 'India' },
  { city: 'São Paulo', country: 'Brazil' }
];

// Need categories
const NEED_CATEGORIES = [
  'Funding', 'Technical Expertise', 'Mentorship', 'Marketing Support',
  'Legal Advice', 'Partnership', 'Talent Acquisition', 'Customer Introductions',
  'Office Space', 'Technology Infrastructure', 'Strategic Guidance',
  'Sales Support', 'Design Services', 'Operational Support', 'Investment Opportunities'
];

// Offering categories
const OFFERING_CATEGORIES = [
  'Capital Investment', 'Technical Skills', 'Business Mentorship', 'Marketing Expertise',
  'Legal Services', 'Strategic Partnerships', 'Recruitment', 'Network Introductions',
  'Co-working Space', 'Cloud Infrastructure', 'Business Advice',
  'Sales Expertise', 'Design Skills', 'Operations Management', 'Industry Connections'
];

// Generate realistic user data
export function generateUsers(count: number = 50): UserData[] {
  const users: UserData[] = [];

  const firstNames = [
    'Alice', 'Bob', 'Carol', 'David', 'Emma', 'Frank', 'Grace', 'Henry',
    'Iris', 'Jack', 'Karen', 'Leo', 'Maria', 'Nathan', 'Olivia', 'Paul',
    'Quinn', 'Rachel', 'Sam', 'Tina', 'Uma', 'Victor', 'Wendy', 'Xavier',
    'Yara', 'Zack', 'Ava', 'Benjamin', 'Charlotte', 'Daniel', 'Elena', 'Felix',
    'Gina', 'Hugo', 'Isabella', 'James', 'Kara', 'Liam', 'Mia', 'Noah',
    'Sophia', 'Thomas', 'Victoria', 'William', 'Zoe', 'Adrian', 'Bella', 'Chris',
    'Diana', 'Ethan'
  ];

  const lastNames = [
    'Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Fischer', 'Garcia', 'Hall',
    'Ibrahim', 'Johnson', 'Kim', 'Lee', 'Martinez', 'Nguyen', 'O\'Brien', 'Patel',
    'Quinn', 'Rodriguez', 'Smith', 'Taylor', 'Ueda', 'Vargas', 'Williams', 'Xu',
    'Yang', 'Zhang', 'Ahmed', 'Baker', 'Cooper', 'Diaz', 'Edwards', 'Foster',
    'Green', 'Harris', 'Jackson', 'Jones', 'Khan', 'Lewis', 'Moore', 'Nelson',
    'Parker', 'Robinson', 'Singh', 'Thompson', 'Walker', 'White', 'Wilson', 'Young',
    'Adams', 'Clark'
  ];

  for (let i = 0; i < count; i++) {
    const firstName = firstNames[i % firstNames.length];
    const lastName = lastNames[i % lastNames.length];
    const name = `${firstName} ${lastName}`;
    const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}@bondai-demo.com`;

    const location = CITIES[i % CITIES.length];
    const industry = INDUSTRIES[i % INDUSTRIES.length];

    // Select 2-4 expertise areas
    const expertiseCount = 2 + (i % 3);
    const expertiseAreas = [];
    for (let j = 0; j < expertiseCount; j++) {
      const idx = (i * 3 + j) % EXPERTISE_AREAS.length;
      expertiseAreas.push(EXPERTISE_AREAS[idx]);
    }

    // Generate 1-3 needs
    const needCount = 1 + (i % 3);
    const needs = [];
    const priorities: ('low' | 'medium' | 'high' | 'critical')[] = ['low', 'medium', 'high', 'critical'];
    const urgencies: ('flexible' | 'weeks' | 'days' | 'immediate')[] = ['flexible', 'weeks', 'days', 'immediate'];

    for (let j = 0; j < needCount; j++) {
      const idx = (i * 2 + j) % NEED_CATEGORIES.length;
      const category = NEED_CATEGORIES[idx];

      needs.push({
        category,
        description: `Looking for ${category.toLowerCase()} to help scale our ${industry.toLowerCase()} business`,
        priority: priorities[j % priorities.length],
        urgency: urgencies[j % urgencies.length],
        flexibility: 0.3 + (i % 7) * 0.1
      });
    }

    // Generate 1-3 offerings
    const offeringCount = 1 + (i % 3);
    const offerings = [];
    const capacities: ('limited' | 'moderate' | 'high' | 'unlimited')[] = ['limited', 'moderate', 'high', 'unlimited'];

    for (let j = 0; j < offeringCount; j++) {
      const idx = (i * 2 + j) % OFFERING_CATEGORIES.length;
      const category = OFFERING_CATEGORIES[idx];

      offerings.push({
        category,
        description: `Providing ${category.toLowerCase()} with ${expertiseAreas[0].toLowerCase()} background`,
        value: `${10 + (i % 10)} years of experience in ${industry}`,
        capacity: capacities[j % capacities.length]
      });
    }

    // Generate bio
    const bio = `${name} is a ${industry} professional with expertise in ${expertiseAreas.join(', ')}. ` +
               `Based in ${location.city}, ${location.country}, ${firstName} is passionate about innovation and collaboration. ` +
               `Currently ${needs[0].priority === 'critical' ? 'urgently ' : ''}seeking ${needs[0].category.toLowerCase()} ` +
               `and offering ${offerings[0].category.toLowerCase()} to the right partners.`;

    users.push({
      name,
      email,
      password: 'Demo@1234', // All demo users have same password
      industry,
      bio,
      location: {
        ...location,
        remote: i % 3 === 0 // Every 3rd user is remote
      },
      expertiseAreas,
      needs,
      offerings
    });
  }

  return users;
}

/**
 * Seed the database with users
 */
export async function seedUsers(pool: Pool, users: UserData[]): Promise<Map<string, string>> {
  const client = await pool.connect();
  const userIdMap = new Map<string, string>(); // email -> userId

  try {
    console.log('Starting user seeding...');

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
            expertiseAreas: user.expertiseAreas
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
          JSON.stringify({}),
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

      // Create agent for user
      await client.query(
        `INSERT INTO agents (
          user_id, agent_type, capabilities, negotiation_style, risk_tolerance, metadata
        )
        VALUES ($1, 'user_representative', $2, $3, $4, $5)`,
        [
          userId,
          JSON.stringify(['negotiate', 'analyze', 'match']),
          'collaborative',
          0.5 + (users.indexOf(user) % 5) * 0.1, // Vary risk tolerance
          JSON.stringify({
            minAcceptableScore: 0.6,
            learningEnabled: true
          })
        ]
      );

      console.log(`✓ Created user: ${user.name} (${user.email})`);
    }

    console.log(`\n✅ Successfully seeded ${users.length} users`);
    return userIdMap;

  } catch (error) {
    console.error('Error seeding users:', error);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Create connections between users
 */
export async function seedConnections(pool: Pool, userIdMap: Map<string, string>): Promise<void> {
  const client = await pool.connect();

  try {
    console.log('\nCreating connections between users...');

    const userIds = Array.from(userIdMap.values());
    let connectionCount = 0;

    // Create connections: each user connects to 5-15 random other users
    for (let i = 0; i < userIds.length; i++) {
      const userId = userIds[i];
      const connectionsToCreate = 5 + (i % 11); // 5-15 connections

      for (let j = 0; j < connectionsToCreate; j++) {
        const targetIdx = (i + j + 1) % userIds.length;
        const targetUserId = userIds[targetIdx];

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

        // Create connection
        const trustLevel = 0.4 + (Math.random() * 0.5); // 0.4-0.9
        const connectionStrength = 0.3 + (Math.random() * 0.6); // 0.3-0.9
        const degreeOfSeparation = j < 3 ? 1 : j < 8 ? 2 : 3;

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

      if ((i + 1) % 10 === 0) {
        console.log(`  Created connections for ${i + 1}/${userIds.length} users...`);
      }
    }

    console.log(`\n✅ Created ${connectionCount} connections`);

  } catch (error) {
    console.error('Error seeding connections:', error);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Clean existing seed data
 */
export async function cleanSeedData(pool: Pool): Promise<void> {
  const client = await pool.connect();

  try {
    console.log('Cleaning existing seed data...');

    // Delete all demo users (cascade will delete related records)
    await client.query(
      `DELETE FROM users WHERE email LIKE '%@bondai-demo.com'`
    );

    console.log('✅ Cleaned existing seed data');

  } catch (error) {
    console.error('Error cleaning seed data:', error);
    throw error;
  } finally {
    client.release();
  }
}
