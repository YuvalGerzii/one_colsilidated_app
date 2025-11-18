# Unified Platform - Complete Capabilities Documentation

A consolidated enterprise platform combining Finance, Real Estate, Bond.AI, Legacy Systems, and Labor Transformation services with 26+ AI agents and 100+ API endpoints.

## Table of Contents

- [Platform Overview](#platform-overview)
- [Quick Start](#quick-start)
- [Port Mapping](#port-mapping)
- [Platform 1: Finance Platform](#platform-1-finance-platform)
- [Platform 2: Real Estate Dashboard](#platform-2-real-estate-dashboard)
- [Platform 3: Bond.AI](#platform-3-bondai)
- [Platform 4: Legacy Systems](#platform-4-legacy-systems)
- [Platform 5: Labor Transformation](#platform-5-labor-transformation)
- [Infrastructure Services](#infrastructure-services)
- [Configuration](#configuration)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## Platform Overview

| Platform | Backend Port | Frontend Port | AI Agents | Description |
|----------|-------------|---------------|-----------|-------------|
| Finance Platform | 8100 | 3102 | 7+ | Portfolio management, arbitrage detection, extreme events |
| Real Estate Dashboard | 8101 | 3103 | 5+ | Property management, deal analysis, tax optimization |
| Bond.AI | 8102 | 3104 | 11 | AI-powered connection intelligence |
| Legacy Systems | 8103 | - | 3+ | Enterprise legacy modernization |
| Labor Transformation | 8104 | 3105 | 5+ | Learning hub, career navigation |

**Total: 26+ AI Agents | 100+ API Endpoints | 6 PostgreSQL Databases**

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- At least 16GB RAM recommended
- 50GB+ disk space

### Start the Platform

```bash
# Make scripts executable
chmod +x start.sh stop.sh status.sh

# Start all services
./start.sh

# Or use docker compose directly
docker compose up -d

# Access Unified Dashboard
open http://localhost:3100
```

### View API Documentation

- **Finance**: http://localhost:8100/docs
- **Real Estate**: http://localhost:8101/docs
- **Bond.AI**: http://localhost:8102/docs
- **Legacy**: http://localhost:8103/docs
- **Labor**: http://localhost:8104/docs

---

## Port Mapping

### Gateway & Dashboard
| Service | Port | Description |
|---------|------|-------------|
| Unified Dashboard | 3100 | Main entry point |
| Traefik HTTP | 8180 | API Gateway |
| Traefik HTTPS | 8443 | Secure Gateway |
| Traefik Dashboard | 8181 | Gateway Admin |

### Backend APIs
| Service | Port | Internal Port |
|---------|------|---------------|
| Finance Backend | 8100 | 8000 |
| Real Estate Backend | 8101 | 8000 |
| Bond.AI Backend | 8102 | 3002 |
| Legacy Systems Backend | 8103 | 8000 |
| Labor Backend | 8104 | 8000 |
| Bond.AI Python Agents | 8105 | 8000 |

### Frontend UIs
| Service | Port |
|---------|------|
| Unified Dashboard | 3100 |
| Grafana | 3101 |
| Finance UI | 3102 |
| Real Estate UI | 3103 |
| Bond.AI UI | 3104 |
| Labor UI | 3105 |

### Infrastructure
| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5532 | Database (pgvector enabled) |
| Redis | 6479 | Caching |
| RabbitMQ | 5772 / 15772 | Message Queue / Management |
| Keycloak | 8183 | Authentication |
| Ollama | 11534 | Local LLM |
| Weaviate | 8182 | Vector Database |
| Qdrant | 6333 / 6334 | Vector Search |
| Neo4j | 7474 / 7687 | Graph Database |
| Elasticsearch | 9200 | Search Engine |
| MinIO | 9100 / 9101 | Object Storage |
| Prometheus | 9190 | Metrics |

---

## Platform 1: Finance Platform

**Backend**: `http://localhost:8100`
**Frontend**: `http://localhost:3102`
**Traefik Route**: `api.localhost/finance`

### 1.1 Arbitrage Detection & Trading System

A sophisticated multi-agent system for detecting and executing arbitrage opportunities across markets.

**Location**: `FULL_finance_platform/Finance_platform/arbitrage_trader/`

#### Trading Agents

| Agent | Description | File |
|-------|-------------|------|
| **Cross-Exchange Agent** | Detects price discrepancies across exchanges | `agents/cross_exchange_agent.py` |
| **Statistical Arbitrage Agent** | Mean reversion and cointegration strategies | `agents/statistical_agent.py` |
| **Triangular Arbitrage Agent** | Currency/crypto triangular opportunities | `agents/triangular_agent.py` |
| **Risk Manager Agent** | Position sizing and risk limits | `agents/risk_manager_agent.py` |
| **Market Research Agent** | Market microstructure analysis | `agents/market_research_agent.py` |
| **Sentiment Analysis Agent** | News and social sentiment | `agents/sentiment_analysis_agent.py` |
| **Portfolio Manager Agent** | Portfolio optimization | `agents/portfolio_manager_agent.py` |

#### Arbitrage Algorithms

- **Cross-Exchange Detection** - `algorithms/cross_exchange.py`
- **Correlation Analysis** - `algorithms/correlation_analysis.py`
- **Gap Detection** - `algorithms/gap_detection.py`
- **Market Microstructure** - `algorithms/market_microstructure.py`

#### Key Features
- Real-time arbitrage detection with sub-second latency
- Multi-market support: Crypto, Forex, Stocks, Commodities
- Automated execution with risk management
- Performance metrics and analytics

### 1.2 Extreme Events Market Prediction Platform

**Location**: `FULL_finance_platform/Finance_platform/backend/extreme_events_platform/`

A comprehensive platform for predicting market reactions to extreme events with versions 1.0 through 7.0.

#### Event Detection Agents

| Agent | Description | File |
|-------|-------------|------|
| **Pandemic Agent** | Disease outbreak impact | `agents/pandemic_agent.py` |
| **Terrorism Agent** | Security event analysis | `agents/terrorism_agent.py` |
| **Natural Disaster Agent** | Weather and geological events | `agents/natural_disaster_agent.py` |
| **Economic Crisis Agent** | Recession and market crashes | `agents/economic_crisis_agent.py` |
| **Geopolitical Agent** | Political tensions and conflicts | `agents/geopolitical_agent.py` |
| **Cyber Attack Agent** | Cybersecurity threats | `agents/cyber_attack_agent.py` |
| **Climate Crisis Agent** | Long-term climate impacts | `agents/climate_crisis_agent.py` |
| **Compound Event Agent** | Multi-factor event analysis | `agents/compound_event_agent.py` |
| **Inflation Agent** | Inflation prediction | `agents/inflation_agent.py` |
| **Interest Rate Agent** | Rate change impacts | `agents/interest_rate_agent.py` |
| **Recession Agent** | Recession forecasting | `agents/recession_agent.py` |

#### Platform Versions

**Version 7.0 - Market Reading**
- Order flow analysis
- Market breadth indicators
- Intermarket analysis
- HFT detection
- Volume profile analysis

**Version 6.0 - Early Warning System**
- 12-24 month crisis prediction
- 98.8% ML model accuracy
- Early indicators tracking
- Scenario simulation

**Version 5.0 - Cross-Sector Analysis**
- Commodity arbitrage detection
- Weather derivatives
- Energy market events
- Cross-sector correlation

**Version 4.0 - Advanced Trading Strategies**
- Hedge fund strategies
- Derivatives frameworks
- Short selling systems

**Version 3.0 - NLP & Economic Events**
- Sentiment analysis
- Economic event prediction
- News impact scoring

#### Quick Analysis

```python
from extreme_events_platform import quick_analysis

result = quick_analysis('pandemic', {'severity': 4, 'r0': 3.5})
print(result['synthesis']['market_impact_estimate'])
```

### 1.3 Finance API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/v1/trading-agents` | Trading agent management |
| `/api/v1/market-data` | Real-time market data |
| `/api/v1/finance-models` | Financial modeling tools |
| `/api/v1/funds` | Fund management |
| `/api/v1/companies` | Company data |
| `/api/v1/monitoring` | System monitoring |
| `/api/v1/health` | Health check |

---

## Platform 2: Real Estate Dashboard

**Backend**: `http://localhost:8101`
**Frontend**: `http://localhost:3103`
**Traefik Route**: `api.localhost/realestate`

### 2.1 Property Management

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **SFR Management** | Single-family rental tracking | `/api/v1/property-management` |
| **Multifamily** | Apartment complex management | `/api/v1/property-management` |
| **Commercial** | Office/retail properties | `/api/v1/property-management` |
| **Vacation Rentals** | Short-term rental management | `/api/v1/property-management` |

### 2.2 Financial Modeling

| Model | Description | Endpoint |
|-------|-------------|----------|
| **DCF Analysis** | Discounted cash flow models | `/api/v1/financial-models/dcf` |
| **LBO Models** | Leveraged buyout analysis | `/api/v1/financial-models/lbo` |
| **Cap Rate Analysis** | Capitalization rate calculations | `/api/v1/real-estate/cap-rate` |
| **IRR Calculations** | Internal rate of return | `/api/v1/real-estate/irr` |
| **Cash-on-Cash** | Return on investment | `/api/v1/real-estate/cash-on-cash` |

### 2.3 Tax Optimization Strategies

| Strategy | Description | Endpoint |
|----------|-------------|----------|
| **1031 Exchange** | Tax-deferred exchanges | `/api/v1/tax-calculators/1031` |
| **Cost Segregation** | Accelerated depreciation | `/api/v1/advanced-tax/cost-segregation` |
| **Depreciation** | Standard depreciation | `/api/v1/tax-calculators/depreciation` |
| **QSBS Optimization** | Qualified small business stock | `/api/v1/elite-tax/qsbs` |
| **Augusta Rule** | Tax-free rental income | `/api/v1/elite-tax/augusta-rule` |
| **REPS Status** | Real estate professional | `/api/v1/elite-tax/reps` |
| **Estate Planning** | Wealth transfer strategies | `/api/v1/elite-tax/estate-planning` |

### 2.4 Deal Analysis & Pipeline

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Deal Scoring** | AI-powered deal analysis | `/api/v1/deal-analysis` |
| **Pipeline Management** | Deal tracking | `/api/v1/deals` |
| **Sensitivity Analysis** | Risk modeling | `/api/v1/sensitivity-analysis` |
| **Investment Memos** | Automated report generation | `/api/v1/reports` |

### 2.5 Market Intelligence

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Market Data** | Real-time market information | `/api/v1/market-intelligence` |
| **Competitive Analysis** | Market comparisons | `/api/v1/market-intelligence/enhanced` |
| **Stock & REITs** | YFinance integration | `/api/v1/market-intelligence/yfinance` |
| **Economic Indicators** | FRED data integration | `/api/v1/market-intelligence/economics` |

### 2.6 CRM & Contacts

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Contact Management** | Investor and broker contacts | `/api/v1/crm/contacts` |
| **Activity Tracking** | Interactions and follow-ups | `/api/v1/crm/activities` |
| **Pipeline** | Deal flow management | `/api/v1/crm/pipeline` |

### 2.7 Legal Services

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Document Templates** | Legal document generation | `/api/v1/internal-legal/templates` |
| **Clause Analysis** | AI contract analysis | `/api/v1/legal-services/enhanced` |
| **Compliance Audit** | Regulatory compliance | `/api/v1/compliance-audit` |
| **Risk Scoring** | Legal risk assessment | `/api/v1/internal-legal/risk-scoring` |

### 2.8 AI & ML Features

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **AI Chatbot** | Multi-agent assistant | `/api/v1/ai-chatbot` |
| **Predictive Analytics** | Price and rent forecasting | `/api/v1/predictive-analytics` |
| **PDF Extraction** | Document data extraction | `/api/v1/pdf-extraction` |
| **LLM Integration** | Local Ollama models | `/api/v1/llm` |
| **MarkItDown** | Document conversion | `/api/v1/markitdown` |

### 2.9 Portfolio & Reporting

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Portfolio Analytics** | Performance tracking | `/api/v1/portfolio-analytics` |
| **Interactive Dashboards** | Custom KPI dashboards | `/api/v1/dashboards` |
| **Report Generation** | Investment memos | `/api/v1/reports` |
| **Project Tracking** | Task management | `/api/v1/project-tracking` |

### 2.10 Complete API Reference

```
/api/v1/auth                    - Authentication
/api/v1/users                   - User management
/api/v1/companies               - Company management
/api/v1/deals                   - Deal management
/api/v1/property-management     - Property CRUD
/api/v1/real-estate             - RE calculations
/api/v1/accounting              - Financial tracking
/api/v1/tax-calculators         - Tax tools
/api/v1/advanced-tax            - Advanced strategies
/api/v1/elite-tax               - Elite tax loopholes
/api/v1/crm                     - CRM system
/api/v1/market-intelligence     - Market data
/api/v1/integrations            - Third-party APIs
/api/v1/calculations            - Saved calculations
/api/v1/fund-management         - PE/VC funds
/api/v1/financial-models        - DCF/LBO models
/api/v1/debt-management         - Loan tracking
/api/v1/reports                 - Report generation
/api/v1/project-tracking        - Task management
/api/v1/legal-services/enhanced - AI legal
/api/v1/compliance-audit        - Regulatory
/api/v1/pdf-extraction          - Document AI
/api/v1/internal-legal          - Templates
/api/v1/templates               - Model templates
/api/v1/portfolio-analytics     - Performance
/api/v1/dashboards              - Custom dashboards
/api/v1/llm                     - Local LLM
/api/v1/markitdown              - Doc conversion
/api/v1/sensitivity-analysis    - Risk analysis
/api/v1/deal-analysis           - Deal scoring
/api/v1/predictive-analytics    - ML forecasting
/api/v1/ai-chatbot              - Multi-agent chat
```

---

## Platform 3: Bond.AI

**Backend**: `http://localhost:8102`
**Python Agents**: `http://localhost:8105`
**Frontend**: `http://localhost:3104`
**Traefik Route**: `api.localhost/bondai`

### 3.1 AI-Powered Connection Intelligence

Bond.AI is a sophisticated multi-agent system for relationship scoring and professional networking.

**Location**: `bond.ai_code/multi-agent-system/bond.ai/`

### 3.2 Connection Intelligence Agents

| Agent | Description |
|-------|-------------|
| **Relationship Scoring Agent** | Overall relationship quality scoring |
| **Connection Matching Agent** | Find ideal professional connections |
| **Trust Bridge Agent** | Build trust networks |
| **Expertise Matching Agent** | Skill-based professional matching |
| **Communication Style Agent** | Communication optimization |
| **Opportunity Detection Agent** | Identify business opportunities |
| **Network Analysis Agent** | Network graph analysis |
| **NLP Profile Agent** | Natural language profile analysis |
| **Personality Compatibility Agent** | Personality matching |
| **Interest Matching Agent** | Common interest detection |
| **Emotional Intelligence Agent** | EQ-based insights |

### 3.3 Backend Routes

**Location**: `server/routes/`

| Route | Description | File |
|-------|-------------|------|
| **Authentication** | User auth and OAuth | `auth.ts` |
| **Registration** | User registration | `registration.ts` |
| **Search** | Connection search | `search.ts` |
| **Recommendations** | AI recommendations | `recommendations.ts` |
| **Match Quality** | Match scoring | `match-quality.ts` |
| **Network Analysis** | Graph analysis | `network-analysis.ts` |
| **Insights** | Connection insights | `insights.ts` |
| **Collaboration** | Collaboration tools | `collaboration.ts` |
| **Negotiations** | Negotiation support | `negotiations.ts` |
| **Analytics** | Usage analytics | `analytics.ts` |
| **Filters** | Search filters | `filters.ts` |

### 3.4 Integrations

- **LinkedIn OAuth** - Profile import and connection sync
- **PostgreSQL + pgvector** - Vector similarity search
- **Ollama LLM** - Local language model for analysis

### 3.5 Key Features

- AI-powered relationship scoring
- Professional network analysis
- Opportunity detection and recommendations
- Trust network building
- Communication style optimization
- Personality compatibility matching
- LinkedIn integration

---

## Platform 4: Legacy Systems

**Backend**: `http://localhost:8103`
**Traefik Route**: `api.localhost/legacy`

### 4.1 Enterprise Legacy Modernization

**Location**: `Legacy-Systems-Manual-Processes-in-Enterprises/`

An AI-powered platform for legacy code transformation, process mining, and enterprise automation.

### 4.2 Backend Routes

| Route | Description | File |
|-------|-------------|------|
| **Legacy Migrator** | Code transformation | `src/api/routes/legacy_migrator.py` |
| **Process Miner** | Process discovery | `src/api/routes/process_miner.py` |
| **Risk Radar** | Risk assessment | `src/api/routes/risk_radar.py` |
| **Company Brain** | Knowledge graphs | `src/api/routes/company_brain.py` |
| **Document OS** | Document management | `src/api/routes/document_os.py` |
| **Automation Fabric** | RPA orchestration | `src/api/routes/automation_fabric.py` |
| **HITL Hub** | Human-in-the-loop | `src/api/routes/hitl_hub.py` |
| **Governance** | Compliance governance | `src/api/routes/governance.py` |
| **Infrastructure** | System management | `src/api/routes/infrastructure.py` |
| **LLM Monitoring** | Model monitoring | `src/api/routes/llm_monitoring.py` |
| **Agents** | AI agent management | `src/api/routes/agents.py` |

### 4.3 Key Capabilities

| Capability | Description |
|------------|-------------|
| **Legacy Code Analysis** | Analyze and document legacy systems |
| **Code Transformation** | Convert legacy code to modern stacks |
| **Process Mining** | Discover business processes from logs |
| **RPA Integration** | Robotic process automation |
| **Knowledge Graphs** | Build organizational knowledge bases |
| **Risk Assessment** | Identify modernization risks |
| **Document Extraction** | Extract data from legacy documents |

### 4.4 Technology Stack

- **Neo4j** - Knowledge graph database
- **Qdrant** - Vector embeddings
- **Elasticsearch** - Full-text search
- **MinIO** - Object storage
- **Jaeger** - Distributed tracing

---

## Platform 5: Labor Transformation

**Backend**: `http://localhost:8104`
**Frontend**: `http://localhost:3105`
**Traefik Route**: `api.localhost/labor`

### 5.1 Learning Hub - Complete 5-Agent System

**Frontend**: `frontend/src/pages/LearningHub.js`
**Backend**: `backend/app/api/agents.py`

| Agent | Description | Endpoint |
|-------|-------------|----------|
| **Learning Strategist** | Personalized learning paths | `/api/v1/agents/create-learning-path/{worker_id}` |
| **Teaching Coach** | Adaptive teaching sessions | `/api/v1/agents/teaching-session/{worker_id}` |
| **Career Navigator** | Career path exploration | `/api/v1/agents/explore-career-paths/{worker_id}` |
| **Gap Analyzer** | Skills gap analysis | `/api/v1/agents/analyze-gaps/{worker_id}` |
| **Progress Monitor** | Learning progress tracking | `/api/v1/agents/monitor-progress/{worker_id}` |

#### Learning Hub Features

- **Personalized Learning Paths** - AI-generated optimal learning strategies
- **Adaptive Teaching** - 1-on-1 AI coaching with difficulty adjustment
- **Career Exploration** - 5-year career path projections with income potential
- **Practice Problems** - Generated problems with difficulty scaling
- **Progress Tracking** - Metrics, streaks, and recommendations
- **Full 5-Agent Analysis** - Comprehensive career transition planning

#### Example Usage

```javascript
// Create personalized learning path
POST /api/v1/agents/create-learning-path/1

// Start teaching session
POST /api/v1/agents/teaching-session/1?skill=machine_learning&difficulty=medium

// Explore career paths
POST /api/v1/agents/explore-career-paths/1?time_horizon_years=5

// Generate practice problems
POST /api/v1/agents/practice-problems?skill=python&difficulty=medium&count=5

// Run complete 5-agent analysis
POST /api/v1/agents/full-agent-analysis/1
```

### 5.2 Additional Agent Capabilities

| Agent | Description | Endpoint |
|-------|-------------|----------|
| **Job Application Strategist** | Application optimization | `/api/v1/agents/job-strategy` |
| **Mentorship Matcher** | Find mentors | `/api/v1/agents/mentorship` |
| **Personal Brand Builder** | Professional branding | `/api/v1/agents/personal-brand` |

### 5.3 Freelance Workers Hub

**Frontend**: `frontend/src/pages/FreelanceWorkersHub.js`

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Dashboard** | Freelancer overview | `/api/v1/freelance/dashboard/freelancer/{id}` |
| **Profile Optimization** | AI profile improvement | `/api/v1/freelance/profile/{id}/optimize` |
| **Job Search** | Job matching | `/api/v1/freelance/jobs/search` |
| **Proposal Generation** | AI proposal templates | `/api/v1/freelance/proposals/{id}/generate-template` |
| **Pricing Optimization** | Rate recommendations | `/api/v1/freelance/advisor/pricing-optimization/{id}` |
| **Growth Strategy** | Business planning | `/api/v1/freelance/advisor/growth-strategy/{id}` |
| **Contract Management** | Active contracts | `/api/v1/freelance/contracts/freelancer/{id}` |
| **Reviews** | Reputation management | `/api/v1/freelance/reviews/freelancer/{id}` |
| **Portfolio** | Work showcase | `/api/v1/freelance/portfolio/freelancer/{id}` |

### 5.4 Gig Economy Hub

**Frontend**: `frontend/src/pages/GigEconomyHub.js`

| Feature | Description | Endpoint |
|---------|-------------|----------|
| **Gig Dashboard** | Worker overview | `/api/v1/gig/dashboard/{id}` |
| **Skills Matching** | Match skills to gigs | `/api/v1/gig/match-skills-to-gigs` |
| **Benefits Calculator** | Insurance & benefits | `/api/v1/gig/benefits-calculator` |
| **Income Stabilization** | Revenue planning | `/api/v1/gig/income-stabilization-plan` |
| **Gig vs W-2 Comparison** | Employment comparison | `/api/v1/gig/compare-gig-vs-w2` |

### 5.5 Additional Frontend Pages

| Page | Description | File |
|------|-------------|------|
| **Digital Twin Dashboard** | Worker simulation | `pages/DigitalTwinDashboard.js` |
| **Career Simulator** | Career scenario testing | `pages/CareerSimulator.js` |
| **AI Autopilot** | Automated career management | `pages/AIAutopilot.js` |
| **Progress Dashboard** | Learning progress | `pages/ProgressDashboard.js` |
| **Agent Assistant** | Multi-agent chat | `pages/AgentAssistant.js` |
| **Corporate Transformation** | Enterprise workforce | `pages/CorporateTransformation.js` |
| **Government Dashboard** | Policy analysis | `pages/GovernmentDashboard.js` |
| **Agent Network** | Multi-agent visualization | `pages/MultiAgent/AgentNetwork.jsx` |
| **Workflow Dashboard** | Agent workflows | `pages/MultiAgent/WorkflowDashboard.jsx` |

### 5.6 Backend API Modules

```
/api/v1/agents              - AI agent endpoints
/api/v1/workers             - Worker management
/api/v1/skills              - Skills database
/api/v1/jobs                - Job listings
/api/v1/progress            - Progress tracking
/api/v1/freelance           - Freelance hub
/api/v1/gig                 - Gig economy
/api/v1/corporate           - Enterprise features
/api/v1/enterprise          - Corporate transformation
/api/v1/autopilot           - AI automation
/api/v1/digital-twin        - Worker simulation
/api/v1/analytics           - Platform analytics
/api/v1/economic-copilot    - Economic analysis
/api/v1/study-buddy         - Learning companion
/api/v1/career-tools        - Career utilities
/api/v1/multi-agent         - Multi-agent system
```

---

## Infrastructure Services

### Shared Databases

The platform uses a single PostgreSQL instance (port 5532) with pgvector extension:

| Database | Purpose |
|----------|---------|
| `finance_db` | Finance platform data |
| `realestate_db` | Real estate data |
| `bondai_db` | Bond.AI data |
| `legacy_db` | Legacy systems data |
| `labor_db` | Labor platform data |
| `auth_db` | Keycloak authentication |

### AI/ML Infrastructure

| Service | Purpose | Port |
|---------|---------|------|
| **Ollama** | Local LLM inference | 11534 |
| **Weaviate** | Vector database | 8182 |
| **Qdrant** | Vector search | 6333/6334 |
| **Neo4j** | Graph database | 7474/7687 |

### Monitoring & Observability

| Service | Purpose | Port | URL |
|---------|---------|------|-----|
| **Prometheus** | Metrics collection | 9190 | http://localhost:9190 |
| **Grafana** | Visualization | 3101 | http://localhost:3101 |
| **Traefik Dashboard** | Gateway metrics | 8181 | http://localhost:8181 |

### Centralized Authentication

**Keycloak** (Port 8183) provides OAuth2/OIDC authentication:
- **Admin Console**: http://localhost:8183
- **Realm**: `unified-platform`
- **Default Credentials**: admin/admin (change in production)

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# PostgreSQL
POSTGRES_USER=unified_user
POSTGRES_PASSWORD=unified_password

# Redis
REDIS_PASSWORD=unified_redis_pass

# RabbitMQ
RABBITMQ_USER=unified_rabbit
RABBITMQ_PASSWORD=unified_rabbit_pass

# Neo4j
NEO4J_PASSWORD=enterprise_pass

# MinIO
MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin

# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin

# LinkedIn OAuth (Bond.AI)
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_REDIRECT_URI=http://localhost:3104/api/linkedin/callback
```

### Traefik Routing

All services are accessible via Traefik at port 8180:

```
http://localhost:8180/finance/...     -> Finance Backend
http://localhost:8180/realestate/...  -> Real Estate Backend
http://localhost:8180/bondai/...      -> Bond.AI Backend
http://localhost:8180/legacy/...      -> Legacy Backend
http://localhost:8180/labor/...       -> Labor Backend
```

---

## Development

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f finance-backend

# Multiple services
docker compose logs -f finance-backend realestate-backend
```

### Rebuild Services

```bash
# Rebuild specific service
docker compose build finance-backend

# Rebuild and restart
docker compose up -d --build finance-backend
```

### Health Checks

All services expose health endpoints:

```bash
curl http://localhost:8100/health  # Finance
curl http://localhost:8101/health  # Real Estate
curl http://localhost:8102/health  # Bond.AI
curl http://localhost:8103/health  # Legacy
curl http://localhost:8104/health  # Labor
```

---

## Troubleshooting

### Services not starting

1. Check if ports are available: `netstat -tlnp | grep -E '(3100|8100|8101|8102|8103|8104)'`
2. Check Docker logs: `docker compose logs [service-name]`
3. Ensure Docker has enough resources allocated

### Database connection issues

1. Wait for PostgreSQL to be healthy: `docker compose ps postgres`
2. Check database logs: `docker compose logs postgres`
3. Verify credentials in `.env` file

### Memory issues

The platform requires significant memory for all AI/ML services:
- **Minimum**: 16GB RAM
- **Recommended**: 32GB RAM
- If limited, start only essential services

### Port conflicts

All external ports use non-standard values (8100+ for backends, 3100+ for frontends) to avoid conflicts with common development ports (8000, 3000, etc.).

---

## Architecture Summary

```
                    ┌─────────────────┐
                    │  Unified        │
                    │  Dashboard      │
                    │  :3100          │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    Traefik      │
                    │    :8180        │
                    └────────┬────────┘
                             │
        ┌────────────┬───────┼───────┬────────────┬─────────────┐
        │            │       │       │            │             │
   ┌────▼────┐  ┌────▼───┐ ┌─▼──┐ ┌──▼────┐  ┌────▼────┐   ┌────▼────┐
   │ Finance │  │ Real   │ │Bond│ │Legacy │  │ Labor   │   │ Bond.AI │
   │ Backend │  │ Estate │ │.AI │ │Systems│  │ Backend │   │ Agents  │
   │ :8100   │  │ :8101  │ │:8102│ │:8103  │  │ :8104   │   │ :8105   │
   └────┬────┘  └────┬───┘ └─┬──┘ └───┬───┘  └────┬────┘   └────┬────┘
        │            │       │        │           │              │
        └────────────┴───────┴────────┴───────────┴──────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐   ┌──────▼──────┐  ┌──────▼──────┐
              │ PostgreSQL│   │    Redis    │  │   RabbitMQ  │
              │  :5532    │   │    :6479    │  │ :5772/15772 │
              └───────────┘   └─────────────┘  └─────────────┘
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Platforms** | 5 |
| **AI Agents** | 26+ |
| **API Endpoints** | 100+ |
| **PostgreSQL Databases** | 6 |
| **Docker Services** | 25+ |
| **Frontend UIs** | 5 |

---

## License

See individual platform directories for specific licenses.
