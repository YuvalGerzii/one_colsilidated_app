# Bond.AI Scripts

Utility scripts for Bond.AI platform development and demonstration.

## Available Scripts

### 🚀 Demo Script

**Purpose**: Comprehensive end-to-end platform demonstration with 50 users

```bash
npm run demo
```

**What it does**:
1. Seeds 50 diverse users with realistic profiles
2. Creates network connections (5-15 per user)
3. Runs intelligent matching algorithm
4. Generates AI insights (explanations, predictions, introductions)
5. Starts automated negotiations
6. Creates conversations
7. Shows analytics dashboard

**Duration**: ~2-3 minutes

**See also**: [DEMO_GUIDE.md](../DEMO_GUIDE.md) for detailed instructions

---

### 🏥 Health Check

**Purpose**: Verify all system components are working

```bash
npm run health
```

**What it checks**:
- PostgreSQL connectivity
- Required tables existence
- PostgreSQL extensions (pg_trgm, vector)
- Redis connectivity and operations
- API server status

**Duration**: ~5-10 seconds

---

### 🌱 Seed Data

**Purpose**: Seed database with users without running full demo

```bash
npm run seed
```

**What it does**:
- Cleans existing seed data
- Creates 50 diverse users
- Creates network connections
- Does NOT run matching or analytics

**Duration**: ~30 seconds

---

### 🧹 Clean Data

**Purpose**: Remove all demo users and related data

```bash
npm run clean
```

**What it does**:
- Deletes all users with `@bondai-demo.com` emails
- Cascades to delete related records (matches, negotiations, messages, etc.)

**Duration**: ~2-3 seconds

**Warning**: This permanently deletes demo data!

---

## Installation

```bash
# From bond.ai/scripts directory
npm install
```

Dependencies:
- `pg` - PostgreSQL client
- `ioredis` - Redis client
- `axios` - HTTP client for API testing
- `dotenv` - Environment variable management
- `bcryptjs` - Password hashing
- `ts-node` - TypeScript execution
- `typescript` - TypeScript compiler

## Configuration

Scripts use environment variables from `bond.ai/.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bondai
DB_USER=postgres
DB_PASSWORD=your_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# API
API_URL=http://localhost:3005
```

## Script Details

### demo.ts

**Location**: `scripts/demo.ts`

**Key Functions**:
- `runDemo()` - Main orchestration function
- Uses matching engine, explanation engine, prediction engine
- Demonstrates complete platform workflow

**Outputs**:
- Colored console output with progress
- Summary statistics
- Sample login credentials

**Error Handling**:
- Catches and logs all errors
- Cleans up connections on exit
- Returns proper exit codes

---

### healthCheck.ts

**Location**: `scripts/healthCheck.ts`

**Key Functions**:
- `checkDatabase()` - PostgreSQL connectivity and tables
- `checkRedis()` - Redis connectivity and operations
- `checkAPI()` - API server health endpoint
- `checkExtensions()` - PostgreSQL extensions

**Exit Codes**:
- `0` - All checks passed
- `1` - One or more checks failed

**Color Coding**:
- 🟢 Green - Success
- 🔴 Red - Error
- 🟡 Yellow - Warning
- 🔵 Cyan - Info

---

### seed.ts

**Location**: `scripts/seed.ts`

**Key Functions**:
- `generateUsers(count)` - Create user data
- `seedUsers(pool, users)` - Insert users into database
- `seedConnections(pool, userIdMap)` - Create network connections
- `cleanSeedData(pool)` - Remove existing demo data

**User Generation**:
- Industries: 15 different industries
- Cities: 15 global cities
- Expertise: 20 different areas
- Needs: 1-3 per user (varying priority/urgency)
- Offerings: 1-3 per user (varying capacity)

**Connection Pattern**:
- Each user connects to 5-15 others
- Trust levels: 0.4-0.9
- Connection strength: 0.3-0.9
- Degrees of separation: 1-3

---

### clean.ts

**Location**: `scripts/clean.ts`

**Key Functions**:
- `cleanSeedData()` - Delete all demo users

**Cascades**:
Deletes related records from:
- `user_profiles`
- `agents`
- `match_candidates`
- `negotiations`
- `conversations`
- `messages`
- `connections`
- `contacts`
- `user_needs`
- `user_offerings`

---

## Usage Examples

### Run full demo
```bash
cd scripts
npm run demo
```

### Check system health before demo
```bash
npm run health && npm run demo
```

### Reset demo data
```bash
npm run clean
npm run seed
```

### Custom user count (edit demo.ts)
```typescript
// Change line 73
const users = generateUsers(100); // Instead of 50
```

### Run with specific environment
```bash
NODE_ENV=production npm run demo
```

## Development

### Add a new script

1. Create new TypeScript file:
```typescript
#!/usr/bin/env ts-node

import { Pool } from 'pg';
import { config } from 'dotenv';

config();

async function myScript() {
  const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432'),
    database: process.env.DB_NAME || 'bondai',
    user: process.env.DB_USER || 'postgres',
    password: process.env.DB_PASSWORD
  });

  try {
    // Your script logic
  } finally {
    await pool.end();
  }
}

if (require.main === module) {
  myScript().catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}

export { myScript };
```

2. Add to `package.json`:
```json
{
  "scripts": {
    "my-script": "ts-node myScript.ts"
  }
}
```

3. Run it:
```bash
npm run my-script
```

### TypeScript Configuration

Scripts use TypeScript with:
- ES2020 target
- CommonJS modules
- Strict type checking
- Source maps for debugging

Configuration in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

## Troubleshooting

### "Cannot find module" error

```bash
# Install dependencies
cd scripts
npm install
```

### "Connection refused" error

```bash
# Check services are running
sudo service postgresql status
sudo service redis-server status

# Check .env configuration
cat ../.env
```

### "Permission denied" error

```bash
# Make scripts executable
chmod +x *.ts
```

### TypeScript compilation errors

```bash
# Reinstall TypeScript
npm install -D typescript ts-node @types/node
```

## Best Practices

1. **Always run health check first**: `npm run health`
2. **Clean before re-seeding**: `npm run clean && npm run seed`
3. **Check environment variables**: Ensure `.env` is configured
4. **Monitor output**: Watch for errors and warnings
5. **Use exit codes**: Scripts return 0 on success, 1 on failure

## Performance

- **Seed**: ~30s for 50 users
- **Demo**: ~2-3 minutes complete workflow
- **Health**: ~5s all checks
- **Clean**: ~2s deletion

Scales linearly with user count.

## Support

For issues:
1. Run health check: `npm run health`
2. Check logs: Console output shows errors
3. Verify database: `psql -U postgres -d bondai`
4. Check Redis: `redis-cli ping`

## Related Documentation

- [../DEMO_GUIDE.md](../DEMO_GUIDE.md) - Complete demo guide
- [../NEW_FEATURES.md](../NEW_FEATURES.md) - Feature documentation
- [../IMPROVEMENTS.md](../IMPROVEMENTS.md) - AI improvements
