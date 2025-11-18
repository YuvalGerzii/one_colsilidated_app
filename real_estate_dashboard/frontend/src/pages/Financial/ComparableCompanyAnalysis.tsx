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
  IconButton,
  Chip,
  alpha,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Divider,
} from '@mui/material';
import {
  TrendingUp as CompsIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  Calculate as CalculateIcon,
  Save as SaveIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';

interface CompanyData {
  id: string;
  name: string;
  marketCap: string;
  revenue: string;
  ebitda: string;
  netIncome: string;
  enterpriseValue: string;
}

export const ComparableCompanyAnalysis: React.FC = () => {
  const [targetCompany, setTargetCompany] = useState({
    name: '',
    revenue: '',
    ebitda: '',
    netIncome: '',
  });

  const [comparables, setComparables] = useState<CompanyData[]>([
    {
      id: '1',
      name: '',
      marketCap: '',
      revenue: '',
      ebitda: '',
      netIncome: '',
      enterpriseValue: '',
    },
  ]);

  const [results, setResults] = useState<any>(null);

  const addComparable = () => {
    setComparables([
      ...comparables,
      {
        id: Date.now().toString(),
        name: '',
        marketCap: '',
        revenue: '',
        ebitda: '',
        netIncome: '',
        enterpriseValue: '',
      },
    ]);
  };

  const removeComparable = (id: string) => {
    setComparables(comparables.filter(comp => comp.id !== id));
  };

  const updateComparable = (id: string, field: keyof CompanyData, value: string) => {
    setComparables(
      comparables.map(comp =>
        comp.id === id ? { ...comp, [field]: value } : comp
      )
    );
  };

  const calculateMultiples = () => {
    // Filter out empty comparables
    const validComps = comparables.filter(
      comp => comp.revenue && comp.ebitda && comp.enterpriseValue
    );

    if (validComps.length === 0) return;

    // Calculate multiples for each comparable
    const compsWithMultiples = validComps.map(comp => {
      const revenue = parseFloat(comp.revenue) || 1;
      const ebitda = parseFloat(comp.ebitda) || 1;
      const netIncome = parseFloat(comp.netIncome) || 1;
      const ev = parseFloat(comp.enterpriseValue) || 0;
      const marketCap = parseFloat(comp.marketCap) || 0;

      return {
        ...comp,
        evRevenue: ev / revenue,
        evEbitda: ev / ebitda,
        peRatio: marketCap / netIncome,
      };
    });

    // Calculate median multiples
    const evRevenueMultiples = compsWithMultiples.map(c => c.evRevenue).sort((a, b) => a - b);
    const evEbitdaMultiples = compsWithMultiples.map(c => c.evEbitda).sort((a, b) => a - b);
    const peMultiples = compsWithMultiples.map(c => c.peRatio).sort((a, b) => a - b);

    const median = (arr: number[]) => {
      const mid = Math.floor(arr.length / 2);
      return arr.length % 2 !== 0 ? arr[mid] : (arr[mid - 1] + arr[mid]) / 2;
    };

    const medianEVRevenue = median(evRevenueMultiples);
    const medianEVEbitda = median(evEbitdaMultiples);
    const medianPE = median(peMultiples);

    // Calculate mean multiples
    const mean = (arr: number[]) => arr.reduce((sum, val) => sum + val, 0) / arr.length;

    const meanEVRevenue = mean(evRevenueMultiples);
    const meanEVEbitda = mean(evEbitdaMultiples);
    const meanPE = mean(peMultiples);

    // Apply to target company
    const targetRevenue = parseFloat(targetCompany.revenue) || 0;
    const targetEbitda = parseFloat(targetCompany.ebitda) || 0;
    const targetNetIncome = parseFloat(targetCompany.netIncome) || 0;

    const impliedEVByRevenue = targetRevenue * medianEVRevenue;
    const impliedEVByEbitda = targetEbitda * medianEVEbitda;
    const impliedMarketCap = targetNetIncome * medianPE;

    // Average implied valuation
    const avgImpliedEV = (impliedEVByRevenue + impliedEVByEbitda) / 2;

    setResults({
      compsWithMultiples,
      medianEVRevenue,
      medianEVEbitda,
      medianPE,
      meanEVRevenue,
      meanEVEbitda,
      meanPE,
      impliedEVByRevenue,
      impliedEVByEbitda,
      impliedMarketCap,
      avgImpliedEV,
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
            background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
            borderRadius: 3,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 20px rgba(6, 182, 212, 0.3)',
          }}
        >
          <CompsIcon sx={{ fontSize: 32, color: 'white' }} />
        </Box>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>
            Comparable Company Analysis
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Public market valuation using trading multiples
          </Typography>
        </Box>
      </Stack>

      <Grid container spacing={3}>
        {/* Input Panel */}
        <Grid item xs={12} lg={7}>
          <Stack spacing={3}>
            {/* Target Company */}
            <Paper sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Target Company
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <TextField
                    label="Company Name"
                    fullWidth
                    value={targetCompany.name}
                    onChange={(e) => setTargetCompany({ ...targetCompany, name: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    label="Revenue ($M)"
                    type="number"
                    fullWidth
                    value={targetCompany.revenue}
                    onChange={(e) => setTargetCompany({ ...targetCompany, revenue: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    label="EBITDA ($M)"
                    type="number"
                    fullWidth
                    value={targetCompany.ebitda}
                    onChange={(e) => setTargetCompany({ ...targetCompany, ebitda: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={4}>
                  <TextField
                    label="Net Income ($M)"
                    type="number"
                    fullWidth
                    value={targetCompany.netIncome}
                    onChange={(e) => setTargetCompany({ ...targetCompany, netIncome: e.target.value })}
                  />
                </Grid>
              </Grid>
            </Paper>

            {/* Comparable Companies */}
            <Paper sx={{ p: 3 }}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Comparable Companies
                </Typography>
                <Button
                  startIcon={<AddIcon />}
                  onClick={addComparable}
                  variant="outlined"
                  size="small"
                >
                  Add Company
                </Button>
              </Stack>

              <Stack spacing={2}>
                {comparables.map((comp, index) => (
                  <Paper
                    key={comp.id}
                    sx={{
                      p: 2,
                      border: '1px solid',
                      borderColor: 'divider',
                      bgcolor: alpha('#06b6d4', 0.02),
                    }}
                  >
                    <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                        Comparable #{index + 1}
                      </Typography>
                      {comparables.length > 1 && (
                        <IconButton
                          size="small"
                          onClick={() => removeComparable(comp.id)}
                          sx={{ color: 'error.main' }}
                        >
                          <DeleteIcon fontSize="small" />
                        </IconButton>
                      )}
                    </Stack>

                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <TextField
                          label="Company Name"
                          fullWidth
                          size="small"
                          value={comp.name}
                          onChange={(e) => updateComparable(comp.id, 'name', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={6} sm={4}>
                        <TextField
                          label="Market Cap ($M)"
                          type="number"
                          fullWidth
                          size="small"
                          value={comp.marketCap}
                          onChange={(e) => updateComparable(comp.id, 'marketCap', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={6} sm={4}>
                        <TextField
                          label="EV ($M)"
                          type="number"
                          fullWidth
                          size="small"
                          value={comp.enterpriseValue}
                          onChange={(e) => updateComparable(comp.id, 'enterpriseValue', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={6} sm={4}>
                        <TextField
                          label="Revenue ($M)"
                          type="number"
                          fullWidth
                          size="small"
                          value={comp.revenue}
                          onChange={(e) => updateComparable(comp.id, 'revenue', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={6} sm={4}>
                        <TextField
                          label="EBITDA ($M)"
                          type="number"
                          fullWidth
                          size="small"
                          value={comp.ebitda}
                          onChange={(e) => updateComparable(comp.id, 'ebitda', e.target.value)}
                        />
                      </Grid>
                      <Grid item xs={6} sm={4}>
                        <TextField
                          label="Net Income ($M)"
                          type="number"
                          fullWidth
                          size="small"
                          value={comp.netIncome}
                          onChange={(e) => updateComparable(comp.id, 'netIncome', e.target.value)}
                        />
                      </Grid>
                    </Grid>
                  </Paper>
                ))}
              </Stack>

              <Button
                variant="contained"
                startIcon={<CalculateIcon />}
                onClick={calculateMultiples}
                fullWidth
                sx={{
                  mt: 3,
                  py: 1.5,
                  background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
                  fontWeight: 600,
                }}
              >
                Calculate Valuation
              </Button>
            </Paper>
          </Stack>
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} lg={5}>
          <Stack spacing={3}>
            {results && (
              <>
                {/* Implied Valuation Card */}
                <Card sx={{ background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)', color: 'white' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Implied Valuation
                    </Typography>

                    <Box>
                      <Typography variant="caption" sx={{ opacity: 0.9 }}>
                        Average Enterprise Value
                      </Typography>
                      <Typography variant="h3" sx={{ fontWeight: 700, mb: 3 }}>
                        {formatCurrency(results.avgImpliedEV)}M
                      </Typography>
                    </Box>

                    <Divider sx={{ my: 2, bgcolor: 'rgba(255,255,255,0.2)' }} />

                    <Stack spacing={1.5}>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" sx={{ opacity: 0.9 }}>
                          By Revenue Multiple
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(results.impliedEVByRevenue)}M
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" sx={{ opacity: 0.9 }}>
                          By EBITDA Multiple
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(results.impliedEVByEbitda)}M
                        </Typography>
                      </Stack>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography variant="body2" sx={{ opacity: 0.9 }}>
                          Market Cap (by P/E)
                        </Typography>
                        <Typography variant="body2" fontWeight={600}>
                          {formatCurrency(results.impliedMarketCap)}M
                        </Typography>
                      </Stack>
                    </Stack>
                  </CardContent>
                </Card>

                {/* Median Multiples */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Market Multiples
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Multiple</TableCell>
                          <TableCell align="right">Median</TableCell>
                          <TableCell align="right">Mean</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>EV / Revenue</TableCell>
                          <TableCell align="right">{results.medianEVRevenue.toFixed(2)}x</TableCell>
                          <TableCell align="right">{results.meanEVRevenue.toFixed(2)}x</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>EV / EBITDA</TableCell>
                          <TableCell align="right">{results.medianEVEbitda.toFixed(2)}x</TableCell>
                          <TableCell align="right">{results.meanEVEbitda.toFixed(2)}x</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>P / E</TableCell>
                          <TableCell align="right">{results.medianPE.toFixed(2)}x</TableCell>
                          <TableCell align="right">{results.meanPE.toFixed(2)}x</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>

                {/* Comparables Table */}
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Comparable Companies
                  </Typography>

                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Company</TableCell>
                          <TableCell align="right">EV/Rev</TableCell>
                          <TableCell align="right">EV/EBITDA</TableCell>
                          <TableCell align="right">P/E</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {results.compsWithMultiples.map((comp: any, idx: number) => (
                          <TableRow key={idx}>
                            <TableCell>{comp.name || `Company ${idx + 1}`}</TableCell>
                            <TableCell align="right">{comp.evRevenue.toFixed(2)}x</TableCell>
                            <TableCell align="right">{comp.evEbitda.toFixed(2)}x</TableCell>
                            <TableCell align="right">{comp.peRatio.toFixed(2)}x</TableCell>
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
                <CompsIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
                <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                  Add comparable companies and calculate to see the valuation
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Minimum 1 comparable company required
                </Typography>
              </Paper>
            )}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
