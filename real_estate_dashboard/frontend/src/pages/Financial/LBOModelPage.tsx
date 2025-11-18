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
} from '@mui/material';
import {
  AccountBalance as LBOIcon,
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
      id={`lbo-tabpanel-${index}`}
      aria-labelledby={`lbo-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const LBOModelPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    // Transaction
    companyName: '',
    purchasePrice: '',
    entryMultiple: '10',
    exitMultiple: '11',

    // Financing
    seniorDebt: '40',
    subordinatedDebt: '20',
    equityContribution: '40',

    // Operating Assumptions
    year1Revenue: '',
    revenueGrowth: '5',
    ebitdaMargin: '25',

    // Other
    holdPeriod: '5',
    taxRate: '21',
  });

  const [results, setResults] = useState<any>(null);

  const handleInputChange = (field: string, value: string) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const calculateLBO = () => {
    const purchasePrice = parseFloat(inputs.purchasePrice) || 0;
    const entryMultiple = parseFloat(inputs.entryMultiple);
    const exitMultiple = parseFloat(inputs.exitMultiple);
    const seniorDebt = (parseFloat(inputs.seniorDebt) / 100) * purchasePrice;
    const subDebt = (parseFloat(inputs.subordinatedDebt) / 100) * purchasePrice;
    const equity = (parseFloat(inputs.equityContribution) / 100) * purchasePrice;

    const year1Revenue = parseFloat(inputs.year1Revenue) || 0;
    const revenueGrowth = parseFloat(inputs.revenueGrowth) / 100;
    const ebitdaMargin = parseFloat(inputs.ebitdaMargin) / 100;
    const holdPeriod = parseInt(inputs.holdPeriod) || 5;

    // Calculate exit revenue and EBITDA
    const exitRevenue = year1Revenue * Math.pow(1 + revenueGrowth, holdPeriod - 1);
    const exitEBITDA = exitRevenue * ebitdaMargin;
    const exitEV = exitEBITDA * exitMultiple;

    // Simplified debt paydown
    const totalDebt = seniorDebt + subDebt;
    const avgDebtPaydown = totalDebt * 0.4; // Assume 40% debt paydown
    const remainingDebt = totalDebt - avgDebtPaydown;

    // Exit equity value
    const exitEquityValue = exitEV - remainingDebt;

    // Returns
    const moic = exitEquityValue / equity;
    const irr = (Math.pow(moic, 1 / holdPeriod) - 1) * 100;

    setResults({
      purchasePrice,
      seniorDebt,
      subDebt,
      equity,
      totalDebt,
      exitEV,
      exitEBITDA,
      exitEquityValue,
      moic,
      irr,
      remainingDebt,
      avgDebtPaydown,
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
            LBO Model
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Leveraged Buyout analysis for private equity transactions
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={7}>
          <Paper sx={{ p: 3 }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Transaction" />
              <Tab label="Financing" />
              <Tab label="Operations" />
            </Tabs>

            {/* Tab 0: Transaction */}
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
                      label="Purchase Price ($M)"
                      type="number"
                      fullWidth
                      value={inputs.purchasePrice}
                      onChange={(e) => handleInputChange('purchasePrice', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Entry EBITDA Multiple (x)"
                      type="number"
                      fullWidth
                      value={inputs.entryMultiple}
                      onChange={(e) => handleInputChange('entryMultiple', e.target.value)}
                      inputProps={{ step: 0.5 }}
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
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Hold Period (Years)"
                      type="number"
                      fullWidth
                      value={inputs.holdPeriod}
                      onChange={(e) => handleInputChange('holdPeriod', e.target.value)}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 1: Financing */}
            <TabPanel value={tabValue} index={1}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Capital Structure (% of Purchase Price)
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Senior Debt (%)"
                      type="number"
                      fullWidth
                      value={inputs.seniorDebt}
                      onChange={(e) => handleInputChange('seniorDebt', e.target.value)}
                      inputProps={{ step: 5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Subordinated Debt (%)"
                      type="number"
                      fullWidth
                      value={inputs.subordinatedDebt}
                      onChange={(e) => handleInputChange('subordinatedDebt', e.target.value)}
                      inputProps={{ step: 5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <TextField
                      label="Equity (%)"
                      type="number"
                      fullWidth
                      value={inputs.equityContribution}
                      onChange={(e) => handleInputChange('equityContribution', e.target.value)}
                      inputProps={{ step: 5 }}
                    />
                  </Grid>
                </Grid>

                <Chip
                  label={`Total: ${(parseFloat(inputs.seniorDebt) + parseFloat(inputs.subordinatedDebt) + parseFloat(inputs.equityContribution)).toFixed(0)}%`}
                  color={(parseFloat(inputs.seniorDebt) + parseFloat(inputs.subordinatedDebt) + parseFloat(inputs.equityContribution)) === 100 ? 'success' : 'error'}
                />
              </Stack>
            </TabPanel>

            {/* Tab 2: Operations */}
            <TabPanel value={tabValue} index={2}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Operating Performance Assumptions
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Year 1 Revenue ($M)"
                      type="number"
                      fullWidth
                      value={inputs.year1Revenue}
                      onChange={(e) => handleInputChange('year1Revenue', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Annual Revenue Growth (%)"
                      type="number"
                      fullWidth
                      value={inputs.revenueGrowth}
                      onChange={(e) => handleInputChange('revenueGrowth', e.target.value)}
                      inputProps={{ step: 0.5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="EBITDA Margin (%)"
                      type="number"
                      fullWidth
                      value={inputs.ebitdaMargin}
                      onChange={(e) => handleInputChange('ebitdaMargin', e.target.value)}
                      inputProps={{ step: 0.5 }}
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

        {/* Results Panel */}
        <Grid item xs={12} lg={5}>
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
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            IRR
                          </Typography>
                          <Typography variant="h3" sx={{ fontWeight: 700 }}>
                            {results.irr.toFixed(1)}%
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            MOIC
                          </Typography>
                          <Typography variant="h3" sx={{ fontWeight: 700 }}>
                            {results.moic.toFixed(2)}x
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>

                    <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />

                    <Box
                      sx={{
                        p: 2,
                        bgcolor: 'rgba(255,255,255,0.1)',
                        borderRadius: 2,
                      }}
                    >
                      <Typography variant="caption" sx={{ display: 'block', mb: 0.5 }}>
                        Investment Grade
                      </Typography>
                      <Chip
                        label={results.irr >= 25 ? 'EXCELLENT' : results.irr >= 20 ? 'GOOD' : results.irr >= 15 ? 'ACCEPTABLE' : 'BELOW TARGET'}
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
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Transaction Summary
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableBody>
                        <TableRow>
                          <TableCell>Purchase Price</TableCell>
                          <TableCell align="right">{formatCurrency(results.purchasePrice)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Senior Debt</TableCell>
                          <TableCell align="right">{formatCurrency(results.seniorDebt)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Subordinated Debt</TableCell>
                          <TableCell align="right">{formatCurrency(results.subDebt)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell><strong>Equity Contribution</strong></TableCell>
                          <TableCell align="right"><strong>{formatCurrency(results.equity)}M</strong></TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>

                {/* Exit Summary */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Exit Summary
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableBody>
                        <TableRow>
                          <TableCell>Exit EBITDA</TableCell>
                          <TableCell align="right">{formatCurrency(results.exitEBITDA)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Exit Enterprise Value</TableCell>
                          <TableCell align="right">{formatCurrency(results.exitEV)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Remaining Debt</TableCell>
                          <TableCell align="right">({formatCurrency(results.remainingDebt)}M)</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell><strong>Exit Equity Value</strong></TableCell>
                          <TableCell align="right"><strong>{formatCurrency(results.exitEquityValue)}M</strong></TableCell>
                        </TableRow>
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
                    Save Model
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
                  Enter your transaction details and click "Calculate Returns" to see the analysis
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
