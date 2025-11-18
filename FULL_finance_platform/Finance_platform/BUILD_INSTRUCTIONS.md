# Portfolio Dashboard - Build Instructions

## Quick Summary

This document provides complete instructions for building and running the Portfolio Dashboard application.

**Status:** ✅ Environment configured and ready to build

## What's Been Completed

### 1. Backend Setup ✅
- **Location:** `/home/user/Finance_platform/backend`
- **Configuration:** `.env` file created with development settings
- **Framework:** FastAPI + SQLAlchemy + PostgreSQL
- **Port:** 8000

### 2. Frontend Setup ✅
- **Location:** `/home/user/Finance_platform/portfolio-dashboard-frontend`
- **Configuration:** `.env` file created with API endpoint
- **Framework:** React + TypeScript + Vite + Material-UI
- **Port:** 5173 (Vite default) or 3000

### 3. Database Setup ✅
- **Database:** `portfolio_dashboard`
- **User:** `portfolio_user`
- **Password:** `password` (change in production!)
- **Tables:** 10 core tables created
- **PostgreSQL:** Running on port 5432

### 4. Build Scripts Created ✅
- **`build_app.sh`:** Complete build script (requires network)
- **`init_database.sh`:** Database initialization script (already run)

---

## Prerequisites

### Required Software
| Software | Version | Status |
|----------|---------|--------|
| Python | 3.11+ | ✅ Installed (3.11.14) |
| Node.js | 18+ | ✅ Installed |
| PostgreSQL | 14+ | ✅ Running (16) |
| npm | 8+ | ✅ Installed |

### Network Requirements
⚠️ **Important:** Building the application requires internet connectivity to:
- Install Python packages via pip
- Install npm packages
- Download dependencies

---

## Building the Application

### Option 1: Automated Build (Recommended)

When network connectivity is available, run:

```bash
cd /home/user/Finance_platform
bash build_app.sh
```

This script will:
1. ✅ Check all prerequisites
2. ⏳ Install Python dependencies (backend)
3. ⏳ Install npm dependencies (frontend)
4. ⏳ Build the frontend application
5. ✅ Verify setup

**Estimated time:** 5-10 minutes (depending on network speed)

### Option 2: Manual Build

If you prefer to build components individually:

#### Backend

```bash
cd /home/user/Finance_platform/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Frontend

```bash
cd /home/user/Finance_platform/portfolio-dashboard-frontend

# Install dependencies
npm install

# Build for production
npm run build
```

---

## Running the Application

### Development Mode

#### Backend

```bash
cd /home/user/Finance_platform/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Access:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

#### Frontend

```bash
cd /home/user/Finance_platform/portfolio-dashboard-frontend
npm run dev
```

**Access:**
- Application: http://localhost:5173 (Vite) or http://localhost:3000

### Production Mode

#### Backend

```bash
cd /home/user/Finance_platform/backend
source venv/bin/activate
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

#### Frontend

```bash
# Build first
cd /home/user/Finance_platform/portfolio-dashboard-frontend
npm run build

# Serve with a static server
npx serve -s dist -p 3000
```

---

## Environment Configuration

### Backend (.env)

Located at: `/home/user/Finance_platform/backend/.env`

**Key variables:**
```bash
DATABASE_URL=postgresql://portfolio_user:password@localhost:5432/portfolio_dashboard
SECRET_KEY=dev-secret-key-change-in-production-12345678
DEBUG=true
PORT=8000
```

### Frontend (.env)

Located at: `/home/user/Finance_platform/portfolio-dashboard-frontend/.env`

**Key variables:**
```bash
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Portfolio Dashboard
```

---

## Database Management

### Connection Information

```
Host: localhost
Port: 5432
Database: portfolio_dashboard
User: portfolio_user
Password: password
```

### Connect to Database

```bash
psql -U portfolio_user -d portfolio_dashboard
```

### Reinitialize Database

If you need to reset the database:

```bash
cd /home/user/Finance_platform

# Drop and recreate
psql -U postgres -c "DROP DATABASE IF EXISTS portfolio_dashboard;"
psql -U postgres -c "CREATE DATABASE portfolio_dashboard OWNER portfolio_user;"

