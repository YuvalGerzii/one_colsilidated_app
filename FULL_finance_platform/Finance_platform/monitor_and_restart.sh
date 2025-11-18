#!/bin/bash
# Monitor and Auto-Restart Services
# This script monitors backend and frontend services and restarts them if they crash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_LOG="$PROJECT_ROOT/backend.log"
FRONTEND_LOG="$PROJECT_ROOT/frontend.log"
MONITOR_LOG="$PROJECT_ROOT/monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MONITOR_LOG"
}

check_backend() {
    if curl -s -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

check_frontend() {
    if curl -s -f http://localhost:3000 > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

start_backend() {
    log "Starting backend..."
    pkill -f "uvicorn app.main:app"
    sleep 2

    cd "$PROJECT_ROOT/backend"
    source .venv/bin/activate
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!

    sleep 5

    if check_backend; then
        log "✅ Backend started successfully (PID: $BACKEND_PID)"
        echo "$BACKEND_PID" > "$PROJECT_ROOT/backend.pid"
        return 0
    else
        log "❌ Backend failed to start"
        return 1
    fi
}

start_frontend() {
    log "Starting frontend..."
    pkill -f "vite"
    pkill -f "npm run dev"
    sleep 2

    cd "$PROJECT_ROOT/portfolio-dashboard-frontend"
    npm run dev > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!

    sleep 5

    if check_frontend; then
        log "✅ Frontend started successfully (PID: $FRONTEND_PID)"
        echo "$FRONTEND_PID" > "$PROJECT_ROOT/frontend.pid"
        return 0
    else
        log "❌ Frontend failed to start"
        return 1
    fi
}

monitor_services() {
    log "🔍 Starting service monitoring..."

    while true; do
        # Check backend
        if ! check_backend; then
            log "⚠️  Backend is down! Attempting restart..."
            start_backend
        fi

        # Check frontend
        if ! check_frontend; then
            log "⚠️  Frontend is down! Attempting restart..."
            start_frontend
        fi

        # Wait 30 seconds before next check
        sleep 30
    done
}

# Initial startup
log "=========================================="
log "Starting Portfolio Dashboard Services"
log "=========================================="

start_backend
start_frontend

log ""
log "📍 Access Points:"
log "   Frontend: http://localhost:3000"
log "   Backend:  http://localhost:8000"
log "   API Docs: http://localhost:8000/docs"
log ""
log "🔍 Monitoring services (checking every 30 seconds)..."
log "   Press Ctrl+C to stop"
log ""

# Start monitoring
monitor_services
