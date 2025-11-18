# Claude Code Environment - Quick Setup Guide

## 🚀 Quick Start (One Command)

```bash
./start_claude_code.sh
```

This single command will:
- ✅ Check all prerequisites (Python, Node.js, PostgreSQL)
- ✅ Install PostgreSQL if missing (via Homebrew)
- ✅ Create Python virtual environment
- ✅ Install all backend dependencies with fallback strategies
- ✅ Install all frontend dependencies
- ✅ Setup PostgreSQL database and user
- ✅ Run database migrations
- ✅ Start backend server (FastAPI)
- ✅ Start frontend server (React)
- ✅ Perform health checks

---

## 📋 What Gets Installed

### Backend Dependencies
- **Core Framework:** FastAPI, Uvicorn
- **Database:** SQLAlchemy, Alembic, psycopg2-binary, asyncpg
- **Data Processing:** pandas, numpy, matplotlib
- **Excel/PDF:** openpyxl, xlsxwriter, pdfplumber, PyPDF2
- **Security:** python-jose, passlib, bcrypt
- **AI/ML:** anthropic (Claude API)
- **Testing:** pytest, pytest-asyncio, faker
- **Code Quality:** black, flake8, mypy, isort

### Frontend Dependencies
- **React 18** with TypeScript
- **Material-UI** components
- **Vite** build tool
- **React Router** for navigation
- **Axios** for API calls
- **Recharts** for data visualization

---

## 🎯 Access Points

Once started, access the application at:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 or :5173 | React UI |
| **Backend** | http://localhost:8000 | FastAPI server |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Database** | localhost:5432 | PostgreSQL |

**Database Credentials:**
- Database: `portfolio_dashboard`
- User: `portfolio_user`
- Password: `password`

---

## 📝 Log Files

View logs in real-time:

```bash
# Backend logs
tail -f backend.log

# Frontend logs
tail -f frontend.log

# Or use the watch command
watch -n 1 tail -20 backend.log
```

---

## 🛑 Stop Services

### Option 1: Use PIDs from startup
```bash
# Kill both services
kill $(cat .backend.pid) $(cat .frontend.pid)
```

### Option 2: Use the stop script
```bash
./stop_app.sh
```

### Option 3: Manual port cleanup
```bash
# Kill backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Kill frontend (port 3000 or 5173)
lsof -ti:3000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

---

## 🔧 Troubleshooting

### Backend won't start

**Check logs:**
```bash
tail -100 backend.log
```

**Common issues:**
- Port 8000 already in use: `lsof -ti:8000 | xargs kill -9`
- Database connection error: Ensure PostgreSQL is running
- Missing dependencies: Run `./start_claude_code.sh` again

### Frontend won't start

**Check logs:**
```bash
tail -100 frontend.log
```

**Common issues:**
- Port 3000/5173 already in use: `lsof -ti:3000 | xargs kill -9`
- Missing node_modules: `cd portfolio-dashboard-frontend && npm install`

### Database issues

**Check PostgreSQL status:**
```bash
# Homebrew installation
brew services list | grep postgresql

# System installation
pg_isready
```

**Restart PostgreSQL:**
```bash
# Homebrew
brew services restart postgresql@14

# System
sudo systemctl restart postgresql
```

**Recreate database:**
```bash
dropdb portfolio_dashboard
createdb portfolio_dashboard
./start_claude_code.sh
```

---

## 🔄 Development Workflow

### Daily Development

```bash
# 1. Start the app
./start_claude_code.sh

# 2. Make changes to code
# Backend: backend/app/
# Frontend: portfolio-dashboard-frontend/src/

# 3. Watch logs
tail -f backend.log
# Backend will auto-reload on changes (uvicorn --reload)
# Frontend will hot-reload automatically (Vite HMR)

# 4. Stop when done
./stop_app.sh
```

### Running Tests

```bash
# Backend tests
cd backend
source .venv/bin/activate
pytest

# With coverage
pytest --cov=app --cov-report=html

# Frontend tests (if configured)
cd portfolio-dashboard-frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
source .venv/bin/activate
black app/
isort app/
flake8 app/

# Frontend
cd portfolio-dashboard-frontend
npm run lint
```

---

## 🌐 Network & Proxy Support

The script automatically detects and uses `HTTP_PROXY` environment variable:

```bash
# Set proxy before running
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
./start_claude_code.sh
```

---

## 🔐 Environment Variables

Key environment variables in `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://portfolio_user:password@localhost:5432/portfolio_dashboard

# Security
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (optional)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here

# CORS (add your domains)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

---

## 📦 Manual Setup (Alternative)

If you prefer manual control:

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd portfolio-dashboard-frontend
npm install
npm run dev
```

### Database
```bash
createdb portfolio_dashboard
psql -d portfolio_dashboard -c "CREATE USER portfolio_user WITH PASSWORD 'password';"
psql -d portfolio_dashboard -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_dashboard TO portfolio_user;"
```

---

## 🐳 Docker Alternative

Use Docker Compose for containerized setup:

```bash
# Start all services
docker compose up --build -d

# View logs
docker compose logs -f backend

# Stop services
docker compose down
```

---

## 💡 Tips for Claude Code

1. **Virtual Environment:** The script creates `.venv` in backend directory. Always activate it:
   ```bash
   source backend/.venv/bin/activate
   ```

2. **Auto-reload:** Both backend and frontend support hot-reload. No need to restart when making changes.

3. **Database Migrations:** After changing models:
   ```bash
   cd backend
   source .venv/bin/activate
   alembic revision --autogenerate -m "Description"
   alembic upgrade head
   ```

4. **API Testing:** Use the interactive docs at http://localhost:8000/docs

5. **Log Monitoring:** Keep logs open in separate terminal windows

---

## 📚 Additional Resources

- **Full Documentation:** See `PORTFOLIO_DASHBOARD_DEPLOYMENT_GUIDE.md`
- **Quick Reference:** See `QUICK_REFERENCE_CARD.md`
- **API Documentation:** See `API_SETUP_GUIDE.md`
- **Build Instructions:** See `BUILD_INSTRUCTIONS.md`

---

## 🆘 Getting Help

1. Check logs: `backend.log` and `frontend.log`
2. Run health check: `curl http://localhost:8000/health`
3. Check service status: `./start_app.sh --status`
4. View this guide: `cat CLAUDE_CODE_SETUP.md`

---

**Version:** 1.0.0
**Last Updated:** November 2025
**Optimized for:** Claude Code development environment
