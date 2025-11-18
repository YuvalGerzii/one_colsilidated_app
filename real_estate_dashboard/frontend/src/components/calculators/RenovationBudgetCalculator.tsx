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
  Divider,
} from '@mui/material';
import {
  Build as BuildIcon,
  Home as HomeIcon,
  AttachMoney as AttachMoneyIcon,
  Landscape as LandscapeIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  Construction as ConstructionIcon,
  AccountBalance as AccountBalanceIcon,
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
} from 'recharts';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { RenovationBudgetInputs, RenovationBudgetResults } from '../../types/calculatorTypes';
import {
  formatCurrency,
  formatPercent,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';

const DEFAULT_INPUTS: RenovationBudgetInputs = {
  projectName: 'Oakwood Apartments Renovation',
  location: 'Phoenix, AZ',
  analyst: '',
  propertyType: 'Multifamily',
  totalUnits: 24,
  squareFootagePerUnit: 850,
  totalSquareFootage: 20400,
  kitchenRenovationPerUnit: 12000,
  bathroomRenovationPerUnit: 8000,
  flooringPerUnit: 3500,
  paintPerUnit: 1200,
  appliancesPerUnit: 2500,
  fixturesPerUnit: 1500,
  hvacPerUnit: 4000,
  electricalPerUnit: 2000,
  plumbingPerUnit: 2500,
  otherPerUnit: 1000,
  commonAreaRenovation: 50000,
  exteriorImprovements: 75000,
  landscaping: 20000,
  parkingLotRepaving: 30000,
  roofReplacement: 0,
  structuralRepairs: 0,
  contingencyPct: 10,
  softCostsPct: 8,
  currentAvgRent: 1200,
  postRenoAvgRent: 1500,
  currentOccupancy: 75,
  stabilizedOccupancy: 95,
  monthsToComplete: 8,
  unitsRenovatedPerMonth: 3,
  financingCostPct: 6,
  holdingCostsMonthly: 5000,
  tags: '',
  purpose: '',
  references: '',
  notes: '',
};

const COLORS = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];

