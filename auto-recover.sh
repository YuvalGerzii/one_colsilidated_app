#!/bin/bash
# =============================================================================
# UNIFIED PLATFORM - AUTOMATED RECOVERY SCRIPT
# =============================================================================
# This script monitors service health and automatically attempts recovery
# Features:
# - Intelligent restart logic with backoff
# - Dependency-aware recovery
# - Health history tracking
# - Configurable recovery strategies
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

# Configuration
MAX_RESTART_ATTEMPTS=3
RESTART_BACKOFF_BASE=5  # seconds
CHECK_INTERVAL=30       # seconds
HEALTH_HISTORY_FILE="/tmp/health_history.log"

# Service definitions with dependencies
declare -A SERVICE_DEPS
SERVICE_DEPS["finance-backend"]="postgres redis rabbitmq"
SERVICE_DEPS["realestate-backend"]="postgres redis"
SERVICE_DEPS["bondai-backend"]="postgres redis"
SERVICE_DEPS["bondai-agents"]="postgres ollama"
SERVICE_DEPS["legacy-backend"]="postgres redis qdrant neo4j elasticsearch"
SERVICE_DEPS["labor-backend"]="postgres redis"

declare -A RESTART_COUNTS
declare -A LAST_RESTART_TIME

# Initialize
mkdir -p "$(dirname "$HEALTH_HISTORY_FILE")"

echo ""
echo "=========================================="
echo -e "${CYAN}  AUTOMATED RECOVERY SYSTEM${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Started: $(date)${NC}"
echo -e "${BLUE}Check Interval: ${CHECK_INTERVAL}s${NC}"
echo -e "${BLUE}Max Restart Attempts: ${MAX_RESTART_ATTEMPTS}${NC}"
echo ""

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log_event() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$HEALTH_HISTORY_FILE"
}

check_service_health() {
    local service=$1
    local port=$2

    if curl -sf --connect-timeout 3 "http://localhost:$port/health/ready" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

check_container_running() {
    local container=$1

    if ! command -v docker &> /dev/null; then
        return 1
    fi

    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${container}$"; then
        return 0
    else
        return 1
    fi
}

get_restart_backoff() {
    local count=$1
    echo $((RESTART_BACKOFF_BASE * (2 ** (count - 1))))
}

check_dependencies() {
    local service=$1
    local deps="${SERVICE_DEPS[$service]}"

    if [ -z "$deps" ]; then
        return 0
    fi

    for dep in $deps; do
        if ! check_container_running "unified-$dep"; then
            echo -e "  ${YELLOW}⚠${NC} Dependency $dep not running"
            return 1
        fi
    done

    return 0
}

restart_service() {
    local service=$1
    local container=$2

    # Check if we've exceeded max attempts
    local count=${RESTART_COUNTS[$service]:-0}
    if [ $count -ge $MAX_RESTART_ATTEMPTS ]; then
        echo -e "  ${RED}✗${NC} Max restart attempts reached for $service"
        log_event "ERROR" "Max restart attempts ($MAX_RESTART_ATTEMPTS) reached for $service"
        return 1
    fi

    # Check cooldown period
    local last_restart=${LAST_RESTART_TIME[$service]:-0}
    local now=$(date +%s)
    local backoff=$(get_restart_backoff $((count + 1)))
    local elapsed=$((now - last_restart))

    if [ $elapsed -lt $backoff ] && [ $last_restart -gt 0 ]; then
        echo -e "  ${YELLOW}⏳${NC} Cooldown period: waiting $((backoff - elapsed))s before restart"
        return 1
    fi

    # Check dependencies before restart
    if ! check_dependencies "$service"; then
        echo -e "  ${YELLOW}⚠${NC} Dependencies not ready, skipping restart"
        return 1
    fi

    # Attempt restart
    echo -e "  ${CYAN}↻${NC} Attempting restart of $service (attempt $((count + 1))/$MAX_RESTART_ATTEMPTS)"
    log_event "INFO" "Restarting $service (attempt $((count + 1)))"

    if docker compose restart "$container" > /dev/null 2>&1; then
        RESTART_COUNTS[$service]=$((count + 1))
        LAST_RESTART_TIME[$service]=$now

        echo -e "  ${GREEN}✓${NC} Restart initiated, waiting for service to be ready..."

        # Wait for service to come back
        local wait_time=0
        local max_wait=60
        while [ $wait_time -lt $max_wait ]; do
            sleep 5
            wait_time=$((wait_time + 5))

            case $service in
                "finance-backend")
                    if check_service_health "$service" 8100; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
                "realestate-backend")
                    if check_service_health "$service" 8101; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
                "bondai-backend")
                    if check_service_health "$service" 8102; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
                "legacy-backend")
                    if check_service_health "$service" 8103; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
                "labor-backend")
                    if check_service_health "$service" 8104; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
                "bondai-agents")
                    if check_service_health "$service" 8105; then
                        echo -e "  ${GREEN}✓${NC} $service is healthy after restart"
                        log_event "SUCCESS" "$service recovered successfully"
                        return 0
                    fi
                    ;;
            esac
        done

        echo -e "  ${YELLOW}⚠${NC} $service did not become healthy within ${max_wait}s"
        log_event "WARNING" "$service restart timeout"
        return 1
    else
        echo -e "  ${RED}✗${NC} Failed to restart $service"
        log_event "ERROR" "Failed to restart $service"
        return 1
    fi
}

