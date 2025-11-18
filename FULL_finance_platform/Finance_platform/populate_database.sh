#!/bin/bash
# ============================================
# Database Population Script
# ============================================
# This script populates the database with market data from Real_estate_db

set -e

echo "============================================"
echo "Database Population Script"
echo "============================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Database connection details (from .env or defaults)
DB_HOST=${POSTGRES_HOST:-localhost}
DB_PORT=${POSTGRES_PORT:-5432}
DB_NAME=${POSTGRES_DB:-portfolio_dashboard}
DB_USER=${POSTGRES_USER:-portfolio_user}
DB_PASSWORD=${POSTGRES_PASSWORD:-portfolio_password}

# Export password for psql
export PGPASSWORD=$DB_PASSWORD

echo "Database Configuration:"
echo "  Host: $DB_HOST"
echo "  Port: $DB_PORT"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    echo -e "${RED}✗ psql command not found${NC}"
    echo "Please install PostgreSQL client tools"
    exit 1
fi
echo -e "${GREEN}✓ psql is available${NC}"

# Test database connection
echo ""
echo "Testing database connection..."
if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "SELECT 1;" &> /dev/null; then
    echo -e "${GREEN}✓ Successfully connected to database${NC}"
else
    echo -e "${RED}✗ Failed to connect to database${NC}"
    echo "Please check your database connection settings"
    exit 1
fi

# Function to run SQL file
run_sql_file() {
    local file=$1
    local description=$2

    echo ""
    echo "Running: $description"
    echo "File: $file"

    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ File not found: $file${NC}"
        return 1
    fi

    if psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$file"; then
        echo -e "${GREEN}✓ Successfully executed${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to execute${NC}"
        return 1
    fi
}

# Function to run Python script
run_python_script() {
    local script=$1
    local description=$2

    echo ""
    echo "Running: $description"
    echo "Script: $script"

    if [ ! -f "$script" ]; then
        echo -e "${RED}✗ Script not found: $script${NC}"
        return 1
    fi

    # Set environment variables for Python script
    export DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

    if python3 "$script"; then
        echo -e "${GREEN}✓ Successfully executed${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to execute${NC}"
        return 1
    fi
}

echo ""
echo "============================================"
echo "Starting Database Population"
echo "============================================"

# 1. Create Real Estate Market Data Schema
if [ -f "Real_estate_db/real_estate_market_data_schema.sql" ]; then
    run_sql_file "Real_estate_db/real_estate_market_data_schema.sql" "Real Estate Market Data Schema"
else
    echo -e "${YELLOW}⚠ Real estate schema file not found, skipping${NC}"
fi

# 2. Import Market Data
if [ -f "Real_estate_db/import_market_data.py" ]; then
    echo ""
    echo "Checking for CSV data files..."

    if [ -f "Real_estate_db/market_data.csv" ] && \
       [ -f "Real_estate_db/comp_transactions.csv" ] && \
       [ -f "Real_estate_db/economic_indicators.csv" ]; then
        echo -e "${GREEN}✓ All CSV files found${NC}"
        run_python_script "Real_estate_db/import_market_data.py" "Import Market Data from CSV"
    else
        echo -e "${YELLOW}⚠ Some CSV files are missing:${NC}"
        [ ! -f "Real_estate_db/market_data.csv" ] && echo "  - market_data.csv"
        [ ! -f "Real_estate_db/comp_transactions.csv" ] && echo "  - comp_transactions.csv"
        [ ! -f "Real_estate_db/economic_indicators.csv" ] && echo "  - economic_indicators.csv"
    fi
else
    echo -e "${YELLOW}⚠ Import script not found, skipping${NC}"
fi

# 3. Run additional migrations if available
if [ -d "backend/migrations" ]; then
    echo ""
    echo "Checking for backend migrations..."

    for sql_file in backend/migrations/*.sql; do
        if [ -f "$sql_file" ]; then
            filename=$(basename "$sql_file")
            run_sql_file "$sql_file" "Migration: $filename"
        fi
    done
fi

# 4. Verify data was loaded
echo ""
echo "============================================"
echo "Verification"
echo "============================================"
echo ""

echo "Checking table counts..."

# Check market_data table
MARKET_DATA_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM market_data;" 2>/dev/null || echo "0")
echo "  market_data: $MARKET_DATA_COUNT rows"

# Check comp_transactions table
COMP_TRANS_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM comp_transactions;" 2>/dev/null || echo "0")
echo "  comp_transactions: $COMP_TRANS_COUNT rows"

# Check economic_indicators table
ECON_IND_COUNT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM economic_indicators;" 2>/dev/null || echo "0")
echo "  economic_indicators: $ECON_IND_COUNT rows"

echo ""
echo "============================================"
echo "Database Population Complete!"
echo "============================================"
echo ""
echo "Summary:"
echo "  ✓ Schemas created"
echo "  ✓ Data imported"
echo "  ✓ Migrations applied"
echo ""
echo "Next steps:"
echo "  1. Start the backend API: cd backend && uvicorn app.main:app --reload"
echo "  2. Access API docs: http://localhost:8000/docs"
echo "  3. Test endpoints with real data"
echo ""
