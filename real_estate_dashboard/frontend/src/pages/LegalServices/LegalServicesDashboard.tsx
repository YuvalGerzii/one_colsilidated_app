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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  Alert,
  IconButton,
  Divider,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Gavel as GavelIcon,
  Description as DocumentIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  AccountBalance as AccountBalanceIcon,
  Assessment as AssessmentIcon,
  Event as EventIcon,
  Add as AddIcon,
  ExpandMore as ExpandMoreIcon,
  Upload as UploadIcon,
  Download as DownloadIcon,
  Search as SearchIcon,
  Info as InfoIcon,
  AttachMoney as MoneyIcon,
  Business as BusinessIcon,
  Article as ArticleIcon,
  Policy as PolicyIcon,
  Verified as VerifiedIcon,
  Error as ErrorIcon,
  LibraryBooks as LibraryIcon,
  Calculate as CalculateIcon,
  Timeline as TimelineIcon,
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
      id={`legal-tabpanel-${index}`}
      aria-labelledby={`legal-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const LegalServicesDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState('');

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  // Legal Documents & Templates
  const documentTemplates = [
    { name: 'Purchase Agreement', category: 'Acquisition', status: 'Ready' },
    { name: 'Lease Agreement - Residential', category: 'Leasing', status: 'Ready' },
    { name: 'Lease Agreement - Commercial', category: 'Leasing', status: 'Ready' },
    { name: 'Property Deed', category: 'Transfer', status: 'Ready' },
    { name: 'Non-Disclosure Agreement', category: 'General', status: 'Ready' },
    { name: 'Joint Venture Agreement', category: 'Partnership', status: 'Ready' },
    { name: 'Construction Contract', category: 'Development', status: 'Ready' },
    { name: 'Property Management Agreement', category: 'Management', status: 'Ready' },
    { name: 'Option to Purchase', category: 'Acquisition', status: 'Ready' },
    { name: 'Easement Agreement', category: 'Rights', status: 'Ready' },
  ];

  // Compliance Checklist
  const complianceItems = [
    { item: 'Property Title Search', status: 'complete', priority: 'high', dueDate: '2025-11-15' },
    { item: 'Zoning Verification', status: 'pending', priority: 'high', dueDate: '2025-11-20' },
    { item: 'Environmental Assessment', status: 'in-progress', priority: 'medium', dueDate: '2025-11-25' },
    { item: 'Building Permits Verification', status: 'pending', priority: 'high', dueDate: '2025-11-18' },
    { item: 'Tax Lien Search', status: 'complete', priority: 'high', dueDate: '2025-11-12' },
    { item: 'Insurance Policy Review', status: 'in-progress', priority: 'medium', dueDate: '2025-11-22' },
    { item: 'HOA Documents Review', status: 'pending', priority: 'low', dueDate: '2025-11-30' },
    { item: 'Survey Verification', status: 'complete', priority: 'high', dueDate: '2025-11-10' },
  ];

  // Tax Advisory Features
  const taxAdvisoryTopics = [
    {
      title: '1031 Exchange Planning',
      description: 'Defer capital gains taxes through like-kind property exchanges',
      features: ['Exchange Timeline Calculator', 'Qualified Intermediary Finder', 'Replacement Property Criteria'],
    },
    {
      title: 'Depreciation Strategies',
      description: 'Maximize tax benefits through cost segregation and bonus depreciation',
      features: ['Cost Segregation Analysis', 'Depreciation Schedule', 'Bonus Depreciation Calculator'],
    },
    {
      title: 'Entity Structuring',
      description: 'Optimize legal structure for tax efficiency (LLC, LP, C-Corp, S-Corp)',
      features: ['Entity Comparison Tool', 'Tax Impact Analyzer', 'State Tax Considerations'],
    },
    {
      title: 'Opportunity Zones',
      description: 'Leverage qualified opportunity zone tax incentives',
      features: ['Zone Eligibility Checker', 'Investment Timeline', 'Tax Benefit Calculator'],
    },
  ];

  // Due Diligence Checklist
  const dueDiligenceCategories = [
    {
      category: 'Legal Documentation',
      items: [
        'Purchase and sale agreement review',
        'Title commitment and exceptions',
        'Survey and legal description',
        'Existing leases and tenant files',
        'Service contracts and warranties',
        'Litigation and claims history',
      ],
    },
    {
      category: 'Regulatory Compliance',
      items: [
        'Zoning and land use compliance',
        'Building code compliance',
        'Environmental compliance (Phase I/II)',
        'ADA compliance verification',
        'Fire safety and life safety codes',
        'Local ordinances and restrictions',
      ],
    },
    {
      category: 'Financial & Tax',
      items: [
        'Property tax records and assessments',
        'Outstanding tax liens or judgments',
        'Operating statements (3 years)',
        'Rent roll verification',
        'Capital expenditure history',
        'Insurance claims history',
      ],
    },
  ];

  // Contract Review Metrics
  const contractReviewMetrics = {
    totalContracts: 24,
    underReview: 5,
    approved: 18,
    needsRevision: 1,
    avgReviewTime: '3.2 days',
    highRiskClauses: 8,
  };

  // Legal Calendar Events
  const upcomingDeadlines = [
    { date: '2025-11-12', event: 'Title Policy Expiration - 123 Main St', priority: 'high' },
    { date: '2025-11-15', event: 'Lease Renewal - Commercial Plaza', priority: 'medium' },
    { date: '2025-11-18', event: 'HOA Board Meeting', priority: 'low' },
    { date: '2025-11-20', event: 'Property Tax Appeal Deadline', priority: 'high' },
    { date: '2025-11-25', event: 'Construction Contract Review', priority: 'medium' },
    { date: '2025-11-30', event: 'Quarterly Compliance Report', priority: 'high' },
  ];

  // Risk Assessment
  const riskAssessments = [
    { property: 'Oak Street Apartments', riskLevel: 'Low', score: 85, issues: [] },
    { property: 'Downtown Plaza', riskLevel: 'Medium', score: 65, issues: ['Pending Litigation', 'Zoning Variance'] },
    { property: 'Industrial Park', riskLevel: 'High', score: 45, issues: ['Environmental Concerns', 'Title Defects', 'Code Violations'] },
  ];

  return (
    <Box>
      {/* Header */}
      <Paper elevation={2} sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Stack direction="row" alignItems="center" spacing={2}>
          <Box
            sx={{
              width: 60,
              height: 60,
              background: 'rgba(255, 255, 255, 0.2)',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backdropFilter: 'blur(10px)',
            }}
          >
            <GavelIcon sx={{ fontSize: 32, color: 'white' }} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" sx={{ fontWeight: 700, color: 'white', mb: 0.5 }}>
              Legal Services Center
            </Typography>
            <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.9)' }}>
              Comprehensive legal tools and services for real estate professionals
            </Typography>
          </Box>
        </Stack>
      </Paper>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Box sx={{ p: 1.5, bgcolor: 'primary.light', borderRadius: 2 }}>
                  <DocumentIcon sx={{ color: 'primary.main' }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {contractReviewMetrics.totalContracts}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Contracts
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
                <Box sx={{ p: 1.5, bgcolor: 'warning.light', borderRadius: 2 }}>
                  <WarningIcon sx={{ color: 'warning.main' }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {contractReviewMetrics.underReview}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Under Review
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
                <Box sx={{ p: 1.5, bgcolor: 'success.light', borderRadius: 2 }}>
                  <CheckCircleIcon sx={{ color: 'success.main' }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {complianceItems.filter(i => i.status === 'complete').length}/{complianceItems.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Compliance Items
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
                <Box sx={{ p: 1.5, bgcolor: 'error.light', borderRadius: 2 }}>
                  <ScheduleIcon sx={{ color: 'error.main' }} />
                </Box>
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 700 }}>
                    {upcomingDeadlines.length}
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
          <Tab icon={<LibraryIcon />} iconPosition="start" label="Document Library" />
          <Tab icon={<CheckCircleIcon />} iconPosition="start" label="Compliance Tracker" />
          <Tab icon={<MoneyIcon />} iconPosition="start" label="Tax Advisory" />
          <Tab icon={<ArticleIcon />} iconPosition="start" label="Due Diligence" />
          <Tab icon={<AssessmentIcon />} iconPosition="start" label="Risk Assessment" />
          <Tab icon={<EventIcon />} iconPosition="start" label="Legal Calendar" />
        </Tabs>

        {/* Tab 0: Document Library */}
        <TabPanel value={activeTab} index={0}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
              <TextField
                placeholder="Search documents..."
                size="small"
                sx={{ flex: 1 }}
                InputProps={{
                  startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                }}
              />
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Category</InputLabel>
                <Select label="Category" defaultValue="all">
                  <MenuItem value="all">All Categories</MenuItem>
                  <MenuItem value="acquisition">Acquisition</MenuItem>
                  <MenuItem value="leasing">Leasing</MenuItem>
                  <MenuItem value="development">Development</MenuItem>
                  <MenuItem value="general">General</MenuItem>
                </Select>
              </FormControl>
              <Button variant="contained" startIcon={<AddIcon />}>
                Upload Document
              </Button>
            </Stack>

            <Grid container spacing={2}>
              {documentTemplates.map((template, index) => (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                        <ArticleIcon color="primary" />
                        <Typography variant="h6" sx={{ fontSize: '0.95rem', fontWeight: 600 }}>
                          {template.name}
                        </Typography>
                      </Stack>
                      <Chip label={template.category} size="small" color="primary" variant="outlined" sx={{ mb: 1 }} />
                      <Typography variant="body2" color="text.secondary">
                        Pre-approved template ready for customization
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<DownloadIcon />}>
                        Download
                      </Button>
                      <Button size="small" startIcon={<InfoIcon />}>
                        Details
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                AI-Powered Contract Review
              </Typography>
              <Paper variant="outlined" sx={{ p: 3, bgcolor: 'background.default' }}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Stack spacing={2}>
                      <Typography variant="body2" color="text.secondary">
                        Upload contracts for AI-powered analysis to identify:
                      </Typography>
                      <List dense>
                        <ListItem>
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <CheckCircleIcon fontSize="small" color="success" />
                          </ListItemIcon>
                          <ListItemText primary="High-risk clauses and terms" />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <CheckCircleIcon fontSize="small" color="success" />
                          </ListItemIcon>
                          <ListItemText primary="Missing standard provisions" />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <CheckCircleIcon fontSize="small" color="success" />
                          </ListItemIcon>
                          <ListItemText primary="Compliance issues" />
                        </ListItem>
                        <ListItem>
                          <ListItemIcon sx={{ minWidth: 36 }}>
                            <CheckCircleIcon fontSize="small" color="success" />
                          </ListItemIcon>
                          <ListItemText primary="Financial term extraction" />
                        </ListItem>
                      </List>
                      <Button variant="contained" startIcon={<UploadIcon />} sx={{ alignSelf: 'flex-start' }}>
                        Upload Contract for Review
                      </Button>
                    </Stack>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Card sx={{ bgcolor: 'primary.light', color: 'primary.dark' }}>
                      <CardContent>
                        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                          Review Metrics
                        </Typography>
                        <Stack spacing={2}>
                          <Box>
                            <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                              <Typography variant="body2">Avg. Review Time</Typography>
                              <Typography variant="body2" fontWeight={600}>
                                {contractReviewMetrics.avgReviewTime}
                              </Typography>
                            </Stack>
                            <LinearProgress variant="determinate" value={75} />
                          </Box>
                          <Box>
                            <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                              <Typography variant="body2">Approval Rate</Typography>
                              <Typography variant="body2" fontWeight={600}>
                                {Math.round((contractReviewMetrics.approved / contractReviewMetrics.totalContracts) * 100)}%
                              </Typography>
                            </Stack>
                            <LinearProgress variant="determinate" value={(contractReviewMetrics.approved / contractReviewMetrics.totalContracts) * 100} />
                          </Box>
                          <Alert severity="warning" sx={{ mt: 1 }}>
                            {contractReviewMetrics.highRiskClauses} high-risk clauses detected in active contracts
                          </Alert>
                        </Stack>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 1: Compliance Tracker */}
        <TabPanel value={activeTab} index={1}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Real Estate Compliance Checklist
              </Typography>
              <Button variant="contained" startIcon={<AddIcon />}>
                Add Compliance Item
              </Button>
            </Stack>

            <TableContainer component={Paper} variant="outlined">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Status</TableCell>
                    <TableCell>Compliance Item</TableCell>
                    <TableCell>Priority</TableCell>
                    <TableCell>Due Date</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {complianceItems.map((item, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        {item.status === 'complete' && <CheckCircleIcon color="success" />}
                        {item.status === 'in-progress' && <ScheduleIcon color="warning" />}
                        {item.status === 'pending' && <WarningIcon color="error" />}
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" fontWeight={500}>
                          {item.item}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={item.priority.toUpperCase()}
                          size="small"
                          color={item.priority === 'high' ? 'error' : item.priority === 'medium' ? 'warning' : 'default'}
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{item.dueDate}</Typography>
                      </TableCell>
                      <TableCell>
                        <Button size="small">Update</Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Regulatory Compliance Areas
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                        <PolicyIcon color="primary" />
                        <Typography variant="h6" fontSize="0.95rem" fontWeight={600}>
                          Zoning & Land Use
                        </Typography>
                      </Stack>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Verify property zoning compliance and permitted uses
                      </Typography>
                      <Button size="small" variant="outlined" fullWidth>
                        Check Zoning
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                        <BusinessIcon color="primary" />
                        <Typography variant="h6" fontSize="0.95rem" fontWeight={600}>
                          Building Codes
                        </Typography>
                      </Stack>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Ensure compliance with local building regulations
                      </Typography>
                      <Button size="small" variant="outlined" fullWidth>
                        Verify Codes
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                        <VerifiedIcon color="primary" />
                        <Typography variant="h6" fontSize="0.95rem" fontWeight={600}>
                          Environmental
                        </Typography>
                      </Stack>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Phase I/II environmental assessments and reports
                      </Typography>
                      <Button size="small" variant="outlined" fullWidth>
                        View Reports
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 2: Tax Advisory */}
        <TabPanel value={activeTab} index={2}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Tax Planning & Advisory Services
            </Typography>

            <Grid container spacing={3}>
              {taxAdvisoryTopics.map((topic, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                        <AccountBalanceIcon color="primary" />
                        <Typography variant="h6" sx={{ fontSize: '1rem', fontWeight: 600 }}>
                          {topic.title}
                        </Typography>
                      </Stack>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        {topic.description}
                      </Typography>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                        Available Tools:
                      </Typography>
                      <List dense>
                        {topic.features.map((feature, fidx) => (
                          <ListItem key={fidx} disableGutters>
                            <ListItemIcon sx={{ minWidth: 32 }}>
                              <CheckCircleIcon fontSize="small" color="success" />
                            </ListItemIcon>
                            <ListItemText primary={feature} primaryTypographyProps={{ variant: 'body2' }} />
                          </ListItem>
                        ))}
                      </List>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<CalculateIcon />}>
                        Launch Calculator
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Card sx={{ bgcolor: 'info.light' }}>
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <InfoIcon sx={{ color: 'info.main', fontSize: 40 }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                        Schedule Tax Consultation
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        Connect with certified tax advisors specializing in real estate taxation
                      </Typography>
                      <Button variant="contained" size="small">
                        Book Consultation
                      </Button>
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Box>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Tax Compliance Calendar
              </Typography>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <EventIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Q4 Estimated Tax Payment"
                      secondary="January 15, 2026"
                      primaryTypographyProps={{ fontWeight: 600 }}
                    />
                    <Chip label="Upcoming" color="warning" size="small" />
                  </ListItem>
                  <Divider />
                  <ListItem>
                    <ListItemIcon>
                      <EventIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="Annual Property Tax Filing"
                      secondary="April 15, 2026"
                      primaryTypographyProps={{ fontWeight: 600 }}
                    />
                    <Chip label="Planned" size="small" />
                  </ListItem>
                  <Divider />
                  <ListItem>
                    <ListItemIcon>
                      <EventIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary="1031 Exchange Identification Period"
                      secondary="45 days from sale"
                      primaryTypographyProps={{ fontWeight: 600 }}
                    />
                    <Chip label="Critical" color="error" size="small" />
                  </ListItem>
                </List>
              </Paper>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 3: Due Diligence */}
        <TabPanel value={activeTab} index={3}>
          <Box sx={{ p: 3 }}>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Comprehensive Due Diligence Checklist
            </Typography>

            {dueDiligenceCategories.map((category, index) => (
              <Accordion key={index} defaultExpanded={index === 0}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="h6" sx={{ fontSize: '1rem', fontWeight: 600 }}>
                    {category.category}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <List>
                    {category.items.map((item, itemIndex) => (
                      <ListItem key={itemIndex}>
                        <ListItemIcon>
                          <CheckCircleIcon color="action" />
                        </ListItemIcon>
                        <ListItemText primary={item} />
                        <Button size="small">Mark Complete</Button>
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
            ))}

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Due Diligence Timeline
              </Typography>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <Stack spacing={2}>
                  <Alert severity="info">
                    Standard due diligence period: 30-60 days from contract execution
                  </Alert>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            Phase 1: Initial Review
                          </Typography>
                          <Typography variant="h6" fontWeight={600}>
                            Days 1-15
                          </Typography>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            Title search, preliminary financials, physical inspection
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            Phase 2: Deep Dive
                          </Typography>
                          <Typography variant="h6" fontWeight={600}>
                            Days 16-40
                          </Typography>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            Environmental, legal docs, tenant verification, surveys
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                            Phase 3: Final Review
                          </Typography>
                          <Typography variant="h6" fontWeight={600}>
                            Days 41-60
                          </Typography>
                          <Typography variant="body2" sx={{ mt: 1 }}>
                            Final negotiations, contingency removal, closing prep
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  </Grid>
                </Stack>
              </Paper>
            </Box>

            <Box sx={{ mt: 4 }}>
              <Card sx={{ bgcolor: 'warning.light' }}>
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <WarningIcon sx={{ color: 'warning.main', fontSize: 40 }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                        Red Flags to Watch For
                      </Typography>
                      <List dense>
                        <ListItem disableGutters>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText primary="Incomplete or missing documentation" />
                        </ListItem>
                        <ListItem disableGutters>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText primary="Undisclosed liens or encumbrances" />
                        </ListItem>
                        <ListItem disableGutters>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText primary="Zoning or code violations" />
                        </ListItem>
                        <ListItem disableGutters>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <ErrorIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText primary="Environmental contamination" />
                        </ListItem>
                      </List>
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 4: Risk Assessment */}
        <TabPanel value={activeTab} index={4}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Legal Risk Assessment Dashboard
              </Typography>
              <Button variant="contained" startIcon={<AddIcon />}>
                New Assessment
              </Button>
            </Stack>

            <Grid container spacing={3}>
              {riskAssessments.map((assessment, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card variant="outlined" sx={{ height: '100%' }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        {assessment.property}
                      </Typography>
                      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                          <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                            <Typography variant="body2">Risk Score</Typography>
                            <Typography variant="body2" fontWeight={600}>
                              {assessment.score}/100
                            </Typography>
                          </Stack>
                          <LinearProgress
                            variant="determinate"
                            value={assessment.score}
                            color={assessment.score > 70 ? 'success' : assessment.score > 50 ? 'warning' : 'error'}
                            sx={{ height: 8, borderRadius: 4 }}
                          />
                        </Box>
                      </Stack>
                      <Chip
                        label={`${assessment.riskLevel} Risk`}
                        size="small"
                        color={assessment.riskLevel === 'Low' ? 'success' : assessment.riskLevel === 'Medium' ? 'warning' : 'error'}
                        sx={{ mb: 2 }}
                      />
                      {assessment.issues.length > 0 && (
                        <>
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                            Identified Issues:
                          </Typography>
                          <List dense>
                            {assessment.issues.map((issue, issueIndex) => (
                              <ListItem key={issueIndex} disableGutters>
                                <ListItemIcon sx={{ minWidth: 32 }}>
                                  <WarningIcon fontSize="small" color="warning" />
                                </ListItemIcon>
                                <ListItemText primary={issue} primaryTypographyProps={{ variant: 'body2' }} />
                              </ListItem>
                            ))}
                          </List>
                        </>
                      )}
                    </CardContent>
                    <CardActions>
                      <Button size="small">View Details</Button>
                      <Button size="small">Generate Report</Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Risk Assessment Criteria
              </Typography>
              <Paper variant="outlined" sx={{ p: 3 }}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
                      Legal Risk Factors:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Title clarity and chain of ownership" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Pending or historical litigation" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Regulatory compliance status" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Zoning and land use restrictions" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Environmental liabilities" />
                      </ListItem>
                    </List>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" sx={{ mb: 2, fontWeight: 600 }}>
                      Operational Risk Factors:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Lease agreement quality and terms" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Insurance coverage adequacy" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Property condition and maintenance" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Tenant creditworthiness" />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon sx={{ minWidth: 36 }}>
                          <TimelineIcon fontSize="small" color="primary" />
                        </ListItemIcon>
                        <ListItemText primary="Market and economic factors" />
                      </ListItem>
                    </List>
                  </Grid>
                </Grid>
              </Paper>
            </Box>

            <Box sx={{ mt: 4 }}>
              <Alert severity="info" sx={{ mb: 2 }}>
                Risk assessments are automatically updated based on new data and should be reviewed quarterly
              </Alert>
              <Button variant="outlined" startIcon={<DownloadIcon />}>
                Export Risk Report
              </Button>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 5: Legal Calendar */}
        <TabPanel value={activeTab} index={5}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                Legal Deadlines & Events Calendar
              </Typography>
              <Button variant="contained" startIcon={<AddIcon />}>
                Add Event
              </Button>
            </Stack>

            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <Paper variant="outlined" sx={{ p: 3 }}>
                  <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                    Upcoming Deadlines
                  </Typography>
                  <List>
                    {upcomingDeadlines.map((deadline, index) => (
                      <React.Fragment key={index}>
                        <ListItem>
                          <ListItemIcon>
                            <EventIcon
                              color={deadline.priority === 'high' ? 'error' : deadline.priority === 'medium' ? 'warning' : 'action'}
                            />
                          </ListItemIcon>
                          <ListItemText
                            primary={deadline.event}
                            secondary={new Date(deadline.date).toLocaleDateString('en-US', {
                              weekday: 'long',
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                            primaryTypographyProps={{ fontWeight: 500 }}
                          />
                          <Chip
                            label={deadline.priority.toUpperCase()}
                            size="small"
                            color={deadline.priority === 'high' ? 'error' : deadline.priority === 'medium' ? 'warning' : 'default'}
                          />
                        </ListItem>
                        {index < upcomingDeadlines.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Stack spacing={2}>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        Critical Deadlines
                      </Typography>
                      <Typography variant="h4" fontWeight={700} color="error.main">
                        {upcomingDeadlines.filter(d => d.priority === 'high').length}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Require immediate attention
                      </Typography>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent>
                      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                        This Month
                      </Typography>
                      <Typography variant="h4" fontWeight={700} color="primary.main">
                        {upcomingDeadlines.length}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Total events scheduled
                      </Typography>
                    </CardContent>
                  </Card>
                  <Card sx={{ bgcolor: 'info.light' }}>
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={1}>
                        <InfoIcon color="info" />
                        <Typography variant="body2">
                          Enable calendar sync to receive reminders
                        </Typography>
                      </Stack>
                      <Button variant="contained" size="small" sx={{ mt: 2 }} fullWidth>
                        Sync Calendar
                      </Button>
                    </CardContent>
                  </Card>
                </Stack>
              </Grid>
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Important Legal Milestone Reminders
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={2}>
                        <Box sx={{ p: 1.5, bgcolor: 'warning.light', borderRadius: 2 }}>
                          <ScheduleIcon sx={{ color: 'warning.main' }} />
                        </Box>
                        <Box>
                          <Typography variant="subtitle1" fontWeight={600}>
                            Statute of Limitations Tracking
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Monitor filing deadlines for legal claims
                          </Typography>
                        </Box>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={2}>
                        <Box sx={{ p: 1.5, bgcolor: 'success.light', borderRadius: 2 }}>
                          <CheckCircleIcon sx={{ color: 'success.main' }} />
                        </Box>
                        <Box>
                          <Typography variant="subtitle1" fontWeight={600}>
                            Contract Renewal Reminders
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Track lease and service contract expirations
                          </Typography>
                        </Box>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </TabPanel>
      </Paper>

      {/* Bottom CTA */}
      <Paper elevation={2} sx={{ p: 3, mt: 3, bgcolor: 'primary.main', color: 'white' }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={8}>
            <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
              Need Expert Legal Counsel?
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              Connect with experienced real estate attorneys for complex transactions, disputes, and regulatory matters.
            </Typography>
          </Grid>
          <Grid item xs={12} md={4} sx={{ textAlign: { md: 'right' } }}>
            <Button variant="contained" size="large" sx={{ bgcolor: 'white', color: 'primary.main', '&:hover': { bgcolor: 'grey.100' } }}>
              Schedule Consultation
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default LegalServicesDashboard;
