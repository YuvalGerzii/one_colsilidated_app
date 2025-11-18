# Portfolio Dashboard - Quick Start Guide

## 🚀 Getting Started in 4 Weeks

This guide will help you build a working MVP of the Portfolio Dashboard in 4 weeks. We'll focus on **Phase 1 features only**: company management, manual financial data entry, and basic dashboards.

---

## Week 1: Setup & Foundation

### Day 1-2: Environment Setup

#### 1. Install Required Software

```bash
# Install Python 3.10+
python --version  # Should be 3.10 or higher

# Install PostgreSQL
# Mac: brew install postgresql
# Ubuntu: sudo apt-get install postgresql
# Windows: Download from postgresql.org

# Install Node.js 18+ (for frontend)
node --version  # Should be 18 or higher
npm --version
```

#### 2. Create Project Structure

```bash
# Create main project directory
mkdir portfolio-dashboard
cd portfolio-dashboard

# Create backend
mkdir backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-multipart

# Create frontend
cd ..
npx create-react-app frontend --template typescript
cd frontend
npm install @mui/material @emotion/react @emotion/styled
npm install recharts axios react-router-dom
```

#### 3. Project Structure

```
portfolio-dashboard/
│
├── backend/
│   ├── venv/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── auth.py
│   │   └── routers/
│   │       ├── companies.py
│   │       ├── financials.py
│   │       └── funds.py
│   ├── alembic/  (for database migrations)
│   ├── requirements.txt
│   └── .env
│
└── frontend/
    ├── node_modules/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.tsx
    │   │   ├── CompanyList.tsx
    │   │   ├── CompanyDetail.tsx
    │   │   └── FinancialForm.tsx
    │   ├── services/
    │   │   └── api.ts
    │   ├── types/
    │   │   └── index.ts
    │   ├── App.tsx
    │   └── index.tsx
    ├── package.json
    └── .env
```

### Day 3: Database Setup

#### 1. Create Database

```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
\q
```

#### 2. Create `.env` file in backend/

```env
DATABASE_URL=postgresql://portfolio_user:your_secure_password@localhost/portfolio_db
SECRET_KEY=your-secret-key-here-generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 3. Create `backend/app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 4. Create `backend/app/models.py` (Simplified for Week 1)

```python
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class Fund(Base):
    __tablename__ = 'funds'
    
    fund_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_name = Column(String(255), nullable=False)
    vintage_year = Column(Integer, nullable=False)
    fund_size = Column(Numeric(15, 2), nullable=False)
    committed_capital = Column(Numeric(15, 2), nullable=False)
    drawn_capital = Column(Numeric(15, 2), default=0)
    fund_strategy = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class PortfolioCompany(Base):
    __tablename__ = 'portfolio_companies'
    
    company_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fund_id = Column(UUID(as_uuid=True), nullable=False)
    company_name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False)
    investment_date = Column(Date, nullable=False)
    purchase_price = Column(Numeric(15, 2))
    equity_invested = Column(Numeric(15, 2))
    ownership_percentage = Column(Numeric(5, 4))
    company_status = Column(String(50), default='Active')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class FinancialMetric(Base):
    __tablename__ = 'financial_metrics'
    
    metric_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), nullable=False)
    period_date = Column(Date, nullable=False)
    period_type = Column(String(20), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer)
    
    revenue = Column(Numeric(15, 2))
    cogs = Column(Numeric(15, 2))
    gross_profit = Column(Numeric(15, 2))
    ebitda = Column(Numeric(15, 2))
    net_income = Column(Numeric(15, 2))
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
```

#### 5. Initialize Database

```python
# backend/app/init_db.py
from .database import engine, Base
from . import models

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")

if __name__ == "__main__":
    init_db()
```

```bash
# Run it
python -m app.init_db
```

### Day 4-5: Backend API

#### Create `backend/app/schemas.py`

