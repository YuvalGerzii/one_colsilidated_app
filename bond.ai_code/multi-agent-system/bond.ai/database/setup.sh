#!/bin/bash

# Bond.AI Database Setup Script
# Sets up PostgreSQL database and Redis

set -e

echo "🚀 Setting up Bond.AI database infrastructure..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_NAME="${DB_NAME:-bondai}"
DB_USER="${DB_USER:-bondai_user}"
DB_PASSWORD="${DB_PASSWORD:-bondai_password}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

echo "Configuration:"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Host: $DB_HOST:$DB_PORT"
echo "  Redis: $REDIS_HOST:$REDIS_PORT"
echo ""

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    echo "Please install PostgreSQL first:"
    echo "  macOS: brew install postgresql@14"
    echo "  Ubuntu: sudo apt-get install postgresql-14"
    exit 1
fi

echo -e "${GREEN}✓${NC} PostgreSQL is installed"

# Check if Redis is installed
if ! command -v redis-cli &> /dev/null; then
    echo -e "${YELLOW}⚠${NC}  Redis is not installed"
    echo "Installing Redis is recommended:"
    echo "  macOS: brew install redis"
    echo "  Ubuntu: sudo apt-get install redis-server"
else
    echo -e "${GREEN}✓${NC} Redis is installed"
fi

# Check if PostgreSQL is running
if ! pg_isready -h $DB_HOST -p $DB_PORT &> /dev/null; then
    echo -e "${YELLOW}⚠${NC}  PostgreSQL is not running"
    echo "Starting PostgreSQL..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql@14
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo service postgresql start
    fi

    sleep 2
fi

echo -e "${GREEN}✓${NC} PostgreSQL is running"

# Create database and user
echo ""
echo "📦 Creating database and user..."

# Create user if doesn't exist
psql -h $DB_HOST -p $DB_PORT -U postgres -tc "SELECT 1 FROM pg_user WHERE usename = '$DB_USER'" | grep -q 1 || \
  psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"

echo -e "${GREEN}✓${NC} Database user created/verified"

# Create database if doesn't exist
psql -h $DB_HOST -p $DB_PORT -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
  psql -h $DB_HOST -p $DB_PORT -U postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;"

echo -e "${GREEN}✓${NC} Database created/verified"

# Grant privileges
psql -h $DB_HOST -p $DB_PORT -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo -e "${GREEN}✓${NC} Privileges granted"

# Run schema
echo ""
echo "🏗️  Creating database schema..."
export PGPASSWORD=$DB_PASSWORD
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$(dirname "$0")/schema.sql"

echo -e "${GREEN}✓${NC} Schema created successfully"

# Check if Redis is running
if command -v redis-cli &> /dev/null; then
    echo ""
    echo "🔄 Checking Redis..."

    if redis-cli -h $REDIS_HOST -p $REDIS_PORT ping &> /dev/null; then
        echo -e "${GREEN}✓${NC} Redis is running"
    else
        echo -e "${YELLOW}⚠${NC}  Redis is not running"
        echo "Starting Redis..."

        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew services start redis
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo service redis-server start
        fi

        sleep 1

        if redis-cli -h $REDIS_HOST -p $REDIS_PORT ping &> /dev/null; then
            echo -e "${GREEN}✓${NC} Redis started successfully"
        else
            echo -e "${RED}❌ Failed to start Redis${NC}"
        fi
    fi
fi

# Create .env file
echo ""
echo "📝 Creating .env file..."

cat > "$(dirname "$0")/../.env" <<EOF
# Database Configuration
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

# Redis Configuration
REDIS_URL=redis://$REDIS_HOST:$REDIS_PORT

# Server Configuration
PORT=3000
NODE_ENV=development

# JWT Secret (change in production!)
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# CORS
CORS_ORIGIN=http://localhost:3001

# Optional: OpenAI API Key for NLP features
# OPENAI_API_KEY=your-openai-api-key
EOF

echo -e "${GREEN}✓${NC} .env file created"

echo ""
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run seed script: npm run seed:1000"
echo "  2. Start server: npm run dev"
echo ""
echo "Connection string:"
echo "  postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
echo ""
