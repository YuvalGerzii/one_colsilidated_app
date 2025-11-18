# Finance Platform – Completed Delivery Overview

This repository contains the production-ready **Portfolio Finance Platform** that unifies data ingestion, financial modeling, and interactive underwriting workflows for private equity and real estate operators. The codebase includes:

- A **FastAPI** backend with PostgreSQL persistence, market data aggregation services, model generators, and document processing utilities.
- A **React + Material UI** frontend delivered with Vite that surfaces dashboards, portfolio operations, document tooling, and embedded real estate models.
- Domain-specific tooling for discounted cash flow (DCF), leveraged buyout (LBO), real estate underwriting, renovation budgeting, lease abstraction, and comparative deal analytics.

This document explains how the components fit together, how to run the full stack locally, and where to find major feature areas.

---

## 1. System Architecture

```
workspace/
├── backend/                        # FastAPI application
│   ├── app/
│   │   ├── api/                    # Versioned REST endpoints
│   │   ├── core/                   # Database + security utilities
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   ├── repositories/           # Data access helpers
│   │   ├── scripts/real_estate/    # Interactive underwriting engines
│   │   ├── services/               # External data integrations (Zillow, CoStar, Census...)
│   │   └── templates/real_estate/  # Jinja views for interactive model UI
│   ├── migrations/                 # Alembic migrations (if using PostgreSQL)
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Container build for the API
│
├── portfolio-dashboard-frontend/   # React/Vite SPA
│   ├── src/
│   │   ├── components/             # Layout, charting, reusable widgets
│   │   ├── hooks/                  # React Query data hooks
│   │   ├── pages/                  # Dashboard, Companies, Market Data, Real Estate, etc.
│   │   └── services/               # Axios API client + domain services
│   ├── public/                     # Static assets
│   └── package.json                # Frontend dependencies & scripts
│
├── start_app.sh                    # Orchestrates DB, backend API, and frontend dev server
├── build_app.sh                    # Creates backend venv, installs deps, builds frontend
├── docker-compose.yml              # Alternative container-based deployment
├── requirements.txt                # Monorepo-level dependency snapshot
└── domain packages (deal comparison, lease analyzer, etc.)
```

**Data flow**

1. React frontend issues API requests to the FastAPI backend under the `/api/v1` prefix (`services/api.ts`).
2. FastAPI routes handle analytics (`market_data`), health checks, and the new real estate tooling (`/real-estate/tools`).
3. Real estate endpoints render Jinja templates that call into Python underwriting engines housed in `backend/app/scripts/real_estate/` and return full tables plus chart specifications.
4. Supporting directories (e.g., `deal comparison`, `lease analyzer`, `Real_estate_db`) provide supplemental templates, SQL schemas, and AI automation scripts that extend the platform when required.

---

## 2. Quick Start Checklist

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (local or remote)
- (Optional) Docker if you prefer containerized services

### 2.1 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # set DATABASE_URL, SECRET_KEY, etc.
alembic upgrade head      # apply migrations if using PostgreSQL
uvicorn app.main:app --reload --port 8000
```

The API becomes available at `http://localhost:8000` with interactive docs at `/docs` (when `DEBUG=True`).

### 2.2 Frontend Setup

```bash
cd portfolio-dashboard-frontend
npm install
npm run dev -- --host 0.0.0.0 --port 4173
```

Visit the UI at `http://localhost:4173`. The frontend expects the API at `/api/v1` by default; override with `VITE_API_URL` in `.env` if needed.

### 2.3 Unified Startup Script

Run `./build_app.sh` (once) to bootstrap virtualenv and install Node dependencies, then `./start_app.sh` to launch backend and frontend together. Helpful flags:

- `./start_app.sh --stop` – stop both services
- `./start_app.sh --status` – check health probes
- `./start_app.sh --logs` – tail backend/frontend logs

---

## 3. Platform Navigation & Feature Map

