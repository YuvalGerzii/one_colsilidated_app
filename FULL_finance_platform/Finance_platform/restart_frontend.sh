#!/bin/bash
# Restart Frontend with Clean Cache

echo "🔄 Restarting Frontend..."
echo ""

# Kill existing frontend processes
echo "Stopping existing frontend..."
pkill -f "vite" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
sleep 2

# Clear Vite cache
echo "Clearing Vite cache..."
cd "$(dirname "$0")/portfolio-dashboard-frontend"
rm -rf node_modules/.vite
rm -rf dist

# Start frontend
echo "Starting Vite dev server..."
npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Check if it's running
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo ""
    echo "✅ Frontend started successfully!"
    echo ""
    echo "📍 URL: http://localhost:3000"
    echo "📋 PID: $FRONTEND_PID"
    echo "📄 Logs: /tmp/frontend.log"
    echo ""
    echo "🌐 Opening in browser..."

    # Try to open in default browser
    if command -v open &> /dev/null; then
        open http://localhost:3000
    elif command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000
    else
        echo "⚠️  Could not open browser automatically"
        echo "   Please open: http://localhost:3000"
    fi

    echo ""
    echo "💡 If the page is blank:"
    echo "   1. Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)"
    echo "   2. Clear browser cache completely"
    echo "   3. Try incognito/private mode"
    echo "   4. Check console for errors (F12)"
else
    echo ""
    echo "❌ Frontend failed to start"
    echo "   Check logs: tail -f /tmp/frontend.log"
    exit 1
fi
