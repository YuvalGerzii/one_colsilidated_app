import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Stack,
  Chip,
  IconButton,
  alpha,
  useTheme,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Folder as FolderIcon,
  Delete as DeleteIcon,
  Visibility as VisibilityIcon,
  GetApp as GetAppIcon,
  Home as HomeIcon,
  Apartment as ApartmentIcon,
  Hotel as HotelIcon,
  Business as BusinessIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';

interface SavedReport {
  id: string;
  modelType: string;
  projectName: string;
  location: string;
  date: string;
  results: any;
  inputs: any;
}

const MODEL_ICONS: Record<string, any> = {
  'fix-flip': HomeIcon,
  'single-family-rental': HomeIcon,
  'small-multifamily': ApartmentIcon,
  'extended-multifamily': ApartmentIcon,
  'hotel': HotelIcon,
  'mixed-use': BusinessIcon,
};

const MODEL_COLORS: Record<string, string> = {
  'fix-flip': '#3b82f6',
  'single-family-rental': '#10b981',
  'small-multifamily': '#8b5cf6',
  'extended-multifamily': '#6366f1',
  'hotel': '#f59e0b',
  'mixed-use': '#14b8a6',
};

export const SavedReports: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [reports, setReports] = useState<SavedReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<SavedReport | null>(null);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = () => {
    const saved = localStorage.getItem('savedReports');
    if (saved) {
      setReports(JSON.parse(saved));
    }
  };

  const handleDelete = (id: string) => {
    const updated = reports.filter((r) => r.id !== id);
    setReports(updated);
    localStorage.setItem('savedReports', JSON.stringify(updated));
  };

  const handleView = (report: SavedReport) => {
    setSelectedReport(report);
    setViewDialogOpen(true);
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
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
          <Box
            sx={{
              width: 48,
              height: 48,
              borderRadius: 3,
              background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 16px rgba(59, 130, 246, 0.3)',
            }}
          >
            <FolderIcon sx={{ fontSize: 24, color: 'white' }} />
          </Box>
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              Saved Reports
            </Typography>
            <Typography variant="body2" color="text.secondary">
              View and manage your saved model analyses
            </Typography>
          </Box>
        </Stack>
      </Box>

      {/* Reports Grid */}
      {reports.length === 0 ? (
        <Card
          sx={{
            p: 6,
            textAlign: 'center',
            background: isDark
              ? `linear-gradient(135deg, ${alpha('#94a3b8', 0.05)} 0%, ${alpha('#64748b', 0.05)} 100%)`
              : `linear-gradient(135deg, ${alpha('#3b82f6', 0.03)} 0%, ${alpha('#8b5cf6', 0.03)} 100%)`,
            border: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#3b82f6', 0.1)}`,
          }}
        >
          <FolderIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
          <Typography variant="h6" sx={{ mb: 1 }}>
            No Saved Reports
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Save your model analyses to review them later
          </Typography>
          <Button variant="contained" onClick={() => navigate('/real-estate-tools')}>
            Go to Models
          </Button>
        </Card>
      ) : (
        <Grid container spacing={3}>
          {reports.map((report) => {
            const Icon = MODEL_ICONS[report.modelType] || HomeIcon;
            const color = MODEL_COLORS[report.modelType] || '#3b82f6';

            return (
              <Grid item xs={12} md={6} lg={4} key={report.id}>
                <Card
                  sx={{
                    height: '100%',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: isDark
                        ? '0 12px 32px rgba(0, 0, 0, 0.3)'
                        : '0 12px 32px rgba(0, 0, 0, 0.1)',
                    },
                  }}
                >
                  <CardContent sx={{ p: 3 }}>
                    {/* Header */}
                    <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
                      <Box
                        sx={{
                          width: 48,
                          height: 48,
                          borderRadius: 2,
                          background: `linear-gradient(135deg, ${color} 0%, ${alpha(color, 0.8)} 100%)`,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          boxShadow: `0 4px 16px ${alpha(color, 0.3)}`,
                        }}
                      >
                        <Icon sx={{ fontSize: 24, color: 'white' }} />
                      </Box>
                      <Box flex={1}>
                        <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
                          {report.projectName}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {report.location}
                        </Typography>
                      </Box>
                    </Stack>

                    {/* Model Type */}
                    <Chip
                      label={report.modelType.split('-').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      size="small"
                      sx={{
                        mb: 2,
                        background: alpha(color, 0.1),
                        color: color,
                        border: `1px solid ${alpha(color, 0.3)}`,
                        fontWeight: 600,
                      }}
                    />

                    {/* Key Metrics */}
                    <Stack spacing={1.5} sx={{ mb: 3 }}>
                      {report.modelType === 'fix-flip' && report.results && (
                        <>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              ROI
                            </Typography>
                            <Typography
                              variant="caption"
                              sx={{
                                fontWeight: 600,
                                color: report.results.roi >= 15 ? '#10b981' : '#f59e0b',
                              }}
                            >
                              {formatPercent(report.results.roi)}
                            </Typography>
                          </Stack>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              Net Profit
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(report.results.grossProfit)}
                            </Typography>
                          </Stack>
                          <Stack direction="row" justifyContent="space-between">
                            <Typography variant="caption" color="text.secondary">
                              MAO
                            </Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatCurrency(report.results.mao)}
                            </Typography>
                          </Stack>
                        </>
                      )}
                    </Stack>

                    {/* Date */}
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2 }}>
                      Saved on {new Date(report.date).toLocaleDateString()}
                    </Typography>

                    {/* Actions */}
                    <Stack direction="row" spacing={1}>
                      <Button
                        size="small"
                        variant="contained"
                        startIcon={<VisibilityIcon />}
                        fullWidth
                        onClick={() => handleView(report)}
                      >
                        View
                      </Button>
                      <IconButton
                        size="small"
                        color="error"
                        onClick={() => handleDelete(report.id)}
                        sx={{
                          border: `1px solid ${alpha('#ef4444', 0.3)}`,
                        }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      )}

      {/* View Dialog */}
      <Dialog
        open={viewDialogOpen}
        onClose={() => setViewDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedReport && (
          <>
            <DialogTitle>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>
                {selectedReport.projectName}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {selectedReport.location} • Saved on {new Date(selectedReport.date).toLocaleDateString()}
              </Typography>
            </DialogTitle>
            <DialogContent>
              <Stack spacing={3}>
                {/* Inputs */}
                <Box>
                  <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                    Inputs
                  </Typography>
                  <Grid container spacing={2}>
                    {Object.entries(selectedReport.inputs).map(([key, value]) => (
                      <Grid item xs={6} key={key}>
                        <Typography variant="caption" color="text.secondary">
                          {key.replace(/([A-Z])/g, ' $1').trim()}
                        </Typography>
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          {typeof value === 'number' ? (
                            key.toLowerCase().includes('price') ||
                            key.toLowerCase().includes('cost') ||
                            key.toLowerCase().includes('value') ||
                            key.toLowerCase().includes('payment') ||
                            key.toLowerCase().includes('arv') ? (
                              formatCurrency(value)
                            ) : key.toLowerCase().includes('rate') ||
                              key.toLowerCase().includes('ltv') ||
                              key.toLowerCase().includes('points') ||
                              key.toLowerCase().includes('pct') ? (
                              `${value}%`
                            ) : (
                              value
                            )
                          ) : (
                            String(value)
                          )}
                        </Typography>
                      </Grid>
                    ))}
                  </Grid>
                </Box>

                {/* Results */}
                {selectedReport.results && (
                  <Box>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Results
                    </Typography>
                    <Grid container spacing={2}>
                      {Object.entries(selectedReport.results)
                        .filter(([key]) => typeof selectedReport.results[key] === 'number')
                        .map(([key, value]) => (
                          <Grid item xs={6} key={key}>
                            <Typography variant="caption" color="text.secondary">
                              {key.replace(/([A-Z])/g, ' $1').trim()}
                            </Typography>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {typeof value === 'number' ? (
                                key.toLowerCase().includes('roi') ||
                                key.toLowerCase().includes('margin') ||
                                key.toLowerCase().includes('return') ||
                                key.toLowerCase().includes('ratio') ? (
                                  formatPercent(value)
                                ) : (
                                  formatCurrency(value as number)
                                )
                              ) : (
                                String(value)
                              )}
                            </Typography>
                          </Grid>
                        ))}
                    </Grid>
                  </Box>
                )}
              </Stack>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setViewDialogOpen(false)}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default SavedReports;
