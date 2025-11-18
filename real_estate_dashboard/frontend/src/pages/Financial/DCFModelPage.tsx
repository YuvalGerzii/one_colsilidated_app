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
  alpha,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';

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

export const DCFModelPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    // Company Info
    companyName: '',
    currentStockPrice: '',
    sharesOutstanding: '',

    // Financial Projections (Year 1-5)
    revenue1: '',
    revenue2: '',
    revenue3: '',
    revenue4: '',
    revenue5: '',

    ebitdaMargin1: '',
    ebitdaMargin2: '',
    ebitdaMargin3: '',
    ebitdaMargin4: '',
    ebitdaMargin5: '',

    // WACC Inputs
    riskFreeRate: '4.5',
    beta: '1.2',
    marketRiskPremium: '7.0',
    costOfDebt: '5.0',
    taxRate: '21',
    debtToEquity: '0.5',

    // Terminal Value
    terminalGrowthRate: '2.5',
    exitMultiple: '12',
  });

  const [results, setResults] = useState<any>(null);

  const handleInputChange = (field: string, value: string) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const calculateDCF = () => {
    // WACC Calculation
    const riskFree = parseFloat(inputs.riskFreeRate) / 100;
    const beta = parseFloat(inputs.beta);
    const marketPremium = parseFloat(inputs.marketRiskPremium) / 100;
    const costOfDebt = parseFloat(inputs.costOfDebt) / 100;
    const taxRate = parseFloat(inputs.taxRate) / 100;
    const debtToEquity = parseFloat(inputs.debtToEquity);

    const costOfEquity = riskFree + beta * marketPremium;
    const wacc = (costOfEquity * (1 / (1 + debtToEquity))) + (costOfDebt * (1 - taxRate) * (debtToEquity / (1 + debtToEquity)));

    // Calculate FCF for each year
    const revenues = [
      parseFloat(inputs.revenue1 || '0'),
      parseFloat(inputs.revenue2 || '0'),
      parseFloat(inputs.revenue3 || '0'),
      parseFloat(inputs.revenue4 || '0'),
      parseFloat(inputs.revenue5 || '0'),
    ];

    const ebitdaMargins = [
      parseFloat(inputs.ebitdaMargin1 || '20') / 100,
      parseFloat(inputs.ebitdaMargin2 || '22') / 100,
      parseFloat(inputs.ebitdaMargin3 || '24') / 100,
      parseFloat(inputs.ebitdaMargin4 || '25') / 100,
      parseFloat(inputs.ebitdaMargin5 || '26') / 100,
    ];

    const fcfs = revenues.map((rev, i) => rev * ebitdaMargins[i] * 0.7); // Simplified FCF

    // Terminal Value
    const terminalGrowth = parseFloat(inputs.terminalGrowthRate) / 100;
    const terminalValue = (fcfs[4] * (1 + terminalGrowth)) / (wacc - terminalGrowth);

    // PV Calculations
    const pvFCFs = fcfs.map((fcf, i) => fcf / Math.pow(1 + wacc, i + 1));
    const pvTerminal = terminalValue / Math.pow(1 + wacc, 5);

    const enterpriseValue = pvFCFs.reduce((sum, pv) => sum + pv, 0) + pvTerminal;
    const sharesOutstanding = parseFloat(inputs.sharesOutstanding) || 1;
    const impliedSharePrice = enterpriseValue / sharesOutstanding;

    const currentPrice = parseFloat(inputs.currentStockPrice) || 0;
    const upside = currentPrice > 0 ? ((impliedSharePrice - currentPrice) / currentPrice) * 100 : 0;

    setResults({
      wacc: wacc * 100,
      costOfEquity: costOfEquity * 100,
      fcfs,
      pvFCFs,
      terminalValue,
      pvTerminal,
      enterpriseValue,
      impliedSharePrice,
      currentPrice,
      upside,
    });
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${value.toFixed(2)}%`;
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
            DCF Valuation Model
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Discounted Cash Flow analysis with comprehensive sensitivity testing
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={7}>
          <Paper sx={{ p: 3 }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Company Info" />
              <Tab label="Projections" />
              <Tab label="WACC" />
              <Tab label="Terminal Value" />
            </Tabs>

            {/* Tab 0: Company Info */}
            <TabPanel value={tabValue} index={0}>
              <Stack spacing={3}>
                <TextField
                  label="Company Name"
                  fullWidth
                  value={inputs.companyName}
                  onChange={(e) => handleInputChange('companyName', e.target.value)}
                />
                <Grid container spacing={2}>
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
              </Stack>
            </TabPanel>

            {/* Tab 1: Projections */}
            <TabPanel value={tabValue} index={1}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  5-Year Financial Projections (in millions)
                </Typography>

                <Box>
                  <Typography variant="body2" fontWeight={600} sx={{ mb: 2 }}>
                    Revenue Projections
                  </Typography>
                  <Grid container spacing={2}>
                    {[1, 2, 3, 4, 5].map((year) => (
                      <Grid item xs={12} sm={6} md={4} key={`revenue-${year}`}>
                        <TextField
                          label={`Year ${year} Revenue`}
                          type="number"
                          fullWidth
                          value={inputs[`revenue${year}` as keyof typeof inputs]}
                          onChange={(e) => handleInputChange(`revenue${year}`, e.target.value)}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Box>

                <Box>
                  <Typography variant="body2" fontWeight={600} sx={{ mb: 2 }}>
                    EBITDA Margin (%)
                  </Typography>
                  <Grid container spacing={2}>
                    {[1, 2, 3, 4, 5].map((year) => (
                      <Grid item xs={12} sm={6} md={4} key={`ebitda-${year}`}>
                        <TextField
                          label={`Year ${year} Margin`}
                          type="number"
                          fullWidth
                          value={inputs[`ebitdaMargin${year}` as keyof typeof inputs]}
                          onChange={(e) => handleInputChange(`ebitdaMargin${year}`, e.target.value)}
                          inputProps={{ step: 0.1 }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              </Stack>
            </TabPanel>

            {/* Tab 2: WACC */}
            <TabPanel value={tabValue} index={2}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Weighted Average Cost of Capital Components
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Risk-Free Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.riskFreeRate}
                      onChange={(e) => handleInputChange('riskFreeRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Beta"
                      type="number"
                      fullWidth
                      value={inputs.beta}
                      onChange={(e) => handleInputChange('beta', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Market Risk Premium (%)"
                      type="number"
                      fullWidth
                      value={inputs.marketRiskPremium}
                      onChange={(e) => handleInputChange('marketRiskPremium', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cost of Debt (%)"
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
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Debt-to-Equity Ratio"
                      type="number"
                      fullWidth
                      value={inputs.debtToEquity}
                      onChange={(e) => handleInputChange('debtToEquity', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 3: Terminal Value */}
            <TabPanel value={tabValue} index={3}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Terminal Value Assumptions
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Terminal Growth Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.terminalGrowthRate}
                      onChange={(e) => handleInputChange('terminalGrowthRate', e.target.value)}
                      inputProps={{ step: 0.1 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Exit EBITDA Multiple (x)"
                      type="number"
                      fullWidth
                      value={inputs.exitMultiple}
                      onChange={(e) => handleInputChange('exitMultiple', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Calculate Button */}
            <Box sx={{ mt: 3 }}>
              <Stack direction="row" spacing={2}>
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
              </Stack>
            </Box>
          </Paper>
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} lg={5}>
          <Stack spacing={3}>
            {/* Summary Card */}
            {results && (
              <>
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
                          label={results.upside >= 20 ? 'STRONG BUY' : results.upside >= 10 ? 'BUY' : results.upside >= 0 ? 'HOLD' : results.upside >= -10 ? 'SELL' : 'STRONG SELL'}
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

                {/* Detailed Results */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Detailed Analysis
                  </Typography>

                  <Stack spacing={2}>
                    <Box>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          WACC
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatPercent(results.wacc)}
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          Cost of Equity
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatPercent(results.costOfEquity)}
                        </Typography>
                      </Stack>
                    </Box>

                    <Divider />

                    <Box>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          Enterprise Value
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(results.enterpriseValue)}M
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.5 }}>
                        <Typography variant="body2" color="text.secondary">
                          Terminal Value (PV)
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(results.pvTerminal)}M
                        </Typography>
                      </Stack>
                    </Box>
                  </Stack>
                </Paper>

                {/* Cash Flow Table */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Free Cash Flow Analysis
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Year</TableCell>
                          <TableCell align="right">FCF ($M)</TableCell>
                          <TableCell align="right">PV ($M)</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {results.fcfs.map((fcf: number, idx: number) => (
                          <TableRow key={idx}>
                            <TableCell>{idx + 1}</TableCell>
                            <TableCell align="right">{formatCurrency(fcf)}</TableCell>
                            <TableCell align="right">{formatCurrency(results.pvFCFs[idx])}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>

                {/* Action Buttons */}
                <Stack direction="row" spacing={2}>
                  <Button
                    variant="outlined"
                    startIcon={<SaveIcon />}
                    fullWidth
                  >
                    Save Report
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<DownloadIcon />}
                    fullWidth
                  >
                    Export Excel
                  </Button>
                </Stack>
              </>
            )}

            {!results && (
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <AssessmentIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  Enter your inputs and click "Calculate Valuation" to see the results
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
