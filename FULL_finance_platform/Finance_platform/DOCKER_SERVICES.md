# Docker Services Documentation

This document provides comprehensive information about all Docker services configured in the Finance Platform.

## Table of Contents

- [Overview](#overview)
- [Services](#services)
- [Quick Start](#quick-start)
- [Service Details](#service-details)
- [Configuration](#configuration)
- [Accessing Services](#accessing-services)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The Finance Platform uses a microservices architecture with the following components:

- **Reverse Proxy**: Traefik, Nginx
- **Database**: PostgreSQL with PgAdmin
- **Caching & Messaging**: Redis, RabbitMQ
- **Vector Database**: Weaviate (for AI/RAG applications)
- **Monitoring**: Prometheus, Grafana
- **Applications**: Backend API, Frontend, Celery Workers

## Services

### Infrastructure Services

| Service | Image | Ports | Purpose |
|---------|-------|-------|---------|
| **Traefik** | traefik:latest | 80, 443, 8080 | Reverse proxy and load balancer |
| **Nginx** | nginx:latest | 8081 | Web server and reverse proxy |
| **PostgreSQL** | postgres:latest | 5432 | Primary relational database |
| **PgAdmin** | dpage/pgadmin4:latest | 5050 | Database administration UI |
| **Redis** | redis:alpine | 6379 | In-memory cache and data store |
| **RabbitMQ** | rabbitmq:3-management | 5672, 15672 | Message broker |
| **Weaviate** | semitechnologies/weaviate:latest | 8082 | Vector database for AI |
| **Prometheus** | prom/prometheus:latest | 9090 | Metrics collection |
| **Grafana** | grafana/grafana:latest | 3001 | Monitoring dashboards |

### Application Services

| Service | Build Context | Ports | Purpose |
|---------|--------------|-------|---------|
| **Backend** | ./backend | 8000 | FastAPI backend API |
| **Frontend** | ./portfolio-dashboard-frontend | 3000 | React/Vue frontend |
| **Celery Worker** | ./backend | - | Asynchronous task processing |

## Quick Start

### 1. Initial Setup

```bash
# Copy environment variables file
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

### 2. Start All Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 3. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

## Service Details

### Traefik (Reverse Proxy)

**Purpose**: Modern HTTP reverse proxy and load balancer with automatic service discovery.

**Configuration**:
- Static config: `config/traefik/traefik.yml`
- Dynamic config: `config/traefik/dynamic/`

**Features**:
- Automatic service discovery via Docker labels
- Load balancing
- Dashboard at http://localhost:8080
- HTTP/HTTPS routing

**Docker Labels**:
Services use Traefik labels for automatic routing:
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.localhost`)"
  - "traefik.http.routers.myapp.entrypoints=web"
```

### Nginx (Web Server)

**Purpose**: High-performance web server and reverse proxy.

**Configuration**:
- Main config: `config/nginx/nginx.conf`
- Additional configs: `config/nginx/conf.d/*.conf`

**Access**: http://localhost:8081

### PostgreSQL (Database)

**Purpose**: Primary relational database for application data.

**Configuration**:
- Database: `portfolio_dashboard` (configurable via `POSTGRES_DB`)
- User: `portfolio_user` (configurable via `POSTGRES_USER`)
- Password: Set in `.env` file

**Initialization Scripts**:
Place SQL scripts in `config/postgres/init/` to run on first startup.

**Data Persistence**:
Data stored in Docker volume `finance_postgres_data`

### PgAdmin (Database Administration)

**Purpose**: Web-based PostgreSQL administration tool.

**Access**: http://localhost:5050
- Email: Set via `PGADMIN_DEFAULT_EMAIL` (default: admin@admin.com)
- Password: Set via `PGADMIN_DEFAULT_PASSWORD` (default: admin)

**Pre-configured Server**:
PostgreSQL server is automatically configured via `config/pgadmin/servers.json`

### Redis (Cache)

**Purpose**: In-memory data structure store for caching and session management.

**Features**:
- Persistence enabled (AOF)
- Password protected (set via `REDIS_PASSWORD`)

**Connection String**:
```
redis://:your_password@redis:6379/0
```

### RabbitMQ (Message Broker)

**Purpose**: Message queue for asynchronous task processing.

**Access**:
- AMQP Port: 5672
- Management UI: http://localhost:15672
- Credentials: Set via `RABBITMQ_USER` and `RABBITMQ_PASSWORD`

**Features**:
- Management plugin enabled
- Web-based monitoring interface

### Weaviate (Vector Database)

**Purpose**: Vector database for AI/ML applications, RAG (Retrieval-Augmented Generation).

**Access**: http://localhost:8082

**Features**:
- Semantic search
- Vector storage
- GraphQL API

### Prometheus (Metrics)

**Purpose**: Time-series database for metrics collection and monitoring.

**Access**: http://localhost:9090

**Configuration**: `config/prometheus/prometheus.yml`

**Scrape Targets**:
- Prometheus itself
- Backend API
- RabbitMQ
- Traefik
- Add custom targets in config file

### Grafana (Dashboards)

**Purpose**: Visualization and analytics platform for metrics.

**Access**: http://localhost:3001
- Username: Set via `GRAFANA_ADMIN_USER` (default: admin)
- Password: Set via `GRAFANA_ADMIN_PASSWORD` (default: admin)

**Features**:
- Pre-configured Prometheus datasource
- Dashboard provisioning from `config/grafana/dashboards/`
- Custom dashboards can be created and saved

**Add Dashboards**:
1. Create dashboard in Grafana UI
2. Export as JSON
3. Save to `config/grafana/dashboards/`

## Configuration

### Environment Variables

All environment variables are defined in `.env` file. Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

**Key Variables**:

```bash
# Database
POSTGRES_DB=portfolio_dashboard
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=your_secure_password

# Redis
REDIS_PASSWORD=your_redis_password

# RabbitMQ
RABBITMQ_USER=rabbitmq
RABBITMQ_PASSWORD=your_rabbitmq_password

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_grafana_password

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
```

### Custom Configuration

**Traefik**: Edit `config/traefik/traefik.yml` or add files to `config/traefik/dynamic/`

**Nginx**: Edit `config/nginx/nginx.conf` or add files to `config/nginx/conf.d/`

**Prometheus**: Edit `config/prometheus/prometheus.yml` to add scrape targets

**Grafana**: Add dashboard JSON files to `config/grafana/dashboards/`

## Accessing Services

### Web Interfaces

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| **Frontend** | http://localhost:3000 | - |
| **Backend API** | http://localhost:8000 | - |
| **Traefik Dashboard** | http://localhost:8080 | - |
| **Nginx** | http://localhost:8081 | - |
| **PgAdmin** | http://localhost:5050 | admin@admin.com / admin |
| **Grafana** | http://localhost:3001 | admin / admin |
| **Prometheus** | http://localhost:9090 | - |
| **RabbitMQ Management** | http://localhost:15672 | rabbitmq / rabbitmq_password |
| **Weaviate** | http://localhost:8082 | - |

### Database Connection

**PostgreSQL via PgAdmin**: Already pre-configured in PgAdmin

**PostgreSQL via CLI**:
```bash
docker-compose exec postgres psql -U portfolio_user -d portfolio_dashboard
```

**PostgreSQL from Application**:
```
postgresql://portfolio_user:password@postgres:5432/portfolio_dashboard
```

### Redis Connection

**Redis via CLI**:
```bash
docker-compose exec redis redis-cli -a your_redis_password
```

## Monitoring

### Prometheus Metrics

Prometheus scrapes metrics from:
- Backend API (`/metrics` endpoint)
- RabbitMQ
- Traefik
- Prometheus itself

**Add Custom Metrics**: Update `config/prometheus/prometheus.yml`

### Grafana Dashboards

1. Access Grafana at http://localhost:3001
2. Prometheus is pre-configured as datasource
3. Create dashboards or import from https://grafana.com/grafana/dashboards/

**Recommended Dashboards**:
- Node Exporter Full (ID: 1860) - System metrics
- Docker Container Monitoring (ID: 193)
- RabbitMQ Overview (ID: 10991)
- PostgreSQL Database (ID: 9628)

## Troubleshooting

### Check Service Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f postgres
docker-compose logs -f backend
```

### Check Service Health

```bash
# List all services with status
docker-compose ps

# Check specific service
docker-compose ps postgres
```

### Restart a Service

```bash
docker-compose restart postgres
docker-compose restart backend
```

### Rebuild Service

```bash
# Rebuild and restart
docker-compose up -d --build backend

# Force rebuild without cache
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Database Issues

**Cannot connect to PostgreSQL**:
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Verify health check
docker-compose exec postgres pg_isready -U portfolio_user
```

**Reset Database** (WARNING: Deletes all data):
```bash
docker-compose down
docker volume rm finance_postgres_data
docker-compose up -d
```

### Redis Issues

**Test Redis connection**:
```bash
docker-compose exec redis redis-cli -a your_password ping
# Should return: PONG
```

### Port Conflicts

If you get port binding errors:

1. Check which service is using the port:
```bash
sudo lsof -i :PORT_NUMBER
```

2. Either stop the conflicting service or change the port in `.env`:
```bash
POSTGRES_PORT=5433  # Instead of 5432
```

### Clean Up

**Remove all containers and volumes**:
```bash
docker-compose down -v
```

**Remove unused images**:
```bash
docker system prune -a
```

**Remove specific volume**:
```bash
docker volume rm finance_postgres_data
```

## Network Architecture

All services are connected via the `finance_network` bridge network, allowing:
- Service-to-service communication via container names
- Isolation from other Docker networks
- Custom DNS resolution

**Internal Hostnames**:
- `postgres` - PostgreSQL database
- `redis` - Redis cache
- `rabbitmq` - RabbitMQ broker
- `backend` - Backend API
- `frontend` - Frontend app
- `traefik` - Traefik proxy
- `prometheus` - Metrics server
- `grafana` - Dashboard

## Security Recommendations

For production deployment:

1. **Change all default passwords** in `.env`
2. **Enable HTTPS** in Traefik configuration
3. **Disable insecure API** in Traefik (set `api.insecure: false`)
4. **Use secrets management** for sensitive data
5. **Enable authentication** on exposed services
6. **Configure firewall rules** to restrict external access
7. **Regular backups** of database volumes
8. **Keep images updated**: `docker-compose pull && docker-compose up -d`

## Additional Resources

- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
