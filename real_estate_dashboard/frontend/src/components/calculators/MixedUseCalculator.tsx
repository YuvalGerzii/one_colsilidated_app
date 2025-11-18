import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Tabs,
  Tab,
  Stack,
  Chip,
  Paper,
  alpha,
  useTheme,
} from '@mui/material';
import {
  Business as BusinessIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  CheckCircle as CheckCircleIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { MixedUseInputs, MixedUseResults, MixedUseProjection } from '../../types/calculatorTypes';

const COMPONENTS = ['Multifamily', 'Office', 'Retail', 'Hotel', 'Restaurant'] as const;
const COMPONENT_COLORS = {
  Multifamily: '#3b82f6',
  Office: '#8b5cf6',
  Retail: '#f59e0b',
  Hotel: '#ec4899',
  Restaurant: '#10b981',
};

// Helper functions
const annuityPayment = (principal: number, annualRate: number, years: number): number => {
  if (annualRate === 0) return principal / (years * 12);
  const monthlyRate = annualRate / 12;
  const numPayments = years * 12;
  return (principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments))) / (Math.pow(1 + monthlyRate, numPayments) - 1);
};

const remainingBalance = (principal: number, annualRate: number, totalYears: number, paymentsMade: number): number => {
  if (annualRate === 0) {
    const totalPayments = totalYears * 12;
    return principal * (totalPayments - paymentsMade) / totalPayments;
  }
  const monthlyRate = annualRate / 12;
  const totalPayments = totalYears * 12;
  return principal * (Math.pow(1 + monthlyRate, totalPayments) - Math.pow(1 + monthlyRate, paymentsMade)) / (Math.pow(1 + monthlyRate, totalPayments) - 1);
};

const calculateIRR = (cashFlows: number[], initialGuess: number = 0.1): number => {
  let irr = initialGuess;
  const maxIterations = 100;
  const tolerance = 0.0001;

  for (let i = 0; i < maxIterations; i++) {
    let npv = 0;
    let dnpv = 0;

    for (let t = 0; t < cashFlows.length; t++) {
      npv += cashFlows[t] / Math.pow(1 + irr, t);
      if (t > 0) {
        dnpv -= (t * cashFlows[t]) / Math.pow(1 + irr, t + 1);
      }
    }

    if (Math.abs(npv) < tolerance) {
      return irr;
    }

    if (dnpv === 0) {
      return 0;
    }

    irr = irr - npv / dnpv;

    if (irr < -0.99) irr = -0.99;
    if (irr > 10) irr = 10;
  }

  return irr;
};

