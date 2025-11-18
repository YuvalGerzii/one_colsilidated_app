#!/usr/bin/env bash
set -e

# =============================================================================
# Portfolio Dashboard - Claude Code Environment Startup Script
# =============================================================================
# This script is optimized for Claude Code environments with:
# - Automatic dependency installation with fallback strategies
# - Proxy support for restricted networks
# - Virtual environment management
# - Database initialization
# - Service health checks
# =============================================================================

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[⚠]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_header() {
    echo -e "${MAGENTA}=================================================================="
    echo -e "  $1"
    echo -e "==================================================================${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_header "🚀 Portfolio Dashboard - Claude Code Setup"
echo ""

# =============================================================================
# 1. Check Prerequisites
# =============================================================================
log_info "Step 1/6: Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
log_success "Python found: $PYTHON_VERSION"

# Check Node.js
if ! command -v node &> /dev/null; then
    log_error "Node.js is not installed. Please install Node.js 16+"
    exit 1
fi
NODE_VERSION=$(node --version)
log_success "Node.js found: $NODE_VERSION"

# Check PostgreSQL
PSQL_BIN=""
if command -v psql &> /dev/null; then
    PSQL_BIN="psql"
    CREATEDB_BIN="createdb"
    log_success "PostgreSQL found (system)"
elif [ -f "/opt/homebrew/opt/postgresql@14/bin/psql" ]; then
    PSQL_BIN="/opt/homebrew/opt/postgresql@14/bin/psql"
    CREATEDB_BIN="/opt/homebrew/opt/postgresql@14/bin/createdb"
    log_success "PostgreSQL found (Homebrew)"
else
    log_warning "PostgreSQL not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install postgresql@14
        brew services start postgresql@14
        PSQL_BIN="/opt/homebrew/opt/postgresql@14/bin/psql"
        CREATEDB_BIN="/opt/homebrew/opt/postgresql@14/bin/createdb"
        sleep 3
        log_success "PostgreSQL installed and started"
    else
        log_error "Homebrew not found. Please install PostgreSQL manually"
        exit 1
    fi
fi

echo ""

# =============================================================================
# 2. Setup Backend Dependencies
# =============================================================================
log_header "🔧 Installing Backend Dependencies"
echo ""

cd "$SCRIPT_DIR/backend"

# Create virtual environment
if [ ! -d ".venv" ]; then
    log_info "Creating Python virtual environment..."
    python3 -m venv .venv
    log_success "Virtual environment created"
else
    log_success "Virtual environment already exists"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip safely
log_info "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel --quiet

# Proxy fallback (optional)
if [ -n "$HTTP_PROXY" ]; then
    log_info "Using proxy: $HTTP_PROXY"
fi

# Ensure requirements.txt exists with comprehensive dependencies
log_info "Preparing requirements.txt..."
cat > requirements.txt <<'EOF'
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.13.0
psycopg2-binary==2.9.9
asyncpg==0.29.0

# Validation & Serialization
pydantic==2.5.2
pydantic-settings==2.1.0
email-validator==2.1.0

# Excel Processing
openpyxl==3.1.2
xlsxwriter==3.1.9

# PDF Processing
pdfplumber==0.10.3
PyPDF2==3.0.1
pytesseract==0.3.10
pillow==10.1.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
bcrypt==4.1.1

# HTTP & API
httpx==0.25.2
requests==2.31.0

# Data Processing
pandas==2.1.4
numpy==1.26.2
matplotlib==3.8.4

# Utilities
python-dateutil==2.8.2
pytz==2023.3.post1
rich==13.7.0

# Caching & Background Tasks
redis==5.0.1
celery==5.3.4

# Logging & Monitoring
loguru==0.7.2

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
faker==20.1.0

# Code Quality
black==23.12.0
flake8==6.1.0
mypy==1.7.1
isort==5.13.2

# Documentation
mkdocs==1.5.3
mkdocs-material==9.5.3

# AWS/Cloud (optional)
boto3==1.34.10

# AI/ML (optional)
anthropic>=0.39.0
EOF

# Install dependencies with cache fallback
log_info "Installing Python dependencies (this may take a few minutes)..."
if pip install -r requirements.txt --quiet; then
    log_success "Dependencies installed successfully"
elif pip install --no-cache-dir -r requirements.txt; then
    log_success "Dependencies installed (no-cache fallback)"
else
    log_error "Failed to install dependencies"
    exit 1
fi

# Mark dependencies as installed
touch .venv/.dependencies_installed

echo ""

# =============================================================================
# 3. Setup Frontend Dependencies
# =============================================================================
log_header "⚛️  Installing Frontend Dependencies"
echo ""

cd "$SCRIPT_DIR/portfolio-dashboard-frontend"

if [ ! -d "node_modules" ]; then
    log_info "Installing npm dependencies..."
    npm install --silent
    log_success "Frontend dependencies installed"
else
    log_success "Frontend dependencies already installed"
fi

echo ""

# =============================================================================
# 4. Setup Database
# =============================================================================
log_header "🗄️  Setting Up Database"
echo ""

# Create database if it doesn't exist
if ! $PSQL_BIN -lqt | cut -d \| -f 1 | grep -qw portfolio_dashboard; then
    log_info "Creating database 'portfolio_dashboard'..."
    $CREATEDB_BIN portfolio_dashboard
    log_success "Database created"
else
    log_success "Database already exists"
fi

# Create user if it doesn't exist
$PSQL_BIN -d portfolio_dashboard -tAc "SELECT 1 FROM pg_roles WHERE rolname='portfolio_user'" | grep -q 1 2>/dev/null || {
    log_info "Creating database user 'portfolio_user'..."
    $PSQL_BIN -d portfolio_dashboard -c "CREATE USER portfolio_user WITH PASSWORD 'password';" 2>/dev/null || true
    log_success "User created"
}

# Grant privileges
log_info "Granting privileges..."
$PSQL_BIN -d portfolio_dashboard -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_dashboard TO portfolio_user;" 2>/dev/null || true
$PSQL_BIN -d portfolio_dashboard -c "GRANT ALL PRIVILEGES ON SCHEMA public TO portfolio_user;" 2>/dev/null || true
$PSQL_BIN -d portfolio_dashboard -c "ALTER SCHEMA public OWNER TO portfolio_user;" 2>/dev/null || true
log_success "Privileges granted"

# Run migrations if available
cd "$SCRIPT_DIR/backend"
source .venv/bin/activate
if [ -d "migrations" ] && [ -f "alembic.ini" ]; then
    log_info "Running database migrations..."
    alembic upgrade head 2>/dev/null && log_success "Migrations applied" || log_warning "Migration skipped"
fi

echo ""

# =============================================================================
# 5. Start Services
# =============================================================================
log_header "🚀 Starting Services"
echo ""

# Clean up existing processes
log_info "Cleaning up existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true
sleep 1

# Start Backend
log_info "Starting backend server..."
cd "$SCRIPT_DIR/backend"
source .venv/bin/activate
nohup python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 \
    > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"

# Wait for backend
sleep 3
if kill -0 $BACKEND_PID 2>/dev/null; then
    log_success "Backend started (PID: $BACKEND_PID)"
else
    log_error "Backend failed to start. Check backend.log"
    exit 1
fi

# Start Frontend
log_info "Starting frontend server..."
cd "$SCRIPT_DIR/portfolio-dashboard-frontend"
nohup npm run dev > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"

# Wait for frontend
sleep 3
if kill -0 $FRONTEND_PID 2>/dev/null; then
    log_success "Frontend started (PID: $FRONTEND_PID)"
else
    log_error "Frontend failed to start. Check frontend.log"
    exit 1
fi

echo ""

# =============================================================================
# 6. Health Checks
# =============================================================================
log_header "🏥 Running Health Checks"
echo ""

# Check Backend
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Backend is healthy"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    log_warning "Backend health check timeout (may still be starting)"
fi

# Check Frontend
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:3000 > /dev/null 2>&1 || curl -s http://localhost:5173 > /dev/null 2>&1; then
        log_success "Frontend is accessible"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 1
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    log_warning "Frontend may still be starting..."
fi

echo ""

# =============================================================================
# Summary
# =============================================================================
log_header "✅ Portfolio Dashboard is Running!"
echo ""
echo -e "${CYAN}📍 Access Points:${NC}"
echo -e "   Frontend:    ${GREEN}http://localhost:3000${NC} or ${GREEN}http://localhost:5173${NC}"
echo -e "   Backend:     ${GREEN}http://localhost:8000${NC}"
echo -e "   API Docs:    ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   Redoc:       ${GREEN}http://localhost:8000/redoc${NC}"
echo ""
echo -e "${CYAN}📊 Service Info:${NC}"
echo -e "   Backend PID:   ${GREEN}$BACKEND_PID${NC}"
echo -e "   Frontend PID:  ${GREEN}$FRONTEND_PID${NC}"
echo -e "   Database:      ${GREEN}postgresql://localhost:5432/portfolio_dashboard${NC}"
echo ""
echo -e "${CYAN}📝 Logs:${NC}"
echo -e "   Backend:   ${YELLOW}tail -f $SCRIPT_DIR/backend.log${NC}"
echo -e "   Frontend:  ${YELLOW}tail -f $SCRIPT_DIR/frontend.log${NC}"
echo ""
echo -e "${CYAN}🛑 Stop Services:${NC}"
echo -e "   ${YELLOW}kill $BACKEND_PID $FRONTEND_PID${NC}"
echo -e "   or run: ${YELLOW}./stop_app.sh${NC}"
echo ""
echo -e "${GREEN}🎉 Happy coding with Claude Code!${NC}"
echo ""
