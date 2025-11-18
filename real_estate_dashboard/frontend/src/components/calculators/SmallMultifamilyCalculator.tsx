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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  Divider,
} from '@mui/material';
import {
  Apartment as ApartmentIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as AttachMoneyIcon,
  Build as BuildIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  ShowChart as ShowChartIcon,
  AccountBalance as AccountBalanceIcon,
  CheckCircle as CheckCircleIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  Warning as WarningIcon,
  Star as StarIcon,
  Analytics as AnalyticsIcon,
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
  Area,
  AreaChart,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { SmallMultifamilyInputs, SmallMultifamilyResults, YearProjection } from '../../types/calculatorTypes';
import { MarkdownViewer } from '../common/MarkdownViewer';
import { EXTENDED_MULTIFAMILY_QUICK_REF } from '../../constants/documentation/extendedMultifamilyDocs';
import {
  formatCurrency,
  formatPercent,
  annuityPayment,
  remainingBalance,
  calculateIRR,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';
import { BreakEvenAnalysis } from './advanced/BreakEvenAnalysis';
import { calculateBreakEvenMetrics } from '../../utils/breakEvenCalculations';
import { SensitivityAnalysisDashboard } from '../sensitivity';

const DEFAULT_INPUTS: SmallMultifamilyInputs = {
  projectName: 'Oak Ridge Apartments',
  location: 'Denver, CO',
  analyst: '',
  propertyType: 'Value-Add', // Changed to match backend asset_class
  squareFootage: 0,
  bedrooms: 0,
  bathrooms: 0,
  yearBuilt: 0,
  purchasePrice: 3900000,
  closingCosts: 60000,
  renovationCosts: 300000,
  units: 24,
  currentRentPerUnit: 1800,
  targetRentPerUnit: 2200,
  vacancyRate: 5,
  otherIncomePerUnit: 150,
  otherIncomeGrowth: 2, // Added to match backend
  managementPct: 4, // Changed to match backend default (8 was too high)
  repairMaintenancePerUnit: 1200,
  utilitiesPerUnit: 1800,
  insuranceAnnual: 20000, // Added to match backend
  propertyTaxAnnual: 130000, // Added to match backend
  payrollPerUnit: 1000, // Added to match backend
  insurancePerUnit: 0,
  propertyTaxPerUnit: 0,
  otherExpensesPerUnit: 600,
  capexReservePerUnit: 500,
  rentGrowthRate: 3,
  expenseGrowthRate: 2.5,
  appreciationRate: 3,
  stabilizationMonths: 36,
  holdPeriodYears: 5,
  exitCapRate: 5.5, // Changed to match backend default
  loanLtv: 65,
  interestRate: 6,
  amortizationYears: 30,
  locationScore: 8,
  conditionScore: 7,
  financialScore: 6,
  rentUpsideScore: 8,
  dealStructureScore: 7,
};

export const SmallMultifamilyCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [docTab, setDocTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<SmallMultifamilyInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<SmallMultifamilyResults>({
    loanAmount: 0,
    downPayment: 0,
    equityInvested: 0,
    totalProjectCost: 0,
    stabilizedNoi: 0,
    stabilizedCashFlow: 0,
    year1CapRate: 0,
    year1CashOnCash: 0,
    year1Dscr: 0,
    exitValue: 0,
    netSaleProceeds: 0,
    irr: 0,
    equityMultiple: 0,
    totalScore: 0,
    projections: [],
  });

  const updateInput = <K extends keyof SmallMultifamilyInputs>(
    key: K,
    value: SmallMultifamilyInputs[K]
  ) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    if (!showResults) return;

    const loanAmount = inputs.purchasePrice * (inputs.loanLtv / 100);
    const downPayment = inputs.purchasePrice - loanAmount;
    const equityInvested = downPayment + inputs.closingCosts + inputs.renovationCosts;
    const totalProjectCost = inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts;
    const monthlyPayment = annuityPayment(loanAmount, inputs.interestRate / 100, inputs.amortizationYears);
    const annualDebtService = monthlyPayment * 12;

    const units = inputs.units;
    const vacancy = inputs.vacancyRate / 100;
    const rentGrowth = inputs.rentGrowthRate / 100;
    const otherIncomeGrowth = inputs.otherIncomeGrowth / 100; // Use input value directly
    const expenseGrowth = inputs.expenseGrowthRate / 100;
    const stabilizationYears = inputs.stabilizationMonths / 12;
    const holdYears = inputs.holdPeriodYears;

    // Use input values directly - no fallback to percentage-based calculations
    const propertyTaxAnnual = inputs.propertyTaxAnnual;
    const insuranceAnnual = inputs.insuranceAnnual;

    const projections: YearProjection[] = [];
    let cumulativeCashFlow = 0;

    for (let year = 1; year <= holdYears; year++) {
      let avgRent: number;

      // Stabilization logic
      if (year <= stabilizationYears) {
        const progress = year / stabilizationYears;
        avgRent = inputs.currentRentPerUnit + progress * (inputs.targetRentPerUnit - inputs.currentRentPerUnit);
      } else {
        avgRent = inputs.targetRentPerUnit * Math.pow(1 + rentGrowth, year - stabilizationYears);
      }

      const grossPotential = avgRent * 12 * units;
      const vacancyLoss = grossPotential * vacancy;
      const otherIncome = inputs.otherIncomePerUnit * 12 * units * Math.pow(1 + otherIncomeGrowth, year - 1);
      const effectiveGrossIncome = grossPotential - vacancyLoss + otherIncome;

      const propertyTax = propertyTaxAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const insurance = insuranceAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const utilities = inputs.utilitiesPerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
      const repairs = inputs.repairMaintenancePerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
      const payroll = inputs.payrollPerUnit * units * Math.pow(1 + expenseGrowth, year - 1); // Use input value directly
      const adminMisc = inputs.otherExpensesPerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
      const reserves = inputs.capexReservePerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
      const managementFee = effectiveGrossIncome * (inputs.managementPct / 100);

      const operatingExpenses = propertyTax + insurance + utilities + repairs + payroll + adminMisc + reserves + managementFee;

      const noi = effectiveGrossIncome - operatingExpenses;
      const cashFlow = noi - annualDebtService;

      cumulativeCashFlow += cashFlow;

      projections.push({
        year,
        grossRent: avgRent,
        vacancy: vacancyLoss,
        otherIncome,
        effectiveGrossIncome,
        operatingExpenses,
        noi,
        debtService: annualDebtService,
        cashFlow,
        loanBalance: 0,
        propertyValue: 0,
        equity: 0,
        cumulativeCashFlow,
      });
    }

    // Exit calculations
    const exitNoi = projections[holdYears - 1].noi;
    const exitValue = exitNoi / (inputs.exitCapRate / 100);
    const loanBalanceExit = remainingBalance(loanAmount, inputs.interestRate / 100, inputs.amortizationYears, holdYears * 12);
    const netSaleProceeds = exitValue - loanBalanceExit;

    // Calculate IRR
    const cashFlows = [-equityInvested];
    projections.forEach((proj, index) => {
      let cf = proj.cashFlow;
      if (index === projections.length - 1) {
        cf += netSaleProceeds;
      }
      cashFlows.push(cf);
    });

    const irrValue = calculateIRR(cashFlows);
    const equityMultiple = cashFlows.slice(1).reduce((sum, cf) => sum + cf, 0) / equityInvested;

    // Year 1 metrics
    const year1 = projections[0];
    const year1CapRate = year1.noi / inputs.purchasePrice;
    const year1CashOnCash = year1.cashFlow / equityInvested;
    const year1Dscr = year1.noi / annualDebtService;

    // Opportunity score
    const totalScore = (
      inputs.locationScore +
      inputs.conditionScore +
      inputs.financialScore +
      inputs.rentUpsideScore +
      inputs.dealStructureScore
    ) / 5;

    setResults({
      loanAmount,
      downPayment,
      equityInvested,
      totalProjectCost,
      stabilizedNoi: projections[Math.min(Math.floor(stabilizationYears), projections.length - 1)].noi,
      stabilizedCashFlow: projections[Math.min(Math.floor(stabilizationYears), projections.length - 1)].cashFlow,
      year1CapRate,
      year1CashOnCash,
      year1Dscr,
      exitValue,
      netSaleProceeds,
      irr: irrValue * 100,
      equityMultiple,
      totalScore,
      projections,
    });
  }, [inputs, showResults]);

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    saveToLocalStorage('small-multifamily', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });

    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  const performanceData = results.projections.map((p) => ({
    year: p.year,
    NOI: p.noi,
    'Cash Flow': p.cashFlow,
    'Debt Service': p.debtService,
  }));

  const incomeExpenseData = results.projections.map((p) => ({
    year: p.year,
    'Effective Gross Income': p.effectiveGrossIncome,
    'Operating Expenses': p.operatingExpenses,
  }));

  const opportunityScores = [
    { category: 'Location', score: inputs.locationScore },
    { category: 'Condition', score: inputs.conditionScore },
    { category: 'Financial', score: inputs.financialScore },
    { category: 'Rent Upside', score: inputs.rentUpsideScore },
    { category: 'Deal Structure', score: inputs.dealStructureScore },
  ];

  // Risk flags
  const riskFlags = [];
  if (results.year1CapRate < 0.05) riskFlags.push('Low entry cap rate');
  if (results.year1Dscr < 1.2) riskFlags.push('DSCR below 1.20x');
  if (results.projections.length > 0 && results.projections[0].cashFlow < 0) riskFlags.push('Negative year-one cash flow');

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
              <Box sx={{ width: 1, height: 24, bgcolor: isDark ? alpha('#94a3b8', 0.2) : alpha('#0f172a', 0.2) }} />
              <Box
                sx={{
                  width: 48,
                  height: 48,
                  borderRadius: 3,
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 16px rgba(139, 92, 246, 0.3)',
                }}
              >
                <ApartmentIcon sx={{ fontSize: 24, color: 'white' }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>
                  {inputs.projectName}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {inputs.location} • {inputs.units} Units
                </Typography>
              </Box>
            </Stack>
            <Stack direction="row" spacing={2}>
              {showResults && (
                <>
                  <Chip
                    label={`${results.totalScore.toFixed(1)}/10 Score`}
                    icon={<StarIcon sx={{ color: 'white !important' }} />}
                    sx={{
                      background: results.totalScore >= 8
                        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        : results.totalScore >= 6
                        ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        : 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                  <Chip
                    label={`${formatPercent(results.irr, 1)} IRR`}
                    sx={{
                      background: results.irr >= 18
                        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        : results.irr >= 15
                        ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        : results.irr >= 12
                        ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                        : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                      color: 'white',
                      fontWeight: 600,
                    }}
                  />
                </>
              )}
              {saveMessage && (
                <Chip
                  label={saveMessage}
                  icon={<CheckCircleIcon sx={{ color: 'white !important' }} />}
                  sx={{
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                />
              )}
              <Button
                variant="contained"
                startIcon={<PlayArrowIcon />}
                onClick={handleRunModel}
                sx={{
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
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
              ? `linear-gradient(135deg, ${alpha('#8b5cf6', 0.05)} 0%, ${alpha('#7c3aed', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#8b5cf6', 0.03)} 0%, ${alpha('#7c3aed', 0.03)} 100%)`,
            border: `1px solid ${alpha('#8b5cf6', 0.2)}`,
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
            Value-add multifamily analysis with rent stabilization, per-unit expense tracking, and institutional
            underwriting metrics. Includes opportunity scoring and risk assessment for informed investment decisions.
          </Typography>
        </Paper>
      </Box>

      {/* Tabs */}
      <Box sx={{ px: 4, mb: 4 }}>
        <Tabs value={currentTab} onChange={(e, v) => setCurrentTab(v)}>
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
            {/* Left Column - Inputs */}
            <Grid item xs={12} lg={7}>
              <Stack spacing={3}>
                {/* Property Overview */}
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
                        <ApartmentIcon sx={{ fontSize: 20, color: '#6366f1' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Property Overview
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Basic property information
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Property Name
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
                          Unit Count
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.units}
                          onChange={(e) => updateInput('units', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 4, step: 1 }}
                          error={inputs.units < 4}
                          helperText={inputs.units < 4 ? 'Minimum 4 units' : ''}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Acquisition & Capex */}
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
                          Acquisition & CapEx
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Purchase and renovation costs
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
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
                          inputProps={{ min: 500000, step: 10000 }}
                          error={inputs.purchasePrice < 500000}
                          helperText={inputs.purchasePrice < 500000 ? 'Minimum $500,000' : `$${(inputs.purchasePrice / 1000000).toFixed(2)}M`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Price per Unit
                        </Typography>
                        <TextField
                          type="number"
                          value={Math.round(inputs.purchasePrice / inputs.units)}
                          disabled
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          helperText="Calculated automatically"
                          sx={{ '& .MuiInputBase-input.Mui-disabled': { WebkitTextFillColor: 'text.primary' } }}
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
                          inputProps={{ min: 0, step: 1000 }}
                          helperText={`${((inputs.closingCosts / inputs.purchasePrice) * 100).toFixed(2)}% of purchase price`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Renovation Budget
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.renovationCosts}
                          onChange={(e) => updateInput('renovationCosts', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                          }}
                          inputProps={{ min: 0, step: 5000 }}
                          helperText={`$${Math.round(inputs.renovationCosts / inputs.units).toLocaleString()} per unit`}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Box sx={{ p: 2, bgcolor: alpha(isDark ? '#3b82f6' : '#3b82f6', 0.05), borderRadius: 1, border: `1px solid ${alpha('#3b82f6', 0.2)}` }}>
                          <Stack direction="row" justifyContent="space-between" alignItems="center">
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              Total Project Cost
                            </Typography>
                            <Typography variant="h6" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                              ${(inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts).toLocaleString()}
                            </Typography>
                          </Stack>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Revenue Assumptions */}
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
                        <TrendingUpIcon sx={{ fontSize: 20, color: '#10b981' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Revenue Assumptions
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Rent and income projections
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={3}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          In-Place Rent per Unit
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.currentRentPerUnit}
                          onChange={(e) => updateInput('currentRentPerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 400, step: 25 }}
                          error={inputs.currentRentPerUnit < 400}
                          helperText={inputs.currentRentPerUnit < 400 ? 'Minimum $400' : `$${(inputs.currentRentPerUnit * 12).toLocaleString()}/year`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Target Rent per Unit
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.targetRentPerUnit}
                          onChange={(e) => updateInput('targetRentPerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 400, step: 25 }}
                          error={inputs.targetRentPerUnit < 400}
                          helperText={inputs.targetRentPerUnit < 400 ? 'Minimum $400' : `+$${inputs.targetRentPerUnit - inputs.currentRentPerUnit}/mo (+${(((inputs.targetRentPerUnit - inputs.currentRentPerUnit) / inputs.currentRentPerUnit) * 100).toFixed(1)}%)`}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Box sx={{ p: 2, bgcolor: alpha('#10b981', 0.05), borderRadius: 1, border: `1px solid ${alpha('#10b981', 0.2)}` }}>
                          <Grid container spacing={2}>
                            <Grid item xs={6}>
                              <Typography variant="caption" color="text.secondary">Current Annual Gross</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600, color: '#10b981' }}>
                                ${(inputs.currentRentPerUnit * 12 * inputs.units).toLocaleString()}
                              </Typography>
                            </Grid>
                            <Grid item xs={6}>
                              <Typography variant="caption" color="text.secondary">Target Annual Gross</Typography>
                              <Typography variant="body1" sx={{ fontWeight: 600, color: '#10b981' }}>
                                ${(inputs.targetRentPerUnit * 12 * inputs.units).toLocaleString()}
                              </Typography>
                            </Grid>
                          </Grid>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Vacancy Rate
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.vacancyRate}
                          onChange={(e) => updateInput('vacancyRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 0, max: 30, step: 0.5 }}
                          error={inputs.vacancyRate < 0 || inputs.vacancyRate > 30}
                          helperText={inputs.vacancyRate < 0 || inputs.vacancyRate > 30 ? 'Range: 0-30%' : 'Market standard: 5-10%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Income per Unit
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherIncomePerUnit}
                          onChange={(e) => updateInput('otherIncomePerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 10 }}
                          helperText="Parking, laundry, pet fees, etc."
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Rent Growth Rate
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.rentGrowthRate}
                          onChange={(e) => updateInput('rentGrowthRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
                          error={inputs.rentGrowthRate < 0 || inputs.rentGrowthRate > 12}
                          helperText={inputs.rentGrowthRate < 0 || inputs.rentGrowthRate > 12 ? 'Range: 0-12%' : 'Typical: 2-4%'}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Operating Expenses */}
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
                        <BuildIcon sx={{ fontSize: 20, color: '#f59e0b' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Operating Expenses
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Annual operating costs
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Property Taxes (Annual $)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.propertyTaxAnnual}
                          onChange={(e) => updateInput('propertyTaxAnnual', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/year</Typography>,
                          }}
                          inputProps={{ min: 0, step: 1000 }}
                          helperText={inputs.totalUnits > 0 ? `$${(inputs.propertyTaxAnnual / inputs.totalUnits).toLocaleString()} per unit` : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Insurance (Annual $)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.insuranceAnnual}
                          onChange={(e) => updateInput('insuranceAnnual', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/year</Typography>,
                          }}
                          inputProps={{ min: 0, step: 1000 }}
                          helperText={inputs.totalUnits > 0 ? `$${(inputs.insuranceAnnual / inputs.totalUnits).toLocaleString()} per unit` : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Utilities / Unit ($/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.utilitiesPerUnit}
                          onChange={(e) => updateInput('utilitiesPerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 50 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Repairs / Unit ($/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.repairMaintenancePerUnit}
                          onChange={(e) => updateInput('repairMaintenancePerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 50 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Payroll / Unit ($/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.payrollPerUnit}
                          onChange={(e) => updateInput('payrollPerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 50 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Admin & Misc / Unit ($/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherExpensesPerUnit}
                          onChange={(e) => updateInput('otherExpensesPerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          CapEx Reserve / Unit ($/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.capexReservePerUnit}
                          onChange={(e) => updateInput('capexReservePerUnit', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Management Fee (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.managementPct}
                          onChange={(e) => updateInput('managementPct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 15, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Expense Growth (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.expenseGrowthRate}
                          onChange={(e) => updateInput('expenseGrowthRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Hold & Exit */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#8b5cf6', 0.2)} 0%, ${alpha('#7c3aed', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#8b5cf6', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <AssessmentIcon sx={{ fontSize: 20, color: '#8b5cf6' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Hold & Exit Strategy
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Investment timeline and exit assumptions
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Stabilization Period (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.stabilizationMonths / 12}
                          onChange={(e) => updateInput('stabilizationMonths', Number(e.target.value) * 12)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 1, max: 5, step: 1 }}
                          error={inputs.stabilizationMonths / 12 < 1 || inputs.stabilizationMonths / 12 > 5}
                          helperText={inputs.stabilizationMonths / 12 < 1 || inputs.stabilizationMonths / 12 > 5 ? 'Range: 1-5 years' : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Hold Period (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdPeriodYears}
                          onChange={(e) => updateInput('holdPeriodYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 3, max: 15, step: 1 }}
                          error={inputs.holdPeriodYears < 3 || inputs.holdPeriodYears > 15}
                          helperText={inputs.holdPeriodYears < 3 || inputs.holdPeriodYears > 15 ? 'Range: 3-15 years' : ''}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Exit Cap Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.exitCapRate}
                          onChange={(e) => updateInput('exitCapRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 3, max: 12, step: 0.25 }}
                          error={inputs.exitCapRate < 3 || inputs.exitCapRate > 12}
                          helperText={inputs.exitCapRate < 3 || inputs.exitCapRate > 12 ? 'Range: 3-12%' : ''}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Financing */}
                <Card>
                  <CardContent sx={{ p: 3 }}>
                    <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                      <Box
                        sx={{
                          width: 40,
                          height: 40,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${alpha('#ec4899', 0.2)} 0%, ${alpha('#db2777', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#ec4899', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <AccountBalanceIcon sx={{ fontSize: 20, color: '#ec4899' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Financing
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Loan terms and structure
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Loan-to-Value (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.loanLtv}
                          onChange={(e) => updateInput('loanLtv', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 40, max: 85, step: 1 }}
                          error={inputs.loanLtv < 40 || inputs.loanLtv > 85}
                          helperText={inputs.loanLtv < 40 || inputs.loanLtv > 85 ? 'Range: 40-85%' : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Interest Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.interestRate}
                          onChange={(e) => updateInput('interestRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 2, max: 15, step: 0.25 }}
                          error={inputs.interestRate < 2 || inputs.interestRate > 15}
                          helperText={inputs.interestRate < 2 || inputs.interestRate > 15 ? 'Range: 2-15%' : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Amortization (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.amortizationYears}
                          onChange={(e) => updateInput('amortizationYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 10, max: 40, step: 1 }}
                          error={inputs.amortizationYears < 10 || inputs.amortizationYears > 40}
                          helperText={inputs.amortizationYears < 10 || inputs.amortizationYears > 40 ? 'Range: 10-40 years' : ''}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Investment Thesis */}
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
                        <StarIcon sx={{ fontSize: 20, color: '#f59e0b' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Investment Thesis (1-10 Scale)
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Opportunity scoring criteria
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      {[
                        { key: 'locationScore' as const, label: 'Location Score' },
                        { key: 'conditionScore' as const, label: 'Condition Score' },
                        { key: 'financialScore' as const, label: 'Financial Score' },
                        { key: 'rentUpsideScore' as const, label: 'Rent Upside Score' },
                        { key: 'dealStructureScore' as const, label: 'Deal Structure Score' },
                      ].map((item) => (
                        <Grid item xs={12} sm={6} md={4} key={item.key}>
                          <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                            {item.label}
                          </Typography>
                          <TextField
                            type="number"
                            value={inputs[item.key]}
                            onChange={(e) => updateInput(item.key, Number(e.target.value))}
                            fullWidth
                            size="small"
                            inputProps={{ min: 1, max: 10, step: 1 }}
                          />
                        </Grid>
                      ))}
                    </Grid>
                  </CardContent>
                </Card>
              </Stack>
            </Grid>

            {/* Right Column - Results */}
            <Grid item xs={12} lg={5}>
              {!showResults ? (
                <Card
                  sx={{
                    p: 6,
                    textAlign: 'center',
                    background: isDark
                      ? `linear-gradient(135deg, ${alpha('#8b5cf6', 0.1)} 0%, ${alpha('#7c3aed', 0.1)} 100%)`
                      : `linear-gradient(135deg, ${alpha('#8b5cf6', 0.05)} 0%, ${alpha('#7c3aed', 0.05)} 100%)`,
                    border: `2px dashed ${alpha('#8b5cf6', 0.3)}`,
                  }}
                >
                  <Box
                    sx={{
                      width: 72,
                      height: 72,
                      borderRadius: '50%',
                      background: `linear-gradient(135deg, ${alpha('#8b5cf6', 0.2)} 0%, ${alpha('#7c3aed', 0.2)} 100%)`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 3,
                    }}
                  >
                    <PlayArrowIcon sx={{ fontSize: 36, color: '#8b5cf6' }} />
                  </Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Ready to Analyze
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                    Enter your multifamily property details and assumptions, then click "Run Model" to see
                    projections, opportunity scores, and exit analysis.
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PlayArrowIcon />}
                    onClick={handleRunModel}
                    sx={{
                      background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
                      },
                    }}
                  >
                    Run Model
                  </Button>
                </Card>
              ) : (
                <Stack spacing={3}>
                  {/* Risk Flags */}
                  {riskFlags.length > 0 && (
                    <Alert severity="warning" icon={<WarningIcon />}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                        Risk Flags
                      </Typography>
                      <Stack spacing={0.5}>
                        {riskFlags.map((flag, index) => (
                          <Typography key={index} variant="caption">
                            • {flag}
                          </Typography>
                        ))}
                      </Stack>
                    </Alert>
                  )}

                  {/* Opportunity Score */}
                  <Card sx={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)', color: 'white' }}>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        Opportunity Score
                      </Typography>
                      <Typography variant="h2" sx={{ fontWeight: 700, mb: 1 }}>
                        {results.totalScore.toFixed(1)}/10
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
                        {results.totalScore >= 8
                          ? 'Excellent opportunity'
                          : results.totalScore >= 6
                          ? 'Good opportunity'
                          : 'Fair opportunity'}
                      </Typography>
                    </CardContent>
                  </Card>

                  {/* Year 1 Metrics */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        Year 1 Metrics
                      </Typography>
                      <Grid container spacing={2}>
                        {[
                          { label: 'Cap Rate', value: formatPercent(results.year1CapRate * 100, 2) },
                          { label: 'Cash-on-Cash', value: formatPercent(results.year1CashOnCash * 100, 2) },
                          { label: 'DSCR', value: `${results.year1Dscr.toFixed(2)}x` },
                          { label: 'Year 1 NOI', value: formatCurrency(results.projections[0]?.noi || 0) },
                        ].map((item) => (
                          <Grid item xs={6} key={item.label}>
                            <Typography variant="caption" color="text.secondary">
                              {item.label}
                            </Typography>
                            <Typography variant="h6" sx={{ fontWeight: 700 }}>
                              {item.value}
                            </Typography>
                          </Grid>
                        ))}
                      </Grid>
                    </CardContent>
                  </Card>

                  {/* Acquisition Summary */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        Acquisition Summary
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Purchase Price', value: inputs.purchasePrice },
                          { label: 'All-In Cost', value: results.totalProjectCost },
                          { label: 'Loan Amount', value: results.loanAmount },
                          { label: 'Equity Invested', value: results.equityInvested },
                        ].map((item) => (
                          <Stack
                            key={item.label}
                            direction="row"
                            justifyContent="space-between"
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

                  {/* Exit Summary */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        {inputs.holdPeriodYears}-Year Exit
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Exit Value', value: formatCurrency(results.exitValue) },
                          { label: 'Net Sale Proceeds', value: formatCurrency(results.netSaleProceeds) },
                          { label: 'Project IRR', value: formatPercent(results.irr, 1) },
                          { label: 'Equity Multiple', value: `${results.equityMultiple.toFixed(2)}x` },
                        ].map((item) => (
                          <Stack
                            key={item.label}
                            direction="row"
                            justifyContent="space-between"
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
                              {item.value}
                            </Typography>
                          </Stack>
                        ))}
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
          <Stack spacing={4}>
            {/* Break-Even Analysis */}
            {results && (() => {
              const calculateResultsForBreakEven = (testInputs: SmallMultifamilyInputs) => {
                // Calculate financials for break-even testing
                const loanAmount = testInputs.purchasePrice * (testInputs.loanLtv / 100);
                const downPayment = testInputs.purchasePrice - loanAmount;
                const equityInvested = downPayment + testInputs.closingCosts + testInputs.renovationCosts;
                const monthlyPayment = annuityPayment(loanAmount, testInputs.interestRate / 100, testInputs.amortizationYears);
                const annualDebtService = monthlyPayment * 12;

                const units = testInputs.units;
                const vacancy = testInputs.vacancyRate / 100;
                const rentGrowth = testInputs.rentGrowthRate / 100;
                const otherIncomeGrowth = 0.02;
                const expenseGrowth = testInputs.expenseGrowthRate / 100;
                const stabilizationYears = testInputs.stabilizationMonths / 12;
                const holdYears = testInputs.holdPeriodYears;

                const propertyTaxAnnual = testInputs.propertyTaxPerUnit > 0
                  ? testInputs.propertyTaxPerUnit * units
                  : (testInputs.purchasePrice * 0.0125);
                const insuranceAnnual = testInputs.insurancePerUnit > 0
                  ? testInputs.insurancePerUnit * units
                  : (testInputs.purchasePrice * 0.003);

                const projections: YearProjection[] = [];
                let cumulativeCashFlow = 0;

                for (let year = 1; year <= holdYears; year++) {
                  let avgRent: number;
                  if (year <= stabilizationYears) {
                    const progress = year / stabilizationYears;
                    avgRent = testInputs.currentRentPerUnit + progress * (testInputs.targetRentPerUnit - testInputs.currentRentPerUnit);
                  } else {
                    avgRent = testInputs.targetRentPerUnit * Math.pow(1 + rentGrowth, year - stabilizationYears);
                  }

                  const grossPotential = avgRent * 12 * units;
                  const vacancyLoss = grossPotential * vacancy;
                  const otherIncome = testInputs.otherIncomePerUnit * 12 * units * Math.pow(1 + otherIncomeGrowth, year - 1);
                  const effectiveGrossIncome = grossPotential - vacancyLoss + otherIncome;

                  const propertyTax = propertyTaxAnnual * Math.pow(1 + expenseGrowth, year - 1);
                  const insurance = insuranceAnnual * Math.pow(1 + expenseGrowth, year - 1);
                  const utilities = testInputs.utilitiesPerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
                  const repairs = testInputs.repairMaintenancePerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
                  const payroll = 1000 * units * Math.pow(1 + expenseGrowth, year - 1);
                  const adminMisc = testInputs.otherExpensesPerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
                  const reserves = testInputs.capexReservePerUnit * units * Math.pow(1 + expenseGrowth, year - 1);
                  const managementFee = effectiveGrossIncome * (testInputs.managementPct / 100);

                  const operatingExpenses = propertyTax + insurance + utilities + repairs + payroll + adminMisc + reserves + managementFee;
                  const noi = effectiveGrossIncome - operatingExpenses;
                  const cashFlow = noi - annualDebtService;
                  cumulativeCashFlow += cashFlow;

                  projections.push({
                    year,
                    grossRent: avgRent,
                    vacancy: vacancyLoss,
                    otherIncome,
                    effectiveGrossIncome,
                    operatingExpenses,
                    noi,
                    debtService: annualDebtService,
                    cashFlow,
                    loanBalance: 0,
                    propertyValue: 0,
                    equity: 0,
                    cumulativeCashFlow,
                  });
                }

                // IRR calculation
                const exitNoi = projections[holdYears - 1].noi;
                const exitValue = exitNoi / (testInputs.exitCapRate / 100);
                const loanBalanceExit = remainingBalance(loanAmount, testInputs.interestRate / 100, testInputs.amortizationYears, holdYears * 12);
                const netSaleProceeds = exitValue - loanBalanceExit;

                const cashFlows = [-equityInvested];
                projections.forEach((proj, index) => {
                  let cf = proj.cashFlow;
                  if (index === projections.length - 1) {
                    cf += netSaleProceeds;
                  }
                  cashFlows.push(cf);
                });

                const irr = calculateIRR(cashFlows);
                const noi = projections[0].noi;
                const debtService = annualDebtService;

                return { noi, debtService, irr, projections };
              };

              const breakEvenMetrics = calculateBreakEvenMetrics(
                inputs,
                results,
                calculateResultsForBreakEven,
                0.15 // 15% target IRR
              );

              return <BreakEvenAnalysis metrics={breakEvenMetrics} />;
            })()}

            <Divider sx={{ my: 4 }} />

            {/* Existing Charts */}
            <Grid container spacing={3}>
              {/* Performance Chart */}
              <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    NOI, Cash Flow, and Debt Service
                  </Typography>
                  <Box sx={{ height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={performanceData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => formatCurrency(value)}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="NOI" stroke="#10b981" strokeWidth={2} />
                        <Line type="monotone" dataKey="Cash Flow" stroke="#3b82f6" strokeWidth={2} />
                        <Line type="monotone" dataKey="Debt Service" stroke="#ef4444" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Income vs Expenses */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Income vs Expenses
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={incomeExpenseData}>
                        <defs>
                          <linearGradient id="colorIncome" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="colorExpense" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => formatCurrency(value)}
                        />
                        <Legend />
                        <Area
                          type="monotone"
                          dataKey="Effective Gross Income"
                          stroke="#10b981"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorIncome)"
                        />
                        <Area
                          type="monotone"
                          dataKey="Operating Expenses"
                          stroke="#ef4444"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorExpense)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Opportunity Scores */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Opportunity Score Breakdown
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={opportunityScores}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                        <XAxis dataKey="category" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <YAxis domain={[0, 10]} stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                        />
                        <Bar dataKey="score" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Projection Table */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    {inputs.holdPeriodYears}-Year Projection
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Year</TableCell>
                          <TableCell align="right">Avg Rent</TableCell>
                          <TableCell align="right">Vacancy</TableCell>
                          <TableCell align="right">EGI</TableCell>
                          <TableCell align="right">Op. Exp.</TableCell>
                          <TableCell align="right">NOI</TableCell>
                          <TableCell align="right">Debt Service</TableCell>
                          <TableCell align="right">Cash Flow</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {results.projections.map((proj) => (
                          <TableRow key={proj.year}>
                            <TableCell>{proj.year}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.grossRent)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.vacancy)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.effectiveGrossIncome)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.operatingExpenses)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.noi)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.debtService)}</TableCell>
                            <TableCell align="right" sx={{ fontWeight: 600 }}>
                              {formatCurrency(proj.cashFlow)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            </Grid>
          </Stack>
        </Box>
      )}

      {/* Sensitivity Analysis Tab */}
      {currentTab === 2 && showResults && (
        <Box sx={{ px: 4, pb: 4 }}>
          <SensitivityAnalysisDashboard
            baseInputs={{
              annual_noi: results.stabilizedNoi,
              total_cash_invested: results.equityInvested,
              property_value: inputs.purchasePrice + inputs.renovationCosts,
            }}
            propertyType="multifamily"
            metricType="cash_on_cash"
            metricName="Cash on Cash Return"
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
          </Tabs>
          <Box sx={{ p: 4 }}>
            {docTab === 0 && <MarkdownViewer content={EXTENDED_MULTIFAMILY_QUICK_REF} />}
          </Box>
        </Box>
      )}
    </Box>
  );
};
