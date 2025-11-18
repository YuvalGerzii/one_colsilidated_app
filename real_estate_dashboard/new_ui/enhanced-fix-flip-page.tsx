import React, { useState, useMemo, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Tab,
  Tabs,
  TextField,
  Button,
  Grid,
  Paper,
  Chip,
  Stack,
  Alert,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Divider,
  Card,
  CardContent,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  ShowChart as ShowChartIcon,
  MenuBook as MenuBookIcon,
  Analytics as AnalyticsIcon,
  CheckCircle as CheckCircleIcon,
  Refresh as RefreshIcon,
  Save as SaveIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';

// Custom styled components for the dark theme
const DarkHeaderSection = styled(Box)(({ theme }) => ({
  background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
  color: 'white',
  minHeight: '100vh',
  width: '100%',
  margin: 0,
  padding: 0,
  position: 'relative',
}));

const ContentWrapper = styled(Box)(({ theme }) => ({
  width: '100%',
  maxWidth: '100%',
  margin: 0,
  padding: 0,
}));

const StyledTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    color: 'white',
    '& fieldset': {
      borderColor: 'rgba(255, 255, 255, 0.2)',
    },
    '&:hover fieldset': {
      borderColor: 'rgba(255, 255, 255, 0.3)',
    },
    '&.Mui-focused fieldset': {
      borderColor: 'rgba(255, 255, 255, 0.5)',
    },
  },
  '& .MuiInputLabel-root': {
    color: 'rgba(255, 255, 255, 0.7)',
  },
  '& .MuiInputLabel-root.Mui-focused': {
    color: 'white',
  },
}));

const StyledSelect = styled(Select)(({ theme }) => ({
  backgroundColor: 'rgba(255, 255, 255, 0.05)',
  color: 'white',
  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(255, 255, 255, 0.2)',
  },
  '&:hover .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
    borderColor: 'rgba(255, 255, 255, 0.5)',
  },
  '& .MuiSvgIcon-root': {
    color: 'rgba(255, 255, 255, 0.7)',
  },
}));

const StyledTabs = styled(Tabs)(({ theme }) => ({
  backgroundColor: 'rgba(255, 255, 255, 0.05)',
  borderRadius: '12px',
  padding: '4px',
  minHeight: '48px',
  '& .MuiTabs-indicator': {
    backgroundColor: 'white',
    height: '3px',
    borderRadius: '3px',
  },
}));

const StyledTab = styled(Tab)(({ theme }) => ({
  color: 'rgba(255, 255, 255, 0.7)',
  minHeight: '44px',
  textTransform: 'none',
  fontSize: '0.95rem',
  fontWeight: 500,
  '&.Mui-selected': {
    color: 'white',
  },
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
  },
}));

