/**
 * Seed 1000 users with realistic data
 * Includes diverse profiles, connections, and relationships
 */

import { Pool } from 'pg';
import bcrypt from 'bcrypt';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost:5432/bondai',
});

// Data generators
const FIRST_NAMES = [
  'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth',
  'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen',
  'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
  'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
  'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn',
  'Liam', 'Noah', 'Oliver', 'Elijah', 'William', 'James', 'Benjamin', 'Lucas', 'Henry', 'Alexander',
  'Aiden', 'Jackson', 'Sebastian', 'Jack', 'Owen', 'Samuel', 'Matthew', 'Joseph', 'Levi', 'Mateo',
  'Yuki', 'Hiro', 'Kenji', 'Sakura', 'Wei', 'Li', 'Chen', 'Ahmed', 'Fatima', 'Mohammed',
  'Rajesh', 'Priya', 'Sanjay', 'Ananya', 'Carlos', 'Maria', 'Jose', 'Ana', 'Luis', 'Sofia'
];

const LAST_NAMES = [
  'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
  'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
  'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
  'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
  'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
  'Yamamoto', 'Suzuki', 'Tanaka', 'Watanabe', 'Wang', 'Zhang', 'Liu', 'Chen', 'Khan', 'Ali',
  'Patel', 'Kumar', 'Singh', 'Sharma', 'Fernandez', 'Silva', 'Santos', 'Oliveira', 'Costa', 'Rodrigues'
];

const INDUSTRIES = [
  'Technology', 'Finance', 'Healthcare', 'Education', 'Retail', 'Manufacturing',
  'Consulting', 'Marketing', 'Real Estate', 'Legal', 'Media', 'Entertainment',
  'Non-profit', 'Government', 'Energy', 'Transportation', 'Hospitality',
  'Telecommunications', 'Agriculture', 'Construction', 'Automotive', 'Aerospace',
  'Biotechnology', 'Pharmaceuticals', 'E-commerce', 'Gaming', 'Sports',
  'Fashion', 'Food & Beverage', 'Insurance', 'Investment Banking', 'Venture Capital'
];

const JOB_TITLES = [
  'Software Engineer', 'Product Manager', 'Data Scientist', 'UX Designer', 'CEO',
  'CTO', 'CFO', 'VP of Engineering', 'Marketing Manager', 'Sales Director',
  'Business Analyst', 'Consultant', 'Researcher', 'Professor', 'Founder',
  'Co-founder', 'Director of Operations', 'HR Manager', 'Legal Counsel',
  'Investment Analyst', 'Venture Partner', 'Growth Manager', 'DevOps Engineer',
  'ML Engineer', 'Design Lead', 'Content Strategist', 'Account Executive',
  'Customer Success Manager', 'Strategy Consultant', 'Creative Director'
];

const COMPANIES = [
  'Google', 'Apple', 'Microsoft', 'Amazon', 'Meta', 'Tesla', 'Netflix', 'Adobe',
  'Salesforce', 'Oracle', 'IBM', 'Intel', 'Nvidia', 'PayPal', 'Uber', 'Airbnb',
  'Spotify', 'Twitter', 'LinkedIn', 'Dropbox', 'Zoom', 'Slack', 'Stripe',
  'McKinsey', 'BCG', 'Bain', 'Deloitte', 'PwC', 'EY', 'KPMG',
  'Goldman Sachs', 'JP Morgan', 'Morgan Stanley', 'Sequoia Capital', 'a16z',
  'Y Combinator', 'TechStars', 'Stanford University', 'MIT', 'Harvard'
];

