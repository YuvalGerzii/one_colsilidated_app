# Advanced Health & Monitoring Features

## Overview

This document describes the advanced health monitoring, auto-recovery, and operational features added to the Unified Platform.

## 🎯 Features Summary

| Feature | Purpose | Script/Service | Status |
|---------|---------|----------------|--------|
| **Health Aggregation** | Unified view of all services | `health-aggregator/` | ✅ Active |
| **Auto-Recovery** | Automatic service restart on failure | `auto-recover.sh` | ✅ Active |
| **Smart Startup** | Intelligent platform initialization | `smart-start.sh` | ✅ Active |
| **Dependency Waiting** | Services wait for dependencies | `wait-for-deps.sh` | ✅ Active |
| **Health Verification** | Comprehensive health checks | `verify-health.sh` | ✅ Active |
| **Performance Metrics** | Response time tracking | Built into health endpoints | ✅ Active |
| **Prometheus Export** | Metrics for monitoring systems | Health aggregator endpoint | ✅ Active |

---

## 1. Health Aggregation Dashboard

### Description
A beautiful, real-time web dashboard that monitors all platform services and provides a unified health view.

### Features
- **Real-time monitoring** - Auto-refreshes every 10 seconds
- **Platform health score** - Percentage-based overall health
- **Service categorization** - Infrastructure, AI/ML, Backend, Frontend, Monitoring
- **Performance metrics** - Response time tracking for all services
- **Status badges** - Visual indicators (Healthy, Degraded, Down, Timeout)
- **Prometheus integration** - Metrics export for external monitoring

### Access
```bash
# Web Dashboard
http://localhost:8200

# JSON API
curl http://localhost:8200/api/health | jq

# Performance Metrics
curl http://localhost:8200/api/metrics | jq

# Prometheus Metrics
curl http://localhost:8200/api/prometheus
```

### API Response Example
```json
{
  "overall_status": "healthy",
  "health_score": 95.5,
  "status_counts": {
    "healthy": 21,
    "degraded": 1,
    "down": 0,
    "timeout": 0
  },
  "services": {
    "backend": {
      "finance": {
        "status": "healthy",
        "response_time": 45.2,
        "details": {
          "status": "healthy",
          "checks": {...}
        }
      }
    }
  }
}
```

### Docker Integration
The health aggregator runs as a containerized service:

```yaml
health-aggregator:
  ports:
    - "8200:8200"
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8200/api/health"]
```

---

## 2. Auto-Recovery System

### Description
Intelligent monitoring and automatic recovery of failed services with dependency-aware restart logic.

### Features
- **Continuous monitoring** - Checks services every 30 seconds
- **Dependency awareness** - Only restarts if dependencies are healthy
- **Exponential backoff** - Progressive delays between restart attempts (5s, 10s, 20s, 40s...)
- **Max attempts** - Prevents infinite restart loops (default: 3 attempts)
- **Health history** - Logs all events to `/tmp/health_history.log`
- **Automatic reset** - Clears restart count after 5 minutes of stability

### Usage
```bash
# Start auto-recovery
./auto-recover.sh

# Start in background
nohup ./auto-recover.sh > /tmp/auto-recover.log 2>&1 &
echo $! > /tmp/auto-recover.pid

# View logs
tail -f /tmp/auto-recover.log
tail -f /tmp/health_history.log

# Stop auto-recovery
kill $(cat /tmp/auto-recover.pid)
```

### Configuration
Edit `auto-recover.sh` to customize:

```bash
MAX_RESTART_ATTEMPTS=3     # Maximum restart attempts per service
RESTART_BACKOFF_BASE=5     # Base backoff time in seconds
CHECK_INTERVAL=30          # Health check frequency in seconds
```

### Service Dependencies
```bash
SERVICE_DEPS["finance-backend"]="postgres redis rabbitmq"
SERVICE_DEPS["realestate-backend"]="postgres redis"
SERVICE_DEPS["bondai-agents"]="postgres ollama"
# ... add more as needed
```

### Recovery Process
1. **Detect failure** - Service health check fails
2. **Check dependencies** - Ensure required services are running
3. **Check restart count** - Verify not exceeded max attempts
4. **Check cooldown** - Respect exponential backoff period
5. **Restart service** - Execute `docker compose restart`
6. **Verify recovery** - Wait up to 60s for service to become healthy
7. **Log result** - Record success or failure

### Example Output
```
[Check #5 - 14:32:15]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✗ Container finance-backend is not running
  ↻ Attempting restart of finance-backend (attempt 1/3)
  ✓ Restart initiated, waiting for service to be ready...
  ✓ finance-backend is healthy after restart

Restart Statistics:
  finance-backend: 1 restarts

Next check in 30s...
```

---

## 3. Smart Startup

### Description
Intelligent platform initialization with health verification, optional services, and informative output.

