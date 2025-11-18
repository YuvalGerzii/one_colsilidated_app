# Frontend Troubleshooting Guide

## Current Status ✅

The application is **running correctly**:
- ✅ Backend API: http://localhost:8000 (responding)
- ✅ Frontend Server: http://localhost:3000 (responding)
- ✅ Database: 5 companies, 122 market data records
- ✅ API Proxy: Working (tested successfully)

## If Dashboard Appears Blank

### Step 1: Clear Browser Cache
The most common issue is browser cache showing old empty state.

**Chrome:**
1. Open http://localhost:3000
2. Press `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows/Linux)
3. Or: Right-click → Inspect → Network tab → Check "Disable cache" → Refresh

**Safari:**
1. Open http://localhost:3000
2. Press `Cmd + Option + E` to empty caches
3. Then `Cmd + R` to reload

**Firefox:**
1. Open http://localhost:3000
2. Press `Cmd + Shift + R` (Mac) or `Ctrl + Shift + R` (Windows/Linux)

### Step 2: Check Browser Console

1. Open http://localhost:3000
2. Press `F12` or `Cmd + Option + I` (Mac) or `Ctrl + Shift + I` (Windows)
3. Go to **Console** tab
4. Look for red error messages

**Common Errors and Fixes:**

- **"Failed to fetch"** → Backend not running, restart with `./start_app.sh`
- **"Unexpected token"** → JavaScript syntax error, check recent code changes
- **"Module not found"** → Missing dependency, run `npm install`
- **Empty/nothing** → Hard refresh with cache clear (Step 1)

### Step 3: Test API Directly

Open these URLs in your browser:

1. **Backend Health**: http://localhost:8000/api/v1/health
   - Should show: `{"status":"healthy","database":"up",...}`

2. **Companies API**: http://localhost:8000/api/v1/companies/
   - Should show: JSON array with 5 companies

3. **Frontend Proxy**: http://localhost:3000/api/v1/companies/
   - Should show: Same JSON array (proxied through Vite)

If any of these fail, the issue is with the server, not the browser.

### Step 4: Try a Different Browser

Sometimes cache persists even after clearing. Try:
- Chrome → Safari
- Safari → Firefox
- Or use Incognito/Private mode

### Step 5: Check for JavaScript Disabled

Make sure JavaScript is enabled in your browser:
- **Chrome**: Settings → Privacy and security → Site Settings → JavaScript → Allowed
- **Safari**: Preferences → Security → Enable JavaScript
- **Firefox**: about:config → javascript.enabled → true

### Step 6: Verify React is Loading

1. Open http://localhost:3000
2. Press `F12` to open DevTools
3. Go to **Elements** tab (Chrome) or **Inspector** tab (Firefox)
4. Look for `<div id="root">`
5. It should have child elements (Dashboard components)
6. If it's empty (`<div id="root"></div>`), React failed to mount

### Step 7: Check Network Requests

1. Open http://localhost:3000
2. Press `F12` → Go to **Network** tab
3. Refresh the page
4. Look for:
   - ✅ `index.html` → 200 OK
   - ✅ `src/index.tsx` → 200 OK
   - ✅ `src/App.tsx` → 200 OK
   - ✅ `/api/v1/companies/` → 200 OK (should return JSON)

If any show red (404, 500), that's your issue.

## Manual Restart

If all else fails, restart everything:

```bash
# Stop all services
pkill -f uvicorn
pkill -f vite
pkill -f "npm run dev"

# Start backend
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &

# Start frontend
cd ../portfolio-dashboard-frontend
npm run dev &

# Wait 5 seconds
sleep 5

# Open browser
open http://localhost:3000
```

## Expected Dashboard View

Once working, you should see:

### Header
- "Portfolio Overview" title
- "Add Company" button

### KPI Cards (4 cards)
1. Total Revenue: $175M (+8.4%)
2. Total EBITDA: $41M (+5.1%)
3. Operating Cash Flow: $24.6M (+3.2%)
4. Portfolio ROI: Multiple displayed

### Charts Section
- **Revenue & EBITDA Trend**: Line chart by year
- **Sector Allocation**: Pie chart showing Technology, Healthcare, etc.

### Companies Table
Should list 5 companies:
1. TechCorp Solutions - Technology (Active)
2. HealthTech Innovations - Healthcare (Active)
3. FinServe Group - Financial Services (Exited)
4. CloudScale Systems - Technology (Active)
5. EcommerceNow - Consumer (Active)

### Activity Feed
Recent updates for the companies

## Still Not Working?

If the page is still blank after all these steps:

1. **Take a screenshot** of:
   - The blank page
   - Browser console (F12 → Console tab)
   - Network tab (F12 → Network tab, with requests shown)

2. **Share the error messages** from the console

3. **Check if the data is accessible**:
   ```bash
   curl http://localhost:3000/api/v1/companies/ | python3 -m json.tool
   ```

   Should output JSON with 5 companies. If this works but browser doesn't, it's a browser-specific issue.

## Quick Test Script

Run this to verify everything:

```bash
echo "=== System Check ==="
echo "Backend: $(curl -s http://localhost:8000/api/v1/health | grep -o '"status":"[^"]*"')"
echo "Frontend: $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000)"
echo "Companies: $(curl -s http://localhost:3000/api/v1/companies/ | python3 -c 'import sys,json; print(len(json.load(sys.stdin)))' 2>/dev/null) available"
echo ""
echo "If all show OK/200/5, the issue is in your browser."
echo "Try: Hard refresh (Cmd+Shift+R) or different browser"
```