```python
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

# Fund schemas
class FundBase(BaseModel):
    fund_name: str
    vintage_year: int
    fund_size: Decimal
    committed_capital: Decimal
    fund_strategy: Optional[str] = None

class FundCreate(FundBase):
    pass

class Fund(FundBase):
    fund_id: str
    drawn_capital: Decimal
    created_at: datetime
    
    class Config:
        from_attributes = True

# Company schemas
class CompanyBase(BaseModel):
    company_name: str
    sector: str
    investment_date: date
    purchase_price: Optional[Decimal] = None
    equity_invested: Optional[Decimal] = None
    ownership_percentage: Optional[Decimal] = None

class CompanyCreate(CompanyBase):
    fund_id: str

class Company(CompanyBase):
    company_id: str
    fund_id: str
    company_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Financial metrics schemas
class FinancialMetricBase(BaseModel):
    period_date: date
    period_type: str
    fiscal_year: int
    fiscal_quarter: Optional[int] = None
    revenue: Optional[Decimal] = None
    ebitda: Optional[Decimal] = None
    net_income: Optional[Decimal] = None

class FinancialMetricCreate(FinancialMetricBase):
    pass

class FinancialMetric(FinancialMetricBase):
    metric_id: str
    company_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Create `backend/app/routers/companies.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])

@router.get("/", response_model=List[schemas.Company])
def get_companies(
    fund_id: str = None,
    status: str = "Active",
    db: Session = Depends(get_db)
):
    query = db.query(models.PortfolioCompany)
    if fund_id:
        query = query.filter(models.PortfolioCompany.fund_id == fund_id)
    if status:
        query = query.filter(models.PortfolioCompany.company_status == status)
    return query.all()