| Sidebar Route | Description | Key Files |
| ------------- | ----------- | --------- |
| **Dashboard** | Portfolio-level KPIs, revenue/EBITDA trends, sector allocation, quick access launcher for advanced modeling tools. | `src/pages/Dashboard/Dashboard.tsx` |
| **Companies** | DataGrid of portfolio companies with filters, linked to detail view and model generator. | `src/pages/Companies/CompanyList.tsx`, `CompanyDetail.tsx` |
| **Model Generator** | Launches Excel-based DCF, LBO, Merger, DD, and QoE model generators. | `src/pages/Models/ModelGenerator.tsx`, `src/services/models.ts` |
| **Real Estate Models** | **New:** Embedded interactive underwriting suite (Fix & Flip, Single-Family Rental, Small Multifamily, High-Rise Multifamily, Hotel, Mixed-Use Tower) with full tables/charts mirroring the Excel workbooks. | `src/pages/RealEstate/RealEstateTools.tsx`, backend templates + scripts |
| **Market Data** | Aggregated macro insights sourced from backend services (`market_data` endpoint). | `src/pages/MarketData/MarketData.tsx` |
| **Documents** | AI-assisted PDF extraction workflow and document library. | `src/pages/Documents/DocumentExtraction.tsx`, `DocumentsLibrary.tsx` |
| **Financial Data Entry** | Structured input forms for company-level metrics. | `src/pages/Financials/FinancialDataEntry.tsx` |
| **Reports** | Portfolio reporting hub. | `src/pages/Reports/Reports.tsx` |
| **Settings** | User and workspace preferences placeholder. | `src/pages/Settings/SettingsPage.tsx` |

Every tab renders a dedicated UI view and is reachable from the persistent Material UI sidebar (`src/components/layout/Sidebar.tsx`). The dashboard entry card now links to both the Excel model generator and the new real estate tools workspace for a cohesive experience.

---

## 4. Real Estate Modeling Suite

- **Endpoint registry**: `backend/app/api/v1/endpoints/real_estate_tools.py` registers six underwriting engines, normalizes user input, and returns report tables and chart specs.
- **Templates**: `backend/app/templates/real_estate/tools_index.html` presents the model chooser, while `model_detail.html` renders assumption forms, output tables, and chart canvases.
- **Python engines**: Located in `backend/app/scripts/real_estate/`, each CLI module (including the new `extended_multifamily_cli.py` and `mixed_use_cli.py`) exposes `DEFAULT_INPUTS`, `FORM_FIELDS`, and builder functions used by the API and UI.
- **Frontend integration**: `RealEstateTools.tsx` embeds the landing page inside the dashboard via an iframe (`/api/v1/real-estate/tools`), offers a refresh action, and allows opening the full experience in a new tab.

This mirrors the Excel templates by exposing identical assumption tables, preview tables, and charts, while keeping results in sync with backend computations.

---

## 5. Supporting Toolkits

- **Deal Comparison** (`deal comparison/`): APIs, SQL schema, and visualization components for cross-model property comparisons and IC memo generation.
- **Lease Analyzer** (`lease analyzer/`): AI-assisted lease abstraction scripts, prompt engineering guides, and SQL schema for rent rolls.
- **Renovation Budget Builder** (`renovation budget builder/`): Value-add project planning templates with delivery summaries.
- **Real Estate Market DB** (`Real_estate_db/`): Structured NYC & Miami market data ready for PostgreSQL import.
- **Miscellaneous models**: Additional Excel frameworks (small multifamily, single family rental, hotel, etc.) preserved for reference and offline use.

These packages can be integrated with the core platform via the backend services layer or external ETL processes.

---

## 6. Testing & Quality Assurance

| Component | Suggested Checks |
| --------- | ---------------- |
| Backend | `python -m compileall backend/app` for syntax validation; `pytest` for unit/integration tests (tests not yet authored). |
| Frontend | `npm run build` (Vite production build) and optional `npm run lint`. |
| E2E | Launch via `start_app.sh` and manually validate each sidebar route, especially the real estate workspace and dashboard quick links. |

Continuous integration can use the provided scripts together with container builds from `Dockerfile` and `docker-compose.yml`.

---

## 7. Deployment Notes

- **Backend container**: `backend/Dockerfile` installs requirements and runs `uvicorn app.main:app`.
- **Frontend container**: `portfolio-dashboard-frontend/Dockerfile` builds the Vite app and serves static assets via Nginx (`nginx.conf`).
- **Environment variables**: Configure API base URL (`VITE_API_URL`) for the frontend and database credentials/feature toggles via `backend/.env`.
- **Production hosting**: Recommend running PostgreSQL separately, deploying the backend behind a reverse proxy (e.g., Traefik, Nginx), and serving the built frontend from a CDN or static host.

---

## 8. Next Steps & Enhancements

- Backfill automated tests for real estate endpoints and front-end route guards.
- Wire additional backend services (funds, reports, AI workflows) into the unified API router.
- Expand CI/CD using the provided scripts to lint, test, and build containers automatically.
- Implement authentication and role-based access (placeholders exist in backend models/services).

---

## 9. Contact & Support

For questions about implementation details:

- Backend architecture: `backend/PROJECT_STRUCTURE.md`, `BACKEND_PACKAGE_SUMMARY.md`
- Frontend guidelines: `portfolio-dashboard-frontend/README.md`
- Real estate models: Documentation in `real estate/`, `single family rental/`, `small multi family/`, and `hotel model/`

Happy modeling! 🚀
