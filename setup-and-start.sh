#!/bin/bash
# =============================================================================
# UNIFIED PLATFORM - COMPLETE SETUP AND START SCRIPT
# =============================================================================
# This script:
# 1. Checks and installs prerequisites
# 2. Downloads all Docker images
# 3. Builds all services
# 4. Starts the platform
# 5. Verifies all components are running
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters for summary
PASSED=0
FAILED=0
WARNINGS=0

echo ""
echo "=========================================="
echo -e "${CYAN}  UNIFIED PLATFORM - SETUP & START${NC}"
echo "=========================================="
echo ""

# =============================================================================
# STEP 1: CHECK PREREQUISITES
# =============================================================================

echo -e "${BLUE}[1/6] Checking prerequisites...${NC}"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}ERROR: Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker installed: $(docker --version)"

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}ERROR: Docker Compose is not available${NC}"
    echo "Please install Docker Compose or update Docker Desktop"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker Compose: $(docker compose version --short)"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Docker daemon is not running${NC}"
    echo "Please start Docker Desktop or the Docker service"
    exit 1
fi
echo -e "  ${GREEN}✓${NC} Docker daemon is running"

# Check available memory
if command -v sysctl &> /dev/null; then
    TOTAL_MEM=$(sysctl -n hw.memsize 2>/dev/null || echo "0")
    TOTAL_MEM_GB=$((TOTAL_MEM / 1024 / 1024 / 1024))
    if [ "$TOTAL_MEM_GB" -lt 16 ]; then
        echo -e "  ${YELLOW}⚠${NC} System memory: ${TOTAL_MEM_GB}GB (16GB+ recommended)"
        ((WARNINGS++))
    else
        echo -e "  ${GREEN}✓${NC} System memory: ${TOTAL_MEM_GB}GB"
    fi
fi

# Check available disk space
AVAILABLE_SPACE=$(df -BG . 2>/dev/null | awk 'NR==2 {print $4}' | tr -d 'G' || echo "0")
if [ "$AVAILABLE_SPACE" -lt 50 ]; then
    echo -e "  ${YELLOW}⚠${NC} Disk space: ${AVAILABLE_SPACE}GB available (50GB+ recommended)"
    ((WARNINGS++))
else
    echo -e "  ${GREEN}✓${NC} Disk space: ${AVAILABLE_SPACE}GB available"
fi

echo ""

# =============================================================================
# STEP 2: CREATE REQUIRED DIRECTORIES AND FILES
# =============================================================================

echo -e "${BLUE}[2/6] Creating required directories and files...${NC}"
echo ""

# Create config directories if they don't exist
mkdir -p ./config/postgres
mkdir -p ./config/prometheus
mkdir -p ./config/grafana/provisioning
mkdir -p ./config/traefik

# Create PostgreSQL init script if it doesn't exist
if [ ! -f "./config/postgres/init-multiple-dbs.sh" ]; then
    cat > ./config/postgres/init-multiple-dbs.sh << 'INITDB'
#!/bin/bash
set -e
set -u

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_database $db
    done
    echo "Multiple databases created"
fi
INITDB
    chmod +x ./config/postgres/init-multiple-dbs.sh
    echo -e "  ${GREEN}✓${NC} Created PostgreSQL init script"
fi

# Create Prometheus config if it doesn't exist
if [ ! -f "./config/prometheus/prometheus.yml" ]; then
    cat > ./config/prometheus/prometheus.yml << 'PROMCONFIG'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'traefik'
    static_configs:
      - targets: ['traefik:8080']
PROMCONFIG
    echo -e "  ${GREEN}✓${NC} Created Prometheus config"
fi

# Create .env file if it doesn't exist
if [ ! -f "./.env" ]; then
    cat > ./.env << 'ENVFILE'
# PostgreSQL
POSTGRES_USER=unified_user
POSTGRES_PASSWORD=unified_password

# Redis
REDIS_PASSWORD=unified_redis_pass

# RabbitMQ
RABBITMQ_USER=unified_rabbit
RABBITMQ_PASSWORD=unified_rabbit_pass

# Neo4j
NEO4J_PASSWORD=enterprise_pass

# MinIO
MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin

# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# Grafana
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin
ENVFILE
    echo -e "  ${GREEN}✓${NC} Created .env file with default values"
else
    echo -e "  ${GREEN}✓${NC} .env file exists"
fi

echo ""

# =============================================================================
# STEP 3: PULL DOCKER IMAGES
# =============================================================================

echo -e "${BLUE}[3/6] Pulling Docker images...${NC}"
echo ""

# List of images to pull
IMAGES=(
    "traefik:v2.10"
    "ankane/pgvector:v0.5.1"
    "redis:7-alpine"
    "rabbitmq:3-management-alpine"
    "ollama/ollama:latest"
    "semitechnologies/weaviate:latest"
    "qdrant/qdrant:latest"
    "neo4j:5-community"
    "docker.elastic.co/elasticsearch/elasticsearch:8.11.0"
    "minio/minio:latest"
    "prom/prometheus:latest"
    "grafana/grafana:latest"
    "quay.io/keycloak/keycloak:23.0"
    "nginx:alpine"
    "node:18-alpine"
    "python:3.11-slim"
)

for image in "${IMAGES[@]}"; do
    echo -n "  Pulling $image... "
    if docker pull "$image" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠ (may be pulled during build)${NC}"
        ((WARNINGS++))
    fi
done

echo ""

# =============================================================================
# STEP 4: BUILD AND START SERVICES
# =============================================================================

echo -e "${BLUE}[4/6] Building and starting services...${NC}"
echo ""

# Stop any existing services
echo "  Stopping existing services..."
docker compose down --remove-orphans 2>/dev/null || true