@router.post("/", response_model=schemas.Company)
def create_company(
    company: schemas.CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = models.PortfolioCompany(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/{company_id}", response_model=schemas.Company)
def get_company(company_id: str, db: Session = Depends(get_db)):
    company = db.query(models.PortfolioCompany).filter(
        models.PortfolioCompany.company_id == company_id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=schemas.Company)
def update_company(
    company_id: str,
    company: schemas.CompanyBase,
    db: Session = Depends(get_db)
):
    db_company = db.query(models.PortfolioCompany).filter(
        models.PortfolioCompany.company_id == company_id
    ).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company
```

#### Create `backend/app/routers/financials.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/v1", tags=["financials"])

@router.post("/companies/{company_id}/financials", response_model=schemas.FinancialMetric)
def add_financials(
    company_id: str,
    financials: schemas.FinancialMetricCreate,
    db: Session = Depends(get_db)
):
    db_metric = models.FinancialMetric(
        company_id=company_id,
        **financials.dict()
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/companies/{company_id}/financials", response_model=List[schemas.FinancialMetric])
def get_financials(
    company_id: str,
    period_type: str = "Quarterly",
    limit: int = 8,
    db: Session = Depends(get_db)
):
    metrics = db.query(models.FinancialMetric).filter(
        models.FinancialMetric.company_id == company_id,
        models.FinancialMetric.period_type == period_type
    ).order_by(models.FinancialMetric.period_date.desc()).limit(limit).all()
    return metrics
```

#### Create `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import companies, financials

app = FastAPI(title="Portfolio Dashboard API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router)
app.include_router(financials.router)

@app.get("/")
def read_root():
    return {"message": "Portfolio Dashboard API", "version": "1.0.0"}
```

#### Run the backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Visit http://localhost:8000/docs to see the API documentation!

---

## Week 2: Frontend Basics

### Day 1-2: Setup & API Service

#### Create `frontend/src/services/api.ts`

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Company {
  company_id: string;
  company_name: string;
  sector: string;
  investment_date: string;
  purchase_price?: number;
  equity_invested?: number;
  ownership_percentage?: number;
  company_status: string;
  fund_id: string;
}

export interface FinancialMetric {
  metric_id: string;
  company_id: string;
  period_date: string;
  period_type: string;
  fiscal_year: number;
  fiscal_quarter?: number;
  revenue?: number;
  ebitda?: number;
  net_income?: number;
}

// Companies
export const getCompanies = async (fundId?: string): Promise<Company[]> => {
  const params = fundId ? { fund_id: fundId } : {};
  const response = await api.get('/companies', { params });
  return response.data;
};

export const getCompany = async (companyId: string): Promise<Company> => {
  const response = await api.get(`/companies/${companyId}`);
  return response.data;
};

export const createCompany = async (company: Partial<Company>): Promise<Company> => {
  const response = await api.post('/companies', company);
  return response.data;
};

// Financials
export const getFinancials = async (
  companyId: string, 
  periodType: string = 'Quarterly'
): Promise<FinancialMetric[]> => {
  const response = await api.get(`/companies/${companyId}/financials`, {
    params: { period_type: periodType }
  });
  return response.data;
};

export const addFinancials = async (
  companyId: string,
  financials: Partial<FinancialMetric>
): Promise<FinancialMetric> => {
  const response = await api.post(`/companies/${companyId}/financials`, financials);
  return response.data;
};

export default api;
```

### Day 3-4: Company List Component

#### Create `frontend/src/components/CompanyList.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
  Paper, Button, Typography, Box, Chip 
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { getCompanies, Company } from '../services/api';

const CompanyList: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      const data = await getCompanies();
      setCompanies(data);
    } catch (error) {
      console.error('Error loading companies:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value?: number) => {
    if (!value) return '-';
    return `${(value * 100).toFixed(1)}%`;
  };

  if (loading) return <div>Loading...</div>;

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Portfolio Companies</Typography>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => navigate('/companies/new')}
        >
          Add Company
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Company Name</TableCell>
              <TableCell>Sector</TableCell>
              <TableCell>Investment Date</TableCell>
              <TableCell align="right">Purchase Price</TableCell>
              <TableCell align="right">Equity Invested</TableCell>
              <TableCell align="right">Ownership</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {companies.map((company) => (
              <TableRow 
                key={company.company_id}
                sx={{ '&:hover': { bgcolor: 'action.hover', cursor: 'pointer' } }}
                onClick={() => navigate(`/companies/${company.company_id}`)}
              >
                <TableCell>{company.company_name}</TableCell>
                <TableCell>{company.sector}</TableCell>
                <TableCell>{new Date(company.investment_date).toLocaleDateString()}</TableCell>
                <TableCell align="right">{formatCurrency(company.purchase_price)}</TableCell>
                <TableCell align="right">{formatCurrency(company.equity_invested)}</TableCell>
                <TableCell align="right">{formatPercent(company.ownership_percentage)}</TableCell>
                <TableCell>
                  <Chip 
                    label={company.company_status} 
                    color={company.company_status === 'Active' ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Button 
                    size="small" 
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/companies/${company.company_id}`);
                    }}
                  >
                    View
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default CompanyList;
```

### Day 5: Company Detail Component

#### Create `frontend/src/components/CompanyDetail.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Box, Typography, Paper, Grid, Chip, Button,
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow
} from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { getCompany, getFinancials, Company, FinancialMetric } from '../services/api';

const CompanyDetail: React.FC = () => {
  const { companyId } = useParams<{ companyId: string }>();
  const [company, setCompany] = useState<Company | null>(null);
  const [financials, setFinancials] = useState<FinancialMetric[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (companyId) {
      loadData();
    }
  }, [companyId]);

  const loadData = async () => {
    try {
      const [companyData, financialsData] = await Promise.all([
        getCompany(companyId!),
        getFinancials(companyId!)
      ]);
      setCompany(companyData);
      setFinancials(financialsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value?: number) => {
    if (!value) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatMillions = (value?: number) => {
    if (!value) return '-';
    return `$${(value / 1000000).toFixed(1)}M`;
  };

  if (loading) return <div>Loading...</div>;
  if (!company) return <div>Company not found</div>;

  // Prepare chart data (reverse to show chronologically)
  const chartData = [...financials].reverse().map(f => ({
    period: f.period_date.substring(0, 7), // YYYY-MM
    revenue: f.revenue ? f.revenue / 1000000 : null,
    ebitda: f.ebitda ? f.ebitda / 1000000 : null,
  }));

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">{company.company_name}</Typography>
        <Chip 
          label={company.company_status} 
          color={company.company_status === 'Active' ? 'success' : 'default'}
        />
      </Box>

      <Grid container spacing={3}>
        {/* Company Overview */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Company Overview</Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Sector</Typography>
                <Typography variant="body1">{company.sector}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Investment Date</Typography>
                <Typography variant="body1">
                  {new Date(company.investment_date).toLocaleDateString()}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Purchase Price</Typography>
                <Typography variant="body1">{formatCurrency(company.purchase_price)}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Equity Invested</Typography>
                <Typography variant="body1">{formatCurrency(company.equity_invested)}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="text.secondary">Ownership</Typography>
                <Typography variant="body1">
                  {company.ownership_percentage ? `${(company.ownership_percentage * 100).toFixed(1)}%` : '-'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Financial Performance Chart */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>Financial Performance</Typography>
            <LineChart width={800} height={300} data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis label={{ value: '$ Millions', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => `$${value}M`} />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#8884d8" name="Revenue" />
              <Line type="monotone" dataKey="ebitda" stroke="#82ca9d" name="EBITDA" />
            </LineChart>
          </Paper>
        </Grid>

        {/* Financial Data Table */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6">Quarterly Financials</Typography>
              <Button variant="outlined" size="small">Add Period</Button>
            </Box>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Period</TableCell>
                    <TableCell align="right">Revenue</TableCell>
                    <TableCell align="right">EBITDA</TableCell>
                    <TableCell align="right">Net Income</TableCell>
                    <TableCell align="right">EBITDA Margin</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {financials.map((metric) => (
                    <TableRow key={metric.metric_id}>
                      <TableCell>{metric.period_date.substring(0, 7)}</TableCell>
                      <TableCell align="right">{formatMillions(metric.revenue)}</TableCell>
                      <TableCell align="right">{formatMillions(metric.ebitda)}</TableCell>
                      <TableCell align="right">{formatMillions(metric.net_income)}</TableCell>
                      <TableCell align="right">
                        {metric.revenue && metric.ebitda 
                          ? `${((metric.ebitda / metric.revenue) * 100).toFixed(1)}%`
                          : '-'
                        }
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CompanyDetail;
```

---

## Week 3: Financial Data Entry

### Create Financial Entry Form

#### `frontend/src/components/FinancialForm.tsx`

```typescript
import React, { useState } from 'react';
import { 
  Dialog, DialogTitle, DialogContent, DialogActions,
  TextField, Button, Grid, MenuItem
} from '@mui/material';
import { addFinancials } from '../services/api';

interface FinancialFormProps {
  open: boolean;
  onClose: () => void;
  companyId: string;
  onSuccess: () => void;
}

const FinancialForm: React.FC<FinancialFormProps> = ({ 
  open, onClose, companyId, onSuccess 
}) => {
  const [formData, setFormData] = useState({
    period_date: '',
    period_type: 'Quarterly',
    fiscal_year: new Date().getFullYear(),
    fiscal_quarter: 1,
    revenue: '',
    cogs: '',
    ebitda: '',
    net_income: ''
  });

  const handleSubmit = async () => {
    try {
      await addFinancials(companyId, {
        ...formData,
        revenue: parseFloat(formData.revenue),
        cogs: parseFloat(formData.cogs),
        ebitda: parseFloat(formData.ebitda),
        net_income: parseFloat(formData.net_income)
      });
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Error saving financials:', error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Add Financial Data</DialogTitle>
      <DialogContent>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Period Date"
              type="date"
              value={formData.period_date}
              onChange={(e) => setFormData({ ...formData, period_date: e.target.value })}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              select
              label="Period Type"
              value={formData.period_type}
              onChange={(e) => setFormData({ ...formData, period_type: e.target.value })}
            >
              <MenuItem value="Monthly">Monthly</MenuItem>
              <MenuItem value="Quarterly">Quarterly</MenuItem>
              <MenuItem value="Annual">Annual</MenuItem>
            </TextField>
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Fiscal Year"
              type="number"
              value={formData.fiscal_year}
              onChange={(e) => setFormData({ ...formData, fiscal_year: parseInt(e.target.value) })}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Fiscal Quarter"
              type="number"
              value={formData.fiscal_quarter}
              onChange={(e) => setFormData({ ...formData, fiscal_quarter: parseInt(e.target.value) })}
              inputProps={{ min: 1, max: 4 }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Revenue"
              type="number"
              value={formData.revenue}
              onChange={(e) => setFormData({ ...formData, revenue: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="COGS"
              type="number"
              value={formData.cogs}
              onChange={(e) => setFormData({ ...formData, cogs: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="EBITDA"
              type="number"
              value={formData.ebitda}
              onChange={(e) => setFormData({ ...formData, ebitda: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Net Income"
              type="number"
              value={formData.net_income}
              onChange={(e) => setFormData({ ...formData, net_income: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
        </Grid>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} variant="contained">Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default FinancialForm;
```

---

## Week 4: Dashboard & Polish

### Create Main Dashboard

#### `frontend/src/components/Dashboard.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import { getCompanies, Company } from '../services/api';

const Dashboard: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const data = await getCompanies();
      setCompanies(data);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const totalInvested = companies.reduce((sum, c) => sum + (c.equity_invested || 0), 0);
  const activeCompanies = companies.filter(c => c.company_status === 'Active').length;
  
  const sectorData = Object.entries(
    companies.reduce((acc, c) => {
      acc[c.sector] = (acc[c.sector] || 0) + (c.equity_invested || 0);
      return acc;
    }, {} as Record<string, number>)
  ).map(([name, value]) => ({ name, value }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  if (loading) return <div>Loading...</div>;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Portfolio Dashboard</Typography>
      
      <Grid container spacing={3}>
        {/* KPI Cards */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">{activeCompanies}</Typography>
            <Typography variant="body1" color="text.secondary">Active Companies</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">
              ${(totalInvested / 1000000).toFixed(1)}M
            </Typography>
            <Typography variant="body1" color="text.secondary">Total Invested</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">
              ${(totalInvested / activeCompanies / 1000000).toFixed(1)}M
            </Typography>
            <Typography variant="body1" color="text.secondary">Avg Investment</Typography>
          </Paper>
        </Grid>

        {/* Sector Allocation */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Investment by Sector</Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sectorData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.name}: $${(entry.value / 1000000).toFixed(1)}M`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sectorData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>Recent Investments</Typography>
            {companies
              .sort((a, b) => new Date(b.investment_date).getTime() - new Date(a.investment_date).getTime())
              .slice(0, 5)
              .map((company) => (
                <Box key={company.company_id} sx={{ mb: 2 }}>
                  <Typography variant="body1">{company.company_name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(company.investment_date).toLocaleDateString()} • {company.sector}
                  </Typography>
                </Box>
              ))
            }
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
```

---

## Testing Your MVP

### 1. Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### 2. Start Frontend
```bash
cd frontend
npm start
```

### 3. Test Flow
1. Visit http://localhost:3000
2. Create a test fund (via API or database)
3. Add a company
4. Add quarterly financials
5. View dashboard

---

## Next Steps After Week 4

**You now have a working MVP!** 

### Phase 2 (Weeks 5-8): Model Integration
- Build model generation engine
- Export to Excel with formulas
- Scenario management

### Phase 3 (Weeks 9-12): PDF Automation
- PDF upload
- Table extraction
- GPT-4 Vision integration
- Validation workflows

---

## Key Resources

### Learning Resources
- FastAPI docs: https://fastapi.tiangolo.com
- React docs: https://react.dev
- Material-UI: https://mui.com
- SQLAlchemy: https://docs.sqlalchemy.org

### Tools
- Postman (API testing): https://postman.com
- pgAdmin (PostgreSQL GUI): https://pgadmin.org
- React DevTools (Chrome extension)

---

## Common Issues & Solutions

**Issue**: CORS errors
**Solution**: Check CORS middleware in `main.py`, ensure frontend URL is allowed

**Issue**: Database connection fails
**Solution**: Check PostgreSQL is running, verify credentials in `.env`

**Issue**: Module not found
**Solution**: Ensure virtual environment is activated, run `pip install -r requirements.txt`

---

**Ready to build? Follow this guide week-by-week and you'll have a working portfolio dashboard in 4 weeks!** 🚀
