// src/App.tsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { theme } from './theme';
import { Layout } from './components/layout/Layout';
import { ErrorBoundary } from './components/common/ErrorBoundary';

// Pages
import { Dashboard } from './pages/Dashboard/Dashboard';
import { CompanyList } from './pages/Companies/CompanyList';
import { CompanyDetail } from './pages/Companies/CompanyDetail';
import { ModelGenerator } from './pages/Models/ModelGenerator';
import { RealEstateTools } from './pages/RealEstate/RealEstateTools';
import { CorporateFinanceModels } from './pages/FinanceModels/CorporateFinanceModels';
import { MarketData } from './pages/MarketData/MarketData';
import { LoginPage } from './pages/Auth/LoginPage';
import { DocumentExtraction } from './pages/Documents/DocumentExtraction';
import { DocumentsLibrary } from './pages/Documents/DocumentsLibrary';
import { FinancialDataEntry } from './pages/Financials/FinancialDataEntry';
import { SettingsPage } from './pages/Settings/SettingsPage';
import { Reports } from './pages/Reports/Reports';
import PropertyManagement from './pages/PropertyManagement/PropertyManagement';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/" element={<Layout />}>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="companies" element={<CompanyList />} />
                <Route path="companies/:companyId" element={<CompanyDetail />} />
                <Route path="companies/:companyId/models" element={<ModelGenerator />} />
                <Route path="models" element={<ModelGenerator />} />
                <Route path="real-estate" element={<RealEstateTools />} />
                <Route path="finance-models" element={<CorporateFinanceModels />} />
                <Route path="market-data" element={<MarketData />} />
                <Route path="property-management" element={<PropertyManagement />} />
                <Route path="documents/upload" element={<DocumentExtraction />} />
                <Route path="documents/library" element={<DocumentsLibrary />} />
                <Route path="financials/data-entry" element={<FinancialDataEntry />} />
                <Route path="reports" element={<Reports />} />
                <Route path="settings" element={<SettingsPage />} />
              </Route>
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
};

export default App;
