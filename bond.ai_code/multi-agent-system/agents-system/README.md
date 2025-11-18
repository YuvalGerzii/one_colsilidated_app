# Agents System - Standalone Behavior Analysis AI

A standalone system featuring AI agents that emulate the thinking patterns, decision-making styles, and strategic approaches of world-renowned business leaders. Users can consult individual agents or leverage "board rooms" where multiple agents collaborate to provide consensus-driven advice.

## Features

- **8 Business Leader Agents**: Elon Musk, Steve Jobs, Mark Zuckerberg, Jeff Bezos, Larry Fink, Donald Trump, Sam Zell, Donald Bren
- **Predefined Board Rooms**: 8 specialized board rooms for different business contexts
- **Custom Board Rooms**: Create your own board rooms with selected agents
- **AI-Powered Conversations**: Natural language chatbot interface
- **Decision Analysis**: Multi-criteria decision analysis with confidence scoring
- **Strategic Guidance**: Action plans, risk assessments, and success predictions
- **User Preferences**: Favorite agents, consultation history, ratings
- **Standalone Infrastructure**: Independent database, authentication, and caching

## Architecture

```
agents-system/
├── src/
│   ├── agents/          # Behavior agent implementations
│   ├── engines/         # Conversation, decision, negotiation engines
│   ├── types/           # TypeScript type definitions
│   └── index.ts         # Main exports
├── server/
│   ├── routes/          # API route handlers
│   ├── middleware/      # Auth, error handling
│   └── index.ts         # Express server
├── database/
│   └── migrations/      # SQL schema migrations
├── config/
│   ├── database.ts      # PostgreSQL configuration
│   └── redis.ts         # Redis configuration
└── package.json
```

## Tech Stack

- **Runtime**: Node.js with TypeScript
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT with bcrypt
- **Security**: Helmet, CORS, rate limiting

## Prerequisites

- Node.js 18+ and npm
- PostgreSQL 14+
- Redis 6+

## Installation

### 1. Clone and Install Dependencies

```bash
cd agents-system
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Server
PORT=4000
NODE_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agents_system
DB_USER=agents_user
DB_PASSWORD=your_password_here

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-super-secret-key-change-this
JWT_EXPIRES_IN=7d

# CORS
CORS_ORIGIN=http://localhost:3000
```

### 3. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE agents_system;
CREATE USER agents_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE agents_system TO agents_user;
```

### 4. Run Migrations

```bash
psql -U agents_user -d agents_system -f database/migrations/001_initial_schema.sql
```

This creates:
- **Users table**: Authentication and user management
- **Behavior agents**: 8 business leaders with profiles
- **Board rooms**: 8 predefined board rooms + custom boards
- **Conversations & Messages**: Chatbot conversation history
- **Consultations**: Complete advice history with ratings
- **User Preferences**: Favorites and usage tracking

### 5. Start the Server

```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm run build
npm start
```

The server will start at `http://localhost:4000`

## API Endpoints

### Authentication (`/api/auth`)

#### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "fullName": "John Doe"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe"
  }
}
```

#### Get Current User
```bash
GET /api/auth/me
Authorization: Bearer <token>
```

### Agents (`/api/agents`)

#### List All Agents
```bash
GET /api/agents
```

#### Get Agent Details
```bash
GET /api/agents/musk
```

#### Get Agent Statistics (Authenticated)
```bash
GET /api/agents/musk/stats
Authorization: Bearer <token>
```

#### Toggle Favorite (Authenticated)
```bash
POST /api/agents/musk/favorite
Authorization: Bearer <token>
Content-Type: application/json

