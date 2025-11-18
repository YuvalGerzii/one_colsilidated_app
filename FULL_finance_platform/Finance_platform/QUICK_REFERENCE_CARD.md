# Portfolio Dashboard - Quick Reference Card

## 🚀 Quick Start (30 Minutes)

### 1. Database Setup (5 min)
```bash
# Create database
createdb portfolio_dashboard

# Create user
psql postgres -c "CREATE USER portfolio_user WITH PASSWORD 'your_password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_dashboard TO portfolio_user;"

# Apply schema
psql -U portfolio_user -d portfolio_dashboard -f database/init/01_schema.sql

# Verify
psql -U portfolio_user -d portfolio_dashboard -c "\dt"
```

### 2. Backend Setup (10 min)
```bash
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Update DATABASE_URL, SECRET_KEY, OPENAI_API_KEY

# Run server
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup (10 min)
```bash
cd frontend

# Install dependencies
npm install

# Configure API URL
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env

# Run development server
npm start
```

### 4. Verify (5 min)
```bash
# Test backend
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test frontend
open http://localhost:3000
```

---

## 🐳 Docker Quick Start (10 Minutes)

```bash
# Create environment file
cat > .env << 'EOF'
SECRET_KEY=$(openssl rand -hex 32)
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://portfolio_user:password@db:5432/portfolio_dashboard
EOF

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access services
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/api/docs
# Database: localhost:5432
```

---

## 📊 Common Commands

### Database
```bash
# Connect to database
psql -U portfolio_user -d portfolio_dashboard

# List tables
\dt

# View table structure
\d+ portfolio_companies

# Run query
SELECT * FROM funds LIMIT 5;

# Backup database
pg_dump -U portfolio_user portfolio_dashboard > backup.sql

# Restore database
psql -U portfolio_user portfolio_dashboard < backup.sql
```

### Backend
```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
uvicorn app.main:app --reload --port 8000

# Run with debugger
uvicorn app.main:app --reload --port 8000 --log-level debug

# Run tests
pytest

# Check code style
black app/
flake8 app/

# Generate requirements
pip freeze > requirements.txt
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Check TypeScript
npm run type-check

# Lint code
npm run lint
```

### Docker
```bash
# Build and start
docker-compose up --build -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart single service
docker-compose restart backend

# Remove everything (including volumes)
docker-compose down -v

# Rebuild single service
docker-compose build backend
docker-compose up -d backend
```

---

## 🔧 Environment Variables

### Backend (.env)
```bash
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/portfolio_dashboard
SECRET_KEY=generate-with-openssl-rand-hex-32
OPENAI_API_KEY=sk-your-openai-key

# Optional
FINANCIAL_DATASETS_API_KEY=your-key
UPLOAD_DIR=/var/uploads/portfolio_dashboard
MAX_UPLOAD_SIZE_MB=50
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENVIRONMENT=development
```

---

## 📝 API Endpoints

### Authentication
```bash
POST /api/v1/auth/login
POST /api/v1/auth/register
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

### Funds
```bash
GET    /api/v1/funds
POST   /api/v1/funds
GET    /api/v1/funds/{fund_id}
PUT    /api/v1/funds/{fund_id}
DELETE /api/v1/funds/{fund_id}
```

### Companies
```bash
GET    /api/v1/companies
POST   /api/v1/companies
GET    /api/v1/companies/{company_id}
PUT    /api/v1/companies/{company_id}
DELETE /api/v1/companies/{company_id}
```

### Financial Metrics
```bash
GET  /api/v1/companies/{company_id}/financials
POST /api/v1/companies/{company_id}/financials
GET  /api/v1/companies/{company_id}/financials/{metric_id}
PUT  /api/v1/companies/{company_id}/financials/{metric_id}
```

### Models
```bash
POST /api/v1/models/generate
GET  /api/v1/models/{model_id}
GET  /api/v1/models/{model_id}/download
```

### Test with curl:
```bash
# Create fund
curl -X POST http://localhost:8000/api/v1/funds \
  -H "Content-Type: application/json" \
  -d '{
    "fund_name": "Test Fund I",
    "vintage_year": 2024,
    "fund_size": 100000000,
    "committed_capital": 80000000
  }'

# Get all funds
curl http://localhost:8000/api/v1/funds

# Get company financials
curl http://localhost:8000/api/v1/companies/{company_id}/financials
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Must be 3.11+

# Check database connection
psql -U portfolio_user -d portfolio_dashboard -c "SELECT 1"

# Check .env file
cat backend/.env

# Check port availability
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### Frontend won't start
```bash
# Clear node_modules
rm -rf node_modules package-lock.json
npm install

