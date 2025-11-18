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
  Alert,
  Button,
  IconButton,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  alpha,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ChartIcon,
  Refresh as RefreshIcon,
  DateRange as DateRangeIcon,
  Add as AddIcon,
  Remove as RemoveIcon,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

interface DataPoint {
  date: string;
  value: number | null;
  change_from_previous?: number | null;
  change_percent?: number | null;
}

interface HistoricalSeries {
  indicator_name: string;
  country: string;
  category?: string;
  unit?: string;
  data_points: DataPoint[];
  count: number;
  start_date: string;
  end_date: string;
  frequency?: string;
  statistics?: {
    min: number;
    max: number;
    avg: number;
    latest: number;
    first: number;
    total_change: number;
    total_change_percent: number;
  };
}

interface ChartData {
  date: string;
  [key: string]: string | number | null;
}

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

const TIME_RANGES = [
  { value: 30, label: '1 Month' },
  { value: 90, label: '3 Months' },
  { value: 180, label: '6 Months' },
  { value: 365, label: '1 Year' },
  { value: 730, label: '2 Years' },
  { value: 1825, label: '5 Years' },
];

export const HistoricalCharts: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedIndicators, setSelectedIndicators] = useState<string[]>(['GDP']);
  const [timeRange, setTimeRange] = useState(365);
  const [seriesData, setSeriesData] = useState<HistoricalSeries[]>([]);
  const [chartData, setChartData] = useState<ChartData[]>([]);

  useEffect(() => {
    if (selectedIndicators.length > 0) {
      loadHistoricalData();
    }
  }, [selectedIndicators, timeRange]);

  const loadHistoricalData = async () => {
    setLoading(true);
    setError(null);

    try {
      // Calculate date range
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - timeRange);

      const response = await api.get('/market-intelligence/data/usa-economics/history/multiple', {
        params: {
          indicator_names: selectedIndicators,
          start_date: startDate.toISOString().split('T')[0],
          end_date: endDate.toISOString().split('T')[0],
          limit: timeRange,
        },
      });

      const series: HistoricalSeries[] = response.data.series || [];
      setSeriesData(series);

      // Transform data for chart
      if (series.length > 0) {
        // Collect all unique dates
        const allDates = new Set<string>();
        series.forEach(s => {
          s.data_points.forEach(dp => {
            allDates.add(dp.date);
          });
        });

        // Sort dates
        const sortedDates = Array.from(allDates).sort();

        // Create chart data
        const transformedData: ChartData[] = sortedDates.map(date => {
          const dataPoint: ChartData = { date };

          series.forEach(s => {
            const point = s.data_points.find(dp => dp.date === date);
            dataPoint[s.indicator_name] = point?.value ?? null;
          });

          return dataPoint;
        });

        setChartData(transformedData);
      }
    } catch (err: any) {
      console.error('Error loading historical data:', err);
      setError('Failed to load historical data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const addIndicator = (indicator: string) => {
    if (!selectedIndicators.includes(indicator) && selectedIndicators.length < 5) {
      setSelectedIndicators([...selectedIndicators, indicator]);
    }
  };

  const removeIndicator = (indicator: string) => {
    setSelectedIndicators(selectedIndicators.filter(i => i !== indicator));
  };

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  const formatNumber = (value: number | null): string => {
    if (value === null || value === undefined) return '-';
    return value.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  };

  const getLineColor = (index: number): string => {
    const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
    return colors[index % colors.length];
  };

  const getTrendIcon = (series: HistoricalSeries) => {
    if (!series.statistics) return null;
    return series.statistics.total_change > 0 ? (
      <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
    ) : (
      <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
    );
  };

  const getTrendColor = (change: number | null): string => {
    if (change === null || change === 0) return isDark ? '#9ca3af' : '#6b7280';
    return change > 0 ? '#10b981' : '#ef4444';
  };

  return (
    <Stack spacing={4}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Stack direction="row" alignItems="center" spacing={2}>
          <ChartIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              Historical Economic Data
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Analyze trends over time for key economic indicators
            </Typography>
          </Box>
        </Stack>
        <Stack direction="row" spacing={1}>
          <Chip
            label={`${selectedIndicators.length} Indicator${selectedIndicators.length !== 1 ? 's' : ''}`}
            color="primary"
            size="small"
          />
          <Tooltip title="Refresh">
            <IconButton onClick={loadHistoricalData} disabled={loading} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {/* Controls */}
      <Card>
        <CardContent>
          <Grid container spacing={3}>
            {/* Time Range Selection */}
            <Grid item xs={12} md={4}>
              <FormControl fullWidth>
                <InputLabel>Time Range</InputLabel>
                <Select
                  value={timeRange}
                  label="Time Range"
                  onChange={(e) => setTimeRange(e.target.value as number)}
                >
                  {TIME_RANGES.map((range) => (
                    <MenuItem key={range.value} value={range.value}>
                      {range.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            {/* Add Indicator */}
            <Grid item xs={12} md={8}>
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary">
                  Selected Indicators (max 5):
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                  {selectedIndicators.map((indicator) => (
                    <Chip
                      key={indicator}
                      label={indicator}
                      onDelete={() => removeIndicator(indicator)}
                      color="primary"
                      deleteIcon={<RemoveIcon />}
                    />
                  ))}
                </Stack>
              </Stack>
            </Grid>

            {/* Popular Indicators */}
            <Grid item xs={12}>
              <Stack spacing={1}>
                <Typography variant="caption" color="text.secondary">
                  Add from popular indicators:
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
                  {POPULAR_INDICATORS.filter(
                    (ind) => !selectedIndicators.includes(ind.value)
                  ).map((indicator) => (
                    <Button
                      key={indicator.value}
                      size="small"
                      variant="outlined"
                      startIcon={<AddIcon />}
                      onClick={() => addIndicator(indicator.value)}
                      disabled={selectedIndicators.length >= 5}
                    >
                      {indicator.label}
                    </Button>
                  ))}
                </Stack>
              </Stack>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {loading && (
        <Box sx={{ textAlign: 'center', py: 8 }}>
          <CircularProgress size={48} />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Loading historical data...
          </Typography>
        </Box>
      )}

      {/* Statistics Cards */}
      {!loading && seriesData.length > 0 && (
        <Grid container spacing={3}>
          {seriesData.map((series, idx) => (
            <Grid item xs={12} sm={6} md={4} key={series.indicator_name}>
              <Card
                sx={{
                  border: `2px solid ${getLineColor(idx)}`,
                  bgcolor: isDark
                    ? alpha(getLineColor(idx), 0.05)
                    : alpha(getLineColor(idx), 0.02),
                }}
              >
                <CardContent>
                  <Stack spacing={2}>
                    <Stack direction="row" justifyContent="space-between" alignItems="flex-start">
                      <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>
                        {series.indicator_name}
                      </Typography>
                      {getTrendIcon(series)}
                    </Stack>

                    <Box>
                      <Typography variant="h4" sx={{ fontWeight: 700, color: getLineColor(idx) }}>
                        {series.statistics ? formatNumber(series.statistics.latest) : '-'}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {series.unit || 'value'}
                      </Typography>
                    </Box>

                    {series.statistics && (
                      <Grid container spacing={1}>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Change
                          </Typography>
                          <Typography
                            variant="body2"
                            sx={{
                              fontWeight: 600,
                              color: getTrendColor(series.statistics.total_change),
                            }}
                          >
                            {series.statistics.total_change > 0 ? '+' : ''}
                            {formatNumber(series.statistics.total_change)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            % Change
                          </Typography>
                          <Typography
                            variant="body2"
                            sx={{
                              fontWeight: 600,
                              color: getTrendColor(series.statistics.total_change_percent),
                            }}
                          >
                            {series.statistics.total_change_percent > 0 ? '+' : ''}
                            {series.statistics.total_change_percent.toFixed(2)}%
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Min
                          </Typography>
                          <Typography variant="body2">
                            {formatNumber(series.statistics.min)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" color="text.secondary">
                            Max
                          </Typography>
                          <Typography variant="body2">
                            {formatNumber(series.statistics.max)}
                          </Typography>
                        </Grid>
                      </Grid>
                    )}

                    <Typography variant="caption" color="text.secondary">
                      {series.count} data points • {series.frequency || 'monthly'}
                    </Typography>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Line Chart */}
      {!loading && chartData.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Time Series Chart
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                <XAxis
                  dataKey="date"
                  tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
                  tickFormatter={formatDate}
                />
                <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                <RechartsTooltip
                  contentStyle={{
                    backgroundColor: isDark ? '#1f2937' : '#ffffff',
                    border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                  }}
                  formatter={(value: any) => formatNumber(value)}
                  labelFormatter={formatDate}
                />
                <Legend />
                {selectedIndicators.map((indicator, idx) => (
                  <Line
                    key={indicator}
                    type="monotone"
                    dataKey={indicator}
                    name={indicator}
                    stroke={getLineColor(idx)}
                    strokeWidth={2}
                    dot={false}
                    activeDot={{ r: 6 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Area Chart (Alternative View) */}
      {!loading && chartData.length > 0 && selectedIndicators.length === 1 && (
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              Area Chart
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                <XAxis
                  dataKey="date"
                  tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
                  tickFormatter={formatDate}
                />
                <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                <RechartsTooltip
                  contentStyle={{
                    backgroundColor: isDark ? '#1f2937' : '#ffffff',
                    border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                  }}
                  formatter={(value: any) => formatNumber(value)}
                  labelFormatter={formatDate}
                />
                <Area
                  type="monotone"
                  dataKey={selectedIndicators[0]}
                  stroke={getLineColor(0)}
                  fill={getLineColor(0)}
                  fillOpacity={0.3}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Empty State */}
      {!loading && chartData.length === 0 && selectedIndicators.length > 0 && (
        <Card>
          <CardContent>
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <ChartIcon sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No Historical Data Available
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Historical data for the selected indicators is not available in the database.
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Try selecting different indicators or check if data has been imported.
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Info Alert */}
      <Alert severity="info" icon={<DateRangeIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          Historical Data Features:
        </Typography>
        <Typography variant="caption" component="div">
          • Compare up to 5 economic indicators simultaneously
        </Typography>
        <Typography variant="caption" component="div">
          • View trends from 1 month to 5 years
        </Typography>
        <Typography variant="caption" component="div">
          • Automatic statistics calculation (min, max, average, total change)
        </Typography>
        <Typography variant="caption" component="div">
          • Interactive charts with tooltips
        </Typography>
        <Typography variant="caption" component="div" sx={{ mt: 1 }}>
          Note: Historical data availability depends on database records. If no data is displayed,
          the system may need to fetch and store historical data first.
        </Typography>
      </Alert>
    </Stack>
  );
};