{
  "isFavorite": true
}
```

#### Get Favorites (Authenticated)
```bash
GET /api/agents/favorites/list
Authorization: Bearer <token>
```

#### Get Agents by Sector
```bash
GET /api/agents/by-sector/technology
```

### Board Rooms (`/api/boardrooms`)

#### List Predefined Board Rooms
```bash
GET /api/boardrooms
```

#### Get My Custom Boards (Authenticated)
```bash
GET /api/boardrooms/my-boards
Authorization: Bearer <token>
```

#### Create Custom Board Room (Authenticated)
```bash
POST /api/boardrooms
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Tech Board",
  "description": "AI and automation focus",
  "focusSectors": ["technology"],
  "decisionStyle": "majority",
  "consensusThreshold": 0.6,
  "members": [
    { "agentKey": "musk", "votingWeight": 0.4 },
    { "agentKey": "jobs", "votingWeight": 0.3 },
    { "agentKey": "zuckerberg", "votingWeight": 0.3 }
  ]
}
```

#### Update Custom Board (Authenticated)
```bash
PUT /api/boardrooms/<board-id>
Authorization: Bearer <token>
```

#### Delete Custom Board (Authenticated)
```bash
DELETE /api/boardrooms/<board-id>
Authorization: Bearer <token>
```

### Chatbot (`/api/chatbot`)

#### Create Conversation (Authenticated)
```bash
POST /api/chatbot/conversations
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Product Launch Strategy",
  "contextType": "board_room",
  "selectedAgents": ["musk", "jobs", "bezos"],
  "boardRoomId": "uuid-of-board-room"
}
```

#### List Conversations (Authenticated)
```bash
GET /api/chatbot/conversations
Authorization: Bearer <token>
```

#### Get Conversation Details (Authenticated)
```bash
GET /api/chatbot/conversations/<conversation-id>
Authorization: Bearer <token>
```

#### Ask a Question (Authenticated)
```bash
POST /api/chatbot/ask
Authorization: Bearer <token>
Content-Type: application/json

# Individual agents
{
  "conversationId": "uuid",
  "question": "Should we acquire this startup for $50M?",
  "agentKeys": ["musk", "bezos", "fink"],
  "decisionContext": "ACQUISITION"
}

# Board room
{
  "conversationId": "uuid",
  "question": "What's our go-to-market strategy?",
  "boardRoomId": "uuid",
  "decisionContext": "STRATEGIC_PLANNING"
}
```

#### Rate Consultation (Authenticated)
```bash
POST /api/chatbot/rate
Authorization: Bearer <token>
Content-Type: application/json

{
  "consultationId": "uuid",
  "rating": 5,
  "feedback": "Extremely helpful insights"
}
```

## Available Agents

### Tech Leaders

1. **Elon Musk** (`musk`)
   - First principles thinking
   - Aggressive timelines
   - Vertical integration

2. **Steve Jobs** (`jobs`)
   - User experience first
   - Simplification and design
   - Holistic innovation

3. **Mark Zuckerberg** (`zuckerberg`)
   - Data-driven decisions
   - Move fast and break things
   - Long-term bets

4. **Jeff Bezos** (`bezos`)
   - Customer obsession
   - Day 1 mentality
   - Embrace failure

### Finance Leaders

5. **Larry Fink** (`fink`)
   - Long-term sustainability
   - Stakeholder capitalism
   - Risk management

### Real Estate & Entrepreneurs

6. **Donald Trump** (`trump`)
   - Aggressive negotiation
   - Extreme anchoring
   - Branding and marketing

7. **Sam Zell** (`zell`)
   - Distressed opportunities
   - Supply and demand
   - Contrarian investing

8. **Donald Bren** (`bren`)
   - Quality and detail
   - Long-term vision
   - Sustainability

## Predefined Board Rooms

1. **Tech Innovation Board**: Musk, Jobs, Zuckerberg, Bezos
2. **Investment & Finance Board**: Fink (40%), Zell (30%), Bren (30%)
3. **Real Estate Development Board**: Zell, Bren, Trump
4. **Negotiation & Deal Making Board**: Trump, Zell, Musk, Fink
5. **Product Strategy Board**: Jobs, Zuckerberg, Bezos, Musk
6. **Growth & Scale Board**: Bezos, Zuckerberg, Musk, Fink
7. **Crisis Management Board**: Musk, Trump, Fink, Zell
8. **Executive Leadership Board**: All 8 agents (equal weight)

## Decision Contexts

- `STRATEGIC_PLANNING` - Long-term strategy
- `TACTICAL_EXECUTION` - Short-term execution
- `CRISIS_MANAGEMENT` - Urgent problems
- `OPPORTUNITY_EVALUATION` - New opportunities
- `RISK_ASSESSMENT` - Risk analysis
- `TEAM_BUILDING` - Hiring and teams
- `PRODUCT_DEVELOPMENT` - Product strategy
- `MARKET_EXPANSION` - Market entry
- `NEGOTIATION` - Deal making
- `FINANCIAL_PLANNING` - Financial strategy
- `INNOVATION` - R&D decisions
- `ACQUISITION` - M&A decisions
- `PARTNERSHIP` - Partnership evaluation
- `COMPETITIVE_RESPONSE` - Competitive strategy
- `GENERAL` - General advice

## Business Sectors

- `TECHNOLOGY` - Software, hardware, AI
- `E_COMMERCE` - Online retail
- `FINANCE` - Investment, banking
- `REAL_ESTATE` - Property development
- `AUTOMOTIVE` - Vehicle manufacturing
- `AEROSPACE` - Space, aviation
- `SOCIAL_MEDIA` - Social networks
- `GENERAL` - Cross-industry

## Development

### Project Structure

```typescript
// Import agents
import { ElonMuskBehaviorAgent } from './src/agents/ElonMuskBehaviorAgent';
import { BehaviorAgentFactory } from './src/agents/BehaviorAgentFactory';

