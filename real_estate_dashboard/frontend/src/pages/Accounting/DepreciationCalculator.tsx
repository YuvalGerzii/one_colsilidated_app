import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Card,
  CardContent,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Divider,
  Stack,
  Chip,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  TrendingUp as TrendingUpIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { apiClient } from '@/services/apiClient';

interface CostSegregationResult {
  building_cost: number;
  land_cost: number;
  property_type: string;
  total_basis: number;
  traditional_depreciation: {
    annual_amount: number;
    recovery_period: number;
    total_over_life: number;
  };
  cost_segregation: {
    year_5: { amount: number; percentage: number };
    year_7: { amount: number; percentage: number };
    year_15: { amount: number; percentage: number };
    year_27_5_or_39: { amount: number; percentage: number };
  };
  first_year_comparison: {
    traditional: number;
    with_cost_seg: number;
    additional_deduction: number;
    tax_savings_estimate: number;
  };
}

export const DepreciationCalculator: React.FC = () => {
  const [buildingCost, setBuildingCost] = useState('500000');
  const [landCost, setLandCost] = useState('200000');
  const [propertyType, setPropertyType] = useState<'residential' | 'commercial'>('commercial');
  const [result, setResult] = useState<CostSegregationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.post('/tax-calculators/cost-segregation', {
        building_cost: parseFloat(buildingCost),
        land_cost: parseFloat(landCost),
        property_type: propertyType,
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error calculating cost segregation');
    } finally {
      setLoading(false);
    }
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
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Cost Segregation & Depreciation Calculator
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Accelerate depreciation deductions by identifying property components that qualify for shorter recovery periods
        </Typography>
      </Box>

      {/* Input Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Property Information
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Building Cost (Excluding Land)"
              type="number"
              value={buildingCost}
              onChange={(e) => setBuildingCost(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Land Value"
              type="number"
              value={landCost}
              onChange={(e) => setLandCost(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Property Type</InputLabel>
              <Select
                value={propertyType}
                label="Property Type"
                onChange={(e) => setPropertyType(e.target.value as 'residential' | 'commercial')}
              >
                <MenuItem value="residential">Residential (27.5 years)</MenuItem>
                <MenuItem value="commercial">Commercial (39 years)</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              startIcon={<CalculateIcon />}
              onClick={handleCalculate}
              disabled={loading}
            >
              {loading ? 'Calculating...' : 'Calculate Cost Segregation Benefit'}
            </Button>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {/* Results Section */}
      {result && (
        <>
          {/* Summary Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Total Depreciable Basis
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    {formatCurrency(result.total_basis)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: 'error.light' }}>
                <CardContent>
                  <Typography variant="body2" gutterBottom>
                    Traditional Year 1
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    {formatCurrency(result.first_year_comparison.traditional)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: 'success.light' }}>
                <CardContent>
                  <Typography variant="body2" gutterBottom>
                    With Cost Segregation
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    {formatCurrency(result.first_year_comparison.with_cost_seg)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ bgcolor: 'primary.light' }}>
                <CardContent>
                  <Typography variant="body2" gutterBottom>
                    Tax Savings (37% Rate)
                  </Typography>
                  <Typography variant="h5" fontWeight="bold" color="white">
                    {formatCurrency(result.first_year_comparison.tax_savings_estimate)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Detailed Breakdown */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Component Allocation
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Recovery Period</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell align="right">Amount</TableCell>
                    <TableCell align="right">Percentage</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>
                      <Chip label="5 Years" color="success" size="small" />
                    </TableCell>
                    <TableCell>Land improvements, carpeting, decorative items</TableCell>
                    <TableCell align="right">{formatCurrency(result.cost_segregation.year_5.amount)}</TableCell>
                    <TableCell align="right">{formatPercent(result.cost_segregation.year_5.percentage)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>
                      <Chip label="7 Years" color="info" size="small" />
                    </TableCell>
                    <TableCell>Furniture, fixtures, equipment, signage</TableCell>
                    <TableCell align="right">{formatCurrency(result.cost_segregation.year_7.amount)}</TableCell>
                    <TableCell align="right">{formatPercent(result.cost_segregation.year_7.percentage)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>
                      <Chip label="15 Years" color="warning" size="small" />
                    </TableCell>
                    <TableCell>Site utilities, parking lots, landscaping</TableCell>
                    <TableCell align="right">{formatCurrency(result.cost_segregation.year_15.amount)}</TableCell>
                    <TableCell align="right">{formatPercent(result.cost_segregation.year_15.percentage)}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>
                      <Chip label={propertyType === 'residential' ? '27.5 Years' : '39 Years'} color="error" size="small" />
                    </TableCell>
                    <TableCell>Building structure</TableCell>
                    <TableCell align="right">
                      {formatCurrency(result.cost_segregation.year_27_5_or_39.amount)}
                    </TableCell>
                    <TableCell align="right">
                      {formatPercent(result.cost_segregation.year_27_5_or_39.percentage)}
                    </TableCell>
                  </TableRow>
                  <TableRow sx={{ bgcolor: 'primary.light' }}>
                    <TableCell colSpan={2}>
                      <strong>Total</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.total_basis)}</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>100%</strong>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          {/* Additional Insights */}
          <Alert severity="success" icon={<TrendingUpIcon />}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Additional First-Year Deduction: {formatCurrency(result.first_year_comparison.additional_deduction)}
            </Typography>
            <Typography variant="body2">
              By reclassifying {formatPercent(1 - result.cost_segregation.year_27_5_or_39.percentage)} of the property into
              shorter-lived assets, you can accelerate{' '}
              {formatCurrency(result.first_year_comparison.additional_deduction)} of deductions to Year 1.
            </Typography>
          </Alert>

          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Next Steps
            </Typography>
            <Typography variant="body2" component="div">
              <ul style={{ margin: 0, paddingLeft: 20 }}>
                <li>Hire qualified cost segregation specialist ($5K-$15K)</li>
                <li>Typical ROI: 5-20x the cost of the study</li>
                <li>File Form 3115 if applying retroactively</li>
                <li>Combine with bonus depreciation for maximum benefit</li>
                <li>Consider state tax conformity before implementing</li>
              </ul>
            </Typography>
          </Alert>
        </>
      )}

      {/* Educational Info */}
      <Paper sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <InfoIcon color="primary" />
          <Typography variant="h6">What is Cost Segregation?</Typography>
        </Stack>
        <Divider sx={{ mb: 2 }} />
        <Typography variant="body2" paragraph>
          Cost segregation is an IRS-approved tax strategy that accelerates depreciation deductions by identifying property
          components that qualify for shorter recovery periods (5, 7, or 15 years) instead of the standard 27.5 or 39 years.
        </Typography>
        <Typography variant="body2" paragraph>
          <strong>Best For:</strong> Commercial properties over $500K, properties with recent improvements, high-income
          taxpayers in top brackets, real estate professionals (REPS).
        </Typography>
        <Typography variant="body2">
          <strong>Important:</strong> This calculator provides estimates based on industry averages. A professional cost
          segregation study will provide more precise allocations based on detailed engineering analysis.
        </Typography>
      </Paper>
    </Container>
  );
};
