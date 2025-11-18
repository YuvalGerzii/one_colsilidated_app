import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Stack,
  Button,
  Paper,
  Chip,
  useTheme,
  alpha,
  Divider,
} from '@mui/material';
import {
  HomeWork as PropertyIcon,
  Assessment as ModelsIcon,
  Calculate as FinancialIcon,
  BusinessCenter as FundIcon,
  MonetizationOn as DebtIcon,
  Gavel as LegalIcon,
  AccountBalance as TaxIcon,
  ShowChart as MarketIcon,
  Handshake as CRMIcon,
  Assignment as ProjectIcon,
  Apartment as PortfolioIcon,
  CloudUpload as PDFIcon,
  IntegrationInstructions as IntegrationIcon,
  Folder as ReportsIcon,
  ArrowForward as ArrowForwardIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useCompany } from '../../context/CompanyContext';

export const EnhancedDashboard: React.FC = () => {
  const navigate = useNavigate();
  const theme = useTheme();
  const { selectedCompany } = useCompany();

  // Platform modules organized by category
  const modules = {
    'Core Operations': [
      {
        icon: PropertyIcon,
        title: 'Property Management',
        description: 'Track properties, units, leases, and maintenance',
        path: '/property-management',
        color: theme.palette.primary.main,
        badge: 'Core',
      },
      {
        icon: TaxIcon,
        title: 'Accounting & Bookkeeping',
        description: 'Financial statements, journal entries, and reporting',
        path: '/accounting',
        color: theme.palette.success.main,
        badge: 'New',
      },
      {
        icon: CRMIcon,
        title: 'Deal Pipeline & CRM',
        description: 'Track deals, brokers, and opportunities',
        path: '/crm/deals',
        color: theme.palette.secondary.main,
      },
    ],
    'Financial Analysis': [
      {
        icon: ModelsIcon,
        title: 'Real Estate Models',
        description: '12+ property-level models (Fix & Flip, Rental, Multifamily, Hotel, etc.)',
        path: '/real-estate-tools',
        color: theme.palette.info.main,
        badge: 'Popular',
      },
      {
        icon: FinancialIcon,
        title: 'Company Financial Analysis',
        description: 'DCF, LBO, M&A, Comps, Due Diligence',
        path: '/financial-models',
        color: theme.palette.warning.main,
      },
      {
        icon: PortfolioIcon,
        title: 'Portfolio Dashboard',
        description: 'Portfolio-level analytics and performance metrics',
        path: '/portfolio-dashboard',
        color: theme.palette.primary.dark,
      },
    ],
    'Capital & Legal': [
      {
        icon: FundIcon,
        title: 'Fund Management',
        description: 'LP management, capital calls, distributions, waterfall',
        path: '/fund-management',
        color: theme.palette.info.dark,
      },
      {
        icon: DebtIcon,
        title: 'Debt Management',
        description: 'Loan tracking, amortization, refinancing analysis',
        path: '/debt-management',
        color: theme.palette.error.main,
      },
      {
        icon: LegalIcon,
        title: 'Legal Services',
        description: 'Contract analysis, compliance tracking, document management',
        path: '/legal-services',
        color: theme.palette.secondary.dark,
      },
    ],
    'Data & Intelligence': [
      {
        icon: MarketIcon,
        title: 'Market Intelligence',
        description: 'Market data, trends, and competitive analysis',
        path: '/market-intelligence',
        color: theme.palette.success.dark,
        badge: 'Beta',
      },
      {
        icon: TaxIcon,
        title: 'Tax Strategy',
        description: '1031 Exchange, Cost Segregation, QSBS, Section 179',
        path: '/tax-strategy',
        color: theme.palette.warning.dark,
      },
      {
        icon: PDFIcon,
        title: 'PDF Extraction',
        description: 'Extract data from rent rolls, T-12s, and financial statements',
        path: '/pdf-extraction',
        color: theme.palette.info.light,
      },
    ],
    'Management & Reporting': [
      {
        icon: ProjectIcon,
        title: 'Project Tracking',
        description: 'Development projects, renovations, and capital improvements',
        path: '/project-tracking',
        color: theme.palette.primary.light,
      },
      {
        icon: ReportsIcon,
        title: 'Reports & Documents',
        description: 'Generate and save professional reports',
        path: '/saved-reports',
        color: theme.palette.secondary.light,
      },
      {
        icon: IntegrationIcon,
        title: 'Integrations',
        description: 'Connect to external data sources and APIs',
        path: '/integrations',
        color: theme.palette.info.main,
      },
    ],
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', pb: 6 }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
          color: 'white',
          pt: 4,
          pb: 6,
          mb: 4,
        }}
      >
        <Container maxWidth="xl">
          <Stack spacing={2}>
            <Typography variant="h3" fontWeight="bold">
              Welcome to RE Capital Analytics
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, fontWeight: 400 }}>
              Comprehensive real estate investment platform
            </Typography>
            {selectedCompany && (
              <Box>
                <Chip
                  label={`Company: ${selectedCompany.name}`}
                  sx={{
                    bgcolor: alpha(theme.palette.common.white, 0.2),
                    color: 'white',
                    fontWeight: 600,
                  }}
                  icon={<PropertyIcon sx={{ color: 'white !important' }} />}
                />
              </Box>
            )}
          </Stack>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="xl">
        {/* Quick Stats */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Paper
              sx={{
                p: 3,
                background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`,
                border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
              }}
            >
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  PLATFORM MODULES
                </Typography>
                <Typography variant="h3" fontWeight="bold" color="primary.main">
                  18+
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive toolset
                </Typography>
              </Stack>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper
              sx={{
                p: 3,
                background: `linear-gradient(135deg, ${alpha(theme.palette.success.main, 0.1)} 0%, ${alpha(theme.palette.success.main, 0.05)} 100%)`,
                border: `1px solid ${alpha(theme.palette.success.main, 0.2)}`,
              }}
            >
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  FINANCIAL MODELS
                </Typography>
                <Typography variant="h3" fontWeight="bold" color="success.main">
                  17+
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Institutional-grade analysis
                </Typography>
              </Stack>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper
              sx={{
                p: 3,
                background: `linear-gradient(135deg, ${alpha(theme.palette.warning.main, 0.1)} 0%, ${alpha(theme.palette.warning.main, 0.05)} 100%)`,
                border: `1px solid ${alpha(theme.palette.warning.main, 0.2)}`,
              }}
            >
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  MULTI-COMPANY
                </Typography>
                <Typography variant="h3" fontWeight="bold" color="warning.main">
                  <TrendingUpIcon sx={{ fontSize: 40, verticalAlign: 'middle' }} />
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Isolated data by company
                </Typography>
              </Stack>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper
              sx={{
                p: 3,
                background: `linear-gradient(135deg, ${alpha(theme.palette.info.main, 0.1)} 0%, ${alpha(theme.palette.info.main, 0.05)} 100%)`,
                border: `1px solid ${alpha(theme.palette.info.main, 0.2)}`,
              }}
            >
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  PLATFORM STATUS
                </Typography>
                <Typography variant="h3" fontWeight="bold" color="info.main">
                  Live
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  v2.4.1 - All systems operational
                </Typography>
              </Stack>
            </Paper>
          </Grid>
        </Grid>

        {/* Platform Modules by Category */}
        {Object.entries(modules).map(([category, items]) => (
          <Box key={category} sx={{ mb: 5 }}>
            <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 3 }}>
              <Divider sx={{ flexGrow: 1 }} />
              <Typography variant="h5" fontWeight="bold" color="text.primary">
                {category}
              </Typography>
              <Divider sx={{ flexGrow: 1 }} />
            </Stack>

            <Grid container spacing={3}>
              {items.map((item, index) => {
                const Icon = item.icon;
                return (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card
                      sx={{
                        height: '100%',
                        cursor: 'pointer',
                        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                        position: 'relative',
                        overflow: 'visible',
                        '&:hover': {
                          transform: 'translateY(-8px)',
                          boxShadow: `0 12px 24px ${alpha(item.color, 0.2)}`,
                          '& .action-button': {
                            opacity: 1,
                            transform: 'translateX(0)',
                          },
                        },
                      }}
                      onClick={() => navigate(item.path)}
                    >
                      <CardContent sx={{ p: 3, height: '100%' }}>
                        <Stack spacing={2} height="100%">
                          <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                            <Box
                              sx={{
                                width: 56,
                                height: 56,
                                borderRadius: 2,
                                background: `linear-gradient(135deg, ${alpha(item.color, 0.2)} 0%, ${alpha(item.color, 0.1)} 100%)`,
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                border: `2px solid ${alpha(item.color, 0.3)}`,
                              }}
                            >
                              <Icon sx={{ fontSize: 32, color: item.color }} />
                            </Box>
                            {item.badge && (
                              <Chip
                                label={item.badge}
                                size="small"
                                sx={{
                                  bgcolor: alpha(item.color, 0.15),
                                  color: item.color,
                                  fontWeight: 700,
                                  fontSize: '0.7rem',
                                  height: 24,
                                }}
                              />
                            )}
                          </Stack>

                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="h6" fontWeight="bold" gutterBottom>
                              {item.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              {item.description}
                            </Typography>
                          </Box>

                          <Button
                            className="action-button"
                            endIcon={<ArrowForwardIcon />}
                            sx={{
                              alignSelf: 'flex-start',
                              opacity: 0,
                              transform: 'translateX(-10px)',
                              transition: 'all 0.3s',
                              color: item.color,
                              fontWeight: 600,
                              px: 0,
                              '&:hover': {
                                bgcolor: 'transparent',
                                textDecoration: 'underline',
                              },
                            }}
                          >
                            Open Module
                          </Button>
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                );
              })}
            </Grid>
          </Box>
        ))}

        {/* Getting Started Section */}
        <Paper
          elevation={0}
          sx={{
            p: 4,
            background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
            borderRadius: 3,
            border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
            textAlign: 'center',
          }}
        >
          <Typography variant="h5" fontWeight="bold" gutterBottom>
            Need Help Getting Started?
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph sx={{ maxWidth: 600, mx: 'auto', mb: 3 }}>
            Our platform provides comprehensive tools for real estate investment analysis, management, and reporting.
            {!selectedCompany && ' Select a company from the header to begin.'}
          </Typography>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
            <Button
              variant="contained"
              size="large"
              startIcon={<PropertyIcon />}
              onClick={() => navigate('/property-management')}
              sx={{ minWidth: 200 }}
            >
              Property Management
            </Button>
            <Button
              variant="outlined"
              size="large"
              startIcon={<ModelsIcon />}
              onClick={() => navigate('/real-estate-tools')}
              sx={{ minWidth: 200 }}
            >
              Financial Models
            </Button>
          </Stack>
        </Paper>
      </Container>
    </Box>
  );
};

export default EnhancedDashboard;