# Build and start all services
echo "  Building all services (this may take 5-15 minutes)..."
if docker compose up -d --build 2>&1 | tee /tmp/docker-build.log | grep -E "Built|Started|Creating|Pulling"; then
    echo -e "  ${GREEN}✓${NC} Services built and started"
else
    echo -e "  ${YELLOW}⚠${NC} Some services may have issues, checking status..."
    ((WARNINGS++))
fi

echo ""
echo "  Waiting for services to initialize (60 seconds)..."
sleep 60

# =============================================================================
# STEP 5: VERIFY INFRASTRUCTURE SERVICES
# =============================================================================

echo ""
echo -e "${BLUE}[5/6] Verifying infrastructure services...${NC}"
echo ""

check_service() {
    local name=$1
    local url=$2
    local container=$3

    # First check if container is running
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        # Then check if service responds
        if curl -sf "$url" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} $name is running"
            ((PASSED++))
            return 0
        else
            echo -e "  ${YELLOW}⚠${NC} $name container running but not responding yet"
            ((WARNINGS++))
            return 1
        fi
    else
        echo -e "  ${RED}✗${NC} $name is not running"
        ((FAILED++))
        return 1
    fi
}

# Infrastructure services
echo "Infrastructure Services:"
check_service "PostgreSQL" "http://localhost:5532" "unified-postgres" || true
check_service "Redis" "http://localhost:6479" "unified-redis" || true
check_service "RabbitMQ" "http://localhost:15772" "unified-rabbitmq" || true
check_service "Prometheus" "http://localhost:9190/-/healthy" "unified-prometheus" || true
check_service "Grafana" "http://localhost:3101/api/health" "unified-grafana" || true
check_service "Keycloak" "http://localhost:8183" "unified-keycloak" || true
check_service "Traefik" "http://localhost:8181/api/overview" "unified-traefik" || true
check_service "Ollama" "http://localhost:11534/api/tags" "unified-ollama" || true
check_service "Weaviate" "http://localhost:8182/v1/.well-known/ready" "unified-weaviate" || true
check_service "Qdrant" "http://localhost:6333/" "unified-qdrant" || true
check_service "Neo4j" "http://localhost:7474" "unified-neo4j" || true
check_service "Elasticsearch" "http://localhost:9200/_cluster/health" "unified-elasticsearch" || true
check_service "MinIO" "http://localhost:9100/minio/health/live" "unified-minio" || true

# =============================================================================
# STEP 6: VERIFY APPLICATION SERVICES
# =============================================================================

echo ""
echo -e "${BLUE}[6/6] Verifying application services...${NC}"
echo ""

echo "Backend Services:"
check_service "Finance Backend (8100)" "http://localhost:8100/health" "finance-backend" || true
check_service "Real Estate Backend (8101)" "http://localhost:8101/health" "realestate-backend" || true
check_service "Bond.AI Backend (8102)" "http://localhost:8102/health" "bondai-backend" || true
check_service "Legacy Backend (8103)" "http://localhost:8103/health" "legacy-backend" || true
check_service "Labor Backend (8104)" "http://localhost:8104/health" "labor-backend" || true
check_service "Bond.AI Agents (8105)" "http://localhost:8105/health" "bondai-agents" || true

echo ""
echo "Frontend Services:"
check_service "Unified Dashboard (3100)" "http://localhost:3100" "unified-dashboard" || true
check_service "Finance Frontend (3102)" "http://localhost:3102" "finance-frontend" || true
check_service "Real Estate Frontend (3103)" "http://localhost:3103" "realestate-frontend" || true
check_service "Bond.AI Frontend (3104)" "http://localhost:3104" "bondai-frontend" || true
check_service "Labor Frontend (3105)" "http://localhost:3105" "labor-frontend" || true

# =============================================================================
# SUMMARY
# =============================================================================

echo ""
echo "=========================================="
echo -e "${CYAN}  SETUP COMPLETE - SUMMARY${NC}"
echo "=========================================="
echo ""
echo -e "  ${GREEN}Passed:${NC}   $PASSED services"
echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "  ${RED}Failed:${NC}   $FAILED services"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All services started successfully!${NC}"
else
    echo -e "${YELLOW}Some services may need more time to start.${NC}"
    echo "Run './status.sh' to check again or view logs with:"
    echo "  docker compose logs -f [service-name]"
fi

echo ""
echo "=========================================="
echo "  ACCESS POINTS"
echo "=========================================="
echo ""
echo "Main Dashboard:"
echo "  - Unified Dashboard: http://localhost:3100"
echo ""
echo "Platform UIs:"
echo "  - Finance:           http://localhost:3102"
echo "  - Real Estate:       http://localhost:3103"
echo "  - Bond.AI:           http://localhost:3104"
echo "  - Labor:             http://localhost:3105"
echo ""
echo "APIs (with Swagger docs at /docs):"
echo "  - Finance API:       http://localhost:8100/docs"
echo "  - Real Estate API:   http://localhost:8101/docs"
echo "  - Bond.AI API:       http://localhost:8102/docs"
echo "  - Legacy API:        http://localhost:8103/docs"
echo "  - Labor API:         http://localhost:8104/docs"
echo ""
echo "Infrastructure:"
echo "  - Grafana:           http://localhost:3101 (admin/admin)"
echo "  - Traefik:           http://localhost:8181"
echo "  - Prometheus:        http://localhost:9190"
echo "  - Keycloak:          http://localhost:8183 (admin/admin)"
echo "  - RabbitMQ:          http://localhost:15772"
echo "  - Neo4j:             http://localhost:7474"
echo "  - MinIO:             http://localhost:9101"
echo ""
echo "=========================================="
echo ""
echo "To stop all services: ./stop.sh"
echo "To view logs: docker compose logs -f"
echo "To check status: ./status.sh"
echo ""
