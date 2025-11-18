import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  Chip,
  alpha,
  useTheme,
  LinearProgress,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Home as HomeIcon,
  AccountBalance as BalanceIcon,
  Assessment as AssessmentIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Add as AddIcon,
  Delete as DeleteIcon,
  CloudUpload as ImportIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import { useCompany } from '../../context/CompanyContext';

interface Property {
  id: string;
  name: string;
  type: string;
  location: string;
  value: number;
  equity: number;
  noi: number;
  occupancy: number;
  capRate: number;
}

interface PortfolioMetrics {
  totalValue: number;
  totalEquity: number;
  totalDebt: number;
  annualNOI: number;
  annualDebtService: number;
  annualCashFlow: number;
  portfolioCapRate: number;
  averageOccupancy: number;
  propertiesCount: number;
}

interface SavedReport {
  id: string;
  modelType: string;
  projectName: string;
  location: string;
  date: string;
  results: any;
  inputs: any;
}

const PROPERTY_TYPES = [
  'Multifamily',
  'Commercial Office',
  'Retail',
  'Industrial',
  'Mixed Use',
  'Hotel',
  'Single Family Rental',
  'Storage',
];

export const PortfolioDashboard: React.FC = () => {
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const { selectedCompany } = useCompany();

  // State
  const [properties, setProperties] = useState<Property[]>([]);
  const [addDialogOpen, setAddDialogOpen] = useState(false);
  const [importDialogOpen, setImportDialogOpen] = useState(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
  const [propertyToDelete, setPropertyToDelete] = useState<string | null>(null);
  const [savedReports, setSavedReports] = useState<SavedReport[]>([]);

  // New property form state
  const [newProperty, setNewProperty] = useState<Partial<Property>>({
    name: '',
    type: 'Multifamily',
    location: '',
    value: 0,
    equity: 0,
    noi: 0,
    occupancy: 0,
    capRate: 0,
  });

  // Load properties and saved reports from localStorage (company-specific)
  useEffect(() => {
    if (!selectedCompany?.id) {
      // No company selected - show empty state
      setProperties([]);
      setSavedReports([]);
      return;
    }

    // Company-specific localStorage keys
    const propertiesKey = `portfolioProperties_${selectedCompany.id}`;
    const reportsKey = `savedReports_${selectedCompany.id}`;

    const saved = localStorage.getItem(propertiesKey);
    if (saved) {
      setProperties(JSON.parse(saved));
    } else {
      // Start with empty array - no default data for new companies
      setProperties([]);
    }

    const reports = localStorage.getItem(reportsKey);
    if (reports) {
      setSavedReports(JSON.parse(reports));
    } else {
      setSavedReports([]);
    }
  }, [selectedCompany?.id]);

  // Calculate portfolio metrics
  const portfolioMetrics: PortfolioMetrics = React.useMemo(() => {
    const totalValue = properties.reduce((sum, p) => sum + p.value, 0);
    const totalEquity = properties.reduce((sum, p) => sum + p.equity, 0);
    const totalDebt = properties.reduce((sum, p) => sum + (p.value - p.equity), 0);
    const annualNOI = properties.reduce((sum, p) => sum + p.noi, 0);
    const averageOccupancy = properties.length > 0
      ? properties.reduce((sum, p) => sum + p.occupancy, 0) / properties.length
      : 0;
    const portfolioCapRate = totalValue > 0 ? (annualNOI / totalValue) * 100 : 0;

    return {
      totalValue,
      totalEquity,
      totalDebt,
      annualNOI,
      annualDebtService: annualNOI * 0.55, // Estimate
      annualCashFlow: annualNOI * 0.45, // Estimate
      portfolioCapRate,
      averageOccupancy,
      propertiesCount: properties.length,
    };
  }, [properties]);

  // Save properties to localStorage whenever they change (company-specific)
  useEffect(() => {
    if (!selectedCompany?.id) return;

    const propertiesKey = `portfolioProperties_${selectedCompany.id}`;
    if (properties.length > 0) {
      localStorage.setItem(propertiesKey, JSON.stringify(properties));
    } else {
      // Remove key if empty to keep localStorage clean
      localStorage.removeItem(propertiesKey);
    }
  }, [properties, selectedCompany?.id]);

  // Add property manually
  const handleAddProperty = () => {
    if (!newProperty.name || !newProperty.location || !newProperty.value) {
      return;
    }

    const property: Property = {
      id: `prop_${Date.now()}`,
      name: newProperty.name,
      type: newProperty.type || 'Multifamily',
      location: newProperty.location,
      value: newProperty.value,
      equity: newProperty.equity || 0,
      noi: newProperty.noi || 0,
      occupancy: newProperty.occupancy || 0,
      capRate: newProperty.capRate || 0,
    };

    setProperties([...properties, property]);
    setAddDialogOpen(false);
    setNewProperty({
      name: '',
      type: 'Multifamily',
      location: '',
      value: 0,
      equity: 0,
      noi: 0,
      occupancy: 0,
      capRate: 0,
    });
  };

  // Import property from saved report
  const handleImportReport = (report: SavedReport) => {
    const property: Property = {
      id: `prop_${Date.now()}`,
      name: report.projectName,
      type: mapModelTypeToPropertyType(report.modelType),
      location: report.location,
      value: extractPropertyValue(report),
      equity: extractEquity(report),
      noi: extractNOI(report),
      occupancy: extractOccupancy(report),
      capRate: extractCapRate(report),
    };

    setProperties([...properties, property]);
    setImportDialogOpen(false);
  };

  // Delete property
  const handleDeleteProperty = () => {
    if (propertyToDelete) {
      setProperties(properties.filter(p => p.id !== propertyToDelete));
      setPropertyToDelete(null);
      setDeleteConfirmOpen(false);
    }
  };

  // Helper functions to extract data from saved reports
  const mapModelTypeToPropertyType = (modelType: string): string => {
    const typeMap: Record<string, string> = {
      'fix-flip': 'Single Family Rental',
      'single-family-rental': 'Single Family Rental',
      'small-multifamily': 'Multifamily',
      'extended-multifamily': 'Multifamily',
      'hotel': 'Hotel',
      'mixed-use': 'Mixed Use',
    };
    return typeMap[modelType] || 'Multifamily';
  };

  const extractPropertyValue = (report: SavedReport): number => {
    return report.inputs?.purchasePrice || report.inputs?.arv || report.inputs?.propertyValue || 0;
  };

  const extractEquity = (report: SavedReport): number => {
    const value = extractPropertyValue(report);
    const downPayment = report.inputs?.downPayment || 0;
    return downPayment;
  };

  const extractNOI = (report: SavedReport): number => {
    return report.results?.annualNOI || report.results?.noi || 0;
  };

  const extractOccupancy = (report: SavedReport): number => {
    return report.inputs?.occupancyRate || 95;
  };

  const extractCapRate = (report: SavedReport): number => {
    return report.results?.capRate || 0;
  };

  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatPercent = (value: number): string => {
    return `${value.toFixed(2)}%`;
  };

  return (
    <Box sx={{ p: 4 }}>
      {/* Header */}
      <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
            Multi-Property Portfolio Dashboard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Comprehensive portfolio analytics and performance tracking
          </Typography>
        </Box>
        <Stack direction="row" spacing={2} alignItems="center">
          <Chip
            label={`${portfolioMetrics.propertiesCount} Properties`}
            color="primary"
            sx={{ fontWeight: 600 }}
          />
          <Chip
            label={formatPercent(portfolioMetrics.portfolioCapRate) + ' Avg Cap Rate'}
            sx={{
              bgcolor: alpha('#10b981', 0.1),
              color: '#10b981',
              fontWeight: 600,
            }}
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setAddDialogOpen(true)}
            sx={{
              background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
            }}
          >
            Add Property
          </Button>
          <Button
            variant="outlined"
            startIcon={<ImportIcon />}
            onClick={() => setImportDialogOpen(true)}
          >
            Import from Reports
          </Button>
        </Stack>
      </Stack>

      {/* Key Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <HomeIcon sx={{ color: 'white', fontSize: 24 }} />
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Portfolio Value
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    {formatCurrency(portfolioMetrics.totalValue)}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <TrendingUpIcon sx={{ color: 'white', fontSize: 24 }} />
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Total Equity
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    {formatCurrency(portfolioMetrics.totalEquity)}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <BalanceIcon sx={{ color: 'white', fontSize: 24 }} />
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Annual NOI
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>
                    {formatCurrency(portfolioMetrics.annualNOI)}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={2}>
                <Box
                  sx={{
                    width: 48,
                    height: 48,
                    borderRadius: 2,
                    background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <AssessmentIcon sx={{ color: 'white', fontSize: 24 }} />
                </Box>
                <Box>
                  <Typography variant="body2" color="text.secondary">
                    Annual Cash Flow
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700, color: '#10b981' }}>
                    {formatCurrency(portfolioMetrics.annualCashFlow)}
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Properties List */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>
            Portfolio Properties
          </Typography>
          <Grid container spacing={3}>
            {properties.map((property) => (
              <Grid item xs={12} md={6} lg={4} key={property.id}>
                <Card
                  sx={{
                    background: isDark
                      ? alpha('#1e293b', 0.5)
                      : alpha('#f8fafc', 0.5),
                    border: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}`,
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: isDark
                        ? '0 12px 24px rgba(0, 0, 0, 0.2)'
                        : '0 12px 24px rgba(0, 0, 0, 0.1)',
                    },
                  }}
                >
                  <CardContent>
                    <Stack spacing={2}>
                      <Stack direction="row" justifyContent="space-between" alignItems="start">
                        <Box flex={1}>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {property.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {property.location}
                          </Typography>
                        </Box>
                        <Stack direction="row" spacing={1} alignItems="center">
                          <Chip
                            label={property.type}
                            size="small"
                            sx={{
                              bgcolor: alpha('#3b82f6', 0.1),
                              color: '#3b82f6',
                            }}
                          />
                          <Tooltip title="Delete property">
                            <IconButton
                              size="small"
                              onClick={() => {
                                setPropertyToDelete(property.id);
                                setDeleteConfirmOpen(true);
                              }}
                              sx={{
                                color: 'error.main',
                                '&:hover': {
                                  bgcolor: alpha('#ef4444', 0.1),
                                },
                              }}
                            >
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Stack>
                      </Stack>

                      <Box>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                          <Typography variant="body2" color="text.secondary">
                            Property Value
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {formatCurrency(property.value)}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                          <Typography variant="body2" color="text.secondary">
                            Equity
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {formatCurrency(property.equity)}
                          </Typography>
                        </Stack>
                        <Stack direction="row" justifyContent="space-between" sx={{ mb: 1 }}>
                          <Typography variant="body2" color="text.secondary">
                            Annual NOI
                          </Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {formatCurrency(property.noi)}
                          </Typography>
                        </Stack>
                      </Box>

                      <Box>
                        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 0.5 }}>
                          <Typography variant="caption" color="text.secondary">
                            Occupancy
                          </Typography>
                          <Typography variant="caption" sx={{ fontWeight: 600 }}>
                            {property.occupancy}%
                          </Typography>
                        </Stack>
                        <LinearProgress
                          variant="determinate"
                          value={property.occupancy}
                          sx={{
                            height: 6,
                            borderRadius: 3,
                            bgcolor: isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1),
                            '& .MuiLinearProgress-bar': {
                              bgcolor: property.occupancy >= 90 ? '#10b981' : property.occupancy >= 80 ? '#f59e0b' : '#ef4444',
                              borderRadius: 3,
                            },
                          }}
                        />
                      </Box>

                      <Stack direction="row" spacing={1}>
                        <Chip
                          label={`${formatPercent(property.capRate)} Cap Rate`}
                          size="small"
                          sx={{
                            bgcolor: alpha('#10b981', 0.1),
                            color: '#10b981',
                            fontSize: '0.75rem',
                          }}
                        />
                      </Stack>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Alerts & Notifications */}
      <Card sx={{ mt: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 3 }}>
            Alerts & Notifications
          </Typography>
          <Stack spacing={2}>
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                border: `1px solid ${alpha('#f59e0b', 0.3)}`,
                bgcolor: alpha('#f59e0b', 0.05),
              }}
            >
              <Stack direction="row" spacing={2} alignItems="start">
                <WarningIcon sx={{ color: '#f59e0b', mt: 0.5 }} />
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    Lease Expiration Alert
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Downtown Office Tower: Major lease expires in 6 months (June 30, 2025)
                  </Typography>
                </Box>
              </Stack>
            </Box>
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                border: `1px solid ${alpha('#10b981', 0.3)}`,
                bgcolor: alpha('#10b981', 0.05),
              }}
            >
              <Stack direction="row" spacing={2} alignItems="start">
                <CheckCircleIcon sx={{ color: '#10b981', mt: 0.5 }} />
                <Box>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                    Strong Performance
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Portfolio maintains {formatPercent(portfolioMetrics.averageOccupancy)} average occupancy across all properties
                  </Typography>
                </Box>
              </Stack>
            </Box>
          </Stack>
        </CardContent>
      </Card>

      {/* Add Property Dialog */}
      <Dialog open={addDialogOpen} onClose={() => setAddDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Typography variant="h5" sx={{ fontWeight: 700 }}>
            Add New Property
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 2 }}>
            <TextField
              label="Property Name"
              fullWidth
              value={newProperty.name}
              onChange={(e) => setNewProperty({ ...newProperty, name: e.target.value })}
              required
            />
            <TextField
              label="Property Type"
              select
              fullWidth
              value={newProperty.type}
              onChange={(e) => setNewProperty({ ...newProperty, type: e.target.value })}
            >
              {PROPERTY_TYPES.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Location"
              fullWidth
              value={newProperty.location}
              onChange={(e) => setNewProperty({ ...newProperty, location: e.target.value })}
              required
            />
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Property Value"
                  type="number"
                  fullWidth
                  value={newProperty.value}
                  onChange={(e) => setNewProperty({ ...newProperty, value: Number(e.target.value) })}
                  required
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Equity"
                  type="number"
                  fullWidth
                  value={newProperty.equity}
                  onChange={(e) => setNewProperty({ ...newProperty, equity: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Annual NOI"
                  type="number"
                  fullWidth
                  value={newProperty.noi}
                  onChange={(e) => setNewProperty({ ...newProperty, noi: Number(e.target.value) })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Occupancy %"
                  type="number"
                  fullWidth
                  value={newProperty.occupancy}
                  onChange={(e) => setNewProperty({ ...newProperty, occupancy: Number(e.target.value) })}
                  inputProps={{ min: 0, max: 100 }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Cap Rate %"
                  type="number"
                  fullWidth
                  value={newProperty.capRate}
                  onChange={(e) => setNewProperty({ ...newProperty, capRate: Number(e.target.value) })}
                />
              </Grid>
            </Grid>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAddDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleAddProperty}
            disabled={!newProperty.name || !newProperty.location || !newProperty.value}
          >
            Add Property
          </Button>
        </DialogActions>
      </Dialog>

      {/* Import from Reports Dialog */}
      <Dialog open={importDialogOpen} onClose={() => setImportDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          <Typography variant="h5" sx={{ fontWeight: 700 }}>
            Import from Saved Reports
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Select a saved report to add to your portfolio
          </Typography>
        </DialogTitle>
        <DialogContent>
          {savedReports.length === 0 ? (
            <Box sx={{ py: 4, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                No saved reports found
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Create and save a model analysis first to import it here
              </Typography>
            </Box>
          ) : (
            <Stack spacing={2} sx={{ mt: 2 }}>
              {savedReports.map((report) => (
                <Card
                  key={report.id}
                  sx={{
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 3,
                    },
                  }}
                  onClick={() => handleImportReport(report)}
                >
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Box>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          {report.projectName}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {report.location} • {report.modelType.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                        </Typography>
                      </Box>
                      <Button variant="outlined" size="small">
                        Import
                      </Button>
                    </Stack>
                  </CardContent>
                </Card>
              ))}
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setImportDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle>
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Confirm Delete
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1">
            Are you sure you want to remove this property from your portfolio? This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)}>Cancel</Button>
          <Button variant="contained" color="error" onClick={handleDeleteProperty}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
