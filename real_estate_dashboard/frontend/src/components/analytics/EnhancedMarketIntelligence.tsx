import React, { useState, useEffect, useMemo } from 'react';
import {
  Box,
  Grid,
  Typography,
  Tabs,
  Tab,
  Button,
  Chip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  CircularProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  LocationCity,
  Assessment,
  CompareArrows,
  Refresh,
  Download,
  Timeline,
  ShowChart,
  PieChart,
  BarChart as BarChartIcon,
  Lightbulb,
  Warning,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Cell,
} from 'recharts';
import { GlassCard, GlassMetricCard, MicroInteraction, GradientGlassCard } from '../ui/GlassComponents';
import AlertsPanel from '../alerts/AlertsPanel';

interface MarketData {
  date: string;
  medianPrice: number;
  medianRent: number;
  inventoryLevel: number;
  daysOnMarket: number;
  pricePerSqFt: number;
  rentYield: number;
  vacancyRate: number;
  capRate: number;
}

interface MarketInsight {
  id: string;
  type: 'opportunity' | 'risk' | 'trend' | 'forecast';
  title: string;
  description: string;
  confidence: number;
  impact: 'high' | 'medium' | 'low';
  actionItems: string[];
}

interface CompetitorData {
  name: string;
  occupancy: number;
  avgRent: number;
  amenityScore: number;
  reputation: number;
  capRate: number;
}

