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
  Divider,
} from '@mui/material';
import {
  Hotel as HotelIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as AttachMoneyIcon,
  Restaurant as RestaurantIcon,
  Build as BuildIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  AccountBalance as AccountBalanceIcon,
  CheckCircle as CheckCircleIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  Warning as WarningIcon,
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
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { HotelInputs, HotelResults, HotelProjection } from '../../types/calculatorTypes';
import { MarkdownViewer } from '../common/MarkdownViewer';
import { HOTEL_QUICK_REFERENCE, HOTEL_USER_GUIDE, HOTEL_DELIVERY_SUMMARY } from '../../constants/documentation/hotelDocs';
import { BreakEvenAnalysis } from './advanced/BreakEvenAnalysis';
import { calculateBreakEvenMetrics } from '../../utils/breakEvenCalculations';

const HOTEL_TYPES = ['Luxury', 'Upper Upscale', 'Upscale', 'Midscale', 'Economy'];

// Helper function to calculate monthly annuity payment
const annuityPayment = (principal: number, annualRate: number, years: number): number => {
  if (annualRate === 0) return principal / (years * 12);
  const monthlyRate = annualRate / 12;
  const numPayments = years * 12;
  return (principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments))) / (Math.pow(1 + monthlyRate, numPayments) - 1);
};

// Helper function to calculate remaining loan balance
const remainingBalance = (principal: number, annualRate: number, totalYears: number, paymentsMade: number): number => {
  if (annualRate === 0) {
    const totalPayments = totalYears * 12;
    return principal * (totalPayments - paymentsMade) / totalPayments;
  }
  const monthlyRate = annualRate / 12;
  const totalPayments = totalYears * 12;
  return principal * (Math.pow(1 + monthlyRate, totalPayments) - Math.pow(1 + monthlyRate, paymentsMade)) / (Math.pow(1 + monthlyRate, totalPayments) - 1);
};

// Helper function to calculate IRR using Newton-Raphson method
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

