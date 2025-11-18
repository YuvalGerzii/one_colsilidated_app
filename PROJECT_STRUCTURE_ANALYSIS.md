# COMPREHENSIVE PROJECT STRUCTURE ANALYSIS
## One Consolidated App - Complete Overview

**Last Updated:** November 18, 2025
**Base Location:** `/home/user/one_colsilidated_app`
**Git Status:** Currently on branch `claude/review-project-structure-01DqfavB1pQC67czm9hESXtb`

---

## TABLE OF CONTENTS

1. [Top-Level Structure](#top-level-structure)
2. [Services & Platforms Overview](#services--platforms-overview)
3. [Complete Port Mapping](#complete-port-mapping)
4. [Database Services](#database-services)
5. [Frontend Applications](#frontend-applications)
6. [Backend Services & APIs](#backend-services--apis)
7. [Agents & Skills Architecture](#agents--skills-architecture)
8. [Docker Compose Configurations](#docker-compose-configurations)
9. [Technology Stack Summary](#technology-stack-summary)
10. [API Endpoints Structure](#api-endpoints-structure)

---

## TOP-LEVEL STRUCTURE

### Directory Hierarchy (3+ Levels Deep)

```
/home/user/one_colsilidated_app/
├── .claude/                              # Claude Code configuration
│   └── settings.local.json
│
├── FULL_finance_platform/               # Financial Services Platform
│   └── Finance_platform/
│       ├── .claude/
│       ├── backend/                     # Main backend service
│       │   ├── app/
│       │   │   ├── api/
│       │   │   │   ├── v1/
│       │   │   │   │   └── endpoints/
│       │   │   │   ├── router.py
│       │   │   │   └── deps.py
│       │   │   ├── models/
│       │   │   ├── services/
│       │   │   ├── repositories/
│       │   │   ├── core/
│       │   │   ├── scripts/
│       │   │   ├── trading_agents/      # AI Trading Agents
│       │   │   └── main.py
│       │   ├── portfolio-dashboard-frontend/  # React Frontend
│       │   ├── Dockerfile
│       │   └── requirements.txt
│       ├── arbitrage_trader/             # Arbitrage Trading System
│       │   └── requirements.txt
│       ├── config/                       # Infrastructure configs
│       │   ├── traefik/                 # Reverse proxy
│       │   ├── nginx/                   # Web server
│       │   ├── postgres/                # Database config
│       │   ├── prometheus/              # Metrics config
│       │   └── grafana/                 # Dashboard config
│       ├── docker-compose.yml           # Main orchestration
│       ├── .env.example
│       └── startup scripts (*.sh)
│
├── bond.ai_code/                        # AI-Powered Connection Intelligence
│   └── multi-agent-system/
│       ├── .claude/
│       ├── config.yaml                  # Agent system configuration
│       ├── bond.ai/                     # Main bond.ai application
│       │   ├── docker-compose.yml
│       │   ├── server/                  # Node.js API Server
│       │   │   ├── src/
│       │   │   ├── routes/
│       │   │   ├── services/
│       │   │   ├── database/
│       │   │   ├── Dockerfile
│       │   │   ├── package.json
│       │   │   └── .env.example
│       │   ├── frontend/                # React Frontend
│       │   │   ├── src/
│       │   │   ├── Dockerfile
│       │   │   └── package.json
│       │   ├── python-agents/           # Python Agent System
│       │   │   ├── agents/
│       │   │   │   ├── communication_style_analysis.py
│       │   │   │   ├── connection_matching.py
│       │   │   │   ├── expertise_skills_matching.py
│       │   │   │   ├── interest_hobby_matching.py
│       │   │   │   ├── network_analysis.py
│       │   │   │   ├── nlp_profile_analysis.py
│       │   │   │   ├── opportunity_detection.py
│       │   │   │   ├── personality_compatibility.py
│       │   │   │   ├── relationship_scoring.py
│       │   │   │   ├── trust_bridge.py
│       │   │   │   └── value_alignment.py
│       │   │   ├── Dockerfile
│       │   │   └── requirements.txt
│       │   ├── mcp-server/              # Model Context Protocol Server
│       │   ├── package.json
│       │   └── examples/
│       ├── agents-system/
│       ├── multi_agent_system/
│       └── examples/
│
├── Legacy-Systems-Manual-Processes-in-Enterprises/
│   └── Legacy-Systems-Manual-Processes-in-Enterprises/
│       ├── docker-compose.yml
│       ├── Dockerfile
│       ├── src/
│       │   └── main.py
│       ├── requirements.txt
│       └── .env.example
│
├── real_estate_dashboard/               # Real Estate & Financial Analysis Platform
│   ├── .claude/
│   │   └── skills/                     # Specialized domain skills
│   │       ├── advanced-data-analysis/
│   │       ├── advanced-data-science/
│   │       ├── advanced-finance/
│   │       ├── advanced-manager/
│   │       ├── advanced-marketing/
│   │       ├── advanced-ui-design/
│   │       ├── api-testing/
│   │       ├── code-quality/
│   │       ├── data-science/
│   │       ├── financial-pdf-extraction/
│   │       ├── frontend-design/
│   │       ├── pe-financial-modeling/
│   │       └── real-estate-domain/
│   ├── backend/                        # FastAPI Backend
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   └── endpoints/
│   │   │   │   ├── router.py
│   │   │   │   └── deps.py
│   │   │   ├── models/
│   │   │   ├── services/
│   │   │   ├── config/
│   │   │   ├── database/
│   │   │   ├── integrations/          # External APIs
│   │   │   ├── ml/                    # ML/Predictive models
│   │   │   ├── multi_agent_system/    # Advanced MAS
│   │   │   │   ├── agents/
│   │   │   │   ├── mcp/
│   │   │   │   ├── memory/
│   │   │   │   ├── communication/
│   │   │   │   ├── tools/
│   │   │   │   ├── persistence/
│   │   │   │   ├── learning/
│   │   │   │   ├── core/
│   │   │   │   └── observability/
│   │   │   ├── templates/
│   │   │   ├── utils/
│   │   │   └── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── alembic/                    # DB migrations
│   ├── frontend/                       # React Frontend
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── docker-compose.yml
│   ├── lease_analyzer/
│   ├── hotel_model/
│   ├── financial_platform/
│   ├── scripts/
│   └── storage/                        # File uploads
│       └── uploads/
│
└── labor_transofrmation/                # Labor Market & Skills Platform
    └── Labor-market-disruption-inequality/
        ├── .claude/
        ├── backend/                    # FastAPI Backend
        ├── frontend/                   # React Frontend
        ├── freelance_workers/
        ├── study_buddy/
        └── docker-compose.yml
```

---

## SERVICES & PLATFORMS OVERVIEW

### 1. FULL Finance Platform (Financial Services & Portfolio Management)

**Purpose:** Comprehensive financial platform for portfolio management, market data analysis, and investment tracking

**Main Components:**
- Backend API (FastAPI on Python 3.11)
- Frontend Dashboard (React + Vite)
- Trading Agents System
- Arbitrage Trader
- Database Backend (PostgreSQL)

**Key Features:**
- Market data integration (real-time)
- Portfolio analytics
- Investment models
- Real estate tools
- Property management
- Company & fund management
- Financial reporting

---

### 2. Bond.AI (AI-Powered Connection Intelligence)

**Purpose:** Multi-agent system for intelligent connection matching, relationship scoring, and opportunity detection

**Main Components:**
- Node.js API Server
- React Frontend
- Python Agents System (FastAPI)
- Ollama LLM Integration
- PostgreSQL with pgvector
- Redis Cache

**Key Features:**
- Intelligent connection matching
- Relationship scoring
- Network analysis
- Communication style matching
- Expertise & skills analysis
- Opportunity detection
- Trust bridge algorithms
- Value alignment analysis

---

### 3. Legacy Systems & Enterprise AI

**Purpose:** AI-powered system for legacy code transformation and process automation

**Main Components:**
- FastAPI Backend
- Neo4j Graph Database
- Qdrant Vector DB
- Multiple specialized databases

**Key Features:**
- Legacy system analysis
- Process automation
- Document OCR/extraction
- System transformation
- Knowledge management

---

### 4. Real Estate Dashboard (Comprehensive Real Estate Analytics)

**Purpose:** Full-stack platform for real estate financial analysis, property management, and investment modeling

**Main Components:**
- FastAPI Backend (Python 3.11+)
- React Frontend (Vite + TypeScript)
- Multi-Agent System with MCP
- Ollama LLM Integration
- PostgreSQL Database
- Redis Cache

**Key Features:**
- Property management
- Real estate financial modeling
- Deal analysis & comparison
- Tax strategy optimization
- Market intelligence
- Lease analysis
- Renovation budgeting
- Investment calculators
- CRM integration
- PDF extraction
- Advanced analytics
- Predictive modeling

**API Endpoints Include:**
- Health checks
- Authentication & user management
- Company management
- Deal management (multi-type)
- Accounting & tax
- Market intelligence
- PDF extraction
- Legal services
- CRM functions
- Financial models
- Reporting
- AI chatbot with multi-agent system
- Sensitivity analysis
- Deal analysis framework

---

### 5. Labor Transformation (Labor Market & Skills Platform)

**Purpose:** Platform for analyzing labor market disruption and connecting freelance workers with opportunities

**Main Components:**
- FastAPI Backend
- React Frontend
- Freelance Hub
- Study Buddy Module

---

## COMPLETE PORT MAPPING

### Finance Platform Ports

| Service | Port | Protocol | Access | Purpose |
|---------|------|----------|--------|---------|
| Traefik HTTP | 80 | HTTP | Public | Reverse Proxy Entry Point |
| Traefik HTTPS | 443 | HTTPS | Public | Secure Gateway |
| Traefik Dashboard | 8080 | HTTP | Internal | Infrastructure UI |
| Frontend (React) | 3000 | HTTP | Public | User Interface |
| Grafana Dashboards | 3001 | HTTP | Internal | Monitoring/Analytics |
| Backend API | 8000 | HTTP | Internal | FastAPI Server |
| Nginx | 8081 | HTTP | Internal | Web Server |
| Weaviate (Vector DB) | 8082 | HTTP | Internal | AI/ML Vector Store |
| Prometheus | 9090 | HTTP | Internal | Metrics Collection |
| PostgreSQL | 5432 | TCP | Internal | Relational DB |
| PgAdmin | 5050 | HTTP | Internal | DB Management UI |
| Redis | 6379 | TCP | Internal | Cache/Message Queue |
| RabbitMQ AMQP | 5672 | TCP | Internal | Message Broker |
| RabbitMQ UI | 15672 | HTTP | Internal | Message Queue UI |

### Bond.AI Ports

| Service | Port | Protocol | Access | Purpose |
|---------|------|----------|--------|---------|
| API Server | 3002 | HTTP | Internal | Node.js Express API |
| Frontend | 5174 | HTTP | Public | React App |
| PostgreSQL (pgvector) | 5433 | TCP | Internal | Vector DB |
| Redis | 6380 | TCP | Internal | Cache |
| Ollama | 11435 | HTTP | Internal | Local LLM |
| Python Agents | 8005 | HTTP | Internal | Python API |

### Legacy Systems Platform

| Service | Port | Protocol | Access | Purpose |
|---------|------|----------|--------|---------|
| FastAPI Backend | 8000 | HTTP | Internal | Main API |
| PostgreSQL | 5432 | TCP | Internal | Primary DB |
| Redis | 6379 | TCP | Internal | Cache |
| Qdrant | 6333, 6334 | HTTP/gRPC | Internal | Vector DB |
| Neo4j | 7474, 7687 | HTTP/Bolt | Internal | Graph DB |
| Elasticsearch | 9200 | HTTP | Internal | Search/Logging |
| MinIO | 9000, 9001 | HTTP | Internal | S3 Storage |
| RabbitMQ | 5672, 15672 | AMQP/HTTP | Internal | Message Queue |
| Prometheus | 9090 | HTTP | Internal | Metrics |
| Grafana | 3000 | HTTP | Internal | Dashboards |
| Jaeger | 5775, 6831, 6832, 5778, 16686, 14268, 14250, 9411 | UDP/HTTP | Internal | Distributed Tracing |
| Ollama | 11434 | HTTP | Internal | Local LLM |

### Real Estate Dashboard

| Service | Port | Protocol | Access | Purpose |
|---------|------|----------|--------|---------|
| Frontend | 80 | HTTP | Public | React App |
| Backend API | 8000 | HTTP | Internal | FastAPI Server |
| PostgreSQL | 5432 | TCP | Internal | Relational DB |
| Redis | 6379 | TCP | Internal | Cache |
| Ollama | 11434 | HTTP | Internal | Local LLM |

### Labor Transformation

| Service | Port | Protocol | Access | Purpose |
|---------|------|----------|--------|---------|
| PostgreSQL | 5432 | TCP | Internal | Database |
| Redis | 6379 | TCP | Internal | Cache |

---

## DATABASE SERVICES

### PostgreSQL Instances

1. **Finance Platform Database**
   - **Container Name:** `postgres`
   - **Port:** 5432
   - **Database:** `portfolio_dashboard`
   - **User:** `portfolio_user`
   - **Features:** Standard relational database for portfolio and market data
   - **Volume:** `finance_postgres_data`

2. **Bond.AI Database (with pgvector)**
   - **Container Name:** `bondai-postgres`
   - **Port:** 5433
   - **Database:** `bondai`
   - **User:** `bondai_user`
   - **Features:** Vector support for AI embeddings
   - **Image:** `ankane/pgvector:v0.5.1`
   - **Volume:** `postgres-data`

3. **Real Estate Dashboard Database**
   - **Container Name:** `real_estate_db`
   - **Port:** 5432
   - **Database:** `real_estate_dashboard`
   - **User:** `postgres`
   - **Features:** Real estate financial data
   - **Volume:** `postgres_data`

4. **Legacy Systems Database**
   - **Container Name:** `enterprise-ai-postgres`
   - **Port:** 5432
   - **Database:** `enterprise_ai`
   - **User:** `enterprise_user`

### Vector & Specialized Databases

- **Weaviate** (Finance Platform)
  - Port: 8082
  - Purpose: Vector embeddings for AI/ML
  - Features: Anonymous access, no authentication required

- **Qdrant** (Legacy Systems)
  - Port: 6333 (HTTP), 6334 (gRPC)
  - Purpose: Vector similarity search
  
- **Neo4j** (Legacy Systems)
  - Ports: 7474 (HTTP), 7687 (Bolt)
  - Purpose: Graph database for relationships and knowledge graphs
  - Auth: neo4j/enterprise_pass

### Cache & Message Queues

- **Redis** instances across all platforms
  - Used for caching, sessions, and task queues
  - Persistence enabled with AOF

- **RabbitMQ** (Finance Platform & Legacy Systems)
  - AMQP: 5672
  - Management UI: 15672
  - Default user: `rabbitmq` / `rabbitmq_password`

### Search & Logging

- **Elasticsearch** (Legacy Systems)
  - Port: 9200
  - Purpose: Full-text search, logging, analytics
  - Configuration: Single-node, no security

- **MinIO** (Legacy Systems)
  - Ports: 9000 (API), 9001 (Console)
  - Purpose: S3-compatible object storage
  - Default credentials: minioadmin/minioadmin

---

## FRONTEND APPLICATIONS

### 1. Finance Platform Frontend
- **Location:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/backend/portfolio-dashboard-frontend`
- **Technology:** React 18 + TypeScript + Vite
- **Port:** 3000
- **Key Libraries:**
  - Material-UI (MUI) for components
  - Zustand for state management
  - React Query for data fetching
  - D3 & Recharts for visualizations
  - React Hook Form for forms
  - Axios for HTTP
- **Features:** Portfolio dashboard, market data visualization, investment tracking

### 2. Bond.AI Frontend
- **Location:** `/home/user/one_colsilidated_app/bond.ai_code/multi-agent-system/bond.ai/frontend`
- **Technology:** React 18 + TypeScript + Vite
- **Port:** 5174 (dev), 5173 (default Vite)
- **Key Libraries:**
  - Zustand for state management
  - React Query for data fetching
  - Socket.io for real-time updates
  - React Hook Form + Zod for validation
  - Framer Motion for animations
  - Tailwind CSS for styling
- **Features:** Connection intelligence, relationship visualization, network analysis

### 3. Real Estate Dashboard Frontend
- **Location:** `/home/user/one_colsilidated_app/real_estate_dashboard/frontend`
- **Technology:** React 18 + TypeScript + Vite
- **Port:** 80
- **Key Libraries:**
  - Material-UI (MUI) 5
  - Radix UI components
  - Tailwind CSS
  - React Query
  - Chart.js / Recharts
  - React Grid Layout
  - React Resizable
  - Framer Motion
- **Features:** Property management, financial modeling, market analysis, deal comparison

### 4. Labor Transformation Frontend
- **Location:** `/home/user/one_colsilidated_app/labor_transofrmation/Labor-market-disruption-inequality/frontend`
- **Technology:** React 18 + TypeScript + Vite
- **Purpose:** Freelance worker connections, labor market analysis

---

## BACKEND SERVICES & APIS

### Finance Platform Backend

**Location:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/backend`

**Technology:**
- FastAPI 0.104.1
- Python 3.11
- SQLAlchemy 2.0 for ORM
- Alembic for migrations
- Uvicorn ASGI server

**Main API Endpoints** (v1):
- `/health` - Health checks
- `/market-data` - Real-time market data, stock quotes
- `/real-estate` - Real estate tools and calculators
- `/finance` - Financial models (DCF, LBO, etc.)
- `/property-management` - Property operations
- `/companies` - Portfolio company management
- `/funds` - Fund management

**Core Modules:**
- `app/api/` - API route handlers
- `app/models/` - SQLAlchemy models
- `app/services/` - Business logic
- `app/repositories/` - Data access layer
- `app/core/` - Core utilities and configurations
- `app/scripts/` - Helper scripts
- `app/trading_agents/` - AI trading agents

**Key Features:**
- Market data integration (Yahoo Finance, etc.)
- Portfolio analytics and reporting
- Investment modeling
- Real estate financial tools
- Property management operations
- Company and fund management
- Trading agent system for automated analysis

---

### Real Estate Dashboard Backend

**Location:** `/home/user/one_colsilidated_app/real_estate_dashboard/backend`

**Technology:**
- FastAPI 0.109.2
- Python 3.11+
- SQLAlchemy 2.0
- Alembic for migrations
- Local LLM support (Ollama)
- Redis for caching

**Main API Endpoints** (v1):
- `/health` - Health checks
- `/auth` - User authentication
- `/users` - User management
- `/companies` - Company management
- `/deals` - Multi-type deal management (real estate, acquisitions, shares, commodities)
- `/property-management` - Property operations
- `/accounting` - Accounting functions
- `/tax-calculators` - Tax optimization
- `/market-intelligence` - Market data & analysis
- `/crm` - Customer relationship management
- `/reports` - Financial reports
- `/pdf-extraction` - Document processing
- `/legal` - Legal services integration
- `/llm` - Local LLM integration endpoints
- `/ai-chatbot` - Multi-agent AI system
- `/sensitivity-analysis` - Financial sensitivity analysis
- `/deal-analysis` - Advanced deal analysis
- `/predictive-analytics` - ML-based predictions

**Core Modules:**
- `app/api/` - API endpoints
- `app/models/` - Database models
- `app/services/` - Business logic
- `app/config/` - Configuration management
- `app/database/` - DB utilities
- `app/integrations/` - External API integrations
- `app/ml/` - Machine learning models
- `app/multi_agent_system/` - Advanced MAS with MCP
  - `agents/` - Agent implementations
  - `mcp/` - Model Context Protocol
  - `memory/` - Agent memory systems
  - `communication/` - Inter-agent communication
  - `tools/` - Agent tools
  - `persistence/` - State persistence
  - `learning/` - Learning mechanisms
  - `core/` - Core MAS framework
  - `observability/` - Monitoring & observability
- `app/templates/` - Email & document templates
- `app/utils/` - Utility functions
- `app/tasks/` - Background tasks
- `app/scripts/` - Data scripts

**Key Features:**
- Property and portfolio management
- Advanced real estate financial modeling
- Multi-type deal management (SFR, multifamily, commercial)
- Tax strategy optimization
- Lease analysis and benchmarking
- Market intelligence and forecasting
- Deal pipeline automation
- Multi-agent AI system for complex analysis
- Local LLM integration (Ollama)
- PDF document extraction
- Sensitivity and scenario analysis
- Predictive analytics
- Legal services integration

---

### Bond.AI Backend

**Location:** `/home/user/one_colsilidated_app/bond.ai_code/multi-agent-system/bond.ai/server`

**Technology:**
- Node.js 18 + TypeScript
- Express.js framework
- PostgreSQL with pgvector
- Redis for caching
- Ollama for local LLM

**Main API Endpoints:**
- Authentication endpoints
- User profile management
- Connection matching
- Relationship scoring
- Network analysis
- Opportunity detection
- Message/communication endpoints

**Core Modules:**
- `routes/` - API route handlers
- `services/` - Business logic
- `database/` - DB operations
- `middleware/` - Express middleware
- `auth/` - Authentication
- `utils/` - Utility functions

---

### Python Agents System

**Location:** `/home/user/one_colsilidated_app/bond.ai_code/multi-agent-system/bond.ai/python-agents`

**Technology:**
- FastAPI 0.104.0
- Python 3.11+
- Custom agent system

**Agent Types Implemented:**
1. **Communication Style Analysis** - Analyzes verbal and written communication patterns
2. **Connection Matching** - Identifies compatible connections based on multiple factors
3. **Expertise & Skills Matching** - Matches professional capabilities
4. **Interest & Hobby Matching** - Finds common interests
5. **Network Analysis** - Analyzes network topology and influence
6. **NLP Profile Analysis** - Processes and analyzes profile text
7. **Opportunity Detection** - Identifies potential opportunities
8. **Personality Compatibility** - Scores personality alignment
9. **Relationship Scoring** - Quantifies relationship potential
10. **Trust Bridge** - Identifies trusted intermediaries
11. **Value Alignment** - Assesses value system alignment

**API Endpoints:**
- `GET /health` - Health check
- `POST /analyze` - Run analysis agents
- `POST /match` - Execute matching algorithms

---

### Legacy Systems Backend

**Location:** `/home/user/one_colsilidated_app/Legacy-Systems-Manual-Processes-in-Enterprises/Legacy-Systems-Manual-Processes-in-Enterprises`

**Technology:**
- FastAPI 0.109.2
- Python 3.11
- Uvicorn server
- Multiple specialized databases

**Features:**
- Legacy code analysis
- Process automation
- Document extraction (OCR, PDF)
- System transformation capabilities
- Knowledge graph building

---

## AGENTS & SKILLS ARCHITECTURE

### Bond.AI Multi-Agent System

**Configuration File:** `/home/user/one_colsilidated_app/bond.ai_code/multi-agent-system/config.yaml`

**System Parameters:**
- **Max Agents:** 10
- **Parallel Execution:** Enabled
- **Timeout:** 300 seconds
- **Max Workers:** 5 (orchestrator)
- **Delegation Strategy:** Capability-based

**Learning System:**
- **Algorithm:** Q-Learning
- **Learning Rate:** 0.1
- **Discount Factor:** 0.95
- **Exploration Rate:** 0.2 (decaying)
- **Batch Size:** 32
- **Replay Buffer:** 10,000 experiences
- **Update Frequency:** Every 10 episodes
- **Save Frequency:** Every 100 episodes

**Memory System:**
- **Short-term:** 1,000 items
- **Long-term:** Persistent storage in `./data/memory`
- **Consolidation Interval:** 3,600 seconds
- **Consolidation Threshold:** 0.7 importance score

**Worker Types:**
1. **Researcher** (max 2 instances)
   - Capabilities: web_search, analysis, information_gathering

2. **Coder** (max 2 instances)
   - Capabilities: code_generation, debugging, refactoring

3. **Tester** (max 2 instances)
   - Capabilities: test_creation, validation, quality_assurance

4. **Data Analyst** (max 1 instance)
   - Capabilities: data_processing, visualization, statistical_analysis

**Tools Enabled:**
- File operations
- Code execution
- Web access
- Data processing
- Sandbox mode with 60-second timeout

---

### Real Estate Dashboard Skills

**Location:** `/home/user/one_colsilidated_app/real_estate_dashboard/.claude/skills/`

**Available Skills (15 specialized domains):**
1. Advanced Data Analysis
2. Advanced Data Science
3. Advanced Finance
4. Advanced Manager
5. Advanced Marketing
6. Advanced UI Design
7. API Testing
8. Code Quality
9. Data Science
10. Financial PDF Extraction
11. Frontend Design
12. PE Financial Modeling
13. Real Estate Domain
14. Database Migration Helper
15. UI/UX Reviewer

**Purpose:** Domain-specific AI assistance for specialized tasks in real estate, finance, and development

---

### Finance Platform Agents

**Trading Agents System:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/backend/app/trading_agents/`

**Purpose:** Automated trading and investment analysis agents

---

### Real Estate Dashboard Multi-Agent System

**Location:** `/home/user/one_colsilidated_app/real_estate_dashboard/backend/app/multi_agent_system/`

**Core Components:**
- **Agents:** Individual agent implementations
- **MCP (Model Context Protocol):** Integration layer
- **Memory:** Short/long-term memory management
- **Communication:** Inter-agent communication protocols
- **Tools:** Shared tools and utilities
- **Persistence:** State and history persistence
- **Learning:** ML-based improvement mechanisms
- **Observability:** Monitoring, logging, tracing

---

## DOCKER COMPOSE CONFIGURATIONS

### 1. Finance Platform Docker Compose

**File:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/docker-compose.yml`

**Network:** `finance_network` (bridge driver)

**Services (14 total):**

#### Infrastructure
1. **Traefik**
   - Image: traefik:latest
   - Ports: 80, 443, 8080
   - Role: Reverse proxy and load balancer

2. **Nginx**
   - Image: nginx:latest
   - Port: 8081
   - Role: Web server

#### Databases
3. **PostgreSQL**
   - Image: postgres:latest
   - Port: 5432
   - Volume: `finance_postgres_data`

4. **PgAdmin**
   - Image: dpage/pgadmin4:latest
   - Port: 5050
   - Volume: `finance_pgadmin_data`

#### Caching & Message Queue
5. **Redis**
   - Image: redis:alpine
   - Port: 6379
   - Volume: `finance_redis_data`
   - Features: AOF persistence, password protected

6. **RabbitMQ**
   - Image: rabbitmq:3-management
   - Ports: 5672 (AMQP), 15672 (UI)
   - Volume: `finance_rabbitmq_data`

#### Vector Database
7. **Weaviate**
   - Image: semitechnologies/weaviate:latest
   - Port: 8082
   - Volume: `finance_weaviate_data`
   - Purpose: AI/ML vector embeddings

#### Monitoring
8. **Prometheus**
   - Image: prom/prometheus:latest
   - Port: 9090
   - Volume: `finance_prometheus_data`

9. **Grafana**
   - Image: grafana/grafana:latest
   - Port: 3001
   - Volume: `finance_grafana_data`

#### Applications
10. **Backend API**
    - Build: ./backend/Dockerfile
    - Port: 8000
    - Depends On: postgres, redis, rabbitmq
    - Volume: ./backend:/app
    - Command: Uvicorn FastAPI app

11. **Frontend**
    - Build: ./portfolio-dashboard-frontend/Dockerfile
    - Port: 3000
    - Depends On: backend
    - Build Args: VITE_API_URL

12. **Celery Worker**
    - Build: ./backend/Dockerfile
    - Command: celery worker
    - Depends On: postgres, redis, rabbitmq, backend

**Volumes:**
- finance_postgres_data
- finance_pgadmin_data
- finance_redis_data
- finance_rabbitmq_data
- finance_weaviate_data
- finance_prometheus_data
- finance_grafana_data
- finance_nginx_logs

---

### 2. Bond.AI Docker Compose

**File:** `/home/user/one_colsilidated_app/bond.ai_code/multi-agent-system/bond.ai/docker-compose.yml`

**Network:** `bondai-network` (bridge driver)

**Services (6 total):**

1. **PostgreSQL (pgvector)**
   - Image: ankane/pgvector:v0.5.1
   - Port: 5433
   - Database: bondai
   - Volume: postgres-data

2. **Redis**
   - Image: redis:7-alpine
   - Port: 6380
   - Volume: redis-data

3. **Ollama**
   - Image: ollama/ollama:latest
   - Port: 11435
   - Volume: ollama-data
   - GPU Support: Optional (configurable)

4. **Python Agents**
   - Build: ./python-agents/Dockerfile
   - Port: 8005
   - Command: python api_server.py
   - Health Check: curl http://localhost:8000/health

5. **API Server**
   - Build: ./server/Dockerfile
   - Port: 3002
   - Technology: Node.js, Express
   - Command: npm run dev
   - Environment: Database, Redis, Ollama URLs configured

6. **Frontend**
   - Build: ./frontend/Dockerfile
   - Port: 5174
   - Technology: React, Vite
   - Command: npm run dev -- --host 0.0.0.0

---

### 3. Legacy Systems Docker Compose

**File:** `/home/user/one_colsilidated_app/Legacy-Systems-Manual-Processes-in-Enterprises/Legacy-Systems-Manual-Processes-in-Enterprises/docker-compose.yml`

**Network:** `enterprise-network` (bridge driver)

**Services (13 total):**

1. PostgreSQL (5432)
2. Redis (6379)
3. Qdrant Vector DB (6333, 6334)
4. Neo4j (7474, 7687)
5. Elasticsearch (9200)
6. MinIO (9000, 9001)
7. RabbitMQ (5672, 15672)
8. Prometheus (9090)
9. Grafana (3000)
10. Jaeger (multiple ports)
11. Ollama (11434)
12. FastAPI Backend (8000)
13. Celery Worker & Celery Beat

---

### 4. Real Estate Dashboard Docker Compose

**File:** `/home/user/one_colsilidated_app/real_estate_dashboard/docker-compose.yml`

**Services (4 total):**

1. **PostgreSQL**
   - Image: postgres:15-alpine
   - Port: 5432
   - Database: real_estate_dashboard

2. **Redis**
   - Image: redis:7-alpine
   - Port: 6379

3. **Backend API**
   - Build: ./backend/Dockerfile
   - Port: 8000
   - Command: uvicorn app.main:app

4. **Frontend**
   - Build: ./frontend/Dockerfile
   - Port: 80

5. **Ollama**
   - Image: ollama/ollama:latest
   - Port: 11434
   - Resources: 2GB-4GB memory, 2 CPU cores

---

## TECHNOLOGY STACK SUMMARY

### Backend Technologies

| Component | Technology | Version | Used In |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.104.1 - 0.109.2 | Finance, Real Estate, Legacy Systems |
| **Runtime** | Python | 3.11-3.11+ | All FastAPI services |
| **Runtime** | Node.js | 18 | Bond.AI Server |
| **Server** | Uvicorn | 0.24.0+ | FastAPI apps |
| **ORM** | SQLAlchemy | 2.0.23 | All databases |
| **Migrations** | Alembic | 1.13.0 | Database version control |
| **Database Driver** | psycopg2-binary / asyncpg | 2.9.9 / 0.29.0 | PostgreSQL access |
| **Validation** | Pydantic | 2.5.0+ | Request/response validation |

### Frontend Technologies

| Component | Technology | Version | Used In |
|-----------|-----------|---------|---------|
| **Framework** | React | 18.2.0 - 18.3.1 | All frontends |
| **Build Tool** | Vite | 5.0.0+ | All React apps |
| **Language** | TypeScript | 5.2.2+ | All frontends |
| **UI Framework** | Material-UI (MUI) | 5.14.0 - 5.15.0 | Finance, Real Estate |
| **UI Components** | Radix UI | latest | Real Estate |
| **Styling** | Tailwind CSS | 3.3.6 - 4.1.3 | All frontends |
| **State Mgmt** | Zustand | 4.4.0+ | React apps |
| **Data Fetching** | React Query | 3.39.0 - 5.14.0 | All frontends |
| **Routing** | React Router | 6.20.0 | All frontends |
| **Forms** | React Hook Form | 7.48.0 - 7.55.0 | All frontends |
| **Charting** | Recharts / Chart.js | 2.10.0+ | Dashboards |
| **HTTP Client** | Axios | 1.6.0+ | API calls |

### Data Processing & ML

| Component | Technology | Version | Used In |
|-----------|-----------|---------|---------|
| **Data Manipulation** | Pandas | 2.1.4 | Finance, Real Estate |
| **Numerical** | NumPy | 1.26.2 | All data processing |
| **ML Framework** | scikit-learn | 1.3.2 | Real Estate, Legacy |
| **Boosting** | XGBoost | 2.0.3 | Real Estate |
| **Market Data** | yfinance | 0.2.66 | Finance Platform |
| **LLM Integration** | Ollama | latest | Real Estate, Legacy, Bond.AI |
| **Vector Search** | Weaviate | latest | Finance Platform |
| **Vector Store** | Qdrant | latest | Legacy Systems |
| **Graph Database** | Neo4j | 5-community | Legacy Systems |
| **Search** | Elasticsearch | 8.11.3 | Legacy Systems |

### Cache & Message Queues

| Component | Technology | Version | Used In |
|-----------|-----------|---------|---------|
| **Cache** | Redis | 7-alpine | All platforms |
| **Message Queue** | RabbitMQ | 3-management | Finance, Legacy |
| **Task Queue** | Celery | 5.3.4 | Finance, Real Estate, Legacy |

### Infrastructure & DevOps

| Component | Technology | Version | Used In |
|-----------|-----------|---------|---------|
| **Reverse Proxy** | Traefik | latest | Finance Platform |
| **Web Server** | Nginx | latest | Finance Platform |
| **Container Runtime** | Docker | (latest) | All services |
| **Orchestration** | Docker Compose | 3.8 | All services |
| **Monitoring** | Prometheus | latest | Finance, Legacy |
| **Dashboards** | Grafana | latest | Finance, Legacy |
| **Tracing** | Jaeger | latest | Legacy Systems |
| **Object Storage** | MinIO | latest | Legacy Systems |
| **DB Admin** | PgAdmin | 4 | Finance Platform |

---

## API ENDPOINTS STRUCTURE

### Finance Platform API

**Base URL:** `http://localhost:8000/api/v1`

**Endpoint Categories:**

```
/health              - Health check & status
/market-data         - Stock quotes, historical data, indices
/real-estate         - Real estate calculators & tools
/finance             - Financial models (DCF, LBO, acquisition models)
/property-management - Property operations, tenants, maintenance
/companies           - Portfolio companies management
/funds               - Fund operations & reporting
```

**Future Endpoints (TODO):**
- /financials - Detailed financial statements
- /models - Model management
- /pdf - Document processing
- /reports - Report generation
- /dashboard - Dashboard configuration

---

### Real Estate Dashboard API

**Base URL:** `http://localhost:8000/api/v1`

**Main Endpoint Categories (40+ endpoints):**

```
/health                    - Health checks
/auth                      - User authentication & session
/users                     - User management & profiles
/companies                 - Organization management
/deals                     - Multi-type deal management
/property-management       - Property operations
/accounting                - Accounting functions
/tax-calculators           - Tax strategies & optimization
/advanced-tax-strategies   - Advanced tax planning
/elite-tax-strategies      - Premium tax strategies
/crm                       - Customer relationship management
/market-intelligence       - Market data & trends
/enhanced-market-intelligence - Advanced market analysis
/yfinance-economics        - Yahoo Finance & economic data
/integrations              - Third-party API integrations
/integrations/official-data - Government data sources
/saved-calculations        - Saved model calculations
/fund-management           - Fund operations
/financial-models          - Model templates & management
/debt-management           - Debt analysis & strategies
/reports                   - Report generation
/project-tracking          - Project management
/legal                     - Legal services integration
/pdf-extraction            - Document processing
/compliance-audit          - Compliance & audit
/model-templates           - Financial model templates
/portfolio-analytics       - Portfolio analysis
/interactive-dashboards    - Custom dashboards
/llm                       - Local LLM endpoints
/markitdown                - Document conversion
/sensitivity-analysis      - Sensitivity analysis
/deal-analysis             - Deal analysis framework
/predictive-analytics      - ML predictions
/ai-chatbot                - Multi-agent AI system
```

---

### Bond.AI API

**Base URL:** `http://localhost:3002/api`

**Core Endpoints:**

```
/auth                 - Authentication
/users                - User profiles
/connections          - Connection management
/matches              - Connection matching
/relationships        - Relationship data
/analysis             - Agent analysis results
/network              - Network visualization
/opportunities        - Opportunity detection
```

---

### Legacy Systems API

**Base URL:** `http://localhost:8000/api`

**Capabilities:**

```
/health              - Health checks
/analysis            - Code analysis
/transformation      - System transformation
/extraction          - Document extraction
/knowledge-graph     - Knowledge management
/automation          - Process automation
```

---

## ROUTING & GATEWAY CONFIGURATION

### Finance Platform Routing

**Traefik Configuration:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/config/traefik/`

**Services Registered:**
- Frontend: `localhost` on web entrypoint
- Backend API: `api.localhost`
- PgAdmin: `pgadmin.localhost`
- Prometheus: `prometheus.localhost`
- Grafana: `grafana.localhost`
- RabbitMQ: `rabbitmq.localhost` (port 15672)
- Nginx: `nginx.localhost`

**Traefik Features:**
- HTTP (80) and HTTPS (443) entrypoints
- Docker socket integration
- Load balancing
- Dashboard at port 8080

### Nginx Configuration

**Location:** `/home/user/one_colsilidated_app/FULL_finance_platform/Finance_platform/config/nginx/`

**Purpose:** Additional HTTP routing and reverse proxy configuration

---

## CONFIGURATION FILES SUMMARY

### Environment Files

Each service has `.env.example` files documenting all configuration variables:

1. **Finance Platform:** `.env.example` (90+ variables)
   - Database credentials
   - Redis configuration
   - RabbitMQ credentials
   - Service ports
   - API settings (CORS, etc.)
   - LLM configuration
   - Grafana credentials

2. **Bond.AI:** `server/.env.example`
   - Database & Redis config
   - JWT secrets
   - CORS settings
   - Ollama LLM setup
   - Python Agents URL
   - OAuth providers (LinkedIn, Google)

3. **Real Estate Dashboard:** Environment variables in docker-compose.yml
   - Database configuration
   - LLM settings (Ollama)
   - Cache configuration
   - API base URLs

---

## KEY FEATURES ACROSS PLATFORMS

### Horizontal Features (Present in Multiple Platforms)

1. **Multi-Agent Systems**
   - Bond.AI: Specialized agents for relationship matching
   - Real Estate: Advanced MAS with MCP for deal analysis
   - Finance: Trading agents

2. **LLM Integration**
   - All platforms support Ollama for local inference
   - Vector databases for embeddings
   - Custom prompt templates

3. **Real-time Updates**
   - WebSocket support (Bond.AI)
   - Redis pub/sub for messaging
   - RabbitMQ for task distribution

4. **Advanced Analytics**
   - Financial modeling & forecasting
   - Market intelligence
   - Predictive analytics (ML)
   - Sensitivity analysis

5. **Document Processing**
   - PDF extraction & analysis
   - OCR capabilities
   - MarkItDown conversion

6. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Jaeger distributed tracing (Legacy Systems)
   - Health checks across all services

7. **Extensible Architecture**
   - Claude Code skills for domain expertise
   - MCP (Model Context Protocol) support
   - Pluggable agent systems
   - Integration frameworks

---

## DEPLOYMENT CONSIDERATIONS

### Docker Images Used

**Official Images:**
- traefik:latest
- nginx:latest
- postgres:latest, postgres:15-alpine
- redis:alpine, redis:7-alpine
- rabbitmq:3-management, rabbitmq:3-management-alpine
- node:18-alpine
- python:3.11-slim
- grafana/grafana:latest
- prom/prometheus:latest
- dpage/pgadmin4:latest
- ollama/ollama:latest
- semitechnologies/weaviate:latest
- qdrant/qdrant:latest
- neo4j:5-community
- elasticsearch:8.11.3
- minio/minio:latest
- jaegertracing/all-in-one:latest

**Custom Built:**
- Finance Backend (Python 3.11)
- Real Estate Backend (Python 3.11)
- Bond.AI Server (Node.js 18)
- Bond.AI Python Agents (Python 3.11)
- Bond.AI Frontend (Node.js build)
- Real Estate Frontend (Node.js build)
- Finance Frontend (Node.js build)
- Legacy Systems Backend (Python 3.11)

### Data Persistence

**Docker Volumes:**
- postgres_data / finance_postgres_data
- redis_data / finance_redis_data
- rabbitmq_data / finance_rabbitmq_data
- pgadmin_data / finance_pgadmin_data
- weaviate_data / finance_weaviate_data
- prometheus_data / finance_prometheus_data
- grafana_data / finance_grafana_data
- ollama_data
- qdrant_data
- neo4j_data
- elasticsearch_data
- minio_data

---

## SUMMARY

This consolidated application represents a comprehensive suite of financial and enterprise platforms with:

- **5 Major Platforms** with distinct purposes
- **14+ Microservices** running in containers
- **4 Primary Databases** with specialized engines
- **40+ API Endpoints** across all services
- **Multiple AI/ML Capabilities** (agents, embeddings, local LLMs)
- **Sophisticated Observability** (Prometheus, Grafana, Jaeger)
- **Advanced Real-time Features** (WebSockets, message queues, streaming)
- **13+ Domain-Specific Skills** for specialized tasks
- **Full-stack Applications** with React frontends and FastAPI/Express backends

**Total Managed Services:** 50+ Docker containers across all platforms
**Total Codebase Size:** Large monorepo with diverse microservices
**Technology Diversity:** Python, Node.js, React, PostgreSQL, vector databases, graphs, and more

