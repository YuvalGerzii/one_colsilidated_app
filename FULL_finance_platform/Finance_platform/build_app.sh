#!/bin/bash

#######################################################################
# Portfolio Dashboard - Complete Build Script
#######################################################################
#
# This script builds the complete Portfolio Dashboard application:
# - Backend (Python/FastAPI)
# - Frontend (React/TypeScript)
# - Database setup
#
# Prerequisites:
# - Python 3.11+
# - Node.js 18+
# - PostgreSQL 14+
# - Internet connection
#
# Usage:
#   bash build_app.sh
#
#######################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Header
echo "======================================================================="
echo "  Portfolio Dashboard - Build Script"
echo "======================================================================="
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "Working directory: $SCRIPT_DIR"
echo ""

#######################################################################
# 1. PREREQUISITES CHECK
#######################################################################

log_info "Step 1: Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_success "Python $PYTHON_VERSION found"

# Check Node.js
if ! command -v node &> /dev/null; then
    log_error "Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
NODE_VERSION=$(node --version)
log_success "Node.js $NODE_VERSION found"

# Check npm
if ! command -v npm &> /dev/null; then
    log_error "npm is not installed. Please install npm"
    exit 1
fi
NPM_VERSION=$(npm --version)
log_success "npm $NPM_VERSION found"

HAS_POSTGRES=true

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    log_warning "PostgreSQL command-line tools not found. Skipping database checks."
    HAS_POSTGRES=false
else
    PSQL_VERSION=$(psql --version | cut -d' ' -f3)
    log_success "PostgreSQL $PSQL_VERSION found"

    # Check if PostgreSQL is running
    if ! pg_isready &> /dev/null; then
        log_warning "PostgreSQL is not running. Attempting to start..."
        if command -v systemctl &> /dev/null; then
            sudo systemctl start postgresql || HAS_POSTGRES=false
        elif command -v service &> /dev/null; then
            sudo service postgresql start || HAS_POSTGRES=false
        else
            log_warning "Could not start PostgreSQL automatically."
            HAS_POSTGRES=false
        fi
        if [ "$HAS_POSTGRES" = true ]; then
            sleep 2
            if pg_isready &> /dev/null; then
                log_success "PostgreSQL started successfully"
            else
                log_warning "Failed to confirm PostgreSQL startup. Continuing without database checks."
                HAS_POSTGRES=false
            fi
        fi
    else
        log_success "PostgreSQL is running"
    fi
fi

echo ""

#######################################################################
# 2. BACKEND SETUP
#######################################################################

log_info "Step 2: Setting up backend..."

cd "$SCRIPT_DIR/backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    log_warning ".env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_success ".env file created"
    else
        log_warning "No .env.example found. Using default configuration."
    fi
else
    log_success ".env file exists"
fi

# Install Python dependencies
log_info "Installing Python dependencies..."
if [ ! -d "venv" ]; then
    log_info "Creating Python virtual environment..."
    python3 -m venv venv
    log_success "Virtual environment created"
fi

BACKEND_DEPS_INSTALLED=true

source venv/bin/activate
log_info "Installing requirements..."
if ! pip install --upgrade pip; then
    log_warning "Could not upgrade pip. Continuing with existing version."
fi
if ! pip install -r requirements.txt; then
    log_warning "Failed to install backend requirements from PyPI (likely due to offline environment)."
    BACKEND_DEPS_INSTALLED=false
else
    log_success "Backend dependencies installed"
fi
deactivate

