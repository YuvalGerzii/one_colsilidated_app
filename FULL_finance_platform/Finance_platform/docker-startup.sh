#!/bin/bash
# ============================================
# Docker Startup and Validation Script
# ============================================
# This script validates configuration and starts Docker services

set -e

echo "============================================"
echo "Finance Platform - Docker Startup"
echo "============================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Docker is not installed${NC}"
    echo "Please install Docker first: https://docs.docker.com/engine/install/ubuntu/"
    exit 1
fi
echo -e "${GREEN}✓ Docker is installed${NC}"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo -e "${RED}✗ Docker daemon is not running${NC}"
    echo "Please start Docker: sudo systemctl start docker"
    exit 1
fi
echo -e "${GREEN}✓ Docker daemon is running${NC}"

# Check if docker-compose is available
if ! docker compose version &> /dev/null; then
    echo -e "${RED}✗ Docker Compose is not available${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose is available${NC}"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found, creating from .env.example${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
    else
        echo -e "${RED}✗ .env.example not found${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file exists${NC}"
fi

# Check if required directories exist
echo ""
echo "Checking directories..."
REQUIRED_DIRS=(
    "config/postgres/init"
    "config/traefik"
    "config/nginx"
    "config/prometheus"
    "config/grafana"
    "backend"
    "portfolio-dashboard-frontend"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓ $dir${NC}"
    else
        echo -e "${RED}✗ $dir not found${NC}"
        exit 1
    fi
done

# Validate docker-compose.yml
echo ""
echo "Validating docker-compose.yml..."
if docker compose config &> /dev/null; then
    echo -e "${GREEN}✓ docker-compose.yml is valid${NC}"
else
    echo -e "${RED}✗ docker-compose.yml has errors${NC}"
    docker compose config
    exit 1
fi

# Check backend requirements
echo ""
echo "Checking backend configuration..."
if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓ backend/requirements.txt exists${NC}"
else
    echo -e "${RED}✗ backend/requirements.txt not found${NC}"
    exit 1
fi

if [ -f "backend/Dockerfile" ]; then
    echo -e "${GREEN}✓ backend/Dockerfile exists${NC}"
else
    echo -e "${RED}✗ backend/Dockerfile not found${NC}"
    exit 1
fi

# Check frontend configuration
echo ""
echo "Checking frontend configuration..."
if [ -f "portfolio-dashboard-frontend/package.json" ]; then
    echo -e "${GREEN}✓ frontend/package.json exists${NC}"
else
    echo -e "${RED}✗ frontend/package.json not found${NC}"
    exit 1
fi

if [ -f "portfolio-dashboard-frontend/Dockerfile" ]; then
    echo -e "${GREEN}✓ frontend/Dockerfile exists${NC}"
else
    echo -e "${RED}✗ frontend/Dockerfile not found${NC}"
    exit 1
fi

echo ""
echo "============================================"
echo "All validations passed!"
echo "============================================"
echo ""

# Ask user what to do
echo "What would you like to do?"
echo "1) Build and start all services (fresh build)"
echo "2) Start services (use existing images)"
echo "3) Stop all services"
echo "4) View logs"
echo "5) Show service status"
echo "6) Restart services"
echo "7) Clean up (remove containers, volumes, and images)"
echo "8) Exit"
echo ""
read -p "Enter your choice (1-8): " choice

case $choice in
    1)
        echo ""
        echo "Building and starting all services..."
        docker compose up --build -d
        echo ""
        echo -e "${GREEN}✓ Services started${NC}"
        echo ""
        echo "Access URLs:"
        echo "  Frontend:            http://localhost:3000"
        echo "  Backend API:         http://localhost:8000"
        echo "  API Docs:            http://localhost:8000/docs"
        echo "  Traefik Dashboard:   http://localhost:8080"
        echo "  PgAdmin:             http://localhost:5050"
        echo "  Grafana:             http://localhost:3001"
        echo "  Prometheus:          http://localhost:9090"
        echo "  RabbitMQ Management: http://localhost:15672"
        echo ""
        echo "View logs with: docker compose logs -f [service-name]"
        ;;
    2)
        echo ""
        echo "Starting services..."
        docker compose up -d
        echo ""
        echo -e "${GREEN}✓ Services started${NC}"
        ;;
    3)
        echo ""
        echo "Stopping services..."
        docker compose down
        echo -e "${GREEN}✓ Services stopped${NC}"
        ;;
    4)
        echo ""
        echo "Select service to view logs:"
        echo "1) All services"
        echo "2) Backend"
        echo "3) Frontend"
        echo "4) Postgres"
        echo "5) Redis"
        echo "6) RabbitMQ"
        read -p "Enter choice: " log_choice
        case $log_choice in
            1) docker compose logs -f ;;
            2) docker compose logs -f backend ;;
            3) docker compose logs -f frontend ;;
            4) docker compose logs -f postgres ;;
            5) docker compose logs -f redis ;;
            6) docker compose logs -f rabbitmq ;;
            *) echo "Invalid choice" ;;
        esac
        ;;
    5)
        echo ""
        docker compose ps
        ;;
    6)
        echo ""
        echo "Restarting services..."
        docker compose restart
        echo -e "${GREEN}✓ Services restarted${NC}"
        ;;
    7)
        echo ""
        echo -e "${YELLOW}WARNING: This will remove all containers, volumes, and images${NC}"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            docker compose down -v --rmi all
            echo -e "${GREEN}✓ Cleanup complete${NC}"
        else
            echo "Cancelled"
        fi
        ;;
    8)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
