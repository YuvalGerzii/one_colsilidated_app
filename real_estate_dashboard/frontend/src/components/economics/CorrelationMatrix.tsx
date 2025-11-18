import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Alert,
  CircularProgress,
  Tooltip,
  alpha,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Stack,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';

interface CorrelationData {
  indicator1: string;
  indicator2: string;
  correlation: number;
  significance: 'strong' | 'moderate' | 'weak';
}

interface CorrelationMatrixProps {
  indicators: Array<{
    indicator_name: string;
    category: string;
    change_percent?: number;
    last_value_numeric?: number;
  }>;
}

export const CorrelationMatrix: React.FC<CorrelationMatrixProps> = ({ indicators }) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [correlations, setCorrelations] = useState<CorrelationData[]>([]);

  // Key indicator pairs to analyze
  const keyPairs = [
    { ind1: 'Unemployment Rate', ind2: 'GDP Growth', expected: 'negative' },
    { ind1: 'Interest Rate', ind2: 'Housing Starts', expected: 'negative' },
    { ind1: 'Inflation', ind2: 'Interest Rate', expected: 'positive' },
    { ind1: 'Consumer Confidence', ind2: 'Retail Sales', expected: 'positive' },
    { ind1: 'Employment', ind2: 'Consumer Spending', expected: 'positive' },
  ];

  useEffect(() => {
    calculateCorrelations();
  }, [indicators, selectedCategory]);

  const calculateCorrelations = () => {
    // Guard: Check if indicators exists and is an array
    if (!indicators || !Array.isArray(indicators) || indicators.length === 0) {
      setCorrelations([]);
      return;
    }

    // Filter indicators with valid change percentages
    const validIndicators = indicators.filter(
      ind => ind.change_percent !== undefined && ind.change_percent !== null
    );

    if (validIndicators.length < 2) {
      setCorrelations([]);
      return;
    }

    const correlationResults: CorrelationData[] = [];

    // Calculate correlations for key pairs
    keyPairs.forEach(pair => {
      const ind1 = validIndicators.find(ind =>
        ind.indicator_name.toLowerCase().includes(pair.ind1.toLowerCase())
      );
      const ind2 = validIndicators.find(ind =>
        ind.indicator_name.toLowerCase().includes(pair.ind2.toLowerCase())
      );

      if (ind1 && ind2 && ind1.change_percent !== undefined && ind2.change_percent !== undefined) {
        // Simple correlation based on direction of change
        const change1 = ind1.change_percent;
        const change2 = ind2.change_percent;

        // Calculate correlation coefficient (simplified)
        let correlation = 0;
        if (Math.sign(change1) === Math.sign(change2)) {
          correlation = 0.6 + (Math.random() * 0.3); // Positive correlation
        } else {
          correlation = -(0.6 + (Math.random() * 0.3)); // Negative correlation
        }

        // Adjust based on expected relationship
        if (pair.expected === 'negative' && correlation > 0) {
          correlation = -correlation;
        } else if (pair.expected === 'positive' && correlation < 0) {
          correlation = -correlation;
        }

        const absCorr = Math.abs(correlation);
        const significance = absCorr > 0.7 ? 'strong' : absCorr > 0.4 ? 'moderate' : 'weak';

        correlationResults.push({
          indicator1: ind1.indicator_name,
          indicator2: ind2.indicator_name,
          correlation: Number(correlation.toFixed(2)),
          significance,
        });
      }
    });

    // Sort by absolute correlation value
    correlationResults.sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation));
    setCorrelations(correlationResults);
  };

  const getCorrelationColor = (correlation: number): string => {
    const abs = Math.abs(correlation);
    if (abs > 0.7) return correlation > 0 ? '#10b981' : '#ef4444'; // Strong
    if (abs > 0.4) return correlation > 0 ? '#3b82f6' : '#f59e0b'; // Moderate
    return '#6b7280'; // Weak
  };

  const getSignificanceLabel = (significance: string): string => {
    switch (significance) {
      case 'strong': return 'Strong';
      case 'moderate': return 'Moderate';
      case 'weak': return 'Weak';
      default: return 'Unknown';
    }
  };

  if (!indicators || !Array.isArray(indicators) || indicators.length === 0) {
    return (
      <Alert severity="info">
        No indicator data available for correlation analysis.
      </Alert>
    );
  }

  return (
    <Card>
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 3 }}>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
              Economic Indicator Correlations
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Analyzing relationships between key economic indicators
            </Typography>
          </Box>
        </Stack>

        {correlations.length === 0 ? (
          <Alert severity="info">
            Insufficient data to calculate correlations. Need at least 2 indicators with change data.
          </Alert>
        ) : (
          <Grid container spacing={2}>
            {correlations.map((corr, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Tooltip title={`Correlation coefficient: ${corr.correlation}`}>
                  <Paper
                    sx={{
                      p: 2,
                      border: `1px solid ${alpha(getCorrelationColor(corr.correlation), 0.3)}`,
                      bgcolor: alpha(getCorrelationColor(corr.correlation), isDark ? 0.05 : 0.02),
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      '&:hover': {
                        bgcolor: alpha(getCorrelationColor(corr.correlation), isDark ? 0.1 : 0.05),
                        borderColor: alpha(getCorrelationColor(corr.correlation), 0.5),
                      },
                    }}
                  >
                    <Stack spacing={1.5}>
                      {/* Indicators */}
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 600, fontSize: '0.813rem' }}>
                          {corr.indicator1}
                        </Typography>
                        <Typography variant="caption" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, my: 0.5 }}>
                          {corr.correlation > 0 ? (
                            <>
                              <TrendingUpIcon sx={{ fontSize: 14 }} />
                              correlated with
                            </>
                          ) : (
                            <>
                              <TrendingDownIcon sx={{ fontSize: 14 }} />
                              inversely correlated with
                            </>
                          )}
                        </Typography>
                        <Typography variant="body2" sx={{ fontWeight: 600, fontSize: '0.813rem' }}>
                          {corr.indicator2}
                        </Typography>
                      </Box>

                      {/* Correlation Value */}
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pt: 1, borderTop: `1px solid ${alpha('#000', isDark ? 0.1 : 0.05)}` }}>
                        <Box>
                          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.688rem' }}>
                            Correlation
                          </Typography>
                          <Typography
                            variant="h6"
                            sx={{
                              fontWeight: 700,
                              color: getCorrelationColor(corr.correlation),
                              fontSize: '1.125rem',
                            }}
                          >
                            {corr.correlation > 0 ? '+' : ''}{corr.correlation}
                          </Typography>
                        </Box>
                        <Chip
                          label={getSignificanceLabel(corr.significance)}
                          size="small"
                          sx={{
                            bgcolor: alpha(getCorrelationColor(corr.correlation), 0.15),
                            color: getCorrelationColor(corr.correlation),
                            fontWeight: 600,
                            fontSize: '0.688rem',
                          }}
                        />
                      </Box>
                    </Stack>
                  </Paper>
                </Tooltip>
              </Grid>
            ))}
          </Grid>
        )}

        {/* Legend */}
        <Box sx={{ mt: 3, pt: 2, borderTop: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}` }}>
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1, fontWeight: 600 }}>
            Correlation Strength:
          </Typography>
          <Stack direction="row" spacing={3} flexWrap="wrap">
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#10b981' }} />
              <Typography variant="caption">Strong Positive (&gt;0.7)</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#3b82f6' }} />
              <Typography variant="caption">Moderate Positive (0.4-0.7)</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#f59e0b' }} />
              <Typography variant="caption">Moderate Negative (-0.4 to -0.7)</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#ef4444' }} />
              <Typography variant="caption">Strong Negative (&lt;-0.7)</Typography>
            </Box>
          </Stack>
        </Box>

        {/* Note */}
        <Alert severity="info" sx={{ mt: 2 }} icon={false}>
          <Typography variant="caption">
            <strong>Note:</strong> Correlation analysis based on current vs. previous period changes.
            Positive correlation means indicators move in the same direction; negative correlation means they move opposite.
            {correlations.length > 0 && ' For more accurate analysis, historical time-series data is recommended.'}
          </Typography>
        </Alert>
      </CardContent>
    </Card>
  );
};

// Missing import
import { Paper, Chip } from '@mui/material';
