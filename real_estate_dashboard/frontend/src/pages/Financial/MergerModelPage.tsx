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
  MergeType as MergerIcon,
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
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
      id={`merger-tabpanel-${index}`}
      aria-labelledby={`merger-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const MergerModelPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [inputs, setInputs] = useState({
    // Acquirer
    acquirerName: '',
    acquirerShares: '',
    acquirerSharePrice: '',
    acquirerEPS: '',
    acquirerPE: '',
    acquirerNetIncome: '',

    // Target
    targetName: '',
    targetShares: '',
    targetSharePrice: '',
    targetEPS: '',
    targetPE: '',
    targetNetIncome: '',

    // Deal Terms
    offerPremium: '30',
    cashPortion: '50',
    stockPortion: '50',

    // Synergies
    costSynergies: '',
    revenueSynergies: '',
    synergiesYear: '3',

    // Financing
    debtFinancing: '',
    debtInterestRate: '6',
    taxRate: '21',
  });

  const [results, setResults] = useState<any>(null);

  const handleInputChange = (field: string, value: string) => {
    setInputs(prev => ({ ...prev, [field]: value }));
  };

  const calculateMerger = () => {
    // Acquirer metrics
    const acquirerShares = parseFloat(inputs.acquirerShares) || 0;
    const acquirerPrice = parseFloat(inputs.acquirerSharePrice) || 0;
    const acquirerEPS = parseFloat(inputs.acquirerEPS) || 0;
    const acquirerNetIncome = parseFloat(inputs.acquirerNetIncome) || 0;

    // Target metrics
    const targetShares = parseFloat(inputs.targetShares) || 0;
    const targetPrice = parseFloat(inputs.targetSharePrice) || 0;
    const targetNetIncome = parseFloat(inputs.targetNetIncome) || 0;

    // Deal terms
    const premium = parseFloat(inputs.offerPremium) / 100;
    const cashPortion = parseFloat(inputs.cashPortion) / 100;
    const stockPortion = parseFloat(inputs.stockPortion) / 100;

    // Calculate offer price and value
    const offerPrice = targetPrice * (1 + premium);
    const targetEquityValue = targetShares * offerPrice;

    // Calculate shares issued
    const cashConsideration = targetEquityValue * cashPortion;
    const stockConsideration = targetEquityValue * stockPortion;
    const newSharesIssued = stockConsideration / acquirerPrice;

    // Calculate debt financing
    const debtFinancing = parseFloat(inputs.debtFinancing) || 0;
    const debtRate = parseFloat(inputs.debtInterestRate) / 100;
    const taxRate = parseFloat(inputs.taxRate) / 100;
    const annualInterest = debtFinancing * debtRate;
    const afterTaxInterest = annualInterest * (1 - taxRate);

    // Calculate synergies
    const costSynergies = parseFloat(inputs.costSynergies) || 0;
    const revenueSynergies = parseFloat(inputs.revenueSynergies) || 0;
    const totalSynergies = (costSynergies + revenueSynergies) * (1 - taxRate);

    // Pro forma calculations
    const proFormaNetIncome = acquirerNetIncome + targetNetIncome - afterTaxInterest + totalSynergies;
    const proFormaShares = acquirerShares + newSharesIssued;
    const proFormaEPS = proFormaNetIncome / proFormaShares;

    // Accretion/Dilution
    const accretionDilution = ((proFormaEPS - acquirerEPS) / acquirerEPS) * 100;
    const isAccretive = accretionDilution > 0;

    // Ownership split
    const acquirerOwnership = (acquirerShares / proFormaShares) * 100;
    const targetOwnership = (newSharesIssued / proFormaShares) * 100;

    setResults({
      offerPrice,
      targetEquityValue,
      cashConsideration,
      stockConsideration,
      newSharesIssued,
      proFormaNetIncome,
      proFormaShares,
      proFormaEPS,
      accretionDilution,
      isAccretive,
      acquirerOwnership,
      targetOwnership,
      totalSynergies,
      afterTaxInterest,
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
            background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(245, 158, 11, 0.3)',
          }}
        >
          <MergerIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            M&A Merger Model
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Accretion/Dilution analysis for merger & acquisition transactions
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={7}>
          <Paper sx={{ p: 3 }}>
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ mb: 3 }}>
              <Tab label="Companies" />
              <Tab label="Deal Terms" />
              <Tab label="Synergies" />
            </Tabs>

            {/* Tab 0: Companies */}
            <TabPanel value={tabValue} index={0}>
              <Stack spacing={4}>
                {/* Acquirer */}
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                    Acquirer Company
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <TextField
                        label="Company Name"
                        fullWidth
                        value={inputs.acquirerName}
                        onChange={(e) => handleInputChange('acquirerName', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Shares Outstanding (M)"
                        type="number"
                        fullWidth
                        value={inputs.acquirerShares}
                        onChange={(e) => handleInputChange('acquirerShares', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Current Share Price ($)"
                        type="number"
                        fullWidth
                        value={inputs.acquirerSharePrice}
                        onChange={(e) => handleInputChange('acquirerSharePrice', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="EPS ($)"
                        type="number"
                        fullWidth
                        value={inputs.acquirerEPS}
                        onChange={(e) => handleInputChange('acquirerEPS', e.target.value)}
                        inputProps={{ step: 0.01 }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Net Income ($M)"
                        type="number"
                        fullWidth
                        value={inputs.acquirerNetIncome}
                        onChange={(e) => handleInputChange('acquirerNetIncome', e.target.value)}
                      />
                    </Grid>
                  </Grid>
                </Box>

                <Divider />

                {/* Target */}
                <Box>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2 }}>
                    Target Company
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12}>
                      <TextField
                        label="Company Name"
                        fullWidth
                        value={inputs.targetName}
                        onChange={(e) => handleInputChange('targetName', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Shares Outstanding (M)"
                        type="number"
                        fullWidth
                        value={inputs.targetShares}
                        onChange={(e) => handleInputChange('targetShares', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Current Share Price ($)"
                        type="number"
                        fullWidth
                        value={inputs.targetSharePrice}
                        onChange={(e) => handleInputChange('targetSharePrice', e.target.value)}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="EPS ($)"
                        type="number"
                        fullWidth
                        value={inputs.targetEPS}
                        onChange={(e) => handleInputChange('targetEPS', e.target.value)}
                        inputProps={{ step: 0.01 }}
                      />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField
                        label="Net Income ($M)"
                        type="number"
                        fullWidth
                        value={inputs.targetNetIncome}
                        onChange={(e) => handleInputChange('targetNetIncome', e.target.value)}
                      />
                    </Grid>
                  </Grid>
                </Box>
              </Stack>
            </TabPanel>

            {/* Tab 1: Deal Terms */}
            <TabPanel value={tabValue} index={1}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Transaction Structure
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Offer Premium (%)"
                      type="number"
                      fullWidth
                      value={inputs.offerPremium}
                      onChange={(e) => handleInputChange('offerPremium', e.target.value)}
                      inputProps={{ step: 5 }}
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
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cash Portion (%)"
                      type="number"
                      fullWidth
                      value={inputs.cashPortion}
                      onChange={(e) => handleInputChange('cashPortion', e.target.value)}
                      inputProps={{ step: 5 }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Stock Portion (%)"
                      type="number"
                      fullWidth
                      value={inputs.stockPortion}
                      onChange={(e) => handleInputChange('stockPortion', e.target.value)}
                      inputProps={{ step: 5 }}
                    />
                  </Grid>
                </Grid>

                <Chip
                  label={`Mix: ${inputs.cashPortion}% Cash / ${inputs.stockPortion}% Stock`}
                  color={(parseFloat(inputs.cashPortion) + parseFloat(inputs.stockPortion)) === 100 ? 'success' : 'error'}
                />

                <Divider />

                <Typography variant="subtitle2" color="text.secondary">
                  Financing
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Debt Financing ($M)"
                      type="number"
                      fullWidth
                      value={inputs.debtFinancing}
                      onChange={(e) => handleInputChange('debtFinancing', e.target.value)}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Interest Rate (%)"
                      type="number"
                      fullWidth
                      value={inputs.debtInterestRate}
                      onChange={(e) => handleInputChange('debtInterestRate', e.target.value)}
                      inputProps={{ step: 0.25 }}
                    />
                  </Grid>
                </Grid>
              </Stack>
            </TabPanel>

            {/* Tab 2: Synergies */}
            <TabPanel value={tabValue} index={2}>
              <Stack spacing={3}>
                <Typography variant="subtitle2" color="text.secondary">
                  Expected Synergies (Annual Run-Rate)
                </Typography>

                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Cost Synergies ($M)"
                      type="number"
                      fullWidth
                      value={inputs.costSynergies}
                      onChange={(e) => handleInputChange('costSynergies', e.target.value)}
                      helperText="Operational efficiencies, headcount reduction"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Revenue Synergies ($M)"
                      type="number"
                      fullWidth
                      value={inputs.revenueSynergies}
                      onChange={(e) => handleInputChange('revenueSynergies', e.target.value)}
                      helperText="Cross-selling, market expansion"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      label="Years to Full Realization"
                      type="number"
                      fullWidth
                      value={inputs.synergiesYear}
                      onChange={(e) => handleInputChange('synergiesYear', e.target.value)}
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
                onClick={calculateMerger}
                fullWidth
                sx={{
                  py: 1.5,
                  background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                  fontWeight: 600,
                }}
              >
                Calculate Impact
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} lg={5}>
          <Stack spacing={3}>
            {results && (
              <>
                {/* Accretion/Dilution Card */}
                <Card
                  sx={{
                    background: results.isAccretive
                      ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
                      : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
                    color: 'white',
                  }}
                >
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                      {results.isAccretive ? 'Accretive' : 'Dilutive'} Transaction
                    </Typography>

                    <Box>
                      <Typography variant="caption" sx={{ opacity: 0.9 }}>
                        EPS Impact
                      </Typography>
                      <Stack direction="row" alignItems="baseline" spacing={1}>
                        {results.isAccretive ? (
                          <TrendingUpIcon sx={{ fontSize: 40 }} />
                        ) : (
                          <TrendingDownIcon sx={{ fontSize: 40 }} />
                        )}
                        <Typography variant="h2" sx={{ fontWeight: 700 }}>
                          {results.accretionDilution >= 0 ? '+' : ''}
                          {results.accretionDilution.toFixed(2)}%
                        </Typography>
                      </Stack>
                    </Box>

                    <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />

                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Current EPS
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700 }}>
                            ${parseFloat(inputs.acquirerEPS).toFixed(2)}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6}>
                        <Box>
                          <Typography variant="caption" sx={{ opacity: 0.9 }}>
                            Pro Forma EPS
                          </Typography>
                          <Typography variant="h5" sx={{ fontWeight: 700 }}>
                            ${results.proFormaEPS.toFixed(2)}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>

                {/* Deal Summary */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Deal Summary
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableBody>
                        <TableRow>
                          <TableCell>Offer Price per Share</TableCell>
                          <TableCell align="right">${results.offerPrice.toFixed(2)}</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Total Purchase Price</TableCell>
                          <TableCell align="right">{formatCurrency(results.targetEquityValue)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Cash Consideration</TableCell>
                          <TableCell align="right">{formatCurrency(results.cashConsideration)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Stock Consideration</TableCell>
                          <TableCell align="right">{formatCurrency(results.stockConsideration)}M</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell><strong>New Shares Issued</strong></TableCell>
                          <TableCell align="right"><strong>{results.newSharesIssued.toFixed(2)}M</strong></TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>

                {/* Ownership */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Pro Forma Ownership
                  </Typography>

                  <Stack spacing={2}>
                    <Box>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                        <Typography variant="body2">Acquirer Shareholders</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatPercent(results.acquirerOwnership)}
                        </Typography>
                      </Stack>
                      <Box sx={{ width: '100%', height: 8, bgcolor: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
                        <Box
                          sx={{
                            width: `${results.acquirerOwnership}%`,
                            height: '100%',
                            bgcolor: '#3b82f6',
                          }}
                        />
                      </Box>
                    </Box>

                    <Box>
                      <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                        <Typography variant="body2">Target Shareholders</Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatPercent(results.targetOwnership)}
                        </Typography>
                      </Stack>
                      <Box sx={{ width: '100%', height: 8, bgcolor: '#e5e7eb', borderRadius: 4, overflow: 'hidden' }}>
                        <Box
                          sx={{
                            width: `${results.targetOwnership}%`,
                            height: '100%',
                            bgcolor: '#f59e0b',
                          }}
                        />
                      </Box>
                    </Box>
                  </Stack>
                </Paper>

                {/* Action Buttons */}
                <Stack direction="row" spacing={2}>
                  <Button
                    variant="outlined"
                    startIcon={<SaveIcon />}
                    fullWidth
                  >
                    Save Analysis
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
                  Enter company details and deal terms to analyze the merger impact
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
