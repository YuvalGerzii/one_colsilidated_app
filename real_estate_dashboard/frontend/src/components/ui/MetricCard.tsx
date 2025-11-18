/**
 * MetricCard Component - Reusable metric display card
 *
 * @version 1.1.0
 * @created 2025-11-15
 * @description Reusable component for displaying metrics with loading states, trend indicators, and hover animations
 */
import React from 'react';
import {
  Card,
  Stack,
  Typography,
  Box,
  Skeleton,
  alpha,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Remove as NeutralIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import { designTokens, alphaColor } from '../../theme/designTokens';

export interface MetricCardProps {
  label: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
  icon?: React.ElementType;
  color?: string;
  loading?: boolean;
  subtext?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  change,
  trend = 'neutral',
  icon: Icon,
  color = designTokens.colors.chart.blue,
  loading = false,
  subtext,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return designTokens.colors.semantic.success;
      case 'down':
        return designTokens.colors.semantic.error;
      default:
        return isDark ? 'rgba(255, 255, 255, 0.5)' : 'rgba(0, 0, 0, 0.5)';
    }
  };

  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon sx={{ fontSize: 16 }} />;
      case 'down':
        return <TrendingDownIcon sx={{ fontSize: 16 }} />;
      default:
        return <NeutralIcon sx={{ fontSize: 16 }} />;
    }
  };

  return (
    <Card
      sx={{
        p: 3,
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        background: isDark
          ? 'rgba(255, 255, 255, 0.03)'
          : 'rgba(255, 255, 255, 0.95)',
        border: `1px solid ${alphaColor(color, isDark ? 0.2 : 0.1)}`,
        borderRadius: designTokens.radius.lg,
        transition: `all ${designTokens.transitions.duration.base} ${designTokens.transitions.timing.inOut}`,
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: `0 12px 24px ${alphaColor(color, 0.15)}`,
          borderColor: alphaColor(color, 0.3),
        },
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '3px',
          background: `linear-gradient(90deg, ${color} 0%, ${alphaColor(color, 0.5)} 100%)`,
        },
      }}
    >
      <Stack spacing={2}>
        {/* Label with icon */}
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          {loading ? (
            <Skeleton variant="text" width="60%" height={20} />
          ) : (
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{
                fontWeight: designTokens.typography.fontWeight.semibold,
                textTransform: 'uppercase',
                letterSpacing: designTokens.typography.letterSpacing.wide,
                fontSize: designTokens.typography.fontSize.xs,
              }}
            >
              {label}
            </Typography>
          )}
          {Icon && !loading && (
            <Box
              sx={{
                width: 32,
                height: 32,
                borderRadius: designTokens.radius.md,
                background: alphaColor(color, 0.1),
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transition: `all ${designTokens.transitions.duration.fast} ${designTokens.transitions.timing.inOut}`,
                '.MuiCard-root:hover &': {
                  background: alphaColor(color, 0.15),
                  transform: 'scale(1.05)',
                },
              }}
            >
              <Icon sx={{ fontSize: 18, color }} />
            </Box>
          )}
          {loading && <Skeleton variant="circular" width={32} height={32} />}
        </Stack>

        {/* Value */}
        {loading ? (
          <Skeleton variant="text" width="70%" height={56} />
        ) : (
          <Typography
            variant="h3"
            sx={{
              fontWeight: designTokens.typography.fontWeight.extrabold,
              color,
              fontVariantNumeric: 'tabular-nums',
              lineHeight: designTokens.typography.lineHeight.none,
              fontSize: { xs: designTokens.typography.fontSize['3xl'], md: designTokens.typography.fontSize['4xl'] },
            }}
          >
            {value}
          </Typography>
        )}

        {/* Change indicator */}
        {(change || subtext) && (
          <Stack direction="row" alignItems="center" spacing={0.5}>
            {loading ? (
              <Skeleton variant="text" width="40%" height={20} />
            ) : (
              <>
                {change && (
                  <>
                    <Box sx={{ color: getTrendColor(), display: 'flex', alignItems: 'center' }}>
                      {getTrendIcon()}
                    </Box>
                    <Typography
                      variant="body2"
                      sx={{
                        fontWeight: designTokens.typography.fontWeight.semibold,
                        color: getTrendColor(),
                        fontVariantNumeric: 'tabular-nums',
                        fontSize: designTokens.typography.fontSize.sm,
                      }}
                    >
                      {change}
                    </Typography>
                  </>
                )}
                {subtext && (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{
                      fontSize: designTokens.typography.fontSize.xs,
                      ml: change ? 1 : 0,
                    }}
                  >
                    {subtext}
                  </Typography>
                )}
              </>
            )}
          </Stack>
        )}
      </Stack>
    </Card>
  );
};

export default MetricCard;
