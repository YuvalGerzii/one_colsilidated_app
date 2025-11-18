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
  Paper,
  useTheme,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Divider,
} from '@mui/material';
import {
  Description as DescriptionIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as AttachMoneyIcon,
  Business as BusinessIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  PeopleAlt as PeopleAltIcon,
  EventNote as EventNoteIcon,
  LocalOffer as LocalOfferIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ComposedChart,
  Area,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { LeaseAnalyzerInputs, LeaseAnalyzerResults, LeaseAnalyzerProjection } from '../../types/calculatorTypes';
import {
  formatCurrency,
  formatPercent,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';

const DEFAULT_INPUTS: LeaseAnalyzerInputs = {
  projectName: 'Office Lease Analysis',
  location: 'Downtown District',
  analyst: '',
  propertyType: 'Office',
  totalSquareFootage: 50000,
  numTenants: 5,
  weightedAvgRentPsf: 28.50,
  totalAnnualRent: 1425000,
  vacancyRate: 10,
  operatingExpenseRatio: 35,
  annualRentGrowth: 2.5,
  weightedAvgLeaseTerm: 5.0,
  tenantImprovementPsf: 25.0,
  leasingCommissionPct: 5,
  leaseExpiryYear1: 15,
  leaseExpiryYear2: 20,
  leaseExpiryYear3: 25,
  leaseExpiryYear4: 20,
  leaseExpiryYear5: 20,
  renewalProbability: 70,
  marketRentPsf: 30.00,
  freeRentMonths: 2,
  capRate: 7,
  projectionYears: 10,
  tags: '',
  purpose: '',
  references: '',
  notes: '',
};

export const LeaseAnalyzerCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<LeaseAnalyzerInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<LeaseAnalyzerResults>({
    totalSf: 0,
    occupiedSf: 0,
    walt: 0,
    avgRentPsf: 0,
    marketRentPsf: 0,
    avgAnnualNoi: 0,
    avgAnnualCashFlow: 0,
    totalLeasingCosts: 0,
    stabilizedValue: 0,
    capRate: 0,
    projections: [],
  });

  const updateInput = <K extends keyof LeaseAnalyzerInputs>(
    key: K,
    value: LeaseAnalyzerInputs[K]
  ) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    if (!showResults) return;

    const years = inputs.projectionYears;
    const totalSf = inputs.totalSquareFootage;
    const baseRentPsf = inputs.weightedAvgRentPsf;
    const vacancy = inputs.vacancyRate / 100;
    const opexRatio = inputs.operatingExpenseRatio / 100;
    const rentGrowth = inputs.annualRentGrowth / 100;
    const tiPsf = inputs.tenantImprovementPsf;
    const commissionPct = inputs.leasingCommissionPct / 100;
    const marketRent = inputs.marketRentPsf;
    const renewalProb = inputs.renewalProbability / 100;
    const freeMonths = inputs.freeRentMonths;
    const capRate = inputs.capRate / 100;

    // Lease expiry schedule
    const expirySchedule = [
      inputs.leaseExpiryYear1 / 100,
      inputs.leaseExpiryYear2 / 100,
      inputs.leaseExpiryYear3 / 100,
      inputs.leaseExpiryYear4 / 100,
      inputs.leaseExpiryYear5 / 100,
    ];

    const projections: LeaseAnalyzerProjection[] = [];
    const occupiedSf = totalSf * (1 - vacancy);

    for (let year = 1; year <= years; year++) {
      // Calculate rent per SF for this year
      const currentRentPsf = baseRentPsf * Math.pow(1 + rentGrowth, year - 1);

      // Determine lease rollover
      const expiryIdx = Math.min(year - 1, expirySchedule.length - 1);
      const rolloverPct = year <= 5 ? expirySchedule[expiryIdx] : 0.20;
      const rolloverSf = occupiedSf * rolloverPct;

      // Calculate leasing costs
      const renewedSf = rolloverSf * renewalProb;
      const newTenantSf = rolloverSf * (1 - renewalProb);

      // TI and commissions
      const tiCost = newTenantSf * tiPsf;
      const commission = (renewedSf + newTenantSf) * marketRent * commissionPct;
      const totalLeasingCosts = tiCost + commission;

      // Calculate revenue
      const grossRent = occupiedSf * currentRentPsf;
      const freeRentLoss = (freeMonths / 12) * (newTenantSf * marketRent);
      const effectiveGrossIncome = grossRent - freeRentLoss;

      // Operating expenses
      const operatingExpenses = effectiveGrossIncome * opexRatio;

      // NOI
      const noi = effectiveGrossIncome - operatingExpenses;

      // Cash flow after leasing costs
      const cashFlow = noi - totalLeasingCosts;

      // Property value
      const propertyValue = capRate > 0 ? noi / capRate : 0;

      projections.push({
        year,
        occupiedSf,
        rolloverSf,
        renewedSf,
        newTenantSf,
        rentPsf: currentRentPsf,
        grossRent,
        freeRentLoss,
        effectiveGrossIncome,
        operatingExpenses,
        noi,
        tiCost,
        commission,
        totalLeasingCosts,
        cashFlow,
        propertyValue,
      });
    }

    // Calculate summary metrics
    const totalNoi = projections.reduce((sum, p) => sum + p.noi, 0);
    const avgNoi = totalNoi / projections.length;
    const totalLeasingCosts = projections.reduce((sum, p) => sum + p.totalLeasingCosts, 0);
    const avgCashFlow = projections.reduce((sum, p) => sum + p.cashFlow, 0) / projections.length;
    const stabilizedValue = capRate > 0 ? avgNoi / capRate : 0;

    setResults({
      totalSf,
      occupiedSf,
      walt: inputs.weightedAvgLeaseTerm,
      avgRentPsf: baseRentPsf,
      marketRentPsf: marketRent,
      avgAnnualNoi: avgNoi,
      avgAnnualCashFlow: avgCashFlow,
      totalLeasingCosts,
      stabilizedValue,
      capRate,
      projections,
    });
  }, [inputs, showResults]);

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    saveToLocalStorage('lease-analyzer', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });

    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  // Chart data
  const noiCashFlowData = results.projections.map((p) => ({
    year: `Year ${p.year}`,
    NOI: p.noi,
    'Cash Flow': p.cashFlow,
    'Leasing Costs': p.totalLeasingCosts,
  }));

  const rolloverData = results.projections.map((p) => ({
    year: `Year ${p.year}`,
    'Renewed Leases (SF)': p.renewedSf,
    'New Tenant Leases (SF)': p.newTenantSf,
  }));

  const leasingCostsData = results.projections.map((p) => ({
    year: `Year ${p.year}`,
    'TI Costs': p.tiCost,
    'Commissions': p.commission,
  }));

  const cardBgColor = isDark ? 'rgba(30, 30, 30, 0.7)' : 'rgba(255, 255, 255, 0.9)';

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: isDark ? '#121212' : '#f5f7fa', py: 4 }}>
      {/* Header */}
      <Box sx={{ px: 4, mb: 4 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
          <Stack direction="row" alignItems="center" spacing={2}>
            <BusinessIcon sx={{ fontSize: 40, color: 'primary.main' }} />
            <Typography variant="h4" fontWeight="bold">
              Lease Analyzer
            </Typography>
          </Stack>
          <Stack direction="row" spacing={2}>
            <Button
              variant="contained"
              startIcon={<PlayArrowIcon />}
              onClick={handleRunModel}
              size="large"
            >
              Run Analysis
            </Button>
            {showResults && (
              <Button
                variant="outlined"
                startIcon={<SaveIcon />}
                onClick={handleSave}
              >
                Save Report
              </Button>
            )}
          </Stack>
        </Stack>
        {saveMessage && (
          <Typography color="success.main" variant="body2">
            {saveMessage}
          </Typography>
        )}
      </Box>

      {/* Inputs */}
      <Box sx={{ px: 4, mb: 4 }}>
        <Grid container spacing={3}>
          {/* Property Profile */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <DescriptionIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Property Profile
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Property Name"
                    value={inputs.projectName}
                    onChange={(e) => updateInput('projectName', e.target.value)}
                    fullWidth
                    size="small"
                  />
                  <TextField
                    label="Location"
                    value={inputs.location}
                    onChange={(e) => updateInput('location', e.target.value)}
                    fullWidth
                    size="small"
                  />
                  <TextField
                    label="Analyst"
                    value={inputs.analyst}
                    onChange={(e) => updateInput('analyst', e.target.value)}
                    fullWidth
                    size="small"
                  />
                  <TextField
                    label="Property Type"
                    value={inputs.propertyType}
                    onChange={(e) => updateInput('propertyType', e.target.value)}
                    fullWidth
                    size="small"
                    helperText="e.g., Office, Retail, Industrial"
                  />
                  <TextField
                    type="number"
                    value={inputs.totalSquareFootage}
                    onChange={(e) => updateInput('totalSquareFootage', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Total Square Footage"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>SF</Typography>,
                    }}
                    inputProps={{ min: 5000, step: 1000 }}
                    error={inputs.totalSquareFootage < 5000}
                    helperText={inputs.totalSquareFootage < 5000 ? 'Minimum 5,000 SF' : `${(inputs.totalSquareFootage / 1000).toFixed(0)}K SF total`}
                  />
                  <TextField
                    type="number"
                    value={inputs.numTenants}
                    onChange={(e) => updateInput('numTenants', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Number of Tenants"
                    inputProps={{ min: 1, max: 100, step: 1 }}
                    error={inputs.numTenants < 1}
                    helperText={inputs.numTenants < 1 ? 'Minimum 1 tenant' : `Avg size: ${inputs.numTenants > 0 ? (inputs.totalSquareFootage / inputs.numTenants).toLocaleString(0) : 0} SF/tenant`}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Lease Economics */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AttachMoneyIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Lease Economics
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    value={inputs.weightedAvgRentPsf}
                    onChange={(e) => updateInput('weightedAvgRentPsf', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Weighted Avg Rent"
                    InputProps={{
                      startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/SF/year</Typography>,
                    }}
                    inputProps={{ min: 10, max: 100, step: 0.5 }}
                    error={inputs.weightedAvgRentPsf < 10 || inputs.weightedAvgRentPsf > 100}
                    helperText={inputs.weightedAvgRentPsf < 10 || inputs.weightedAvgRentPsf > 100 ? 'Range: $10-100/SF' : `Market average: $25-35/SF`}
                  />
                  <TextField
                    type="number"
                    value={inputs.totalAnnualRent}
                    onChange={(e) => updateInput('totalAnnualRent', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Total Annual Rent"
                    InputProps={{
                      startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                    }}
                    inputProps={{ min: 50000, step: 10000 }}
                    error={inputs.totalAnnualRent < 50000}
                    helperText={inputs.totalAnnualRent < 50000 ? 'Minimum $50,000' : `${(inputs.totalAnnualRent / 1000).toFixed(0)}K annual`}
                  />
                  <TextField
                    type="number"
                    value={inputs.vacancyRate}
                    onChange={(e) => updateInput('vacancyRate', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Vacancy Rate"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 30, step: 1 }}
                    error={inputs.vacancyRate < 0 || inputs.vacancyRate > 30}
                    helperText={inputs.vacancyRate < 0 || inputs.vacancyRate > 30 ? 'Range: 0-30%' : 'Typical: 5-10%'}
                  />
                  <TextField
                    type="number"
                    value={inputs.operatingExpenseRatio}
                    onChange={(e) => updateInput('operatingExpenseRatio', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Operating Expense Ratio"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 15, max: 60, step: 1 }}
                    error={inputs.operatingExpenseRatio < 15 || inputs.operatingExpenseRatio > 60}
                    helperText={inputs.operatingExpenseRatio < 15 || inputs.operatingExpenseRatio > 60 ? 'Range: 15-60%' : 'Office: 30-40%'}
                  />
                  <TextField
                    type="number"
                    value={inputs.annualRentGrowth}
                    onChange={(e) => updateInput('annualRentGrowth', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Annual Rent Growth"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%/year</Typography>,
                    }}
                    inputProps={{ min: 0, max: 10, step: 0.25 }}
                    error={inputs.annualRentGrowth < 0 || inputs.annualRentGrowth > 10}
                    helperText={inputs.annualRentGrowth < 0 || inputs.annualRentGrowth > 10 ? 'Range: 0-10%' : 'CPI + 0-3%'}
                  />
                  <TextField
                    type="number"
                    value={inputs.weightedAvgLeaseTerm}
                    onChange={(e) => updateInput('weightedAvgLeaseTerm', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Weighted Avg Lease Term (WALT)"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>years</Typography>,
                    }}
                    inputProps={{ min: 1, max: 20, step: 0.5 }}
                    error={inputs.weightedAvgLeaseTerm < 1 || inputs.weightedAvgLeaseTerm > 20}
                    helperText={inputs.weightedAvgLeaseTerm < 1 || inputs.weightedAvgLeaseTerm > 20 ? 'Range: 1-20 years' : 'Office typical: 3-7 years'}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Leasing Costs */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <LocalOfferIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Leasing Costs
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    value={inputs.tenantImprovementPsf}
                    onChange={(e) => updateInput('tenantImprovementPsf', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Tenant Improvements"
                    InputProps={{
                      startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/SF</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.tenantImprovementPsf < 0 || inputs.tenantImprovementPsf > 100}
                    helperText={inputs.tenantImprovementPsf < 0 || inputs.tenantImprovementPsf > 100 ? 'Range: $0-100/SF' : 'Office typical: $15-40/SF'}
                  />
                  <TextField
                    type="number"
                    value={inputs.leasingCommissionPct}
                    onChange={(e) => updateInput('leasingCommissionPct', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Leasing Commission"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 10, step: 0.5 }}
                    error={inputs.leasingCommissionPct < 0 || inputs.leasingCommissionPct > 10}
                    helperText={inputs.leasingCommissionPct < 0 || inputs.leasingCommissionPct > 10 ? 'Range: 0-10%' : 'Typical: 4-6% of rent'}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Lease Rollover Schedule */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <EventNoteIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Lease Rollover Schedule
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    value={inputs.leaseExpiryYear1}
                    onChange={(e) => updateInput('leaseExpiryYear1', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Lease Expiry Year 1"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.leaseExpiryYear1 < 0 || inputs.leaseExpiryYear1 > 100}
                    helperText={inputs.leaseExpiryYear1 < 0 || inputs.leaseExpiryYear1 > 100 ? 'Range: 0-100%' : '% of occupied SF expiring'}
                  />
                  <TextField
                    type="number"
                    value={inputs.leaseExpiryYear2}
                    onChange={(e) => updateInput('leaseExpiryYear2', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Lease Expiry Year 2"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.leaseExpiryYear2 < 0 || inputs.leaseExpiryYear2 > 100}
                    helperText={inputs.leaseExpiryYear2 < 0 || inputs.leaseExpiryYear2 > 100 ? 'Range: 0-100%' : '% of occupied SF expiring'}
                  />
                  <TextField
                    type="number"
                    value={inputs.leaseExpiryYear3}
                    onChange={(e) => updateInput('leaseExpiryYear3', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Lease Expiry Year 3"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.leaseExpiryYear3 < 0 || inputs.leaseExpiryYear3 > 100}
                    helperText={inputs.leaseExpiryYear3 < 0 || inputs.leaseExpiryYear3 > 100 ? 'Range: 0-100%' : '% of occupied SF expiring'}
                  />
                  <TextField
                    type="number"
                    value={inputs.leaseExpiryYear4}
                    onChange={(e) => updateInput('leaseExpiryYear4', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Lease Expiry Year 4"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.leaseExpiryYear4 < 0 || inputs.leaseExpiryYear4 > 100}
                    helperText={inputs.leaseExpiryYear4 < 0 || inputs.leaseExpiryYear4 > 100 ? 'Range: 0-100%' : '% of occupied SF expiring'}
                  />
                  <TextField
                    type="number"
                    value={inputs.leaseExpiryYear5}
                    onChange={(e) => updateInput('leaseExpiryYear5', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Lease Expiry Year 5"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 1 }}
                    error={inputs.leaseExpiryYear5 < 0 || inputs.leaseExpiryYear5 > 100}
                    helperText={inputs.leaseExpiryYear5 < 0 || inputs.leaseExpiryYear5 > 100 ? 'Range: 0-100%' : '% of occupied SF expiring'}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Market Assumptions */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <TrendingUpIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Market Assumptions
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    value={inputs.renewalProbability}
                    onChange={(e) => updateInput('renewalProbability', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Renewal Probability"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 0, max: 100, step: 5 }}
                    error={inputs.renewalProbability < 0 || inputs.renewalProbability > 100}
                    helperText={inputs.renewalProbability < 0 || inputs.renewalProbability > 100 ? 'Range: 0-100%' : 'Typical: 60-80%'}
                  />
                  <TextField
                    type="number"
                    value={inputs.marketRentPsf}
                    onChange={(e) => updateInput('marketRentPsf', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Market Rent"
                    InputProps={{
                      startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/SF/year</Typography>,
                    }}
                    inputProps={{ min: 10, max: 100, step: 0.5 }}
                    error={inputs.marketRentPsf < 10 || inputs.marketRentPsf > 100}
                    helperText={inputs.marketRentPsf < 10 || inputs.marketRentPsf > 100 ? 'Range: $10-100/SF' : 'For new tenant leases'}
                  />
                  <TextField
                    type="number"
                    value={inputs.freeRentMonths}
                    onChange={(e) => updateInput('freeRentMonths', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Free Rent Period"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>months</Typography>,
                    }}
                    inputProps={{ min: 0, max: 12, step: 1 }}
                    error={inputs.freeRentMonths < 0 || inputs.freeRentMonths > 12}
                    helperText={inputs.freeRentMonths < 0 || inputs.freeRentMonths > 12 ? 'Range: 0-12 months' : 'Concession for new tenants'}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Valuation */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AssessmentIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Valuation
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    type="number"
                    value={inputs.capRate}
                    onChange={(e) => updateInput('capRate', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Cap Rate"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                    }}
                    inputProps={{ min: 3, max: 12, step: 0.25 }}
                    error={inputs.capRate < 3 || inputs.capRate > 12}
                    helperText={inputs.capRate < 3 || inputs.capRate > 12 ? 'Range: 3-12%' : 'Office typical: 5-8%'}
                  />
                  <TextField
                    type="number"
                    value={inputs.projectionYears}
                    onChange={(e) => updateInput('projectionYears', Number(e.target.value))}
                    fullWidth
                    size="small"
                    label="Projection Period"
                    InputProps={{
                      endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>years</Typography>,
                    }}
                    inputProps={{ min: 5, max: 20, step: 1 }}
                    error={inputs.projectionYears < 5 || inputs.projectionYears > 20}
                    helperText={inputs.projectionYears < 5 || inputs.projectionYears > 20 ? 'Range: 5-20 years' : 'Standard: 10 years'}
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Results */}
      {showResults && (
        <Box sx={{ px: 4 }}>
          <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
            <Tabs
              value={currentTab}
              onChange={(_, val) => setCurrentTab(val)}
              sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
            >
              <Tab label="Summary" />
              <Tab label="Analytics" />
              <Tab label="Projections" />
              <Tab label="Documentation" />
            </Tabs>

            {/* Summary Tab */}
            {currentTab === 0 && (
              <Box sx={{ p: 4 }}>
                <Grid container spacing={3}>
                  {/* Key Metrics */}
                  <Grid item xs={12} md={6}>
                    <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                      <Typography variant="h6" fontWeight="bold" gutterBottom color="primary">
                        Key Metrics
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      <Stack spacing={1.5}>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Total Square Footage:</Typography>
                          <Typography fontWeight="bold">{results.totalSf.toLocaleString()} SF</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Occupied Square Footage:</Typography>
                          <Typography fontWeight="bold">{results.occupiedSf.toLocaleString()} SF</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">WALT (Weighted Avg Lease Term):</Typography>
                          <Typography fontWeight="bold">{results.walt.toFixed(1)} years</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Average Rent ($/SF):</Typography>
                          <Typography fontWeight="bold">${results.avgRentPsf.toFixed(2)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Market Rent ($/SF):</Typography>
                          <Typography fontWeight="bold">${results.marketRentPsf.toFixed(2)}</Typography>
                        </Box>
                      </Stack>
                    </Paper>
                  </Grid>

                  {/* Financial Summary */}
                  <Grid item xs={12} md={6}>
                    <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                      <Typography variant="h6" fontWeight="bold" gutterBottom color="primary">
                        Financial Summary
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      <Stack spacing={1.5}>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Average Annual NOI:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.avgAnnualNoi)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Average Annual Cash Flow:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.avgAnnualCashFlow)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Total Leasing Costs (All Years):</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.totalLeasingCosts)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Stabilized Property Value:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.stabilizedValue)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Cap Rate:</Typography>
                          <Typography fontWeight="bold">{formatPercent(results.capRate * 100)}</Typography>
                        </Box>
                      </Stack>
                    </Paper>
                  </Grid>
                </Grid>
              </Box>
            )}

            {/* Analytics Tab */}
            {currentTab === 1 && (
              <Box sx={{ p: 4 }}>
                <Stack spacing={4}>
                  {/* NOI vs Cash Flow Chart */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      NOI vs Cash Flow Over Time
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <ComposedChart data={noiCashFlowData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Bar dataKey="NOI" fill="#82ca9d" />
                        <Line type="monotone" dataKey="Cash Flow" stroke="#8884d8" strokeWidth={2} />
                        <Line type="monotone" dataKey="Leasing Costs" stroke="#ff7300" strokeWidth={2} strokeDasharray="5 5" />
                      </ComposedChart>
                    </ResponsiveContainer>
                  </Box>

                  {/* Lease Rollover Chart */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Lease Rollover Schedule
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={rolloverData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip formatter={(value: number) => `${value.toLocaleString()} SF`} />
                        <Legend />
                        <Bar dataKey="Renewed Leases (SF)" stackId="a" fill="#36a2eb" />
                        <Bar dataKey="New Tenant Leases (SF)" stackId="a" fill="#ffce56" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>

                  {/* Leasing Costs Chart */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Annual Leasing Costs
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={leasingCostsData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="year" />
                        <YAxis />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Bar dataKey="TI Costs" stackId="a" fill="#9966ff" />
                        <Bar dataKey="Commissions" stackId="a" fill="#ff9f40" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </Stack>
              </Box>
            )}

            {/* Projections Tab */}
            {currentTab === 2 && (
              <Box sx={{ p: 4 }}>
                <Typography variant="h6" fontWeight="bold" gutterBottom>
                  Year-by-Year Projections
                </Typography>
                <TableContainer component={Paper} elevation={0}>
                  <Table size="small">
                    <TableHead>
                      <TableRow sx={{ bgcolor: isDark ? 'rgba(40, 40, 40, 0.7)' : 'rgba(240, 240, 240, 0.9)' }}>
                        <TableCell><strong>Year</strong></TableCell>
                        <TableCell align="right"><strong>Rollover (SF)</strong></TableCell>
                        <TableCell align="right"><strong>Renewed (SF)</strong></TableCell>
                        <TableCell align="right"><strong>New Tenant (SF)</strong></TableCell>
                        <TableCell align="right"><strong>NOI</strong></TableCell>
                        <TableCell align="right"><strong>Leasing Costs</strong></TableCell>
                        <TableCell align="right"><strong>Cash Flow</strong></TableCell>
                        <TableCell align="right"><strong>Property Value</strong></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.projections.map((proj) => (
                        <TableRow key={proj.year} hover>
                          <TableCell>Year {proj.year}</TableCell>
                          <TableCell align="right">{proj.rolloverSf.toLocaleString()} SF</TableCell>
                          <TableCell align="right">{proj.renewedSf.toLocaleString()} SF</TableCell>
                          <TableCell align="right">{proj.newTenantSf.toLocaleString()} SF</TableCell>
                          <TableCell align="right">{formatCurrency(proj.noi)}</TableCell>
                          <TableCell align="right">{formatCurrency(proj.totalLeasingCosts)}</TableCell>
                          <TableCell align="right">{formatCurrency(proj.cashFlow)}</TableCell>
                          <TableCell align="right">{formatCurrency(proj.propertyValue)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            )}

            {/* Documentation Tab */}
            {currentTab === 3 && (
              <Box sx={{ p: 4 }}>
                <Typography variant="h6" fontWeight="bold" gutterBottom>
                  Model Documentation
                </Typography>
                <Stack spacing={3}>
                  <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Overview
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      The Lease Analyzer model projects future NOI and cash flows by modeling lease rollover,
                      tenant renewals, and associated leasing costs over time. It helps asset managers evaluate
                      the impact of lease expiration schedules and leasing assumptions on property performance.
                    </Typography>
                  </Paper>

                  <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Key Calculations
                    </Typography>
                    <Stack spacing={1}>
                      <Typography variant="body2"><strong>Lease Rollover:</strong> Percentage of leased space expiring each year</Typography>
                      <Typography variant="body2"><strong>Renewals:</strong> Rollover SF × Renewal Probability</Typography>
                      <Typography variant="body2"><strong>New Tenants:</strong> Rollover SF × (1 - Renewal Probability)</Typography>
                      <Typography variant="body2"><strong>TI Costs:</strong> New Tenant SF × TI $/SF</Typography>
                      <Typography variant="body2"><strong>Commissions:</strong> (Renewed + New Tenant SF) × Market Rent × Commission %</Typography>
                      <Typography variant="body2"><strong>Free Rent Loss:</strong> (Free Months / 12) × New Tenant SF × Market Rent</Typography>
                      <Typography variant="body2"><strong>Effective Gross Income:</strong> Gross Rent - Free Rent Loss</Typography>
                      <Typography variant="body2"><strong>Operating Expenses:</strong> EGI × OpEx Ratio</Typography>
                      <Typography variant="body2"><strong>NOI:</strong> EGI - Operating Expenses</Typography>
                      <Typography variant="body2"><strong>Cash Flow:</strong> NOI - Total Leasing Costs</Typography>
                      <Typography variant="body2"><strong>Property Value:</strong> NOI / Cap Rate</Typography>
                    </Stack>
                  </Paper>

                  <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Key Assumptions
                    </Typography>
                    <Stack spacing={1}>
                      <Typography variant="body2">• Lease expiry schedule represents % of occupied SF rolling over each year</Typography>
                      <Typography variant="body2">• After Year 5, assumes 20% annual rollover</Typography>
                      <Typography variant="body2">• Renewal probability applies to all expiring leases</Typography>
                      <Typography variant="body2">• TI costs only apply to new tenant leases (not renewals)</Typography>
                      <Typography variant="body2">• Commissions apply to both renewals and new leases</Typography>
                      <Typography variant="body2">• Free rent concessions only for new tenants</Typography>
                      <Typography variant="body2">• In-place rent grows at annual growth rate</Typography>
                      <Typography variant="body2">• Mark-to-market rent adjustments at market rent</Typography>
                    </Stack>
                  </Paper>
                </Stack>
              </Box>
            )}
          </Card>
        </Box>
      )}
    </Box>
  );
};
