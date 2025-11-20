#!/bin/bash
# =============================================================================
# UNIFIED PLATFORM - COMPREHENSIVE HEALTH VERIFICATION SCRIPT
# =============================================================================
# This script verifies all platform services and their dependencies
# Provides detailed health status with color-coded output
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Timeout for health checks
TIMEOUT=3

echo ""
echo "=========================================="
echo -e "${CYAN}  UNIFIED PLATFORM - HEALTH VERIFICATION${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}$(date)${NC}"
echo ""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

check_endpoint() {
    local name=$1
    local url=$2
    local critical=$3  # "critical" or "optional"

    ((TOTAL_CHECKS++))

    if curl -sf --connect-timeout $TIMEOUT "$url" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} $name is ${GREEN}healthy${NC}"
        ((PASSED_CHECKS++))
        return 0
    else
        if [ "$critical" == "critical" ]; then
            echo -e "  ${RED}✗${NC} $name is ${RED}DOWN${NC} (CRITICAL)"
            ((FAILED_CHECKS++))
        else
            echo -e "  ${YELLOW}⚠${NC} $name is ${YELLOW}unavailable${NC} (optional)"
            ((WARNING_CHECKS++))
        fi
        return 1
    fi
}

check_detailed_endpoint() {
    local name=$1
    local url=$2

    ((TOTAL_CHECKS++))

    response=$(curl -sf --connect-timeout $TIMEOUT "$url" 2>/dev/null)
    if [ $? -eq 0 ]; then
        status=$(echo "$response" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)

        if [ "$status" == "healthy" ] || [ "$status" == "ok" ]; then
            echo -e "  ${GREEN}✓${NC} $name: ${GREEN}$status${NC}"
            ((PASSED_CHECKS++))

            # Show additional info if available
            ready=$(echo "$response" | grep -o '"ready":[^,}]*' | cut -d':' -f2)
            if [ ! -z "$ready" ]; then
                echo -e "    ${CYAN}→${NC} Ready: $ready"
            fi

            return 0
        elif [ "$status" == "degraded" ]; then
            echo -e "  ${YELLOW}⚠${NC} $name: ${YELLOW}$status${NC}"
            ((WARNING_CHECKS++))
            return 1
        else
            echo -e "  ${RED}✗${NC} $name: ${RED}$status${NC}"
            ((FAILED_CHECKS++))
            return 1
        fi
    else
        echo -e "  ${RED}✗${NC} $name is ${RED}not responding${NC}"
        ((FAILED_CHECKS++))
        return 1
    fi
}

check_container() {
    local name=$1
    local container=$2

    ((TOTAL_CHECKS++))

    if command -v docker &> /dev/null; then
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${container}$"; then
            echo -e "  ${GREEN}✓${NC} Container $name is ${GREEN}running${NC}"
            ((PASSED_CHECKS++))
            return 0
        else
            echo -e "  ${RED}✗${NC} Container $name is ${RED}not running${NC}"
            ((FAILED_CHECKS++))
            return 1
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Docker not available - skipping container check"
        ((WARNING_CHECKS++))
        return 1
    fi
}

# =============================================================================
# INFRASTRUCTURE SERVICES
# =============================================================================

echo -e "${MAGENTA}[1/6] Infrastructure Services${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_endpoint "Traefik Dashboard" "http://localhost:8181/api/overview" "critical"
check_endpoint "PostgreSQL" "http://localhost:5532" "critical" || echo -e "    ${CYAN}→${NC} Database port accessible check"
check_endpoint "Redis" "http://localhost:6479" "critical" || echo -e "    ${CYAN}→${NC} Cache port accessible check"
check_endpoint "RabbitMQ Management" "http://localhost:15772" "optional"
check_endpoint "Prometheus" "http://localhost:9190/-/healthy" "optional"
check_endpoint "Grafana" "http://localhost:3101/api/health" "optional"
check_endpoint "Keycloak" "http://localhost:8183" "optional"

echo ""

# =============================================================================
# AI/ML SERVICES
# =============================================================================

echo -e "${MAGENTA}[2/6] AI/ML Infrastructure${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_endpoint "Ollama (LLM)" "http://localhost:11534/api/tags" "optional"
check_endpoint "Weaviate (Vector DB)" "http://localhost:8182/v1/.well-known/ready" "optional"
check_endpoint "Qdrant (Vector DB)" "http://localhost:6333/" "optional"
check_endpoint "Neo4j Browser" "http://localhost:7474" "optional"
check_endpoint "Elasticsearch" "http://localhost:9200/_cluster/health" "optional"
check_endpoint "MinIO API" "http://localhost:9100/minio/health/live" "optional"

