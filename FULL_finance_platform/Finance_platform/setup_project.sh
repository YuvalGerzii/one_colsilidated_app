#!/bin/bash

# ============================================================================
# Portfolio Dashboard - Automated Setup Script
# ============================================================================
# This script initializes the project structure and prepares the environment
# for development.
#
# Usage: bash setup_project.sh
#
# Requirements:
#   - Python 3.11+
#   - Node.js 16+
#   - PostgreSQL 14+
#   - Git
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_NAME="portfolio-dashboard"
DB_NAME="portfolio_dashboard"
DB_USER="portfolio_user"
DB_PASSWORD="change_this_password_123!"

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║       Portfolio Dashboard - Automated Setup Script        ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check Python
if command -v python3.11 &> /dev/null; then
    PYTHON_VERSION=$(python3.11 --version)
    echo -e "${GREEN}✓${NC} Python 3.11+ found: $PYTHON_VERSION"
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
    if [ "$(echo "$PYTHON_VERSION >= 3.11" | bc)" -eq 1 ]; then
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    else
        echo -e "${RED}✗${NC} Python 3.11+ required, found $PYTHON_VERSION"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Python not found. Please install Python 3.11+"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js found: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓${NC} npm found: v$NPM_VERSION"
else
    echo -e "${RED}✗${NC} npm not found"
    exit 1
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    echo -e "${GREEN}✓${NC} PostgreSQL found: v$PSQL_VERSION"
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL client not found (optional for remote DB)"
fi

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}✓${NC} Git found: $GIT_VERSION"
else
    echo -e "${RED}✗${NC} Git not found"
    exit 1
fi

echo ""

# ============================================================================
# Step 2: Create Project Structure
# ============================================================================

echo -e "${YELLOW}Step 2: Creating project structure...${NC}"

# Create main directories
mkdir -p $PROJECT_NAME/{backend/{app/{routers,services,utils},tests},frontend/src/{components,pages,services,types},database/{init,migrations},deploy}

cd $PROJECT_NAME

# Create placeholder files
touch backend/app/__init__.py
touch backend/app/routers/__init__.py
touch backend/app/services/__init__.py
touch backend/app/utils/__init__.py
touch backend/tests/__init__.py

echo -e "${GREEN}✓${NC} Project structure created"

# ============================================================================
# Step 3: Create Backend Files
# ============================================================================

echo -e "${YELLOW}Step 3: Creating backend configuration files...${NC}"

# Create requirements.txt
cat > backend/requirements.txt << 'EOF'
# FastAPI Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Data Validation
pydantic==2.5.3
pydantic-settings==2.1.0

# Excel Processing
openpyxl==3.1.2
xlsxwriter==3.1.9

# PDF Processing
pdfplumber==0.10.3
PyPDF2==3.0.1

# AI / ML
openai==1.10.0

# Date/Time
python-dateutil==2.8.2

# HTTP Requests
httpx==0.26.0
requests==2.31.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3

# Utilities
python-slugify==8.0.1
EOF

echo -e "${GREEN}✓${NC} requirements.txt created"

# Create .env.example
cat > backend/.env.example << 'EOF'
# Database
DATABASE_URL=postgresql://portfolio_user:change_password@localhost:5432/portfolio_dashboard

# Security
SECRET_KEY=generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key-here

# Financial Datasets API (optional)
FINANCIAL_DATASETS_API_KEY=your-api-key-here

# File Storage
UPLOAD_DIR=/var/uploads/portfolio_dashboard
MAX_UPLOAD_SIZE_MB=50

# Environment
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
EOF

echo -e "${GREEN}✓${NC} .env.example created"

# Create actual .env with generated SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "CHANGE-THIS-SECRET-KEY-$(date +%s)")
cp backend/.env.example backend/.env
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/generate-with-openssl-rand-hex-32/$SECRET_KEY/" backend/.env
else
    sed -i "s/generate-with-openssl-rand-hex-32/$SECRET_KEY/" backend/.env
fi

echo -e "${GREEN}✓${NC} .env created with generated SECRET_KEY"

# ============================================================================
# Step 4: Create Frontend Files
# ============================================================================

echo -e "${YELLOW}Step 4: Creating frontend configuration files...${NC}"

