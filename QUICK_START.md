# Quick Start Guide - Unified Platform

Get up and running in minutes with the Unified Platform's intelligent health monitoring and auto-recovery features.

## 🚀 60-Second Quick Start

```bash
# 1. Start the platform with auto-recovery
./smart-start.sh

# 2. Open the health dashboard
open http://localhost:8200

# 3. That's it! ✨
```

---

## 📋 Installation & Prerequisites

### Requirements
- Docker 20.10+ with Docker Compose v2+
- 16GB+ RAM recommended
- 50GB+ free disk space
- Linux, macOS, or Windows with WSL2

### Verify Installation
```bash
docker --version          # Should be 20.10+
docker compose version    # Should be v2.x+
docker info              # Check daemon is running
```

---

## 🎯 Usage Scenarios

### Scenario 1: First Time Setup

**Goal**: Start the platform for the first time with all features.

```bash
# Run setup and start
./setup-and-start.sh

# This will:
# ✓ Check prerequisites
# ✓ Create configuration files
# ✓ Pull Docker images
# ✓ Build and start services
# ✓ Verify health
```

**Access Points:**
- Health Dashboard: http://localhost:8200
- Unified Dashboard: http://localhost:3100
- API Documentation: http://localhost:8100/docs

---

### Scenario 2: Quick Development Start

**Goal**: Start core services quickly for development.

```bash
# Smart start in normal mode (fastest)
./smart-start.sh

# Or minimal mode (infrastructure only)
START_MODE=minimal ./smart-start.sh
```

**What's Running:**
- ✓ PostgreSQL, Redis, Traefik
- ✓ All backend services
- ✓ Health monitoring
- ✓ Auto-recovery

---

### Scenario 3: Production Deployment

**Goal**: Deploy with full monitoring and auto-recovery.

```bash
# Full start with all features
START_MODE=full ENABLE_AUTO_RECOVERY=true ./smart-start.sh

# Monitor health
tail -f /tmp/auto-recover.log &
open http://localhost:8200
```

**Production Features:**
- ✓ All services running
- ✓ Auto-recovery enabled
- ✓ Health monitoring active
- ✓ Prometheus metrics exported

---

### Scenario 4: Debugging Issues

**Goal**: Diagnose and fix service problems.

```bash
# 1. Run comprehensive health check
./verify-health.sh

# 2. Check specific service
curl http://localhost:8100/health/detailed | jq

# 3. View auto-recovery logs
tail -f /tmp/auto-recover.log

# 4. View health history
tail -f /tmp/health_history.log

# 5. Manual restart if needed
docker compose restart finance-backend
```

---

## 📊 Health Monitoring

### Web Dashboard
```bash
# Open beautiful web dashboard
open http://localhost:8200

Features:
- Real-time health status (10s refresh)
- Platform health score
- Service categorization
- Response time metrics
- Status badges
```

### API Access
```bash
# Get all service health
curl http://localhost:8200/api/health | jq

# Get performance metrics
curl http://localhost:8200/api/metrics | jq

# Get Prometheus metrics
curl http://localhost:8200/api/prometheus
```

### CLI Monitoring
```bash
# Quick health check
./verify-health.sh

# Continuous monitoring
watch -n 10 ./verify-health.sh

# Service-specific
curl http://localhost:8100/health/detailed | jq '.checks'
```

---

## 🔄 Auto-Recovery

### Enable Auto-Recovery
```bash
# Included in smart-start.sh by default
./smart-start.sh

# Or manually
./auto-recover.sh &
echo $! > /tmp/auto-recover.pid
```

### Monitor Recovery
```bash
# View real-time logs
tail -f /tmp/auto-recover.log

# View health history
tail -f /tmp/health_history.log

# Check recovery stats in logs
grep "restart" /tmp/health_history.log
```

### Disable Auto-Recovery
```bash
# Stop background process
kill $(cat /tmp/auto-recover.pid)

# Or start without it
ENABLE_AUTO_RECOVERY=false ./smart-start.sh
```

---

## 🛠️ Common Commands

### Start/Stop
```bash
# Smart start (recommended)
./smart-start.sh

# Traditional start
./start.sh

# Setup and start (first time)
./setup-and-start.sh

# Stop all services
./stop.sh

# Restart specific service
docker compose restart finance-backend
```

### Health Checks
```bash
# Comprehensive verification
./verify-health.sh

# Quick status
./status.sh

# Health dashboard
open http://localhost:8200

# Service-specific
curl http://localhost:8100/health/ready
curl http://localhost:8101/health/detailed | jq
```

### Logs & Debugging
```bash
# All logs
docker compose logs -f

# Specific service
docker compose logs -f finance-backend

# Auto-recovery logs
tail -f /tmp/auto-recover.log

# Health history
tail -f /tmp/health_history.log

# Container status
docker compose ps
```

