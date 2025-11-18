# Bond.AI Setup Guide

Complete guide to setting up and running Bond.AI locally and in production.

## 📋 Prerequisites

### Required Software

1. **Node.js** >= 18.0.0
   ```bash
   node --version  # Should be >= 18.0.0
   ```

2. **PostgreSQL** >= 14
   ```bash
   psql --version  # Should be >= 14
   ```

3. **Redis** >= 7
   ```bash
   redis-cli --version  # Should be >= 7
   ```

4. **Ollama** (for local LLM)
   ```bash
   # Install from https://ollama.ai
   ollama --version
   ```

5. **Docker & Docker Compose** (optional, for containerized setup)
   ```bash
   docker --version
   docker-compose --version
   ```

---

## 🚀 Quick Start (Docker - Recommended)

### Step 1: Clone Repository

```bash
cd bond.ai
```

### Step 2: Setup Environment

```bash
cp server/.env.example server/.env
# Edit server/.env with your configuration
```

### Step 3: Start Services

```bash
# Start all services (PostgreSQL, Redis, Ollama, API)
docker-compose up -d

# View logs
docker-compose logs -f api
```

### Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec api npm run migrate

# Optional: Seed test data
docker-compose exec api npm run seed
```

### Step 5: Pull Ollama Model

```bash
# Pull LLaMA 2 model (recommended for local development)
docker-compose exec ollama ollama pull llama2

# Or pull a smaller model (faster, less accurate)
docker-compose exec ollama ollama pull tinyllama

# Or pull a larger model (slower, more accurate)
docker-compose exec ollama ollama pull mistral
```

### Step 6: Access API

```
🚀 API Server: http://localhost:3005
📊 Health Check: http://localhost:3005/health
📚 API Docs: http://localhost:3005/api-docs (if enabled)
```

---

## 🛠️ Manual Setup (Without Docker)

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

### Step 2: Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE bondai;
CREATE USER bondai_user WITH PASSWORD 'bondai_password';
GRANT ALL PRIVILEGES ON DATABASE bondai TO bondai_user;

# Optional: Enable pg_vector extension
\c bondai
CREATE EXTENSION IF NOT EXISTS vector;
\q
```

### Step 3: Run Schema

```bash
psql -U bondai_user -d bondai -f server/database/schema.sql
```

### Step 4: Install Redis

**macOS:**
```bash
brew install redis
brew services start redis
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**Windows:**
Download from https://redis.io/download

### Step 5: Install Ollama

```bash
# macOS/Linux
curl https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull a model
ollama pull llama2
```

### Step 6: Install Node Dependencies

```bash
cd server
npm install
```

### Step 7: Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 8: Start Development Server

```bash
# Development mode with hot reload
npm run dev

# Or build and run production
npm run build
npm start
```

---

## 🔧 Configuration

### Environment Variables

Edit `server/.env`:

```bash
# Server
PORT=3000
NODE_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bondai
DB_USER=bondai_user
DB_PASSWORD=bondai_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-super-secret-key  # CHANGE THIS!

# Ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# LinkedIn OAuth
LINKEDIN_CLIENT_ID=your-client-id
LINKEDIN_CLIENT_SECRET=your-client-secret
LINKEDIN_REDIRECT_URI=http://localhost:3005/api/linkedin/callback
```

### LinkedIn OAuth Setup

1. Go to https://www.linkedin.com/developers/apps
2. Create new app
3. Set redirect URI to `http://localhost:3005/api/linkedin/callback`
4. Copy Client ID and Secret to `.env`

---

## 📦 Project Structure

```
bond.ai/
├── server/                          # API Server
│   ├── database/                    # Database schemas and migrations
│   │   ├── schema.sql              # PostgreSQL schema
│   │   └── connection.ts           # DB connection manager
│   ├── auth/                        # Authentication
│   │   └── jwt.ts                  # JWT helpers
│   ├── routes/                      # API routes
│   │   ├── auth.ts                 # Auth endpoints
│   │   ├── users.ts                # User management
│   │   ├── matching.ts             # Matching endpoints
│   │   ├── negotiations.ts         # Negotiation endpoints
│   │   └── linkedin.ts             # LinkedIn OAuth
│   ├── services/                    # Business logic
│   │   ├── SemanticMatcher.ts      # NLP matching
│   │   ├── RLAgent.ts              # Reinforcement learning
│   │   ├── NotificationService.ts  # Real-time notifications
│   │   ├── LLMService.ts           # Ollama LLM integration
│   │   └── LinkedInService.ts      # LinkedIn integration
│   ├── index.ts                     # Server entry point
│   ├── package.json                # Dependencies
│   └── tsconfig.json               # TypeScript config
├── src/                             # Core Bond.AI library
│   ├── agents/                     # Agent-based matching
│   ├── network/                    # Network mapping
│   ├── intelligence/               # Intelligence engine
│   ├── matching/                   # Traditional matching
│   └── activation/                 # Introduction facilitation
├── examples/                        # Example scripts
├── docker-compose.yml              # Docker setup
└── .github/workflows/ci.yml        # CI/CD pipeline
```

