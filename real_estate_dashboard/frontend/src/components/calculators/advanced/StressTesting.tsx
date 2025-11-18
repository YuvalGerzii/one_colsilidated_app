import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  alpha,
  Tooltip,
  Stack,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { useAppTheme } from '../../../contexts/ThemeContext';
import { StressTestResults } from '../../../types/advancedAnalysisTypes';
import { formatScenarioMetric, calculatePercentageChange, getScenarioRiskLevel } from '../../../utils/stressTestingCalculations';
import { getScenarioColor } from '../../../constants/stressTestingScenarios';

interface StressTestingProps {
  results: StressTestResults;
  title?: string;
  targetIrr?: number;
}

export const StressTesting: React.FC<StressTestingProps> = ({
  results,
  title = 'Stress Testing & Scenario Analysis',
  targetIrr = 0.15,
}) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  const getRiskColor = (riskLevel: string): string => {
    switch (riskLevel) {
      case 'excellent':
        return '#10b981';
      case 'strong':
        return '#3b82f6';
      case 'acceptable':
        return '#f59e0b';
      case 'weak':
        return '#f97316';
      case 'unacceptable':
        return '#ef4444';
      default:
        return '#6b7280';
    }
  };

  const getRiskIcon = (riskLevel: string) => {
    switch (riskLevel) {
      case 'excellent':
      case 'strong':
        return <CheckCircleIcon sx={{ fontSize: 18 }} />;
      case 'acceptable':
        return <WarningIcon sx={{ fontSize: 18 }} />;
      case 'weak':
      case 'unacceptable':
        return <CancelIcon sx={{ fontSize: 18 }} />;
      default:
        return <InfoIcon sx={{ fontSize: 18 }} />;
    }
  };

  const formatChangeCell = (current: number, base: number, isPositiveBetter: boolean = true) => {
    const change = calculatePercentageChange(current, base);
    const isPositive = change > 0;
    const isBetter = isPositiveBetter ? isPositive : !isPositive;

    return (
      <Stack direction="row" spacing={0.5} alignItems="center" justifyContent="flex-end">
        {Math.abs(change) > 0.1 && (
          <>
            {isBetter ? (
              <TrendingUpIcon sx={{ fontSize: 14, color: '#10b981' }} />
            ) : (
              <TrendingDownIcon sx={{ fontSize: 14, color: '#ef4444' }} />
            )}
            <Typography
              variant="caption"
              sx={{
                fontWeight: 600,
                color: isBetter ? '#10b981' : '#ef4444',
              }}
            >
              {isPositive ? '+' : ''}{change.toFixed(1)}%
            </Typography>
          </>
        )}
      </Stack>
    );
  };

  // Prepare tornado chart data
  const tornadoData = results.sensitivityRanking.map(item => ({
    name: item.displayName,
    lowImpact: ((item.lowValue - item.baseValue) / item.baseValue) * 100,
    highImpact: ((item.highValue - item.baseValue) / item.baseValue) * 100,
    impact: item.impact,
  }));

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" sx={{ fontWeight: 700, mb: 1 }}>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Test your investment's resilience under various market conditions and identify the most impactful variables.
        </Typography>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card
            elevation={0}
            sx={{
              border: `2px solid ${alpha('#3b82f6', 0.3)}`,
              bgcolor: isDark ? alpha('#3b82f6', 0.1) : alpha('#3b82f6', 0.05),
            }}
          >
            <CardContent>
              <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                Base Case IRR
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                {formatScenarioMetric(results.baseCase.irr, 'irr')}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            elevation={0}
            sx={{
              border: `2px solid ${alpha('#ef4444', 0.3)}`,
              bgcolor: isDark ? alpha('#ef4444', 0.1) : alpha('#ef4444', 0.05),
            }}
          >
            <CardContent>
              <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                Worst Case Scenario
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: '#ef4444', mb: 0.5 }}>
                {formatScenarioMetric(results.worstCase.irr, 'irr')}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {results.worstCase.scenarioName}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            elevation={0}
            sx={{
              border: `2px solid ${alpha('#10b981', 0.3)}`,
              bgcolor: isDark ? alpha('#10b981', 0.1) : alpha('#10b981', 0.05),
            }}
          >
            <CardContent>
              <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
                Best Case Scenario
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: 700, color: '#10b981', mb: 0.5 }}>
                {formatScenarioMetric(results.bestCase.irr, 'irr')}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {results.bestCase.scenarioName}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Scenario Comparison Table */}
      <Card elevation={0} sx={{ mb: 4 }}>
        <CardContent sx={{ p: 0 }}>
          <Box sx={{ px: 3, py: 2, borderBottom: `1px solid ${isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)}` }}>
            <Typography variant="h6" sx={{ fontWeight: 600 }}>
              Scenario Comparison
            </Typography>
          </Box>
          <TableContainer sx={{ maxHeight: 600 }}>
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 700, minWidth: 180 }}>Scenario</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 120 }}>IRR</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 120 }}>Change</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 140 }}>Equity Multiple</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 140 }}>Exit Value</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 120 }}>Year 1 NOI</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 120 }}>Cash Flow</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 700, minWidth: 100 }}>DSCR</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 700, minWidth: 100 }}>Status</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results.scenarios.map((scenario) => {
                  const riskLevel = getScenarioRiskLevel(scenario.irr, targetIrr);
                  const riskColor = getRiskColor(riskLevel);
                  const scenarioColor = getScenarioColor(scenario.scenarioId);
                  const isBaseCase = scenario.scenarioId === 'base-case';

                  return (
                    <TableRow
                      key={scenario.scenarioId}
                      sx={{
                        bgcolor: isBaseCase
                          ? isDark
                            ? alpha('#3b82f6', 0.05)
                            : alpha('#3b82f6', 0.03)
                          : 'transparent',
                        '&:hover': {
                          bgcolor: isDark ? alpha('#94a3b8', 0.05) : alpha('#0f172a', 0.03),
                        },
                      }}
                    >
                      <TableCell>
                        <Stack direction="row" spacing={1} alignItems="center">
                          <Box
                            sx={{
                              width: 4,
                              height: 32,
                              borderRadius: 2,
                              bgcolor: scenarioColor,
                            }}
                          />
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 600 }}>
                              {scenario.scenarioName}
                              {isBaseCase && (
                                <Chip
                                  label="Base"
                                  size="small"
                                  sx={{
                                    ml: 1,
                                    height: 20,
                                    fontSize: '0.7rem',
                                    bgcolor: alpha('#3b82f6', 0.2),
                                    color: '#3b82f6',
                                  }}
                                />
                              )}
                            </Typography>
                          </Box>
                        </Stack>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          {formatScenarioMetric(scenario.irr, 'irr')}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        {!isBaseCase && formatChangeCell(scenario.irr, results.baseCase.irr, true)}
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatScenarioMetric(scenario.equityMultiple, 'multiple')}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatScenarioMetric(scenario.exitValue, 'currency')}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatScenarioMetric(scenario.noi, 'currency')}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {formatScenarioMetric(scenario.cashFlow, 'currency')}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Typography variant="body2">
                          {scenario.dscr.toFixed(2)}x
                        </Typography>
                      </TableCell>
                      <TableCell align="center">
                        <Tooltip title={riskLevel.toUpperCase()} arrow>
                          <Chip
                            icon={getRiskIcon(riskLevel)}
                            label={riskLevel}
                            size="small"
                            sx={{
                              bgcolor: alpha(riskColor, 0.15),
                              color: riskColor,
                              fontWeight: 600,
                              textTransform: 'capitalize',
                              '& .MuiChip-icon': { color: riskColor },
                            }}
                          />
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Tornado Chart - Sensitivity Ranking */}
      <Card elevation={0}>
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
            Sensitivity Analysis - Tornado Chart
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Shows how changes in each variable impact IRR. Longer bars indicate higher sensitivity.
          </Typography>
          <Box sx={{ height: 400 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={tornadoData}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 120, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke={isDark ? alpha('#94a3b8', 0.1) : alpha('#0f172a', 0.1)} />
                <XAxis
                  type="number"
                  stroke={isDark ? '#94a3b8' : '#64748b'}
                  tickFormatter={(value) => `${value.toFixed(0)}%`}
                />
                <YAxis type="category" dataKey="name" stroke={isDark ? '#94a3b8' : '#64748b'} width={110} />
                <RechartsTooltip
                  formatter={(value: number) => `${value.toFixed(2)}%`}
                  contentStyle={{
                    backgroundColor: isDark ? '#1e293b' : '#ffffff',
                    border: `1px solid ${isDark ? '#334155' : '#e2e8f0'}`,
                    borderRadius: 8,
                  }}
                />
                <ReferenceLine x={0} stroke={isDark ? '#94a3b8' : '#64748b'} strokeWidth={2} />
                <Bar dataKey="lowImpact" fill="#ef4444" stackId="stack" />
                <Bar dataKey="highImpact" fill="#10b981" stackId="stack" />
              </BarChart>
            </ResponsiveContainer>
          </Box>
        </CardContent>
      </Card>

      {/* Info Card */}
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
              Understanding Stress Testing
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
              Stress testing reveals how your investment performs under adverse conditions. The{' '}
              <strong>tornado chart</strong> ranks variables by their impact on returns—focus on the most
              sensitive variables. A resilient investment maintains positive IRR even in the{' '}
              <strong>worst-case scenario</strong>.
            </Typography>
          </Box>
        </Box>
      </Card>
    </Box>
  );
};
