import React, { useState, useMemo } from 'react';
import {
  Box,
  Grid,
  Typography,
  TextField,
  Button,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  Divider,
  InputAdornment,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { TrendingUp, Assessment, AccountBalance } from '@mui/icons-material';
import { GlassCard, GlassMetricCard, GlassButton, MicroInteraction } from '../ui/GlassComponents';
import {
  calculateDCF,
  calculateNPV,
  calculateIRR,
  calculateNOI,
  calculateCapRate,
  calculateDSCR,
  calculateCashOnCashReturn,
  scenarioAnalysis,
  monteCarloSimulation,
  generateAmortizationSchedule,
  calculateBreakEven,
} from '../../utils/financialCalculations';

interface ProFormaInputs {
  propertyValue: number;
  purchasePrice: number;
  downPayment: number;
  interestRate: number;
  loanTerm: number;

  // Income
  grossRentalIncome: number;
  otherIncome: number;
  vacancyRate: number;

  // Operating Expenses
  propertyTax: number;
  insurance: number;
  maintenance: number;
  utilities: number;
  propertyManagement: number;
  otherExpenses: number;

  // Projections
  annualRentGrowth: number;
  annualExpenseGrowth: number;
  projectionYears: number;

  // Exit
  holdingPeriod: number;
  exitCapRate: number;
  sellingCosts: number;

  // Analysis
  discountRate: number;
  terminalGrowthRate: number;
}

const ProFormaGenerator: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [showMonteCarlo, setShowMonteCarlo] = useState(false);

  const [inputs, setInputs] = useState<ProFormaInputs>({
    propertyValue: 1000000,
    purchasePrice: 1000000,
    downPayment: 250000,
    interestRate: 0.05,
    loanTerm: 30,

    grossRentalIncome: 120000,
    otherIncome: 5000,
    vacancyRate: 0.05,

    propertyTax: 12000,
    insurance: 3000,
    maintenance: 8000,
    utilities: 2000,
    propertyManagement: 6000,
    otherExpenses: 3000,

    annualRentGrowth: 0.03,
    annualExpenseGrowth: 0.025,
    projectionYears: 10,

    holdingPeriod: 10,
    exitCapRate: 0.06,
    sellingCosts: 0.06,

    discountRate: 0.08,
    terminalGrowthRate: 0.02,
  });

  const handleInputChange = (field: keyof ProFormaInputs) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setInputs(prev => ({
      ...prev,
      [field]: parseFloat(event.target.value) || 0,
    }));
  };

  // Calculate projections
  const projections = useMemo(() => {
    const years = [];
    const loanAmount = inputs.purchasePrice - inputs.downPayment;

    // Calculate annual debt service
    const monthlyRate = inputs.interestRate / 12;
    const numberOfPayments = inputs.loanTerm * 12;
    const monthlyPayment = loanAmount *
      (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
      (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
    const annualDebtService = monthlyPayment * 12;

    for (let year = 1; year <= inputs.projectionYears; year++) {
      // Income
      const grossIncome = inputs.grossRentalIncome * Math.pow(1 + inputs.annualRentGrowth, year - 1);
      const otherIncome = inputs.otherIncome * Math.pow(1 + inputs.annualRentGrowth, year - 1);
      const potentialGrossIncome = grossIncome + otherIncome;
      const vacancyLoss = potentialGrossIncome * inputs.vacancyRate;
      const effectiveGrossIncome = potentialGrossIncome - vacancyLoss;

      // Operating Expenses
      const growthFactor = Math.pow(1 + inputs.annualExpenseGrowth, year - 1);
      const propertyTax = inputs.propertyTax * growthFactor;
      const insurance = inputs.insurance * growthFactor;
      const maintenance = inputs.maintenance * growthFactor;
      const utilities = inputs.utilities * growthFactor;
      const propertyManagement = inputs.propertyManagement * growthFactor;
      const otherExpenses = inputs.otherExpenses * growthFactor;

      const totalOperatingExpenses = propertyTax + insurance + maintenance + utilities + propertyManagement + otherExpenses;

      const noi = effectiveGrossIncome - totalOperatingExpenses;
      const debtService = year <= inputs.holdingPeriod ? annualDebtService : 0;
      const cashFlow = noi - debtService;

      years.push({
        year,
        potentialGrossIncome,
        vacancyLoss,
        effectiveGrossIncome,
        totalOperatingExpenses,
        noi,
        debtService,
        cashFlow,
      });
    }

    return years;
  }, [inputs]);

  // Calculate key metrics
  const metrics = useMemo(() => {
    const firstYearNOI = projections[0]?.noi || 0;
    const capRate = calculateCapRate(firstYearNOI, inputs.purchasePrice);

    const cashFlows = projections.map(p => p.cashFlow);
    const initialInvestment = inputs.downPayment;

    const irrResult = calculateIRR([-initialInvestment, ...cashFlows]);
    const npv = calculateNPV(cashFlows, inputs.discountRate, initialInvestment);

    const firstYearCashFlow = projections[0]?.cashFlow || 0;
    const cashOnCash = calculateCashOnCashReturn(firstYearCashFlow, initialInvestment);

    const loanAmount = inputs.purchasePrice - inputs.downPayment;
    const annualDebtService = projections[0]?.debtService || 0;
    const dscr = annualDebtService > 0 ? calculateDSCR(firstYearNOI, annualDebtService) : 0;

    // DCF Analysis
    const dcfResult = calculateDCF({
      cashFlows,
      discountRate: inputs.discountRate,
      terminalGrowthRate: inputs.terminalGrowthRate,
    });

    // Scenario Analysis
    const scenarios = scenarioAnalysis({
      cashFlows,
      discountRate: inputs.discountRate,
      pessimisticGrowth: 0.01,
      baseGrowth: inputs.terminalGrowthRate,
      optimisticGrowth: 0.04,
    });

    // Break-Even Analysis
    const breakEven = calculateBreakEven([-initialInvestment, ...cashFlows]);

    return {
      capRate,
      irr: irrResult.irr,
      npv,
      cashOnCash,
      dscr,
      dcf: dcfResult,
      scenarios,
      breakEven,
      totalCashFlow: cashFlows.reduce((sum, cf) => sum + cf, 0),
    };
  }, [projections, inputs]);

  // Monte Carlo Simulation
  const monteCarloResults = useMemo(() => {
    if (!showMonteCarlo) return null;

    return monteCarloSimulation({
      baseCashFlow: projections[0]?.cashFlow || 0,
      years: inputs.projectionYears,
      growthMean: inputs.annualRentGrowth,
      growthStdDev: 0.02,
      discountRate: inputs.discountRate,
      simulations: 1000,
    });
  }, [showMonteCarlo, projections, inputs]);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 700 }}>
          <AccountBalance sx={{ mr: 1, verticalAlign: 'middle' }} />
          Interactive Pro Forma Generator
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Comprehensive financial analysis with DCF valuation, scenario analysis, and Monte Carlo simulation
        </Typography>
      </Box>

      <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 3 }}>
        <Tab label="Property Inputs" />
        <Tab label="Projections" />
        <Tab label="Key Metrics" />
        <Tab label="DCF Analysis" />
        <Tab label="Scenario Analysis" />
      </Tabs>

      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Purchase Details
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Property Value"
                    type="number"
                    value={inputs.propertyValue}
                    onChange={handleInputChange('propertyValue')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Purchase Price"
                    type="number"
                    value={inputs.purchasePrice}
                    onChange={handleInputChange('purchasePrice')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Down Payment"
                    type="number"
                    value={inputs.downPayment}
                    onChange={handleInputChange('downPayment')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Interest Rate"
                    type="number"
                    value={inputs.interestRate * 100}
                    onChange={(e) => handleInputChange('interestRate')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Loan Term"
                    type="number"
                    value={inputs.loanTerm}
                    onChange={handleInputChange('loanTerm')}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">years</InputAdornment>,
                    }}
                  />
                </Grid>
              </Grid>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Income
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Gross Rental Income (Annual)"
                    type="number"
                    value={inputs.grossRentalIncome}
                    onChange={handleInputChange('grossRentalIncome')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Other Income (Annual)"
                    type="number"
                    value={inputs.otherIncome}
                    onChange={handleInputChange('otherIncome')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Vacancy Rate"
                    type="number"
                    value={inputs.vacancyRate * 100}
                    onChange={(e) => handleInputChange('vacancyRate')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
              </Grid>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Operating Expenses (Annual)
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Property Tax"
                    type="number"
                    value={inputs.propertyTax}
                    onChange={handleInputChange('propertyTax')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Insurance"
                    type="number"
                    value={inputs.insurance}
                    onChange={handleInputChange('insurance')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Maintenance"
                    type="number"
                    value={inputs.maintenance}
                    onChange={handleInputChange('maintenance')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Utilities"
                    type="number"
                    value={inputs.utilities}
                    onChange={handleInputChange('utilities')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Property Management"
                    type="number"
                    value={inputs.propertyManagement}
                    onChange={handleInputChange('propertyManagement')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Other Expenses"
                    type="number"
                    value={inputs.otherExpenses}
                    onChange={handleInputChange('otherExpenses')}
                    InputProps={{
                      startAdornment: <InputAdornment position="start">$</InputAdornment>,
                    }}
                  />
                </Grid>
              </Grid>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Projections & Analysis
              </Typography>
              <Divider sx={{ mb: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Annual Rent Growth"
                    type="number"
                    value={inputs.annualRentGrowth * 100}
                    onChange={(e) => handleInputChange('annualRentGrowth')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Annual Expense Growth"
                    type="number"
                    value={inputs.annualExpenseGrowth * 100}
                    onChange={(e) => handleInputChange('annualExpenseGrowth')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Projection Years"
                    type="number"
                    value={inputs.projectionYears}
                    onChange={handleInputChange('projectionYears')}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">years</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Discount Rate"
                    type="number"
                    value={inputs.discountRate * 100}
                    onChange={(e) => handleInputChange('discountRate')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Terminal Growth Rate"
                    type="number"
                    value={inputs.terminalGrowthRate * 100}
                    onChange={(e) => handleInputChange('terminalGrowthRate')({
                      ...e,
                      target: { ...e.target, value: String(parseFloat(e.target.value) / 100) }
                    } as any)}
                    InputProps={{
                      endAdornment: <InputAdornment position="end">%</InputAdornment>,
                    }}
                  />
                </Grid>
              </Grid>
            </GlassCard>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <GlassCard sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            10-Year Cash Flow Projections
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Year</TableCell>
                  <TableCell align="right">Potential Gross Income</TableCell>
                  <TableCell align="right">Vacancy Loss</TableCell>
                  <TableCell align="right">Effective Gross Income</TableCell>
                  <TableCell align="right">Operating Expenses</TableCell>
                  <TableCell align="right">NOI</TableCell>
                  <TableCell align="right">Debt Service</TableCell>
                  <TableCell align="right">Cash Flow</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {projections.map((row) => (
                  <TableRow key={row.year}>
                    <TableCell>Year {row.year}</TableCell>
                    <TableCell align="right">{formatCurrency(row.potentialGrossIncome)}</TableCell>
                    <TableCell align="right" sx={{ color: 'error.main' }}>
                      ({formatCurrency(row.vacancyLoss)})
                    </TableCell>
                    <TableCell align="right">{formatCurrency(row.effectiveGrossIncome)}</TableCell>
                    <TableCell align="right" sx={{ color: 'warning.main' }}>
                      ({formatCurrency(row.totalOperatingExpenses)})
                    </TableCell>
                    <TableCell align="right" sx={{ fontWeight: 600 }}>
                      {formatCurrency(row.noi)}
                    </TableCell>
                    <TableCell align="right" sx={{ color: 'error.main' }}>
                      ({formatCurrency(row.debtService)})
                    </TableCell>
                    <TableCell align="right" sx={{ fontWeight: 700, color: 'success.main' }}>
                      {formatCurrency(row.cashFlow)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Cash Flow Visualization
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={projections}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip formatter={(value: number) => formatCurrency(value)} />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="effectiveGrossIncome"
                  stackId="1"
                  stroke="#4caf50"
                  fill="#4caf50"
                  fillOpacity={0.6}
                  name="Effective Gross Income"
                />
                <Area
                  type="monotone"
                  dataKey="totalOperatingExpenses"
                  stackId="2"
                  stroke="#ff9800"
                  fill="#ff9800"
                  fillOpacity={0.6}
                  name="Operating Expenses"
                />
                <Line
                  type="monotone"
                  dataKey="noi"
                  stroke="#2196f3"
                  strokeWidth={3}
                  name="NOI"
                  dot={{ r: 4 }}
                />
                <Line
                  type="monotone"
                  dataKey="cashFlow"
                  stroke="#9c27b0"
                  strokeWidth={3}
                  name="Cash Flow"
                  dot={{ r: 4 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          </Box>
        </GlassCard>
      )}

      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  Cap Rate
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'primary.main' }}>
                  {formatPercent(metrics.capRate)}
                </Typography>
                <Chip
                  label={metrics.capRate > 0.06 ? 'Excellent' : metrics.capRate > 0.04 ? 'Good' : 'Fair'}
                  color={metrics.capRate > 0.06 ? 'success' : metrics.capRate > 0.04 ? 'primary' : 'warning'}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  IRR
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'success.main' }}>
                  {formatPercent(metrics.irr)}
                </Typography>
                <Chip
                  label={metrics.irr > 0.15 ? 'Excellent' : metrics.irr > 0.10 ? 'Good' : 'Fair'}
                  color={metrics.irr > 0.15 ? 'success' : metrics.irr > 0.10 ? 'primary' : 'warning'}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  NPV
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: metrics.npv > 0 ? 'success.main' : 'error.main' }}>
                  {formatCurrency(metrics.npv)}
                </Typography>
                <Chip
                  label={metrics.npv > 0 ? 'Positive' : 'Negative'}
                  color={metrics.npv > 0 ? 'success' : 'error'}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  Cash on Cash Return
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'info.main' }}>
                  {formatPercent(metrics.cashOnCash)}
                </Typography>
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  DSCR
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'secondary.main' }}>
                  {metrics.dscr.toFixed(2)}x
                </Typography>
                <Chip
                  label={metrics.dscr >= 1.25 ? 'Strong' : metrics.dscr >= 1.0 ? 'Adequate' : 'Weak'}
                  color={metrics.dscr >= 1.25 ? 'success' : metrics.dscr >= 1.0 ? 'primary' : 'error'}
                  size="small"
                  sx={{ mt: 1 }}
                />
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          <Grid item xs={12} md={4}>
            <MicroInteraction variant="lift">
              <GlassMetricCard>
                <Typography variant="overline" color="text.secondary">
                  Total Cash Flow (10Y)
                </Typography>
                <Typography variant="h3" sx={{ fontWeight: 700, color: 'success.main' }}>
                  {formatCurrency(metrics.totalCashFlow)}
                </Typography>
              </GlassMetricCard>
            </MicroInteraction>
          </Grid>

          {metrics.breakEven.breakEvenPeriod && (
            <Grid item xs={12}>
              <Alert severity="success" icon={<TrendingUp />}>
                Break-even achieved in Year {metrics.breakEven.breakEvenPeriod}
              </Alert>
            </Grid>
          )}
        </Grid>
      )}

      {activeTab === 3 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                <Assessment sx={{ mr: 1, verticalAlign: 'middle' }} />
                DCF Valuation Summary
              </Typography>
              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="overline" color="text.secondary">
                      Present Value of Cash Flows
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>
                      {formatCurrency(metrics.dcf.sumPVCashFlows)}
                    </Typography>
                  </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="overline" color="text.secondary">
                      Terminal Value
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>
                      {formatCurrency(metrics.dcf.terminalValue)}
                    </Typography>
                  </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Box>
                    <Typography variant="overline" color="text.secondary">
                      PV of Terminal Value
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>
                      {formatCurrency(metrics.dcf.presentValueTerminalValue)}
                    </Typography>
                  </Box>
                </Grid>

                <Grid item xs={12}>
                  <Divider />
                </Grid>

                <Grid item xs={12}>
                  <Box sx={{ textAlign: 'center', p: 3, bgcolor: 'primary.main', borderRadius: 2, color: 'white' }}>
                    <Typography variant="overline">
                      Enterprise Value (DCF)
                    </Typography>
                    <Typography variant="h2" sx={{ fontWeight: 700 }}>
                      {formatCurrency(metrics.dcf.enterpriseValue)}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>

              <Box sx={{ mt: 4 }}>
                <Typography variant="h6" gutterBottom>
                  Present Value by Year
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={metrics.dcf.presentValueCashFlows.map((pv, index) => ({
                      year: `Year ${index + 1}`,
                      presentValue: pv,
                      cashFlow: projections[index]?.cashFlow || 0,
                    }))}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip formatter={(value: number) => formatCurrency(value)} />
                    <Legend />
                    <Bar dataKey="cashFlow" fill="#4caf50" name="Cash Flow" />
                    <Bar dataKey="presentValue" fill="#2196f3" name="Present Value" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </GlassCard>
          </Grid>

          <Grid item xs={12}>
            <GlassCard sx={{ p: 3 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={showMonteCarlo}
                    onChange={(e) => setShowMonteCarlo(e.target.checked)}
                  />
                }
                label="Run Monte Carlo Simulation (1,000 iterations)"
              />

              {showMonteCarlo && monteCarloResults && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Monte Carlo Valuation Distribution
                  </Typography>

                  <Grid container spacing={2} sx={{ mb: 3 }}>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">5th Percentile</Typography>
                      <Typography variant="h6">{formatCurrency(monteCarloResults.percentile5)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">25th Percentile</Typography>
                      <Typography variant="h6">{formatCurrency(monteCarloResults.percentile25)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">Median</Typography>
                      <Typography variant="h6" sx={{ color: 'primary.main' }}>
                        {formatCurrency(monteCarloResults.median)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">75th Percentile</Typography>
                      <Typography variant="h6">{formatCurrency(monteCarloResults.percentile75)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">95th Percentile</Typography>
                      <Typography variant="h6">{formatCurrency(monteCarloResults.percentile95)}</Typography>
                    </Grid>
                    <Grid item xs={6} md={2}>
                      <Typography variant="caption" color="text.secondary">Std Dev</Typography>
                      <Typography variant="h6">{formatCurrency(monteCarloResults.stdDev)}</Typography>
                    </Grid>
                  </Grid>

                  <Alert severity="info">
                    Mean valuation: {formatCurrency(monteCarloResults.mean)} with standard deviation of {formatCurrency(monteCarloResults.stdDev)}
                  </Alert>
                </Box>
              )}
            </GlassCard>
          </Grid>
        </Grid>
      )}

      {activeTab === 4 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Scenario Analysis
              </Typography>
              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 3, border: '2px solid', borderColor: 'error.main', borderRadius: 2 }}>
                    <Typography variant="overline" color="error">
                      Pessimistic (1% Growth)
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                      {formatCurrency(metrics.scenarios.pessimistic.enterpriseValue)}
                    </Typography>
                  </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 3, border: '2px solid', borderColor: 'primary.main', borderRadius: 2 }}>
                    <Typography variant="overline" color="primary">
                      Base ({formatPercent(inputs.terminalGrowthRate)} Growth)
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                      {formatCurrency(metrics.scenarios.base.enterpriseValue)}
                    </Typography>
                  </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                  <Box sx={{ p: 3, border: '2px solid', borderColor: 'success.main', borderRadius: 2 }}>
                    <Typography variant="overline" color="success">
                      Optimistic (4% Growth)
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                      {formatCurrency(metrics.scenarios.optimistic.enterpriseValue)}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>

              <Box sx={{ mt: 4 }}>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={[
                      { scenario: 'Pessimistic', value: metrics.scenarios.pessimistic.enterpriseValue },
                      { scenario: 'Base', value: metrics.scenarios.base.enterpriseValue },
                      { scenario: 'Optimistic', value: metrics.scenarios.optimistic.enterpriseValue },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="scenario" />
                    <YAxis />
                    <Tooltip formatter={(value: number) => formatCurrency(value)} />
                    <Bar dataKey="value" fill="#2196f3" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </GlassCard>
          </Grid>
        </Grid>
      )}

      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <MicroInteraction variant="scale">
          <GlassButton
            variant="contained"
            size="large"
            startIcon={<Assessment />}
            onClick={() => window.print()}
          >
            Export Pro Forma Report
          </GlassButton>
        </MicroInteraction>
      </Box>
    </Box>
  );
};

export default ProFormaGenerator;
