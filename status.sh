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

check_health "Finance API" "http://localhost:8100/health"
check_health "Real Estate API" "http://localhost:8101/health"
check_health "Bond.AI API" "http://localhost:8102/health"
check_health "Legacy API" "http://localhost:8103/health"
check_health "Labor API" "http://localhost:8104/health"
check_health "Unified Dashboard" "http://localhost:3100"
check_health "Traefik" "http://localhost:8181"
check_health "Prometheus" "http://localhost:9190"
check_health "Grafana" "http://localhost:3101"
check_health "Keycloak" "http://localhost:8183/health/ready"
check_health "Qdrant" "http://localhost:6333/"
check_health "Neo4j" "http://localhost:7474"
check_health "Elasticsearch" "http://localhost:9200/_cluster/health"
check_health "MinIO" "http://localhost:9100/minio/health/live"

echo ""