# Reinitialize schema
bash init_database.sh
```

### View Tables

```bash
psql -U portfolio_user -d portfolio_dashboard -c "\dt"
```

---

## Project Structure

```
Finance_platform/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                  # Application entry point
│   │   ├── config.py                # Configuration management
│   │   ├── core/
│   │   │   └── database.py          # Database connection
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── fund.py
│   │   │   ├── company.py
│   │   │   ├── financial_metric.py
│   │   │   └── ...
│   │   └── api/
│   │       └── v1/                  # API endpoints
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # ✅ Environment config
│   └── README.md
│
├── portfolio-dashboard-frontend/    # React Frontend
│   ├── src/
│   │   ├── App.tsx                  # Main app component
│   │   ├── components/              # UI components
│   │   ├── pages/                   # Page views
│   │   ├── services/                # API services
│   │   └── types/                   # TypeScript types
│   ├── package.json                 # npm dependencies
│   ├── .env                         # ✅ Environment config
│   ├── vite.config.ts               # Vite configuration
│   └── README.md
│
├── build_app.sh                     # ✅ Automated build script
├── init_database.sh                 # ✅ Database initialization
├── BUILD_INSTRUCTIONS.md            # This file
└── README.md                        # Main project README
```

---

## Technology Stack

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Material-UI** - Component library
- **React Query** - Data fetching
- **Zustand** - State management
- **Recharts** - Data visualization

---

## Testing

### Backend Tests

```bash
cd /home/user/Finance_platform/backend
source venv/bin/activate
pytest
```

### Frontend Tests

```bash
cd /home/user/Finance_platform/portfolio-dashboard-frontend
npm test
```

---

## Troubleshooting

### Issue: Cannot connect to database

**Solution:**
```bash
# Check PostgreSQL status
pg_isready

# If not running, start it
pg_ctlcluster 16 main start
```

### Issue: Port already in use

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Issue: Python packages installation fails

**Check:**
1. Internet connectivity
2. Python version (3.11+)
3. pip version (`pip install --upgrade pip`)

### Issue: npm installation fails

**Check:**
1. Internet connectivity
2. Node.js version (18+)
3. npm version
4. Clear cache: `npm cache clean --force`

### Issue: Database connection refused

**Solution:**
```bash
# Verify PostgreSQL is running
pg_isready

# Check connection string in backend/.env
cat backend/.env | grep DATABASE_URL

# Test connection directly
psql -U portfolio_user -d portfolio_dashboard -c "SELECT 1"
```

---

## Next Steps

### After Building

1. **Start the backend:**
   ```bash
   cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   ```

2. **Start the frontend:**
   ```bash
   cd portfolio-dashboard-frontend && npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Development Workflow

1. Make changes to backend code in `backend/app/`
2. Make changes to frontend code in `portfolio-dashboard-frontend/src/`
3. Backend auto-reloads with `--reload` flag
4. Frontend auto-reloads with Vite
5. Test changes in the browser
6. Commit changes with git

### Production Deployment

See `PORTFOLIO_DASHBOARD_DEPLOYMENT_GUIDE.md` for:
- Docker containerization
- AWS deployment
- Cloud database setup
- Environment configuration
- Security best practices

---

## Support & Documentation

### Key Documentation Files

1. **README.md** - Project overview and quick start
2. **BUILD_INSTRUCTIONS.md** (this file) - Build and run instructions
3. **backend/README.md** - Backend API documentation
4. **portfolio-dashboard-frontend/README.md** - Frontend documentation
5. **PORTFOLIO_DASHBOARD_DEPLOYMENT_GUIDE.md** - Full deployment guide
6. **QUICK_REFERENCE_CARD.md** - Common commands reference

### Getting Help

- Check the troubleshooting section above
- Review the README files
- Check API docs at http://localhost:8000/docs
- Review error logs in terminal output

---

## Summary Checklist

- [x] PostgreSQL installed and running
- [x] Database and user created
- [x] Database schema initialized (10 tables)
- [x] Backend .env configured
- [x] Frontend .env configured
- [x] Build scripts created and tested
- [ ] Python dependencies installed (requires network)
- [ ] npm dependencies installed (requires network)
- [ ] Frontend built (requires network)
- [ ] Backend started
- [ ] Frontend started
- [ ] Application accessible

---

**Last Updated:** November 4, 2025
**Status:** Ready to build (pending network connectivity for package installation)
