# Workforce Transition Platform - Setup Guide

## Quick Start with Docker

The easiest way to run the entire platform:

```bash
docker-compose up
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend React app (port 3000)

Access the application at `http://localhost:3000`

API documentation available at `http://localhost:8000/docs`

## Manual Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. Create database:
```bash
createdb workforce_db
```

5. Initialize database with sample data:
```bash
python create_db.py
```

6. Run the backend:
```bash
python main.py
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Set environment variables:
```bash
echo "REACT_APP_API_URL=http://localhost:8000/api/v1" > .env
```

3. Run the frontend:
```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## Sample Data

After running `create_db.py`, you'll have:

### Workers
- ID 1: John Doe (Data Entry Specialist - High Risk)
- ID 2: Jane Smith (Customer Service Rep - Medium Risk)
- ID 3: Mike Johnson (Software Developer - Low Risk)

### Jobs
- ID 1: Data Analyst at Tech Corp
- ID 2: ML Engineer at AI Innovations
- ID 3: Project Manager at Global Solutions

### Enterprise
- ID 1: Enterprise Demo Corp

## Testing the Platform

### 1. Check Worker Risk Assessment
```bash
curl http://localhost:8000/api/v1/workers/1/risk-assessment
```

### 2. Find Job Matches for Worker
```bash
curl -X POST http://localhost:8000/api/v1/jobs/match \
  -H "Content-Type: application/json" \
  -d '{"worker_id": 1, "top_n": 5}'
```

### 3. Analyze Skill Gap
```bash
curl -X POST http://localhost:8000/api/v1/analytics/skill-gap \
  -H "Content-Type: application/json" \
  -d '{"worker_id": 1, "target_job_id": 1}'
```

### 4. Get Market Trends
```bash
curl http://localhost:8000/api/v1/analytics/market-trends
```

### 5. View Enterprise Dashboard
```bash
curl http://localhost:8000/api/v1/enterprise/1/dashboard
```

## Architecture Overview

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
│  - Worker Portal│
│  - Enterprise HR│
│  - Analytics    │
└────────┬────────┘
         │
         │ REST API
         │
┌────────▼────────┐
│  FastAPI Backend│  (Port 8000)
│  - ML Models    │
│  - Job Matching │
│  - Risk Scoring │
└────────┬────────┘
         │
         │ SQLAlchemy
         │
┌────────▼────────┐
│   PostgreSQL    │  (Port 5432)
│   Database      │
└─────────────────┘
```

## Key Features

### For Workers
- Job loss risk assessment
- Skill gap analysis
- Personalized job matching
- Reskilling pathway recommendations

### For Enterprises
- Workforce risk dashboard
- Skills gap analytics
- Training ROI analysis
- Workforce planning insights

## Development

### Running Tests
```bash
cd backend
pytest
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI)

## Deployment

For production deployment:

1. Set strong `SECRET_KEY` in environment
2. Use production database with proper credentials
3. Configure CORS appropriately
4. Enable HTTPS
5. Set up proper authentication
6. Configure Stripe for payments (enterprise subscriptions)

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### Frontend Can't Connect to API
- Check REACT_APP_API_URL in frontend/.env
- Ensure backend is running on port 8000
- Check CORS settings

### Docker Issues
- Run `docker-compose down -v` to reset
- Check Docker logs: `docker-compose logs`

## Support

For issues, please check the documentation or create an issue in the repository.