---

## 🧪 Testing

### Run All Tests

```bash
cd server
npm test
```

### Run Tests with Coverage

```bash
npm test -- --coverage
```

### Run Specific Test File

```bash
npm test -- auth.test.ts
```

### Watch Mode

```bash
npm run test:watch
```

---

## 📊 Database Management

### Migrations

```bash
# Create new migration
npm run migrate:create <migration_name>

# Run migrations
npm run migrate

# Rollback last migration
npm run migrate:rollback
```

### Seed Data

```bash
# Seed test data
npm run seed
```

### Backup Database

```bash
# Backup
pg_dump -U bondai_user bondai > backup.sql

# Restore
psql -U bondai_user -d bondai < backup.sql
```

---

## 🔍 Monitoring & Debugging

### View Logs

**Docker:**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f postgres
docker-compose logs -f redis
```

**Manual:**
```bash
# Server logs
cd server && npm run dev

# PostgreSQL logs
tail -f /usr/local/var/log/postgres.log  # macOS
sudo tail -f /var/log/postgresql/postgresql-15-main.log  # Ubuntu

# Redis logs
redis-cli MONITOR
```

### Health Checks

```bash
# API Health
curl http://localhost:3005/health

# Database
psql -U bondai_user -d bondai -c "SELECT 1"

# Redis
redis-cli ping

# Ollama
curl http://localhost:11434/api/tags
```

### Performance Monitoring

```bash
# Database connections
SELECT count(*) FROM pg_stat_activity WHERE datname = 'bondai';

# Redis info
redis-cli INFO

# API metrics (if implemented)
curl http://localhost:3005/metrics
```

---

## 🚀 Deployment

### Environment Setup

1. **Production Database**
   - Use managed PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
   - Enable SSL connections
   - Set up automated backups
   - Configure connection pooling

2. **Production Redis**
   - Use managed Redis (AWS ElastiCache, Redis Cloud, etc.)
   - Enable persistence
   - Set up replication

3. **Environment Variables**
   ```bash
   NODE_ENV=production
   JWT_SECRET=<strong-random-secret>
   DB_SSL=true
   # ... other production configs
   ```

### Deployment Options

#### Option 1: Docker + Cloud Provider

```bash
# Build production image
docker build -t bondai/api:latest ./server

# Push to registry
docker push bondai/api:latest

# Deploy to cloud (AWS ECS, Google Cloud Run, etc.)
```

#### Option 2: Platform-as-a-Service

**Railway.app:**
```bash
npm install -g railway
railway login
railway up
```

**Heroku:**
```bash
heroku create bondai-api
git push heroku main
```

**Render:**
- Connect GitHub repo
- Configure build command: `cd server && npm install && npm run build`
- Configure start command: `cd server && npm start`

#### Option 3: Manual VPS Deployment

```bash
# SSH into server
ssh user@your-server.com

# Clone repository
git clone <your-repo>
cd bond.ai/server

# Install dependencies
npm install --production

# Build
npm run build

# Start with PM2
npm install -g pm2
pm2 start dist/index.js --name bondai-api

# Save PM2 config
pm2 save
pm2 startup
```

---

## 🔒 Security Checklist

- [ ] Change default JWT secret
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up CORS properly
- [ ] Enable Helmet security headers
- [ ] Implement request validation
- [ ] Set up logging and monitoring
- [ ] Regular security audits (`npm audit`)
- [ ] Keep dependencies updated
- [ ] Implement API authentication
- [ ] Use prepared statements (SQL injection protection)
- [ ] Sanitize user inputs
- [ ] Implement CSRF protection

---

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
ps aux | grep postgres

# Check port
lsof -i :5432

# Test connection
psql -U bondai_user -d bondai -h localhost
```

### Redis Connection Issues

```bash
# Check Redis is running
ps aux | grep redis

# Test connection
redis-cli ping
```

### Ollama Issues

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Pull model again
ollama pull llama2

# Check model list
ollama list
```

### Port Already in Use

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

### NPM Install Errors

```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Additional Resources

- **Documentation:** See ROADMAP.md for feature development plans
- **Agent System:** See AGENT_MATCHING_GUIDE.md for agent-based matching
- **API Reference:** See API.md (if available) for API documentation
- **Contributing:** See CONTRIBUTING.md for contribution guidelines

---

## 💡 Next Steps

1. **Explore Examples:**
   ```bash
   # Run basic example
   npm run example:basic

   # Run agent-to-agent matching
   npm run example:agent-matching
   ```

2. **Build Your First Integration:**
   - Register a user via API
   - Import LinkedIn contacts
   - Run agent-based matching
   - Create introductions

3. **Customize:**
   - Add custom domain matchers
   - Implement additional OAuth providers
   - Build frontend application
   - Add custom analytics

---

## 🆘 Support

- **Issues:** https://github.com/yourusername/bond.ai/issues
- **Discussions:** https://github.com/yourusername/bond.ai/discussions
- **Discord:** [Your Discord server]
- **Email:** support@bond.ai

---

**Happy Building! 🚀**
