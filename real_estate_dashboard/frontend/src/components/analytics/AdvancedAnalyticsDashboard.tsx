import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  TextField,
  Button,
  Tabs,
  Tab,
  Card,
  CardContent,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress,
  Slider,
  Tooltip,
  IconButton,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Psychology,
  AutoGraph,
  Warning,
  Lightbulb,
  Refresh,
  Download,
  ShowChart,
  Assessment,
  Speed,
  TimerOutlined,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
  Cell,
  ReferenceLine,
} from 'recharts';
import { GlassCard, GlassMetricCard, GlassButton, MicroInteraction, GradientGlassCard } from '../ui/GlassComponents';
import axios from 'axios';

interface PredictionData {
  price_prediction: {
    predicted_value: number;
    confidence_interval_lower: number;
    confidence_interval_upper: number;
    confidence_score: number;
    model_used: string;
    features_importance: { [key: string]: number };
  };
  rent_forecast: {
    next_12_months: number[];
    trend: string;
    confidence: string;
  };
  risk_score: {
    predicted_value: number;
    confidence_score: number;
  };
  opportunity_score: {
    predicted_value: number;
    confidence_score: number;
  };
  recommendation: string;
}

const AdvancedAnalyticsDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<PredictionData | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Property input state
  const [propertyInputs, setPropertyInputs] = useState({
    square_feet: 2000,
    bedrooms: 3,
    bathrooms: 2.5,
    year_built: 2015,
    lot_size: 5000,
    location_score: 75,
    school_rating: 8.5,
    walkability_score: 65,
    current_price: 450000,
  });

  useEffect(() => {
    loadDemoPredictions();
  }, []);

  const loadDemoPredictions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8001/api/v1/predictive-analytics/demo-prediction');
      setPredictions(response.data);
    } catch (err: any) {
      setError(err.message || 'Failed to load predictions');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score: number) => {
    if (score < 30) return '#10b981'; // Low risk - green
    if (score < 60) return '#f59e0b'; // Medium risk - amber
    return '#ef4444'; // High risk - red
  };

  const getOpportunityColor = (score: number) => {
    if (score > 70) return '#10b981'; // High opportunity - green
    if (score > 40) return '#f59e0b'; // Medium opportunity - amber
    return '#ef4444'; // Low opportunity - red
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
    return `${(value * 100).toFixed(1)}%`;
  };

  // Prepare rent forecast chart data
  const rentForecastData = predictions ? predictions.rent_forecast.next_12_months.map((rent, idx) => ({
    month: `Month ${idx + 1}`,
    rent,
    monthNum: idx + 1,
  })) : [];

  // Prepare feature importance chart data
  const featureImportanceData = predictions ? Object.entries(predictions.price_prediction.features_importance).map(([name, value]) => ({
    feature: name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    importance: value * 100,
  })).sort((a, b) => b.importance - a.importance) : [];

  // Risk breakdown data (for radar chart)
  const riskBreakdown = [
    { category: 'Market Risk', value: 35, fullMark: 100 },
    { category: 'Property Condition', value: 20, fullMark: 100 },
    { category: 'Financial Metrics', value: 25, fullMark: 100 },
    { category: 'Location Risk', value: 15, fullMark: 100 },
    { category: 'Economic Risk', value: 30, fullMark: 100 },
  ];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Psychology sx={{ fontSize: 40, color: 'primary.main' }} />
            Advanced Analytics Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            ML-powered predictions, forecasting, and investment intelligence
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Tooltip title="Refresh predictions">
            <IconButton onClick={loadDemoPredictions} disabled={loading}>
              {loading ? <CircularProgress size={24} /> : <Refresh />}
            </IconButton>
          </Tooltip>
          <Button variant="contained" startIcon={<Download />}>
            Export Report
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Key Metrics Overview */}
      {predictions && (
        <>
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <MicroInteraction variant="lift">
                <GlassMetricCard>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Predicted Price</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mt: 1, color: 'primary.main' }}>
                        {formatCurrency(predictions.price_prediction.predicted_value)}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                        Confidence: {formatPercent(predictions.price_prediction.confidence_score)}
                      </Typography>
                    </Box>
                    <ShowChart sx={{ fontSize: 40, opacity: 0.3, color: 'primary.main' }} />
                  </Box>
                </GlassMetricCard>
              </MicroInteraction>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <MicroInteraction variant="lift">
                <GlassMetricCard>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Rent Forecast (12M)</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mt: 1, color: 'success.main' }}>
                        {predictions.rent_forecast.trend === 'increasing' ? <TrendingUp sx={{ verticalAlign: 'middle' }} /> : <TrendingDown sx={{ verticalAlign: 'middle' }} />}
                        {predictions.rent_forecast.trend}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                        Confidence: {predictions.rent_forecast.confidence}
                      </Typography>
                    </Box>
                    <AutoGraph sx={{ fontSize: 40, opacity: 0.3, color: 'success.main' }} />
                  </Box>
                </GlassMetricCard>
              </MicroInteraction>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <MicroInteraction variant="lift">
                <GlassMetricCard>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ width: '100%' }}>
                      <Typography variant="caption" color="text.secondary">Risk Score</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mt: 1, color: getRiskColor(predictions.risk_score.predicted_value) }}>
                        {predictions.risk_score.predicted_value.toFixed(1)}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={predictions.risk_score.predicted_value}
                        sx={{
                          mt: 1,
                          height: 8,
                          borderRadius: 4,
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getRiskColor(predictions.risk_score.predicted_value)
                          }
                        }}
                      />
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                        {predictions.risk_score.predicted_value < 30 ? 'Low Risk' : predictions.risk_score.predicted_value < 60 ? 'Medium Risk' : 'High Risk'}
                      </Typography>
                    </Box>
                  </Box>
                </GlassMetricCard>
              </MicroInteraction>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <MicroInteraction variant="lift">
                <GlassMetricCard>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Box sx={{ width: '100%' }}>
                      <Typography variant="caption" color="text.secondary">Opportunity Score</Typography>
                      <Typography variant="h4" sx={{ fontWeight: 700, mt: 1, color: getOpportunityColor(predictions.opportunity_score.predicted_value) }}>
                        {predictions.opportunity_score.predicted_value.toFixed(1)}
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={predictions.opportunity_score.predicted_value}
                        sx={{
                          mt: 1,
                          height: 8,
                          borderRadius: 4,
                          '& .MuiLinearProgress-bar': {
                            backgroundColor: getOpportunityColor(predictions.opportunity_score.predicted_value)
                          }
                        }}
                      />
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                        {predictions.opportunity_score.predicted_value > 70 ? 'High Opportunity' : predictions.opportunity_score.predicted_value > 40 ? 'Medium Opportunity' : 'Low Opportunity'}
                      </Typography>
                    </Box>
                  </Box>
                </GlassMetricCard>
              </MicroInteraction>
            </Grid>
          </Grid>

          {/* Recommendation Alert */}
          <Alert
            severity={predictions.recommendation.includes('Strong Buy') ? 'success' : predictions.recommendation.includes('Hold') ? 'info' : 'warning'}
            icon={predictions.recommendation.includes('Strong Buy') ? <Lightbulb /> : <Assessment />}
            sx={{ mb: 4 }}
          >
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              AI Recommendation: {predictions.recommendation}
            </Typography>
          </Alert>

          {/* Tabs */}
          <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)} sx={{ mb: 3 }}>
            <Tab label="Price Prediction" icon={<ShowChart />} iconPosition="start" />
            <Tab label="Rent Forecast" icon={<AutoGraph />} iconPosition="start" />
            <Tab label="Risk Analysis" icon={<Warning />} iconPosition="start" />
            <Tab label="ML Insights" icon={<Psychology />} iconPosition="start" />
          </Tabs>

          {/* Tab Content */}
          {activeTab === 0 && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={8}>
                <GlassCard sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    Price Prediction with Confidence Interval
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    Model: {predictions.price_prediction.model_used}
                  </Typography>

                  <ResponsiveContainer width="100%" height={350}>
                    <ComposedChart
                      data={[
                        {
                          name: 'Predicted Price',
                          lower: predictions.price_prediction.confidence_interval_lower,
                          upper: predictions.price_prediction.confidence_interval_upper,
                          predicted: predictions.price_prediction.predicted_value,
                          current: propertyInputs.current_price,
                        }
                      ]}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <RechartsTooltip formatter={(value: number) => formatCurrency(value)} />
                      <Legend />
                      <Bar dataKey="lower" fill="#3b82f6" fillOpacity={0.3} name="Lower Bound" />
                      <Bar dataKey="upper" fill="#3b82f6" fillOpacity={0.3} name="Upper Bound" />
                      <Bar dataKey="predicted" fill="#3b82f6" name="Predicted Price" />
                      <Bar dataKey="current" fill="#10b981" name="Current Price" />
                    </ComposedChart>
                  </ResponsiveContainer>

                  <Box sx={{ mt: 3, display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2 }}>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Lower Bound</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {formatCurrency(predictions.price_prediction.confidence_interval_lower)}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Predicted Value</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                        {formatCurrency(predictions.price_prediction.predicted_value)}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Upper Bound</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600 }}>
                        {formatCurrency(predictions.price_prediction.confidence_interval_upper)}
                      </Typography>
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Price Range</Typography>
                      <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                        {formatCurrency(predictions.price_prediction.confidence_interval_upper - predictions.price_prediction.confidence_interval_lower)}
                      </Typography>
                    </Box>
                  </Box>
                </GlassCard>
              </Grid>

              <Grid item xs={12} md={4}>
                <GlassCard sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    Feature Importance
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    Top factors influencing price
                  </Typography>

                  <ResponsiveContainer width="100%" height={350}>
                    <BarChart data={featureImportanceData} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" unit="%" />
                      <YAxis dataKey="feature" type="category" width={120} />
                      <RechartsTooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
                      <Bar dataKey="importance" fill="#8b5cf6">
                        {featureImportanceData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={`hsl(${270 - index * 30}, 70%, 60%)`} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </GlassCard>
              </Grid>
            </Grid>
          )}

          {activeTab === 1 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <GlassCard sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    12-Month Rent Forecast
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                    <Chip
                      label={`Trend: ${predictions.rent_forecast.trend}`}
                      color={predictions.rent_forecast.trend === 'increasing' ? 'success' : 'warning'}
                      icon={predictions.rent_forecast.trend === 'increasing' ? <TrendingUp /> : <TrendingDown />}
                    />
                    <Chip
                      label={`Confidence: ${predictions.rent_forecast.confidence}`}
                      color="primary"
                      variant="outlined"
                    />
                  </Box>

                  <ResponsiveContainer width="100%" height={400}>
                    <AreaChart data={rentForecastData}>
                      <defs>
                        <linearGradient id="colorRent" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <RechartsTooltip formatter={(value: number) => formatCurrency(value)} />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="rent"
                        stroke="#10b981"
                        fillOpacity={1}
                        fill="url(#colorRent)"
                        name="Forecasted Rent"
                      />
                    </AreaChart>
                  </ResponsiveContainer>

                  <Grid container spacing={2} sx={{ mt: 2 }}>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 2, bgcolor: 'action.hover', borderRadius: 2 }}>
                        <Typography variant="caption" color="text.secondary">Current Rent</Typography>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                          {formatCurrency(rentForecastData[0]?.rent || 0)}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 2, bgcolor: 'action.hover', borderRadius: 2 }}>
                        <Typography variant="caption" color="text.secondary">12-Month Forecast</Typography>
                        <Typography variant="h6" sx={{ fontWeight: 600, color: 'success.main' }}>
                          {formatCurrency(rentForecastData[rentForecastData.length - 1]?.rent || 0)}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                      <Box sx={{ p: 2, bgcolor: 'action.hover', borderRadius: 2 }}>
                        <Typography variant="caption" color="text.secondary">Expected Growth</Typography>
                        <Typography variant="h6" sx={{ fontWeight: 600, color: 'primary.main' }}>
                          {rentForecastData.length > 0 ? formatPercent((rentForecastData[rentForecastData.length - 1].rent - rentForecastData[0].rent) / rentForecastData[0].rent) : '0%'}
                        </Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </GlassCard>
              </Grid>
            </Grid>
          )}

          {activeTab === 2 && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <GlassCard sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    Risk Score Breakdown
                  </Typography>
                  <Box sx={{ textAlign: 'center', my: 3 }}>
                    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                      <CircularProgress
                        variant="determinate"
                        value={predictions.risk_score.predicted_value}
                        size={200}
                        thickness={4}
                        sx={{
                          color: getRiskColor(predictions.risk_score.predicted_value),
                        }}
                      />
                      <Box
                        sx={{
                          top: 0,
                          left: 0,
                          bottom: 0,
                          right: 0,
                          position: 'absolute',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexDirection: 'column',
                        }}
                      >
                        <Typography variant="h3" sx={{ fontWeight: 700, color: getRiskColor(predictions.risk_score.predicted_value) }}>
                          {predictions.risk_score.predicted_value.toFixed(1)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Risk Score
                        </Typography>
                      </Box>
                    </Box>
                  </Box>

                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={riskBreakdown}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="category" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      <Radar
                        name="Risk Level"
                        dataKey="value"
                        stroke="#ef4444"
                        fill="#ef4444"
                        fillOpacity={0.6}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </GlassCard>
              </Grid>

              <Grid item xs={12} md={6}>
                <GlassCard sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
                    Opportunity Score Analysis
                  </Typography>
                  <Box sx={{ textAlign: 'center', my: 3 }}>
                    <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                      <CircularProgress
                        variant="determinate"
                        value={predictions.opportunity_score.predicted_value}
                        size={200}
                        thickness={4}
                        sx={{
                          color: getOpportunityColor(predictions.opportunity_score.predicted_value),
                        }}
                      />
                      <Box
                        sx={{
                          top: 0,
                          left: 0,
                          bottom: 0,
                          right: 0,
                          position: 'absolute',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexDirection: 'column',
                        }}
                      >
                        <Typography variant="h3" sx={{ fontWeight: 700, color: getOpportunityColor(predictions.opportunity_score.predicted_value) }}>
                          {predictions.opportunity_score.predicted_value.toFixed(1)}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Opportunity Score
                        </Typography>
                      </Box>
                    </Box>
                  </Box>

                  <Box sx={{ mt: 4 }}>
                    <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                      Key Factors
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Market Growth</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>85%</Typography>
                        </Box>
                        <LinearProgress variant="determinate" value={85} sx={{ height: 8, borderRadius: 4 }} />
                      </Box>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Location Quality</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>75%</Typography>
                        </Box>
                        <LinearProgress variant="determinate" value={75} sx={{ height: 8, borderRadius: 4 }} />
                      </Box>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Price Upside</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>92%</Typography>
                        </Box>
                        <LinearProgress variant="determinate" value={92} sx={{ height: 8, borderRadius: 4 }} />
                      </Box>
                      <Box>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                          <Typography variant="body2">Economic Indicators</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>68%</Typography>
                        </Box>
                        <LinearProgress variant="determinate" value={68} sx={{ height: 8, borderRadius: 4 }} />
                      </Box>
                    </Box>
                  </Box>
                </GlassCard>
              </Grid>
            </Grid>
          )}

          {activeTab === 3 && (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <GradientGlassCard sx={{ p: 4 }}>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <Psychology sx={{ fontSize: 48, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                        AI-Powered Investment Insights
                      </Typography>
                      <Typography variant="body1" sx={{ mb: 3 }}>
                        Our machine learning models analyze {featureImportanceData.length}+ features including property characteristics,
                        market conditions, and economic indicators to provide data-driven investment recommendations.
                      </Typography>

                      <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                          <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2 }}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                              Model Performance
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • Price Prediction Accuracy: {formatPercent(predictions.price_prediction.confidence_score)}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • Rent Forecast Confidence: {predictions.rent_forecast.confidence}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • Risk Assessment Accuracy: {formatPercent(predictions.risk_score.confidence_score)}
                            </Typography>
                          </Box>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2 }}>
                            <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                              Models Used
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • {predictions.price_prediction.model_used}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • LSTM Time Series Forecasting
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              • Multi-Factor Risk Scoring
                            </Typography>
                          </Box>
                        </Grid>
                      </Grid>

                      <Divider sx={{ my: 3 }} />

                      <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                        Key Insights
                      </Typography>
                      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                          <Lightbulb sx={{ color: 'success.main', mt: 0.5 }} />
                          <Typography variant="body2">
                            <strong>Price Opportunity:</strong> The predicted value of {formatCurrency(predictions.price_prediction.predicted_value)} suggests
                            a {formatPercent((predictions.price_prediction.predicted_value - propertyInputs.current_price) / propertyInputs.current_price)} upside
                            potential from the current price.
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                          <TrendingUp sx={{ color: 'success.main', mt: 0.5 }} />
                          <Typography variant="body2">
                            <strong>Rent Growth:</strong> The {predictions.rent_forecast.trend} trend in rent forecasts indicates favorable market conditions
                            with projected 12-month growth of {rentForecastData.length > 0 ? formatPercent((rentForecastData[rentForecastData.length - 1].rent - rentForecastData[0].rent) / rentForecastData[0].rent) : '0%'}.
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
                          <Warning sx={{ color: getRiskColor(predictions.risk_score.predicted_value), mt: 0.5 }} />
                          <Typography variant="body2">
                            <strong>Risk Profile:</strong> With a risk score of {predictions.risk_score.predicted_value.toFixed(1)},
                            this investment is classified as {predictions.risk_score.predicted_value < 30 ? 'low' : predictions.risk_score.predicted_value < 60 ? 'moderate' : 'high'} risk.
                            {predictions.risk_score.predicted_value < 30 ? ' Strong fundamentals detected.' : predictions.risk_score.predicted_value < 60 ? ' Standard market conditions apply.' : ' Careful due diligence recommended.'}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>
                  </Box>
                </GradientGlassCard>
              </Grid>
            </Grid>
          )}
        </>
      )}
    </Box>
  );
};

export default AdvancedAnalyticsDashboard;
