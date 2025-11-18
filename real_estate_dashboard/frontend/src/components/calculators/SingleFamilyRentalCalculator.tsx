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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  HomeWork as HomeWorkIcon,
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
import { useUIMode } from '../../contexts/UIModeContext';
import { SingleFamilyRentalCalculatorNew } from './SingleFamilyRentalCalculatorNew';
import { SingleFamilyRentalInputs, SingleFamilyRentalResults, YearProjection } from '../../types/calculatorTypes';
import {
  formatCurrency,
  formatPercent,
  annuityPayment,
  remainingBalance,
  calculateIRR,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';
import { SensitivityAnalysisDashboard } from '../sensitivity';
import { Alert } from '@mui/material';

const DEFAULT_INPUTS: SingleFamilyRentalInputs = {
  // Property Profile
  projectName: 'Maple Street Rental',
  location: 'Charlotte, NC',
  analyst: '',
  propertyType: 'Single-Family Residence',
  squareFootage: 1600,
  bedrooms: 3,
  bathrooms: 2,
  yearBuilt: 1990,

  // Acquisition & Rehab
  purchasePrice: 280000,
  closingCosts: 5000,
  renovationCosts: 30000,
  arv: 340000,
  holdingCostsMonthly: 600,
  holdingPeriodMonths: 6,

  // Income & Growth
  monthlyRent: 2200,
  otherIncomeMonthly: 0,
  rentGrowthRate: 3,
  vacancyRate: 8,
  appreciationRate: 3,

  // Operating Expenses
  managementPct: 8,
  maintenancePct: 8,
  propertyTaxAnnual: 3500,
  insuranceAnnual: 1500,
  utilitiesMonthly: 150,
  hoaMonthly: 0,
  otherExpensesMonthly: 50,
  capexReserveMonthly: 200,
  expenseGrowthRate: 2.5,

  // Financing & Disposition
  downPaymentPct: 25,
  interestRate: 6.5,
  loanTermYears: 30,
  refinanceLtv: 75,
  refinanceRate: 6,
  refinanceTermYears: 30,
  refinanceYear: 0,
  refinanceCostPct: 3,
  sellingCostPct: 7,

  // Holding Strategy
  holdPeriodYears: 10,
};

export const SingleFamilyRentalCalculator: React.FC = () => {
  const { uiMode } = useUIMode();

  // If New UI is selected, use the new calculator
  if (uiMode === 'new') {
    return <SingleFamilyRentalCalculatorNew />;
  }

  // Otherwise, use the old calculator
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<SingleFamilyRentalInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<SingleFamilyRentalResults>({
    loanAmount: 0,
    downPayment: 0,
    equityInvested: 0,
    totalProjectCost: 0,
    annualDebtService: 0,
    year1GrossRent: 0,
    year1Vacancy: 0,
    year1EffectiveIncome: 0,
    year1OperatingExpenses: 0,
    year1Noi: 0,
    year1CashFlow: 0,
    capRate: 0,
    cashOnCash: 0,
    dscr: 0,
    onePercentRule: 0,
    exitValue: 0,
    netSaleProceeds: 0,
    loanBalanceExit: 0,
    irr: 0,
    equityMultiple: 0,
    cashOutRefi: 0,
    flipGrossProfit: 0,
    flipRoi: 0,
    flipProfitMargin: 0,
    brrrCashOut: 0,
    brrrYear2CashFlow: 0,
    holdYear10CashFlow: 0,
    holdMonthlyCashFlow: 0,
    projections: [],
    cashFlows: [],
    cumulativeCashFlows: [],
  });

  const updateInput = <K extends keyof SingleFamilyRentalInputs>(
    key: K,
    value: SingleFamilyRentalInputs[K]
  ) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    if (!showResults) return;

    // Calculate derived finance fields
    const downPayment = inputs.purchasePrice * (inputs.downPaymentPct / 100);
    const loanAmount = inputs.purchasePrice - downPayment;
    const equityInvested = downPayment + inputs.closingCosts + inputs.renovationCosts;
    const totalProjectCost = inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts;
    const monthlyPayment = annuityPayment(loanAmount, inputs.interestRate / 100, inputs.loanTermYears);
    const annualDebtService = monthlyPayment * 12;

    // Build 10-year projections
    const years = 10;
    const rentGrowth = inputs.rentGrowthRate / 100;
    const expenseGrowth = inputs.expenseGrowthRate / 100;
    const appreciation = inputs.appreciationRate / 100;
    const refinanceYear = inputs.refinanceYear;
    const performRefi = inputs.refinanceLtv > 0 && refinanceYear > 0;

    const projections: YearProjection[] = [];
    const cashFlows: number[] = [-equityInvested];
    let cashOutRefi = 0;

    let currentPrincipal = loanAmount;
    let currentRate = inputs.interestRate / 100;
    let currentTerm = inputs.loanTermYears;
    let paymentsMade = 0;
    let refiExecuted = false;

    const debtServices: number[] = [];
    const loanBalances: number[] = [];

    // Calculate debt service and loan balances for each year
    for (let year = 1; year <= years; year++) {
      const annualPayment = annuityPayment(currentPrincipal, currentRate, currentTerm) * 12;
      debtServices.push(annualPayment);
      paymentsMade += 12;
      let balanceEnd = remainingBalance(currentPrincipal, currentRate, currentTerm, paymentsMade);

      // Handle refinance
      if (performRefi && !refiExecuted && year === refinanceYear) {
        const propertyValue = inputs.arv * Math.pow(1 + appreciation, year);
        const newPrincipal = propertyValue * (inputs.refinanceLtv / 100);
        const refinanceCosts = newPrincipal * (inputs.refinanceCostPct / 100);
        cashOutRefi = newPrincipal - balanceEnd - refinanceCosts;
        currentPrincipal = newPrincipal;
        currentRate = inputs.refinanceRate / 100;
        currentTerm = inputs.refinanceTermYears;
        paymentsMade = 0;
        refiExecuted = true;
        balanceEnd = currentPrincipal;
      }

      loanBalances.push(balanceEnd);
    }

    let cumulativeCashFlow = 0;

    for (let year = 1; year <= years; year++) {
      const rentAnnual = inputs.monthlyRent * Math.pow(1 + rentGrowth, year - 1) * 12;
      const otherIncome = inputs.otherIncomeMonthly * Math.pow(1 + rentGrowth, year - 1) * 12;
      const vacancyLoss = rentAnnual * (inputs.vacancyRate / 100);
      const effectiveGrossIncome = rentAnnual - vacancyLoss + otherIncome;

      const mgmtExpense = rentAnnual * (inputs.managementPct / 100);
      const maintenanceExpense = rentAnnual * (inputs.maintenancePct / 100);
      const propertyTaxAnnual = inputs.propertyTaxAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const insuranceAnnual = inputs.insuranceAnnual * Math.pow(1 + expenseGrowth, year - 1);
      const utilities = inputs.utilitiesMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const hoa = inputs.hoaMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const otherExpense = inputs.otherExpensesMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;
      const capex = inputs.capexReserveMonthly * Math.pow(1 + expenseGrowth, year - 1) * 12;

      const operatingExpenses =
        mgmtExpense +
        maintenanceExpense +
        propertyTaxAnnual +
        insuranceAnnual +
        utilities +
        hoa +
        otherExpense +
        capex;

      const noi = effectiveGrossIncome - operatingExpenses;
      const debtService = debtServices[year - 1];

      let annualCashFlow = noi - debtService;
      if (performRefi && year === refinanceYear) {
        annualCashFlow += cashOutRefi;
      }

      const propertyValue = inputs.arv * Math.pow(1 + appreciation, year);
      const loanBalance = loanBalances[year - 1];
      const equity = propertyValue - loanBalance;

      cumulativeCashFlow += annualCashFlow;

      projections.push({
        year,
        grossRent: rentAnnual,
        vacancy: vacancyLoss,
        otherIncome,
        effectiveGrossIncome,
        operatingExpenses,
        noi,
        debtService,
        cashFlow: annualCashFlow,
        loanBalance,
        propertyValue,
        equity,
        cumulativeCashFlow,
      });

      cashFlows.push(annualCashFlow);
    }

    // Exit calculations
    const holdYears = inputs.holdPeriodYears;
    const exitValue = inputs.arv * Math.pow(1 + appreciation, holdYears);
    const sellingCosts = exitValue * (inputs.sellingCostPct / 100);
    const loanBalanceExit = loanBalances[holdYears - 1];
    const netSaleProceeds = exitValue - sellingCosts - loanBalanceExit;

    // Add net sale proceeds to final cash flow for IRR calculation
    const cashFlowsWithExit = [...cashFlows];
    cashFlowsWithExit[holdYears] += netSaleProceeds;

    const irrValue = calculateIRR(cashFlowsWithExit);
    const equityMultiple = cashFlowsWithExit.slice(1).reduce((sum, cf) => sum + cf, 0) / equityInvested;

    // Year 1 metrics
    const year1 = projections[0];
    const capRate = year1.noi / totalProjectCost;
    const cashOnCash = year1.cashFlow / equityInvested;
    const dscr = year1.noi / annualDebtService;
    const onePercentRule = (inputs.monthlyRent / inputs.purchasePrice) * 100;

    // Exit strategy comparison
    const holdingCosts = inputs.holdingCostsMonthly * inputs.holdingPeriodMonths;
    const allInCost = inputs.purchasePrice + inputs.closingCosts + inputs.renovationCosts + holdingCosts;
    const sellingCostsFlip = inputs.arv * (inputs.sellingCostPct / 100);
    const flipGrossProfit = inputs.arv - sellingCostsFlip - allInCost;
    const flipRoi = (flipGrossProfit / equityInvested) * 100;
    const flipProfitMargin = (flipGrossProfit / inputs.arv) * 100;

    const brrrCashOut = cashOutRefi;
    const brrrYear2CashFlow = projections[Math.min(1, projections.length - 1)].cashFlow;

    const holdYear10CashFlow = projections[projections.length - 1].cashFlow;
    const holdMonthlyCashFlow = holdYear10CashFlow / 12;

    const cumulativeCashFlows = projections.map((p) => p.cumulativeCashFlow);

    setResults({
      loanAmount,
      downPayment,
      equityInvested,
      totalProjectCost,
      annualDebtService,
      year1GrossRent: year1.grossRent,
      year1Vacancy: year1.vacancy,
      year1EffectiveIncome: year1.effectiveGrossIncome,
      year1OperatingExpenses: year1.operatingExpenses,
      year1Noi: year1.noi,
      year1CashFlow: year1.cashFlow,
      capRate,
      cashOnCash,
      dscr,
      onePercentRule,
      exitValue,
      netSaleProceeds,
      loanBalanceExit,
      irr: irrValue * 100,
      equityMultiple,
      cashOutRefi,
      flipGrossProfit,
      flipRoi,
      flipProfitMargin,
      brrrCashOut,
      brrrYear2CashFlow,
      holdYear10CashFlow,
      holdMonthlyCashFlow,
      projections,
      cashFlows: cashFlowsWithExit,
      cumulativeCashFlows,
    });
  }, [inputs, showResults]);

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    saveToLocalStorage('single-family-rental', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });

    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  const cashFlowData = results.projections.map((p) => ({
    year: p.year,
    NOI: p.noi,
    'Debt Service': p.debtService,
    'Cash Flow': p.cashFlow,
  }));

  const equityData = results.projections.map((p) => ({
    year: p.year,
    'Property Value': p.propertyValue,
    Equity: p.equity,
    'Loan Balance': p.loanBalance,
  }));

  const exitComparisonData = [
    { strategy: 'Flip', value: results.flipGrossProfit },
    { strategy: 'BRRRR', value: results.brrrCashOut },
    { strategy: 'Hold', value: results.netSaleProceeds },
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
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 4px 16px rgba(16, 185, 129, 0.3)',
                }}
              >
                <HomeWorkIcon sx={{ fontSize: 24, color: 'white' }} />
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
                  label={`${formatPercent(results.irr, 1)} IRR`}
                  sx={{
                    background:
                      results.irr >= 20
                        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        : results.irr >= 15
                        ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        : results.irr >= 10
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
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
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
              ? `linear-gradient(135deg, ${alpha('#10b981', 0.05)} 0%, ${alpha('#059669', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#10b981', 0.03)} 0%, ${alpha('#059669', 0.03)} 100%)`,
            border: `1px solid ${alpha('#10b981', 0.2)}`,
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
            Comprehensive rental property analysis with 10-year cash flow projections, multiple exit
            strategies (Flip, BRRRR, Hold), and refinancing scenarios. Includes detailed operating
            expense tracking and institutional-grade metrics.
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
                        <HomeWorkIcon sx={{ fontSize: 20, color: '#6366f1' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Property Profile
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Property details and characteristics
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
                      <Grid item xs={12} sm={6}>
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
                      <Grid item xs={12} sm={6}>
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
                    </Grid>
                  </CardContent>
                </Card>

                {/* Acquisition & Rehab */}
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
                          Acquisition & Rehab
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Purchase details and renovation costs
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
                          inputProps={{ min: 50000, step: 1000 }}
                          error={inputs.purchasePrice < 50000}
                          helperText={inputs.purchasePrice < 50000 ? 'Minimum $50,000' : `$${(inputs.purchasePrice / 1000).toFixed(0)}K`}
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
                          inputProps={{ min: 0, step: 500 }}
                          helperText={`Typical: $15-50 per sqft`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          After Repair Value
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
                          helperText={inputs.arv < 50000 ? 'Minimum $50,000' : inputs.purchasePrice > 0 ? `+${(((inputs.arv - inputs.purchasePrice) / inputs.purchasePrice) * 100).toFixed(1)}% appreciation` : ''}
                        />
                      </Grid>
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
                          helperText="During renovation period"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Holding Period (Months)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdingPeriodMonths}
                          onChange={(e) => updateInput('holdingPeriodMonths', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 1, step: 1 }}
                          error={inputs.holdingPeriodMonths < 1}
                          helperText={inputs.holdingPeriodMonths < 1 ? 'Minimum 1 month' : `Total: $${(inputs.holdingCostsMonthly * inputs.holdingPeriodMonths).toLocaleString()}`}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Income & Growth */}
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
                          Income & Growth
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Rental income and appreciation assumptions
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Monthly Rent
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.monthlyRent}
                          onChange={(e) => updateInput('monthlyRent', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 500, step: 50 }}
                          error={inputs.monthlyRent < 500}
                          helperText={inputs.monthlyRent < 500 ? 'Minimum $500' : inputs.purchasePrice > 0 ? `1% rule: ${((inputs.monthlyRent / inputs.purchasePrice) * 100).toFixed(2)}%` : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Monthly Income
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherIncomeMonthly}
                          onChange={(e) => updateInput('otherIncomeMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 25 }}
                          helperText="Laundry, parking, etc."
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Rent Growth
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
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                          error={inputs.rentGrowthRate < 0 || inputs.rentGrowthRate > 10}
                          helperText={inputs.rentGrowthRate < 0 || inputs.rentGrowthRate > 10 ? 'Range: 0-10%' : 'Typical: 2-4%'}
                        />
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
                          inputProps={{ min: 0, max: 25, step: 0.25 }}
                          error={inputs.vacancyRate < 0 || inputs.vacancyRate > 25}
                          helperText={inputs.vacancyRate < 0 || inputs.vacancyRate > 25 ? 'Range: 0-25%' : 'Market standard: 5-10%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Appreciation
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.appreciationRate}
                          onChange={(e) => updateInput('appreciationRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
                          error={inputs.appreciationRate < 0 || inputs.appreciationRate > 12}
                          helperText={inputs.appreciationRate < 0 || inputs.appreciationRate > 12 ? 'Range: 0-12%' : 'Long-term avg: 3-4%'}
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
                          Monthly and annual operating costs
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Management Fee
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.managementPct}
                          onChange={(e) => updateInput('managementPct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% of rent</Typography>,
                          }}
                          inputProps={{ min: 0, max: 20, step: 0.25 }}
                          error={inputs.managementPct < 0 || inputs.managementPct > 20}
                          helperText={inputs.managementPct < 0 || inputs.managementPct > 20 ? 'Range: 0-20%' : 'Typical: 8-10%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Maintenance Allowance
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.maintenancePct}
                          onChange={(e) => updateInput('maintenancePct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% of rent</Typography>,
                          }}
                          inputProps={{ min: 0, max: 25, step: 0.25 }}
                          error={inputs.maintenancePct < 0 || inputs.maintenancePct > 25}
                          helperText={inputs.maintenancePct < 0 || inputs.maintenancePct > 25 ? 'Range: 0-25%' : 'Typical: 5-10%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Property Tax
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
                          inputProps={{ min: 0, step: 250 }}
                          helperText="Annual property taxes"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Insurance
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
                          inputProps={{ min: 0, step: 100 }}
                          helperText="Annual insurance premium"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Utilities
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.utilitiesMonthly}
                          onChange={(e) => updateInput('utilitiesMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 25 }}
                          helperText="If landlord-paid"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          HOA Dues
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.hoaMonthly}
                          onChange={(e) => updateInput('hoaMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 10 }}
                          helperText="Homeowner association fees"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Expenses
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherExpensesMonthly}
                          onChange={(e) => updateInput('otherExpensesMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 10 }}
                          helperText="Misc monthly expenses"
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          CapEx Reserve
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.capexReserveMonthly}
                          onChange={(e) => updateInput('capexReserveMonthly', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            startAdornment: <Typography variant="body2" sx={{ mr: 0.5, color: 'text.secondary' }}>$</Typography>,
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>/mo</Typography>,
                          }}
                          inputProps={{ min: 0, step: 10 }}
                          helperText="Capital expenditure reserve"
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Expense Growth
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.expenseGrowthRate}
                          onChange={(e) => updateInput('expenseGrowthRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                          error={inputs.expenseGrowthRate < 0 || inputs.expenseGrowthRate > 10}
                          helperText={inputs.expenseGrowthRate < 0 || inputs.expenseGrowthRate > 10 ? 'Range: 0-10%' : 'Typical: 2-3%'}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Financing & Disposition */}
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
                        <AccountBalanceIcon sx={{ fontSize: 20, color: '#8b5cf6' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Financing & Disposition
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Loan terms and exit strategy
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Down Payment (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.downPaymentPct}
                          onChange={(e) => updateInput('downPaymentPct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 0, max: 60, step: 1 }}
                          error={inputs.downPaymentPct < 0 || inputs.downPaymentPct > 60}
                          helperText={inputs.downPaymentPct < 0 || inputs.downPaymentPct > 60 ? 'Range: 0-60%' : inputs.purchasePrice > 0 ? `$${((inputs.purchasePrice * inputs.downPaymentPct) / 100).toLocaleString()}` : ''}
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
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 2, max: 15, step: 0.25 }}
                          error={inputs.interestRate < 2 || inputs.interestRate > 15}
                          helperText={inputs.interestRate < 2 || inputs.interestRate > 15 ? 'Range: 2-15%' : 'Conventional: 6-8%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Loan Term (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.loanTermYears}
                          onChange={(e) => updateInput('loanTermYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>years</Typography>,
                          }}
                          inputProps={{ min: 5, max: 40, step: 5 }}
                          error={inputs.loanTermYears < 5 || inputs.loanTermYears > 40}
                          helperText={inputs.loanTermYears < 5 || inputs.loanTermYears > 40 ? 'Range: 5-40 years' : 'Typical: 30 years'}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Divider sx={{ my: 1 }}>
                          <Chip label="Refinance Options (0 = No Refinance)" size="small" />
                        </Divider>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Refinance LTV (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.refinanceLtv}
                          onChange={(e) => updateInput('refinanceLtv', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 0, max: 85, step: 1 }}
                          error={inputs.refinanceLtv < 0 || inputs.refinanceLtv > 85}
                          helperText={inputs.refinanceLtv < 0 || inputs.refinanceLtv > 85 ? 'Range: 0-85%' : 'Typical: 70-75%'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Refinance Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.refinanceRate}
                          onChange={(e) => updateInput('refinanceRate', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>% /year</Typography>,
                          }}
                          inputProps={{ min: 2, max: 12, step: 0.25 }}
                          error={inputs.refinanceRate < 2 || inputs.refinanceRate > 12}
                          helperText={inputs.refinanceRate < 2 || inputs.refinanceRate > 12 ? 'Range: 2-12%' : 'Usually lower than purchase'}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Refinance Term (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.refinanceTermYears}
                          onChange={(e) => updateInput('refinanceTermYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>years</Typography>,
                          }}
                          inputProps={{ min: 5, max: 40, step: 5 }}
                          error={inputs.refinanceTermYears < 5 || inputs.refinanceTermYears > 40}
                          helperText={inputs.refinanceTermYears < 5 || inputs.refinanceTermYears > 40 ? 'Range: 5-40 years' : ''}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Refinance Year (0 = none)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.refinanceYear}
                          onChange={(e) => updateInput('refinanceYear', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 10, step: 1 }}
                          error={inputs.refinanceYear < 0 || inputs.refinanceYear > 10}
                          helperText={inputs.refinanceYear < 0 || inputs.refinanceYear > 10 ? 'Range: 0-10' : inputs.refinanceYear === 0 ? 'No refinance planned' : `Refinance in year ${inputs.refinanceYear}`}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Refinance Costs (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.refinanceCostPct}
                          onChange={(e) => updateInput('refinanceCostPct', Number(e.target.value))}
                          fullWidth
                          size="small"
                          InputProps={{
                            endAdornment: <Typography variant="body2" sx={{ ml: 0.5, color: 'text.secondary' }}>%</Typography>,
                          }}
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                          error={inputs.refinanceCostPct < 0 || inputs.refinanceCostPct > 10}
                          helperText={inputs.refinanceCostPct < 0 || inputs.refinanceCostPct > 10 ? 'Range: 0-10%' : 'Typical: 2-3%'}
                        />
                      </Grid>
                      <Grid item xs={12}>
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
                          helperText={inputs.sellingCostPct < 3 || inputs.sellingCostPct > 12 ? 'Range: 3-12%' : 'Agent fees (5-6%) + closing costs (1-2%)'}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Holding Strategy */}
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
                        <ScheduleIcon sx={{ fontSize: 20, color: '#ec4899' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Holding Strategy
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Investment timeline
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Hold Period (years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdPeriodYears}
                          onChange={(e) => updateInput('holdPeriodYears', Number(e.target.value))}
                          fullWidth
                          size="small"
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
                      ? `linear-gradient(135deg, ${alpha('#10b981', 0.1)} 0%, ${alpha('#059669', 0.1)} 100%)`
                      : `linear-gradient(135deg, ${alpha('#10b981', 0.05)} 0%, ${alpha('#059669', 0.05)} 100%)`,
                    border: `2px dashed ${alpha('#10b981', 0.3)}`,
                  }}
                >
                  <Box
                    sx={{
                      width: 72,
                      height: 72,
                      borderRadius: '50%',
                      background: `linear-gradient(135deg, ${alpha('#10b981', 0.2)} 0%, ${alpha('#059669', 0.2)} 100%)`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 3,
                    }}
                  >
                    <PlayArrowIcon sx={{ fontSize: 36, color: '#10b981' }} />
                  </Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Ready to Analyze
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                    Enter your rental property details and financing assumptions, then click "Run Model" to see
                    10-year projections, exit strategies, and investment metrics.
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PlayArrowIcon />}
                    onClick={handleRunModel}
                    sx={{
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
                      },
                    }}
                  >
                    Run Model
                  </Button>
                </Card>
              ) : (
                <Stack spacing={3}>
                  {/* Key Metrics Card */}
                  <Card
                    sx={{
                      background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                      color: 'white',
                    }}
                  >
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        Year 1 Key Metrics
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            1% Rule
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {formatPercent(results.onePercentRule, 2)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Cap Rate
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {formatPercent(results.capRate * 100, 2)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Cash-on-Cash
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {formatPercent(results.cashOnCash * 100, 2)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            DSCR
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 700 }}>
                            {results.dscr.toFixed(2)}x
                          </Typography>
                        </Grid>
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

                  {/* Hold Strategy */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                        {inputs.holdPeriodYears}-Year Hold Strategy
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Exit Value', value: results.exitValue },
                          { label: 'Net Sale Proceeds', value: results.netSaleProceeds },
                          { label: 'Project IRR', value: `${formatPercent(results.irr, 1)}`, isPercent: true },
                          { label: 'Equity Multiple', value: `${results.equityMultiple.toFixed(2)}x`, isText: true },
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
                              {item.isPercent || item.isText ? item.value : formatCurrency(Number(item.value))}
                            </Typography>
                          </Stack>
                        ))}
                      </Stack>
                    </CardContent>
                  </Card>

                  {/* Exit Strategy Comparison */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                        Exit Strategy Comparison
                      </Typography>
                      <Stack spacing={3}>
                        <Box>
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                            Flip
                          </Typography>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              Gross Profit
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(results.flipGrossProfit)}
                            </Typography>
                          </Stack>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              ROI
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatPercent(results.flipRoi, 1)}
                            </Typography>
                          </Stack>
                        </Box>
                        <Box>
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                            BRRRR
                          </Typography>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              Cash Out at Refi
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(results.brrrCashOut)}
                            </Typography>
                          </Stack>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              Year 2 Cash Flow
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(results.brrrYear2CashFlow)}
                            </Typography>
                          </Stack>
                        </Box>
                        <Box>
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                            Hold {inputs.holdPeriodYears} Years
                          </Typography>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              Monthly Cash Flow
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(results.holdMonthlyCashFlow)}
                            </Typography>
                          </Stack>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              IRR
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatPercent(results.irr, 1)}
                            </Typography>
                          </Stack>
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
            {/* Cash Flow Components */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    10-Year Cash Flow Components
                  </Typography>
                  <Box sx={{ height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={cashFlowData}>
                        <defs>
                          <linearGradient id="colorNOI" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="colorDebt" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="colorCF" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
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
                          dataKey="NOI"
                          stroke="#10b981"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorNOI)"
                        />
                        <Area
                          type="monotone"
                          dataKey="Debt Service"
                          stroke="#ef4444"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorDebt)"
                        />
                        <Area
                          type="monotone"
                          dataKey="Cash Flow"
                          stroke="#3b82f6"
                          strokeWidth={2}
                          fillOpacity={1}
                          fill="url(#colorCF)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Equity Growth */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Equity Growth
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={equityData}>
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
                        <Line type="monotone" dataKey="Property Value" stroke="#10b981" strokeWidth={2} />
                        <Line type="monotone" dataKey="Equity" stroke="#3b82f6" strokeWidth={2} />
                        <Line type="monotone" dataKey="Loan Balance" stroke="#ef4444" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Exit Strategy Comparison */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Exit Strategy Value Comparison
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={exitComparisonData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} opacity={0.2} />
                        <XAxis dataKey="strategy" stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} fontSize={12} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: isDark ? '#1e293b' : '#fff',
                            border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                            borderRadius: '12px',
                          }}
                          formatter={(value: number) => formatCurrency(value)}
                        />
                        <Bar dataKey="value" fill="#10b981" radius={[8, 8, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* 10-Year Projection Table */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    10-Year Cash Flow Projection
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Year</TableCell>
                          <TableCell align="right">Gross Rent</TableCell>
                          <TableCell align="right">Vacancy</TableCell>
                          <TableCell align="right">Op. Expenses</TableCell>
                          <TableCell align="right">NOI</TableCell>
                          <TableCell align="right">Debt Service</TableCell>
                          <TableCell align="right">Cash Flow</TableCell>
                          <TableCell align="right">Equity</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {results.projections.map((proj) => (
                          <TableRow key={proj.year}>
                            <TableCell>{proj.year}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.grossRent)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.vacancy)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.operatingExpenses)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.noi)}</TableCell>
                            <TableCell align="right">{formatCurrency(proj.debtService)}</TableCell>
                            <TableCell align="right" sx={{ fontWeight: 600 }}>
                              {formatCurrency(proj.cashFlow)}
                            </TableCell>
                            <TableCell align="right">{formatCurrency(proj.equity)}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
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
              annual_noi: results.year1Noi,
              total_cash_invested: results.equityInvested,
              property_value: results.totalProjectCost,
            }}
            propertyType="single_family"
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
        <Box sx={{ px: 4, pb: 4 }}>
          <Card sx={{ maxWidth: 900, mx: 'auto' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h4" sx={{ mb: 4, fontWeight: 700 }}>
                Single Family Rental Model Documentation
              </Typography>
              <Stack spacing={4}>
                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Overview
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                    This comprehensive rental property model analyzes long-term buy-and-hold strategies including
                    BRRRR (Buy, Rehab, Rent, Refinance, Repeat). It projects 10 years of cash flows with growth
                    assumptions and compares multiple exit strategies to help you make informed investment decisions.
                  </Typography>
                </Box>

                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Key Metrics Targets
                  </Typography>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Metric</TableCell>
                          <TableCell>Target</TableCell>
                          <TableCell>Excellent</TableCell>
                          <TableCell>Formula</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {[
                          { metric: '1% Rule', target: '≥1.0%', excellent: '≥1.5%', formula: 'Monthly Rent / Purchase Price' },
                          { metric: 'Cap Rate', target: '≥7.0%', excellent: '≥9.0%', formula: 'NOI / All-In Cost' },
                          { metric: 'Cash-on-Cash', target: '≥10%', excellent: '≥15%', formula: 'Annual CF / Equity Invested' },
                          { metric: 'DSCR', target: '≥1.25x', excellent: '≥1.35x', formula: 'NOI / Annual Debt Service' },
                          { metric: '10-Year IRR', target: '≥15%', excellent: '≥20%', formula: 'Internal Rate of Return' },
                        ].map((row) => (
                          <TableRow key={row.metric}>
                            <TableCell sx={{ fontWeight: 600 }}>{row.metric}</TableCell>
                            <TableCell>{row.target}</TableCell>
                            <TableCell sx={{ color: '#10b981', fontWeight: 600 }}>{row.excellent}</TableCell>
                            <TableCell>{row.formula}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Box>

                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Exit Strategies
                  </Typography>
                  <Stack spacing={2}>
                    <Box sx={{ p: 2, bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05), borderRadius: 2 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                        Flip Strategy
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Renovate and sell quickly for immediate profit. Best for markets with strong appreciation and
                        high demand.
                      </Typography>
                    </Box>
                    <Box sx={{ p: 2, bgcolor: isDark ? alpha('#10b981', 0.1) : alpha('#10b981', 0.05), borderRadius: 2 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                        BRRRR Strategy
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Buy, Rehab, Rent, Refinance, Repeat. Pull out capital through refinancing to recycle into new
                        deals while maintaining rental income.
                      </Typography>
                    </Box>
                    <Box sx={{ p: 2, bgcolor: isDark ? alpha('#8b5cf6', 0.1) : alpha('#8b5cf6', 0.05), borderRadius: 2 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                        Hold Strategy
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Long-term buy-and-hold for steady cash flow, appreciation, and tax benefits through depreciation.
                      </Typography>
                    </Box>
                  </Stack>
                </Box>

                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Best Practices
                  </Typography>
                  <Stack spacing={1.5}>
                    {[
                      'Use conservative rent growth assumptions (2-4%) to avoid over-optimistic projections',
                      'Budget at least 8-10% for management fees even if self-managing to value your time',
                      'Set aside 1-2% of property value annually for CapEx reserves',
                      'Factor in 5-8% vacancy rate even in strong markets',
                      'Verify comps and rent potential before finalizing purchase',
                      'Aim for DSCR above 1.25x to ensure stable debt coverage',
                      'Consider refinancing after forced appreciation through renovations',
                    ].map((practice, index) => (
                      <Stack key={index} direction="row" spacing={1.5} alignItems="flex-start">
                        <CheckCircleIcon sx={{ fontSize: 18, color: '#10b981', mt: 0.25, flexShrink: 0 }} />
                        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                          {practice}
                        </Typography>
                      </Stack>
                    ))}
                  </Stack>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Box>
      )}
    </Box>
  );
};
