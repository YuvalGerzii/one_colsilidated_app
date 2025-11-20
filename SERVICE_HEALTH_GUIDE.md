# Service Health & Dependency Guide

## Overview

This document provides comprehensive information about service health checks, dependencies, and fallback mechanisms in the Unified Platform.

## Service Architecture

### Infrastructure Services (Critical)
- **PostgreSQL** - Primary database for all services
- **Redis** - Caching and session management
- **Traefik** - API Gateway and reverse proxy

### Infrastructure Services (Optional)
- **RabbitMQ** - Message queue for async tasks
- **Keycloak** - Authentication and authorization
- **Prometheus** - Metrics collection
- **Grafana** - Monitoring dashboards

### AI/ML Services (Optional)
- **Ollama** - Local LLM service
- **Weaviate** - Vector database
- **Qdrant** - Vector database (Legacy systems)
- **Neo4j** - Graph database (Legacy systems)
- **Elasticsearch** - Search and analytics
- **MinIO** - Object storage

### Application Services
1. **Finance Backend** (Port 8100)
2. **Real Estate Backend** (Port 8101)
3. **Bond.AI Backend** (Port 8102)
4. **Bond.AI Python Agents** (Port 8105)
5. **Legacy Systems Backend** (Port 8103)
6. **Labor Transformation Backend** (Port 8104)

## Health Check Endpoints

All application services now support the following health check endpoints:

### `/health`
**Basic health check** - Lightweight probe for quick status verification
```bash
curl http://localhost:8100/health
```
Response:
```json
{
  "status": "healthy",
  "service": "finance-backend",
  "timestamp": 1234567890
}
```

### `/health/live`
**Liveness probe** - Kubernetes-style check to verify the service is alive
```bash
curl http://localhost:8100/health/live
```
Response:
```json
{
  "alive": true,
  "service": "finance-backend",
  "uptime": 12345.67
}
```

### `/health/ready`
**Readiness probe** - Checks if service is ready to accept traffic
```bash
curl http://localhost:8100/health/ready
```
Response:
```json
{
  "ready": true,
  "service": "finance-backend",
  "checks": {
    "database": {"healthy": true, "critical": true},
    "redis": {"healthy": true, "critical": true}
  }
}
```

### `/health/detailed`
**Detailed health check** - Comprehensive status of all dependencies
```bash
curl http://localhost:8100/health/detailed
```
Response includes:
- Overall service status
- Individual component checks
- System information
- Fallback information

## Service Dependencies

### Finance Backend
**Critical Dependencies:**
- PostgreSQL (database)
- Redis (caching)

**Optional Dependencies:**
- RabbitMQ (background tasks)
- Ollama (LLM features)
- Weaviate (vector search)

**Fallbacks:**
- LLM features disabled if Ollama unavailable
- Vector search disabled if Weaviate unavailable
- Background tasks may be affected if RabbitMQ unavailable

### Real Estate Backend
**Critical Dependencies:**
- PostgreSQL (database)
- Redis (caching)

**Optional Dependencies:**
- Ollama (LLM and AI features)

**Fallbacks:**
- LLM and AI features disabled if Ollama unavailable
- Caching degraded if Redis unavailable

### Bond.AI Backend
**Critical Dependencies:**
- PostgreSQL (database)
- Redis (session management)

**Optional Dependencies:**
- Bond.AI Python Agents (enhanced matching)
- Ollama (LLM features)

**Fallbacks:**
- Basic matching without enhanced psychometric analysis
- LLM features disabled if unavailable

### Bond.AI Python Agents
**Critical Dependencies:**
- Agents loaded successfully

**Optional Dependencies:**
- PostgreSQL (persistent storage)
- Ollama (LLM features)

**Fallbacks:**
- In-memory processing if database unavailable
- Limited LLM features if Ollama unavailable

### Legacy Systems Backend
**Critical Dependencies:**
- PostgreSQL (database)
- Redis (caching)

**Optional Dependencies:**
- Ollama (LLM features)
- Qdrant (vector search)
- Neo4j (knowledge graph)
- Elasticsearch (advanced search)
- MinIO (object storage)

**Fallbacks:**
- LLM features disabled if Ollama unavailable
- Vector search disabled if Qdrant unavailable
- Knowledge graph features disabled if Neo4j unavailable
- Advanced search disabled if Elasticsearch unavailable
- Object storage features disabled if MinIO unavailable

### Labor Transformation Backend
**Critical Dependencies:**
- PostgreSQL (database)
- Redis (caching)

**Fallbacks:**
- Service will start with warnings if dependencies are unavailable

## Verification Scripts

### Quick Health Check
```bash
./status.sh
```
Performs basic health checks on all services.

### Comprehensive Verification
```bash
./verify-health.sh
```
Performs detailed health checks including:
- Infrastructure services
- AI/ML services
- Backend services (basic and detailed)
- Readiness probes
- Frontend services

Exit codes:
- `0` - All critical services healthy
- `1` - Some services down, platform partially operational
- `2` - Multiple critical services down

### Setup and Start
```bash
./setup-and-start.sh
```
Complete setup with health verification:
1. Checks prerequisites
2. Creates required configurations
3. Pulls Docker images
4. Builds and starts services
5. Verifies infrastructure services
6. Verifies application services

## Troubleshooting

### Service Not Responding
```bash
# View logs for specific service
docker compose logs -f [service-name]

# Check service status
docker compose ps

# Restart specific service
docker compose restart [service-name]
```

### Database Connection Issues
```bash
# Check PostgreSQL status
docker compose logs -f postgres

# Verify database is healthy
curl http://localhost:5532 || docker compose restart postgres
```

### Redis Connection Issues
```bash
# Check Redis status
docker compose logs -f redis

# Test Redis connectivity
docker compose exec redis redis-cli ping
```

### Service Degraded Status
When a service shows "degraded" status:
1. Check `/health/detailed` endpoint for specific component failures
2. Review fallback information to understand impact
3. Decide if optional dependencies need to be restored
4. Check service logs for error details

### Complete System Restart
```bash
# Stop all services
./stop.sh

# Start all services
./start.sh

# Or combined restart
docker compose down && docker compose up -d

# Wait for services to initialize
sleep 60

# Verify health
./verify-health.sh
```

## Monitoring and Alerting

### Prometheus Metrics
Access metrics at: `http://localhost:9190`

### Grafana Dashboards
Access dashboards at: `http://localhost:3101` (admin/admin)

### Health Check Intervals
- Basic health: Every 30 seconds
- Readiness probe: Every 30 seconds
- Liveness probe: Every 60 seconds

## Best Practices

1. **Always check readiness before routing traffic** - Use `/health/ready` endpoint
2. **Monitor detailed health periodically** - Check `/health/detailed` for early warning signs
3. **Understand fallback behavior** - Know what features are affected when optional services are down
4. **Use verification scripts** - Run `./verify-health.sh` after deployments
5. **Review logs regularly** - Check service logs for warnings and errors
6. **Test degraded scenarios** - Verify application behavior when optional services are unavailable

## API Documentation

Each service provides Swagger/OpenAPI documentation:
- Finance API: http://localhost:8100/docs
- Real Estate API: http://localhost:8101/docs
- Bond.AI API: http://localhost:8102/docs
- Legacy API: http://localhost:8103/docs
- Labor API: http://localhost:8104/docs
- Bond.AI Agents: http://localhost:8105/docs

## Support

For issues or questions:
1. Check service logs: `docker compose logs -f [service-name]`
2. Run verification script: `./verify-health.sh`
3. Review this documentation
4. Check individual service README files
