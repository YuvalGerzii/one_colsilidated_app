# Crash Handling and Error Recovery

## Overview

The Portfolio Dashboard now includes comprehensive crash handling and error recovery mechanisms at multiple levels:

### 1. Frontend Error Handling

#### React Error Boundary
- **Location**: `portfolio-dashboard-frontend/src/components/common/ErrorBoundary.tsx`
- **Purpose**: Catches JavaScript errors anywhere in the React component tree
- **Features**:
  - Displays user-friendly error message
  - Shows detailed error info in development mode
  - Provides "Reload Application" button
  - Prevents entire app from crashing due to component errors

#### Component-Level Error Handling
- **Dashboard Component**:
  - Loading states with skeleton screens
  - Error states with retry functionality
  - Empty states for better UX
  - Wrapped refetch calls to prevent type errors

#### Data Fetching Error Handling
- **React Query Configuration**:
  - Automatic retry on failure (1 retry)
  - No refetch on window focus (prevents unnecessary requests)
  - 5-minute stale time for cached data

### 2. Backend Error Handling

#### Database Connection
- Automatic retry on connection failure
- Graceful error messages in logs
- Health check endpoint for monitoring

#### API Endpoints
- Try-catch blocks for all operations
- Proper HTTP status codes
- Detailed error messages in development

### 3. Service Monitoring

#### Monitoring Script
**File**: `monitor_and_restart.sh`

**Features**:
- Checks backend health every 30 seconds
- Checks frontend availability every 30 seconds
- Automatically restarts crashed services
- Logs all monitoring activity to `monitor.log`

**Usage**:
```bash
./monitor_and_restart.sh
```

**What it does**:
1. Starts backend and frontend if not running
2. Continuously monitors both services
3. Automatically restarts any crashed service
4. Maintains detailed logs of all restarts

#### Status Check Script
**File**: `check_status.sh`

**Features**:
- Quick health check of all services
- Tests API endpoints
- Shows process IDs
- Displays company count from API

**Usage**:
```bash
./check_status.sh
```

**Output includes**:
- ✅ Backend status and PID
- ✅ Frontend status and PID
- ✅ Database connection status
- ✅ API test results (company count)
- Log file locations
- Quick action commands

### 4. Common Issues and Solutions

#### Dashboard Shows Blank Page

**Causes**:
1. Browser cache showing old state
2. Backend not running
3. JavaScript errors

**Solutions**:
1. Hard refresh: `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows)
2. Check services: `./check_status.sh`
3. Open browser console (F12) to see errors
4. Check logs: `tail -f frontend.log`

#### Backend Crashes

**Detection**:
- Health check fails at http://localhost:8000/api/v1/health
- `check_status.sh` shows ❌ for backend

**Recovery**:
1. Automatic: If using `monitor_and_restart.sh`
2. Manual: `./start_app.sh` or restart backend only

**Check logs**:
```bash
tail -f backend.log
```

#### Frontend Crashes

**Detection**:
- Cannot access http://localhost:3000
- `check_status.sh` shows ❌ for frontend

**Recovery**:
1. Automatic: If using `monitor_and_restart.sh`
2. Manual: Restart frontend

**Check logs**:
```bash
tail -f frontend.log
```

### 5. Error Logging

#### Backend Logs
- **Location**: `backend.log`
- **Contains**:
  - API requests and responses
  - Database queries (in development)
  - Error stack traces
  - Application startup/shutdown events

#### Frontend Logs
- **Location**: `frontend.log`
- **Contains**:
  - Vite dev server output
  - Hot module replacement (HMR) updates
  - Build errors and warnings
  - Deprecation warnings

#### Monitor Logs
- **Location**: `monitor.log`
- **Contains**:
  - Service health check results
  - Restart events
  - Timestamps for all monitoring activities

### 6. Preventive Measures

#### Fixed Issues
1. ✅ CardActionArea import error removed from Dashboard.tsx
2. ✅ Added refetch function to useCompanies hook
3. ✅ Wrapped refetch calls in arrow functions for proper typing
4. ✅ Added ErrorBoundary to catch React component errors
5. ✅ Improved error states in Dashboard component

#### Best Practices
- Always use `check_status.sh` before starting work
- Run `monitor_and_restart.sh` during development to auto-recover from crashes
- Check browser console for client-side errors
- Use hard refresh after code changes if page seems stuck
- Monitor logs when debugging issues

### 7. Quick Reference Commands

```bash
# Check status of all services
./check_status.sh

# Start all services
./start_app.sh

# Stop all services
./stop_app.sh

# Monitor and auto-restart services
./monitor_and_restart.sh

# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# View monitor logs
tail -f monitor.log

# Restart just frontend (manual)
pkill -f vite
cd portfolio-dashboard-frontend && npm run dev &

# Restart just backend (manual)
pkill -f uvicorn
cd backend && source .venv/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
```

### 8. Architecture

```
┌─────────────────────────────────────────┐
│         ErrorBoundary (React)           │
│  ┌───────────────────────────────────┐  │
│  │      QueryClientProvider          │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │       App Routes            │  │  │
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │   Dashboard           │  │  │  │
│  │  │  │  - Error States       │  │  │  │
│  │  │  │  - Loading States     │  │  │  │
│  │  │  │  - Empty States       │  │  │  │
│  │  │  │  - Refetch Handlers   │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓ HTTP Requests
┌─────────────────────────────────────────┐
│     Backend (FastAPI + Uvicorn)         │
│  ┌───────────────────────────────────┐  │
│  │     API Error Handlers            │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │    Database Connection      │  │  │
│  │  │    - Retry Logic            │  │  │
│  │  │    - Health Checks          │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓ Monitored by
┌─────────────────────────────────────────┐
│    monitor_and_restart.sh               │
│  - Health checks every 30s              │
│  - Auto-restart on failure              │
│  - Logging to monitor.log               │
└─────────────────────────────────────────┘
```

## Summary

The application now has multiple layers of crash protection:
1. **React Error Boundary** - Catches UI errors
2. **Component Error States** - Graceful error display
3. **Service Monitoring** - Auto-restart crashed services
4. **Comprehensive Logging** - Easy debugging
5. **Status Checks** - Quick health verification

All services are currently running and healthy! 🎉
