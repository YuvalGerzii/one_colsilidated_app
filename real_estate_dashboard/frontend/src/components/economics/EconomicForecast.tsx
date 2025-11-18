import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Slider,
  FormControlLabel,
  Switch,
  Paper,
  List,
  ListItem,
  ListItemText,
  Tooltip,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  TrendingUp,
  TrendingDown,
  Timeline,
  Analytics,
  Warning,
  CheckCircle,
  Info,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  Area,
  AreaChart,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';
import api from '../../services/api';

// Types
interface ForecastDataPoint {
  date: string;
  value: number;
  lower_bound: number;
  upper_bound: number;
  is_forecast: boolean;
  trend?: number;
  yearly_seasonality?: number;
}

interface ForecastMetrics {
  mae: number;
  mape: number;
  rmse: number;
  r_squared: number;
  forecast_quality: string;
  forecast_mean: number;
  forecast_min: number;
  forecast_max: number;
  forecast_std: number;
  total_change: number;
  total_change_percent: number;
  avg_confidence_interval_width: number;
}

interface ForecastComponents {
  trend?: Array<{ date: string; value: number }>;
  trend_direction?: string;
  trend_strength?: number;
  yearly_seasonality?: Array<{ date: string; value: number }>;
  seasonality_strength?: number;
  changepoints?: string[];
}

interface ForecastResponse {
  indicator_name: string;
  country: string;
  forecast_start: string;
  forecast_end: string;
  forecast_periods: number;
  historical_periods: number;
  historical_start: string;
  historical_end: string;
  forecast: ForecastDataPoint[];
  components: ForecastComponents;
  metrics: ForecastMetrics;
  parameters: {
    seasonality_mode: string;
    changepoint_prior_scale: number;
    seasonality_prior_scale: number;
    confidence_interval: number;
    include_holidays: boolean;
  };
  timestamp: string;
}

interface Recommendation {
  type: string;
  severity: string;
  message: string;
}

interface RecommendationsResponse {
  recommendations: Recommendation[];
  risk_level: string;
  confidence: string;
  key_insights: {
    trend_direction: string;
    trend_strength_pct: number;
    expected_change_pct: number;
    volatility_cv: number;
    forecast_quality: string;
    mape: number;
  };
}

// Popular indicators
const POPULAR_INDICATORS = [
  { value: 'GDP', label: 'GDP' },
  { value: 'Unemployment Rate', label: 'Unemployment Rate' },
  { value: 'Inflation Rate', label: 'Inflation Rate' },
  { value: 'Interest Rate', label: 'Interest Rate' },
  { value: 'Housing Starts', label: 'Housing Starts' },
  { value: 'Consumer Confidence', label: 'Consumer Confidence' },
  { value: 'Retail Sales', label: 'Retail Sales' },
  { value: 'Industrial Production', label: 'Industrial Production' },
];

