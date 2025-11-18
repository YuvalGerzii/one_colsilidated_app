# Bond.AI Platform Demo Guide

This guide will help you run the comprehensive Bond.AI platform demonstration with 50 diverse users.

## Prerequisites

Before running the demo, ensure you have the following installed and running:

1. **PostgreSQL** (v14+) with extensions:
   - `pg_trgm` (Trigram matching for fuzzy search)
   - `vector` (pgvector for semantic search)

2. **Redis** (v6+)

3. **Node.js** (v18+)

4. **npm** or **yarn**

## Quick Start

### 1. Install Dependencies

```bash
# Install server dependencies
cd bond.ai
npm install

# Install script dependencies
cd scripts
npm install
```

### 2. Configure Environment

Create a `.env` file in the `bond.ai` directory:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bondai
DB_USER=postgres
DB_PASSWORD=your_password

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# API Configuration
API_URL=http://localhost:3005
PORT=3000

# Security
JWT_SECRET=your_jwt_secret_here
CORS_ORIGIN=http://localhost:3001

# Environment
NODE_ENV=development
```

### 3. Initialize Database

```bash
# Run database migrations
cd bond.ai
npm run migrate

# Or manually run the migration files in order:
psql -U postgres -d bondai -f server/database/migrations/001_initial_schema.sql
psql -U postgres -d bondai -f server/database/migrations/002_smart_filters.sql
psql -U postgres -d bondai -f server/database/migrations/003_dynamic_profile.sql
psql -U postgres -d bondai -f server/database/migrations/004_messaging.sql
psql -U postgres -d bondai -f server/database/migrations/005_advanced_search.sql
```

### 4. Run Health Check

Before running the demo, verify all systems are operational:

```bash
cd scripts
npm run health
```

This will check:
- ✅ PostgreSQL connectivity
- ✅ All required tables exist
- ✅ PostgreSQL extensions installed (pg_trgm, vector)
- ✅ Redis connectivity and read/write
- ✅ API server status

Expected output:
```
============================================================
Bond.AI Health Check
============================================================

Checking PostgreSQL...
✓ PostgreSQL connected
  ✓ Table 'users' exists
  ✓ Table 'user_profiles' exists
  ...

Checking PostgreSQL Extensions...
  ✓ Extension 'pg_trgm' installed
  ✓ Extension 'vector' installed

Checking Redis...
✓ Redis connected
  ✓ Redis read/write working

Checking API Server...
✓ API server responding
  Status: ok
  Database: OK
  Redis: OK

============================================================
Health Check Summary
============================================================

✅ All checks passed! System is healthy.
```

### 5. Run the Demo

```bash
cd scripts
npm run demo
```

## What the Demo Does

The demo script performs a comprehensive end-to-end demonstration:

### Step 1: Seed Database (50 Users)
- Creates 50 diverse users across:
  - 15 different industries
  - 15 global cities
  - 20 expertise areas
- Each user has:
  - 2-4 areas of expertise
  - 1-3 needs (with varying priority and urgency)
  - 1-3 offerings (with varying capacity)
  - Realistic bio and profile

### Step 2: Network Connections
- Creates 5-15 connections per user
- Varying trust levels (0.4-0.9)
- Different degrees of separation (1-3)
- ~400-750 total connections

### Step 3: Intelligent Matching
- Runs matching algorithm for first 10 users
- Finds compatible partners based on:
  - Need-offering alignment
  - Network proximity
  - Industry compatibility
  - Expertise match
- Stores top 5 matches per user in database

### Step 4: AI-Powered Insights
For each match, generates:
- **Match Explanation**: Why they're compatible
  - Primary alignment factors
  - Network strength analysis
  - Industry synergies
  - Behavioral compatibility

- **Success Prediction**: Probability of successful collaboration
  - 7-factor analysis
  - Confidence intervals
  - Risk assessment
  - Actionable recommendations

- **Personalized Introduction**: AI-written message
  - Professional, friendly, casual, or formal tone
  - Highlights key synergies
  - Suggests collaboration opportunities

### Step 5: Start Negotiations
- Initiates 5 automated negotiations
- Uses multi-agent strategies:
  - Tit-for-Tat with Forgiveness
  - Cooperative Multi-Agent
  - Adaptive Reinforcement Learning
- Tracks conversation history

### Step 6: Create Conversations
- Creates 3 introduction conversations
- Sends personalized introduction messages
- Demonstrates messaging system

### Step 7: Analytics Dashboard
Shows comprehensive metrics:
- Total matches found
- Active negotiations
- Network size
- Average match score
- Matches by type
- Engagement statistics

## Demo Output

Expected console output includes:

```
🚀 BOND.AI PLATFORM DEMO
================================================================================

Step 1: Seeding Database with 50 Users
================================================================================

Generated 50 diverse users
✓ Created 50 users in database
✓ Created network connections

Step 2: Running Intelligent Matching
================================================================================

Finding matches for Alice Anderson...
  Found 8 potential matches
  Top match: Bob Brown (87.5% compatible)

Finding matches for Carol Chen...
  Found 12 potential matches
  Top match: David Davis (92.1% compatible)

...

✓ Created 45 high-quality matches

Step 3: AI-Powered Insights
================================================================================

Analyzing match: Alice Anderson ↔ Bob Brown
  Primary reasons: 3
    - Need-Offering Alignment: Perfect match between funding need and capital offering
  Success probability: 87.5%
  Confidence: 0.82 - 0.93
  Recommendation: Introduce immediately with focus on mutual value creation
  Generated introduction: "Strategic Partnership Opportunity in Technology Sector"

...

