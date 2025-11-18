#!/bin/bash

# Real Estate Dashboard Startup Script
# This script stops any running instances and starts both backend and frontend servers

echo "🛑 Stopping existing servers..."
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

echo "🚀 Starting backend server on port 8001..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload > /dev/null 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

sleep 3

echo "🚀 Starting frontend server on port 3000..."
cd ../frontend
npm run dev > /dev/null 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

sleep 3

echo ""
echo "✅ Servers started successfully!"
echo ""
echo "📍 Backend:  http://localhost:8001"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "💡 To stop servers: pkill -f 'uvicorn app.main:app' && pkill -f 'npm run dev'"
