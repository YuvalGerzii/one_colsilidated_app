/**
 * Dashboard Metric Card Component
 * Displays key metrics with trend indicators and sparklines
 */
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Info,
  ArrowUpward,
  ArrowDownward,
} from '@mui/icons-material';

const MetricCard = ({
  title,
  value,
  unit = '',
  trend,
  trendValue,
  icon: Icon,
  color = 'primary',
  subtitle,
  actions,
  sparklineData,
}) => {
  const trendUp = trend === 'up' || trendValue > 0;
  const trendColor = trendUp ? 'success' : 'error';

  return (
    <Card
      sx={{
        height: '100%',
        position: 'relative',
        overflow: 'visible',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 6,
        },
      }}
    >
      <CardContent>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            mb: 2,
          }}
        >
          <Box sx={{ flex: 1 }}>
            <Typography
              variant="overline"
              sx={{
                color: 'text.secondary',
                fontWeight: 600,
                letterSpacing: 1,
                display: 'flex',
                alignItems: 'center',
                gap: 0.5,
              }}
            >
              {title}
              <Tooltip title={subtitle || 'More information'}>
                <Info sx={{ fontSize: 16, cursor: 'pointer' }} />
              </Tooltip>
            </Typography>
          </Box>

          {Icon && (
            <Box
              sx={{
                width: 48,
                height: 48,
                borderRadius: 2,
                bgcolor: `${color}.50`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: `${color}.main`,
              }}
            >
              <Icon sx={{ fontSize: 28 }} />
            </Box>
          )}
        </Box>

        {/* Value */}
        <Typography
          variant="h3"
          sx={{
            fontWeight: 700,
            color: 'text.primary',
            mb: 1,
            fontFamily: 'Poppins',
          }}
        >
          {value}
          {unit && (
            <Typography
              component="span"
              variant="h5"
              sx={{ color: 'text.secondary', ml: 0.5 }}
            >
              {unit}
            </Typography>
          )}
        </Typography>

        {/* Trend Indicator */}
        {(trend || trendValue !== undefined) && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              icon={trendUp ? <ArrowUpward /> : <ArrowDownward />}
              label={`${trendUp ? '+' : ''}${trendValue}%`}
              size="small"
              color={trendColor}
              sx={{
                fontWeight: 600,
                '& .MuiChip-icon': {
                  fontSize: 16,
                },
              }}
            />
            <Typography variant="caption" color="text.secondary">
              vs last period
            </Typography>
          </Box>
        )}

        {/* Sparkline placeholder */}
        {sparklineData && (
          <Box
            sx={{
              mt: 2,
              height: 40,
              display: 'flex',
              alignItems: 'flex-end',
              gap: 0.5,
            }}
          >
            {sparklineData.map((value, index) => (
              <Box
                key={index}
                sx={{
                  flex: 1,
                  height: `${(value / Math.max(...sparklineData)) * 100}%`,
                  bgcolor: `${color}.${trendUp ? '400' : '200'}`,
                  borderRadius: 0.5,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    bgcolor: `${color}.600`,
                  },
                }}
              />
            ))}
          </Box>
        )}

        {/* Additional Info */}
        {subtitle && !Icon && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            {subtitle}
          </Typography>
        )}

        {/* Actions */}
        {actions && (
          <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
            {actions}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default MetricCard;
