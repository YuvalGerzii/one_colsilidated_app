import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Tabs,
  Tab,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Stack,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  TextField,
  LinearProgress,
  Alert,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Avatar,
  Stepper,
  Step,
  StepLabel,
  Badge,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  AccountBalance as AccountBalanceIcon,
  Verified as VerifiedIcon,
  Policy as PolicyIcon,
  Shield as ShieldIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as MoneyIcon,
  LocationCity as LocationIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Timeline as TimelineIcon,
  Business as BusinessIcon,
  Speed as SpeedIcon,
  Calculate as CalculateIcon,
  Add as AddIcon,
  Event as EventIcon,
  CompareArrows as CompareIcon,
  Notifications as NotificationIcon,
  FindInPage as AuditIcon,
  PlaylistAddCheck as ChecklistIcon,
  Lock as LockIcon,
  People as PeopleIcon,
  Info as InfoIcon,
} from '@mui/icons-material';

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
      id={`compliance-tabpanel-${index}`}
      aria-labelledby={`compliance-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const ComplianceAuditDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  // Sample data for 1031 Exchanges
  const exchange1031Data = [
    {
      name: '123 Oak St Exchange',
      status: 'Exchange Period',
      relinquishedValue: 850000,
      saleDate: '2025-10-15',
      identificationDeadline: '2025-11-29',
      exchangeDeadline: '2026-04-13',
      estimatedSavings: 170000,
    },
    {
      name: 'Main Plaza Property',
      status: 'Identification Period',
      relinquishedValue: 1200000,
      saleDate: '2025-11-01',
      identificationDeadline: '2025-12-16',
      exchangeDeadline: '2026-04-30',
      estimatedSavings: 240000,
    },
  ];

  // Sample data for Opportunity Zones
  const opportunityZoneData = [
    {
      name: 'Riverside Development',
      address: '456 River Rd',
      investmentAmount: 2000000,
      investmentDate: '2023-03-15',
      fiveYearMilestone: '2028-03-15',
      sevenYearMilestone: '2030-03-15',
      requiredHoldDate: '2033-03-15',
      basisStepUp5yr: 200000,
      basisStepUp7yr: 100000,
      estimatedTaxFreeGain: 600000,
    },
  ];

  // Sample FIRPTA data
  const firptaData = [
    {
      transaction: 'International Plaza Sale',
      seller: 'Foreign Investment Corp',
      salePrice: 3500000,
      withholdingRate: 15,
      withholdingAmount: 525000,
      status: 'Under Review',
      form8288Filed: false,
    },
  ];

  // Sample Fair Housing data
  const fairHousingProperties = [
    {
      address: '789 Elm Street',
      complianceScore: 100,
      lastCheck: '2025-10-01',
      trainingCurrent: true,
      violations: 0,
    },
    {
      address: '321 Pine Avenue',
      complianceScore: 85,
      lastCheck: '2025-09-15',
      trainingCurrent: false,
      violations: 0,
    },
  ];

  // Sample KYC/AML data
  const investorKYCData = [
    {
      name: 'John Smith',
      type: 'Individual',
      country: 'USA',
      riskRating: 'Low',
      kycStatus: 'Approved',
      accredited: true,
      pepScreening: 'Clear',
      sanctionsScreening: 'Clear',
    },
    {
      name: 'Global Investments LLC',
      type: 'Entity',
      country: 'Cayman Islands',
      riskRating: 'High',
      kycStatus: 'Enhanced Due Diligence',
      accredited: true,
      pepScreening: 'Pending',
      sanctionsScreening: 'Clear',
    },
  ];

  // Sample Legal Holds
  const legalHolds = [
    {
      name: 'Smith v. Property Management',
      caseNumber: '2025-CV-1234',
      issuedDate: '2025-10-01',
      custodians: 5,
      documentsPreserved: 247,
      status: 'Active',
    },
  ];

  // Sample Statute of Limitations
  const statuteTrackers = [
    {
      matter: 'Contract Dispute - Oak Street',
      incidentDate: '2023-01-15',
      statuteDeadline: '2026-01-15',
      daysRemaining: 67,
      claimFiled: false,
    },
    {
      matter: 'Property Defects - Main Plaza',
      incidentDate: '2022-06-20',
      statuteDeadline: '2026-06-20',
      daysRemaining: 223,
      claimFiled: false,
    },
  ];

  // Sample Audit Preparation
  const auditPreparations = [
    {
      name: '2024 Financial Audit',
      type: 'Financial',
      year: 2024,
      status: 'In Progress',
      collectionProgress: 75,
      checklistCompletion: 60,
      auditor: 'KPMG',
    },
  ];

  // Sample SOC 2
  const soc2Assessment = {
    name: 'Q4 2025 SOC 2 Type II',
    overallReadiness: 82,
    security: 90,
    availability: 85,
    processingIntegrity: 80,
    confidentiality: 75,
    privacy: 80,
    gapsIdentified: 12,
    criticalGaps: 2,
  };

  return (
    <Box>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Stack direction="row" alignItems="center" spacing={2}>
          <Box
            sx={{
              width: 70,
              height: 70,
              background: 'rgba(255, 255, 255, 0.25)',
              borderRadius: 3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backdropFilter: 'blur(10px)',
              border: '2px solid rgba(255, 255, 255, 0.3)',
            }}
          >
            <ShieldIcon sx={{ fontSize: 38, color: 'white' }} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, color: 'white', mb: 0.5 }}>
              Compliance & Audit Center
            </Typography>
            <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.95)', fontWeight: 500 }}>
              Regulatory compliance | Investor verification | Audit preparation | SOC 2 readiness
            </Typography>
          </Box>
        </Stack>
      </Paper>

      {/* Quick Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'success.main', width: 56, height: 56 }}>
                  <TrendingUpIcon />
                </Avatar>
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    2
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active 1031 Exchanges
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'info.main', width: 56, height: 56 }}>
                  <PeopleIcon />
                </Avatar>
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    12
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Investors (KYC/AML)
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'warning.main', width: 56, height: 56 }}>
                  <AuditIcon />
                </Avatar>
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    1
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Audits
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'error.main', width: 56, height: 56 }}>
                  <EventIcon />
                </Avatar>
                <Box>
                  <Typography variant="h4" fontWeight={700}>
                    3
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Upcoming Deadlines
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content Tabs */}
      <Paper elevation={2}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
        >
          <Tab icon={<TrendingUpIcon />} iconPosition="start" label="1031 Exchanges" />
          <Tab icon={<LocationIcon />} iconPosition="start" label="Opportunity Zones" />
          <Tab icon={<MoneyIcon />} iconPosition="start" label="FIRPTA" />
          <Tab icon={<PolicyIcon />} iconPosition="start" label="Fair Housing" />
          <Tab icon={<SecurityIcon />} iconPosition="start" label="KYC/AML" />
          <Tab icon={<LockIcon />} iconPosition="start" label="Legal Holds" />
          <Tab icon={<TimelineIcon />} iconPosition="start" label="Statute Tracking" />
          <Tab icon={<AuditIcon />} iconPosition="start" label="Audit Prep" />
          <Tab icon={<VerifiedIcon />} iconPosition="start" label="SOC 2" />
          <Tab icon={<CompareIcon />} iconPosition="start" label="Clause Compare" />
        </Tabs>

        {/* Tab 0: 1031 Exchanges */}
        <TabPanel value={activeTab} index={0}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  1031 Like-Kind Exchange Tracking
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Track tax-deferred exchanges and maximize tax benefits
                </Typography>
              </Box>
              <Button variant="contained" startIcon={<AddIcon />}>
                New 1031 Exchange
              </Button>
            </Stack>

            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="subtitle2" fontWeight={600}>
                Critical Timeline Requirements
              </Typography>
              <Typography variant="body2">
                • 45-day identification period: Must identify replacement properties within 45 days of sale
                <br />
                • 180-day exchange period: Must close on replacement property within 180 days of sale
              </Typography>
            </Alert>

            <Grid container spacing={3}>
              {exchange1031Data.map((exchange, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 2 }}>
                        <Typography variant="h6" fontWeight={600}>
                          {exchange.name}
                        </Typography>
                        <Chip
                          label={exchange.status}
                          size="small"
                          color={exchange.status.includes('Period') ? 'warning' : 'success'}
                        />
                      </Stack>

                      <Stack spacing={1.5}>
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            Relinquished Property Value
                          </Typography>
                          <Typography variant="h6" color="primary.main" fontWeight={600}>
                            ${exchange.relinquishedValue.toLocaleString()}
                          </Typography>
                        </Box>

                        <Divider />

                        <Box>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            Timeline
                          </Typography>
                          <Stack spacing={0.5}>
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="body2">Sale Date:</Typography>
                              <Typography variant="body2" fontWeight={600}>
                                {exchange.saleDate}
                              </Typography>
                            </Stack>
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="body2">45-Day Deadline:</Typography>
                              <Typography variant="body2" fontWeight={600} color="warning.main">
                                {exchange.identificationDeadline}
                              </Typography>
                            </Stack>
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="body2">180-Day Deadline:</Typography>
                              <Typography variant="body2" fontWeight={600} color="error.main">
                                {exchange.exchangeDeadline}
                              </Typography>
                            </Stack>
                          </Stack>
                        </Box>

                        <Divider />

                        <Alert severity="success" icon={<MoneyIcon />}>
                          <Typography variant="body2" fontWeight={600}>
                            Estimated Tax Savings: ${exchange.estimatedSavings.toLocaleString()}
                          </Typography>
                        </Alert>
                      </Stack>
                    </CardContent>
                    <CardActions>
                      <Button size="small">View Details</Button>
                      <Button size="small" startIcon={<CalculateIcon />}>
                        Calculate Savings
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Card sx={{ mt: 3, bgcolor: 'primary.light' }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  1031 Exchange Calculator
                </Typography>
                <Typography variant="body2" paragraph>
                  Estimate your potential tax savings and ensure compliance with IRS requirements
                </Typography>
                <Button variant="contained">Launch Calculator</Button>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>

        {/* Tab 1: Opportunity Zones */}
        <TabPanel value={activeTab} index={1}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Qualified Opportunity Zone Investments
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Track OZ investments and tax incentives through 10-year hold period
                </Typography>
              </Box>
              <Button variant="contained" startIcon={<AddIcon />}>
                New OZ Investment
              </Button>
            </Stack>

            {opportunityZoneData.map((investment, index) => (
              <Card variant="outlined" key={index} sx={{ mb: 3 }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 2 }}>
                    <Box>
                      <Typography variant="h6" fontWeight={600}>
                        {investment.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {investment.address}
                      </Typography>
                    </Box>
                    <Chip label="Active Investment" color="success" />
                  </Stack>

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Investment Details
                      </Typography>
                      <Stack spacing={1}>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Investment Amount:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            ${investment.investmentAmount.toLocaleString()}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Investment Date:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {investment.investmentDate}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Required Hold Until:</Typography>
                          <Typography variant="body2" fontWeight={600} color="primary.main">
                            {investment.requiredHoldDate}
                          </Typography>
                        </Stack>
                      </Stack>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Tax Benefits
                      </Typography>
                      <Stack spacing={1}>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">5-Year Basis Step-up (10%):</Typography>
                          <Typography variant="body2" fontWeight={600} color="success.main">
                            ${investment.basisStepUp5yr.toLocaleString()}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">7-Year Basis Step-up (5%):</Typography>
                          <Typography variant="body2" fontWeight={600} color="success.main">
                            ${investment.basisStepUp7yr.toLocaleString()}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Est. Tax-Free Gain (10yr):</Typography>
                          <Typography variant="body2" fontWeight={600} color="success.main">
                            ${investment.estimatedTaxFreeGain.toLocaleString()}
                          </Typography>
                        </Stack>
                      </Stack>
                    </Grid>
                  </Grid>

                  <Box sx={{ mt: 3 }}>
                    <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                      Key Milestones
                    </Typography>
                    <Stepper activeStep={1} sx={{ mt: 2 }}>
                      <Step>
                        <StepLabel>Investment Date</StepLabel>
                      </Step>
                      <Step>
                        <StepLabel>5-Year Milestone ({investment.fiveYearMilestone})</StepLabel>
                      </Step>
                      <Step>
                        <StepLabel>7-Year Milestone ({investment.sevenYearMilestone})</StepLabel>
                      </Step>
                      <Step>
                        <StepLabel>10-Year Hold Complete ({investment.requiredHoldDate})</StepLabel>
                      </Step>
                    </Stepper>
                  </Box>
                </CardContent>
              </Card>
            ))}

            <Alert severity="info">
              <Typography variant="subtitle2" fontWeight={600}>
                Opportunity Zone Requirements
              </Typography>
              <Typography variant="body2">
                • Must invest within 180 days of capital gain
                <br />
                • Hold investment for at least 10 years for maximum tax-free appreciation
                <br />
                • 5-year hold: 10% basis step-up | 7-year hold: Additional 5% step-up | 10-year hold: Tax-free appreciation
              </Typography>
            </Alert>
          </Box>
        </TabPanel>

        {/* Tab 2: FIRPTA Compliance */}
        <TabPanel value={activeTab} index={2}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  FIRPTA Withholding Calculator
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Foreign Investment in Real Property Tax Act compliance
                </Typography>
              </Box>
              <Button variant="contained" startIcon={<AddIcon />}>
                New FIRPTA Transaction
              </Button>
            </Stack>

            <Card sx={{ mb: 3, bgcolor: 'warning.light' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={2}>
                  <WarningIcon sx={{ fontSize: 40, color: 'warning.main' }} />
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      FIRPTA Withholding Requirements
                    </Typography>
                    <Typography variant="body2">
                      When purchasing US real property from a foreign person, buyers must withhold and remit:
                      <br />
                      • 15% of gross sale price (standard rate)
                      <br />
                      • 10% if residential property under $1 million
                      <br />
                      • File Form 8288 within 20 days of transfer
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>

            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Transaction</TableCell>
                    <TableCell>Seller</TableCell>
                    <TableCell align="right">Sale Price</TableCell>
                    <TableCell align="right">Withholding</TableCell>
                    <TableCell>Form 8288</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {firptaData.map((record, index) => (
                    <TableRow key={index}>
                      <TableCell>{record.transaction}</TableCell>
                      <TableCell>{record.seller}</TableCell>
                      <TableCell align="right">${record.salePrice.toLocaleString()}</TableCell>
                      <TableCell align="right">
                        <Stack>
                          <Typography variant="body2" fontWeight={600}>
                            ${record.withholdingAmount.toLocaleString()}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            ({record.withholdingRate}%)
                          </Typography>
                        </Stack>
                      </TableCell>
                      <TableCell>
                        {record.form8288Filed ? (
                          <Chip label="Filed" size="small" color="success" icon={<CheckCircleIcon />} />
                        ) : (
                          <Chip label="Not Filed" size="small" color="error" icon={<WarningIcon />} />
                        )}
                      </TableCell>
                      <TableCell>
                        <Chip label={record.status} size="small" color="warning" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Button size="small">Manage</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  FIRPTA Withholding Calculator
                </Typography>
                <Grid container spacing={2} sx={{ mt: 1 }}>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="Sale Price"
                      type="number"
                      InputProps={{ startAdornment: '$' }}
                    />
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <TextField
                      fullWidth
                      label="Property Type"
                      select
                      defaultValue="Commercial"
                    >
                      <option value="Residential">Residential</option>
                      <option value="Commercial">Commercial</option>
                      <option value="Land">Land</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Button variant="contained" fullWidth sx={{ height: '56px' }} startIcon={<CalculateIcon />}>
                      Calculate Withholding
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>

        {/* Tab 3: Fair Housing */}
        <TabPanel value={activeTab} index={3}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Fair Housing Act Compliance
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Ensure compliance with federal fair housing laws across all properties
            </Typography>

            <Grid container spacing={3}>
              {fairHousingProperties.map((property, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 2 }}>
                        <Typography variant="h6" fontWeight={600}>
                          {property.address}
                        </Typography>
                        <Chip
                          label={property.complianceScore === 100 ? 'Fully Compliant' : 'Needs Attention'}
                          size="small"
                          color={property.complianceScore === 100 ? 'success' : 'warning'}
                        />
                      </Stack>

                      <Box sx={{ mb: 2 }}>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                          <Typography variant="body2">Compliance Score</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {property.complianceScore}/100
                          </Typography>
                        </Stack>
                        <LinearProgress
                          variant="determinate"
                          value={property.complianceScore}
                          color={property.complianceScore === 100 ? 'success' : 'warning'}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>

                      <Stack spacing={1}>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Last Check:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {property.lastCheck}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Staff Training:</Typography>
                          <Chip
                            label={property.trainingCurrent ? 'Current' : 'Expired'}
                            size="small"
                            color={property.trainingCurrent ? 'success' : 'error'}
                          />
                        </Stack>
                        <Stack direction="row" justifyContent="space-between">
                          <Typography variant="body2">Violations:</Typography>
                          <Typography variant="body2" fontWeight={600} color={property.violations === 0 ? 'success.main' : 'error.main'}>
                            {property.violations}
                          </Typography>
                        </Stack>
                      </Stack>
                    </CardContent>
                    <CardActions>
                      <Button size="small">Full Report</Button>
                      <Button size="small">Update Check</Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Card sx={{ mt: 3, bgcolor: 'info.light' }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Fair Housing Compliance Checklist
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <List dense>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Equal Opportunity Housing poster displayed" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Non-discriminatory advertising practices" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Standardized application process" />
                      </ListItem>
                    </List>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <List dense>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Reasonable accommodation policy" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <WarningIcon color="warning" />
                        </ListItemIcon>
                        <ListItemText primary="Annual staff training (due soon)" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Consistent screening criteria" />
                      </ListItem>
                    </List>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>

        {/* Continue with remaining tabs... Due to length, I'll create a condensed version of the remaining tabs */}

        {/* Tab 4: KYC/AML */}
        <TabPanel value={activeTab} index={4}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Investor KYC & AML Compliance
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Know Your Customer and Anti-Money Laundering verification for all investors
            </Typography>

            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Investor</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Country</TableCell>
                    <TableCell>Risk Rating</TableCell>
                    <TableCell>Accredited</TableCell>
                    <TableCell>KYC Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {investorKYCData.map((investor, index) => (
                    <TableRow key={index}>
                      <TableCell>{investor.name}</TableCell>
                      <TableCell>{investor.type}</TableCell>
                      <TableCell>{investor.country}</TableCell>
                      <TableCell>
                        <Chip
                          label={investor.riskRating}
                          size="small"
                          color={investor.riskRating === 'Low' ? 'success' : investor.riskRating === 'High' ? 'error' : 'warning'}
                        />
                      </TableCell>
                      <TableCell>
                        {investor.accredited ? (
                          <CheckCircleIcon color="success" />
                        ) : (
                          <WarningIcon color="warning" />
                        )}
                      </TableCell>
                      <TableCell>
                        <Chip label={investor.kycStatus} size="small" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Button size="small">View Profile</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Grid container spacing={2} sx={{ mt: 3 }}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <SecurityIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
                    <Typography variant="h6" fontWeight={600}>
                      PEP Screening
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Politically Exposed Persons screening
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <ShieldIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
                    <Typography variant="h6" fontWeight={600}>
                      Sanctions Check
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      OFAC and global sanctions screening
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <VerifiedIcon sx={{ fontSize: 48, color: 'info.main', mb: 1 }} />
                    <Typography variant="h6" fontWeight={600}>
                      Accreditation
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Accredited investor verification
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        </TabPanel>

        {/* Tab 5: Legal Holds */}
        <TabPanel value={activeTab} index={5}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Legal Hold Management
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Preserve documents and data for litigation and investigations
            </Typography>

            <Grid container spacing={3}>
              {legalHolds.map((hold, index) => (
                <Grid item xs={12} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                        <Box sx={{ flex: 1 }}>
                          <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 1 }}>
                            <LockIcon color="error" />
                            <Typography variant="h6" fontWeight={600}>
                              {hold.name}
                            </Typography>
                            <Chip label={hold.status} size="small" color="error" />
                          </Stack>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            Case: {hold.caseNumber} | Issued: {hold.issuedDate}
                          </Typography>

                          <Grid container spacing={2}>
                            <Grid item xs={6} md={3}>
                              <Typography variant="body2" color="text.secondary">
                                Custodians
                              </Typography>
                              <Typography variant="h6">{hold.custodians}</Typography>
                            </Grid>
                            <Grid item xs={6} md={3}>
                              <Typography variant="body2" color="text.secondary">
                                Documents Preserved
                              </Typography>
                              <Typography variant="h6">{hold.documentsPreserved}</Typography>
                            </Grid>
                          </Grid>
                        </Box>
                        <Stack spacing={1}>
                          <Button size="small" variant="outlined">
                            View Details
                          </Button>
                          <Button size="small" variant="outlined" color="error">
                            Release Hold
                          </Button>
                        </Stack>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        </TabPanel>

        {/* Tab 6: Statute of Limitations */}
        <TabPanel value={activeTab} index={6}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Statute of Limitations Tracking
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Monitor critical filing deadlines for potential legal claims
            </Typography>

            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Matter</TableCell>
                    <TableCell>Incident Date</TableCell>
                    <TableCell>Statute Deadline</TableCell>
                    <TableCell>Days Remaining</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {statuteTrackers.map((tracker, index) => (
                    <TableRow key={index}>
                      <TableCell>{tracker.matter}</TableCell>
                      <TableCell>{tracker.incidentDate}</TableCell>
                      <TableCell>{tracker.statuteDeadline}</TableCell>
                      <TableCell>
                        <Chip
                          label={`${tracker.daysRemaining} days`}
                          size="small"
                          color={tracker.daysRemaining < 90 ? 'error' : tracker.daysRemaining < 180 ? 'warning' : 'success'}
                        />
                      </TableCell>
                      <TableCell>
                        {tracker.claimFiled ? (
                          <Chip label="Filed" size="small" color="success" />
                        ) : (
                          <Chip label="Not Filed" size="small" color="warning" />
                        )}
                      </TableCell>
                      <TableCell>
                        <Button size="small">Manage</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </TabPanel>

        {/* Tab 7: Audit Preparation */}
        <TabPanel value={activeTab} index={7}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Audit Preparation Dashboard
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Streamline audit preparation with automated document collection
            </Typography>

            {auditPreparations.map((audit, index) => (
              <Card key={index} sx={{ mb: 3 }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 3 }}>
                    <Box>
                      <Typography variant="h6" fontWeight={600}>
                        {audit.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {audit.type} Audit | Year: {audit.year} | Auditor: {audit.auditor}
                      </Typography>
                    </Box>
                    <Chip label={audit.status} color="info" />
                  </Stack>

                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Document Collection Progress
                      </Typography>
                      <Box sx={{ mb: 1 }}>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                          <Typography variant="body2">Collection</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {audit.collectionProgress}%
                          </Typography>
                        </Stack>
                        <LinearProgress
                          variant="determinate"
                          value={audit.collectionProgress}
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                    </Grid>

                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Checklist Completion
                      </Typography>
                      <Box sx={{ mb: 1 }}>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                          <Typography variant="body2">Checklist</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {audit.checklistCompletion}%
                          </Typography>
                        </Stack>
                        <LinearProgress
                          variant="determinate"
                          value={audit.checklistCompletion}
                          color="secondary"
                          sx={{ height: 8, borderRadius: 4 }}
                        />
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
                <CardActions>
                  <Button size="small">View Checklist</Button>
                  <Button size="small">Upload Documents</Button>
                  <Button size="small">Generate Report</Button>
                </CardActions>
              </Card>
            ))}

            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <ChecklistIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Automated Checklist Generator
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Generate comprehensive audit checklists based on audit type and requirements
                    </Typography>
                    <Button variant="contained">Generate Checklist</Button>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card variant="outlined">
                  <CardContent>
                    <DocumentIcon sx={{ fontSize: 48, color: 'success.main', mb: 2 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Document Collection Automation
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Automate document requests and track submission status
                    </Typography>
                    <Button variant="contained">Start Collection</Button>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        </TabPanel>

        {/* Tab 8: SOC 2 Compliance */}
        <TabPanel value={activeTab} index={8}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              SOC 2 Compliance Readiness
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Track SOC 2 Type I & II readiness across all Trust Service Criteria
            </Typography>

            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 3 }}>
                  <Box>
                    <Typography variant="h6" fontWeight={600}>
                      {soc2Assessment.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Overall Readiness Assessment
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h3" fontWeight={700} color="primary.main">
                      {soc2Assessment.overallReadiness}%
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Overall Score
                    </Typography>
                  </Box>
                </Stack>

                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Box sx={{ mb: 2 }}>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2">Security</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {soc2Assessment.security}%
                        </Typography>
                      </Stack>
                      <LinearProgress variant="determinate" value={soc2Assessment.security} sx={{ height: 8, borderRadius: 4 }} />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2">Availability</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {soc2Assessment.availability}%
                        </Typography>
                      </Stack>
                      <LinearProgress variant="determinate" value={soc2Assessment.availability} sx={{ height: 8, borderRadius: 4 }} />
                    </Box>

                    <Box>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2">Processing Integrity</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {soc2Assessment.processingIntegrity}%
                        </Typography>
                      </Stack>
                      <LinearProgress variant="determinate" value={soc2Assessment.processingIntegrity} sx={{ height: 8, borderRadius: 4 }} />
                    </Box>
                  </Grid>

                  <Grid item xs={12} md={6}>
                    <Box sx={{ mb: 2 }}>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2">Confidentiality</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {soc2Assessment.confidentiality}%
                        </Typography>
                      </Stack>
                      <LinearProgress variant="determinate" value={soc2Assessment.confidentiality} sx={{ height: 8, borderRadius: 4 }} />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2">Privacy</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {soc2Assessment.privacy}%
                        </Typography>
                      </Stack>
                      <LinearProgress variant="determinate" value={soc2Assessment.privacy} sx={{ height: 8, borderRadius: 4 }} />
                    </Box>

                    <Stack spacing={1}>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2">Gaps Identified:</Typography>
                        <Typography variant="body2" fontWeight={600} color="warning.main">
                          {soc2Assessment.gapsIdentified}
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2">Critical Gaps:</Typography>
                        <Typography variant="body2" fontWeight={600} color="error.main">
                          {soc2Assessment.criticalGaps}
                        </Typography>
                      </Stack>
                    </Stack>
                  </Grid>
                </Grid>
              </CardContent>
              <CardActions>
                <Button size="small">View Gap Analysis</Button>
                <Button size="small">Remediation Plan</Button>
                <Button size="small">Schedule Audit</Button>
              </CardActions>
            </Card>

            <Alert severity="info">
              <Typography variant="subtitle2" fontWeight={600}>
                SOC 2 Trust Service Criteria
              </Typography>
              <Typography variant="body2">
                SOC 2 evaluates controls relevant to Security (required) and optionally Availability, Processing Integrity,
                Confidentiality, and Privacy. Type I examines design, Type II examines operating effectiveness over time.
              </Typography>
            </Alert>
          </Box>
        </TabPanel>

        {/* Tab 9: Clause Comparison */}
        <TabPanel value={activeTab} index={9}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Contract Clause Comparison Tool
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
              Compare clauses across contracts to identify differences and negotiate effectively
            </Typography>

            <Card>
              <CardContent>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={5}>
                    <TextField
                      fullWidth
                      label="Document A"
                      placeholder="Upload or select contract"
                      InputProps={{
                        endAdornment: (
                          <Button size="small" variant="outlined">
                            Upload
                          </Button>
                        ),
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <CompareIcon sx={{ fontSize: 32, color: 'text.secondary' }} />
                  </Grid>
                  <Grid item xs={12} md={5}>
                    <TextField
                      fullWidth
                      label="Document B"
                      placeholder="Upload or select contract"
                      InputProps={{
                        endAdornment: (
                          <Button size="small" variant="outlined">
                            Upload
                          </Button>
                        ),
                      }}
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <Button variant="contained" fullWidth size="large" startIcon={<CompareIcon />}>
                      Compare Documents
                    </Button>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            <Card sx={{ mt: 3, bgcolor: 'primary.light' }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  AI-Powered Clause Analysis
                </Typography>
                <Typography variant="body2" paragraph>
                  Our AI analyzes and compares:
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <List dense>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Payment terms and conditions" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Liability and indemnification" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Termination provisions" />
                      </ListItem>
                    </List>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <List dense>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Warranty and representation" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Dispute resolution mechanisms" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color="success" />
                        </ListItemIcon>
                        <ListItemText primary="Governing law and jurisdiction" />
                      </ListItem>
                    </List>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>
      </Paper>
    </Box>
  );
};

export default ComplianceAuditDashboard;