export const MixedUseCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [showResults, setShowResults] = useState(true);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs] = useState<MixedUseInputs>({
    projectName: 'Metropolitan Mixed-Use Tower',
    location: 'Chicago, IL',
    totalBuildingSf: 500000,
    analysisYears: 10,
    multifamilyAllocation: 0.4,
    officeAllocation: 0.25,
    retailAllocation: 0.15,
    hotelAllocation: 0.15,
    restaurantAllocation: 0.05,
    mfAvgUnitSf: 850,
    mfAvgRent: 3500,
    mfOccupancy: 0.96,
    mfRentGrowth: 0.035,
    mfOtherIncomePerUnit: 150,
    mfOperatingExpensePerUnit: 650,
    officeLoadFactor: 1.2,
    officeRentPerSf: 45,
    officeOccupancy: 0.95,
    officeRentGrowth: 0.03,
    officeExpensePerSf: 15,
    officeExpenseRecovery: 0.98,
    retailRentPerSf: 55,
    retailOccupancy: 0.92,
    retailRentGrowth: 0.04,
    retailPercentageRentPct: 0.08,
    retailSalesPerSf: 500,
    retailCamPerSf: 12,
    retailExpensePerSf: 18,
    hotelAvgRoomSf: 500,
    hotelAdr: 285,
    hotelOccupancy: 0.75,
    hotelRevparGrowth: 0.04,
    hotelFnbPerRoom: 45,
    hotelOtherPerRoom: 15,
    hotelOperatingExpensePct: 0.65,
    hotelManagementFeePct: 0.03,
    restaurantRentPerSf: 60,
    restaurantPercentageRentPct: 0.1,
    restaurantSalesPerSf: 800,
    restaurantOccupancy: 0.9,
    restaurantRentGrowth: 0.035,
    restaurantExpensePerSf: 20,
    landCost: 75000000,
    hardCostPerSf: 425,
    softCostPct: 0.18,
    mfFfePerUnit: 8000,
    hotelFfePerRoom: 15000,
    restaurantFfePerSf: 125,
    developerFeePct: 0.03,
    contingencyPct: 0.05,
    ltc: 0.65,
    interestRate: 0.065,
    loanTermYears: 30,
    interestOnlyYears: 0,
    loanFeesPct: 0.015,
    holdPeriodYears: 10,
    mfExitCap: 0.048,
    officeExitCap: 0.065,
    retailExitCap: 0.06,
    hotelExitCap: 0.07,
    restaurantExitCap: 0.065,
    sellingCostPct: 0.025,
  });

  const [results, setResults] = useState<MixedUseResults | null>(null);

  useEffect(() => {
    // Normalize allocations
    const raw = {
      Multifamily: inputs.multifamilyAllocation,
      Office: inputs.officeAllocation,
      Retail: inputs.retailAllocation,
      Hotel: inputs.hotelAllocation,
      Restaurant: inputs.restaurantAllocation,
    };
    const total = Object.values(raw).reduce((sum, val) => sum + val, 0);
    const allocations = total === 0
      ? { Multifamily: 0, Office: 0, Retail: 0, Hotel: 0, Restaurant: 0 }
      : {
          Multifamily: raw.Multifamily / total,
          Office: raw.Office / total,
          Retail: raw.Retail / total,
          Hotel: raw.Hotel / total,
          Restaurant: raw.Restaurant / total,
        };

    const componentSf = {
      Multifamily: inputs.totalBuildingSf * allocations.Multifamily,
      Office: inputs.totalBuildingSf * allocations.Office,
      Retail: inputs.totalBuildingSf * allocations.Retail,
      Hotel: inputs.totalBuildingSf * allocations.Hotel,
      Restaurant: inputs.totalBuildingSf * allocations.Restaurant,
    };

    const mfUnits = Math.max(Math.round(componentSf.Multifamily / inputs.mfAvgUnitSf), 1);
    const hotelRooms = Math.max(Math.round(componentSf.Hotel / inputs.hotelAvgRoomSf), 0);
    const officeRsf = componentSf.Office * inputs.officeLoadFactor;

    // Development budget
    const hardCosts = inputs.totalBuildingSf * inputs.hardCostPerSf;
    const softCosts = hardCosts * inputs.softCostPct;
    const mfFfe = mfUnits * inputs.mfFfePerUnit;
    const hotelFfe = hotelRooms * inputs.hotelFfePerRoom;
    const restaurantFfe = componentSf.Restaurant * inputs.restaurantFfePerSf;
    const subtotal = inputs.landCost + hardCosts + softCosts + mfFfe + hotelFfe + restaurantFfe;
    const developerFee = subtotal * inputs.developerFeePct;
    const contingency = (hardCosts + softCosts) * inputs.contingencyPct;
    const totalDevelopmentCost = subtotal + developerFee + contingency;
    const loanAmount = totalDevelopmentCost * inputs.ltc;
    const loanFees = loanAmount * inputs.loanFeesPct;
    const totalProjectCost = totalDevelopmentCost + loanFees;
    const equity = totalProjectCost - loanAmount;

    // Revenue baselines (Year 1)
    const mfGprYear1 = mfUnits * inputs.mfAvgRent * 12;
    const mfOtherIncomeYear1 = mfUnits * inputs.mfOtherIncomePerUnit * 12;
    const mfOperatingExpenseYear1 = mfUnits * inputs.mfOperatingExpensePerUnit * 12;

    const officeGrossRentYear1 = officeRsf * inputs.officeRentPerSf;
    const officeNetExpensePerSf = inputs.officeExpensePerSf * (1 - inputs.officeExpenseRecovery);

    const retailBaseRentYear1 = componentSf.Retail * inputs.retailRentPerSf * inputs.retailOccupancy;
    const retailPercentageRentYear1 = componentSf.Retail * inputs.retailSalesPerSf * inputs.retailPercentageRentPct;
    const retailCamYear1 = componentSf.Retail * inputs.retailCamPerSf;
    const retailExpensesYear1 = componentSf.Retail * inputs.retailExpensePerSf;

    const hotelRoomRevenueYear1 = hotelRooms * inputs.hotelAdr * inputs.hotelOccupancy * 365;
    const hotelFnbYear1 = hotelRooms * inputs.hotelFnbPerRoom * 365;
    const hotelOtherYear1 = hotelRooms * inputs.hotelOtherPerRoom * 365;

    const restaurantBaseRentYear1 = componentSf.Restaurant * inputs.restaurantRentPerSf * inputs.restaurantOccupancy;
    const restaurantPercentageRentYear1 = componentSf.Restaurant * inputs.restaurantSalesPerSf * inputs.restaurantPercentageRentPct;
    const restaurantExpensesYear1 = componentSf.Restaurant * inputs.restaurantExpensePerSf;

    // Debt service schedule
    const analysisYears = Math.max(Math.min(inputs.analysisYears, 20), 1);
    const holdPeriod = Math.max(Math.min(inputs.holdPeriodYears, analysisYears), 1);
    const ioYears = Math.min(inputs.interestOnlyYears, inputs.loanTermYears);
    const amortYears = Math.max(inputs.loanTermYears - ioYears, 0);
    const amortPayment = amortYears > 0 ? annuityPayment(loanAmount, inputs.interestRate, amortYears) * 12 : loanAmount * inputs.interestRate;

    const debtServiceSchedule: number[] = [];
    for (let year = 1; year <= analysisYears; year++) {
      if (year <= ioYears) {
        debtServiceSchedule.push(loanAmount * inputs.interestRate);
      } else {
        debtServiceSchedule.push(amortPayment);
      }
    }

    // Multi-year projections
    const projections: MixedUseProjection[] = [];
    const componentDetails: Array<{ Multifamily: number; Office: number; Retail: number; Hotel: number; Restaurant: number }> = [];
    let cumulativeCashFlow = 0;

    for (let year = 1; year <= analysisYears; year++) {
      // Multifamily
      const mfGpr = mfGprYear1 * Math.pow(1 + inputs.mfRentGrowth, year - 1);
      const mfEffectiveIncome = mfGpr * inputs.mfOccupancy + (mfOtherIncomeYear1 * Math.pow(1 + inputs.mfRentGrowth, year - 1));
      const mfExpenses = mfOperatingExpenseYear1 * Math.pow(1 + inputs.mfRentGrowth, year - 1);
      const mfNoi = mfEffectiveIncome - mfExpenses;

      // Office
      const officeIncome = officeGrossRentYear1 * Math.pow(1 + inputs.officeRentGrowth, year - 1);
      const officeEffectiveIncome = officeIncome * inputs.officeOccupancy;
      const officeExpenses = officeRsf * officeNetExpensePerSf * Math.pow(1 + inputs.officeRentGrowth, year - 1);
      const officeNoi = officeEffectiveIncome - officeExpenses;

      // Retail
      const retailIncome = (
        retailBaseRentYear1 * Math.pow(1 + inputs.retailRentGrowth, year - 1) +
        retailPercentageRentYear1 * Math.pow(1 + inputs.retailRentGrowth, year - 1) +
        retailCamYear1 * Math.pow(1 + inputs.retailRentGrowth, year - 1)
      );
      const retailNoi = retailIncome - (retailExpensesYear1 * Math.pow(1 + inputs.retailRentGrowth, year - 1));

      // Hotel
      const hotelTotalRevenue = (
        hotelRoomRevenueYear1 * Math.pow(1 + inputs.hotelRevparGrowth, year - 1) +
        hotelFnbYear1 * Math.pow(1 + inputs.hotelRevparGrowth, year - 1) +
        hotelOtherYear1 * Math.pow(1 + inputs.hotelRevparGrowth, year - 1)
      );
      const hotelOperatingExpense = hotelTotalRevenue * inputs.hotelOperatingExpensePct;
      const hotelManagementFee = hotelTotalRevenue * inputs.hotelManagementFeePct;
      const hotelNoi = hotelTotalRevenue - hotelOperatingExpense - hotelManagementFee;

      // Restaurant
      const restaurantIncome = (
        restaurantBaseRentYear1 * Math.pow(1 + inputs.restaurantRentGrowth, year - 1) +
        restaurantPercentageRentYear1 * Math.pow(1 + inputs.restaurantRentGrowth, year - 1)
      );
      const restaurantNoi = restaurantIncome - (restaurantExpensesYear1 * Math.pow(1 + inputs.restaurantRentGrowth, year - 1));

      const componentNois = {
        Multifamily: mfNoi,
        Office: officeNoi,
        Retail: retailNoi,
        Hotel: hotelNoi,
        Restaurant: restaurantNoi,
      };

      const totalNoi = Object.values(componentNois).reduce((sum, val) => sum + val, 0);
      const totalIncome = mfEffectiveIncome + officeEffectiveIncome + retailIncome + hotelTotalRevenue + restaurantIncome;
      const debtService = debtServiceSchedule[year - 1];
      const cashFlow = totalNoi - debtService;
      cumulativeCashFlow += cashFlow;

      projections.push({
        year,
        totalIncome,
        totalNoi,
        debtService,
        cashFlow,
        cumulativeCashFlow,
        componentNois,
      });
      componentDetails.push(componentNois);
    }

    // Exit calculations
    const exitYear = holdPeriod;
    const exitNois = componentDetails[exitYear - 1];
    const exitValues = {
      Multifamily: inputs.mfExitCap > 0 ? exitNois.Multifamily / inputs.mfExitCap : 0,
      Office: inputs.officeExitCap > 0 ? exitNois.Office / inputs.officeExitCap : 0,
      Retail: inputs.retailExitCap > 0 ? exitNois.Retail / inputs.retailExitCap : 0,
      Hotel: inputs.hotelExitCap > 0 ? exitNois.Hotel / inputs.hotelExitCap : 0,
      Restaurant: inputs.restaurantExitCap > 0 ? exitNois.Restaurant / inputs.restaurantExitCap : 0,
    };

    const totalExitValue = Object.values(exitValues).reduce((sum, val) => sum + val, 0);
    const weightedExitCap = totalExitValue > 0 ? Object.values(exitNois).reduce((sum, val) => sum + val, 0) / totalExitValue : 0;
    const sellingCosts = totalExitValue * inputs.sellingCostPct;

    let loanBalanceExit: number;
    if (exitYear <= ioYears || amortYears === 0) {
      loanBalanceExit = loanAmount;
    } else {
      const paymentsMade = (exitYear - ioYears) * 12;
      loanBalanceExit = remainingBalance(loanAmount, inputs.interestRate, amortYears, paymentsMade);
    }

    const netSale = totalExitValue - sellingCosts - loanBalanceExit;

    // Cash flows for IRR
    const cashFlows = [-equity];
    for (let year = 1; year <= analysisYears; year++) {
      let cf = projections[year - 1].cashFlow;
      if (year === exitYear) {
        cf += netSale;
      }
      cashFlows.push(cf);
    }

    const irr = calculateIRR(cashFlows.slice(0, exitYear + 1));
    const totalReturns = cashFlows.slice(1, exitYear + 1).reduce((sum, cf) => sum + cf, 0);
    const equityMultiple = equity > 0 ? totalReturns / equity : 0;
    const cashOnCash = equity > 0 ? projections[0].cashFlow / equity : 0;

    setResults({
      componentSf,
      mfUnits,
      hotelRooms,
      officeRsf,
      hardCosts,
      softCosts,
      mfFfe,
      hotelFfe,
      restaurantFfe,
      developerFee,
      contingency,
      totalDevelopmentCost,
      loanAmount,
      loanFees,
      totalProjectCost,
      equity,
      componentNoiYear1: componentDetails[0],
      componentNoiExit: exitNois,
      exitValues,
      totalExitValue,
      weightedExitCap,
      sellingCosts,
      loanBalanceExit,
      netSale,
      irr,
      equityMultiple,
      cashOnCash,
      exitYear,
      projections,
      cashFlows,
      cumulativeCashFlows: projections.map(p => p.cumulativeCashFlow),
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
    return `${(value * 100).toFixed(2)}%`;
  };

  const handleSave = () => {
    const report = {
      id: Date.now().toString(),
      modelType: 'mixed-use',
      projectName: inputs.projectName,
      location: inputs.location,
      date: new Date().toISOString(),
      inputs: inputs,
      results: results,
    };

    const existing = localStorage.getItem('savedReports');
    const reports = existing ? JSON.parse(existing) : [];
    reports.unshift(report);
    localStorage.setItem('savedReports', JSON.stringify(reports));

    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  const getDealQuality = (): string => {
    if (!results) return 'N/A';
    const irr = results.irr;
    if (irr >= 0.18) return 'Excellent';
    if (irr >= 0.14) return 'Strong';
    if (irr >= 0.10) return 'Average';
    return 'Below Target';
  };

  const allocationData = results ? COMPONENTS.map(comp => ({
    name: comp,
    value: results.componentSf[comp],
    color: COMPONENT_COLORS[comp],
  })) : [];

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
                  background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                  boxShadow: '0 4px 16px rgba(99, 102, 241, 0.3)',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(to top, rgba(255,255,255,0.2), transparent)',
                    borderRadius: 3,
                  },
                }}
              >
                <BusinessIcon sx={{ fontSize: 24, color: 'white', position: 'relative', zIndex: 1 }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>
                  {inputs.projectName}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {inputs.location} • {inputs.totalBuildingSf.toLocaleString()} SF Mixed-Use
                </Typography>
              </Box>
            </Stack>
            <Stack direction="row" spacing={2}>
              {showResults && results && (
                <Chip
                  label={getDealQuality()}
                  sx={{
                    background:
                      getDealQuality() === 'Excellent'
                        ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                        : getDealQuality() === 'Strong'
                        ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                        : getDealQuality() === 'Average'
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
              <Button variant="outlined" startIcon={<SaveIcon />} onClick={handleSave} disabled={!showResults}>
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
              ? `linear-gradient(135deg, ${alpha('#6366f1', 0.05)} 0%, ${alpha('#4f46e5', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#6366f1', 0.03)} 0%, ${alpha('#4f46e5', 0.03)} 100%)`,
            border: `1px solid ${alpha('#6366f1', 0.2)}`,
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
            Comprehensive mixed-use development financial model with component-level analysis for Multifamily, Office,
            Retail, Hotel, and Restaurant spaces. Features dynamic space allocation, component-specific revenue and expense
            modeling, development budget waterfall, and consolidated returns analysis across all property types.
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
          <Tab icon={<AssessmentIcon />} iconPosition="start" label="Analytics" />
          <Tab icon={<DescriptionIcon />} iconPosition="start" label="Documentation" />
        </Tabs>
      </Box>

      {/* Analytics Tab */}
      {currentTab === 0 && results && (
        <Box sx={{ px: 4, pb: 4 }}>
          <Grid container spacing={3}>
            {/* Key Metrics */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Project Overview
                  </Typography>
                  <Stack spacing={2}>
                    {[
                      { label: 'Total Project Cost', value: formatCurrency(results.totalProjectCost) },
                      { label: 'Equity Required', value: formatCurrency(results.equity) },
                      { label: 'IRR', value: formatPercent(results.irr) },
                      { label: 'Equity Multiple', value: `${results.equityMultiple.toFixed(2)}x` },
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
                          {item.value}
                        </Typography>
                      </Stack>
                    ))}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            {/* Component Allocations */}
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Component Allocations
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={allocationData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                          outerRadius={120}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {allocationData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value: number) => `${value.toLocaleString()} SF`} />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Component NOI Progression */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Component NOI Progression
                  </Typography>
                  <Box sx={{ height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        {COMPONENTS.map((comp) => (
                          <Line
                            key={comp}
                            type="monotone"
                            dataKey={`componentNois.${comp}`}
                            stroke={COMPONENT_COLORS[comp]}
                            name={comp}
                            strokeWidth={2}
                          />
                        ))}
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Cash Flow Projection */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Total NOI & Cash Flow
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Line type="monotone" dataKey="totalNoi" stroke="#3b82f6" name="Total NOI" strokeWidth={2} />
                        <Line type="monotone" dataKey="cashFlow" stroke="#10b981" name="Cash Flow" strokeWidth={2} />
                        <Line type="monotone" dataKey="debtService" stroke="#ef4444" name="Debt Service" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Cumulative Cash Flow */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Cumulative Cash Flow
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Line type="monotone" dataKey="cumulativeCashFlow" stroke="#8b5cf6" name="Cumulative CF" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}

      {/* Documentation Tab */}
      {currentTab === 1 && (
        <Box sx={{ px: 4, pb: 4 }}>
          <Card sx={{ maxWidth: 900, mx: 'auto' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h4" sx={{ mb: 4, fontWeight: 700 }}>
                Mixed-Use Model Documentation
              </Typography>
              <Stack spacing={4}>
                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Overview
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                    Comprehensive mixed-use development financial model supporting five distinct property types:
                    Multifamily, Office, Retail, Hotel, and Restaurant. Features dynamic space allocation with
                    automatic normalization, component-specific revenue and expense modeling, development budget
                    waterfall, and consolidated investment returns analysis.
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Component Details
                  </Typography>
                  <Stack spacing={2}>
                    {[
                      {
                        title: 'Multifamily (40% default allocation)',
                        description: 'Residential component with unit-based rent modeling, occupancy assumptions, other income, and operating expenses per unit.',
                      },
                      {
                        title: 'Office (25% default allocation)',
                        description: 'Commercial office space with load factor adjustment, triple-net lease structure, expense recovery, and rentable square footage calculations.',
                      },
                      {
                        title: 'Retail (15% default allocation)',
                        description: 'Retail space with base rent, percentage rent tied to sales, CAM charges, and tenant reimbursements.',
                      },
                      {
                        title: 'Hotel (15% default allocation)',
                        description: 'Hospitality component with ADR/occupancy modeling, F&B revenue, RevPAR growth, operating expense ratios, and management fees.',
                      },
                      {
                        title: 'Restaurant (5% default allocation)',
                        description: 'Food service space with base rent, percentage rent, sales per SF assumptions, and operating expense modeling.',
                      },
                    ].map((comp) => (
                      <Box
                        key={comp.title}
                        sx={{
                          p: 2,
                          bgcolor: isDark ? alpha('#94a3b8', 0.05) : alpha('#0f172a', 0.03),
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                          {comp.title}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                          {comp.description}
                        </Typography>
                      </Box>
                    ))}
                  </Stack>
                </Box>
                <Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Key Features
                  </Typography>
                  <Stack spacing={1.5}>
                    {[
                      '500,000 SF building with automatic space allocation normalization',
                      'Component-specific revenue growth rates and expense escalators',
                      'Development budget with FF&E for Multifamily, Hotel, and Restaurant',
                      '65% LTC financing with 30-year amortization',
                      'Component-specific exit cap rates ranging from 4.8% (MF) to 7.0% (Hotel)',
                      '10-year projection period with consolidated cash flows and returns',
                      'IRR, equity multiple, and cash-on-cash return calculations',
                    ].map((feature, index) => (
                      <Stack key={index} direction="row" spacing={1.5} alignItems="flex-start">
                        <CheckCircleIcon sx={{ fontSize: 18, color: '#10b981', mt: 0.25, flexShrink: 0 }} />
                        <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
                          {feature}
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
