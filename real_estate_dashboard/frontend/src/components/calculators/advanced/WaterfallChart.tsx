import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Stack,
  Chip,
  alpha,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
  LabelList,
} from 'recharts';
import { useAppTheme } from '../../../contexts/ThemeContext';
import { WaterfallData } from '../../../types/advancedAnalysisTypes';

interface WaterfallChartProps {
  data: WaterfallData[];
  title: string;
  subtitle?: string;
  height?: number;
}

export const WaterfallChart: React.FC<WaterfallChartProps> = ({
  data,
  title,
  subtitle,
  height = 400,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  // Prepare data for Recharts
  const chartData = data.map((item, index) => {
    const isStart = item.category === 'start';
    const isTotal = item.category === 'total';
    const isIncrease = item.category === 'increase';
    const isDecrease = item.category === 'decrease';

    let base = 0;
    if (!isStart && !isTotal && index > 0) {
      base = data[index - 1].cumulative;
    }

    return {
      name: item.label,
      value: Math.abs(item.value),
      cumulative: item.cumulative,
      base: isTotal ? 0 : base,
      displayValue: item.value,
      color: item.color,
      category: item.category,
      tooltip: item.details?.tooltip || '',
      description: item.details?.description || '',
    };
  });

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
      notation: Math.abs(value) >= 1000000 ? 'compact' : 'standard',
      compactDisplay: 'short',
    }).format(value);
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (!active || !payload || !payload.length) return null;

    const data = payload[0].payload;

    return (
      <Box
        sx={{
          bgcolor: isDark ? '#1e293b' : '#ffffff',
          border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
          borderRadius: 2,
          p: 2,
          boxShadow: `0 4px 12px ${isDark ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.1)'}`,
        }}
      >
        <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 1 }}>
          {data.name}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {data.description}
        </Typography>
        <Stack spacing={0.5}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Amount:
            </Typography>
            <Typography variant="caption" sx={{ fontWeight: 600 }}>
              {formatCurrency(data.displayValue)}
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', gap: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Cumulative:
            </Typography>
            <Typography variant="caption" sx={{ fontWeight: 600 }}>
              {formatCurrency(data.cumulative)}
            </Typography>
          </Box>
        </Stack>
        {data.tooltip && (
          <Typography
            variant="caption"
            sx={{
              display: 'block',
              mt: 1,
              pt: 1,
              borderTop: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
              fontStyle: 'italic',
              color: 'text.secondary',
            }}
          >
            {data.tooltip}
          </Typography>
        )}
      </Box>
    );
  };

  // Calculate summary statistics
  const totalPositive = data
    .filter(d => d.category === 'increase' && d.value > 0)
    .reduce((sum, d) => sum + d.value, 0);

  const totalNegative = data
    .filter(d => d.category === 'decrease' || d.value < 0)
    .reduce((sum, d) => sum + Math.abs(d.value), 0);

  const netResult = data[data.length - 1]?.cumulative || 0;
  const equityInvested = Math.abs(data[0]?.value || 0);
  const multiple = equityInvested > 0 ? (netResult + equityInvested) / equityInvested : 0;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
          {title}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ bgcolor: isDark ? alpha('#10b981', 0.1) : alpha('#10b981', 0.05) }}>
            <CardContent sx={{ p: 2 }}>
              <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 0.5 }}>
                <TrendingUpIcon sx={{ fontSize: 16, color: '#10b981' }} />
                <Typography variant="caption" color="text.secondary">
                  Total Gains
                </Typography>
              </Stack>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#10b981' }}>
                {formatCurrency(totalPositive)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ bgcolor: isDark ? alpha('#ef4444', 0.1) : alpha('#ef4444', 0.05) }}>
            <CardContent sx={{ p: 2 }}>
              <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 0.5 }}>
                <TrendingDownIcon sx={{ fontSize: 16, color: '#ef4444' }} />
                <Typography variant="caption" color="text.secondary">
                  Total Costs
                </Typography>
              </Stack>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#ef4444' }}>
                {formatCurrency(totalNegative)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card
            elevation={0}
            sx={{
              bgcolor: isDark
                ? alpha(netResult >= 0 ? '#10b981' : '#ef4444', 0.1)
                : alpha(netResult >= 0 ? '#10b981' : '#ef4444', 0.05),
            }}
          >
            <CardContent sx={{ p: 2 }}>
              <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: 'block' }}>
                Net Result
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  fontWeight: 700,
                  color: netResult >= 0 ? '#10b981' : '#ef4444',
                }}
              >
                {formatCurrency(netResult)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card elevation={0} sx={{ bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05) }}>
            <CardContent sx={{ p: 2 }}>
              <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: 'block' }}>
                Equity Multiple
              </Typography>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                {multiple.toFixed(2)}x
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Waterfall Chart */}
      <Card elevation={0}>
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ height }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 80 }}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}
                  vertical={false}
                />
                <XAxis
                  dataKey="name"
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  fontSize={12}
                />
                <YAxis
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  tickFormatter={(value) => formatCurrency(value)}
                  fontSize={12}
                />
                <RechartsTooltip content={<CustomTooltip />} cursor={{ fill: isDark ? alpha('#94a3b8', 0.05) : alpha('#0f172a', 0.03) }} />
                <ReferenceLine y={0} stroke={isDark ? '#94a3b8' : '#64748b'} strokeWidth={2} />

                {/* Base bars (invisible, for stacking) */}
                <Bar dataKey="base" stackId="stack" fill="transparent" />

                {/* Value bars */}
                <Bar dataKey="value" stackId="stack" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                  <LabelList
                    dataKey="displayValue"
                    position="top"
                    formatter={(value: number) => formatCurrency(value)}
                    fontSize={11}
                    fontWeight={600}
                    fill={isDark ? '#e2e8f0' : '#0f172a'}
                  />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Box>

          {/* Legend */}
          <Stack direction="row" spacing={2} sx={{ mt: 3, flexWrap: 'wrap', gap: 1 }}>
            <Chip
              label="Starting Value"
              size="small"
              sx={{ bgcolor: alpha('#ef4444', 0.15), color: '#ef4444' }}
            />
            <Chip
              label="Increases"
              size="small"
              sx={{ bgcolor: alpha('#10b981', 0.15), color: '#10b981' }}
            />
            <Chip
              label="Decreases"
              size="small"
              sx={{ bgcolor: alpha('#f59e0b', 0.15), color: '#f59e0b' }}
            />
            <Chip
              label="Final Total"
              size="small"
              sx={{ bgcolor: alpha('#3b82f6', 0.15), color: '#3b82f6' }}
            />
          </Stack>
        </CardContent>
      </Card>

      {/* Info Card */}
      <Card
        elevation={0}
        sx={{
          mt: 3,
          p: 2,
          bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05),
          border: `1px solid ${isDark ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)'}`,
        }}
      >
        <Stack direction="row" spacing={1.5} alignItems="flex-start">
          <InfoIcon sx={{ color: '#3b82f6', fontSize: 20, mt: 0.2 }} />
          <Box>
            <Typography variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 0.5 }}>
              Reading the Waterfall
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ lineHeight: 1.6 }}>
              Each bar shows a component of value creation. Bars building upward represent gains, while bars going
              downward represent costs or losses. The final bar shows your total return.
            </Typography>
          </Box>
        </Stack>
      </Card>
    </Box>
  );
};
