#!/bin/bash

#######################################################################
# Portfolio Dashboard - Unified Startup Script
#######################################################################
#
# This script starts the complete Portfolio Dashboard application:
# 1. PostgreSQL Database
# 2. Backend API (FastAPI)
# 3. Frontend UI (React/Vite)
#
# All services start in the background and logs are shown in real-time.
#
# Usage:
#   ./start_app.sh              # Start all services
#   ./start_app.sh --stop       # Stop all services
#   ./start_app.sh --restart    # Restart all services
#   ./start_app.sh --status     # Check service status
#
#######################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${MAGENTA}==================================================================="
    echo -e "  $1"
    echo -e "===================================================================${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# PID file locations
BACKEND_PID_FILE="/tmp/portfolio_backend.pid"
FRONTEND_PID_FILE="/tmp/portfolio_frontend.pid"

# Stop all services
stop_services() {
    log_header "Stopping Portfolio Dashboard Services"

    # Stop frontend
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if kill -0 "$FRONTEND_PID" 2>/dev/null; then
            log_info "Stopping frontend (PID: $FRONTEND_PID)..."
            kill "$FRONTEND_PID"
            rm -f "$FRONTEND_PID_FILE"
            log_success "Frontend stopped"
        else
            rm -f "$FRONTEND_PID_FILE"
        fi
    fi

    # Stop backend
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if kill -0 "$BACKEND_PID" 2>/dev/null; then
            log_info "Stopping backend (PID: $BACKEND_PID)..."
            kill "$BACKEND_PID"
            rm -f "$BACKEND_PID_FILE"
            log_success "Backend stopped"
        else
            rm -f "$BACKEND_PID_FILE"
        fi
    fi

    if command -v pg_isready >/dev/null 2>&1; then
        log_info "PostgreSQL remains running (system service)"
    else
        log_info "PostgreSQL management skipped (client tools unavailable)"
    fi

    echo ""
    log_success "All application services stopped"
}

# Check service status
check_status() {
    log_header "Portfolio Dashboard Service Status"

    # PostgreSQL
    if command -v pg_isready >/dev/null 2>&1; then
        if pg_isready &>/dev/null; then
            log_success "PostgreSQL: Running"
        else
            log_error "PostgreSQL: Not running"
        fi
    else
        log_warning "PostgreSQL status check skipped (pg_isready not available)"
    fi

    # Backend
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if kill -0 "$BACKEND_PID" 2>/dev/null; then
            log_success "Backend: Running (PID: $BACKEND_PID, Port: 8000)"
        else
            log_error "Backend: Not running (stale PID file)"
            rm -f "$BACKEND_PID_FILE"
        fi
    else
        log_warning "Backend: Not running"
    fi

    # Frontend
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if kill -0 "$FRONTEND_PID" 2>/dev/null; then
            log_success "Frontend: Running (PID: $FRONTEND_PID, Port: 4173)"
        else
            log_error "Frontend: Not running (stale PID file)"
            rm -f "$FRONTEND_PID_FILE"
        fi
    else
        log_warning "Frontend: Not running"
    fi

    echo ""
    echo -e "${CYAN}Access URLs:${NC}"
    echo "  Frontend:  http://localhost:4173"
    echo "  Backend:   http://localhost:8000"
    echo "  API Docs:  http://localhost:8000/docs"
}

# Start all services
wait_for_backend() {
    local max_attempts=30
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -sSf "http://127.0.0.1:8000/health" >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    return 1
}

wait_for_frontend() {
    local max_attempts=45
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if curl -sSf "http://127.0.0.1:4173" >/dev/null 2>&1; then
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done
    return 1
}

show_logs() {
    if [ -f /tmp/portfolio_backend.log ]; then
        log_info "--- Backend Logs ---"
        tail -n 20 /tmp/portfolio_backend.log
    else
        log_warning "Backend logs not found"
    fi

    if [ -f /tmp/portfolio_frontend.log ]; then
        log_info "--- Frontend Logs ---"
        tail -n 20 /tmp/portfolio_frontend.log
    else
        log_warning "Frontend logs not found"
    fi
}

