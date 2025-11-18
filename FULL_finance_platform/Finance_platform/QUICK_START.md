# Portfolio Dashboard - Quick Start Guide

## 🚀 Easy Startup

### First Time Setup

1. **Build the application** (one-time setup):
   ```bash
   cd /home/user/Finance_platform
   bash build_app.sh
   ```
   This installs all dependencies and sets up the database.

### Starting the Application

**Easy way** - Just run:
```bash
./start_app.sh
```

This single command:
- ✅ Starts PostgreSQL database
- ✅ Starts Backend API (port 8000)
- ✅ Starts Frontend UI (port 3000)
- ✅ Shows live logs

### Accessing the Application

Once started, open your browser:

- **Frontend Dashboard**: http://localhost:3000
- **Market Data Page**: http://localhost:3000/market-data
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Managing Services

```bash
# Check if services are running
./start_app.sh --status

# Stop all services
./start_app.sh --stop
# OR
./stop_app.sh

# Restart all services
./start_app.sh --restart
```

### Viewing Logs

```bash
# Backend logs
tail -f /tmp/portfolio_backend.log

# Frontend logs
tail -f /tmp/portfolio_frontend.log
```

## 📊 Market Data Integration

The Market Data Integration is **fully functional** and includes:

### Features
- ✅ **Automatic Database Persistence** - All market data is automatically saved
- ✅ **24-Hour Cache** - Reduces API calls by caching data for 24 hours
- ✅ **Multiple Data Sources**:
  - CoStar (cap rates, market trends, vacancy rates)
  - Zillow/Redfin (property values, rent estimates)
  - Census (demographics, income, employment)
  - Walk Score (walkability, transit, bike scores)

### How It Works

1. **User searches** for property via UI (http://localhost:3000/market-data)
2. **Backend checks database** for recent data (< 24 hours old)
3. If not found or expired:
   - **Fetches from APIs** (or uses mock data if no API keys)
   - **Automatically saves** to database
   - **Returns results** to user
4. Next search for same property uses **cached data** from database

### Testing It

1. Go to http://localhost:3000/market-data
2. Enter property details:
   - Address: 123 Main St
   - City: San Francisco
   - State: CA
   - ZIP: 94103
   - Property Type: Multifamily
3. Click "Get Market Data"
4. Data is fetched and **automatically saved to database**

### Viewing Saved Data

```bash
# Connect to database
PGPASSWORD=password psql -U portfolio_user -d portfolio_dashboard

# View all market data
SELECT id, address, city, state, property_type, created_at FROM market_data;

# View details of a specific record
SELECT * FROM market_data WHERE id = 1;

# Exit
\q
```

## 🔧 Troubleshooting

### PostgreSQL Not Running
```bash
pg_ctlcluster 16 main start
```

### Backend Won't Start
Check logs:
```bash
tail -f /tmp/portfolio_backend.log
```

### Frontend Won't Start
Check logs:
```bash
tail -f /tmp/portfolio_frontend.log
```

### Database Connection Issues
Test connection:
```bash
PGPASSWORD=password psql -U portfolio_user -d portfolio_dashboard -c "SELECT version();"
```

## 📝 Database Credentials

- **Database**: portfolio_dashboard
- **User**: portfolio_user
- **Password**: password
- **Host**: localhost
- **Port**: 5432

**⚠️ Change these in production!**

## 🛠️ Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd portfolio-dashboard-frontend
npm run dev
```

### Database Migrations
```bash
# View current schema
PGPASSWORD=password psql -U portfolio_user -d portfolio_dashboard -c "\d market_data"
```

## 📚 API Endpoints

### Market Data Endpoints
- `POST /api/v1/market-data/comprehensive` - Get all market data
- `POST /api/v1/market-data/investment-summary` - Get investment analysis
- `GET /api/v1/health` - Health check

Full API documentation: http://localhost:8000/docs

## 💾 Data Persistence

All market data queries are **automatically persisted** to the PostgreSQL database:
- No manual saving required
- Data cached for 24 hours
- Use `force_refresh=true` parameter to bypass cache
- Automatic cleanup of old data (future enhancement)

## 🎯 Next Steps

1. Configure API keys (see `API_SETUP_GUIDE.md`)
2. Customize UI styling
3. Add more property types
4. Integrate with existing workflows
5. Set up production deployment

---

**Last Updated**: November 4, 2025