if [ "$BACKEND_DEPS_INSTALLED" = false ]; then
    log_warning "Attempting fallback by recreating the virtual environment with system site-packages..."
    rm -rf venv
    python3 -m venv --system-site-packages venv
    source venv/bin/activate
    MISSING_MODULES=$(python - <<'PY'
modules = [
    'fastapi',
    'uvicorn',
    'sqlalchemy',
    'alembic',
    'psycopg2',
    'asyncpg',
    'pydantic',
    'pdfplumber',
    'PyPDF2',
    'pytesseract',
    'PIL',
    'jose',
    'passlib',
    'requests',
    'pandas',
    'numpy'
]
missing = []
for module in modules:
    try:
        __import__(module)
    except Exception:
        missing.append(module)
if missing:
    print(" ".join(sorted(set(missing))))
PY
)
    if [ -z "$MISSING_MODULES" ]; then
        log_success "Backend environment configured using system site-packages"
        BACKEND_DEPS_INSTALLED=true
    else
        log_error "Missing backend Python modules: $MISSING_MODULES"
        log_warning "Install the missing packages manually once network access is available."
    fi
    deactivate
fi

echo ""

#######################################################################
# 3. FRONTEND SETUP
#######################################################################

log_info "Step 3: Setting up frontend..."

cd "$SCRIPT_DIR/portfolio-dashboard-frontend"

# Check if .env exists
if [ ! -f ".env" ]; then
    log_warning ".env file not found. Creating from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        log_success ".env file created"
    else
        log_warning "No .env.example found. Using default configuration."
    fi
else
    log_success ".env file exists"
fi

# Install npm dependencies
log_info "Installing npm dependencies..."
FRONTEND_DEPS_INSTALLED=true
if ! npm install; then
    log_warning "Failed to install frontend dependencies. Frontend build may be incomplete."
    FRONTEND_DEPS_INSTALLED=false
else
    log_success "Frontend dependencies installed"
fi

echo ""

#######################################################################
# 4. DATABASE INITIALIZATION
#######################################################################

log_info "Step 4: Initializing database..."

cd "$SCRIPT_DIR"

if [ "$HAS_POSTGRES" = true ]; then
    # Check if database initialization script exists
    if [ -f "init_database.sh" ]; then
        log_info "Running database initialization script..."
        bash init_database.sh
        log_success "Database initialized"
    else
        log_warning "No database initialization script found. Skipping..."
    fi
else
    log_warning "Skipping database initialization because PostgreSQL is unavailable."
fi

echo ""

#######################################################################
# 5. BUILD FRONTEND
#######################################################################

log_info "Step 5: Building frontend..."

cd "$SCRIPT_DIR/portfolio-dashboard-frontend"

if [ "$FRONTEND_DEPS_INSTALLED" = true ]; then
    log_info "Running TypeScript compilation and Vite build..."
    if npm run build -- --logLevel silent; then
        log_success "Frontend built successfully"
    else
        log_warning "Frontend build failed. Check dependency installation and build logs."
    fi
else
    log_warning "Skipping frontend build because dependencies are missing."
fi

echo ""

#######################################################################
# 6. VERIFY SETUP
#######################################################################

log_info "Step 6: Verifying setup..."

# Check backend files
if [ -f "$SCRIPT_DIR/backend/app/main.py" ]; then
    log_success "Backend main.py exists"
else
    log_error "Backend main.py not found"
fi

# Check frontend build
if [ -d "$SCRIPT_DIR/portfolio-dashboard-frontend/dist" ]; then
    log_success "Frontend build directory exists"
else
    log_warning "Frontend build directory not found"
fi

# Check database connection
if [ "$HAS_POSTGRES" = true ]; then
    if psql -U postgres -lqt | cut -d \| -f 1 | grep -qw portfolio_dashboard; then
        log_success "Database 'portfolio_dashboard' exists"
    else
        log_warning "Database 'portfolio_dashboard' not found"
    fi
else
    log_warning "Database verification skipped because PostgreSQL is unavailable."
fi

echo ""

#######################################################################
# 7. SUMMARY
#######################################################################

echo "======================================================================="
echo "  Build Complete!"
echo "======================================================================="
echo ""
echo "To start the application:"
echo ""
echo "Backend:"
echo "  cd $SCRIPT_DIR/backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo "Frontend:"
echo "  cd $SCRIPT_DIR/portfolio-dashboard-frontend"
echo "  npm run dev"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:3000 (or http://localhost:5173 for Vite)"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "======================================================================="
