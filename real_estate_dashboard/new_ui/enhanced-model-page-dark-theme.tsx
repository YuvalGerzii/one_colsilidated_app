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
  Button,
  Container,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Calculate as CalculateIcon,
  Assessment as AssessmentIcon,
  ShowChart as ShowChartIcon,
  MenuBook as MenuBookIcon,
  Analytics as AnalyticsIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
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

// Styled components for dark theme
const DarkThemeWrapper = styled(Box, {
  shouldForwardProp: (prop) => prop !== 'isDarkTheme',
})<{ isDarkTheme?: boolean }>(({ theme, isDarkTheme }) => ({
  ...(isDarkTheme && {
    background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
    minHeight: '100vh',
    margin: '-24px',
    padding: '24px',
    width: 'calc(100% + 48px)',

    '& .MuiTypography-root': {
      color: 'white',
    },
    
    '& .MuiTypography-body2, & .MuiTypography-caption': {
      color: 'rgba(255, 255, 255, 0.8)',
    },

    '& .MuiPaper-root, & .MuiCard-root': {
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
      backdropFilter: 'blur(10px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
    },
  }),
}));

const StyledTabs = styled(Tabs, {
  shouldForwardProp: (prop) => prop !== 'isDarkTheme',
})<{ isDarkTheme?: boolean }>(({ theme, isDarkTheme }) => ({
  borderBottom: isDarkTheme ? 'none' : '1px solid',
  borderColor: isDarkTheme ? 'transparent' : theme.palette.divider,
  ...(isDarkTheme && {
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    borderRadius: '12px',
    padding: '4px',
    '& .MuiTabs-indicator': {
      backgroundColor: 'white',
      height: '3px',
    },
  }),
}));

const StyledTab = styled(Tab, {
  shouldForwardProp: (prop) => prop !== 'isDarkTheme',
})<{ isDarkTheme?: boolean }>(({ theme, isDarkTheme }) => ({
  minHeight: 64,
  textTransform: 'none',
  fontSize: '0.95rem',
  fontWeight: 500,
  ...(isDarkTheme && {
    color: 'rgba(255, 255, 255, 0.7)',
    '&.Mui-selected': {
      color: 'white',
    },
    '&:hover': {
      backgroundColor: 'rgba(255, 255, 255, 0.05)',
    },
  }),
}));

