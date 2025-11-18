import React, { useState, useMemo, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  CircularProgress,
  Stack,
  Tab,
  Tabs,
  Typography,
  Alert,
  Chip,
  Grid,
  Paper,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  ShowChart as ShowChartIcon,
  MenuBook as MenuBookIcon,
  Analytics as AnalyticsIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';
import { PageHeader } from '../../components/common/PageHeader';
import { ModelConfig } from '../../config/modelConfig';
import ReactMarkdown from 'react-markdown';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

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
      id={`model-tabpanel-${index}`}
      aria-labelledby={`model-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

interface EnhancedModelPageProps {
  modelConfig: ModelConfig;
  children?: React.ReactNode;
}

interface ModelResults {
  tables?: Array<{
    title: string;
    headers?: string[];
    rows?: Array<string[]>;
    columns?: string[];
    kind?: string;
    metrics?: Record<string, string>;
  }>;
  charts?: Array<{
    title: string;
    type: string;
    data: {
      labels: string[];
      datasets: Array<{
        label: string;
        data: number[];
        backgroundColor?: string | string[];
        borderColor?: string;
      }>;
    };
  }>;
}

export const EnhancedModelPage: React.FC<EnhancedModelPageProps> = ({
  modelConfig,
  children,
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const [isCalculatorLoaded, setCalculatorLoaded] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);
  const [modelResults, setModelResults] = useState<ModelResults | null>(null);
  const [hasRunAnalysis, setHasRunAnalysis] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [loadTimeout, setLoadTimeout] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const modelUrl = useMemo(() => {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const normalizedBase = API_BASE_URL.replace(/\/$/, '');
    const backendSlug = modelConfig.id.replace(/-/g, '_');
    return `${normalizedBase}/real-estate/tools/${backendSlug}`;
  }, [modelConfig.id]);

  const handleRefreshCalculator = () => {
    setCalculatorLoaded(false);
    setLoadError(false);
    setLoadTimeout(false);
    setIframeKey((prev) => prev + 1);
    setModelResults(null);
    setHasRunAnalysis(false);
    setRetryCount((prev) => prev + 1);
  };

  // Listen for messages from iframe
  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === 'MODEL_RESULTS') {
        console.log('Received model results:', event.data);
        setModelResults(event.data.data);
        setHasRunAnalysis(true);
      } else if (event.data.type === 'MODEL_ERROR') {
        console.error('Model error:', event.data.error);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  // Timeout detection for calculator loading
  useEffect(() => {
    if (!isCalculatorLoaded && !loadError && !loadTimeout) {
      const timeoutId = setTimeout(() => {
        if (!isCalculatorLoaded) {
          console.warn('Calculator loading timed out after 30 seconds');
          setLoadTimeout(true);
        }
      }, 30000); // 30 second timeout

      return () => clearTimeout(timeoutId);
    }
  }, [isCalculatorLoaded, loadError, loadTimeout, iframeKey]);

  const renderMetricCard = (label: string, value: string, index: number) => {
    return (
      <Grid item xs={12} sm={6} md={4} key={index}>
        <Paper
          elevation={3}
          sx={{
            p: 3,
            borderLeft: `6px solid ${modelConfig.color}`,
            height: '100%',
            background: `linear-gradient(135deg, ${modelConfig.color}08 0%, ${modelConfig.color}15 100%)`,
            transition: 'transform 0.2s, box-shadow 0.2s',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ fontSize: '0.875rem', fontWeight: 500 }}>
            {label}
          </Typography>
          <Typography variant="h3" sx={{ color: modelConfig.color, fontWeight: 700, fontSize: '2.5rem', mt: 1 }}>
            {value}
          </Typography>
        </Paper>
      </Grid>
    );
  };

  const renderTable = (table: any, index: number) => {
    // Handle metrics display
    if (table.kind === 'metrics' && table.metrics) {
      return (
        <Box key={index} sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
            {table.title}
          </Typography>
          <Grid container spacing={3}>
            {Object.entries(table.metrics).map(([label, value], idx) =>
              renderMetricCard(label, value as string, idx)
            )}
          </Grid>
        </Box>
      );
    }

    // Handle standard tables
    const headers = table.headers || table.columns || [];
    const rows = table.rows || [];

    return (
      <Box key={index} sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
          {table.title}
        </Typography>
        <TableContainer component={Paper} elevation={2}>
          <Table sx={{ minWidth: 650 }}>
            <TableHead sx={{ bgcolor: `${modelConfig.color}15` }}>
              <TableRow>
                {headers.map((header: string, idx: number) => (
                  <TableCell
                    key={idx}
                    sx={{
                      fontWeight: 700,
                      fontSize: '0.95rem',
                      color: modelConfig.color,
                    }}
                  >
                    {header}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row: any, rowIdx: number) => (
                <TableRow
                  key={rowIdx}
                  sx={{
                    '&:nth-of-type(odd)': { bgcolor: 'action.hover' },
                    '&:hover': { bgcolor: 'action.selected' },
                  }}
                >
                  {Array.isArray(row) ? (
                    row.map((cell: string, cellIdx: number) => (
                      <TableCell key={cellIdx} sx={{ fontSize: '0.9rem' }}>
                        {cell}
                      </TableCell>
                    ))
                  ) : (
                    headers.map((header: string, cellIdx: number) => (
                      <TableCell key={cellIdx} sx={{ fontSize: '0.9rem' }}>
                        {row[header] || row[header.toLowerCase()] || ''}
                      </TableCell>
                    ))
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    );
  };

  const renderChart = (chart: any, index: number) => {
    const chartData = {
      labels: chart.data?.labels || [],
      datasets: (chart.data?.datasets || []).map((dataset: any, idx: number) => ({
        ...dataset,
        backgroundColor: dataset.backgroundColor || [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ][idx % 5],
        borderColor: dataset.borderColor || modelConfig.color,
        borderWidth: 2,
      })),
    };

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top' as const,
        },
        title: {
          display: false,
        },
      },
    };

    const ChartComponent = chart.type === 'bar' ? Bar : chart.type === 'pie' ? Pie : Line;

    return (
      <Grid item xs={12} md={6} key={index}>
        <Paper elevation={3} sx={{ p: 3, height: 400 }}>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: 2 }}>
            {chart.title}
          </Typography>
          <Box sx={{ height: 320 }}>
            <ChartComponent data={chartData} options={options} />
          </Box>
        </Paper>
      </Grid>
    );
  };

  return (
    <Stack spacing={3}>
      {/* Header */}
      <PageHeader
        title={modelConfig.label}
        description={modelConfig.description}
        icon={modelConfig.icon}
      />

      {/* Model Info Card */}
      <Card sx={{ bgcolor: `${modelConfig.color}10`, borderLeft: `4px solid ${modelConfig.color}` }}>
        <CardContent>
          <Stack direction="row" spacing={2} alignItems="center" flexWrap="wrap">
            <Chip
              label={modelConfig.category.toUpperCase()}
              size="small"
              sx={{
                bgcolor: modelConfig.color,
                color: 'white',
                fontWeight: 600,
              }}
            />
            <Typography variant="body2" color="text.secondary" sx={{ flex: 1 }}>
              {modelConfig.description}
            </Typography>
            {hasRunAnalysis && (
              <Chip
                icon={<CheckCircleIcon />}
                label="Analysis Complete"
                color="success"
                size="small"
              />
            )}
          </Stack>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Card>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs
            value={activeTab}
            onChange={handleTabChange}
            aria-label="model tabs"
            variant="scrollable"
            scrollButtons="auto"
            sx={{
              px: 2,
              '& .MuiTab-root': {
                minHeight: 64,
                textTransform: 'none',
                fontSize: '0.95rem',
                fontWeight: 500,
              },
            }}
          >
            <Tab
              icon={<CalculateIcon />}
              iconPosition="start"
              label="Calculator"
              id="model-tab-0"
            />
            <Tab
              icon={<AssessmentIcon />}
              iconPosition="start"
              label="Results"
              id="model-tab-1"
            />
            <Tab
              icon={<ShowChartIcon />}
              iconPosition="start"
              label="Charts"
              id="model-tab-2"
            />
            <Tab
              icon={<MenuBookIcon />}
              iconPosition="start"
              label="Documentation"
              id="model-tab-3"
            />
            <Tab
              icon={<AnalyticsIcon />}
              iconPosition="start"
              label="Advanced Analysis"
              id="model-tab-4"
            />
          </Tabs>
        </Box>

        <CardContent sx={{ p: 0 }}>
          {/* Calculator Tab */}
          <TabPanel value={activeTab} index={0}>
            <Box sx={{ p: 3 }}>
              {(loadError || loadTimeout) ? (
                <Alert
                  severity="error"
                  sx={{ mb: 3 }}
                  action={
                    <Stack direction="row" spacing={1}>
                      <Box
                        component="a"
                        href={modelUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        sx={{
                          px: 2,
                          py: 1,
                          bgcolor: modelConfig.color,
                          color: 'white',
                          borderRadius: 1,
                          textDecoration: 'none',
                          fontSize: '0.875rem',
                          fontWeight: 500,
                          '&:hover': {
                            opacity: 0.9,
                          },
                        }}
                      >
                        Open in New Tab
                      </Box>
                      <Box
                        component="button"
                        onClick={handleRefreshCalculator}
                        sx={{
                          px: 2,
                          py: 1,
                          bgcolor: 'grey.700',
                          color: 'white',
                          border: 0,
                          borderRadius: 1,
                          cursor: 'pointer',
                          fontSize: '0.875rem',
                          fontWeight: 500,
                          '&:hover': {
                            bgcolor: 'grey.800',
                          },
                        }}
                      >
                        Retry ({retryCount})
                      </Box>
                    </Stack>
                  }
                >
                  <Typography variant="subtitle2" gutterBottom>
                    {loadTimeout ? 'Calculator Loading Timeout' : 'Calculator Loading Error'}
                  </Typography>
                  <Typography variant="body2">
                    {loadTimeout
                      ? `The calculator is taking longer than expected to load. This might be due to network issues or server delays.`
                      : `There was an error loading the calculator. This might be due to connectivity issues or the backend server being unavailable.`
                    }
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <strong>Troubleshooting:</strong>
                  </Typography>
                  <Typography variant="body2" component="div" sx={{ mt: 0.5 }}>
                    • Click "Retry" to reload the calculator (Attempt {retryCount})
                    <br />
                    • Click "Open in New Tab" to access the calculator directly
                    <br />
                    • Check that the backend server is running on port 8001
                    <br />
                    • Verify your network connection
                    <br />
                    • Check browser console for detailed error messages
                  </Typography>
                </Alert>
              ) : null}

              <Box sx={{ position: 'relative', minHeight: { xs: 1200, md: 2000 } }}>
                {!isCalculatorLoaded && !loadError && !loadTimeout && (
                  <Stack
                    spacing={2}
                    alignItems="center"
                    justifyContent="center"
                    sx={{
                      position: 'absolute',
                      inset: 0,
                      bgcolor: 'background.default',
                      zIndex: 1,
                    }}
                  >
                    <CircularProgress size={60} sx={{ color: modelConfig.color }} />
                    <Typography variant="h6" color="text.secondary">
                      Loading {modelConfig.label} Calculator…
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Preparing interactive model interface
                    </Typography>
                    <Typography variant="caption" color="text.disabled" sx={{ mt: 1 }}>
                      {retryCount > 0 ? `Retry attempt ${retryCount}` : 'This may take a few seconds'}
                    </Typography>
                  </Stack>
                )}
                <Box
                  component="iframe"
                  key={iframeKey}
                  src={modelUrl}
                  title={`${modelConfig.label} Calculator`}
                  sx={{
                    border: 0,
                    width: '100%',
                    height: { xs: 1200, md: 2000 },
                    display: isCalculatorLoaded ? 'block' : 'none',
                    borderRadius: 1,
                  }}
                  onLoad={() => {
                    setCalculatorLoaded(true);
                    setLoadError(false);
                    setLoadTimeout(false);
                  }}
                  onError={() => {
                    console.error('Calculator iframe failed to load');
                    setLoadError(true);
                  }}
                />
              </Box>
            </Box>
          </TabPanel>

          {/* Results Tab */}
          <TabPanel value={activeTab} index={1}>
            <Box sx={{ p: 3 }}>
              {!hasRunAnalysis ? (
                <Alert severity="info" icon={<InfoIcon />} sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    How to View Results
                  </Typography>
                  <Typography variant="body2">
                    Click "Run Analysis" in the Calculator tab to generate financial projections,
                    metrics, and recommendations. Results will appear here automatically.
                  </Typography>
                </Alert>
              ) : modelResults?.tables ? (
                <Box>
                  {modelResults.tables.map((table, index) => renderTable(table, index))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 8 }}>
                  No results available yet
                </Typography>
              )}
            </Box>
          </TabPanel>

          {/* Charts Tab */}
          <TabPanel value={activeTab} index={2}>
            <Box sx={{ p: 3 }}>
              {!hasRunAnalysis ? (
                <Alert severity="info" icon={<ShowChartIcon />} sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Visualizations
                  </Typography>
                  <Typography variant="body2">
                    Interactive charts and graphs will appear here after running an analysis.
                    Visualizations include cash flow projections, ROI analysis, sensitivity
                    scenarios, and more.
                  </Typography>
                </Alert>
              ) : modelResults?.charts && modelResults.charts.length > 0 ? (
                <Grid container spacing={3}>
                  {modelResults.charts.map((chart, index) => renderChart(chart, index))}
                </Grid>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 8 }}>
                  No charts available for this model
                </Typography>
              )}
            </Box>
          </TabPanel>

          {/* Documentation Tab */}
          <TabPanel value={activeTab} index={3}>
            <Box sx={{ p: 3 }}>
              {modelConfig.quickStartGuide && (
                <Paper sx={{ p: 3, mb: 3, bgcolor: 'background.default' }}>
                  <Typography variant="h5" gutterBottom sx={{ color: modelConfig.color }}>
                    📖 Quick Start Guide
                  </Typography>
                  <Divider sx={{ my: 2 }} />
                  <Box
                    sx={{
                      '& h2': {
                        fontSize: '1.5rem',
                        fontWeight: 600,
                        mt: 3,
                        mb: 2,
                        color: 'text.primary',
                      },
                      '& h3': {
                        fontSize: '1.25rem',
                        fontWeight: 600,
                        mt: 2,
                        mb: 1,
                        color: 'text.primary',
                      },
                      '& p': {
                        mb: 2,
                        lineHeight: 1.7,
                      },
                      '& code': {
                        bgcolor: 'rgba(0, 0, 0, 0.05)',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontFamily: 'monospace',
                      },
                      '& pre': {
                        bgcolor: 'rgba(0, 0, 0, 0.05)',
                        p: 2,
                        borderRadius: 1,
                        overflow: 'auto',
                      },
                      '& ul, & ol': {
                        mb: 2,
                        pl: 3,
                      },
                      '& li': {
                        mb: 1,
                      },
                      '& table': {
                        width: '100%',
                        borderCollapse: 'collapse',
                        mb: 2,
                      },
                      '& th, & td': {
                        border: '1px solid',
                        borderColor: 'divider',
                        p: 1.5,
                        textAlign: 'left',
                      },
                      '& th': {
                        bgcolor: 'rgba(0, 0, 0, 0.05)',
                        fontWeight: 600,
                      },
                    }}
                  >
                    <ReactMarkdown>{modelConfig.quickStartGuide}</ReactMarkdown>
                  </Box>
                </Paper>
              )}

              {/* Additional Documentation Links */}
              <Paper sx={{ p: 3, bgcolor: `${modelConfig.color}08` }}>
                <Typography variant="h6" gutterBottom>
                  📚 Additional Resources
                </Typography>
                <Stack spacing={1}>
                  <Typography variant="body2">
                    • Complete user guide available in the model folder
                  </Typography>
                  <Typography variant="body2">
                    • Quick reference card for key formulas
                  </Typography>
                  <Typography variant="body2">
                    • Industry benchmarks and best practices
                  </Typography>
                  <Typography variant="body2">
                    • Step-by-step tutorials and examples
                  </Typography>
                </Stack>
              </Paper>
            </Box>
          </TabPanel>

          {/* Advanced Analysis Tab */}
          <TabPanel value={activeTab} index={4}>
            <Box sx={{ p: 3 }}>
              {!hasRunAnalysis ? (
                <Alert severity="info" icon={<AnalyticsIcon />} sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Advanced Analytics
                  </Typography>
                  <Typography variant="body2">
                    Detailed tables, sensitivity analysis, scenario comparison, and export
                    capabilities will appear here after running an analysis. Perfect for
                    in-depth financial modeling and presentation preparation.
                  </Typography>
                </Alert>
              ) : modelResults?.tables ? (
                <Box>
                  <Typography variant="h5" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
                    Detailed Analysis
                  </Typography>
                  {modelResults.tables.map((table, index) => renderTable(table, index))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary" align="center" sx={{ py: 8 }}>
                  Advanced analysis available after running calculations
                </Typography>
              )}
            </Box>
          </TabPanel>
        </CardContent>
      </Card>

      {/* Help Section */}
      <Alert severity="info" icon={<InfoIcon />}>
        <Typography variant="subtitle2" gutterBottom>
          How to Use This Model
        </Typography>
        <Typography variant="body2">
          1. Start with the <strong>Calculator</strong> tab to input your assumptions
        </Typography>
        <Typography variant="body2">
          2. Click "Run Analysis" to generate financial projections
        </Typography>
        <Typography variant="body2">
          3. Review <strong>Results</strong> and <strong>Charts</strong> for key insights
        </Typography>
        <Typography variant="body2">
          4. Check the <strong>Documentation</strong> tab for detailed guidance
        </Typography>
        <Typography variant="body2">
          5. Use <strong>Advanced Analysis</strong> for detailed tables and export options
        </Typography>
      </Alert>
    </Stack>
  );
};