export const HotelCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [docTab, setDocTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<HotelInputs>({
    projectName: 'Harbor View Hotel',
    hotelType: 'Upscale',
    location: 'Miami, FL',
    brandAffiliation: 'Independent',
    analyst: '',
    rooms: 180,
    adr: 210,
    year1Occupancy: 0.55,
    stabilizedOccupancy: 0.70,
    adrGrowthRate: 0.03,
    fnbGrowthRate: 0.03,
    otherIncomeGrowthRate: 0.02,
    fnbOutletPerRoomDay: 35,
    banquetRevPerGroupRoom: 90,
    groupRoomPct: 0.30,
    meetingRevPerRoom: 1000,
    parkingRevPerRoom: 800,
    spaRevPerRoom: 300,
    otherOperatedRevPerRoom: 500,
    roomsDeptPct: 0.28,
    fnbDeptPct: 0.65,
    otherDeptPct: 0.35,
    adminPerRoom: 8000,
    maintenancePerRoom: 3200,
    utilitiesPerRoom: 2600,
    insurancePct: 0.015,
    propertyTaxPct: 0.035,
    expenseGrowthRate: 0.03,
    totalProjectCost: 45000000,
    loanToCost: 0.60,
    interestRate: 0.065,
    amortYears: 25,
    holdPeriodYears: 5,
    exitCapRate: 0.075,
  });

  const [results, setResults] = useState<HotelResults | null>(null);

  const updateInput = (key: keyof HotelInputs, value: number | string) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    // Calculate results
    const projectionYears = Math.max(5, inputs.holdPeriodYears);
    const projections: HotelProjection[] = [];

    // Financing
    const loanAmount = inputs.totalProjectCost * inputs.loanToCost;
    const equity = inputs.totalProjectCost - loanAmount;
    const monthlyPayment = annuityPayment(loanAmount, inputs.interestRate, inputs.amortYears);
    const annualDebtService = monthlyPayment * 12;

    let cumulativeCashFlow = 0;

    // Multi-year projections
    for (let year = 1; year <= projectionYears; year++) {
      const occupancy = year === 1 ? inputs.year1Occupancy : inputs.stabilizedOccupancy;
      const adrYear = inputs.adr * Math.pow(1 + inputs.adrGrowthRate, year - 1);
      const roomsSold = inputs.rooms * 365 * occupancy;
      const roomsRevenue = roomsSold * adrYear;

      // F&B Revenue
      const fnbMultiplier = Math.pow(1 + inputs.fnbGrowthRate, year - 1);
      const restaurantRevenue = inputs.fnbOutletPerRoomDay * inputs.rooms * 365 * fnbMultiplier;
      const banquetRevenue = inputs.banquetRevPerGroupRoom * roomsSold * inputs.groupRoomPct * fnbMultiplier;
      const fnbRevenue = restaurantRevenue + banquetRevenue;

      // Other Revenue
      const otherComponents = inputs.meetingRevPerRoom + inputs.parkingRevPerRoom + inputs.spaRevPerRoom + inputs.otherOperatedRevPerRoom;
      const otherRevenue = inputs.rooms * otherComponents * Math.pow(1 + inputs.otherIncomeGrowthRate, year - 1);

      const totalRevenue = roomsRevenue + fnbRevenue + otherRevenue;

      // Departmental Expenses
      const roomsExpense = roomsRevenue * inputs.roomsDeptPct;
      const fnbExpense = fnbRevenue * inputs.fnbDeptPct;
      const otherExpense = otherRevenue * inputs.otherDeptPct;
      const departmentalExpenses = roomsExpense + fnbExpense + otherExpense;

      // Undistributed Expenses
      const expenseMultiplier = Math.pow(1 + inputs.expenseGrowthRate, year - 1);
      const undistributed = inputs.rooms * (inputs.adminPerRoom + inputs.maintenancePerRoom + inputs.utilitiesPerRoom) * expenseMultiplier;

      // Fixed Charges
      const insurance = totalRevenue * inputs.insurancePct;
      const propertyTax = totalRevenue * inputs.propertyTaxPct;

      const totalExpenses = departmentalExpenses + undistributed + insurance + propertyTax;

      const gop = totalRevenue - departmentalExpenses;
      const gopMargin = totalRevenue > 0 ? gop / totalRevenue : 0;
      const noi = totalRevenue - totalExpenses;
      const noiMargin = totalRevenue > 0 ? noi / totalRevenue : 0;
      const cashFlow = noi - annualDebtService;
      cumulativeCashFlow += cashFlow;
      const revpar = adrYear * occupancy;

      projections.push({
        year,
        occupancy,
        adr: adrYear,
        revpar,
        roomsRevenue,
        fnbRevenue,
        otherRevenue,
        totalRevenue,
        departmentalExpenses,
        undistributed,
        insurance,
        propertyTax,
        totalExpenses,
        gop,
        gopMargin,
        noi,
        noiMargin,
        cashFlow,
        cumulativeCashFlow,
      });
    }

    // Exit calculations
    const holdYears = inputs.holdPeriodYears;
    const exitProjection = projections[holdYears - 1];
    const exitNoi = exitProjection.noi;
    const exitValue = inputs.exitCapRate > 0 ? exitNoi / inputs.exitCapRate : 0;
    const loanBalanceExit = remainingBalance(loanAmount, inputs.interestRate, inputs.amortYears, holdYears * 12);
    const netSaleProceeds = exitValue - loanBalanceExit;

    // Cash flows for IRR
    const cashFlows = [-equity];
    for (let year = 1; year <= projectionYears; year++) {
      let cf = projections[year - 1].cashFlow;
      if (year === holdYears) {
        cf += netSaleProceeds;
      }
      cashFlows.push(cf);
    }

    const irr = calculateIRR(cashFlows.slice(0, holdYears + 1));
    const totalReturns = cashFlows.slice(1, holdYears + 1).reduce((sum, cf) => sum + cf, 0);
    const equityMultiple = equity > 0 ? totalReturns / equity : 0;
    const dscr = annualDebtService > 0 ? projections[0].noi / annualDebtService : 0;

    // Year 1 metrics
    const year1 = projections[0];

    setResults({
      loanAmount,
      equity,
      annualDebtService,
      year1RoomsRevenue: year1.roomsRevenue,
      year1FnbRevenue: year1.fnbRevenue,
      year1OtherRevenue: year1.otherRevenue,
      year1TotalRevenue: year1.totalRevenue,
      year1Occupancy: year1.occupancy,
      year1Adr: year1.adr,
      year1Revpar: year1.revpar,
      year1Noi: year1.noi,
      year1NoiMargin: year1.noiMargin,
      year1GopMargin: year1.gopMargin,
      year1CashFlow: year1.cashFlow,
      dscr,
      irr,
      equityMultiple,
      exitNoi,
      exitValue,
      loanBalanceExit,
      netSaleProceeds,
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

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    const report = {
      id: Date.now().toString(),
      modelType: 'hotel',
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

  const revenueBreakdownData = results ? [
    { name: 'Rooms', value: results.year1RoomsRevenue, color: '#3b82f6' },
    { name: 'F&B', value: results.year1FnbRevenue, color: '#8b5cf6' },
    { name: 'Other', value: results.year1OtherRevenue, color: '#f59e0b' },
  ] : [];

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
                  background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                  boxShadow: '0 4px 16px rgba(236, 72, 153, 0.3)',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(to top, rgba(255,255,255,0.2), transparent)',
                    borderRadius: 3,
                  },
                }}
              >
                <HotelIcon sx={{ fontSize: 24, color: 'white', position: 'relative', zIndex: 1 }} />
              </Box>
              <Box>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>
                  {inputs.projectName}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {inputs.location} • {inputs.hotelType}
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
              <Button
                variant="contained"
                startIcon={<PlayArrowIcon />}
                onClick={handleRunModel}
                sx={{
                  background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #db2777 0%, #be185d 100%)',
                  },
                }}
              >
                Run Model
              </Button>
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
              ? `linear-gradient(135deg, ${alpha('#ec4899', 0.05)} 0%, ${alpha('#db2777', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#ec4899', 0.03)} 0%, ${alpha('#db2777', 0.03)} 100%)`,
            border: `1px solid ${alpha('#ec4899', 0.2)}`,
          }}
        >
          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
            Comprehensive hotel financial model with detailed revenue mix analysis, department-level expense tracking,
            RevPAR projections, and institutional-grade returns metrics. Supports full-service and select-service hotel types
            with ancillary revenue streams including F&B, meetings, parking, and spa facilities.
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
          <Tab icon={<TrendingUpIcon />} iconPosition="start" label="Analytics" disabled={!showResults} />
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
                        <HotelIcon sx={{ fontSize: 20, color: '#6366f1' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Property Overview
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Hotel details and brand positioning
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
                          Hotel Type
                        </Typography>
                        <FormControl fullWidth size="small">
                          <Select
                            value={inputs.hotelType}
                            onChange={(e) => updateInput('hotelType', e.target.value)}
                          >
                            {HOTEL_TYPES.map((type) => (
                              <MenuItem key={type} value={type}>
                                {type}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Brand Affiliation
                        </Typography>
                        <TextField
                          value={inputs.brandAffiliation}
                          onChange={(e) => updateInput('brandAffiliation', e.target.value)}
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
                          Room Count
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.rooms}
                          onChange={(e) => updateInput('rooms', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 20 }}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Room & Demand */}
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
                        <TrendingUpIcon sx={{ fontSize: 20, color: '#3b82f6' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Room Revenue & Demand
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Occupancy, ADR, and growth assumptions
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Year 1 ADR ($)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.adr}
                          onChange={(e) => updateInput('adr', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 50, step: 5 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Year 1 Occupancy (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.year1Occupancy * 100}
                          onChange={(e) => updateInput('year1Occupancy', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 20, max: 90, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Stabilized Occupancy (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.stabilizedOccupancy * 100}
                          onChange={(e) => updateInput('stabilizedOccupancy', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 30, max: 95, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          ADR Growth Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.adrGrowthRate * 100}
                          onChange={(e) => updateInput('adrGrowthRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          F&B Growth Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.fnbGrowthRate * 100}
                          onChange={(e) => updateInput('fnbGrowthRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Income Growth (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherIncomeGrowthRate * 100}
                          onChange={(e) => updateInput('otherIncomeGrowthRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Ancillary Revenue */}
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
                        <RestaurantIcon sx={{ fontSize: 20, color: '#8b5cf6' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Ancillary Revenue
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          F&B, meetings, parking, spa, and other income
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          F&B Outlet ($/room/day)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.fnbOutletPerRoomDay}
                          onChange={(e) => updateInput('fnbOutletPerRoomDay', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 5 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Banquet ($/group room)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.banquetRevPerGroupRoom}
                          onChange={(e) => updateInput('banquetRevPerGroupRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 5 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Group Room Mix (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.groupRoomPct * 100}
                          onChange={(e) => updateInput('groupRoomPct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 80, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Meeting Revenue ($/room/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.meetingRevPerRoom}
                          onChange={(e) => updateInput('meetingRevPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Parking Revenue ($/room/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.parkingRevPerRoom}
                          onChange={(e) => updateInput('parkingRevPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Spa Revenue ($/room/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.spaRevPerRoom}
                          onChange={(e) => updateInput('spaRevPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 10 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Revenue ($/room/year)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherOperatedRevPerRoom}
                          onChange={(e) => updateInput('otherOperatedRevPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 10 }}
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
                          Department margins and fixed costs
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                          Department Expense (% of Dept Revenue)
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Rooms Dept (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.roomsDeptPct * 100}
                          onChange={(e) => updateInput('roomsDeptPct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 10, max: 80, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          F&B Dept (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.fnbDeptPct * 100}
                          onChange={(e) => updateInput('fnbDeptPct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 20, max: 90, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Other Dept (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.otherDeptPct * 100}
                          onChange={(e) => updateInput('otherDeptPct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 10, max: 80, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12}>
                        <Divider sx={{ my: 1 }} />
                        <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                          Undistributed Expenses ($/room/year)
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Admin & General
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.adminPerRoom}
                          onChange={(e) => updateInput('adminPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 50 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Maintenance
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.maintenancePerRoom}
                          onChange={(e) => updateInput('maintenancePerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 50 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={4}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Utilities
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.utilitiesPerRoom}
                          onChange={(e) => updateInput('utilitiesPerRoom', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, step: 25 }}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Fixed Charges */}
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
                        <AttachMoneyIcon sx={{ fontSize: 20, color: '#10b981' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Fixed Charges & Escalators
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Insurance, taxes, and expense growth
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Insurance (% of Revenue)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.insurancePct * 100}
                          onChange={(e) => updateInput('insurancePct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Property Tax (% of Revenue)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.propertyTaxPct * 100}
                          onChange={(e) => updateInput('propertyTaxPct', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 10, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Expense Growth Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.expenseGrowthRate * 100}
                          onChange={(e) => updateInput('expenseGrowthRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 0, max: 12, step: 0.25 }}
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
                          background: `linear-gradient(135deg, ${alpha('#ef4444', 0.2)} 0%, ${alpha('#dc2626', 0.2)} 100%)`,
                          border: `1px solid ${alpha('#ef4444', 0.3)}`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                        }}
                      >
                        <AccountBalanceIcon sx={{ fontSize: 20, color: '#ef4444' }} />
                      </Box>
                      <Box>
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                          Financing & Exit
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Loan structure and exit assumptions
                        </Typography>
                      </Box>
                    </Stack>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Total Project Cost ($)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.totalProjectCost}
                          onChange={(e) => updateInput('totalProjectCost', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 1000000, step: 100000 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Loan-to-Cost (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.loanToCost * 100}
                          onChange={(e) => updateInput('loanToCost', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 30, max: 85, step: 1 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Interest Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.interestRate * 100}
                          onChange={(e) => updateInput('interestRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 2, max: 15, step: 0.25 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Amortization (Years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.amortYears}
                          onChange={(e) => updateInput('amortYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 5, max: 40 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Hold Period (Years)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.holdPeriodYears}
                          onChange={(e) => updateInput('holdPeriodYears', Number(e.target.value))}
                          fullWidth
                          size="small"
                          inputProps={{ min: 3, max: 15 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                          Exit Cap Rate (%)
                        </Typography>
                        <TextField
                          type="number"
                          value={inputs.exitCapRate * 100}
                          onChange={(e) => updateInput('exitCapRate', Number(e.target.value) / 100)}
                          fullWidth
                          size="small"
                          inputProps={{ min: 5, max: 15, step: 0.25 }}
                        />
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Stack>
            </Grid>

            {/* Right Column - Results */}
            <Grid item xs={12} lg={5}>
              {!showResults || !results ? (
                <Card
                  sx={{
                    p: 6,
                    textAlign: 'center',
                    background: isDark
                      ? `linear-gradient(135deg, ${alpha('#ec4899', 0.1)} 0%, ${alpha('#db2777', 0.1)} 100%)`
                      : `linear-gradient(135deg, ${alpha('#ec4899', 0.05)} 0%, ${alpha('#db2777', 0.05)} 100%)`,
                    border: `2px dashed ${alpha('#ec4899', 0.3)}`,
                  }}
                >
                  <Box
                    sx={{
                      width: 72,
                      height: 72,
                      borderRadius: '50%',
                      background: `linear-gradient(135deg, ${alpha('#ec4899', 0.2)} 0%, ${alpha('#db2777', 0.2)} 100%)`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mx: 'auto',
                      mb: 3,
                    }}
                  >
                    <PlayArrowIcon sx={{ fontSize: 36, color: '#ec4899' }} />
                  </Box>
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>
                    Ready to Analyze
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 4 }}>
                    Configure your hotel parameters on the left, then click "Run Model" to see comprehensive financial analysis,
                    RevPAR projections, and institutional-grade returns metrics.
                  </Typography>
                  <Button
                    variant="contained"
                    size="large"
                    startIcon={<PlayArrowIcon />}
                    onClick={handleRunModel}
                    sx={{
                      background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
                      '&:hover': {
                        background: 'linear-gradient(135deg, #db2777 0%, #be185d 100%)',
                      },
                    }}
                  >
                    Run Model
                  </Button>
                </Card>
              ) : (
                <Stack spacing={3}>
                  {/* Key Returns Card */}
                  <Card
                    sx={{
                      background: 'linear-gradient(135deg, #ec4899 0%, #db2777 100%)',
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
                            bgcolor: results.irr >= 0.14 ? '#10b981' : results.irr >= 0.10 ? '#f59e0b' : '#ef4444',
                            boxShadow: `0 0 8px ${results.irr >= 0.14 ? 'rgba(16, 185, 129, 0.8)' : results.irr >= 0.10 ? 'rgba(245, 158, 11, 0.8)' : 'rgba(239, 68, 68, 0.8)'}`,
                          }}
                        />
                        <Typography variant="caption" sx={{ opacity: 0.9, textTransform: 'uppercase', letterSpacing: 1 }}>
                          RevPAR (Year 1)
                        </Typography>
                      </Stack>
                      <Typography variant="h3" sx={{ fontWeight: 700, mb: 2 }}>
                        {formatCurrency(results.year1Revpar)}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9, lineHeight: 1.6 }}>
                        {formatPercent(results.year1Occupancy)} occupancy × {formatCurrency(results.year1Adr)} ADR
                      </Typography>
                    </CardContent>
                  </Card>

                  {/* Revenue Mix */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                        Revenue Mix (Year 1)
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Rooms Revenue', value: results.year1RoomsRevenue },
                          { label: 'F&B Revenue', value: results.year1FnbRevenue },
                          { label: 'Other Revenue', value: results.year1OtherRevenue },
                          { label: 'Total Revenue', value: results.year1TotalRevenue },
                        ].map((item, idx) => (
                          <Stack
                            key={item.label}
                            direction="row"
                            justifyContent="space-between"
                            alignItems="center"
                            sx={{
                              pb: 2,
                              borderBottom:
                                idx < 3 ? `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}` : 'none',
                              '&:last-child': { pb: 0 },
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

                  {/* Profitability */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                        Profitability (Year 1)
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'GOP Margin', value: formatPercent(results.year1GopMargin) },
                          { label: 'NOI', value: formatCurrency(results.year1Noi) },
                          { label: 'NOI Margin', value: formatPercent(results.year1NoiMargin) },
                          { label: 'Cash Flow', value: formatCurrency(results.year1CashFlow) },
                          { label: 'DSCR', value: results.dscr.toFixed(2) + 'x' },
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

                  {/* Returns */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                        Investment Returns
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Total Project Cost', value: formatCurrency(inputs.totalProjectCost) },
                          { label: 'Equity Invested', value: formatCurrency(results.equity) },
                          { label: 'Annual Debt Service', value: formatCurrency(results.annualDebtService) },
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

                  {/* Exit Scenario */}
                  <Card>
                    <CardContent sx={{ p: 3 }}>
                      <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                        Exit Scenario (Year {inputs.holdPeriodYears})
                      </Typography>
                      <Stack spacing={2}>
                        {[
                          { label: 'Exit Value', value: formatCurrency(results.exitValue) },
                          { label: 'Loan Balance', value: formatCurrency(results.loanBalanceExit) },
                          { label: 'Net Sale Proceeds', value: formatCurrency(results.netSaleProceeds) },
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

                  {/* Deal Analysis */}
                  <Card
                    sx={{
                      border: `2px solid ${
                        results.irr >= 0.18
                          ? '#10b981'
                          : results.irr >= 0.14
                          ? '#3b82f6'
                          : results.irr >= 0.10
                          ? '#f59e0b'
                          : '#ef4444'
                      }`,
                      background: isDark
                        ? alpha(
                            results.irr >= 0.18
                              ? '#10b981'
                              : results.irr >= 0.14
                              ? '#3b82f6'
                              : results.irr >= 0.10
                              ? '#f59e0b'
                              : '#ef4444',
                            0.1
                          )
                        : alpha(
                            results.irr >= 0.18
                              ? '#10b981'
                              : results.irr >= 0.14
                              ? '#3b82f6'
                              : results.irr >= 0.10
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
                              results.irr >= 0.18
                                ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                                : results.irr >= 0.14
                                ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
                                : results.irr >= 0.10
                                ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
                                : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                            color: 'white',
                          }}
                        >
                          {results.irr >= 0.10 ? (
                            <CheckCircleIcon sx={{ fontSize: 24 }} />
                          ) : (
                            <WarningIcon sx={{ fontSize: 24 }} />
                          )}
                        </Box>
                        <Box flex={1}>
                          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                            Deal Analysis
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                            {results.irr >= 0.18 && (
                              <>
                                <strong>Excellent hotel investment</strong> with {formatPercent(results.irr)} IRR and{' '}
                                {results.equityMultiple.toFixed(2)}x equity multiple. Significantly exceeds institutional targets for
                                hotel investments.
                              </>
                            )}
                            {results.irr >= 0.14 && results.irr < 0.18 && (
                              <>
                                <strong>Strong hotel opportunity</strong> with {formatPercent(results.irr)} IRR. Meets institutional
                                return targets with acceptable risk profile for the hotel sector.
                              </>
                            )}
                            {results.irr >= 0.10 && results.irr < 0.14 && (
                              <>
                                <strong>Average returns</strong> with {formatPercent(results.irr)} IRR. Consider optimizing RevPAR
                                growth, ancillary revenue, or cost structure to improve returns.
                              </>
                            )}
                            {results.irr < 0.10 && (
                              <>
                                <strong>Below target returns</strong> with {formatPercent(results.irr)} IRR. Significant risk-return
                                imbalance. Consider passing or restructuring the deal.
                              </>
                            )}
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
      {currentTab === 1 && results && (
        <Box sx={{ px: 4, pb: 4 }}>
          <Stack spacing={4}>
            {/* Break-Even Analysis */}
            {(() => {
              const calculateResultsForBreakEven = (testInputs: HotelInputs) => {
                // Calculate financials for break-even testing
                const occupancy = testInputs.year1Occupancy;
                const adr = testInputs.adr;
                const roomsSold = testInputs.rooms * 365 * occupancy;
                const roomsRevenue = roomsSold * adr;

                // F&B Revenue
                const restaurantRevenue = testInputs.fnbOutletPerRoomDay * testInputs.rooms * 365;
                const banquetRevenue = testInputs.banquetRevPerGroupRoom * roomsSold * testInputs.groupRoomPct;
                const fnbRevenue = restaurantRevenue + banquetRevenue;

                // Other Revenue
                const otherComponents = testInputs.meetingRevPerRoom + testInputs.parkingRevPerRoom + testInputs.spaRevPerRoom + testInputs.otherOperatedRevPerRoom;
                const otherRevenue = testInputs.rooms * otherComponents;

                const totalRevenue = roomsRevenue + fnbRevenue + otherRevenue;

                // Departmental Expenses
                const roomsExpense = roomsRevenue * testInputs.roomsDeptPct;
                const fnbExpense = fnbRevenue * testInputs.fnbDeptPct;
                const otherExpense = otherRevenue * testInputs.otherDeptPct;
                const departmentalExpenses = roomsExpense + fnbExpense + otherExpense;

                // Undistributed Expenses
                const undistributed = testInputs.rooms * (testInputs.adminPerRoom + testInputs.maintenancePerRoom + testInputs.utilitiesPerRoom);

                // Fixed Charges
                const insurance = totalRevenue * testInputs.insurancePct;
                const propertyTax = totalRevenue * testInputs.propertyTaxPct;

                const totalExpenses = departmentalExpenses + undistributed + insurance + propertyTax;
                const noi = totalRevenue - totalExpenses;

                // Debt Service
                const loanAmount = testInputs.totalProjectCost * testInputs.loanToCost;
                const monthlyPayment = annuityPayment(loanAmount, testInputs.interestRate, testInputs.amortYears);
                const debtService = monthlyPayment * 12;

                // Multi-year projections for IRR calculation
                const projections: HotelProjection[] = [];
                let cumulativeCashFlow = 0;

                for (let year = 1; year <= testInputs.holdPeriodYears; year++) {
                  const yearOccupancy = year === 1 ? testInputs.year1Occupancy : testInputs.stabilizedOccupancy;
                  const adrYear = testInputs.adr * Math.pow(1 + testInputs.adrGrowthRate, year - 1);
                  const roomsSoldYear = testInputs.rooms * 365 * yearOccupancy;
                  const roomsRevenueYear = roomsSoldYear * adrYear;

                  const fnbMultiplier = Math.pow(1 + testInputs.fnbGrowthRate, year - 1);
                  const restaurantRevenueYear = testInputs.fnbOutletPerRoomDay * testInputs.rooms * 365 * fnbMultiplier;
                  const banquetRevenueYear = testInputs.banquetRevPerGroupRoom * roomsSoldYear * testInputs.groupRoomPct * fnbMultiplier;
                  const fnbRevenueYear = restaurantRevenueYear + banquetRevenueYear;

                  const otherRevenueYear = testInputs.rooms * otherComponents * Math.pow(1 + testInputs.otherIncomeGrowthRate, year - 1);
                  const totalRevenueYear = roomsRevenueYear + fnbRevenueYear + otherRevenueYear;

                  const roomsExpenseYear = roomsRevenueYear * testInputs.roomsDeptPct;
                  const fnbExpenseYear = fnbRevenueYear * testInputs.fnbDeptPct;
                  const otherExpenseYear = otherRevenueYear * testInputs.otherDeptPct;
                  const departmentalExpensesYear = roomsExpenseYear + fnbExpenseYear + otherExpenseYear;

                  const expenseMultiplier = Math.pow(1 + testInputs.expenseGrowthRate, year - 1);
                  const undistributedYear = testInputs.rooms * (testInputs.adminPerRoom + testInputs.maintenancePerRoom + testInputs.utilitiesPerRoom) * expenseMultiplier;

                  const insuranceYear = totalRevenueYear * testInputs.insurancePct;
                  const propertyTaxYear = totalRevenueYear * testInputs.propertyTaxPct;

                  const totalExpensesYear = departmentalExpensesYear + undistributedYear + insuranceYear + propertyTaxYear;
                  const noiYear = totalRevenueYear - totalExpensesYear;
                  const cashFlowYear = noiYear - debtService;
                  cumulativeCashFlow += cashFlowYear;

                  projections.push({
                    year,
                    occupancy: yearOccupancy,
                    adr: adrYear,
                    revpar: adrYear * yearOccupancy,
                    roomsRevenue: roomsRevenueYear,
                    fnbRevenue: fnbRevenueYear,
                    otherRevenue: otherRevenueYear,
                    totalRevenue: totalRevenueYear,
                    departmentalExpenses: departmentalExpensesYear,
                    undistributed: undistributedYear,
                    insurance: insuranceYear,
                    propertyTax: propertyTaxYear,
                    totalExpenses: totalExpensesYear,
                    gop: totalRevenueYear - departmentalExpensesYear,
                    gopMargin: totalRevenueYear > 0 ? (totalRevenueYear - departmentalExpensesYear) / totalRevenueYear : 0,
                    noi: noiYear,
                    noiMargin: totalRevenueYear > 0 ? noiYear / totalRevenueYear : 0,
                    cashFlow: cashFlowYear,
                    cumulativeCashFlow,
                  });
                }

                // IRR calculation
                const exitNoi = projections[projections.length - 1].noi;
                const exitValue = testInputs.exitCapRate > 0 ? exitNoi / testInputs.exitCapRate : 0;
                const loanBalanceExit = remainingBalance(loanAmount, testInputs.interestRate, testInputs.amortYears, testInputs.holdPeriodYears * 12);
                const netSaleProceeds = exitValue - loanBalanceExit;

                const equity = testInputs.totalProjectCost - loanAmount;
                const cashFlows = [-equity];
                for (let year = 1; year <= testInputs.holdPeriodYears; year++) {
                  let cf = projections[year - 1].cashFlow;
                  if (year === testInputs.holdPeriodYears) {
                    cf += netSaleProceeds;
                  }
                  cashFlows.push(cf);
                }

                const irr = calculateIRR(cashFlows);

                return { noi, debtService, irr, projections };
              };

              const breakEvenMetrics = calculateBreakEvenMetrics(
                inputs,
                results,
                calculateResultsForBreakEven,
                0.14 // 14% target IRR for hotel investments
              );

              return <BreakEvenAnalysis metrics={breakEvenMetrics} />;
            })()}

            <Divider sx={{ my: 4 }} />

            {/* Existing Charts */}
            <Grid container spacing={3}>
              {/* Revenue Mix Pie Chart */}
              <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Revenue Mix (Year 1)
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={revenueBreakdownData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {revenueBreakdownData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* RevPAR Trend */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    RevPAR Growth
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${Math.round(value)}`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Line type="monotone" dataKey="revpar" stroke="#3b82f6" name="RevPAR" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Revenue Streams Over Time */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Revenue Streams Over Time
                  </Typography>
                  <Box sx={{ height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Line type="monotone" dataKey="roomsRevenue" stroke="#3b82f6" name="Rooms Revenue" strokeWidth={2} />
                        <Line type="monotone" dataKey="fnbRevenue" stroke="#8b5cf6" name="F&B Revenue" strokeWidth={2} />
                        <Line type="monotone" dataKey="otherRevenue" stroke="#f59e0b" name="Other Revenue" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* NOI Margin Trend */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Profitability Margins
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
                        <Tooltip formatter={(value: number) => formatPercent(value)} />
                        <Legend />
                        <Line type="monotone" dataKey="gopMargin" stroke="#4ECDC4" name="GOP Margin" strokeWidth={2} />
                        <Line type="monotone" dataKey="noiMargin" stroke="#95E1D3" name="NOI Margin" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Cash Flow */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Cash Flow Projection
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={results.projections}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                        <XAxis dataKey="year" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Bar dataKey="cashFlow" fill="#36A2EB" name="Annual Cash Flow" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            </Grid>
          </Stack>
        </Box>
      )}

      {/* Documentation Tab */}
      {currentTab === 2 && (
        <Box>
          <Tabs value={docTab} onChange={(e, v) => setDocTab(v)} sx={{ borderBottom: 1, borderColor: 'divider', px: 4, pt: 2 }}>
            <Tab label="Quick Reference" />
            <Tab label="User Guide" />
            <Tab label="Delivery Summary" />
          </Tabs>
          <Box sx={{ p: 4 }}>
            {docTab === 0 && <MarkdownViewer content={HOTEL_QUICK_REFERENCE} />}
            {docTab === 1 && <MarkdownViewer content={HOTEL_USER_GUIDE} />}
            {docTab === 2 && <MarkdownViewer content={HOTEL_DELIVERY_SUMMARY} />}
          </Box>
        </Box>
      )}
    </Box>
  );
};
