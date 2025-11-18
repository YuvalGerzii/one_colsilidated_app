import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Stack,
  Chip,
  CircularProgress,
  Alert,
  Paper,
  Grid,
  alpha,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ChartIcon,
  Place as PlaceIcon,
  CalendarToday as CalendarIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import { api } from '../../services/apiClient';

export type MarketScope = 'national' | 'state' | 'metro' | 'property' | 'portfolio';
export type TimeRange = 'current' | 'ytd' | '1y' | '3y' | '5y';

interface MarketSnapshotProps {
  scope: MarketScope;
  timeRange?: TimeRange;
  entity?: string; // Optional: property ID, state name, metro area, etc.
  compact?: boolean; // Compact view for sidebars
  workspaceFilter?: string; // Filter data by workspace (operate, invest, etc.)
}

interface MarketMetric {
  label: string;
  value: string | number;
  change?: number;
  trend?: 'up' | 'down' | 'neutral';
  unit?: string;
}

export const MarketSnapshot: React.FC<MarketSnapshotProps> = ({
  scope,
  timeRange = 'current',
  entity,
  compact = false,
  workspaceFilter,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<MarketMetric[]>([]);
  const [scopeLabel, setScopeLabel] = useState('');

  useEffect(() => {
    fetchMarketData();
  }, [scope, timeRange, entity, workspaceFilter]);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Determine scope label
      let label = '';
      switch (scope) {
        case 'national':
          label = 'United States';
          break;
        case 'state':
          label = entity || 'State';
          break;
        case 'metro':
          label = entity || 'Metro Area';
          break;
        case 'property':
          label = entity || 'Property';
          break;
        case 'portfolio':
          label = entity || 'Portfolio';
          break;
      }
      setScopeLabel(label);

      // Fetch relevant market data based on scope
      let marketData: MarketMetric[] = [];

      if (scope === 'national' || !entity) {
        // Fetch USA economics key indicators
        const response = await api.get('/market-intelligence/data/usa-economics/analysis');
        const data = response.data;

        if (data.key_indicators) {
          marketData = Object.entries(data.key_indicators).map(([key, value]: [string, any]) => ({
            label: key,
            value: value.value,
            change: value.change_percent,
            trend: value.change_percent > 0 ? 'up' : value.change_percent < 0 ? 'down' : 'neutral',
            unit: value.unit,
          }));
        }
      }

      // Add workspace-specific filters
      if (workspaceFilter) {
        marketData = filterMetricsByWorkspace(marketData, workspaceFilter);
      }

      setMetrics(marketData);
    } catch (error: any) {
      console.error('Error fetching market snapshot:', error);
      setError('Failed to load market data');
    } finally {
      setLoading(false);
    }
  };

  const filterMetricsByWorkspace = (metrics: MarketMetric[], workspace: string): MarketMetric[] => {
    // Filter metrics based on workspace context
    const workspaceRelevantMetrics: Record<string, string[]> = {
      operate: ['Unemployment Rate', 'Consumer Confidence', 'CPI', 'Housing Starts'],
      invest: ['GDP Growth', 'Interest Rate', 'Inflation Rate', 'Industrial Production'],
      capital: ['Interest Rate', 'Inflation Rate', 'GDP Growth'],
      analytics: ['GDP Growth', 'Unemployment Rate', 'Interest Rate', 'Consumer Confidence'],
    };

    const relevant = workspaceRelevantMetrics[workspace] || [];
    if (relevant.length === 0) return metrics;

    return metrics.filter(m => relevant.some(r => m.label.includes(r)));
  };

  if (loading) {
    return (
      <Card sx={{ height: compact ? 'auto' : '100%' }}>
        <CardContent>
          <Box sx={{ textAlign: 'center', py: compact ? 2 : 4 }}>
            <CircularProgress size={compact ? 32 : 48} />
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
              Loading market data...
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ height: compact ? 'auto' : '100%' }}>
        <CardContent>
          <Alert severity="warning" icon={<InfoIcon />}>
            {error}
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      sx={{
        height: compact ? 'auto' : '100%',
        background: isDark
          ? 'linear-gradient(135deg, rgba(15, 20, 25, 0.6) 0%, rgba(15, 20, 25, 0.8) 100%)'
          : 'linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.95) 100%)',
      }}
    >
      <CardContent>
        <Stack spacing={compact ? 2 : 3}>
          {/* Header */}
          <Stack direction="row" justifyContent="space-between" alignItems="center">
            <Stack direction="row" alignItems="center" spacing={1}>
              <ChartIcon sx={{ color: '#3b82f6', fontSize: compact ? 20 : 24 }} />
              <Typography variant={compact ? 'subtitle1' : 'h6'} sx={{ fontWeight: 600 }}>
                Market Snapshot
              </Typography>
            </Stack>
            <Chip
              label={timeRange.toUpperCase()}
              size="small"
              sx={{
                bgcolor: isDark ? 'rgba(59, 130, 246, 0.1)' : 'rgba(59, 130, 246, 0.05)',
                color: '#3b82f6',
                fontWeight: 600,
              }}
            />
          </Stack>

          {/* Scope Info */}
          <Paper
            sx={{
              p: compact ? 1.5 : 2,
              bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)',
            }}
          >
            <Stack direction="row" alignItems="center" spacing={1}>
              <PlaceIcon sx={{ fontSize: 16, color: 'text.secondary' }} />
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {scopeLabel}
              </Typography>
            </Stack>
          </Paper>

          {/* Metrics Grid */}
          <Stack spacing={compact ? 1 : 2}>
            {metrics.slice(0, compact ? 4 : 6).map((metric, index) => (
              <Paper
                key={index}
                sx={{
                  p: compact ? 1.5 : 2,
                  bgcolor: isDark ? 'rgba(255, 255, 255, 0.02)' : 'rgba(0, 0, 0, 0.01)',
                  border: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.05)}`,
                }}
              >
                <Stack spacing={0.5}>
                  <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'uppercase' }}>
                    {metric.label}
                  </Typography>
                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Typography variant={compact ? 'h6' : 'h5'} sx={{ fontWeight: 700 }}>
                      {metric.value} {metric.unit && <span style={{ fontSize: '0.7em' }}>{metric.unit}</span>}
                    </Typography>
                    {metric.change !== undefined && metric.change !== null && (
                      <Stack direction="row" alignItems="center" spacing={0.5}>
                        {metric.trend === 'up' ? (
                          <TrendingUpIcon sx={{ fontSize: compact ? 16 : 20, color: '#10b981' }} />
                        ) : metric.trend === 'down' ? (
                          <TrendingDownIcon sx={{ fontSize: compact ? 16 : 20, color: '#ef4444' }} />
                        ) : null}
                        <Typography
                          variant="caption"
                          sx={{
                            fontWeight: 600,
                            color: metric.trend === 'up' ? '#10b981' : metric.trend === 'down' ? '#ef4444' : 'text.secondary',
                          }}
                        >
                          {metric.change > 0 ? '+' : ''}
                          {metric.change.toFixed(2)}%
                        </Typography>
                      </Stack>
                    )}
                  </Stack>
                </Stack>
              </Paper>
            ))}
          </Stack>

          {/* View Full Link */}
          {compact && (
            <Typography
              variant="caption"
              sx={{
                color: '#3b82f6',
                cursor: 'pointer',
                textAlign: 'center',
                '&:hover': { textDecoration: 'underline' }
              }}
              onClick={() => window.location.href = '/market-intelligence'}
            >
              View Full Market Intelligence →
            </Typography>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};
