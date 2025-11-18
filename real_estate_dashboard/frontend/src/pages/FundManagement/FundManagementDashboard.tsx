import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  TrendingUp as TrendingUpIcon,
  AccountBalance as FundIcon,
  People as PeopleIcon,
  Assessment as AssessmentIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Calculate as CalculateIcon,
} from '@mui/icons-material';
import { api } from '../../services/apiClient';

interface Fund {
  id: string;
  name: string;
  fund_number: string;
  fund_type: string;
  status: string;
  target_size: number;
  committed_capital: number;
  total_called: number;
  total_distributed: number;
  nav: number;
  irr: number | null;
  moic: number | null;
  dpi: number | null;
  rvpi: number | null;
  tvpi: number | null;
  management_fee_rate: number;
  carried_interest_rate: number;
  preferred_return_rate: number;
}

interface LimitedPartner {
  id: string;
  name: string;
  legal_name: string;
  lp_type: string;
  email: string;
}

const FundManagementDashboard: React.FC = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [funds, setFunds] = useState<Fund[]>([]);
  const [lps, setLPs] = useState<LimitedPartner[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Dialogs
  const [createFundOpen, setCreateFundOpen] = useState(false);
  const [createLPOpen, setCreateLPOpen] = useState(false);
  const [waterfallCalcOpen, setWaterfallCalcOpen] = useState(false);

  // Form states
  const [newFund, setNewFund] = useState({
    name: '',
    fund_number: '',
    fund_type: 'Private Equity',
    description: '',
    target_size: '',
    vintage_year: new Date().getFullYear().toString(),
    management_fee_rate: '0.02',
    carried_interest_rate: '0.20',
    preferred_return_rate: '0.08',
  });

  const [newLP, setNewLP] = useState({
    name: '',
    legal_name: '',
    lp_type: '',
    contact_person: '',
    email: '',
    phone: '',
  });

  const [waterfallCalc, setWaterfallCalc] = useState({
    distribution_amount: '',
    total_invested: '',
    total_distributed_to_date: '',
    preferred_return_rate: '0.08',
    carried_interest_rate: '0.20',
    waterfall_type: 'american',
  });

  const [waterfallResult, setWaterfallResult] = useState<any>(null);

  // Removed auto-load on mount - data loads on-demand when users navigate to specific tabs

  const fetchFunds = async () => {
    try {
      setLoading(true);
      const response = await api.get('/fund-management/funds');
      setFunds(response.data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch funds');
    } finally {
      setLoading(false);
    }
  };

  const fetchLPs = async () => {
    try {
      const response = await api.get('/fund-management/lps');
      setLPs(response.data);
    } catch (err: any) {
      console.error('Failed to fetch LPs:', err);
    }
  };

  const handleCreateFund = async () => {
    try {
      await api.post('/fund-management/funds', {
        ...newFund,
        target_size: parseFloat(newFund.target_size),
        management_fee_rate: parseFloat(newFund.management_fee_rate),
        carried_interest_rate: parseFloat(newFund.carried_interest_rate),
        preferred_return_rate: parseFloat(newFund.preferred_return_rate),
      });

      setCreateFundOpen(false);
      setNewFund({
        name: '',
        fund_number: '',
        fund_type: 'Private Equity',
        description: '',
        target_size: '',
        vintage_year: new Date().getFullYear().toString(),
        management_fee_rate: '0.02',
        carried_interest_rate: '0.20',
        preferred_return_rate: '0.08',
      });
      fetchFunds();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create fund');
    }
  };

  const handleCreateLP = async () => {
    try {
      await api.post('/fund-management/lps', newLP);

      setCreateLPOpen(false);
      setNewLP({
        name: '',
        legal_name: '',
        lp_type: '',
        contact_person: '',
        email: '',
        phone: '',
      });
      fetchLPs();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create LP');
    }
  };

  const handleCalculateWaterfall = async () => {
    try {
      const response = await api.post('/fund-management/calculate/waterfall', {
        distribution_amount: parseFloat(waterfallCalc.distribution_amount),
        total_invested: parseFloat(waterfallCalc.total_invested),
        total_distributed_to_date: parseFloat(waterfallCalc.total_distributed_to_date),
        preferred_return_rate: parseFloat(waterfallCalc.preferred_return_rate),
        carried_interest_rate: parseFloat(waterfallCalc.carried_interest_rate),
        waterfall_type: waterfallCalc.waterfall_type,
      });
      setWaterfallResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate waterfall');
    }
  };

  const formatCurrency = (value: number | null | undefined) => {
    if (value === null || value === undefined) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercentage = (value: number | null | undefined, decimals = 2) => {
    if (value === null || value === undefined) return 'N/A';
    return `${(value * 100).toFixed(decimals)}%`;
  };

  const formatMultiple = (value: number | null | undefined) => {
    if (value === null || value === undefined) return 'N/A';
    return `${value.toFixed(2)}x`;
  };

  const getStatusColor = (status: string) => {
    const colors: { [key: string]: 'primary' | 'success' | 'warning' | 'error' | 'info' } = {
      'Fundraising': 'info',
      'Investing': 'primary',
      'Harvesting': 'success',
      'Liquidating': 'warning',
      'Closed': 'error',
    };
    return colors[status] || 'default';
  };

  // Summary Statistics
  const totalAUM = funds.reduce((sum, fund) => sum + (fund.nav || 0), 0);
  const totalCommitted = funds.reduce((sum, fund) => sum + fund.committed_capital, 0);
  const totalCalled = funds.reduce((sum, fund) => sum + fund.total_called, 0);
  const totalDistributed = funds.reduce((sum, fund) => sum + fund.total_distributed, 0);

  const avgIRR = funds.length > 0
    ? funds.reduce((sum, fund) => sum + (fund.irr || 0), 0) / funds.filter(f => f.irr).length
    : 0;

  const avgMOIC = funds.length > 0
    ? funds.reduce((sum, fund) => sum + (fund.moic || 0), 0) / funds.filter(f => f.moic).length
    : 0;

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Fund Management
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<CalculateIcon />}
            onClick={() => setWaterfallCalcOpen(true)}
          >
            Waterfall Calculator
          </Button>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateFundOpen(true)}
          >
            Create Fund
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <FundIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="subtitle2" color="text.secondary">
                  Total AUM
                </Typography>
              </Box>
              <Typography variant="h5">{formatCurrency(totalAUM)}</Typography>
              <Typography variant="caption" color="text.secondary">
                {funds.length} Active Funds
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpIcon sx={{ mr: 1, color: 'success.main' }} />
                <Typography variant="subtitle2" color="text.secondary">
                  Avg IRR
                </Typography>
              </Box>
              <Typography variant="h5">{formatPercentage(avgIRR)}</Typography>
              <Typography variant="caption" color="text.secondary">
                Avg MOIC: {formatMultiple(avgMOIC)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AssessmentIcon sx={{ mr: 1, color: 'warning.main' }} />
                <Typography variant="subtitle2" color="text.secondary">
                  Capital Called
                </Typography>
              </Box>
              <Typography variant="h5">{formatCurrency(totalCalled)}</Typography>
              <Typography variant="caption" color="text.secondary">
                of {formatCurrency(totalCommitted)} Committed
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <PeopleIcon sx={{ mr: 1, color: 'info.main' }} />
                <Typography variant="subtitle2" color="text.secondary">
                  Limited Partners
                </Typography>
              </Box>
              <Typography variant="h5">{lps.length}</Typography>
              <Typography variant="caption" color="text.secondary">
                Distributed: {formatCurrency(totalDistributed)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={(_, newValue) => setCurrentTab(newValue)}>
          <Tab label="Overview" />
          <Tab label="Funds" />
          <Tab label="Limited Partners" />
        </Tabs>
      </Paper>

      {/* Overview Tab */}
      {currentTab === 0 && (
        <Paper sx={{ p: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Box sx={{ bgcolor: 'primary.main', color: 'primary.contrastText', p: 3, borderRadius: 1 }}>
                <Typography variant="h5" gutterBottom>
                  Welcome to Fund Management
                </Typography>
                <Typography variant="body1">
                  Comprehensive platform for managing PE/VC funds, limited partners, capital calls, distributions, and portfolio performance tracking.
                </Typography>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <FundIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Fund Management</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Create and manage PE/VC funds with complete lifecycle tracking.
                  </Typography>
                  <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
                    <li>Fund creation and setup</li>
                    <li>Performance metrics (IRR, MOIC, DPI, TVPI)</li>
                    <li>Capital structure tracking</li>
                    <li>Fund status management</li>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <PeopleIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Limited Partner Management</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Manage LP relationships and commitments.
                  </Typography>
                  <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
                    <li>LP database and profiles</li>
                    <li>Commitment tracking</li>
                    <li>Capital call management</li>
                    <li>Distribution processing</li>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <CalculateIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Waterfall Calculator</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Calculate distribution waterfalls with preferred returns and carry.
                  </Typography>
                  <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
                    <li>American vs European waterfall</li>
                    <li>Preferred return calculations</li>
                    <li>Carried interest modeling</li>
                    <li>LP vs GP distributions</li>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <AssessmentIcon sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                    <Typography variant="h6">Portfolio Analytics</Typography>
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Track and analyze fund performance across your portfolio.
                  </Typography>
                  <Typography variant="body2" component="ul" sx={{ pl: 2 }}>
                    <li>IRR and MOIC tracking</li>
                    <li>Vintage year analysis</li>
                    <li>Portfolio-level metrics</li>
                    <li>Investment pipeline</li>
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Box sx={{ bgcolor: 'background.default', p: 3, borderRadius: 1 }}>
                <Typography variant="h6" gutterBottom>
                  Getting Started
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      1. Create a Fund
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Set up a new PE/VC fund with target size, fees, and carry structure.
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      2. Add Limited Partners
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Build your LP base and track commitments to the fund.
                    </Typography>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Typography variant="subtitle2" color="primary" gutterBottom>
                      3. Manage Capital & Distributions
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Issue capital calls, track investments, and process distributions.
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Funds Tab */}
      {currentTab === 1 && (
        <Paper>
          {loading ? (
            <Box sx={{ p: 4, display: 'flex', justifyContent: 'center' }}>
              <CircularProgress />
            </Box>
          ) : (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Fund Name</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell align="right">Committed</TableCell>
                    <TableCell align="right">Called</TableCell>
                    <TableCell align="right">NAV</TableCell>
                    <TableCell align="right">IRR</TableCell>
                    <TableCell align="right">MOIC</TableCell>
                    <TableCell align="right">DPI</TableCell>
                    <TableCell align="right">TVPI</TableCell>
                    <TableCell align="center">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {funds.map((fund) => (
                    <TableRow key={fund.id} hover>
                      <TableCell>
                        <Typography variant="body2" fontWeight="medium">
                          {fund.name}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {fund.fund_number}
                        </Typography>
                      </TableCell>
                      <TableCell>{fund.fund_type}</TableCell>
                      <TableCell>
                        <Chip
                          label={fund.status}
                          color={getStatusColor(fund.status)}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="right">{formatCurrency(fund.committed_capital)}</TableCell>
                      <TableCell align="right">{formatCurrency(fund.total_called)}</TableCell>
                      <TableCell align="right">{formatCurrency(fund.nav)}</TableCell>
                      <TableCell align="right">{formatPercentage(fund.irr)}</TableCell>
                      <TableCell align="right">{formatMultiple(fund.moic)}</TableCell>
                      <TableCell align="right">{formatMultiple(fund.dpi)}</TableCell>
                      <TableCell align="right">{formatMultiple(fund.tvpi)}</TableCell>
                      <TableCell align="center">
                        <IconButton size="small" color="primary">
                          <ViewIcon />
                        </IconButton>
                        <IconButton size="small">
                          <EditIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                  {funds.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={11} align="center" sx={{ py: 4 }}>
                        <Typography color="text.secondary">
                          No funds created yet. Click "Create Fund" to get started.
                        </Typography>
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      )}

      {/* LPs Tab */}
      {currentTab === 2 && (
        <Paper>
          <Box sx={{ p: 2, display: 'flex', justifyContent: 'flex-end' }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setCreateLPOpen(true)}
            >
              Add LP
            </Button>
          </Box>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Legal Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {lps.map((lp) => (
                  <TableRow key={lp.id} hover>
                    <TableCell>{lp.name}</TableCell>
                    <TableCell>{lp.legal_name || '-'}</TableCell>
                    <TableCell>{lp.lp_type || '-'}</TableCell>
                    <TableCell>{lp.email || '-'}</TableCell>
                    <TableCell align="center">
                      <IconButton size="small" color="primary">
                        <ViewIcon />
                      </IconButton>
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
                {lps.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} align="center" sx={{ py: 4 }}>
                      <Typography color="text.secondary">
                        No limited partners added yet. Click "Add LP" to get started.
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}

      {/* Create Fund Dialog */}
      <Dialog open={createFundOpen} onClose={() => setCreateFundOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Fund</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Fund Name"
                value={newFund.name}
                onChange={(e) => setNewFund({ ...newFund, name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Fund Number"
                value={newFund.fund_number}
                onChange={(e) => setNewFund({ ...newFund, fund_number: e.target.value })}
                placeholder="e.g., Fund I, Fund II"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                select
                label="Fund Type"
                value={newFund.fund_type}
                onChange={(e) => setNewFund({ ...newFund, fund_type: e.target.value })}
              >
                <MenuItem value="Private Equity">Private Equity</MenuItem>
                <MenuItem value="Venture Capital">Venture Capital</MenuItem>
                <MenuItem value="Real Estate">Real Estate</MenuItem>
                <MenuItem value="Debt">Debt</MenuItem>
                <MenuItem value="Infrastructure">Infrastructure</MenuItem>
                <MenuItem value="Hybrid">Hybrid</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Vintage Year"
                value={newFund.vintage_year}
                onChange={(e) => setNewFund({ ...newFund, vintage_year: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Target Size ($)"
                value={newFund.target_size}
                onChange={(e) => setNewFund({ ...newFund, target_size: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Management Fee (%)"
                value={parseFloat(newFund.management_fee_rate) * 100}
                onChange={(e) => setNewFund({ ...newFund, management_fee_rate: (parseFloat(e.target.value) / 100).toString() })}
                InputProps={{ endAdornment: '%' }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Carried Interest (%)"
                value={parseFloat(newFund.carried_interest_rate) * 100}
                onChange={(e) => setNewFund({ ...newFund, carried_interest_rate: (parseFloat(e.target.value) / 100).toString() })}
                InputProps={{ endAdornment: '%' }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Preferred Return (%)"
                value={parseFloat(newFund.preferred_return_rate) * 100}
                onChange={(e) => setNewFund({ ...newFund, preferred_return_rate: (parseFloat(e.target.value) / 100).toString() })}
                InputProps={{ endAdornment: '%' }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={3}
                label="Description"
                value={newFund.description}
                onChange={(e) => setNewFund({ ...newFund, description: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateFundOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateFund} variant="contained">Create</Button>
        </DialogActions>
      </Dialog>

      {/* Create LP Dialog */}
      <Dialog open={createLPOpen} onClose={() => setCreateLPOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Add Limited Partner</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Name"
                value={newLP.name}
                onChange={(e) => setNewLP({ ...newLP, name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Legal Name"
                value={newLP.legal_name}
                onChange={(e) => setNewLP({ ...newLP, legal_name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Type"
                value={newLP.lp_type}
                onChange={(e) => setNewLP({ ...newLP, lp_type: e.target.value })}
                placeholder="e.g., Pension Fund, Endowment, Family Office"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Contact Person"
                value={newLP.contact_person}
                onChange={(e) => setNewLP({ ...newLP, contact_person: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="email"
                label="Email"
                value={newLP.email}
                onChange={(e) => setNewLP({ ...newLP, email: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Phone"
                value={newLP.phone}
                onChange={(e) => setNewLP({ ...newLP, phone: e.target.value })}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateLPOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateLP} variant="contained">Add LP</Button>
        </DialogActions>
      </Dialog>

      {/* Waterfall Calculator Dialog */}
      <Dialog open={waterfallCalcOpen} onClose={() => setWaterfallCalcOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Distribution Waterfall Calculator</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                select
                label="Waterfall Type"
                value={waterfallCalc.waterfall_type}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, waterfall_type: e.target.value })}
              >
                <MenuItem value="american">American (Deal-by-Deal)</MenuItem>
                <MenuItem value="european">European (Whole Fund)</MenuItem>
              </TextField>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Distribution Amount ($)"
                value={waterfallCalc.distribution_amount}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, distribution_amount: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Total Invested ($)"
                value={waterfallCalc.total_invested}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, total_invested: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Total Distributed to Date ($)"
                value={waterfallCalc.total_distributed_to_date}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, total_distributed_to_date: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                type="number"
                label="Preferred Return (%)"
                value={parseFloat(waterfallCalc.preferred_return_rate) * 100}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, preferred_return_rate: (parseFloat(e.target.value) / 100).toString() })}
                InputProps={{ endAdornment: '%' }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="number"
                label="Carried Interest (%)"
                value={parseFloat(waterfallCalc.carried_interest_rate) * 100}
                onChange={(e) => setWaterfallCalc({ ...waterfallCalc, carried_interest_rate: (parseFloat(e.target.value) / 100).toString() })}
                InputProps={{ endAdornment: '%' }}
              />
            </Grid>

            {waterfallResult && (
              <Grid item xs={12}>
                <Paper sx={{ p: 2, mt: 2, bgcolor: 'background.default' }}>
                  <Typography variant="h6" gutterBottom>
                    Waterfall Breakdown ({waterfallResult.waterfall_type})
                  </Typography>
                  <TableContainer>
                    <Table size="small">
                      <TableBody>
                        {Object.entries(waterfallResult.calculation).map(([key, value]) => (
                          <TableRow key={key}>
                            <TableCell>
                              {key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                            </TableCell>
                            <TableCell align="right">
                              <Typography variant="body2" fontWeight="medium">
                                {formatCurrency(value as number)}
                              </Typography>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Paper>
              </Grid>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setWaterfallCalcOpen(false);
            setWaterfallResult(null);
          }}>Close</Button>
          <Button onClick={handleCalculateWaterfall} variant="contained">Calculate</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default FundManagementDashboard;
