import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  Chip,
  CircularProgress,
  Paper,
  Alert,
  LinearProgress,
  Divider,
  alpha,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ChartIcon,
  Assessment as AssessmentIcon,
  LocalFireDepartment as FireIcon,
  Speed as SpeedIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';
import { CorrelationMatrix } from './CorrelationMatrix';
import { InvestmentInsights } from './InvestmentInsights';

interface AnalysisData {
  economic_health_score: number;
  health_rating: string;
  category_stats: Record<string, any>;
  key_indicators: Record<string, any>;
  summary: any;
}

interface TrendsData {
  top_gainers: any[];
  top_losers: any[];
  most_volatile: any[];
}

export const USAEconomicsAnalysis: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [loading, setLoading] = useState(true);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [trendsData, setTrendsData] = useState<TrendsData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalysisData();
  }, []);

  const fetchAnalysisData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [analysisResponse, trendsResponse] = await Promise.all([
        api.get('/market-intelligence/data/usa-economics/analysis'),
        api.get('/market-intelligence/data/usa-economics/trends'),
      ]);

      setAnalysisData(analysisResponse.data);
      setTrendsData(trendsResponse.data);
    } catch (error: any) {
      console.error('Error fetching analysis:', error);
      setError('Failed to load economic analysis');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <CircularProgress size={48} />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Analyzing economic data...
        </Typography>
      </Box>
    );
  }

  if (error || !analysisData) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error || 'No analysis data available'}
      </Alert>
    );
  }

  // Prepare chart data
  const categoryChartData = Object.entries(analysisData.category_stats).map(([category, stats]: [string, any]) => ({
    category: category.replace(/_/g, ' '),
    positive: stats.positive_changes,
    negative: stats.negative_changes,
    avgChange: stats.avg_change_percent,
  }));

  const trendChartData = Object.entries(analysisData.category_stats).map(([category, stats]: [string, any]) => ({
    category: category.replace(/_/g, ' '),
    value: stats.avg_change_percent,
  }));

  const healthColor = analysisData.economic_health_score > 75 ? '#10b981' :
                      analysisData.economic_health_score > 50 ? '#f59e0b' : '#ef4444';

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f43f5e'];

  return (
    <Stack spacing={4}>
      {/* Economic Health Score */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
              background: `linear-gradient(135deg, ${healthColor} 0%, ${alpha(healthColor, 0.7)} 100%)`,
              color: 'white',
              height: '100%',
            }}
          >
            <CardContent>
              <Stack spacing={2} alignItems="center" sx={{ py: 2 }}>
                <SpeedIcon sx={{ fontSize: 48 }} />
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  Economic Health Score
                </Typography>
                <Typography variant="h2" sx={{ fontWeight: 700 }}>
                  {analysisData.economic_health_score}
                </Typography>
                <Chip
                  label={analysisData.health_rating.toUpperCase()}
                  sx={{
                    bgcolor: 'rgba(255,255,255,0.2)',
                    color: 'white',
                    fontWeight: 600,
                  }}
                />
                <Typography variant="body2" sx={{ textAlign: 'center', opacity: 0.9 }}>
                  Based on GDP growth, unemployment, and inflation targets
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                Economic Summary
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(59, 130, 246, 0.1)' : 'rgba(59, 130, 246, 0.05)' }}>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                      {analysisData.summary.total_categories}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Categories
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(16, 185, 129, 0.1)' : 'rgba(16, 185, 129, 0.05)' }}>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981' }}>
                      {analysisData.summary.bullish_categories}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Bullish
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(239, 68, 68, 0.1)' : 'rgba(239, 68, 68, 0.05)' }}>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#ef4444' }}>
                      {analysisData.summary.bearish_categories}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Bearish
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center', bgcolor: isDark ? 'rgba(139, 92, 246, 0.1)' : 'rgba(139, 92, 246, 0.05)' }}>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#8b5cf6' }}>
                      {analysisData.summary.total_indicators}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Total Indicators
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Key Economic Indicators */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Key Economic Indicators
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(analysisData.key_indicators).map(([name, data]: [string, any]) => (
              <Grid item xs={12} sm={6} md={4} key={name}>
                <Paper
                  sx={{
                    p: 2,
                    height: '100%',
                    border: `1px solid ${isDark ? alpha('#94a3b8', 0.2) : alpha('#0f172a', 0.1)}`,
                  }}
                >
                  <Stack spacing={1}>
                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                      {name}
                    </Typography>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="h5" sx={{ fontWeight: 700 }}>
                        {data.value}
                      </Typography>
                      {data.change_percent !== null && (
                        <Stack direction="row" alignItems="center" spacing={0.5}>
                          {data.change_percent > 0 ? (
                            <TrendingUpIcon sx={{ fontSize: 20, color: '#10b981' }} />
                          ) : (
                            <TrendingDownIcon sx={{ fontSize: 20, color: '#ef4444' }} />
                          )}
                          <Typography
                            variant="body2"
                            sx={{
                              fontWeight: 600,
                              color: data.change_percent > 0 ? '#10b981' : '#ef4444',
                            }}
                          >
                            {data.change_percent > 0 ? '+' : ''}
                            {data.change_percent.toFixed(2)}%
                          </Typography>
                        </Stack>
                      )}
                    </Stack>
                    <Typography variant="caption" color="text.secondary">
                      Previous: {data.previous} {data.unit}
                    </Typography>
                  </Stack>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Category Trends Chart */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Category Trends (Average % Change)
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={trendChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
              <XAxis dataKey="category" tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }} angle={-45} textAnchor="end" height={100} />
              <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: isDark ? '#1f2937' : '#ffffff',
                  border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                }}
              />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Positive vs Negative Changes */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Indicator Changes by Category
          </Typography>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
              <XAxis dataKey="category" tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }} angle={-45} textAnchor="end" height={100} />
              <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: isDark ? '#1f2937' : '#ffffff',
                  border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                }}
              />
              <Legend />
              <Bar dataKey="positive" fill="#10b981" name="Positive Changes" radius={[8, 8, 0, 0]} />
              <Bar dataKey="negative" fill="#ef4444" name="Negative Changes" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Top Movers */}
      {trendsData && (
        <Grid container spacing={3}>
          {/* Top Gainers */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                  <TrendingUpIcon sx={{ color: '#10b981' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Top Gainers
                  </Typography>
                </Stack>
                <Stack spacing={1}>
                  {trendsData.top_gainers.slice(0, 5).map((item, idx) => (
                    <Paper
                      key={idx}
                      sx={{
                        p: 2,
                        bgcolor: isDark ? 'rgba(16, 185, 129, 0.05)' : 'rgba(16, 185, 129, 0.02)',
                      }}
                    >
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {item.indicator_name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.category}
                          </Typography>
                        </Box>
                        <Stack alignItems="flex-end">
                          <Typography variant="h6" sx={{ fontWeight: 700, color: '#10b981' }}>
                            +{item.change_percent}%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.current_value}
                          </Typography>
                        </Stack>
                      </Stack>
                    </Paper>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          {/* Top Losers */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
                  <TrendingDownIcon sx={{ color: '#ef4444' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Top Losers
                  </Typography>
                </Stack>
                <Stack spacing={1}>
                  {trendsData.top_losers.slice(0, 5).map((item, idx) => (
                    <Paper
                      key={idx}
                      sx={{
                        p: 2,
                        bgcolor: isDark ? 'rgba(239, 68, 68, 0.05)' : 'rgba(239, 68, 68, 0.02)',
                      }}
                    >
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {item.indicator_name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.category}
                          </Typography>
                        </Box>
                        <Stack alignItems="flex-end">
                          <Typography variant="h6" sx={{ fontWeight: 700, color: '#ef4444' }}>
                            {item.change_percent}%
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {item.current_value}
                          </Typography>
                        </Stack>
                      </Stack>
                    </Paper>
                  ))}
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Investment Insights */}
      <InvestmentInsights analysisData={analysisData} />

      {/* Correlation Matrix */}
      {analysisData && analysisData.key_indicators && (
        <CorrelationMatrix
          indicators={Object.entries(analysisData.key_indicators).map(([name, data]: [string, any]) => ({
            indicator_name: name,
            category: analysisData.category_stats?.[Object.keys(analysisData.category_stats)[0]]?.category || 'general',
            change_percent: data.change_percent,
            last_value_numeric: typeof data.value === 'number' ? data.value : parseFloat(data.value) || 0,
          }))}
        />
      )}

      {/* Cache Info */}
      <Alert severity="info" icon={<ChartIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          Analysis Features:
        </Typography>
        <Typography variant="caption" component="div">
          • Economic Health Score: Calculated from GDP growth, unemployment, and inflation metrics
        </Typography>
        <Typography variant="caption" component="div">
          • Category Trends: Shows average percentage change across all indicators in each category
        </Typography>
        <Typography variant="caption" component="div">
          • Top Movers: Highlights indicators with the largest positive and negative changes
        </Typography>
        <Typography variant="caption" component="div" sx={{ mt: 1 }}>
          Data is cached for 1 hour for optimal performance
        </Typography>
      </Alert>
    </Stack>
  );
};
