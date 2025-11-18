import React, { useState } from 'react';
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
  LinearProgress,
} from '@mui/material';
import {
  AccountBalance as LBOIcon,
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
  TrendingUp as TrendingUpIcon,
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
      id={`lbo-tabpanel-${index}`}
      aria-labelledby={`lbo-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const LBOModelEnhanced: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    // Company Info
    companyName: '',
    industry: '',
    holdingPeriod: '5',

    // Entry Valuation
    ltmRevenue: '',
    ltmEbitda: '',
    entryEvEbitdaMultiple: '10',

    // Financing
    totalLeverage: '5.0',
    seniorLeverage: '4.0',

    // Debt Terms
    revolverSize: '0',
    revolverRate: '5.0',
    revolverUndrawnFee: '0.5',

    tlaAmount: '',
    tlaRate: '6.0',
    tlaMandAmort: '5',
    tlaCashSweep: '100',

    tlbAmount: '',
    tlbRate: '7.5',
    tlbMandAmort: '1',
    tlbCashSweep: '50',

    subDebtAmount: '',
    subDebtRate: '10.0',

    // Sources & Uses
    existingCash: '0',
    existingDebtPayoff: '0',
    transactionCosts: '2',

    // Operating Assumptions
    revenueGrowthY1: '5',
    revenueGrowthY2: '5',
    revenueGrowthY3: '4',
    revenueGrowthY4: '4',
    revenueGrowthY5: '3',
    revenueGrowthY6: '3',
    revenueGrowthY7: '3',

    ebitdaMarginY1: '22',
    ebitdaMarginY2: '23',
    ebitdaMarginY3: '24',
    ebitdaMarginY4: '24',
    ebitdaMarginY5: '25',
    ebitdaMarginY6: '25',
    ebitdaMarginY7: '25',

    dnaPercent: '3',
    capexPercent: '3',
    nwcPercent: '10',
    taxRate: '25',

    // Cash Sweep
    minCashBalance: '20',

    // Exit
    exitEvEbitdaMultiple: '10',

    // Waterfall
    preferredReturn: '8',
    gpCatchup: '100',
    carriedInterest: '20',
  });

  const [results, setResults] = useState<any>(null);

  const handleInputChange = (field: string, value: string) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const calculateLBO = () => {
    try {
      // Parse inputs
      const ltmRevenue = parseFloat(inputs.ltmRevenue) || 0;
      const ltmEbitda = parseFloat(inputs.ltmEbitda) || 0;
      const entryMultiple = parseFloat(inputs.entryEvEbitdaMultiple);
      const holdingPeriod = parseInt(inputs.holdingPeriod);

      // Purchase Price
      const purchasePrice = ltmEbitda * entryMultiple;

      // Financing Structure
      const totalLeverage = parseFloat(inputs.totalLeverage);
      const seniorLeverage = parseFloat(inputs.seniorLeverage);

      const totalDebt = ltmEbitda * totalLeverage;
      const seniorDebt = ltmEbitda * seniorLeverage;
      const subDebt = totalDebt - seniorDebt;

      // Transaction Costs
      const existingCash = parseFloat(inputs.existingCash) || 0;
      const existingDebtPayoff = parseFloat(inputs.existingDebtPayoff) || 0;
      const transCosts = (parseFloat(inputs.transactionCosts) / 100) * purchasePrice;

      // Sources & Uses
      const totalUses = purchasePrice + transCosts - existingCash + existingDebtPayoff;
      const equityContribution = totalUses - totalDebt;

      // Debt Allocation
      const tlaAmount = parseFloat(inputs.tlaAmount) || (seniorDebt * 0.5);
      const tlbAmount = parseFloat(inputs.tlbAmount) || (seniorDebt * 0.5);
      const subDebtAmount = parseFloat(inputs.subDebtAmount) || subDebt;

      // Operating Projections
      const years = Array.from({ length: holdingPeriod + 1 }, (_, i) => i);
      const revenueGrowthRates = [
        0,
        parseFloat(inputs.revenueGrowthY1) / 100,
        parseFloat(inputs.revenueGrowthY2) / 100,
        parseFloat(inputs.revenueGrowthY3) / 100,
        parseFloat(inputs.revenueGrowthY4) / 100,
        parseFloat(inputs.revenueGrowthY5) / 100,
        parseFloat(inputs.revenueGrowthY6) / 100,
        parseFloat(inputs.revenueGrowthY7) / 100,
      ];

      const ebitdaMargins = [
        ltmEbitda / ltmRevenue,
        parseFloat(inputs.ebitdaMarginY1) / 100,
        parseFloat(inputs.ebitdaMarginY2) / 100,
        parseFloat(inputs.ebitdaMarginY3) / 100,
        parseFloat(inputs.ebitdaMarginY4) / 100,
        parseFloat(inputs.ebitdaMarginY5) / 100,
        parseFloat(inputs.ebitdaMarginY6) / 100,
        parseFloat(inputs.ebitdaMarginY7) / 100,
      ];

      // Revenue & EBITDA Projections
      const revenues = [ltmRevenue];
      for (let i = 1; i <= holdingPeriod; i++) {
        revenues.push(revenues[i - 1] * (1 + revenueGrowthRates[i]));
      }

      const ebitdas = revenues.map((rev, i) => rev * ebitdaMargins[i]);

      // Debt Schedule with Cash Sweep
      const tlaRate = parseFloat(inputs.tlaRate) / 100;
      const tlbRate = parseFloat(inputs.tlbRate) / 100;
      const subRate = parseFloat(inputs.subDebtRate) / 100;
      const taxRate = parseFloat(inputs.taxRate) / 100;
      const tlaMandAmort = parseFloat(inputs.tlaMandAmort) / 100;
      const tlbMandAmort = parseFloat(inputs.tlbMandAmort) / 100;
      const tlaCashSweep = parseFloat(inputs.tlaCashSweep) / 100;
      const tlbCashSweep = parseFloat(inputs.tlbCashSweep) / 100;
      const minCash = parseFloat(inputs.minCashBalance);

      const dnaPercent = parseFloat(inputs.dnaPercent) / 100;
      const capexPercent = parseFloat(inputs.capexPercent) / 100;
      const nwcPercent = parseFloat(inputs.nwcPercent) / 100;

      let tlaBalance = tlaAmount;
      let tlbBalance = tlbAmount;
      let subBalance = subDebtAmount;

      const debtSchedule = [];
      const fcfSchedule = [];
      const creditMetrics = [];

      for (let i = 1; i <= holdingPeriod; i++) {
        // Beginning balances
        const begTLA = tlaBalance;
        const begTLB = tlbBalance;
        const begSub = subBalance;
        const totalBegDebt = begTLA + begTLB + begSub;

        // Interest expense
        const tlaInterest = begTLA * tlaRate;
        const tlbInterest = begTLB * tlbRate;
        const subInterest = begSub * subRate;
        const totalInterest = tlaInterest + tlbInterest + subInterest;

        // Cash Flow
        const revenue = revenues[i];
        const ebitda = ebitdas[i];
        const dna = revenue * dnaPercent;
        const ebit = ebitda - dna;
        const nopat = ebit * (1 - taxRate);
        const capex = revenue * capexPercent;
        const nwc = revenue * nwcPercent;
        const prevNwc = revenues[i - 1] * nwcPercent;
        const changeNwc = nwc - prevNwc;

        const fcf = nopat + dna - capex - changeNwc - totalInterest;
        fcfSchedule.push(fcf);

        // Mandatory Amortization
        const tlaMandPayment = tlaAmount * tlaMandAmort;
        const tlbMandPayment = tlbAmount * tlbMandAmort;

        // Cash available for sweep
        const cashAvailForSweep = Math.max(0, fcf - tlaMandPayment - tlbMandPayment - minCash);

        // Cash Sweep Logic
        let tlaOptPayment = 0;
        let tlbOptPayment = 0;

        if (cashAvailForSweep > 0 && begTLA > 0) {
          tlaOptPayment = Math.min(cashAvailForSweep * tlaCashSweep, begTLA - tlaMandPayment);
        }

        const remainingCash = cashAvailForSweep - tlaOptPayment;
        if (remainingCash > 0 && begTLB > 0 && begTLA - tlaMandPayment - tlaOptPayment <= 0) {
          tlbOptPayment = Math.min(remainingCash * tlbCashSweep, begTLB - tlbMandPayment);
        }

        // Update balances
        tlaBalance = Math.max(0, begTLA - tlaMandPayment - tlaOptPayment);
        tlbBalance = Math.max(0, begTLB - tlbMandPayment - tlbOptPayment);
        subBalance = begSub; // No amortization on sub debt

        debtSchedule.push({
          year: i,
          tla: { beg: begTLA, mandAmort: tlaMandPayment, optPayment: tlaOptPayment, end: tlaBalance },
          tlb: { beg: begTLB, mandAmort: tlbMandPayment, optPayment: tlbOptPayment, end: tlbBalance },
          sub: { beg: begSub, end: subBalance },
          totalDebt: tlaBalance + tlbBalance + subBalance,
          interest: totalInterest,
        });

        // Credit Metrics
        const leverage = (tlaBalance + tlbBalance + subBalance) / ebitda;
        const interestCoverage = ebitda / totalInterest;

        creditMetrics.push({
          year: i,
          totalDebtEbitda: leverage,
          ebitdaInterest: interestCoverage,
          ebitInterest: ebit / totalInterest,
        });
      }

      // Exit Valuation
      const exitMultiple = parseFloat(inputs.exitEvEbitdaMultiple);
      const exitEbitda = ebitdas[holdingPeriod];
      const exitEV = exitEbitda * exitMultiple;
      const exitDebt = tlaBalance + tlbBalance + subBalance;
      const exitEquityValue = exitEV - exitDebt;

      // Returns Analysis
      const moic = exitEquityValue / equityContribution;
      const irr = (Math.pow(moic, 1 / holdingPeriod) - 1) * 100;
      const totalReturn = exitEquityValue - equityContribution;
      const totalReturnPct = (totalReturn / equityContribution) * 100;

      // Distribution Waterfall (European-style)
      const preferredReturnRate = parseFloat(inputs.preferredReturn) / 100;
      const gpCatchupPct = parseFloat(inputs.gpCatchup) / 100;
      const carryPct = parseFloat(inputs.carriedInterest) / 100;

      const waterfall = calculateWaterfall(
        equityContribution,
        exitEquityValue,
        holdingPeriod,
        preferredReturnRate,
        gpCatchupPct,
        carryPct
      );

      // Sensitivity Analysis
      const sensitivity = generateSensitivityAnalysis(
        ltmRevenue,
        ltmEbitda,
        entryMultiple,
        holdingPeriod,
        equityContribution,
        totalDebt,
        ebitdaMargins,
        revenueGrowthRates
      );

      setResults({
        // Transaction Summary
        purchasePrice,
        totalDebt,
        seniorDebt,
        subDebt: subDebtAmount,
        equityContribution,
        tlaAmount,
        tlbAmount,

        // Projections
        revenues,
        ebitdas,
        fcfSchedule,

        // Debt Schedule
        debtSchedule,
        totalDebtPaydown: totalDebt - exitDebt,

        // Exit
        exitEV,
        exitEbitda,
        exitDebt,
        exitEquityValue,

        // Returns
        moic,
        irr,
        totalReturn,
        totalReturnPct,

        // Credit Metrics
        creditMetrics,

        // Distribution Waterfall
        waterfall,

        // Sensitivity
        sensitivity,
      });
    } catch (error) {
      console.error('LBO calculation error:', error);
      alert('Error calculating LBO. Please check your inputs.');
    }
  };

  const calculateWaterfall = (
    initialInvestment: number,
    totalDistributions: number,
    years: number,
    preferredReturn: number,
    gpCatchup: number,
    carry: number
  ) => {
    // Tier 1: Return of Capital
    let remaining = totalDistributions;
    const tier1 = Math.min(remaining, initialInvestment);
    remaining -= tier1;

    // Tier 2: Preferred Return
    const preferredReturnAmount = initialInvestment * (Math.pow(1 + preferredReturn, years) - 1);
    const tier2 = Math.min(remaining, preferredReturnAmount);
    remaining -= tier2;

    // Tier 3: GP Catch-Up
    const lpSoFar = tier1 + tier2;
    const targetGPCarry = lpSoFar * (carry / (1 - carry));
    const tier3 = Math.min(remaining, targetGPCarry * gpCatchup);
    remaining -= tier3;

    // Tier 4: Carried Interest Split
    const lpTier4 = remaining * (1 - carry);
    const gpTier4 = remaining * carry;

    const totalLP = tier1 + tier2 + lpTier4;
    const totalGP = tier3 + gpTier4;

    return {
      totalDistributions,
      tier1ReturnOfCapital: tier1,
      tier2PreferredReturn: tier2,
      tier3GPCatchup: tier3,
      tier4Split: { lp: lpTier4, gp: gpTier4 },
      totalLP,
      totalGP,
      lpPct: (totalLP / totalDistributions) * 100,
      gpPct: (totalGP / totalDistributions) * 100,
    };
  };

  const generateSensitivityAnalysis = (
    baseRevenue: number,
    baseEbitda: number,
    entryMultiple: number,
    years: number,
    equity: number,
    debt: number,
    ebitdaMargins: number[],
    growthRates: number[]
  ) => {
    const exitMultiples = [8, 9, 10, 11, 12];
    const revenueGrowthScenarios = [0.02, 0.03, 0.04, 0.05, 0.06];

    const irrTable: number[][] = [];

    for (const growthScenario of revenueGrowthScenarios) {
      const row: number[] = [];
      for (const exitMult of exitMultiples) {
        // Simplified calculation
        const exitRevenue = baseRevenue * Math.pow(1 + growthScenario, years);
        const exitEbitda = exitRevenue * ebitdaMargins[Math.min(years, ebitdaMargins.length - 1)];
        const exitEV = exitEbitda * exitMult;

        // Assume 40% debt paydown
        const exitDebt = debt * 0.6;
        const exitEquity = exitEV - exitDebt;

        const moic = exitEquity / equity;
        const irr = (Math.pow(moic, 1 / years) - 1) * 100;

        row.push(irr);
      }
      irrTable.push(row);
    }

    return {
      exitMultiples,
      revenueGrowthScenarios,
      irrTable,
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

  const formatPercent = (value: number, decimals: number = 1) => {
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
            background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(139, 92, 246, 0.3)',
          }}
        >
          <LBOIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            LBO Model - Enhanced
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Comprehensive LBO analysis with debt schedule, cash sweep, and distribution waterfall
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Transaction" />
              <Tab label="Debt Terms" />
              <Tab label="Operations" />
              <Tab label="Exit & Waterfall" />
              <Tab label="Scenario Analysis" icon={<ShowChartIcon />} iconPosition="start" />
            </Tabs>

            {/* Tab 0: Transaction */}
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
                      label="Industry"
                      fullWidth
                      value={inputs.industry}
                      onChange={(e) => handleInputChange('industry', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Holding Period (Years)"
                      type="number"
                      fullWidth
                      value={inputs.holdingPeriod}
                      onChange={(e) => handleInputChange('holdingPeriod', e.target.value)}
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Entry Valuation</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="LTM Revenue ($M)"
                      type="number"
                      fullWidth
                      value={inputs.ltmRevenue}
                      onChange={(e) => handleInputChange('ltmRevenue', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="LTM EBITDA ($M)"
                      type="number"
                      fullWidth
                      value={inputs.ltmEbitda}
                      onChange={(e) => handleInputChange('ltmEbitda', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Entry EV/EBITDA Multiple (x)"
                      type="number"
                      fullWidth
                      value={inputs.entryEvEbitdaMultiple}
                      onChange={(e) => handleInputChange('entryEvEbitdaMultiple', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Financing Structure</Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Total Leverage (Debt/EBITDA)"
                      type="number"
                      fullWidth
                      value={inputs.totalLeverage}
                      onChange={(e) => handleInputChange('totalLeverage', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="Typically 4.0x to 6.0x"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Senior Leverage (Senior Debt/EBITDA)"
                      type="number"
                      fullWidth
                      value={inputs.seniorLeverage}
                      onChange={(e) => handleInputChange('seniorLeverage', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="Typically 3.0x to 4.5x"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Transaction Costs (% of EV)"
                      type="number"
                      fullWidth
                      value={inputs.transactionCosts}
                      onChange={(e) => handleInputChange('transactionCosts', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 1: Debt Terms */}
            <TabPanel value={tabValue} index={1}>
              <Stack spacing={3}>
                <Alert severity="info">
                  Configure debt tranches and cash sweep mechanics
                </Alert>

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Term Loan A</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Amount ($M) - Optional"
                      type="number"
                      fullWidth
                      value={inputs.tlaAmount}
                      onChange={(e) => handleInputChange('tlaAmount', e.target.value)}
                      helperText="Leave blank to auto-calculate"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Interest Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlaRate}
                      onChange={(e) => handleInputChange('tlaRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Mandatory Amortization (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlaMandAmort}
                      onChange={(e) => handleInputChange('tlaMandAmort', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="% of original principal, annually"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cash Sweep (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlaCashSweep}
                      onChange={(e) => handleInputChange('tlaCashSweep', e.target.value)}
                      helperText="Typically 100%"
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Term Loan B</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Amount ($M) - Optional"
                      type="number"
                      fullWidth
                      value={inputs.tlbAmount}
                      onChange={(e) => handleInputChange('tlbAmount', e.target.value)}
                      helperText="Leave blank to auto-calculate"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Interest Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlbRate}
                      onChange={(e) => handleInputChange('tlbRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Mandatory Amortization (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlbMandAmort}
                      onChange={(e) => handleInputChange('tlbMandAmort', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cash Sweep (%)"
                      type="number"
                      fullWidth
                      value={inputs.tlbCashSweep}
                      onChange={(e) => handleInputChange('tlbCashSweep', e.target.value)}
                      helperText="After TLA paid off"
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Subordinated Debt</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Amount ($M) - Optional"
                      type="number"
                      fullWidth
                      value={inputs.subDebtAmount}
                      onChange={(e) => handleInputChange('subDebtAmount', e.target.value)}
                      helperText="Leave blank to auto-calculate"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Interest Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.subDebtRate}
                      onChange={(e) => handleInputChange('subDebtRate', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Cash Sweep Parameters</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Minimum Cash Balance ($M)"
                      type="number"
                      fullWidth
                      value={inputs.minCashBalance}
                      onChange={(e) => handleInputChange('minCashBalance', e.target.value)}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 2: Operations */}
            <TabPanel value={tabValue} index={2}>
              <Stack spacing={3}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>Revenue Growth Rates (%)</Typography>
                <Grid container spacing={2}>
                  {[1, 2, 3, 4, 5, 6, 7].map((year) => (
                    <Grid item xs={6} sm={4} md={3} key={`rev-growth-${year}`}>
                      <TextField
                        label={`Year ${year}`}
                        type="number"
                        fullWidth
                        size="small"
                        value={inputs[`revenueGrowthY${year}` as keyof typeof inputs]}
                        onChange={(e) => handleInputChange(`revenueGrowthY${year}`, e.target.value)}
                        inputProps={{ step: 0.5 }}
                      />
                    </Grid>
                  ))}
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>EBITDA Margins (%)</Typography>
                <Grid container spacing={2}>
                  {[1, 2, 3, 4, 5, 6, 7].map((year) => (
                    <Grid item xs={6} sm={4} md={3} key={`ebitda-margin-${year}`}>
                      <TextField
                        label={`Year ${year}`}
                        type="number"
                        fullWidth
                        size="small"
                        value={inputs[`ebitdaMarginY${year}` as keyof typeof inputs]}
                        onChange={(e) => handleInputChange(`ebitdaMarginY${year}`, e.target.value)}
                        inputProps={{ step: 0.5 }}
                      />
                    </Grid>
                  ))}
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Other Operating Assumptions</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={3}>
                    <TextField
                      label="D&A (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.dnaPercent}
                      onChange={(e) => handleInputChange('dnaPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={3}>
                    <TextField
                      label="CapEx (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.capexPercent}
                      onChange={(e) => handleInputChange('capexPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={3}>
                    <TextField
                      label="NWC (% of Revenue)"
                      type="number"
                      fullWidth
                      value={inputs.nwcPercent}
                      onChange={(e) => handleInputChange('nwcPercent', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={3}>
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
              </Stack>
            </TabPanel>

            {/* Tab 3: Exit & Waterfall */}
            <TabPanel value={tabValue} index={3}>
              <Stack spacing={3}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>Exit Assumptions</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Exit EV/EBITDA Multiple (x)"
                      type="number"
                      fullWidth
                      value={inputs.exitEvEbitdaMultiple}
                      onChange={(e) => handleInputChange('exitEvEbitdaMultiple', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="Conservative: same as entry"
                    />
                  </Grid>
                </Grid>

                <Divider />

                <Typography variant="h6" sx={{ fontWeight: 600 }}>Distribution Waterfall (European-Style)</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Preferred Return / Hurdle (%)"
                      type="number"
                      fullWidth
                      value={inputs.preferredReturn}
                      onChange={(e) => handleInputChange('preferredReturn', e.target.value)}
                      inputProps={{ step: 0.5 }}
                      helperText="Typically 8%"
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="GP Catch-Up (%)"
                      type="number"
                      fullWidth
                      value={inputs.gpCatchup}
                      onChange={(e) => handleInputChange('gpCatchup', e.target.value)}
                      helperText="Typically 100%"
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Carried Interest (%)"
                      type="number"
                      fullWidth
                      value={inputs.carriedInterest}
                      onChange={(e) => handleInputChange('carriedInterest', e.target.value)}
                      helperText="Typically 20%"
                    />
                  </Grid>
                </Grid>

                <Alert severity="info">
                  European waterfall: GP carry only after ALL LP capital returned + preferred return
                </Alert>
              </Stack>
            </TabPanel>

            {/* Tab 4: Scenario Analysis */}
            <TabPanel value={tabValue} index={4}>
              <Stack spacing={3}>
                <Alert severity="info">
                  Comprehensive risk analysis with Monte Carlo simulations, sensitivity analysis, and break-even calculations for LBO returns.
                </Alert>

                {(() => {
                  // Define scenario variables based on current LBO inputs
                  const scenarioVariables: Variable[] = [
                    {
                      name: 'ltmEbitda',
                      label: 'LTM EBITDA',
                      baseValue: parseFloat(inputs.ltmEbitda || '100'),
                      min: parseFloat(inputs.ltmEbitda || '100') * 0.7,
                      max: parseFloat(inputs.ltmEbitda || '100') * 1.3,
                      step: 5,
                      unit: '$M',
                    },
                    {
                      name: 'entryMultiple',
                      label: 'Entry EV/EBITDA Multiple',
                      baseValue: parseFloat(inputs.entryEvEbitdaMultiple || '10'),
                      min: 7,
                      max: 13,
                      step: 0.5,
                      unit: 'x',
                    },
                    {
                      name: 'exitMultiple',
                      label: 'Exit EV/EBITDA Multiple',
                      baseValue: parseFloat(inputs.exitEvEbitdaMultiple || '10'),
                      min: 7,
                      max: 13,
                      step: 0.5,
                      unit: 'x',
                    },
                    {
                      name: 'revenueGrowth',
                      label: 'Avg Revenue Growth',
                      baseValue: parseFloat(inputs.revenueGrowthY1 || '5'),
                      min: 0,
                      max: 15,
                      step: 0.5,
                      unit: '%',
                    },
                    {
                      name: 'ebitdaMargin',
                      label: 'EBITDA Margin',
                      baseValue: parseFloat(inputs.ebitdaMarginY1 || '22'),
                      min: 15,
                      max: 35,
                      step: 1,
                      unit: '%',
                    },
                    {
                      name: 'totalLeverage',
                      label: 'Total Leverage (Debt/EBITDA)',
                      baseValue: parseFloat(inputs.totalLeverage || '5'),
                      min: 3,
                      max: 7,
                      step: 0.25,
                      unit: 'x',
                    },
                  ];

                  // LBO IRR calculation function for scenario analysis
                  const calculateIRR = (vars: Record<string, number>): number => {
                    try {
                      const ltmEbitda = vars.ltmEbitda;
                      const entryMultiple = vars.entryMultiple;
                      const exitMultiple = vars.exitMultiple;
                      const avgGrowth = vars.revenueGrowth / 100;
                      const avgEbitdaMargin = vars.ebitdaMargin / 100;
                      const totalLeverage = vars.totalLeverage;

                      const holdingPeriod = parseInt(inputs.holdingPeriod || '5');

                      // Purchase Price
                      const purchasePrice = ltmEbitda * entryMultiple;

                      // Financing
                      const totalDebt = ltmEbitda * totalLeverage;
                      const transCosts = (parseFloat(inputs.transactionCosts || '2') / 100) * purchasePrice;
                      const existingCash = parseFloat(inputs.existingCash || '0');
                      const existingDebtPayoff = parseFloat(inputs.existingDebtPayoff || '0');
                      const totalUses = purchasePrice + transCosts - existingCash + existingDebtPayoff;
                      const equityContribution = totalUses - totalDebt;

                      // Exit projection
                      const ltmRevenue = parseFloat(inputs.ltmRevenue || '1000');
                      const exitRevenue = ltmRevenue * Math.pow(1 + avgGrowth, holdingPeriod);
                      const exitEbitda = exitRevenue * avgEbitdaMargin;
                      const exitEV = exitEbitda * exitMultiple;

                      // Simplified debt paydown (assume 40% of original debt paid down)
                      const debtPaydownPct = 0.4;
                      const exitDebt = totalDebt * (1 - debtPaydownPct);

                      // Exit equity value
                      const exitEquityValue = exitEV - exitDebt;

                      // Returns
                      const moic = exitEquityValue / equityContribution;
                      const irr = (Math.pow(moic, 1 / holdingPeriod) - 1) * 100;

                      return irr;
                    } catch (error) {
                      console.error('LBO scenario calculation error:', error);
                      return 0;
                    }
                  };

                  return (
                    <ScenarioAnalysis
                      calculateMetric={calculateIRR}
                      variables={scenarioVariables}
                      metricName="IRR"
                      metricUnit="%"
                      breakEvenTarget={15}
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
                onClick={calculateLBO}
                fullWidth
                sx={{
                  py: 1.5,
                  background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                  fontWeight: 600,
                }}
              >
                Calculate Returns
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Results Summary Panel */}
        <Grid item xs={12} lg={4}>
          <Stack spacing={3}>
            {results && (
              <>
                {/* Returns Card */}
                <Card sx={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)', color: 'white' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                      Investment Returns
                    </Typography>

                    <Grid container spacing={3}>
                      <Grid item xs={6}>
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>IRR</Typography>
                          <Typography variant="h3" sx={{ fontWeight: 700 }}>
                            {results.irr.toFixed(1)}%
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>MOIC</Typography>
                          <Typography variant="h3" sx={{ fontWeight: 700 }}>
                            {results.moic.toFixed(2)}x
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>

                    <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />

                    <Box sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                      <Typography variant="caption" sx={{ display: 'block', mb: 0.5 }}>
                        Investment Grade
                      </Typography>
                      <Chip
                        label={
                          results.irr >= 25 ? 'EXCELLENT' :
                          results.irr >= 20 ? 'GOOD' :
                          results.irr >= 15 ? 'ACCEPTABLE' : 'BELOW TARGET'
                        }
                        sx={{
                          bgcolor: results.irr >= 20 ? '#10b981' : results.irr >= 15 ? '#f59e0b' : '#ef4444',
                          color: 'white',
                          fontWeight: 700,
                        }}
                      />
                    </Box>
                  </CardContent>
                </Card>

                {/* Transaction Summary */}
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1.5, fontWeight: 600 }}>
                    Transaction Summary
                  </Typography>
                  <Stack spacing={1}>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="caption">Purchase Price</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatCurrency(results.purchasePrice)}M</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="caption">Total Debt</Typography>
                      <Typography variant="body2">{formatCurrency(results.totalDebt)}M</Typography>
                    </Stack>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="caption">Equity</Typography>
                      <Typography variant="body2" fontWeight={600}>{formatCurrency(results.equityContribution)}M</Typography>
                    </Stack>
                  </Stack>
                </Paper>

                {/* Debt Paydown Progress */}
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle2" sx={{ mb: 1.5, fontWeight: 600 }}>
                    Debt Paydown
                  </Typography>
                  <Stack spacing={1}>
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="caption">Initial Debt</Typography>
                      <Typography variant="body2">{formatCurrency(results.totalDebt)}M</Typography>
                    </Stack>
                    <LinearProgress
                      variant="determinate"
                      value={(results.totalDebtPaydown / results.totalDebt) * 100}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                    <Stack direction="row" justifyContent="space-between">
                      <Typography variant="caption">Debt Paid Down</Typography>
                      <Typography variant="body2" fontWeight={600} color="success.main">
                        {formatCurrency(results.totalDebtPaydown)}M ({formatPercent((results.totalDebtPaydown / results.totalDebt) * 100, 0)})
                      </Typography>
                    </Stack>
                  </Stack>
                </Paper>

                {/* Action Buttons */}
                <Stack direction="row" spacing={2}>
                  <Button variant="outlined" startIcon={<SaveIcon />} fullWidth>Save</Button>
                  <Button variant="outlined" startIcon={<DownloadIcon />} fullWidth>Export</Button>
                </Stack>
              </>
            )}

            {!results && (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  Enter transaction details and click "Calculate Returns"
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>

        {/* Full Width Results Tables */}
        {results && (
          <>
            {/* Debt Schedule */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Debt Schedule with Cash Sweep
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Year</TableCell>
                        <TableCell align="right">TLA Beg</TableCell>
                        <TableCell align="right">TLA Amort</TableCell>
                        <TableCell align="right">TLA End</TableCell>
                        <TableCell align="right">TLB Beg</TableCell>
                        <TableCell align="right">TLB Amort</TableCell>
                        <TableCell align="right">TLB End</TableCell>
                        <TableCell align="right">Sub Debt</TableCell>
                        <TableCell align="right">Total Debt</TableCell>
                        <TableCell align="right">Interest</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.debtSchedule.map((row: any) => (
                        <TableRow key={row.year}>
                          <TableCell>{row.year}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tla.beg)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tla.mandAmort + row.tla.optPayment)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tla.end)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tlb.beg)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tlb.mandAmort + row.tlb.optPayment)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.tlb.end)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.sub.end)}</TableCell>
                          <TableCell align="right" sx={{ fontWeight: 600 }}>{formatCurrency(row.totalDebt)}</TableCell>
                          <TableCell align="right">{formatCurrency(row.interest)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Credit Metrics */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Credit Metrics
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Year</TableCell>
                        <TableCell align="right">Debt/EBITDA</TableCell>
                        <TableCell align="right">EBITDA/Interest</TableCell>
                        <TableCell align="right">EBIT/Interest</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.creditMetrics.map((row: any) => (
                        <TableRow key={row.year}>
                          <TableCell>{row.year}</TableCell>
                          <TableCell align="right">
                            <Typography
                              variant="body2"
                              sx={{ color: row.totalDebtEbitda <= 4.0 ? '#10b981' : row.totalDebtEbitda <= 5.5 ? '#f59e0b' : '#ef4444' }}
                            >
                              {row.totalDebtEbitda.toFixed(2)}x
                            </Typography>
                          </TableCell>
                          <TableCell align="right">
                            <Typography
                              variant="body2"
                              sx={{ color: row.ebitdaInterest >= 3.0 ? '#10b981' : row.ebitdaInterest >= 2.0 ? '#f59e0b' : '#ef4444' }}
                            >
                              {row.ebitdaInterest.toFixed(2)}x
                            </Typography>
                          </TableCell>
                          <TableCell align="right">{row.ebitInterest.toFixed(2)}x</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Paper>
            </Grid>

            {/* Distribution Waterfall */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Distribution Waterfall
                </Typography>

                <Stack spacing={2}>
                  <Box sx={{ p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                    <Typography variant="caption" color="text.secondary">Total Distributions</Typography>
                    <Typography variant="h6" fontWeight={700}>{formatCurrency(results.waterfall.totalDistributions)}M</Typography>
                  </Box>

                  <Table size="small">
                    <TableBody>
                      <TableRow>
                        <TableCell>Tier 1: Return of Capital</TableCell>
                        <TableCell align="right">{formatCurrency(results.waterfall.tier1ReturnOfCapital)}M</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Tier 2: Preferred Return</TableCell>
                        <TableCell align="right">{formatCurrency(results.waterfall.tier2PreferredReturn)}M</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Tier 3: GP Catch-Up</TableCell>
                        <TableCell align="right">{formatCurrency(results.waterfall.tier3GPCatchup)}M</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Tier 4: LP Share</TableCell>
                        <TableCell align="right">{formatCurrency(results.waterfall.tier4Split.lp)}M</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Tier 4: GP Share</TableCell>
                        <TableCell align="right">{formatCurrency(results.waterfall.tier4Split.gp)}M</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>

                  <Divider />

                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Box sx={{ p: 2, bgcolor: 'primary.50', borderRadius: 1 }}>
                        <Typography variant="caption" color="text.secondary">Total to LPs</Typography>
                        <Typography variant="h6" fontWeight={700}>{formatCurrency(results.waterfall.totalLP)}M</Typography>
                        <Typography variant="body2" color="primary">{formatPercent(results.waterfall.lpPct)}</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Box sx={{ p: 2, bgcolor: 'success.50', borderRadius: 1 }}>
                        <Typography variant="caption" color="text.secondary">Total to GP</Typography>
                        <Typography variant="h6" fontWeight={700}>{formatCurrency(results.waterfall.totalGP)}M</Typography>
                        <Typography variant="body2" color="success.main">{formatPercent(results.waterfall.gpPct)}</Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Stack>
              </Paper>
            </Grid>

            {/* Sensitivity Analysis */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Sensitivity Analysis: Revenue Growth vs Exit Multiple (IRR %)
                </Typography>

                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell>Revenue Growth →<br />Exit Multiple ↓</TableCell>
                        {results.sensitivity.revenueGrowthScenarios.map((growth: number, idx: number) => (
                          <TableCell key={idx} align="center">
                            {formatPercent(growth * 100, 0)}
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {results.sensitivity.exitMultiples.map((exitMult: number, rowIdx: number) => (
                        <TableRow key={rowIdx}>
                          <TableCell sx={{ fontWeight: 600 }}>{exitMult.toFixed(1)}x</TableCell>
                          {results.sensitivity.irrTable.map((row: number[], colIdx: number) => (
                            <TableCell
                              key={colIdx}
                              align="center"
                              sx={{
                                bgcolor: row[rowIdx] >= 20 ? 'rgba(16, 185, 129, 0.1)' : row[rowIdx] >= 15 ? 'rgba(245, 158, 11, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                                fontWeight: 500,
                              }}
                            >
                              {formatPercent(row[rowIdx])}
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
