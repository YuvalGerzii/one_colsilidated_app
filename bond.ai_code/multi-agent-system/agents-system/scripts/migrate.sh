#!/bin/bash

# Load environment variables
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Default values
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-agents_system}
DB_USER=${DB_USER:-agents_user}

echo "🚀 Running database migrations..."
echo "📍 Host: $DB_HOST:$DB_PORT"
echo "📍 Database: $DB_NAME"
echo "📍 User: $DB_USER"
echo ""

# Run migration
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f database/migrations/001_initial_schema.sql

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Migration completed successfully!"
else
  echo ""
  echo "❌ Migration failed!"
  exit 1
fi
