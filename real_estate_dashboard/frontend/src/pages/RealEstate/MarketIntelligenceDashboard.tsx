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
  Tabs,
  Tab,
  TextField,
  MenuItem,
  Button,
  LinearProgress,
  IconButton,
  Divider,
  Paper,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Assessment as AssessmentIcon,
  Public as PublicIcon,
  LocationCity as LocationCityIcon,
  Business as BusinessIcon,
  Newspaper as NewspaperIcon,
  Refresh as RefreshIcon,
  FilterList as FilterListIcon,
  AccountBalance as BankIcon,
  ShowChart as ChartIcon,
  People as PeopleIcon,
  Construction as ConstructionIcon,
  Article as ArticleIcon,
  CalendarToday as CalendarIcon,
  LocationOn as LocationIcon,
  Domain as DomainIcon,
  Place as PlaceIcon,
  CompareArrows as CompareIcon,
  GetApp as DownloadIcon,
  Search as SearchIcon,
  ExpandMore as ExpandMoreIcon,
  Flag as FlagIcon,
  Language as LanguageIcon,
  Home as HomeIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';
import GentrificationScoreCard from '../../components/GentrificationScoreCard';
import { MarketDataWidget } from '../../components/MarketDataWidget';
import {
  USAEconomicsAnalysis,
  EconomicForecast,
  HistoricalCharts,
  CorrelationMatrix,
  DataUploadDialog,
  MarketDataVisualization,
  MarketIntelligenceInsights,
  AdvancedMarketData,
  FinancialMarketsAnalytics,
  STRDeepDive,
  ZoningIntelligence,
  AnalysisInsightsHub
} from '../../components/economics';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