### Features
- **Pre-flight checks** - Validates Docker, disk space, system requirements
- **Multiple modes** - minimal, normal, full
- **Health verification** - Runs comprehensive checks after startup
- **Auto-recovery integration** - Optionally starts background monitoring
- **Helpful output** - Shows all access points and commands

### Usage
```bash
# Normal startup (core services)
./smart-start.sh

# Minimal startup (infrastructure only)
START_MODE=minimal ./smart-start.sh

# Full startup (all services)
START_MODE=full ./smart-start.sh

# Without auto-recovery
ENABLE_AUTO_RECOVERY=false ./smart-start.sh

# Custom configuration
START_MODE=normal ENABLE_AUTO_RECOVERY=true ./smart-start.sh
```

### Startup Modes

#### Minimal Mode
Starts only essential infrastructure:
- PostgreSQL
- Redis
- Traefik

#### Normal Mode (Default)
Starts core platform services:
- All infrastructure (PostgreSQL, Redis, RabbitMQ, Traefik)
- All backend services (Finance, Real Estate, Bond.AI, Legacy, Labor)
- Health aggregator

#### Full Mode
Starts everything defined in docker-compose.yml:
- All infrastructure services
- All AI/ML services (Ollama, Weaviate, Qdrant, Neo4j, etc.)
- All backend and frontend services
- All monitoring services (Prometheus, Grafana)

### Output Example
```
==========================================
  SMART STARTUP - UNIFIED PLATFORM
==========================================

Mode: normal
Auto-Recovery: true
Health Dashboard: true

[1/5] Pre-flight Checks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Docker installed: 24.0.7
✓ Docker Compose: v2.23.0
✓ Docker daemon is running
✓ Disk space: 85GB available

[2/5] Starting Services
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting core services
Waiting for services to initialize (60s)...

[3/5] Health Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

[4/5] Optional Services
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Starting auto-recovery service in background...
✓ Auto-recovery running (PID: 12345)

[5/5] Startup Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Platform is ready!
```

---

## 4. Dependency Waiting

### Description
Utility script to wait for service dependencies before starting an application. Can be used as a Docker entrypoint wrapper.

### Features
- **TCP connection waiting** - Wait for ports to be open
- **HTTP endpoint waiting** - Wait for HTTP services to respond
- **Configurable timeout** - Default 120s, customizable
- **Retry interval** - Default 2s, customizable
- **Multiple dependencies** - Check multiple services simultaneously

### Usage

#### Standalone
```bash
# Wait for PostgreSQL and Redis
./wait-for-deps.sh -h postgres:5432 -h redis:6379 -- python app.py

# Wait for HTTP endpoints
./wait-for-deps.sh -u http://postgres:5432 -u http://redis:6379 -- npm start

# Custom timeout and interval
TIMEOUT=180 RETRY_INTERVAL=5 ./wait-for-deps.sh -h db:5432 -- ./start.sh
```

#### Docker Entrypoint
```dockerfile
FROM python:3.11-slim

COPY wait-for-deps.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-deps.sh

ENTRYPOINT ["wait-for-deps.sh", "-h", "postgres:5432", "-h", "redis:6379", "--"]
CMD ["python", "app.py"]
```

#### Docker Compose
```yaml
services:
  app:
    build: .
    command: >
      sh -c "
        ./wait-for-deps.sh -h postgres:5432 -h redis:6379 --
        python app.py
      "
    depends_on:
      - postgres
      - redis
```

### Options
- `-h HOST:PORT` - Wait for TCP connection (can specify multiple)
- `-u URL` - Wait for HTTP endpoint (can specify multiple)
- `-t TIMEOUT` - Timeout in seconds (default: 120)
- `-i INTERVAL` - Retry interval in seconds (default: 2)

---

## 5. Enhanced Health Endpoints

All backend services now include enhanced health endpoints with additional features:

### New Capabilities
- **Performance metrics** - Response time tracking
- **Dependency status** - Individual component health
- **Fallback information** - What happens when dependencies fail
- **Critical vs Optional** - Distinguishes critical from optional dependencies
- **System information** - Python version, uptime, etc.

### Endpoint Comparison

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| `/health` | Basic check | Quick liveness verification |
| `/health/live` | Liveness probe | Kubernetes liveness checks |
| `/health/ready` | Readiness probe | Load balancer health checks |
| `/health/detailed` | Full diagnostics | Troubleshooting, monitoring |

### Example: Finance Backend `/health/detailed`
```json
{
  "status": "healthy",
  "service": "finance-backend",
  "timestamp": 1234567890.123,
  "checks": {
    "database": {
      "healthy": true,
      "critical": true,
      "status": "operational"
    },
    "redis": {
      "healthy": true,
      "configured": true,
      "critical": true
    },
    "ollama": {
      "healthy": false,
      "error": "Service unavailable",
      "critical": false,
      "fallback": "LLM features disabled"
    }
  },
  "system": {
    "python_version": "3.11.0",
    "uptime": 12345.67
  },
  "fallback_info": {
    "ollama": "LLM features will be disabled if unavailable",
    "weaviate": "Vector search will be disabled if unavailable",
    "rabbitmq": "Background tasks may be affected if unavailable"
  }
}
```

