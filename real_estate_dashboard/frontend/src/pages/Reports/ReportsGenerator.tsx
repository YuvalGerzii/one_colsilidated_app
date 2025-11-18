import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Stack,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Chip,
  IconButton,
  Alert,
  CircularProgress,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  useTheme,
  alpha,
  SelectChangeEvent,
} from '@mui/material';
import {
  Description as DescriptionIcon,
  GetApp as GetAppIcon,
  PictureAsPdf as PdfIcon,
  Slideshow as PowerPointIcon,
  Assessment as AssessmentIcon,
  AccountBalance as FundIcon,
  Business as BusinessIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

interface Deal {
  id: string;
  property_name: string;
  property_type: string;
  asking_price: number;
  stage: string;
}

interface Fund {
  id: string;
  fund_name: string;
  fund_type: string;
  target_size: number;
}

interface GeneratedReport {
  id: string;
  report_type: string;
  report_name: string;
  status: string;
  data: any;
  generated_at: string;
  error_message?: string;
}

const REPORT_TYPES = [
  {
    value: 'investment_committee_memo',
    label: 'Investment Committee Memo',
    description: 'Professional IC memo from deal data with financial analysis',
    icon: DescriptionIcon,
    color: '#3b82f6',
    requiresDeal: true,
  },
  {
    value: 'quarterly_portfolio',
    label: 'Quarterly Portfolio Report',
    description: 'Portfolio performance report with fund analytics',
    icon: AssessmentIcon,
    color: '#10b981',
    requiresFund: false,
  },
  {
    value: 'market_research',
    label: 'Market Research Report',
    description: 'Market analysis with comparable transactions',
    icon: BusinessIcon,
    color: '#8b5cf6',
    requiresMarket: true,
  },
  {
    value: 'due_diligence_summary',
    label: 'Due Diligence Summary',
    description: 'DD checklist and findings summary for deals',
    icon: CheckCircleIcon,
    color: '#f59e0b',
    requiresDeal: true,
  },
];

export const ReportsGenerator: React.FC = () => {
  const navigate = useNavigate();
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  // State
  const [selectedReportType, setSelectedReportType] = useState('');
  const [reportName, setReportName] = useState('');
  const [selectedDeal, setSelectedDeal] = useState('');
  const [selectedFund, setSelectedFund] = useState('');
  const [market, setMarket] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [quarter, setQuarter] = useState<number>(1);
  const [year, setYear] = useState<number>(new Date().getFullYear());
  const [includeCharts, setIncludeCharts] = useState(true);

  // Data
  const [deals, setDeals] = useState<Deal[]>([]);
  const [funds, setFunds] = useState<Fund[]>([]);
  const [generatedReports, setGeneratedReports] = useState<GeneratedReport[]>([]);

  // UI State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [previewDialog, setPreviewDialog] = useState(false);
  const [currentReport, setCurrentReport] = useState<GeneratedReport | null>(null);

  useEffect(() => {
    loadData();
    loadReports();
  }, []);

  const loadData = async () => {
    try {
      // Load deals
      const dealsResponse = await api.get('/crm/api/deals');
      if (dealsResponse.data.success) {
        setDeals(dealsResponse.data.data);
      }

      // Load funds
      const fundsResponse = await api.get('/fund-management/api/funds');
      if (fundsResponse.data.success) {
        setFunds(fundsResponse.data.data);
      }
    } catch (err) {
      console.error('Error loading data:', err);
    }
  };

  const loadReports = async () => {
    try {
      const response = await api.get('/reports');
      if (response.data.success) {
        setGeneratedReports(response.data.data);
      }
    } catch (err) {
      console.error('Error loading reports:', err);
    }
  };

  const handleGenerateReport = async () => {
    if (!selectedReportType || !reportName) {
      setError('Please fill in all required fields');
      return;
    }

    const selectedType = REPORT_TYPES.find((t) => t.value === selectedReportType);
    if (!selectedType) return;

    if (selectedType.requiresDeal && !selectedDeal) {
      setError('Please select a deal for this report type');
      return;
    }

    if (selectedType.requiresMarket && !market) {
      setError('Please enter a market for this report type');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      const payload: any = {
        report_type: selectedReportType,
        report_name: reportName,
        include_charts: includeCharts,
      };

      if (selectedDeal) payload.deal_id = selectedDeal;
      if (selectedFund) payload.fund_id = selectedFund;
      if (market) payload.market = market;
      if (propertyType) payload.property_type = propertyType;
      if (selectedReportType === 'quarterly_portfolio') {
        payload.quarter = quarter;
        payload.year = year;
      }

      const response = await api.post('/reports/generate', payload);

      if (response.data.success || response.data.id) {
        setSuccess('Report generated successfully!');
        setCurrentReport(response.data);
        loadReports();

        // Reset form
        setReportName('');
        setSelectedDeal('');
        setSelectedFund('');
        setMarket('');
        setPropertyType('');
      }
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async (reportId: string) => {
    try {
      const response = await api.post(
        `/reports/${reportId}/export/pdf`,
        {},
        { responseType: 'blob' }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${reportId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to export PDF');
    }
  };

  const handleExportPowerPoint = async (reportId: string) => {
    try {
      const response = await api.post(
        `/reports/${reportId}/export/powerpoint`,
        {},
        { responseType: 'blob' }
      );

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${reportId}.pptx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to export PowerPoint');
    }
  };

  const selectedType = REPORT_TYPES.find((t) => t.value === selectedReportType);

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>
        Professional Report Generator
      </Typography>

      <Grid container spacing={3}>
        {/* Report Type Selection */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3 }}>
                Generate New Report
              </Typography>

              {error && (
                <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
                  {error}
                </Alert>
              )}

              {success && (
                <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
                  {success}
                </Alert>
              )}

              <Stack spacing={3}>
                {/* Report Type */}
                <FormControl fullWidth>
                  <InputLabel>Report Type</InputLabel>
                  <Select
                    value={selectedReportType}
                    onChange={(e: SelectChangeEvent) => setSelectedReportType(e.target.value)}
                    label="Report Type"
                  >
                    {REPORT_TYPES.map((type) => (
                      <MenuItem key={type.value} value={type.value}>
                        <Stack direction="row" spacing={1} alignItems="center">
                          <type.icon sx={{ color: type.color }} />
                          <Box>
                            <Typography>{type.label}</Typography>
                            <Typography variant="caption" color="text.secondary">
                              {type.description}
                            </Typography>
                          </Box>
                        </Stack>
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                {/* Report Name */}
                <TextField
                  fullWidth
                  label="Report Name"
                  value={reportName}
                  onChange={(e) => setReportName(e.target.value)}
                  placeholder="e.g., Q1 2024 Portfolio Performance"
                />

                {/* Deal Selection */}
                {selectedType?.requiresDeal && (
                  <FormControl fullWidth>
                    <InputLabel>Select Deal</InputLabel>
                    <Select
                      value={selectedDeal}
                      onChange={(e: SelectChangeEvent) => setSelectedDeal(e.target.value)}
                      label="Select Deal"
                    >
                      {deals.map((deal) => (
                        <MenuItem key={deal.id} value={deal.id}>
                          {deal.property_name} - {deal.property_type} - $
                          {deal.asking_price?.toLocaleString()}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                )}

                {/* Fund Selection */}
                {selectedReportType === 'quarterly_portfolio' && (
                  <>
                    <FormControl fullWidth>
                      <InputLabel>Select Fund (Optional)</InputLabel>
                      <Select
                        value={selectedFund}
                        onChange={(e: SelectChangeEvent) => setSelectedFund(e.target.value)}
                        label="Select Fund (Optional)"
                      >
                        <MenuItem value="">All Funds</MenuItem>
                        {funds.map((fund) => (
                          <MenuItem key={fund.id} value={fund.id}>
                            {fund.fund_name} - {fund.fund_type}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>

                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <FormControl fullWidth>
                          <InputLabel>Quarter</InputLabel>
                          <Select
                            value={quarter.toString()}
                            onChange={(e: SelectChangeEvent) =>
                              setQuarter(parseInt(e.target.value))
                            }
                            label="Quarter"
                          >
                            <MenuItem value={1}>Q1</MenuItem>
                            <MenuItem value={2}>Q2</MenuItem>
                            <MenuItem value={3}>Q3</MenuItem>
                            <MenuItem value={4}>Q4</MenuItem>
                          </Select>
                        </FormControl>
                      </Grid>
                      <Grid item xs={6}>
                        <TextField
                          fullWidth
                          label="Year"
                          type="number"
                          value={year}
                          onChange={(e) => setYear(parseInt(e.target.value))}
                        />
                      </Grid>
                    </Grid>
                  </>
                )}

                {/* Market Research Fields */}
                {selectedType?.requiresMarket && (
                  <>
                    <TextField
                      fullWidth
                      label="Market"
                      value={market}
                      onChange={(e) => setMarket(e.target.value)}
                      placeholder="e.g., Austin, TX"
                    />
                    <TextField
                      fullWidth
                      label="Property Type (Optional)"
                      value={propertyType}
                      onChange={(e) => setPropertyType(e.target.value)}
                      placeholder="e.g., Multifamily"
                    />
                  </>
                )}

                {/* Generate Button */}
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGenerateReport}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <DescriptionIcon />}
                >
                  {loading ? 'Generating...' : 'Generate Report'}
                </Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        {/* Report Types Info */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Available Report Types
              </Typography>
              <List>
                {REPORT_TYPES.map((type) => (
                  <ListItem key={type.value}>
                    <ListItemIcon>
                      <type.icon sx={{ color: type.color }} />
                    </ListItemIcon>
                    <ListItemText
                      primary={type.label}
                      secondary={type.description}
                      primaryTypographyProps={{ fontWeight: 'medium' }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Generated Reports List */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                Generated Reports
              </Typography>

              {generatedReports.length === 0 ? (
                <Alert severity="info">No reports generated yet</Alert>
              ) : (
                <Grid container spacing={2}>
                  {generatedReports.map((report) => (
                    <Grid item xs={12} md={6} lg={4} key={report.id}>
                      <Paper
                        sx={{
                          p: 2,
                          borderLeft: 4,
                          borderColor:
                            REPORT_TYPES.find((t) => t.value === report.report_type)?.color ||
                            'primary.main',
                        }}
                      >
                        <Stack spacing={2}>
                          <Box>
                            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                              {report.report_name}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {new Date(report.generated_at).toLocaleString()}
                            </Typography>
                          </Box>

                          <Chip
                            label={
                              REPORT_TYPES.find((t) => t.value === report.report_type)?.label ||
                              report.report_type
                            }
                            size="small"
                            sx={{
                              alignSelf: 'flex-start',
                              bgcolor:
                                REPORT_TYPES.find((t) => t.value === report.report_type)?.color ||
                                'primary.main',
                              color: 'white',
                            }}
                          />

                          {report.status === 'completed' ? (
                            <Stack direction="row" spacing={1}>
                              <Button
                                size="small"
                                variant="outlined"
                                startIcon={<PdfIcon />}
                                onClick={() => handleExportPDF(report.id)}
                              >
                                PDF
                              </Button>
                              <Button
                                size="small"
                                variant="outlined"
                                startIcon={<PowerPointIcon />}
                                onClick={() => handleExportPowerPoint(report.id)}
                              >
                                PPT
                              </Button>
                            </Stack>
                          ) : report.status === 'failed' ? (
                            <Alert severity="error">
                              {report.error_message || 'Generation failed'}
                            </Alert>
                          ) : (
                            <CircularProgress size={24} />
                          )}
                        </Stack>
                      </Paper>
                    </Grid>
                  ))}
                </Grid>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ReportsGenerator;
