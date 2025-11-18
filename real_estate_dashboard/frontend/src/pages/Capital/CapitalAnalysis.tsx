/**
 * CapitalAnalysis Component - Capital & Structure workspace page
 *
 * @version 1.1.0
 * @updated 2025-11-15
 * @description Standalone page for financial/economic analysis with MetricCard integration
 * @changelog
 *   v1.1.0 - Integrated design tokens, added MetricCard components, cleaner hero header
 */
import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  Tabs,
  Tab,
  Stack,
  Grid,
  IconButton,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Timeline as TimelineIcon,
  ShowChart as ChartIcon,
  AccountBalance as BankIcon,
  AttachMoney as MoneyIcon,
  Assessment as AssessmentIcon,
  Refresh as RefreshIcon,
  Savings as SavingsIcon,
} from '@mui/icons-material';
import { useAppTheme } from '../../contexts/ThemeContext';
import {
  USAEconomicsAnalysis,
  EconomicForecast,
  HistoricalCharts,
  CorrelationMatrix,
  FinancialMarketsAnalytics,
} from '../../components/economics';
import { MetricCard } from '../../components/ui/MetricCard';
import { designTokens, alphaColor } from '../../theme/designTokens';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div role="tabpanel" hidden={value !== index} {...other}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const CAPITAL_TABS = [
  {
    id: 0,
    label: 'Economic Overview',
    icon: TrendingUpIcon,
    color: '#3b82f6',
    description: 'Real-time economic health and key indicators',
  },
  {
    id: 1,
    label: 'Financial Markets',
    icon: ChartIcon,
    color: '#10b981',
    description: 'Treasury yields, Fed policy, and market analytics',
  },
  {
    id: 2,
    label: 'Economic Forecasting',
    icon: TimelineIcon,
    color: '#8b5cf6',
    description: 'AI-powered predictions and trend analysis',
  },
  {
    id: 3,
    label: 'Historical Analysis',
    icon: AssessmentIcon,
    color: '#f59e0b',
    description: 'Multi-indicator historical trends',
  },
  {
    id: 4,
    label: 'Correlations',
    icon: ChartIcon,
    color: '#ef4444',
    description: 'Economic indicator relationships',
  },
];

export const CapitalAnalysis: React.FC = () => {
  const { theme } = useAppTheme();
  const isDark = theme === 'dark';
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const activeTabInfo = CAPITAL_TABS[activeTab];

  return (
    <Box sx={{ p: { xs: 3, md: 4 } }}>
      {/* Cleaner Hero Header */}
      <Box
        sx={{
          mb: 4,
          p: { xs: 3, md: 4 },
          borderRadius: designTokens.radius.xl,
          background: `linear-gradient(135deg, ${alphaColor(designTokens.colors.workspace.capital, 0.08)} 0%, ${alphaColor(designTokens.colors.workspace.capital, 0.03)} 100%)`,
          borderBottom: `1px solid ${alphaColor(designTokens.colors.workspace.capital, 0.1)}`,
        }}
      >
        <Stack direction="row" alignItems="center" spacing={3}>
          <Box
            sx={{
              width: 56,
              height: 56,
              borderRadius: designTokens.radius.lg,
              background: designTokens.colors.workspace.capital,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <MoneyIcon sx={{ fontSize: 28, color: 'white' }} />
          </Box>

          <Box flex={1}>
            <Typography
              variant="h3"
              sx={{
                fontWeight: designTokens.typography.fontWeight.bold,
                mb: 0.5,
                fontSize: { xs: designTokens.typography.fontSize['2xl'], md: designTokens.typography.fontSize['3xl'] },
              }}
            >
              Capital & Structure
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ fontSize: designTokens.typography.fontSize.sm }}
            >
              {activeTabInfo.description}
            </Typography>
          </Box>

          <Stack direction="row" spacing={1} sx={{ display: { xs: 'none', sm: 'flex' } }}>
            <IconButton
              size="small"
              sx={{
                color: designTokens.colors.workspace.capital,
                '&:hover': {
                  background: alphaColor(designTokens.colors.workspace.capital, 0.1),
                },
              }}
            >
              <RefreshIcon fontSize="small" />
            </IconButton>
          </Stack>
        </Stack>
      </Box>

      {/* Key Metrics Grid with new MetricCard component */}
      <Grid container spacing={{ xs: 2, md: 3 }} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Economic Health Score"
            value="82/100"
            change="+3.2%"
            trend="up"
            icon={AssessmentIcon}
            color={designTokens.colors.semantic.success}
            subtext="vs last quarter"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="Fed Funds Rate"
            value="5.33%"
            change="0.00%"
            trend="neutral"
            icon={BankIcon}
            color={designTokens.colors.chart.blue}
            subtext="unchanged"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="10Y Treasury"
            value="4.25%"
            change="-0.12%"
            trend="down"
            icon={SavingsIcon}
            color={designTokens.colors.chart.purple}
            subtext="vs last month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            label="GDP Growth"
            value="2.8%"
            change="+0.3%"
            trend="up"
            icon={TrendingUpIcon}
            color={designTokens.colors.chart.amber}
            subtext="annual rate"
          />
        </Grid>
      </Grid>

      {/* Cleaner Tab Navigation */}
      <Card sx={{ mb: 4, borderRadius: designTokens.radius.xl }}>
        <Tabs
          value={activeTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          allowScrollButtonsMobile
          sx={{
            px: 2,
            '& .MuiTab-root': {
              minHeight: 56,
              textTransform: 'none',
              fontSize: designTokens.typography.fontSize.sm,
              fontWeight: designTokens.typography.fontWeight.semibold,
              px: 3,
              py: 2,
              transition: `all ${designTokens.transitions.duration.base} ${designTokens.transitions.timing.inOut}`,
              '&.Mui-selected': {
                color: activeTabInfo.color,
              },
              '&:hover': {
                background: alphaColor(activeTabInfo.color, 0.04),
              },
            },
            '& .MuiTabs-indicator': {
              height: 3,
              borderRadius: '3px 3px 0 0',
              background: `linear-gradient(90deg, ${activeTabInfo.color} 0%, ${alphaColor(activeTabInfo.color, 0.7)} 100%)`,
            },
          }}
        >
          {CAPITAL_TABS.map((tab) => (
            <Tab
              key={tab.id}
              icon={<tab.icon sx={{ fontSize: 20 }} />}
              iconPosition="start"
              label={tab.label}
              title={tab.description}
            />
          ))}
        </Tabs>
      </Card>

      {/* Tab Content */}
      <Box>
        <TabPanel value={activeTab} index={0}>
          <USAEconomicsAnalysis />
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <FinancialMarketsAnalytics />
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <EconomicForecast />
        </TabPanel>

        <TabPanel value={activeTab} index={3}>
          <HistoricalCharts />
        </TabPanel>

        <TabPanel value={activeTab} index={4}>
          <CorrelationMatrix />
        </TabPanel>
      </Box>
    </Box>
  );
};

export default CapitalAnalysis;
