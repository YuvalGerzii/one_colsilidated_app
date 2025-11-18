# Bond.AI MCP Server

Model Context Protocol server that provides AI assistants with rich context about Bond.AI users, networks, and recommendations.

## Features

### 📚 Resources (Read-only data access)

- `bondai://user/{userId}/profile` - User profile
- `bondai://user/{userId}/network` - Network connections
- `bondai://user/{userId}/recommendations` - Personalized recommendations
- `bondai://user/{userId}/communities` - Community memberships
- `bondai://user/{userId}/trajectory` - Growth history
- `bondai://user/{userId}/health` - Network health
- `bondai://user/{userId}/opportunities` - Detected opportunities
- `bondai://match/{userId}/{targetId}` - Match analysis
- `bondai://conversation/{userId}/context` - Conversation context

### 🛠️ Tools (Interactive capabilities)

- `get_recommendations` - Get personalized connection recommendations
- `analyze_match` - Analyze match quality between two users
- `predict_collaboration` - Predict collaboration success
- `detect_intent` - Detect user intent from message
- `generate_introduction` - Generate personalized introduction
- `detect_opportunities` - Find collaboration opportunities
- `analyze_relationship_health` - Analyze relationship health
- `get_network_insights` - Get network intelligence insights
- `suggest_next_action` - Suggest optimal next networking action
- `analyze_conversation` - Analyze conversation for insights

## Installation

```bash
cd bond.ai/mcp-server
npm install
npm run build
```

## Configuration

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "bondai": {
      "command": "node",
      "args": ["/path/to/bond.ai/mcp-server/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost:5432/bondai",
        "REDIS_URL": "redis://localhost:6379"
      }
    }
  }
}
```

## Usage Examples

Once configured, Claude can access Bond.AI data and tools:

**Example 1: Get user recommendations**
```
User: "Get recommendations for user abc123"
Claude: [Uses get_recommendations tool]
```

**Example 2: Analyze match quality**
```
User: "How well would user abc123 and user xyz789 match?"
Claude: [Uses analyze_match tool]
```

**Example 3: Access user profile**
```
User: "Show me the profile for user abc123"
Claude: [Reads bondai://user/abc123/profile resource]
```

## Architecture

The MCP server integrates with all Bond.AI agents:

- **RecommendationEngine** - Strategic recommendations
- **MatchQualityAgent** - ML-ready matching
- **CollaborationPredictionAgent** - Success prediction
- **CommunityDetectionAgent** - Community analysis
- **TemporalAnalysisAgent** - Network evolution
- **IntentRecognitionAgent** - Intent detection
- **RelationshipHealthAgent** - Health monitoring
- **OpportunityDetectionAgent** - Opportunity finding
- **ConversationIntelligenceAgent** - Conversation analysis
- **NetworkIntelligenceAgent** - Network insights
- **IntroductionOrchestrationAgent** - Introduction generation

## Development

```bash
# Watch mode for development
npm run dev

# Build
npm run build

# Start server
npm start
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (required)
- `REDIS_URL` - Redis connection string (required)

## Security

The MCP server should only be run locally and never exposed to the internet. It provides full access to the Bond.AI database.

## License

MIT