// Create factory
const factory = new BehaviorAgentFactory(pool, redis);

// Get individual agent
const musk = factory.getAgentByName('musk');
const advice = await musk.getAdvice(
  'Should we launch in Q4?',
  'STRATEGIC_PLANNING'
);

// Get board room consensus
const { boardRoom, config } = factory.createTechInnovationBoard();
const consensus = await boardRoom.getBoardRoomConsensus(
  config.name,
  'Should we launch in Q4?',
  'STRATEGIC_PLANNING',
  'TECHNOLOGY'
);
```

### Adding New Agents

1. Create agent file in `src/agents/`
2. Implement `IBehaviorAgent` interface
3. Add agent to database migration
4. Update `BehaviorAgentFactory.ts`
5. Export from `src/index.ts`

### Running Tests

```bash
npm test
```

## Production Deployment

### Environment Variables

Set production values for:
- `NODE_ENV=production`
- `JWT_SECRET` - Strong random secret
- `DB_PASSWORD` - Secure database password
- `CORS_ORIGIN` - Your frontend URL

### Database

- Enable SSL connections
- Set up connection pooling
- Configure backups
- Set up replication for high availability

### Redis

- Enable persistence (RDB/AOF)
- Configure maxmemory policy
- Set up Redis cluster for high availability

### Server

- Use process manager (PM2, systemd)
- Enable HTTPS with SSL certificates
- Set up reverse proxy (Nginx, Caddy)
- Configure logging and monitoring
- Set up health checks

### Example PM2 Configuration

```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'agents-system',
    script: './dist/server/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 4000
    }
  }]
};
```

```bash
npm run build
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Performance

- **Caching**: Redis caches agent profiles and common responses
- **Connection Pooling**: PostgreSQL connection pool (min: 2, max: 10)
- **Rate Limiting**: 100 requests per 15 minutes per IP
- **Compression**: gzip compression for responses
- **Indexes**: Optimized database indexes for fast queries

## Security

- **Authentication**: JWT tokens with configurable expiration
- **Password Hashing**: bcrypt with 10 salt rounds
- **HTTPS**: Required for production
- **Helmet**: Security headers protection
- **CORS**: Configurable origin restrictions
- **Rate Limiting**: Prevents abuse
- **SQL Injection**: Parameterized queries
- **XSS Protection**: Input sanitization

## License

MIT

## Support

For issues and questions:
- GitHub Issues: (your-repo-url)
- Email: support@yourcompany.com
