import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Stack,
  Button,
  Tabs,
  Tab,
  Chip,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  useTheme,
  alpha,
} from '@mui/material';
import {
  AccountBalance as AccountBalanceIcon,
  Receipt as ReceiptIcon,
  TrendingUp as TrendingUpIcon,
  Description as DescriptionIcon,
  Settings as SettingsIcon,
  Business as BusinessIcon,
  Person as PersonIcon,
  AccountTree as AccountTreeIcon,
  Savings as SavingsIcon,
  Home as HomeIcon,
  Calculate as CalculateIcon,
  IntegrationInstructions as IntegrationIcon,
  CheckCircle as CheckCircleIcon,
  Lightbulb as LightbulbIcon,
  Assignment as AssignmentIcon,
  MenuBook as MenuBookIcon,
  CalendarMonth as CalendarIcon,
  Shield as ShieldIcon,
  CompareArrows as CompareIcon,
  Gavel as GavelIcon,
} from '@mui/icons-material';
import { TaxStrategyAdvisor } from './TaxStrategyAdvisor';
import { Big4ReportGenerator } from './Big4ReportGenerator';
import { DepreciationCalculator } from './DepreciationCalculator';
import { EntityComparisonTool } from './EntityComparisonTool';
import { AuditRiskAssessment } from './AuditRiskAssessment';
import { ComplianceCalendar } from './ComplianceCalendar';
import { AdvancedTaxStrategies } from './AdvancedTaxStrategies';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`accounting-tabpanel-${index}`}
      aria-labelledby={`accounting-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const Accounting: React.FC = () => {
  const theme = useTheme();
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const accountingTypes = [
    {
      icon: BusinessIcon,
      title: 'Small Business',
      description: 'Accounting for small companies and startups',
      features: ['Chart of Accounts', 'Transaction Tracking', 'Financial Reports', 'Tax Preparation'],
      color: theme.palette.primary.main,
    },
    {
      icon: PersonIcon,
      title: 'Individual & HNW',
      description: 'Personal and high net worth individual accounting',
      features: ['Asset Tracking', 'Investment Management', 'Estate Planning', 'Tax Optimization'],
      color: theme.palette.secondary.main,
    },
    {
      icon: HomeIcon,
      title: 'Property Management',
      description: 'Specialized accounting for rental properties',
      features: ['Rental Income', 'Operating Expenses', 'Property-Level Tracking', 'Depreciation'],
      color: theme.palette.info.main,
    },
    {
      icon: AccountBalanceIcon,
      title: 'Financial Institutions',
      description: 'Accounting for financial institutions and fund managers',
      features: ['Portfolio Management', 'Client Accounting', 'Regulatory Compliance', 'Performance Reporting'],
      color: theme.palette.warning.main,
    },
  ];

  const taxBenefits = [
    {
      title: 'Depreciation',
      description: 'Maximize depreciation deductions (27.5 years residential, 39 years commercial)',
      icon: TrendingUpIcon,
      savings: 'Up to 40% of property value over time',
    },
    {
      title: 'Cost Segregation',
      description: 'Accelerate depreciation by identifying property components',
      icon: CalculateIcon,
      savings: '20-40% of costs to 5-15 year recovery',
    },
    {
      title: 'Mortgage Interest',
      description: 'Deduct mortgage interest on investment properties',
      icon: HomeIcon,
      savings: 'Full deduction on Schedule E',
    },
    {
      title: '1031 Exchange',
      description: 'Defer capital gains taxes by exchanging properties',
      icon: SavingsIcon,
      savings: 'Defer 100% of capital gains',
    },
    {
      title: 'Tax-Loss Harvesting',
      description: 'Offset gains with strategic losses (HNW)',
      icon: TrendingUpIcon,
      savings: '$3,000 annual ordinary income offset',
    },
    {
      title: 'Charitable Giving',
      description: 'Donate appreciated securities (HNW)',
      icon: CheckCircleIcon,
      savings: 'FMV deduction + avoid capital gains',
    },
  ];

  const integrations = [
    { name: 'QuickBooks Online', category: 'Accounting', status: 'Available' },
    { name: 'Xero', category: 'Accounting', status: 'Available' },
    { name: 'Yardi Voyager', category: 'Property Management', status: 'Available' },
    { name: 'AppFolio', category: 'Property Management', status: 'Available' },
    { name: 'DocuSign', category: 'E-Signatures', status: 'Available' },
    { name: 'Dropbox', category: 'Document Storage', status: 'Available' },
    { name: 'Box', category: 'Document Storage', status: 'Available' },
    { name: 'Google Calendar', category: 'Calendar Sync', status: 'Available' },
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
          color: 'white',
          pt: 6,
          pb: 8,
        }}
      >
        <Container maxWidth="lg">
          <Stack spacing={2}>
            <Chip
              icon={<AccountBalanceIcon />}
              label="Professional Accounting Platform"
              sx={{
                bgcolor: alpha(theme.palette.common.white, 0.2),
                color: 'white',
                fontWeight: 600,
                width: 'fit-content',
              }}
            />
            <Typography variant="h3" fontWeight="bold">
              Comprehensive Accounting
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, maxWidth: '800px' }}>
              Full-featured accounting for small businesses, individuals, high net worth clients, and property management - with advanced tax benefits tracking
            </Typography>
          </Stack>
        </Container>
      </Box>

      {/* Main Content */}
      <Container maxWidth="lg" sx={{ mt: -4, mb: 6 }}>
        {/* Accounting Types Cards */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {accountingTypes.map((type, index) => {
            const Icon = type.icon;
            return (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card
                  sx={{
                    height: '100%',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Stack spacing={2}>
                      <Box
                        sx={{
                          width: 56,
                          height: 56,
                          borderRadius: 2,
                          bgcolor: alpha(type.color, 0.1),
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <Icon sx={{ fontSize: 32, color: type.color }} />
                      </Box>
                      <Typography variant="h6" fontWeight="bold">
                        {type.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ minHeight: 60 }}>
                        {type.description}
                      </Typography>
                      <Stack spacing={0.5}>
                        {type.features.map((feature, idx) => (
                          <Typography key={idx} variant="caption" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CheckCircleIcon sx={{ fontSize: 14, color: 'success.main' }} />
                            {feature}
                          </Typography>
                        ))}
                      </Stack>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>

        {/* Tabs Section */}
        <Paper sx={{ borderRadius: 2, overflow: 'hidden' }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            variant="scrollable"
            scrollButtons="auto"
            sx={{
              bgcolor: alpha(theme.palette.primary.main, 0.05),
              '& .MuiTab-root': {
                minHeight: 64,
                fontWeight: 600,
              },
            }}
          >
            <Tab icon={<AccountTreeIcon />} label="Chart of Accounts" iconPosition="start" />
            <Tab icon={<ReceiptIcon />} label="Transactions" iconPosition="start" />
            <Tab icon={<SavingsIcon />} label="Tax Benefits" iconPosition="start" />
            <Tab icon={<CalculateIcon />} label="Depreciation Calculator" iconPosition="start" />
            <Tab icon={<CompareIcon />} label="Entity Comparison" iconPosition="start" />
            <Tab icon={<ShieldIcon />} label="Audit Risk" iconPosition="start" />
            <Tab icon={<CalendarIcon />} label="Compliance Calendar" iconPosition="start" />
            <Tab icon={<GavelIcon />} label="Advanced Strategies" iconPosition="start" />
            <Tab icon={<LightbulbIcon />} label="Tax Strategy Advisor" iconPosition="start" />
            <Tab icon={<AssignmentIcon />} label="Big-4 Reports" iconPosition="start" />
            <Tab icon={<MenuBookIcon />} label="Guides & Best Practices" iconPosition="start" />
            <Tab icon={<IntegrationIcon />} label="Integrations" iconPosition="start" />
            <Tab icon={<DescriptionIcon />} label="Reports" iconPosition="start" />
            <Tab icon={<SettingsIcon />} label="Settings" iconPosition="start" />
          </Tabs>

          {/* Chart of Accounts Tab */}
          <TabPanel value={activeTab} index={0}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Chart of Accounts
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Organize your financial accounts with industry-standard templates or customize your own structure.
                </Typography>
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Card>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          Account Structure
                        </Typography>
                        <List>
                          <ListItem>
                            <ListItemIcon>
                              <AccountBalanceIcon color="primary" />
                            </ListItemIcon>
                            <ListItemText
                              primary="Assets (1000-1999)"
                              secondary="Cash, accounts receivable, property, equipment"
                            />
                          </ListItem>
                          <Divider />
                          <ListItem>
                            <ListItemIcon>
                              <AccountBalanceIcon color="error" />
                            </ListItemIcon>
                            <ListItemText
                              primary="Liabilities (2000-2999)"
                              secondary="Accounts payable, loans, mortgages, deposits"
                            />
                          </ListItem>
                          <Divider />
                          <ListItem>
                            <ListItemIcon>
                              <AccountBalanceIcon color="secondary" />
                            </ListItemIcon>
                            <ListItemText
                              primary="Equity (3000-3999)"
                              secondary="Owner's equity, retained earnings"
                            />
                          </ListItem>
                          <Divider />
                          <ListItem>
                            <ListItemIcon>
                              <TrendingUpIcon color="success" />
                            </ListItemIcon>
                            <ListItemText
                              primary="Revenue (4000-4999)"
                              secondary="Rental income, sales, service revenue"
                            />
                          </ListItem>
                          <Divider />
                          <ListItem>
                            <ListItemIcon>
                              <ReceiptIcon color="warning" />
                            </ListItemIcon>
                            <ListItemText
                              primary="Expenses (5000-9999)"
                              secondary="Operating expenses, maintenance, taxes, depreciation"
                            />
                          </ListItem>
                        </List>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Card sx={{ bgcolor: alpha(theme.palette.info.main, 0.05) }}>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          Quick Setup
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Choose a pre-configured template based on your entity type:
                        </Typography>
                        <Stack spacing={1}>
                          <Button variant="outlined" fullWidth>
                            Small Business
                          </Button>
                          <Button variant="outlined" fullWidth>
                            Property Management
                          </Button>
                          <Button variant="outlined" fullWidth>
                            High Net Worth
                          </Button>
                          <Button variant="outlined" fullWidth>
                            Financial Institution
                          </Button>
                        </Stack>
                        <Divider />
                        <Button variant="contained" fullWidth>
                          Custom Setup
                        </Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Stack>
          </TabPanel>

          {/* Transactions Tab */}
          <TabPanel value={activeTab} index={1}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Transaction Management
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Record and manage all financial transactions with double-entry bookkeeping.
                </Typography>
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={12} sm={6} md={3}>
                  <Button variant="contained" fullWidth size="large" startIcon={<ReceiptIcon />}>
                    New Income
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button variant="contained" fullWidth size="large" startIcon={<ReceiptIcon />}>
                    New Expense
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button variant="outlined" fullWidth size="large">
                    Transfer
                  </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Button variant="outlined" fullWidth size="large">
                    Adjustment
                  </Button>
                </Grid>
              </Grid>

              <Card>
                <CardContent>
                  <Typography variant="h6" fontWeight="bold" gutterBottom>
                    Recent Transactions
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    No transactions yet. Click the buttons above to record your first transaction.
                  </Typography>
                </CardContent>
              </Card>
            </Stack>
          </TabPanel>

          {/* Tax Benefits Tab */}
          <TabPanel value={activeTab} index={2}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Tax Benefits & Optimization
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Track deductions, credits, and tax optimization strategies to maximize your tax savings.
                </Typography>
              </Box>

              <Grid container spacing={3}>
                {taxBenefits.map((benefit, index) => {
                  const Icon = benefit.icon;
                  return (
                    <Grid item xs={12} md={6} key={index}>
                      <Card sx={{ height: '100%' }}>
                        <CardContent>
                          <Stack spacing={2}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                              <Icon color="primary" />
                              <Typography variant="h6" fontWeight="bold">
                                {benefit.title}
                              </Typography>
                            </Box>
                            <Typography variant="body2" color="text.secondary">
                              {benefit.description}
                            </Typography>
                            <Chip
                              label={benefit.savings}
                              color="success"
                              size="small"
                              sx={{ width: 'fit-content' }}
                            />
                          </Stack>
                        </CardContent>
                      </Card>
                    </Grid>
                  );
                })}
              </Grid>
            </Stack>
          </TabPanel>

          {/* Depreciation Calculator Tab */}
          <TabPanel value={activeTab} index={3}>
            <DepreciationCalculator />
          </TabPanel>

          {/* Entity Comparison Tool Tab */}
          <TabPanel value={activeTab} index={4}>
            <EntityComparisonTool />
          </TabPanel>

          {/* Audit Risk Assessment Tab */}
          <TabPanel value={activeTab} index={5}>
            <AuditRiskAssessment />
          </TabPanel>

          {/* Compliance Calendar Tab */}
          <TabPanel value={activeTab} index={6}>
            <ComplianceCalendar />
          </TabPanel>

          {/* Advanced Tax Strategies Tab */}
          <TabPanel value={activeTab} index={7}>
            <AdvancedTaxStrategies />
          </TabPanel>

          {/* Tax Strategy Advisor Tab */}
          <TabPanel value={activeTab} index={8}>
            <TaxStrategyAdvisor />
          </TabPanel>

          {/* Big-4 Report Generator Tab */}
          <TabPanel value={activeTab} index={9}>
            <Big4ReportGenerator />
          </TabPanel>

          {/* Guides & Best Practices Tab */}
          <TabPanel value={activeTab} index={10}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Accounting Guides & Best Practices
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Comprehensive guides covering accounting fundamentals, tax strategies, and compliance requirements.
                </Typography>
              </Box>

              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          📚 Accounting Fundamentals
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Master double-entry bookkeeping, accrual vs cash accounting, revenue recognition (ASC 606), and internal controls.
                        </Typography>
                        <Button variant="contained">Open Guide</Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          🏠 Real Estate Accounting
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Property-level tracking, security deposit accounting, capital vs repairs, depreciation strategies, and cost segregation.
                        </Typography>
                        <Button variant="contained">Open Guide</Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          📅 Year-Round Tax Planning
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Quarterly tasks, estimated taxes, year-end strategies, and IRS safe harbor rules to maximize tax savings.
                        </Typography>
                        <Button variant="contained">Open Guide</Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack spacing={2}>
                        <Typography variant="h6" fontWeight="bold">
                          ✅ Compliance Checklist
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Monthly, quarterly, and annual tasks. Tax filings, deadlines, audit-proof documentation standards.
                        </Typography>
                        <Button variant="contained">Open Guide</Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Stack>
          </TabPanel>

          {/* Integrations Tab */}
          <TabPanel value={activeTab} index={11}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Third-Party Integrations
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Connect with popular accounting, property management, and productivity tools.
                </Typography>
              </Box>

              <Grid container spacing={2}>
                {integrations.map((integration, index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card>
                      <CardContent>
                        <Stack spacing={1}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Typography variant="subtitle1" fontWeight="bold">
                              {integration.name}
                            </Typography>
                            <Chip label={integration.status} color="success" size="small" />
                          </Box>
                          <Typography variant="caption" color="text.secondary">
                            {integration.category}
                          </Typography>
                          <Button variant="outlined" size="small" sx={{ mt: 1 }}>
                            Configure
                          </Button>
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Stack>
          </TabPanel>

          {/* Reports Tab */}
          <TabPanel value={activeTab} index={12}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Financial Reports
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Generate comprehensive financial reports and tax documents.
                </Typography>
              </Box>

              <Grid container spacing={2}>
                {[
                  'Balance Sheet',
                  'Income Statement (P&L)',
                  'Cash Flow Statement',
                  'Trial Balance',
                  'General Ledger',
                  'Schedule E (Rental Properties)',
                  'Tax Summary Report',
                  'Depreciation Schedule',
                ].map((report, index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card>
                      <CardContent>
                        <Stack direction="row" justifyContent="space-between" alignItems="center">
                          <Typography variant="subtitle1">{report}</Typography>
                          <Button variant="text" size="small">
                            Generate
                          </Button>
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Stack>
          </TabPanel>

          {/* Settings Tab */}
          <TabPanel value={activeTab} index={13}>
            <Stack spacing={3} sx={{ px: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight="bold" gutterBottom>
                  Accounting Settings
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Configure your accounting preferences and entity information.
                </Typography>
              </Box>

              <Card>
                <CardContent>
                  <Stack spacing={3}>
                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Entity Type
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Select your entity type to load appropriate chart of accounts and tax templates.
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Fiscal Year End
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Default: December 31
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Accounting Method
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Accrual (recommended for most businesses) or Cash
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Property-Specific Tracking
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Enable to track income and expenses by individual property
                      </Typography>
                    </Box>

                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Trust Accounting
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Enable for security deposits and tenant advance payments
                      </Typography>
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Stack>
          </TabPanel>
        </Paper>
      </Container>
    </Box>
  );
};