export const MarketIntelligenceDashboard: React.FC = () => {
  const muiTheme = useTheme();
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Real-time Market Data States (from failsafe endpoints)
  const [marketSummary, setMarketSummary] = useState<any>(null);
  const [employmentData, setEmploymentData] = useState<any>(null);
  const [housingData, setHousingData] = useState<any>(null);
  const [interestRates, setInterestRates] = useState<any>(null);
  const [integrationHealth, setIntegrationHealth] = useState<any>(null);

  // Official Data States
  const [usDatasets, setUsDatasets] = useState<any[]>([]);
  const [israeliDatasets, setIsraeliDatasets] = useState<any[]>([]);
  const [fredHousingData, setFredHousingData] = useState<any>(null);
  const [hudFairMarketRent, setHudFairMarketRent] = useState<any>(null);
  const [fhfaHouseIndex, setFhfaHouseIndex] = useState<any>(null);
  const [boiData, setBoiData] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('housing');
  const [zipCode, setZipCode] = useState('10001');
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);

  // USA Economics Data States
  const [usaEconomicsData, setUsaEconomicsData] = useState<any>(null);
  const [usaEconomicsCategories, setUsaEconomicsCategories] = useState<any>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [indicatorSearchQuery, setIndicatorSearchQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('change'); // 'change', 'name', 'value'
  const [showPositiveOnly, setShowPositiveOnly] = useState<boolean>(false);
  const [showNegativeOnly, setShowNegativeOnly] = useState<boolean>(false);

  // Fetch Real-Time Market Data with Failsafe
  const fetchMarketData = async (retryCount = 0) => {
    try {
      setLoading(true);
      setError(null);

      // Add timeout to prevent hanging
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      try {
        // Fetch comprehensive market summary (with automatic failbacks)
        const summaryResponse = await api.get('/market-intelligence/data/summary', {
          signal: controller.signal
        });
        setMarketSummary(summaryResponse.data);

        // Fetch employment data
        const employmentResponse = await api.get('/market-intelligence/data/employment', {
          signal: controller.signal
        });
        setEmploymentData(employmentResponse.data);

        // Fetch housing indicators
        const housingResponse = await api.get('/market-intelligence/data/housing-indicators', {
          signal: controller.signal
        });
        setHousingData(housingResponse.data);

        // Fetch interest rates
        const ratesResponse = await api.get('/market-intelligence/data/interest-rates', {
          signal: controller.signal
        });
        setInterestRates(ratesResponse.data);

        // Fetch integration health status
        const healthResponse = await api.get('/market-intelligence/data/health', {
          signal: controller.signal
        });
        setIntegrationHealth(healthResponse.data);

        clearTimeout(timeoutId);
      } catch (fetchError) {
        clearTimeout(timeoutId);
        throw fetchError;
      }

    } catch (error: any) {
      console.error('Error fetching market data:', error);

      // Retry logic for network errors
      if (retryCount < 2 && (error.code === 'ECONNABORTED' || error.message?.includes('Network Error') || error.name === 'AbortError')) {
        console.log(`Retrying market data fetch... attempt ${retryCount + 1}`);
        setTimeout(() => fetchMarketData(retryCount + 1), 1000 * (retryCount + 1));
        return;
      }

      // Use fallback data if API fails
      console.warn('Using fallback market intelligence data');

      // Set fallback market summary
      setMarketSummary({
        overview: 'Market data temporarily unavailable - using cached data',
        last_updated: new Date().toISOString(),
        source: 'fallback_data'
      });

      // Set fallback employment data
      setEmploymentData({
        unemployment_rate: 3.8,
        nonfarm_payrolls: 156000,
        labor_force_participation: 62.6,
        average_hourly_earnings: 34.45,
        source: 'mock_data',
        last_updated: new Date().toISOString()
      });

      // Set fallback housing data
      setHousingData({
        house_price_index: 298.5,
        year_over_year_change: 5.2,
        median_home_price: 417900,
        housing_starts: 1372000,
        existing_home_sales: 4090000,
        source: 'mock_data',
        last_updated: new Date().toISOString()
      });

      // Set fallback interest rates
      setInterestRates({
        federal_funds_rate: 5.33,
        mortgage_30y: 7.08,
        mortgage_15y: 6.38,
        treasury_10y: 4.25,
        prime_rate: 8.50,
        source: 'mock_data',
        last_updated: new Date().toISOString()
      });

      // Set fallback integration health
      setIntegrationHealth({
        overall_health: 'degraded',
        total_integrations: 4,
        active_integrations: 0,
        data_sources: ['Cached Data'],
        message: 'Using fallback data - API unavailable'
      });

      setError(`API unavailable - showing cached data. ${error.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  // Fetch US Official Data
  const fetchUSData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch FHFA House Price Index (working integration)
      try {
        const fhfaResponse = await api.get('/integrations/official-data/fhfa/house-price-index');
        setFhfaHouseIndex(fhfaResponse.data);
      } catch (err) {
        console.log('FHFA data not available');
      }

      // Fetch HUD Fair Market Rent (working integration)
      try {
        const hudResponse = await api.get(`/integrations/official-data/hud/fair-market-rent?zip_code=${zipCode}`);
        setHudFairMarketRent(hudResponse.data);
      } catch (err) {
        console.log('HUD data not available');
      }
    } catch (error: any) {
      console.error('Error fetching US data:', error);
      setError('Some US data sources are temporarily unavailable.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch Israeli Official Data
  const fetchIsraeliData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Fetch Bank of Israel data (working integration)
      try {
        const boiHousingResponse = await api.get('/integrations/official-data/bank-of-israel/housing-price-index');
        const boiCpiResponse = await api.get('/integrations/official-data/bank-of-israel/cpi');
        const boiInterestResponse = await api.get('/integrations/official-data/bank-of-israel/interest-rate');

        setBoiData({
          housing: boiHousingResponse.data,
          cpi: boiCpiResponse.data,
          interest: boiInterestResponse.data,
        });
      } catch (err) {
        console.log('Bank of Israel data not available');
      }
    } catch (error: any) {
      console.error('Error fetching Israeli data:', error);
      setError('Israeli data sources are temporarily unavailable.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch USA Economics Data
  const fetchUSAEconomicsData = async (category?: string | null) => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all categories first
      const categoriesResponse = await api.get('/market-intelligence/data/usa-economics/categories');
      setUsaEconomicsCategories(categoriesResponse.data);

      // Fetch indicators with optional category filter
      const params: any = {};
      if (category) {
        params.category = category;
      }
      const dataResponse = await api.get('/market-intelligence/data/usa-economics', { params });
      setUsaEconomicsData(dataResponse.data);
    } catch (error: any) {
      console.error('Error fetching USA economics data:', error);
      setError('USA economics data temporarily unavailable.');
    } finally {
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchMarketData();
  }, []);

  useEffect(() => {
    if (tabValue === 0) { // USA Economics tab
      fetchUSAEconomicsData(selectedCategory);
    } else if (tabValue === 2) { // US Official Data tab
      fetchUSData();
    } else if (tabValue === 3) { // Israeli Official Data tab
      fetchIsraeliData();
    }
  }, [tabValue, zipCode, selectedCategory]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleRefresh = () => {
    fetchMarketData();
    if (tabValue === 0) {
      fetchUSAEconomicsData(selectedCategory);
    } else if (tabValue === 2) {
      fetchUSData();
    } else if (tabValue === 3) {
      fetchIsraeliData();
    }
  };

  // Dynamic stats from real data
  const stats = [
    {
      label: 'Federal Funds Rate',
      value: interestRates ? `${interestRates.federal_funds_rate?.toFixed(2) || '5.33'}%` : 'Loading...',
      change: '+0.00%',
      trend: 'neutral',
      icon: BankIcon,
      color: '#3b82f6',
    },
    {
      label: 'Unemployment Rate',
      value: employmentData ? `${employmentData.unemployment_rate?.toFixed(1) || '3.8'}%` : 'Loading...',
      change: employmentData?.source === 'mock_data' ? '(Mock)' : '(Live)',
      trend: 'down',
      icon: PeopleIcon,
      color: '#10b981',
    },
    {
      label: '30Y Mortgage Rate',
      value: interestRates ? `${interestRates.mortgage_30y?.toFixed(2) || '7.08'}%` : 'Loading...',
      change: interestRates?.source === 'mock_data' ? '(Mock)' : '(Live)',
      trend: 'neutral',
      icon: HomeIcon,
      color: '#8b5cf6',
    },
    {
      label: 'House Price Index',
      value: housingData ? `${housingData.house_price_index?.toFixed(1) || '298.5'}` : 'Loading...',
      change: housingData ? `+${housingData.year_over_year_change?.toFixed(1) || '5.2'}%` : '',
      trend: 'up',
      icon: TimelineIcon,
      color: '#f59e0b',
    },
  ];

  const chartColors = {
    primary: '#3b82f6',
    secondary: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#14b8a6',
  };

  return (
    <Box sx={{ px: 4, py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
          <Stack direction="row" alignItems="center" spacing={2}>
            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
                background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              Market Intelligence
            </Typography>
            <Chip
              icon={<PublicIcon sx={{ fontSize: 16 }} />}
              label="Live Official Data"
              size="small"
              sx={{
                background: isDark
                  ? 'rgba(16, 185, 129, 0.1)'
                  : 'rgba(16, 185, 129, 0.15)',
                color: '#10b981',
                border: `1px solid ${alpha('#10b981', 0.2)}`,
                fontWeight: 600,
              }}
            />
          </Stack>
          <IconButton
            onClick={handleRefresh}
            disabled={loading}
            sx={{
              bgcolor: isDark ? 'rgba(59, 130, 246, 0.1)' : 'rgba(59, 130, 246, 0.05)',
              '&:hover': {
                bgcolor: isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)',
              },
            }}
          >
            <RefreshIcon sx={{ color: '#3b82f6' }} />
          </IconButton>
        </Stack>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: '800px' }}>
          Official government data, economic indicators, and market intelligence from US and Israeli sources
        </Typography>
      </Box>

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {/* Error Alert */}
      {error && (
        <Alert severity="warning" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Integration Health Status */}
      {integrationHealth && (
        <Alert
          severity={integrationHealth.overall_health === 'healthy' ? 'success' : 'info'}
          sx={{ mb: 3 }}
          icon={<PublicIcon />}
        >
          <strong>Data Sources:</strong> {integrationHealth.active_integrations} of {integrationHealth.total_integrations} integrations active
          {integrationHealth.data_sources && integrationHealth.data_sources.length > 0 && (
            <span> ({integrationHealth.data_sources.join(', ')})</span>
          )}
        </Alert>
      )}

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                background: isDark
                  ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
                  : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
                border: isDark
                  ? `1px solid ${alpha('#94a3b8', 0.1)}`
                  : `1px solid ${alpha('#0f172a', 0.1)}`,
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: isDark
                    ? '0 12px 32px rgba(0, 0, 0, 0.18)'
                    : '0 12px 32px rgba(0, 0, 0, 0.08)',
                },
              }}
            >
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                  <Box>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                      {stat.label}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, mb: 0.5 }}>
                      {stat.value}
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={0.5}>
                      {stat.trend === 'up' && <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />}
                      {stat.trend === 'down' && <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />}
                      <Typography
                        variant="caption"
                        sx={{
                          color: stat.trend === 'up' ? '#10b981' : stat.trend === 'down' ? '#ef4444' : 'text.secondary',
                          fontWeight: 600,
                        }}
                      >
                        {stat.change}
                      </Typography>
                    </Stack>
                  </Box>
                  <Box
                    sx={{
                      width: 48,
                      height: 48,
                      borderRadius: 3,
                      background: `linear-gradient(135deg, ${stat.color} 0%, ${alpha(stat.color, 0.7)} 100%)`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      boxShadow: `0 4px 16px ${alpha(stat.color, 0.3)}`,
                    }}
                  >
                    <stat.icon sx={{ fontSize: 24, color: 'white' }} />
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Tabs */}
      <Card
        sx={{
          background: isDark
            ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
            : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
          border: isDark
            ? `1px solid ${alpha('#94a3b8', 0.1)}`
            : `1px solid ${alpha('#0f172a', 0.1)}`,
        }}
      >
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            px: 2,
            borderBottom: isDark
              ? `1px solid ${alpha('#94a3b8', 0.1)}`
              : `1px solid ${alpha('#0f172a', 0.1)}`,
          }}
        >
          <Tab icon={<AssessmentIcon />} iconPosition="start" label="🇺🇸 USA Economics (345 Indicators)" />
          <Tab icon={<ChartIcon />} iconPosition="start" label="📊 Analysis & Insights" />
          <Tab icon={<FlagIcon />} iconPosition="start" label="🇺🇸 US Official Data" />
          <Tab icon={<FlagIcon />} iconPosition="start" label="🇮🇱 Israeli Official Data" />
          <Tab icon={<BankIcon />} iconPosition="start" label="Economic Indicators" />
          <Tab icon={<ChartIcon />} iconPosition="start" label="Global Market Data" />
          <Tab icon={<HomeIcon />} iconPosition="start" label="Housing Data" />
          <Tab icon={<PlaceIcon />} iconPosition="start" label="Market Presets" />
          <Tab icon={<TimelineIcon />} iconPosition="start" label="📈 Financial Markets Analytics" />
          <Tab icon={<HomeIcon />} iconPosition="start" label="🏠 STR Deep Dive" />
          <Tab icon={<LocationCityIcon />} iconPosition="start" label="🏗️ Zoning Intelligence" />
        </Tabs>

        {/* USA Economics Tab */}
        <TabPanel value={tabValue} index={0}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={4}>
              {/* Header Section */}
              <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={2}>
                <Stack spacing={1}>
                  <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <AssessmentIcon sx={{ color: '#3b82f6' }} />
                    United States Economic Indicators ({usaEconomicsData?.total_indicators || '...'} Total)
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Comprehensive economic data across {Object.keys(usaEconomicsData?.category_summary || {}).length || '...'} categories from official US sources
                  </Typography>
                </Stack>
                <Button
                  variant="contained"
                  startIcon={<DownloadIcon sx={{ transform: 'rotate(180deg)' }} />}
                  onClick={() => setUploadDialogOpen(true)}
                  sx={{ flexShrink: 0 }}
                >
                  Upload Data
                </Button>
              </Stack>

              {/* Summary Stats */}
              {usaEconomicsData && (
                <Grid container spacing={3}>
                  <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' }}>
                      <Typography variant="h3" sx={{ fontWeight: 700, color: 'white' }}>
                        {usaEconomicsData.total_indicators}
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                        Total Indicators
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={3}>
                    <Paper sx={{ p: 3, textAlign: 'center', background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' }}>
                      <Typography variant="h3" sx={{ fontWeight: 700, color: 'white' }}>
                        {Object.keys(usaEconomicsData.category_summary || {}).length}
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.9)' }}>
                        Categories
                      </Typography>
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3 }}>
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
                          <PublicIcon sx={{ color: 'white', fontSize: 28 }} />
                        </Box>
                        <Box>
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {usaEconomicsData.country}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Official Economic Data
                          </Typography>
                        </Box>
                      </Stack>
                    </Paper>
                  </Grid>
                </Grid>
              )}

              {/* Advanced Filters & Search */}
              {usaEconomicsCategories && (
                <Paper sx={{ p: 3 }}>
                  <Stack spacing={3}>
                    {/* Category Filters */}
                    <Box>
                      <Typography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                        Filter by Category
                      </Typography>
                      <Stack direction="row" spacing={1} flexWrap="wrap" sx={{ gap: 1 }}>
                        <Chip
                          label="All Categories"
                          onClick={() => setSelectedCategory(null)}
                          color={selectedCategory === null ? 'primary' : 'default'}
                          sx={{ fontWeight: 600 }}
                        />
                        {usaEconomicsCategories.categories?.map((cat: any) => (
                          <Chip
                            key={cat.category}
                            label={`${cat.category} (${cat.count})`}
                            onClick={() => setSelectedCategory(cat.category)}
                            color={selectedCategory === cat.category ? 'primary' : 'default'}
                            icon={<ChartIcon />}
                          />
                        ))}
                      </Stack>
                    </Box>

                    <Divider />

                    {/* Search and Advanced Filters */}
                    <Grid container spacing={2} alignItems="center">
                      <Grid item xs={12} md={4}>
                        <TextField
                          fullWidth
                          size="small"
                          placeholder="Search indicators..."
                          value={indicatorSearchQuery}
                          onChange={(e) => setIndicatorSearchQuery(e.target.value)}
                          InputProps={{
                            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                          }}
                        />
                      </Grid>
                      <Grid item xs={12} md={3}>
                        <TextField
                          fullWidth
                          size="small"
                          select
                          label="Sort By"
                          value={sortBy}
                          onChange={(e) => setSortBy(e.target.value)}
                        >
                          <MenuItem value="change">Largest Change %</MenuItem>
                          <MenuItem value="name">Indicator Name</MenuItem>
                          <MenuItem value="value">Current Value</MenuItem>
                        </TextField>
                      </Grid>
                      <Grid item xs={12} md={5}>
                        <Stack direction="row" spacing={1}>
                          <Chip
                            label="Positive Only"
                            onClick={() => {
                              setShowPositiveOnly(!showPositiveOnly);
                              setShowNegativeOnly(false);
                            }}
                            color={showPositiveOnly ? 'success' : 'default'}
                            icon={<TrendingUpIcon />}
                          />
                          <Chip
                            label="Negative Only"
                            onClick={() => {
                              setShowNegativeOnly(!showNegativeOnly);
                              setShowPositiveOnly(false);
                            }}
                            color={showNegativeOnly ? 'error' : 'default'}
                            icon={<TrendingDownIcon />}
                          />
                          <Button
                            variant="outlined"
                            size="small"
                            startIcon={<DownloadIcon />}
                            onClick={() => {
                              // Export to CSV
                              if (usaEconomicsData?.indicators) {
                                const csv = [
                                  ['Indicator', 'Category', 'Current Value', 'Previous Value', 'Change %', 'Unit', 'Reference Period'].join(','),
                                  ...usaEconomicsData.indicators.map((ind: any) =>
                                    [ind.indicator_name, ind.category, ind.last_value, ind.previous_value, ind.change_percent || 'N/A', ind.unit || '', ind.reference_period || ''].join(',')
                                  )
                                ].join('\n');
                                const blob = new Blob([csv], { type: 'text/csv' });
                                const url = URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = 'usa-economic-indicators.csv';
                                a.click();
                              }
                            }}
                          >
                            Export CSV
                          </Button>
                        </Stack>
                      </Grid>
                    </Grid>
                  </Stack>
                </Paper>
              )}

              {/* Filtered & Sorted Indicators Table */}
              {usaEconomicsData && (() => {
                // Apply filters and sorting
                let filteredIndicators = usaEconomicsData.indicators || [];

                // Apply search filter
                if (indicatorSearchQuery) {
                  filteredIndicators = filteredIndicators.filter((ind: any) =>
                    ind.indicator_name.toLowerCase().includes(indicatorSearchQuery.toLowerCase()) ||
                    ind.category.toLowerCase().includes(indicatorSearchQuery.toLowerCase())
                  );
                }

                // Apply positive/negative filters
                if (showPositiveOnly) {
                  filteredIndicators = filteredIndicators.filter((ind: any) => ind.change_percent > 0);
                }
                if (showNegativeOnly) {
                  filteredIndicators = filteredIndicators.filter((ind: any) => ind.change_percent < 0);
                }

                // Apply sorting
                if (sortBy === 'change') {
                  filteredIndicators = [...filteredIndicators].sort((a: any, b: any) =>
                    Math.abs(b.change_percent || 0) - Math.abs(a.change_percent || 0)
                  );
                } else if (sortBy === 'name') {
                  filteredIndicators = [...filteredIndicators].sort((a: any, b: any) =>
                    a.indicator_name.localeCompare(b.indicator_name)
                  );
                } else if (sortBy === 'value') {
                  filteredIndicators = [...filteredIndicators].sort((a: any, b: any) =>
                    (b.last_value_numeric || 0) - (a.last_value_numeric || 0)
                  );
                }

                return (
                  <Paper sx={{ p: 3 }}>
                    <Stack spacing={2}>
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          Indicators ({filteredIndicators.length})
                        </Typography>
                        {(indicatorSearchQuery || showPositiveOnly || showNegativeOnly) && (
                          <Chip
                            label="Clear Filters"
                            size="small"
                            onDelete={() => {
                              setIndicatorSearchQuery('');
                              setShowPositiveOnly(false);
                              setShowNegativeOnly(false);
                            }}
                            color="primary"
                            variant="outlined"
                          />
                        )}
                      </Stack>

                      <Grid container spacing={2}>
                        {filteredIndicators.slice(0, 20).map((indicator: any, idx: number) => (
                          <Grid item xs={12} md={6} lg={4} key={idx}>
                            <Paper
                              sx={{
                                p: 2,
                                height: '100%',
                                bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)',
                                border: `1px solid ${isDark ? 'rgba(59, 130, 246, 0.2)' : 'rgba(59, 130, 246, 0.1)'}`,
                                transition: 'all 0.2s',
                                '&:hover': {
                                  transform: 'translateY(-2px)',
                                  boxShadow: 3,
                                },
                              }}
                            >
                              <Stack spacing={1.5}>
                                <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                                  <Box sx={{ flex: 1, pr: 1 }}>
                                    <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
                                      {indicator.indicator_name}
                                    </Typography>
                                    <Chip
                                      label={indicator.category}
                                      size="small"
                                      sx={{
                                        fontSize: '0.65rem',
                                        height: 18,
                                        textTransform: 'capitalize',
                                      }}
                                    />
                                  </Box>
                                  <Box sx={{ textAlign: 'right' }}>
                                    <Typography variant="h6" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                                      {indicator.last_value || 'N/A'}
                                    </Typography>
                                    {indicator.unit && (
                                      <Typography variant="caption" color="text.secondary">
                                        {indicator.unit}
                                      </Typography>
                                    )}
                                  </Box>
                                </Stack>

                                <Divider />

                                <Stack direction="row" justifyContent="space-between" alignItems="center">
                                  <Typography variant="caption" color="text.secondary">
                                    Previous: {indicator.previous_value || 'N/A'}
                                  </Typography>
                                  {indicator.change_percent !== null && indicator.change_percent !== undefined && (
                                    <Stack direction="row" alignItems="center" spacing={0.5}>
                                      {indicator.change_percent > 0 ? (
                                        <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                                      ) : indicator.change_percent < 0 ? (
                                        <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                                      ) : null}
                                      <Typography
                                        variant="caption"
                                        sx={{
                                          color: indicator.change_percent > 0 ? '#10b981' : indicator.change_percent < 0 ? '#ef4444' : 'text.secondary',
                                          fontWeight: 700,
                                          fontSize: '0.85rem',
                                        }}
                                      >
                                        {indicator.change_percent > 0 ? '+' : ''}
                                        {indicator.change_percent.toFixed(2)}%
                                      </Typography>
                                    </Stack>
                                  )}
                                </Stack>

                                <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                                  {indicator.reference_period || 'Period N/A'}
                                </Typography>
                              </Stack>
                            </Paper>
                          </Grid>
                        ))}
                      </Grid>

                      {filteredIndicators.length > 20 && (
                        <Alert severity="info">
                          Showing first 20 of {filteredIndicators.length} indicators. Use filters to narrow down results.
                        </Alert>
                      )}

                      {filteredIndicators.length === 0 && (
                        <Alert severity="warning">
                          No indicators match your current filters. Try adjusting your search or filter criteria.
                        </Alert>
                      )}
                    </Stack>
                  </Paper>
                );
              })()}

              {/* Loading State */}
              {!usaEconomicsData && loading && (
                <Box sx={{ textAlign: 'center', py: 8 }}>
                  <CircularProgress size={48} />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                    Loading USA economic indicators...
                  </Typography>
                </Box>
              )}

              {/* Data Source Info */}
              <Paper sx={{ p: 3, bgcolor: isDark ? 'rgba(16, 185, 129, 0.05)' : 'rgba(16, 185, 129, 0.02)' }}>
                <Stack spacing={2}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    Data Sources & Categories
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    This data includes 10 major economic categories: GDP, Labour, Inflation, Money, Trade, Government,
                    Consumer, Housing, Taxes, and Business confidence metrics from official United States sources.
                  </Typography>
                  <Alert severity="success" icon={<PublicIcon />}>
                    All data is loaded from official government and economic sources through the Sugra AI Economics API
                  </Alert>
                </Stack>
              </Paper>
            </Stack>
          </Box>
        </TabPanel>

        {/* Analysis & Insights Tab */}
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ px: 2 }}>
            <AnalysisInsightsHub />
          </Box>
        </TabPanel>

        {/* US Official Data Tab */}
        <TabPanel value={tabValue} index={2}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={4}>
              {/* Header Section */}
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Stack spacing={1}>
                  <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <FlagIcon sx={{ color: '#3b82f6' }} />
                    United States Official Government Data
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    FREE data from Data.gov, HUD, FHFA, and FRED - No API keys required
                  </Typography>
                </Stack>
                <TextField
                  size="small"
                  label="ZIP Code"
                  value={zipCode}
                  onChange={(e) => setZipCode(e.target.value)}
                  sx={{ width: 120 }}
                />
              </Stack>

              {/* FHFA House Price Index */}
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <TimelineIcon sx={{ color: '#3b82f6' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        FHFA House Price Index
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Official national housing price trends from Federal Housing Finance Agency
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {fhfaHouseIndex ? (
                    <Stack spacing={2}>
                      <Alert severity="info">
                        {fhfaHouseIndex.description}
                      </Alert>
                      <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                          <Paper sx={{ p: 2 }}>
                            <Typography variant="body2" color="text.secondary">Geography Type</Typography>
                            <Typography variant="h6">{fhfaHouseIndex.geography_type}</Typography>
                          </Paper>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Paper sx={{ p: 2 }}>
                            <Typography variant="body2" color="text.secondary">Frequency</Typography>
                            <Typography variant="h6">{fhfaHouseIndex.frequency}</Typography>
                          </Paper>
                        </Grid>
                      </Grid>
                      <Button
                        variant="contained"
                        startIcon={<DownloadIcon />}
                        href="https://www.fhfa.gov/DataTools/Downloads/Pages/House-Price-Index-Datasets.aspx"
                        target="_blank"
                      >
                        Download FHFA Datasets
                      </Button>
                    </Stack>
                  ) : (
                    <CircularProgress />
                  )}
                </AccordionDetails>
              </Accordion>

              {/* HUD Fair Market Rent */}
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <HomeIcon sx={{ color: '#10b981' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        HUD Fair Market Rent (ZIP: {zipCode})
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Official rental rates from US Department of Housing & Urban Development
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {hudFairMarketRent ? (
                    <Stack spacing={2}>
                      <Alert severity="success">
                        {hudFairMarketRent.message || 'Fair Market Rent data available'}
                      </Alert>
                      <Typography variant="body2" color="text.secondary">
                        {hudFairMarketRent.description}
                      </Typography>
                      <Button
                        variant="outlined"
                        href={hudFairMarketRent.data_source}
                        target="_blank"
                      >
                        View Official HUD Data
                      </Button>
                    </Stack>
                  ) : (
                    <Alert severity="info">Enter a ZIP code to view Fair Market Rent data</Alert>
                  )}
                </AccordionDetails>
              </Accordion>

              {/* FRED Housing Indicators */}
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <ChartIcon sx={{ color: '#f59e0b' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        FRED Housing Market Indicators
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Federal Reserve Economic Data - Housing market metrics
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {fredHousingData?.housing_indicators ? (
                    <Grid container spacing={2}>
                      {Object.entries(fredHousingData.housing_indicators).map(([key, value]: [string, any]) => (
                        <Grid item xs={12} md={6} lg={4} key={key}>
                          <Card variant="outlined">
                            <CardContent>
                              <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                                {key.replace(/_/g, ' ')}
                              </Typography>
                              <Typography variant="h6" sx={{ fontWeight: 700, my: 1 }}>
                                {value.series_id}
                              </Typography>
                              {value.latest_value && (
                                <Typography variant="body2">
                                  Latest: {value.latest_value.value} ({value.latest_value.date})
                                </Typography>
                              )}
                            </CardContent>
                          </Card>
                        </Grid>
                      ))}
                    </Grid>
                  ) : (
                    <Alert severity="info">Loading FRED housing indicators...</Alert>
                  )}
                </AccordionDetails>
              </Accordion>

              {/* Data.gov Real Estate Datasets */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <PublicIcon sx={{ color: '#8b5cf6' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Data.gov Real Estate Datasets
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        300,000+ government datasets - {usDatasets.length} real estate datasets found
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {usDatasets.length > 0 ? (
                    <List>
                      {usDatasets.slice(0, 5).map((dataset: any, index: number) => (
                        <ListItem key={index} divider>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: '#3b82f6' }}>
                              <ArticleIcon />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={dataset.title || dataset.name}
                            secondary={dataset.notes?.substring(0, 150) + '...'}
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Alert severity="info">Loading real estate datasets from Data.gov...</Alert>
                  )}
                </AccordionDetails>
              </Accordion>
            </Stack>
          </Box>
        </TabPanel>

        {/* Israeli Official Data Tab */}
        <TabPanel value={tabValue} index={3}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={4}>
              {/* Header Section */}
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <FlagIcon sx={{ color: '#3b82f6' }} />
                  Israeli Official Government Data
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  FREE data from Data.gov.il and Bank of Israel - No API keys required
                </Typography>
              </Stack>

              {/* Bank of Israel Economic Data */}
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <BankIcon sx={{ color: '#3b82f6' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Bank of Israel Economic Indicators
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Official economic data from Israel's central bank
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {boiData ? (
                    <Grid container spacing={3}>
                      {/* Housing Price Index */}
                      <Grid item xs={12} md={4}>
                        <Paper sx={{ p: 3, height: '100%' }}>
                          <Stack spacing={2}>
                            <Stack direction="row" alignItems="center" spacing={1}>
                              <HomeIcon sx={{ color: '#10b981' }} />
                              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                Housing Price Index
                              </Typography>
                            </Stack>
                            <Typography variant="body2" color="text.secondary">
                              {boiData.housing?.description}
                            </Typography>
                            <Button
                              variant="outlined"
                              size="small"
                              href={boiData.housing?.data_source}
                              target="_blank"
                            >
                              View Data
                            </Button>
                          </Stack>
                        </Paper>
                      </Grid>

                      {/* CPI */}
                      <Grid item xs={12} md={4}>
                        <Paper sx={{ p: 3, height: '100%' }}>
                          <Stack spacing={2}>
                            <Stack direction="row" alignItems="center" spacing={1}>
                              <ChartIcon sx={{ color: '#f59e0b' }} />
                              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                Consumer Price Index
                              </Typography>
                            </Stack>
                            <Typography variant="body2" color="text.secondary">
                              {boiData.cpi?.description}
                            </Typography>
                            <Button
                              variant="outlined"
                              size="small"
                              href={boiData.cpi?.dashboard_url}
                              target="_blank"
                            >
                              View Dashboard
                            </Button>
                          </Stack>
                        </Paper>
                      </Grid>

                      {/* Interest Rate */}
                      <Grid item xs={12} md={4}>
                        <Paper sx={{ p: 3, height: '100%' }}>
                          <Stack spacing={2}>
                            <Stack direction="row" alignItems="center" spacing={1}>
                              <BankIcon sx={{ color: '#8b5cf6' }} />
                              <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                Interest Rate
                              </Typography>
                            </Stack>
                            <Typography variant="body2" color="text.secondary">
                              {boiData.interest?.message}
                            </Typography>
                            <Button
                              variant="outlined"
                              size="small"
                              href={boiData.interest?.data_source}
                              target="_blank"
                            >
                              View Data
                            </Button>
                          </Stack>
                        </Paper>
                      </Grid>
                    </Grid>
                  ) : (
                    <Alert severity="info">Loading Bank of Israel data...</Alert>
                  )}
                </AccordionDetails>
              </Accordion>

              {/* Data.gov.il Real Estate Datasets */}
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Stack direction="row" alignItems="center" spacing={2}>
                    <PublicIcon sx={{ color: '#10b981' }} />
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        Data.gov.il Real Estate Datasets
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        Israeli government open data - {israeliDatasets.length} real estate datasets (נדל״ן)
                      </Typography>
                    </Box>
                  </Stack>
                </AccordionSummary>
                <AccordionDetails>
                  {israeliDatasets.length > 0 ? (
                    <List>
                      {israeliDatasets.slice(0, 5).map((dataset: any, index: number) => (
                        <ListItem key={index} divider>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: '#10b981' }}>
                              <ArticleIcon />
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={dataset.title || dataset.name}
                            secondary={dataset.notes?.substring(0, 150) + '...'}
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Alert severity="info">Loading real estate datasets from Data.gov.il...</Alert>
                  )}
                </AccordionDetails>
              </Accordion>

              {/* Data Source Links */}
              <Paper sx={{ p: 3, bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)' }}>
                <Stack spacing={2}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    Official Data Sources
                  </Typography>
                  <Stack direction="row" spacing={2} flexWrap="wrap">
                    <Button
                      variant="outlined"
                      href="https://data.gov.il"
                      target="_blank"
                      startIcon={<LanguageIcon />}
                    >
                      Data.gov.il
                    </Button>
                    <Button
                      variant="outlined"
                      href="https://www.boi.org.il/en/economic-roles/statistics/"
                      target="_blank"
                      startIcon={<BankIcon />}
                    >
                      Bank of Israel
                    </Button>
                  </Stack>
                </Stack>
              </Paper>
            </Stack>
          </Box>
        </TabPanel>

        {/* Economic Indicators Tab */}
        <TabPanel value={tabValue} index={4}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={4}>
              {/* Header Section */}
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <AssessmentIcon sx={{ color: '#3b82f6' }} />
                  Economic Indicators & Analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Advanced economic analysis tools powered by real-time market data
                </Typography>
              </Stack>

              {/* Gentrification Risk Score */}
              <Box>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Gentrification Risk Analysis
                </Typography>
                <GentrificationScoreCard />
              </Box>

              {/* Placeholder for future indicators */}
              <Paper sx={{ p: 3, bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)' }}>
                <Stack spacing={2}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                    Coming Soon
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Additional economic indicators and analysis tools will be added here, including:
                  </Typography>
                  <Stack spacing={1} sx={{ pl: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      • Market Cycle Indicator - Identify optimal entry/exit points
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      • Rent Growth Predictor - Forecast rental income trends
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      • Property Investment Score - Comprehensive investment analysis
                    </Typography>
                  </Stack>
                </Stack>
              </Paper>
            </Stack>
          </Box>
        </TabPanel>

        {/* Global Market Data Tab */}
        <TabPanel value={tabValue} index={5}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={4}>
              {/* Header Section */}
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <PublicIcon sx={{ color: '#3b82f6' }} />
                  Global Market Intelligence
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Real-time market data from Yahoo Finance and global economic indicators
                </Typography>
              </Stack>

              {/* Market Data Widget */}
              <MarketDataWidget />
            </Stack>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={6}>
          <Box sx={{ px: 2 }}>
            <Alert severity="info">
              Housing Data tab - Add your existing housing data content here
            </Alert>
          </Box>
        </TabPanel>

        <TabPanel value={tabValue} index={7}>
          <Box sx={{ px: 2 }}>
            <Alert severity="info">
              Market Presets tab - Add your existing market presets content here
            </Alert>
          </Box>
        </TabPanel>

        {/* Financial Markets Analytics Tab */}
        <TabPanel value={tabValue} index={8}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={3}>
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <TimelineIcon sx={{ color: '#3b82f6' }} />
                  Financial Markets Analytics
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Time-series data for Treasury Yield Curve, Fed Policy, Banking Sector, Credit Markets, Global Economics, Corporate Earnings, Consumer Finance, Currency/Commodities, and Institutional Asset Allocation
                </Typography>
              </Stack>
              <FinancialMarketsAnalytics />
            </Stack>
          </Box>
        </TabPanel>

        {/* STR Deep Dive Tab */}
        <TabPanel value={tabValue} index={9}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={3}>
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <HomeIcon sx={{ color: '#10b981' }} />
                  Short-Term Rental (STR) Deep Dive
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive STR analytics across 9 categories: Competitive Analysis, Compliance, Demographics, Economics, Market Impact, Investment Analysis, Platform Performance, Pricing, and Supply-Demand
                </Typography>
              </Stack>
              <STRDeepDive />
            </Stack>
          </Box>
        </TabPanel>

        {/* Zoning Intelligence Tab */}
        <TabPanel value={tabValue} index={10}>
          <Box sx={{ px: 2 }}>
            <Stack spacing={3}>
              <Stack spacing={1}>
                <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <LocationCityIcon sx={{ color: '#f59e0b' }} />
                  Zoning & Development Intelligence
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Comprehensive zoning data across 5 categories: Entitled Land Inventory, Future Initiatives, Regulatory Barriers, Transit-Oriented Development, and Master Metrics
                </Typography>
              </Stack>
              <ZoningIntelligence />
            </Stack>
          </Box>
        </TabPanel>
      </Card>

      {/* Data Upload Dialog */}
      <DataUploadDialog
        open={uploadDialogOpen}
        onClose={() => setUploadDialogOpen(false)}
        onUploadSuccess={() => {
          // Refresh USA economics data after successful upload
          loadUSAEconomicsData();
        }}
      />
    </Box>
  );
};
