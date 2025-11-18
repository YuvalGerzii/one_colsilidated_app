import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Tabs,
  Tab,
  Stack,
  Chip,
  Paper,
  alpha,
  useTheme,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  Divider,
} from '@mui/material';
import {
  Home as HomeIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as AttachMoneyIcon,
  Build as BuildIcon,
  Schedule as ScheduleIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  Percent as PercentIcon,
  ShowChart as ShowChartIcon,
  AccountBalance as AccountBalanceIcon,
  Person as PersonIcon,
  LocationOn as LocationOnIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  LineChart,
  Line,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { MarkdownViewer } from '../common/MarkdownViewer';
import { FIX_AND_FLIP_QUICK_REFERENCE, FIX_AND_FLIP_COMPLETE_SUMMARY } from '../../constants/documentation/fixAndFlipDocs';
import { SensitivityAnalysisDashboard } from '../sensitivity';
import { Alert } from '@mui/material';

interface Inputs {
  // Property Profile
  projectName: string;
  location: string;
  analyst: string;
  propertyType: string;
  squareFootage: number;
  bedrooms: number;
  bathrooms: number;
  yearBuilt: number;
  marketType: 'Hot' | 'Moderate' | 'Slow';

  // Acquisition & Costs
  arv: number;
  purchasePrice: number;
  repairCosts: number;
  closingCosts: number;

  // Timeline & Holding
  holdingCostsMonthly: number;
  holdingPeriodMonths: number;
  acquisitionMonths: number;
  renovationMonths: number;
  marketingMonths: number;

  // Financing & Exit
  loanLtv: number;
  loanPoints: number;
  interestRate: number;
  sellingCostPct: number;
}

interface Results {
  mao: number;
  maoRatio: number;
  loanAmount: number;
  downPayment: number;
  pointsCost: number;
  interestCost: number;
  financingCosts: number;
  holdingCosts: number;
  totalCost: number;
  sellingCosts: number;
  grossProfit: number;
  cashInvested: number;
  roi: number;
  profitMargin: number;
  returnOnCost: number;
  passesMao: boolean;
  dealQuality: string;
}

const MARKET_RULES = {
  Hot: 0.65,
  Moderate: 0.70,
  Slow: 0.75,
};

export const FixFlipCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [docTab, setDocTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<Inputs>({
    // Property Profile
    projectName: 'Sample Fix & Flip',
    location: 'Austin, TX',
    analyst: '',
    propertyType: 'Single Family Home',
    squareFootage: 1800,
    bedrooms: 3,
    bathrooms: 2,
    yearBuilt: 1985,
    marketType: 'Moderate',

    // Acquisition & Costs
    arv: 325000,
    purchasePrice: 215000,
    repairCosts: 45000,
    closingCosts: 6000,

    // Timeline & Holding
    holdingCostsMonthly: 700,
    holdingPeriodMonths: 6,
    acquisitionMonths: 1,
    renovationMonths: 3,
    marketingMonths: 2,

    // Financing & Exit
    loanLtv: 75,
    loanPoints: 2,
    interestRate: 9.5,
    sellingCostPct: 7,
  });

  const [results, setResults] = useState<Results>({
    mao: 0,
    maoRatio: 0,
    loanAmount: 0,
    downPayment: 0,
    pointsCost: 0,
    interestCost: 0,
    financingCosts: 0,
    holdingCosts: 0,
    totalCost: 0,
    sellingCosts: 0,
    grossProfit: 0,
    cashInvested: 0,
    roi: 0,
    profitMargin: 0,
    returnOnCost: 0,
    passesMao: false,
    dealQuality: 'Marginal',
  });

  const updateInput = (key: keyof Inputs, value: number | string) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    // Calculate MAO based on market type
    const maoRatio = MARKET_RULES[inputs.marketType];
    const mao = inputs.arv * maoRatio - inputs.repairCosts;

    // Financing calculations
    const loanAmount = inputs.purchasePrice * (inputs.loanLtv / 100);
    const downPayment = inputs.purchasePrice - loanAmount;
    const pointsCost = loanAmount * (inputs.loanPoints / 100);
    const monthlyInterest = (inputs.interestRate / 100 / 12) * loanAmount;
    const interestCost = monthlyInterest * inputs.holdingPeriodMonths;
    const financingCosts = pointsCost + interestCost;

    // Holding costs
    const holdingCosts = inputs.holdingCostsMonthly * inputs.holdingPeriodMonths;

    // Total project cost
    const totalCost = inputs.purchasePrice + inputs.closingCosts + inputs.repairCosts + holdingCosts + financingCosts;

    // Selling costs
    const sellingCosts = inputs.arv * (inputs.sellingCostPct / 100);

    // Profit calculations
    const grossProfit = inputs.arv - sellingCosts - totalCost;
    const cashInvested = downPayment + inputs.closingCosts + inputs.repairCosts + pointsCost + holdingCosts;
    const roi = cashInvested > 0 ? (grossProfit / cashInvested) * 100 : 0;
    const profitMargin = inputs.arv > 0 ? (grossProfit / inputs.arv) * 100 : 0;
    const returnOnCost = totalCost > 0 ? (grossProfit / totalCost) * 100 : 0;

    // Deal quality
    let dealQuality = 'Marginal';
    if (roi >= 35) dealQuality = 'Excellent';
    else if (roi >= 25) dealQuality = 'Strong';
    else if (roi >= 15) dealQuality = 'Average';

    setResults({
      mao,
      maoRatio,
      loanAmount,
      downPayment,
      pointsCost,
      interestCost,
      financingCosts,
      holdingCosts,
      totalCost,
      sellingCosts,
      grossProfit,
      cashInvested,
      roi,
      profitMargin,
      returnOnCost,
      passesMao: inputs.purchasePrice <= mao,
      dealQuality,
    });
  }, [inputs]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value.toFixed(2)}%`;
  };

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0); // Switch to calculator tab to see results
  };

  const handleSave = () => {
    const report = {
      id: Date.now().toString(),
      modelType: 'fix-flip',
      projectName: inputs.projectName,
      location: inputs.location,
      date: new Date().toISOString(),
      inputs: inputs,
      results: results,
    };

    // Get existing reports
    const existing = localStorage.getItem('savedReports');
    const reports = existing ? JSON.parse(existing) : [];

    // Add new report
    reports.unshift(report);

    // Save to localStorage
    localStorage.setItem('savedReports', JSON.stringify(reports));

    // Show success message
    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  const costBreakdownData = [
    { name: 'Purchase', value: inputs.purchasePrice, color: '#3b82f6' },
    { name: 'Renovation', value: inputs.repairCosts, color: '#8b5cf6' },
    { name: 'Closing', value: inputs.closingCosts, color: '#f59e0b' },
    { name: 'Holding', value: results.holdingCosts, color: '#ec4899' },
    { name: 'Financing', value: results.financingCosts, color: '#ef4444' },
  ];

  const timelineData = [
    { phase: 'Acquisition', months: inputs.acquisitionMonths },
    { phase: 'Renovation', months: inputs.renovationMonths },
    { phase: 'Marketing', months: inputs.marketingMonths },
  ];

  const profitData = [
    { name: 'Total Costs', value: results.totalCost, color: '#ef4444' },
    { name: 'ARV', value: inputs.arv, color: '#10b981' },
  ];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* Header */}
      <Paper
        elevation={0}
        sx={{
          borderBottom: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}`,
          bgcolor: isDark ? alpha('#0f1419', 0.8) : alpha('#ffffff', 0.8),
          backdropFilter: 'blur(10px)',
          position: 'sticky',
          top: 0,
          zIndex: 10,
        }}
      >
        <Box sx={{ px: 4, py: 3 }}>
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Stack direction="row" alignItems="center" spacing={2}>
              <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/real-estate-tools')}
                sx={{ color: 'text.secondary' }}
              >
                All Models
              </Button>
              <Box
                sx={{
                  width: 1,
                  height: 24,
                  bgcolor: isDark ? alpha('#94a3b8', 0.2) : alpha('#0f172a', 0.2),
                }}
              />
              <Box
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                  boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(to top, rgba(255,255,255,0.2), transparent)',
                    borderRadius: 3,
                  },
                }}
              >
                <HomeIcon sx={{ fontSize: 24, color: 'white', position: 'relative', zIndex: 1 }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>
                  {inputs.projectName}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {inputs.location}
                </Typography>
              </Box>
            </Stack>
            <Stack direction="row" spacing={2}>
              {showResults && (
                <Chip
                  label={results.dealQuality}
                  sx={{
                    background:
                      results.dealQuality === 'Excellent'
                        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        : results.dealQuality === 'Strong'
                        ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        : results.dealQuality === 'Average'
                        ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                        : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                />
              )}
              {saveMessage && (
                <Chip
                  label={saveMessage}
                  sx={{
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                  icon={<CheckCircleIcon sx={{ color: 'white !important' }} />}
                />
              )}
              <Button
                variant="contained"
                startIcon={<PlayArrowIcon />}
                onClick={handleRunModel}
                sx={{
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
                  },
                }}
              >
                Run Model
              </Button>
              <Button
                variant="outlined"
                startIcon={<SaveIcon />}
                onClick={handleSave}
                disabled={!showResults}
              >
                Save
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Paper>

      {/* Description */}
      <Box sx={{ px: 4, py: 3 }}>
        <Paper
          sx={{
            p: 3,
            background: isDark
              ? `linear-gradient(135deg, ${alpha('#3b82f6', 0.05)} 0%, ${alpha('#8b5cf6', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#3b82f6', 0.03)} 0%, ${alpha('#8b5cf6', 0.03)} 100%)`,
            border: `1px solid ${alpha('#3b82f6', 0.2)}`,
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
            Comprehensive fix & flip analysis with MAO calculation using market-adjusted rules, detailed timeline tracking,
            and complete financing scenarios. Track acquisition through marketing phases with institutional-grade metrics.
          </Typography>
        </Paper>
      </Box>

      {/* Tabs */}
      <Box sx={{ px: 4, mb: 4 }}>
        <Tabs
          value={currentTab}
          onChange={(e, v) => setCurrentTab(v)}
          sx={{
            '& .MuiTabs-indicator': {
              height: 3,
              borderRadius: '3px 3px 0 0',
            },
          }}
        >
          <Tab icon={<AssessmentIcon />} iconPosition="start" label="Calculator" />
          <Tab icon={<ShowChartIcon />} iconPosition="start" label="Analytics" />
          <Tab icon={<AnalyticsIcon />} iconPosition="start" label="Sensitivity Analysis" />
          <Tab icon={<DescriptionIcon />} iconPosition="start" label="Documentation" />
        </Tabs>
      </Box>

      {/* Calculator Tab */}
      {currentTab === 0 && (
        <Box sx={{ px: 4, pb: 4 }}>
          <Grid container spacing={3}>
            {/* Left Column - Inputs (7 columns) */}
            <Grid item xs={12} lg={7}>
              <Stack spacing={3}>
                {/* Property Profile */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#6366f1', 0.2)} 0%, ${alpha('#4f46e5', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#6366f1', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <HomeIcon sx={{ fontSize: 20, color: '#6366f1' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Property Profile
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Project details and property characteristics
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Project Name
                        </Typography>
                        <TextField
                          value={inputs.projectName}
                          onChange={(e) => updateInput('projectName', e.target.value)}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Location
                        </Typography>
                        <TextField
                          value={inputs.location}
                          onChange={(e) => updateInput('location', e.target.value)}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Analyst
                        </Typography>
                        <TextField
                          value={inputs.analyst}
                          onChange={(e) => updateInput('analyst', e.target.value)}
                          fullWidth
                          size="small"
                          placeholder="Optional"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Property Type
                        </Typography>
                        <TextField
                          value={inputs.propertyType}
                          onChange={(e) => updateInput('propertyType', e.target.value)}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Square Footage
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.squareFootage}
                          onChange={(e) => updateInput('squareFootage', Number(e.target.value))}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Market Type
                        </Typography>
                        <FormControl fullWidth size="small">
                          <Select
                            value={inputs.marketType}
                            onChange={(e) => updateInput('marketType', e.target.value)}
                          >
                            <MenuItem value="Hot">Hot (65% rule)</MenuItem>
                            <MenuItem value="Moderate">Moderate (70% rule)</MenuItem>
                            <MenuItem value="Slow">Slow (75% rule)</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Bedrooms
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.bedrooms}
                          onChange={(e) => updateInput('bedrooms', Number(e.target.value))}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Bathrooms
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.bathrooms}
                          onChange={(e) => updateInput('bathrooms', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ step: 0.5 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Year Built
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.yearBuilt}
                          onChange={(e) => updateInput('yearBuilt', Number(e.target.value))}
                          fullWidth
                          size="small"
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Acquisition & Costs */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#3b82f6', 0.2)} 0%, ${alpha('#2563eb', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#3b82f6', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <AttachMoneyIcon sx={{ fontSize: 20, color: '#3b82f6' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Acquisition & Costs
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Purchase price and renovation budget
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          After Repair Value (ARV)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.arv}
                          onChange={(e) => updateInput('arv', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          inputProps={{ min: 50000, step: 1000 }}
                          error={inputs.arv < 50000}
                          helperText={inputs.arv < 50000 ? 'Minimum $50,000' : `$${(inputs.arv / 1000).toFixed(0)}K`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Purchase Price
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.purchasePrice}
                          onChange={(e) => updateInput('purchasePrice', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          inputProps={{ min: 50000, step: 1000 }}
                          error={inputs.purchasePrice < 50000}
                          helperText={inputs.purchasePrice < 50000 ? 'Minimum $50,000' : `$${(inputs.purchasePrice / 1000).toFixed(0)}K`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Renovation Budget
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.repairCosts}
                          onChange={(e) => updateInput('repairCosts', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          inputProps={{ min: 0, step: 500 }}
                          helperText={inputs.arv > 0 ? `${((inputs.repairCosts / inputs.arv) * 100).toFixed(1)}% of ARV` : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Closing Costs
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.closingCosts}
                          onChange={(e) => updateInput('closingCosts', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          inputProps={{ min: 0, step: 500 }}
                          helperText={inputs.purchasePrice > 0 ? `${((inputs.closingCosts / inputs.purchasePrice) * 100).toFixed(2)}% of purchase` : ''}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Timeline & Holding */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#f59e0b', 0.2)} 0%, ${alpha('#d97706', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#f59e0b', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <ScheduleIcon sx={{ fontSize: 20, color: '#f59e0b' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Timeline & Holding Costs
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Project phases and monthly expenses
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Monthly Holding Costs
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdingCostsMonthly}
                          onChange={(e) => updateInput('holdingCostsMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 50 }}
                          helperText="Utilities, taxes, insurance, etc."
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Total Hold Period (Months)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdingPeriodMonths}
                          onChange={(e) => updateInput('holdingPeriodMonths', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 1, step: 1 }}
                          error={inputs.holdingPeriodMonths < 1}
                          helperText={inputs.holdingPeriodMonths < 1 ? 'Minimum 1 month' : `Total holding cost: $${(inputs.holdingCostsMonthly * inputs.holdingPeriodMonths).toLocaleString()}`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Acquisition (Months)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.acquisitionMonths}
                          onChange={(e) => updateInput('acquisitionMonths', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 1 }}
                          helperText="Time to close"
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Renovation (Months)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.renovationMonths}
                          onChange={(e) => updateInput('renovationMonths', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 1 }}
                          helperText="Construction timeline"
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Marketing (Months)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.marketingMonths}
                          onChange={(e) => updateInput('marketingMonths', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 1 }}
                          helperText="Time to sell"
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Financing & Exit */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#10b981', 0.2)} 0%, ${alpha('#059669', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#10b981', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <AccountBalanceIcon sx={{ fontSize: 20, color: '#10b981' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Financing & Exit
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Loan terms and selling costs
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Loan-to-Value (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.loanLtv}
                          onChange={(e) => updateInput('loanLtv', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 50, max: 90, step: 1 }}
                          error={inputs.loanLtv < 50 || inputs.loanLtv > 90}
                          helperText={inputs.loanLtv < 50 || inputs.loanLtv > 90 ? 'Range: 50-90%' : `Loan: $${((inputs.purchasePrice * inputs.loanLtv) / 100).toLocaleString()}`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Origination Points (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.loanPoints}
                          onChange={(e) => updateInput('loanPoints', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 0, max: 5, step: 0.25 }}
                          error={inputs.loanPoints < 0 || inputs.loanPoints > 5}
                          helperText={inputs.loanPoints < 0 || inputs.loanPoints > 5 ? 'Range: 0-5%' : 'Typical: 1-3%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Interest Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.interestRate}
                          onChange={(e) => updateInput('interestRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 2, max: 25, step: 0.25 }}
                          error={inputs.interestRate < 2 || inputs.interestRate > 25}
                          helperText={inputs.interestRate < 2 || inputs.interestRate > 25 ? 'Range: 2-25%' : 'Hard money: 8-15%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Selling Costs (% of ARV)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.sellingCostPct}
                          onChange={(e) => updateInput('sellingCostPct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 3, max: 12, step: 0.25 }}
                          error={inputs.sellingCostPct < 3 || inputs.sellingCostPct > 12}
                          helperText={inputs.sellingCostPct < 3 || inputs.sellingCostPct > 12 ? 'Range: 3-12%' : inputs.arv > 0 ? `$${((inputs.arv * inputs.sellingCostPct) / 100).toLocaleString()}` : 'Commission + closing'}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Stack>
            </Grid>

            {/* Right Column - Results (5 columns) */}
            <Grid item xs={12} lg={5}>
              {!showResults ? (
                <Card
                  sx={{
                    p: 6,
                    textAlign: 'center',
                    background: isDark
                      ? `linear-gradient(135deg, ${alpha('#3b82f6', 0.1)} 0%, ${alpha('#8b5cf6', 0.1)} 100%)`
                      : `linear-gradient(135deg, ${alpha('#3b82f6', 0.05)} 0%, ${alpha('#8b5cf6', 0.05)} 100%)`,
                    border: `2px dashed ${alpha('#3b82f6', 0.3)}`,
                  }}
                >
                  <Box
                    sx={{
                      width: 72,
                      height: 72,
                      borderRadius: '50%',
                      background: `linear-gradient(135deg, ${alpha('#3b82f6', 0.2)} 0%, ${alpha('#8b5cf6', 0.2)} 100%)`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 3,
                    }}
                  >
                    <PlayArrowIcon sx={{ fontSize: 36, color: '#3b82f6' }} />
                  </Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Ready to Analyze
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                    Fill in your property details on the left, then click "Run Model" to see comprehensive financial analysis, charts, and deal evaluation.
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PlayArrowIcon />}
                    onClick={handleRunModel}
                    sx={{
                      background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)',
                      },
                    }}
                  >
                    Run Model
                  </Button>
                </Card>
              ) : (
                <Stack spacing={3}>
                {/* MAO Card */}
                <Card
                  sx={{
                    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    color: 'white',
                    position: 'relative',
                    overflow: 'hidden',
                  }}
                >
                  <Box
                    sx={{
                      position: 'absolute',
                      inset: 0,
                      background: 'linear-gradient(to top, rgba(255,255,255,0.1), transparent)',
                    }}
                  />
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 0,
                      right: 0,
                      width: 200,
                      height: 200,
                      background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
                      transform: 'translate(50%, -50%)',
                    }}
                  />
                  <CardContent sx={{ p: 4, position: 'relative', zIndex: 1 }}>
                    <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                      <Box
                        sx={{
                          width: 8,
                          height: 8,
                          borderRadius: '50%',
                          bgcolor: results.passesMao ? '#10b981' : '#f59e0b',
                          boxShadow: results.passesMao ? '0 0 8px rgba(16, 185, 129, 0.8)' : '0 0 8px rgba(245, 158, 11, 0.8)',
                        }}
                      />
                      <Typography variant="caption" sx={{ opacity: 0.9, textTransform: 'uppercase', letterSpacing: 1 }}>
                        Maximum Allowable Offer ({results.maoRatio * 100}% Rule)
                      </Typography>
                    </Stack>
                    <Typography variant="h3" sx={{ fontWeight: 700, mb: 2 }}>
                      {formatCurrency(results.mao)}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.9, lineHeight: 1.6 }}>
                      Based on the {inputs.marketType.toLowerCase()} market {results.maoRatio * 100}% rule: {formatPercent(results.maoRatio * 100)} of ARV minus
                      renovation costs
                    </Typography>
                    {!results.passesMao && (
                      <Box
                        sx={{
                          mt: 3,
                          p: 2,
                          bgcolor: alpha('#f59e0b', 0.2),
                          border: `1px solid ${alpha('#f59e0b', 0.3)}`,
                          borderRadius: 2,
                        }}
                      >
                        <Stack direction="row" spacing={1} alignItems="center">
                          <WarningIcon sx={{ fontSize: 18 }} />
                          <Box>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              Purchase price exceeds MAO
                            </Typography>
                            <Typography variant="caption" display="block">
                              Overpayment: {formatCurrency(inputs.purchasePrice - results.mao)}
                            </Typography>
                          </Box>
                        </Stack>
                      </Box>
                    )}
                  </CardContent>
                </Card>

                {/* Profitability Metrics */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                      Profitability Metrics
                    </Typography>
                    <Stack spacing={3}>
                      <Box>
                        <Stack direction="row" justifyContent="space-between" alignItems="baseline" sx={{ mb: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            Gross Profit
                          </Typography>
                          <Typography
                            variant="h5"
                            sx={{
                              fontWeight: 700,
                              color: results.grossProfit >= 0 ? '#10b981' : '#ef4444',
                            }}
                          >
                            {formatCurrency(results.grossProfit)}
                          </Typography>
                        </Stack>
                        <Box
                          sx={{
                            height: 8,
                            bgcolor: isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1),
                            borderRadius: 1,
                            overflow: 'hidden',
                          }}
                        >
                          <Box
                            sx={{
                              height: '100%',
                              bgcolor: results.grossProfit >= 0 ? '#10b981' : '#ef4444',
                              width: `${Math.min(Math.abs(results.profitMargin), 100)}%`,
                              transition: 'width 0.3s ease',
                            }}
                          />
                        </Box>
                      </Box>

                      <Box>
                        <Stack direction="row" justifyContent="space-between" alignItems="baseline" sx={{ mb: 1 }}>
                          <Typography variant="caption" color="text.secondary">
                            Return on Investment (ROI)
                          </Typography>
                          <Typography
                            variant="h5"
                            sx={{
                              fontWeight: 700,
                              color: results.roi >= 15 ? '#10b981' : results.roi >= 0 ? '#f59e0b' : '#ef4444',
                            }}
                          >
                            {formatPercent(results.roi)}
                          </Typography>
                        </Stack>
                        <Box
                          sx={{
                            height: 8,
                            bgcolor: isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1),
                            borderRadius: 1,
                            overflow: 'hidden',
                          }}
                        >
                          <Box
                            sx={{
                              height: '100%',
                              bgcolor: results.roi >= 15 ? '#10b981' : results.roi >= 0 ? '#f59e0b' : '#ef4444',
                              width: `${Math.min(Math.abs(results.roi), 100)}%`,
                              transition: 'width 0.3s ease',
                            }}
                          />
                        </Box>
                        <Stack direction="row" justifyContent="space-between" sx={{ mt: 0.5 }}>
                          <Typography variant="caption" color="text.secondary">
                            0%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Target: 15%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            50%
                          </Typography>
                        </Stack>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>

                {/* Investment Summary */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                      Investment Summary
                    </Typography>
                    <Stack spacing={2}>
                      {[
                        { label: 'Total Investment', value: results.totalCost },
                        { label: 'Cash Invested', value: results.cashInvested },
                        { label: 'Loan Amount', value: results.loanAmount },
                        { label: 'Down Payment', value: results.downPayment },
                        { label: 'Points Cost', value: results.pointsCost },
                        { label: 'Interest Cost', value: results.interestCost },
                        { label: 'Holding Costs', value: results.holdingCosts },
                        { label: 'Selling Costs', value: results.sellingCosts },
                      ].map((item) => (
                        <Stack
                          key={item.label}
                          direction="row"
                          justifyContent="space-between"
                          alignItems="center"
                          sx={{
                            pb: 2,
                            borderBottom: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}`,
                            '&:last-child': { borderBottom: 'none', pb: 0 },
                          }}
                        >
                          <Typography variant="body2" color="text.secondary">
                            {item.label}
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {formatCurrency(item.value)}
                          </Typography>
                        </Stack>
                      ))}
                    </Stack>
                  </CardContent>
                </Card>

                {/* Deal Analysis */}
                <Card
                  sx={{
                    border: `2px solid ${
                      results.roi >= 35
                        ? '#10b981'
                        : results.roi >= 25
                        ? '#3b82f6'
                        : results.roi >= 15
                        ? '#f59e0b'
                        : '#ef4444'
                    }`,
                    background: isDark
                      ? alpha(
                          results.roi >= 35
                            ? '#10b981'
                            : results.roi >= 25
                            ? '#3b82f6'
                            : results.roi >= 15
                            ? '#f59e0b'
                            : '#ef4444',
                          0.1
                        )
                      : alpha(
                          results.roi >= 35
                            ? '#10b981'
                            : results.roi >= 25
                            ? '#3b82f6'
                            : results.roi >= 15
                            ? '#f59e0b'
                            : '#ef4444',
                          0.05
                        ),
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} alignItems="flex-start">
                      <Box
                        sx={{
                          width: 48,
                          height: 48,
                          borderRadius: 2,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          background:
                            results.roi >= 35
                              ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                              : results.roi >= 25
                              ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                              : results.roi >= 15
                              ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                              : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                          color: 'white',
                        }}
                      >
                        {results.roi >= 15 ? (
                          <CheckCircleIcon sx={{ fontSize: 24 }} />
                        ) : (
                          <WarningIcon sx={{ fontSize: 24 }} />
                        )}
                      </Box>
                      <Box flex={1}>
                        <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                          Deal Analysis
                        </Typography>
                        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7, mb: 2 }}>
                          {results.roi >= 35 && (
                            <>
                              <strong>Excellent opportunity</strong> with {formatPercent(results.roi)} ROI. This significantly
                              exceeds typical fix & flip targets of 15-20%.
                            </>
                          )}
                          {results.roi >= 25 && results.roi < 35 && (
                            <>
                              <strong>Strong deal</strong> with {formatPercent(results.roi)} ROI. Well above industry standard
                              targets.
                            </>
                          )}
                          {results.roi >= 15 && results.roi < 25 && (
                            <>
                              <strong>Average deal</strong> with {formatPercent(results.roi)} ROI. Meets minimum investment
                              criteria but consider risk factors.
                            </>
                          )}
                          {results.roi < 15 && (
                            <>
                              <strong>Marginal returns</strong> with {formatPercent(results.roi)} ROI. Consider negotiating a
                              lower purchase price or passing on this opportunity.
                            </>
                          )}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Your maximum allowable offer is <strong>{formatCurrency(results.mao)}</strong> based on the {inputs.marketType.toLowerCase()} market {results.maoRatio * 100}% rule.
                        </Typography>
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>
              </Stack>
              )}
            </Grid>
          </Grid>
        </Box>
      )}

      {/* Analytics Tab */}
      {currentTab === 1 && (
        <Box sx={{ px: 4, pb: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Cost Breakdown
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={costBreakdownData}>
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke={isDark ? '#334155' : '#e2e8f0'}
                          opacity={0.2}
                          vertical={false}
                        />
                        <XAxis dataKey="name" tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} />
                        <YAxis tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => formatCurrency(value)}
                        />
                        <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                          {costBreakdownData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Investment vs Return
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={profitData}>
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke={isDark ? '#334155' : '#e2e8f0'}
                          opacity={0.2}
                          vertical={false}
                        />
                        <XAxis dataKey="name" tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} />
                        <YAxis tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => formatCurrency(value)}
                        />
                        <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                          {profitData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Project Timeline
                  </Typography>
                  <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={timelineData}>
                        <CartesianGrid
                          strokeDasharray="3 3"
                          stroke={isDark ? '#334155' : '#e2e8f0'}
                          opacity={0.2}
                          vertical={false}
                        />
                        <XAxis dataKey="phase" tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} />
                        <YAxis tick={{ fontSize: 12, fill: isDark ? '#94a3b8' : '#64748b' }} label={{ value: 'Months', angle: -90, position: 'insideLeft' }} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => `${value} months`}
                        />
                        <Bar dataKey="months" fill="#3b82f6" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}

      {/* Sensitivity Analysis Tab */}
      {currentTab === 2 && showResults && (
        <Box sx={{ px: 4, pb: 4 }}>
          <SensitivityAnalysisDashboard
            baseInputs={{
              annual_noi: results.grossProfit,
              total_cash_invested: results.cashInvested,
              property_value: inputs.arv,
            }}
            propertyType="fix_and_flip"
            metricType="cash_on_cash"
            metricName="Return on Investment (ROI)"
          />
        </Box>
      )}

      {currentTab === 2 && !showResults && (
        <Box sx={{ px: 4, py: 8, textAlign: 'center' }}>
          <Alert severity="info">
            Please run the calculator first to see sensitivity analysis results.
          </Alert>
        </Box>
      )}

      {/* Documentation Tab */}
      {currentTab === 3 && (
        <Box>
          <Tabs value={docTab} onChange={(e, v) => setDocTab(v)} sx={{ borderBottom: 1, borderColor: 'divider', px: 4, pt: 2 }}>
            <Tab label="Quick Reference" />
            <Tab label="Complete Summary" />
          </Tabs>
          <Box sx={{ p: 4 }}>
            {docTab === 0 && <MarkdownViewer content={FIX_AND_FLIP_QUICK_REFERENCE} />}
            {docTab === 1 && <MarkdownViewer content={FIX_AND_FLIP_COMPLETE_SUMMARY} />}
          </Box>
        </Box>
      )}
    </Box>
  );
};