const CITIES = [
  { city: 'San Francisco', country: 'USA', lat: 37.7749, lng: -122.4194 },
  { city: 'New York', country: 'USA', lat: 40.7128, lng: -74.0060 },
  { city: 'London', country: 'UK', lat: 51.5074, lng: -0.1278 },
  { city: 'Berlin', country: 'Germany', lat: 52.5200, lng: 13.4050 },
  { city: 'Paris', country: 'France', lat: 48.8566, lng: 2.3522 },
  { city: 'Tokyo', country: 'Japan', lat: 35.6762, lng: 139.6503 },
  { city: 'Singapore', country: 'Singapore', lat: 1.3521, lng: 103.8198 },
  { city: 'Sydney', country: 'Australia', lat: -33.8688, lng: 151.2093 },
  { city: 'Toronto', country: 'Canada', lat: 43.6532, lng: -79.3832 },
  { city: 'Amsterdam', country: 'Netherlands', lat: 52.3676, lng: 4.9041 },
  { city: 'Stockholm', country: 'Sweden', lat: 59.3293, lng: 18.0686 },
  { city: 'Tel Aviv', country: 'Israel', lat: 32.0853, lng: 34.7818 },
  { city: 'Bangalore', country: 'India', lat: 12.9716, lng: 77.5946 },
  { city: 'Shanghai', country: 'China', lat: 31.2304, lng: 121.4737 },
  { city: 'São Paulo', country: 'Brazil', lat: -23.5505, lng: -46.6333 },
  { city: 'Dubai', country: 'UAE', lat: 25.2048, lng: 55.2708 },
  { city: 'Austin', country: 'USA', lat: 30.2672, lng: -97.7431 },
  { city: 'Seattle', country: 'USA', lat: 47.6062, lng: -122.3321 },
  { city: 'Boston', country: 'USA', lat: 42.3601, lng: -71.0589 },
  { city: 'Los Angeles', country: 'USA', lat: 34.0522, lng: -118.2437 }
];

const EXPERTISE_AREAS = [
  'JavaScript', 'Python', 'Java', 'C++', 'Go', 'Rust', 'TypeScript',
  'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring Boot',
  'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision', 'AI',
  'Data Science', 'Data Engineering', 'Big Data', 'Analytics',
  'Cloud Architecture', 'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
  'DevOps', 'CI/CD', 'Microservices', 'System Design', 'Distributed Systems',
  'Product Management', 'Agile', 'Scrum', 'Product Strategy',
  'UX Design', 'UI Design', 'Design Systems', 'User Research',
  'Digital Marketing', 'SEO', 'Content Marketing', 'Growth Hacking',
  'Sales', 'Business Development', 'Partnerships', 'Fundraising',
  'Financial Modeling', 'Investment Analysis', 'M&A', 'Corporate Strategy',
  'Leadership', 'Team Building', 'Hiring', 'Mentorship', 'Public Speaking'
];

const NEEDS = [
  'Co-founder', 'Technical Co-founder', 'Funding', 'Seed Funding', 'Series A',
  'Angel Investors', 'Mentorship', 'Advisors', 'Board Members',
  'Engineering Talent', 'Product Managers', 'Designers', 'Marketing Help',
  'Business Development', 'Strategic Partnerships', 'Customers', 'Beta Testers',
  'Market Research', 'Industry Insights', 'Introductions', 'Networking',
  'Legal Advice', 'Accounting Help', 'Office Space', 'Growth Strategy',
  'Technical Architecture', 'Scaling Help', 'Internationalization', 'Acquisition Targets'
];

const OFFERS = [
  'Mentorship', 'Introductions', 'Investment', 'Advisory', 'Technical Expertise',
  'Product Strategy', 'Go-to-Market Strategy', 'Fundraising Help', 'Recruiting Help',
  'Marketing Expertise', 'Sales Expertise', 'Design Help', 'Legal Guidance',
  'Industry Connections', 'Customer Introductions', 'Partnership Opportunities',
  'Office Space', 'Technical Infrastructure', 'Beta Testing', 'Feedback',
  'Public Speaking', 'Content Creation', 'Social Media Promotion', 'Press Connections',
  'Board Membership', 'Strategic Advice', 'International Expansion', 'M&A Advice'
];