---

## 6. Prometheus Integration

### Description
Export health and performance metrics in Prometheus format for integration with monitoring systems.

### Metrics Endpoint
```bash
curl http://localhost:8200/api/prometheus
```

### Sample Output
```
service_health{service="finance",category="backend"} 1
service_response_time_ms{service="finance",category="backend"} 45.2
service_health{service="postgres",category="infrastructure"} 1
service_response_time_ms{service="postgres",category="infrastructure"} 12.5
platform_health_score 95.5
```

### Prometheus Configuration
Add to `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'platform-health'
    static_configs:
      - targets: ['health-aggregator:8200']
    metrics_path: '/api/prometheus'
    scrape_interval: 30s
```

### Grafana Dashboard
Use the provided metrics to create dashboards:

1. **Platform Health Score** - Gauge showing overall health percentage
2. **Service Status Grid** - Heatmap of service health (1=healthy, 0=down)
3. **Response Time Chart** - Line graph of service response times
4. **Status Distribution** - Pie chart of healthy/degraded/down services

---

## 7. Best Practices

### For Development
```bash
# Quick start with auto-recovery
./smart-start.sh

# View aggregated health
open http://localhost:8200

# Monitor specific service
curl http://localhost:8100/health/detailed | jq
```

### For Production
```bash
# Full startup with all services
START_MODE=full ./smart-start.sh

# Enable auto-recovery in background
ENABLE_AUTO_RECOVERY=true ./smart-start.sh

# Monitor health logs
tail -f /tmp/health_history.log

# Set up Prometheus scraping
# Add health aggregator to prometheus.yml
```

### For CI/CD
```bash
# Health verification in pipeline
./verify-health.sh
if [ $? -ne 0 ]; then
  echo "Health check failed"
  exit 1
fi

# Quick health check
curl -f http://localhost:8200/api/health || exit 1
```

### For Debugging
```bash
# Check detailed service health
curl http://localhost:8100/health/detailed | jq '.checks'

# View auto-recovery logs
tail -f /tmp/auto-recover.log

# Check health history
tail -f /tmp/health_history.log

# Monitor container status
docker compose ps
docker compose logs -f [service-name]
```

---

## 8. Troubleshooting

### Health Dashboard Not Loading
```bash
# Check if service is running
docker ps | grep health-aggregator

# View logs
docker compose logs health-aggregator

# Restart service
docker compose restart health-aggregator
```

### Auto-Recovery Not Working
```bash
# Check if process is running
ps aux | grep auto-recover

# View logs
tail -f /tmp/auto-recover.log

# Restart manually
kill $(cat /tmp/auto-recover.pid)
./auto-recover.sh &
```

### Service Stuck in Restart Loop
```bash
# Stop auto-recovery
kill $(cat /tmp/auto-recover.pid)

# Check health history
tail -100 /tmp/health_history.log | grep [service-name]

# Manual intervention
docker compose restart [service-name]
```

### Dependencies Not Ready
```bash
# Use wait-for-deps with verbose output
./wait-for-deps.sh -h postgres:5432 -h redis:6379 -- echo "Ready!"

# Check dependency health
curl http://localhost:8200/api/health | jq '.services.infrastructure'
```

---

## 9. Performance Considerations

### Resource Usage

| Component | CPU | Memory | Disk I/O |
|-----------|-----|--------|----------|
| Health Aggregator | ~5% | ~50MB | Low |
| Auto-Recovery | ~2% | ~10MB | Low |
| Health Checks | ~1% | ~5MB | Low |

### Optimization Tips

1. **Adjust check intervals** - Reduce frequency if needed
   ```bash
   CHECK_INTERVAL=60  # Check every 60s instead of 30s
   ```

2. **Limit history** - Prevent log file growth
   ```bash
   # Rotate health history
   echo "" > /tmp/health_history.log
   ```

3. **Selective monitoring** - Monitor only critical services
   ```bash
   # Edit auto-recover.sh to remove non-critical services
   ```

4. **Disable in development** - Save resources when not needed
   ```bash
   ENABLE_AUTO_RECOVERY=false ./smart-start.sh
   ```

---

## 10. Future Enhancements

- [ ] Email/Slack notifications on service failures
- [ ] Historical health data persistence (TimescaleDB)
- [ ] Advanced alerting rules and thresholds
- [ ] Service dependency graph visualization
- [ ] Automated rollback on failed deployments
- [ ] Circuit breaker pattern implementation
- [ ] Health trend analysis and predictions
- [ ] Mobile app for health monitoring

---

## Support

For issues or questions:
1. Check health dashboard: http://localhost:8200
2. Review logs: `/tmp/health_history.log`, `/tmp/auto-recover.log`
3. Run verification: `./verify-health.sh`
4. Check documentation: `SERVICE_HEALTH_GUIDE.md`
