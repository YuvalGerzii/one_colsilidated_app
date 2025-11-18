#!/bin/bash
# =============================================================================
# UNIFIED PLATFORM - STATUS SCRIPT
# =============================================================================

echo "=========================================="
echo "  UNIFIED PLATFORM - Service Status      "
echo "=========================================="
echo ""

# Check Docker services
docker compose ps

echo ""
echo "=========================================="
echo "  Health Check Endpoints                 "
echo "=========================================="
echo ""

# Function to check service health
check_health() {
    local name=$1
    local url=$2

    if curl -s --connect-timeout 2 "$url" > /dev/null 2>&1; then
        echo -e "✓ $name is healthy"
    else
        echo -e "✗ $name is not responding"
    fi
}

check_health "Finance API" "http://localhost:8000/health"
check_health "Real Estate API" "http://localhost:8001/health"
check_health "Bond.AI API" "http://localhost:8002/health"
check_health "Legacy API" "http://localhost:8003/health"
check_health "Labor API" "http://localhost:8004/health"
check_health "Unified Dashboard" "http://localhost:3000"
check_health "Traefik" "http://localhost:8080"
check_health "Prometheus" "http://localhost:9090"
check_health "Grafana" "http://localhost:3001"

echo ""