// Helper functions
function random<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function randomSubset<T>(array: T[], min: number, max: number): T[] {
  const count = randomInt(min, max);
  const shuffled = [...array].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

function generateEmail(firstName: string, lastName: string): string {
  const domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com', 'icloud.com'];
  return `${firstName.toLowerCase()}.${lastName.toLowerCase()}@${random(domains)}`;
}

function generateBio(name: string, title: string, company: string, expertise: string[]): string {
  const templates = [
    `${title} at ${company}. Passionate about ${expertise.slice(0, 3).join(', ')}. Always happy to help and connect.`,
    `Experienced ${title} with ${randomInt(5, 20)} years in ${random(INDUSTRIES)}. Expert in ${expertise.slice(0, 2).join(' and ')}. Looking to connect with like-minded professionals.`,
    `Building the future at ${company}. Specializing in ${expertise[0]}. Open to collaborations and partnerships.`,
    `${title} | ${company} | ${expertise.slice(0, 2).join(', ')} enthusiast. Let's connect!`,
    `Helping companies scale through ${expertise[0]} and ${expertise[1]}. Currently at ${company}. Always learning, always connecting.`
  ];
  return random(templates);
}

async function main() {
  console.log('🚀 Starting seed process for 1000 users...\n');

  const client = await pool.connect();

  try {
    await client.query('BEGIN');

    // Generate 1000 users
    console.log('👥 Creating 1000 users...');
    const userIds: string[] = [];
    const passwordHash = await bcrypt.hash('password123', 10);

    for (let i = 0; i < 1000; i++) {
      const firstName = random(FIRST_NAMES);
      const lastName = random(LAST_NAMES);
      const email = `user${i}@bondai.test`; // Use numbered emails for uniqueness
      const name = `${firstName} ${lastName}`;
      const industry = random(INDUSTRIES);

      const userResult = await client.query(
        `INSERT INTO users (email, name, password_hash, industry, verified)
         VALUES ($1, $2, $3, $4, true)
         RETURNING id`,
        [email, name, passwordHash, industry]
      );

      userIds.push(userResult.rows[0].id);

      if ((i + 1) % 100 === 0) {
        console.log(`  ✓ Created ${i + 1} users`);
      }
    }

    console.log(`✅ Created ${userIds.length} users\n`);

    // Create user profiles
    console.log('📝 Creating user profiles...');
    for (let i = 0; i < userIds.length; i++) {
      const userId = userIds[i];
      const jobTitle = random(JOB_TITLES);
      const company = random(COMPANIES);
      const location = random(CITIES);
      const expertise = randomSubset(EXPERTISE_AREAS, 3, 8);
      const needs = randomSubset(NEEDS, 1, 5);
      const offers = randomSubset(OFFERS, 1, 5);
      const yearsExperience = randomInt(1, 25);

      // Get user name for bio
      const userResult = await client.query('SELECT name FROM users WHERE id = $1', [userId]);
      const name = userResult.rows[0].name;
      const bio = generateBio(name, jobTitle, company, expertise);

      await client.query(
        `INSERT INTO user_profiles
         (user_id, bio, job_title, company, location, expertise_areas, needs, offers, years_experience)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
        [
          userId,
          bio,
          jobTitle,
          company,
          JSON.stringify(location),
          expertise,
          needs,
          offers,
          yearsExperience
        ]
      );

      if ((i + 1) % 100 === 0) {
        console.log(`  ✓ Created ${i + 1} profiles`);
      }
    }

    console.log(`✅ Created ${userIds.length} profiles\n`);

    // Create connections (average 15 connections per user, range 3-50)
    console.log('🔗 Creating connections...');
    let totalConnections = 0;

    for (let i = 0; i < userIds.length; i++) {
      const userId = userIds[i];

      // Determine connection strategy
      let connectionCount: number;
      const rand = Math.random();

      if (rand < 0.05) {
        // 5% are super connectors (50-100 connections)
        connectionCount = randomInt(50, 100);
      } else if (rand < 0.15) {
        // 10% are isolated (0-3 connections)
        connectionCount = randomInt(0, 3);
      } else if (rand < 0.30) {
        // 15% are selective (3-8 connections)
        connectionCount = randomInt(3, 8);
      } else {
        // 70% are normal (8-30 connections)
        connectionCount = randomInt(8, 30);
      }

      // Select random users to connect with
      const potentialConnections = userIds.filter(id => id !== userId);
      const connectionsToMake = Math.min(connectionCount, potentialConnections.length);
      const selectedConnections = randomSubset(potentialConnections, connectionsToMake, connectionsToMake);

      for (const targetId of selectedConnections) {
        // Create contact first
        const targetUser = await client.query(
          'SELECT name, email FROM users WHERE id = $1',
          [targetId]
        );

        const contactResult = await client.query(
          `INSERT INTO contacts (user_id, email, name, source)
           VALUES ($1, $2, $3, 'internal')
           RETURNING id`,
          [userId, targetUser.rows[0].email, targetUser.rows[0].name]
        );

        // Create connection with varying strength and trust
        const strength = Math.random() * 0.5 + 0.3; // 0.3 to 0.8
        const trustLevel = Math.random() * 0.6 + 0.3; // 0.3 to 0.9
        const interactionCount = randomInt(1, 50);
        const daysSinceInteraction = randomInt(1, 180);
        const lastInteraction = new Date();
        lastInteraction.setDate(lastInteraction.getDate() - daysSinceInteraction);

        await client.query(
          `INSERT INTO connections
           (user_id, contact_id, strength, trust_level, interaction_count, last_interaction)
           VALUES ($1, $2, $3, $4, $5, $6)`,
          [userId, contactResult.rows[0].id, strength, trustLevel, interactionCount, lastInteraction]
        );

        totalConnections++;
      }

      if ((i + 1) % 100 === 0) {
        console.log(`  ✓ Created connections for ${i + 1} users (${totalConnections} total connections)`);
      }
    }

    console.log(`✅ Created ${totalConnections} connections\n`);

    // Create some opportunities
    console.log('💡 Creating opportunities...');
    const opportunityTypes = ['collaboration', 'introduction', 'hiring', 'investment', 'knowledge_exchange'];
    let totalOpportunities = 0;

    for (let i = 0; i < userIds.length; i++) {
      if (Math.random() < 0.3) { // 30% of users have opportunities
        const userId = userIds[i];
        const oppCount = randomInt(1, 3);

        for (let j = 0; j < oppCount; j++) {
          const type = random(opportunityTypes);
          const score = randomInt(60, 95);
          const confidence = (Math.random() * 0.4 + 0.6).toFixed(2); // 0.6 to 1.0

          await client.query(
            `INSERT INTO opportunities
             (user_id, type, title, description, score, confidence, status)
             VALUES ($1, $2, $3, $4, $5, $6, 'active')`,
            [
              userId,
              type,
              `${type.charAt(0).toUpperCase() + type.slice(1)} opportunity`,
              `Great opportunity for ${type}`,
              score,
              confidence
            ]
          );

          totalOpportunities++;
        }
      }
    }

    console.log(`✅ Created ${totalOpportunities} opportunities\n`);

    // Create some network snapshots
    console.log('📊 Creating network snapshots...');
    let totalSnapshots = 0;

    for (let i = 0; i < Math.min(100, userIds.length); i++) {
      const userId = userIds[i];

      // Create snapshots for the last 30 days
      for (let day = 30; day >= 0; day -= 7) {
        const timestamp = new Date();
        timestamp.setDate(timestamp.getDate() - day);

        await client.query(
          `INSERT INTO network_snapshots
           (user_id, timestamp, total_connections, avg_trust_level, degree_centrality,
            betweenness_centrality, page_rank, clustering_coefficient, community_count, network_density)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
          [
            userId,
            timestamp,
            randomInt(5, 50),
            (Math.random() * 0.4 + 0.5).toFixed(2),
            (Math.random() * 0.3 + 0.1).toFixed(4),
            (Math.random() * 0.3 + 0.1).toFixed(4),
            (Math.random() * 0.3 + 0.1).toFixed(4),
            (Math.random() * 0.4 + 0.3).toFixed(4),
            randomInt(1, 5),
            (Math.random() * 0.3 + 0.2).toFixed(4)
          ]
        );

        totalSnapshots++;
      }
    }

    console.log(`✅ Created ${totalSnapshots} network snapshots\n`);

    await client.query('COMMIT');

    console.log('🎉 Seed completed successfully!\n');
    console.log('Summary:');
    console.log(`  Users: ${userIds.length}`);
    console.log(`  Profiles: ${userIds.length}`);
    console.log(`  Connections: ${totalConnections}`);
    console.log(`  Opportunities: ${totalOpportunities}`);
    console.log(`  Network Snapshots: ${totalSnapshots}`);
    console.log(`  Average connections per user: ${(totalConnections / userIds.length).toFixed(1)}`);

  } catch (error) {
    await client.query('ROLLBACK');
    console.error('❌ Error during seed:', error);
    throw error;
  } finally {
    client.release();
    await pool.end();
  }
}

main().catch(console.error);
