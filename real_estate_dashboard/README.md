# 🏢 Real Estate Dashboard

A comprehensive, professional-grade dashboard for **Real Estate Property Management** and **Financial Modeling**. This independent application provides institutional-quality tools for managing property portfolios and analyzing real estate investments.

## ✨ Features

### 🏘️ Property Management System
- **Portfolio Overview**: Real-time dashboard with key metrics and alerts
- **Property Tracking**: Comprehensive property management with detailed profiles
- **Unit Management**: Track individual units, occupancy, and rent rolls
- **Lease Management**: Monitor lease terms, expirations, and renewals
- **Maintenance Tracking**: Manage maintenance requests with priority levels
- **ROI Analysis**: Calculate IRR, cash-on-cash returns, and cap rates
- **Financial Analytics**: Track income, expenses, and NOI by property

### 📊 Real Estate Financial Models
- **Fix & Flip**: Short-term value-add residential project analysis
- **Single Family Rental**: Long-term buy-and-hold with BRRRR strategy
- **Small Multifamily**: 2-6 unit property analysis with unit-level inputs
- **High-Rise Multifamily**: 7+ unit extended analysis
- **Hotel**: Hospitality investment modeling with room and outlet projections
- **Mixed-Use**: Combined commercial and residential development

## 🎨 Professional UI/UX Design

- **Modern Material Design**: Clean, intuitive interface using Material-UI
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Professional Color Palette**: Carefully selected colors for readability and aesthetics
- **Gradient Accents**: Subtle gradients for visual appeal
- **Interactive Charts**: Dynamic visualizations with Recharts
- **Smooth Animations**: Polished transitions and micro-interactions

## 🏗️ Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: RESTful API with automatic OpenAPI documentation
- **Models**: Comprehensive data models for property management and real estate

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI) v5
- **Routing**: React Router v6
- **State Management**: React Hooks
- **Build Tool**: Vite
- **HTTP Client**: Axios

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+, PostgreSQL 15+

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd real_estate_dashboard
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   # Create PostgreSQL database
   createdb real_estate_dashboard

   # Run migrations
   alembic upgrade head
   ```

6. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## 📚 API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🗂️ Project Structure

```
real_estate_dashboard/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── property_management.py
│   │   │           └── real_estate_tools.py
│   │   ├── core/
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── property_management.py
│   │   │   └── real_estate.py
│   │   ├── scripts/
│   │   │   └── real_estate/
│   │   ├── templates/
│   │   │   └── real_estate/
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   └── Layout.tsx
│   │   ├── pages/
│   │   │   ├── PropertyManagement/
│   │   │   └── RealEstate/
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── theme/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### Backend Configuration
Edit `backend/.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/real_estate_dashboard
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### Frontend Configuration
Edit `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 📊 Key Features in Detail

### Property Management Dashboard
- **Real-time Metrics**: Total properties, units, occupancy rates, monthly NOI
- **Alert System**: Lease expirations, vacant units, emergency maintenance
- **Interactive Tables**: Sortable, filterable property and unit listings
- **Financial Tracking**: Income, expenses, and profitability by property

### Real Estate Financial Models
- **Interactive Input Forms**: User-friendly forms with validation
- **Dynamic Calculations**: Real-time updates as inputs change
- **Professional Reports**: Detailed financial statements and metrics
- **Chart Visualizations**: Cash flow waterfalls, IRR profiles, sensitivity tables
- **Export Capabilities**: Download reports and screenshots

## 🎯 Use Cases

- **Property Managers**: Track portfolios, leases, maintenance, and finances
- **Real Estate Investors**: Analyze deals with institutional-grade models
- **Asset Managers**: Monitor portfolio performance and ROI
- **Developers**: Model new developments and renovations
- **Lenders**: Underwrite deals with comprehensive financial analysis

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: React, TypeScript, Material-UI, React Router, Axios
- **Build Tools**: Vite, Docker, Docker Compose
- **Data Visualization**: Recharts, Matplotlib
- **Financial Calculations**: NumPy, Pandas

## 📝 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality
```bash
# Backend
black app/
flake8 app/
mypy app/

# Frontend
npm run lint
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Material-UI for the excellent component library
- FastAPI for the modern Python web framework
- The real estate investment community for domain knowledge

## 📧 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

Built with ❤️ for real estate professionals