# Check backend is running
curl http://localhost:8000/health

# Check CORS configuration
# Backend .env should include: CORS_ORIGINS=http://localhost:3000
```

### Database connection fails
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list  # macOS

# Test connection
psql -U portfolio_user -d portfolio_dashboard

# Reset password
psql postgres -c "ALTER USER portfolio_user PASSWORD 'new_password';"
```

### Docker issues
```bash
# Clear everything
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔑 Important Files

### Project Structure
```
portfolio-dashboard/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── config.py        # Settings
│   │   └── routers/         # API routes
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── services/api.ts  # API client
│   │   └── components/
│   ├── package.json
│   ├── .env
│   └── Dockerfile
├── database/
│   ├── init/
│   │   └── 01_schema.sql    # Database schema
│   └── migrations/
└── docker-compose.yml        # Docker orchestration
```

### Reference Documentation
```
/mnt/project/
├── Portfolio_Dashboard_Implementation_Plan.md
├── Portfolio_Dashboard_Database_Schema.md
├── Portfolio_Dashboard_Quick_Start.md
├── DCF_MODEL_GUIDE.md
├── LBO_MODEL_GUIDE.md
├── MERGER_MODEL_USER_GUIDE.md
├── DD_TRACKER_USER_GUIDE.md
└── QOE_ANALYSIS_USER_GUIDE.md
```

---

## 🎯 Development Workflow

### Starting a new feature
```bash
# 1. Create feature branch
git checkout -b feature/new-dashboard

# 2. Backend: Create router
touch backend/app/routers/new_feature.py

# 3. Frontend: Create component
mkdir frontend/src/components/NewFeature
touch frontend/src/components/NewFeature/index.tsx

# 4. Run tests
cd backend && pytest
cd frontend && npm test

# 5. Commit changes
git add .
git commit -m "Add: New dashboard feature"
git push origin feature/new-dashboard
```

### Making a database change
```bash
# 1. Create migration file
touch database/migrations/002_add_new_table.sql

# 2. Write migration
nano database/migrations/002_add_new_table.sql

# 3. Apply migration
psql -U portfolio_user -d portfolio_dashboard -f database/migrations/002_add_new_table.sql

# 4. Update models.py
nano backend/app/models.py
```

### Deploying to production
```bash
# 1. Run tests
pytest && npm test

# 2. Build Docker images
docker-compose build

# 3. Tag for production
docker tag portfolio-backend:latest portfolio-backend:v1.0.0

# 4. Push to registry (ECR, Docker Hub, etc.)
docker push <registry>/portfolio-backend:v1.0.0

# 5. Deploy to server
ssh production-server
docker-compose pull
docker-compose up -d
```

---

## 📞 Support & Resources

### Documentation
- Full Deployment Guide: `PORTFOLIO_DASHBOARD_DEPLOYMENT_GUIDE.md`
- Implementation Plan: `/mnt/project/Portfolio_Dashboard_Implementation_Plan.md`
- Database Schema: `/mnt/project/Portfolio_Dashboard_Database_Schema.md`

### External Resources
- FastAPI Docs: https://fastapi.tiangolo.com/
- React Docs: https://react.dev/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Docker Docs: https://docs.docker.com/

### Getting Help
1. Check documentation in `/mnt/project/`
2. Review API docs at http://localhost:8000/api/docs
3. Use Claude Code/Cursor for development assistance
4. Check logs: `docker-compose logs -f`

---

## ✅ Pre-Launch Checklist

### Development
- [ ] All tests passing (`pytest` and `npm test`)
- [ ] No console errors in frontend
- [ ] API documentation up to date
- [ ] Database migrations tested
- [ ] Sample data loaded

### Security
- [ ] Change default passwords
- [ ] Generate strong SECRET_KEY
- [ ] API keys secured in .env
- [ ] CORS configured correctly
- [ ] Input validation on all endpoints

### Performance
- [ ] Database indexes created
- [ ] Large queries optimized
- [ ] Frontend bundle size < 1MB
- [ ] API response times < 500ms
- [ ] Images optimized

### Production Ready
- [ ] Environment variables set
- [ ] SSL certificates configured
- [ ] Backups scheduled
- [ ] Monitoring configured
- [ ] Error tracking enabled
- [ ] Documentation complete

---

*Quick Reference v1.0.0 | November 2025*
