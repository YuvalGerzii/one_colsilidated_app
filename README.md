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
│  │   Gateway    │    │        (Port 3100)           │   │
│  │  (Port 8180) │    └──────────────────────────────┘   │
│  └──────┬───────┘                                        │
│         │                                                │
│         ▼                                                │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Backend Services                     │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Finance  │ │RealEst. │ │Bond.AI  │            │   │
│  │  │ :8100   │ │ :8101   │ │ :8102   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │Legacy   │ │Labor    │ │Agents   │            │   │
│  │  │ :8103   │ │ :8104   │ │ :8105   │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Shared Infrastructure                   │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │PostgreSQL│ │ Redis  │ │RabbitMQ │            │   │
│  │  │ :5532   │ │ :6479   │ │:5772    │            │   │
│  │  └─────────┘ └─────────┘ └─────────┘            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │   │
│  │  │ Ollama  │ │Weaviate │ │Prometheus│           │   │
│  │  │ :11534  │ │ :8182   │ │ :9190   │            │   │
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
| Unified Dashboard | 3100 | Main entry point - access all services |
| Traefik Dashboard | 8181 | API Gateway management |
| Grafana | 3101 | Monitoring dashboards |
| Prometheus | 9190 | Metrics collection |

### Backend APIs
| Service | Port | Description |
|---------|------|-------------|
| Finance API | 8100 | Portfolio & investment management |
| Real Estate API | 8101 | Property & deal management |
| Bond.AI API | 8102 | Connection intelligence |
| Legacy Systems API | 8103 | Code transformation |
| Labor API | 8104 | Labor market platform |
| Bond.AI Agents | 8105 | Python AI agents |

### Frontend UIs
| Service | Port | Description |
|---------|------|-------------|
| Finance UI | 3102 | Finance platform dashboard |
| Real Estate UI | 3103 | Real estate dashboard |
| Bond.AI UI | 3104 | Connection intelligence UI |
| Labor UI | 3105 | Labor platform UI |

### Infrastructure
| Service | Port | Description |
|---------|------|-------------|
| PostgreSQL | 5532 | Shared database (6 databases) |
| Redis | 6479 | Shared cache |
| RabbitMQ | 5772, 15772 | Message queue |
| Ollama | 11534 | Local LLM |
| Weaviate | 8182 | Vector database |
| Keycloak | 8183 | Centralized authentication |

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

# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin
AUTH_REALM=unified-platform
```

### Databases

The platform uses a single PostgreSQL instance with pgvector extension, containing multiple databases:

- `finance_db` - Finance platform data
- `realestate_db` - Real estate dashboard data
- `bondai_db` - Bond.AI connection data
- `legacy_db` - Legacy systems data
- `labor_db` - Labor platform data
- `auth_db` - Keycloak authentication data

### Centralized Authentication

The platform uses Keycloak for centralized OAuth2/OIDC authentication:

- **Admin Console**: http://localhost:8183
- **Realm**: `unified-platform`
- **Default Credentials**: admin/admin (change in production)

All backend services are configured to authenticate against Keycloak using the `AUTH_SERVER_URL` and `AUTH_REALM` environment variables.

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

1. Check if ports are available: `netstat -tlnp | grep -E '(3100|8100|8101|8102|8103|8104)'`
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