const EnhancedMarketIntelligence: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [selectedMarket, setSelectedMarket] = useState('national');
  const [selectedMetro, setSelectedMetro] = useState('all');
  const [loading, setLoading] = useState(false);
  const [timeRange, setTimeRange] = useState('12m');

  // Sample market data - replace with API calls
  const marketData: MarketData[] = useMemo(() => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return months.map((month, idx) => ({
      date: month,
      medianPrice: 350000 + Math.random() * 50000 + (idx * 5000),
      medianRent: 1800 + Math.random() * 200 + (idx * 20),
      inventoryLevel: 15000 - (idx * 500) + Math.random() * 1000,
      daysOnMarket: 45 - (idx * 2) + Math.random() * 10,
      pricePerSqFt: 250 + Math.random() * 30 + (idx * 3),
      rentYield: 0.048 + Math.random() * 0.01,
      vacancyRate: 0.065 - (idx * 0.002) + Math.random() * 0.01,
      capRate: 0.055 + Math.random() * 0.01,
    }));
  }, []);

  const marketInsights: MarketInsight[] = [
    {
      id: '1',
      type: 'opportunity',
      title: 'Emerging Market: Austin Tech Corridor',
      description: 'Tech job growth of 18% YoY is driving strong rental demand. Population growth 3x national average.',
      confidence: 0.87,
      impact: 'high',
      actionItems: [
        'Research Class A multifamily assets near tech hubs',
        'Analyze rent growth projections for next 24 months',
        'Connect with local property managers for market intel',
        'Model pro forma for potential acquisitions'
      ]
    },
    {
      id: '2',
      type: 'risk',
      title: 'Supply Surge Warning: Downtown Seattle',
      description: '4,200 new units coming online Q3-Q4. Potential rent compression of 5-8%.',
      confidence: 0.92,
      impact: 'high',
      actionItems: [
        'Review lease renewal strategies for Seattle properties',
        'Consider offering concessions to retain tenants',
        'Analyze competitive positioning vs new construction',
        'Prepare marketing campaigns for differentiation'
      ]
    },
    {
      id: '3',
      type: 'trend',
      title: 'Cap Rate Compression Continues',
      description: 'Cap rates compressed 25bps QoQ across all asset classes. Strong investor appetite.',
      confidence: 0.81,
      impact: 'medium',
      actionItems: [
        'Evaluate portfolio for disposition opportunities',
        'Update asset valuations using current cap rates',
        'Consider refinancing to capture increased values',
        'Model IRR scenarios for potential exits'
      ]
    },
    {
      id: '4',
      type: 'forecast',
      title: 'Rent Growth Forecast: Sunbelt Markets',
      description: 'ML models predict 6-9% rent growth in Phoenix, Tampa, Charlotte over next 12 months.',
      confidence: 0.76,
      impact: 'high',
      actionItems: [
        'Prioritize Sunbelt markets for new acquisitions',
        'Analyze rent comps in target submarkets',
        'Build relationships with brokers in these markets',
        'Prepare capital for opportunistic deals'
      ]
    },
    {
      id: '5',
      type: 'opportunity',
      title: 'Value-Add Play: Suburban Office Conversions',
      description: 'Suburban office occupancy at 62%. Conversion to multifamily viable with 18-22% IRR.',
      confidence: 0.69,
      impact: 'medium',
      actionItems: [
        'Identify underperforming office assets in target markets',
        'Engage architects for conversion feasibility studies',
        'Model construction costs and timeline',
        'Research zoning requirements for conversions'
      ]
    }
  ];

  const competitorData: CompetitorData[] = [
    { name: 'Property A', occupancy: 95, avgRent: 2100, amenityScore: 8.5, reputation: 4.6, capRate: 5.2 },
    { name: 'Property B', occupancy: 88, avgRent: 1950, amenityScore: 7.2, reputation: 4.2, capRate: 5.8 },
    { name: 'Property C', occupancy: 92, avgRent: 2250, amenityScore: 9.1, reputation: 4.8, capRate: 4.9 },
    { name: 'Your Portfolio', occupancy: 91, avgRent: 2050, amenityScore: 7.8, reputation: 4.4, capRate: 5.5 },
    { name: 'Property D', occupancy: 85, avgRent: 1850, amenityScore: 6.9, reputation: 4.0, capRate: 6.1 },
  ];

  const economicIndicators = [
    { indicator: 'GDP Growth', value: 2.4, change: 0.3, trend: 'up' },
    { indicator: 'Unemployment', value: 3.8, change: -0.2, trend: 'down' },
    { indicator: '10Y Treasury', value: 4.25, change: 0.15, trend: 'up' },
    { indicator: 'Inflation (CPI)', value: 3.2, change: -0.4, trend: 'down' },
    { indicator: 'Housing Starts', value: 1450, change: 85, trend: 'up' },
    { indicator: 'Consumer Confidence', value: 108, change: 5, trend: 'up' },
  ];

  const marketComparison = [
    { market: 'National', rentGrowth: 4.2, priceGrowth: 5.8, capRate: 5.5, vacancyRate: 6.5 },
    { market: 'Austin', rentGrowth: 8.5, priceGrowth: 12.3, capRate: 4.8, vacancyRate: 5.2 },
    { market: 'Phoenix', rentGrowth: 7.2, priceGrowth: 10.1, capRate: 5.1, vacancyRate: 5.8 },
    { market: 'Seattle', rentGrowth: 3.1, priceGrowth: 4.2, capRate: 4.5, vacancyRate: 7.8 },
    { market: 'Tampa', rentGrowth: 6.8, priceGrowth: 9.5, capRate: 5.3, vacancyRate: 5.5 },
    { market: 'Denver', rentGrowth: 5.5, priceGrowth: 7.8, capRate: 5.0, vacancyRate: 6.1 },
  ];

  const refreshData = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const getInsightIcon = (type: string) => {
    switch (type) {
      case 'opportunity': return <Lightbulb sx={{ color: 'success.main' }} />;
      case 'risk': return <Warning sx={{ color: 'error.main' }} />;
      case 'trend': return <Timeline sx={{ color: 'info.main' }} />;
      case 'forecast': return <ShowChart sx={{ color: 'primary.main' }} />;
      default: return <Assessment />;
    }
  };

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'opportunity': return 'success';
      case 'risk': return 'error';
      case 'trend': return 'info';
      case 'forecast': return 'primary';
      default: return 'default';
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
    return `${value.toFixed(1)}%`;
  };

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Assessment sx={{ fontSize: 40 }} />
            Market Intelligence Hub
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            AI-powered insights, competitive analysis, and market forecasting
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Time Range</InputLabel>
            <Select value={timeRange} onChange={(e) => setTimeRange(e.target.value)} label="Time Range">
              <MenuItem value="3m">Last 3 Months</MenuItem>
              <MenuItem value="6m">Last 6 Months</MenuItem>
              <MenuItem value="12m">Last 12 Months</MenuItem>
              <MenuItem value="24m">Last 24 Months</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Metro</InputLabel>
            <Select value={selectedMetro} onChange={(e) => setSelectedMetro(e.target.value)} label="Metro">
              <MenuItem value="all">All Markets</MenuItem>
              <MenuItem value="austin">Austin</MenuItem>
              <MenuItem value="phoenix">Phoenix</MenuItem>
              <MenuItem value="seattle">Seattle</MenuItem>
              <MenuItem value="tampa">Tampa</MenuItem>
              <MenuItem value="denver">Denver</MenuItem>
            </Select>
          </FormControl>
          <Tooltip title="Refresh data">
            <IconButton onClick={refreshData} disabled={loading}>
              {loading ? <CircularProgress size={24} /> : <Refresh />}
            </IconButton>
          </Tooltip>
          <Button variant="contained" startIcon={<Download />}>
            Export Report
          </Button>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MicroInteraction variant="lift">
            <GlassMetricCard>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">Median Home Price</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                    {formatCurrency(marketData[marketData.length - 1]?.medianPrice || 0)}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
                    <Typography variant="body2" sx={{ color: 'success.main', fontWeight: 600 }}>
                      +5.8% YoY
                    </Typography>
                  </Box>
                </Box>
                <LocationCity sx={{ fontSize: 40, opacity: 0.3, color: 'primary.main' }} />
              </Box>
            </GlassMetricCard>
          </MicroInteraction>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MicroInteraction variant="lift">
            <GlassMetricCard>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">Median Rent</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                    {formatCurrency(marketData[marketData.length - 1]?.medianRent || 0)}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingUp sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
                    <Typography variant="body2" sx={{ color: 'success.main', fontWeight: 600 }}>
                      +4.2% YoY
                    </Typography>
                  </Box>
                </Box>
                <Assessment sx={{ fontSize: 40, opacity: 0.3, color: 'success.main' }} />
              </Box>
            </GlassMetricCard>
          </MicroInteraction>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MicroInteraction variant="lift">
            <GlassMetricCard>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">Days on Market</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                    {Math.round(marketData[marketData.length - 1]?.daysOnMarket || 0)}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingDown sx={{ fontSize: 16, color: 'success.main', mr: 0.5 }} />
                    <Typography variant="body2" sx={{ color: 'success.main', fontWeight: 600 }}>
                      -12% vs avg
                    </Typography>
                  </Box>
                </Box>
                <Timeline sx={{ fontSize: 40, opacity: 0.3, color: 'info.main' }} />
              </Box>
            </GlassMetricCard>
          </MicroInteraction>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MicroInteraction variant="lift">
            <GlassMetricCard>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <Box>
                  <Typography variant="caption" color="text.secondary">Average Cap Rate</Typography>
                  <Typography variant="h4" sx={{ fontWeight: 700, mt: 1 }}>
                    {formatPercent((marketData[marketData.length - 1]?.capRate || 0) * 100)}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <TrendingDown sx={{ fontSize: 16, color: 'warning.main', mr: 0.5 }} />
                    <Typography variant="body2" sx={{ color: 'warning.main', fontWeight: 600 }}>
                      -25 bps
                    </Typography>
                  </Box>
                </Box>
                <CompareArrows sx={{ fontSize: 40, opacity: 0.3, color: 'secondary.main' }} />
              </Box>
            </GlassMetricCard>
          </MicroInteraction>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 3 }}>
        <Tab label="Market Trends" icon={<Timeline />} iconPosition="start" />
        <Tab label="AI Insights" icon={<Lightbulb />} iconPosition="start" />
        <Tab label="Competitive Analysis" icon={<CompareArrows />} iconPosition="start" />
        <Tab label="Economic Indicators" icon={<BarChartIcon />} iconPosition="start" />
        <Tab label="Smart Alerts" icon={<Warning />} iconPosition="start" />
      </Tabs>

      {/* Tab Content */}
      {activeTab === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Price & Rent Trends (12 Months)
              </Typography>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={marketData}>
                  <defs>
                    <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorRent" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip
                    formatter={(value: number, name: string) => {
                      if (name === 'Median Price') return formatCurrency(value);
                      if (name === 'Median Rent') return formatCurrency(value);
                      return value;
                    }}
                  />
                  <Legend />
                  <Area
                    yAxisId="left"
                    type="monotone"
                    dataKey="medianPrice"
                    stroke="#3b82f6"
                    fillOpacity={1}
                    fill="url(#colorPrice)"
                    name="Median Price"
                  />
                  <Area
                    yAxisId="right"
                    type="monotone"
                    dataKey="medianRent"
                    stroke="#10b981"
                    fillOpacity={1}
                    fill="url(#colorRent)"
                    name="Median Rent"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>

          <Grid item xs={12} lg={4}>
            <GlassCard sx={{ p: 3, height: '100%' }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Market Comparison
              </Typography>
              <List>
                {marketComparison.slice(0, 6).map((market, idx) => (
                  <ListItem key={idx} sx={{ px: 0 }}>
                    <ListItemText
                      primary={market.market}
                      secondary={
                        <Box sx={{ mt: 1 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                            <Typography variant="caption">Rent Growth:</Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600, color: 'success.main' }}>
                              {formatPercent(market.rentGrowth)}
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                            <Typography variant="caption">Cap Rate:</Typography>
                            <Typography variant="caption" sx={{ fontWeight: 600 }}>
                              {formatPercent(market.capRate)}
                            </Typography>
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Inventory & Days on Market
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={marketData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="inventoryLevel"
                    stroke="#8b5cf6"
                    strokeWidth={2}
                    name="Inventory"
                    dot={{ r: 4 }}
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="daysOnMarket"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    name="Days on Market"
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Cap Rate & Vacancy Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={marketData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <RechartsTooltip formatter={(value: number) => formatPercent((value as number) * 100)} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="capRate"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    name="Cap Rate"
                    dot={{ r: 4 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="vacancyRate"
                    stroke="#ef4444"
                    strokeWidth={2}
                    name="Vacancy Rate"
                    dot={{ r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>
        </Grid>
      )}

      {activeTab === 1 && (
        <Grid container spacing={3}>
          {marketInsights.map((insight) => (
            <Grid item xs={12} md={6} key={insight.id}>
              <MicroInteraction variant="lift">
                <GradientGlassCard sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <Box>{getInsightIcon(insight.type)}</Box>
                    <Box sx={{ flex: 1 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1, flexWrap: 'wrap' }}>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          {insight.title}
                        </Typography>
                        <Chip
                          label={insight.type}
                          size="small"
                          color={getInsightColor(insight.type) as any}
                          variant="outlined"
                        />
                        <Chip
                          label={`${Math.round(insight.confidence * 100)}% confidence`}
                          size="small"
                          variant="filled"
                          sx={{ ml: 'auto' }}
                        />
                      </Box>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        {insight.description}
                      </Typography>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                        Recommended Actions:
                      </Typography>
                      <List dense>
                        {insight.actionItems.map((action, idx) => (
                          <ListItem key={idx} sx={{ py: 0.5, px: 0 }}>
                            <ListItemText
                              primary={`${idx + 1}. ${action}`}
                              primaryTypographyProps={{ variant: 'body2' }}
                            />
                          </ListItem>
                        ))}
                      </List>
                      <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                        <Button variant="contained" size="small">
                          Explore Opportunity
                        </Button>
                        <Button variant="outlined" size="small">
                          Save for Later
                        </Button>
                      </Box>
                    </Box>
                  </Box>
                </GradientGlassCard>
              </MicroInteraction>
            </Grid>
          ))}

          <Grid item xs={12}>
            <Alert severity="info" icon={<Lightbulb />}>
              <Typography variant="body2">
                <strong>AI-Powered Insights:</strong> These insights are generated using machine learning models trained on historical market data,
                economic indicators, and real-time transaction data. Confidence scores indicate model certainty.
              </Typography>
            </Alert>
          </Grid>
        </Grid>
      )}

      {activeTab === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Competitive Positioning Analysis
              </Typography>
              <ResponsiveContainer width="100%" height={400}>
                <RadarChart data={competitorData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="name" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name="Occupancy"
                    dataKey="occupancy"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                  />
                  <Radar
                    name="Amenity Score"
                    dataKey="amenityScore"
                    stroke="#10b981"
                    fill="#10b981"
                    fillOpacity={0.3}
                  />
                  <Legend />
                </RadarChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Average Rent Comparison
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={competitorData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip formatter={(value: number) => formatCurrency(value)} />
                  <Bar dataKey="avgRent" name="Average Rent">
                    {competitorData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.name === 'Your Portfolio' ? '#3b82f6' : COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Occupancy vs Cap Rate
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="occupancy" name="Occupancy" unit="%" />
                  <YAxis dataKey="capRate" name="Cap Rate" unit="%" />
                  <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter name="Properties" data={competitorData} fill="#8b5cf6">
                    {competitorData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.name === 'Your Portfolio' ? '#3b82f6' : COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </GlassCard>
          </Grid>
        </Grid>
      )}

      {activeTab === 3 && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <GlassCard sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                Key Economic Indicators
              </Typography>
              <Grid container spacing={3} sx={{ mt: 1 }}>
                {economicIndicators.map((indicator, idx) => (
                  <Grid item xs={12} sm={6} md={4} key={idx}>
                    <MicroInteraction variant="scale">
                      <Box sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                        <Typography variant="caption" color="text.secondary">
                          {indicator.indicator}
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                          <Typography variant="h5" sx={{ fontWeight: 700 }}>
                            {indicator.indicator.includes('Housing')
                              ? `${indicator.value}K`
                              : indicator.indicator.includes('Confidence')
                              ? indicator.value
                              : `${indicator.value}%`}
                          </Typography>
                          {indicator.trend === 'up' ? (
                            <TrendingUp sx={{ color: 'success.main' }} />
                          ) : (
                            <TrendingDown sx={{ color: indicator.indicator === 'Unemployment' || indicator.indicator === 'Inflation (CPI)' ? 'success.main' : 'error.main' }} />
                          )}
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                          {indicator.change > 0 ? '+' : ''}{indicator.change}
                          {indicator.indicator.includes('Housing') ? 'K' : indicator.indicator.includes('Confidence') ? '' : '%'} vs prior
                        </Typography>
                      </Box>
                    </MicroInteraction>
                  </Grid>
                ))}
              </Grid>
            </GlassCard>
          </Grid>

          <Grid item xs={12}>
            <Alert severity="info">
              <Typography variant="body2">
                <strong>Economic Context:</strong> Current macroeconomic conditions suggest a moderately favorable environment for real estate investment.
                Strong employment, stabilizing inflation, and robust consumer confidence support rental demand, though rising interest rates may compress cap rates further.
              </Typography>
            </Alert>
          </Grid>
        </Grid>
      )}

      {activeTab === 4 && (
        <Box>
          <AlertsPanel />
        </Box>
      )}
    </Box>
  );
};

export default EnhancedMarketIntelligence;
