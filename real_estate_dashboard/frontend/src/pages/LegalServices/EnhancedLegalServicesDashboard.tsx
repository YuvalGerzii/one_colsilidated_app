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
  Badge,
  Avatar,
  InputAdornment,
  Stepper,
  Step,
  StepLabel,
  Switch,
  FormControlLabel,
  RadioGroup,
  Radio,
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
  AutoAwesome as AIIcon,
  Edit as EditIcon,
  ContentCopy as CopyIcon,
  Settings as SettingsIcon,
  Public as PublicIcon,
  LocationCity as LocationIcon,
  Language as LanguageIcon,
  Autorenew as AutomationIcon,
  Psychology as SmartIcon,
  CloudSync as SyncIcon,
  Shield as ShieldIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  Draw as SignatureIcon,
  Analytics as AnalyticsIcon,
  CompareArrows as CompareIcon,
  FindReplace as FindIcon,
  AutoFixHigh as MagicIcon,
  School as EducationIcon,
  Support as SupportIcon,
  Notifications as NotificationIcon,
  Map as MapIcon,
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

const EnhancedLegalServicesDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [documentGeneratorOpen, setDocumentGeneratorOpen] = useState(false);
  const [clauseLibraryOpen, setClauseLibraryOpen] = useState(false);
  const [aiAnalysisOpen, setAIAnalysisOpen] = useState(false);
  const [zoningCheckerOpen, setZoningCheckerOpen] = useState(false);
  const [selectedState, setSelectedState] = useState('');
  const [selectedDocType, setSelectedDocType] = useState('');

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  // Comprehensive State-Specific Forms Library
  const stateFormsLibrary = [
    { state: 'California', forms: 156, categories: ['Residential', 'Commercial', 'Disclosure'] },
    { state: 'Texas', forms: 142, categories: ['Purchase', 'Lease', 'HOA'] },
    { state: 'Florida', forms: 138, categories: ['Condo', 'Timeshare', 'Commercial'] },
    { state: 'New York', forms: 134, categories: ['Co-op', 'Condo', 'Rental'] },
    { state: 'Illinois', forms: 98, categories: ['Residential', 'Commercial', 'Transfer'] },
    { state: 'All States', forms: 85, categories: ['Federal', 'Universal', 'Multi-State'] },
  ];

  // AI-Powered Clause Library
  const clauseLibrary = [
    {
      category: 'Purchase & Sale',
      clauses: [
        { name: 'As-Is Clause', usage: 'High Risk', aiScore: 72 },
        { name: 'Financing Contingency', usage: 'Standard', aiScore: 95 },
        { name: 'Inspection Contingency', usage: 'Essential', aiScore: 98 },
        { name: 'Title Contingency', usage: 'Required', aiScore: 99 },
        { name: 'Appraisal Contingency', usage: 'Recommended', aiScore: 90 },
      ],
    },
    {
      category: 'Leasing',
      clauses: [
        { name: 'Triple Net Lease', usage: 'Commercial', aiScore: 88 },
        { name: 'Subletting Prohibition', usage: 'Standard', aiScore: 85 },
        { name: 'Rent Escalation', usage: 'Long-term', aiScore: 92 },
        { name: 'Early Termination', usage: 'Negotiable', aiScore: 75 },
        { name: 'Maintenance Responsibility', usage: 'Essential', aiScore: 94 },
      ],
    },
    {
      category: 'Risk Mitigation',
      clauses: [
        { name: 'Indemnification', usage: 'Essential', aiScore: 96 },
        { name: 'Force Majeure', usage: 'Recommended', aiScore: 89 },
        { name: 'Limitation of Liability', usage: 'Negotiable', aiScore: 80 },
        { name: 'Arbitration Clause', usage: 'Alternative', aiScore: 78 },
        { name: 'Confidentiality', usage: 'Standard', aiScore: 93 },
      ],
    },
  ];

  // Automated Document Generation Templates
  const documentTemplates = [
    {
      name: 'Residential Purchase Agreement',
      type: 'acquisition',
      complexity: 'Medium',
      time: '5 min',
      aiPowered: true,
      stateSpecific: true,
    },
    {
      name: 'Commercial Lease Agreement',
      type: 'leasing',
      complexity: 'High',
      time: '8 min',
      aiPowered: true,
      stateSpecific: true,
    },
    {
      name: 'Property Deed Transfer',
      type: 'transfer',
      complexity: 'Medium',
      time: '4 min',
      aiPowered: false,
      stateSpecific: true,
    },
    {
      name: 'Construction Contract',
      type: 'development',
      complexity: 'High',
      time: '12 min',
      aiPowered: true,
      stateSpecific: false,
    },
    {
      name: 'Non-Disclosure Agreement',
      type: 'general',
      complexity: 'Low',
      time: '3 min',
      aiPowered: true,
      stateSpecific: false,
    },
    {
      name: 'Lease Amendment',
      type: 'leasing',
      complexity: 'Low',
      time: '4 min',
      aiPowered: true,
      stateSpecific: true,
    },
  ];

  // Zoning & Compliance Database
  const zoningCategories = [
    { name: 'Residential Zoning', code: 'R1-R5', description: 'Single and multi-family residential' },
    { name: 'Commercial Zoning', code: 'C1-C4', description: 'Retail, office, and service commercial' },
    { name: 'Industrial Zoning', code: 'I1-I3', description: 'Light to heavy industrial uses' },
    { name: 'Mixed-Use Zoning', code: 'MX1-MX3', description: 'Combined residential/commercial' },
    { name: 'Agricultural Zoning', code: 'A1-A2', description: 'Farming and agricultural operations' },
    { name: 'Special Purpose', code: 'SP1-SP2', description: 'Institutional, recreational, etc.' },
  ];

  // AI Contract Analysis Results (Mock)
  const aiAnalysisResults = {
    riskScore: 68,
    highRiskClauses: [
      { clause: 'Unlimited Liability', severity: 'Critical', location: 'Section 12.3' },
      { clause: 'One-sided Termination', severity: 'High', location: 'Section 8.1' },
      { clause: 'Vague Payment Terms', severity: 'Medium', location: 'Section 5.2' },
    ],
    missingProvisions: [
      'Force Majeure Clause',
      'Dispute Resolution Process',
      'Confidentiality Agreement',
    ],
    complianceIssues: [
      'Missing Fair Housing Language (Federal Requirement)',
      'Incomplete Disclosure Requirements (State Law)',
    ],
    recommendations: [
      'Add arbitration clause to reduce litigation risk',
      'Include specific performance metrics',
      'Clarify termination conditions',
    ],
  };

  // Legal Automation Workflows
  const automationWorkflows = [
    {
      name: 'Lease Renewal Automation',
      description: 'Automatically generate renewal notices 90 days before expiration',
      status: 'Active',
      triggers: 12,
    },
    {
      name: 'Compliance Monitoring',
      description: 'Monitor property compliance with zoning and building codes',
      status: 'Active',
      triggers: 28,
    },
    {
      name: 'Document Expiration Alerts',
      description: 'Alert on expiring licenses, permits, and legal documents',
      status: 'Active',
      triggers: 5,
    },
    {
      name: 'Contract Review Queue',
      description: 'Auto-route contracts for review based on value and risk',
      status: 'Active',
      triggers: 8,
    },
  ];

  // Legal Knowledge Base
  const knowledgeBase = [
    {
      topic: 'Fair Housing Act',
      articles: 24,
      lastUpdated: '2025-10-15',
      category: 'Federal Law',
    },
    {
      topic: '1031 Exchange Rules',
      articles: 18,
      lastUpdated: '2025-09-22',
      category: 'Tax Law',
    },
    {
      topic: 'Landlord-Tenant Laws',
      articles: 45,
      lastUpdated: '2025-11-01',
      category: 'State Law',
    },
    {
      topic: 'Environmental Regulations',
      articles: 32,
      lastUpdated: '2025-10-28',
      category: 'EPA/Environmental',
    },
    {
      topic: 'Title Insurance',
      articles: 15,
      lastUpdated: '2025-10-10',
      category: 'Real Estate',
    },
  ];

  return (
    <Box>
      {/* Enhanced Header with AI Badge */}
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
            <GavelIcon sx={{ fontSize: 38, color: 'white' }} />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 0.5 }}>
              <Typography variant="h4" sx={{ fontWeight: 700, color: 'white' }}>
                Legal Services Center
              </Typography>
              <Chip
                icon={<AIIcon sx={{ color: 'white !important' }} />}
                label="AI-Powered"
                size="small"
                sx={{
                  bgcolor: 'rgba(255, 255, 255, 0.25)',
                  color: 'white',
                  fontWeight: 600,
                  backdropFilter: 'blur(10px)',
                }}
              />
              <Chip
                icon={<AutomationIcon sx={{ color: 'white !important' }} />}
                label="Automated"
                size="small"
                sx={{
                  bgcolor: 'rgba(255, 255, 255, 0.25)',
                  color: 'white',
                  fontWeight: 600,
                  backdropFilter: 'blur(10px)',
                }}
              />
            </Stack>
            <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.95)', fontWeight: 500 }}>
              AI-powered legal automation | Smart document generation | Compliance monitoring
            </Typography>
          </Box>
          <Button
            variant="contained"
            startIcon={<SmartIcon />}
            sx={{
              bgcolor: 'white',
              color: 'primary.main',
              fontWeight: 600,
              '&:hover': { bgcolor: 'rgba(255,255,255,0.9)' },
            }}
          >
            Legal AI Assistant
          </Button>
        </Stack>
      </Paper>

      {/* Quick Action Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
            }}
            onClick={() => setDocumentGeneratorOpen(true)}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'primary.main', width: 56, height: 56 }}>
                  <MagicIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Generate Document
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI-powered in 3 min
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
            }}
            onClick={() => setAIAnalysisOpen(true)}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'success.main', width: 56, height: 56 }}>
                  <AnalyticsIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Analyze Contract
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    AI risk assessment
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
            }}
            onClick={() => setZoningCheckerOpen(true)}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'warning.main', width: 56, height: 56 }}>
                  <MapIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Check Zoning
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Instant verification
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s',
              '&:hover': { transform: 'translateY(-4px)', boxShadow: 6 },
            }}
            onClick={() => setClauseLibraryOpen(true)}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Avatar sx={{ bgcolor: 'info.main', width: 56, height: 56 }}>
                  <LibraryIcon />
                </Avatar>
                <Box>
                  <Typography variant="h6" fontWeight={600}>
                    Clause Library
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    500+ pre-approved
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
          <Tab icon={<MagicIcon />} iconPosition="start" label="Document Generator" />
          <Tab icon={<LibraryIcon />} iconPosition="start" label="Clause Library" />
          <Tab icon={<PublicIcon />} iconPosition="start" label="State Forms" />
          <Tab icon={<AIIcon />} iconPosition="start" label="AI Contract Analysis" />
          <Tab icon={<MapIcon />} iconPosition="start" label="Zoning & Compliance" />
          <Tab icon={<AutomationIcon />} iconPosition="start" label="Automation" />
          <Tab icon={<EducationIcon />} iconPosition="start" label="Legal Knowledge" />
          <Tab icon={<SignatureIcon />} iconPosition="start" label="E-Signature" />
        </Tabs>

        {/* Tab 0: Automated Document Generator */}
        <TabPanel value={activeTab} index={0}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  AI-Powered Document Generator
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Generate legally compliant documents in minutes with AI assistance
                </Typography>
              </Box>
              <Chip
                icon={<SpeedIcon />}
                label="90% Faster"
                color="success"
                sx={{ fontWeight: 600 }}
              />
            </Stack>

            <Grid container spacing={3}>
              {documentTemplates.map((template, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <Card variant="outlined" sx={{ height: '100%', position: 'relative' }}>
                    {template.aiPowered && (
                      <Chip
                        icon={<AIIcon fontSize="small" />}
                        label="AI"
                        size="small"
                        color="primary"
                        sx={{ position: 'absolute', top: 12, right: 12, fontWeight: 600 }}
                      />
                    )}
                    <CardContent sx={{ pb: 1 }}>
                      <Stack direction="row" alignItems="flex-start" spacing={2}>
                        <Avatar sx={{ bgcolor: 'primary.light' }}>
                          <ArticleIcon color="primary" />
                        </Avatar>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h6" sx={{ fontSize: '1rem', fontWeight: 600, mb: 1 }}>
                            {template.name}
                          </Typography>
                          <Stack direction="row" spacing={1} sx={{ mb: 1.5 }}>
                            <Chip
                              label={template.complexity}
                              size="small"
                              color={template.complexity === 'High' ? 'error' : template.complexity === 'Medium' ? 'warning' : 'success'}
                              variant="outlined"
                            />
                            <Chip label={`~${template.time}`} size="small" variant="outlined" />
                            {template.stateSpecific && (
                              <Chip label="State-Specific" size="small" color="info" variant="outlined" />
                            )}
                          </Stack>
                          <Typography variant="body2" color="text.secondary">
                            Automated field population, clause suggestions, and compliance checks
                          </Typography>
                        </Box>
                      </Stack>
                    </CardContent>
                    <CardActions>
                      <Button
                        size="small"
                        startIcon={<MagicIcon />}
                        fullWidth
                        variant="contained"
                        onClick={() => {
                          setSelectedDocType(template.type);
                          setDocumentGeneratorOpen(true);
                        }}
                      >
                        Generate Now
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Alert severity="info" icon={<SmartIcon />} sx={{ mb: 2 }}>
                <Typography variant="subtitle2" fontWeight={600}>
                  Smart Document Assembly
                </Typography>
                <Typography variant="body2">
                  Our AI analyzes your inputs and automatically selects appropriate clauses, ensures state compliance,
                  and flags potential issues before generation.
                </Typography>
              </Alert>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 1: Clause Library */}
        <TabPanel value={activeTab} index={1}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Pre-Approved Clause Library
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  500+ vetted clauses with AI scoring and usage recommendations
                </Typography>
              </Box>
              <Stack direction="row" spacing={1}>
                <TextField
                  placeholder="Search clauses..."
                  size="small"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                  }}
                  sx={{ width: 250 }}
                />
                <Button variant="contained" startIcon={<AddIcon />}>
                  Custom Clause
                </Button>
              </Stack>
            </Stack>

            {clauseLibrary.map((category, catIndex) => (
              <Accordion key={catIndex} defaultExpanded={catIndex === 0}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2} sx={{ width: '100%' }}>
                    <LibraryIcon color="primary" />
                    <Typography variant="h6" fontWeight={600}>
                      {category.category}
                    </Typography>
                    <Chip label={`${category.clauses.length} clauses`} size="small" />
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Clause Name</TableCell>
                          <TableCell>Usage Recommendation</TableCell>
                          <TableCell>AI Safety Score</TableCell>
                          <TableCell>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {category.clauses.map((clause, clauseIndex) => (
                          <TableRow key={clauseIndex}>
                            <TableCell>
                              <Typography variant="body2" fontWeight={500}>
                                {clause.name}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Chip
                                label={clause.usage}
                                size="small"
                                color={
                                  clause.usage.includes('Essential') || clause.usage.includes('Required')
                                    ? 'success'
                                    : clause.usage.includes('Risk')
                                    ? 'error'
                                    : 'default'
                                }
                              />
                            </TableCell>
                            <TableCell>
                              <Stack direction="row" alignItems="center" spacing={1}>
                                <LinearProgress
                                  variant="determinate"
                                  value={clause.aiScore}
                                  sx={{ flex: 1, height: 8, borderRadius: 4 }}
                                  color={clause.aiScore >= 90 ? 'success' : clause.aiScore >= 75 ? 'warning' : 'error'}
                                />
                                <Typography variant="body2" fontWeight={600}>
                                  {clause.aiScore}
                                </Typography>
                              </Stack>
                            </TableCell>
                            <TableCell>
                              <Stack direction="row" spacing={1}>
                                <Tooltip title="Preview Clause">
                                  <IconButton size="small">
                                    <InfoIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Copy to Clipboard">
                                  <IconButton size="small">
                                    <CopyIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                                <Tooltip title="Add to Document">
                                  <IconButton size="small" color="primary">
                                    <AddIcon fontSize="small" />
                                  </IconButton>
                                </Tooltip>
                              </Stack>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </AccordionDetails>
              </Accordion>
            ))}

            <Card sx={{ mt: 3, bgcolor: 'primary.light' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={2}>
                  <AIIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                  <Box>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      AI Clause Recommendations
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Our AI analyzes your document context and suggests the most appropriate clauses based on
                      jurisdiction, property type, and transaction structure.
                    </Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Box>
        </TabPanel>

        {/* Tab 2: State-Specific Forms */}
        <TabPanel value={activeTab} index={2}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  State-Specific Legal Forms Library
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Access jurisdiction-specific forms with automatic compliance updates
                </Typography>
              </Box>
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Select State</InputLabel>
                <Select
                  value={selectedState}
                  label="Select State"
                  onChange={(e) => setSelectedState(e.target.value)}
                >
                  <MenuItem value="">All States</MenuItem>
                  {stateFormsLibrary.map((state, index) => (
                    <MenuItem key={index} value={state.state}>
                      {state.state}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Stack>

            <Grid container spacing={3}>
              {stateFormsLibrary.map((state, index) => (
                <Grid item xs={12} md={6} lg={4} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
                        <Avatar sx={{ bgcolor: 'info.main', width: 50, height: 50 }}>
                          <PublicIcon />
                        </Avatar>
                        <Box>
                          <Typography variant="h6" fontWeight={600}>
                            {state.state}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {state.forms} available forms
                          </Typography>
                        </Box>
                      </Stack>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle2" fontWeight={600} gutterBottom>
                        Categories:
                      </Typography>
                      <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
                        {state.categories.map((cat, catIndex) => (
                          <Chip key={catIndex} label={cat} size="small" variant="outlined" sx={{ mb: 0.5 }} />
                        ))}
                      </Stack>
                    </CardContent>
                    <CardActions>
                      <Button size="small" fullWidth variant="outlined">
                        Browse Forms
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Alert severity="success" icon={<SyncIcon />}>
                <Typography variant="subtitle2" fontWeight={600}>
                  Auto-Updated Compliance
                </Typography>
                <Typography variant="body2">
                  All state forms are automatically updated when regulations change. Last update: November 2025
                </Typography>
              </Alert>
            </Box>

            <Paper variant="outlined" sx={{ p: 3, mt: 3 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Multi-State Transaction Support
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Our platform automatically identifies when your transaction involves multiple states and
                provides the necessary forms and compliance requirements for each jurisdiction.
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <LanguageIcon color="primary" sx={{ fontSize: 32, mb: 1 }} />
                      <Typography variant="subtitle1" fontWeight={600}>
                        50 State Coverage
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Complete form libraries for all US states
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <ShieldIcon color="primary" sx={{ fontSize: 32, mb: 1 }} />
                      <Typography variant="subtitle1" fontWeight={600}>
                        Compliance Guaranteed
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Forms reviewed by licensed attorneys
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <NotificationIcon color="primary" sx={{ fontSize: 32, mb: 1 }} />
                      <Typography variant="subtitle1" fontWeight={600}>
                        Update Notifications
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Alerts when regulations change
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Paper>
          </Box>
        </TabPanel>

        {/* Tab 3: AI Contract Analysis */}
        <TabPanel value={activeTab} index={3}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  AI-Powered Contract Analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Upload contracts for instant AI risk assessment and clause extraction
                </Typography>
              </Box>
              <Button variant="contained" startIcon={<UploadIcon />} size="large">
                Upload Contract
              </Button>
            </Stack>

            <Grid container spacing={3}>
              {/* Risk Score Card */}
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Overall Risk Score
                    </Typography>
                    <Box sx={{ position: 'relative', display: 'inline-flex', my: 2 }}>
                      <Box
                        sx={{
                          width: 120,
                          height: 120,
                          borderRadius: '50%',
                          background: `conic-gradient(${
                            aiAnalysisResults.riskScore > 70 ? '#f44336' : aiAnalysisResults.riskScore > 40 ? '#ff9800' : '#4caf50'
                          } ${aiAnalysisResults.riskScore * 3.6}deg, #e0e0e0 0deg)`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <Box
                          sx={{
                            width: 100,
                            height: 100,
                            borderRadius: '50%',
                            bgcolor: 'background.paper',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexDirection: 'column',
                          }}
                        >
                          <Typography variant="h3" fontWeight={700}>
                            {aiAnalysisResults.riskScore}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Risk Score
                          </Typography>
                        </Box>
                      </Box>
                    </Box>
                    <Alert severity={aiAnalysisResults.riskScore > 70 ? 'error' : aiAnalysisResults.riskScore > 40 ? 'warning' : 'success'}>
                      {aiAnalysisResults.riskScore > 70
                        ? 'High Risk - Review Required'
                        : aiAnalysisResults.riskScore > 40
                        ? 'Medium Risk - Some Concerns'
                        : 'Low Risk - Good Standing'}
                    </Alert>
                  </CardContent>
                </Card>
              </Grid>

              {/* High Risk Clauses */}
              <Grid item xs={12} md={8}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      High Risk Clauses Detected
                    </Typography>
                    <List>
                      {aiAnalysisResults.highRiskClauses.map((item, index) => (
                        <React.Fragment key={index}>
                          <ListItem>
                            <ListItemIcon>
                              <ErrorIcon
                                color={item.severity === 'Critical' ? 'error' : item.severity === 'High' ? 'warning' : 'action'}
                              />
                            </ListItemIcon>
                            <ListItemText
                              primary={
                                <Stack direction="row" alignItems="center" spacing={1}>
                                  <Typography variant="body1" fontWeight={600}>
                                    {item.clause}
                                  </Typography>
                                  <Chip
                                    label={item.severity}
                                    size="small"
                                    color={item.severity === 'Critical' ? 'error' : item.severity === 'High' ? 'warning' : 'default'}
                                  />
                                </Stack>
                              }
                              secondary={`Found in ${item.location}`}
                            />
                            <Button size="small" variant="outlined">
                              View Details
                            </Button>
                          </ListItem>
                          {index < aiAnalysisResults.highRiskClauses.length - 1 && <Divider />}
                        </React.Fragment>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>

              {/* Missing Provisions */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                      <FindIcon color="warning" />
                      <Typography variant="h6" fontWeight={600}>
                        Missing Provisions
                      </Typography>
                    </Stack>
                    <List dense>
                      {aiAnalysisResults.missingProvisions.map((provision, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <WarningIcon fontSize="small" color="warning" />
                          </ListItemIcon>
                          <ListItemText primary={provision} />
                        </ListItem>
                      ))}
                    </List>
                    <Button variant="outlined" fullWidth sx={{ mt: 2 }}>
                      Add Suggested Clauses
                    </Button>
                  </CardContent>
                </Card>
              </Grid>

              {/* Compliance Issues */}
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                      <ShieldIcon color="error" />
                      <Typography variant="h6" fontWeight={600}>
                        Compliance Issues
                      </Typography>
                    </Stack>
                    <List dense>
                      {aiAnalysisResults.complianceIssues.map((issue, index) => (
                        <ListItem key={index}>
                          <ListItemIcon>
                            <ErrorIcon fontSize="small" color="error" />
                          </ListItemIcon>
                          <ListItemText primary={issue} />
                        </ListItem>
                      ))}
                    </List>
                    <Button variant="contained" color="error" fullWidth sx={{ mt: 2 }}>
                      Fix Compliance Issues
                    </Button>
                  </CardContent>
                </Card>
              </Grid>

              {/* AI Recommendations */}
              <Grid item xs={12}>
                <Card sx={{ bgcolor: 'info.light' }}>
                  <CardContent>
                    <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
                      <AIIcon sx={{ fontSize: 36, color: 'info.main' }} />
                      <Typography variant="h6" fontWeight={600}>
                        AI Recommendations
                      </Typography>
                    </Stack>
                    <Grid container spacing={2}>
                      {aiAnalysisResults.recommendations.map((rec, index) => (
                        <Grid item xs={12} md={4} key={index}>
                          <Paper variant="outlined" sx={{ p: 2, bgcolor: 'background.paper' }}>
                            <Stack direction="row" spacing={1} alignItems="flex-start">
                              <CheckCircleIcon color="success" sx={{ mt: 0.5 }} />
                              <Typography variant="body2">{rec}</Typography>
                            </Stack>
                          </Paper>
                        </Grid>
                      ))}
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Paper variant="outlined" sx={{ p: 3, bgcolor: 'background.default' }}>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Contract Comparison Tool
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  Upload multiple versions to see changes, identify deviations from your playbook, and track negotiations.
                </Typography>
                <Button variant="contained" startIcon={<CompareIcon />}>
                  Compare Contracts
                </Button>
              </Paper>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 4: Zoning & Compliance */}
        <TabPanel value={activeTab} index={4}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Zoning & Regulatory Compliance
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Instant zoning verification and compliance automation for all US jurisdictions
                </Typography>
              </Box>
            </Stack>

            <Grid container spacing={3}>
              {/* Zoning Lookup Tool */}
              <Grid item xs={12} md={8}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Property Zoning Lookup
                    </Typography>
                    <Stack spacing={2} sx={{ mt: 2 }}>
                      <TextField
                        label="Property Address"
                        placeholder="123 Main Street, City, State ZIP"
                        fullWidth
                        InputProps={{
                          endAdornment: (
                            <InputAdornment position="end">
                              <LocationIcon />
                            </InputAdornment>
                          ),
                        }}
                      />
                      <Stack direction="row" spacing={2}>
                        <FormControl fullWidth>
                          <InputLabel>City/County</InputLabel>
                          <Select label="City/County">
                            <MenuItem value="los-angeles">Los Angeles, CA</MenuItem>
                            <MenuItem value="chicago">Chicago, IL</MenuItem>
                            <MenuItem value="houston">Houston, TX</MenuItem>
                            <MenuItem value="new-york">New York, NY</MenuItem>
                          </Select>
                        </FormControl>
                        <FormControl fullWidth>
                          <InputLabel>Property Type</InputLabel>
                          <Select label="Property Type">
                            <MenuItem value="residential">Residential</MenuItem>
                            <MenuItem value="commercial">Commercial</MenuItem>
                            <MenuItem value="industrial">Industrial</MenuItem>
                            <MenuItem value="mixed">Mixed-Use</MenuItem>
                          </Select>
                        </FormControl>
                      </Stack>
                      <Button variant="contained" size="large" startIcon={<SearchIcon />} fullWidth>
                        Check Zoning Status
                      </Button>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              {/* Quick Zoning Info */}
              <Grid item xs={12} md={4}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Zoning Database
                    </Typography>
                    <Stack spacing={1} sx={{ mt: 2 }}>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          Jurisdictions:
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          3,200+
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          Zoning Codes:
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          125,000+
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" color="text.secondary">
                          Last Updated:
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          Nov 2025
                        </Typography>
                      </Stack>
                      <Divider sx={{ my: 1 }} />
                      <Alert severity="success" icon={<SyncIcon />} sx={{ mt: 1 }}>
                        Real-time updates from municipal sources
                      </Alert>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              {/* Zoning Categories */}
              <Grid item xs={12}>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Common Zoning Classifications
                </Typography>
                <Grid container spacing={2}>
                  {zoningCategories.map((zone, index) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Card variant="outlined">
                        <CardContent>
                          <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 1 }}>
                            <Chip label={zone.code} color="primary" size="small" />
                            <Typography variant="subtitle1" fontWeight={600}>
                              {zone.name}
                            </Typography>
                          </Stack>
                          <Typography variant="body2" color="text.secondary">
                            {zone.description}
                          </Typography>
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Grid>

              {/* Compliance Automation */}
              <Grid item xs={12}>
                <Card sx={{ bgcolor: 'success.light' }}>
                  <CardContent>
                    <Stack direction="row" alignItems="center" spacing={2}>
                      <AutomationIcon sx={{ fontSize: 40, color: 'success.main' }} />
                      <Box>
                        <Typography variant="h6" fontWeight={600} gutterBottom>
                          Automated Compliance Monitoring
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Track zoning changes, permit requirements, and code violations automatically.
                          Get alerts when regulations change affecting your properties.
                        </Typography>
                      </Box>
                    </Stack>
                    <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
                      <Button variant="contained">Enable Auto-Monitoring</Button>
                      <Button variant="outlined">View Compliance Dashboard</Button>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>

              {/* Additional Compliance Tools */}
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <PolicyIcon color="primary" sx={{ fontSize: 36, mb: 1 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Building Codes
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Access local building codes and permit requirements
                    </Typography>
                    <Button variant="outlined" fullWidth>
                      Check Codes
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <VerifiedIcon color="primary" sx={{ fontSize: 36, mb: 1 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Environmental
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      EPA compliance and environmental regulations
                    </Typography>
                    <Button variant="outlined" fullWidth>
                      View Reports
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <ShieldIcon color="primary" sx={{ fontSize: 36, mb: 1 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Fair Housing
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Fair Housing Act compliance verification
                    </Typography>
                    <Button variant="outlined" fullWidth>
                      Compliance Check
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Box>
        </TabPanel>

        {/* Tab 5: Legal Automation */}
        <TabPanel value={activeTab} index={5}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Legal Workflow Automation
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Automate repetitive legal tasks and processes
                </Typography>
              </Box>
              <Button variant="contained" startIcon={<AddIcon />}>
                Create Workflow
              </Button>
            </Stack>

            <Grid container spacing={3}>
              {automationWorkflows.map((workflow, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card>
                    <CardContent>
                      <Stack direction="row" justifyContent="space-between" alignItems="flex-start" sx={{ mb: 2 }}>
                        <Stack direction="row" spacing={2} alignItems="center">
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            <AutomationIcon />
                          </Avatar>
                          <Box>
                            <Typography variant="h6" fontWeight={600}>
                              {workflow.name}
                            </Typography>
                            <Chip
                              label={workflow.status}
                              size="small"
                              color="success"
                              sx={{ mt: 0.5 }}
                            />
                          </Box>
                        </Stack>
                        <FormControlLabel
                          control={<Switch defaultChecked />}
                          label=""
                        />
                      </Stack>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {workflow.description}
                      </Typography>
                      <Divider sx={{ my: 2 }} />
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Stack direction="row" spacing={1} alignItems="center">
                          <SpeedIcon fontSize="small" color="action" />
                          <Typography variant="body2" color="text.secondary">
                            {workflow.triggers} triggers this month
                          </Typography>
                        </Stack>
                        <Button size="small" variant="outlined">
                          Configure
                        </Button>
                      </Stack>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Available Automation Templates
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        Document Expiration
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Auto-generate renewal notices and track expiring documents
                      </Typography>
                      <Button variant="text" sx={{ mt: 1 }}>
                        Set Up →
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        Compliance Alerts
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Get notified of regulatory changes affecting your properties
                      </Typography>
                      <Button variant="text" sx={{ mt: 1 }}>
                        Set Up →
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        Contract Routing
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Automatically route contracts to appropriate reviewers
                      </Typography>
                      <Button variant="text" sx={{ mt: 1 }}>
                        Set Up →
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 6: Legal Knowledge Base */}
        <TabPanel value={activeTab} index={6}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Legal Knowledge Base
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive legal resources and regulatory information
                </Typography>
              </Box>
              <TextField
                placeholder="Search knowledge base..."
                size="small"
                sx={{ width: 300 }}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                }}
              />
            </Stack>

            <Grid container spacing={3}>
              {knowledgeBase.map((kb, index) => (
                <Grid item xs={12} md={6} key={index}>
                  <Card variant="outlined">
                    <CardContent>
                      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
                        <Avatar sx={{ bgcolor: 'info.light' }}>
                          <EducationIcon color="info" />
                        </Avatar>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h6" fontWeight={600}>
                            {kb.topic}
                          </Typography>
                          <Chip label={kb.category} size="small" variant="outlined" />
                        </Box>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between" sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                          {kb.articles} articles
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Updated {kb.lastUpdated}
                        </Typography>
                      </Stack>
                    </CardContent>
                    <CardActions>
                      <Button size="small" fullWidth>
                        Browse Articles
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Card sx={{ bgcolor: 'primary.light' }}>
                <CardContent>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <SupportIcon sx={{ fontSize: 40, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        Expert Legal Support
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Need help? Connect with licensed real estate attorneys for consultations and complex matters.
                      </Typography>
                      <Button variant="contained" sx={{ mt: 2 }}>
                        Schedule Consultation
                      </Button>
                    </Box>
                  </Stack>
                </CardContent>
              </Card>
            </Box>
          </Box>
        </TabPanel>

        {/* Tab 7: E-Signature Integration */}
        <TabPanel value={activeTab} index={7}>
          <Box sx={{ p: 3 }}>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
              <Box>
                <Typography variant="h5" fontWeight={600} gutterBottom>
                  Electronic Signature Management
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Secure, legally binding e-signatures integrated with document generation
                </Typography>
              </Box>
            </Stack>

            <Grid container spacing={3}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <SignatureIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Send for Signature
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Upload documents and send to multiple signers with tracking
                    </Typography>
                    <Button variant="contained" fullWidth>
                      Start Signing Process
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <SecurityIcon sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Audit Trail
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      Complete signature history with timestamps and IP verification
                    </Typography>
                    <Button variant="contained" fullWidth>
                      View Audit Logs
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <VerifiedIcon sx={{ fontSize: 60, color: 'info.main', mb: 2 }} />
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      Legally Binding
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      ESIGN Act and UETA compliant signatures
                    </Typography>
                    <Button variant="contained" fullWidth>
                      Learn More
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            <Box sx={{ mt: 4 }}>
              <Alert severity="info">
                <Typography variant="subtitle2" fontWeight={600}>
                  Integrated E-Signature Workflow
                </Typography>
                <Typography variant="body2">
                  Generate documents with our AI assistant, send for signature, track status, and store completed
                  documents—all in one platform.
                </Typography>
              </Alert>
            </Box>
          </Box>
        </TabPanel>
      </Paper>

      {/* Document Generator Dialog */}
      <Dialog open={documentGeneratorOpen} onClose={() => setDocumentGeneratorOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Stack direction="row" alignItems="center" spacing={1}>
            <MagicIcon color="primary" />
            <Typography variant="h6" fontWeight={600}>
              AI Document Generator
            </Typography>
            <Chip icon={<AIIcon />} label="AI-Powered" size="small" color="primary" />
          </Stack>
        </DialogTitle>
        <DialogContent>
          <Stepper activeStep={0} sx={{ mt: 2, mb: 4 }}>
            <Step>
              <StepLabel>Select Template</StepLabel>
            </Step>
            <Step>
              <StepLabel>Fill Details</StepLabel>
            </Step>
            <Step>
              <StepLabel>Review & Generate</StepLabel>
            </Step>
          </Stepper>
          <FormControl fullWidth>
            <InputLabel>Document Type</InputLabel>
            <Select value={selectedDocType} onChange={(e) => setSelectedDocType(e.target.value)} label="Document Type">
              <MenuItem value="purchase">Purchase Agreement</MenuItem>
              <MenuItem value="lease">Lease Agreement</MenuItem>
              <MenuItem value="deed">Property Deed</MenuItem>
              <MenuItem value="construction">Construction Contract</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDocumentGeneratorOpen(false)}>Cancel</Button>
          <Button variant="contained" startIcon={<MagicIcon />}>
            Continue
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EnhancedLegalServicesDashboard;