Step 4: Starting Automated Negotiations
================================================================================

Starting negotiation: Alice Anderson ↔ Bob Brown
  ✓ Started negotiation 1

...

✓ Started 5 negotiations

Step 5: Creating Conversations
================================================================================

Created conversation: Alice Anderson → Bob Brown
Created conversation: Carol Chen → David Davis
Created conversation: Emma Evans → Frank Fischer

✓ Created 3 conversations

Step 6: Platform Analytics
================================================================================

Dashboard Metrics:
  Total Matches: 45
  Active Negotiations: 5
  Network Size: 15
  Average Match Score: 78.3%

  Matches by Type:
    need_offering: 20
    expertise: 15
    industry: 10

📊 Demo Summary
================================================================================

✅ Users Created: 50
✅ Matches Found: 45
✅ Negotiations Started: 5
✅ Conversations Created: 3
✅ Messages Sent: 3
✅ Network Connections: 487

🎉 Demo completed successfully!

You can now:
  1. Login with any demo user (password: Demo@1234)
  2. View matches and insights
  3. Check analytics dashboard
  4. Send messages and start negotiations

Sample login credentials:
  Email: alice.anderson@bondai-demo.com | Password: Demo@1234
  Email: bob.brown@bondai-demo.com | Password: Demo@1234
  Email: carol.chen@bondai-demo.com | Password: Demo@1234
```

## Using Demo Data

After running the demo, you can:

### 1. Login to the Platform

Use any of the 50 demo users:
- Email format: `{firstname}.{lastname}@bondai-demo.com`
- Password: `Demo@1234` (all users)

Examples:
```
alice.anderson@bondai-demo.com
bob.brown@bondai-demo.com
carol.chen@bondai-demo.com
```

### 2. Explore Features

**View Matches:**
```bash
GET /api/matching/matches
Authorization: Bearer {token}
```

**View Match Explanation:**
```bash
GET /api/insights/match/{matchId}/explanation
Authorization: Bearer {token}
```

**View Success Prediction:**
```bash
GET /api/insights/match/{matchId}/prediction
Authorization: Bearer {token}
```

**Generate Introduction:**
```bash
GET /api/insights/match/{matchId}/introduction?tone=professional
Authorization: Bearer {token}
```

**View Analytics:**
```bash
GET /api/analytics/dashboard?timeRange=30d
Authorization: Bearer {token}
```

### 3. Clean Demo Data

To remove all demo users and start fresh:

```bash
cd scripts
npm run clean
```

This will delete all users with `@bondai-demo.com` email addresses.

## Troubleshooting

### Database Connection Error

```
✗ PostgreSQL error: connect ECONNREFUSED
```

**Solution:**
- Ensure PostgreSQL is running: `sudo service postgresql start`
- Check connection settings in `.env`
- Verify database exists: `psql -U postgres -l | grep bondai`

### Missing Tables

```
✗ Table 'users' missing
```

**Solution:**
- Run migrations: `npm run migrate`
- Or manually run migration SQL files

### Missing Extensions

```
✗ Extension 'pg_trgm' missing
```

**Solution:**
```sql
-- Connect to database
psql -U postgres -d bondai

-- Install extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS vector;
```

### Redis Connection Error

```
✗ Redis error: connect ECONNREFUSED
```

**Solution:**
- Ensure Redis is running: `sudo service redis-server start`
- Check Redis connection settings in `.env`

### API Server Not Running

```
✗ API server not running
  Start with: npm run dev
```

**Solution:**
```bash
# Terminal 1: Start API server
cd bond.ai
npm run dev

# Terminal 2: Run demo
cd scripts
npm run demo
```

## Advanced Usage

### Customize User Count

Edit `scripts/demo.ts`:

```typescript
// Change from 50 to desired number
const users = generateUsers(100);
```

### Customize Matching Parameters

Edit `scripts/demo.ts`:

```typescript
const matchingEngine = new MatchingEngine({
  maxDegreeOfSeparation: 3,  // Change network depth
  minRelationshipStrength: 0.3,  // Minimum trust level
  minCompatibilityScore: 0.6,  // Minimum match score
  enabledMatchTypes: ['all'],  // Or specific types
  priorityWeights: {
    valuePotential: 0.35,  // Adjust weight distribution
    successProbability: 0.25,
    trustLevel: 0.25,
    timing: 0.15
  }
});
```

### Run Only Specific Steps

Create custom scripts:

```typescript
// seed-only.ts
import { generateUsers, seedUsers, cleanSeedData } from '../server/utils/seedData';

async function seedOnly() {
  await cleanSeedData(pool);
  const users = generateUsers(50);
  await seedUsers(pool, users);
}
```

## Performance Considerations

- **Database**: Matching queries can be intensive with many users
- **Redis**: Cache hit rate improves with repeated queries
- **API Server**: WebSocket connections scale horizontally
- **Search**: Reindexing happens async, non-blocking

## Next Steps

After running the demo:

1. **Explore the API**: Try different endpoints
2. **View Database**: Inspect generated data
3. **Test Features**: Try matching, messaging, analytics
4. **Scale Up**: Run with 100+ users
5. **Customize**: Modify matching algorithms, add strategies

## Support

For issues or questions:
- Check health status: `npm run health`
- View logs: Check console output
- Database queries: Use `psql` to inspect data
- API testing: Use Postman or curl

## Related Documentation

- [NEW_FEATURES.md](./NEW_FEATURES.md) - Features 1-5 documentation
- [IMPROVEMENTS.md](./IMPROVEMENTS.md) - AI-powered features documentation
- [API.md](./API.md) - Complete API reference
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
