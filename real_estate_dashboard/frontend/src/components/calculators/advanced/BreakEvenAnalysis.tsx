import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  LinearProgress,
  Chip,
  Divider,
  alpha,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../../contexts/ThemeContext';
import { BreakEvenMetrics } from '../../../types/advancedAnalysisTypes';
import {
  formatBreakEvenMetric,
  getRiskLevel,
} from '../../../utils/breakEvenCalculations';

interface BreakEvenAnalysisProps {
  metrics: BreakEvenMetrics;
  title?: string;
}

export const BreakEvenAnalysis: React.FC<BreakEvenAnalysisProps> = ({
  metrics,
  title = 'Break-Even Analysis',
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const getStatusColor = (riskLevel: 'safe' | 'moderate' | 'risk'): string => {
    switch (riskLevel) {
      case 'safe':
        return '#10b981';
      case 'moderate':
        return '#f59e0b';
      case 'risk':
        return '#ef4444';
    }
  };

  const getStatusIcon = (riskLevel: 'safe' | 'moderate' | 'risk') => {
    switch (riskLevel) {
      case 'safe':
        return <CheckCircleIcon sx={{ fontSize: 20 }} />;
      case 'moderate':
        return <WarningIcon sx={{ fontSize: 20 }} />;
      case 'risk':
        return <TrendingDownIcon sx={{ fontSize: 20 }} />;
    }
  };

  const renderMetricCard = (
    label: string,
    breakEvenValue: number,
    currentValue: number | undefined,
    safetyMargin: number,
    type: 'percent' | 'currency' | 'years',
    description: string
  ) => {
    const riskLevel = getRiskLevel(safetyMargin);
    const statusColor = getStatusColor(riskLevel);
    const isValid = !isNaN(breakEvenValue) && isFinite(breakEvenValue);

    return (
      <Grid item xs={12} md={6}>
        <Card
          elevation={0}
          sx={{
            height: '100%',
            bgcolor: isDark ? 'rgba(30, 41, 59, 0.8)' : 'rgba(255, 255, 255, 0.9)',
            border: `2px solid ${alpha(statusColor, 0.3)}`,
            borderRadius: 3,
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'translateY(-4px)',
              boxShadow: isDark
                ? `0 12px 24px ${alpha(statusColor, 0.2)}`
                : `0 12px 24px ${alpha(statusColor, 0.15)}`,
            },
          }}
        >
          <CardContent sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
              <Box>
                <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 0.5 }}>
                  {label}
                </Typography>
                <Tooltip title={description} arrow>
                  <Box sx={{ display: 'inline-flex', alignItems: 'center', gap: 0.5 }}>
                    <Typography variant="h5" sx={{ fontWeight: 700, color: statusColor }}>
                      {isValid ? formatBreakEvenMetric(breakEvenValue, type) : 'N/A'}
                    </Typography>
                    <InfoIcon sx={{ fontSize: 16, color: 'text.secondary', cursor: 'pointer' }} />
                  </Box>
                </Tooltip>
              </Box>
              <Chip
                icon={getStatusIcon(riskLevel)}
                label={riskLevel.toUpperCase()}
                size="small"
                sx={{
                  bgcolor: alpha(statusColor, 0.15),
                  color: statusColor,
                  fontWeight: 600,
                  '& .MuiChip-icon': { color: statusColor },
                }}
              />
            </Box>

            {isValid && currentValue !== undefined && (
              <>
                <Divider sx={{ my: 2 }} />
                <Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Current Value
                    </Typography>
                    <Typography variant="caption" sx={{ fontWeight: 600 }}>
                      {formatBreakEvenMetric(currentValue, type)}
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      Safety Margin
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {safetyMargin > 0 ? (
                        <TrendingUpIcon sx={{ fontSize: 14, color: '#10b981' }} />
                      ) : (
                        <TrendingDownIcon sx={{ fontSize: 14, color: '#ef4444' }} />
                      )}
                      <Typography
                        variant="caption"
                        sx={{
                          fontWeight: 700,
                          color: safetyMargin > 0 ? '#10b981' : '#ef4444',
                        }}
                      >
                        {safetyMargin > 0 ? '+' : ''}
                        {safetyMargin.toFixed(1)}%
                      </Typography>
                    </Box>
                  </Box>

                  <LinearProgress
                    variant="determinate"
                    value={Math.min(Math.max((safetyMargin / 50) * 100 + 50, 0), 100)}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      bgcolor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)',
                      '& .MuiLinearProgress-bar': {
                        bgcolor: statusColor,
                        borderRadius: 4,
                      },
                    }}
                  />

                  <Typography
                    variant="caption"
                    sx={{
                      display: 'block',
                      mt: 1,
                      color: 'text.secondary',
                      fontStyle: 'italic',
                    }}
                  >
                    {description}
                  </Typography>
                </Box>
              </>
            )}

            {!isValid && (
              <Typography variant="body2" color="warning.main" sx={{ mt: 2, fontStyle: 'italic' }}>
                Break-even cannot be achieved within reasonable parameters
              </Typography>
            )}
          </CardContent>
        </Card>
      </Grid>
    );
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Analyze the minimum performance thresholds required to meet financial targets and assess your safety margins.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {metrics.occupancyBreakEven !== undefined && metrics.currentOccupancy !== undefined && (
          renderMetricCard(
            'Occupancy Break-Even',
            metrics.occupancyBreakEven,
            metrics.currentOccupancy,
            metrics.safetyMargins.occupancy,
            'percent',
            'Minimum occupancy rate needed to cover debt service payments'
          )
        )}

        {metrics.rentBreakEven !== undefined && metrics.currentRent !== undefined && (
          renderMetricCard(
            'Rent Break-Even',
            metrics.rentBreakEven,
            metrics.currentRent,
            metrics.safetyMargins.rent,
            'currency',
            'Minimum rent per unit/room needed to achieve your target IRR'
          )
        )}

        {metrics.exitCapBreakEven !== undefined && metrics.currentExitCap !== undefined && (
          renderMetricCard(
            'Exit Cap Rate Break-Even',
            metrics.exitCapBreakEven,
            metrics.currentExitCap,
            metrics.safetyMargins.exitCap,
            'percent',
            'Maximum exit cap rate that still provides positive returns'
          )
        )}

        {metrics.yearsToBreakEven !== undefined && !isNaN(metrics.yearsToBreakEven) && (
          <Grid item xs={12} md={6}>
            <Card
              elevation={0}
              sx={{
                height: '100%',
                bgcolor: isDark ? 'rgba(30, 41, 59, 0.8)' : 'rgba(255, 255, 255, 0.9)',
                border: `2px solid ${isDark ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)'}`,
                borderRadius: 3,
                transition: 'all 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: isDark
                    ? '0 12px 24px rgba(59, 130, 246, 0.2)'
                    : '0 12px 24px rgba(59, 130, 246, 0.15)',
                },
              }}
            >
              <CardContent sx={{ p: 3 }}>
                <Typography variant="subtitle2" sx={{ color: 'text.secondary', mb: 0.5 }}>
                  Time to Break-Even
                </Typography>
                <Typography variant="h5" sx={{ fontWeight: 700, color: '#3b82f6', mb: 2 }}>
                  {formatBreakEvenMetric(metrics.yearsToBreakEven, 'years')}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic' }}>
                  Time until cumulative cash flow turns positive
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Summary Card */}
      <Card
        elevation={0}
        sx={{
          mt: 4,
          p: 3,
          bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05),
          border: `2px solid ${isDark ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)'}`,
          borderRadius: 3,
        }}
      >
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'flex-start' }}>
          <InfoIcon sx={{ color: '#3b82f6', mt: 0.5 }} />
          <Box>
            <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
              Understanding Break-Even Analysis
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
              Break-even metrics show the minimum performance levels required to meet your financial goals.
              A <strong>safety margin above 20%</strong> indicates a safe buffer between current assumptions
              and break-even thresholds. Margins below 10% suggest higher risk and less room for unexpected changes.
            </Typography>
          </Box>
        </Box>
      </Card>
    </Box>
  );
};
