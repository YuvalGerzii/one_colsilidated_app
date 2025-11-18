# Finance Platform - Docker Deployment Guide

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.0+ ([Installation Guide](https://docs.docker.com/engine/install/))
- Docker Compose v2.0+
- 4GB+ RAM available
- 20GB+ disk space

### One-Command Startup

```bash
# Run the automated startup script
./docker-startup.sh
```

Or manually:

```bash
# Build and start all services
docker compose up --build -d

# View logs
docker compose logs -f
```

## 📋 What's Included

This Docker setup includes the following services:

### Core Application Services

1. **Backend API** (Port 8000)
   - FastAPI application
   - REST API endpoints
   - PDF processing
   - Excel model generation
   - Market data integration

2. **Frontend** (Port 3000)
   - React + TypeScript
   - Material-UI components
   - Data visualizations
   - Portfolio dashboard

3. **PostgreSQL** (Port 5432)
   - Primary database
   - Persistent storage for:
     - Portfolio companies
     - Financial metrics
     - Market data
     - Documents

### Infrastructure Services

4. **PgAdmin** (Port 5050)
   - Database administration interface
   - Query builder
   - Visual database management

5. **Redis** (Port 6379)
   - Caching layer
   - Session storage
   - Task queue backend

6. **RabbitMQ** (Port 5672, Management: 15672)
   - Message broker
   - Asynchronous task processing
   - Background jobs

7. **Traefik** (Port 80/443, Dashboard: 8080)
   - Reverse proxy
   - Load balancer
   - Automatic SSL/TLS

8. **Nginx** (Port 8081)
   - Static file serving
   - Alternative reverse proxy

### Monitoring Services

9. **Prometheus** (Port 9090)
   - Metrics collection
   - Time-series database
   - Service monitoring

10. **Grafana** (Port 3001)
    - Metrics visualization
    - Custom dashboards
    - Alerting

11. **Weaviate** (Port 8082)
    - Vector database
    - AI/ML features
    - Semantic search

### Background Workers

12. **Celery Worker**
    - Asynchronous task processing
    - PDF extraction
    - Model generation
    - Email sending

## 🔧 Configuration

### Environment Variables

The root `.env` file controls all services. Key variables:

```bash
# Application
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key

# Database
POSTGRES_DB=portfolio_dashboard
POSTGRES_USER=portfolio_user
POSTGRES_PASSWORD=portfolio_password
POSTGRES_PORT=5432

# Redis
REDIS_PASSWORD=redis_password
REDIS_PORT=6379

# RabbitMQ
RABBITMQ_USER=rabbitmq
RABBITMQ_PASSWORD=rabbitmq_password
RABBITMQ_PORT=5672
RABBITMQ_MGMT_PORT=15672

# Monitoring
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001

# Ports
BACKEND_PORT=8000
FRONTEND_PORT=3000
PGADMIN_PORT=5050
```

### Backend Configuration

Edit `backend/.env` for backend-specific settings:

```bash
# Database connection (Docker networking)
DATABASE_URL=postgresql://portfolio_user:portfolio_password@postgres:5432/portfolio_dashboard

# Redis connection
REDIS_URL=redis://:redis_password@redis:6379/0

# API Keys (add your own)
OPENAI_API_KEY=your-openai-api-key-here
```

## 📦 Directory Structure

```
Finance_platform/
├── docker-compose.yml           # Service orchestration
├── .env                          # Environment variables
├── docker-startup.sh            # Automated startup script
├── populate_database.sh         # Database population script
│
├── backend/                     # Backend API
│   ├── Dockerfile
│   ├── docker-entrypoint.sh
│   ├── requirements.txt
│   ├── .env
│   └── app/
│       ├── main.py
│       ├── models/
│       ├── api/
│       └── services/
│
├── portfolio-dashboard-frontend/  # Frontend app
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── src/
│
├── config/                      # Service configurations
│   ├── postgres/init/           # Database init scripts
│   ├── traefik/                 # Reverse proxy config
│   ├── nginx/                   # Nginx config
│   ├── prometheus/              # Monitoring config
│   └── grafana/                 # Dashboard config
│
└── Real_estate_db/              # Market data
    ├── real_estate_market_data_schema.sql
    ├── import_market_data.py
    ├── market_data.csv
    ├── comp_transactions.csv
    └── economic_indicators.csv
```

## 🏃 Running the Application

### Method 1: Using the Startup Script (Recommended)

```bash
# Make script executable (first time only)
chmod +x docker-startup.sh

# Run the script
./docker-startup.sh
```

The script provides options to:
1. Build and start all services
2. Start services (existing images)
3. Stop all services
4. View logs
5. Show service status
6. Restart services
7. Clean up everything

### Method 2: Manual Docker Compose Commands

```bash
# Start all services (build if needed)
docker compose up --build -d

# Start without rebuilding
docker compose up -d

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Restart a service
docker compose restart backend

# Rebuild a service
docker compose up --build -d backend
```

### Method 3: Individual Service Commands

```bash
# Start only database and backend
docker compose up -d postgres backend

# Start frontend separately
docker compose up -d frontend

# Scale services
docker compose up -d --scale celery-worker=3
```

## 🗄️ Database Setup

### Initial Database Population

After starting the services, populate the database:

```bash
# Make script executable
chmod +x populate_database.sh

# Run the population script
./populate_database.sh
```

This script will:
1. Create database schemas
2. Import market data from CSV files
3. Run migrations
4. Verify data was loaded

### Manual Database Access

```bash
# Using psql directly
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard

# Using PgAdmin
# Open http://localhost:5050
# Login: admin@admin.com / admin
# Add server: postgres:5432
```

### Database Backups

```bash
# Create backup
docker compose exec postgres pg_dump -U portfolio_user portfolio_dashboard > backup.sql

# Restore backup
cat backup.sql | docker compose exec -T postgres psql -U portfolio_user portfolio_dashboard
```

## 🔍 Accessing Services

Once services are running, access them at:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | N/A |
| **Backend API** | http://localhost:8000 | N/A |
| **API Documentation** | http://localhost:8000/docs | N/A |
| **Health Check** | http://localhost:8000/health | N/A |
| **Monitoring Endpoints** | http://localhost:8000/api/v1/monitoring/health | N/A |
| **PgAdmin** | http://localhost:5050 | admin@admin.com / admin |
| **Grafana** | http://localhost:3001 | admin / admin |
| **Prometheus** | http://localhost:9090 | N/A |
| **Traefik Dashboard** | http://localhost:8080 | N/A |
| **RabbitMQ Management** | http://localhost:15672 | rabbitmq / rabbitmq_password |
| **Weaviate** | http://localhost:8082 | N/A |

## 📊 Monitoring & Debugging

### Health Checks

```bash
# Check all services status
docker compose ps

# API health check
curl http://localhost:8000/health

# Comprehensive health check (with metrics)
curl http://localhost:8000/api/v1/monitoring/health

# Database tables
curl http://localhost:8000/api/v1/monitoring/database/tables

# Performance metrics
curl http://localhost:8000/api/v1/monitoring/metrics

# System info (debug mode only)
curl http://localhost:8000/api/v1/monitoring/info
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend

# Last 100 lines
docker compose logs --tail=100 backend

# Since timestamp
docker compose logs --since="2025-11-05T10:00:00" backend
```

### Debugging Services

```bash
# Enter container shell
docker compose exec backend bash
docker compose exec frontend sh
docker compose exec postgres bash

# Check service health
docker compose exec backend curl http://localhost:8000/health

# Check environment variables
docker compose exec backend env

# Test database connection
docker compose exec backend python -c "from app.core.database import check_db_connection; print(check_db_connection())"
```

## 🔧 Development Workflow

### Making Code Changes

#### Backend Changes

```bash
# Code is mounted as volume, changes are reflected immediately
# Restart if needed:
docker compose restart backend

# View updated logs:
docker compose logs -f backend
```

#### Frontend Changes

```bash
# For development with hot reload:
docker compose restart frontend

# Or run frontend locally:
cd portfolio-dashboard-frontend
npm install
npm run dev
```

### Database Migrations

```bash
# Create new migration
docker compose exec backend python -c "from app.models import database; database.init_db()"

# Or manually add SQL file to:
# config/postgres/init/03_your_migration.sql

# Restart postgres to apply:
docker compose restart postgres
```

### Adding New Dependencies

#### Backend

```bash
# Add to backend/requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt

# Rebuild backend
docker compose up --build -d backend
```

#### Frontend

```bash
# Add to package.json or use npm
docker compose exec frontend npm install new-package

# Rebuild frontend
docker compose up --build -d frontend
```

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
docker compose exec backend pytest

# Run with coverage
docker compose exec backend pytest --cov=app --cov-report=html

# Run specific test file
docker compose exec backend pytest tests/test_models.py
```

### Frontend Tests

```bash
# Run tests
docker compose exec frontend npm test

# Run with coverage
docker compose exec frontend npm run test:coverage
```

### Integration Tests

```bash
# Test API endpoints
curl -X GET http://localhost:8000/api/v1/market-data/
curl -X POST http://localhost:8000/api/v1/market-data/ -H "Content-Type: application/json" -d '{"data":"example"}'

# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/monitoring/health
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
```

#### Database Connection Failed

```bash
# Check if postgres is running
docker compose ps postgres

# Check logs
docker compose logs postgres

# Restart postgres
docker compose restart postgres

# Verify connection
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard -c "SELECT 1;"
```

#### Container Won't Start

```bash
# Check logs
docker compose logs [service-name]

# Remove and rebuild
docker compose down
docker compose up --build -d

# Clean rebuild (removes volumes)
docker compose down -v
docker compose up --build -d
```

#### Out of Disk Space

```bash
# Clean up unused images
docker system prune -a

# Clean up volumes
docker volume prune

# Check disk usage
docker system df
```

#### Slow Performance

```bash
# Check resource usage
docker stats

# Increase Docker memory limit (Docker Desktop)
# Settings > Resources > Memory > Increase

# Optimize database
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard -c "VACUUM ANALYZE;"
```

## 🔐 Security

### Production Deployment

**Important security steps for production:**

1. **Change Default Passwords**
   ```bash
   # Update .env with strong passwords:
   POSTGRES_PASSWORD=<strong-random-password>
   REDIS_PASSWORD=<strong-random-password>
   RABBITMQ_PASSWORD=<strong-random-password>
   SECRET_KEY=<strong-random-secret-key>
   ```

2. **Disable Debug Mode**
   ```bash
   DEBUG=False
   ENVIRONMENT=production
   ```

3. **Enable HTTPS**
   - Configure Traefik with SSL certificates
   - Use Let's Encrypt for automatic SSL

4. **Restrict Access**
   - Set up firewall rules
   - Use VPN for admin interfaces
   - Disable unnecessary ports

5. **Environment Variables**
   - Never commit .env to git
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)

6. **Update Docker Images**
   ```bash
   docker compose pull
   docker compose up -d
   ```

## 📈 Performance Optimization

### Database Optimization

```sql
-- Add indexes for frequently queried columns
CREATE INDEX idx_market_data_city ON market_data(city, state);
CREATE INDEX idx_companies_name ON portfolio_companies(name);

-- Analyze tables
ANALYZE market_data;
ANALYZE portfolio_companies;
```

### Redis Caching

Configure caching in backend for:
- API responses
- Database queries
- Session data

### Scaling

```bash
# Scale workers
docker compose up -d --scale celery-worker=5

# Add more resources to services in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## 🔄 Updates & Maintenance

### Updating Services

```bash
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d

# Or rebuild from Dockerfile
docker compose up --build -d
```

### Database Maintenance

```bash
# Vacuum database
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard -c "VACUUM FULL;"

# Reindex
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard -c "REINDEX DATABASE portfolio_dashboard;"

# Check database size
docker compose exec postgres psql -U portfolio_user -d portfolio_dashboard -c "SELECT pg_size_pretty(pg_database_size('portfolio_dashboard'));"
```

## 🆘 Support

### Get Help

1. **Check Logs First**
   ```bash
   docker compose logs -f [service-name]
   ```

2. **Verify Configuration**
   ```bash
   ./docker-startup.sh  # Option 5: Show service status
   ```

3. **Health Checks**
   ```bash
   curl http://localhost:8000/api/v1/monitoring/health
   ```

4. **Documentation**
   - API Docs: http://localhost:8000/docs
   - This guide: You're reading it!
   - Main README: [../README.md](../README.md)

### Quick Reference Commands

```bash
# Start everything
docker compose up -d

# Stop everything
docker compose down

# Restart service
docker compose restart [service-name]

# View logs
docker compose logs -f [service-name]

# Service status
docker compose ps

# Clean restart
docker compose down && docker compose up --build -d

# Nuclear option (removes everything)
docker compose down -v --rmi all && docker compose up --build -d
```

## 📝 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [React Documentation](https://react.dev/)

---

**Version:** 1.0.0
**Last Updated:** November 2025
**Maintained by:** Finance Platform Team