const JumpToChip = styled(Chip)(({ theme }) => ({
  cursor: 'pointer',
  transition: 'all 0.2s',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
  },
}));

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
  darkTheme?: boolean;
  fullPage?: boolean;
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
  darkTheme = false,
  fullPage = false,
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const [isCalculatorLoaded, setCalculatorLoaded] = useState(false);
  const [iframeKey, setIframeKey] = useState(0);
  const [modelResults, setModelResults] = useState<ModelResults | null>(null);
  const [hasRunAnalysis, setHasRunAnalysis] = useState(false);
  const navigate = useNavigate();
  const theme = useTheme();

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
    setIframeKey((prev) => prev + 1);
    setModelResults(null);
    setHasRunAnalysis(false);
  };

  // Quick jump models configuration
  const quickJumpModels = [
    { label: 'Single-Family Rental', path: '/real-estate-models/single-family-rental' },
    { label: 'Small Multifamily (2-6 units)', path: '/real-estate-models/small-multifamily' },
    { label: 'Hotel', path: '/real-estate-models/hotel' },
    { label: 'High-Rise Multifamily (7+ units)', path: '/real-estate-models/extended-multifamily' },
    { label: 'Mixed-Use Tower', path: '/real-estate-models/mixed-use' },
    { label: 'Lease Analyzer', path: '/real-estate-models/lease-analyzer' },
    { label: 'Renovation Budget', path: '/real-estate-models/renovation-budget' },
  ];

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

  const renderMetricCard = (label: string, value: string, index: number) => {
    return (
      <Grid item xs={12} sm={6} md={4} key={index}>
        <Paper
          elevation={3}
          sx={{
            p: 3,
            borderLeft: `6px solid ${modelConfig.color}`,
            height: '100%',
            background: darkTheme 
              ? `rgba(255, 255, 255, 0.05)`
              : `linear-gradient(135deg, ${modelConfig.color}08 0%, ${modelConfig.color}15 100%)`,
            backdropFilter: darkTheme ? 'blur(10px)' : 'none',
            border: darkTheme ? '1px solid rgba(255, 255, 255, 0.1)' : 'none',
            transition: 'transform 0.2s, box-shadow 0.2s',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: 6,
            },
          }}
        >
          <Typography 
            variant="subtitle2" 
            color={darkTheme ? 'rgba(255, 255, 255, 0.8)' : 'text.secondary'} 
            gutterBottom 
            sx={{ fontSize: '0.875rem', fontWeight: 500 }}
          >
            {label}
          </Typography>
          <Typography 
            variant="h3" 
            sx={{ 
              color: darkTheme ? 'white' : modelConfig.color, 
              fontWeight: 700, 
              fontSize: '2.5rem', 
              mt: 1 
            }}
          >
            {value}
          </Typography>
        </Paper>
      </Grid>
    );
  };

  const ContentWrapper = fullPage ? Box : Container;
  const contentProps = fullPage ? {} : { maxWidth: 'xl' as const };

  return (
    <DarkThemeWrapper isDarkTheme={darkTheme}>
      <ContentWrapper {...contentProps}>
        <Stack spacing={3}>
          {/* Header */}
          <Box sx={{ mb: 2 }}>
            <Button
              startIcon={<ArrowBackIcon />}
              onClick={() => navigate('/real-estate-tools')}
              sx={{
                color: darkTheme ? 'rgba(255, 255, 255, 0.9)' : 'primary.main',
                mb: 3,
                '&:hover': {
                  backgroundColor: darkTheme ? 'rgba(255, 255, 255, 0.1)' : 'action.hover',
                },
              }}
            >
              All real estate models
            </Button>

            <Typography 
              variant="h3" 
              sx={{ 
                fontWeight: 700, 
                mb: 2,
                color: darkTheme ? 'white' : 'text.primary'
              }}
            >
              {modelConfig.label} financial model
            </Typography>

            <Typography 
              variant="h6" 
              sx={{ 
                mb: 4, 
                opacity: darkTheme ? 0.9 : 1, 
                lineHeight: 1.6, 
                maxWidth: '900px',
                color: darkTheme ? 'rgba(255, 255, 255, 0.9)' : 'text.secondary'
              }}
            >
              {modelConfig.description}
            </Typography>

            {/* Jump to section - only show in dark theme */}
            {darkTheme && (
              <Box sx={{ mb: 4 }}>
                <Typography 
                  variant="body1" 
                  sx={{ 
                    mb: 2, 
                    opacity: 0.8,
                    color: 'rgba(255, 255, 255, 0.8)'
                  }}
                >
                  Jump to:
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                  {quickJumpModels.map((model, index) => (
                    <JumpToChip
                      key={index}
                      label={model.label}
                      onClick={() => navigate(model.path)}
                      sx={{ 
                        mb: 1,
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        color: 'white',
                        border: '1px solid rgba(255, 255, 255, 0.2)',
                        '&:hover': {
                          backgroundColor: 'rgba(255, 255, 255, 0.15)',
                        },
                      }}
                    />
                  ))}
                </Stack>
              </Box>
            )}
          </Box>

          {/* Model Info Card - skip in dark theme */}
          {!darkTheme && (
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
          )}

          {/* Tabs */}
          <Card sx={{ 
            bgcolor: darkTheme ? 'transparent' : 'background.paper',
            boxShadow: darkTheme ? 'none' : 1
          }}>
            <Box sx={{ borderBottom: darkTheme ? 0 : 1, borderColor: 'divider', p: darkTheme ? 0 : undefined }}>
              <StyledTabs
                value={activeTab}
                onChange={handleTabChange}
                aria-label="model tabs"
                variant="scrollable"
                scrollButtons="auto"
                isDarkTheme={darkTheme}
                sx={{ px: darkTheme ? 0 : 2 }}
              >
                <StyledTab
                  icon={<CalculateIcon />}
                  iconPosition="start"
                  label="Calculator"
                  id="model-tab-0"
                  isDarkTheme={darkTheme}
                />
                <StyledTab
                  icon={<AssessmentIcon />}
                  iconPosition="start"
                  label="Results"
                  id="model-tab-1"
                  isDarkTheme={darkTheme}
                />
                <StyledTab
                  icon={<ShowChartIcon />}
                  iconPosition="start"
                  label="Charts"
                  id="model-tab-2"
                  isDarkTheme={darkTheme}
                />
                <StyledTab
                  icon={<MenuBookIcon />}
                  iconPosition="start"
                  label="Documentation"
                  id="model-tab-3"
                  isDarkTheme={darkTheme}
                />
                <StyledTab
                  icon={<AnalyticsIcon />}
                  iconPosition="start"
                  label="Advanced Analysis"
                  id="model-tab-4"
                  isDarkTheme={darkTheme}
                />
              </StyledTabs>
            </Box>

            <CardContent sx={{ p: darkTheme ? 0 : 3 }}>
              {/* Calculator Tab */}
              <TabPanel value={activeTab} index={0}>
                <Box sx={{ p: darkTheme ? 0 : 3 }}>
                  <Box sx={{ position: 'relative', minHeight: { xs: 600, md: 800 } }}>
                    {!isCalculatorLoaded && (
                      <Stack
                        spacing={2}
                        alignItems="center"
                        justifyContent="center"
                        sx={{
                          position: 'absolute',
                          inset: 0,
                          bgcolor: darkTheme ? 'rgba(30, 60, 114, 0.9)' : 'background.default',
                          zIndex: 1,
                          borderRadius: 1,
                        }}
                      >
                        <CircularProgress 
                          size={60} 
                          sx={{ color: darkTheme ? 'white' : modelConfig.color }} 
                        />
                        <Typography variant="h6" color={darkTheme ? 'white' : 'text.secondary'}>
                          Loading {modelConfig.label} Calculator…
                        </Typography>
                        <Typography variant="body2" color={darkTheme ? 'rgba(255, 255, 255, 0.8)' : 'text.secondary'}>
                          Preparing interactive model interface
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
                        height: { xs: 600, md: 800 },
                        display: isCalculatorLoaded ? 'block' : 'none',
                        borderRadius: 1,
                      }}
                      onLoad={() => setCalculatorLoaded(true)}
                    />
                  </Box>
                </Box>
              </TabPanel>

              {/* Results Tab */}
              <TabPanel value={activeTab} index={1}>
                <Box sx={{ p: darkTheme ? 0 : 3 }}>
                  {!hasRunAnalysis ? (
                    <Alert 
                      severity="info" 
                      icon={<InfoIcon />} 
                      sx={{ 
                        mb: 3,
                        bgcolor: darkTheme ? 'rgba(33, 150, 243, 0.1)' : undefined,
                        color: darkTheme ? 'white' : undefined,
                        '& .MuiAlert-icon': {
                          color: darkTheme ? '#42a5f5' : undefined,
                        },
                      }}
                    >
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
                      {modelResults.tables.map((table, index) => (
                        <Box key={index}>{/* Render table content */}</Box>
                      ))}
                    </Box>
                  ) : (
                    <Typography variant="body2" color={darkTheme ? 'rgba(255, 255, 255, 0.7)' : 'text.secondary'} align="center" sx={{ py: 8 }}>
                      No results available yet
                    </Typography>
                  )}
                </Box>
              </TabPanel>

              {/* Additional tabs content... */}
            </CardContent>
          </Card>
        </Stack>
      </ContentWrapper>
    </DarkThemeWrapper>
  );
};
