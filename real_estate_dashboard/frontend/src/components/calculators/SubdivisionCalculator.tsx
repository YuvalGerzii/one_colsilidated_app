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
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Landscape as LandscapeIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as AttachMoneyIcon,
  Build as BuildIcon,
  Assessment as AssessmentIcon,
  Description as DescriptionIcon,
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  PlayArrow as PlayArrowIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
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
import { SubdivisionInputs, SubdivisionResults, SubdivisionProjection } from '../../types/calculatorTypes';
import {
  formatCurrency,
  formatPercent,
  calculateIRR,
  saveToLocalStorage,
} from '../../utils/calculatorUtils';
import { BreakEvenAnalysis } from './advanced/BreakEvenAnalysis';
import { calculateBreakEvenMetrics } from '../../utils/breakEvenCalculations';
import { StressTesting } from './advanced/StressTesting';
import { calculateStressTestResults } from '../../utils/stressTestingCalculations';
import { STRESS_SCENARIOS } from '../../constants/stressTestingScenarios';
import { WaterfallChart } from './advanced/WaterfallChart';
import { calculateDevelopmentCostWaterfall } from '../../utils/waterfallCalculations';

const DEFAULT_INPUTS: SubdivisionInputs = {
  projectName: 'Oak Ridge Estates',
  location: 'Austin, TX',
  analyst: '',
  totalAcres: 50,
  landCostPerAcre: 75000,
  closingCosts: 50000,
  dueDiligenceCosts: 25000,
  totalLots: 75,
  averageLotSizeAcres: 0.5,
  lotTypes: {
    standard: { count: 45, size: 0.4, salePrice: 125000 },
    premium: { count: 20, size: 0.6, salePrice: 165000 },
    estate: { count: 10, size: 1.0, salePrice: 250000 },
  },
  siteworkPerAcre: 15000,
  streetsPerFoot: 150,
  totalStreetFeet: 8000,
  waterSewerPerLot: 12000,
  stormwaterPerAcre: 8000,
  landscapingPerAcre: 5000,
  amenitiesCost: 500000,
  contingencyPct: 10,
  engineeringPct: 5,
  architecturePct: 2,
  legalPermitsPct: 3,
  marketingSalesPct: 3,
  developerFeePct: 5,
  absorptionMonths: 24,
  salesStartMonth: 12,
  priceEscalationPct: 3,
  ltc: 70,
  interestRate: 7.5,
  loanTermYears: 3,
  loanFeesPct: 2,
  propertyTaxRate: 1.25,
  insuranceAnnual: 15000,
  maintenanceMonthly: 2500,
};