# Create package.json
cat > frontend/package.json << 'EOF'
{
  "name": "portfolio-dashboard-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.3",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.15.5",
    "@mui/material": "^5.15.5",
    "@tanstack/react-query": "^5.17.9",
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "axios": "^1.6.5",
    "date-fns": "^3.3.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.3",
    "react-scripts": "5.0.1",
    "recharts": "^2.10.4",
    "typescript": "^5.3.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
EOF

echo -e "${GREEN}✓${NC} package.json created"

# Create frontend .env
cat > frontend/.env << 'EOF'
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_ENVIRONMENT=development
EOF

echo -e "${GREEN}✓${NC} Frontend .env created"

# ============================================================================
# Step 5: Create Docker Files
# ============================================================================

echo -e "${YELLOW}Step 5: Creating Docker configuration...${NC}"

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    container_name: portfolio_db
    environment:
      POSTGRES_DB: portfolio_dashboard
      POSTGRES_USER: portfolio_user
      POSTGRES_PASSWORD: change_this_password_123!
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    networks:
      - portfolio_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U portfolio_user -d portfolio_dashboard"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: portfolio_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://portfolio_user:change_this_password_123!@db:5432/portfolio_dashboard
    volumes:
      - ./backend:/app
      - uploads:/var/uploads/portfolio_dashboard
    depends_on:
      db:
        condition: service_healthy
    networks:
      - portfolio_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: portfolio_frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - portfolio_network

volumes:
  postgres_data:
  uploads:

networks:
  portfolio_network:
    driver: bridge
EOF

echo -e "${GREEN}✓${NC} docker-compose.yml created"

# ============================================================================
# Step 6: Create .gitignore
# ============================================================================

echo -e "${YELLOW}Step 6: Creating .gitignore...${NC}"

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.coverage
htmlcov/
.pytest_cache/

# Build
/build
/dist
*.egg-info

# Database
*.db
*.sqlite3
*.sql.backup

# Logs
*.log
logs/

# Uploads
uploads/
/var/uploads/

# OS
Thumbs.db
.DS_Store
EOF

echo -e "${GREEN}✓${NC} .gitignore created"

# ============================================================================
# Step 7: Initialize Git Repository
# ============================================================================

echo -e "${YELLOW}Step 7: Initializing Git repository...${NC}"

git init
git add .
git commit -m "Initial commit: Project structure and configuration"

echo -e "${GREEN}✓${NC} Git repository initialized"

# ============================================================================
# Step 8: Setup Python Virtual Environment
# ============================================================================

echo -e "${YELLOW}Step 8: Setting up Python virtual environment...${NC}"

cd backend
$PYTHON_CMD -m venv venv

# Activate virtual environment and install dependencies
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓${NC} Python virtual environment created and dependencies installed"

cd ..

# ============================================================================
# Step 9: Database Setup (if PostgreSQL is available)
# ============================================================================

echo ""
echo -e "${YELLOW}Step 9: Database setup${NC}"

if command -v psql &> /dev/null; then
    echo "Would you like to create the database now? (y/n)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo "Creating database..."
        
        # Try to create database and user
        psql postgres -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Database may already exist"
        psql postgres -c "CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User may already exist"
        psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null
        
        echo -e "${GREEN}✓${NC} Database setup complete"
        
        # Apply schema if it exists
        if [ -f "database/init/01_schema.sql" ]; then
            echo "Applying database schema..."
            psql -U $DB_USER -d $DB_NAME -f database/init/01_schema.sql
            echo -e "${GREEN}✓${NC} Database schema applied"
        else
            echo -e "${YELLOW}⚠${NC} Database schema file not found. You'll need to create it."
        fi
    else
        echo -e "${YELLOW}⚠${NC} Skipping database creation. Run manually later."
    fi
else
    echo -e "${YELLOW}⚠${NC} PostgreSQL not found. You'll need to set up the database manually."
fi

# ============================================================================
# Step 10: Install Frontend Dependencies
# ============================================================================

echo ""
echo -e "${YELLOW}Step 10: Installing frontend dependencies...${NC}"
echo "This may take a few minutes..."

cd frontend
npm install

echo -e "${GREEN}✓${NC} Frontend dependencies installed"

cd ..

# ============================================================================
# Final Summary
# ============================================================================

echo ""
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║                  Setup Complete! 🎉                        ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${GREEN}Project initialized successfully!${NC}"
echo ""
echo "📁 Project structure:"
echo "   • backend/     - Python FastAPI backend"
echo "   • frontend/    - React TypeScript frontend"
echo "   • database/    - PostgreSQL schemas and migrations"
echo "   • deploy/      - Deployment configurations"
echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Or use Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "📚 Documentation:"
echo "   • Full Guide: PORTFOLIO_DASHBOARD_DEPLOYMENT_GUIDE.md"
echo "   • Quick Ref:  QUICK_REFERENCE_CARD.md"
echo ""
echo "🌐 Access your application:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend:  http://localhost:8000"
echo "   • API Docs: http://localhost:8000/api/docs"
echo ""
echo -e "${YELLOW}⚠ Important:${NC}"
echo "   • Update backend/.env with your API keys"
echo "   • Change database password in production"
echo "   • Review security settings before deployment"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