### Monitoring
```bash
# Prometheus metrics
curl http://localhost:8200/api/prometheus

# Performance metrics
curl http://localhost:8200/api/metrics | jq

# Grafana dashboards
open http://localhost:3101  # admin/admin
```

---

## 🎛️ Configuration

### Environment Variables

```bash
# Startup mode
START_MODE=normal|minimal|full

# Auto-recovery
ENABLE_AUTO_RECOVERY=true|false

# Health dashboard
ENABLE_HEALTH_DASHBOARD=true|false

# Timeouts
TIMEOUT=120              # Dependency wait timeout
CHECK_INTERVAL=30        # Auto-recovery check interval
MAX_RESTART_ATTEMPTS=3   # Max auto-restart attempts
```

### Example: Custom Configuration
```bash
# Development setup
START_MODE=normal \
  ENABLE_AUTO_RECOVERY=false \
  ./smart-start.sh

# Production setup
START_MODE=full \
  ENABLE_AUTO_RECOVERY=true \
  MAX_RESTART_ATTEMPTS=5 \
  CHECK_INTERVAL=60 \
  ./smart-start.sh
```

---

## 🔍 Service Access Points

### Dashboards
| Service | URL | Credentials |
|---------|-----|-------------|
| Health Dashboard | http://localhost:8200 | - |
| Unified Dashboard | http://localhost:3100 | - |
| Traefik | http://localhost:8181 | - |
| Grafana | http://localhost:3101 | admin/admin |
| Prometheus | http://localhost:9190 | - |

### Backend APIs
| Service | URL | Docs |
|---------|-----|------|
| Finance | http://localhost:8100 | /docs |
| Real Estate | http://localhost:8101 | /docs |
| Bond.AI | http://localhost:8102 | /docs |
| Bond.AI Agents | http://localhost:8105 | /docs |
| Legacy Systems | http://localhost:8103 | /docs |
| Labor | http://localhost:8104 | /docs |

### Infrastructure
| Service | URL | Port |
|---------|-----|------|
| PostgreSQL | localhost:5532 | 5432 |
| Redis | localhost:6479 | 6379 |
| RabbitMQ | http://localhost:15772 | 15672 |

---

## 📚 Learn More

- **Full Features**: See `ADVANCED_FEATURES.md`
- **Service Health**: See `SERVICE_HEALTH_GUIDE.md`
- **Architecture**: See `PROJECT_STRUCTURE_ANALYSIS.md`
- **Scripts Reference**: See individual script `--help`

---

## 🆘 Troubleshooting

### Platform Won't Start
```bash
# Check prerequisites
docker --version
docker compose version
docker info

# Check disk space
df -h

# View startup logs
./smart-start.sh 2>&1 | tee startup.log
```

### Services Unhealthy
```bash
# Run verification
./verify-health.sh

# Check specific service
docker compose logs -f [service-name]

# Check dependencies
curl http://localhost:8200/api/health | jq '.services.infrastructure'
```

### Auto-Recovery Not Working
```bash
# Check if running
ps aux | grep auto-recover

# View logs
tail -f /tmp/auto-recover.log

# Restart
kill $(cat /tmp/auto-recover.pid)
./auto-recover.sh &
```

### Port Conflicts
```bash
# Check what's using ports
lsof -i :8200  # Health dashboard
lsof -i :8100  # Finance API
# etc.

# Stop conflicting services or change ports in docker-compose.yml
```

---

## 💡 Pro Tips

1. **Use smart-start.sh** - It's the easiest way to get started
2. **Monitor the health dashboard** - Keep http://localhost:8200 open
3. **Enable auto-recovery in production** - Let it handle transient failures
4. **Check logs regularly** - `tail -f /tmp/health_history.log`
5. **Use verify-health.sh** - After deployments and changes
6. **Bookmark the docs** - All endpoints documented at `/docs`

---

## 🎉 Next Steps

After getting started:

1. **Explore the health dashboard** - http://localhost:8200
2. **Try the API endpoints** - http://localhost:8100/docs
3. **Set up Grafana** - http://localhost:3101
4. **Read advanced features** - `ADVANCED_FEATURES.md`
5. **Integrate monitoring** - Add Prometheus scraping
6. **Customize scripts** - Edit for your specific needs

---

## 📞 Support

- **Issues**: Check service logs and health endpoints
- **Documentation**: `ADVANCED_FEATURES.md`, `SERVICE_HEALTH_GUIDE.md`
- **Health Dashboard**: http://localhost:8200
- **Verification**: `./verify-health.sh`

Happy coding! 🚀
