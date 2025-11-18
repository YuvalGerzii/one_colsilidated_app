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
  Stack,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  FormControlLabel,
  Checkbox,
  LinearProgress,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  Shield as ShieldIcon,
} from '@mui/icons-material';
import { apiClient } from '@/services/apiClient';

interface AuditRiskResult {
  risk_score: number;
  risk_level: string;
  risk_description: string;
  audit_probability: number;
  red_flags: string[];
  warnings: string[];
  recommendations: string[];
  base_rate: number;
  income_level: string;
  filing_status: string;
}

export const AuditRiskAssessment: React.FC = () => {
  const [income, setIncome] = useState('150000');
  const [businessType, setBusinessType] = useState('consulting');
  const [filingStatus, setFilingStatus] = useState('married');
  const [hasScheduleC, setHasScheduleC] = useState(false);
  const [rentalProperties, setRentalProperties] = useState('0');
  const [claimsReps, setClaimsReps] = useState(false);
  const [foreignAccounts, setForeignAccounts] = useState(false);
  const [charitableContributions, setCharitableContributions] = useState('0');
  const [homeOffice, setHomeOffice] = useState(false);
  const [businessLosses, setBusinessLosses] = useState('0');

  const [deductions, setDeductions] = useState({
    meals_entertainment: '0',
    travel: '0',
    vehicle: '0',
  });

  const [result, setResult] = useState<AuditRiskResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await apiClient.post('/tax-calculators/audit-risk', {
        income: parseFloat(income),
        business_type: businessType,
        deductions: {
          meals_entertainment: parseFloat(deductions.meals_entertainment),
          travel: parseFloat(deductions.travel),
          vehicle: parseFloat(deductions.vehicle),
        },
        filing_status: filingStatus,
        has_schedule_c: hasScheduleC,
        has_rental_properties: parseInt(rentalProperties),
        claims_reps: claimsReps,
        has_foreign_accounts: foreignAccounts,
        large_charitable: parseFloat(charitableContributions),
        home_office: homeOffice,
        large_losses: parseFloat(businessLosses),
      });
      setResult(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error assessing audit risk');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (level: string): 'success' | 'info' | 'warning' | 'error' => {
    switch (level) {
      case 'LOW':
        return 'success';
      case 'MODERATE':
        return 'info';
      case 'HIGH':
        return 'warning';
      case 'VERY HIGH':
        return 'error';
      default:
        return 'info';
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

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          IRS Audit Risk Assessment
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Analyze your tax return characteristics to estimate IRS audit risk and identify potential red flags
        </Typography>
      </Box>

      {/* Input Section */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Tax Return Profile
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Total Income"
              type="number"
              value={income}
              onChange={(e) => setIncome(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Business Type</InputLabel>
              <Select value={businessType} label="Business Type" onChange={(e) => setBusinessType(e.target.value)}>
                <MenuItem value="consulting">Consulting</MenuItem>
                <MenuItem value="cash_intensive">Cash Intensive (Restaurant, Bar)</MenuItem>
                <MenuItem value="real_estate">Real Estate</MenuItem>
                <MenuItem value="professional">Professional Services</MenuItem>
                <MenuItem value="retail">Retail</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Filing Status</InputLabel>
              <Select value={filingStatus} label="Filing Status" onChange={(e) => setFilingStatus(e.target.value)}>
                <MenuItem value="single">Single</MenuItem>
                <MenuItem value="married">Married Filing Jointly</MenuItem>
                <MenuItem value="head_of_household">Head of Household</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Business Deductions
            </Typography>
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Meals & Entertainment"
              type="number"
              value={deductions.meals_entertainment}
              onChange={(e) => setDeductions({ ...deductions, meals_entertainment: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Travel Expenses"
              type="number"
              value={deductions.travel}
              onChange={(e) => setDeductions({ ...deductions, travel: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Vehicle Expenses"
              type="number"
              value={deductions.vehicle}
              onChange={(e) => setDeductions({ ...deductions, vehicle: e.target.value })}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Additional Factors
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={<Checkbox checked={hasScheduleC} onChange={(e) => setHasScheduleC(e.target.checked)} />}
              label="Has Schedule C (Self-Employment)"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={<Checkbox checked={homeOffice} onChange={(e) => setHomeOffice(e.target.checked)} />}
              label="Claims Home Office Deduction"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={<Checkbox checked={claimsReps} onChange={(e) => setClaimsReps(e.target.checked)} />}
              label="Claims Real Estate Professional Status"
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControlLabel
              control={<Checkbox checked={foreignAccounts} onChange={(e) => setForeignAccounts(e.target.checked)} />}
              label="Has Foreign Bank Accounts"
            />
          </Grid>

          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Number of Rental Properties"
              type="number"
              value={rentalProperties}
              onChange={(e) => setRentalProperties(e.target.value)}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Charitable Contributions"
              type="number"
              value={charitableContributions}
              onChange={(e) => setCharitableContributions(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Business Losses"
              type="number"
              value={businessLosses}
              onChange={(e) => setBusinessLosses(e.target.value)}
              InputProps={{ startAdornment: '$' }}
            />
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
              {loading ? 'Analyzing...' : 'Assess Audit Risk'}
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
          {/* Risk Score Card */}
          <Card sx={{ mb: 4, border: 2, borderColor: `${getRiskColor(result.risk_level)}.main` }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
                <Typography variant="h5" fontWeight="bold">
                  Audit Risk Assessment
                </Typography>
                <Chip label={result.risk_level} color={getRiskColor(result.risk_level)} size="medium" />
              </Stack>

              <Typography variant="h3" fontWeight="bold" color={`${getRiskColor(result.risk_level)}.main`} gutterBottom>
                {result.risk_score.toFixed(1)} / 25
              </Typography>

              <LinearProgress
                variant="determinate"
                value={(result.risk_score / 25) * 100}
                color={getRiskColor(result.risk_level)}
                sx={{ height: 10, borderRadius: 5, mb: 2 }}
              />

              <Typography variant="body1" paragraph>
                {result.risk_description}
              </Typography>

              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Base Audit Rate (Income Level):
                  </Typography>
                  <Typography variant="h6">{result.base_rate.toFixed(2)}%</Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2" color="text.secondary">
                    Estimated Audit Probability:
                  </Typography>
                  <Typography variant="h6">{result.audit_probability.toFixed(2)}%</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Red Flags */}
          {result.red_flags.length > 0 && (
            <Paper sx={{ p: 3, mb: 4 }}>
              <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                <ErrorIcon color="error" />
                <Typography variant="h6" fontWeight="bold">
                  Red Flags ({result.red_flags.length})
                </Typography>
              </Stack>
              <Alert severity="error">
                <List dense>
                  {result.red_flags.map((flag, idx) => (
                    <ListItem key={idx} sx={{ py: 0 }}>
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <ErrorIcon color="error" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={flag} />
                    </ListItem>
                  ))}
                </List>
              </Alert>
            </Paper>
          )}

          {/* Warnings */}
          {result.warnings.length > 0 && (
            <Paper sx={{ p: 3, mb: 4 }}>
              <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
                <WarningIcon color="warning" />
                <Typography variant="h6" fontWeight="bold">
                  Warnings ({result.warnings.length})
                </Typography>
              </Stack>
              <Alert severity="warning">
                <List dense>
                  {result.warnings.map((warning, idx) => (
                    <ListItem key={idx} sx={{ py: 0 }}>
                      <ListItemIcon sx={{ minWidth: 30 }}>
                        <WarningIcon color="warning" fontSize="small" />
                      </ListItemIcon>
                      <ListItemText primary={warning} />
                    </ListItem>
                  ))}
                </List>
              </Alert>
            </Paper>
          )}

          {/* Recommendations */}
          <Paper sx={{ p: 3, mb: 4 }}>
            <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
              <ShieldIcon color="primary" />
              <Typography variant="h6" fontWeight="bold">
                Recommendations ({result.recommendations.length})
              </Typography>
            </Stack>
            <List>
              {result.recommendations.map((rec, idx) => (
                <ListItem key={idx}>
                  <ListItemIcon>
                    <CheckIcon color="success" />
                  </ListItemIcon>
                  <ListItemText primary={rec} />
                </ListItem>
              ))}
            </List>
          </Paper>

          {/* General Tips */}
          <Alert severity="info" icon={<InfoIcon />}>
            <Typography variant="subtitle2" fontWeight="bold" gutterBottom>
              Reducing Audit Risk
            </Typography>
            <Typography variant="body2" component="div">
              <ul style={{ margin: 0, paddingLeft: 20 }}>
                <li>Use actual amounts, never round numbers</li>
                <li>Keep detailed contemporaneous records</li>
                <li>Document business purpose for all deductions</li>
                <li>File on time even if you can't pay</li>
                <li>Respond promptly to any IRS correspondence</li>
                <li>Consider professional tax preparation for complex returns</li>
              </ul>
            </Typography>
          </Alert>
        </>
      )}
    </Container>
  );
};