export const SubdivisionCalculator: React.FC = () => {
  const navigate = useNavigate();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [inputs, setInputs] = useState<SubdivisionInputs>(DEFAULT_INPUTS);
  const [results, setResults] = useState<SubdivisionResults | null>(null);
  const [showResults, setShowResults] = useState(false);
  const [currentTab, setCurrentTab] = useState(0);
  const [saveMessage, setSaveMessage] = useState('');

  const handleInputChange = (field: keyof SubdivisionInputs, value: any) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const handleLotTypeChange = (type: 'standard' | 'premium' | 'estate', field: string, value: number) => {
    setInputs(prev => ({
      ...prev,
      lotTypes: {
        ...prev.lotTypes,
        [type]: {
          ...prev.lotTypes[type],
          [field]: value,
        },
      },
    }));
  };

  useEffect(() => {
    if (!showResults) return;

    // Land & Acquisition
    const totalLandCost = inputs.totalAcres * inputs.landCostPerAcre;
    const totalAcquisitionCost = totalLandCost + inputs.closingCosts + inputs.dueDiligenceCosts;
    const costPerLot = totalAcquisitionCost / inputs.totalLots;
    const costPerAcre = totalAcquisitionCost / inputs.totalAcres;

    // Development Costs
    const siteworkCost = inputs.totalAcres * inputs.siteworkPerAcre;
    const streetsCost = inputs.totalStreetFeet * inputs.streetsPerFoot;
    const utilitiesCost = inputs.totalLots * inputs.waterSewerPerLot;
    const stormwaterCost = inputs.totalAcres * inputs.stormwaterPerAcre;
    const landscapingCost = inputs.totalAcres * inputs.landscapingPerAcre;
    const amenitiesCost = inputs.amenitiesCost;
    const totalHardCosts = siteworkCost + streetsCost + utilitiesCost + stormwaterCost + landscapingCost + amenitiesCost;
    const hardCostPerLot = totalHardCosts / inputs.totalLots;
    const contingencyCost = totalHardCosts * (inputs.contingencyPct / 100);

    // Soft Costs (before marketing and developer fee)
    const engineeringCost = totalHardCosts * (inputs.engineeringPct / 100);
    const architectureCost = totalHardCosts * (inputs.architecturePct / 100);
    const legalPermitsCost = totalHardCosts * (inputs.legalPermitsPct / 100);

    // Calculate gross sales revenue
    const standardRevenue = inputs.lotTypes.standard.count * inputs.lotTypes.standard.salePrice;
    const premiumRevenue = inputs.lotTypes.premium.count * inputs.lotTypes.premium.salePrice;
    const estateRevenue = inputs.lotTypes.estate.count * inputs.lotTypes.estate.salePrice;
    const grossSalesRevenue = standardRevenue + premiumRevenue + estateRevenue;
    const averageSalePricePerLot = grossSalesRevenue / inputs.totalLots;

    // Marketing and Developer Fee (based on sales)
    const marketingSalesCost = grossSalesRevenue * (inputs.marketingSalesPct / 100);
    const totalDevelopmentCost = totalAcquisitionCost + totalHardCosts + contingencyCost;
    const developerFee = totalDevelopmentCost * (inputs.developerFeePct / 100);
    const totalSoftCosts = engineeringCost + architectureCost + legalPermitsCost + marketingSalesCost + developerFee;

    // Total Project Cost
    const allInCostPerLot = (totalDevelopmentCost + totalSoftCosts) / inputs.totalLots;

    // Financing
    const loanAmount = totalDevelopmentCost * (inputs.ltc / 100);
    const loanFees = loanAmount * (inputs.loanFeesPct / 100);
    const equityRequired = totalDevelopmentCost - loanAmount + loanFees;

    // Monthly projections
    const developmentMonths = inputs.salesStartMonth;
    const salesMonths = inputs.absorptionMonths;
    const totalMonths = developmentMonths + salesMonths;
    const lotsPerMonth = inputs.totalLots / salesMonths;

    const projections: SubdivisionProjection[] = [];
    let cumulativeCosts = totalAcquisitionCost;
    let cumulativeRevenue = 0;
    let cumulativeLotsSold = 0;
    let cumulativeCashFlow = -equityRequired;
    let loanBalance = loanAmount;
    let totalInterestCost = 0;

    for (let month = 1; month <= totalMonths; month++) {
      let phase: 'acquisition' | 'development' | 'sales' | 'completed' = 'development';
      let monthlyCosts = 0;
      let monthlyRevenue = 0;
      let lotsSold = 0;
      let interestExpense = 0;

      if (month === 1) {
        phase = 'acquisition';
      } else if (month <= developmentMonths) {
        phase = 'development';
        // Spread development costs evenly
        monthlyCosts = (totalHardCosts + contingencyCost + engineeringCost + architectureCost + legalPermitsCost) / developmentMonths;
        monthlyCosts += inputs.propertyTaxRate / 100 / 12 * totalLandCost;
        monthlyCosts += inputs.insuranceAnnual / 12;
        monthlyCosts += inputs.maintenanceMonthly;
      } else if (month <= developmentMonths + salesMonths) {
        phase = 'sales';
        // Calculate lots sold this month
        lotsSold = Math.min(lotsPerMonth, inputs.totalLots - cumulativeLotsSold);

        // Calculate revenue with price escalation
        const yearsElapsed = (month - developmentMonths) / 12;
        const priceMultiplier = Math.pow(1 + inputs.priceEscalationPct / 100, yearsElapsed);
        const avgPrice = averageSalePricePerLot * priceMultiplier;
        monthlyRevenue = lotsSold * avgPrice;

        // Ongoing costs
        monthlyCosts = inputs.propertyTaxRate / 100 / 12 * totalLandCost;
        monthlyCosts += inputs.insuranceAnnual / 12;
        monthlyCosts += inputs.maintenanceMonthly;
        monthlyCosts += marketingSalesCost / salesMonths;
      } else {
        phase = 'completed';
      }

      // Interest expense
      if (loanBalance > 0) {
        interestExpense = loanBalance * (inputs.interestRate / 100 / 12);
        totalInterestCost += interestExpense;
      }

      // Update cumulative values
      cumulativeCosts += monthlyCosts + interestExpense;
      cumulativeRevenue += monthlyRevenue;
      cumulativeLotsSold += lotsSold;

      // Pay down loan with sales proceeds
      if (monthlyRevenue > 0 && loanBalance > 0) {
        const loanPaydown = Math.min(monthlyRevenue * 0.7, loanBalance); // Use 70% of sales to pay down
        loanBalance -= loanPaydown;
      }

      const cashFlow = monthlyRevenue - monthlyCosts - interestExpense;
      cumulativeCashFlow += cashFlow;

      projections.push({
        month,
        phase,
        lotsSold,
        cumulativeLotsSold,
        monthlyRevenue,
        cumulativeRevenue,
        monthlyCosts: monthlyCosts + interestExpense,
        cumulativeCosts,
        loanBalance,
        interestExpense,
        cashFlow,
        cumulativeCashFlow,
      });
    }

    const netSalesRevenue = cumulativeRevenue;
    const grossProfit = netSalesRevenue - (totalDevelopmentCost + totalSoftCosts + totalInterestCost + loanFees);
    const grossProfitMargin = netSalesRevenue > 0 ? (grossProfit / netSalesRevenue) * 100 : 0;
    const netProfit = grossProfit;
    const netProfitMargin = netSalesRevenue > 0 ? (netProfit / netSalesRevenue) * 100 : 0;
    const roi = equityRequired > 0 ? (netProfit / equityRequired) * 100 : 0;

    // IRR calculation
    const cashFlows = [-equityRequired];
    projections.forEach(p => {
      cashFlows.push(p.cashFlow);
    });
    const irrValue = calculateIRR(cashFlows);

    const equityMultiple = equityRequired > 0 ? (netProfit + equityRequired) / equityRequired : 0;
    const totalCashCollected = projections.reduce((sum, p) => sum + p.monthlyRevenue, 0);
    const cashOnCash = equityRequired > 0 ? (totalCashCollected / equityRequired) * 100 : 0;

    setResults({
      totalLandCost,
      totalAcquisitionCost,
      costPerLot,
      costPerAcre,
      siteworkCost,
      streetsCost,
      utilitiesCost,
      stormwaterCost,
      landscapingCost,
      amenitiesCost,
      totalHardCosts,
      hardCostPerLot,
      engineeringCost,
      architectureCost,
      legalPermitsCost,
      marketingSalesCost,
      developerFee,
      totalSoftCosts,
      totalDevelopmentCost,
      allInCostPerLot,
      contingencyCost,
      loanAmount,
      loanFees,
      totalInterestCost,
      equityRequired,
      grossSalesRevenue: cumulativeRevenue,
      averageSalePricePerLot,
      netSalesRevenue,
      grossProfit,
      grossProfitMargin,
      netProfit,
      netProfitMargin,
      irr: irrValue * 100,
      equityMultiple,
      cashOnCash,
      roi,
      totalMonths,
      developmentMonths,
      salesMonths,
      projections,
    });
  }, [inputs, showResults]);

  const handleRunModel = () => {
    setShowResults(true);
    setCurrentTab(0);
  };

  const handleSave = () => {
    saveToLocalStorage('subdivision', {
      projectName: inputs.projectName,
      location: inputs.location,
      inputs,
      results,
    });
    setSaveMessage('Project saved successfully!');
    setTimeout(() => setSaveMessage(''), 3000);
  };

  // Chart data preparation
  const costBreakdownData = results
    ? [
        { name: 'Land', value: results.totalLandCost, color: '#8b5cf6' },
        { name: 'Sitework', value: results.siteworkCost, color: '#3b82f6' },
        { name: 'Streets', value: results.streetsCost, color: '#10b981' },
        { name: 'Utilities', value: results.utilitiesCost, color: '#f59e0b' },
        { name: 'Amenities', value: results.amenitiesCost, color: '#ef4444' },
        { name: 'Soft Costs', value: results.totalSoftCosts, color: '#6b7280' },
      ]
    : [];

  const cashFlowData = results
    ? results.projections.filter((_,i) => i % 3 === 0).map(p => ({
        month: p.month,
        revenue: p.monthlyRevenue,
        costs: -p.monthlyCosts,
        cumulative: p.cumulativeCashFlow,
      }))
    : [];

  const lotSalesData = results
    ? results.projections.filter(p => p.lotsSold > 0).map(p => ({
        month: p.month,
        lotsSold: p.lotsSold,
        cumulative: p.cumulativeLotsSold,
      }))
    : [];

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: isDark ? '#0f172a' : '#f8fafc', pb: 4 }}>
      {/* Header */}
      <Paper
        elevation={0}
        sx={{
          p: 3,
          mb: 3,
          borderRadius: 0,
          bgcolor: isDark ? '#1e293b' : '#ffffff',
          borderBottom: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={2}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/calculators')}
            sx={{ color: 'text.secondary' }}
          >
            Back
          </Button>
          <LandscapeIcon sx={{ fontSize: 32, color: '#10b981' }} />
          <Box sx={{ flex: 1 }}>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              Subdivision Development Calculator
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Analyze land subdivision projects with lot sales projections
            </Typography>
          </Box>
          {showResults && (
            <Button
              variant="outlined"
              startIcon={<SaveIcon />}
              onClick={handleSave}
              sx={{ borderRadius: 2 }}
            >
              Save Project
            </Button>
          )}
        </Stack>
        {saveMessage && (
          <Typography variant="body2" color="success.main" sx={{ mt: 2 }}>
            {saveMessage}
          </Typography>
        )}
      </Paper>

      {/* Tabs */}
      <Box sx={{ px: 4 }}>
        <Tabs value={currentTab} onChange={(_, v) => setCurrentTab(v)} sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tab label="Calculator" icon={<LandscapeIcon />} iconPosition="start" />
          <Tab label="Analytics" icon={<AssessmentIcon />} iconPosition="start" disabled={!showResults} />
          <Tab label="Projections" icon={<TrendingUpIcon />} iconPosition="start" disabled={!showResults} />
          <Tab label="Documentation" icon={<DescriptionIcon />} iconPosition="start" />
        </Tabs>
      </Box>

      {/* Calculator Tab */}
      {currentTab === 0 && (
        <Box sx={{ p: 4 }}>
          <Grid container spacing={4}>
            {/* Input Sections */}
            {/* Project Info */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Project Information
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={4}>
                      <TextField
                        fullWidth
                        label="Project Name"
                        value={inputs.projectName}
                        onChange={(e) => handleInputChange('projectName', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <TextField
                        fullWidth
                        label="Location"
                        value={inputs.location}
                        onChange={(e) => handleInputChange('location', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <TextField
                        fullWidth
                        label="Analyst"
                        value={inputs.analyst}
                        onChange={(e) => handleInputChange('analyst', e.target.value)}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Land Acquisition */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Land Acquisition
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Total Acres"
                        type="number"
                        value={inputs.totalAcres}
                        onChange={(e) => handleInputChange('totalAcres', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: 'acres' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Cost Per Acre"
                        type="number"
                        value={inputs.landCostPerAcre}
                        onChange={(e) => handleInputChange('landCostPerAcre', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Closing Costs"
                        type="number"
                        value={inputs.closingCosts}
                        onChange={(e) => handleInputChange('closingCosts', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Due Diligence"
                        type="number"
                        value={inputs.dueDiligenceCosts}
                        onChange={(e) => handleInputChange('dueDiligenceCosts', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Lot Details */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Subdivision Details
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Total Lots"
                        type="number"
                        value={inputs.totalLots}
                        onChange={(e) => handleInputChange('totalLots', parseInt(e.target.value))}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Avg Lot Size"
                        type="number"
                        value={inputs.averageLotSizeAcres}
                        onChange={(e) => handleInputChange('averageLotSizeAcres', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: 'acres' }}
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="subtitle2" sx={{ mb: 1 }}>
                        Lot Types
                      </Typography>
                    </Grid>
                    {(['standard', 'premium', 'estate'] as const).map((type) => (
                      <React.Fragment key={type}>
                        <Grid item xs={12} sm={4}>
                          <TextField
                            fullWidth
                            size="small"
                            label={`${type.charAt(0).toUpperCase() + type.slice(1)} Count`}
                            type="number"
                            value={inputs.lotTypes[type].count}
                            onChange={(e) => handleLotTypeChange(type, 'count', parseInt(e.target.value))}
                          />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                          <TextField
                            fullWidth
                            size="small"
                            label="Size (acres)"
                            type="number"
                            value={inputs.lotTypes[type].size}
                            onChange={(e) => handleLotTypeChange(type, 'size', parseFloat(e.target.value))}
                          />
                        </Grid>
                        <Grid item xs={12} sm={4}>
                          <TextField
                            fullWidth
                            size="small"
                            label="Sale Price"
                            type="number"
                            value={inputs.lotTypes[type].salePrice}
                            onChange={(e) => handleLotTypeChange(type, 'salePrice', parseFloat(e.target.value))}
                            InputProps={{ startAdornment: '$' }}
                          />
                        </Grid>
                      </React.Fragment>
                    ))}
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Development Costs */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Development Costs
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Sitework Per Acre"
                        type="number"
                        value={inputs.siteworkPerAcre}
                        onChange={(e) => handleInputChange('siteworkPerAcre', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Street Cost Per Foot"
                        type="number"
                        value={inputs.streetsPerFoot}
                        onChange={(e) => handleInputChange('streetsPerFoot', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Total Street Feet"
                        type="number"
                        value={inputs.totalStreetFeet}
                        onChange={(e) => handleInputChange('totalStreetFeet', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: 'ft' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Water/Sewer Per Lot"
                        type="number"
                        value={inputs.waterSewerPerLot}
                        onChange={(e) => handleInputChange('waterSewerPerLot', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Stormwater Per Acre"
                        type="number"
                        value={inputs.stormwaterPerAcre}
                        onChange={(e) => handleInputChange('stormwaterPerAcre', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Landscaping Per Acre"
                        type="number"
                        value={inputs.landscapingPerAcre}
                        onChange={(e) => handleInputChange('landscapingPerAcre', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Amenities Cost"
                        type="number"
                        value={inputs.amenitiesCost}
                        onChange={(e) => handleInputChange('amenitiesCost', parseFloat(e.target.value))}
                        InputProps={{ startAdornment: '$' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                      <TextField
                        fullWidth
                        label="Contingency %"
                        type="number"
                        value={inputs.contingencyPct}
                        onChange={(e) => handleInputChange('contingencyPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Soft Costs & Sales */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Soft Costs & Fees
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Engineering %"
                        type="number"
                        value={inputs.engineeringPct}
                        onChange={(e) => handleInputChange('engineeringPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Architecture %"
                        type="number"
                        value={inputs.architecturePct}
                        onChange={(e) => handleInputChange('architecturePct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Legal/Permits %"
                        type="number"
                        value={inputs.legalPermitsPct}
                        onChange={(e) => handleInputChange('legalPermitsPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Marketing/Sales %"
                        type="number"
                        value={inputs.marketingSalesPct}
                        onChange={(e) => handleInputChange('marketingSalesPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Developer Fee %"
                        type="number"
                        value={inputs.developerFeePct}
                        onChange={(e) => handleInputChange('developerFeePct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Timeline & Financing */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Timeline & Financing
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Sales Start Month"
                        type="number"
                        value={inputs.salesStartMonth}
                        onChange={(e) => handleInputChange('salesStartMonth', parseInt(e.target.value))}
                        InputProps={{ endAdornment: 'months' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Absorption Period"
                        type="number"
                        value={inputs.absorptionMonths}
                        onChange={(e) => handleInputChange('absorptionMonths', parseInt(e.target.value))}
                        InputProps={{ endAdornment: 'months' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Price Escalation %"
                        type="number"
                        value={inputs.priceEscalationPct}
                        onChange={(e) => handleInputChange('priceEscalationPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%/year' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Loan to Cost %"
                        type="number"
                        value={inputs.ltc}
                        onChange={(e) => handleInputChange('ltc', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Interest Rate"
                        type="number"
                        value={inputs.interestRate}
                        onChange={(e) => handleInputChange('interestRate', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        fullWidth
                        label="Loan Fees %"
                        type="number"
                        value={inputs.loanFeesPct}
                        onChange={(e) => handleInputChange('loanFeesPct', parseFloat(e.target.value))}
                        InputProps={{ endAdornment: '%' }}
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Run Model Button */}
            <Grid item xs={12}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                startIcon={<PlayArrowIcon />}
                onClick={handleRunModel}
                sx={{
                  py: 2,
                  bgcolor: '#10b981',
                  '&:hover': { bgcolor: '#059669' },
                  borderRadius: 2,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                }}
              >
                Run Financial Model
              </Button>
            </Grid>

            {/* Results Summary */}
            {showResults && results && (
              <Grid item xs={12}>
                <Card sx={{ bgcolor: isDark ? alpha('#10b981', 0.1) : alpha('#10b981', 0.05) }}>
                  <CardContent sx={{ p: 3 }}>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                      Investment Summary
                    </Typography>
                    <Grid container spacing={3}>
                      <Grid item xs={12} sm={6} md={3}>
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            Total Investment
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: '#10b981' }}>
                            {formatCurrency(results.equityRequired)}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            Net Profit
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: '#10b981' }}>
                            {formatCurrency(results.netProfit)}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            IRR
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: '#10b981' }}>
                            {formatPercent(results.irr / 100)}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} sm={6} md={3}>
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            Equity Multiple
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700, color: '#10b981' }}>
                            {results.equityMultiple.toFixed(2)}x
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            )}
          </Grid>
        </Box>
      )}

      {/* Analytics Tab */}
      {currentTab === 1 && results && (
        <Box sx={{ p: 4 }}>
          <Grid container spacing={3}>
            {/* Cost Breakdown Pie */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Cost Breakdown
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={costBreakdownData}
                          cx="50%"
                          cy="50%"
                          outerRadius={120}
                          dataKey="value"
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                          {costBreakdownData.map((entry, index) => (
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

            {/* Lot Sales Progress */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Lot Sales Progress
                  </Typography>
                  <Box sx={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={lotSalesData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} />
                        <XAxis dataKey="month" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <Tooltip />
                        <Legend />
                        <Area type="monotone" dataKey="cumulative" fill="#10b981" stroke="#10b981" name="Cumulative Lots Sold" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Cash Flow Chart */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    Cash Flow Analysis
                  </Typography>
                  <Box sx={{ height: 400 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={cashFlowData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#334155' : '#e2e8f0'} />
                        <XAxis dataKey="month" stroke={isDark ? '#94a3b8' : '#64748b'} />
                        <YAxis stroke={isDark ? '#94a3b8' : '#64748b'} tickFormatter={(v) => formatCurrency(v)} />
                        <Tooltip formatter={(value: number) => formatCurrency(value)} />
                        <Legend />
                        <Bar dataKey="revenue" fill="#10b981" name="Revenue" />
                        <Bar dataKey="costs" fill="#ef4444" name="Costs" />
                      </BarChart>
                    </ResponsiveContainer>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Advanced Analysis Section */}
            <Grid item xs={12}>
              <Divider sx={{ my: 4 }}>
                <Chip
                  label="Advanced Analysis"
                  icon={<AssessmentIcon />}
                  sx={{
                    bgcolor: isDark ? alpha('#8b5cf6', 0.2) : alpha('#8b5cf6', 0.1),
                    color: '#8b5cf6',
                    fontWeight: 600,
                    fontSize: '1rem',
                    px: 2,
                  }}
                />
              </Divider>
            </Grid>

            {/* Break-Even Analysis */}
            <Grid item xs={12}>
              <BreakEvenAnalysis
                metrics={(() => {
                  // Create calculation function for break-even analysis
                  const calculateSubdivisionResults = (testInputs: SubdivisionInputs): any => {
                    // Recalculate results based on test inputs
                    const totalLandCost = testInputs.totalAcres * testInputs.landCostPerAcre;
                    const totalAcquisitionCost = totalLandCost + testInputs.closingCosts + testInputs.dueDiligenceCosts;

                    const totalLots = testInputs.lotTypes.standard.count + testInputs.lotTypes.premium.count + testInputs.lotTypes.estate.count;

                    // Development costs
                    const siteworkCost = testInputs.totalAcres * testInputs.siteworkPerAcre;
                    const streetsCost = testInputs.totalStreetFeet * testInputs.streetsPerFoot;
                    const utilitiesCost = totalLots * testInputs.waterSewerPerLot;
                    const stormwaterCost = testInputs.totalAcres * testInputs.stormwaterPerAcre;
                    const landscapingCost = testInputs.totalAcres * testInputs.landscapingPerAcre;
                    const totalHardCosts = siteworkCost + streetsCost + utilitiesCost + stormwaterCost + landscapingCost + testInputs.amenitiesCost;
                    const contingencyCost = totalHardCosts * (testInputs.contingencyPct / 100);

                    // Soft costs
                    const engineeringCost = totalHardCosts * (testInputs.engineeringPct / 100);
                    const architectureCost = totalHardCosts * (testInputs.architecturePct / 100);
                    const legalPermitsCost = totalHardCosts * (testInputs.legalPermitsPct / 100);
                    const developerFee = totalHardCosts * (testInputs.developerFeePct / 100);

                    const grossSalesRevenue = (
                      testInputs.lotTypes.standard.count * testInputs.lotTypes.standard.salePrice +
                      testInputs.lotTypes.premium.count * testInputs.lotTypes.premium.salePrice +
                      testInputs.lotTypes.estate.count * testInputs.lotTypes.estate.salePrice
                    );

                    const marketingSalesCost = grossSalesRevenue * (testInputs.marketingSalesPct / 100);
                    const totalSoftCosts = engineeringCost + architectureCost + legalPermitsCost + marketingSalesCost + developerFee;

                    const totalDevelopmentCost = totalAcquisitionCost + totalHardCosts + contingencyCost + totalSoftCosts;
                    const loanAmount = totalDevelopmentCost * (testInputs.ltc / 100);
                    const loanFees = loanAmount * (testInputs.loanFeesPct / 100);
                    const totalInterestCost = loanAmount * (testInputs.interestRate / 100) * (testInputs.absorptionMonths / 12);

                    const netSalesRevenue = grossSalesRevenue - marketingSalesCost;
                    const netProfit = netSalesRevenue - totalDevelopmentCost - loanFees - totalInterestCost;
                    const netProfitMargin = (netProfit / grossSalesRevenue) * 100;

                    // Simple IRR approximation for break-even
                    const totalMonths = testInputs.salesStartMonth + testInputs.absorptionMonths;
                    const equityRequired = totalDevelopmentCost + loanFees - loanAmount;
                    const holdYears = totalMonths / 12;
                    const annualizedReturn = holdYears > 0 ? ((netProfit / equityRequired) / holdYears) : 0;
                    const irr = annualizedReturn / 100;

                    return {
                      irr,
                      netProfit,
                      netProfitMargin,
                      equityRequired,
                      grossSalesRevenue,
                      netSalesRevenue,
                    };
                  };

                  return calculateBreakEvenMetrics(
                    inputs,
                    results,
                    calculateSubdivisionResults,
                    0.18 // Target 18% IRR for subdivisions
                  );
                })()}
              />
            </Grid>

            {/* Stress Testing */}
            <Grid item xs={12}>
              <StressTesting
                results={(() => {
                  // Create calculation function for stress testing
                  const calculateSubdivisionForStress = (testInputs: SubdivisionInputs): any => {
                    // Full calculation similar to break-even but returning all metrics
                    const totalLandCost = testInputs.totalAcres * testInputs.landCostPerAcre;
                    const totalAcquisitionCost = totalLandCost + testInputs.closingCosts + testInputs.dueDiligenceCosts;

                    const totalLots = testInputs.lotTypes.standard.count + testInputs.lotTypes.premium.count + testInputs.lotTypes.estate.count;

                    const siteworkCost = testInputs.totalAcres * testInputs.siteworkPerAcre;
                    const streetsCost = testInputs.totalStreetFeet * testInputs.streetsPerFoot;
                    const utilitiesCost = totalLots * testInputs.waterSewerPerLot;
                    const stormwaterCost = testInputs.totalAcres * testInputs.stormwaterPerAcre;
                    const landscapingCost = testInputs.totalAcres * testInputs.landscapingPerAcre;
                    const totalHardCosts = siteworkCost + streetsCost + utilitiesCost + stormwaterCost + landscapingCost + testInputs.amenitiesCost;
                    const contingencyCost = totalHardCosts * (testInputs.contingencyPct / 100);

                    const engineeringCost = totalHardCosts * (testInputs.engineeringPct / 100);
                    const architectureCost = totalHardCosts * (testInputs.architecturePct / 100);
                    const legalPermitsCost = totalHardCosts * (testInputs.legalPermitsPct / 100);
                    const developerFee = totalHardCosts * (testInputs.developerFeePct / 100);

                    const grossSalesRevenue = (
                      testInputs.lotTypes.standard.count * testInputs.lotTypes.standard.salePrice +
                      testInputs.lotTypes.premium.count * testInputs.lotTypes.premium.salePrice +
                      testInputs.lotTypes.estate.count * testInputs.lotTypes.estate.salePrice
                    );

                    const marketingSalesCost = grossSalesRevenue * (testInputs.marketingSalesPct / 100);
                    const totalSoftCosts = engineeringCost + architectureCost + legalPermitsCost + marketingSalesCost + developerFee;

                    const totalDevelopmentCost = totalAcquisitionCost + totalHardCosts + contingencyCost + totalSoftCosts;
                    const loanAmount = totalDevelopmentCost * (testInputs.ltc / 100);
                    const loanFees = loanAmount * (testInputs.loanFeesPct / 100);
                    const totalInterestCost = loanAmount * (testInputs.interestRate / 100) * (testInputs.absorptionMonths / 12);

                    const netSalesRevenue = grossSalesRevenue - marketingSalesCost;
                    const netProfit = netSalesRevenue - totalDevelopmentCost - loanFees - totalInterestCost;
                    const exitValue = netSalesRevenue;
                    const equityRequired = totalDevelopmentCost + loanFees - loanAmount;
                    const equityMultiple = (netProfit + equityRequired) / equityRequired;

                    // IRR approximation
                    const totalMonths = testInputs.salesStartMonth + testInputs.absorptionMonths;
                    const holdYears = totalMonths / 12;
                    const annualizedReturn = holdYears > 0 ? ((netProfit / equityRequired) / holdYears) : 0;
                    const irr = annualizedReturn / 100;

                    // Approximate metrics for display
                    const avgMonthlyRevenue = grossSalesRevenue / testInputs.absorptionMonths;
                    const avgMonthlyCosts = totalDevelopmentCost / (testInputs.salesStartMonth + testInputs.absorptionMonths);

                    return {
                      irr,
                      equityMultiple,
                      exitValue,
                      noi: avgMonthlyRevenue * 12, // Use annual revenue as proxy
                      cashFlow: (avgMonthlyRevenue - avgMonthlyCosts) * 12,
                      dscr: avgMonthlyRevenue > 0 ? avgMonthlyRevenue / avgMonthlyCosts : 0,
                    };
                  };

                  return calculateStressTestResults(
                    inputs,
                    results,
                    calculateSubdivisionForStress,
                    STRESS_SCENARIOS
                  );
                })()}
                targetIrr={0.18}
              />
            </Grid>

            {/* Waterfall Analysis */}
            <Grid item xs={12}>
              <Box sx={{ mb: 4 }}>
                <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
                  Waterfall Analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Visual breakdown of project costs and how value flows through the development.
                </Typography>
              </Box>

              {/* Development Cost Waterfall */}
              <Grid item xs={12}>
                <WaterfallChart
                  data={calculateDevelopmentCostWaterfall(
                    results.totalLandCost,
                    results.totalHardCosts,
                    results.totalSoftCosts,
                    results.loanFees + results.totalInterestCost,
                    results.contingencyCost
                  )}
                  title="Development Cost Buildup"
                />
              </Grid>
            </Grid>
          </Grid>
        </Box>
      )}

      {/* Projections Tab */}
      {currentTab === 2 && results && (
        <Box sx={{ p: 4 }}>
          <Card>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                Monthly Projections
              </Typography>
              <TableContainer sx={{ maxHeight: 600 }}>
                <Table stickyHeader size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Month</TableCell>
                      <TableCell>Phase</TableCell>
                      <TableCell align="right">Lots Sold</TableCell>
                      <TableCell align="right">Revenue</TableCell>
                      <TableCell align="right">Costs</TableCell>
                      <TableCell align="right">Cash Flow</TableCell>
                      <TableCell align="right">Cumulative CF</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {results.projections.filter((_, i) => i % 3 === 0 || i === results.projections.length - 1).map((proj) => (
                      <TableRow key={proj.month}>
                        <TableCell>{proj.month}</TableCell>
                        <TableCell>
                          <Chip
                            label={proj.phase}
                            size="small"
                            sx={{
                              textTransform: 'capitalize',
                              bgcolor:
                                proj.phase === 'sales'
                                  ? alpha('#10b981', 0.2)
                                  : proj.phase === 'development'
                                  ? alpha('#3b82f6', 0.2)
                                  : alpha('#6b7280', 0.2),
                            }}
                          />
                        </TableCell>
                        <TableCell align="right">{proj.lotsSold.toFixed(1)}</TableCell>
                        <TableCell align="right">{formatCurrency(proj.monthlyRevenue)}</TableCell>
                        <TableCell align="right">{formatCurrency(proj.monthlyCosts)}</TableCell>
                        <TableCell align="right" sx={{ color: proj.cashFlow >= 0 ? '#10b981' : '#ef4444' }}>
                          {formatCurrency(proj.cashFlow)}
                        </TableCell>
                        <TableCell align="right" sx={{ fontWeight: 600 }}>
                          {formatCurrency(proj.cumulativeCashFlow)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Box>
      )}

      {/* Documentation Tab */}
      {currentTab === 3 && (
        <Box sx={{ p: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 2 }}>
            Subdivision Development Model Guide
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
            Comprehensive financial analysis for land subdivision projects from acquisition through lot sales.
          </Typography>

          <Grid container spacing={3}>
            {/* Overview */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Overview
                  </Typography>
                  <Typography variant="body1" paragraph>
                    The Subdivision Development Model is designed for developers and investors analyzing residential or commercial
                    land subdivision projects. This calculator models the complete development lifecycle including land acquisition,
                    entitlements, infrastructure development, financing, and phased lot sales.
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Unlike traditional real estate investments, subdivision development involves:
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Front-loaded capital requirements</strong> for land, engineering, and infrastructure</li>
                    <li><strong>Phased revenue</strong> from lot sales over an absorption period</li>
                    <li><strong>Development risk</strong> from entitlement, construction, and market timing</li>
                    <li><strong>Lot type stratification</strong> with varying sizes, prices, and absorption rates</li>
                    <li><strong>Construction debt</strong> that pays down as lots sell</li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Key Metrics */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Key Performance Metrics
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Profitability Metrics
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>
                      <strong>IRR (Internal Rate of Return):</strong> Time-weighted return considering all cash inflows and outflows.
                      For subdivisions, target IRRs typically range from 15-25% depending on risk profile and market.
                    </li>
                    <li>
                      <strong>Equity Multiple:</strong> Total cash returned divided by equity invested. Measures gross return without
                      time consideration. A 2.0x multiple means doubling your equity.
                    </li>
                    <li>
                      <strong>Net Profit Margin:</strong> Net profit as a percentage of gross sales revenue. Typical subdivision margins
                      range from 20-40% depending on land basis and market strength.
                    </li>
                    <li>
                      <strong>ROI (Return on Investment):</strong> Simple return calculation (Profit / Total Investment). Unlike IRR,
                      this doesn't account for timing of cash flows.
                    </li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Cost Metrics
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>
                      <strong>All-In Cost Per Lot:</strong> Total project cost (land + hard costs + soft costs + financing) divided
                      by number of lots. Critical for pricing decisions.
                    </li>
                    <li>
                      <strong>Land Cost Per Lot:</strong> Acquisition cost allocated across all lots. Typically represents 15-25%
                      of final lot sale price.
                    </li>
                    <li>
                      <strong>Hard Cost Per Lot:</strong> Infrastructure and development costs per lot. Includes streets, utilities,
                      grading, drainage, and amenities.
                    </li>
                    <li>
                      <strong>Total Development Cost:</strong> Sum of land acquisition, hard costs, soft costs, financing costs,
                      and contingency.
                    </li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Market & Sales Metrics
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>
                      <strong>Absorption Rate:</strong> Lots sold per month during active sales period. Varies by market, lot type,
                      and price point. Typical rates: 2-6 lots/month for retail subdivisions.
                    </li>
                    <li>
                      <strong>Average Sale Price:</strong> Weighted average across all lot types based on count and individual prices.
                    </li>
                    <li>
                      <strong>Price Escalation:</strong> Annual price increases applied to lot sales. Accounts for market appreciation
                      during sales period.
                    </li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Input Sections */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Input Sections Explained
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    1. Land Acquisition
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Total Acres:</strong> Gross acreage purchased (not net developable acres)</li>
                    <li><strong>Land Cost Per Acre:</strong> Purchase price per gross acre</li>
                    <li><strong>Closing Costs:</strong> Title, escrow, broker fees (typically 2-4% of purchase price)</li>
                    <li><strong>Due Diligence Costs:</strong> Environmental studies, surveys, soil tests, market studies</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    2. Subdivision Details
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Total Lots:</strong> Total number of finished lots to be created</li>
                    <li><strong>Average Lot Size:</strong> Used for density calculations and planning validation</li>
                    <li><strong>Lot Types:</strong> Standard, Premium, and Estate with different sizes, counts, and prices</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    3. Development Costs (Hard Costs)
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Sitework Per Acre:</strong> Mass grading, clearing, erosion control ($15,000-$30,000/acre typical)</li>
                    <li><strong>Streets:</strong> Cost per linear foot × total street feet. Includes base, paving, curbs ($150-$300/LF)</li>
                    <li><strong>Water/Sewer Per Lot:</strong> Utility infrastructure to each lot ($8,000-$15,000/lot typical)</li>
                    <li><strong>Stormwater Per Acre:</strong> Detention ponds, drainage systems ($5,000-$12,000/acre)</li>
                    <li><strong>Landscaping Per Acre:</strong> Entry features, street trees, common areas ($3,000-$8,000/acre)</li>
                    <li><strong>Amenities:</strong> Clubhouse, pool, trails, parks (varies widely by project scale)</li>
                    <li><strong>Contingency %:</strong> Reserve for cost overruns (typically 5-10% of hard costs)</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    4. Soft Costs & Fees
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Engineering:</strong> Civil engineering, surveying (3-5% of hard costs)</li>
                    <li><strong>Architecture:</strong> Site planning, landscape architecture (1-2% of hard costs)</li>
                    <li><strong>Legal & Permits:</strong> Entitlements, HOA docs, impact fees (2-4% of hard costs)</li>
                    <li><strong>Marketing & Sales:</strong> Model homes, signage, broker commissions (3-6% of sales revenue)</li>
                    <li><strong>Developer Fee:</strong> Developer profit/overhead (5-10% of hard costs)</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    5. Timeline & Financing
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Absorption (months):</strong> Time to sell all lots once sales begin</li>
                    <li><strong>Sales Start Month:</strong> Month when first lots go to market (after entitlement & development)</li>
                    <li><strong>Price Escalation:</strong> Annual price appreciation during sales period</li>
                    <li><strong>LTC (Loan-to-Cost):</strong> Percentage of total project cost financed (typically 50-75%)</li>
                    <li><strong>Interest Rate:</strong> Construction loan rate (typically prime + 2-4%)</li>
                    <li><strong>Loan Fees:</strong> Origination, commitment fees (1-3% of loan amount)</li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Calculation Methodology */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Calculation Methodology
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Monthly Projection Model
                  </Typography>
                  <Typography variant="body1" paragraph>
                    The calculator uses a month-by-month projection approach with four distinct phases:
                  </Typography>
                  <Box sx={{ ml: 3, mb: 2 }}>
                    <Typography variant="body2" paragraph>
                      <strong>Phase 1 - Acquisition (Month 1):</strong>
                      <br />• Land purchase, closing costs, and due diligence
                      <br />• Initial equity injection
                      <br />• Construction loan funding
                    </Typography>
                    <Typography variant="body2" paragraph>
                      <strong>Phase 2 - Development (Months 2 through Sales Start):</strong>
                      <br />• Hard cost expenditures (sitework, streets, utilities)
                      <br />• Soft cost expenditures (engineering, permits, marketing setup)
                      <br />• Interest accrual on construction loan
                      <br />• Carrying costs (taxes, insurance, maintenance)
                    </Typography>
                    <Typography variant="body2" paragraph>
                      <strong>Phase 3 - Sales Period (Sales Start through Absorption):</strong>
                      <br />• Lot sales revenue with price escalation
                      <br />• Loan paydown from sales proceeds
                      <br />• Ongoing carrying costs on unsold inventory
                      <br />• Interest on declining loan balance
                    </Typography>
                    <Typography variant="body2" paragraph>
                      <strong>Phase 4 - Completion (Final Month):</strong>
                      <br />• Final lot sales
                      <br />• Loan payoff
                      <br />• Return of remaining equity
                    </Typography>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Lot Sales Distribution
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Lot sales are distributed evenly across the absorption period. For example, with 75 lots and
                    18-month absorption starting at month 6:
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>Lots per month = 75 / 18 = 4.17 lots/month</li>
                    <li>Month 6-23: Steady sales of 4-5 lots/month</li>
                    <li>Each month's revenue = (lots sold) × (average price) × (1 + escalation)^years</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    IRR Calculation
                  </Typography>
                  <Typography variant="body1" paragraph>
                    IRR is calculated using the Newton-Raphson iterative method on the net present value (NPV) equation:
                  </Typography>
                  <Box sx={{ ml: 3, mb: 2 }}>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace', mb: 1 }}>
                      NPV = Σ [Cash Flow_t / (1 + IRR)^t] = 0
                    </Typography>
                    <Typography variant="body2">
                      Where t is the time period in months, converted to years for annualized IRR.
                    </Typography>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Loan Balance Tracking
                  </Typography>
                  <Typography variant="body1" paragraph>
                    The construction loan balance changes throughout the project:
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Funding Phase:</strong> Draws occur as development costs are incurred</li>
                    <li><strong>Accrual Phase:</strong> Interest accrues monthly and capitalizes to loan balance</li>
                    <li><strong>Paydown Phase:</strong> Sales proceeds pay down principal before returning equity</li>
                    <li><strong>Interest Calculation:</strong> (Loan Balance × Interest Rate) / 12 months</li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Best Practices */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Best Practices & Rules of Thumb
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Land Acquisition
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>1/3 Rule:</strong> Land cost should be approximately 1/3 of finished lot value</li>
                    <li><strong>Zoning Buffer:</strong> Assume 20-30% of gross acres will be non-developable (streets, setbacks, open space)</li>
                    <li><strong>Entitlement Risk:</strong> Factor 10-20% discount if purchasing pre-entitled vs. entitled land</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Development Costs
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Infrastructure Percentage:</strong> Hard costs typically 30-40% of finished lot sale price</li>
                    <li><strong>Soft Cost Range:</strong> Budget 15-25% of hard costs for all soft costs combined</li>
                    <li><strong>Contingency Allocation:</strong> Use 10% for first-time markets, 5% for experienced teams</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Return Targets
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>IRR Benchmarks:</strong> 18-22% for suburban residential, 15-18% for master-planned communities</li>
                    <li><strong>Profit Margin:</strong> Target minimum 25% net margin; 35%+ for higher-risk projects</li>
                    <li><strong>Equity Multiple:</strong> Aim for 1.7x+ on 2-year projects, 2.0x+ on 3+ year projects</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Risk Management
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Phased Development:</strong> Only develop infrastructure for lots selling in next 12-18 months</li>
                    <li><strong>Absorption Stress Test:</strong> Model scenarios at 75% and 50% of projected absorption</li>
                    <li><strong>Price Sensitivity:</strong> Test impact of 10% price reduction on returns</li>
                    <li><strong>Pre-Sales:</strong> Consider requiring 30-40% pre-sales before breaking ground</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Market Analysis
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Comparable Sales:</strong> Analyze absorption rates from 3-5 comparable subdivisions</li>
                    <li><strong>Builder Demand:</strong> Pre-qualify builders before projecting absorption</li>
                    <li><strong>Economic Cycles:</strong> Subdivisions are highly cyclical; avoid peak-market acquisitions</li>
                    <li><strong>Location Premium:</strong> Lots within 5 miles of growing employment centers command 20-40% premium</li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Common Pitfalls */}
            <Grid item xs={12}>
              <Card sx={{ bgcolor: isDark ? alpha('#f59e0b', 0.1) : alpha('#f59e0b', 0.05), border: `2px solid ${alpha('#f59e0b', 0.3)}` }}>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <WarningIcon sx={{ color: '#f59e0b' }} />
                    Common Pitfalls to Avoid
                  </Typography>
                  <Box component="ul" sx={{ ml: 3 }}>
                    <li>
                      <strong>Underestimating Absorption:</strong> Overly optimistic absorption is the #1 cause of subdivision failures.
                      Always stress test at 50% slower absorption.
                    </li>
                    <li>
                      <strong>Ignoring Carrying Costs:</strong> Property taxes, insurance, and interest during slow absorption periods
                      can devastate returns. Model these carefully.
                    </li>
                    <li>
                      <strong>Construction Cost Escalation:</strong> If development takes 18+ months, factor 3-5% annual cost escalation.
                    </li>
                    <li>
                      <strong>Impact Fees:</strong> Water, sewer, traffic, and school impact fees can add $5,000-$25,000 per lot.
                      Verify fees early in due diligence.
                    </li>
                    <li>
                      <strong>Utility Capacity:</strong> Insufficient water/sewer capacity can delay projects 1-2 years. Confirm
                      availability during due diligence.
                    </li>
                    <li>
                      <strong>Market Timing:</strong> Subdivisions take 2-4 years start to finish. Buying at market peaks risks
                      selling in downturns.
                    </li>
                    <li>
                      <strong>Single Lot Type:</strong> Offering multiple lot sizes/price points reduces absorption risk and
                      captures broader market.
                    </li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Analytics Tab Features */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Analytics Features
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Cost Breakdown Pie Chart
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Visualizes the allocation of total project costs across major categories:
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>Land acquisition (including closing and due diligence)</li>
                    <li>Hard costs (sitework, streets, utilities, stormwater, landscaping, amenities)</li>
                    <li>Soft costs (engineering, architecture, legal, marketing, developer fee)</li>
                    <li>Financing costs (loan fees and total interest expense)</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Lot Sales Progress Chart
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Area chart showing cumulative lot sales over time. Helps visualize the sales trajectory and
                    identify when cash generation begins accelerating.
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Monthly Cash Flow Analysis
                  </Typography>
                  <Typography variant="body1" paragraph>
                    Stacked bar chart comparing monthly revenue against monthly costs. Shows the transition from
                    capital-intensive development phase to cash-generating sales phase.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Example Scenarios */}
            <Grid item xs={12}>
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    Example Scenarios
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Suburban Infill Development
                  </Typography>
                  <Box sx={{ ml: 3, mb: 2 }}>
                    <Typography variant="body2" paragraph>
                      • 25 acres @ $150,000/acre = $3.75M land cost
                      <br />• 60 lots (2.4 lots/acre density)
                      <br />• Mix: 40 standard ($95k), 15 premium ($120k), 5 estate ($165k)
                      <br />• 12-month development, 18-month absorption
                      <br />• 65% LTC financing
                      <br />• <strong>Target Returns:</strong> 22% IRR, 2.1x equity multiple, 32% profit margin
                    </Typography>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Master-Planned Community (Phase 1)
                  </Typography>
                  <Box sx={{ ml: 3, mb: 2 }}>
                    <Typography variant="body2" paragraph>
                      • 150 acres @ $75,000/acre = $11.25M land cost
                      <br />• 200 lots (1.33 lots/acre with amenities and open space)
                      <br />• Mix: 120 standard ($75k), 60 premium ($95k), 20 estate ($135k)
                      <br />• 18-month development, 30-month absorption
                      <br />• 70% LTC financing
                      <br />• Amenities: $2.5M clubhouse, pool, trails
                      <br />• <strong>Target Returns:</strong> 18% IRR, 2.3x equity multiple, 28% profit margin
                    </Typography>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 3, mb: 2 }}>
                    Rural Estate Lots
                  </Typography>
                  <Box sx={{ ml: 3, mb: 2 }}>
                    <Typography variant="body2" paragraph>
                      • 80 acres @ $25,000/acre = $2M land cost
                      <br />• 25 lots (3.2 acres average)
                      <br />• Mix: 15 standard 2-acre ($75k), 10 estate 5-acre ($125k)
                      <br />• 9-month development, 24-month absorption (slower)
                      <br />• 50% LTC financing (higher risk = lower leverage)
                      <br />• Lower infrastructure costs, minimal amenities
                      <br />• <strong>Target Returns:</strong> 16% IRR, 1.9x equity multiple, 35% profit margin
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Additional Resources */}
            <Grid item xs={12}>
              <Card sx={{ bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05), border: `2px solid ${alpha('#3b82f6', 0.3)}` }}>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <InfoIcon sx={{ color: '#3b82f6' }} />
                    Additional Considerations
                  </Typography>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 2, mb: 1 }}>
                    Regulatory & Legal
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>Subdivision plat approval (typically 3-9 months)</li>
                    <li>Environmental clearances (wetlands, endangered species)</li>
                    <li>HOA formation and CC&R documentation</li>
                    <li>Utility easement dedications</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 2, mb: 1 }}>
                    Market Dynamics
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li>Builder allocation strategies (volume discounts vs. retail pricing)</li>
                    <li>Seasonal absorption patterns (spring/summer typically stronger)</li>
                    <li>Competition from nearby subdivisions</li>
                    <li>New home construction trends in the market</li>
                  </Box>

                  <Typography variant="h6" sx={{ fontWeight: 600, mt: 2, mb: 1 }}>
                    Exit Strategies
                  </Typography>
                  <Box component="ul" sx={{ ml: 3, mb: 2 }}>
                    <li><strong>Bulk Sale:</strong> Sell remaining lots in bulk to builder at 15-25% discount</li>
                    <li><strong>Phased Sale:</strong> Sell subdivision in phases to multiple developers</li>
                    <li><strong>Retail Completion:</strong> Hold through full absorption for maximum returns</li>
                    <li><strong>JV Restructure:</strong> Bring in JV partner mid-project to reduce exposure</li>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};