const EconomicForecast: React.FC = () => {
  // State
  const [selectedIndicator, setSelectedIndicator] = useState<string>('GDP');
  const [forecastData, setForecastData] = useState<ForecastResponse | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendationsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showConfidenceInterval, setShowConfidenceInterval] = useState(true);
  const [showTrend, setShowTrend] = useState(false);

  // Forecast parameters
  const [forecastPeriods, setForecastPeriods] = useState(365);
  const [historicalDays, setHistoricalDays] = useState(730);
  const [seasonalityMode, setSeasonalityMode] = useState<'additive' | 'multiplicative'>('additive');
  const [includeHolidays, setIncludeHolidays] = useState(false);
  const [confidenceInterval, setConfidenceInterval] = useState(0.95);

  // Load forecast on component mount or when indicator changes
  useEffect(() => {
    if (selectedIndicator) {
      loadForecast();
    }
  }, [selectedIndicator]);

  const loadForecast = async () => {
    setLoading(true);
    setError(null);

    try {
      // Generate forecast
      const response = await api.post(
        `/market-intelligence/data/usa-economics/forecast/${encodeURIComponent(selectedIndicator)}`,
        {
          forecast_periods: forecastPeriods,
          historical_days: historicalDays,
          seasonality_mode: seasonalityMode,
          include_holidays: includeHolidays,
          confidence_interval: confidenceInterval,
        }
      );

      setForecastData(response.data);

      // Get recommendations
      try {
        const recResponse = await api.post(
          `/market-intelligence/data/usa-economics/forecast/${encodeURIComponent(selectedIndicator)}/recommendations`,
          {
            forecast_periods: forecastPeriods,
            historical_days: historicalDays,
            seasonality_mode: seasonalityMode,
            include_holidays: includeHolidays,
            confidence_interval: confidenceInterval,
          }
        );
        setRecommendations(recResponse.data);
      } catch (recErr) {
        console.warn('Failed to load recommendations:', recErr);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load forecast');
      console.error('Error loading forecast:', err);
    } finally {
      setLoading(false);
    }
  };

  // Format chart data
  const getChartData = () => {
    if (!forecastData) return [];

    return forecastData.forecast.map((point) => ({
      date: new Date(point.date).toLocaleDateString('en-US', {
        month: 'short',
        year: 'numeric',
      }),
      fullDate: point.date,
      value: point.value,
      lower: point.lower_bound,
      upper: point.upper_bound,
      isForecast: point.is_forecast,
      trend: point.trend,
    }));
  };

  // Get quality color
  const getQualityColor = (quality: string) => {
    switch (quality) {
      case 'excellent':
        return 'success';
      case 'good':
        return 'info';
      case 'fair':
        return 'warning';
      case 'poor':
        return 'error';
      default:
        return 'default';
    }
  };

  // Get risk level color
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low':
        return 'success';
      case 'medium':
        return 'warning';
      case 'high':
        return 'error';
      default:
        return 'default';
    }
  };

  // Get severity icon
  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return <Warning color="error" />;
      case 'medium':
        return <Info color="warning" />;
      default:
        return <CheckCircle color="success" />;
    }
  };

  // Format number
  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US', {
      maximumFractionDigits: 2,
    }).format(num);
  };

  const chartData = getChartData();
  const splitIndex = chartData.findIndex((d) => d.isForecast);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Timeline /> Economic Indicator Forecasting
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        AI-powered forecasting using Facebook Prophet for trend analysis and future predictions
      </Typography>

      {/* Indicator Selection */}
      <Card sx={{ mt: 3, mb: 3 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Economic Indicator</InputLabel>
                <Select
                  value={selectedIndicator}
                  onChange={(e) => setSelectedIndicator(e.target.value)}
                  label="Economic Indicator"
                >
                  {POPULAR_INDICATORS.map((indicator) => (
                    <MenuItem key={indicator.value} value={indicator.value}>
                      {indicator.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={8}>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {POPULAR_INDICATORS.map((indicator) => (
                  <Chip
                    key={indicator.value}
                    label={indicator.label}
                    onClick={() => setSelectedIndicator(indicator.value)}
                    color={selectedIndicator === indicator.value ? 'primary' : 'default'}
                    variant={selectedIndicator === indicator.value ? 'filled' : 'outlined'}
                  />
                ))}
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Advanced Parameters */}
      <Accordion sx={{ mb: 3 }}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography variant="h6">Forecast Parameters</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography gutterBottom>
                Forecast Horizon: {forecastPeriods} days ({Math.round(forecastPeriods / 30)} months)
              </Typography>
              <Slider
                value={forecastPeriods}
                onChange={(_, value) => setForecastPeriods(value as number)}
                min={30}
                max={1825}
                step={30}
                marks={[
                  { value: 30, label: '1mo' },
                  { value: 365, label: '1yr' },
                  { value: 730, label: '2yr' },
                  { value: 1825, label: '5yr' },
                ]}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography gutterBottom>
                Historical Data: {historicalDays} days ({Math.round(historicalDays / 365)} years)
              </Typography>
              <Slider
                value={historicalDays}
                onChange={(_, value) => setHistoricalDays(value as number)}
                min={365}
                max={3650}
                step={365}
                marks={[
                  { value: 365, label: '1yr' },
                  { value: 730, label: '2yr' },
                  { value: 1825, label: '5yr' },
                  { value: 3650, label: '10yr' },
                ]}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Seasonality Mode</InputLabel>
                <Select
                  value={seasonalityMode}
                  onChange={(e) => setSeasonalityMode(e.target.value as 'additive' | 'multiplicative')}
                  label="Seasonality Mode"
                >
                  <MenuItem value="additive">Additive</MenuItem>
                  <MenuItem value="multiplicative">Multiplicative</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography gutterBottom>Confidence Interval: {(confidenceInterval * 100).toFixed(0)}%</Typography>
              <Slider
                value={confidenceInterval}
                onChange={(_, value) => setConfidenceInterval(value as number)}
                min={0.8}
                max={0.99}
                step={0.01}
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <FormControlLabel
                control={
                  <Switch checked={includeHolidays} onChange={(e) => setIncludeHolidays(e.target.checked)} />
                }
                label="Include US Holidays"
              />
            </Grid>
            <Grid item xs={12}>
              <Button variant="contained" onClick={loadForecast} disabled={loading} fullWidth>
                Generate Forecast
              </Button>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Loading State */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Forecast Results */}
      {forecastData && !loading && (
        <>
          {/* Key Metrics */}
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" variant="body2">
                    Forecast Quality
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    <Chip
                      label={forecastData.metrics.forecast_quality.toUpperCase()}
                      color={getQualityColor(forecastData.metrics.forecast_quality) as any}
                      size="small"
                    />
                    <Typography variant="caption">MAPE: {forecastData.metrics.mape.toFixed(2)}%</Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" variant="body2">
                    Expected Change
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 1 }}>
                    {forecastData.metrics.total_change_percent > 0 ? (
                      <TrendingUp color="success" />
                    ) : (
                      <TrendingDown color="error" />
                    )}
                    <Typography variant="h6">
                      {forecastData.metrics.total_change_percent > 0 ? '+' : ''}
                      {forecastData.metrics.total_change_percent.toFixed(2)}%
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" variant="body2">
                    Forecast Range
                  </Typography>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    {formatNumber(forecastData.metrics.forecast_min)} - {formatNumber(forecastData.metrics.forecast_max)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" variant="body2">
                    R-Squared
                  </Typography>
                  <Typography variant="h6" sx={{ mt: 1 }}>
                    {forecastData.metrics.r_squared.toFixed(4)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Main Forecast Chart */}
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">Forecast: {forecastData.indicator_name}</Typography>
                <Box>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={showConfidenceInterval}
                        onChange={(e) => setShowConfidenceInterval(e.target.checked)}
                        size="small"
                      />
                    }
                    label="Confidence Interval"
                  />
                  <FormControlLabel
                    control={
                      <Switch checked={showTrend} onChange={(e) => setShowTrend(e.target.checked)} size="small" />
                    }
                    label="Show Trend"
                  />
                </Box>
              </Box>

              <ResponsiveContainer width="100%" height={450}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2196f3" stopOpacity={0.1} />
                      <stop offset="95%" stopColor="#2196f3" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="date"
                    tick={{ fontSize: 12 }}
                    interval={Math.floor(chartData.length / 10)}
                  />
                  <YAxis tick={{ fontSize: 12 }} />
                  <RechartsTooltip
                    formatter={(value: any) => formatNumber(value)}
                    labelFormatter={(label) => `Date: ${label}`}
                  />
                  <Legend />

                  {/* Confidence Interval */}
                  {showConfidenceInterval && (
                    <>
                      <Area
                        type="monotone"
                        dataKey="upper"
                        stroke="none"
                        fill="#2196f3"
                        fillOpacity={0.1}
                        name="Upper Bound"
                      />
                      <Area
                        type="monotone"
                        dataKey="lower"
                        stroke="none"
                        fill="#2196f3"
                        fillOpacity={0.1}
                        name="Lower Bound"
                      />
                    </>
                  )}

                  {/* Main forecast line */}
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#2196f3"
                    strokeWidth={2}
                    fill="url(#colorForecast)"
                    name="Forecast"
                  />

                  {/* Trend line */}
                  {showTrend && (
                    <Line
                      type="monotone"
                      dataKey="trend"
                      stroke="#ff9800"
                      strokeWidth={2}
                      dot={false}
                      name="Trend"
                      strokeDasharray="5 5"
                    />
                  )}

                  {/* Vertical line at forecast start */}
                  {splitIndex > 0 && (
                    <ReferenceLine
                      x={chartData[splitIndex].date}
                      stroke="#666"
                      strokeDasharray="3 3"
                      label="Forecast Start"
                    />
                  )}
                </AreaChart>
              </ResponsiveContainer>

              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                Historical Period: {new Date(forecastData.historical_start).toLocaleDateString()} -{' '}
                {new Date(forecastData.historical_end).toLocaleDateString()} | Forecast Period:{' '}
                {new Date(forecastData.forecast_start).toLocaleDateString()} -{' '}
                {new Date(forecastData.forecast_end).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>

          {/* Recommendations */}
          {recommendations && (
            <Grid container spacing={2} sx={{ mb: 3 }}>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Risk Assessment
                    </Typography>
                    <Chip
                      label={recommendations.risk_level.toUpperCase()}
                      color={getRiskColor(recommendations.risk_level) as any}
                      sx={{ mb: 2 }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      Trend: {recommendations.key_insights.trend_direction} (
                      {recommendations.key_insights.trend_strength_pct.toFixed(2)}%)
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Volatility: {recommendations.key_insights.volatility_cv.toFixed(2)}%
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>

              <Grid item xs={12} md={8}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Recommendations
                    </Typography>
                    <List dense>
                      {recommendations.recommendations.map((rec, idx) => (
                        <ListItem key={idx}>
                          <Box sx={{ mr: 1 }}>{getSeverityIcon(rec.severity)}</Box>
                          <ListItemText
                            primary={rec.message}
                            secondary={`Type: ${rec.type} | Severity: ${rec.severity}`}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}

          {/* Model Details */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6">Model Details & Metrics</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Quality Metrics
                  </Typography>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="body2">MAE: {forecastData.metrics.mae.toFixed(4)}</Typography>
                    <Typography variant="body2">MAPE: {forecastData.metrics.mape.toFixed(2)}%</Typography>
                    <Typography variant="body2">RMSE: {forecastData.metrics.rmse.toFixed(4)}</Typography>
                    <Typography variant="body2">R²: {forecastData.metrics.r_squared.toFixed(4)}</Typography>
                    <Typography variant="body2">
                      Avg CI Width: {forecastData.metrics.avg_confidence_interval_width.toFixed(4)}
                    </Typography>
                  </Paper>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Model Parameters
                  </Typography>
                  <Paper sx={{ p: 2 }}>
                    <Typography variant="body2">
                      Seasonality: {forecastData.parameters.seasonality_mode}
                    </Typography>
                    <Typography variant="body2">
                      Confidence Interval: {(forecastData.parameters.confidence_interval * 100).toFixed(0)}%
                    </Typography>
                    <Typography variant="body2">
                      Holidays: {forecastData.parameters.include_holidays ? 'Yes' : 'No'}
                    </Typography>
                    <Typography variant="body2">
                      Changepoint Prior: {forecastData.parameters.changepoint_prior_scale}
                    </Typography>
                  </Paper>
                </Grid>

                {forecastData.components.changepoints && forecastData.components.changepoints.length > 0 && (
                  <Grid item xs={12}>
                    <Typography variant="subtitle2" gutterBottom>
                      Recent Trend Changepoints
                    </Typography>
                    <Paper sx={{ p: 2 }}>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        {forecastData.components.changepoints.map((cp, idx) => (
                          <Chip
                            key={idx}
                            label={new Date(cp).toLocaleDateString()}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                      </Box>
                    </Paper>
                  </Grid>
                )}
              </Grid>
            </AccordionDetails>
          </Accordion>
        </>
      )}
    </Box>
  );
};

export default EconomicForecast;
