import React, { useMemo, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { SnackbarProvider } from 'notistack';
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { createAppTheme } from './theme';
import { ThemeProvider as AppThemeProvider, useAppTheme } from './contexts/ThemeContext';
import { AuthProvider } from './contexts/AuthContext';
import { UIModeProvider } from './contexts/UIModeContext';
import { GlobalContextProvider } from './contexts/GlobalContext';
import { TailwindThemeProvider } from './providers/ThemeProvider';
import { Layout } from './components/Layout';
import ErrorBoundary from './components/ErrorBoundary';
import { queryClient } from './config/react-query';
import { clearLegacyLocalStorage } from './utils/clearOldData';
import { EnhancedDashboard } from './pages/Dashboard/EnhancedDashboard';
import { PropertyManagement } from './pages/PropertyManagement/PropertyManagement';
import { RealEstateTools } from './pages/RealEstate/RealEstateTools';
import { FixAndFlipPage } from './pages/RealEstate/FixAndFlipPage';
import { SingleFamilyRentalPage } from './pages/RealEstate/SingleFamilyRentalPage';
import { SmallMultifamilyPage } from './pages/RealEstate/SmallMultifamilyPage';
import { ExtendedMultifamilyPage } from './pages/RealEstate/ExtendedMultifamilyPage';
import { HotelPage } from './pages/RealEstate/HotelPage';
import { MixedUsePage } from './pages/RealEstate/MixedUsePage';
import { SubdivisionPage } from './pages/RealEstate/SubdivisionPage';
import { SmallMultifamilyAcquisitionPage } from './pages/RealEstate/SmallMultifamilyAcquisitionPage';
import { LeaseAnalyzerPage } from './pages/RealEstate/LeaseAnalyzerPage';
import { RenovationBudgetPage } from './pages/RealEstate/RenovationBudgetPage';
import { TaxStrategyPage } from './pages/RealEstate/TaxStrategyPage';
import { MarketIntelligenceDashboard } from './pages/RealEstate/MarketIntelligenceDashboard';
import { SavedReports } from './pages/SavedReports/SavedReports';
import { PortfolioDashboard } from './pages/PortfolioDashboard/PortfolioDashboard';
import IntegrationsPage from './pages/IntegrationsPage';
import { ReportsGenerator } from './pages/Reports/ReportsGenerator';
import { DealTracker } from './pages/CRM/DealTracker';
import { FinancialModels } from './pages/Financial/FinancialModels';
import { DCFModelEnhanced } from './pages/Financial/DCFModelEnhanced';
import { LBOModelEnhanced } from './pages/Financial/LBOModelEnhanced';
import { MergerModelPage } from './pages/Financial/MergerModelPage';
import { DueDiligenceModel } from './pages/Financial/DueDiligenceModel';
import { ComparableCompanyAnalysis } from './pages/Financial/ComparableCompanyAnalysis';
import { PDFExtraction } from './pages/PDFExtraction/PDFExtraction';
import FundManagementDashboard from './pages/FundManagement/FundManagementDashboard';
import DebtManagementDashboard from './pages/DebtManagement/DebtManagementDashboard';
import ProjectTrackingDashboard from './pages/ProjectTracking/ProjectTrackingDashboard';
import { Accounting } from './pages/Accounting';
import EnhancedLegalServicesDashboard from './pages/LegalServices/EnhancedLegalServicesDashboard';
import ComplianceAuditDashboard from './pages/LegalServices/ComplianceAuditDashboard';
import { CapitalAnalysis } from './pages/Capital/CapitalAnalysis';
import { OperateIntelligence } from './pages/Operate/OperateIntelligence';
import { CompanyProvider } from './context/CompanyContext';
import { CommandCenter } from './pages/CommandCenter';
import { PlatformOverview } from './pages/PlatformOverview';
import { MainDashboard } from './pages/MainDashboard';
import { OperateSummary } from './pages/OperateSummary';
import { RealTimeData } from './pages/RealTimeData';
import { AuditLog, UsersRoles, Companies, APIIntegrations, SystemSettings } from './pages/Admin';
import { DataManagement } from './components/admin/DataManagement';
import ProFormaGenerator from './components/analytics/ProFormaGenerator';
import EnhancedMarketIntelligence from './components/analytics/EnhancedMarketIntelligence';
import AdvancedAnalyticsDashboard from './components/analytics/AdvancedAnalyticsDashboard';
import AIChatbot from './components/chat/AIChatbot';
// DISABLED: Dashboard builder was added from wrong repo (Figmarealestatefinancialplatform-main)
// import { DashboardBuilder } from './components/dashboard-builder/DashboardBuilder';
// import { DashboardBuilderProvider } from './contexts/DashboardBuilderContext';

function AppContent() {
  const { theme: appTheme } = useAppTheme();
  const muiTheme = useMemo(() => createAppTheme(appTheme), [appTheme]);

  // Clean up legacy localStorage data on app load
  useEffect(() => {
    const cleared = clearLegacyLocalStorage();
    if (cleared > 0) {
      console.log(`[App] Cleaned up ${cleared} legacy localStorage keys`);
    }
  }, []);

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider theme={muiTheme}>
          <CssBaseline />
          <TailwindThemeProvider>
            <SnackbarProvider
              maxSnack={3}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              autoHideDuration={3000}
              style={{
                marginTop: '64px',
              }}
            >
              <AuthProvider>
                <CompanyProvider>
                  <UIModeProvider>
                    <GlobalContextProvider>
                      {/* DISABLED: DashboardBuilderProvider - from wrong repo */}
                      {/* <DashboardBuilderProvider> */}
                      <Router>
                        <Layout>
                      <Routes>
                  <Route path="/" element={<MainDashboard />} />
                  <Route path="/dashboard" element={<MainDashboard />} />
                  <Route path="/main-dashboard" element={<MainDashboard />} />
                  <Route path="/enhanced-dashboard" element={<EnhancedDashboard />} />
                  <Route path="/command-center" element={<CommandCenter onNavigate={(ws, mod) => {}} />} />
                  <Route path="/platform-overview" element={<PlatformOverview onNavigate={() => {}} />} />
                  <Route path="/readme" element={<PlatformOverview onNavigate={() => {}} />} />
                  <Route path="/operate-summary" element={<OperateSummary />} />
                  <Route path="/real-time-data" element={<RealTimeData />} />
                  <Route path="/property-management" element={<PropertyManagement />} />
                  <Route path="/accounting" element={<Accounting />} />
                  <Route path="/real-estate-tools" element={<RealEstateTools />} />
                  <Route path="/real-estate-models" element={<RealEstateTools />} />
                  <Route path="/financial-models" element={<FinancialModels />} />
                  <Route path="/financial-models/dcf" element={<DCFModelEnhanced />} />
                  <Route path="/financial-models/lbo" element={<LBOModelEnhanced />} />
                  <Route path="/financial-models/merger" element={<MergerModelPage />} />
                  <Route path="/financial-models/dd" element={<DueDiligenceModel />} />
                  <Route path="/financial-models/comps" element={<ComparableCompanyAnalysis />} />
                  <Route path="/pdf-extraction" element={<PDFExtraction />} />
                  <Route path="/fund-management" element={<FundManagementDashboard />} />
                  <Route path="/debt-management" element={<DebtManagementDashboard />} />
                  <Route path="/project-tracking" element={<ProjectTrackingDashboard />} />
                  <Route path="/capital-analysis" element={<CapitalAnalysis />} />
                  <Route path="/operate-intelligence" element={<OperateIntelligence />} />
                  <Route path="/legal-services" element={<EnhancedLegalServicesDashboard />} />
                  <Route path="/legal-services/compliance" element={<ComplianceAuditDashboard />} />
                  {/* Admin Routes */}
                  <Route path="/admin/audit-log" element={<AuditLog />} />
                  <Route path="/admin/users-roles" element={<UsersRoles />} />
                  <Route path="/admin/companies" element={<Companies />} />
                  <Route path="/admin/api-integrations" element={<APIIntegrations />} />
                  <Route path="/admin/system-settings" element={<SystemSettings />} />
                  <Route path="/admin/data-management" element={<DataManagement />} />
                  <Route path="/portfolio-dashboard" element={<PortfolioDashboard />} />
                  {/* DISABLED: Dashboard builder route - from wrong repo */}
                  {/* <Route path="/dashboard-builder" element={<DashboardBuilder />} /> */}
                  <Route path="/crm/deals" element={<DealTracker />} />
                  <Route path="/market-intelligence" element={<MarketIntelligenceDashboard />} />
                  <Route path="/enhanced-market-intelligence" element={<EnhancedMarketIntelligence />} />
                  <Route path="/advanced-analytics" element={<AdvancedAnalyticsDashboard />} />
                  <Route path="/ai-assistant" element={<AIChatbot />} />
                  <Route path="/tax-strategy" element={<TaxStrategyPage />} />
                  <Route path="/integrations" element={<IntegrationsPage />} />
                  <Route path="/saved-reports" element={<SavedReports />} />
                  <Route path="/reports" element={<ReportsGenerator />} />
                  <Route path="/pro-forma-generator" element={<ProFormaGenerator />} />
                  <Route path="/real-estate-models/fix-and-flip" element={<FixAndFlipPage />} />
                  <Route path="/real-estate-models/single-family-rental" element={<SingleFamilyRentalPage />} />
                  <Route path="/real-estate-models/small-multifamily" element={<SmallMultifamilyPage />} />
                  <Route path="/real-estate-models/extended-multifamily" element={<ExtendedMultifamilyPage />} />
                  <Route path="/real-estate-models/hotel" element={<HotelPage />} />
                  <Route path="/real-estate-models/mixed-use" element={<MixedUsePage />} />
                  <Route path="/real-estate-models/subdivision" element={<SubdivisionPage />} />
                  <Route path="/real-estate-models/small-multifamily-acquisition" element={<SmallMultifamilyAcquisitionPage />} />
                  <Route path="/real-estate-models/lease-analyzer" element={<LeaseAnalyzerPage />} />
                  <Route path="/real-estate-models/renovation-budget" element={<RenovationBudgetPage />} />
                  <Route path="/real-estate-models/tax-strategy" element={<TaxStrategyPage />} />
                  <Route path="/real-estate-models/market-intelligence" element={<MarketIntelligenceDashboard />} />
                      </Routes>
                    </Layout>
                  </Router>
                  {/* </DashboardBuilderProvider> */}
                </GlobalContextProvider>
              </UIModeProvider>
            </CompanyProvider>
          </AuthProvider>
        </SnackbarProvider>
      </TailwindThemeProvider>
    </ThemeProvider>
    {/* React Query DevTools - only visible in development */}
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
</ErrorBoundary>
  );
}

function App() {
  console.log('[App] Rendering App component');
  return (
    <AppThemeProvider>
      <AppContent />
    </AppThemeProvider>
  );
}

export default App;
console.log('[App] App module loaded');
