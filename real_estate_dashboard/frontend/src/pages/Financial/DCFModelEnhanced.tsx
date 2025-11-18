import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Stack,
  Card,
  CardContent,
  Tabs,
  Tab,
  Divider,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
  Info as InfoIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';
import { ScenarioAnalysis, Variable } from '../../components/ScenarioAnalysis/ScenarioAnalysis';

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
      id={`dcf-tabpanel-${index}`}
      aria-labelledby={`dcf-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

interface ComparableCompany {
  name: string;
  ticker: string;
  marketCap: number;
  ev: number;
  revenue: number;
  ebitda: number;
  revenueGrowth: number;
}

export const DCFModelEnhanced: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    // Company Info
    companyName: '',
    ticker: '',
    currentStockPrice: '',
    sharesOutstanding: '',

    // Balance Sheet
    cash: '',
    totalDebt: '',
    preferredStock: '',
    minorityInterest: '',

    // Revenue Projections
    baseYearRevenue: '',
    revenue1Growth: '5',
    revenue2Growth: '5',
    revenue3Growth: '4',
    revenue4Growth: '4',
    revenue5Growth: '3',

    // EBITDA Margins
    baseYearEbitdaMargin: '20',
    ebitdaMargin1: '21',
    ebitdaMargin2: '22',
    ebitdaMargin3: '23',
    ebitdaMargin4: '24',
    ebitdaMargin5: '25',

    // Other Operating Assumptions
    dnaPercent: '3',
    capexPercent: '3',
    nwcPercent: '10',

    // WACC Inputs
    riskFreeRate: '4.5',
    beta: '1.2',
    marketRiskPremium: '7.0',
    costOfDebt: '5.0',
    taxRate: '21',
    marketValueEquity: '',
    marketValueDebt: '',

    // Terminal Value
    terminalGrowthRate: '2.5',
    terminalEbitdaMultiple: '12',
    terminalMethod: 'growth', // 'growth' or 'multiple'
  });

  const [comparables, setComparables] = useState<ComparableCompany[]>([]);
  const [results, setResults] = useState<any>(null);

  const handleInputChange = (field: string, value: string) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const addComparable = () => {
    setComparables([...comparables, {
      name: '',
      ticker: '',
      marketCap: 0,
      ev: 0,
      revenue: 0,
      ebitda: 0,
      revenueGrowth: 0,
    }]);
  };

  const removeComparable = (index: number) => {
    setComparables(comparables.filter((_, i) => i !== index));
  };

  const updateComparable = (index: number, field: keyof ComparableCompany, value: any) => {
    const updated = [...comparables];
    updated[index] = { ...updated[index], [field]: value };
    setComparables(updated);
  };

  const calculateDCF = () => {
    try {
      // Parse inputs
      const baseRevenue = parseFloat(inputs.baseYearRevenue) || 0;
      const sharesOut = parseFloat(inputs.sharesOutstanding) || 1;

      // WACC Calculation
      const riskFree = parseFloat(inputs.riskFreeRate) / 100;
      const beta = parseFloat(inputs.beta);
      const marketPremium = parseFloat(inputs.marketRiskPremium) / 100;
      const costOfDebt = parseFloat(inputs.costOfDebt) / 100;
      const taxRate = parseFloat(inputs.taxRate) / 100;

      const marketValueEquity = parseFloat(inputs.marketValueEquity) || (parseFloat(inputs.currentStockPrice) * sharesOut);
      const marketValueDebt = parseFloat(inputs.marketValueDebt) || parseFloat(inputs.totalDebt) || 0;
      const totalCapital = marketValueEquity + marketValueDebt;

      const costOfEquity = riskFree + beta * marketPremium;
      const wacc = (costOfEquity * (marketValueEquity / totalCapital)) +
                   (costOfDebt * (1 - taxRate) * (marketValueDebt / totalCapital));

      // Revenue Projections
      const revenueGrowthRates = [
        parseFloat(inputs.revenue1Growth) / 100,
        parseFloat(inputs.revenue2Growth) / 100,
        parseFloat(inputs.revenue3Growth) / 100,
        parseFloat(inputs.revenue4Growth) / 100,
        parseFloat(inputs.revenue5Growth) / 100,
      ];

      const revenues = [baseRevenue];
      for (let i = 0; i < 5; i++) {
        revenues.push(revenues[i] * (1 + revenueGrowthRates[i]));
      }

      // EBITDA Projections
      const ebitdaMargins = [
        parseFloat(inputs.baseYearEbitdaMargin) / 100,
        parseFloat(inputs.ebitdaMargin1) / 100,
        parseFloat(inputs.ebitdaMargin2) / 100,
        parseFloat(inputs.ebitdaMargin3) / 100,
        parseFloat(inputs.ebitdaMargin4) / 100,
        parseFloat(inputs.ebitdaMargin5) / 100,
      ];

      const ebitdas = revenues.map((rev, i) => rev * ebitdaMargins[i]);

      // D&A, CapEx, NWC
      const dnaPercent = parseFloat(inputs.dnaPercent) / 100;
      const capexPercent = parseFloat(inputs.capexPercent) / 100;
      const nwcPercent = parseFloat(inputs.nwcPercent) / 100;

      // Free Cash Flow Calculation (Years 1-5)
      const fcfs: number[] = [];
      for (let i = 1; i <= 5; i++) {
        const revenue = revenues[i];
        const ebitda = ebitdas[i];
        const dna = revenue * dnaPercent;
        const ebit = ebitda - dna;
        const nopat = ebit * (1 - taxRate);
        const capex = revenue * capexPercent;
        const nwc = revenue * nwcPercent;
        const prevNwc = revenues[i - 1] * nwcPercent;
        const changeNwc = nwc - prevNwc;

        const fcf = nopat + dna - capex - changeNwc;
        fcfs.push(fcf);
      }

      // Terminal Value
      const terminalGrowth = parseFloat(inputs.terminalGrowthRate) / 100;
      const terminalMultiple = parseFloat(inputs.terminalEbitdaMultiple);

      let terminalValue = 0;
      if (inputs.terminalMethod === 'growth') {
        terminalValue = (fcfs[4] * (1 + terminalGrowth)) / (wacc - terminalGrowth);
      } else {
        terminalValue = ebitdas[5] * terminalMultiple;
      }

      // Present Value Calculations
      const pvFCFs = fcfs.map((fcf, i) => fcf / Math.pow(1 + wacc, i + 1));
      const pvTerminal = terminalValue / Math.pow(1 + wacc, 5);

      // Enterprise Value
      const enterpriseValue = pvFCFs.reduce((sum, pv) => sum + pv, 0) + pvTerminal;

      // Equity Value
      const cash = parseFloat(inputs.cash) || 0;
      const debt = parseFloat(inputs.totalDebt) || 0;
      const preferred = parseFloat(inputs.preferredStock) || 0;
      const minority = parseFloat(inputs.minorityInterest) || 0;

      const equityValue = enterpriseValue + cash - debt - preferred - minority;
      const impliedSharePrice = equityValue / sharesOut;

      const currentPrice = parseFloat(inputs.currentStockPrice) || 0;
      const upside = currentPrice > 0 ? ((impliedSharePrice - currentPrice) / currentPrice) * 100 : 0;

      // Sensitivity Analysis
      const sensitivityWaccVsGrowth = generateSensitivityTable(
        fcfs[4],
        [0.01, 0.015, 0.02, 0.025, 0.03],
        [0.06, 0.07, 0.08, 0.09, 0.10],
        (growth, waccVal) => {
          const tv = (fcfs[4] * (1 + growth)) / (waccVal - growth);
          const ev = pvFCFs.reduce((sum, pv) => sum + pv, 0) + (tv / Math.pow(1 + waccVal, 5));
          const eqVal = ev + cash - debt - preferred - minority;
          return eqVal / sharesOut;
        }
      );

      const sensitivityWaccVsMultiple = generateSensitivityTable(
        ebitdas[5],
        [10, 11, 12, 13, 14],
        [0.06, 0.07, 0.08, 0.09, 0.10],
        (multiple, waccVal) => {
          const tv = ebitdas[5] * multiple;
          const ev = pvFCFs.reduce((sum, pv) => sum + pv, 0) + (tv / Math.pow(1 + waccVal, 5));
          const eqVal = ev + cash - debt - preferred - minority;
          return eqVal / sharesOut;
        }
      );

      // Scenario Analysis
      const scenarios = calculateScenarios(baseRevenue, sharesOut, taxRate, cash, debt, preferred, minority);

      // Trading Comps Analysis
      const compsAnalysis = calculateTradingComps();

      setResults({
        wacc: wacc * 100,
        costOfEquity: costOfEquity * 100,
        revenues,
        ebitdas,
        fcfs,
        pvFCFs,
        terminalValue,
        pvTerminal,
        enterpriseValue,
        equityValue,
        impliedSharePrice,
        currentPrice,
        upside,
        sensitivityWaccVsGrowth,
        sensitivityWaccVsMultiple,
        scenarios,
        compsAnalysis,
      });
    } catch (error) {
      console.error('DCF calculation error:', error);
      alert('Error calculating DCF. Please check your inputs.');
    }
  };

  const generateSensitivityTable = (
    baseValue: number,
    rowValues: number[],
    colValues: number[],
    calcFn: (rowVal: number, colVal: number) => number
  ) => {
    const table: number[][] = [];
    for (const rowVal of rowValues) {
      const row: number[] = [];
      for (const colVal of colValues) {
        row.push(calcFn(rowVal, colVal));
      }
      table.push(row);
    }
    return {
      rows: rowValues,
      cols: colValues,
      values: table,
    };
  };

  const calculateScenarios = (
    baseRevenue: number,
    sharesOut: number,
    taxRate: number,
    cash: number,
    debt: number,
    preferred: number,
    minority: number
  ) => {
    const scenarios = [
      {
        name: 'Bear Case',
        revenueCAGR: 0.02,
        ebitdaMargin: 0.18,
        terminalGrowth: 0.015,
        wacc: 0.10,
        probability: 0.25,
      },
      {
        name: 'Base Case',
        revenueCAGR: 0.04,
        ebitdaMargin: 0.22,
        terminalGrowth: 0.025,
        wacc: 0.08,
        probability: 0.50,
      },
      {
        name: 'Bull Case',
        revenueCAGR: 0.06,
        ebitdaMargin: 0.26,
        terminalGrowth: 0.03,
        wacc: 0.07,
        probability: 0.25,
      },
    ];

    return scenarios.map(scenario => {
      const year5Revenue = baseRevenue * Math.pow(1 + scenario.revenueCAGR, 5);
      const year5EBITDA = year5Revenue * scenario.ebitdaMargin;
      const fcf5 = year5EBITDA * 0.7; // Simplified
      const tv = (fcf5 * (1 + scenario.terminalGrowth)) / (scenario.wacc - scenario.terminalGrowth);
      const ev = (fcf5 * 3) + (tv / Math.pow(1 + scenario.wacc, 5)); // Simplified
      const eqVal = ev + cash - debt - preferred - minority;
      const price = eqVal / sharesOut;

      return {
        ...scenario,
        impliedPrice: price,
      };
    });
  };

  const calculateTradingComps = () => {
    if (comparables.length === 0) return null;

    const validComps = comparables.filter(c => c.ev > 0 && c.ebitda > 0);
    if (validComps.length === 0) return null;

    const evEbitdaMultiples = validComps.map(c => c.ev / c.ebitda);
    const evRevenueMultiples = validComps.map(c => c.ev / c.revenue);

    const mean = (arr: number[]) => arr.reduce((sum, v) => sum + v, 0) / arr.length;
    const median = (arr: number[]) => {
      const sorted = [...arr].sort((a, b) => a - b);
      const mid = Math.floor(sorted.length / 2);
      return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
    };

    return {
      evEbitda: {
        mean: mean(evEbitdaMultiples),
        median: median(evEbitdaMultiples),
        min: Math.min(...evEbitdaMultiples),
        max: Math.max(...evEbitdaMultiples),
      },
      evRevenue: {
        mean: mean(evRevenueMultiples),
        median: median(evRevenueMultiples),
        min: Math.min(...evRevenueMultiples),
        max: Math.max(...evRevenueMultiples),
      },
    };
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number, decimals: number = 2) => {
    return `${value.toFixed(decimals)}%`;
  };

  return (
    <Box>
      {/* Header */}
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 3 }}>
        <Box
          sx={{
            width: 56,
            height: 56,
            background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(59, 130, 246, 0.3)',
          }}
        >
          <TrendingUpIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            DCF Valuation Model - Enhanced
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Comprehensive DCF analysis with sensitivity, scenarios, and trading comps
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Company" />
              <Tab label="Projections" />
              <Tab label="WACC" />
              <Tab label="Terminal Value" />
              <Tab label="Trading Comps" />
              <Tab label="Scenario Analysis" icon={<ShowChartIcon />} iconPosition="start" />
            </Tabs>

            {/* Tab 0: Company Info */}
            <TabPanel value={tabValue} index={0}>
              <Stack spacing={3}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>Company Information</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Company Name"
                      fullWidth
                      value={inputs.companyName}
                      onChange={(e) => handleInputChange('companyName', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Ticker Symbol"
                      fullWidth
                      value={inputs.ticker}
                      onChange={(e) => handleInputChange('ticker', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Current Stock Price ($)"
                      type="number"
                      fullWidth
                      value={inputs.currentStockPrice}
                      onChange={(e) => handleInputChange('currentStockPrice', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Shares Outstanding (M)"
                      type="number"
                      fullWidth
                      value={inputs.sharesOutstanding}
                      onChange={(e) => handleInputChange('sharesOutstanding', e.target.value)}
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Balance Sheet Items</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cash & Equivalents ($M)"
                      type="number"
                      fullWidth
                      value={inputs.cash}
                      onChange={(e) => handleInputChange('cash', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Total Debt ($M)"
                      type="number"
                      fullWidth
                      value={inputs.totalDebt}
                      onChange={(e) => handleInputChange('totalDebt', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Preferred Stock ($M)"
                      type="number"
                      fullWidth
                      value={inputs.preferredStock}
                      onChange={(e) => handleInputChange('preferredStock', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Minority Interest ($M)"
                      type="number"
                      fullWidth
                      value={inputs.minorityInterest}
                      onChange={(e) => handleInputChange('minorityInterest', e.target.value)}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 1: Projections */}
            <TabPanel value={tabValue} index={1}>
              <Stack spacing={3}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>Revenue Projections</Typography>

                <TextField
                  label="Base Year Revenue ($M)"
                  type="number"
                  fullWidth
                  value={inputs.baseYearRevenue}
                  onChange={(e) => handleInputChange('baseYearRevenue', e.target.value)}
                />

                <Typography variant="body2" fontWeight={600}>
                  Revenue Growth Rates (%)
                </Typography>
                <Grid container spacing={2}>
                  {[1, 2, 3, 4, 5].map((year) => (
                    <Grid item xs={12} sm={6} md={4} key={`rev-growth-${year}`}>
                      <TextField
                        label={`Year ${year} Growth %`}
                        type="number"
                        fullWidth
                        value={inputs[`revenue${year}Growth` as keyof typeof inputs]}
                        onChange={(e) => handleInputChange(`revenue${year}Growth`, e.target.value)}
                        inputProps={{ step: 0.5 }}
                      />
                    </Grid>
                  ))}
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>EBITDA Margins</Typography>

                <TextField
                  label="Base Year EBITDA Margin (%)"
                  type="number"
                  fullWidth
                  value={inputs.baseYearEbitdaMargin}
                  onChange={(e) => handleInputChange('baseYearEbitdaMargin', e.target.value)}
                  inputProps={{ step: 0.5 }}
                />

                <Typography variant="body2" fontWeight={600}>
                  Projected EBITDA Margins (%)
                </Typography>
                <Grid container spacing={2}>
                  {[1, 2, 3, 4, 5].map((year) => (
                    <Grid item xs={12} sm={6} md={4} key={`ebitda-margin-${year}`}>
                      <TextField
                        label={`Year ${year} Margin %`}
                        type="number"
                        fullWidth
                        value={inputs[`ebitdaMargin${year}` as keyof typeof inputs]}
                        onChange={(e) => handleInputChange(`ebitdaMargin${year}`, e.target.value)}
                        inputProps={{ step: 0.5 }}
                      />
                    </Grid>
                  ))}
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Other Operating Assumptions</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="D&A (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.dnaPercent}
                      onChange={(e) => handleInputChange('dnaPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="CapEx (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.capexPercent}
                      onChange={(e) => handleInputChange('capexPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="NWC (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.nwcPercent}
                      onChange={(e) => handleInputChange('nwcPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 2: WACC */}
            <TabPanel value={tabValue} index={2}>
              <Stack spacing={3}>
                <Alert severity="info">
                  WACC (Weighted Average Cost of Capital) is the discount rate used for DCF analysis.
                </Alert>

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Cost of Equity (CAPM)</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Risk-Free Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.riskFreeRate}
                      onChange={(e) => handleInputChange('riskFreeRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                      helperText="10-Year Treasury"
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Beta"
                      type="number"
                      fullWidth
                      value={inputs.beta}
                      onChange={(e) => handleInputChange('beta', e.target.value)}
                      inputProps={{ step: 0.1 }}
                      helperText="Levered Beta"
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Market Risk Premium (%)"
                      type="number"
                      fullWidth
                      value={inputs.marketRiskPremium}
                      onChange={(e) => handleInputChange('marketRiskPremium', e.target.value)}
                      inputProps={{ step: 0.1 }}
                      helperText="Equity Risk Premium"
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Cost of Debt</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Pre-Tax Cost of Debt (%)"
                      type="number"
                      fullWidth
                      value={inputs.costOfDebt}
                      onChange={(e) => handleInputChange('costOfDebt', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Tax Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.taxRate}
                      onChange={(e) => handleInputChange('taxRate', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Capital Structure</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Market Value of Equity ($M)"
                      type="number"
                      fullWidth
                      value={inputs.marketValueEquity}
                      onChange={(e) => handleInputChange('marketValueEquity', e.target.value)}
                      helperText="Leave blank to auto-calculate"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Market Value of Debt ($M)"
                      type="number"
                      fullWidth
                      value={inputs.marketValueDebt}
                      onChange={(e) => handleInputChange('marketValueDebt', e.target.value)}
                      helperText="Leave blank to use Total Debt"
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 3: Terminal Value */}
            <TabPanel value={tabValue} index={3}>
              <Stack spacing={3}>
                <Alert severity="info">
                  Terminal Value represents the value of all cash flows beyond the projection period.
                </Alert>

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Terminal Value Method</Typography>

                <Box>
                  <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
                    <Chip
                      label="Perpetuity Growth"
                      color={inputs.terminalMethod === 'growth' ? 'primary' : 'default'}
                      onClick={() => handleInputChange('terminalMethod', 'growth')}
                      clickable
                    />
                    <Chip
                      label="Exit Multiple"
                      color={inputs.terminalMethod === 'multiple' ? 'primary' : 'default'}
                      onClick={() => handleInputChange('terminalMethod', 'multiple')}
                      clickable
                    />
                  </Stack>

                  {inputs.terminalMethod === 'growth' ? (
                    <TextField
                      label="Terminal Growth Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.terminalGrowthRate}
                      onChange={(e) => handleInputChange('terminalGrowthRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                      helperText="Typically 2-3% (GDP growth)"
                    />
                  ) : (
                    <TextField
                      label="Exit EBITDA Multiple (x)"
                      type="number"
                      fullWidth
                      value={inputs.terminalEbitdaMultiple}
                      onChange={(e) => handleInputChange('terminalEbitdaMultiple', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="Typically same as entry multiple"
                    />
                  )}
                </Box>
              </Stack>
            </TabPanel>

            {/* Tab 4: Trading Comps */}
            <TabPanel value={tabValue} index={4}>
              <Stack spacing={3}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>Trading Comparables</Typography>
                  <Button
                    variant="outlined"
                    startIcon={<AddIcon />}
                    onClick={addComparable}
                    size="small"
                  >
                    Add Comparable
                  </Button>
                </Box>

                {comparables.length === 0 ? (
                  <Alert severity="info">
                    Add comparable companies to perform relative valuation analysis.
                  </Alert>
                ) : (
                  <Stack spacing={2}>
                    {comparables.map((comp, index) => (
                      <Paper key={index} sx={{ p: 2, bgcolor: 'grey.50' }}>
                        <Stack spacing={2}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <Typography variant="subtitle2" fontWeight={600}>
                              Comparable #{index + 1}
                            </Typography>
                            <IconButton
                              size="small"
                              color="error"
                              onClick={() => removeComparable(index)}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Box>

                          <Grid container spacing={2}>
                            <Grid item xs={12} sm={6}>
                              <TextField
                                label="Company Name"
                                size="small"
                                fullWidth
                                value={comp.name}
                                onChange={(e) => updateComparable(index, 'name', e.target.value)}
                              />
                            </Grid>
                            <Grid item xs={12} sm={6}>
                              <TextField
                                label="Ticker"
                                size="small"
                                fullWidth
                                value={comp.ticker}
                                onChange={(e) => updateComparable(index, 'ticker', e.target.value)}
                              />
                            </Grid>
                            <Grid item xs={6} sm={4}>
                              <TextField
                                label="Market Cap ($M)"
                                size="small"
                                type="number"
                                fullWidth
                                value={comp.marketCap || ''}
                                onChange={(e) => updateComparable(index, 'marketCap', parseFloat(e.target.value) || 0)}
                              />
                            </Grid>
                            <Grid item xs={6} sm={4}>
                              <TextField
                                label="EV ($M)"
                                size="small"
                                type="number"
                                fullWidth
                                value={comp.ev || ''}
                                onChange={(e) => updateComparable(index, 'ev', parseFloat(e.target.value) || 0)}
                              />
                            </Grid>
                            <Grid item xs={6} sm={4}>
                              <TextField
                                label="Revenue ($M)"
                                size="small"
                                type="number"
                                fullWidth
                                value={comp.revenue || ''}
                                onChange={(e) => updateComparable(index, 'revenue', parseFloat(e.target.value) || 0)}
                              />
                            </Grid>
                            <Grid item xs={6} sm={4}>
                              <TextField
                                label="EBITDA ($M)"
                                size="small"
                                type="number"
                                fullWidth
                                value={comp.ebitda || ''}
                                onChange={(e) => updateComparable(index, 'ebitda', parseFloat(e.target.value) || 0)}
                              />
                            </Grid>
                            <Grid item xs={6} sm={4}>
                              <TextField
                                label="Revenue Growth (%)"
                                size="small"
                                type="number"
                                fullWidth
                                value={comp.revenueGrowth || ''}
                                onChange={(e) => updateComparable(index, 'revenueGrowth', parseFloat(e.target.value) || 0)}
                              />
                            </Grid>
                          </Grid>
                        </Stack>
                      </Paper>
                    ))}
                  </Stack>
                )}
              </Stack>
            </TabPanel>

            {/* Tab 5: Scenario Analysis */}
            <TabPanel value={tabValue} index={5}>
              <Stack spacing={3}>
                <Alert severity="info">
                  Comprehensive risk analysis with Monte Carlo simulations, sensitivity analysis, and break-even calculations.
                </Alert>

                {(() => {
                  // Define scenario variables based on current inputs
                  const scenarioVariables: Variable[] = [
                    {
                      name: 'baseYearRevenue',
                      label: 'Base Revenue',
                      baseValue: parseFloat(inputs.baseYearRevenue || '1000'),
                      min: parseFloat(inputs.baseYearRevenue || '1000') * 0.5,
                      max: parseFloat(inputs.baseYearRevenue || '1000') * 1.5,
                      step: 50,
                      unit: '$M',
                    },
                    {
                      name: 'revenueGrowth',
                      label: 'Avg Revenue Growth',
                      baseValue: parseFloat(inputs.revenue1Growth || '5'),
                      min: 0,
                      max: 15,
                      step: 0.5,
                      unit: '%',
                    },
                    {
                      name: 'ebitdaMargin',
                      label: 'EBITDA Margin',
                      baseValue: parseFloat(inputs.baseYearEbitdaMargin || '20'),
                      min: 10,
                      max: 40,
                      step: 1,
                      unit: '%',
                    },
                    {
                      name: 'wacc',
                      label: 'WACC',
                      baseValue: parseFloat(inputs.riskFreeRate || '4.5') + parseFloat(inputs.beta || '1.2') * parseFloat(inputs.marketRiskPremium || '7') / 100,
                      min: 5,
                      max: 20,
                      step: 0.5,
                      unit: '%',
                    },
                    {
                      name: 'terminalGrowth',
                      label: 'Terminal Growth',
                      baseValue: parseFloat(inputs.terminalGrowthRate || '2.5'),
                      min: 0,
                      max: 5,
                      step: 0.25,
                      unit: '%',
                    },
                    {
                      name: 'taxRate',
                      label: 'Tax Rate',
                      baseValue: parseFloat(inputs.taxRate || '21'),
                      min: 15,
                      max: 35,
                      step: 1,
                      unit: '%',
                    },
                  ];

                  // DCF calculation function for scenario analysis
                  const calculateEnterpriseValue = (vars: Record<string, number>): number => {
                    try {
                      const baseRevenue = vars.baseYearRevenue;
                      const avgGrowth = vars.revenueGrowth / 100;
                      const ebitdaMargin = vars.ebitdaMargin / 100;
                      const wacc = vars.wacc / 100;
                      const terminalGrowth = vars.terminalGrowth / 100;
                      const taxRate = vars.taxRate / 100;

                      // Project revenues for 5 years
                      const revenues = [baseRevenue];
                      for (let i = 0; i < 5; i++) {
                        revenues.push(revenues[i] * (1 + avgGrowth));
                      }

                      // Calculate EBITDA and FCF for each year
                      const dnaPercent = parseFloat(inputs.dnaPercent || '3') / 100;
                      const capexPercent = parseFloat(inputs.capexPercent || '3') / 100;
                      const nwcPercent = parseFloat(inputs.nwcPercent || '10') / 100;

                      const fcfs: number[] = [];
                      for (let i = 1; i <= 5; i++) {
                        const revenue = revenues[i];
                        const ebitda = revenue * ebitdaMargin;
                        const dna = revenue * dnaPercent;
                        const ebit = ebitda - dna;
                        const nopat = ebit * (1 - taxRate);
                        const capex = revenue * capexPercent;
                        const nwc = revenue * nwcPercent;
                        const prevNwc = revenues[i - 1] * nwcPercent;
                        const changeNwc = nwc - prevNwc;

                        const fcf = nopat + dna - capex - changeNwc;
                        fcfs.push(fcf);
                      }

                      // Terminal Value
                      const terminalValue = (fcfs[4] * (1 + terminalGrowth)) / (wacc - terminalGrowth);

                      // Present Value Calculations
                      const pvFCFs = fcfs.map((fcf, i) => fcf / Math.pow(1 + wacc, i + 1));
                      const pvTerminal = terminalValue / Math.pow(1 + wacc, 5);

                      // Enterprise Value
                      const enterpriseValue = pvFCFs.reduce((sum, pv) => sum + pv, 0) + pvTerminal;

                      return enterpriseValue;
                    } catch (error) {
                      console.error('Scenario calculation error:', error);
                      return 0;
                    }
                  };

                  return (
                    <ScenarioAnalysis
                      calculateMetric={calculateEnterpriseValue}
                      variables={scenarioVariables}
                      metricName="Enterprise Value"
                      metricUnit="$M"
                      breakEvenTarget={parseFloat(inputs.totalDebt || '0')}
                    />
                  );
                })()}
              </Stack>
            </TabPanel>

            {/* Calculate Button */}
            <Box sx={{ mt: 3 }}>
              <Button
                variant="contained"
                startIcon={<CalculateIcon />}
                onClick={calculateDCF}
                fullWidth
                sx={{
                  py: 1.5,
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                  fontWeight: 600,
                }}
              >
                Calculate Valuation
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} lg={4}>
          <Stack spacing={3}>
            {results && (
              <>
                {/* Summary Card */}
                <Card sx={{ background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', color: 'white' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Valuation Summary
                    </Typography>

                    <Stack spacing={2}>
                      <Box>
                        <Typography variant="caption" sx={{ opacity: 0.9 }}>
                          Implied Share Price
                        </Typography>
                        <Typography variant="h3" sx={{ fontWeight: 700 }}>
                          ${results.impliedSharePrice.toFixed(2)}
                        </Typography>
                      </Box>

                      <Divider sx={{ bgcolor: 'rgba(255,255,255,0.2)' }} />

                      <Stack direction="row" justifyContent="space-between">
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Current Price
                          </Typography>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            ${results.currentPrice.toFixed(2)}
                          </Typography>
                        </Box>
                        <Box sx={{ textAlign: 'right' }}>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Upside/Downside
                          </Typography>
                          <Typography
                            variant="h6"
                            sx={{
                              fontWeight: 600,
                              color: results.upside >= 0 ? '#10b981' : '#ef4444',
                            }}
                          >
                            {results.upside >= 0 ? '+' : ''}{results.upside.toFixed(1)}%
                          </Typography>
                        </Box>
                      </Stack>

                      <Box
                        sx={{
                          mt: 2,
                          p: 2,
                          bgcolor: 'rgba(255,255,255,0.1)',
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="caption" sx={{ display: 'block', mb: 0.5 }}>
                          Recommendation
                        </Typography>
                        <Chip
                          label={
                            results.upside >= 20 ? 'STRONG BUY' :
                            results.upside >= 10 ? 'BUY' :
                            results.upside >= 0 ? 'HOLD' :
                            results.upside >= -10 ? 'SELL' : 'STRONG SELL'
                          }
                          sx={{
                            bgcolor: results.upside >= 10 ? '#10b981' : results.upside >= 0 ? '#f59e0b' : '#ef4444',
                            color: 'white',
                            fontWeight: 700,
                          }}
                        />
                      </Box>
                    </Stack>
                  </CardContent>
                </Card>

                {/* Key Metrics */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Key Metrics
                  </Typography>

                  <Stack spacing={1.5}>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" color="text.secondary">WACC</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatPercent(results.wacc)}</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" color="text.secondary">Cost of Equity</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatPercent(results.costOfEquity)}</Typography>
                    </Stack>
                    <Divider />
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" color="text.secondary">Enterprise Value</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatCurrency(results.enterpriseValue)}M</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" color="text.secondary">Terminal Value (PV)</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatCurrency(results.pvTerminal)}M</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="body2" color="text.secondary">Equity Value</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatCurrency(results.equityValue)}M</Typography>
                    </Stack>
                  </Stack>
                </Paper>

                {/* Action Buttons */}
                <Stack direction="row" spacing={2}>
                  <Button variant="outlined" startIcon={<SaveIcon />} fullWidth>
                    Save
                  </Button>
                  <Button variant="outlined" startIcon={<DownloadIcon />} fullWidth>
                    Export
                  </Button>
                </Stack>
              </>
            )}

            {!results && (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  Enter your inputs and click "Calculate Valuation" to see results
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>

        {/* Full Width Results Sections */}
        {results && (
          <>
            {/* Free Cash Flow Table */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Free Cash Flow Analysis
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Year</TableCell>
                        <TableCell align="right">Revenue ($M)</TableCell>
                        <TableCell align="right">EBITDA ($M)</TableCell>
                        <TableCell align="right">FCF ($M)</TableCell>
                        <TableCell align="right">PV of FCF ($M)</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.fcfs.map((fcf: number, idx: number) => (
                        <TableRow key={idx}>
                          <TableCell>{idx + 1}</TableCell>
                          <TableCell align="right">{formatCurrency(results.revenues[idx + 1])}</TableCell>
                          <TableCell align="right">{formatCurrency(results.ebitdas[idx + 1])}</TableCell>
                          <TableCell align="right">{formatCurrency(fcf)}</TableCell>
                          <TableCell align="right">{formatCurrency(results.pvFCFs[idx])}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Scenario Analysis */}
            {results.scenarios && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Scenario Analysis
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Scenario</TableCell>
                          <TableCell align="right">Probability</TableCell>
                          <TableCell align="right">Implied Price</TableCell>
                          <TableCell align="right">Upside/Downside</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {results.scenarios.map((scenario: any, idx: number) => {
                          const upside = ((scenario.impliedPrice - results.currentPrice) / results.currentPrice) * 100;
                          return (
                            <TableRow key={idx}>
                              <TableCell>
                                <Chip
                                  label={scenario.name}
                                  size="small"
                                  color={scenario.name === 'Bull Case' ? 'success' : scenario.name === 'Bear Case' ? 'error' : 'default'}
                                />
                              </TableCell>
                              <TableCell align="right">{formatPercent(scenario.probability * 100, 0)}</TableCell>
                              <TableCell align="right">${scenario.impliedPrice.toFixed(2)}</TableCell>
                              <TableCell align="right">
                                <Typography
                                  variant="body2"
                                  sx={{ color: upside >= 0 ? '#10b981' : '#ef4444', fontWeight: 600 }}
                                >
                                  {upside >= 0 ? '+' : ''}{upside.toFixed(1)}%
                                </Typography>
                              </TableCell>
                            </TableRow>
                          );
                        })}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>
              </Grid>
            )}

            {/* Trading Comps Summary */}
            {results.compsAnalysis && (
              <Grid item xs={12} md={6}>
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Trading Comps Summary
                  </Typography>

                  <Stack spacing={2}>
                    <Box>
                      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                        EV / EBITDA Multiples
                      </Typography>
                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Mean:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {results.compsAnalysis.evEbitda.mean.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Median:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {results.compsAnalysis.evEbitda.median.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Min:</Typography>
                          <Typography variant="body2">
                            {results.compsAnalysis.evEbitda.min.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Max:</Typography>
                          <Typography variant="body2">
                            {results.compsAnalysis.evEbitda.max.toFixed(2)}x
                          </Typography>
                        </Grid>
                      </Grid>
                    </Box>

                    <Divider />

                    <Box>
                      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                        EV / Revenue Multiples
                      </Typography>
                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Mean:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {results.compsAnalysis.evRevenue.mean.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Median:</Typography>
                          <Typography variant="body2" fontWeight={600}>
                            {results.compsAnalysis.evRevenue.median.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Min:</Typography>
                          <Typography variant="body2">
                            {results.compsAnalysis.evRevenue.min.toFixed(2)}x
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">Max:</Typography>
                          <Typography variant="body2">
                            {results.compsAnalysis.evRevenue.max.toFixed(2)}x
                          </Typography>
                        </Grid>
                      </Grid>
                    </Box>
                  </Stack>
                </Paper>
              </Grid>
            )}

            {/* Sensitivity Analysis - WACC vs Terminal Growth */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Sensitivity Analysis: WACC vs Terminal Growth Rate
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Terminal Growth →<br />WACC ↓</TableCell>
                        {results.sensitivityWaccVsGrowth.rows.map((growth: number, idx: number) => (
                          <TableCell key={idx} align="center">
                            {formatPercent(growth * 100, 1)}
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.sensitivityWaccVsGrowth.cols.map((waccVal: number, rowIdx: number) => (
                        <TableRow key={rowIdx}>
                          <TableCell sx={{ fontWeight: 600 }}>
                            {formatPercent(waccVal * 100, 1)}
                          </TableCell>
                          {results.sensitivityWaccVsGrowth.values[rowIdx].map((price: number, colIdx: number) => (
                            <TableCell
                              key={colIdx}
                              align="center"
                              sx={{
                                bgcolor: price > results.currentPrice ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                fontWeight: 500,
                              }}
                            >
                              ${price.toFixed(2)}
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Sensitivity Analysis - WACC vs Exit Multiple */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Sensitivity Analysis: WACC vs Exit EBITDA Multiple
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Exit Multiple →<br />WACC ↓</TableCell>
                        {results.sensitivityWaccVsMultiple.rows.map((multiple: number, idx: number) => (
                          <TableCell key={idx} align="center">
                            {multiple.toFixed(1)}x
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.sensitivityWaccVsMultiple.cols.map((waccVal: number, rowIdx: number) => (
                        <TableRow key={rowIdx}>
                          <TableCell sx={{ fontWeight: 600 }}>
                            {formatPercent(waccVal * 100, 1)}
                          </TableCell>
                          {results.sensitivityWaccVsMultiple.values[rowIdx].map((price: number, colIdx: number) => (
                            <TableCell
                              key={colIdx}
                              align="center"
                              sx={{
                                bgcolor: price > results.currentPrice ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                fontWeight: 500,
                              }}
                            >
                              ${price.toFixed(2)}
                            </TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>
          </>
        )}
      </Grid>
    </Box>
  );
};
