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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  LinearProgress,
  alpha,
  Button,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  AccountBalance as BankIcon,
  Refresh as RefreshIcon,
  CompareArrows as CompareIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
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
} from 'recharts';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

interface REITData {
  ticker: string;
  company_name: string;
  current_price: number;
  price_change: number;
  price_change_pct: number;
  volume: number;
  market_cap: number;
  pe_ratio: number | null;
  dividend_yield: number | null;
  sector: string;
  industry: string;
  '52_week_high': number;
  '52_week_low': number;
  timestamp: string;
}

interface MarketSummary {
  market_indices: {
    indices: Array<{
      symbol: string;
      name: string;
      value: number;
      change: number;
      change_pct: number;
    }>;
  };
  reits: {
    reits: REITData[];
    count: number;
  };
  treasury_rates: {
    rates: Array<{
      symbol: string;
      name: string;
      rate: number;
      change: number;
      change_pct: number;
    }>;
  };
}

export const REITComparables: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<MarketSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [selectedREITs, setSelectedREITs] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadMarketData();
    // Load favorites from localStorage
    const saved = localStorage.getItem('reit_favorites');
    if (saved) {
      setFavorites(new Set(JSON.parse(saved)));
    }
  }, []);

  const loadMarketData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/market-intelligence/yfinance/market-summary');
      setData(response.data);
    } catch (err: any) {
      console.error('Error loading market data:', err);
      setError('Failed to load market data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleFavorite = (ticker: string) => {
    const newFavorites = new Set(favorites);
    if (newFavorites.has(ticker)) {
      newFavorites.delete(ticker);
    } else {
      newFavorites.add(ticker);
    }
    setFavorites(newFavorites);
    localStorage.setItem('reit_favorites', JSON.stringify(Array.from(newFavorites)));
  };

  const toggleSelection = (ticker: string) => {
    const newSelection = new Set(selectedREITs);
    if (newSelection.has(ticker)) {
      newSelection.delete(ticker);
    } else {
      // Limit to 5 selections for comparison
      if (newSelection.size < 5) {
        newSelection.add(ticker);
      }
    }
    setSelectedREITs(newSelection);
  };

  const formatCurrency = (value: number | null | undefined): string => {
    if (value === null || value === undefined) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value);
  };

  const formatMarketCap = (value: number | null | undefined): string => {
    if (value === null || value === undefined) return '-';
    if (value >= 1e12) return `$${(value / 1e12).toFixed(2)}T`;
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`;
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`;
    return `$${value.toFixed(0)}`;
  };

  const formatPercent = (value: number | null | undefined): string => {
    if (value === null || value === undefined) return '-';
    return `${value.toFixed(2)}%`;
  };

  const getPerformanceColor = (pct: number | null): string => {
    if (pct === null) return isDark ? '#9ca3af' : '#6b7280';
    if (pct > 0) return '#10b981';
    if (pct < 0) return '#ef4444';
    return isDark ? '#9ca3af' : '#6b7280';
  };

  if (loading) {
    return (
      <Box sx={{ textAlign: 'center', py: 8 }}>
        <CircularProgress size={48} />
        <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
          Loading REIT market data...
        </Typography>
      </Box>
    );
  }

  if (error || !data) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error || 'No market data available'}
      </Alert>
    );
  }

  const reits = data.reits.reits || [];
  const selectedREITsData = reits.filter(r => selectedREITs.has(r.ticker));

  // Prepare comparison chart data
  const comparisonData = selectedREITsData.map(reit => ({
    ticker: reit.ticker,
    'Dividend Yield': (reit.dividend_yield || 0) * 100,
    'P/E Ratio': reit.pe_ratio || 0,
    'Price Change %': reit.price_change_pct || 0,
    '52W Performance': reit.current_price && reit['52_week_low']
      ? ((reit.current_price - reit['52_week_low']) / reit['52_week_low']) * 100
      : 0,
  }));

  // Radar chart data for selected REITs
  const radarData = [
    { metric: 'Dividend Yield', ...Object.fromEntries(selectedREITsData.map(r => [r.ticker, (r.dividend_yield || 0) * 100])) },
    { metric: 'Price Momentum', ...Object.fromEntries(selectedREITsData.map(r => [r.ticker, Math.abs(r.price_change_pct || 0)])) },
    { metric: '52W Performance', ...Object.fromEntries(selectedREITsData.map(r => [r.ticker, r.current_price && r['52_week_low'] ? ((r.current_price - r['52_week_low']) / r['52_week_low']) * 100 : 0])) },
  ];

  return (
    <Stack spacing={4}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Stack direction="row" alignItems="center" spacing={2}>
          <BankIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              REIT Comparables
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Compare your properties against public REITs
            </Typography>
          </Box>
        </Stack>
        <Stack direction="row" spacing={1}>
          <Chip
            label={`${reits.length} REITs`}
            color="primary"
            size="small"
          />
          {selectedREITs.size > 0 && (
            <Chip
              label={`${selectedREITs.size} Selected`}
              color="secondary"
              size="small"
              icon={<CompareIcon />}
            />
          )}
          <Tooltip title="Refresh">
            <IconButton onClick={loadMarketData} disabled={loading} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {/* Market Indices Overview */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
            Market Overview
          </Typography>
          <Grid container spacing={2}>
            {data.market_indices.indices.slice(0, 4).map((index) => (
              <Grid item xs={12} sm={6} md={3} key={index.symbol}>
                <Paper
                  sx={{
                    p: 2,
                    bgcolor: isDark
                      ? alpha('#1e293b', 0.5)
                      : alpha('#f8fafc', 0.8),
                  }}
                >
                  <Typography variant="caption" color="text.secondary">
                    {index.name}
                  </Typography>
                  <Typography variant="h6" sx={{ fontWeight: 700, my: 0.5 }}>
                    {index.value?.toLocaleString()}
                  </Typography>
                  <Stack direction="row" alignItems="center" spacing={0.5}>
                    {index.change_pct !== null && index.change_pct > 0 ? (
                      <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                    ) : (
                      <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                    )}
                    <Typography
                      variant="caption"
                      sx={{
                        fontWeight: 600,
                        color: getPerformanceColor(index.change_pct),
                      }}
                    >
                      {index.change_pct !== null ? `${index.change_pct > 0 ? '+' : ''}${index.change_pct.toFixed(2)}%` : '-'}
                    </Typography>
                  </Stack>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* REIT Comparison Selection Hint */}
      {selectedREITs.size === 0 && (
        <Alert severity="info" icon={<CompareIcon />}>
          Select up to 5 REITs from the table below to compare their performance metrics
        </Alert>
      )}

      {/* Comparison Charts - Only show if REITs are selected */}
      {selectedREITs.size > 0 && (
        <Grid container spacing={3}>
          {/* Bar Chart Comparison */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Metrics Comparison
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={comparisonData}>
                    <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
                    <XAxis dataKey="ticker" tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                    <YAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                    <RechartsTooltip
                      contentStyle={{
                        backgroundColor: isDark ? '#1f2937' : '#ffffff',
                        border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                      }}
                    />
                    <Legend />
                    <Bar dataKey="Dividend Yield" fill="#10b981" />
                    <Bar dataKey="Price Change %" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Radar Chart */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  Performance Radar
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData}>
                    <PolarGrid stroke={isDark ? '#374151' : '#e5e7eb'} />
                    <PolarAngleAxis
                      dataKey="metric"
                      tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
                    />
                    <PolarRadiusAxis tick={{ fill: isDark ? '#9ca3af' : '#6b7280' }} />
                    {selectedREITsData.map((reit, idx) => {
                      const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'];
                      return (
                        <Radar
                          key={reit.ticker}
                          name={reit.ticker}
                          dataKey={reit.ticker}
                          stroke={colors[idx % colors.length]}
                          fill={colors[idx % colors.length]}
                          fillOpacity={0.3}
                        />
                      );
                    })}
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* REIT Data Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Major REITs & Real Estate ETFs
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>Compare</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Favorite</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Ticker</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Company</TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    Price
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    Change
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    Dividend Yield
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    P/E Ratio
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    Market Cap
                  </TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="right">
                    52W Range
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {reits.map((reit) => {
                  const isSelected = selectedREITs.has(reit.ticker);
                  const isFavorite = favorites.has(reit.ticker);
                  const range52w = reit.current_price && reit['52_week_low']
                    ? ((reit.current_price - reit['52_week_low']) / (reit['52_week_high'] - reit['52_week_low'])) * 100
                    : 50;

                  return (
                    <TableRow
                      key={reit.ticker}
                      hover
                      sx={{
                        bgcolor: isSelected ? alpha('#3b82f6', 0.05) : 'transparent',
                      }}
                    >
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => toggleSelection(reit.ticker)}
                          disabled={!isSelected && selectedREITs.size >= 5}
                          color={isSelected ? 'primary' : 'default'}
                        >
                          <CompareIcon />
                        </IconButton>
                      </TableCell>
                      <TableCell>
                        <IconButton
                          size="small"
                          onClick={() => toggleFavorite(reit.ticker)}
                          color={isFavorite ? 'warning' : 'default'}
                        >
                          {isFavorite ? <StarIcon /> : <StarBorderIcon />}
                        </IconButton>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={reit.ticker}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          {reit.company_name || reit.ticker}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {reit.industry || reit.sector}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatCurrency(reit.current_price)}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Stack alignItems="flex-end" spacing={0.5}>
                          <Stack direction="row" alignItems="center" spacing={0.5}>
                            {reit.price_change_pct !== null && reit.price_change_pct > 0 ? (
                              <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                            ) : (
                              <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                            )}
                            <Typography
                              variant="body2"
                              sx={{
                                fontWeight: 600,
                                color: getPerformanceColor(reit.price_change_pct),
                              }}
                            >
                              {reit.price_change_pct !== null
                                ? `${reit.price_change_pct > 0 ? '+' : ''}${reit.price_change_pct.toFixed(2)}%`
                                : '-'}
                            </Typography>
                          </Stack>
                          <Typography variant="caption" color="text.secondary">
                            {formatCurrency(reit.price_change)}
                          </Typography>
                        </Stack>
                      </TableCell>
                      <TableCell align="right">
                        <Typography
                          variant="body2"
                          sx={{
                            fontWeight: 600,
                            color: reit.dividend_yield ? '#10b981' : 'text.primary',
                          }}
                        >
                          {reit.dividend_yield ? formatPercent(reit.dividend_yield * 100) : '-'}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {reit.pe_ratio ? reit.pe_ratio.toFixed(2) : '-'}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatMarketCap(reit.market_cap)}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ width: 100 }}>
                          <Stack spacing={0.5}>
                            <LinearProgress
                              variant="determinate"
                              value={range52w}
                              sx={{
                                height: 6,
                                borderRadius: 3,
                                bgcolor: isDark ? '#374151' : '#e5e7eb',
                                '& .MuiLinearProgress-bar': {
                                  bgcolor:
                                    range52w > 75
                                      ? '#10b981'
                                      : range52w > 50
                                      ? '#3b82f6'
                                      : range52w > 25
                                      ? '#f59e0b'
                                      : '#ef4444',
                                },
                              }}
                            />
                            <Stack direction="row" justifyContent="space-between">
                              <Typography variant="caption" color="text.secondary">
                                {formatCurrency(reit['52_week_low'])}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {formatCurrency(reit['52_week_high'])}
                              </Typography>
                            </Stack>
                          </Stack>
                        </Box>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Treasury Rates */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Treasury Rates & Yields
          </Typography>
          <Grid container spacing={2}>
            {data.treasury_rates.rates.map((rate) => (
              <Grid item xs={12} sm={6} md={3} key={rate.symbol}>
                <Paper
                  sx={{
                    p: 2,
                    bgcolor: isDark
                      ? alpha('#1e293b', 0.5)
                      : alpha('#f8fafc', 0.8),
                  }}
                >
                  <Typography variant="caption" color="text.secondary">
                    {rate.name}
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 700, my: 0.5 }}>
                    {rate.rate?.toFixed(2)}%
                  </Typography>
                  <Stack direction="row" alignItems="center" spacing={0.5}>
                    {rate.change_pct !== null && rate.change_pct > 0 ? (
                      <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                    ) : (
                      <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                    )}
                    <Typography
                      variant="caption"
                      sx={{
                        fontWeight: 600,
                        color: getPerformanceColor(rate.change_pct),
                      }}
                    >
                      {rate.change_pct !== null ? `${rate.change_pct > 0 ? '+' : ''}${rate.change_pct.toFixed(2)}%` : '-'}
                    </Typography>
                  </Stack>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Info Alert */}
      <Alert severity="info" icon={<BankIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          How to use REIT Comparables:
        </Typography>
        <Typography variant="caption" component="div">
          • Compare your property's cap rate, NOI, and performance against public REITs
        </Typography>
        <Typography variant="caption" component="div">
          • Use dividend yields as a benchmark for expected property returns
        </Typography>
        <Typography variant="caption" component="div">
          • Monitor treasury rates as they affect REIT valuations and property cap rates
        </Typography>
        <Typography variant="caption" component="div">
          • Track market sentiment through indices (VIX shows volatility)
        </Typography>
        <Typography variant="caption" component="div" sx={{ mt: 1 }}>
          Data refreshes every 15 minutes. Click the refresh button for latest data.
        </Typography>
      </Alert>
    </Stack>
  );
};
