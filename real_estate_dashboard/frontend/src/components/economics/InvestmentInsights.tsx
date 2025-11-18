/**
 * Investment Insights Component
 *
 * Provides actionable investment strategies and tips based on
 * current economic conditions and real estate market indicators.
 */

import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Stack,
  Chip,
  Paper,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  alpha,
} from '@mui/material';
import {
  Lightbulb as LightbulbIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon,
  Cancel as CancelIcon,
  Info as InfoIcon,
  Psychology as PsychologyIcon,
  AttachMoney as MoneyIcon,
  Home as HomeIcon,
  Business as BusinessIcon,
  ShowChart as ChartIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';

interface InvestmentInsightsProps {
  analysisData: {
    economic_health_score: number;
    health_rating: string;
    category_stats: Record<string, any>;
    key_indicators: Record<string, any>;
  };
}

interface Strategy {
  title: string;
  description: string;
  type: 'opportunity' | 'caution' | 'neutral';
  category: string;
  actionItems: string[];
}

export const InvestmentInsights: React.FC<InvestmentInsightsProps> = ({ analysisData }) => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';

  // Generate strategies based on economic data
  const generateStrategies = (): Strategy[] => {
    const strategies: Strategy[] = [];
    const { category_stats, key_indicators, economic_health_score } = analysisData;

    // Housing Market Analysis
    if (category_stats.housing) {
      const housingTrend = category_stats.housing.trend;
      const avgChange = category_stats.housing.avg_change_percent;

      if (avgChange > 5) {
        strategies.push({
          title: 'Hot Housing Market',
          description: 'Housing indicators show strong growth. Prices may be elevated.',
          type: 'caution',
          category: 'Housing',
          actionItems: [
            'Be cautious of overpaying in heated markets',
            'Focus on cash flow over appreciation',
            'Consider emerging markets with lower prices',
            'Negotiate aggressively on purchase price',
            'Factor in potential market correction',
          ],
        });
      } else if (avgChange < -2) {
        strategies.push({
          title: 'Cooling Housing Market',
          description: 'Housing indicators declining. Buyer opportunities may emerge.',
          type: 'opportunity',
          category: 'Housing',
          actionItems: [
            'Excellent time for buyer negotiations',
            'Look for motivated sellers',
            'Lock in low prices before rebound',
            'Consider fix-and-flip opportunities',
            'Build portfolio while prices are down',
          ],
        });
      }
    }

    // Interest Rate Analysis
    if (key_indicators['Interest Rate']) {
      const interestRate = parseFloat(key_indicators['Interest Rate'].value);
      const rateChange = key_indicators['Interest Rate'].change_percent || 0;

      if (interestRate > 5) {
        strategies.push({
          title: 'High Interest Rate Environment',
          description: `Current rate at ${interestRate}% impacts financing costs significantly.`,
          type: 'caution',
          category: 'Money',
          actionItems: [
            'Prioritize all-cash or high down payment deals',
            'Focus on properties with strong cash flow',
            'Consider seller financing options',
            'Look for assumable mortgages',
            'Refinance existing properties if possible',
          ],
        });
      } else if (interestRate < 4) {
        strategies.push({
          title: 'Favorable Financing Conditions',
          description: `Low interest rates at ${interestRate}% enhance deal economics.`,
          type: 'opportunity',
          category: 'Money',
          actionItems: [
            'Maximize leverage with low-cost debt',
            'Lock in long-term fixed rates',
            'Consider cash-out refinancing',
            'Scale portfolio acquisitions',
            'Invest in higher-value properties',
          ],
        });
      }
    }

    // Inflation Analysis
    if (key_indicators['Inflation Rate']) {
      const inflation = parseFloat(key_indicators['Inflation Rate'].value);

      if (inflation > 4) {
        strategies.push({
          title: 'High Inflation Environment',
          description: `Inflation at ${inflation}% erodes purchasing power but benefits real assets.`,
          type: 'opportunity',
          category: 'Prices',
          actionItems: [
            'Real estate is an inflation hedge',
            'Increase rents to match inflation',
            'Fixed-rate debt becomes cheaper over time',
            'Operating costs will rise - budget accordingly',
            'Hard assets outperform cash holdings',
          ],
        });
      }
    }

    // Employment Analysis
    if (key_indicators['Unemployment Rate']) {
      const unemployment = parseFloat(key_indicators['Unemployment Rate'].value);

      if (unemployment < 4) {
        strategies.push({
          title: 'Strong Employment Market',
          description: `Low unemployment at ${unemployment}% supports rental demand.`,
          type: 'opportunity',
          category: 'Labour',
          actionItems: [
            'Rental demand should remain strong',
            'Consider workforce housing investments',
            'Tenant quality likely to be high',
            'Rental rate growth opportunities',
            'Low default/eviction risk',
          ],
        });
      } else if (unemployment > 6) {
        strategies.push({
          title: 'Weakening Job Market',
          description: `Rising unemployment at ${unemployment}% may impact tenants.`,
          type: 'caution',
          category: 'Labour',
          actionItems: [
            'Screen tenants more rigorously',
            'Maintain larger cash reserves',
            'Consider rent concessions to retain tenants',
            'Focus on recession-resistant locations',
            'Diversify tenant base',
          ],
        });
      }
    }

    // GDP Analysis
    if (category_stats.gdp) {
      const gdpTrend = category_stats.gdp.trend;

      if (gdpTrend === 'bullish') {
        strategies.push({
          title: 'Growing Economy',
          description: 'Strong GDP growth supports real estate fundamentals.',
          type: 'opportunity',
          category: 'GDP',
          actionItems: [
            'Population growth drives housing demand',
            'Business expansion increases commercial demand',
            'Job creation supports rental markets',
            'Infrastructure investment benefits all sectors',
            'Consumer confidence boosts retail/hospitality',
          ],
        });
      }
    }

    // Overall Health Score Strategy
    if (economic_health_score > 75) {
      strategies.push({
        title: 'Strong Economic Environment',
        description: `Health score of ${economic_health_score} indicates robust conditions.`,
        type: 'opportunity',
        category: 'Overall',
        actionItems: [
          'Favorable conditions for acquisitions',
          'Consider more aggressive growth strategies',
          'Explore value-add opportunities',
          'Refinance to improve cash flow',
          'Expand into new markets',
        ],
      });
    } else if (economic_health_score < 50) {
      strategies.push({
        title: 'Economic Headwinds',
        description: `Health score of ${economic_health_score} suggests challenging environment.`,
        type: 'caution',
        category: 'Overall',
        actionItems: [
          'Preserve capital and maintain liquidity',
          'Focus on defensive positions',
          'Reduce leverage if possible',
          'Prepare for distressed opportunities',
          'Avoid speculative investments',
        ],
      });
    }

    return strategies;
  };

  const strategies = generateStrategies();

  // Categorize strategies
  const opportunities = strategies.filter((s) => s.type === 'opportunity');
  const cautions = strategies.filter((s) => s.type === 'caution');

  const getStrategyColor = (type: string) => {
    switch (type) {
      case 'opportunity':
        return '#10b981';
      case 'caution':
        return '#f59e0b';
      default:
        return '#3b82f6';
    }
  };

  const getStrategyIcon = (type: string) => {
    switch (type) {
      case 'opportunity':
        return <TrendingUpIcon />;
      case 'caution':
        return <WarningIcon />;
      default:
        return <InfoIcon />;
    }
  };

  return (
    <Stack spacing={4}>
      {/* Header */}
      <Card
        sx={{
          background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
          color: 'white',
        }}
      >
        <CardContent>
          <Stack direction="row" spacing={2} alignItems="center">
            <PsychologyIcon sx={{ fontSize: 48 }} />
            <Box>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>
                AI-Powered Investment Insights
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9, mt: 0.5 }}>
                Actionable strategies based on current economic conditions
              </Typography>
            </Box>
          </Stack>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', bgcolor: isDark ? 'rgba(16, 185, 129, 0.1)' : 'rgba(16, 185, 129, 0.05)' }}>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <CheckIcon sx={{ fontSize: 40, color: '#10b981' }} />
                <Box>
                  <Typography variant="h3" sx={{ fontWeight: 700, color: '#10b981' }}>
                    {opportunities.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Investment Opportunities
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%', bgcolor: isDark ? 'rgba(245, 158, 11, 0.1)' : 'rgba(245, 158, 11, 0.05)' }}>
            <CardContent>
              <Stack direction="row" spacing={2} alignItems="center">
                <WarningIcon sx={{ fontSize: 40, color: '#f59e0b' }} />
                <Box>
                  <Typography variant="h3" sx={{ fontWeight: 700, color: '#f59e0b' }}>
                    {cautions.length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Areas of Caution
                  </Typography>
                </Box>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Strategies */}
      <Grid container spacing={3}>
        {strategies.map((strategy, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card
              sx={{
                height: '100%',
                borderLeft: `4px solid ${getStrategyColor(strategy.type)}`,
              }}
            >
              <CardContent>
                <Stack spacing={2}>
                  {/* Header */}
                  <Stack direction="row" spacing={2} alignItems="flex-start">
                    <Box
                      sx={{
                        p: 1,
                        borderRadius: 2,
                        bgcolor: alpha(getStrategyColor(strategy.type), 0.1),
                        color: getStrategyColor(strategy.type),
                      }}
                    >
                      {getStrategyIcon(strategy.type)}
                    </Box>
                    <Box sx={{ flex: 1 }}>
                      <Stack direction="row" spacing={1} alignItems="center" sx={{ mb: 0.5 }}>
                        <Typography variant="h6" sx={{ fontWeight: 700 }}>
                          {strategy.title}
                        </Typography>
                        <Chip
                          label={strategy.category}
                          size="small"
                          sx={{
                            bgcolor: alpha(getStrategyColor(strategy.type), 0.1),
                            color: getStrategyColor(strategy.type),
                            fontWeight: 600,
                            fontSize: '0.7rem',
                          }}
                        />
                      </Stack>
                      <Typography variant="body2" color="text.secondary">
                        {strategy.description}
                      </Typography>
                    </Box>
                  </Stack>

                  <Divider />

                  {/* Action Items */}
                  <Box>
                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                      Action Items:
                    </Typography>
                    <List dense sx={{ py: 0 }}>
                      {strategy.actionItems.map((item, idx) => (
                        <ListItem key={idx} sx={{ py: 0.5, px: 0 }}>
                          <ListItemIcon sx={{ minWidth: 32 }}>
                            <Box
                              sx={{
                                width: 6,
                                height: 6,
                                borderRadius: '50%',
                                bgcolor: getStrategyColor(strategy.type),
                              }}
                            />
                          </ListItemIcon>
                          <ListItemText
                            primary={item}
                            primaryTypographyProps={{
                              variant: 'body2',
                              color: 'text.secondary',
                            }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Market-Specific Tips */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
            <LightbulbIcon sx={{ color: '#f59e0b' }} />
            Real Estate Investment Tips
          </Typography>
          <Grid container spacing={3}>
            {/* Residential */}
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 3,
                  height: '100%',
                  bgcolor: isDark ? 'rgba(59, 130, 246, 0.05)' : 'rgba(59, 130, 246, 0.02)',
                }}
              >
                <Stack spacing={2}>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <HomeIcon sx={{ color: '#3b82f6' }} />
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      Residential
                    </Typography>
                  </Stack>
                  <List dense>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Focus on employment hubs"
                        secondary="Areas with job growth = rental demand"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="1% Rule for cash flow"
                        secondary="Monthly rent ≥ 1% of purchase price"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Target 15%+ CoC return"
                        secondary="After all expenses and debt service"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                  </List>
                </Stack>
              </Paper>
            </Grid>

            {/* Commercial */}
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 3,
                  height: '100%',
                  bgcolor: isDark ? 'rgba(16, 185, 129, 0.05)' : 'rgba(16, 185, 129, 0.02)',
                }}
              >
                <Stack spacing={2}>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <BusinessIcon sx={{ color: '#10b981' }} />
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      Commercial
                    </Typography>
                  </Stack>
                  <List dense>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Triple net leases preferred"
                        secondary="Tenant pays taxes, insurance, maintenance"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Long-term tenants = stability"
                        secondary="5-10 year leases reduce vacancy risk"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Location, location, location"
                        secondary="Visibility and accessibility drive value"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                  </List>
                </Stack>
              </Paper>
            </Grid>

            {/* Fix & Flip */}
            <Grid item xs={12} md={4}>
              <Paper
                sx={{
                  p: 3,
                  height: '100%',
                  bgcolor: isDark ? 'rgba(139, 92, 246, 0.05)' : 'rgba(139, 92, 246, 0.02)',
                }}
              >
                <Stack spacing={2}>
                  <Stack direction="row" spacing={1} alignItems="center">
                    <MoneyIcon sx={{ color: '#8b5cf6' }} />
                    <Typography variant="h6" sx={{ fontWeight: 700 }}>
                      Fix & Flip
                    </Typography>
                  </Stack>
                  <List dense>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="70% ARV Rule"
                        secondary="Max offer = (ARV × 0.70) - Repairs"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Speed is profit"
                        secondary="Every month holding costs you money"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemText
                        primary="Conservative ARV estimates"
                        secondary="Better to under-promise, over-deliver"
                        primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                    </ListItem>
                  </List>
                </Stack>
              </Paper>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Risk Factors */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
            <WarningIcon sx={{ color: '#ef4444' }} />
            Key Risk Factors to Monitor
          </Typography>
          <Grid container spacing={2}>
            {[
              {
                title: 'Interest Rate Risk',
                description: 'Rising rates increase financing costs and reduce property values',
                mitigation: 'Lock in fixed rates, focus on cash flow, reduce leverage',
              },
              {
                title: 'Market Cycle Risk',
                description: 'Real estate is cyclical - timing matters for returns',
                mitigation: 'Buy based on fundamentals, not speculation; hold long-term',
              },
              {
                title: 'Vacancy Risk',
                description: 'Empty units = no cash flow and ongoing expenses',
                mitigation: 'Prime locations, competitive pricing, excellent property management',
              },
              {
                title: 'Economic Recession',
                description: 'Downturn affects employment, rents, and property values',
                mitigation: 'Maintain cash reserves, diversify holdings, stress test deals',
              },
            ].map((risk, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Alert
                  severity="warning"
                  icon={<WarningIcon />}
                  sx={{
                    '.MuiAlert-message': { width: '100%' },
                  }}
                >
                  <Typography variant="subtitle2" sx={{ fontWeight: 700, mb: 0.5 }}>
                    {risk.title}
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    {risk.description}
                  </Typography>
                  <Typography variant="caption" sx={{ fontWeight: 600 }}>
                    Mitigation: {risk.mitigation}
                  </Typography>
                </Alert>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Economic Indicators to Watch */}
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
            <ChartIcon sx={{ color: '#3b82f6' }} />
            Key Economic Indicators for Real Estate Investors
          </Typography>
          <Grid container spacing={2}>
            {[
              {
                indicator: 'Federal Funds Rate',
                why: 'Directly impacts mortgage rates and financing costs',
                action: 'Rising = tighten underwriting, lock rates early',
              },
              {
                indicator: 'Unemployment Rate',
                why: 'Low unemployment = strong rental demand and tenant quality',
                action: 'Rising = focus on affordable housing, increase reserves',
              },
              {
                indicator: 'Housing Starts',
                why: 'Indicates new supply entering the market',
                action: 'High starts = potential oversupply, be selective',
              },
              {
                indicator: 'CPI / Inflation',
                why: 'Real estate hedge against inflation; rents typically rise',
                action: 'High inflation = raise rents, use fixed-rate debt',
              },
              {
                indicator: 'GDP Growth',
                why: 'Strong economy supports real estate fundamentals',
                action: 'Strong GDP = favorable for acquisitions and development',
              },
              {
                indicator: 'Consumer Confidence',
                why: 'Indicates willingness to spend and move for housing',
                action: 'Low confidence = expect slower sales, focus on rentals',
              },
            ].map((item, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Paper sx={{ p: 2, height: '100%' }}>
                  <Stack spacing={1}>
                    <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#3b82f6' }}>
                      {item.indicator}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      <strong>Why it matters:</strong> {item.why}
                    </Typography>
                    <Typography variant="caption" sx={{ fontStyle: 'italic' }}>
                      ▸ {item.action}
                    </Typography>
                  </Stack>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <Alert severity="info" icon={<InfoIcon />}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          Investment Disclaimer
        </Typography>
        <Typography variant="caption">
          These insights are generated from economic data analysis and are for informational purposes only.
          They do not constitute financial, investment, or legal advice. Always conduct thorough due diligence
          and consult with qualified professionals before making investment decisions.
        </Typography>
      </Alert>
    </Stack>
  );
};
