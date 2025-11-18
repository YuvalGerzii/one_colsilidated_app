import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Tab,
  Tabs,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  TextField,
  Alert,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Add as AddIcon,
  AccountBalance as LoanIcon,
  Calculate as CalculateIcon,
  CompareArrows as CompareIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Assessment as AssessmentIcon,
  Schedule as ScheduleIcon,
  Analytics as AnalyticsIcon,
  MonetizationOn as MoneyIcon,
} from '@mui/icons-material';
import { api } from '../../services/apiClient';

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
      id={`debt-tabpanel-${index}`}
      aria-labelledby={`debt-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const DebtManagementDashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // DSCR Calculator State
  const [dscrNOI, setDscrNOI] = useState('');
  const [dscrDebtService, setDscrDebtService] = useState('');
  const [dscrResult, setDscrResult] = useState<any>(null);

  // Amortization State
  const [amortLoanAmount, setAmortLoanAmount] = useState('');
  const [amortRate, setAmortRate] = useState('');
  const [amortTerm, setAmortTerm] = useState('360');
  const [amortStartDate, setAmortStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [amortSchedule, setAmortSchedule] = useState<any[]>([]);

  // Rate Sensitivity State
  const [rateSensLoanAmount, setRateSensLoanAmount] = useState('');
  const [rateSensBaseRate, setRateSensBaseRate] = useState('');
  const [rateSensTerm, setRateSensTerm] = useState('360');
  const [rateSensResult, setRateSensResult] = useState<any>(null);

  const calculateDSCR = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.post('/debt-management/calculate/dscr', {
        net_operating_income: parseFloat(dscrNOI),
        annual_debt_service: parseFloat(dscrDebtService)
      });
      setDscrResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate DSCR');
    } finally {
      setLoading(false);
    }
  };

  const generateAmortization = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.post('/debt-management/calculate/amortization', {
        loan_amount: parseFloat(amortLoanAmount),
        annual_rate: parseFloat(amortRate) / 100,
        term_months: parseInt(amortTerm),
        start_date: amortStartDate,
        interest_only_months: 0
      });
      setAmortSchedule(response.data.schedule || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate amortization schedule');
    } finally {
      setLoading(false);
    }
  };

  const analyzeRateSensitivity = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.post('/debt-management/calculate/rate-sensitivity', {
        loan_amount: parseFloat(rateSensLoanAmount),
        base_rate: parseFloat(rateSensBaseRate) / 100,
        term_months: parseInt(rateSensTerm)
      });
      setRateSensResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze rate sensitivity');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          <LoanIcon sx={{ mr: 1, verticalAlign: 'middle', fontSize: 36 }} />
          Debt Management
        </Typography>
        <Typography variant="body1" color="textSecondary">
          Comprehensive loan tracking, analysis, and financial calculations for debt management
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Tabs */}
      <Paper sx={{ width: '100%' }}>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)} aria-label="debt management tabs">
          <Tab label="Overview" />
          <Tab label="DSCR Calculator" />
          <Tab label="Rate Sensitivity" />
          <Tab label="Amortization" />
        </Tabs>

        {/* Tab 0: Overview */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            {/* Introduction */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3, bgcolor: 'primary.main', color: 'primary.contrastText' }}>
                <Typography variant="h5" gutterBottom>
                  Welcome to Debt Management
                </Typography>
                <Typography variant="body1">
                  Manage your loans, analyze financing options, and make data-driven decisions about your debt portfolio.
                </Typography>
              </Paper>
            </Grid>

            {/* Features Grid */}
            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CalculateIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">DSCR Calculator</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Calculate Debt Service Coverage Ratio to assess your ability to service debt obligations.
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Quick DSCR calculation" secondary="Input NOI and debt service" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Interpretation guidance" secondary="Strong, Adequate, Marginal, or Insufficient" />
                    </ListItem>
                  </List>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => setTabValue(1)}>Open Calculator</Button>
                </CardActions>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <ScheduleIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Amortization Schedule</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Generate detailed payment schedules showing principal and interest breakdown.
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Payment-by-payment breakdown" secondary="See exactly where your money goes" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Cumulative totals" secondary="Track total interest and principal paid" />
                    </ListItem>
                  </List>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => setTabValue(3)}>Generate Schedule</Button>
                </CardActions>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <TrendingUpIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Rate Sensitivity Analysis</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Test how interest rate changes impact your monthly payments and total cost.
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Multiple rate scenarios" secondary="Test rates from -2% to +2%" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><CheckIcon color="success" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Payment impact analysis" secondary="See monthly and annual differences" />
                    </ListItem>
                  </List>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => setTabValue(2)}>Analyze Rates</Button>
                </CardActions>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CompareIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Additional Tools</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    More advanced features for comprehensive debt management.
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon><MoneyIcon color="primary" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Loan Comparison" secondary="Compare multiple loan scenarios" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><AnalyticsIcon color="primary" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Refinancing Analyzer" secondary="Evaluate refinancing opportunities" />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon><AssessmentIcon color="primary" fontSize="small" /></ListItemIcon>
                      <ListItemText primary="Covenant Tracking" secondary="Monitor debt covenant compliance" />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>

            {/* Quick Start Guide */}
            <Grid item xs={12}>
              <Paper sx={{ p: 3, bgcolor: 'background.default' }}>
                <Typography variant="h6" gutterBottom>
                  Quick Start Guide
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      1. Calculate DSCR
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Use the DSCR Calculator to assess your debt service coverage. Input your NOI and annual debt service to get instant results.
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      2. Analyze Rates
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Test different interest rate scenarios to understand payment sensitivity and plan for rate changes.
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      3. Review Schedules
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Generate amortization schedules to see exactly how each payment breaks down between principal and interest.
                    </Typography>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Tab 1: DSCR Calculator */}
        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Calculate DSCR</Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                DSCR = Net Operating Income / Annual Debt Service
              </Typography>
              <TextField
                fullWidth
                label="Net Operating Income (Annual)"
                type="number"
                value={dscrNOI}
                onChange={(e) => setDscrNOI(e.target.value)}
                margin="normal"
                InputProps={{ startAdornment: '$' }}
                helperText="Total annual income from the property minus operating expenses"
              />
              <TextField
                fullWidth
                label="Annual Debt Service"
                type="number"
                value={dscrDebtService}
                onChange={(e) => setDscrDebtService(e.target.value)}
                margin="normal"
                InputProps={{ startAdornment: '$' }}
                helperText="Total annual principal and interest payments"
              />
              <Button
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <CalculateIcon />}
                onClick={calculateDSCR}
                sx={{ mt: 2 }}
                disabled={!dscrNOI || !dscrDebtService || loading}
                fullWidth
              >
                Calculate DSCR
              </Button>
            </Grid>

            <Grid item xs={12} md={6}>
              {dscrResult ? (
                <Paper sx={{ p: 3, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>Results</Typography>
                  <Divider sx={{ my: 2 }} />
                  <Typography variant="h3" color="primary" gutterBottom>
                    {dscrResult.dscr?.toFixed(2)}
                  </Typography>
                  <Chip
                    label={dscrResult.interpretation}
                    color={
                      dscrResult.interpretation === 'Strong' ? 'success' :
                      dscrResult.interpretation === 'Adequate' ? 'info' :
                      dscrResult.interpretation === 'Marginal' ? 'warning' : 'error'
                    }
                    sx={{ mb: 2 }}
                  />
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="textSecondary" gutterBottom display="block">
                      DSCR Guidelines:
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemText
                          primary="≥ 1.25: Strong"
                          secondary="Excellent coverage, low default risk"
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemText
                          primary="1.15-1.24: Adequate"
                          secondary="Good coverage, acceptable risk"
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemText
                          primary="1.0-1.14: Marginal"
                          secondary="Minimal coverage, higher risk"
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemText
                          primary="< 1.0: Insufficient"
                          secondary="Income doesn't cover debt service"
                        />
                      </ListItem>
                    </List>
                  </Box>
                </Paper>
              ) : (
                <Paper sx={{ p: 3, bgcolor: 'background.default', textAlign: 'center' }}>
                  <CalculateIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" color="textSecondary">
                    Enter values and calculate to see results
                  </Typography>
                </Paper>
              )}
            </Grid>
          </Grid>
        </TabPanel>

        {/* Tab 2: Rate Sensitivity */}
        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Interest Rate Sensitivity Analysis</Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                Analyze how rate changes impact monthly payments
              </Typography>
              <TextField
                fullWidth
                label="Loan Amount"
                type="number"
                value={rateSensLoanAmount}
                onChange={(e) => setRateSensLoanAmount(e.target.value)}
                margin="normal"
                InputProps={{ startAdornment: '$' }}
              />
              <TextField
                fullWidth
                label="Base Interest Rate (%)"
                type="number"
                value={rateSensBaseRate}
                onChange={(e) => setRateSensBaseRate(e.target.value)}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Term (months)"
                type="number"
                value={rateSensTerm}
                onChange={(e) => setRateSensTerm(e.target.value)}
                margin="normal"
              />
              <Button
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <TrendingUpIcon />}
                onClick={analyzeRateSensitivity}
                sx={{ mt: 2 }}
                disabled={!rateSensLoanAmount || !rateSensBaseRate || loading}
                fullWidth
              >
                Analyze Sensitivity
              </Button>
            </Grid>

            <Grid item xs={12}>
              {rateSensResult ? (
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>Sensitivity Results</Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Rate Change</TableCell>
                          <TableCell align="right">Adjusted Rate</TableCell>
                          <TableCell align="right">Monthly Payment</TableCell>
                          <TableCell align="right">Payment Difference</TableCell>
                          <TableCell align="right">Annual Difference</TableCell>
                          <TableCell align="right">Total Interest</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {rateSensResult.scenarios?.map((scenario: any, index: number) => (
                          <TableRow
                            key={index}
                            sx={{
                              bgcolor: scenario.rate_change === 0 ? 'action.selected' : 'inherit',
                              fontWeight: scenario.rate_change === 0 ? 'bold' : 'normal'
                            }}
                          >
                            <TableCell>
                              {scenario.rate_change >= 0 ? '+' : ''}{(scenario.rate_change * 100).toFixed(2)}%
                            </TableCell>
                            <TableCell align="right">{(scenario.adjusted_rate * 100).toFixed(2)}%</TableCell>
                            <TableCell align="right">${scenario.monthly_payment.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right" sx={{ color: scenario.payment_difference > 0 ? 'error.main' : 'success.main' }}>
                              ${scenario.payment_difference.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                            </TableCell>
                            <TableCell align="right">${scenario.annual_difference.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right">${scenario.total_interest.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>
              ) : (
                <Paper sx={{ p: 5, textAlign: 'center', bgcolor: 'background.default' }}>
                  <TrendingUpIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" color="textSecondary">
                    Enter loan details and analyze to see rate sensitivity results
                  </Typography>
                </Paper>
              )}
            </Grid>
          </Grid>
        </TabPanel>

        {/* Tab 3: Amortization Schedule */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>Generate Amortization Schedule</Typography>
              <Typography variant="body2" color="textSecondary" paragraph>
                See payment-by-payment breakdown
              </Typography>
              <TextField
                fullWidth
                label="Loan Amount"
                type="number"
                value={amortLoanAmount}
                onChange={(e) => setAmortLoanAmount(e.target.value)}
                margin="normal"
                InputProps={{ startAdornment: '$' }}
              />
              <TextField
                fullWidth
                label="Annual Interest Rate (%)"
                type="number"
                value={amortRate}
                onChange={(e) => setAmortRate(e.target.value)}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Term (months)"
                type="number"
                value={amortTerm}
                onChange={(e) => setAmortTerm(e.target.value)}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Start Date"
                type="date"
                value={amortStartDate}
                onChange={(e) => setAmortStartDate(e.target.value)}
                margin="normal"
                InputLabelProps={{ shrink: true }}
              />
              <Button
                variant="contained"
                startIcon={loading ? <CircularProgress size={20} /> : <ScheduleIcon />}
                onClick={generateAmortization}
                sx={{ mt: 2 }}
                disabled={!amortLoanAmount || !amortRate || !amortTerm || loading}
                fullWidth
              >
                Generate Schedule
              </Button>
            </Grid>

            <Grid item xs={12}>
              {amortSchedule.length > 0 ? (
                <Paper sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>Amortization Schedule</Typography>
                  <TableContainer sx={{ maxHeight: 500 }}>
                    <Table stickyHeader size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Payment #</TableCell>
                          <TableCell>Date</TableCell>
                          <TableCell align="right">Beginning Balance</TableCell>
                          <TableCell align="right">Payment</TableCell>
                          <TableCell align="right">Principal</TableCell>
                          <TableCell align="right">Interest</TableCell>
                          <TableCell align="right">Ending Balance</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {amortSchedule.slice(0, 100).map((entry: any) => (
                          <TableRow key={entry.payment_number}>
                            <TableCell>{entry.payment_number}</TableCell>
                            <TableCell>{new Date(entry.payment_date).toLocaleDateString()}</TableCell>
                            <TableCell align="right">${entry.beginning_balance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right">${entry.payment_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right">${entry.principal_payment.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right">${entry.interest_payment.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                            <TableCell align="right">${entry.ending_balance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                  {amortSchedule.length > 100 && (
                    <Typography variant="caption" color="textSecondary" sx={{ mt: 1, display: 'block' }}>
                      Showing first 100 payments of {amortSchedule.length}
                    </Typography>
                  )}
                </Paper>
              ) : (
                <Paper sx={{ p: 5, textAlign: 'center', bgcolor: 'background.default' }}>
                  <ScheduleIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="body1" color="textSecondary">
                    Enter loan details and generate to see amortization schedule
                  </Typography>
                </Paper>
              )}
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default DebtManagementDashboard;
