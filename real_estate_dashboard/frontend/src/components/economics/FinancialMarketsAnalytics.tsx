import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Chip,
  Stack,
  Paper,
  alpha,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ChartIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import api from '../../services/api';

interface Category {
  source_category: string;
  count: number;
  start_date: string | null;
  end_date: string | null;
}

interface Indicator {
  indicator_name: string;
  count: number;
}

interface TimeSeriesData {
  id: number;
  date: string | null;
  period_type: string;
  indicator_name: string;
  indicator_value: number | null;
  indicator_unit: string | null;
  source_category: string;
  data_source: string | null;
  notes: string | null;
}

export const FinancialMarketsAnalytics: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [indicators, setIndicators] = useState<Indicator[]>([]);
  const [selectedIndicator, setSelectedIndicator] = useState<string>('');
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([]);

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Fetch indicators when category changes
  useEffect(() => {
    if (selectedCategory) {
      fetchIndicators(selectedCategory);
    }
  }, [selectedCategory]);

  // Fetch time series data when indicator changes
  useEffect(() => {
    if (selectedCategory && selectedIndicator) {
      fetchTimeSeriesData();
    }
  }, [selectedCategory, selectedIndicator]);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/market-intelligence/data/financial-time-series/categories');
      setCategories(response.data.categories || []);

      // Auto-select first category
      if (response.data.categories && response.data.categories.length > 0) {
        setSelectedCategory(response.data.categories[0].source_category);
      }
    } catch (err: any) {
      console.error('Error fetching categories:', err);
      setError('Failed to load financial categories');
    } finally {
      setLoading(false);
    }
  };

  const fetchIndicators = async (category: string) => {
    try {
      setLoading(true);
      const response = await api.get(`/market-intelligence/data/financial-time-series/indicators`, {
        params: { source_category: category }
      });
      setIndicators(response.data.indicators || []);

      // Auto-select first indicator
      if (response.data.indicators && response.data.indicators.length > 0) {
        setSelectedIndicator(response.data.indicators[0].indicator_name);
      } else {
        setSelectedIndicator('');
        setTimeSeriesData([]);
      }
    } catch (err: any) {
      console.error('Error fetching indicators:', err);
      setError('Failed to load indicators');
      setIndicators([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchTimeSeriesData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await api.get('/market-intelligence/data/financial-time-series', {
        params: {
          source_category: selectedCategory,
          indicator_name: selectedIndicator,
          limit: 1000
        }
      });

      // Sort data by date ascending for chart display
      const sortedData = (response.data.data || []).sort((a: TimeSeriesData, b: TimeSeriesData) => {
        if (!a.date || !b.date) return 0;
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      });

      setTimeSeriesData(sortedData);
    } catch (err: any) {
      console.error('Error fetching time series data:', err);
      setError('Failed to load time series data');
      setTimeSeriesData([]);
    } finally {
      setLoading(false);
    }
  };

  // Format category name for display
  const formatCategoryName = (category: string) => {
    return category
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  // Prepare chart data
  const chartData = timeSeriesData.map(item => ({
    date: item.date ? new Date(item.date).toLocaleDateString() : 'N/A',
    value: item.indicator_value,
    fullDate: item.date,
  }));

  // Calculate statistics
  const latestValue = timeSeriesData.length > 0 ? timeSeriesData[0].indicator_value : null;
  const earliestValue = timeSeriesData.length > 0 ? timeSeriesData[timeSeriesData.length - 1].indicator_value : null;
  const change = latestValue && earliestValue ? ((latestValue - earliestValue) / earliestValue) * 100 : null;
  const isPositiveChange = change ? change > 0 : null;

  const avgValue = timeSeriesData.length > 0
    ? timeSeriesData.reduce((sum, item) => sum + (item.indicator_value || 0), 0) / timeSeriesData.length
    : null;

  const maxValue = timeSeriesData.length > 0
    ? Math.max(...timeSeriesData.map(item => item.indicator_value || 0))
    : null;

  const minValue = timeSeriesData.length > 0
    ? Math.min(...timeSeriesData.map(item => item.indicator_value || 0).filter(v => v !== 0))
    : null;

  return (
    <Box>
      <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <AssessmentIcon />
        Financial Markets Analytics
      </Typography>

      {/* Category and Indicator Selection */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <FormControl fullWidth>
            <InputLabel>Financial Category</InputLabel>
            <Select
              value={selectedCategory}
              label="Financial Category"
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              {categories.map((cat) => (
                <MenuItem key={cat.source_category} value={cat.source_category}>
                  {formatCategoryName(cat.source_category)} ({cat.count} records)
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6}>
          <FormControl fullWidth disabled={!selectedCategory || indicators.length === 0}>
            <InputLabel>Indicator</InputLabel>
            <Select
              value={selectedIndicator}
              label="Indicator"
              onChange={(e) => setSelectedIndicator(e.target.value)}
            >
              {indicators.map((ind) => (
                <MenuItem key={ind.indicator_name} value={ind.indicator_name}>
                  {ind.indicator_name} ({ind.count} data points)
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {loading && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <CircularProgress size={48} />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Loading financial data...
          </Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!loading && !error && timeSeriesData.length > 0 && (
        <>
          {/* Statistics Cards */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{
                background: isPositiveChange
                  ? `linear-gradient(135deg, ${alpha('#10b981', 0.1)} 0%, ${alpha('#10b981', 0.05)} 100%)`
                  : `linear-gradient(135deg, ${alpha('#ef4444', 0.1)} 0%, ${alpha('#ef4444', 0.05)} 100%)`,
              }}>
                <CardContent>
                  <Stack spacing={1}>
                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                      Latest Value
                    </Typography>
                    <Stack direction="row" alignItems="center" spacing={1}>
                      <Typography variant="h4" sx={{ fontWeight: 700 }}>
                        {latestValue?.toFixed(2) || 'N/A'}
                      </Typography>
                      {timeSeriesData[0]?.indicator_unit && (
                        <Typography variant="body2" color="text.secondary">
                          {timeSeriesData[0].indicator_unit}
                        </Typography>
                      )}
                    </Stack>
                    {change !== null && (
                      <Stack direction="row" alignItems="center" spacing={0.5}>
                        {isPositiveChange ? (
                          <TrendingUpIcon sx={{ fontSize: 20, color: '#10b981' }} />
                        ) : (
                          <TrendingDownIcon sx={{ fontSize: 20, color: '#ef4444' }} />
                        )}
                        <Typography
                          variant="body2"
                          sx={{
                            fontWeight: 600,
                            color: isPositiveChange ? '#10b981' : '#ef4444',
                          }}
                        >
                          {isPositiveChange ? '+' : ''}{change.toFixed(2)}% from start
                        </Typography>
                      </Stack>
                    )}
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Stack spacing={1}>
                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                      Average Value
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700 }}>
                      {avgValue?.toFixed(2) || 'N/A'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Over {timeSeriesData.length} periods
                    </Typography>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Stack spacing={1}>
                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                      Maximum Value
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981' }}>
                      {maxValue?.toFixed(2) || 'N/A'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Peak level
                    </Typography>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent>
                  <Stack spacing={1}>
                    <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                      Minimum Value
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#ef4444' }}>
                      {minValue?.toFixed(2) || 'N/A'}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Lowest level
                    </Typography>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Time Series Chart */}
          <Card>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600 }}>
                  {selectedIndicator} - Time Series
                </Typography>
                <Chip
                  label={`${timeSeriesData.length} data points`}
                  size="small"
                  icon={<ChartIcon />}
                />
              </Stack>

              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                  <XAxis
                    dataKey="date"
                    tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                  />
                  <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: isDark ? '#1f2937' : '#ffffff',
                      border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                    }}
                    labelFormatter={(label) => `Date: ${label}`}
                    formatter={(value: any) => [
                      `${value?.toFixed(2) || 'N/A'} ${timeSeriesData[0]?.indicator_unit || ''}`,
                      'Value'
                    ]}
                  />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#3b82f6"
                    fillOpacity={1}
                    fill="url(#colorValue)"
                    name={selectedIndicator}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Data Source Info */}
          {timeSeriesData[0]?.data_source && (
            <Alert severity="info" sx={{ mt: 3 }}>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                Data Source: {timeSeriesData[0].data_source}
              </Typography>
              {timeSeriesData[0].notes && (
                <Typography variant="caption" component="div" sx={{ mt: 1 }}>
                  {timeSeriesData[0].notes}
                </Typography>
              )}
            </Alert>
          )}
        </>
      )}

      {!loading && !error && selectedCategory && selectedIndicator && timeSeriesData.length === 0 && (
        <Alert severity="warning">
          No data available for the selected indicator. Please try a different selection.
        </Alert>
      )}

      {!loading && !error && !selectedCategory && categories.length > 0 && (
        <Alert severity="info">
          Please select a financial category to view data.
        </Alert>
      )}
    </Box>
  );
};

export default FinancialMarketsAnalytics;