const JumpToChip = styled(Chip)(({ theme }) => ({
  backgroundColor: 'rgba(255, 255, 255, 0.1)',
  color: 'white',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  '&:hover': {
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    cursor: 'pointer',
  },
}));

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
      id={`model-tabpanel-${index}`}
      aria-labelledby={`model-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export const EnhancedFixAndFlipPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(0);
  const [isCalculatorLoaded, setCalculatorLoaded] = useState(false);
  const [hasRunAnalysis, setHasRunAnalysis] = useState(false);
  const [formData, setFormData] = useState({
    projectName: 'Sample Fix & Flip',
    market: 'Austin, TX',
    analyst: '',
    propertyType: 'Single Family',
    address: '',
    squareFeet: '',
    bedrooms: '',
    bathrooms: '',
    purchasePrice: '',
    afterRepairValue: '',
    renovationCost: '',
    holdingPeriod: '6',
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleInputChange = (field: string) => (event: any) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleRunAnalysis = () => {
    setHasRunAnalysis(true);
    // Trigger analysis logic here
  };

  const quickJumpModels = [
    { label: 'Single-Family Rental', path: '/real-estate-models/single-family-rental' },
    { label: 'Small Multifamily (2-6 units)', path: '/real-estate-models/small-multifamily' },
    { label: 'Hotel', path: '/real-estate-models/hotel' },
    { label: 'High-Rise Multifamily (7+ units)', path: '/real-estate-models/extended-multifamily' },
    { label: 'Mixed-Use Tower', path: '/real-estate-models/mixed-use' },
    { label: 'Lease Analyzer', path: '/real-estate-models/lease-analyzer' },
    { label: 'Renovation Budget', path: '/real-estate-models/renovation-budget' },
  ];

  const modelUrl = useMemo(() => {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const normalizedBase = API_BASE_URL.replace(/\/$/, '');
    return `${normalizedBase}/real-estate/tools/fix_and_flip`;
  }, []);

  return (
    <DarkHeaderSection>
      <ContentWrapper>
        {/* Header Section */}
        <Box sx={{ p: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/real-estate-tools')}
            sx={{
              color: 'rgba(255, 255, 255, 0.9)',
              mb: 3,
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            All real estate models
          </Button>

          <Typography variant="h3" sx={{ fontWeight: 700, mb: 2 }}>
            Fix & Flip financial model
          </Typography>

          <Typography variant="h6" sx={{ mb: 4, opacity: 0.9, lineHeight: 1.6, maxWidth: '900px' }}>
            Analyze short-term renovation projects with comprehensive financial modeling. This model
            calculates the Maximum Allowable Offer (MAO), tracks renovation costs, holding expenses, and
            exit strategies using the 70% rule and market-speed adjustments.
          </Typography>

          {/* Jump to section */}
          <Box sx={{ mb: 6 }}>
            <Typography variant="body1" sx={{ mb: 2, opacity: 0.8 }}>
              Jump to:
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              {quickJumpModels.map((model, index) => (
                <JumpToChip
                  key={index}
                  label={model.label}
                  onClick={() => navigate(model.path)}
                  sx={{ mb: 1 }}
                />
              ))}
            </Stack>
          </Box>

          {/* Tabs */}
          <StyledTabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
            <StyledTab icon={<CalculateIcon />} iconPosition="start" label="Calculator" />
            <StyledTab icon={<AssessmentIcon />} iconPosition="start" label="Results" />
            <StyledTab icon={<ShowChartIcon />} iconPosition="start" label="Charts" />
            <StyledTab icon={<MenuBookIcon />} iconPosition="start" label="Documentation" />
            <StyledTab icon={<AnalyticsIcon />} iconPosition="start" label="Advanced Analysis" />
          </StyledTabs>
        </Box>

        {/* Tab Content */}
        <Box sx={{ px: 4, pb: 4 }}>
          {/* Calculator Tab */}
          <TabPanel value={activeTab} index={0}>
            <Grid container spacing={4}>
              {/* Key Assumptions Section */}
              <Grid item xs={12}>
                <Paper
                  sx={{
                    bgcolor: 'rgba(255, 255, 255, 0.05)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    p: 3,
                  }}
                >
                  <Typography variant="h5" sx={{ mb: 3, color: 'white' }}>
                    Key assumptions
                  </Typography>

                  {/* Property Profile */}
                  <Box
                    sx={{
                      bgcolor: 'rgba(66, 165, 245, 0.15)',
                      borderLeft: '4px solid #42a5f5',
                      p: 2,
                      mb: 3,
                    }}
                  >
                    <Typography
                      variant="subtitle1"
                      sx={{
                        color: '#42a5f5',
                        fontWeight: 600,
                        mb: 2,
                        textTransform: 'uppercase',
                        letterSpacing: 1,
                      }}
                    >
                      PROPERTY PROFILE
                    </Typography>

                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <StyledTextField
                          fullWidth
                          label="Project Name"
                          value={formData.projectName}
                          onChange={handleInputChange('projectName')}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <StyledTextField
                          fullWidth
                          label="Market / Location"
                          value={formData.market}
                          onChange={handleInputChange('market')}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <StyledTextField
                          fullWidth
                          label="Analyst"
                          value={formData.analyst}
                          onChange={handleInputChange('analyst')}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <FormControl fullWidth>
                          <InputLabel sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>Property Type</InputLabel>
                          <StyledSelect
                            value={formData.propertyType}
                            onChange={handleInputChange('propertyType')}
                            label="Property Type"
                          >
                            <MenuItem value="Single Family">Single Family</MenuItem>
                            <MenuItem value="Condo">Condo</MenuItem>
                            <MenuItem value="Townhouse">Townhouse</MenuItem>
                            <MenuItem value="Multi-Family">Multi-Family</MenuItem>
                          </StyledSelect>
                        </FormControl>
                      </Grid>
                    </Grid>
                  </Box>

                  {/* Purchase Analysis */}
                  <Box
                    sx={{
                      bgcolor: 'rgba(46, 125, 50, 0.15)',
                      borderLeft: '4px solid #4caf50',
                      p: 2,
                      mb: 3,
                    }}
                  >
                    <Typography
                      variant="subtitle1"
                      sx={{
                        color: '#4caf50',
                        fontWeight: 600,
                        mb: 2,
                        textTransform: 'uppercase',
                        letterSpacing: 1,
                      }}
                    >
                      PURCHASE ANALYSIS
                    </Typography>

                    <Grid container spacing={3}>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="Purchase Price"
                          value={formData.purchasePrice}
                          onChange={handleInputChange('purchasePrice')}
                          type="number"
                          InputProps={{
                            startAdornment: <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', mr: 1 }}>$</Typography>,
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="After Repair Value (ARV)"
                          value={formData.afterRepairValue}
                          onChange={handleInputChange('afterRepairValue')}
                          type="number"
                          InputProps={{
                            startAdornment: <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', mr: 1 }}>$</Typography>,
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="Renovation Cost"
                          value={formData.renovationCost}
                          onChange={handleInputChange('renovationCost')}
                          type="number"
                          InputProps={{
                            startAdornment: <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', mr: 1 }}>$</Typography>,
                          }}
                        />
                      </Grid>
                    </Grid>
                  </Box>

                  {/* Property Details */}
                  <Box
                    sx={{
                      bgcolor: 'rgba(255, 152, 0, 0.15)',
                      borderLeft: '4px solid #ff9800',
                      p: 2,
                      mb: 3,
                    }}
                  >
                    <Typography
                      variant="subtitle1"
                      sx={{
                        color: '#ff9800',
                        fontWeight: 600,
                        mb: 2,
                        textTransform: 'uppercase',
                        letterSpacing: 1,
                      }}
                    >
                      PROPERTY DETAILS
                    </Typography>

                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <StyledTextField
                          fullWidth
                          label="Address"
                          value={formData.address}
                          onChange={handleInputChange('address')}
                        />
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <StyledTextField
                          fullWidth
                          label="Square Feet"
                          value={formData.squareFeet}
                          onChange={handleInputChange('squareFeet')}
                          type="number"
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="Bedrooms"
                          value={formData.bedrooms}
                          onChange={handleInputChange('bedrooms')}
                          type="number"
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="Bathrooms"
                          value={formData.bathrooms}
                          onChange={handleInputChange('bathrooms')}
                          type="number"
                        />
                      </Grid>
                      <Grid item xs={12} md={4}>
                        <StyledTextField
                          fullWidth
                          label="Holding Period (months)"
                          value={formData.holdingPeriod}
                          onChange={handleInputChange('holdingPeriod')}
                          type="number"
                        />
                      </Grid>
                    </Grid>
                  </Box>

                  {/* Action Buttons */}
                  <Stack direction="row" spacing={2} justifyContent="flex-end" sx={{ mt: 4 }}>
                    <Button
                      variant="outlined"
                      startIcon={<SaveIcon />}
                      sx={{
                        color: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                        '&:hover': {
                          borderColor: 'rgba(255, 255, 255, 0.5)',
                          backgroundColor: 'rgba(255, 255, 255, 0.05)',
                        },
                      }}
                    >
                      Save Draft
                    </Button>
                    <Button
                      variant="contained"
                      startIcon={<CalculateIcon />}
                      onClick={handleRunAnalysis}
                      sx={{
                        bgcolor: 'white',
                        color: '#1e3c72',
                        fontWeight: 600,
                        '&:hover': {
                          bgcolor: 'rgba(255, 255, 255, 0.9)',
                        },
                      }}
                    >
                      Run Analysis
                    </Button>
                  </Stack>

                  {hasRunAnalysis && (
                    <Alert
                      severity="success"
                      icon={<CheckCircleIcon />}
                      sx={{
                        mt: 3,
                        bgcolor: 'rgba(46, 125, 50, 0.1)',
                        color: 'white',
                        '& .MuiAlert-icon': {
                          color: '#4caf50',
                        },
                      }}
                    >
                      Analysis complete! View results in the Results and Charts tabs.
                    </Alert>
                  )}
                </Paper>
              </Grid>

              {/* Embedded Calculator (if needed) */}
              <Grid item xs={12}>
                <Paper
                  sx={{
                    bgcolor: 'rgba(255, 255, 255, 0.05)',
                    backdropFilter: 'blur(10px)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    p: 0,
                    overflow: 'hidden',
                    minHeight: 600,
                    position: 'relative',
                  }}
                >
                  {!isCalculatorLoaded && (
                    <Stack
                      spacing={2}
                      alignItems="center"
                      justifyContent="center"
                      sx={{
                        position: 'absolute',
                        inset: 0,
                        bgcolor: 'rgba(30, 60, 114, 0.9)',
                        zIndex: 1,
                      }}
                    >
                      <CircularProgress size={60} sx={{ color: 'white' }} />
                      <Typography variant="h6" sx={{ color: 'white' }}>
                        Loading Fix & Flip Calculator…
                      </Typography>
                    </Stack>
                  )}
                  <Box
                    component="iframe"
                    src={modelUrl}
                    title="Fix & Flip Calculator"
                    sx={{
                      border: 0,
                      width: '100%',
                      height: 600,
                      display: isCalculatorLoaded ? 'block' : 'none',
                    }}
                    onLoad={() => setCalculatorLoaded(true)}
                  />
                </Paper>
              </Grid>
            </Grid>
          </TabPanel>

          {/* Results Tab */}
          <TabPanel value={activeTab} index={1}>
            <Paper
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                p: 3,
                minHeight: 400,
              }}
            >
              <Typography variant="h5" sx={{ color: 'white', mb: 3 }}>
                Analysis Results
              </Typography>
              {!hasRunAnalysis ? (
                <Alert
                  severity="info"
                  sx={{
                    bgcolor: 'rgba(33, 150, 243, 0.1)',
                    color: 'white',
                    '& .MuiAlert-icon': {
                      color: '#42a5f5',
                    },
                  }}
                >
                  Run an analysis in the Calculator tab to see results here.
                </Alert>
              ) : (
                <Grid container spacing={3}>
                  {/* Add result cards here */}
                  <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'rgba(76, 175, 80, 0.1)', border: '1px solid rgba(76, 175, 80, 0.3)' }}>
                      <CardContent>
                        <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }}>
                          Maximum Allowable Offer
                        </Typography>
                        <Typography variant="h4" sx={{ color: '#4caf50', fontWeight: 700 }}>
                          $165,000
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'rgba(33, 150, 243, 0.1)', border: '1px solid rgba(33, 150, 243, 0.3)' }}>
                      <CardContent>
                        <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }}>
                          Expected Profit
                        </Typography>
                        <Typography variant="h4" sx={{ color: '#42a5f5', fontWeight: 700 }}>
                          $45,000
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Card sx={{ bgcolor: 'rgba(255, 152, 0, 0.1)', border: '1px solid rgba(255, 152, 0, 0.3)' }}>
                      <CardContent>
                        <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 1 }}>
                          ROI
                        </Typography>
                        <Typography variant="h4" sx={{ color: '#ff9800', fontWeight: 700 }}>
                          27.3%
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              )}
            </Paper>
          </TabPanel>

          {/* Charts Tab */}
          <TabPanel value={activeTab} index={2}>
            <Paper
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                p: 3,
                minHeight: 400,
              }}
            >
              <Typography variant="h5" sx={{ color: 'white', mb: 3 }}>
                Visualizations
              </Typography>
              {!hasRunAnalysis ? (
                <Alert
                  severity="info"
                  sx={{
                    bgcolor: 'rgba(33, 150, 243, 0.1)',
                    color: 'white',
                    '& .MuiAlert-icon': {
                      color: '#42a5f5',
                    },
                  }}
                >
                  Charts and graphs will appear here after running an analysis.
                </Alert>
              ) : (
                <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  [Charts will be rendered here]
                </Typography>
              )}
            </Paper>
          </TabPanel>

          {/* Documentation Tab */}
          <TabPanel value={activeTab} index={3}>
            <Paper
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                p: 3,
              }}
            >
              <Typography variant="h5" sx={{ color: 'white', mb: 3 }}>
                📖 Quick Start Guide
              </Typography>
              <Divider sx={{ borderColor: 'rgba(255, 255, 255, 0.1)', mb: 3 }} />
              <Box sx={{ color: 'rgba(255, 255, 255, 0.9)' }}>
                <Typography variant="h6" sx={{ mb: 2 }}>
                  Quick Start (5 Steps)
                </Typography>
                <ol style={{ paddingLeft: '20px', lineHeight: 1.8 }}>
                  <li>Open the Calculator tab</li>
                  <li>Enter your property details and purchase price</li>
                  <li>Input renovation costs and ARV (After Repair Value)</li>
                  <li>Review the 70% Rule calculation</li>
                  <li>Analyze profitability metrics and recommendations</li>
                </ol>

                <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
                  The 70% Rule (Core Formula)
                </Typography>
                <Box
                  sx={{
                    bgcolor: 'rgba(0, 0, 0, 0.3)',
                    p: 2,
                    borderRadius: 1,
                    fontFamily: 'monospace',
                    mb: 3,
                  }}
                >
                  <Typography>Maximum Allowable Offer (MAO) = (ARV × 70%) - Repair Costs</Typography>
                </Box>

                <Typography variant="h6" sx={{ mb: 2 }}>
                  Example:
                </Typography>
                <ul style={{ paddingLeft: '20px', lineHeight: 1.8 }}>
                  <li>ARV: $300,000</li>
                  <li>Repairs: $50,000</li>
                  <li>
                    <strong>MAO = $160,000</strong> ← Don't pay more than this!
                  </li>
                </ul>
              </Box>
            </Paper>
          </TabPanel>

          {/* Advanced Analysis Tab */}
          <TabPanel value={activeTab} index={4}>
            <Paper
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                p: 3,
                minHeight: 400,
              }}
            >
              <Typography variant="h5" sx={{ color: 'white', mb: 3 }}>
                Advanced Analysis
              </Typography>
              {!hasRunAnalysis ? (
                <Alert
                  severity="info"
                  sx={{
                    bgcolor: 'rgba(33, 150, 243, 0.1)',
                    color: 'white',
                    '& .MuiAlert-icon': {
                      color: '#42a5f5',
                    },
                  }}
                >
                  Detailed tables and sensitivity analysis will appear here after running an analysis.
                </Alert>
              ) : (
                <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                  [Advanced analysis tables will be rendered here]
                </Typography>
              )}
            </Paper>
          </TabPanel>
        </Box>
      </ContentWrapper>
    </DarkHeaderSection>
  );
};
