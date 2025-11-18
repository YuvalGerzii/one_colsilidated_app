#!/bin/bash
# Check Status of Portfolio Dashboard Services

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==========================================="
echo "  Portfolio Dashboard - Status Check"
echo "==========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Backend
echo -n "Backend (http://localhost:8000): "
if curl -s -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Running${NC}"
    BACKEND_PID=$(pgrep -f "uvicorn app.main:app" | head -1)
    if [ -n "$BACKEND_PID" ]; then
        echo "   PID: $BACKEND_PID"
    fi
else
    echo -e "${RED}❌ Not responding${NC}"
fi

# Check Frontend
echo -n "Frontend (http://localhost:3000): "
if curl -s -f -o /dev/null http://localhost:3000; then
    echo -e "${GREEN}✅ Running${NC}"
    FRONTEND_PID=$(pgrep -f "vite" | head -1)
    if [ -n "$FRONTEND_PID" ]; then
        echo "   PID: $FRONTEND_PID"
    fi
else
    echo -e "${RED}❌ Not responding${NC}"
fi

# Check Database
echo -n "Database: "
if psql -h localhost -U yuvalgerzi -d portfolio_dashboard -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Connected${NC}"
else
    echo -e "${RED}❌ Cannot connect${NC}"
fi

echo ""
echo "==========================================="
echo "  API Tests"
echo "==========================================="
echo ""

# Test Companies API
echo -n "Companies API: "
COMPANIES_COUNT=$(curl -s http://localhost:8000/api/v1/companies/ 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data))" 2>/dev/null)
if [ -n "$COMPANIES_COUNT" ]; then
    echo -e "${GREEN}✅ $COMPANIES_COUNT companies${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

# Test Frontend Proxy
echo -n "Frontend API Proxy: "
PROXY_COUNT=$(curl -s http://localhost:3000/api/v1/companies/ 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data))" 2>/dev/null)
if [ -n "$PROXY_COUNT" ]; then
    echo -e "${GREEN}✅ $PROXY_COUNT companies${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

echo ""
echo "==========================================="
echo "  Logs"
echo "==========================================="
echo ""
echo "Backend log:  tail -f $PROJECT_ROOT/backend.log"
echo "Frontend log: tail -f $PROJECT_ROOT/frontend.log"
echo ""
echo "==========================================="
echo "  Quick Actions"
echo "==========================================="
echo ""
echo "Start services:   ./start_app.sh"
echo "Stop services:    ./stop_app.sh"
echo "Monitor services: ./monitor_and_restart.sh"
echo ""
