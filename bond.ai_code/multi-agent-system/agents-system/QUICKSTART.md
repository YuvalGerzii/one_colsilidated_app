# Quick Start Guide

Get the Agents System up and running in 5 minutes.

## Prerequisites

Ensure you have installed:
- Node.js 18+ (`node --version`)
- PostgreSQL 14+ (`psql --version`)
- Redis 6+ (`redis-cli --version`)

## Step 1: Install Dependencies

```bash
cd agents-system
npm install
```

## Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
# Minimal required configuration
DB_NAME=agents_system
DB_USER=agents_user
DB_PASSWORD=your_secure_password
JWT_SECRET=your_random_secret_key_at_least_32_characters
```

## Step 3: Set Up Database

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL shell:
CREATE DATABASE agents_system;
CREATE USER agents_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE agents_system TO agents_user;
\q
```

### Run Migrations

```bash
chmod +x scripts/migrate.sh
./scripts/migrate.sh
```

Or manually:
```bash
psql -U agents_user -d agents_system -f database/migrations/001_initial_schema.sql
```

## Step 4: Start Redis

```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis

# Or run manually
redis-server
```

## Step 5: Start the Server

```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm run build
npm start
```

Server will be available at: `http://localhost:4000`

## Step 6: Test the API

### Register a User

```bash
curl -X POST http://localhost:4000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "fullName": "Test User"
  }'
```

Save the `token` from the response.

### Get All Agents

```bash
curl http://localhost:4000/api/agents
```

### Create a Conversation

```bash
curl -X POST http://localhost:4000/api/chatbot/conversations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "Test Conversation",
    "contextType": "individual",
    "selectedAgents": ["musk"]
  }'
```

Save the `conversation.id` from the response.

### Ask a Question

```bash
curl -X POST http://localhost:4000/api/chatbot/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "conversationId": "YOUR_CONVERSATION_ID",
    "question": "Should I launch my product now or wait 3 months?",
    "agentKeys": ["musk"],
    "decisionContext": "STRATEGIC_PLANNING"
  }'
```

## Available Endpoints

- **Health Check**: `GET /health`
- **List Agents**: `GET /api/agents`
- **List Board Rooms**: `GET /api/boardrooms`
- **Register**: `POST /api/auth/register`
- **Login**: `POST /api/auth/login`
- **Create Conversation**: `POST /api/chatbot/conversations`
- **Ask Question**: `POST /api/chatbot/ask`

Full API documentation in [README.md](./README.md)

## Troubleshooting

### Database Connection Failed

- Check PostgreSQL is running: `pg_isready`
- Verify credentials in `.env`
- Test connection: `psql -U agents_user -d agents_system`

### Redis Connection Failed

- Check Redis is running: `redis-cli ping`
- Should return `PONG`
- Verify Redis host/port in `.env`

### Port Already in Use

Change port in `.env`:
```env
PORT=4001
```

### Migration Errors

- Ensure database exists and user has privileges
- Check migration file path is correct
- Run migration manually to see detailed errors

## Next Steps

1. **Frontend Integration**: Build a React/Vue frontend using the API
2. **Custom Board Rooms**: Create specialized board rooms for your use case
3. **Additional Agents**: Add more business leaders to the system
4. **Production Deployment**: Follow production guide in README.md

## Need Help?

- Full documentation: [README.md](./README.md)
- API reference: Check `/api` endpoints after starting server
- Issues: (your-github-repo-url)/issues