export const RenovationBudgetCalculator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [currentTab, setCurrentTab] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');

  const [inputs, setInputs] = useState<RenovationBudgetInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<RenovationBudgetResults>({
    totalUnits: 0,
    interiorPerUnit: 0,
    totalInteriorCosts: 0,
    exteriorCosts: 0,
    majorCapital: 0,
    hardCosts: 0,
    contingency: 0,
    softCosts: 0,
    totalBudget: 0,
    financingCosts: 0,
    totalHoldingCosts: 0,
    allInCost: 0,
    costPerUnit: 0,
    costPerSf: 0,
    currentMonthlyRevenue: 0,
    stabilizedMonthlyRevenue: 0,
    monthlyRevenueIncrease: 0,
    annualRevenueIncrease: 0,
    renovationYield: 0,
    paybackYears: 0,
    breakdown: {
      kitchen: 0,
      bathroom: 0,
      flooring: 0,
      paint: 0,
      appliances: 0,
      fixtures: 0,
      hvac: 0,
      electrical: 0,
      plumbing: 0,
      other: 0,
      commonAreas: 0,
      exterior: 0,
      landscaping: 0,
      parking: 0,
      roof: 0,
      structural: 0,
    },
  });

  const updateInput = <K extends keyof RenovationBudgetInputs>(
    key: K,
    value: RenovationBudgetInputs[K]
  ) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  useEffect(() => {
    if (!showResults) return;

    const totalUnits = inputs.totalUnits;

    // Calculate per-unit interior costs
    const interiorPerUnit =
      inputs.kitchenRenovationPerUnit +
      inputs.bathroomRenovationPerUnit +
      inputs.flooringPerUnit +
      inputs.paintPerUnit +
      inputs.appliancesPerUnit +
      inputs.fixturesPerUnit +
      inputs.hvacPerUnit +
      inputs.electricalPerUnit +
      inputs.plumbingPerUnit +
      inputs.otherPerUnit;

    const totalInteriorCosts = interiorPerUnit * totalUnits;

    // Exterior and common area costs
    const exteriorCosts =
      inputs.commonAreaRenovation +
      inputs.exteriorImprovements +
      inputs.landscaping +
      inputs.parkingLotRepaving;

    // Major capital items
    const majorCapital = inputs.roofReplacement + inputs.structuralRepairs;

    // Hard costs subtotal
    const hardCosts = totalInteriorCosts + exteriorCosts + majorCapital;

    // Contingency and soft costs
    const contingency = hardCosts * (inputs.contingencyPct / 100);
    const softCosts = hardCosts * (inputs.softCostsPct / 100);

    // Total renovation budget
    const totalBudget = hardCosts + contingency + softCosts;

    // Financing costs
    const months = inputs.monthsToComplete;
    const financingRate = inputs.financingCostPct / 100;
    const avgOutstandingBalance = totalBudget / 2; // Assume linear drawdown
    const financingCosts = (avgOutstandingBalance * financingRate * months) / 12;

    // Holding costs
    const totalHoldingCosts = inputs.holdingCostsMonthly * months;

    // All-in cost
    const allInCost = totalBudget + financingCosts + totalHoldingCosts;

    // Revenue impact analysis
    const currentMonthlyRevenue =
      inputs.currentAvgRent * totalUnits * (inputs.currentOccupancy / 100);
    const stabilizedMonthlyRevenue =
      inputs.postRenoAvgRent * totalUnits * (inputs.stabilizedOccupancy / 100);
    const monthlyRevenueIncrease = stabilizedMonthlyRevenue - currentMonthlyRevenue;
    const annualRevenueIncrease = monthlyRevenueIncrease * 12;

    // ROI calculations
    let renovationYield = 0;
    let paybackYears = 999;
    if (allInCost > 0) {
      renovationYield = annualRevenueIncrease / allInCost;
      paybackYears =
        annualRevenueIncrease > 0 ? allInCost / annualRevenueIncrease : 999;
    }

    // Cost per unit and per SF
    const costPerUnit = totalBudget / totalUnits;
    const costPerSf =
      inputs.totalSquareFootage > 0 ? totalBudget / inputs.totalSquareFootage : 0;

    // Breakdown by category
    const breakdown = {
      kitchen: inputs.kitchenRenovationPerUnit * totalUnits,
      bathroom: inputs.bathroomRenovationPerUnit * totalUnits,
      flooring: inputs.flooringPerUnit * totalUnits,
      paint: inputs.paintPerUnit * totalUnits,
      appliances: inputs.appliancesPerUnit * totalUnits,
      fixtures: inputs.fixturesPerUnit * totalUnits,
      hvac: inputs.hvacPerUnit * totalUnits,
      electrical: inputs.electricalPerUnit * totalUnits,
      plumbing: inputs.plumbingPerUnit * totalUnits,
      other: inputs.otherPerUnit * totalUnits,
      commonAreas: inputs.commonAreaRenovation,
      exterior: inputs.exteriorImprovements,
      landscaping: inputs.landscaping,
      parking: inputs.parkingLotRepaving,
      roof: inputs.roofReplacement,
      structural: inputs.structuralRepairs,
    };

    setResults({
      totalUnits,
      interiorPerUnit,
      totalInteriorCosts,
      exteriorCosts,
      majorCapital,
      hardCosts,
      contingency,
      softCosts,
      totalBudget,
      financingCosts,
      totalHoldingCosts,
      allInCost,
      costPerUnit,
      costPerSf,
      currentMonthlyRevenue,
      stabilizedMonthlyRevenue,
      monthlyRevenueIncrease,
      annualRevenueIncrease,
      renovationYield,
      paybackYears,
      breakdown,
    });
  }, [inputs, showResults]);

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    saveToLocalStorage('renovation-budget', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });

    setSaveMessage('Report saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  // Chart data
  const budgetPieData = [
    { name: 'Interior Renovations', value: results.totalInteriorCosts },
    { name: 'Exterior & Common', value: results.exteriorCosts },
    { name: 'Major Capital', value: results.majorCapital },
    { name: 'Contingency', value: results.contingency },
    { name: 'Soft Costs', value: results.softCosts },
  ];

  const interiorBarData = [
    { name: 'Kitchen', value: results.breakdown.kitchen },
    { name: 'Bathroom', value: results.breakdown.bathroom },
    { name: 'HVAC', value: results.breakdown.hvac },
    { name: 'Flooring', value: results.breakdown.flooring },
    { name: 'Appliances', value: results.breakdown.appliances },
    { name: 'Electrical', value: results.breakdown.electrical },
    { name: 'Plumbing', value: results.breakdown.plumbing },
    { name: 'Fixtures', value: results.breakdown.fixtures },
    { name: 'Paint', value: results.breakdown.paint },
    { name: 'Other', value: results.breakdown.other },
  ].filter((item) => item.value > 0);

  const revenueData = [
    { name: 'Current Monthly Revenue', value: results.currentMonthlyRevenue },
    { name: 'Stabilized Monthly Revenue', value: results.stabilizedMonthlyRevenue },
  ];

  const cardBgColor = isDark ? 'rgba(30, 30, 30, 0.7)' : 'rgba(255, 255, 255, 0.9)';

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: isDark ? '#121212' : '#f5f7fa', py: 4 }}>
      {/* Header */}
      <Box sx={{ px: 4, mb: 4 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}>
          <Stack direction="row" alignItems="center" spacing={2}>
            <BuildIcon sx={{ fontSize: 40, color: 'primary.main' }} />
            <Typography variant="h4" fontWeight="bold">
              Renovation Budget Analyzer
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
                  <HomeIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Property Profile
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Project Name"
                    value={inputs.projectName}
                    onChange={(e) => updateInput('projectName', e.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Location"
                    value={inputs.location}
                    onChange={(e) => updateInput('location', e.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Analyst"
                    value={inputs.analyst}
                    onChange={(e) => updateInput('analyst', e.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Property Type"
                    value={inputs.propertyType}
                    onChange={(e) => updateInput('propertyType', e.target.value)}
                    fullWidth
                  />
                  <TextField
                    label="Total Units"
                    type="number"
                    value={inputs.totalUnits}
                    onChange={(e) => updateInput('totalUnits', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Square Footage Per Unit"
                    type="number"
                    value={inputs.squareFootagePerUnit}
                    onChange={(e) => updateInput('squareFootagePerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Total Square Footage"
                    type="number"
                    value={inputs.totalSquareFootage}
                    onChange={(e) => updateInput('totalSquareFootage', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Interior Renovation Costs */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <ConstructionIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Interior Renovation Costs
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Kitchen Renovation ($/unit)"
                    type="number"
                    value={inputs.kitchenRenovationPerUnit}
                    onChange={(e) => updateInput('kitchenRenovationPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Bathroom Renovation ($/unit)"
                    type="number"
                    value={inputs.bathroomRenovationPerUnit}
                    onChange={(e) => updateInput('bathroomRenovationPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Flooring ($/unit)"
                    type="number"
                    value={inputs.flooringPerUnit}
                    onChange={(e) => updateInput('flooringPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Paint ($/unit)"
                    type="number"
                    value={inputs.paintPerUnit}
                    onChange={(e) => updateInput('paintPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Appliances ($/unit)"
                    type="number"
                    value={inputs.appliancesPerUnit}
                    onChange={(e) => updateInput('appliancesPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Fixtures & Hardware ($/unit)"
                    type="number"
                    value={inputs.fixturesPerUnit}
                    onChange={(e) => updateInput('fixturesPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Systems & Mechanical */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <BuildIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Systems & Mechanical
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="HVAC ($/unit)"
                    type="number"
                    value={inputs.hvacPerUnit}
                    onChange={(e) => updateInput('hvacPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Electrical ($/unit)"
                    type="number"
                    value={inputs.electricalPerUnit}
                    onChange={(e) => updateInput('electricalPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Plumbing ($/unit)"
                    type="number"
                    value={inputs.plumbingPerUnit}
                    onChange={(e) => updateInput('plumbingPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Other Interior Costs ($/unit)"
                    type="number"
                    value={inputs.otherPerUnit}
                    onChange={(e) => updateInput('otherPerUnit', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Exterior & Common Areas */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <LandscapeIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Exterior & Common Areas
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Common Area Renovation ($)"
                    type="number"
                    value={inputs.commonAreaRenovation}
                    onChange={(e) => updateInput('commonAreaRenovation', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Exterior Improvements ($)"
                    type="number"
                    value={inputs.exteriorImprovements}
                    onChange={(e) => updateInput('exteriorImprovements', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Landscaping ($)"
                    type="number"
                    value={inputs.landscaping}
                    onChange={(e) => updateInput('landscaping', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Parking Lot ($)"
                    type="number"
                    value={inputs.parkingLotRepaving}
                    onChange={(e) => updateInput('parkingLotRepaving', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Major Capital Items */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AssessmentIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Major Capital Items
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Roof Replacement ($)"
                    type="number"
                    value={inputs.roofReplacement}
                    onChange={(e) => updateInput('roofReplacement', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Structural Repairs ($)"
                    type="number"
                    value={inputs.structuralRepairs}
                    onChange={(e) => updateInput('structuralRepairs', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Budget Adjustments */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AttachMoneyIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Budget Adjustments
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Contingency (%)"
                    type="number"
                    value={inputs.contingencyPct}
                    onChange={(e) => updateInput('contingencyPct', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Soft Costs (%)"
                    type="number"
                    value={inputs.softCostsPct}
                    onChange={(e) => updateInput('softCostsPct', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Revenue Impact */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AttachMoneyIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Revenue Impact
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Current Avg Rent ($/month)"
                    type="number"
                    value={inputs.currentAvgRent}
                    onChange={(e) => updateInput('currentAvgRent', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Post-Renovation Avg Rent ($/month)"
                    type="number"
                    value={inputs.postRenoAvgRent}
                    onChange={(e) => updateInput('postRenoAvgRent', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Current Occupancy (%)"
                    type="number"
                    value={inputs.currentOccupancy}
                    onChange={(e) => updateInput('currentOccupancy', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Stabilized Occupancy (%)"
                    type="number"
                    value={inputs.stabilizedOccupancy}
                    onChange={(e) => updateInput('stabilizedOccupancy', Number(e.target.value))}
                    fullWidth
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Timeline & Financing */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: cardBgColor, backdropFilter: 'blur(10px)' }}>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} mb={2}>
                  <AccountBalanceIcon color="primary" />
                  <Typography variant="h6" fontWeight="bold">
                    Timeline & Financing
                  </Typography>
                </Stack>
                <Stack spacing={2}>
                  <TextField
                    label="Project Duration (months)"
                    type="number"
                    value={inputs.monthsToComplete}
                    onChange={(e) => updateInput('monthsToComplete', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Units Renovated Per Month"
                    type="number"
                    value={inputs.unitsRenovatedPerMonth}
                    onChange={(e) => updateInput('unitsRenovatedPerMonth', Number(e.target.value))}
                    fullWidth
                  />
                  <TextField
                    label="Financing Interest Rate (%)"
                    type="number"
                    value={inputs.financingCostPct}
                    onChange={(e) => updateInput('financingCostPct', Number(e.target.value))}
                    fullWidth
                    inputProps={{ step: 0.25 }}
                  />
                  <TextField
                    label="Monthly Holding Costs ($)"
                    type="number"
                    value={inputs.holdingCostsMonthly}
                    onChange={(e) => updateInput('holdingCostsMonthly', Number(e.target.value))}
                    fullWidth
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
              <Tab label="Documentation" />
            </Tabs>

            {/* Summary Tab */}
            {currentTab === 0 && (
              <Box sx={{ p: 4 }}>
                <Grid container spacing={3}>
                  {/* Budget Summary */}
                  <Grid item xs={12} md={6}>
                    <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                      <Typography variant="h6" fontWeight="bold" gutterBottom color="primary">
                        Renovation Budget Summary
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      <Stack spacing={1.5}>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Total Units:</Typography>
                          <Typography fontWeight="bold">{results.totalUnits}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Hard Costs:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.hardCosts)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Contingency:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.contingency)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Soft Costs:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.softCosts)}</Typography>
                        </Box>
                        <Divider />
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary" fontWeight="bold">Total Renovation Budget:</Typography>
                          <Typography fontWeight="bold" color="primary.main">{formatCurrency(results.totalBudget)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Financing Costs:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.financingCosts)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Holding Costs:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.totalHoldingCosts)}</Typography>
                        </Box>
                        <Divider />
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary" fontWeight="bold">All-In Cost:</Typography>
                          <Typography fontWeight="bold" color="primary.main">{formatCurrency(results.allInCost)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Cost Per Unit:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.costPerUnit)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Cost Per SF:</Typography>
                          <Typography fontWeight="bold">${results.costPerSf.toFixed(2)}</Typography>
                        </Box>
                      </Stack>
                    </Paper>
                  </Grid>

                  {/* ROI Analysis */}
                  <Grid item xs={12} md={6}>
                    <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                      <Typography variant="h6" fontWeight="bold" gutterBottom color="primary">
                        Return on Investment Analysis
                      </Typography>
                      <Divider sx={{ mb: 2 }} />
                      <Stack spacing={1.5}>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Current Monthly Revenue:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.currentMonthlyRevenue)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Stabilized Monthly Revenue:</Typography>
                          <Typography fontWeight="bold">{formatCurrency(results.stabilizedMonthlyRevenue)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Monthly Revenue Increase:</Typography>
                          <Typography fontWeight="bold" color="success.main">{formatCurrency(results.monthlyRevenueIncrease)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary">Annual Revenue Increase:</Typography>
                          <Typography fontWeight="bold" color="success.main">{formatCurrency(results.annualRevenueIncrease)}</Typography>
                        </Box>
                        <Divider />
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary" fontWeight="bold">Renovation Yield:</Typography>
                          <Typography fontWeight="bold" color="primary.main">{formatPercent(results.renovationYield * 100)}</Typography>
                        </Box>
                        <Box display="flex" justifyContent="space-between">
                          <Typography color="text.secondary" fontWeight="bold">Payback Period:</Typography>
                          <Typography fontWeight="bold" color="primary.main">
                            {results.paybackYears < 100 ? `${results.paybackYears.toFixed(1)} years` : 'N/A'}
                          </Typography>
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
                  {/* Budget Breakdown Pie Chart */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Budget Breakdown
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={budgetPieData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={(entry) => `${entry.name}: ${formatCurrency(entry.value)}`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {budgetPieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </Box>

                  {/* Interior Costs Breakdown */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Interior Renovation Costs by Category
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={interiorBarData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Bar dataKey="value" fill="#4BC0C0" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>

                  {/* Revenue Impact */}
                  <Box>
                    <Typography variant="h6" fontWeight="bold" gutterBottom>
                      Revenue Impact
                    </Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={revenueData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Bar dataKey="value" fill="#36A2EB" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </Stack>
              </Box>
            )}

            {/* Documentation Tab */}
            {currentTab === 2 && (
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
                      The Renovation Budget Analyzer helps you estimate the total costs and ROI of a property
                      renovation project. It breaks down costs by category, calculates financing and holding costs,
                      and projects the revenue impact to determine renovation yield and payback period.
                    </Typography>
                  </Paper>

                  <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Key Calculations
                    </Typography>
                    <Stack spacing={1}>
                      <Typography variant="body2"><strong>Interior Per Unit:</strong> Sum of all per-unit interior renovation costs</Typography>
                      <Typography variant="body2"><strong>Total Interior Costs:</strong> Interior Per Unit × Total Units</Typography>
                      <Typography variant="body2"><strong>Exterior Costs:</strong> Sum of common areas, exterior, landscaping, and parking</Typography>
                      <Typography variant="body2"><strong>Major Capital:</strong> Roof replacement + Structural repairs</Typography>
                      <Typography variant="body2"><strong>Hard Costs:</strong> Total Interior + Exterior + Major Capital</Typography>
                      <Typography variant="body2"><strong>Contingency:</strong> Hard Costs × Contingency %</Typography>
                      <Typography variant="body2"><strong>Soft Costs:</strong> Hard Costs × Soft Costs %</Typography>
                      <Typography variant="body2"><strong>Total Budget:</strong> Hard Costs + Contingency + Soft Costs</Typography>
                      <Typography variant="body2"><strong>Financing Costs:</strong> (Avg Outstanding Balance × Rate × Months) / 12</Typography>
                      <Typography variant="body2"><strong>Holding Costs:</strong> Monthly Holding Costs × Project Duration</Typography>
                      <Typography variant="body2"><strong>All-In Cost:</strong> Total Budget + Financing + Holding Costs</Typography>
                      <Typography variant="body2"><strong>Revenue Increase:</strong> (Post-Reno Rent × Stabilized Occ.) - (Current Rent × Current Occ.)</Typography>
                      <Typography variant="body2"><strong>Renovation Yield:</strong> Annual Revenue Increase / All-In Cost</Typography>
                      <Typography variant="body2"><strong>Payback Period:</strong> All-In Cost / Annual Revenue Increase</Typography>
                    </Stack>
                  </Paper>

                  <Paper elevation={0} sx={{ p: 3, bgcolor: isDark ? 'rgba(40, 40, 40, 0.5)' : 'rgba(240, 240, 240, 0.7)' }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      Key Assumptions
                    </Typography>
                    <Stack spacing={1}>
                      <Typography variant="body2">• Financing assumes linear drawdown (average outstanding = 50% of total budget)</Typography>
                      <Typography variant="body2">• Per-unit costs are applied uniformly across all units</Typography>
                      <Typography variant="body2">• Contingency and soft costs are calculated as percentages of hard costs only</Typography>
                      <Typography variant="body2">• Revenue impact assumes all units are renovated to the same standard</Typography>
                      <Typography variant="body2">• Occupancy rates are applied to the total unit count</Typography>
                      <Typography variant="body2">• Renovation yield is calculated on an annual basis</Typography>
                      <Typography variant="body2">• Does not account for phased renovation or partial unit completion</Typography>
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
