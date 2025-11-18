# Unified Platform

A consolidated platform that brings together multiple enterprise services under one unified system with a central dashboard.

## Platforms Included

1. **Finance Platform** - Portfolio management, market data analysis, and investment tracking
2. **Real Estate Dashboard** - Property management, financial modeling, and deal analysis
3. **Bond.AI** - AI-powered connection intelligence and relationship scoring
4. **Legacy Systems** - AI-powered legacy code transformation and process automation
5. **Labor Transformation** - Labor market analysis and freelance worker platform

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   UNIFIED PLATFORM                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────────────────────┐   │
│  │   Traefik    │───▶│     Unified Dashboard        │   │
│  │   Gateway    │    │        (Port 3000)           │   │
│  │  (Port 80)   │    └──────────────────────────────┘   │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Backend Services                     │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Finance  │ │RealEst. │ │Bond.AI  │            │   │
│  │  │ :8000   │ │ :8001   │ │ :8002   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Legacy   │ │Labor    │ │Agents   │            │   │
│  │  │ :8003   │ │ :8004   │ │ :8005   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Shared Infrastructure                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │PostgreSQL│ │ Redis  │ │RabbitMQ │            │   │
│  │  │ :5432   │ │ :6379   │ │:5672    │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │ Ollama  │ │Weaviate │ │Prometheus│           │   │
│  │  │ :11434  │ │ :8082   │ │ :9090   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

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

# Or start specific service groups
./start.sh infrastructure
./start.sh backends
./start.sh frontends
```

### Stop the Platform

```bash
./stop.sh

# To remove volumes
docker compose down -v
```

### Check Status

```bash
./status.sh
```

## Port Mapping

### Main Access Points
| Service | Port | Description |
|---------|------|-------------|
| Unified Dashboard | 3000 | Main entry point - access all services |
| Traefik Dashboard | 8080 | API Gateway management |
| Grafana | 3001 | Monitoring dashboards |
| Prometheus | 9090 | Metrics collection |

### Backend APIs
| Service | Port | Description |
|---------|------|-------------|
| Finance API | 8000 | Portfolio & investment management |
| Real Estate API | 8001 | Property & deal management |
| Bond.AI API | 8002 | Connection intelligence |
| Legacy Systems API | 8003 | Code transformation |
| Labor API | 8004 | Labor market platform |
| Bond.AI Agents | 8005 | Python AI agents |

### Frontend UIs
| Service | Port | Description |
|---------|------|-------------|
| Finance UI | 3002 | Finance platform dashboard |
| Real Estate UI | 3003 | Real estate dashboard |
| Bond.AI UI | 3004 | Connection intelligence UI |
| Labor UI | 3005 | Labor platform UI |

### Infrastructure
| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5432 | Shared database (5 databases) |
| Redis | 6379 | Shared cache |
| RabbitMQ | 5672, 15672 | Message queue |
| Ollama | 11434 | Local LLM |
| Weaviate | 8082 | Vector database |

## Configuration

### Environment Variables

Copy `.env` file and modify as needed:

```bash
# Database
POSTGRES_USER=unified_user
POSTGRES_PASSWORD=unified_password

# Redis
REDIS_PASSWORD=unified_redis_pass

# RabbitMQ
RABBITMQ_USER=unified_rabbit
RABBITMQ_PASSWORD=unified_rabbit_pass

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin
```

### Databases

The platform uses a single PostgreSQL instance with pgvector extension, containing multiple databases:

- `finance_db` - Finance platform data
- `realestate_db` - Real estate dashboard data
- `bondai_db` - Bond.AI connection data
- `legacy_db` - Legacy systems data
- `labor_db` - Labor platform data

## Features

### AI/ML Capabilities

- **26+ AI Agents** across all platforms
- **Local LLM** via Ollama (no external API dependencies)
- **Vector databases** for embeddings (Weaviate, pgvector)
- **Multi-agent systems** with MCP support

### Monitoring & Observability

- **Prometheus** for metrics collection
- **Grafana** for visualization dashboards
- **Centralized logging** across all services
- **Health checks** for all services

### Routing

All services are accessible via Traefik:

- `localhost` - Unified Dashboard
- `api.localhost/finance` - Finance API
- `api.localhost/realestate` - Real Estate API
- `api.localhost/bondai` - Bond.AI API
- `api.localhost/legacy` - Legacy API
- `api.localhost/labor` - Labor API
- `finance.localhost` - Finance UI
- `realestate.localhost` - Real Estate UI
- `bondai.localhost` - Bond.AI UI
- `labor.localhost` - Labor UI

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

### Scale Services

```bash
docker compose up -d --scale bondai-agents=3
```

## Troubleshooting

### Services not starting

1. Check if ports are available: `netstat -tlnp | grep -E '(3000|8000|8001|8002|8003|8004)'`
2. Check Docker logs: `docker compose logs [service-name]`
3. Ensure Docker has enough resources allocated

### Database connection issues

1. Wait for PostgreSQL to be healthy: `docker compose ps postgres`
2. Check database logs: `docker compose logs postgres`
3. Verify credentials in `.env` file

### Memory issues

The platform requires significant memory for all AI/ML services. Minimum recommended:
- 16GB RAM
- If limited, start only essential services

## Contributing

1. Each platform is in its own directory
2. Shared configurations are in `/config`
3. The unified dashboard is in `/unified-dashboard`

## License

See individual platform directories for specific licenses.
