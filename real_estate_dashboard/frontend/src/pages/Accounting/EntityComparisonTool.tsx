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
  Stack,
  Chip,
  Divider,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  Business as BusinessIcon,
  CheckCircle as CheckIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { apiClient } from '@/services/apiClient';

interface EntityResult {
  net_income: number;
  llc: {
    self_employment_tax: number;
    income_tax: number;
    total_tax: number;
    effective_rate: number;
    after_tax_income: number;
  };
  s_corp: {
    salary: number;
    distribution: number;
    payroll_tax_employee: number;
    payroll_tax_employer: number;
    income_tax: number;
    total_tax: number;
    effective_rate: number;
    after_tax_income: number;
    savings_vs_llc: number;
  };
  c_corp: {
    corporate_tax: number;
    dividend: number;
    dividend_tax: number;
    total_tax: number;
    effective_rate: number;
    after_tax_income: number;
  };
  recommendation: string;
}

export const EntityComparisonTool: React.FC = () => {
  const [netIncome, setNetIncome] = useState('150000');
  const [reasonableSalary, setReasonableSalary] = useState('');
  const [stateTaxRate, setStateTaxRate] = useState('5.0');
  const [filingStatus, setFilingStatus] = useState<'single' | 'married'>('married');
  const [result, setResult] = useState<EntityResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.post('/tax-calculators/entity-comparison', {
        net_income: parseFloat(netIncome),
        reasonable_salary: reasonableSalary ? parseFloat(reasonableSalary) : null,
        state_tax_rate: parseFloat(stateTaxRate),
        filing_status: filingStatus,
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error comparing entity structures');
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
    return `${value.toFixed(2)}%`;
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Entity Structure Tax Comparison
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Compare LLC, S-Corp, and C-Corp to find the most tax-efficient structure for your business
        </Typography>
      </Box>

      {/* Input Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Business Information
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Annual Net Income"
              type="number"
              value={netIncome}
              onChange={(e) => setNetIncome(e.target.value)}
              InputProps={{ startAdornment: '$' }}
              helperText="Business profit before owner compensation"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="Reasonable Salary (Optional)"
              type="number"
              value={reasonableSalary}
              onChange={(e) => setReasonableSalary(e.target.value)}
              InputProps={{ startAdornment: '$' }}
              helperText="For S-Corp (default: 40% of income)"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              label="State Tax Rate"
              type="number"
              value={stateTaxRate}
              onChange={(e) => setStateTaxRate(e.target.value)}
              InputProps={{ endAdornment: '%' }}
              helperText="Your state income tax rate"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Filing Status</InputLabel>
              <Select
                value={filingStatus}
                label="Filing Status"
                onChange={(e) => setFilingStatus(e.target.value as 'single' | 'married')}
              >
                <MenuItem value="single">Single</MenuItem>
                <MenuItem value="married">Married Filing Jointly</MenuItem>
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
              {loading ? 'Calculating...' : 'Compare Entity Structures'}
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
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6" fontWeight="bold">
                      LLC (Sole Prop/Partnership)
                    </Typography>
                    <BusinessIcon color="action" />
                  </Stack>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Total Tax Burden
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="error.main">
                    {formatCurrency(result.llc.total_tax)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Effective Rate: {formatPercent(result.llc.effective_rate)}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="body2">
                    <strong>After-Tax Income:</strong> {formatCurrency(result.llc.after_tax_income)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card sx={{ border: 2, borderColor: 'success.main' }}>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6" fontWeight="bold">
                      S-Corporation
                    </Typography>
                    <CheckIcon color="success" />
                  </Stack>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Total Tax Burden
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="success.main">
                    {formatCurrency(result.s_corp.total_tax)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Effective Rate: {formatPercent(result.s_corp.effective_rate)}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="body2">
                    <strong>After-Tax Income:</strong> {formatCurrency(result.s_corp.after_tax_income)}
                  </Typography>
                  <Chip
                    label={`Saves ${formatCurrency(result.s_corp.savings_vs_llc)}`}
                    color="success"
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="h6" fontWeight="bold">
                      C-Corporation
                    </Typography>
                    <BusinessIcon color="action" />
                  </Stack>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Total Tax Burden
                  </Typography>
                  <Typography variant="h4" fontWeight="bold" color="warning.main">
                    {formatCurrency(result.c_corp.total_tax)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Effective Rate: {formatPercent(result.c_corp.effective_rate)}
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="body2">
                    <strong>After-Tax Income:</strong> {formatCurrency(result.c_corp.after_tax_income)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Detailed Comparison Table */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Typography variant="h6" gutterBottom>
              Detailed Tax Breakdown
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Tax Component</TableCell>
                    <TableCell align="right">LLC</TableCell>
                    <TableCell align="right">S-Corp</TableCell>
                    <TableCell align="right">C-Corp</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Self-Employment / Payroll Tax</TableCell>
                    <TableCell align="right">{formatCurrency(result.llc.self_employment_tax)}</TableCell>
                    <TableCell align="right">
                      {formatCurrency(result.s_corp.payroll_tax_employee + result.s_corp.payroll_tax_employer)}
                    </TableCell>
                    <TableCell align="right">N/A</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Federal + State Income Tax</TableCell>
                    <TableCell align="right">{formatCurrency(result.llc.income_tax)}</TableCell>
                    <TableCell align="right">{formatCurrency(result.s_corp.income_tax)}</TableCell>
                    <TableCell align="right">
                      {formatCurrency(result.c_corp.corporate_tax + result.c_corp.dividend_tax)}
                    </TableCell>
                  </TableRow>
                  <TableRow sx={{ bgcolor: 'grey.100' }}>
                    <TableCell>
                      <strong>Total Tax</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.llc.total_tax)}</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.s_corp.total_tax)}</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.c_corp.total_tax)}</strong>
                    </TableCell>
                  </TableRow>
                  <TableRow sx={{ bgcolor: 'success.light' }}>
                    <TableCell>
                      <strong>After-Tax Income</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.llc.after_tax_income)}</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.s_corp.after_tax_income)}</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{formatCurrency(result.c_corp.after_tax_income)}</strong>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          {/* S-Corp Details */}
          {result.s_corp.savings_vs_llc > 0 && (
            <Paper sx={{ p: 3, mb: 4, bgcolor: 'success.light' }}>
              <Typography variant="h6" gutterBottom>
                S-Corp Breakdown
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Reasonable Salary (W-2):
                  </Typography>
                  <Typography variant="h6">{formatCurrency(result.s_corp.salary)}</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Distribution (No SE Tax):
                  </Typography>
                  <Typography variant="h6">{formatCurrency(result.s_corp.distribution)}</Typography>
                </Grid>
              </Grid>
              <Alert severity="success" sx={{ mt: 2 }}>
                <Typography variant="body2">
                  By electing S-Corp status, you save <strong>{formatCurrency(result.s_corp.savings_vs_llc)}</strong> in
                  self-employment taxes by taking {formatCurrency(result.s_corp.distribution)} as a distribution instead of
                  salary.
                </Typography>
              </Alert>
            </Paper>
          )}

          {/* Recommendation */}
          <Alert severity="info" icon={<BusinessIcon />}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Recommendation
            </Typography>
            <Typography variant="body2">{result.recommendation}</Typography>
          </Alert>

          {/* Additional Considerations */}
          <Paper sx={{ p: 3, mt: 4, bgcolor: 'grey.50' }}>
            <Typography variant="h6" gutterBottom>
              Entity Selection Factors
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Factor</TableCell>
                    <TableCell align="center">LLC</TableCell>
                    <TableCell align="center">S-Corp</TableCell>
                    <TableCell align="center">C-Corp</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Ease of Setup</TableCell>
                    <TableCell align="center">
                      <CheckIcon color="success" />
                    </TableCell>
                    <TableCell align="center">
                      <CheckIcon color="warning" />
                    </TableCell>
                    <TableCell align="center">
                      <CancelIcon color="error" />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Administrative Burden</TableCell>
                    <TableCell align="center">Low</TableCell>
                    <TableCell align="center">Medium (Payroll)</TableCell>
                    <TableCell align="center">High</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Ideal Income Level</TableCell>
                    <TableCell align="center">&lt; $60K</TableCell>
                    <TableCell align="center">$60K - $400K</TableCell>
                    <TableCell align="center">&gt; $500K</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Best For</TableCell>
                    <TableCell align="center">Solo/Startups</TableCell>
                    <TableCell align="center">Service Businesses</TableCell>
                    <TableCell align="center">High Growth/VC</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </>
      )}
    </Container>
  );
};
