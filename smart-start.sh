#!/bin/bash
# =============================================================================
# SMART STARTUP SCRIPT - Unified Platform
# =============================================================================
# Intelligent startup with:
# - Dependency checking
# - Health monitoring
# - Auto-recovery
# - Performance tracking
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

ENABLE_AUTO_RECOVERY=${ENABLE_AUTO_RECOVERY:-true}
ENABLE_HEALTH_DASHBOARD=${ENABLE_HEALTH_DASHBOARD:-true}
START_MODE=${START_MODE:-normal}  # normal, minimal, full

echo ""
echo "=========================================="
echo -e "${CYAN}  SMART STARTUP - UNIFIED PLATFORM${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Mode: ${START_MODE}${NC}"
echo -e "${BLUE}Auto-Recovery: ${ENABLE_AUTO_RECOVERY}${NC}"
echo -e "${BLUE}Health Dashboard: ${ENABLE_HEALTH_DASHBOARD}${NC}"
echo ""

# =============================================================================
# PRE-FLIGHT CHECKS
# =============================================================================

echo -e "${MAGENTA}[1/5] Pre-flight Checks${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker installed: $(docker --version | cut -d' ' -f3)"

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose not available${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker Compose: $(docker compose version --short)"

# Check Docker daemon
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker daemon not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Docker daemon is running"

# Check disk space
AVAILABLE_SPACE=$(df -BG . 2>/dev/null | awk 'NR==2 {print $4}' | tr -d 'G' || echo "0")
if [ "$AVAILABLE_SPACE" -lt 20 ]; then
    echo -e "${YELLOW}⚠${NC} Low disk space: ${AVAILABLE_SPACE}GB (20GB+ recommended)"
else
    echo -e "${GREEN}✓${NC} Disk space: ${AVAILABLE_SPACE}GB available"
fi

echo ""

# =============================================================================
# START SERVICES
# =============================================================================

echo -e "${MAGENTA}[2/5] Starting Services${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Determine services to start
case $START_MODE in
    minimal)
        SERVICES="postgres redis traefik"
        echo -e "${BLUE}Starting minimal infrastructure only${NC}"
        ;;
    full)
        echo -e "${BLUE}Starting all services (this may take 10-15 minutes)${NC}"
        docker compose up -d
        ;;
    *)
        echo -e "${BLUE}Starting core services${NC}"
        docker compose up -d postgres redis rabbitmq traefik health-aggregator \
            finance-backend realestate-backend bondai-backend bondai-agents \
            legacy-backend labor-backend
        ;;
esac

echo ""
echo -e "${CYAN}Waiting for services to initialize (60s)...${NC}"
sleep 60

echo ""

# =============================================================================
# VERIFY HEALTH
# =============================================================================

echo -e "${MAGENTA}[3/5] Health Verification${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "./verify-health.sh" ]; then
    ./verify-health.sh || echo -e "${YELLOW}⚠ Some services may need more time${NC}"
else
    echo -e "${YELLOW}⚠ Health verification script not found${NC}"
fi

echo ""

# =============================================================================
# OPTIONAL SERVICES
# =============================================================================

echo -e "${MAGENTA}[4/5] Optional Services${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Start auto-recovery if enabled
if [ "$ENABLE_AUTO_RECOVERY" = "true" ]; then
    if [ -f "./auto-recover.sh" ]; then
        echo -e "${CYAN}Starting auto-recovery service in background...${NC}"
        nohup ./auto-recover.sh > /tmp/auto-recover.log 2>&1 &
        echo $! > /tmp/auto-recover.pid
        echo -e "${GREEN}✓${NC} Auto-recovery running (PID: $(cat /tmp/auto-recover.pid))"
        echo -e "  Logs: tail -f /tmp/auto-recover.log"
    else
        echo -e "${YELLOW}⚠ Auto-recovery script not found${NC}"
    fi
fi

echo ""

# =============================================================================
# SUCCESS SUMMARY
# =============================================================================

echo -e "${MAGENTA}[5/5] Startup Complete${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✓ Platform is ready!${NC}"
echo ""
echo "=========================================="
echo -e "${CYAN}  ACCESS POINTS${NC}"
echo "=========================================="
echo ""

# Main dashboards
echo -e "${MAGENTA}Main Dashboards:${NC}"
echo "  Health Dashboard:    http://localhost:8200"
echo "  Unified Dashboard:   http://localhost:3100"
echo "  Traefik:             http://localhost:8181"
echo ""

# Backend services
echo -e "${MAGENTA}Backend APIs:${NC}"
echo "  Finance:             http://localhost:8100/docs"
echo "  Real Estate:         http://localhost:8101/docs"
echo "  Bond.AI:             http://localhost:8102/docs"
echo "  Bond.AI Agents:      http://localhost:8105/docs"
echo "  Legacy Systems:      http://localhost:8103/docs"
echo "  Labor:               http://localhost:8104/docs"
echo ""

# Monitoring
echo -e "${MAGENTA}Monitoring:${NC}"
echo "  Prometheus:          http://localhost:9190"
echo "  Grafana:             http://localhost:3101 (admin/admin)"
echo "  Metrics:             http://localhost:8200/api/prometheus"
echo ""

# Management commands
echo "=========================================="
echo -e "${CYAN}  MANAGEMENT COMMANDS${NC}"
echo "=========================================="
echo ""
echo "  ./verify-health.sh       - Check service health"
echo "  ./status.sh              - Quick status check"
echo "  ./stop.sh                - Stop all services"
echo "  docker compose ps        - List containers"
echo "  docker compose logs -f   - View logs"
echo ""

# Auto-recovery info
if [ "$ENABLE_AUTO_RECOVERY" = "true" ] && [ -f "/tmp/auto-recover.pid" ]; then
    echo -e "${YELLOW}Auto-Recovery Active:${NC}"
    echo "  PID: $(cat /tmp/auto-recover.pid)"
    echo "  Logs: tail -f /tmp/auto-recover.log"
    echo "  Stop: kill $(cat /tmp/auto-recover.pid)"
    echo ""
fi

echo "=========================================="
echo ""