start_services() {
    log_header "Starting Portfolio Dashboard"
    echo ""

    # 1. Ensure PostgreSQL is running
    log_info "Step 1/3: Checking PostgreSQL..."
    if command -v pg_isready >/dev/null 2>&1; then
        if pg_isready &>/dev/null; then
            log_success "PostgreSQL is running"
        else
            log_warning "PostgreSQL is not running. Attempting to start..."
            if command -v pg_ctlcluster >/dev/null 2>&1; then
                pg_ctlcluster 16 main start
                sleep 2
                if pg_isready &>/dev/null; then
                    log_success "PostgreSQL started"
                else
                    log_error "Failed to start PostgreSQL"
                    exit 1
                fi
            else
                log_warning "pg_ctlcluster not available; please start PostgreSQL manually."
            fi
        fi
    else
        log_warning "PostgreSQL client tools not available; skipping automatic check."
    fi
    echo ""

    # 2. Start Backend
    log_info "Step 2/3: Starting Backend API..."
    cd "$SCRIPT_DIR/backend"

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        log_error "Virtual environment not found. Please run build_app.sh first."
        exit 1
    fi

    # Start backend in background
    source venv/bin/activate
    nohup uvicorn app.main:app --reload --port 8000 --host 0.0.0.0 \
        > /tmp/portfolio_backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BACKEND_PID_FILE"
    deactivate

    # Wait for backend to start
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        log_error "Backend failed to start. Check logs at /tmp/portfolio_backend.log"
        rm -f "$BACKEND_PID_FILE"
        exit 1
    fi

    if wait_for_backend; then
        log_success "Backend healthy (PID: $BACKEND_PID)"
    else
        log_error "Backend did not become healthy in time."
        kill "$BACKEND_PID" 2>/dev/null || true
        rm -f "$BACKEND_PID_FILE"
        show_logs
        exit 1
    fi
    echo ""

    # 3. Start Frontend
    log_info "Step 3/3: Starting Frontend UI..."
    cd "$SCRIPT_DIR/portfolio-dashboard-frontend"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        log_error "Frontend dependencies not installed. Please run build_app.sh first."
        exit 1
    fi

    # Start frontend in background (bind to all interfaces for container access)
    nohup npm run dev -- --host 0.0.0.0 --port 4173 > /tmp/portfolio_frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$FRONTEND_PID_FILE"

    # Wait for frontend to start
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        log_error "Frontend failed to start. Check logs at /tmp/portfolio_frontend.log"
        rm -f "$FRONTEND_PID_FILE"
        exit 1
    fi

    if wait_for_frontend; then
        log_success "Frontend reachable (PID: $FRONTEND_PID)"
    else
        log_error "Frontend did not become reachable in time."
        kill "$FRONTEND_PID" 2>/dev/null || true
        rm -f "$FRONTEND_PID_FILE"
        show_logs
        exit 1
    fi
    echo ""

    # Summary
    log_header "🚀 Portfolio Dashboard Started Successfully!"
    echo ""
    echo -e "${GREEN}All services are running!${NC}"
    echo ""
    echo -e "${CYAN}Access URLs:${NC}"
    echo "  🌐 Frontend:    http://localhost:4173"
    echo "  🔧 Backend API: http://localhost:8000"
    echo "  📚 API Docs:    http://localhost:8000/docs"
    echo "  📊 Market Data: http://localhost:4173/market-data"
    echo ""
    echo -e "${YELLOW}Logs:${NC}"
    echo "  Backend:  tail -f /tmp/portfolio_backend.log"
    echo "  Frontend: tail -f /tmp/portfolio_frontend.log"
    echo ""
    echo -e "${YELLOW}Management:${NC}"
    echo "  Stop:    ./start_app.sh --stop"
    echo "  Status:  ./start_app.sh --status"
    echo "  Restart: ./start_app.sh --restart"
    echo ""
    log_info "For live logs run: ./start_app.sh --logs"
}

# Main script logic
case "${1:-}" in
    --stop)
        stop_services
        ;;
    --status)
        check_status
        ;;
    --logs)
        show_logs
        ;;
    --restart)
        stop_services
        sleep 2
        start_services
        ;;
    --help)
        echo "Portfolio Dashboard Startup Script"
        echo ""
        echo "Usage:"
        echo "  ./start_app.sh              Start all services"
        echo "  ./start_app.sh --stop       Stop all services"
        echo "  ./start_app.sh --restart    Restart all services"
        echo "  ./start_app.sh --status     Check service status"
        echo "  ./start_app.sh --help       Show this help"
        ;;
    *)
        start_services
        ;;
esac