monitor_service() {
    local service=$1
    local container=$2
    local port=$3

    # Check if container is running
    if ! check_container_running "$container"; then
        echo -e "${RED}✗${NC} Container $container is not running"
        log_event "ERROR" "$container is not running"
        restart_service "$service" "$container"
        return
    fi

    # Check health endpoint
    if ! check_service_health "$service" "$port"; then
        echo -e "${YELLOW}⚠${NC} Service $service is unhealthy (port $port)"
        log_event "WARNING" "$service is unhealthy"
        restart_service "$service" "$container"
        return
    fi

    # Service is healthy - reset restart count if it's been stable
    local last_restart=${LAST_RESTART_TIME[$service]:-0}
    local now=$(date +%s)
    local stable_period=$((RESTART_BACKOFF_BASE * 60))  # 5 minutes

    if [ $((now - last_restart)) -gt $stable_period ] && [ ${RESTART_COUNTS[$service]:-0} -gt 0 ]; then
        echo -e "${GREEN}✓${NC} $service has been stable, resetting restart count"
        RESTART_COUNTS[$service]=0
        log_event "INFO" "$service stable - reset restart count"
    fi
}

# =============================================================================
# MAIN MONITORING LOOP
# =============================================================================

echo -e "${MAGENTA}Starting monitoring loop...${NC}"
echo -e "${BLUE}Press Ctrl+C to stop${NC}"
echo ""

# Trap SIGINT and SIGTERM for graceful shutdown
trap 'echo -e "\n${YELLOW}Shutting down monitoring...${NC}"; exit 0' SIGINT SIGTERM

iteration=0
while true; do
    iteration=$((iteration + 1))
    echo -e "${CYAN}[Check #$iteration - $(date '+%H:%M:%S')]${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Monitor each service
    monitor_service "finance-backend" "finance-backend" 8100
    monitor_service "realestate-backend" "realestate-backend" 8101
    monitor_service "bondai-backend" "bondai-backend" 8102
    monitor_service "bondai-agents" "bondai-agents" 8105
    monitor_service "legacy-backend" "legacy-backend" 8103
    monitor_service "labor-backend" "labor-backend" 8104

    echo ""

    # Show restart statistics
    if [ ${#RESTART_COUNTS[@]} -gt 0 ]; then
        echo -e "${BLUE}Restart Statistics:${NC}"
        for service in "${!RESTART_COUNTS[@]}"; do
            local count=${RESTART_COUNTS[$service]}
            if [ $count -gt 0 ]; then
                echo -e "  $service: $count restarts"
            fi
        done
        echo ""
    fi

    # Wait for next check
    echo -e "${BLUE}Next check in ${CHECK_INTERVAL}s...${NC}"
    echo ""
    sleep $CHECK_INTERVAL
done