echo ""

# =============================================================================
# BACKEND SERVICES
# =============================================================================

echo -e "${MAGENTA}[3/6] Backend Services - Basic Health${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_endpoint "Finance Backend (8100)" "http://localhost:8100/health" "critical"
check_endpoint "Real Estate Backend (8101)" "http://localhost:8101/health" "critical"
check_endpoint "Bond.AI Backend (8102)" "http://localhost:8102/health" "critical"
check_endpoint "Legacy Backend (8103)" "http://localhost:8103/health" "critical"
check_endpoint "Labor Backend (8104)" "http://localhost:8104/health" "critical"
check_endpoint "Bond.AI Agents (8105)" "http://localhost:8105/health" "critical"

echo ""

# =============================================================================
# BACKEND SERVICES - DETAILED CHECKS
# =============================================================================

echo -e "${MAGENTA}[4/6] Backend Services - Detailed Health${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_detailed_endpoint "Finance Backend" "http://localhost:8100/health/detailed"
check_detailed_endpoint "Real Estate Backend" "http://localhost:8101/health/detailed"
check_detailed_endpoint "Legacy Backend" "http://localhost:8103/health/detailed"
check_detailed_endpoint "Labor Backend" "http://localhost:8104/health/detailed"
check_detailed_endpoint "Bond.AI Agents" "http://localhost:8105/health/detailed"

echo ""

# =============================================================================
# READINESS PROBES
# =============================================================================

echo -e "${MAGENTA}[5/6] Service Readiness Probes${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_endpoint "Finance Ready" "http://localhost:8100/health/ready" "critical"
check_endpoint "Real Estate Ready" "http://localhost:8101/health/ready" "critical"
check_endpoint "Legacy Ready" "http://localhost:8103/health/ready" "critical"
check_endpoint "Labor Ready" "http://localhost:8104/health/ready" "critical"
check_endpoint "Bond.AI Agents Ready" "http://localhost:8105/health/ready" "critical"

echo ""

# =============================================================================
# FRONTEND SERVICES
# =============================================================================

echo -e "${MAGENTA}[6/6] Frontend Services${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_endpoint "Unified Dashboard (3100)" "http://localhost:3100" "critical"
check_endpoint "Finance Frontend (3102)" "http://localhost:3102" "optional"
check_endpoint "Real Estate Frontend (3103)" "http://localhost:3103" "optional"
check_endpoint "Bond.AI Frontend (3104)" "http://localhost:3104" "optional"
check_endpoint "Labor Frontend (3105)" "http://localhost:3105" "optional"

echo ""

# =============================================================================
# SUMMARY
# =============================================================================

echo "=========================================="
echo -e "${CYAN}  HEALTH CHECK SUMMARY${NC}"
echo "=========================================="
echo ""

PASS_PERCENT=0
if [ $TOTAL_CHECKS -gt 0 ]; then
    PASS_PERCENT=$((100 * PASSED_CHECKS / TOTAL_CHECKS))
fi

echo -e "Total Checks:    $TOTAL_CHECKS"
echo -e "${GREEN}Passed:${NC}          $PASSED_CHECKS ($PASS_PERCENT%)"
echo -e "${YELLOW}Warnings:${NC}        $WARNING_CHECKS"
echo -e "${RED}Failed:${NC}          $FAILED_CHECKS"
echo ""

if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✓ All critical services are healthy!${NC}"
    EXIT_CODE=0
elif [ $FAILED_CHECKS -lt 5 ]; then
    echo -e "${YELLOW}⚠ Some services are down but platform is partially operational${NC}"
    EXIT_CODE=1
else
    echo -e "${RED}✗ Multiple critical services are down${NC}"
    EXIT_CODE=2
fi

echo ""
echo "=========================================="
echo -e "${BLUE}Troubleshooting:${NC}"
echo "  - View all logs:        docker compose logs -f"
echo "  - View specific service: docker compose logs -f [service-name]"
echo "  - Restart service:      docker compose restart [service-name]"
echo "  - Check status:         docker compose ps"
echo "  - Full restart:         docker compose down && docker compose up -d"
echo "=========================================="
echo ""

exit $EXIT_CODE
