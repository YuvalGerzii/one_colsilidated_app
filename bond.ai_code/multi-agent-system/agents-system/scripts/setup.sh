#!/bin/bash

echo "🚀 Setting up Agents System..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
  echo "📋 Creating .env file from .env.example..."
  cp .env.example .env
  echo "✅ .env file created. Please edit it with your configuration."
  echo ""
else
  echo "✅ .env file already exists"
  echo ""
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
  echo "❌ Failed to install dependencies"
  exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Ask if user wants to run migrations
read -p "Do you want to run database migrations now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  chmod +x scripts/migrate.sh
  ./scripts/migrate.sh
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Run 'npm run build' and 'npm start' for production"
echo ""
echo "Available scripts:"
echo "  npm run dev      - Start development server with auto-reload"
echo "  npm run build    - Build for production"
echo "  npm start        - Start production server"
echo "  npm test         - Run tests"
echo ""
