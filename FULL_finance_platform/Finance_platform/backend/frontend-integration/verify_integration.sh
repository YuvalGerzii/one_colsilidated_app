#!/bin/bash

# Portfolio Dashboard - Integration Verification Script
# This script checks if frontend and backend are properly integrated

echo "🔍 Portfolio Dashboard Integration Verification"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track issues
ISSUES_FOUND=0

# Check 1: Backend Health
echo "1️⃣  Checking Backend Health..."
BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$BACKEND_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✅ Backend is running and healthy${NC}"
else
    echo -e "${RED}❌ Backend is not responding (HTTP $BACKEND_RESPONSE)${NC}"
    echo "   → Make sure backend is running: uvicorn app.main:app --reload"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 2: Backend API Endpoints
echo "2️⃣  Checking Backend API Endpoints..."
ENDPOINTS=(
    "/api/v1/funds"
    "/api/v1/companies"
    "/api/v1/financials"
)

for endpoint in "${ENDPOINTS[@]}"; do
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000$endpoint")
    if [ "$RESPONSE" == "200" ] || [ "$RESPONSE" == "422" ]; then
        echo -e "${GREEN}✅ $endpoint${NC}"
    else
        echo -e "${RED}❌ $endpoint (HTTP $RESPONSE)${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
done
echo ""

# Check 3: Frontend Server
echo "3️⃣  Checking Frontend Server..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || curl -s -o /dev/null -w "%{http_code}" http://localhost:5173)

if [ "$FRONTEND_RESPONSE" == "200" ]; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend is not responding${NC}"
    echo "   → Make sure frontend is running: npm run dev"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 4: Database Connection
echo "4️⃣  Checking Database Connection..."
if command -v psql &> /dev/null; then
    # Try to connect to database
    DB_CHECK=$(psql -h localhost -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw portfolio_dashboard && echo "found" || echo "not_found")
    
    if [ "$DB_CHECK" == "found" ]; then
        echo -e "${GREEN}✅ Database 'portfolio_dashboard' exists${NC}"
    else
        echo -e "${YELLOW}⚠️  Database 'portfolio_dashboard' not found${NC}"
        echo "   → Create database: createdb portfolio_dashboard"
    fi
else
    echo -e "${YELLOW}⚠️  psql not found, skipping database check${NC}"
fi
echo ""

# Check 5: CORS Configuration
echo "5️⃣  Checking CORS Configuration..."
CORS_RESPONSE=$(curl -s -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET" -H "Access-Control-Request-Headers: Content-Type" -X OPTIONS http://localhost:8000/api/v1/companies 2>&1)

if echo "$CORS_RESPONSE" | grep -q "Access-Control-Allow-Origin"; then
    echo -e "${GREEN}✅ CORS is configured correctly${NC}"
else
    echo -e "${RED}❌ CORS headers not found${NC}"
    echo "   → Check CORS middleware in backend/app/main.py"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 6: Environment Files
echo "6️⃣  Checking Environment Files..."

if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✅ Backend .env file exists${NC}"
    
    # Check for required variables
    if grep -q "DATABASE_URL" backend/.env; then
        echo -e "${GREEN}   ✅ DATABASE_URL is set${NC}"
    else
        echo -e "${RED}   ❌ DATABASE_URL not found in .env${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}❌ Backend .env file not found${NC}"
    echo "   → Create .env file: cp backend/.env.example backend/.env"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi

if [ -f "frontend/.env" ]; then
    echo -e "${GREEN}✅ Frontend .env file exists${NC}"
    
    # Check for required variables
    if grep -q "VITE_API_BASE_URL" frontend/.env; then
        echo -e "${GREEN}   ✅ VITE_API_BASE_URL is set${NC}"
    else
        echo -e "${RED}   ❌ VITE_API_BASE_URL not found in .env${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi
else
    echo -e "${RED}❌ Frontend .env file not found${NC}"
    echo "   → Create .env file: cp frontend/.env.example frontend/.env"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 7: Node Modules
echo "7️⃣  Checking Frontend Dependencies..."
if [ -d "frontend/node_modules" ]; then
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
else
    echo -e "${RED}❌ Frontend node_modules not found${NC}"
    echo "   → Install dependencies: cd frontend && npm install"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
fi
echo ""

# Check 8: Python Virtual Environment
echo "8️⃣  Checking Backend Dependencies..."
if [ -d "backend/venv" ] || [ -d "backend/.venv" ]; then
    echo -e "${GREEN}✅ Python virtual environment exists${NC}"
else
    echo -e "${YELLOW}⚠️  Virtual environment not found${NC}"
    echo "   → Create venv: cd backend && python -m venv venv"
fi
echo ""

# Summary
echo "================================================"
echo "📊 Verification Summary"
echo "================================================"

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}"
    echo "🎉 All checks passed! Your integration looks good."
    echo ""
    echo "Next steps:"
    echo "1. Open http://localhost:3000 in your browser"
    echo "2. Check browser console for any errors (F12)"
    echo "3. Run integration tests from the UI or console"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "⚠️  Found $ISSUES_FOUND issue(s) that need attention."
    echo ""
    echo "Please fix the issues above and run this script again."
    echo -e "${NC}"
    exit 1
fi
