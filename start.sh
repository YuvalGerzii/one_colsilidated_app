#!/bin/bash
# =============================================================================
# UNIFIED PLATFORM - STARTUP SCRIPT
# =============================================================================

set -e

echo "=========================================="
echo "  UNIFIED PLATFORM - Starting Services   "
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Make PostgreSQL init script executable
chmod +x ./config/postgres/init-multiple-dbs.sh

# Function to start services in groups
start_infrastructure() {
    echo -e "${BLUE}Starting infrastructure services...${NC}"
    docker compose up -d traefik postgres redis rabbitmq ollama weaviate prometheus grafana
    echo -e "${GREEN}Infrastructure services started!${NC}"
}

start_backends() {
    echo -e "${BLUE}Starting backend services...${NC}"
    docker compose up -d finance-backend realestate-backend bondai-backend bondai-agents legacy-backend labor-backend
    echo -e "${GREEN}Backend services started!${NC}"
}

start_frontends() {
    echo -e "${BLUE}Starting frontend services...${NC}"
    docker compose up -d unified-dashboard finance-frontend realestate-frontend bondai-frontend labor-frontend
    echo -e "${GREEN}Frontend services started!${NC}"
}

start_workers() {
    echo -e "${BLUE}Starting worker services...${NC}"
    docker compose up -d finance-celery
    echo -e "${GREEN}Worker services started!${NC}"
}

# Parse command line arguments
case "${1:-all}" in
    infrastructure)
        start_infrastructure
        ;;
    backends)
        start_backends
        ;;
    frontends)
        start_frontends
        ;;
    workers)
        start_workers
        ;;
    all)
        start_infrastructure
        echo ""
        echo "Waiting for infrastructure to be ready..."
        sleep 10
        start_backends
        echo ""
        echo "Waiting for backends to be ready..."
        sleep 5
        start_frontends
        start_workers
        ;;
    *)
        echo "Usage: $0 {infrastructure|backends|frontends|workers|all}"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo -e "${GREEN}  Services Started Successfully!${NC}"
echo "=========================================="
echo ""
echo "Access points:"
echo "  - Unified Dashboard: http://localhost:3100"
echo "  - Traefik Dashboard: http://localhost:8181"
echo "  - Grafana:           http://localhost:3101"
echo "  - Prometheus:        http://localhost:9190"
echo ""
echo "Platform UIs:"
echo "  - Finance:           http://localhost:3102"
echo "  - Real Estate:       http://localhost:3103"
echo "  - Bond.AI:           http://localhost:3104"
echo "  - Labor:             http://localhost:3105"
echo ""
echo "APIs:"
echo "  - Finance API:       http://localhost:8100"
echo "  - Real Estate API:   http://localhost:8101"
echo "  - Bond.AI API:       http://localhost:8102"
echo "  - Legacy API:        http://localhost:8103"
echo "  - Labor API:         http://localhost:8104"
echo ""
echo "To view logs: docker compose logs -f [service-name]"
echo "To stop: ./stop.sh"
echo ""
