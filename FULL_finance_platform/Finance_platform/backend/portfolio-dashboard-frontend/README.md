# Portfolio Dashboard - Frontend Application

React + TypeScript frontend for the Portfolio Dashboard platform.

## 📦 What's Included

### Complete React Application
- ✅ TypeScript configuration
- ✅ Vite build tool
- ✅ Material-UI component library
- ✅ React Router for navigation
- ✅ React Query for data fetching
- ✅ Zustand for state management
- ✅ Recharts for data visualization

### Project Structure
```
src/
├── components/          # Reusable UI components
│   ├── charts/         # Data visualization components
│   ├── layout/         # Layout components (Header, Sidebar)
│   └── ...
├── pages/              # Full page views
│   ├── Dashboard/      # Main dashboard
│   ├── Companies/      # Company management
│   └── Models/         # Model generation
├── services/           # API integration
│   ├── api.ts         # Base API client
│   ├── companies.ts   # Company endpoints
│   ├── financials.ts  # Financial endpoints
│   ├── models.ts      # Model generation
│   └── pdf.ts         # PDF extraction
├── hooks/              # Custom React hooks
├── types/              # TypeScript definitions
├── utils/              # Utility functions
├── store/              # State management (Zustand)
├── App.tsx             # Main app component
├── index.tsx           # Entry point
└── theme.ts            # Material-UI theme
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

The app will be available at http://localhost:3000

### Build for Production

```bash
npm run build
```

## 🔌 API Integration

The frontend expects a backend API at `http://localhost:8000/api/v1` by default.

Update `.env` to change the API URL:
```
REACT_APP_API_URL=http://your-api-url/api/v1
```

## 📝 Key Features

### Pages Implemented
1. **Dashboard** - Portfolio overview with KPI cards
2. **Company List** - DataGrid with all companies
3. **Company Detail** - Individual company view
4. **Model Generator** - Generate Excel models

### API Services
- `companyService` - CRUD operations for companies
- `financialService` - Financial metrics management
- `modelService` - Model generation
- `pdfService` - PDF extraction

### Custom Hooks
- `useCompanies` - Fetch and manage companies
- `useFinancials` - Financial data operations
- `useModelGeneration` - Generate models

### State Management
- `companyStore` - Company selection and filters
- `uiStore` - UI state (sidebar, snackbar)

## 🎨 Styling

Uses Material-UI with custom theme:
- Primary color: #1976d2 (Professional blue)
- Secondary color: #2e7d32 (Green for positive metrics)
- Clean, professional design
- Responsive layout

## 📊 Charts

Using Recharts for data visualization:
- Revenue & EBITDA trends
- Portfolio performance
- Customizable and responsive

## 🔧 Development

### Adding a New Page
1. Create component in `src/pages/YourPage/`
2. Add route in `src/App.tsx`
3. Add navigation item in `src/components/layout/Sidebar.tsx`

### Adding a New API Service
1. Create service in `src/services/yourService.ts`
2. Define TypeScript types in `src/types/`
3. Create custom hook in `src/hooks/useYourService.ts`

## 📦 Dependencies

### Core
- react 18.2.0
- react-dom 18.2.0
- typescript 5.3.0

### UI
- @mui/material 5.14.0
- @mui/icons-material 5.14.0
- @mui/x-data-grid 6.18.0

### Data & State
- react-query 3.39.0
- zustand 4.4.0
- axios 1.6.0

### Charts
- recharts 2.10.0

### Forms
- react-hook-form 7.48.0
- yup 1.3.0

## 🚧 TODO

Items not yet implemented:
- [ ] Financial data entry form
- [ ] PDF upload interface
- [ ] Advanced analytics page
- [ ] User settings page
- [ ] Authentication UI
- [ ] More chart types
- [ ] Export functionality
- [ ] Mobile responsiveness improvements

## 📄 License

Private - Portfolio Dashboard Project
