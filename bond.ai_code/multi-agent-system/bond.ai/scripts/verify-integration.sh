#!/bin/bash

# Bond.AI Integration Verification Script
# Verifies that all components are properly configured and working

set -e

echo "========================================="
echo "Bond.AI Integration Verification"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success() {
    echo -e "${GREEN}✓${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if services are running
check_service() {
    local name=$1
    local url=$2
    local expected=$3

    echo "Checking $name..."

    if curl -sf "$url" > /dev/null 2>&1; then
        success "$name is running at $url"
        return 0
    else
        error "$name is not accessible at $url"
        return 1
    fi
}

# Check Python
echo "1. Python Environment"
echo "--------------------"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python installed: $PYTHON_VERSION"
else
    error "Python 3 not found"
fi
echo ""

# Check Node.js
echo "2. Node.js Environment"
echo "--------------------"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    success "Node.js installed: $NODE_VERSION"
else
    error "Node.js not found"
fi
echo ""

# Check PostgreSQL
echo "3. PostgreSQL Database"
echo "--------------------"
if command -v psql &> /dev/null; then
    success "PostgreSQL client installed"
    if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
        success "PostgreSQL server is running"
    else
        warning "PostgreSQL server not detected on localhost:5432"
    fi
else
    warning "PostgreSQL client not found"
fi
echo ""

# Check Redis
echo "4. Redis Cache"
echo "--------------------"
if command -v redis-cli &> /dev/null; then
    success "Redis client installed"
    if redis-cli ping > /dev/null 2>&1; then
        success "Redis server is running"
    else
        warning "Redis server not detected"
    fi
else
    warning "Redis client not found"
fi
echo ""

# Check Docker
echo "5. Docker (Optional)"
echo "--------------------"
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    success "Docker installed: $DOCKER_VERSION"

    if command -v docker-compose &> /dev/null; then
        COMPOSE_VERSION=$(docker-compose --version)
        success "Docker Compose installed: $COMPOSE_VERSION"
    fi
else
    warning "Docker not found (optional)"
fi
echo ""

# Check running services
echo "6. Running Services"
echo "--------------------"

# Python Agents API
if check_service "Python Agents API" "http://localhost:8005/health" "healthy"; then
    AGENTS_STATUS=$(curl -s http://localhost:8005/health | grep -o '"status":"[^"]*"' || echo "unknown")
    echo "   Status: $AGENTS_STATUS"
fi

# TypeScript API
if check_service "TypeScript API" "http://localhost:3005/health" "ok"; then
    API_STATUS=$(curl -s http://localhost:3005/health | grep -o '"status":"[^"]*"' || echo "unknown")
    echo "   Status: $API_STATUS"
fi

echo ""

# Check file structure
echo "7. File Structure"
echo "--------------------"

check_file() {
    if [ -f "$1" ]; then
        success "$1"
    else
        error "$1 not found"
    fi
}

check_file "bond.ai/python-agents/api_server.py"
check_file "bond.ai/python-agents/requirements.txt"
check_file "bond.ai/python-agents/Dockerfile"
check_file "bond.ai/server/services/PythonAgentService.ts"
check_file "bond.ai/src/agents/HybridMatchingAgent.ts"
check_file "bond.ai/src/agents/ContextualMatchingAgent.ts"
check_file "bond.ai/docker-compose.yml"
check_file "bond.ai/INTEGRATION_GUIDE.md"

echo ""

# Check Python dependencies
echo "8. Python Dependencies"
echo "--------------------"
cd bond.ai/python-agents
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null || true
fi

if python3 -c "import fastapi" 2>/dev/null; then
    success "FastAPI installed"
else
    warning "FastAPI not installed (run: pip install -r requirements.txt)"
fi

if python3 -c "import transformers" 2>/dev/null; then
    success "Transformers installed"
else
    warning "Transformers not installed"
fi

cd ../..
echo ""

# Check TypeScript dependencies
echo "9. TypeScript Dependencies"
echo "--------------------"
cd bond.ai/server
if [ -d "node_modules" ]; then
    success "Node modules installed"
else
    warning "Node modules not found (run: npm install)"
fi
cd ../..
echo ""

# Test integration
echo "10. Integration Test"
echo "--------------------"

if curl -sf http://localhost:8005/health > /dev/null 2>&1 && \
   curl -sf http://localhost:3005/health > /dev/null 2>&1; then

    success "Both services are running"

    # Test match endpoint
    echo "   Testing match calculation..."
    MATCH_RESPONSE=$(curl -s -X POST http://localhost:8005/match \
        -H "Content-Type: application/json" \
        -d '{
            "profile1": {
                "id": "test1",
                "name": "Test User 1",
                "skills": ["AI", "ML"]
            },
            "profile2": {
                "id": "test2",
                "name": "Test User 2",
                "skills": ["Data Science"]
            },
            "dimensions": ["skills"]
        }' 2>/dev/null || echo "error")

    if echo "$MATCH_RESPONSE" | grep -q "overall_score"; then
        success "Match calculation working"
        SCORE=$(echo "$MATCH_RESPONSE" | grep -o '"overall_score":[0-9.]*' | cut -d: -f2)
        echo "   Sample match score: $SCORE"
    else
        error "Match calculation failed"
    fi
else
    warning "Services not running - skipping integration test"
fi

echo ""
echo "========================================="
echo "Verification Complete"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. If services aren't running, start them with: docker-compose up -d"
echo "2. Or start manually (see INTEGRATION_GUIDE.md)"
echo "3. Check logs if any errors: docker-compose logs -f"
echo ""
